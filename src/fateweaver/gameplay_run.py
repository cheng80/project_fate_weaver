from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from random import Random

from fateweaver.card_selection import select_cards_from_pool
from fateweaver.card_candidate_json import card_candidate_pool_json, card_json
from fateweaver.card_candidates import build_card_candidate_pool
from fateweaver.gameplay_setup import load_foundation
from fateweaver.quest_lifecycle import complete_quest_lifecycle
from fateweaver.gameplay_models import CardCandidateContext, CardSelectionContext, GameplayRunRequest, Quest, RunState, TurnLogRequest
from fateweaver.quest_objectives import QuestReportRequest, build_quest_report, quest_completed
from fateweaver.gameplay_rules import (
    advance_clock,
    apply_turn_result,
    clock_json,
    combined_result,
    influences,
    initial_state,
    int_map,
    multi_select_json,
    ontology_event_weight,
    repeat_memory_json,
    select_cards,
    select_storylet,
)
from fateweaver.quest_sequence import load_next_foundation
from fateweaver.logger import save_run_log
from fateweaver.models import Event, JsonMap
from fateweaver.ontology_reasoner import OntologyReasonerContext, load_ontology_core, run_reasoner
from fateweaver.state_manager import is_failed
from fateweaver.text_mud_log import save_text_mud_log


