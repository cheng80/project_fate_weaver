from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    from .manual_choice_runner_agents import policy_ids
except ImportError:
    from manual_choice_runner_agents import policy_ids


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--seeds", required=True)
    parser.add_argument("--agents", default=",".join(policy_ids()))
    parser.add_argument("--max-turns", type=int, default=25)
    parser.add_argument("--output-dir", required=True)
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
    summary = _batch_summary(seeds, agents, runs)
    summary_path = output_dir / "batch_summary.json"
    report_path = output_dir / "batch_report.md"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(_render_batch_report(summary), encoding="utf-8")
    print(f"MANUAL_BATCH_SUMMARY: {summary_path}")
    print(f"MANUAL_BATCH_REPORT: {report_path}")
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
            "run_dir": str(run_dir),
        }
    summary = json.loads((run_dir / f"manual_seed_{seed}_summary.json").read_text(encoding="utf-8"))
    trace = json.loads((run_dir / f"manual_seed_{seed}_choice_trace.json").read_text(encoding="utf-8"))
    warnings = _trace_warnings(trace)
    lifecycle = _lifecycle_counts(trace)
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
        "warning_count": len(warnings),
        "warnings": warnings,
        **lifecycle,
        "run_dir": str(run_dir),
    }


def _batch_summary(seeds: list[int], agents: list[str], runs: list[dict]) -> dict:
    agent_summary = {}
    for agent in agents:
        agent_runs = [run for run in runs if run["agent_id"] == agent]
        total_turns = sum(int(run["turn_count"]) for run in agent_runs)
        agent_summary[agent] = {
            "runs": len(agent_runs),
            "average_turns": total_turns / len(agent_runs) if agent_runs else 0,
            "final_outcomes": dict(Counter(str(run["result_type"]) for run in agent_runs)),
            "stop_reasons": dict(Counter(str(run["stop_reason"]) for run in agent_runs)),
            "warning_count": sum(int(run["warning_count"]) for run in agent_runs),
        }
    return {
        "seeds": seeds,
        "agents": agents,
        "total_runs": len(runs),
        "crash_count": sum(1 for run in runs if run["crashed"]),
        "invariant_violation_count": sum(1 for run in runs if any("invariant" in warning for warning in run["warnings"])),
        "quest_completion_count": sum(int(run.get("quest_completion_count", 0)) for run in runs),
        "reward_granted_count": sum(int(run.get("reward_granted_count", 0)) for run in runs),
        "duplicate_reward_prevention_count": sum(int(run.get("duplicate_reward_prevention_count", 0)) for run in runs),
        "next_quest_transition_count": sum(int(run.get("next_quest_transition_count", 0)) for run in runs),
        "run_complete_count": sum(int(run.get("run_complete_count", 0)) for run in runs),
        "completion_blocked_by_min_turns_count": sum(int(run.get("completion_blocked_by_min_turns_count", 0)) for run in runs),
        "outcome_counts": dict(Counter(str(run["result_type"]) for run in runs)),
        "agent_summary": agent_summary,
        "runs": runs,
    }


def _render_batch_report(summary: dict) -> str:
    lines = [
        "# Subagent Auto-Play Batch Report",
        "",
        "## Batch Summary",
        f"- seeds: {', '.join(str(seed) for seed in summary['seeds'])}",
        f"- agents: {', '.join(summary['agents'])}",
        f"- total runs: {summary['total_runs']}",
        f"- crash count: {summary['crash_count']}",
        f"- invariant violation count: {summary['invariant_violation_count']}",
        f"- quest completion count: {summary['quest_completion_count']}",
        f"- reward granted count: {summary['reward_granted_count']}",
        f"- duplicate reward prevention count: {summary['duplicate_reward_prevention_count']}",
        f"- next quest transition count: {summary['next_quest_transition_count']}",
        f"- run complete count: {summary['run_complete_count']}",
        f"- completion blocked by min turns count: {summary['completion_blocked_by_min_turns_count']}",
        "",
        "## Agent Summary",
    ]
    for agent, data in summary["agent_summary"].items():
        lines.append(f"- {agent}: runs={data['runs']} avg_turns={data['average_turns']:.1f} warnings={data['warning_count']} stop_reasons={data['stop_reasons']}")
    lines.extend(["", "## Run Matrix"])
    for run in summary["runs"]:
        lines.append(
            f"- seed {run['seed']} / {run['agent_id']}: outcome={run['result_type']} turns={run['turn_count']} "
            f"stop_reason={run['stop_reason']} quest_complete={run.get('quest_completion_count', 0)} "
            f"reward={run.get('reward_granted_count', 0)} warnings={run['warning_count']}"
        )
    lines.extend(["", "## Notable Cases"])
    notable = [run for run in summary["runs"] if run["crashed"] or run["warning_count"]]
    lines.extend(
        f"- seed {run['seed']} / {run['agent_id']}: {run['warnings']}" for run in notable
    )
    if not notable:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def _trace_warnings(trace: list[dict]) -> list[str]:
    warnings = []
    for entry in trace:
        cards = entry.get("presented_card_ids", [])
        if len(cards) != 3:
            warnings.append(f"turn {entry.get('turn')}: 3-card invariant violated")
        if len(cards) != len(set(cards)):
            warnings.append(f"turn {entry.get('turn')}: duplicate presented cards")
        relevance = entry.get("presented_card_relevance", [])
        off_quest = [card.get("card_id") for card in relevance if card.get("off_quest_candidate")]
        fallback = [card.get("card_id") for card in relevance if card.get("fallback_reason")]
        if off_quest:
            warnings.append(f"turn {entry.get('turn')}: off-quest {off_quest}")
        if fallback:
            warnings.append(f"turn {entry.get('turn')}: fallback {fallback}")
    return warnings


def _lifecycle_counts(trace: list[dict]) -> dict[str, int]:
    return {
        "quest_completion_count": sum(1 for entry in trace if entry.get("quest_success")),
        "reward_granted_count": sum(1 for entry in trace if entry.get("reward_granted")),
        "duplicate_reward_prevention_count": sum(1 for entry in trace if entry.get("duplicate_reward_prevented")),
        "next_quest_transition_count": sum(1 for entry in trace if entry.get("next_quest_id")),
        "run_complete_count": sum(1 for entry in trace if entry.get("run_complete")),
        "completion_blocked_by_min_turns_count": sum(1 for entry in trace if entry.get("completion_blocked_by_min_turns")),
    }


def _parse_seeds(raw: str) -> list[int]:
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def _parse_agents(raw: str) -> list[str]:
    requested = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = sorted(set(requested) - set(policy_ids()))
    if unknown:
        raise ValueError(f"unknown agent policies: {', '.join(unknown)}")
    return requested


if __name__ == "__main__":
    raise SystemExit(main())
