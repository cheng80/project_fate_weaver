from __future__ import annotations


def stale_previous_quest_card_count(trace: list[dict]) -> int:
    active_previous_quests: list[str] = []
    count = 0
    for entry in trace:
        completed = str(entry.get("completed_quest_id", ""))
        if entry.get("quest_transition") and completed:
            active_previous_quests.append(completed)
            continue
        for card in entry.get("presented_card_relevance", []):
            card_quests = set(card.get("card_quest_ids", []))
            if any(quest_id in card_quests for quest_id in active_previous_quests):
                count += 1
    return count


def seed_agent_matrix(runs: list[dict]) -> list[dict]:
    return [
        {
            "seed": run["seed"],
            "agent_id": run["agent_id"],
            "outcome": run["result_type"],
            "stop_reason": run["stop_reason"],
            "turns": run["turn_count"],
            "completion_turn": run.get("completion_turns", [None])[0] if run.get("completion_turns") else None,
            "quest_success": int(run.get("quest_completion_count", 0)) > 0,
            "reward_granted": int(run.get("reward_granted_count", 0)) > 0,
            "run_complete": int(run.get("run_complete_count", 0)) > 0,
            "no_next_quest": int(run.get("no_next_quest_count", 0)) > 0,
            "warning_count": run["warning_count"],
            "invariant_status": "fail" if any("invariant" in warning for warning in run["warnings"]) else "pass",
            "min_turn_blocked": int(run.get("completion_blocked_by_min_turns_count", 0)) > 0,
            "stale_previous_quest_cards": int(run.get("stale_previous_quest_card_after_transition_count", 0)),
        }
        for run in runs
    ]
