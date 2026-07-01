from __future__ import annotations

import unittest

from fateweaver.models import JsonMap
from fateweaver.text_mud_log import render_text_mud_log


class TextMudLogTests(unittest.TestCase):
    def test_format_quest_report_when_failure_taxonomy_present_then_renders_existing_lines(self) -> None:
        # Given
        from fateweaver.text_mud_report import format_quest_report

        quest_report: JsonMap = {
            "result_type": "failure",
            "failure_kind": "objective_failed",
            "character_outcome": "alive",
            "result_reason": "primary_objective_failed",
            "review_text": "짐을 되찾지 못했지만 상인은 살아 돌아왔다.",
            "partial_reasons": [],
            "failure_reasons": ["primary_objective_failed"],
            "completed_objectives": [],
            "failed_objectives": ["recover_lost_pack"],
            "reward_status": "no_reward",
            "score": -60,
            "objective_results": [
                {
                    "objective_id": "recover_lost_pack",
                    "status": "failed",
                    "reason": "primary_objective_failed",
                    "score_delta": -30,
                }
            ],
            "score_breakdown": {"objective_completion": -30, "outcome_adjustment": -30},
        }

        # When
        lines = format_quest_report(quest_report)

        # Then
        self.assertEqual("Quest Report:", lines[0])
        self.assertIn("결과 유형: failure", lines)
        self.assertIn("실패 종류: objective_failed", lines)
        self.assertIn("캐릭터 결과: alive", lines)
        self.assertIn("목표 평가:", lines)
        self.assertIn("- recover_lost_pack: 실패 (-/-) reason=primary_objective_failed", lines)
        self.assertIn("점수 상세: objective_completion=-30, outcome_adjustment=-30", lines)

    def test_render_text_mud_log_when_curse_changes_then_frames_it_as_status_detail(self) -> None:
        # Given
        log: JsonMap = {
            "run_id": "mvp0-console-0001",
            "scenario_id": "mvp0_console_test",
            "seed": 42,
            "profile": "balanced",
            "turns": [
                {
                    "turn": 1,
                    "event_id": "old_well",
                    "event_name": "오래된 우물",
                    "event_description": "숲 가장자리의 우물에서 낮은 울림이 난다.",
                    "region_tags": ["forest"],
                    "event_tags": ["exploration", "omen"],
                    "danger_tags": ["darkness"],
                    "state_before": {"health": 3, "curse": 1},
                    "inventory_before": ["rusty_key"],
                    "choices_seen": [
                        {
                            "choice_id": "listen",
                            "choice_text": "우물 아래 소리를 듣는다",
                            "available": True,
                            "expected_risk": "medium",
                            "result": {
                                "status": {"curse": 1},
                                "event_weight": {"lost": -1},
                                "message": "물소리가 다음 갈림길의 방향을 알려주었다.",
                            },
                        }
                    ],
                    "selected_choice_id": "listen",
                    "selected_choice_type": "cautious",
                    "selected_choice_reason": "profile=balanced: top_factors=novelty",
                    "expected_risk": "medium",
                    "regret_score": 3,
                    "influenced_by": ["item:rusty_key", "status:curse"],
                    "result": {
                        "status": {"curse": 1},
                        "event_weight": {"lost": -1},
                        "message": "물소리가 다음 갈림길의 방향을 알려주었다.",
                    },
                    "state_after": {"health": 3, "curse": 2},
                    "inventory_after": ["rusty_key", "silver_thread"],
                },
            ],
            "run_summary": {
                "final_state": {"health": 3, "curse": 2},
                "final_inventory": ["rusty_key", "silver_thread"],
                "run_failed": False,
                "narrative_summary": "auto console validation run",
                "next_run_intent": "auto validation complete",
            },
        }

        # When
        text_log = render_text_mud_log(log)

        # Then
        self.assertIn("[Run 시작]", text_log)
        self.assertIn("장소: forest / 오래된 우물", text_log)
        self.assertIn("발생 사건: 오래된 우물 - 숲 가장자리의 우물에서 낮은 울림이 난다.", text_log)
        self.assertIn("1. 우물 아래 소리를 듣는다 [가능] 위험: medium", text_log)
        self.assertIn("선택 결과: 우물 아래 소리를 듣는다", text_log)
        self.assertIn("위험/보상 판단: 위험=medium; 후회도=3", text_log)
        self.assertIn("상태 변화: curse: 1 -> 2", text_log)
        self.assertIn("아이템/단서/징조 영향: item:rusty_key, status:curse", text_log)
        self.assertIn("다음 사건 변화: 후속 사건 가중치 lost=-1", text_log)
        self.assertIn("[Run 종료]", text_log)
        header = "\n".join(text_log.splitlines()[:5])
        self.assertNotIn("curse", header)

    def test_render_text_mud_log_when_polished_then_frames_choice_and_ending_as_story(self) -> None:
        # Given
        log: JsonMap = {
            "run_id": "standard-run-polish",
            "scenario_id": "standard_run_25_35_turn",
            "seed": 202,
            "profile": "balanced",
            "turns": [
                {
                    "turn": 21,
                    "quest_title": "폭풍 산길 생존 귀환",
                    "run_clock": {"day": 6, "time_of_day": "morning", "turn": 21},
                    "event_name": "두 번째 목격자의 엇갈린 증언",
                    "event_description": "상인의 말과 다른 발자국 이야기가 나온다.",
                    "region_tags": ["village"],
                    "event_tags": ["clue"],
                    "danger_tags": ["storm"],
                    "state_before": {"food": 3, "health": 8, "money": 17, "reputation": 5},
                    "inventory_before": ["torch"],
                    "choices_seen": [
                        {
                            "choice_id": "ration_the_last_supplies",
                            "choice_text": "남은 보급을 배분한다",
                            "choice_type": "resource_alternative",
                            "slot_role": "resource_alternative",
                            "available": True,
                            "expected_risk": "low",
                            "result": {
                                "status": {"food": 1},
                                "message": "남은 식량을 더 오래 버티도록 나눴다.",
                            },
                        },
                    ],
                    "selected_choice_id": "ration_the_last_supplies",
                    "selected_choice_type": "resource_alternative",
                    "selected_choice_reason": "balanced: resource caution",
                    "choice_reason": "남은 보급을 배분한다",
                    "expected_risk": "low",
                    "regret_score": 1,
                    "influenced_by": ["slot:resource_alternative"],
                    "result": {
                        "status": {"food": 1},
                        "gain_clues": ["old_route_receipt"],
                        "gain_omens": ["storm_break"],
                        "next_event_tags": ["storm_pass", "ration"],
                        "message": "남은 식량을 더 오래 버티도록 나눴다.",
                    },
                    "state_after": {"food": 4, "health": 8, "money": 17, "reputation": 5},
                    "inventory_after": ["torch"],
                    "quest_progress": {"storm_shelter_found": 1},
                    "score_change": {"resource_management": 4},
                }
            ],
            "run_summary": {
                "final_state": {"food": 4, "health": 8, "money": 17, "reputation": 5},
                "final_inventory": ["torch"],
                "run_failed": False,
                "narrative_summary": "route prepared",
                "next_run_intent": "complete",
            },
            "quest_report": {
                "result_type": "success",
                "failure_kind": "none",
                "character_outcome": "alive",
                "result_reason": "all_required_objectives_complete",
                "review_text": "피난처와 보급을 확인해 산길을 넘을 준비를 마쳤다.",
                "partial_reasons": [],
                "failure_reasons": [],
                "completed_objectives": ["storm_shelter_found"],
                "failed_objectives": [],
                "reward_status": "full_reward",
                "score": 576,
                "score_breakdown": {"resource_management": 4},
                "resource_summary": {"food": 4, "health": 8},
                "ending": {"id": "prepared_frontier_route", "name": "준비된 변경의 길"},
            },
        }

        # When
        text_log = render_text_mud_log(log)

        # Then
        self.assertIn("장면:", text_log)
        self.assertIn("선택의 의미: 보급과 휴식을 관리해 다음 구간을 버틴다.", text_log)
        self.assertIn("결과 해석: 남은 식량을 더 오래 버티도록 나눴다.", text_log)
        self.assertIn("food: 3 -> 4 (+1) - 식량이 조금 늘어 다음 이동의 여유가 생긴다.", text_log)
        self.assertIn("단서: old_route_receipt - 다음 판단에 연결할 실마리가 생긴다.", text_log)
        self.assertIn("징조: storm_break - 위험이 모습을 드러낸다.", text_log)
        self.assertIn("Run 결말: prepared_frontier_route / 준비된 변경의 길", text_log)
        self.assertIn("Ending 해석: 준비와 단서가 이어져 변경을 넘을 길이 열린다.", text_log)


if __name__ == "__main__":
    unittest.main()
