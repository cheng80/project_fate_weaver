from __future__ import annotations

from typing import Final, Literal, assert_never

from fateweaver.gameplay_p0_models import QuestObjective
from fateweaver.models import JsonMap

ObjectiveStatus = Literal["completed", "partial", "failed"]

DEFAULT_OBJECTIVE_SCORING: Final[dict[str, int]] = {
    "completed_required": 10,
    "completed_optional": 10,
    "partial_required": 5,
    "partial_optional": 5,
    "failed_required": -10,
    "failed_optional": 0,
    "survival_failed": -30,
    "return_failed": -20,
}


def objective_score_delta(objective: QuestObjective, status: ObjectiveStatus, score_rules: JsonMap) -> int:
    rules = _objective_scoring(score_rules)
    match status:
        case "completed":
            key = "completed_required" if objective.required else "completed_optional"
            return rules[key] * objective.reward_weight
        case "partial":
            key = "partial_required" if objective.required else "partial_optional"
            return rules[key] * objective.reward_weight
        case "failed":
            return _failed_score_delta(objective, rules)
        case unreachable:
            assert_never(unreachable)


def _failed_score_delta(objective: QuestObjective, rules: dict[str, int]) -> int:
    if not objective.required:
        return rules["failed_optional"] * objective.reward_weight
    match objective.objective_type:
        case "survive_expedition":
            return rules["survival_failed"]
        case "return_to_region":
            return rules["return_failed"]
        case "collect_item" | "keep_resource_at_least" | "discover_clue" | "optional_action":
            return rules["failed_required"] * objective.reward_weight
        case unreachable:
            assert_never(unreachable)


def _objective_scoring(score_rules: JsonMap) -> dict[str, int]:
    raw = score_rules.get("objective_scoring", {})
    if not isinstance(raw, dict):
        return dict(DEFAULT_OBJECTIVE_SCORING)
    rules = dict(DEFAULT_OBJECTIVE_SCORING)
    rules.update({str(key): int(value) for key, value in raw.items()})
    return rules
