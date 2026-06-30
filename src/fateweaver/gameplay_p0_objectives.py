from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, assert_never

from fateweaver.gameplay_p0_models import Quest, QuestObjective, RunState
from fateweaver.models import JsonMap, ProjectData

ObjectiveStatus = Literal["completed", "partial", "failed"]
ResultType = Literal["success", "partial_success", "failure"]


@dataclass(frozen=True, slots=True)
class ObjectiveEvaluation:
    objective: QuestObjective
    status: ObjectiveStatus
    reason: str
    progress_value: int
    target_value: int
    score_delta: int


@dataclass(frozen=True, slots=True)
class QuestReportRequest:
    quest: Quest
    state: RunState
    bundle: ProjectData
    score_rules: JsonMap


def quest_completed(quest: Quest, state: RunState, bundle: ProjectData) -> bool:
    evaluations = evaluate_objectives(quest, state, bundle)
    return _result_type(evaluations) == "success"


def build_quest_report(request: QuestReportRequest) -> JsonMap:
    evaluations = evaluate_objectives(request.quest, request.state, request.bundle)
    result_type = _result_type(evaluations)
    partial_reasons = _partial_reasons(evaluations, request.state, result_type)
    failure_reasons = _failure_reasons(evaluations, request.state, result_type)
    result_reasons = partial_reasons if result_type == "partial_success" else failure_reasons
    result_reason = result_reasons[0] if result_reasons else "quest_completed"
    score_breakdown = _score_breakdown(request, evaluations, result_type)
    return {
        "quest_id": request.quest.id,
        "result_type": result_type,
        "result_reason": result_reason,
        "objective_results": [_objective_json(evaluation) for evaluation in evaluations],
        "completed_objectives": _completed_objectives(evaluations),
        "failed_objectives": _failed_objectives(evaluations),
        "partial_reasons": partial_reasons,
        "failure_reasons": failure_reasons,
        "resource_summary": dict(request.state.status),
        "score": sum(score_breakdown.values()),
        "score_breakdown": score_breakdown,
        "reward_status": _reward_status(result_type),
        "rewards": request.quest.rewards if result_type == "success" else {},
        "unlocked_or_suggested_next": ["missing_porter_search"] if result_type == "success" else ["retry_herb_gathering"],
        "review_text": _review_text(result_type, result_reason),
    }


def evaluate_objectives(quest: Quest, state: RunState, bundle: ProjectData) -> tuple[ObjectiveEvaluation, ...]:
    return tuple(_evaluate_objective(objective, state, bundle) for objective in quest.objectives)


def _evaluate_objective(objective: QuestObjective, state: RunState, bundle: ProjectData) -> ObjectiveEvaluation:
    match objective.objective_type:
        case "collect_item":
            return _progress_objective(objective, state.quest_progress.get(objective.target, 0), objective.count)
        case "return_to_region":
            progress = state.quest_progress.get(objective.progress_key, 0)
            value = progress if state.region == objective.target else 0
            return _complete_or_failed(objective, value, objective.value)
        case "survive_expedition":
            health = state.status.get(objective.target, bundle.statuses[objective.target].initial)
            return _complete_or_failed(objective, health, objective.value)
        case "keep_resource_at_least":
            return _complete_or_failed(objective, state.status.get(objective.target, 0), objective.value)
        case "discover_clue":
            value = 1 if objective.target in state.clues else 0
            return _complete_or_failed(objective, value, objective.value)
        case "optional_action":
            return _progress_objective(objective, state.quest_progress.get(objective.target, 0), objective.value)
        case unreachable:
            assert_never(unreachable)


def _progress_objective(objective: QuestObjective, progress: int, target: int) -> ObjectiveEvaluation:
    if progress >= target:
        return ObjectiveEvaluation(objective=objective, status="completed", reason="completed", progress_value=progress, target_value=target, score_delta=_score_delta(objective, "completed"))
    if progress > 0:
        return ObjectiveEvaluation(objective=objective, status="partial", reason=objective.partial_reason, progress_value=progress, target_value=target, score_delta=_score_delta(objective, "partial"))
    return ObjectiveEvaluation(objective=objective, status="failed", reason=objective.failure_reason, progress_value=progress, target_value=target, score_delta=_score_delta(objective, "failed"))


def _complete_or_failed(objective: QuestObjective, progress: int, target: int) -> ObjectiveEvaluation:
    status: ObjectiveStatus = "completed" if progress >= target else "failed"
    reason = "completed" if status == "completed" else objective.failure_reason
    return ObjectiveEvaluation(objective=objective, status=status, reason=reason, progress_value=progress, target_value=target, score_delta=_score_delta(objective, status))


def _score_delta(objective: QuestObjective, status: ObjectiveStatus) -> int:
    match status:
        case "completed":
            return 10 * objective.reward_weight
        case "partial":
            return 5 * objective.reward_weight
        case "failed":
            return -10 * objective.reward_weight if objective.required else 0
        case unreachable:
            assert_never(unreachable)


