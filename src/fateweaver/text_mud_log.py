from __future__ import annotations

from pathlib import Path

from fateweaver.models import JsonMap
from fateweaver.text_mud_sections import format_run_header, format_run_summary, format_turn, json_map, json_maps


def save_text_mud_log(log: JsonMap, json_path: Path) -> Path:
    text_path = json_path.with_suffix(".txt")
    text_path.write_text(render_text_mud_log(log), encoding="utf-8")
    return text_path


def render_text_mud_log(log: JsonMap) -> str:
    lines = format_run_header(log)
    for turn in json_maps(log.get("turns")):
        lines.extend(format_turn(turn))
    lines.extend(format_run_summary(json_map(log.get("run_summary")), json_map(log.get("quest_report"))))
    lines.append("[Run 종료]")
    return "\n".join(lines) + "\n"
