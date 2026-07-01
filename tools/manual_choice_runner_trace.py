from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

try:
    from .manual_choice_runner_types import PresentedCardRelevance, RequiredObjectiveTrace, TraceEntry
except ImportError:
    from manual_choice_runner_types import PresentedCardRelevance, RequiredObjectiveTrace, TraceEntry

if TYPE_CHECKING:
    from fateweaver.gameplay_p0_models import Quest, QuestObjective, RunState


def build_trace_entry(
    quest: Quest,
    turn: dict,
    selected_index: int,
    before: RunState,
    after: RunState,
) -> TraceEntry:
    after_tags = tuple(str(value) for value in turn["next_event_tags"])
    is_onboarding_turn = int(turn["turn"]) == 1
    entry: TraceEntry = {
        "turn": turn["turn"],
        "day": turn["run_clock"]["day"],
        "active_quest_id": quest.id,
        "active_quest_title": quest.title,
        "quest_onboarding": is_onboarding_turn,
        "onboarding_reason": "run_start" if is_onboarding_turn else "",
        "required_objective_ids": _required_objective_ids(quest),
        "required_objectives": _required_objectives_trace(quest, before, after),
        "presented_card_ids": [card["card_id"] for card in turn["presented_cards"]],
        "presented_card_relevance": _presented_card_relevance(quest, turn),
        "selected_index": selected_index,
        "selected_card_id": turn["selected_cards"][0],
        "selected_card_slot_role": turn["selected_choice_type"],
        "result_summary": turn["choice_reason"],
        "resource_delta": _int_delta(turn["state_before"], turn["state_after"]),
        "objective_delta": _int_delta(before.quest_progress, turn["quest_progress"]),
        "next_event_tags_delta": [tag for tag in after_tags if tag not in before.next_event_tags],
    }
    if is_onboarding_turn:
        entry["onboarding_turn"] = int(turn["turn"])
    return entry


def _required_objective_ids(quest: Quest) -> list[str]:
    return [objective.id for objective in quest.objectives if objective.required]


def _presented_card_relevance(quest: Quest, turn: dict) -> list[PresentedCardRelevance]:
    candidates = {str(candidate["card_id"]): candidate for candidate in turn["card_candidate_pool"]}
    required_objectives = tuple(objective for objective in quest.objectives if objective.required)
    return [
        _card_relevance(
            str(card["card_id"]),
            str(card["slot_role"]),
            tuple(str(quest_id) for quest_id in card["quest_ids"]),
            tuple(str(value) for value in card["influenced_by"]),
            candidates[str(card["card_id"])],
            quest,
            required_objectives,
        )
        for card in turn["presented_cards"]
    ]


def _card_relevance(
    card_id: str,
    slot_role: str,
    quest_ids: tuple[str, ...],
    influences: tuple[str, ...],
    candidate: dict,
    quest: Quest,
    required_objectives: tuple[QuestObjective, ...],
) -> PresentedCardRelevance:
    active_quest_linked = quest.id in quest_ids
    required_linked = _required_objective_linked(influences, required_objectives)
    storylet_linked = bool(candidate["matched_tags"]) or bool(candidate["matched_storylet_hints"]) or bool(candidate["matched_objectives"])
    resource_or_safety = _resource_or_safety(slot_role, influences, candidate)
    off_quest = not (active_quest_linked or required_linked or storylet_linked or resource_or_safety)
    selection_reason = str(candidate["selected_by"])
    return {
        "card_id": card_id,
        "slot_role": slot_role,
        "active_quest_id": quest.id,
        "required_objective_ids": [objective.id for objective in required_objectives],
        "active_quest_linked": active_quest_linked,
        "required_objective_linked": required_linked,
        "storylet_linked": storylet_linked,
        "resource_or_safety": resource_or_safety,
        "off_quest_candidate": off_quest,
        "relevance_reason": _relevance_reason(active_quest_linked, required_linked, storylet_linked, resource_or_safety),
        "selection_reason": selection_reason,
        "fallback_reason": "slot_window_fallback" if selection_reason == "fallback_pick" else "",
    }


def _required_objective_linked(influences: tuple[str, ...], objectives: tuple[QuestObjective, ...]) -> bool:
    linked = set(influences)
    return any(f"objective:{objective.id}" in linked or f"progress:{objective.progress_key}" in linked for objective in objectives)


def _resource_or_safety(slot_role: str, influences: tuple[str, ...], candidate: dict) -> bool:
    return (
        slot_role == "resource_alternative"
        or "tag:resource" in influences
        or "tag:survival" in influences
        or int(candidate["score"]) >= 70
    )


def _relevance_reason(
    active_quest_linked: bool,
    required_linked: bool,
    storylet_linked: bool,
    resource_or_safety: bool,
) -> str:
    if active_quest_linked:
        return "active_quest"
    if required_linked:
        return "required_objective"
    if storylet_linked:
        return "storylet_context"
    if resource_or_safety:
        return "resource_or_safety"
    return "off_quest"


def _required_objectives_trace(quest: Quest, before: RunState, after: RunState) -> list[RequiredObjectiveTrace]:
    return [
        {
            "id": objective.id,
            "objective_type": objective.objective_type,
            "target": objective.target,
            "progress_key": objective.progress_key,
            "required": objective.required,
            "before_value": _objective_trace_value(objective, before),
            "after_value": _objective_trace_value(objective, after),
            "completed_after": _objective_complete(objective, after),
        }
        for objective in quest.objectives
        if objective.required
    ]


def _objective_trace_value(objective: QuestObjective, state: RunState) -> int:
    match objective.objective_type:
        case "collect_item":
            return 1 if objective.target in state.inventory else 0
        case "discover_clue":
            return 1 if objective.target in state.clues else 0
        case "survive_expedition" | "keep_resource_at_least":
            return int(state.status.get(objective.target, 0))
        case "return_to_region" | "optional_action":
            return int(state.quest_progress.get(objective.progress_key, 0))
        case unreachable:
            assert_never(unreachable)


def _objective_complete(objective: QuestObjective, state: RunState) -> bool:
    match objective.objective_type:
        case "collect_item":
            return _objective_trace_value(objective, state) >= _objective_goal_value(objective)
        case "discover_clue":
            return objective.target in state.clues
        case "survive_expedition" | "keep_resource_at_least":
            return int(state.status.get(objective.target, 0)) >= objective.value
        case "return_to_region":
            return state.region == objective.target and int(state.quest_progress.get(objective.progress_key, 0)) >= objective.value
        case "optional_action":
            return int(state.quest_progress.get(objective.progress_key, 0)) >= objective.value
        case unreachable:
            assert_never(unreachable)


def _objective_goal_value(objective: QuestObjective) -> int:
    if objective.count:
        return objective.count
    if objective.value:
        return objective.value
    return 1


def _int_delta(before: dict, after: dict) -> dict[str, int]:
    keys = sorted({str(key) for key in before} | {str(key) for key in after})
    return {key: int(after.get(key, 0)) - int(before.get(key, 0)) for key in keys}
