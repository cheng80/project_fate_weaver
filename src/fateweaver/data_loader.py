from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from fateweaver.models import (
    Choice,
    Ending,
    Event,
    Item,
    JsonMap,
    JsonValue,
    LoadedProject,
    ProjectData,
    ResultPoolEntry,
    Scenario,
    StatusDefinition,
    StatusRequirement,
)


@dataclass(frozen=True, slots=True)
class DuplicateEventIdError(ValueError):
    event_id: str
    first_source: Path
    duplicate_source: Path

    def __str__(self) -> str:
        return f"Duplicate event id {self.event_id}: {self.first_source} and {self.duplicate_source}"


@dataclass(frozen=True, slots=True)
class DataLoaderTypeError(TypeError):
    label: str
    expected: str

    def __str__(self) -> str:
        return f"{self.label} must be {self.expected}"


def load_project_data(project_root: Path, scenario_path: Path) -> LoadedProject:
    root = project_root.resolve()
    scenario = _load_scenario(root, scenario_path)
    statuses = _load_statuses(root / "data/core/statuses.yaml")
    core_tags = _read_mapping(root / "data/core/tags.yaml")
    choice_types = tuple(_read_string_list(_read_mapping(root / "data/core/choice_types.yaml"), "choice_types"))
    items: dict[str, Item] = {}
    events: list[Event] = []
    endings: dict[str, Ending] = {}
    event_sources: dict[str, Path] = {}
    for source in scenario.content_sources:
        source_path = root / source
        raw = _read_mapping(source_path)
        if "items" in raw:
            items.update(_load_items(raw))
        if "events" in raw:
            for event_raw, event_source in _event_mappings(root, source, raw):
                for event in _load_events(event_raw, event_source):
                    if event.id in event_sources:
                        raise DuplicateEventIdError(event.id, event_sources[event.id], event_source)
                    event_sources[event.id] = event_source
                    events.append(event)
        if "endings" in raw:
            endings.update(_load_endings(raw))
    tags = _mapping_at(core_tags, "tags")
    item_roles = _read_mapping(root / "data/core/item_roles.yaml")
    result_rules = _read_mapping(root / "data/core/result_rules.yaml")
    result_status = _mapping_at(_mapping_at(result_rules, "result_rules"), "status")
    bundle = ProjectData(
        project_root=root,
        statuses=statuses,
        choice_types=choice_types,
        region_tags=tuple(_string_list_at(tags, "region")),
        event_tags=tuple(_string_list_at(tags, "event")),
        danger_tags=tuple(_string_list_at(tags, "danger")),
        item_role_tags=tuple(_string_list_at(tags, "item_role")),
        item_tags=tuple(_string_list_at(tags, "item_tag")),
        weight_targets=tuple(_string_list_at(tags, "weight_target")),
        item_roles=tuple(_mapping_at(item_roles, "item_roles")),
        result_statuses=tuple(_string_list_at(result_status, "allowed")),
        items=items,
        events=tuple(events),
        endings=endings,
    )
    return LoadedProject(bundle=bundle, scenario=scenario)


def _load_scenario(project_root: Path, scenario_path: Path) -> Scenario:
    path = scenario_path if scenario_path.is_absolute() else project_root / scenario_path
    raw = _read_mapping(path)
    return Scenario(
        id=_string_at(raw, "id"),
        name=str(raw.get("name", raw["id"])),
        content_sources=tuple(Path(value) for value in _string_list_at(raw, "content_sources")),
        include_regions=tuple(_string_list_at(raw, "include_regions")),
        include_event_ids=tuple(_optional_string_list(raw, "include_event_ids")),
        include_event_tags=tuple(_optional_string_list(raw, "include_event_tags")),
        exclude_event_ids=tuple(_optional_string_list(raw, "exclude_event_ids")),
        exclude_event_tags=tuple(_optional_string_list(raw, "exclude_event_tags")),
        initial_status={key: int(value) for key, value in _mapping_at(raw, "initial_status").items()},
        initial_items=tuple(_optional_string_list(raw, "initial_items")),
        target_turns=int(raw.get("target_turns", 1)),
        seed=int(raw.get("seed", 0)),
        validation_targets={key: int(value) for key, value in _mapping_at(raw, "validation_targets").items()},
        gameplay_mode=_optional_string(raw, "gameplay_mode"),
        active_quest_id=_optional_string(raw, "active_quest_id"),
        run_clock=_mapping_at(raw, "run_clock"),
    )


def _load_statuses(path: Path) -> dict[str, StatusDefinition]:
    raw_statuses = _mapping_at(_read_mapping(path), "statuses")
    statuses: dict[str, StatusDefinition] = {}
    for status_id, raw_value in raw_statuses.items():
        value = _as_mapping(raw_value, f"statuses.{status_id}")
        fail_when = value.get("fail_when")
        statuses[status_id] = StatusDefinition(
            id=status_id,
            minimum=int(value["min"]),
            maximum=int(value["max"]),
            initial=int(value["initial"]),
            fail_when=None if fail_when is None else int(fail_when),
        )
    return statuses


def _load_items(raw: JsonMap) -> dict[str, Item]:
    items: dict[str, Item] = {}
    for raw_item in _list_at(raw, "items"):
        item = _as_mapping(raw_item, "items[]")
        item_id = _string_at(item, "id")
        items[item_id] = Item(
            id=item_id,
            name=str(item.get("name", item_id)),
            roles=tuple(_optional_string_list(item, "roles")),
            tags=tuple(_optional_string_list(item, "tags")),
            counters=tuple(_optional_string_list(item, "counters")),
        )
    return items


