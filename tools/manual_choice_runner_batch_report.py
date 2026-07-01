from __future__ import annotations


def render_batch_report(summary: dict) -> str:
    lines = [
        "# Subagent Auto-Play Batch Report",
        "",
        "## Batch Summary",
        f"- seeds: {', '.join(str(seed) for seed in summary['seeds'])}",
        f"- agents: {', '.join(summary['agents'])}",
        f"- max turns safety cap: {summary['max_turns']}",
        f"- total runs: {summary['total_runs']}",
        f"- crash count: {summary['crash_count']}",
        f"- invariant violation count: {summary['invariant_violation_count']}",
        f"- same turn duplicate count: {summary['same_turn_duplicate_count']}",
        f"- outcome counts: {summary['outcome_counts']}",
        f"- stop reason counts: {summary['stop_reason_counts']}",
        "",
        "## Quest Lifecycle Summary",
        f"- quest completion count: {summary['quest_completion_count']}",
        f"- reward granted count: {summary['reward_granted_count']}",
        f"- reward missing after success count: {summary['reward_missing_after_success_count']}",
        f"- duplicate reward detected count: {summary['duplicate_reward_detected_count']}",
        f"- duplicate reward prevention count: {summary['duplicate_reward_prevention_count']}",
        f"- next quest transition count: {summary['next_quest_transition_count']}",
        f"- run complete count: {summary['run_complete_count']}",
        f"- no next quest count: {summary['no_next_quest_count']}",
        f"- completion blocked by min turns count: {summary['completion_blocked_by_min_turns_count']}",
        f"- completed quest dragged to max turn count: {summary['completed_quest_dragged_to_max_turn_count']}",
        f"- completion turn distribution: {summary['completion_turn_distribution']}",
        "",
        "## Agent Summary",
    ]
    for agent, data in summary["agent_summary"].items():
        lines.append(
            f"- {agent}: runs={data['runs']} avg_turns={data['average_turns']:.1f} "
            f"warnings={data['warning_count']} stop_reasons={data['stop_reasons']}"
        )
    lines.extend(["", "## Run Matrix"])
    for run in summary["runs"]:
        lines.append(
            f"- seed {run['seed']} / {run['agent_id']}: outcome={run['result_type']} turns={run['turn_count']} "
            f"stop_reason={run['stop_reason']} quest_complete={run.get('quest_completion_count', 0)} "
            f"reward={run.get('reward_granted_count', 0)} run_complete={run.get('run_complete_count', 0)} "
            f"no_next_quest={run.get('no_next_quest_count', 0)} warnings={run['warning_count']}"
        )
    lines.extend(["", "## Notable Cases"])
    notable = [run for run in summary["runs"] if run["crashed"] or run["warning_count"]]
    lines.extend(f"- seed {run['seed']} / {run['agent_id']}: {run['warnings']}" for run in notable)
    if not notable:
        lines.append("- none")
    return "\n".join(lines) + "\n"
