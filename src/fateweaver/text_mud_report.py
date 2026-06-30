from __future__ import annotations

from fateweaver.models import JsonMap
from fateweaver.text_mud_objectives import objective_lines
from fateweaver.text_mud_values import MISSING, text


def format_run_summary(summary: JsonMap, quest_report: JsonMap) -> list[str]:
    lines = [
        "[결과]",
        f"최종 상태: {text(summary.get('final_state'))}",
        f"최종 소지품: {text(summary.get('final_inventory'))}",
        f"실패 여부: {text(summary.get('run_failed'))}",
        f"요약: {text(summary.get('narrative_summary'))}",
        f"다음 실행 의도: {text(summary.get('next_run_intent'))}",
    ]
    if quest_report:
        lines.extend(format_quest_report(quest_report))
    return lines


def format_quest_report(quest_report: JsonMap) -> list[str]:
    lines = [
        "Quest Report:",
        f"결과 유형: {text(quest_report.get('result_type'))}",
        f"실패 종류: {text(quest_report.get('failure_kind'))}",
        f"캐릭터 결과: {text(quest_report.get('character_outcome'))}",
        f"결과 이유: {text(quest_report.get('result_reason'))} / {text(quest_report.get('review_text'))}",
        f"부분 성공 이유: {text(quest_report.get('partial_reasons'))}",
        f"실패 이유: {text(quest_report.get('failure_reasons'))}",
        f"완료 목표: {text(quest_report.get('completed_objectives'))}",
        f"실패 목표: {text(quest_report.get('failed_objectives'))}",
        f"보상 상태: {text(quest_report.get('reward_status'))}",
        f"점수: {text(quest_report.get('score'))}",
    ]
    ending = quest_report.get("ending")
    if isinstance(ending, dict):
        lines.append(f"Run Ending: {text(ending.get('id'))} / {text(ending.get('name'))}")
    score_breakdown = format_score_breakdown(quest_report)
    if score_breakdown != MISSING:
        lines.append(f"점수 상세: {score_breakdown}")
    lines.extend(objective_lines(quest_report))
    return lines


def format_score_breakdown(quest_report: JsonMap) -> str:
    return text(quest_report.get("score_breakdown"))
