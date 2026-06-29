from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random
from typing import Protocol

from fateweaver.choice_resolver import ChoiceSeen, build_choices_seen, select_available_choice, selected_choice_from_seen
from fateweaver.data_loader import load_project_data
from fateweaver.event_selector import select_event
from fateweaver.logger import save_run_log
from fateweaver.models import JsonMap, PlayerChoiceFeedback, RunFeedback
from fateweaver.scenario_filter import filter_events_for_scenario
from fateweaver.state_manager import apply_choice_result, is_failed
from fateweaver.validator import validate_bundle


class InputPort(Protocol):
    def isatty(self) -> bool: ...

    def readline(self) -> str: ...


class OutputPort(Protocol):
    def write(self, text: str) -> int: ...


def run_console_simulation(
    project_root: Path,
    scenario_path: Path,
    seed_override: int | None,
    runs: int,
    logs_dir: Path,
    stdin: InputPort,
    stdout: OutputPort,
) -> list[Path]:
    loaded = load_project_data(project_root, scenario_path)
    bundle, scenario = loaded.bundle, loaded.scenario
    errors = validate_bundle(bundle, scenario)
    if errors:
        joined = "; ".join(errors)
        raise ValueError(f"invalid scenario: {joined}")
    events = filter_events_for_scenario(bundle.events, scenario)
    seed = scenario.seed if seed_override is None else seed_override
    saved_paths: list[Path] = []
    for run_number in range(1, runs + 1):
        saved_paths.append(_run_once(bundle, scenario, events, seed, run_number, logs_dir, stdin, stdout))
    return saved_paths


def _run_once(bundle, scenario, events, seed: int, run_number: int, logs_dir: Path, stdin: InputPort, stdout: OutputPort) -> Path:
    rng = Random(seed + run_number - 1)
    state = dict(scenario.initial_status)
    inventory = tuple(scenario.initial_items)
    run_tags: tuple[str, ...] = ()
    recent_event_ids: tuple[str, ...] = ()
    turns: list[JsonMap] = []
    for turn in range(1, scenario.target_turns + 1):
        event = select_event(events, state, inventory, run_tags, rng, recent_event_ids)
        choices_seen = build_choices_seen(event, state, inventory, run_tags)
        selected = _choose(choices_seen, stdin, stdout)
        feedback = _choice_feedback(selected, stdin, stdout)
        influenced_by = _influenced_by(selected, event.event_tags, choices_seen)
        state_before = dict(state)
        inventory_before = list(inventory)
        transition = apply_choice_result(state, inventory, run_tags, selected.result, bundle.statuses)
        state = transition.status
        inventory = transition.inventory
        run_tags = transition.run_tags
        turns.append(
            {
                "turn": turn,
                "event_id": event.id,
                "event_tags": list(event.event_tags),
                "state_before": state_before,
                "inventory_before": inventory_before,
                "choices_seen": [_choice_seen_json(choice) for choice in choices_seen],
                "selected_choice_id": selected.choice_id,
                "selected_choice_type": selected.choice_type,
                "was_available": selected.available,
                "was_hidden": selected.hidden,
                "choice_time_seconds": 0,
                "choice_reason": feedback.choice_reason,
                "expected_risk": feedback.expected_risk,
                "influenced_by": list(influenced_by),
                "result": selected.result,
                "state_after": dict(state),
                "inventory_after": list(inventory),
                "regret_score": feedback.regret_score,
                "notes": "",
            }
        )
        recent_event_ids = (*recent_event_ids, event.id)
        if is_failed(state, bundle.statuses):
            break
    run_feedback = _run_feedback(turns, is_failed(state, bundle.statuses), stdin, stdout)
    log = _run_log(scenario.id, seed, run_number, turns, state, inventory, run_feedback)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"run_{scenario.id}_{seed}_{timestamp}_{run_number:04d}.json"
    return save_run_log(log, logs_dir, filename)


def _choose(choices_seen: tuple[ChoiceSeen, ...], stdin: InputPort, stdout: OutputPort) -> ChoiceSeen:
    if not stdin.isatty():
        return select_available_choice(choices_seen)
    for choice in choices_seen:
        status = "available" if choice.available else f"unavailable: {choice.unavailable_reason}"
        stdout.write(f"{choice.choice_id}: {status}\n")
    stdout.write("choice> ")
    return selected_choice_from_seen(choices_seen, stdin.readline().strip())


