from __future__ import annotations

import argparse
import json
from pathlib import Path


def render_trace_report(run_log: dict, trace: list[dict]) -> str:
    lines = ["# Manual Run Trace Report", "", "## Run Summary"]
    quest_report = _mapping(run_log.get("quest_report", {}))
    lines.extend(
        [
            f"- seed: {_value(run_log.get('seed'))}",
            f"- max_turns: {_value(run_log.get('max_turns', 'not_recorded'))}",
            f"- final outcome: {_value(quest_report.get('result_type', run_log.get('result_type')))}",
            f"- stop_reason: {_value(run_log.get('stop_reason'))}",
            f"- manual_stop_reason: {_value(run_log.get('manual_stop_reason'))}",
            f"- total turns: {len(_sequence(run_log.get('turns')) or trace)}",
            f"- selected choices: {_selected_pattern(trace)}",
            "",
            "## Quest Onboarding",
        ]
    )
    onboarding = next((entry for entry in trace if entry.get("quest_onboarding")), trace[0] if trace else {})
    completion = next((entry for entry in trace if entry.get("quest_lifecycle_event")), {})
    lines.extend(
        [
            f"- onboarding turn: {_value(onboarding.get('onboarding_turn', onboarding.get('turn')))}",
            f"- active quest: {_value(onboarding.get('active_quest_id'))} / {_value(onboarding.get('active_quest_title'))}",
            f"- required objective ids: {_join(onboarding.get('required_objective_ids'))}",
            f"- initial objective status: {_objective_status(onboarding)}",
            "",
            "## Quest Completion",
            f"- quest_completed: {_value(completion.get('quest_completed', 'not_recorded'))}",
            f"- quest_success: {_value(completion.get('quest_success', 'not_recorded'))}",
            f"- completed quest id: {_value(completion.get('completed_quest_id', 'not_recorded'))}",
            f"- completed required objectives: {_join(completion.get('completed_required_objective_ids'))}",
            f"- Reward Granted: {_value(completion.get('reward_granted', 'not_recorded'))}",
            f"- Reward Delta: {_dict_delta(completion.get('reward_delta'))}",
            f"- Quest Transition: {_quest_transition(completion)}",
            f"- Next Quest Onboarding: {_value(completion.get('next_quest_onboarding', 'not_recorded'))}",
            f"- Run Complete: {_value(completion.get('run_complete', 'not_recorded'))}",
            f"- completion_blocked_by_min_turns: {_value(completion.get('completion_blocked_by_min_turns', 'not_recorded'))}",
            "",
            "## Quest Transitions",
            *_transition_lines(trace),
            "",
            "## Turn Timeline",
        ]
    )
    turns = {int(turn.get("turn", index + 1)): turn for index, turn in enumerate(_sequence(run_log.get("turns")))}
    for entry in trace:
        turn_no = int(entry.get("turn", 0))
        turn = turns.get(turn_no, {})
        lines.extend(_turn_lines(turn_no, turn, entry))
    lines.extend(["", "## Warnings"])
    warnings = _warnings(trace)
    lines.extend(f"- {warning}" for warning in warnings)
    lines.extend(["", "## Invariant Summary", *_invariant_lines(run_log, trace)])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-json", required=True)
    parser.add_argument("--trace-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run_log = json.loads(Path(args.run_json).read_text(encoding="utf-8"))
    trace = json.loads(Path(args.trace_json).read_text(encoding="utf-8"))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_trace_report(run_log, trace), encoding="utf-8")
    print(f"MANUAL_RUN_REPORT: {output}")
    return 0


def _turn_lines(turn_no: int, turn: dict, entry: dict) -> list[str]:
    selected = int(entry.get("selected_index", 0))
    lines = [f"", f"### Turn {turn_no}", f"- selected slot {selected}: {_value(entry.get('selected_card_id'))}"]
    cards = _sequence(turn.get("presented_cards")) or [{"card_id": card_id} for card_id in _sequence(entry.get("presented_card_ids"))]
    relevance_by_id = {str(card.get("card_id", "")): card for card in _sequence(entry.get("presented_card_relevance"))}
    for index, card in enumerate(cards, start=1):
        card_id = str(card.get("card_id", "unknown"))
        relevance = relevance_by_id.get(card_id, {})
        warning = _card_warning(relevance)
        lines.append(
            f"- card {index}: {card_id} ({_value(card.get('slot_role', card.get('choice_type')))}; "
            f"relevance={_value(relevance.get('relevance_reason', 'not_recorded'))}; "
            f"fallback={_fallback_value(relevance)}){warning}"
        )
    lines.extend(
        [
            f"- selected result/outcome: {_value(entry.get('result_summary', turn.get('choice_reason')))}",
            f"- objective before/after/completed: {_objective_status(entry)}",
            f"- objective delta: {_dict_delta(entry.get('objective_delta'))}",
            f"- resource delta: {_dict_delta(entry.get('resource_delta'))}",
        ]
    )
    return lines


