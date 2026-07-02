from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
ALL_ONES = ",".join("1" for _ in range(25))


class QuestCompletionLifecycleTests(unittest.TestCase):
    def test_manual_run_completes_when_required_objectives_satisfied_before_min_turns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, ALL_ONES)
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))
            summary = json.loads((output_dir / "manual_seed_202_summary.json").read_text(encoding="utf-8"))

        last_trace = trace[-1]

        self.assertEqual(0, completed.returncode)
        self.assertEqual("success", summary["result_type"])
        self.assertLess(summary["turn_count"], 25)
        self.assertTrue(last_trace["quest_success"])
        self.assertFalse(last_trace["completion_blocked_by_min_turns"])
        self.assertTrue(last_trace["run_complete"])
        self.assertTrue(last_trace["no_next_quest"])

    def test_quest_success_grants_reward_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, ALL_ONES)
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        reward_entries = [entry for entry in trace if entry.get("reward_granted")]
        final_state = payload["run_summary"]["final_state"]
        reward_deltas = [entry["reward_delta"] for entry in reward_entries]

        self.assertEqual(0, completed.returncode)
        self.assertEqual(2, len(reward_entries))
        self.assertEqual([{"money": 2, "reputation": 1}, {"money": 2, "reputation": 1}], reward_deltas)
        self.assertEqual(reward_entries[-1]["resources_after"]["money"], final_state["money"])
        self.assertEqual(reward_entries[-1]["resources_after"]["reputation"], final_state["reputation"])
        self.assertEqual(0, sum(1 for entry in trace if entry.get("duplicate_reward_prevented")))


def _run_manual(output_dir: Path, choices: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            ".venv/bin/python",
            "tools/manual_choice_runner.py",
            "--scenario",
            str(SCENARIO_PATH),
            "--seed",
            "202",
            "--choices",
            choices,
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
