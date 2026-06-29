from __future__ import annotations

from fateweaver.models import Event, Scenario


def filter_events_for_scenario(events: tuple[Event, ...], scenario: Scenario) -> tuple[Event, ...]:
    filtered: list[Event] = []
    include_ids = set(scenario.include_event_ids)
    include_tags = set(scenario.include_event_tags)
    exclude_ids = set(scenario.exclude_event_ids)
    exclude_tags = set(scenario.exclude_event_tags)
    regions = set(scenario.include_regions)
    for event in events:
        if regions and not regions.intersection(event.region_tags):
            continue
        if include_ids and event.id not in include_ids:
            continue
        if include_tags and not include_tags.intersection(event.event_tags):
            continue
        if event.id in exclude_ids:
            continue
        if exclude_tags.intersection(event.event_tags):
            continue
        filtered.append(event)
    return tuple(filtered)
