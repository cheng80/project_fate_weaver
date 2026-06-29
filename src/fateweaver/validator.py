from __future__ import annotations

from pathlib import Path

from fateweaver.models import Choice, Event, JsonMap, JsonValue, ProjectData, Scenario
from fateweaver.scenario_filter import filter_events_for_scenario


def validate_bundle(bundle: ProjectData, scenario: Scenario) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_scenario_references(bundle, scenario))
    errors.extend(_validate_events(bundle, bundle.events))
    errors.extend(_validate_targets(bundle, scenario))
    return errors


def validate_scenario_file(project_root: Path, scenario_path: Path) -> list[str]:
    from fateweaver.data_loader import load_project_data

    if not scenario_path.exists():
        return [f"Scenario path does not exist: {scenario_path}"]
    try:
        bundle, scenario = load_project_data(project_root, scenario_path)
    except (OSError, TypeError, ValueError) as error:
        return [str(error)]
    return validate_bundle(bundle, scenario)


def _validate_scenario_references(bundle: ProjectData, scenario: Scenario) -> list[str]:
    errors: list[str] = []
    for source in scenario.content_sources:
        if not (bundle.project_root / source).exists():
            errors.append(f"Content source does not exist: {source}")
    region_tags = set(bundle.region_tags)
    for region in scenario.include_regions:
        if region not in region_tags:
            errors.append(f"Unknown include region: {region}")
    for key in scenario.initial_status:
        if key not in bundle.statuses:
            errors.append(f"Unknown initial status: {key}")
    for item_id in scenario.initial_items:
        if item_id not in bundle.items:
            errors.append(f"Unknown initial item: {item_id}")
    min_item_count = scenario.validation_targets.get("min_item_count")
    if min_item_count is not None and len(bundle.items) < min_item_count:
        errors.append(f"Item count {len(bundle.items)} below validation target: {min_item_count}")
    return errors


def _validate_events(bundle: ProjectData, events: tuple[Event, ...]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for event in events:
        if event.id in seen:
            errors.append(f"Duplicate event id: {event.id}")
        seen.add(event.id)
        for region_tag in event.region_tags:
            if region_tag not in bundle.region_tags:
                errors.append(f"Unknown region tag {region_tag} in {event.id}")
        for event_tag in event.event_tags:
            if event_tag not in bundle.event_tags:
                errors.append(f"Unknown event tag {event_tag} in {event.id}")
        for danger_tag in event.danger_tags:
            if danger_tag not in bundle.danger_tags:
                errors.append(f"Unknown danger tag {danger_tag} in {event.id}")
        errors.extend(_validate_requirement(bundle, event.id, event.requires_item, event.requires_status))
        for choice in event.choices:
            errors.extend(_validate_choice(bundle, event, choice))
    for item in bundle.items.values():
        for role in item.roles:
            if role not in bundle.item_roles or role not in bundle.item_role_tags:
                errors.append(f"Unknown item role {role} in {item.id}")
        for tag in item.tags:
            if tag not in bundle.item_tags:
                errors.append(f"Unknown item tag {tag} in {item.id}")
    return errors


def _validate_choice(bundle: ProjectData, event: Event, choice: Choice) -> list[str]:
    errors: list[str] = []
    if choice.choice_type not in bundle.choice_types:
        errors.append(f"Unknown choice type {choice.choice_type} in {event.id}/{choice.id}")
    errors.extend(_validate_requirement(bundle, f"{event.id}/{choice.id}", choice.requires_item, choice.requires_status))
    errors.extend(_validate_result(bundle, f"{event.id}/{choice.id}", choice.result))
    for entry in choice.result_pool:
        errors.extend(_validate_result(bundle, f"{event.id}/{choice.id}", entry.result))
    return errors


def _validate_requirement(
    bundle: ProjectData,
    label: str,
    requires_item: str | None,
    requires_status: JsonValue,
) -> list[str]:
    errors: list[str] = []
    if requires_item is not None and requires_item not in bundle.items:
        errors.append(f"Unknown required item {requires_item} in {label}")
    if isinstance(requires_status, dict):
        for key in requires_status:
            if str(key) not in bundle.statuses:
                errors.append(f"Unknown required status {key} in {label}")
    return errors


def _validate_result(bundle: ProjectData, label: str, result: JsonMap) -> list[str]:
    errors: list[str] = []
    status_result = result.get("status", {})
    if isinstance(status_result, dict):
        for key in status_result:
            if str(key) not in bundle.statuses:
                errors.append(f"Unknown result status {key} in {label}")
            if str(key) not in bundle.result_statuses:
                errors.append(f"Result status {key} is not allowed in {label}")
    event_weight = result.get("event_weight", {})
    if isinstance(event_weight, dict):
        for key in event_weight:
            if str(key) not in bundle.weight_targets:
                errors.append(f"Unknown event_weight target {key} in {label}")
    for key in ("add_item", "remove_item"):
        for item_id in _string_list(result.get(key, [])):
            if item_id not in bundle.items:
                errors.append(f"Unknown result item {item_id} in {label}")
    return errors


def _validate_targets(bundle: ProjectData, scenario: Scenario) -> list[str]:
    errors: list[str] = []
    filtered = filter_events_for_scenario(bundle.events, scenario)
    min_events = scenario.validation_targets.get("min_events", 0)
    min_combat = scenario.validation_targets.get("min_combat_events", 0)
    min_curse = scenario.validation_targets.get("min_curse_events", 0)
    if len(filtered) < min_events:
        errors.append(f"Filtered event count {len(filtered)} below validation target: {min_events}")
    combat_count = sum(1 for event in filtered if "combat" in event.event_tags)
    if combat_count < min_combat:
        errors.append(f"Filtered combat event count {combat_count} below validation target: {min_combat}")
    curse_count = sum(1 for event in filtered if "curse" in event.event_tags)
    if curse_count < min_curse:
        errors.append(f"Filtered curse event count {curse_count} below validation target: {min_curse}")
    return errors


def _string_list(value: JsonValue) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return ()
