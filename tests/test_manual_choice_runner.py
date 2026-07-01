from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import assert_never

from fateweaver.gameplay_p0_models import CardRule, QuestObjective


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
CHOICES = "1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1"
ALL_ONES = ",".join("1" for _ in range(25))


class ManualChoiceRunnerTests(unittest.TestCase):
    def test_manual_choice_sequence_generates_outputs_and_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES)

            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))
            summary = json.loads((output_dir / "manual_seed_202_summary.json").read_text(encoding="utf-8"))
            text_log = (output_dir / "manual_seed_202_text_mud.txt").read_text(encoding="utf-8")

        turns = payload["turns"]
        first_trace = trace[0]
        first_turn = turns[0]

        self.assertEqual(0, completed.returncode)
        self.assertTrue(payload["manual_choice_mode"])
        self.assertEqual("sequence", payload["choice_source"])
        self.assertEqual(len(turns), len(trace))
        self.assertGreaterEqual(len(turns), 1)
        self.assertEqual(first_turn["selected_cards"][0], first_trace["selected_card_id"])
        self.assertEqual(
            first_turn["presented_cards"][first_trace["selected_index"] - 1]["card_id"],
            first_trace["selected_card_id"],
        )
        self.assertEqual(first_trace["resource_delta"]["health"], first_turn["state_after"]["health"] - first_turn["state_before"]["health"])
        if len(turns) > 1:
            self.assertEqual(turns[0]["state_after"], turns[1]["state_before"])
        self.assertEqual(len(turns), summary["turn_count"])
        self.assertTrue(payload["stop_reason"])
        self.assertEqual(payload["stop_reason"], payload["manual_stop_reason"])
        self.assertEqual(summary["stop_reason"], summary["manual_stop_reason"])
        self.assertIn("manual_seed_202.json", completed.stdout)
        self.assertIn("[Run 종료]", text_log)

    def test_manual_choice_runner_marks_completed_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, ALL_ONES)
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            summary = json.loads((output_dir / "manual_seed_202_summary.json").read_text(encoding="utf-8"))

        self.assertEqual(0, completed.returncode)
        self.assertEqual("success", summary["result_type"])
        self.assertEqual("completed", payload["stop_reason"])
        self.assertEqual("completed", payload["manual_stop_reason"])
        self.assertEqual("completed", summary["stop_reason"])
        self.assertEqual("completed", summary["manual_stop_reason"])

    def test_completed_objective_refresh_filters_stale_quest_progress_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, ALL_ONES)
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))

        stale_turns = _stale_unscoped_quest_progress_turns(payload)

        self.assertEqual(0, completed.returncode)
        self.assertEqual([], stale_turns)
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        self.assertTrue(all(_unique_presented_cards(turn) for turn in payload["turns"]))

    def test_manual_choice_runner_stops_cleanly_at_max_turns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, CHOICES, "--max-turns", "5")

            self.assertEqual(0, completed.returncode)
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            summary = json.loads((output_dir / "manual_seed_202_summary.json").read_text(encoding="utf-8"))

        self.assertEqual(5, summary["turn_count"])
        self.assertEqual("max_turn_reached", payload["stop_reason"])
        self.assertEqual("max_turn_reached", payload["manual_stop_reason"])
        self.assertEqual("max_turn_reached", summary["stop_reason"])
        self.assertEqual("max_turn_reached", summary["manual_stop_reason"])

    def test_manual_choice_runner_stops_cleanly_when_sequence_exhausted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            completed = _run_manual(output_dir, "1")
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            summary = json.loads((output_dir / "manual_seed_202_summary.json").read_text(encoding="utf-8"))

        self.assertEqual(0, completed.returncode)
        self.assertEqual("choice_sequence_exhausted", payload["stop_reason"])
        self.assertEqual("choice_sequence_exhausted", payload["manual_stop_reason"])
        self.assertEqual("choice_sequence_exhausted", summary["stop_reason"])
        self.assertEqual("choice_sequence_exhausted", summary["manual_stop_reason"])

    def test_manual_choice_runner_rejects_invalid_choice_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            completed = _run_manual(Path(tmpdir), "4")

        self.assertNotEqual(0, completed.returncode)
        self.assertIn("invalid manual choice", completed.stderr)
        self.assertNotIn("MANUAL_RUN_JSON", completed.stdout)

    def test_manual_choice_file_mode_generates_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            choice_file = Path(tmpdir) / "choices.txt"
            choice_file.write_text("1\n2\n3\n", encoding="utf-8")
            completed = _run_manual_file(output_dir, choice_file)
            payload = json.loads((output_dir / "manual_seed_202.json").read_text(encoding="utf-8"))
            trace = json.loads((output_dir / "manual_seed_202_choice_trace.json").read_text(encoding="utf-8"))

        self.assertEqual(0, completed.returncode)
        self.assertEqual("file", payload["choice_source"])
        self.assertEqual([1, 2, 3], [entry["selected_index"] for entry in trace])

    def test_manual_choice_mode_does_not_change_autoplayer_standard_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            completed = subprocess.run(
                [
                    ".venv/bin/python",
                    "tools/console_simulator.py",
                    "--scenario",
                    str(SCENARIO_PATH),
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    str(tmpdir),
                    "--profile",
                    "balanced",
                ],
                cwd=PROJECT_ROOT,
                env=_env(),
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(next(Path(tmpdir).glob("*.json")).read_text(encoding="utf-8"))

        self.assertEqual(0, completed.returncode)
        self.assertEqual("success", payload["quest_report"]["result_type"])
        self.assertEqual("prepared_frontier_route", payload["quest_report"]["ending"]["id"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))


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


def _run_manual_file(output_dir: Path, choice_file: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            ".venv/bin/python",
            "tools/manual_choice_runner.py",
            "--scenario",
            str(SCENARIO_PATH),
            "--seed",
            "202",
            "--choice-file",
            str(choice_file),
            "--output-dir",
            str(output_dir),
        ],
        cwd=PROJECT_ROOT,
        env=_env(),
        check=False,
        capture_output=True,
        text=True,
    )


