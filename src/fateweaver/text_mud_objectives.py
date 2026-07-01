from __future__ import annotations

from typing import assert_never

from fateweaver.models import JsonMap, JsonValue
from fateweaver.text_mud_values import json_maps, text


def objective_lines(quest_report: JsonMap) -> list[str]:
    lines = ["목표 평가:"]
    for objective in json_maps(quest_report.get("objective_results")):
        lines.append(
            f"- {text(objective.get('objective_id'))}: {_status(objective.get('status'))} "
            f"({text(objective.get('progress_value'))}/{text(objective.get('target_value'))}) "
            f"reason={text(objective.get('reason'))}"
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
            return text(value)
        case unreachable:
            assert_never(unreachable)
