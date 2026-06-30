from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random

from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.gameplay_p0_models import CardRule, ComboRule, GameplayRunRequest, Quest, RunState
from fateweaver.gameplay_p0_objectives import QuestReportRequest, build_quest_report, quest_completed
from fateweaver.gameplay_p0_rules import (
    advance_clock,
    apply_turn_result,
    card_json,
    clock_json,
    combined_result,
    influences,
    initial_state,
    int_map,
    multi_select_json,
    present_cards,
    select_cards,
    select_storylet,
)
from fateweaver.logger import save_run_log
from fateweaver.models import Event, JsonMap
from fateweaver.state_manager import is_failed
from fateweaver.text_mud_log import save_text_mud_log


def run_gameplay_p0(request: GameplayRunRequest) -> Path:
    foundation = load_foundation(request.bundle.project_root, request.scenario.active_quest_id)
    rng = Random(request.seed + request.run_number - 1)
    state = initial_state(request.scenario, foundation.quest)
    turns: list[JsonMap] = []
    while state.clock.turn <= state.clock.max_turns and not is_failed(state.status, request.bundle.statuses):
        event = select_storylet(request.events, state, rng)
        cards = present_cards(foundation.card_rules.cards, state)
        selected_cards, combo = select_cards(cards, foundation.card_rules.combos, state, request.profile)
        result = combined_result(selected_cards, combo, foundation.card_rules.default_extra_cost)
        result["selected_card_ids"] = [card.id for card in selected_cards]
        before = state
        state = apply_turn_result(state, result, request.bundle)
        turns.append(_turn_log(foundation.quest, before, state, event, cards, selected_cards, combo, result))
        if quest_completed(foundation.quest, state, request.bundle) or is_failed(state.status, request.bundle.statuses):
            break
        state = _continue_state(state, event)
    quest_report = build_quest_report(QuestReportRequest(foundation.quest, state, request.bundle, foundation.score_rules))
    log = _run_log(request, foundation.quest, turns, state, quest_report)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    filename = f"run_{request.scenario.id}_{request.profile}_{request.seed}_{timestamp}_{request.run_number:04d}.json"
    json_path = save_run_log(log, request.logs_dir, filename)
    save_text_mud_log(log, json_path)
    return json_path


def _continue_state(state: RunState, event: Event) -> RunState:
    from dataclasses import replace

    return replace(state, clock=advance_clock(state.clock), recent_event_ids=(*state.recent_event_ids, event.id))


def _turn_log(
    quest: Quest,
    before: RunState,
    after: RunState,
    event: Event,
    cards: tuple[CardRule, CardRule, CardRule],
    selected: tuple[CardRule, ...],
    combo: ComboRule | None,
    result: JsonMap,
) -> JsonMap:
    selected_ids = [card.id for card in selected]
    selected_text = " + ".join(card.title for card in selected)
    return {
        "turn": before.clock.turn,
        "run_clock": clock_json(before.clock),
        "quest_id": quest.id,
        "quest_title": quest.title,
        "event_id": event.id,
        "event_name": event.name,
        "event_description": event.description,
        "region_tags": [before.region],
        "event_tags": list(event.event_tags),
        "danger_tags": list(event.danger_tags),
        "state_before": dict(before.status),
        "inventory_before": list(before.inventory),
        "choices_seen": [card_json(card) for card in cards],
        "presented_cards": [card_json(card) for card in cards],
        "selected_choice_id": selected[0].id,
        "selected_choice_type": "multi_select" if combo is not None else selected[0].slot_role,
        "selected_choice_reason": "p0_foundation: selected combo" if combo is not None else "p0_foundation: selected quest progress",
        "selected_cards": selected_ids,
        "multi_select": multi_select_json(combo, selected_ids),
        "was_available": True,
        "was_hidden": False,
        "choice_time_seconds": 0,
        "choice_reason": selected_text,
        "expected_risk": "medium" if combo is not None else "low",
        "influenced_by": influences(selected, combo),
        "result": result,
        "state_after": dict(after.status),
        "inventory_after": list(after.inventory),
        "quest_progress": dict(after.quest_progress),
        "score": dict(after.score),
        "score_change": int_map(result.get("score_changes", {})),
        "next_event_tags": list(after.next_event_tags),
        "clues": list(after.clues),
        "omens": list(after.omens),
        "regret_score": 3 if combo is not None else 1,
        "notes": "",
    }


def _run_log(request: GameplayRunRequest, quest: Quest, turns: list[JsonMap], state: RunState, report: JsonMap) -> JsonMap:
    return {
        "schema_version": "console_validation_log_v0.1",
        "scenario_id": request.scenario.id,
        "seed": request.seed,
        "run_id": f"{request.scenario.id}-{request.seed}-{request.run_number:04d}",
        "profile": request.profile,
        "quest": {"id": quest.id, "title": quest.title},
        "run_clock": clock_json(state.clock),
        "turns": turns,
        "quest_report": report,
        "run_summary": {
            "final_state": dict(state.status),
            "final_inventory": list(state.inventory),
            "run_failed": report["result_type"] == "failure",
            "narrative_summary": report["review_text"],
            "most_memorable_choice": str(turns[-1]["selected_choice_id"]) if turns else "",
            "next_run_intent": "review quest report",
        },
    }
