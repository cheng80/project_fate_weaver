from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.manual_choice_runner_agents import AgentDecisionContext, choose_agent_index, policy_ids


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"


class ManualChoiceRunnerBatchTests(unittest.TestCase):
    def test_subagent_policies_choose_valid_slots(self) -> None:
        context = AgentDecisionContext(
            presented_cards=(
                {
                    "card_id": "quest",
                    "slot_role": "quest_progress",
                    "result": {"quest_progress": {"x": 1}},
                    "influenced_by": ["progress:x"],
                    "expected_risk": "low",
                },
                {
                    "card_id": "risk",
                    "slot_role": "risk_discovery",
                    "result": {"score_changes": {"risk": 10}, "status": {"health": -1}},
                    "influenced_by": ["tag:risk"],
                    "expected_risk": "high",
                },
                {
                    "card_id": "safe",
                    "slot_role": "resource_alternative",
                    "result": {"status": {"food": 1, "health": 1}},
                    "influenced_by": ["tag:survival"],
                    "expected_risk": "low",
                },
            ),
            relevance=(
                {"card_id": "quest", "required_objective_linked": True, "off_quest_candidate": False, "relevance_reason": "required_objective"},
                {"card_id": "risk", "required_objective_linked": False, "off_quest_candidate": False, "relevance_reason": "storylet_context"},
                {"card_id": "safe", "required_objective_linked": False, "off_quest_candidate": False, "relevance_reason": "resource_or_safety"},
            ),
            selected_card_ids=("risk", "risk"),
            turn=1,
        )

        self.assertEqual(("goal_focused", "safety_first", "risk_seeking", "explorer", "contrarian"), policy_ids())
        self.assertEqual(1, choose_agent_index("goal_focused", context))
        self.assertEqual(3, choose_agent_index("safety_first", context))
        self.assertIn(choose_agent_index("risk_seeking", context), (1, 2, 3))
        self.assertIn(choose_agent_index("explorer", context), (1, 2, 3))
        self.assertIn(choose_agent_index("contrarian", context), (1, 2, 3))

    def test_batch_runner_writes_summary_and_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = subprocess.run(
                [
                    ".venv/bin/python",
                    "tools/manual_choice_runner_batch.py",
                    "--scenario",
                    str(SCENARIO_PATH),
                    "--seeds",
                    "202",
                    "--max-turns",
                    "2",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=PROJECT_ROOT,
                env=_env(),
                check=False,
                capture_output=True,
                text=True,
            )
            summary = json.loads((output_dir / "batch_summary.json").read_text(encoding="utf-8"))
            report = (output_dir / "batch_report.md").read_text(encoding="utf-8")

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(5, summary["total_runs"])
        self.assertEqual(5, len(summary["runs"]))
        self.assertIn("quest_completion_count", summary)
        self.assertIn("reward_granted_count", summary)
        self.assertIn("run_complete_count", summary)
        self.assertIn("stop_reason_counts", summary)
        self.assertIn("same_turn_duplicate_count", summary)
        self.assertIn("no_next_quest_count", summary)
        self.assertIn("reward_missing_after_success_count", summary)
        self.assertIn("duplicate_reward_detected_count", summary)
        self.assertIn("completed_quest_dragged_to_max_turn_count", summary)
        self.assertIn("seed_agent_matrix", summary)
        self.assertEqual(0, summary["completion_blocked_by_min_turns_count"])
        self.assertEqual({"goal_focused", "safety_first", "risk_seeking", "explorer", "contrarian"}, set(summary["agent_summary"]))
        self.assertIn("# Subagent Auto-Play Batch Report", report)
        self.assertIn("## Run Matrix", report)
        self.assertIn("stop reason counts", report)

    def test_batch_runner_accepts_seed_ranges_and_report_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "runs"
            report_path = Path(tmpdir) / "baseline.md"
            completed = subprocess.run(
                [
                    ".venv/bin/python",
                    "tools/manual_choice_runner_batch.py",
                    "--scenario",
                    str(SCENARIO_PATH),
                    "--seeds",
                    "202-203",
                    "--agents",
                    "goal_focused",
                    "--max-turns",
                    "2",
                    "--output-dir",
                    str(output_dir),
                    "--report-md",
                    str(report_path),
                ],
                cwd=PROJECT_ROOT,
                env=_env(),
                check=False,
                capture_output=True,
                text=True,
            )
            summary = json.loads((output_dir / "batch_summary.json").read_text(encoding="utf-8"))
            report = report_path.read_text(encoding="utf-8")

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual([202, 203], summary["seeds"])
        self.assertEqual(2, summary["total_runs"])
        self.assertIn("MANUAL_BATCH_REPORT_MD", completed.stdout)
        self.assertIn("## Quest Lifecycle Summary", report)


def _env() -> dict[str, str]:
    return {**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}


if __name__ == "__main__":
    unittest.main()
