from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import TextIO, TypedDict


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root / "src"))

    try:
        args = _parse_args(project_root)
        outputs = run_manual_choice(args, sys.stdin, sys.stdout)
    except (OSError, TypeError, ValueError, KeyError) as error:
        print(f"MANUAL_RUNNER: ERROR {error}", file=sys.stderr)
        return 1

    print(f"MANUAL_RUN_JSON: {outputs.json_path}")
    print(f"MANUAL_RUN_TEXT_MUD: {outputs.text_path}")
    print(f"MANUAL_RUN_TRACE: {outputs.trace_path}")
    print(f"MANUAL_RUN_SUMMARY: {outputs.summary_path}")
    return 0


@dataclass(frozen=True, slots=True)
class ManualRunnerArgs:
    project_root: Path
    scenario_path: Path
    seed: int
    output_dir: Path
    choices: tuple[int, ...]
    choice_source: str


@dataclass(frozen=True, slots=True)
class ManualRunnerOutputs:
    json_path: Path
    text_path: Path
    trace_path: Path
    summary_path: Path


@dataclass(frozen=True, slots=True)
class InvalidManualChoiceError(ValueError):
    raw_choice: str

    def __str__(self) -> str:
        return f"invalid manual choice {self.raw_choice!r}; expected 1, 2, or 3"


class InvalidManualScenarioError(ValueError):
    pass


class TraceEntry(TypedDict):
    turn: int
    day: int
    presented_card_ids: list[str]
    selected_index: int
    selected_card_id: str
    selected_card_slot_role: str
    result_summary: str
    resource_delta: dict[str, int]
    objective_delta: dict[str, int]
    next_event_tags_delta: list[str]


def run_manual_choice(args: ManualRunnerArgs, stdin: TextIO, stdout: TextIO) -> ManualRunnerOutputs:
    from fateweaver.data_loader import load_project_data
    from fateweaver.gameplay_p0 import (
        _continue_state,
        _minimum_completion_turn,
        _ontology_context,
        _run_log,
        _selection_context,
        _turn_log,
        card_candidate_context,
    )
    from fateweaver.gameplay_p0_card_selection import select_cards_from_pool
    from fateweaver.gameplay_p0_cards import build_card_candidate_pool
    from fateweaver.gameplay_p0_data import load_foundation
    from fateweaver.gameplay_p0_models import GameplayRunRequest, TurnLogRequest
    from fateweaver.gameplay_p0_objectives import QuestReportRequest, build_quest_report, quest_completed
    from fateweaver.gameplay_p0_rules import apply_turn_result, combined_result, initial_state, select_storylet
    from fateweaver.ontology_reasoner import load_ontology_core, run_reasoner
    from fateweaver.scenario_filter import filter_events_for_scenario
    from fateweaver.state_manager import is_failed
    from fateweaver.validator import validate_bundle

    loaded = load_project_data(args.project_root, args.scenario_path)
    bundle, scenario = loaded.bundle, loaded.scenario
    errors = validate_bundle(bundle, scenario)
    if errors:
        raise InvalidManualScenarioError(f"invalid scenario: {'; '.join(errors)}")
    if scenario.gameplay_mode != "p0_foundation":
        raise InvalidManualScenarioError("manual choice runner requires p0_foundation scenario")

    events = filter_events_for_scenario(bundle.events, scenario)
    foundation = load_foundation(bundle.project_root, scenario.active_quest_id)
    ontology_core = load_ontology_core(bundle.project_root)
    request = GameplayRunRequest(bundle, scenario, events, args.seed, 1, args.output_dir, stdin, stdout, "manual")
    rng = Random(args.seed)
    state = initial_state(scenario, foundation.quest)
    turns = []
    trace = []
    choice_offset = 0
    stopped_reason = ""
    while len(turns) < scenario.target_turns and state.clock.turn <= state.clock.max_turns and not is_failed(state.status, bundle.statuses):
        if args.choice_source != "interactive" and choice_offset >= len(args.choices):
            stopped_reason = "manual_choices_exhausted"
            break
        ontology_inference = run_reasoner(ontology_core, _ontology_context(foundation.quest.id, state))
        event = select_storylet(events, state, rng, foundation.quest.id, ontology_inference)
        context = card_candidate_context(foundation.quest, event, state, ontology_inference)
        candidate_pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        selection = select_cards_from_pool(candidate_pool, _selection_context(request, foundation.quest, state))
        cards = selection.cards
        selected_index = _next_choice(args, choice_offset, state.clock.turn, stdin, stdout)
        choice_offset += 1
        selected_cards = (cards[selected_index - 1],)
        result = combined_result(selected_cards, None, foundation.card_rules.default_extra_cost)
        result["storylet_id"] = event.id
        result["cooldown_tags"] = list(context.cooldown_tags)
        result["repeat_group"] = context.repeat_group
        result["presented_card_ids"] = [card.id for card in cards]
        result["selected_card_ids"] = [selected_cards[0].id]
        before = state
        state = apply_turn_result(state, result, bundle)
        turn = _turn_log(
            TurnLogRequest(
                quest=foundation.quest,
                before=before,
                after=state,
                event=event,
                context=context,
                candidate_pool=selection.candidate_pool,
                cards=cards,
                selected=selected_cards,
                combo=None,
                result=result,
                ontology_inference=ontology_inference,
            ),
        )
        turn["manual_choice_mode"] = True
        turn["manual_selected_index"] = selected_index
        turns.append(turn)
        trace.append(_trace_entry(turn, selected_index, before.next_event_tags, before.quest_progress))
        if (
            quest_completed(foundation.quest, state, bundle, foundation.score_rules)
            and state.clock.turn >= _minimum_completion_turn(scenario.run_clock)
        ) or is_failed(state.status, bundle.statuses):
            break
        state = _continue_state(state, event)

    report = build_quest_report(QuestReportRequest(foundation.quest, state, bundle, foundation.score_rules))
    log = _run_log(request, foundation.quest, turns, state, report)
    log["manual_choice_mode"] = True
    log["choice_source"] = args.choice_source
    log["manual_choice_trace"] = trace
    log["unused_choices"] = max(0, len(args.choices) - choice_offset)
    log["manual_stop_reason"] = stopped_reason
    return _write_outputs(args.output_dir, args.seed, log, trace)


