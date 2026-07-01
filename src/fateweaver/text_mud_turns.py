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
        f"장면: {_scene_line(turn)}",
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
            f"선택의 의미: {_choice_intent(selected, turn)}",
            f"선택 결과: {_choice_result_line(selected, result)}",
            f"위험/보상 판단: {_risk_reward_judgment(turn)}",
            f"결과 메시지: {text(result.get('message'))}",
            f"결과 해석: {_result_narrative(result)}",
            f"상태 변화: {_state_changes(json_map(turn.get('state_before')), json_map(turn.get('state_after')))}",
            f"변화 의미: {_state_change_narrative(json_map(turn.get('state_before')), json_map(turn.get('state_after')))}",
            f"아이템/단서/징조 영향: {_influences(turn)}",
            f"단서/징조 해석: {_clue_omen_narrative(result)}",
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


def _scene_line(turn: JsonMap) -> str:
    event_name = text(turn.get("event_name"))
    description = text(turn.get("event_description"))
    risk = text(turn.get("expected_risk"))
    if description != MISSING:
        return f"{description} 위험도는 {risk}로 읽힌다."
    if event_name != MISSING:
        return f"{event_name} 앞에서 다음 선택을 고른다."
    return "원정대는 다음 선택지를 살핀다."


def _selected_choice(turn: JsonMap) -> JsonMap:
    selected_id = text(turn.get("selected_choice_id"))
    for choice in json_maps(turn.get("choices_seen")):
        if text(choice.get("choice_id")) == selected_id:
            return choice
    return {}


def _choice_result_line(selected: JsonMap, result: JsonMap) -> str:
    return f"{text(selected.get('choice_text'))} -> {_reward_hint(result)}"


def _choice_intent(selected: JsonMap, turn: JsonMap) -> str:
    role = text(selected.get("slot_role"))
    if role == MISSING:
        role = text(selected.get("choice_type"))
    if role == MISSING:
        role = text(turn.get("selected_choice_type"))
    meanings = {
        "quest_progress": "목표에 직접 다가가는 선택이다.",
        "risk_discovery": "위험을 감수하고 더 많은 정보를 얻는다.",
        "resource_alternative": "보급과 휴식을 관리해 다음 구간을 버틴다.",
        "clue_followup": "이미 얻은 단서를 다음 판단으로 잇는다.",
        "omen_escalation": "불길한 징조를 확인하고 대비한다.",
        "return": "확인한 내용을 들고 돌아갈 때를 고른다.",
        "aftermath": "남은 일을 정리하고 결과를 굳힌다.",
        "resolve_objective": "마지막 목표를 매듭짓는 선택이다.",
    }
    return meanings.get(role, "현재 상황에서 가장 그럴듯한 길을 고른다.")


def _result_narrative(result: JsonMap) -> str:
    message = text(result.get("message"))
    if message != MISSING:
        return message
    hint = _reward_hint(result)
    if hint != MISSING:
        return f"선택의 대가와 보상이 바로 드러난다: {hint}"
    return "상황은 크게 흔들리지 않았지만 선택의 흔적은 남는다."


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
    changes = [_state_change_line(key, before.get(key), after.get(key)) for key in keys if before.get(key) != after.get(key)]
    return ", ".join(changes) if changes else "변화 없음"


def _state_change_line(key: str, before: JsonValue | None, after: JsonValue | None) -> str:
    delta = _numeric_delta(before, after)
    if delta is None:
        return f"{key}: {text(before)} -> {text(after)}"
    sign = f"+{delta}" if delta > 0 else str(delta)
    narrative = _resource_delta_narrative(key, delta)
    return f"{key}: {text(before)} -> {text(after)} ({sign}) - {narrative}"


def _numeric_delta(before: JsonValue | None, after: JsonValue | None) -> int | None:
    if isinstance(before, int) and isinstance(after, int):
        return after - before
    return None


def _resource_delta_narrative(key: str, delta: int) -> str:
    if key == "food":
        return "식량이 조금 늘어 다음 이동의 여유가 생긴다." if delta > 0 else "식량이 줄어 다음 휴식의 압박이 커진다."
    if key == "health":
        return "몸 상태가 나아져 위험을 버틸 힘이 생긴다." if delta > 0 else "피로와 상처가 다음 선택을 무겁게 만든다."
    if key == "money":
        return "쓸 수 있는 돈이 늘어 선택지가 넓어진다." if delta > 0 else "돈을 써서 당장의 실마리를 확보한다."
    if key == "reputation":
        return "평판이 올라 다음 부탁이 쉬워진다." if delta > 0 else "평판이 흔들려 다음 만남이 까다로워진다."
    if key == "curse":
        return "불안한 상태가 짙어진다." if delta > 0 else "불안한 상태가 조금 가라앉는다."
    return "상태가 바뀌어 다음 장면의 조건이 달라진다."


def _state_change_narrative(before: JsonMap, after: JsonMap) -> str:
    keys = [key for key in sorted(before.keys() | after.keys()) if before.get(key) != after.get(key)]
    if not keys:
        return "자원은 그대로지만 선택의 정보가 다음 장면에 남는다."
    return "; ".join(_resource_delta_narrative(key, _numeric_delta(before.get(key), after.get(key)) or 0) for key in keys)


def _clue_omen_narrative(result: JsonMap) -> str:
    parts = []
    parts.extend(f"단서: {text(clue)} - 다음 판단에 연결할 실마리가 생긴다." for clue in json_values(result.get("gain_clues")))
    parts.extend(f"징조: {text(omen)} - 위험이 모습을 드러낸다." for omen in json_values(result.get("gain_omens")))
    return " / ".join(parts) if parts else "새 단서나 징조는 뚜렷하게 늘지 않았다."
