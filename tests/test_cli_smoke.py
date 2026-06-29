from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliSmokeTests(unittest.TestCase):
    def test_validate_data_cli_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/validate_data.py", "--scenario", "data/scenarios/mvp0_console_test.yaml"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("VALIDATION: PASS", result.stdout)

    def test_validate_data_cli_reports_schema_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scenario = Path(tmp) / "bad.yaml"
            scenario.write_text("name: broken\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "tools/validate_data.py", "--scenario", str(scenario)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("VALIDATION: ERROR", result.stdout)

    def test_console_simulator_writes_temp_log_without_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/mvp0_console_test.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            logs = list(Path(tmp).glob("run_*.json"))
            text_logs = list(Path(tmp).glob("run_*.txt"))
            text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(logs), result.stdout + result.stderr)
        self.assertEqual(1, len(text_logs), result.stdout + result.stderr)
        self.assertIn("[Run 시작]", text_log)
        self.assertIn("장소:", text_log)
        self.assertIn("선택:", text_log)
        self.assertIn("위험/보상 판단:", text_log)
        self.assertIn("상태 변화:", text_log)
        self.assertIn("아이템/단서/징조 영향:", text_log)
        self.assertIn("다음 사건 변화:", text_log)
        self.assertIn("[Run 종료]", text_log)

    def test_console_simulator_accepts_balanced_profile_and_logs_weighted_score(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/mvp0_console_test.yaml",
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
            logs = list(Path(tmp).glob("run_*.json"))

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(1, len(logs), result.stdout + result.stderr)
            payload = json.loads(logs[0].read_text(encoding="utf-8"))

        self.assertEqual("balanced", payload["profile"])
        reason = str(payload["turns"][0]["selected_choice_reason"])
        self.assertIn("profile", reason)
        self.assertIn("balanced", reason)
        self.assertIn("final_score", reason)
        self.assertIn("selected_choice_score", payload["turns"][0])

    def test_console_simulator_rejects_invalid_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/mvp0_console_test.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "reckless_ghost",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )

        combined_output = result.stdout + result.stderr
        self.assertNotEqual(0, result.returncode, combined_output)
        self.assertIn("profile", combined_output)
        self.assertNotIn("unrecognized arguments", combined_output)


if __name__ == "__main__":
    unittest.main()
