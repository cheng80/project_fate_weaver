from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from fateweaver.data_loader import load_project_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"


class QuestSequenceTransitionTests(unittest.TestCase):
    def test_standard_run_defines_minimum_two_quest_sequence(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)

        self.assertEqual(
            ("survive_the_storm_pass", "hidden_grove_discovery"),
            loaded.scenario.quest_sequence,
        )

    def test_goal_focused_manual_run_transitions_to_next_quest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual_agent(output_dir)
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))

        self.assertEqual(0, completed.returncode, completed.stderr)
        transitions = [entry for entry in trace if entry.get("quest_transition")]
        self.assertEqual(1, len(transitions))
        transition = transitions[0]
        self.assertEqual("survive_the_storm_pass", transition["previous_quest_id"])
        self.assertEqual("hidden_grove_discovery", transition["next_quest_id"])
        self.assertTrue(transition["reward_granted"])
        self.assertTrue(transition["next_quest_onboarding"])
        self.assertEqual(
            ["find_hidden_grove", "map_grove_path", "report_hidden_grove", "survive_expedition"],
            transition["next_required_objective_ids"],
        )

        next_turn = next(entry for entry in trace if entry["turn"] > transition["turn"])
        self.assertEqual("hidden_grove_discovery", next_turn["active_quest_id"])
        self.assertTrue(
            all(
                "survive_the_storm_pass" not in relevance["card_quest_ids"]
                for relevance in next_turn["presented_card_relevance"]
            ),
        )

        final = trace[-1]
        self.assertEqual("hidden_grove_discovery", final["completed_quest_id"])
        self.assertTrue(final["no_next_quest"])
        self.assertTrue(final["run_complete"])
        self.assertEqual("success", payload["quest_report"]["result_type"])


def _run_manual_agent(output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            ".venv/bin/python",
            "tools/manual_choice_runner.py",
            "--scenario",
            str(SCENARIO_PATH),
            "--seed",
            "202",
            "--agent-policy",
            "goal_focused",
            "--max-turns",
            "10",
            "--output-dir",
            str(output_dir),
        ],
        cwd=PROJECT_ROOT,
        env={**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
        capture_output=True,
        text=True,
    )


if __name__ == "__main__":
    unittest.main()
