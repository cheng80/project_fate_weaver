from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
CHOICES = "1,2,3,1,2,3,1,2,3,1,2,3"


class ManualChoiceRunnerRelevanceTests(unittest.TestCase):
    def test_presented_cards_include_relevance_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES, "--max-turns", "3")
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        first_card = trace[0]["presented_card_relevance"][0]

        self.assertEqual(0, completed.returncode)
        self.assertEqual(trace[0]["presented_card_ids"][0], first_card["card_id"])
        self.assertEqual(trace[0]["active_quest_id"], first_card["active_quest_id"])
        self.assertEqual(trace[0]["required_objective_ids"], first_card["required_objective_ids"])
        self.assertIn("relevance_reason", first_card)
        self.assertIn("off_quest_candidate", first_card)

    def test_off_quest_cards_do_not_occupy_presented_majority(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES, "--max-turns", "12")
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        noisy_turns = [
            entry["turn"]
            for entry in trace
            if sum(1 for card in entry["presented_card_relevance"] if card["off_quest_candidate"]) >= 2
        ]

        self.assertEqual(0, completed.returncode)
        self.assertEqual([], noisy_turns)


def _run_manual(output_dir: Path, choices: str, *extra_args: str) -> subprocess.CompletedProcess[str]:
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
            *extra_args,
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
