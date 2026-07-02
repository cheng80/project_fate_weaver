from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    from .manual_choice_runner_agents import policy_ids
    from .manual_choice_runner_batch_metrics import seed_agent_matrix, stale_previous_quest_card_count
    from .manual_choice_runner_batch_report import render_batch_report
except ImportError:
    from manual_choice_runner_agents import policy_ids
    from manual_choice_runner_batch_metrics import seed_agent_matrix, stale_previous_quest_card_count
    from manual_choice_runner_batch_report import render_batch_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--seeds", required=True)
    parser.add_argument("--agents", default=",".join(policy_ids()))
    parser.add_argument("--max-turns", type=int, default=25)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report-md")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    seeds = _parse_seeds(args.seeds)
    agents = _parse_agents(args.agents)
    runs = []
    for seed in seeds:
        for agent in agents:
            runs.append(_run_agent(project_root, args.scenario, output_dir, seed, agent, args.max_turns))
    summary = _batch_summary(seeds, agents, args.max_turns, runs)
    summary_path = output_dir / "batch_summary.json"
    report_path = output_dir / "batch_report.md"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = render_batch_report(summary)
    report_path.write_text(report, encoding="utf-8")
    print(f"MANUAL_BATCH_SUMMARY: {summary_path}")
    print(f"MANUAL_BATCH_REPORT: {report_path}")
    if args.report_md:
        requested_report_path = Path(args.report_md)
        requested_report_path.parent.mkdir(parents=True, exist_ok=True)
        requested_report_path.write_text(report, encoding="utf-8")
        print(f"MANUAL_BATCH_REPORT_MD: {requested_report_path}")
    return 0 if not any(run["crashed"] for run in runs) else 1


