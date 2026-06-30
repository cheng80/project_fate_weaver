from __future__ import annotations

from dataclasses import dataclass
from typing import Final, assert_never

from fateweaver.gameplay_p0_card_selection import select_cards_from_pool
from fateweaver.gameplay_p0_errors import ExpectedMappingError, MissingCardSlotError
from fateweaver.gameplay_p0_models import (
    BlockedReason,
    CardCandidate,
    CandidateTier,
    CardCandidateContext,
    CardRule,
    CardSelectionContext,
    Quest,
    RunState,
)
from fateweaver.models import JsonMap, JsonValue, StatusMap


TIER_RANK: Final = {"critical": 4, "strong": 3, "normal": 2, "flavor": 1, "blocked": 0}
DEFAULT_MODIFIERS: Final = {
    "quest_objective_match": 30,
    "storylet_tag_match": 20,
    "region_match": 10,
    "slot_role_bonus": 5,
    "storylet_hint_bonus": 25,
    "cooldown_tag_penalty": -15,
    "repeat_group_penalty": -30,
    "recent_repeat_penalty": -25,
    "already_completed": -999,
    "unavailable": -999,
    "low_food_penalty": -10,
}


@dataclass(frozen=True, slots=True)
class CandidateScoreInput:
    card: CardRule
    state: RunState
    matched_tags: tuple[str, ...]
    matched_objectives: tuple[str, ...]
    matched_storylet_hints: tuple[str, ...]
    cooldown_penalty: int
    blocked_reason: BlockedReason


def present_cards(
    cards: tuple[CardRule, ...],
    state: RunState,
    context: CardCandidateContext,
    selection: CardSelectionContext | None = None,
) -> tuple[CardRule, CardRule, CardRule]:
    return cards_from_pool(build_card_candidate_pool(cards, state, context), selection)


def cards_from_pool(
    pool: tuple[CardCandidate, ...],
    selection: CardSelectionContext | None = None,
) -> tuple[CardRule, CardRule, CardRule]:
    if selection is not None:
        return select_cards_from_pool(pool, selection).cards
    available = tuple(candidate for candidate in ranked_candidates(pool) if candidate.tier != "blocked")
    return (
        best_for_slot(available, "quest_progress").card,
        best_for_slot(available, "risk_discovery").card,
        best_for_slot(available, "resource_alternative").card,
    )


def build_card_candidate_pool(cards: tuple[CardRule, ...], state: RunState, context: CardCandidateContext) -> tuple[CardCandidate, ...]:
    return tuple(score_card(card, state, context) for card in cards)


def score_card(card: CardRule, state: RunState, context: CardCandidateContext) -> CardCandidate:
    matched_tags = tuple(tag for tag in card.applies_to_storylet_tags if tag in context.storylet_tags)
    matched_objectives = tuple(objective_id for objective_id in card.applies_to_quest_objectives if objective_id in active_optional_objectives(context.quest))
    matched_storylet_hints = (card.id,) if card.id in context.card_candidate_hints else ()
    cooldown_penalty = candidate_cooldown_penalty(card, state, context)
    blocked_reason = card_blocked_reason(card, state)
    repeat_penalty = modifier(card, "recent_repeat_penalty") if recently_seen_card(card, state) else 0
    score = candidate_score(CandidateScoreInput(card, state, matched_tags, matched_objectives, matched_storylet_hints, cooldown_penalty, blocked_reason))
    return CardCandidate(
        card=card,
        score=score,
        tier=classify_tier(score, blocked_reason),
        matched_tags=matched_tags,
        matched_objectives=matched_objectives,
        blocked_reason=blocked_reason,
        matched_storylet_hints=matched_storylet_hints,
        cooldown_penalty=cooldown_penalty,
        repeat_penalty=repeat_penalty,
    )


def candidate_score(candidate: CandidateScoreInput) -> int:
    card = candidate.card
    state = candidate.state
    score = card.base_weight
    if candidate.matched_objectives:
        score += modifier(card, "quest_objective_match")
    if candidate.matched_tags:
        score += modifier(card, "storylet_tag_match")
    if candidate.matched_storylet_hints:
        score += modifier(card, "storylet_hint_bonus")
    if state.region in card.regions:
        score += modifier(card, "region_match")
    if card.slot_role in {"quest_progress", "risk_discovery", "resource_alternative"}:
        score += modifier(card, "slot_role_bonus")
    if recently_seen_card(card, state):
        score += modifier(card, "recent_repeat_penalty")
    if low_food_penalty_applies(card, state):
        score += modifier(card, "low_food_penalty")
    score += candidate.cooldown_penalty
    match candidate.blocked_reason:
        case "":
            return score
        case "completed_objective":
            return score + modifier(card, "already_completed")
        case "unavailable_requirement":
            return score + modifier(card, "unavailable")
        case unreachable:
            assert_never(unreachable)


