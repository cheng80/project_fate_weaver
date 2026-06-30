from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from random import Random

from fateweaver.event_selector import select_event
from fateweaver.gameplay_p0_models import TIME_OF_DAY, CardRule, ComboRule, Quest, RunClock, RunState
from fateweaver.models import Event, JsonMap, JsonValue, ProjectData, Scenario, StatusMap
from fateweaver.state_manager import apply_choice_result


def initial_state(scenario: Scenario, quest: Quest) -> RunState:
    return RunState(
        clock=run_clock(scenario, quest),
        status=dict(scenario.initial_status),
        inventory=tuple(scenario.initial_items),
        run_tags=(),
        region=quest.start_region,
        quest_progress={},
        clues=(),
        omens=(),
        score={},
        next_event_tags=(),
        recent_event_ids=(),
        selected_choice_history=(),
        combo_used=False,
    )


def run_clock(scenario: Scenario, quest: Quest) -> RunClock:
    raw = scenario.run_clock
    return RunClock(
        day=int(raw.get("day", 1)),
        turn=int(raw.get("turn", 1)),
        turns_today=int(raw.get("turns_today", 0)),
        time_of_day=str(raw.get("time_of_day", "morning")),
        act=int(raw.get("act", 1)),
        max_days=int(raw.get("max_days", quest.max_days)),
        max_turns=int(raw.get("max_turns", quest.max_turns)),
        turns_per_day=int(raw.get("turns_per_day", 4)),
    )


def select_storylet(events: tuple[Event, ...], state: RunState, rng: Random) -> Event:
    regional = tuple(event for event in events if state.region in event.region_tags)
    pool = regional if regional else events
    return select_event(pool, state.status, state.inventory, state.run_tags, rng, state.recent_event_ids)


def present_cards(cards: tuple[CardRule, ...], state: RunState) -> tuple[CardRule, CardRule, CardRule]:
    visible = tuple(card for card in cards if card_available(card, state))
    return (
        quest_card(visible, state),
        first_for_slot(visible, "risk_discovery"),
        first_for_slot(visible, "resource_alternative"),
    )


def select_cards(
    cards: tuple[CardRule, CardRule, CardRule],
    combos: tuple[ComboRule, ...],
    state: RunState,
    profile: str,
) -> tuple[tuple[CardRule, ...], ComboRule | None]:
    combo = available_combo(cards, combos)
    if combo is not None and not state.combo_used:
        return tuple(card for card in cards if card.id in combo.cards), combo
    if _should_select_discovery(cards, state, profile):
        return (cards[1],), None
    if _should_select_resource(cards, state, profile):
        return (cards[2],), None
    return (cards[0],), None


def combined_result(cards: tuple[CardRule, ...], combo: ComboRule | None, default_cost: JsonMap) -> JsonMap:
    result: JsonMap = {}
    for card in cards:
        result = merge_result(result, card.result)
    if combo is None:
        return result
    result = merge_result(result, default_cost)
    result = merge_result(result, combo.result)
    result["multi_select_rule"] = combo.id
    return result


def apply_turn_result(state: RunState, result: JsonMap, bundle: ProjectData) -> RunState:
    merged = merge_result(result, day_end_result(state.clock))
    transition = apply_choice_result(state.status, state.inventory, state.run_tags, merged, bundle.statuses)
    return replace(
        state,
        status=transition.status,
        inventory=transition.inventory,
        run_tags=transition.run_tags,
        region=str(merged.get("move_to_region", state.region)),
        quest_progress=merge_ints(state.quest_progress, int_map(merged.get("quest_progress", {}))),
        clues=append_unique(state.clues, string_tuple(merged.get("gain_clues", []))),
        omens=append_unique(state.omens, string_tuple(merged.get("gain_omens", []))),
        score=merge_ints(state.score, int_map(merged.get("score_changes", {}))),
        next_event_tags=append_unique(state.next_event_tags, string_tuple(merged.get("next_event_tags", []))),
        selected_choice_history=(*state.selected_choice_history, *string_tuple(merged.get("selected_card_ids", []))),
        combo_used=state.combo_used or "multi_select_rule" in merged,
    )


def advance_clock(clock: RunClock) -> RunClock:
    next_turns_today = clock.turns_today + 1
    next_turn = clock.turn + 1
    if next_turns_today >= clock.turns_per_day:
        return replace(clock, day=clock.day + 1, turn=next_turn, turns_today=0, time_of_day="morning", act=min(5, clock.act + 1))
    return replace(clock, turn=next_turn, turns_today=next_turns_today, time_of_day=TIME_OF_DAY[next_turns_today])


def card_json(card: CardRule) -> JsonMap:
    return {
        "choice_id": card.id,
        "card_id": card.id,
        "choice_text": card.title,
        "title": card.title,
        "description": card.description,
        "slot_role": card.slot_role,
        "choice_type": card.slot_role,
        "available": True,
        "unavailable_reason": None,
        "hidden": False,
        "expected_risk": "low" if card.slot_role != "risk_discovery" else "medium",
        "influenced_by": [f"slot:{card.slot_role}"],
        "result": card.result,
    }


