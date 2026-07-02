from __future__ import annotations

from typing import assert_never

from fateweaver.gameplay_models import CardRule, Quest, QuestObjective, RunState

def completed_objective_blocked(card: CardRule, state: RunState, quest: Quest) -> bool:
    if card.progress_key and state.quest_progress.get(card.progress_key, 0) > 0:
        return True
    if _linked_objectives_completed(card, state, quest):
        return True
    return _required_objectives_previously_satisfied(quest, state) and _recent_unscoped_quest_progress(card, state)


def _linked_objectives_completed(card: CardRule, state: RunState, quest: Quest) -> bool:
    linked = tuple(objective for objective in quest.objectives if objective.id in card.applies_to_quest_objectives)
    return bool(linked) and all(_objective_previously_satisfied(objective, state) for objective in linked)


def _required_objectives_previously_satisfied(quest: Quest, state: RunState) -> bool:
    return all(_objective_previously_satisfied(objective, state) for objective in quest.objectives if objective.required)


def _recent_unscoped_quest_progress(card: CardRule, state: RunState) -> bool:
    recent_selected = state.selected_choice_history[-3:]
    return card.slot_role == "quest_progress" and not card.quest_ids and card.id in recent_selected


def _objective_previously_satisfied(objective: QuestObjective, state: RunState) -> bool:
    match objective.objective_type:
        case "collect_item":
            return state.quest_progress.get(objective.target, 0) >= objective.count
        case "return_to_region":
            return state.quest_progress.get(objective.progress_key, 0) >= objective.value
        case "survive_expedition" | "keep_resource_at_least":
            return state.status.get(objective.target, 0) >= objective.value
        case "discover_clue":
            return objective.target in state.clues
        case "optional_action":
            return state.quest_progress.get(objective.progress_key, 0) >= objective.value
        case unreachable:
            assert_never(unreachable)
