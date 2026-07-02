from __future__ import annotations

import argparse
import sys
from pathlib import Path
from random import Random
from typing import TextIO

try:
    from .manual_choice_runner_agents import build_agent_context, choose_agent_index, policy_ids
    from .manual_choice_runner_output import write_outputs
    from .manual_choice_runner_trace import build_trace_entry
    from .manual_choice_runner_types import InvalidManualChoiceError, InvalidManualScenarioError, ManualRunnerArgs
except ImportError:
    from manual_choice_runner_agents import build_agent_context, choose_agent_index, policy_ids
    from manual_choice_runner_output import write_outputs
    from manual_choice_runner_trace import build_trace_entry
    from manual_choice_runner_types import InvalidManualChoiceError, InvalidManualScenarioError, ManualRunnerArgs


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root / "src"))

    try:
        args = _parse_args(project_root)
        json_path, text_path, trace_path, summary_path = run_manual_choice(args, sys.stdin, sys.stdout)
    except (OSError, TypeError, ValueError, KeyError) as error:
        print(f"MANUAL_RUNNER: ERROR {error}", file=sys.stderr)
        return 1

    print(f"MANUAL_RUN_JSON: {json_path}")
    print(f"MANUAL_RUN_TEXT_MUD: {text_path}")
    print(f"MANUAL_RUN_TRACE: {trace_path}")
    print(f"MANUAL_RUN_SUMMARY: {summary_path}")
    return 0


def run_manual_choice(args: ManualRunnerArgs, stdin: TextIO, stdout: TextIO) -> tuple[Path, Path, Path, Path]:
    from fateweaver.data_loader import load_project_data
    from fateweaver.gameplay_p0 import (
        _continue_state,
        _ontology_context,
        _run_log,
        _selection_context,
        _turn_log,
        card_candidate_context,
    )
    from fateweaver.gameplay_p0_card_selection import select_cards_from_pool
    from fateweaver.gameplay_p0_cards import build_card_candidate_pool
    from fateweaver.gameplay_p0_data import load_foundation
    from fateweaver.gameplay_p0_errors import MissingCardSlotError
    from fateweaver.gameplay_p0_lifecycle import complete_quest_lifecycle
    from fateweaver.gameplay_p0_models import GameplayRunRequest, TurnLogRequest
    from fateweaver.gameplay_p0_objectives import QuestReportRequest, build_quest_report, quest_completed
    from fateweaver.gameplay_p0_rules import apply_turn_result, combined_result, initial_state, select_storylet
    from fateweaver.gameplay_p0_sequence import load_next_foundation
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
    stop_reason = "completed"
    onboarding_reason = "run_start"
    while len(turns) < scenario.target_turns and state.clock.turn <= state.clock.max_turns and not is_failed(state.status, bundle.statuses):
        if args.max_turns is not None and len(turns) >= args.max_turns:
            stop_reason = "max_turn_reached"
            break
        if args.choice_source not in {"interactive", "agent"} and choice_offset >= len(args.choices):
            stop_reason = "choice_sequence_exhausted"
            break
        ontology_inference = run_reasoner(ontology_core, _ontology_context(foundation.quest.id, state))
        event = select_storylet(events, state, rng, foundation.quest.id, ontology_inference)
        context = card_candidate_context(foundation.quest, event, state, ontology_inference)
        candidate_pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        try:
            selection = select_cards_from_pool(candidate_pool, _selection_context(request, foundation.quest, state))
        except MissingCardSlotError as error:
            raise InvalidManualScenarioError(str(error)) from error
        cards = selection.cards
        if len(cards) < 3:
            stop_reason = "no_available_cards_handled"
            break
        if args.choice_source == "agent":
            selected_index = _agent_choice(args, cards, selection.candidate_pool, foundation.quest.id, state)
        else:
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
        lifecycle = {}
        if quest_completed(foundation.quest, state, bundle, foundation.score_rules):
            next_foundation = load_next_foundation(bundle.project_root, scenario, foundation.quest.id)
            next_quest = None if next_foundation is None else next_foundation.quest
            state, lifecycle = complete_quest_lifecycle(foundation.quest, state, bundle, foundation.score_rules, next_quest)
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
        if onboarding_reason:
            turn["quest_onboarding"] = True
            turn["onboarding_reason"] = onboarding_reason
            turn["onboarding_turn"] = turn["turn"]
            onboarding_reason = ""
        turn.update(lifecycle)
        turn["manual_choice_mode"] = True
        turn["manual_selected_index"] = selected_index
        turns.append(turn)
        trace.append(build_trace_entry(foundation.quest, turn, selected_index, before, state))
        if lifecycle and not lifecycle.get("run_complete") and next_foundation is not None:
            foundation = next_foundation
            state = _continue_state(state, event)
            onboarding_reason = "quest_transition"
            continue
        if lifecycle or is_failed(state.status, bundle.statuses):
            stop_reason = "failure" if is_failed(state.status, bundle.statuses) else "completed"
            break
        state = _continue_state(state, event)

    report = build_quest_report(QuestReportRequest(foundation.quest, state, bundle, foundation.score_rules))
    if stop_reason in {"completed", "target_turn_reached"} and report.get("result_type") == "success":
        stop_reason = "completed"
    elif len(turns) >= scenario.target_turns and stop_reason == "completed":
        stop_reason = "target_turn_reached"
    log = _run_log(request, foundation.quest, turns, state, report)
    log["seed"] = args.seed
    log["max_turns"] = args.max_turns if args.max_turns is not None else scenario.target_turns
    log["manual_choice_mode"] = True
    log["choice_source"] = args.choice_source
    log["agent_policy"] = args.agent_policy
    log["manual_choice_trace"] = trace
    log["unused_choices"] = max(0, len(args.choices) - choice_offset)
    log["stop_reason"] = stop_reason
    log["manual_stop_reason"] = stop_reason
    return write_outputs(args.output_dir, args.seed, log, trace)


