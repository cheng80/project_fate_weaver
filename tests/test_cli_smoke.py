from __future__ import annotations

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
                text=True,
            )
            logs = list(Path(tmp).glob("run_*.json"))

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(logs))


if __name__ == "__main__":
    unittest.main()