def _result_type(evaluations: tuple[ObjectiveEvaluation, ...]) -> ResultType:
    required = tuple(evaluation for evaluation in evaluations if evaluation.objective.required)
    primary = tuple(evaluation for evaluation in required if evaluation.objective.objective_type != "survive_expedition")
    if _objective_failed(evaluations, "survive_expedition"):
        return "failure"
    if all(evaluation.status == "completed" for evaluation in required):
        return "success"
    if any(evaluation.status in {"completed", "partial"} for evaluation in primary):
        return "partial_success"
    return "failure"


def _partial_reasons(evaluations: tuple[ObjectiveEvaluation, ...], state: RunState, result_type: ResultType) -> list[str]:
    if result_type != "partial_success":
        return []
    reasons: list[str] = []
    for evaluation in evaluations:
        _append_partial_reason(reasons, evaluation)
    if _clock_exceeded(state):
        reasons.append("return_late")
    if reasons:
        reasons.append("reduced_reward")
    return _dedupe(reasons)


def _append_partial_reason(reasons: list[str], evaluation: ObjectiveEvaluation) -> None:
    if evaluation.status == "partial" and evaluation.objective.required:
        reasons.append(evaluation.reason)
    if evaluation.status == "failed" and evaluation.objective.objective_type == "return_to_region":
        reasons.append(evaluation.objective.partial_reason)
    if evaluation.status == "failed" and not evaluation.objective.required:
        reasons.append(evaluation.reason)


def _failure_reasons(evaluations: tuple[ObjectiveEvaluation, ...], state: RunState, result_type: ResultType) -> list[str]:
    if result_type != "failure":
        return []
    reasons = _clock_reasons(state)
    for evaluation in evaluations:
        if evaluation.status == "failed" and evaluation.objective.objective_type == "survive_expedition":
            reasons.append(evaluation.reason)
        if evaluation.status == "failed" and evaluation.objective.objective_type == "return_to_region":
            reasons.append(evaluation.reason)
    if any(evaluation.status == "failed" and evaluation.objective.required for evaluation in evaluations):
        reasons.append("primary_objective_failed")
    return _dedupe(reasons or ["primary_objective_failed"])


def _clock_reasons(state: RunState) -> list[str]:
    reasons: list[str] = []
    if state.clock.day > state.clock.max_days:
        reasons.append("max_day_exceeded")
    if state.clock.turn > state.clock.max_turns:
        reasons.append("max_turn_exceeded")
    return reasons


def _score_breakdown(request: QuestReportRequest, evaluations: tuple[ObjectiveEvaluation, ...], result_type: ResultType) -> dict[str, int]:
    breakdown = dict(request.state.score)
    objective_score = sum(evaluation.score_delta for evaluation in evaluations)
    if objective_score != 0:
        breakdown["objective_completion"] = objective_score
    outcome_score = _outcome_score(result_type, request.score_rules)
    if outcome_score != 0:
        breakdown["outcome_adjustment"] = outcome_score
    return breakdown


def _outcome_score(result_type: ResultType, score_rules: JsonMap) -> int:
    raw_bonus = score_rules.get("ending_bonus", {})
    if not isinstance(raw_bonus, dict):
        return 0
    return int(raw_bonus.get(result_type, 0))


def _objective_json(evaluation: ObjectiveEvaluation) -> JsonMap:
    return {
        "objective_id": evaluation.objective.id,
        "objective_type": evaluation.objective.objective_type,
        "status": evaluation.status,
        "reason": evaluation.reason,
        "progress_value": evaluation.progress_value,
        "target_value": evaluation.target_value,
        "required": evaluation.objective.required,
        "score_key": evaluation.objective.score_key,
        "score_delta": evaluation.score_delta,
    }


def _completed_objectives(evaluations: tuple[ObjectiveEvaluation, ...]) -> list[str]:
    return [evaluation.objective.id for evaluation in evaluations if evaluation.status == "completed" and evaluation.objective.required and evaluation.objective.id != "survive_expedition"]


def _failed_objectives(evaluations: tuple[ObjectiveEvaluation, ...]) -> list[str]:
    return [evaluation.objective.id for evaluation in evaluations if evaluation.status == "failed" and evaluation.objective.required]


def _objective_failed(evaluations: tuple[ObjectiveEvaluation, ...], objective_id: str) -> bool:
    return any(evaluation.objective.id == objective_id and evaluation.status == "failed" for evaluation in evaluations)


def _clock_exceeded(state: RunState) -> bool:
    return state.clock.turn > state.clock.max_turns or state.clock.day > state.clock.max_days


def _reward_status(result_type: ResultType) -> str:
    return {"success": "full_reward", "partial_success": "reduced_reward", "failure": "no_reward"}[result_type]


def _review_text(result_type: ResultType, result_reason: str) -> str:
    match result_type:
        case "success":
            return "목표를 모두 달성했고 다음 의뢰의 실마리를 얻었다."
        case "partial_success":
            if result_reason == "primary_partial":
                return "주 목표를 일부 달성했지만 목표 수량이나 보고를 끝내지 못했다."
            return "일부 목표는 달성했지만 보고나 보조 목표를 완전히 끝내지 못했다."
        case "failure":
            if result_reason == "health_zero":
                return "체력이 바닥나 원정이 중단됐고 자원 관리와 위험 판단을 다시 봐야 한다."
            return "원정은 실패했고 자원 관리와 귀환 판단을 다시 봐야 한다."
        case unreachable:
            assert_never(unreachable)


def _dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
