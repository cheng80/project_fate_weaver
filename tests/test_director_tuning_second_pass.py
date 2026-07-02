from __future__ import annotations

import unittest
from pathlib import Path
from random import Random

from fateweaver.gameplay_models import CooldownCounter, RepeatMemory, RunClock, RunState
from fateweaver.gameplay_rules import director_event_score, select_storylet
from fateweaver.models import Event


class DirectorTuningSecondPassTests(unittest.TestCase):
    def test_next_event_tags_bonus_affects_event_score(self) -> None:
        state = _state(next_event_tags=("shelter", "storm"))
        plain = _event("plain", storylet_tags=("trade",), base_weight=4)
        matching = _event("matching", storylet_tags=("shelter", "storm"), base_weight=4)

        self.assertGreater(director_event_score(matching, state, _inference()), director_event_score(plain, state, _inference()))

    def test_situation_intent_rotation_penalizes_recent_repetition(self) -> None:
        state = _state(repeat_memory=RepeatMemory(recent_storylets=("recent", "recent", "recent")))
        repeated = _event("recent", storylet_tags=("test_survival",), base_weight=8)
        fresh = _event("fresh", storylet_tags=("test_survival",), base_weight=8)

        self.assertLess(director_event_score(repeated, state, _inference(("intent.test_survival",))), director_event_score(fresh, state, _inference(("intent.test_survival",))))

    def test_recent_repeat_group_penalty_affects_event_score(self) -> None:
        state = _state(repeat_memory=RepeatMemory(repeat_groups=(CooldownCounter("family", 2),)))
        repeated = _event("repeated", storylet_tags=("route",), repeat_group="family", base_weight=8)
        fresh = _event("fresh", storylet_tags=("route",), repeat_group="other", base_weight=8)

        self.assertLess(director_event_score(repeated, state, _inference()), director_event_score(fresh, state, _inference()))

    def test_clue_and_omen_followup_bonus_affects_matching_events(self) -> None:
        state = _state(clues=("storm_warning",), omens=("black_cloud",))
        clue = _event("clue", storylet_tags=("clue_followup",), base_weight=4)
        omen = _event("omen", storylet_tags=("omen", "escalate_risk"), base_weight=4)
        plain = _event("plain", storylet_tags=("route",), base_weight=4)

        self.assertGreater(director_event_score(clue, state, _inference()), director_event_score(plain, state, _inference()))
        self.assertGreater(director_event_score(omen, state, _inference()), director_event_score(plain, state, _inference()))

    def test_completed_objective_progress_event_penalty(self) -> None:
        state = _state(quest_progress={"storm_shelter_found": 1, "survival_route_secured": 1, "storm_pass_returned": 1})
        progress = _event("progress", storylet_tags=("test_survival", "unlock_route"), base_weight=8)
        return_event = _event("return", storylet_tags=("invite_return", "resolve_objective"), base_weight=8)

        self.assertGreater(director_event_score(return_event, state, _inference()), director_event_score(progress, state, _inference()))

    def test_director_tuning_does_not_bypass_quest_ids_gate(self) -> None:
        selected = select_storylet(
            (
                _event("wrong_quest", storylet_tags=("shelter",), quest_ids=("other",), base_weight=100),
                _event("right_quest", storylet_tags=("trade",), quest_ids=("active",), base_weight=1),
            ),
            _state(next_event_tags=("shelter",)),
            Random(0),
            "active",
            _inference(),
        )

        self.assertEqual("right_quest", selected.id)

    def test_director_tuning_does_not_bypass_requirements(self) -> None:
        selected = select_storylet(
            (
                _event("blocked", storylet_tags=("shelter",), requires_item="missing", base_weight=100),
                _event("eligible", storylet_tags=("trade",), base_weight=1),
            ),
            _state(next_event_tags=("shelter",)),
            Random(0),
            "active",
            _inference(),
        )

        self.assertEqual("eligible", selected.id)

    def test_director_tuning_is_deterministic(self) -> None:
        state = _state(next_event_tags=("shelter",), recent_event_ids=("old",))
        event = _event("candidate", storylet_tags=("shelter",), base_weight=5)

        self.assertEqual(director_event_score(event, state, _inference(("intent.shelter_search",))), director_event_score(event, state, _inference(("intent.shelter_search",))))


def _event(
    event_id: str,
    *,
    storylet_tags: tuple[str, ...] = (),
    event_tags: tuple[str, ...] = (),
    danger_tags: tuple[str, ...] = (),
    quest_ids: tuple[str, ...] = (),
    repeat_group: str = "",
    base_weight: int = 1,
    requires_item: str | None = None,
) -> Event:
    return Event(
        id=event_id,
        name=event_id,
        description="",
        source_path=Path("unit"),
        region_tags=("forest",),
        event_tags=event_tags,
        danger_tags=danger_tags,
        storylet_tags=storylet_tags,
        card_candidate_hints=(),
        cooldown_tags=(),
        repeat_group=repeat_group,
        quest_ids=quest_ids,
        base_weight=base_weight,
        choices=(),
        max_occurrences_per_run=None,
        cooldown_turns=None,
        requires_item=requires_item,
        requires_status={},
        requires_run_tag=None,
    )


def _state(
    *,
    next_event_tags: tuple[str, ...] = (),
    recent_event_ids: tuple[str, ...] = (),
    repeat_memory: RepeatMemory = RepeatMemory(),
    clues: tuple[str, ...] = (),
    omens: tuple[str, ...] = (),
    quest_progress: dict[str, int] | None = None,
) -> RunState:
    return RunState(
        clock=RunClock(day=1, turn=1, turns_today=0, time_of_day="morning", act=1, max_days=7, max_turns=30, turns_per_day=4),
        status={"health": 9, "food": 9, "money": 4, "reputation": 1, "curse": 1},
        inventory=(),
        run_tags=(),
        region="forest",
        quest_progress={} if quest_progress is None else quest_progress,
        clues=clues,
        omens=omens,
        score={},
        next_event_tags=next_event_tags,
        recent_event_ids=recent_event_ids,
        recent_presented_card_ids=(),
        selected_choice_history=(),
        repeat_memory=repeat_memory,
        combo_used=False,
    )


def _inference(intents: tuple[str, ...] = ()) -> dict[str, object]:
    return {
        "event_weight_modifiers": [],
        "situation_intents": list(intents),
        "trace": [],
    }


if __name__ == "__main__":
    unittest.main()
