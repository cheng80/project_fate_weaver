from __future__ import annotations

import json
from pathlib import Path


def analyze_logs(logs_dir: Path) -> dict[str, float | int]:
    paths = sorted(path for path in logs_dir.glob("*.json") if path.is_file())
    if not paths:
        raise ValueError("no run logs found")
    meaningful_choice_count = 0
    item_unlocked_choice_count = 0
    bad_tradeoff_count = 0
    restart_scores: list[int] = []
    woven_scores: list[int] = []
    failed_interesting = 0
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            log = json.load(handle)
        for turn in log.get("turns", []):
            influenced_by = tuple(turn.get("influenced_by", []))
            if influenced_by:
                meaningful_choice_count += 1
            if any(str(value).startswith("item:") for value in influenced_by):
                item_unlocked_choice_count += 1
            if turn.get("expected_risk") == "high" or int(turn.get("regret_score", 0)) >= 4:
                bad_tradeoff_count += 1
        summary = log.get("run_summary", {})
        restart = int(summary.get("restart_intent_score", 0))
        woven = int(summary.get("player_woven_score", 0))
        restart_scores.append(restart)
        woven_scores.append(woven)
        if summary.get("run_failed") is True and restart >= 4:
            failed_interesting += 1
    return {
        "runs_analyzed": len(paths),
        "meaningful_choice_count": meaningful_choice_count,
        "item_unlocked_choice_count": item_unlocked_choice_count,
        "bad_tradeoff_count": bad_tradeoff_count,
        "restart_intent_score_avg": _average(restart_scores),
        "run_failed_but_interesting_count": failed_interesting,
        "player_woven_score_avg": _average(woven_scores),
    }


def _average(values: list[int]) -> float:
    return round(sum(values) / len(values), 2)