def run_gameplay(request: GameplayRunRequest) -> Path:
    foundation = load_foundation(request.bundle.project_root, request.scenario.active_quest_id)
    ontology_core = load_ontology_core(request.bundle.project_root)
    rng = Random(request.seed + request.run_number - 1)
    state = initial_state(request.scenario, foundation.quest)
    turns: list[JsonMap] = []
    onboarding_reason = "run_start"
    while (
        len(turns) < request.scenario.target_turns
        and state.clock.turn <= state.clock.max_turns
        and not is_failed(state.status, request.bundle.statuses)
    ):
        ontology_inference = run_reasoner(ontology_core, _ontology_context(foundation.quest.id, state))
        event = select_storylet(request.events, state, rng, foundation.quest.id, ontology_inference)
        context = card_candidate_context(foundation.quest, event, state, ontology_inference)
        candidate_pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        selection = select_cards_from_pool(candidate_pool, _selection_context(request, foundation.quest, state))
        candidate_pool = selection.candidate_pool
        cards = selection.cards
        selected_cards, combo = select_cards(cards, foundation.card_rules.combos, state, request.profile)
        result = combined_result(selected_cards, combo, foundation.card_rules.default_extra_cost)
        result["storylet_id"] = event.id
        result["cooldown_tags"] = list(context.cooldown_tags)
        result["repeat_group"] = context.repeat_group
        result["presented_card_ids"] = [card.id for card in cards]
        result["selected_card_ids"] = [card.id for card in selected_cards]
        before = state
        state = apply_turn_result(state, result, request.bundle)
        lifecycle: JsonMap = {}
        if quest_completed(foundation.quest, state, request.bundle, foundation.score_rules):
            next_foundation = load_next_foundation(request.bundle.project_root, request.scenario, foundation.quest.id)
            next_quest = None if next_foundation is None else next_foundation.quest
            state, lifecycle = complete_quest_lifecycle(foundation.quest, state, request.bundle, foundation.score_rules, next_quest)
        turn = _turn_log(
            TurnLogRequest(
                quest=foundation.quest,
                before=before,
                after=state,
                event=event,
                context=context,
                candidate_pool=candidate_pool,
                cards=cards,
                selected=selected_cards,
                combo=combo,
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
        turns.append(turn)
        if lifecycle and not lifecycle.get("run_complete") and next_foundation is not None:
            foundation = next_foundation
            state = _continue_state(state, event)
            onboarding_reason = "quest_transition"
            continue
        if lifecycle or is_failed(state.status, request.bundle.statuses):
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


def _ontology_context(quest_id: str, state: RunState) -> OntologyReasonerContext:
    return OntologyReasonerContext(
        quest_id=quest_id,
        region=state.region,
        status=state.status,
        inventory=state.inventory,
        clues=state.clues,
        omens=state.omens,
        quest_progress=state.quest_progress,
        next_event_tags=state.next_event_tags,
    )


def storylet_tags(event: Event, state: RunState) -> tuple[str, ...]:
    tags = (*event.region_tags, *event.event_tags, *event.danger_tags, *event.storylet_tags, *state.next_event_tags)
    if state.region == "forest" and state.quest_progress.get("herbs_collected", 0) >= 2:
        tags = (*tags, "npc", "aid_opportunity", "injured_traveler", "quest_related")
    return tuple(dict.fromkeys(tags))


def card_candidate_context(quest: Quest, event: Event, state: RunState, ontology_inference: JsonMap | None = None) -> CardCandidateContext:
    return CardCandidateContext(
        quest=quest,
        storylet_tags=storylet_tags(event, state),
        storylet_id=event.id,
        card_candidate_hints=event.card_candidate_hints,
        cooldown_tags=event.cooldown_tags,
        repeat_group=event.repeat_group,
        ontology_inference=ontology_inference,
    )


def _selection_context(request: GameplayRunRequest, quest: Quest, state: RunState) -> CardSelectionContext:
    return CardSelectionContext(
        scenario_id=request.scenario.id,
        seed=request.seed,
        run_number=request.run_number,
        active_quest_id=quest.id,
        day=state.clock.day,
        turn=state.clock.turn,
        current_region=state.region,
    )


def _turn_log(request: TurnLogRequest) -> JsonMap:
    selected_ids = [card.id for card in request.selected]
    selected_text = " + ".join(card.title for card in request.selected)
    return {
        "turn": request.before.clock.turn,
        "run_clock": clock_json(request.before.clock),
        "quest_id": request.quest.id,
        "quest_title": request.quest.title,
        "event_id": request.event.id,
        "event_name": request.event.name,
        "event_description": request.event.description,
        "region_tags": [request.before.region],
        "event_tags": list(request.event.event_tags),
        "storylet_id": request.context.storylet_id,
        "storylet_tags": list(request.context.storylet_tags),
        "card_candidate_hints": list(request.context.card_candidate_hints),
        "cooldown_tags": list(request.context.cooldown_tags),
        "repeat_group": request.context.repeat_group,
        "ontology_inference": request.ontology_inference,
        "ontology_weight_applied": ontology_event_weight(request.event, request.ontology_inference),
        "danger_tags": list(request.event.danger_tags),
        "state_before": dict(request.before.status),
        "inventory_before": list(request.before.inventory),
        "repeat_memory_snapshot": repeat_memory_json(request.before.repeat_memory),
        "card_candidate_pool": card_candidate_pool_json(request.candidate_pool),
        "choices_seen": [card_json(card) for card in request.cards],
        "presented_cards": [card_json(card) for card in request.cards],
        "selected_choice_id": request.selected[0].id,
        "selected_choice_type": "multi_select" if request.combo is not None else request.selected[0].slot_role,
        "selected_choice_reason": "gameplay_run: selected combo" if request.combo is not None else "gameplay_run: selected quest progress",
        "selected_cards": selected_ids,
        "multi_select": multi_select_json(request.combo, selected_ids),
        "was_available": True,
        "was_hidden": False,
        "choice_time_seconds": 0,
        "choice_reason": selected_text,
        "expected_risk": "medium" if request.combo is not None else "low",
        "influenced_by": influences(request.selected, request.combo),
        "result": request.result,
        "state_after": dict(request.after.status),
        "inventory_after": list(request.after.inventory),
        "quest_progress": dict(request.after.quest_progress),
        "repeat_memory_after": repeat_memory_json(request.after.repeat_memory),
        "score": dict(request.after.score),
        "score_change": int_map(request.result.get("score_changes", {})),
        "next_event_tags": list(request.after.next_event_tags),
        "clues": list(request.after.clues),
        "omens": list(request.after.omens),
        "regret_score": 3 if request.combo is not None else 1,
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
