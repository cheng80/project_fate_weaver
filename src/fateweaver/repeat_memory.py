from __future__ import annotations

from fateweaver.gameplay_models import CooldownCounter, RepeatMemory
from fateweaver.models import JsonMap, JsonValue


def repeat_memory_json(memory: RepeatMemory) -> JsonMap:
    return {
        "recent_presented_cards": list(memory.recent_presented_cards),
        "recent_selected_cards": list(memory.recent_selected_cards),
        "recent_storylets": list(memory.recent_storylets),
        "cooldown_tags": {counter.key: counter.remaining_turns for counter in memory.cooldown_tags},
        "repeat_groups": {counter.key: counter.remaining_turns for counter in memory.repeat_groups},
        "card_counts": {counter.key: counter.remaining_turns for counter in memory.card_counts},
        "repeat_group_counts": {counter.key: counter.remaining_turns for counter in memory.repeat_group_counts},
    }


def update_repeat_memory(memory: RepeatMemory, result: JsonMap) -> RepeatMemory:
    return RepeatMemory(
        recent_presented_cards=_string_tuple(result.get("presented_card_ids", [])),
        recent_selected_cards=_string_tuple(result.get("selected_card_ids", [])),
        recent_storylets=_recent_storylets(memory, result),
        cooldown_tags=_refresh_counters(memory.cooldown_tags, _string_tuple(result.get("cooldown_tags", []))),
        repeat_groups=_refresh_counters(memory.repeat_groups, _repeat_group_tuple(result)),
        card_counts=_increment_counters(memory.card_counts, _string_tuple(result.get("presented_card_ids", []))),
        repeat_group_counts=_increment_counters(memory.repeat_group_counts, _repeat_group_tuple(result)),
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


def _increment_counters(counters: tuple[CooldownCounter, ...], additions: tuple[str, ...]) -> tuple[CooldownCounter, ...]:
    counts = {counter.key: counter.remaining_turns for counter in counters}
    for key in additions:
        counts[key] = counts.get(key, 0) + 1
    return tuple(CooldownCounter(key, count) for key, count in sorted(counts.items()))


def _string_tuple(raw: JsonValue) -> tuple[str, ...]:
    if not isinstance(raw, list | tuple):
        return ()
    return tuple(str(value) for value in raw)
