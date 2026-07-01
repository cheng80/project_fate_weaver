from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentDecisionContext:
    presented_cards: tuple[dict, dict, dict]
    relevance: tuple[dict, dict, dict]
    selected_card_ids: tuple[str, ...]
    turn: int


def policy_ids() -> tuple[str, ...]:
    return ("goal_focused", "safety_first", "risk_seeking", "explorer", "contrarian")


def build_agent_context(cards: tuple, candidate_pool: tuple, active_quest_id: str, state) -> AgentDecisionContext:
    candidate_by_id = {candidate.card.id: candidate for candidate in candidate_pool}
    return AgentDecisionContext(
        presented_cards=tuple(_agent_card_payload(card, candidate_by_id.get(card.id)) for card in cards),
        relevance=tuple(_agent_relevance_payload(card, candidate_by_id.get(card.id), active_quest_id) for card in cards),
        selected_card_ids=tuple(str(card_id) for card_id in state.selected_choice_history),
        turn=int(state.clock.turn),
    )


def choose_agent_index(policy_id: str, context: AgentDecisionContext) -> int:
    scores = [_score_card(policy_id, slot, context) for slot in range(1, 4)]
    best = max(scores, key=lambda item: (item[0], item[1]))
    return best[2]


def _score_card(policy_id: str, slot: int, context: AgentDecisionContext) -> tuple[int, int, int]:
    match policy_id:
        case "goal_focused":
            return (_goal_score(slot, context), -slot, slot)
        case "safety_first":
            return (_safety_score(slot, context), -slot, slot)
        case "risk_seeking":
            return (_risk_score(slot, context), slot, slot)
        case "explorer":
            return (_explorer_score(slot, context), -_slot_distance(slot, context.turn), slot)
        case "contrarian":
            return (_contrarian_score(slot, context), slot, slot)
        case _:
            raise ValueError(f"unknown agent policy {policy_id!r}")


def _goal_score(slot: int, context: AgentDecisionContext) -> int:
    card, relevance = _card_and_relevance(slot, context)
    result = _mapping(card.get("result", {}))
    score = 0
    if bool(relevance.get("required_objective_linked")):
        score += 80
    if bool(relevance.get("active_quest_linked")) or _truthy_sequence(card.get("quest_ids")):
        score += 35
    if _mapping(result.get("quest_progress", {})):
        score += 30
    if relevance.get("relevance_reason") in {"required_objective", "active_quest", "storylet_context"}:
        score += 20
    if bool(relevance.get("off_quest_candidate")):
        score -= 35
    return score


def _safety_score(slot: int, context: AgentDecisionContext) -> int:
    card, relevance = _card_and_relevance(slot, context)
    result = _mapping(card.get("result", {}))
    status = _mapping(result.get("status", {}))
    score = 20 if str(card.get("slot_role", "")) == "resource_alternative" else 0
    score += sum(max(0, int(value)) * 20 for value in status.values())
    score -= sum(abs(int(value)) * 18 for value in status.values() if int(value) < 0)
    if str(card.get("expected_risk", "")) == "high":
        score -= 25
    if bool(relevance.get("off_quest_candidate")):
        score -= 10
    return score


def _risk_score(slot: int, context: AgentDecisionContext) -> int:
    card, relevance = _card_and_relevance(slot, context)
    result = _mapping(card.get("result", {}))
    score_changes = _mapping(result.get("score_changes", {}))
    status = _mapping(result.get("status", {}))
    score = sum(abs(int(value)) for value in score_changes.values()) * 8
    score += sum(abs(int(value)) for value in status.values() if int(value) < 0) * 10
    if str(card.get("expected_risk", "")) == "high" or str(card.get("slot_role", "")) == "risk_discovery":
        score += 35
    if str(card.get("card_id", "")) not in context.selected_card_ids:
        score += 10
    if bool(relevance.get("off_quest_candidate")):
        score -= 8
    return score


def _explorer_score(slot: int, context: AgentDecisionContext) -> int:
    card, relevance = _card_and_relevance(slot, context)
    card_id = str(card.get("card_id", ""))
    repeat_count = sum(1 for selected in context.selected_card_ids if selected == card_id)
    score = 50 - repeat_count * 35
    if str(relevance.get("relevance_reason", "")) not in {"", "off_quest"}:
        score += 15
    if bool(relevance.get("off_quest_candidate")):
        score -= 20
    return score


def _contrarian_score(slot: int, context: AgentDecisionContext) -> int:
    _, relevance = _card_and_relevance(slot, context)
    score = 70 - _goal_score(slot, context)
    if bool(relevance.get("off_quest_candidate")):
        score -= 20
    if str(relevance.get("fallback_reason", "")):
        score -= 10
    return score


def _card_and_relevance(slot: int, context: AgentDecisionContext) -> tuple[dict, dict]:
    index = slot - 1
    return context.presented_cards[index], context.relevance[index]


def _slot_distance(slot: int, turn: int) -> int:
    preferred = ((turn - 1) % 3) + 1
    return abs(slot - preferred)


def _mapping(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _truthy_sequence(value: object) -> bool:
    return isinstance(value, (list, tuple)) and bool(value)


def _agent_card_payload(card, candidate) -> dict:
    return {
        "card_id": card.id,
        "slot_role": card.slot_role,
        "result": card.result,
        "quest_ids": list(card.quest_ids),
        "expected_risk": "high" if card.slot_role == "risk_discovery" else "low",
        "score": getattr(candidate, "score", 0),
    }


def _agent_relevance_payload(card, candidate, active_quest_id: str) -> dict:
    active_quest_linked = active_quest_id in card.quest_ids
    required_objective_linked = bool(getattr(candidate, "matched_objectives", ()))
    storylet_linked = bool(getattr(candidate, "matched_tags", ())) or bool(getattr(candidate, "matched_storylet_hints", ()))
    resource_or_safety = card.slot_role == "resource_alternative"
    off_quest = not (active_quest_linked or required_objective_linked or storylet_linked or resource_or_safety)
    return {
        "card_id": card.id,
        "active_quest_linked": active_quest_linked,
        "required_objective_linked": required_objective_linked,
        "storylet_linked": storylet_linked,
        "resource_or_safety": resource_or_safety,
        "off_quest_candidate": off_quest,
        "relevance_reason": _agent_relevance_reason(active_quest_linked, required_objective_linked, storylet_linked, resource_or_safety),
        "fallback_reason": "slot_window_fallback" if getattr(candidate, "selected_by", "") == "fallback_pick" else "",
    }


def _agent_relevance_reason(active_quest: bool, required_objective: bool, storylet: bool, resource: bool) -> str:
    if active_quest:
        return "active_quest"
    if required_objective:
        return "required_objective"
    if storylet:
        return "storylet_context"
    if resource:
        return "resource_or_safety"
    return "off_quest"
