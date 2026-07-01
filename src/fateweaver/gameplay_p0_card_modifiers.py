from __future__ import annotations

from typing import Final, assert_never

from fateweaver.gameplay_p0_models import CardCandidateContext, CardRule, CooldownCounter, RunState


DEFAULT_MODIFIERS: Final = {
    "quest_objective_match": 30,
    "storylet_tag_match": 20,
    "region_match": 10,
    "slot_role_bonus": 5,
    "storylet_hint_bonus": 25,
    "cooldown_tag_penalty": -15,
    "repeat_group_penalty": -30,
    "recent_repeat_penalty": -25,
    "frequency_penalty_per_seen": -6,
    "frequency_penalty_cap": -70,
    "repeat_group_frequency_penalty_per_seen": -3,
    "repeat_group_frequency_penalty_cap": -12,
    "fallback_overuse_penalty": -20,
    "ontology_card_modifier_cap": 3,
    "already_completed": -999,
    "unavailable": -999,
    "low_food_penalty": -10,
}


def modifier(card: CardRule, key: str) -> int:
    value = card.weight_modifiers.get(key)
    match value:
        case None:
            return DEFAULT_MODIFIERS[key]
        case bool():
            return DEFAULT_MODIFIERS[key]
        case int() | float() | str():
            return int(value)
        case list() | dict():
            return DEFAULT_MODIFIERS[key]
        case unreachable:
            assert_never(unreachable)


def candidate_frequency_penalty(card: CardRule, state: RunState, context: CardCandidateContext) -> int:
    card_count = _counter_value(state.repeat_memory.card_counts, card.id)
    penalty = max(
        modifier(card, "frequency_penalty_cap"),
        card_count * modifier(card, "frequency_penalty_per_seen"),
    )
    if context.repeat_group:
        group_count = _counter_value(state.repeat_memory.repeat_group_counts, context.repeat_group)
        penalty += max(
            modifier(card, "repeat_group_frequency_penalty_cap"),
            group_count * modifier(card, "repeat_group_frequency_penalty_per_seen"),
        )
    return penalty


def candidate_fallback_penalty(card: CardRule, state: RunState) -> int:
    if card.quest_ids:
        return 0
    return modifier(card, "fallback_overuse_penalty") if _counter_value(state.repeat_memory.card_counts, card.id) >= 3 else 0


def ontology_card_modifier(card: CardRule, context: CardCandidateContext) -> int:
    inference = context.ontology_inference or {}
    card_tags = {card.slot_role, *card.tags, *card.applies_to_storylet_tags, *card.applies_to_quest_objectives}
    total = 0
    for raw_modifier in inference.get("card_weight_modifiers", []):
        if not isinstance(raw_modifier, dict):
            continue
        tags = {str(tag) for tag in raw_modifier.get("tags", []) if isinstance(tag, str)}
        if card_tags & tags:
            total += int(raw_modifier.get("amount", 0))
    return min(modifier(card, "ontology_card_modifier_cap"), max(0, total))


def _counter_value(counters: tuple[CooldownCounter, ...], key: str) -> int:
    for counter in counters:
        if counter.key == key:
            return counter.remaining_turns
    return 0
