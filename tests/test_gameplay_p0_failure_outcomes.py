from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fateweaver.models import JsonMap


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GameplayP0FailureOutcomeTests(unittest.TestCase):
    def test_merchant_failure_objective_failed_is_alive(self) -> None:
        # Given / When
        payload = _run_scenario("data/scenarios/merchant_lost_pack_recovery_failure.yaml")
        report = payload["quest_report"]
        text_log = payload["_text_log"]

        # Then
        self.assertEqual("failure", report["result_type"])
        self.assertEqual("objective_failed", report["failure_kind"])
        self.assertEqual("alive", report["character_outcome"])
        self.assertIn("primary_objective_failed", report["failure_reasons"])
        self.assertNotIn("health_zero", report["failure_reasons"])
        self.assertIn("실패 종류: objective_failed", text_log)
        self.assertIn("캐릭터 결과: alive", text_log)

    def test_merchant_failure_health_zero_is_incapacitated(self) -> None:
        # Given / When
        payload = _run_scenario("data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml")
        report = payload["quest_report"]
        text_log = payload["_text_log"]

        # Then
        self.assertEqual("failure", report["result_type"])
        self.assertEqual("death_or_incapacitated", report["failure_kind"])
        self.assertEqual("incapacitated", report["character_outcome"])
        self.assertIn("health_zero", report["failure_reasons"])
        self.assertIn("primary_objective_failed", report["failure_reasons"])
        self.assertIn("실패 종류: death_or_incapacitated", text_log)
        self.assertIn("캐릭터 결과: incapacitated", text_log)

    def test_success_and_partial_keep_failure_taxonomy_fields(self) -> None:
        # Given
        cases = (
            ("data/scenarios/merchant_lost_pack_recovery.yaml", "success", "none", "alive"),
            ("data/scenarios/merchant_lost_pack_recovery_partial.yaml", "partial_success", "none", "alive"),
        )

        # When / Then
        for scenario_path, result_type, failure_kind, character_outcome in cases:
            report = _run_scenario(scenario_path)["quest_report"]
            self.assertEqual(result_type, report["result_type"])
            self.assertEqual(failure_kind, report["failure_kind"])
            self.assertEqual(character_outcome, report["character_outcome"])
            self.assertIn("failure_reasons", report)


def _run_scenario(scenario_path: str) -> JsonMap:
    with tempfile.TemporaryDirectory() as tmp:
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
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            text=True,
            timeout=15,
        )
        json_logs = list(Path(tmp).glob("run_*.json"))
        text_logs = list(Path(tmp).glob("run_*.txt"))
        payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
        payload["_text_log"] = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    if len(json_logs) != 1:
        raise AssertionError(result.stdout + result.stderr)
    if len(text_logs) != 1:
        raise AssertionError(result.stdout + result.stderr)
    return payload


if __name__ == "__main__":
    unittest.main()
