from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeAlias


JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonMap: TypeAlias = dict[str, JsonValue]
StatusMap: TypeAlias = dict[str, int]


@dataclass(frozen=True, slots=True)
class StatusDefinition:
    id: str
    minimum: int
    maximum: int
    initial: int
    fail_when: int | None


@dataclass(frozen=True, slots=True)
class Item:
    id: str
    name: str
    roles: tuple[str, ...]
    tags: tuple[str, ...]
    counters: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StatusRequirement:
    minimum: int | None = None
    maximum: int | None = None


@dataclass(frozen=True, slots=True)
class ResultPoolEntry:
    when: JsonMap
    result: JsonMap


@dataclass(frozen=True, slots=True)
class Choice:
    id: str
    text: str
    choice_type: str
    risk_level: str | None
    result: JsonMap
    result_pool: tuple[ResultPoolEntry, ...]
    requires_item: str | None
    requires_status: dict[str, StatusRequirement]
    requires_run_tag: str | None
    hidden: bool
    visible_when_unavailable: bool


@dataclass(frozen=True, slots=True)
class Event:
    id: str
    name: str
    description: str
    source_path: Path
    region_tags: tuple[str, ...]
    event_tags: tuple[str, ...]
    danger_tags: tuple[str, ...]
    base_weight: int
    choices: tuple[Choice, ...]
    max_occurrences_per_run: int | None
    cooldown_turns: int | None
    requires_item: str | None
    requires_status: dict[str, StatusRequirement]
    requires_run_tag: str | None
    storylet_tags: tuple[str, ...] = ()
    card_candidate_hints: tuple[str, ...] = ()
    cooldown_tags: tuple[str, ...] = ()
    repeat_group: str = ""
    quest_ids: tuple[str, ...] = ()

    def __getitem__(self, key: str) -> JsonValue:
        match key:  # noqa: MATCH_OK - Event mapping keys are data compatibility surface.
            case "id":
                return self.id
            case "name":
                return self.name
            case "description":
                return self.description
            case "region_tags":
                return list(self.region_tags)
            case "event_tags":
                return list(self.event_tags)
            case "danger_tags":
                return list(self.danger_tags)
            case "storylet_tags":
                return list(self.storylet_tags)
            case "card_candidate_hints":
                return list(self.card_candidate_hints)
            case "cooldown_tags":
                return list(self.cooldown_tags)
            case "repeat_group":
                return self.repeat_group
            case "quest_ids":
                return list(self.quest_ids)
            case "base_weight":
                return self.base_weight
            case _:
                raise KeyError(key)


@dataclass(frozen=True, slots=True)
class Ending:
    id: str
    name: str
    condition: JsonMap


@dataclass(frozen=True, slots=True)
class Scenario:
    id: str
    name: str
    content_sources: tuple[Path, ...]
    include_regions: tuple[str, ...]
    include_event_ids: tuple[str, ...]
    include_event_tags: tuple[str, ...]
    exclude_event_ids: tuple[str, ...]
    exclude_event_tags: tuple[str, ...]
    initial_status: StatusMap
    initial_items: tuple[str, ...]
    target_turns: int
    seed: int
    validation_targets: dict[str, int] = field(default_factory=dict)
    gameplay_mode: str | None = None
    active_quest_id: str | None = None
    run_clock: JsonMap = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProjectData:
    project_root: Path
    statuses: dict[str, StatusDefinition]
    choice_types: tuple[str, ...]
    region_tags: tuple[str, ...]
    event_tags: tuple[str, ...]
    danger_tags: tuple[str, ...]
    item_role_tags: tuple[str, ...]
    item_tags: tuple[str, ...]
    weight_targets: tuple[str, ...]
    item_roles: tuple[str, ...]
    result_statuses: tuple[str, ...]
    items: dict[str, Item]
    events: tuple[Event, ...]
    endings: dict[str, Ending]

    @property
    def events_by_id(self) -> dict[str, Event]:
        return {event.id: event for event in self.events}


@dataclass(frozen=True, slots=True)
class LoadedProject:
    bundle: ProjectData
    scenario: Scenario

    def __iter__(self) -> Iterator[ProjectData | Scenario]:
        yield self.bundle
        yield self.scenario


@dataclass(frozen=True, slots=True)
class ChoiceSeen:
    choice_id: str
    choice_type: str
    available: bool
    unavailable_reason: str | None
    hidden: bool
    expected_risk: str
    influenced_by: tuple[str, ...]
    result: JsonMap


@dataclass(frozen=True, slots=True)
class StateSnapshot:
    status: StatusMap
    inventory: tuple[str, ...]
    run_tags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PlayerChoiceFeedback:
    choice_reason: str
    expected_risk: str
    regret_score: int


@dataclass(frozen=True, slots=True)
class RunFeedback:
    fairness_score: int
    restart_intent_score: int
    player_woven_score: int
    narrative_summary: str
    most_memorable_choice: str
    next_run_intent: str
