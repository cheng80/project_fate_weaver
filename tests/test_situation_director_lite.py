from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from random import Random

from fateweaver.gameplay_rules import select_storylet
from fateweaver.gameplay_rules import ontology_event_weight
from fateweaver.gameplay_models import RepeatMemory, RunClock, RunState
from fateweaver.models import Event


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class SituationDirectorLiteTests(unittest.TestCase):
    def test_ontology_weight_applies_only_after_quest_gate(self) -> None:
        selected = select_storylet(
            (
                _event("wrong_quest_storm", quest_ids=("other_quest",), danger_tags=("storm",), base_weight=1000),
                _event("right_quest_rest", quest_ids=("active_quest",), event_tags=("rest",), base_weight=1),
            ),
            _state(),
            Random(4),
            "active_quest",
            ontology_inference=_inference(("storm",), 999),
        )

        self.assertEqual("right_quest_rest", selected.id)

    def test_ontology_weight_does_not_bypass_cooldown(self) -> None:
        selected = select_storylet(
            (
                _event("cooldown_storm", danger_tags=("storm",), base_weight=1, cooldown_turns=3),
                _event("eligible_rest", event_tags=("rest",), base_weight=1),
            ),
            _state(recent_event_ids=("cooldown_storm",)),
            Random(4),
            "active_quest",
            ontology_inference=_inference(("storm",), 999),
        )

        self.assertEqual("eligible_rest", selected.id)

    def test_ontology_weight_can_bias_eligible_event(self) -> None:
        selected = select_storylet(
            (
                _event("plain_event", event_tags=("trade",), base_weight=1),
                _event("storm_event", danger_tags=("storm",), base_weight=1),
            ),
            _state(),
            Random(0),
            "active_quest",
            ontology_inference=_inference(("storm",), 200),
        )

        self.assertEqual("storm_event", selected.id)
        self.assertEqual(200, ontology_event_weight(selected, _inference(("storm",), 200)))

    def test_standard_run_logs_ontology_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    ".venv/bin/python",
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/standard_run_25_35_turn.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmpdir,
                    "--profile",
                    "balanced",
                ],
                cwd=PROJECT_ROOT,
                env={**os.environ, "PYTHONPATH": "src", "PYTHONDONTWRITEBYTECODE": "1"},
                check=True,
                capture_output=True,
                text=True,
            )
            log_path = next(Path(tmpdir).glob("*.json"))
            log = json.loads(log_path.read_text(encoding="utf-8"))

        first_turn = log["turns"][0]
        self.assertIn("ontology_inference", first_turn)
        self.assertIn("trace", first_turn["ontology_inference"])
        self.assertIn("ontology_weight_applied", first_turn)


def _event(
    event_id: str,
    *,
    event_tags: tuple[str, ...] = (),
    danger_tags: tuple[str, ...] = (),
    quest_ids: tuple[str, ...] = (),
    base_weight: int = 1,
    cooldown_turns: int | None = None,
) -> Event:
    return Event(
        id=event_id,
        name=event_id,
        description="",
        source_path=Path("unit"),
        region_tags=("forest",),
        event_tags=event_tags,
        danger_tags=danger_tags,
        storylet_tags=(),
        card_candidate_hints=(),
        cooldown_tags=(),
        repeat_group="",
        quest_ids=quest_ids,
        base_weight=base_weight,
        choices=(),
        max_occurrences_per_run=None,
        cooldown_turns=cooldown_turns,
        requires_item=None,
        requires_status={},
        requires_run_tag=None,
    )


def _state(recent_event_ids: tuple[str, ...] = ()) -> RunState:
    return RunState(
        clock=RunClock(day=1, turn=1, turns_today=0, time_of_day="morning", act=1, max_days=7, max_turns=30, turns_per_day=4),
        status={"health": 9, "food": 9, "money": 4, "reputation": 1, "curse": 1},
        inventory=(),
        run_tags=(),
        region="forest",
        quest_progress={},
        clues=(),
        omens=(),
        score={},
        next_event_tags=(),
        recent_event_ids=recent_event_ids,
        recent_presented_card_ids=(),
        selected_choice_history=(),
        repeat_memory=RepeatMemory(),
        combo_used=False,
    )


def _inference(tags: tuple[str, ...], amount: int) -> dict[str, object]:
    return {
        "event_weight_modifiers": [
            {"target": "event", "rule_id": "rule.unit", "tags": list(tags), "amount": amount}
        ],
        "situation_intents": ["intent.unit"],
        "trace": [{"rule_id": "rule.unit", "matched": True}],
    }


if __name__ == "__main__":
    unittest.main()
