from __future__ import annotations

import unittest

from fateweaver.card_candidates import score_card
from fateweaver.gameplay_models import CardCandidateContext, CardRule, CooldownCounter, Quest, QuestObjective, RepeatMemory, RunClock, RunState
from fateweaver.models import JsonMap


class GameplayP0CardRepetitionGateTests(unittest.TestCase):
    def test_frequency_penalty_is_deterministic(self) -> None:
        card = _card("generic_supply")
        state = _state(
            repeat_memory=RepeatMemory(
                card_counts=(CooldownCounter("generic_supply", 4),),
            ),
        )

        first = score_card(card, state, _context())
        second = score_card(card, state, _context())

        self.assertEqual(first.score, second.score)
        self.assertLessEqual(first.frequency_penalty, -8)

    def test_ontology_card_modifier_can_affect_card_score(self) -> None:
        card = _card("inspect_route", tags=("inspect", "route"))
        plain = score_card(card, _state(), _context())
        boosted = score_card(
            card,
            _state(),
            _context(
                ontology_inference={
                    "card_weight_modifiers": [
                        {"target": "card", "rule_id": "rule.inspect", "tags": ["inspect"], "amount": 20}
                    ]
                },
            ),
        )

        self.assertGreater(boosted.score, plain.score)
        self.assertEqual(3, boosted.ontology_modifier_applied)

    def test_ontology_modifier_does_not_bypass_card_gates(self) -> None:
        gated = _card("wrong_quest", quest_ids=("other_quest",), tags=("inspect",))

        candidate = score_card(
            gated,
            _state(),
            _context(
                ontology_inference={
                    "card_weight_modifiers": [
                        {"target": "card", "rule_id": "rule.inspect", "tags": ["inspect"], "amount": 99}
                    ]
                },
            ),
        )

        self.assertEqual("blocked", candidate.tier)
        self.assertEqual("unavailable_requirement", candidate.blocked_reason)

    def test_repeat_group_penalty_reduces_repeated_family(self) -> None:
        card = _card("resource_trade")
        state = _state(repeat_memory=RepeatMemory(repeat_group_counts=(CooldownCounter("storm_pass_probe", 3),)))

        candidate = score_card(card, state, _context(repeat_group="storm_pass_probe"))

        self.assertLessEqual(candidate.frequency_penalty, -6)


def _card(
    card_id: str,
    *,
    tags: tuple[str, ...] = (),
    quest_ids: tuple[str, ...] = (),
) -> CardRule:
    return CardRule(
        id=card_id,
        title=card_id,
        description="",
        slot_role="resource_alternative",
        base_weight=50,
        tier_hint="normal",
        tags=tags,
        regions=("forest",),
        result={},
        requires_item=None,
        requires_progress={},
        requires_status={},
        applies_to_storylet_tags=tags,
        applies_to_quest_objectives=(),
        progress_key="",
        weight_modifiers={},
        quest_ids=quest_ids,
    )


def _context(
    *,
    repeat_group: str = "",
    ontology_inference: JsonMap | None = None,
) -> CardCandidateContext:
    return CardCandidateContext(
        quest=_quest(),
        storylet_tags=("inspect", "route"),
        repeat_group=repeat_group,
        ontology_inference=ontology_inference or {},
    )


def _quest() -> Quest:
    return Quest(
        id="active_quest",
        title="active_quest",
        start_region="forest",
        max_days=7,
        max_turns=30,
        objectives=(
            QuestObjective(
                id="survive",
                objective_type="survive_expedition",
                target="health",
                required=True,
                count=0,
                value=1,
                progress_key="",
                failure_reason="",
                partial_reason="",
                score_key="",
                reward_weight=1,
            ),
        ),
        rewards={},
    )


def _state(*, repeat_memory: RepeatMemory | None = None) -> RunState:
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
        recent_event_ids=(),
        recent_presented_card_ids=(),
        selected_choice_history=(),
        repeat_memory=repeat_memory or RepeatMemory(),
        combo_used=False,
    )


if __name__ == "__main__":
    unittest.main()
