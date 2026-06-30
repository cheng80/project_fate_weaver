from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random
from typing import assert_never

from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.gameplay_p0_models import CardRule, ComboRule, GameplayRunRequest, Quest, RunState
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
from fateweaver.models import Event, JsonMap, ProjectData
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
        if _quest_success(state) or is_failed(state.status, request.bundle.statuses):
            break
        state = _continue_state(state, event)
    quest_report = _quest_report(foundation.quest, state, request.bundle, foundation.score_rules)
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


def _quest_report(quest: Quest, state: RunState, bundle: ProjectData, score_rules: JsonMap) -> JsonMap:
    failed = is_failed(state.status, bundle.statuses)
    success = _quest_success(state)
    result_type = _result_type(failed, success, state.quest_progress)
    score_breakdown = _score_breakdown(state, result_type, score_rules)
    return {
        "quest_id": quest.id,
        "result_type": result_type,
        "completed_objectives": _completed_objectives(state),
        "failed_objectives": _failed_objectives(state, result_type),
        "resource_summary": dict(state.status),
        "score": sum(score_breakdown.values()),
        "score_breakdown": score_breakdown,
        "rewards": quest.rewards if result_type == "success" else {},
        "unlocked_or_suggested_next": ["missing_porter_search"] if result_type == "success" else ["retry_herb_gathering"],
        "review_text": _review_text(result_type),
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


def _quest_success(state: RunState) -> bool:
    return state.quest_progress.get("herbs_collected", 0) >= 3 and state.quest_progress.get("reported_to_apothecary", 0) >= 1


def _result_type(failed: bool, success: bool, progress: dict[str, int]) -> str:
    match failed, success, progress.get("herbs_collected", 0) > 0:
        case True, _, _:
            return "failure"
        case _, True, _:
            return "success"
        case _, _, True:
            return "partial_success"
        case False, False, False:
            return "failure"
        case unreachable:
            assert_never(unreachable)


def _score_breakdown(state: RunState, result_type: str, score_rules: JsonMap) -> dict[str, int]:
    breakdown = dict(state.score)
    outcome_score = _outcome_score(result_type, score_rules)
    if outcome_score != 0:
        breakdown["outcome_adjustment"] = outcome_score
    return breakdown


def _outcome_score(result_type: str, score_rules: JsonMap) -> int:
    raw_bonus = score_rules.get("ending_bonus", {})
    if not isinstance(raw_bonus, dict):
        return 0
    return int(raw_bonus.get(result_type, 0))


def _completed_objectives(state: RunState) -> list[str]:
    completed: list[str] = []
    if state.quest_progress.get("herbs_collected", 0) >= 3:
        completed.append("collect_herbs")
    if state.quest_progress.get("reported_to_apothecary", 0) >= 1:
        completed.append("report_to_apothecary")
    if "old_hunter_trail" in state.clues:
        completed.append("discover_old_hunter_trail")
    return completed


def _failed_objectives(state: RunState, result_type: str) -> list[str]:
    failed: list[str] = []
    if state.quest_progress.get("herbs_collected", 0) < 3:
        failed.append("collect_herbs")
    if state.quest_progress.get("reported_to_apothecary", 0) < 1:
        failed.append("report_to_apothecary")
    if result_type == "failure":
        failed.append("survive_expedition")
    return failed


def _review_text(result_type: str) -> str:
    match result_type:
        case "success":
            return "약초를 모아 보고했고 다음 의뢰의 실마리를 얻었다."
        case "partial_success":
            return "일부 약초와 단서는 얻었지만 의뢰를 완전히 끝내지 못했다."
        case "failure":
            return "원정은 실패했고 자원 관리와 귀환 판단을 다시 봐야 한다."
        case unreachable:
            assert_never(unreachable)
