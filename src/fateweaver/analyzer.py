from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from fateweaver.models import JsonMap


@dataclass(slots=True)
class _MetricBucket:
    meaningful_choice_count: int = 0
    item_unlocked_choice_count: int = 0
    bad_tradeoff_count: int = 0
    restart_scores: list[int] = field(default_factory=list)
    woven_scores: list[int] = field(default_factory=list)
    failed_interesting: int = 0
    selected_choice_counts: dict[str, int] = field(default_factory=dict)

    def add_turn(self, turn: JsonMap) -> None:
        influenced_by = tuple(turn.get("influenced_by", []))
        if influenced_by:
            self.meaningful_choice_count += 1
        if any(str(value).startswith("item:") for value in influenced_by):
            self.item_unlocked_choice_count += 1
        if turn.get("expected_risk") == "high" or int(turn.get("regret_score", 0)) >= 4:
            self.bad_tradeoff_count += 1
        selected_choice_id = str(turn.get("selected_choice_id", ""))
        if selected_choice_id:
            self.selected_choice_counts[selected_choice_id] = self.selected_choice_counts.get(selected_choice_id, 0) + 1

    def add_summary(self, summary: JsonMap) -> None:
        restart = int(summary.get("restart_intent_score", 0))
        woven = int(summary.get("player_woven_score", 0))
        self.restart_scores.append(restart)
        self.woven_scores.append(woven)
        if summary.get("run_failed") is True and restart >= 4:
            self.failed_interesting += 1

    def to_json(self) -> JsonMap:
        most_repeated_choice_id, most_repeated_choice_count = _most_repeated_choice(self.selected_choice_counts)
        selected_total = sum(self.selected_choice_counts.values())
        return {
            "runs_analyzed": len(self.restart_scores),
            "meaningful_choice_count": self.meaningful_choice_count,
            "item_unlocked_choice_count": self.item_unlocked_choice_count,
            "bad_tradeoff_count": self.bad_tradeoff_count,
            "choice_diversity_count": len(self.selected_choice_counts),
            "most_repeated_choice_id": most_repeated_choice_id,
            "most_repeated_choice_count": most_repeated_choice_count,
            "repeat_bias_ratio": _ratio(most_repeated_choice_count, selected_total),
            "restart_intent_score_avg": _average(self.restart_scores),
            "run_failed_but_interesting_count": self.failed_interesting,
            "player_woven_score_avg": _average(self.woven_scores),
        }


def analyze_logs(logs_dir: Path) -> JsonMap:
    paths = sorted(path for path in logs_dir.glob("*.json") if path.is_file())
    if not paths:
        raise ValueError("no run logs found")
    totals = _MetricBucket()
    profile_buckets: dict[str, _MetricBucket] = {}
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            log = json.load(handle)
        profile = str(log.get("profile", "unknown"))
        profile_bucket = profile_buckets.setdefault(profile, _MetricBucket())
        for turn in log.get("turns", []):
            totals.add_turn(turn)
            profile_bucket.add_turn(turn)
        summary = log.get("run_summary", {})
        totals.add_summary(summary)
        profile_bucket.add_summary(summary)
    result = totals.to_json()
    result["profile_metrics"] = {profile: bucket.to_json() for profile, bucket in sorted(profile_buckets.items())}
    return result


def _average(values: list[int]) -> float:
    return round(sum(values) / len(values), 2)


def _most_repeated_choice(choice_counts: dict[str, int]) -> tuple[str, int]:
    if not choice_counts:
        return "", 0
    return max(sorted(choice_counts.items()), key=lambda item: item[1])


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 2)
