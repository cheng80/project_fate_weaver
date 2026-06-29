from __future__ import annotations

from fateweaver.choice_scoring import ChoiceSelection, select_weighted_choice
from fateweaver.models import Choice, ChoiceSeen, Event, JsonMap, JsonValue, StatusMap, StatusRequirement


def build_choices_seen(
    event: Event,
    state: StatusMap,
    inventory: tuple[str, ...],
    run_tags: tuple[str, ...],
) -> tuple[ChoiceSeen, ...]:
    seen: list[ChoiceSeen] = []
    for choice in event.choices:
        available, reason = _availability(choice.requires_item, choice.requires_status, choice.requires_run_tag, state, inventory, run_tags)
        if choice.hidden and not available and not choice.visible_when_unavailable:
            continue
        result = resolve_choice_result(choice, state)
        seen.append(
            ChoiceSeen(
                choice_id=choice.id,
                choice_type=choice.choice_type,
                available=available,
                unavailable_reason=reason,
                hidden=choice.hidden,
                expected_risk=choice.risk_level or "medium",
                influenced_by=_choice_influences(choice),
                result=result,
            )
        )
    return tuple(seen)


def select_available_choice(
    choices_seen: tuple[ChoiceSeen, ...],
    policy: str = "auto",
    profile: str = "balanced",
    state: StatusMap | None = None,
    seed: int = 0,
    turn: int = 0,
    selected_choice_history: tuple[str, ...] = (),
) -> ChoiceSeen:
    return select_choice(choices_seen, policy, profile, state, seed, turn, selected_choice_history).choice


def select_choice(
    choices_seen: tuple[ChoiceSeen, ...],
    policy: str = "auto",
    profile: str = "balanced",
    state: StatusMap | None = None,
    seed: int = 0,
    turn: int = 0,
    selected_choice_history: tuple[str, ...] = (),
) -> ChoiceSelection:
    return select_weighted_choice(choices_seen, policy, profile, state, seed, turn, selected_choice_history)


def selected_choice_from_seen(choices_seen: tuple[ChoiceSeen, ...], choice_id: str) -> ChoiceSeen:
    for choice in choices_seen:
        if choice.choice_id == choice_id:
            if not choice.available:
                raise ValueError(f"Choice is unavailable: {choice_id}")
            return choice
    raise ValueError(f"Unknown choice: {choice_id}")


def resolve_choice_result(choice: Choice, state: StatusMap) -> JsonMap:
    for entry in choice.result_pool:
        if _condition_matches(entry.when, state):
            return dict(entry.result)
    return dict(choice.result)


def requirements_met(
    requires_item: str | None,
    requires_status: dict[str, StatusRequirement],
    requires_run_tag: str | None,
    state: StatusMap,
    inventory: tuple[str, ...],
    run_tags: tuple[str, ...],
) -> bool:
    available, _ = _availability(requires_item, requires_status, requires_run_tag, state, inventory, run_tags)
    return available


def _availability(
    requires_item: str | None,
    requires_status: dict[str, StatusRequirement],
    requires_run_tag: str | None,
    state: StatusMap,
    inventory: tuple[str, ...],
    run_tags: tuple[str, ...],
) -> tuple[bool, str | None]:
    if requires_item is not None and requires_item not in inventory:
        return False, f"requires item: {requires_item}"
    for key, requirement in requires_status.items():
        value = state.get(key, 0)
        if requirement.minimum is not None and value < requirement.minimum:
            return False, f"requires {key} >= {requirement.minimum}"
        if requirement.maximum is not None and value > requirement.maximum:
            return False, f"requires {key} <= {requirement.maximum}"
    if requires_run_tag is not None and requires_run_tag not in run_tags:
        return False, f"requires run tag: {requires_run_tag}"
    return True, None


def _choice_influences(choice: Choice) -> tuple[str, ...]:
    influenced_by: list[str] = []
    if choice.requires_item is not None:
        influenced_by.append(f"item:{choice.requires_item}")
    for key in choice.requires_status:
        influenced_by.append(f"status:{key}")
    if choice.requires_run_tag is not None:
        influenced_by.append(f"run_tag:{choice.requires_run_tag}")
    return tuple(influenced_by)


def _condition_matches(condition: JsonMap, state: StatusMap) -> bool:
    default = condition.get("default")
    if default is True:
        return True
    for key, raw_bounds in condition.items():
        if key == "default":
            continue
        bounds = _as_mapping(raw_bounds)
        value = state.get(key, 0)
        minimum = bounds.get("min")
        maximum = bounds.get("max")
        if minimum is not None and value < int(minimum):
            return False
        if maximum is not None and value > int(maximum):
            return False
    return True


def _as_mapping(value: JsonValue) -> JsonMap:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items()}
