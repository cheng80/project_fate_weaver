from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

try:
    from .manual_choice_runner_types import RequiredObjectiveTrace, TraceEntry
except ImportError:
    from manual_choice_runner_types import RequiredObjectiveTrace, TraceEntry

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