def card_blocked_reason(card: CardRule, state: RunState) -> BlockedReason:
    if card.progress_key and state.quest_progress.get(card.progress_key, 0) > 0:
        return "completed_objective"
    if not card_available(card, state):
        return "unavailable_requirement"
    return ""


def recently_seen_card(card: CardRule, state: RunState) -> bool:
    return card.id in state.recent_presented_card_ids or card.id in state.selected_choice_history


def candidate_cooldown_penalty(card: CardRule, state: RunState, context: CardCandidateContext) -> int:
    penalty = 0
    active_tags = {counter.key for counter in state.repeat_memory.cooldown_tags}
    active_groups = {counter.key for counter in state.repeat_memory.repeat_groups}
    if context.repeat_group and context.repeat_group in active_groups:
        penalty += modifier(card, "repeat_group_penalty")
    if active_tags.intersection(context.cooldown_tags):
        penalty += modifier(card, "cooldown_tag_penalty")
    return penalty


def classify_tier(score: int, blocked_reason: BlockedReason) -> CandidateTier:
    if blocked_reason or score < 0:
        return "blocked"
    if score >= 90:
        return "critical"
    if score >= 70:
        return "strong"
    if score >= 40:
        return "normal"
    return "flavor"


def ranked_candidates(pool: tuple[CardCandidate, ...]) -> tuple[CardCandidate, ...]:
    return tuple(sorted(pool, key=lambda candidate: (TIER_RANK[candidate.tier], candidate.score, candidate.card.id), reverse=True))


def best_for_slot(candidates: tuple[CardCandidate, ...], slot: str) -> CardCandidate:
    for candidate in candidates:
        if candidate.card.slot_role == slot:
            return candidate
    raise MissingCardSlotError(slot)


def card_candidate_pool_json(pool: tuple[CardCandidate, ...]) -> list[JsonMap]:
    return [
        {
            "card_id": candidate.card.id,
            "slot_role": candidate.card.slot_role,
            "score": candidate.score,
            "tier": candidate.tier,
            "matched_tags": list(candidate.matched_tags),
            "matched_objectives": list(candidate.matched_objectives),
            "matched_storylet_hints": list(candidate.matched_storylet_hints),
            "blocked_reason": candidate.blocked_reason,
            "selection_seed_key": candidate.selection_seed_key,
            "variety_window": candidate.variety_window,
            "selected_by": candidate.selected_by,
            "repeat_penalty": candidate.repeat_penalty,
            "cooldown_penalty": candidate.cooldown_penalty,
        }
        for candidate in pool
    ]


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


def low_food_penalty_applies(card: CardRule, state: RunState) -> bool:
    status = as_mapping(card.result.get("status", {}))
    food_delta = status.get("food", 0)
    match food_delta:
        case int() | float() | str():
            return state.status.get("food", 0) <= 2 and int(food_delta) < 0
        case None | bool() | list() | dict():
            return False
        case unreachable:
            assert_never(unreachable)


def card_json(card: CardRule) -> JsonMap:
    return {
        "choice_id": card.id,
        "card_id": card.id,
        "choice_text": card.title,
        "title": card.title,
        "description": card.description,
        "slot_role": card.slot_role,
        "choice_type": card.slot_role,
        "available": True,
        "unavailable_reason": None,
        "hidden": False,
        "expected_risk": "low" if card.slot_role != "risk_discovery" else "medium",
        "influenced_by": card_influences(card),
        "result": card.result,
    }


def card_available(card: CardRule, state: RunState) -> bool:
    return (
        state.region in card.regions
        and (card.requires_item is None or card.requires_item in state.inventory)
        and progress_matches(card.requires_progress, state.quest_progress)
        and status_matches(card.requires_status, state.status)
    )


def progress_matches(requirements: JsonMap, progress: dict[str, int]) -> bool:
    for key, raw_bounds in requirements.items():
        bounds = as_mapping(raw_bounds)
        minimum = bounds.get("min")
        if minimum is not None and progress.get(key, 0) < int(minimum):
            return False
    return True


def status_matches(requirements: JsonMap, status: StatusMap) -> bool:
    for key, raw_bounds in requirements.items():
        bounds = as_mapping(raw_bounds)
        minimum = bounds.get("min")
        if minimum is not None and status.get(key, 0) < int(minimum):
            return False
    return True


def active_optional_objectives(quest: Quest) -> set[str]:
    return {objective.id for objective in quest.objectives if not objective.required}


def card_influences(card: CardRule) -> list[str]:
    values = [f"slot:{card.slot_role}"]
    values.extend(f"tag:{tag}" for tag in card.tags)
    values.extend(f"storylet_tag:{tag}" for tag in card.applies_to_storylet_tags)
    values.extend(f"objective:{objective_id}" for objective_id in card.applies_to_quest_objectives)
    if card.progress_key:
        values.append(f"progress:{card.progress_key}")
    return values


def as_mapping(value: JsonValue) -> JsonMap:
    if not isinstance(value, dict):
        raise ExpectedMappingError(type(value).__name__)
    return {str(key): item for key, item in value.items()}