def _stale_unscoped_quest_progress_turns(payload: dict) -> list[dict]:
    from fateweaver.data_loader import load_project_data
    from fateweaver.gameplay_p0_data import load_foundation

    loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)
    foundation = load_foundation(PROJECT_ROOT, loaded.scenario.active_quest_id)
    card_by_id = {card.id: card for card in foundation.card_rules.cards}
    stale_turns: list[dict] = []
    previous_completed = False
    selected_card_ids: list[str] = []
    region = foundation.quest.start_region
    for turn in payload["turns"]:
        if previous_completed:
            stale_cards = [
                card["card_id"]
                for card in turn["presented_cards"]
                if _is_recent_unscoped_quest_progress_card(card_by_id[str(card["card_id"])], selected_card_ids)
            ]
            if stale_cards:
                stale_turns.append({"turn": int(turn["turn"]), "card_ids": stale_cards})
        region = str(turn["result"].get("move_to_region", region))
        selected_card_ids.extend(str(card_id) for card_id in turn["selected_cards"])
        previous_completed = _required_objectives_complete(foundation.quest.objectives, turn, region)
    return stale_turns


def _unique_presented_cards(turn: dict) -> bool:
    card_ids = [card["card_id"] for card in turn["presented_cards"]]
    return len(card_ids) == len(set(card_ids))


def _is_recent_unscoped_quest_progress_card(card: CardRule, selected_card_ids: list[str]) -> bool:
    return card.slot_role == "quest_progress" and not card.quest_ids and card.id in selected_card_ids[-3:]


def _required_objectives_complete(objectives: tuple[QuestObjective, ...], turn: dict, region: str) -> bool:
    return all(_objective_complete(objective, turn, region) for objective in objectives if objective.required)


def _objective_complete(objective: QuestObjective, turn: dict, region: str) -> bool:
    progress = turn["quest_progress"]
    status = turn["state_after"]
    clues = set(turn.get("clues", []))
    match objective.objective_type:
        case "collect_item":
            return int(progress.get(objective.target, 0)) >= objective.count
        case "return_to_region":
            return region == objective.target and int(progress.get(objective.progress_key, 0)) >= objective.value
        case "survive_expedition" | "keep_resource_at_least":
            return int(status.get(objective.target, 0)) >= objective.value
        case "discover_clue":
            return objective.target in clues
        case "optional_action":
            return int(progress.get(objective.progress_key, 0)) >= objective.value
        case unreachable:
            assert_never(unreachable)


def _env() -> dict[str, str]:
    return {**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"}


if __name__ == "__main__":
    unittest.main()