def _choice_feedback(selected: ChoiceSeen, stdin: InputPort, stdout: OutputPort) -> PlayerChoiceFeedback:
    if not stdin.isatty():
        return PlayerChoiceFeedback(
            choice_reason="auto: selected first available non-hidden choice",
            expected_risk=selected.expected_risk,
            regret_score=_regret_score(selected.expected_risk),
        )
    stdout.write("choice_reason> ")
    reason = stdin.readline().strip() or "player chose without comment"
    stdout.write("expected_risk> ")
    expected_risk = stdin.readline().strip() or selected.expected_risk
    stdout.write("regret_score 1-5> ")
    regret_score = _bounded_score(stdin.readline().strip(), _regret_score(expected_risk))
    return PlayerChoiceFeedback(reason, expected_risk, regret_score)


def _run_feedback(turns: list[JsonMap], run_failed: bool, stdin: InputPort, stdout: OutputPort) -> RunFeedback:
    meaningful_count = sum(1 for turn in turns if turn["influenced_by"])
    auto_restart = 4 if meaningful_count >= 3 else 2
    auto_woven = 4 if _has_item_or_status_influence(turns) else 2
    if not stdin.isatty():
        return RunFeedback(4, auto_restart, auto_woven, "auto console validation run", str(turns[-1]["selected_choice_id"]) if turns else "", "auto validation complete")
    stdout.write("fairness_score 1-5> ")
    fairness = _bounded_score(stdin.readline().strip(), 4)
    stdout.write("restart_intent_score 1-5> ")
    restart = _bounded_score(stdin.readline().strip(), auto_restart)
    stdout.write("player_woven_score 1-5> ")
    woven = _bounded_score(stdin.readline().strip(), auto_woven)
    stdout.write("narrative_summary> ")
    narrative = stdin.readline().strip()
    stdout.write("most_memorable_choice> ")
    memorable = stdin.readline().strip()
    stdout.write("next_run_intent> ")
    next_intent = stdin.readline().strip()
    return RunFeedback(fairness, restart, woven, narrative, memorable, next_intent)


def _run_log(scenario_id: str, seed: int, run_number: int, turns: list[JsonMap], state, inventory, feedback: RunFeedback) -> JsonMap:
    run_failed = bool(state.get("health", 1) <= 0 or state.get("curse", 0) >= 5)
    return {
        "schema_version": "console_validation_log_v0.1",
        "scenario_id": scenario_id,
        "seed": seed,
        "run_id": f"{scenario_id}-{seed}-{run_number:04d}",
        "turns": turns,
        "run_summary": {
            "final_state": dict(state),
            "final_inventory": list(inventory),
            "fairness_score": feedback.fairness_score,
            "restart_intent_score": feedback.restart_intent_score,
            "player_woven_score": feedback.player_woven_score,
            "run_failed": run_failed,
            "run_failed_but_interesting": run_failed and feedback.restart_intent_score >= 4,
            "narrative_summary": feedback.narrative_summary,
            "most_memorable_choice": feedback.most_memorable_choice,
            "next_run_intent": feedback.next_run_intent,
        },
    }


def _choice_seen_json(choice: ChoiceSeen) -> JsonMap:
    return {
        "choice_id": choice.choice_id,
        "choice_type": choice.choice_type,
        "available": choice.available,
        "unavailable_reason": choice.unavailable_reason,
        "hidden": choice.hidden,
    }


def _influenced_by(selected: ChoiceSeen, event_tags: tuple[str, ...], choices_seen: tuple[ChoiceSeen, ...]) -> tuple[str, ...]:
    values = list(selected.influenced_by)
    for choice in choices_seen:
        if not choice.available:
            values.append(f"unavailable:{choice.choice_id}")
    if selected.choice_type == "combat_response" and "combat" in event_tags:
        values.append("tag:combat")
    return tuple(values)


def _regret_score(expected_risk: str) -> int:
    match expected_risk:
        case "low" | "none":
            return 1
        case "high":
            return 4
        case _:
            return 3


def _bounded_score(raw: str, default: int) -> int:
    if raw.isdecimal():
        return min(5, max(1, int(raw)))
    return default


def _has_item_or_status_influence(turns: list[JsonMap]) -> bool:
    for turn in turns:
        influenced = turn.get("influenced_by", [])
        if isinstance(influenced, list):
            for value in influenced:
                text = str(value)
                if text.startswith("item:") or text.startswith("status:"):
                    return True
    return False
