from __future__ import annotations

from dataclasses import replace

from fateweaver.gameplay_models import Quest, RunState
from fateweaver.quest_objectives import evaluate_objectives
from fateweaver.gameplay_rules import merge_ints
from fateweaver.models import JsonMap, ProjectData
from fateweaver.state_manager import apply_choice_result


def complete_quest_lifecycle(
    quest: Quest,
    state: RunState,
    bundle: ProjectData,
    score_rules: JsonMap,
    next_quest: Quest | None = None,
) -> tuple[RunState, JsonMap]:
    reward_tag = f"quest_reward:{quest.id}"
    before = dict(state.status)
    completed_ids = [
        evaluation.objective.id
        for evaluation in evaluate_objectives(quest, state, bundle, score_rules)
        if evaluation.objective.required and evaluation.status == "completed"
    ]
    reward_delta = _reward_status_delta(quest.rewards, bundle)
    score_delta = _reward_score_delta(quest.rewards)
    duplicate = reward_tag in state.run_tags
    if duplicate:
        after_state = state
    else:
        transition = apply_choice_result(state.status, state.inventory, state.run_tags, {"status": reward_delta, "add_run_tag": [reward_tag]}, bundle.statuses)
        after_state = replace(
            state,
            status=transition.status,
            run_tags=transition.run_tags,
            score=merge_ints(state.score, score_delta),
        )
    lifecycle = {
        "quest_lifecycle_event": "quest_success",
        "quest_completed": True,
        "quest_success": True,
        "completed_quest_id": quest.id,
        "completed_required_objective_ids": completed_ids,
        "reward_granted": not duplicate,
        "reward_delta": reward_delta if not duplicate else {},
        "reward_score_delta": score_delta if not duplicate else {},
        "resources_before": before,
        "resources_after": dict(after_state.status),
        "reward_reason": "quest_success" if not duplicate else "duplicate_prevented",
        "duplicate_reward_prevented": duplicate,
        "previous_quest_id": quest.id,
        "completion_blocked_by_min_turns": False,
    }
    if next_quest is None:
        lifecycle.update(
            {
                "next_quest_id": "",
                "no_next_quest": True,
                "next_quest_onboarding": False,
                "run_complete": True,
            },
        )
    else:
        lifecycle.update(
            {
                "quest_transition": True,
                "transition_reason": "quest_success",
                "next_quest_id": next_quest.id,
                "next_required_objective_ids": _required_objective_ids(next_quest),
                "previous_quest_completed_objective_ids": completed_ids,
                "no_next_quest": False,
                "next_quest_onboarding": True,
                "run_complete": False,
            },
        )
    return after_state, lifecycle


def _reward_status_delta(rewards: JsonMap, bundle: ProjectData) -> dict[str, int]:
    return {str(key): int(value) for key, value in rewards.items() if key in bundle.statuses}


def _reward_score_delta(rewards: JsonMap) -> dict[str, int]:
    score = int(rewards.get("score", 0))
    return {"quest_reward": score} if score else {}


def _required_objective_ids(quest: Quest) -> list[str]:
    return [objective.id for objective in quest.objectives if objective.required]
