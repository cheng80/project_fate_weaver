from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Final

from fateweaver.models import ChoiceSeen, JsonMap, JsonValue, StatusMap


VALID_AUTOPLAYER_PROFILES: Final[tuple[str, ...]] = (
    "first_available",
    "balanced",
    "safe_leaning",
    "greedy_leaning",
    "curious_leaning",
    "desperate",
)

_RISK_RANK: Final[dict[str, int]] = {"none": 0, "low": 1, "medium": 2, "high": 3}


@dataclass(frozen=True, slots=True)
class ScoreWeights:
    safety_weight: float
    reward_weight: float
    item_weight: float
    risk_weight: float
    survival_weight: float
    novelty_weight: float
    curse_avoidance_weight: float


@dataclass(frozen=True, slots=True)
class ChoiceSelection:
    choice: ChoiceSeen
    reason: str
    selected_choice_score: JsonMap
    choice_scores: tuple[JsonMap, ...]


@dataclass(frozen=True, slots=True)
class ChoiceScorer:
    profile: str
    state: StatusMap
    seed: int
    turn: int

    def score_choice(self, choice: ChoiceSeen) -> JsonMap:
        weights = self._weights()
        safety_score = _safety_score(choice)
        reward_score = _reward_score(choice)
        item_usage_score = _item_usage_score(choice)
        risk_score = float(_risk_rank(choice))
        survival_need_score = _survival_need_score(choice, self.state)
        novelty_score = _novelty_score(choice)
        curse_penalty = _curse_penalty(choice)
        final_score = (
            safety_score * weights.safety_weight
            + reward_score * weights.reward_weight
            + item_usage_score * weights.item_weight
            + risk_score * weights.risk_weight
            + survival_need_score * weights.survival_weight
            + novelty_score * weights.novelty_weight
            - curse_penalty * weights.curse_avoidance_weight
        )
        return {
            "choice_id": choice.choice_id,
            "safety_score": round(safety_score, 3),
            "reward_score": round(reward_score, 3),
            "item_usage_score": round(item_usage_score, 3),
            "risk_score": round(risk_score, 3),
            "survival_need_score": round(survival_need_score, 3),
            "novelty_score": round(novelty_score, 3),
            "curse_penalty": round(curse_penalty, 3),
            "final_score": round(final_score, 3),
            "tie_breaker": _tie_breaker(self.seed, self.turn, self.profile, choice.choice_id),
        }

    def select(self, choices_seen: tuple[ChoiceSeen, ...]) -> ChoiceSelection:
        eligible = tuple(choice for choice in choices_seen if choice.available and not choice.hidden)
        if not eligible:
            raise ValueError("No available choices")
        choice_scores = tuple(self.score_choice(choice) for choice in eligible)
        selected_score = max(choice_scores, key=lambda score: (float(score["final_score"]), int(score["tie_breaker"])))
        selected = _choice_by_id(eligible, str(selected_score["choice_id"]))
        return ChoiceSelection(selected, _selection_reason(self.profile, selected_score), selected_score, choice_scores)

    def _weights(self) -> ScoreWeights:
        weights = _base_weights(self.profile)
        if self.profile != "desperate":
            return weights
        if self.state.get("health", 10) > 3 and self.state.get("food", 10) > 2:
            return weights
        return ScoreWeights(
            weights.safety_weight,
            weights.reward_weight,
            weights.item_weight,
            weights.risk_weight + 0.8,
            weights.survival_weight + 2.0,
            weights.novelty_weight,
            weights.curse_avoidance_weight,
        )


def select_weighted_choice(
    choices_seen: tuple[ChoiceSeen, ...],
    policy: str = "auto",
    profile: str = "balanced",
    state: StatusMap | None = None,
    seed: int = 0,
    turn: int = 0,
) -> ChoiceSelection:
    if policy != "auto":
        raise ValueError(f"Unsupported choice policy: {policy}")
    eligible = tuple(choice for choice in choices_seen if choice.available and not choice.hidden)
    if not eligible:
        raise ValueError("No available choices")
    if profile not in VALID_AUTOPLAYER_PROFILES:
        raise ValueError(f"Unsupported autoplayer profile: {profile}")
    match profile:
        case "first_available":
            selected = eligible[0]
            score = ChoiceScorer("balanced", state or {}, seed, turn).score_choice(selected)
            score["profile"] = "first_available"
            return ChoiceSelection(selected, "profile=first_available: selected first available non-hidden choice", score, (score,))
        case "balanced" | "safe_leaning" | "greedy_leaning" | "curious_leaning" | "desperate":
            return ChoiceScorer(profile, state or {}, seed, turn).select(choices_seen)
        case unreachable:
            raise ValueError(f"Unsupported autoplayer profile: {unreachable}")