def _run_agent(project_root: Path, scenario: str, output_dir: Path, seed: int, agent: str, max_turns: int) -> dict:
    run_dir = output_dir / f"seed_{seed}_{agent}"
    completed = subprocess.run(
        [
            sys.executable,
            str(project_root / "tools/manual_choice_runner.py"),
            "--scenario",
            scenario,
            "--seed",
            str(seed),
            "--agent-policy",
            agent,
            "--max-turns",
            str(max_turns),
            "--output-dir",
            str(run_dir),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return {
            "seed": seed,
            "agent_id": agent,
            "crashed": True,
            "turn_count": 0,
            "result_type": "error",
            "stop_reason": "runner_error",
            "manual_stop_reason": "runner_error",
            "warning_count": 1,
            "warnings": [completed.stderr.strip()],
            "same_turn_duplicate_count": 0,
            "off_quest_warning_count": 0,
            "fallback_warning_count": 0,
            "completion_turns": [],
            "next_quest_onboarding_count": 0,
            "stale_previous_quest_card_after_transition_count": 0,
            "run_dir": str(run_dir),
        }
    summary = json.loads((run_dir / f"manual_seed_{seed}_summary.json").read_text(encoding="utf-8"))
    trace = json.loads((run_dir / f"manual_seed_{seed}_choice_trace.json").read_text(encoding="utf-8"))
    warning_details = _trace_warning_details(trace)
    lifecycle = _lifecycle_counts(trace)
    stale_count = stale_previous_quest_card_count(trace)
    return {
        "seed": seed,
        "agent_id": agent,
        "crashed": False,
        "turn_count": int(summary["turn_count"]),
        "result_type": str(summary.get("result_type", "unknown")),
        "stop_reason": str(summary.get("stop_reason", "unknown")),
        "manual_stop_reason": str(summary.get("manual_stop_reason", "unknown")),
        "ending": summary.get("ending"),
        "selected_indexes": summary.get("selected_indexes", []),
        "warning_count": len(warning_details["warnings"]),
        **warning_details,
        **lifecycle,
        "stale_previous_quest_card_after_transition_count": stale_count,
        "run_dir": str(run_dir),
    }


def _batch_summary(seeds: list[int], agents: list[str], max_turns: int, runs: list[dict]) -> dict:
    agent_summary = {}
    for agent in agents:
        agent_runs = [run for run in runs if run["agent_id"] == agent]
        total_turns = sum(int(run["turn_count"]) for run in agent_runs)
        completion_turns = [turn for run in agent_runs for turn in run.get("completion_turns", [])]
        agent_summary[agent] = {
            "runs": len(agent_runs),
            "average_turns": total_turns / len(agent_runs) if agent_runs else 0,
            "average_completion_turn": _average(completion_turns),
            "final_outcomes": dict(Counter(str(run["result_type"]) for run in agent_runs)),
            "stop_reasons": dict(Counter(str(run["stop_reason"]) for run in agent_runs)),
            "warning_count": sum(int(run["warning_count"]) for run in agent_runs),
            "off_quest_warning_count": sum(int(run.get("off_quest_warning_count", 0)) for run in agent_runs),
            "fallback_warning_count": sum(int(run.get("fallback_warning_count", 0)) for run in agent_runs),
            "invariant_violation_count": _count_warnings(agent_runs, "invariant"),
            "crash_count": sum(1 for run in agent_runs if run["crashed"]),
            "quest_completion_count": sum(int(run.get("quest_completion_count", 0)) for run in agent_runs),
            "reward_granted_count": sum(int(run.get("reward_granted_count", 0)) for run in agent_runs),
            "run_complete_count": sum(int(run.get("run_complete_count", 0)) for run in agent_runs),
            "next_quest_onboarding_count": sum(int(run.get("next_quest_onboarding_count", 0)) for run in agent_runs),
            "stale_previous_quest_card_after_transition_count": sum(int(run.get("stale_previous_quest_card_after_transition_count", 0)) for run in agent_runs),
            "completion_blocked_by_min_turns_count": sum(int(run.get("completion_blocked_by_min_turns_count", 0)) for run in agent_runs),
        }
    completion_turns = [turn for run in runs for turn in run.get("completion_turns", [])]
    turn_counts = [int(run["turn_count"]) for run in runs]
    quest_success_count = sum(int(run.get("quest_completion_count", 0)) for run in runs)
    reward_granted_count = sum(int(run.get("reward_granted_count", 0)) for run in runs)
    run_complete_count = sum(int(run.get("run_complete_count", 0)) for run in runs)
    return {
        "seeds": seeds,
        "agents": agents,
        "max_turns": max_turns,
        "total_runs": len(runs),
        "crash_count": sum(1 for run in runs if run["crashed"]),
        "invariant_violation_count": _count_warnings(runs, "invariant"),
        "same_turn_duplicate_count": _count_warnings(runs, "duplicate presented cards"),
        "clean_end_count": sum(1 for run in runs if not run["crashed"] and run["stop_reason"] in {"completed", "run_complete"}),
        "clean_error_count": sum(1 for run in runs if not run["crashed"] and run["stop_reason"] in {"max_turn_reached", "choice_sequence_exhausted", "manual_error", "run_error"}),
        "max_turn_reached_count": sum(1 for run in runs if run["stop_reason"] == "max_turn_reached"),
        "quest_completion_count": quest_success_count,
        "quest_success_missing_count": sum(1 for run in runs if not run["crashed"] and int(run.get("quest_completion_count", 0)) == 0),
        "reward_granted_count": reward_granted_count,
        "reward_missing_after_success_count": sum(1 for run in runs if int(run.get("quest_completion_count", 0)) > int(run.get("reward_granted_count", 0))),
        "duplicate_reward_detected_count": sum(max(0, int(run.get("reward_granted_count", 0)) - int(run.get("quest_completion_count", 0))) for run in runs),
        "duplicate_reward_prevention_count": sum(int(run.get("duplicate_reward_prevention_count", 0)) for run in runs),
        "next_quest_transition_count": sum(int(run.get("next_quest_transition_count", 0)) for run in runs),
        "run_complete_count": run_complete_count,
        "next_quest_onboarding_count": sum(int(run.get("next_quest_onboarding_count", 0)) for run in runs),
        "no_next_quest_count": sum(int(run.get("no_next_quest_count", 0)) for run in runs),
        "stale_previous_quest_card_after_transition_count": sum(int(run.get("stale_previous_quest_card_after_transition_count", 0)) for run in runs),
        "completion_blocked_by_min_turns_count": sum(int(run.get("completion_blocked_by_min_turns_count", 0)) for run in runs),
        "completed_quest_dragged_to_max_turn_count": sum(1 for run in runs if int(run.get("quest_completion_count", 0)) > 0 and run["stop_reason"] == "max_turn_reached"),
        "average_completion_turn": _average(completion_turns),
        "min_completion_turn": min(completion_turns) if completion_turns else None,
        "max_completion_turn": max(completion_turns) if completion_turns else None,
        "completion_turn_distribution": dict(Counter(str(turn) for turn in completion_turns)),
        "average_turns": _average(turn_counts),
        "min_turns": min(turn_counts) if turn_counts else 0,
        "max_turns_observed": max(turn_counts) if turn_counts else 0,
        "outcome_counts": dict(Counter(str(run["result_type"]) for run in runs)),
        "stop_reason_counts": dict(Counter(str(run["stop_reason"]) for run in runs)),
        "off_quest_warning_count": sum(int(run.get("off_quest_warning_count", 0)) for run in runs),
        "fallback_warning_count": sum(int(run.get("fallback_warning_count", 0)) for run in runs),
        "agent_summary": agent_summary,
        "seed_agent_matrix": seed_agent_matrix(runs),
        "runs": runs,
    }


def _trace_warning_details(trace: list[dict]) -> dict:
    warnings = []
    off_quest_warning_count = 0
    fallback_warning_count = 0
    same_turn_duplicate_count = 0
    for entry in trace:
        cards = entry.get("presented_card_ids", [])
        if len(cards) != 3:
            warnings.append(f"turn {entry.get('turn')}: 3-card invariant violated")
        if len(cards) != len(set(cards)):
            same_turn_duplicate_count += 1
            warnings.append(f"turn {entry.get('turn')}: duplicate presented cards")
        relevance = entry.get("presented_card_relevance", [])
        off_quest = [card.get("card_id") for card in relevance if card.get("off_quest_candidate")]
        fallback = [card.get("card_id") for card in relevance if card.get("fallback_reason")]
        if off_quest:
            off_quest_warning_count += 1
            warnings.append(f"turn {entry.get('turn')}: off-quest {off_quest}")
        if fallback:
            fallback_warning_count += 1
            warnings.append(f"turn {entry.get('turn')}: fallback {fallback}")
    return {
        "warnings": warnings,
        "off_quest_warning_count": off_quest_warning_count,
        "fallback_warning_count": fallback_warning_count,
        "same_turn_duplicate_count": same_turn_duplicate_count,
    }


def _lifecycle_counts(trace: list[dict]) -> dict[str, int]:
    completion_turns = [int(entry.get("turn", 0)) for entry in trace if entry.get("quest_success")]
    return {
        "quest_completion_count": sum(1 for entry in trace if entry.get("quest_success")),
        "reward_granted_count": sum(1 for entry in trace if entry.get("reward_granted")),
        "duplicate_reward_prevention_count": sum(1 for entry in trace if entry.get("duplicate_reward_prevented")),
        "next_quest_transition_count": sum(1 for entry in trace if entry.get("next_quest_id")),
        "next_quest_onboarding_count": sum(1 for entry in trace if entry.get("next_quest_onboarding")),
        "run_complete_count": sum(1 for entry in trace if entry.get("run_complete")),
        "no_next_quest_count": sum(1 for entry in trace if entry.get("no_next_quest")),
        "completion_blocked_by_min_turns_count": sum(1 for entry in trace if entry.get("completion_blocked_by_min_turns")),
        "completion_turns": completion_turns,
    }


def _parse_seeds(raw: str) -> list[int]:
    seeds = []
    for part in (part.strip() for part in raw.split(",") if part.strip()):
        if "-" in part:
            start, end = (int(value) for value in part.split("-", 1))
            step = 1 if start <= end else -1
            seeds.extend(range(start, end + step, step))
        else:
            seeds.append(int(part))
    return seeds


def _parse_agents(raw: str) -> list[str]:
    requested = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = sorted(set(requested) - set(policy_ids()))
    if unknown:
        raise ValueError(f"unknown agent policies: {', '.join(unknown)}")
    return requested


def _average(values: list[int]) -> float:
    return sum(values) / len(values) if values else 0.0


def _count_warnings(runs: list[dict], needle: str) -> int:
    return sum(1 for run in runs for warning in run["warnings"] if needle in warning)


if __name__ == "__main__":
    raise SystemExit(main())