def multi_select_json(combo: ComboRule | None, selected_ids: list[str]) -> JsonMap:
    if combo is None:
        return {"selected": False, "selected_cards": selected_ids}
    return {"selected": True, "rule_id": combo.id, "selected_cards": selected_ids, "cost_applied": True, "combo_applied": True}


def influences(selected: tuple[CardRule, ...], combo: ComboRule | None) -> list[str]:
    values: list[str] = []
    for card in selected:
        values.append(f"card:{card.id}")
        values.append(f"slot:{card.slot_role}")
    if combo is not None:
        values.append(f"combo:{combo.id}")
        values.append("cost:default_extra_cost")
    return values


def clock_json(clock: RunClock) -> JsonMap:
    return {
        "day": clock.day,
        "turn": clock.turn,
        "turns_today": clock.turns_today,
        "time_of_day": clock.time_of_day,
        "act": clock.act,
        "max_days": clock.max_days,
        "max_turns": clock.max_turns,
        "turns_per_day": clock.turns_per_day,
    }


def card_available(card: CardRule, state: RunState) -> bool:
    return (
        state.region in card.regions
        and (card.requires_item is None or card.requires_item in state.inventory)
        and progress_matches(card.requires_progress, state.quest_progress)
        and status_matches(card.requires_status, state.status)
    )


def progress_matches(requirements: JsonMap, progress: dict[str, int]) -> bool:
    for key, raw_bounds in requirements.items():
        bounds = as_mapping(raw_bounds)
        minimum = bounds.get("min")
        if minimum is not None and progress.get(key, 0) < int(minimum):
            return False
    return True


def status_matches(requirements: JsonMap, status: StatusMap) -> bool:
    for key, raw_bounds in requirements.items():
        bounds = as_mapping(raw_bounds)
        minimum = bounds.get("min")
        if minimum is not None and status.get(key, 0) < int(minimum):
            return False
    return True


def first_for_slot(cards: tuple[CardRule, ...], slot: str) -> CardRule:
    for card in cards:
        if card.slot_role == slot:
            return card
    raise ValueError(f"No P0 card for slot: {slot}")


def quest_card(cards: tuple[CardRule, ...], state: RunState) -> CardRule:
    target = quest_target_card(state)
    for card in cards:
        if card.id == target:
            return card
    return first_for_slot(cards, "quest_progress")


def quest_target_card(state: RunState) -> str:
    herbs = state.quest_progress.get("herbs_collected", 0)
    returned = state.quest_progress.get("returned_to_village", 0)
    if state.region == "village" and herbs >= 3 and returned >= 1:
        return "report_to_apothecary"
    if state.region == "forest" and herbs >= 3:
        return "return_to_village"
    if state.region == "village":
        return "ask_apothecary"
    return "search_herbs"


def available_combo(cards: tuple[CardRule, ...], combos: tuple[ComboRule, ...]) -> ComboRule | None:
    card_ids = {card.id for card in cards}
    for combo in combos:
        if all(card_id in card_ids for card_id in combo.cards):
            return combo
    return None


def _should_select_discovery(cards: tuple[CardRule, CardRule, CardRule], state: RunState, profile: str) -> bool:
    return (
        profile == "curious_leaning"
        and state.region == "forest"
        and state.quest_progress.get("herbs_collected", 0) >= 2
        and "inspect_tracks" not in state.selected_choice_history
    )


def _should_select_resource(cards: tuple[CardRule, CardRule, CardRule], state: RunState, profile: str) -> bool:
    return (
        profile == "safe_leaning"
        and state.region == "forest"
        and state.quest_progress.get("herbs_collected", 0) >= 2
        and cards[2].id not in state.selected_choice_history
    )


def merge_result(left: JsonMap, right: JsonMap) -> JsonMap:
    merged = dict(left)
    for key, value in right.items():
        match key:
            case "status" | "quest_progress" | "score_changes":
                merged[key] = merge_ints(int_map(merged.get(key, {})), int_map(value))
            case "add_item" | "remove_item" | "gain_clues" | "gain_omens" | "next_event_tags":
                merged[key] = list(append_unique(string_tuple(merged.get(key, [])), string_tuple(value)))
            case "message":
                merged[key] = f"{str(merged.get('message', ''))} {value}".strip()
            case "move_to_region" | "multi_select_rule":
                merged[key] = value
            case _:
                merged[key] = value
    return merged


def day_end_result(clock: RunClock) -> JsonMap:
    if clock.time_of_day != "night":
        return {}
    return {"status": {"food": -1}, "score_changes": {"resource_management": -1}, "message": "밤을 넘기며 식량을 소모했다."}


def int_map(value: JsonValue) -> dict[str, int]:
    return {str(key): int(item) for key, item in as_mapping(value).items()}


def merge_ints(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    merged = dict(left)
    for key, value in right.items():
        merged[key] = merged.get(key, 0) + value
    return merged


def append_unique(values: tuple[str, ...], additions: Iterable[str]) -> tuple[str, ...]:
    result = list(values)
    for value in additions:
        if value not in result:
            result.append(value)
    return tuple(result)


def string_tuple(value: JsonValue) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value)


def as_mapping(value: JsonValue) -> JsonMap:
    if not isinstance(value, dict):
        raise TypeError("value must be a mapping")
    return {str(key): item for key, item in value.items()}
