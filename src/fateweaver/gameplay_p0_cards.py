from __future__ import annotations

from fateweaver.gameplay_p0_models import CardCandidateContext, CardRule, Quest, RunState
from fateweaver.models import JsonMap, JsonValue, StatusMap


def present_cards(cards: tuple[CardRule, ...], state: RunState, context: CardCandidateContext) -> tuple[CardRule, CardRule, CardRule]:
    visible = tuple(card for card in cards if card_available(card, state))
    return (
        quest_card(visible, state),
        first_for_slot(visible, "risk_discovery"),
        resource_alternative_card(visible, state, context),
    )


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


def first_for_slot(cards: tuple[CardRule, ...], slot: str) -> CardRule:
    for card in cards:
        if card.slot_role == slot:
            return card
    raise ValueError(f"No P0 card for slot: {slot}")


def resource_alternative_card(cards: tuple[CardRule, ...], state: RunState, context: CardCandidateContext) -> CardRule:
    for card in cards:
        if card.slot_role == "resource_alternative" and card_matches_context(card, state, context):
            return card
    for card in cards:
        if card.slot_role == "resource_alternative" and not card.applies_to_quest_objectives:
            return card
    return first_for_slot(cards, "resource_alternative")


def card_matches_context(card: CardRule, state: RunState, context: CardCandidateContext) -> bool:
    if not card.applies_to_storylet_tags or not card.applies_to_quest_objectives:
        return False
    if card.progress_key and state.quest_progress.get(card.progress_key, 0) > 0:
        return False
    return bool(set(card.applies_to_storylet_tags) & set(context.storylet_tags)) and bool(
        set(card.applies_to_quest_objectives) & active_optional_objectives(context.quest),
    )


def active_optional_objectives(quest: Quest) -> set[str]:
    return {objective.id for objective in quest.objectives if not objective.required}


def quest_card(cards: tuple[CardRule, ...], state: RunState) -> CardRule:
    target = quest_target_card(state)
    for card in cards:
        if card.id == target:
            return card
    return first_for_slot(cards, "quest_progress")


def quest_target_card(state: RunState) -> str:
    herbs = state.quest_progress.get("herbs_collected", 0)
    returned = state.quest_progress.get("returned_to_village", 0)
    if state.region == "village" and herbs >= 3 and returned >= 1:
        return "report_to_apothecary"
    if state.region == "forest" and herbs >= 3:
        return "return_to_village"
    if state.region == "village":
        return "ask_apothecary"
    return "search_herbs"


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
        raise TypeError("value must be a mapping")
    return {str(key): item for key, item in value.items()}
