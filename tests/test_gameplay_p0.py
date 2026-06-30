from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GameplayP0Tests(unittest.TestCase):
    def test_tutorial_herb_quest_cli_outputs_p0_run_contract(self) -> None:
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            # When
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "balanced",
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
        self.assertEqual(1, len(json_logs), result.stdout + result.stderr)
        self.assertEqual(1, len(text_logs), result.stdout + result.stderr)
        self.assertEqual("herb_gathering_tutorial", payload["quest"]["id"])
        self.assertEqual(3, payload["run_clock"]["max_days"])
        self.assertEqual(4, payload["run_clock"]["turns_per_day"])
        self.assertTrue(payload["turns"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        self.assertTrue(any(turn["multi_select"]["selected"] for turn in payload["turns"]))
        self.assertIn("quest_report", payload)
        self.assertIn(payload["quest_report"]["result_type"], {"success", "partial_success", "failure"})
        first_turn = payload["turns"][0]
        self.assertIn("run_clock", first_turn)
        self.assertIn("quest_progress", first_turn)
        self.assertIn("score", first_turn)
        self.assertIn("next_event_tags", first_turn)
        self.assertIn("[Day 1 / Morning / Turn 1]", text_log)
        self.assertIn("Quest: 약초 채집 의뢰", text_log)
        self.assertIn("카드:", text_log)
        self.assertIn("Quest Progress:", text_log)
        self.assertIn("Score Change:", text_log)
        self.assertIn("Quest Report:", text_log)

    def test_tutorial_herb_quest_cli_covers_success_partial_and_failure_outcomes(self) -> None:
        # Given
        cases = (
            ("data/scenarios/tutorial_herb_quest.yaml", "success"),
            ("data/scenarios/tutorial_herb_quest_partial.yaml", "partial_success"),
            ("data/scenarios/tutorial_herb_quest_failure.yaml", "failure"),
        )
        reports = {}

        for scenario_path, expected_result_type in cases:
            with self.subTest(scenario_path=scenario_path), tempfile.TemporaryDirectory() as tmp:
                # When
                result = subprocess.run(
                    [
                        sys.executable,
                        "tools/console_simulator.py",
                        "--scenario",
                        scenario_path,
                        "--seed",
                        "42",
                        "--runs",
                        "1",
                        "--logs",
                        tmp,
                        "--profile",
                        "balanced",
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
                self.assertEqual(1, len(json_logs), result.stdout + result.stderr)
                self.assertEqual(1, len(text_logs), result.stdout + result.stderr)
                self.assertEqual(expected_result_type, payload["quest_report"]["result_type"])
                self.assertIsInstance(payload["quest_report"]["score"], int)
                self.assertTrue(payload["quest_report"]["score_breakdown"])
                self.assertIn("completed_objectives", payload["quest_report"])
                self.assertIn("failed_objectives", payload["quest_report"])
                self.assertIn("review_text", payload["quest_report"])
                self.assertIn(f"결과 유형: {expected_result_type}", text_log)
                self.assertIn(payload["quest_report"]["review_text"], text_log)
                reports[expected_result_type] = payload["quest_report"]

        # Then
        self.assertGreater(int(reports["success"]["score"]), int(reports["partial_success"]["score"]))
        self.assertGreater(int(reports["partial_success"]["score"]), int(reports["failure"]["score"]))
        self.assertEqual(["collect_herbs", "report_to_apothecary"], reports["success"]["completed_objectives"])
        self.assertEqual([], reports["success"]["failed_objectives"])
        self.assertEqual(["collect_herbs"], reports["partial_success"]["completed_objectives"])
        self.assertEqual(["report_to_apothecary"], reports["partial_success"]["failed_objectives"])
        self.assertEqual([], reports["failure"]["completed_objectives"])
        self.assertIn("survive_expedition", reports["failure"]["failed_objectives"])
        self.assertTrue(reports["success"]["rewards"])
        self.assertEqual({}, reports["partial_success"]["rewards"])
        self.assertEqual({}, reports["failure"]["rewards"])
        self.assertLess(int(reports["failure"]["score_breakdown"]["outcome_adjustment"]), 0)


if __name__ == "__main__":
    unittest.main()
