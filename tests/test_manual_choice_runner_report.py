from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.manual_choice_runner_report import render_trace_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"


class ManualChoiceRunnerReportTests(unittest.TestCase):
    def test_report_cli_renders_manual_trace_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            run = _run_manual(output_dir)
            report_path = output_dir / "manual_report.md"
            completed = subprocess.run(
                [
                    ".venv/bin/python",
                    "tools/manual_choice_runner_report.py",
                    "--run-json",
                    str(output_dir / "manual_seed_202.json"),
                    "--trace-json",
                    str(output_dir / "manual_seed_202_choice_trace.json"),
                    "--output",
                    str(report_path),
                ],
                cwd=PROJECT_ROOT,
                env=_env(),
                check=False,
                capture_output=True,
                text=True,
            )
            report = report_path.read_text(encoding="utf-8")

        self.assertEqual(0, run.returncode)
        self.assertEqual(0, completed.returncode)
        self.assertIn("# Manual Run Trace Report", report)
        self.assertIn("## Run Summary", report)
        self.assertIn("## Quest Onboarding", report)
        self.assertIn("## Turn Timeline", report)
        self.assertIn("## Quest Completion", report)
        self.assertIn("Reward Granted", report)
        self.assertIn("relevance=", report)
        self.assertIn("manual_stop_reason", report)

    def test_report_handles_missing_optional_trace_fields(self) -> None:
        report = render_trace_report(
            run_log={"seed": 202, "turns": [], "stop_reason": "completed", "manual_stop_reason": "completed"},
            trace=[{"turn": 1, "presented_card_ids": ["a", "b", "c"], "selected_index": 2}],
        )

        self.assertIn("unknown", report)
        self.assertIn("not_recorded", report)
        self.assertIn("selected slot 2", report)


def _run_manual(output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            ".venv/bin/python",
            "tools/manual_choice_runner.py",
            "--scenario",
            str(SCENARIO_PATH),
            "--seed",
            "202",
            "--choices",
            "1,2,3",
            "--max-turns",
            "3",
            "--output-dir",
            str(output_dir),
        ],
        cwd=PROJECT_ROOT,
        env=_env(),
        check=False,
        capture_output=True,
        text=True,
    )


def _env() -> dict[str, str]:
    return {**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}


if __name__ == "__main__":
    unittest.main()
