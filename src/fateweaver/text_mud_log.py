from __future__ import annotations

from pathlib import Path
from typing import Final, assert_never

from fateweaver.models import JsonMap, JsonValue
from fateweaver.text_mud_objectives import objective_lines


MISSING: Final = "-"


def save_text_mud_log(log: JsonMap, json_path: Path) -> Path:
    text_path = json_path.with_suffix(".txt")
    text_path.write_text(render_text_mud_log(log), encoding="utf-8")
    return text_path


def render_text_mud_log(log: JsonMap) -> str:
    first_turn = _first_turn(log)
    lines = [
        "[Run 시작]",
        f"Run ID: {_text(log.get('run_id'))}",
        f"Seed: {_text(log.get('seed'))}",
        f"Scenario: {_text(log.get('scenario_id'))}",
        f"Profile: {_text(log.get('profile'))}",
        f"현재 상태와 자원: {_text(first_turn.get('state_before'))}",
        f"보유 아이템: {_text(first_turn.get('inventory_before'))}",
        "",
    ]
    for turn in _json_maps(log.get("turns")):
        lines.extend(_render_turn(turn))
    lines.extend(_render_summary(_json_map(log.get("run_summary")), _json_map(log.get("quest_report"))))
    lines.append("[Run 종료]")
    return "\n".join(lines) + "\n"


def _render_turn(turn: JsonMap) -> list[str]:
    turn_heading = _turn_heading(turn)
    selected = _selected_choice(turn)
    result = _json_map(turn.get("result"))
    lines = [
        turn_heading,
        f"Quest: {_text(turn.get('quest_title'))}",
        f"Region: {_region(turn)}",
        f"장소: {_place(turn)}",
        f"현재 상태와 자원: {_text(turn.get('state_before'))}",
        f"보유 아이템: {_text(turn.get('inventory_before'))}",
        f"감지된 단서: {_clues(turn)}",
        f"불길한 징조: {_omens(turn)}",
        f"현재 위험도: {_text(turn.get('expected_risk'))}",
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
            f"결과 메시지: {_text(result.get('message'))}",
            f"상태 변화: {_state_changes(_json_map(turn.get('state_before')), _json_map(turn.get('state_after')))}",
            f"아이템/단서/징조 영향: {_influences(turn)}",
            f"다음 사건 변화: {_event_weight(result)}",
            f"Quest Progress: {_text(turn.get('quest_progress'))}",
            f"Score Change: {_text(turn.get('score_change'))}",
            "",
        ]
    )
    return lines


def _choice_lines(turn: JsonMap) -> list[str]:
    lines: list[str] = []
    for index, choice in enumerate(_json_maps(turn.get("choices_seen")), start=1):
        availability = "가능" if choice.get("available") is True else f"불가({_text(choice.get('unavailable_reason'))})"
        result = _json_map(choice.get("result"))
        lines.append(
            f"{index}. {_text(choice.get('choice_text'))} "
            f"[{availability}] 위험: {_text(choice.get('expected_risk'))} / 보상·비용: {_reward_hint(result)}"
        )
    return lines


def _place(turn: JsonMap) -> str:
    regions = _text(turn.get("region_tags"))
    event_name = _text(turn.get("event_name"))
    return event_name if regions == MISSING else f"{regions} / {event_name}"


def _turn_heading(turn: JsonMap) -> str:
    clock = _json_map(turn.get("run_clock"))
    if not clock:
        return f"[Turn {_text(turn.get('turn'))}]"
    return (
        f"[Day {_text(clock.get('day'))} / "
        f"{_text(clock.get('time_of_day')).title()} / "
        f"Turn {_text(clock.get('turn'))}]"
    )


def _region(turn: JsonMap) -> str:
    values = _json_values(turn.get("region_tags"))
    return MISSING if not values else _text(values[0])


def _event_line(turn: JsonMap) -> str:
    name = _text(turn.get("event_name"))
    description = _text(turn.get("event_description"))
    return name if description == MISSING else f"{name} - {description}"


def _selected_choice(turn: JsonMap) -> JsonMap:
    selected_id = _text(turn.get("selected_choice_id"))
    for choice in _json_maps(turn.get("choices_seen")):
        if _text(choice.get("choice_id")) == selected_id:
            return choice
    return {}


def _choice_result_line(selected: JsonMap, result: JsonMap) -> str:
    return f"{_text(selected.get('choice_text'))} -> {_reward_hint(result)}"


def _risk_reward_judgment(turn: JsonMap) -> str:
    return (
        f"위험={_text(turn.get('expected_risk'))}; "
        f"후회도={_text(turn.get('regret_score'))}; "
        f"선택 근거={_text(turn.get('selected_choice_reason'))}"
    )


def _reward_hint(result: JsonMap) -> str:
    parts = [
        _status_delta(result),
        _items_delta(result),
        _event_weight(result),
    ]
    visible = [part for part in parts if part != MISSING]
    return "; ".join(visible) if visible else _text(result.get("message"))


def _status_delta(result: JsonMap) -> str:
    status = _json_map(result.get("status"))
    if not status:
        return MISSING
    return f"상태 {_text(status)}"


def _items_delta(result: JsonMap) -> str:
    changes = []
    added = _text(result.get("add_item"))
    removed = _text(result.get("remove_item"))
    if added != MISSING:
        changes.append(f"아이템 획득 {added}")
    if removed != MISSING:
        changes.append(f"아이템 소모 {removed}")
    return ", ".join(changes) if changes else MISSING


