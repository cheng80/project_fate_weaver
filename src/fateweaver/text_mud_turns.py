from __future__ import annotations

from fateweaver.models import JsonMap, JsonValue
from fateweaver.text_mud_values import MISSING, json_map, json_maps, json_values, text


def format_run_header(log: JsonMap) -> list[str]:
    first_turn = _first_turn(log)
    return [
        "[Run 시작]",
        f"Run ID: {text(log.get('run_id'))}",
        f"Seed: {text(log.get('seed'))}",
        f"Scenario: {text(log.get('scenario_id'))}",
        f"Profile: {text(log.get('profile'))}",
        f"현재 상태와 자원: {text(first_turn.get('state_before'))}",
        f"보유 아이템: {text(first_turn.get('inventory_before'))}",
        "",
    ]


def format_turn(turn: JsonMap) -> list[str]:
    selected = _selected_choice(turn)
    result = json_map(turn.get("result"))
    lines = [
        _turn_heading(turn),
        f"Quest: {text(turn.get('quest_title'))}",
        f"Region: {_region(turn)}",
        f"장소: {_place(turn)}",
        f"현재 상태와 자원: {text(turn.get('state_before'))}",
        f"보유 아이템: {text(turn.get('inventory_before'))}",
        f"감지된 단서: {_clues(turn)}",
        f"불길한 징조: {_omens(turn)}",
        f"현재 위험도: {text(turn.get('expected_risk'))}",
        f"발생 사건: {_event_line(turn)}",
        "카드:",
    ]
    lines.extend(_choice_lines(turn))
    lines.extend(
        [
            "선택:",
            f"- {_selected_cards(turn)}",
            f"선택 결과: {_choice_result_line(selected, result)}",
            f"위험/보상 판단: {_risk_reward_judgment(turn)}",
            f"결과 메시지: {text(result.get('message'))}",
            f"상태 변화: {_state_changes(json_map(turn.get('state_before')), json_map(turn.get('state_after')))}",
            f"아이템/단서/징조 영향: {_influences(turn)}",
            f"다음 사건 변화: {_event_weight(result)}",
            f"Quest Progress: {text(turn.get('quest_progress'))}",
            f"Score Change: {text(turn.get('score_change'))}",
            "",
        ]
    )
    return lines


def _choice_lines(turn: JsonMap) -> list[str]:
    lines: list[str] = []
    for index, choice in enumerate(json_maps(turn.get("choices_seen")), start=1):
        availability = "가능" if choice.get("available") is True else f"불가({text(choice.get('unavailable_reason'))})"
        result = json_map(choice.get("result"))
        lines.append(
            f"{index}. {text(choice.get('choice_text'))} "
            f"[{availability}] 위험: {text(choice.get('expected_risk'))} / 보상·비용: {_reward_hint(result)}"
        )
    return lines


def _place(turn: JsonMap) -> str:
    regions = text(turn.get("region_tags"))
    event_name = text(turn.get("event_name"))
    return event_name if regions == MISSING else f"{regions} / {event_name}"


def _turn_heading(turn: JsonMap) -> str:
    clock = json_map(turn.get("run_clock"))
    if not clock:
        return f"[Turn {text(turn.get('turn'))}]"
    return f"[Day {text(clock.get('day'))} / {text(clock.get('time_of_day')).title()} / Turn {text(clock.get('turn'))}]"


def _region(turn: JsonMap) -> str:
    values = json_values(turn.get("region_tags"))
    return MISSING if not values else text(values[0])


def _event_line(turn: JsonMap) -> str:
    name = text(turn.get("event_name"))
    description = text(turn.get("event_description"))
    return name if description == MISSING else f"{name} - {description}"


def _selected_choice(turn: JsonMap) -> JsonMap:
    selected_id = text(turn.get("selected_choice_id"))
    for choice in json_maps(turn.get("choices_seen")):
        if text(choice.get("choice_id")) == selected_id:
            return choice
    return {}


def _choice_result_line(selected: JsonMap, result: JsonMap) -> str:
    return f"{text(selected.get('choice_text'))} -> {_reward_hint(result)}"


def _risk_reward_judgment(turn: JsonMap) -> str:
    return (
        f"위험={text(turn.get('expected_risk'))}; "
        f"후회도={text(turn.get('regret_score'))}; "
        f"선택 근거={text(turn.get('selected_choice_reason'))}"
    )


def _reward_hint(result: JsonMap) -> str:
    parts = [_status_delta(result), _items_delta(result), _event_weight(result)]
    visible = [part for part in parts if part != MISSING]
    return "; ".join(visible) if visible else text(result.get("message"))


def _status_delta(result: JsonMap) -> str:
    status = json_map(result.get("status"))
    if not status:
        return MISSING
    return f"상태 {text(status)}"


def _items_delta(result: JsonMap) -> str:
    changes = []
    added = text(result.get("add_item"))
    removed = text(result.get("remove_item"))
    if added != MISSING:
        changes.append(f"아이템 획득 {added}")
    if removed != MISSING:
        changes.append(f"아이템 소모 {removed}")
    return ", ".join(changes) if changes else MISSING


def _event_weight(result: JsonMap) -> str:
    weight = text(result.get("event_weight"))
    tags = text(result.get("next_event_tags"))
    if weight == MISSING and tags == MISSING:
        return "변화 없음"
    if weight == MISSING:
        return f"다음 사건 태그 {tags}"
    if tags == MISSING:
        return f"후속 사건 가중치 {weight}"
    return f"후속 사건 가중치 {weight}; 다음 사건 태그 {tags}"


def _clues(turn: JsonMap) -> str:
    values = [text(turn.get("event_tags")), text(json_map(turn.get("result")).get("message"))]
    clues = [value for value in values if value != MISSING]
    return " / ".join(clues) if clues else MISSING


def _omens(turn: JsonMap) -> str:
    danger = text(turn.get("danger_tags"))
    return "뚜렷한 징조 없음" if danger == MISSING else danger


def _first_turn(log: JsonMap) -> JsonMap:
    turns = json_maps(log.get("turns"))
    return turns[0] if turns else {}


def _influences(turn: JsonMap) -> str:
    direct = text(turn.get("influenced_by"))
    inventory_change = _inventory_changes(json_values(turn.get("inventory_before")), json_values(turn.get("inventory_after")))
    if inventory_change == MISSING:
        return direct
    if direct == MISSING:
        return inventory_change
    return f"{direct}; {inventory_change}"


def _selected_cards(turn: JsonMap) -> str:
    selected = text(turn.get("choice_reason"))
    multi = json_map(turn.get("multi_select"))
    return f"{selected} (Multi-Select: {text(multi.get('rule_id'))})" if multi.get("selected") is True else selected


def _inventory_changes(before: tuple[JsonValue, ...], after: tuple[JsonValue, ...]) -> str:
    before_values = set(text(value) for value in before)
    after_values = set(text(value) for value in after)
    gained = sorted(after_values - before_values)
    lost = sorted(before_values - after_values)
    changes = [*(f"획득:{item}" for item in gained), *(f"상실:{item}" for item in lost)]
    return ", ".join(changes) if changes else MISSING


def _state_changes(before: JsonMap, after: JsonMap) -> str:
    keys = sorted(before.keys() | after.keys())
    changes = [f"{key}: {text(before.get(key))} -> {text(after.get(key))}" for key in keys if before.get(key) != after.get(key)]
    return ", ".join(changes) if changes else "변화 없음"
