from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fateweaver.analyzer import analyze_logs
from fateweaver.logger import write_run_log


class LoggerAnalyzerTests(unittest.TestCase):
    def test_analyzes_core_loop_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logs_dir = Path(tmp)
            write_run_log(
                logs_dir,
                "scenario",
                42,
                1,
                {
                    "turns": [
                        {
                            "influenced_by": ["item:torch", "risk:high"],
                            "expected_risk": "high",
                            "regret_score": 4,
                        }
                    ],
                    "run_summary": {
                        "restart_intent_score": 4,
                        "player_woven_score": 5,
                        "run_failed": True,
                    },
                },
            )

            metrics = analyze_logs(logs_dir)

        self.assertEqual(1, metrics["meaningful_choice_count"])
        self.assertEqual(1, metrics["item_unlocked_choice_count"])
        self.assertEqual(1, metrics["bad_tradeoff_count"])
        self.assertEqual(1, metrics["run_failed_but_interesting_count"])

    def test_empty_log_directory_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                analyze_logs(Path(tmp))


if __name__ == "__main__":
    unittest.main()
