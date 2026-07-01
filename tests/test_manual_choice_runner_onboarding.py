from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
CHOICES = "1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1"


class ManualChoiceRunnerOnboardingTests(unittest.TestCase):
    def test_quest_onboarding_trace_marks_active_quest_at_run_start(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES, "--max-turns", "1")
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        first_trace = trace[0]
        active_quest_id = _active_quest_id()

        self.assertEqual(0, completed.returncode)
        self.assertTrue(first_trace["quest_onboarding"])
        self.assertEqual("run_start", first_trace["onboarding_reason"])
        self.assertEqual(active_quest_id, first_trace["active_quest_id"])
        self.assertTrue(first_trace["active_quest_title"])

    def test_quest_onboarding_trace_exposes_required_objectives(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES, "--max-turns", "1")
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        first_trace = trace[0]

        self.assertEqual(0, completed.returncode)
        self.assertGreaterEqual(len(first_trace["required_objective_ids"]), 1)
        self.assertEqual(
            first_trace["required_objective_ids"],
            [objective["id"] for objective in first_trace["required_objectives"]],
        )
        self.assertTrue(all(objective["required"] for objective in first_trace["required_objectives"]))
        self.assertTrue(all("completed_after" in objective for objective in first_trace["required_objectives"]))

    def test_quest_onboarding_preserves_three_card_invariant_and_unique_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES, "--max-turns", "3")
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        self.assertEqual(0, completed.returncode)
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        self.assertTrue(all(_unique_presented_cards(turn) for turn in payload["turns"]))
        self.assertTrue(all(len(entry["presented_card_ids"]) == 3 for entry in trace))
        self.assertTrue(all(len(entry["presented_card_ids"]) == len(set(entry["presented_card_ids"])) for entry in trace))


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


def _active_quest_id() -> str:
    from fateweaver.data_loader import load_project_data

    loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)
    if loaded.scenario.active_quest_id is None:
        raise AssertionError("scenario must define active_quest_id")
    return loaded.scenario.active_quest_id


def _unique_presented_cards(turn: dict) -> bool:
    card_ids = [card["card_id"] for card in turn["presented_cards"]]
    return len(card_ids) == len(set(card_ids))


def _env() -> dict[str, str]:
    return {**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}


if __name__ == "__main__":
    unittest.main()
