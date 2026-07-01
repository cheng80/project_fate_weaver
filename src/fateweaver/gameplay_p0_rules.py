from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from random import Random

from fateweaver.choice_resolver import requirements_met
from fateweaver.event_selector import select_event
from fateweaver.gameplay_p0_errors import ExpectedMappingError
from fateweaver.gameplay_p0_models import TIME_OF_DAY, CardRule, ComboRule, CooldownCounter, Quest, RepeatMemory, RunClock, RunState
from fateweaver.models import Event, JsonMap, JsonValue, ProjectData, Scenario
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
        recent_presented_card_ids=(),
        selected_choice_history=(),
        repeat_memory=RepeatMemory(),
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


def select_storylet(
    events: tuple[Event, ...],
    state: RunState,
    rng: Random,
    quest_id: str = "",
    ontology_inference: JsonMap | None = None,
) -> Event:
    gated = tuple(event for event in events if not event.quest_ids or quest_id in event.quest_ids)
    regional = tuple(event for event in gated if state.region in event.region_tags)
    pool = regional if regional else gated
    if ontology_inference:
        return _select_event_with_ontology_weight(pool, state, rng, ontology_inference)
    return select_event(pool, state.status, state.inventory, state.run_tags, rng, state.recent_event_ids)


def ontology_event_weight(event: Event, ontology_inference: JsonMap | None) -> int:
    if not ontology_inference:
        return 0
    event_tags = set((*event.region_tags, *event.event_tags, *event.danger_tags, *event.storylet_tags, *event.card_candidate_hints))
    total = 0
    for modifier in _modifier_maps(ontology_inference.get("event_weight_modifiers", [])):
        tags = set(string_tuple(modifier.get("tags", [])))
        if event_tags & tags:
            total += int(modifier.get("amount", 0))
    return total


def _select_event_with_ontology_weight(events: tuple[Event, ...], state: RunState, rng: Random, ontology_inference: JsonMap) -> Event:
    eligible = tuple(event for event in events if _event_eligible(event, state))
    if not eligible:
        raise ValueError("No eligible events")
    weights = tuple(max(1, event.base_weight + min(1, ontology_event_weight(event, ontology_inference))) for event in eligible)
    threshold = rng.uniform(0, float(sum(weights)))
    cursor = 0.0
    for event, weight in zip(eligible, weights):
        cursor += float(weight)
        if threshold <= cursor:
            return event
    return eligible[-1]


def _event_eligible(event: Event, state: RunState) -> bool:
    if not requirements_met(event.requires_item, event.requires_status, event.requires_run_tag, state.status, state.inventory, state.run_tags):
        return False
    if event.max_occurrences_per_run is not None and state.recent_event_ids.count(event.id) >= event.max_occurrences_per_run:
        return False
    if event.cooldown_turns is not None and event.id in state.recent_event_ids[-event.cooldown_turns :]:
        return False
    return True


def _modifier_maps(raw: JsonValue) -> tuple[JsonMap, ...]:
    if not isinstance(raw, list):
        return ()
    return tuple(item for item in raw if isinstance(item, dict))


def select_cards(
    cards: tuple[CardRule, CardRule, CardRule],
    combos: tuple[ComboRule, ...],
    state: RunState,
    profile: str,
) -> tuple[tuple[CardRule, ...], ComboRule | None]:
    combo = available_combo(cards, combos)
    if combo is not None and not state.combo_used:
        return tuple(card for card in cards if card.id in combo.cards), combo
    if _should_select_optional_resource(cards, state, profile):
        return (cards[2],), None
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
        recent_presented_card_ids=string_tuple(merged.get("presented_card_ids", [])),
        selected_choice_history=(*state.selected_choice_history, *string_tuple(merged.get("selected_card_ids", []))),
        repeat_memory=update_repeat_memory(state.repeat_memory, merged),
        combo_used=state.combo_used or "multi_select_rule" in merged,
    )


def advance_clock(clock: RunClock) -> RunClock:
    next_turns_today = clock.turns_today + 1
    next_turn = clock.turn + 1
    if next_turns_today >= clock.turns_per_day:
        return replace(clock, day=clock.day + 1, turn=next_turn, turns_today=0, time_of_day="morning", act=min(5, clock.act + 1))
    return replace(clock, turn=next_turn, turns_today=next_turns_today, time_of_day=TIME_OF_DAY[next_turns_today])


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


def repeat_memory_json(memory: RepeatMemory) -> JsonMap:
    return {
        "recent_presented_cards": list(memory.recent_presented_cards),
        "recent_selected_cards": list(memory.recent_selected_cards),
        "recent_storylets": list(memory.recent_storylets),
        "cooldown_tags": {counter.key: counter.remaining_turns for counter in memory.cooldown_tags},
        "repeat_groups": {counter.key: counter.remaining_turns for counter in memory.repeat_groups},
    }


def update_repeat_memory(memory: RepeatMemory, result: JsonMap) -> RepeatMemory:
    return RepeatMemory(
        recent_presented_cards=string_tuple(result.get("presented_card_ids", [])),
        recent_selected_cards=string_tuple(result.get("selected_card_ids", [])),
        recent_storylets=_recent_storylets(memory, result),
        cooldown_tags=_refresh_counters(memory.cooldown_tags, string_tuple(result.get("cooldown_tags", []))),
        repeat_groups=_refresh_counters(memory.repeat_groups, _repeat_group_tuple(result)),
    )


def _recent_storylets(memory: RepeatMemory, result: JsonMap) -> tuple[str, ...]:
    storylet_id = str(result.get("storylet_id", ""))
    if not storylet_id:
        return memory.recent_storylets[-2:]
    return (*memory.recent_storylets[-2:], storylet_id)


def _repeat_group_tuple(result: JsonMap) -> tuple[str, ...]:
    repeat_group = str(result.get("repeat_group", ""))
    return () if not repeat_group else (repeat_group,)


def _refresh_counters(counters: tuple[CooldownCounter, ...], additions: tuple[str, ...]) -> tuple[CooldownCounter, ...]:
    refreshed = {
        counter.key: counter.remaining_turns - 1
        for counter in counters
        if counter.remaining_turns > 1
    }
    for key in additions:
        refreshed[key] = 2
    return tuple(CooldownCounter(key, turns) for key, turns in sorted(refreshed.items()))


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
        and cards[1].id not in state.selected_choice_history
    )


def _should_select_optional_resource(cards: tuple[CardRule, CardRule, CardRule], state: RunState, profile: str) -> bool:
    return (
        profile == "curious_leaning"
        and state.region == "forest"
        and state.quest_progress.get("herbs_collected", 0) >= 2
        and bool(cards[2].applies_to_quest_objectives)
        and cards[2].id not in state.selected_choice_history
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
        match key:  # noqa: MATCH_OK - result payload keys are open-ended data.
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
        raise ExpectedMappingError(type(value).__name__)
    return {str(key): item for key, item in value.items()}