def _parse_args(project_root: Path) -> ManualRunnerArgs:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--choices")
    parser.add_argument("--choice-file")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--agent-policy", choices=policy_ids())
    parser.add_argument("--max-turns", type=int)
    parser.add_argument("--output-dir", required=True)
    namespace = parser.parse_args()
    sources = sum(1 for value in (namespace.choices, namespace.choice_file, namespace.interactive, namespace.agent_policy) if value)
    if sources != 1:
        parser.error("provide exactly one of --choices, --choice-file, --interactive, or --agent-policy")
    scenario_path = Path(namespace.scenario)
    output_dir = Path(namespace.output_dir)
    choices, source = _choice_source(namespace.choices, namespace.choice_file, namespace.interactive, namespace.agent_policy)
    return ManualRunnerArgs(
        project_root=project_root,
        scenario_path=scenario_path if scenario_path.is_absolute() else project_root / scenario_path,
        seed=namespace.seed,
        output_dir=output_dir if output_dir.is_absolute() else project_root / output_dir,
        choices=choices,
        choice_source=source,
        max_turns=namespace.max_turns,
        agent_policy=namespace.agent_policy,
    )


def _choice_source(raw_choices: str | None, choice_file: str | None, interactive: bool, agent_policy: str | None) -> tuple[tuple[int, ...], str]:
    if raw_choices is not None:
        return _parse_choices(raw_choices), "sequence"
    if choice_file is not None:
        return _parse_choices(Path(choice_file).read_text(encoding="utf-8")), "file"
    if interactive:
        return (), "interactive"
    if agent_policy is not None:
        return (), "agent"
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


def _agent_choice(args: ManualRunnerArgs, cards: tuple, candidate_pool: tuple, active_quest_id: str, state) -> int:
    if args.agent_policy is None:
        raise InvalidManualScenarioError("agent choice source requires --agent-policy")
    return choose_agent_index(args.agent_policy, build_agent_context(cards, candidate_pool, active_quest_id, state))


if __name__ == "__main__":
    raise SystemExit(main())
