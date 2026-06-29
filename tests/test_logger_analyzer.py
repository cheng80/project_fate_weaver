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
                            "selected_choice_id": "use_torch",
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
        self.assertEqual(1, metrics["choice_diversity_count"])
        self.assertEqual("use_torch", metrics["most_repeated_choice_id"])
        self.assertEqual(1, metrics["most_repeated_choice_count"])
        self.assertEqual(1.0, metrics["repeat_bias_ratio"])
        self.assertEqual(1, metrics["run_failed_but_interesting_count"])

    def test_empty_log_directory_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                analyze_logs(Path(tmp))

    def test_analyzes_metrics_by_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logs_dir = Path(tmp)
            write_run_log(
                logs_dir,
                "scenario",
                42,
                1,
                {
                    "profile": "balanced",
                    "turns": [
                        {
                            "selected_choice_id": "use_rope",
                            "influenced_by": ["item:rope"],
                            "expected_risk": "low",
                            "regret_score": 1,
                        }
                    ],
                    "run_summary": {
                        "restart_intent_score": 4,
                        "player_woven_score": 4,
                        "run_failed": False,
                    },
                },
            )
            write_run_log(
                logs_dir,
                "scenario",
                42,
                2,
                {
                    "profile": "greedy_leaning",
                    "turns": [
                        {
                            "selected_choice_id": "open_cache",
                            "influenced_by": [],
                            "expected_risk": "high",
                            "regret_score": 4,
                        }
                    ],
                    "run_summary": {
                        "restart_intent_score": 2,
                        "player_woven_score": 2,
                        "run_failed": False,
                    },
                },
            )

            metrics = analyze_logs(logs_dir)

        profile_metrics = metrics["profile_metrics"]
        self.assertIsInstance(profile_metrics, dict)
        self.assertEqual(1, profile_metrics["balanced"]["item_unlocked_choice_count"])
        self.assertEqual(1, profile_metrics["balanced"]["choice_diversity_count"])
        self.assertEqual("use_rope", profile_metrics["balanced"]["most_repeated_choice_id"])
        self.assertEqual(1.0, profile_metrics["balanced"]["repeat_bias_ratio"])
        self.assertEqual(1, profile_metrics["greedy_leaning"]["bad_tradeoff_count"])

    def test_analyzes_choice_diversity_and_repeat_bias_by_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            logs_dir = Path(tmp)
            write_run_log(
                logs_dir,
                "scenario",
                42,
                1,
                {
                    "profile": "balanced",
                    "turns": [
                        {"selected_choice_id": "use_whistle", "influenced_by": ["item:whistle"], "expected_risk": "low", "regret_score": 0},
                        {"selected_choice_id": "use_whistle", "influenced_by": ["item:whistle"], "expected_risk": "low", "regret_score": 0},
                        {"selected_choice_id": "mark_trail", "influenced_by": [], "expected_risk": "low", "regret_score": 0},
                    ],
                    "run_summary": {
                        "restart_intent_score": 3,
                        "player_woven_score": 3,
                        "run_failed": False,
                    },
                },
            )

            metrics = analyze_logs(logs_dir)

        balanced = metrics["profile_metrics"]["balanced"]
        self.assertEqual(2, balanced["choice_diversity_count"])
        self.assertEqual("use_whistle", balanced["most_repeated_choice_id"])
        self.assertEqual(2, balanced["most_repeated_choice_count"])
        self.assertEqual(0.67, balanced["repeat_bias_ratio"])


if __name__ == "__main__":
    unittest.main()
