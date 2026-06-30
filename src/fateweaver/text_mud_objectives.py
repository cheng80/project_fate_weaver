from __future__ import annotations

from typing import Final, assert_never

from fateweaver.models import JsonMap, JsonValue

MISSING: Final = "-"


def objective_lines(quest_report: JsonMap) -> list[str]:
    lines = ["목표 평가:"]
    for objective in _json_maps(quest_report.get("objective_results")):
        lines.append(
            f"- {_text(objective.get('objective_id'))}: {_status(objective.get('status'))} "
            f"({_text(objective.get('progress_value'))}/{_text(objective.get('target_value'))}) "
            f"reason={_text(objective.get('reason'))}"
        )
    return lines


def _status(value: JsonValue | None) -> str:
    match value:
        case "completed":
            return "성공"
        case "partial":
            return "부분 달성"
        case "failed":
            return "실패"
        case None | bool() | int() | float() | list() | dict() | str():
            return _text(value)
        case unreachable:
            assert_never(unreachable)


def _json_maps(value: JsonValue | None) -> tuple[JsonMap, ...]:
    match value:
        case list():
            return tuple(item for item in value if isinstance(item, dict))
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
