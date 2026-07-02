from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, assert_never

from fateweaver.gameplay_models import Quest, QuestObjective, RunState
from fateweaver.objective_scoring import ObjectiveStatus, objective_score_delta
from fateweaver.models import JsonMap, ProjectData

ResultType = Literal["success", "partial_success", "failure"]
FailureKind = Literal[
    "none",
    "death_or_incapacitated",
    "objective_failed",
    "return_failed",
    "time_expired",
    "reputation_collapse",
    "quest_specific_failure",
    "unknown",
]
CharacterOutcome = Literal["alive", "injured", "incapacitated", "dead_or_lost", "unknown"]


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


def quest_completed(quest: Quest, state: RunState, bundle: ProjectData, score_rules: JsonMap) -> bool:
    evaluations = evaluate_objectives(quest, state, bundle, score_rules)
    return _result_type(evaluations, state) == "success"


def build_quest_report(request: QuestReportRequest) -> JsonMap:
    evaluations = evaluate_objectives(request.quest, request.state, request.bundle, request.score_rules)
    result_type = _result_type(evaluations, request.state)
    partial_reasons = _partial_reasons(evaluations, request.state, result_type)
    failure_reasons = _failure_reasons(evaluations, request.state, result_type)
    result_reasons = partial_reasons if result_type == "partial_success" else failure_reasons
    result_reason = result_reasons[0] if result_reasons else "quest_completed"
    score_breakdown = _score_breakdown(request, evaluations, result_type)
    report = {
        "quest_id": request.quest.id,
        "result_type": result_type,
        "result_reason": result_reason,
        "failure_kind": _failure_kind(failure_reasons, result_type),
        "character_outcome": _character_outcome(request.state),
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
    ending = _selected_ending(report, request.state, request.bundle)
    if ending:
        report["ending"] = ending
    return report


def evaluate_objectives(quest: Quest, state: RunState, bundle: ProjectData, score_rules: JsonMap) -> tuple[ObjectiveEvaluation, ...]:
    return tuple(_evaluate_objective(objective, state, bundle, score_rules) for objective in quest.objectives)


def _evaluate_objective(objective: QuestObjective, state: RunState, bundle: ProjectData, score_rules: JsonMap) -> ObjectiveEvaluation:
    match objective.objective_type:
        case "collect_item":
            return _progress_objective(objective, state.quest_progress.get(objective.target, 0), objective.count, score_rules)
        case "return_to_region":
            progress = state.quest_progress.get(objective.progress_key, 0)
            value = progress if state.region == objective.target else 0
            return _complete_or_failed(objective, value, objective.value, score_rules)
        case "survive_expedition":
            health = state.status.get(objective.target, bundle.statuses[objective.target].initial)
            return _complete_or_failed(objective, health, objective.value, score_rules)
        case "keep_resource_at_least":
            return _complete_or_failed(objective, state.status.get(objective.target, 0), objective.value, score_rules)
        case "discover_clue":
            value = 1 if objective.target in state.clues else 0
            return _complete_or_failed(objective, value, objective.value, score_rules)
        case "optional_action":
            return _progress_objective(objective, state.quest_progress.get(objective.progress_key, 0), objective.value, score_rules)
        case unreachable:
            assert_never(unreachable)


def _progress_objective(objective: QuestObjective, progress: int, target: int, score_rules: JsonMap) -> ObjectiveEvaluation:
    if progress >= target:
        return ObjectiveEvaluation(objective=objective, status="completed", reason="completed", progress_value=progress, target_value=target, score_delta=objective_score_delta(objective, "completed", score_rules))
    if progress > 0:
        return ObjectiveEvaluation(objective=objective, status="partial", reason=objective.partial_reason, progress_value=progress, target_value=target, score_delta=objective_score_delta(objective, "partial", score_rules))
    return ObjectiveEvaluation(objective=objective, status="failed", reason=objective.failure_reason, progress_value=progress, target_value=target, score_delta=objective_score_delta(objective, "failed", score_rules))


def _complete_or_failed(objective: QuestObjective, progress: int, target: int, score_rules: JsonMap) -> ObjectiveEvaluation:
    status: ObjectiveStatus = "completed" if progress >= target else "failed"
    reason = "completed" if status == "completed" else objective.failure_reason
    return ObjectiveEvaluation(objective=objective, status=status, reason=reason, progress_value=progress, target_value=target, score_delta=objective_score_delta(objective, status, score_rules))


def _result_type(evaluations: tuple[ObjectiveEvaluation, ...], state: RunState) -> ResultType:
    required = tuple(evaluation for evaluation in evaluations if evaluation.objective.required)
    primary = tuple(evaluation for evaluation in required if evaluation.objective.objective_type != "survive_expedition")
    if state.clock.day > state.clock.max_days:
        return "failure"
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


def _failure_kind(failure_reasons: list[str], result_type: ResultType) -> FailureKind:
    if result_type != "failure":
        return "none"
    if "health_zero" in failure_reasons:
        return "death_or_incapacitated"
    if "primary_objective_failed" in failure_reasons:
        return "objective_failed"
    if "return_failed" in failure_reasons or "report_failed" in failure_reasons:
        return "return_failed"
    if "max_day_exceeded" in failure_reasons or "max_turn_exceeded" in failure_reasons:
        return "time_expired"
    if "reputation_collapse" in failure_reasons:
        return "reputation_collapse"
    if "recovery_failed" in failure_reasons or "rescue_failed" in failure_reasons:
        return "quest_specific_failure"
    return "unknown"


def _character_outcome(state: RunState) -> CharacterOutcome:
    return "incapacitated" if state.status.get("health", 0) <= 0 else "alive"


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


def _selected_ending(report: JsonMap, state: RunState, bundle: ProjectData) -> JsonMap:
    for ending in bundle.endings.values():
        if _ending_matches(ending.condition, report, state):
            return {"id": ending.id, "name": ending.name, "condition": dict(ending.condition)}
    return {}


def _ending_matches(condition: JsonMap, report: JsonMap, state: RunState) -> bool:
    return (
        _uses_supported_condition_keys(condition, state)
        and _matches_value(condition, "result_type", str(report.get("result_type", "")))
        and _matches_value(condition, "failure_kind", str(report.get("failure_kind", "")))
        and _matches_value(condition, "character_outcome", str(report.get("character_outcome", "")))
        and _matches_value(condition, "reward_status", str(report.get("reward_status", "")))
        and _matches_bounds(condition, "score", int(report.get("score", 0)))
        and _matches_bounds(condition, "reputation", state.status.get("reputation", 0))
        and _matches_bounds(condition, "money", state.status.get("money", 0))
        and _matches_status_bounds(condition, state)
        and _matches_count(condition, "clues", len(state.clues))
        and _matches_count(condition, "omens", len(state.omens))
        and _matches_collection(condition, "required_any_clues", state.clues, any)
        and _matches_collection(condition, "required_all_clues", state.clues, all)
        and _matches_collection(condition, "required_any_omens", state.omens, any)
        and _matches_collection(condition, "required_all_omens", state.omens, all)
        and _matches_collection(condition, "forbidden_omens", state.omens, _none)
        and _matches_collection(condition, "required_any_items", state.inventory, any)
        and _matches_collection(condition, "required_all_items", state.inventory, all)
        and _matches_collection(condition, "required_partial_reasons", _string_list(report.get("partial_reasons", [])), any)
        and _matches_collection(condition, "required_failure_reasons", _string_list(report.get("failure_reasons", [])), any)
        and _matches_collection(condition, "required_completed_objectives", _string_list(report.get("completed_objectives", [])), any)
        and _matches_collection(condition, "required_failed_objectives", _string_list(report.get("failed_objectives", [])), any)
        and _matches_target_turns(condition, state)
        and _matches_status_conditions(condition, state)
    )


def _uses_supported_condition_keys(condition: JsonMap, state: RunState) -> bool:
    supported = {
        "result_type",
        "failure_kind",
        "character_outcome",
        "reward_status",
        "min_score",
        "max_score",
        "min_reputation",
        "max_reputation",
        "min_money",
        "max_money",
        "min_clues",
        "max_clues",
        "min_omens",
        "max_omens",
        "required_any_clues",
        "required_all_clues",
        "required_any_omens",
        "required_all_omens",
        "forbidden_omens",
        "required_any_items",
        "required_all_items",
        "required_partial_reasons",
        "required_failure_reasons",
        "required_completed_objectives",
        "required_failed_objectives",
        "target_turns_reached",
    }
    return all(key in supported or key in state.status or _is_status_bound_key(key, state) for key in condition)


def _is_status_bound_key(key: str, state: RunState) -> bool:
    return any(key in {f"min_{status_id}", f"max_{status_id}"} for status_id in state.status)


def _matches_value(condition: JsonMap, key: str, value: str) -> bool:
    expected = condition.get(key)
    if expected is None:
        return True
    if isinstance(expected, list):
        return value in {str(item) for item in expected}
    return value == str(expected)


def _matches_bounds(condition: JsonMap, key: str, value: int) -> bool:
    minimum = condition.get(f"min_{key}")
    maximum = condition.get(f"max_{key}")
    if minimum is not None and value < int(minimum):
        return False
    return not (maximum is not None and value > int(maximum))


def _matches_count(condition: JsonMap, key: str, value: int) -> bool:
    return _matches_bounds(condition, key, value)


def _matches_status_bounds(condition: JsonMap, state: RunState) -> bool:
    return all(_matches_bounds(condition, status_id, value) for status_id, value in state.status.items())


def _matches_collection(condition: JsonMap, key: str, values: tuple[str, ...], matcher: object) -> bool:
    expected = _string_list(condition.get(key, []))
    if not expected:
        return True
    value_set = set(values)
    matches = [item in value_set for item in expected]
    if matcher is any:
        return any(matches)
    if matcher is all:
        return all(matches)
    return _none(matches)


def _matches_target_turns(condition: JsonMap, state: RunState) -> bool:
    expected = condition.get("target_turns_reached")
    if expected is None:
        return True
    reached = state.clock.turn >= state.clock.max_turns
    return reached if bool(expected) else not reached


def _matches_status_conditions(condition: JsonMap, state: RunState) -> bool:
    for key, raw_bounds in condition.items():
        if key not in state.status:
            continue
        if not isinstance(raw_bounds, dict):
            return False
        minimum = raw_bounds.get("min")
        maximum = raw_bounds.get("max")
        value = state.status.get(key, 0)
        if minimum is not None and value < int(minimum):
            return False
        if maximum is not None and value > int(maximum):
            return False
    return True


def _none(values: list[bool]) -> bool:
    return not any(values)


def _string_list(value: object) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return ()


def _dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
