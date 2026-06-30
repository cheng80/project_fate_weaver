from __future__ import annotations

import unittest

from fateweaver.models import JsonMap
from fateweaver.text_mud_log import render_text_mud_log


class TextMudLogTests(unittest.TestCase):
    def test_format_quest_report_when_failure_taxonomy_present_then_renders_existing_lines(self) -> None:
        # Given
        from fateweaver.text_mud_sections import format_quest_report

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


if __name__ == "__main__":
    unittest.main()
