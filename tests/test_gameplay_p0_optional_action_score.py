from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


class GameplayP0OptionalActionScoreTests(unittest.TestCase):
    def test_optional_action_completed_when_help_card_selected(self) -> None:
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            # When
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest_optional_completed.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "curious_leaning",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            json_logs = list(Path(tmp).glob("run_*.json"))
            text_logs = list(Path(tmp).glob("run_*.txt"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
            text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        optional = _objective(payload["quest_report"], "help_injured_traveler")
        self.assertEqual("optional_action", optional["objective_type"])
        self.assertEqual("completed", optional["status"])
        self.assertGreater(int(optional["score_delta"]), 0)
        self.assertIn("help_injured_traveler", text_log)
        self.assertIn("성공", text_log)

    def test_objective_score_uses_score_rules_yaml(self) -> None:
        # Given
        raw = yaml.safe_load(Path("data/core/score_rules.yaml").read_text(encoding="utf-8"))
        objective_scoring = raw["score_rules"]["objective_scoring"]

        # When
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest_optional_completed.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "curious_leaning",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            json_logs = list(Path(tmp).glob("run_*.json"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        optional = _objective(payload["quest_report"], "help_injured_traveler")
        expected_optional_score = int(objective_scoring["completed_optional"])
        self.assertEqual(expected_optional_score, optional["score_delta"])
        self.assertGreaterEqual(payload["quest_report"]["score_breakdown"]["objective_completion"], expected_optional_score)


def _objective(report: dict, objective_id: str) -> dict:
    for objective in report["objective_results"]:
        if objective["objective_id"] == objective_id:
            return objective
    raise AssertionError(f"missing objective result: {objective_id}")
