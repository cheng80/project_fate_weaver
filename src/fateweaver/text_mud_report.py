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
    narrative = _quest_report_narrative(quest_report)
    if narrative != MISSING:
        lines.append(f"Report 해석: {narrative}")
    ending = quest_report.get("ending")
    if isinstance(ending, dict):
        lines.append(f"Run Ending: {text(ending.get('id'))} / {text(ending.get('name'))}")
        lines.append(f"Run 결말: {text(ending.get('id'))} / {text(ending.get('name'))}")
        lines.append(f"Ending 해석: {_ending_narrative(ending)}")
    score_breakdown = format_score_breakdown(quest_report)
    if score_breakdown != MISSING:
        lines.append(f"점수 상세: {score_breakdown}")
    lines.extend(objective_lines(quest_report))
    return lines


def format_score_breakdown(quest_report: JsonMap) -> str:
    return text(quest_report.get("score_breakdown"))


def _quest_report_narrative(quest_report: JsonMap) -> str:
    review = text(quest_report.get("review_text"))
    if review != MISSING:
        return review
    result_type = text(quest_report.get("result_type"))
    if result_type == "success":
        return "목표를 완수했고 다음 여정을 이어갈 여지를 남겼다."
    if result_type == "partial_success":
        return "핵심 일부는 지켰지만 남은 대가가 다음 선택을 압박한다."
    if result_type == "failure":
        return "원정은 실패했지만 기록은 다음 시도의 단서로 남는다."
    return MISSING


def _ending_narrative(ending: JsonMap) -> str:
    ending_id = text(ending.get("id"))
    if ending_id == "prepared_frontier_route":
        return "준비와 단서가 이어져 변경을 넘을 길이 열린다."
    if ending_id == "survival_return":
        return "무사히 돌아왔지만 길 위의 불확실성은 아직 남아 있다."
    if ending_id == "failed_expedition":
        return "길은 닫혔고 다음 원정은 더 단단한 준비를 요구한다."
    return "이번 여정의 선택들이 마지막 장면으로 모인다."
