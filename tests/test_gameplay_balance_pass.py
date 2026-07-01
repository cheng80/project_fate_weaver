from __future__ import annotations

import unittest

from fateweaver.gameplay_p0_models import CardRule, ComboRule, RepeatMemory, RunClock, RunState
from fateweaver.gameplay_p0_rules import select_cards


class GameplayBalancePassTests(unittest.TestCase):
    def test_balanced_profile_uses_risk_discovery_after_progress_is_high(self) -> None:
        cards = _cards()

        selected, _combo = select_cards(cards, (), _state(), "balanced")

        self.assertEqual("risk_discovery", selected[0].slot_role)

    def test_balanced_profile_uses_resource_when_resources_are_low(self) -> None:
        cards = _cards()

        selected, _combo = select_cards(cards, (), _state(status={"food": 2, "health": 5, "money": 4}), "balanced")

        self.assertEqual("resource_alternative", selected[0].slot_role)

    def test_reward_progress_card_is_not_unconditional_when_progress_is_high(self) -> None:
        cards = _cards(progress_result={"status": {"money": 2, "reputation": 1}})

        selected, _combo = select_cards(cards, (), _state(), "balanced")

        self.assertNotEqual("quest_progress", selected[0].slot_role)

    def test_balance_selection_does_not_bypass_combo_rule(self) -> None:
        cards = _cards()
        combo = ComboRule(id="quest_risk_combo", cards=("quest_progress", "risk_discovery"), result={})

        selected, selected_combo = select_cards(cards, (combo,), _state(combo_used=False), "balanced")

        self.assertEqual(combo, selected_combo)
        self.assertEqual(("quest_progress", "risk_discovery"), tuple(card.id for card in selected))


def _cards(*, progress_result: dict[str, dict[str, int]] | None = None) -> tuple[CardRule, CardRule, CardRule]:
    return (
        _card("quest_progress", "quest_progress", progress_result or {"quest_progress": {"main": 1}}),
        _card("risk_discovery", "risk_discovery", {"status": {"curse": 1}, "gain_clues": ["risk"]}),
        _card("resource_alternative", "resource_alternative", {"status": {"food": 2}}),
    )


def _card(card_id: str, slot_role: str, result: dict[str, object]) -> CardRule:
    return CardRule(
        id=card_id,
        title=card_id,
        description="",
        slot_role=slot_role,
        base_weight=50,
        tier_hint="normal",
        tags=(),
        regions=("forest",),
        result=result,
        requires_item=None,
        requires_progress={},
        requires_status={},
        applies_to_storylet_tags=(),
        applies_to_quest_objectives=(),
        progress_key="",
        weight_modifiers={},
    )


def _state(
    *,
    status: dict[str, int] | None = None,
    combo_used: bool = True,
) -> RunState:
    return RunState(
        clock=RunClock(day=1, turn=1, turns_today=0, time_of_day="morning", act=1, max_days=7, max_turns=30, turns_per_day=4),
        status=status or {"health": 9, "food": 9, "money": 4, "reputation": 1},
        inventory=(),
        run_tags=(),
        region="forest",
        quest_progress={"main": 1, "side": 1, "clue": 1},
        clues=(),
        omens=(),
        score={},
        next_event_tags=(),
        recent_event_ids=(),
        recent_presented_card_ids=(),
        selected_choice_history=(),
        repeat_memory=RepeatMemory(),
        combo_used=combo_used,
    )


if __name__ == "__main__":
    unittest.main()