def _base_weights(profile: str) -> ScoreWeights:
    return {
        "balanced": ScoreWeights(1.0, 1.0, 1.0, 0.45, 1.0, 0.7, 1.0),
        "safe_leaning": ScoreWeights(1.6, 0.7, 0.7, 0.1, 1.5, 0.4, 1.7),
        "greedy_leaning": ScoreWeights(0.7, 1.9, 1.1, 0.45, 0.7, 0.5, 0.7),
        "curious_leaning": ScoreWeights(0.75, 0.9, 1.25, 0.75, 0.7, 1.8, 0.7),
        "desperate": ScoreWeights(0.8, 0.9, 0.7, 1.0, 1.5, 0.5, 0.6),
    }[profile]


def _safety_score(choice: ChoiceSeen) -> float:
    return float(4 - _risk_rank(choice)) + max(0, _status_delta(choice, "health")) + max(0, -_status_delta(choice, "curse"))


def _reward_score(choice: ChoiceSeen) -> float:
    return float(max(0, _status_delta(choice, "money")) * 2 + max(0, _status_delta(choice, "food")) + max(0, _status_delta(choice, "reputation")) + _added_item_count(choice) * 2)


def _item_usage_score(choice: ChoiceSeen) -> float:
    score = 0.0
    if _has_influence(choice, "item:"):
        score += 4.0
    if _has_influence(choice, "status:") or _has_influence(choice, "run_tag:"):
        score += 1.0
    return score


def _survival_need_score(choice: ChoiceSeen, state: StatusMap) -> float:
    score = 0.0
    if state.get("health", 10) <= 3:
        score += max(0, _status_delta(choice, "health")) * 3
        score -= min(0, _status_delta(choice, "health")) * 2
    if state.get("food", 10) <= 2:
        score += max(0, _status_delta(choice, "food")) * 2
        score -= min(0, _status_delta(choice, "food"))
    return score


def _novelty_score(choice: ChoiceSeen) -> float:
    score = 0.0
    if choice.choice_type in {"tool_use", "status_based", "lore", "mystery", "investigate"}:
        score += 2.0
    if _added_item_count(choice) > 0:
        score += 2.0
    if _string_list(choice.result.get("add_run_tag", [])):
        score += 2.0
    if choice.influenced_by:
        score += 1.0
    return score


def _curse_penalty(choice: ChoiceSeen) -> float:
    return float(max(0, _status_delta(choice, "curse")) * 3)


def _risk_rank(choice: ChoiceSeen) -> int:
    return _RISK_RANK.get(choice.expected_risk, 2)


def _has_influence(choice: ChoiceSeen, prefix: str) -> bool:
    return any(value.startswith(prefix) for value in choice.influenced_by)


def _status_delta(choice: ChoiceSeen, key: str) -> int:
    raw_status = _as_mapping(choice.result.get("status", {}))
    raw_delta = raw_status.get(key, 0)
    try:
        return int(raw_delta)
    except (TypeError, ValueError):
        return 0


def _added_item_count(choice: ChoiceSeen) -> int:
    value = choice.result.get("add_item", [])
    if isinstance(value, list):
        return len(value)
    return 0


def _selection_reason(profile: str, score: JsonMap) -> str:
    return (
        f"profile={profile}: final_score={score['final_score']} "
        f"(safety={score['safety_score']}, reward={score['reward_score']}, item={score['item_usage_score']}, "
        f"risk={score['risk_score']}, survival={score['survival_need_score']}, novelty={score['novelty_score']}, "
        f"curse_penalty={score['curse_penalty']})"
    )


def _choice_by_id(choices: tuple[ChoiceSeen, ...], choice_id: str) -> ChoiceSeen:
    for choice in choices:
        if choice.choice_id == choice_id:
            return choice
    raise ValueError(f"Unknown choice: {choice_id}")


def _tie_breaker(seed: int, turn: int, profile: str, choice_id: str) -> int:
    digest = sha256(f"{seed}:{turn}:{profile}:{choice_id}".encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def _string_list(value: JsonValue) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return ()


def _as_mapping(value: JsonValue) -> JsonMap:
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    return {}
