from __future__ import annotations

from fateweaver.models import JsonMap, JsonValue, StateSnapshot, StatusDefinition, StatusMap


def apply_choice_result(
    state: StatusMap,
    inventory: tuple[str, ...],
    run_tags: tuple[str, ...],
    result: JsonMap,
    statuses: dict[str, StatusDefinition],
) -> StateSnapshot:
    next_status = dict(state)
    raw_status = result.get("status", {})
    for key, delta in _as_mapping(raw_status).items():
        definition = statuses[key]
        value = next_status.get(key, definition.initial) + int(delta)
        next_status[key] = min(definition.maximum, max(definition.minimum, value))
    next_inventory = _remove_values(inventory, _string_list(result.get("remove_item", [])))
    next_inventory = _append_unique(next_inventory, _string_list(result.get("add_item", [])))
    next_run_tags = _remove_values(run_tags, _string_list(result.get("remove_run_tag", [])))
    next_run_tags = _append_unique(next_run_tags, _string_list(result.get("add_run_tag", [])))
    return StateSnapshot(status=next_status, inventory=next_inventory, run_tags=next_run_tags)


def is_failed(state: StatusMap, statuses: dict[str, StatusDefinition]) -> bool:
    for key, definition in statuses.items():
        fail_when = definition.fail_when
        if fail_when is None:
            continue
        value = state.get(key, definition.initial)
        if fail_when == definition.minimum and value <= fail_when:
            return True
        if fail_when == definition.maximum and value >= fail_when:
            return True
        if value == fail_when:
            return True
    return False


def _remove_values(values: tuple[str, ...], removals: tuple[str, ...]) -> tuple[str, ...]:
    removal_set = set(removals)
    return tuple(value for value in values if value not in removal_set)


def _append_unique(values: tuple[str, ...], additions: tuple[str, ...]) -> tuple[str, ...]:
    result = list(values)
    for value in additions:
        if value not in result:
            result.append(value)
    return tuple(result)


def _string_list(value: JsonValue) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return ()


def _as_mapping(value: JsonValue) -> JsonMap:
    if isinstance(value, dict):
        return {str(key): item for key, item in value.items()}
    return {}
