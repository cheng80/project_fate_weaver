from __future__ import annotations

from random import Random

from fateweaver.choice_resolver import requirements_met
from fateweaver.models import Event, StatusMap


def select_event(
    events: tuple[Event, ...],
    state: StatusMap,
    inventory: tuple[str, ...],
    run_tags: tuple[str, ...] | dict[str, str],
    rng: Random | int,
    recent_event_ids: tuple[str, ...] | Random,
) -> Event:
    active_rng, recent_ids = _normalize_selector_args(rng, recent_event_ids)
    active_run_tags = tuple(run_tags)
    eligible = tuple(
        event
        for event in events
        if _event_is_eligible(event, state, inventory, active_run_tags, recent_ids)
    )
    if not eligible:
        raise ValueError("No eligible events")
    total_weight = sum(max(1, event.base_weight) for event in eligible)
    threshold = active_rng.uniform(0, float(total_weight))
    cursor = 0.0
    for event in eligible:
        cursor += float(max(1, event.base_weight))
        if threshold <= cursor:
            return event
    return eligible[-1]


def _normalize_selector_args(rng: Random | int, recent_event_ids: tuple[str, ...] | Random) -> tuple[Random, tuple[str, ...]]:
    if isinstance(rng, Random):
        return rng, tuple(recent_event_ids) if not isinstance(recent_event_ids, Random) else ()
    if isinstance(recent_event_ids, Random):
        return recent_event_ids, ()
    return Random(rng), tuple(recent_event_ids)


def _event_is_eligible(
    event: Event,
    state: StatusMap,
    inventory: tuple[str, ...],
    run_tags: tuple[str, ...],
    recent_event_ids: tuple[str, ...],
) -> bool:
    if not requirements_met(event.requires_item, event.requires_status, event.requires_run_tag, state, inventory, run_tags):
        return False
    if event.max_occurrences_per_run is not None and recent_event_ids.count(event.id) >= event.max_occurrences_per_run:
        return False
    if event.cooldown_turns is not None and event.id in recent_event_ids[-event.cooldown_turns :]:
        return False
    return True