def _warnings(trace: list[dict]) -> list[str]:
    warnings: list[str] = []
    for entry in trace:
        relevance = _sequence(entry.get("presented_card_relevance"))
        missing = "presented_card_relevance" not in entry
        off_quest = [card.get("card_id", "unknown") for card in relevance if card.get("off_quest_candidate")]
        fallback = [card.get("card_id", "unknown") for card in relevance if card.get("fallback_reason")]
        if missing:
            warnings.append(f"turn {entry.get('turn', 'unknown')}: missing trace fields: presented_card_relevance")
        if off_quest:
            warnings.append(f"turn {entry.get('turn', 'unknown')}: off-quest candidates {', '.join(str(card) for card in off_quest)}")
        if fallback:
            warnings.append(f"turn {entry.get('turn', 'unknown')}: fallback cards {', '.join(str(card) for card in fallback)}")
    return warnings or ["none"]


def _transition_lines(trace: list[dict]) -> list[str]:
    lifecycle_entries = [entry for entry in trace if entry.get("quest_lifecycle_event")]
    if not lifecycle_entries:
        return ["- none"]
    return [
        "- turn {turn}: previous={previous} next={next_quest} onboarding={onboarding} "
        "required={required} no_next_quest={no_next} run_complete={run_complete}".format(
            turn=_value(entry.get("turn")),
            previous=_value(entry.get("previous_quest_id", entry.get("completed_quest_id"))),
            next_quest=_value(entry.get("next_quest_id", "no_next_quest" if entry.get("no_next_quest") else "")),
            onboarding=_value(entry.get("next_quest_onboarding", "not_recorded")),
            required=_join(entry.get("next_required_objective_ids")),
            no_next=_value(entry.get("no_next_quest", "not_recorded")),
            run_complete=_value(entry.get("run_complete", "not_recorded")),
        )
        for entry in lifecycle_entries
    ]


def _invariant_lines(run_log: dict, trace: list[dict]) -> list[str]:
    three_cards = all(len(_sequence(entry.get("presented_card_ids"))) == 3 for entry in trace)
    unique_cards = all(len(_sequence(entry.get("presented_card_ids"))) == len(set(_sequence(entry.get("presented_card_ids")))) for entry in trace)
    clean_stop = bool(run_log.get("stop_reason") or run_log.get("manual_stop_reason"))
    trace_consistent = len(_sequence(run_log.get("turns"))) in {0, len(trace)}
    return [
        f"- 3-card invariant: {three_cards}",
        f"- no duplicate presented cards in same turn: {unique_cards}",
        f"- clean stop/end: {clean_stop}",
        f"- trace consistency: {trace_consistent}",
    ]


def _objective_status(entry: dict) -> str:
    objectives = _sequence(entry.get("required_objectives"))
    if not objectives:
        return "not_recorded"
    return "; ".join(
        f"{objective.get('id', 'unknown')} {objective.get('before_value', 'unknown')}->{objective.get('after_value', 'unknown')} completed={objective.get('completed_after', 'unknown')}"
        for objective in objectives
    )


def _card_warning(relevance: dict) -> str:
    flags = []
    if relevance.get("off_quest_candidate"):
        flags.append("off-quest")
    if relevance.get("fallback_reason"):
        flags.append("fallback")
    return "" if not flags else f" [{' / '.join(flags)}]"


def _selected_pattern(trace: list[dict]) -> str:
    return ",".join(str(entry.get("selected_index", "unknown")) for entry in trace) or "not_recorded"


def _dict_delta(value: object) -> str:
    data = _mapping(value)
    if not data:
        return "not_recorded"
    return ", ".join(f"{key}:{amount}" for key, amount in data.items())


def _join(value: object) -> str:
    items = _sequence(value)
    return ", ".join(str(item) for item in items) if items else "not_recorded"


def _value(value: object) -> str:
    if value is None or value == "":
        return "unknown"
    return str(value)


def _fallback_value(relevance: dict) -> str:
    if "fallback_reason" not in relevance:
        return "not_recorded"
    value = relevance.get("fallback_reason")
    return "n/a" if value in {None, ""} else str(value)


def _quest_transition(completion: dict) -> str:
    next_quest_id = completion.get("next_quest_id")
    if next_quest_id:
        return str(next_quest_id)
    if completion.get("no_next_quest"):
        return "no_next_quest"
    return "not_recorded"


def _sequence(value: object) -> list:
    return value if isinstance(value, list) else []


def _mapping(value: object) -> dict:
    return value if isinstance(value, dict) else {}


if __name__ == "__main__":
    raise SystemExit(main())