def _event_weight(result: JsonMap) -> str:
    weight = _text(result.get("event_weight"))
    tags = _text(result.get("next_event_tags"))
    if weight == MISSING and tags == MISSING:
        return "변화 없음"
    if weight == MISSING:
        return f"다음 사건 태그 {tags}"
    if tags == MISSING:
        return f"후속 사건 가중치 {weight}"
    return f"후속 사건 가중치 {weight}; 다음 사건 태그 {tags}"


def _clues(turn: JsonMap) -> str:
    values = [_text(turn.get("event_tags")), _text(_json_map(turn.get("result")).get("message"))]
    clues = [value for value in values if value != MISSING]
    return " / ".join(clues) if clues else MISSING


def _omens(turn: JsonMap) -> str:
    danger = _text(turn.get("danger_tags"))
    return "뚜렷한 징조 없음" if danger == MISSING else danger


def _first_turn(log: JsonMap) -> JsonMap:
    turns = _json_maps(log.get("turns"))
    return turns[0] if turns else {}


def _render_summary(summary: JsonMap, quest_report: JsonMap) -> list[str]:
    lines = [
        "[결과]",
        f"최종 상태: {_text(summary.get('final_state'))}",
        f"최종 소지품: {_text(summary.get('final_inventory'))}",
        f"실패 여부: {_text(summary.get('run_failed'))}",
        f"요약: {_text(summary.get('narrative_summary'))}",
        f"다음 실행 의도: {_text(summary.get('next_run_intent'))}",
    ]
    if quest_report:
        lines.extend(
            [
                "Quest Report:",
                f"결과 유형: {_text(quest_report.get('result_type'))}",
                f"실패 종류: {_text(quest_report.get('failure_kind'))}",
                f"캐릭터 결과: {_text(quest_report.get('character_outcome'))}",
                f"결과 이유: {_text(quest_report.get('result_reason'))} / {_text(quest_report.get('review_text'))}",
                f"부분 성공 이유: {_text(quest_report.get('partial_reasons'))}",
                f"실패 이유: {_text(quest_report.get('failure_reasons'))}",
                f"완료 목표: {_text(quest_report.get('completed_objectives'))}",
                f"실패 목표: {_text(quest_report.get('failed_objectives'))}",
                f"보상 상태: {_text(quest_report.get('reward_status'))}",
                f"점수: {_text(quest_report.get('score'))}",
            ]
        )
        lines.extend(objective_lines(quest_report))
    return lines


def _influences(turn: JsonMap) -> str:
    direct = _text(turn.get("influenced_by"))
    inventory_change = _inventory_changes(_json_values(turn.get("inventory_before")), _json_values(turn.get("inventory_after")))
    if inventory_change == MISSING:
        return direct
    if direct == MISSING:
        return inventory_change
    return f"{direct}; {inventory_change}"


def _selected_cards(turn: JsonMap) -> str:
    selected = _text(turn.get("choice_reason"))
    multi = _json_map(turn.get("multi_select"))
    return f"{selected} (Multi-Select: {_text(multi.get('rule_id'))})" if multi.get("selected") is True else selected


def _inventory_changes(before: tuple[JsonValue, ...], after: tuple[JsonValue, ...]) -> str:
    before_values = set(_text(value) for value in before)
    after_values = set(_text(value) for value in after)
    gained = sorted(after_values - before_values)
    lost = sorted(before_values - after_values)
    changes = [*(f"획득:{item}" for item in gained), *(f"상실:{item}" for item in lost)]
    return ", ".join(changes) if changes else MISSING


def _state_changes(before: JsonMap, after: JsonMap) -> str:
    keys = sorted(before.keys() | after.keys())
    changes = [f"{key}: {_text(before.get(key))} -> {_text(after.get(key))}" for key in keys if before.get(key) != after.get(key)]
    return ", ".join(changes) if changes else "변화 없음"


def _json_maps(value: JsonValue | None) -> tuple[JsonMap, ...]:
    match value:
        case list():
            maps: list[JsonMap] = []
            for item in value:
                match item:
                    case dict():
                        maps.append(item)
                    case None | bool() | str() | int() | float() | list():
                        continue
                    case unreachable:
                        assert_never(unreachable)
            return tuple(maps)
        case None | bool() | str() | int() | float() | dict():
            return ()
        case unreachable:
            assert_never(unreachable)


def _json_map(value: JsonValue | None) -> JsonMap:
    match value:
        case dict():
            return value
        case None | bool() | str() | int() | float() | list():
            return {}
        case unreachable:
            assert_never(unreachable)


def _json_values(value: JsonValue | None) -> tuple[JsonValue, ...]:
    match value:
        case list():
            return tuple(value)
        case None | bool() | str() | int() | float() | dict():
            return ()
        case unreachable:
            assert_never(unreachable)


def _text(value: JsonValue | None) -> str:
    match value:
        case None:
            return MISSING
        case bool():
            return str(value).lower()
        case str():
            return value
        case int() | float():
            return str(value)
        case list():
            return ", ".join(_text(item) for item in value) or MISSING
        case dict():
            return ", ".join(f"{key}={_text(nested)}" for key, nested in sorted(value.items())) or MISSING
        case unreachable:
            assert_never(unreachable)
