from __future__ import annotations

from dataclasses import replace

from fateweaver.gameplay_p0_models import Quest, RunState
from fateweaver.gameplay_p0_objectives import evaluate_objectives
from fateweaver.gameplay_p0_rules import merge_ints
from fateweaver.models import JsonMap, ProjectData
from fateweaver.state_manager import apply_choice_result


def complete_quest_lifecycle(quest: Quest, state: RunState, bundle: ProjectData, score_rules: JsonMap) -> tuple[RunState, JsonMap]:
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
    return after_state, {
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
        "next_quest_id": "",
        "no_next_quest": True,
        "next_quest_onboarding": False,
        "run_complete": True,
        "completion_blocked_by_min_turns": False,
    }


def _reward_status_delta(rewards: JsonMap, bundle: ProjectData) -> dict[str, int]:
    return {str(key): int(value) for key, value in rewards.items() if key in bundle.statuses}


def _reward_score_delta(rewards: JsonMap) -> dict[str, int]:
    score = int(rewards.get("score", 0))
    return {"quest_reward": score} if score else {}