def _event_mappings(project_root: Path, source: Path, raw: JsonMap) -> tuple[tuple[JsonMap, Path], ...]:
    event_mappings: list[tuple[JsonMap, Path]] = [(raw, source)]
    if source != Path("data/content/base/events.yaml"):
        return tuple(event_mappings)

    split_dir = project_root / "data/content/events"
    if not split_dir.exists():
        return tuple(event_mappings)

    for split_path in sorted(split_dir.glob("*.yaml")):
        event_mappings.append((_read_mapping(split_path), Path("data/content/events") / split_path.name))
    return tuple(event_mappings)


def _load_events(raw: JsonMap, source_path: Path) -> tuple[Event, ...]:
    events: list[Event] = []
    for raw_event in _list_at(raw, "events"):
        event = _as_mapping(raw_event, "events[]")
        events.append(
            Event(
                id=_string_at(event, "id"),
                name=str(event.get("name", event["id"])),
                description=str(event.get("description", "")),
                source_path=source_path,
                region_tags=tuple(_optional_string_list(event, "region_tags")),
                event_tags=tuple(_optional_string_list(event, "event_tags")),
                danger_tags=tuple(_optional_string_list(event, "danger_tags")),
                storylet_tags=tuple(_optional_string_list(event, "storylet_tags")),
                card_candidate_hints=tuple(_optional_string_list(event, "card_candidate_hints")),
                cooldown_tags=tuple(_optional_string_list(event, "cooldown_tags")),
                repeat_group=str(event.get("repeat_group", "")),
                quest_ids=tuple(_optional_string_list(event, "quest_ids")),
                base_weight=int(event.get("base_weight", 1)),
                choices=tuple(_load_choice(raw_choice) for raw_choice in _list_at(event, "choices")),
                max_occurrences_per_run=_optional_int(event, "max_occurrences_per_run"),
                cooldown_turns=_optional_int(event, "cooldown_turns"),
                requires_item=_optional_string(event, "requires_item"),
                requires_status=_status_requirements(event.get("requires_status")),
                requires_run_tag=_optional_string(event, "requires_run_tag"),
            )
        )
    return tuple(events)


def _load_choice(raw_choice: JsonValue) -> Choice:
    choice = _as_mapping(raw_choice, "choices[]")
    return Choice(
        id=_string_at(choice, "id"),
        text=str(choice.get("text", choice["id"])),
        choice_type=_string_at(choice, "type"),
        risk_level=_optional_string(choice, "risk_level"),
        result=_as_mapping(choice.get("result", {}), "choice.result"),
        result_pool=tuple(_load_result_pool(choice.get("result_pool", []))),
        requires_item=_optional_string(choice, "requires_item"),
        requires_status=_status_requirements(choice.get("requires_status")),
        requires_run_tag=_optional_string(choice, "requires_run_tag"),
        hidden=bool(choice.get("hidden", False)),
        visible_when_unavailable=bool(choice.get("visible_when_unavailable", choice.get("show_when_unavailable", True))),
    )


def _load_result_pool(raw_pool: JsonValue) -> tuple[ResultPoolEntry, ...]:
    entries: list[ResultPoolEntry] = []
    for raw_entry in _as_list(raw_pool, "result_pool"):
        entry = _as_mapping(raw_entry, "result_pool[]")
        entries.append(ResultPoolEntry(when=_mapping_at(entry, "when"), result=_mapping_at(entry, "result")))
    return tuple(entries)


def _load_endings(raw: JsonMap) -> dict[str, Ending]:
    endings: dict[str, Ending] = {}
    for raw_ending in _list_at(raw, "endings"):
        ending = _as_mapping(raw_ending, "endings[]")
        ending_id = _string_at(ending, "id")
        endings[ending_id] = Ending(
            id=ending_id,
            name=str(ending.get("name", ending_id)),
            condition=_mapping_at(ending, "condition"),
        )
    return endings


def _status_requirements(raw: JsonValue) -> dict[str, StatusRequirement]:
    if raw is None:
        return {}
    requirements: dict[str, StatusRequirement] = {}
    for key, value in _as_mapping(raw, "requires_status").items():
        bounds = _as_mapping(value, f"requires_status.{key}")
        requirements[key] = StatusRequirement(
            minimum=None if bounds.get("min") is None else int(bounds["min"]),
            maximum=None if bounds.get("max") is None else int(bounds["max"]),
        )
    return requirements


def _read_mapping(path: Path) -> JsonMap:
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    return _as_mapping(loaded, str(path))


def _mapping_at(raw: JsonMap, key: str) -> JsonMap:
    return _as_mapping(raw.get(key, {}), key)


def _list_at(raw: JsonMap, key: str) -> list[JsonValue]:
    return _as_list(raw.get(key, []), key)


def _string_at(raw: JsonMap, key: str) -> str:
    value = raw[key]
    if not isinstance(value, str):
        raise DataLoaderTypeError(key, "a string")
    return value


def _string_list_at(raw: JsonMap, key: str) -> list[str]:
    return _read_string_list(raw, key)


def _optional_string_list(raw: JsonMap, key: str) -> list[str]:
    return _read_string_list(raw, key) if key in raw else []


def _read_string_list(raw: JsonMap, key: str) -> list[str]:
    values = _as_list(raw.get(key, []), key)
    strings: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise DataLoaderTypeError(f"{key} values", "strings")
        strings.append(value)
    return strings


def _optional_string(raw: JsonMap, key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise DataLoaderTypeError(key, "a string")
    return value


def _optional_int(raw: JsonMap, key: str) -> int | None:
    value = raw.get(key)
    return None if value is None else int(value)


def _as_mapping(value: JsonValue, label: str) -> JsonMap:
    if not isinstance(value, dict):
        raise DataLoaderTypeError(label, "a mapping")
    return {str(key): item for key, item in value.items()}


def _as_list(value: JsonValue, label: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise DataLoaderTypeError(label, "a list")
    return value