def _parse_args(project_root: Path) -> ManualRunnerArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--choices")
    parser.add_argument("--choice-file")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--output-dir", required=True)
    namespace = parser.parse_args()
    sources = sum(1 for value in (namespace.choices, namespace.choice_file, namespace.interactive) if value)
    if sources != 1:
        parser.error("provide exactly one of --choices, --choice-file, or --interactive")
    scenario_path = Path(namespace.scenario)
    output_dir = Path(namespace.output_dir)
    choices, source = _choice_source(namespace.choices, namespace.choice_file, namespace.interactive)
    return ManualRunnerArgs(
        project_root=project_root,
        scenario_path=scenario_path if scenario_path.is_absolute() else project_root / scenario_path,
        seed=namespace.seed,
        output_dir=output_dir if output_dir.is_absolute() else project_root / output_dir,
        choices=choices,
        choice_source=source,
    )


def _choice_source(raw_choices: str | None, choice_file: str | None, interactive: bool) -> tuple[tuple[int, ...], str]:
    if raw_choices is not None:
        return _parse_choices(raw_choices), "sequence"
    if choice_file is not None:
        return _parse_choices(Path(choice_file).read_text(encoding="utf-8")), "file"
    if interactive:
        return (), "interactive"
    raise InvalidManualScenarioError("manual choice source required")


def _parse_choices(raw: str) -> tuple[int, ...]:
    values = []
    for part in raw.replace("\n", ",").split(","):
        choice = part.strip()
        if not choice:
            continue
        values.append(_parse_choice(choice))
    if not values:
        raise InvalidManualChoiceError("")
    return tuple(values)


def _parse_choice(raw: str) -> int:
    try:
        choice = int(raw)
    except ValueError as error:
        raise InvalidManualChoiceError(raw) from error
    if choice not in (1, 2, 3):
        raise InvalidManualChoiceError(raw)
    return choice


def _next_choice(args: ManualRunnerArgs, offset: int, turn: int, stdin: TextIO, stdout: TextIO) -> int:
    if args.choice_source == "interactive":
        while True:
            stdout.write("choice 1/2/3> ")
            stdout.flush()
            try:
                return _parse_choice(stdin.readline().strip())
            except InvalidManualChoiceError:
                stdout.write("1, 2, 3 중 하나로 다시 입력해 주세요.\n")
    if offset >= len(args.choices):
        raise InvalidManualChoiceError(f"missing choice for turn {turn}")
    return args.choices[offset]


def _trace_entry(turn: dict, selected_index: int, before_next_event_tags: tuple[str, ...], before_objectives: dict[str, int]) -> TraceEntry:
    after_tags = tuple(str(value) for value in turn["next_event_tags"])
    return {
        "turn": turn["turn"],
        "day": turn["run_clock"]["day"],
        "presented_card_ids": [card["card_id"] for card in turn["presented_cards"]],
        "selected_index": selected_index,
        "selected_card_id": turn["selected_cards"][0],
        "selected_card_slot_role": turn["selected_choice_type"],
        "result_summary": turn["choice_reason"],
        "resource_delta": _int_delta(turn["state_before"], turn["state_after"]),
        "objective_delta": _int_delta(before_objectives, turn["quest_progress"]),
        "next_event_tags_delta": [tag for tag in after_tags if tag not in before_next_event_tags],
    }


def _int_delta(before: dict, after: dict) -> dict[str, int]:
    keys = sorted({str(key) for key in before} | {str(key) for key in after})
    return {key: int(after.get(key, 0)) - int(before.get(key, 0)) for key in keys}


def _write_outputs(output_dir: Path, seed: int, log: dict, trace: list[dict]) -> ManualRunnerOutputs:
    from fateweaver.text_mud_log import render_text_mud_log

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"manual_seed_{seed}.json"
    text_path = output_dir / f"manual_seed_{seed}_text_mud.txt"
    trace_path = output_dir / f"manual_seed_{seed}_choice_trace.json"
    summary_path = output_dir / f"manual_seed_{seed}_summary.json"
    summary = {
        "manual_choice_mode": True,
        "choice_source": log["choice_source"],
        "turn_count": len(log["turns"]),
        "ending": log["quest_report"].get("ending"),
        "result_type": log["quest_report"].get("result_type"),
        "selected_indexes": [entry["selected_index"] for entry in trace],
        "selected_card_ids": [entry["selected_card_id"] for entry in trace],
        "unused_choices": log["unused_choices"],
        "manual_stop_reason": log["manual_stop_reason"],
    }
    json_path.write_text(json.dumps(log, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text_path.write_text(render_text_mud_log(log), encoding="utf-8")
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ManualRunnerOutputs(json_path, text_path, trace_path, summary_path)


if __name__ == "__main__":
    raise SystemExit(main())
