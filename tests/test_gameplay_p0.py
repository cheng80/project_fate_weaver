from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GameplayP0Tests(unittest.TestCase):
    def test_tutorial_herb_quest_cli_outputs_p0_run_contract(self) -> None:
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            # When
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "balanced",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            json_logs = list(Path(tmp).glob("run_*.json"))
            text_logs = list(Path(tmp).glob("run_*.txt"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
            text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(json_logs), result.stdout + result.stderr)
        self.assertEqual(1, len(text_logs), result.stdout + result.stderr)
        self.assertEqual("herb_gathering_tutorial", payload["quest"]["id"])
        self.assertEqual(3, payload["run_clock"]["max_days"])
        self.assertEqual(4, payload["run_clock"]["turns_per_day"])
        self.assertTrue(payload["turns"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        self.assertTrue(any(turn["multi_select"]["selected"] for turn in payload["turns"]))
        self.assertIn("quest_report", payload)
        self.assertIn(payload["quest_report"]["result_type"], {"success", "partial_success", "failure"})
        first_turn = payload["turns"][0]
        self.assertIn("run_clock", first_turn)
        self.assertIn("quest_progress", first_turn)
        self.assertIn("score", first_turn)
        self.assertIn("next_event_tags", first_turn)
        self.assertIn("[Day 1 / Morning / Turn 1]", text_log)
        self.assertIn("Quest: 약초 채집 의뢰", text_log)
        self.assertIn("카드:", text_log)
        self.assertIn("Quest Progress:", text_log)
        self.assertIn("Score Change:", text_log)
        self.assertIn("Quest Report:", text_log)
        self.assertIn("objective_results", payload["quest_report"])
        self.assertIn("목표 평가:", text_log)

    def test_tutorial_herb_quest_cli_covers_success_partial_and_failure_outcomes(self) -> None:
        # Given
        cases = (
            ("data/scenarios/tutorial_herb_quest.yaml", "success", set(), set()),
            (
                "data/scenarios/tutorial_herb_quest_partial.yaml",
                "partial_success",
                {"report_failed", "optional_failed", "return_late", "reduced_reward"},
                set(),
            ),
            (
                "data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml",
                "partial_success",
                {"primary_partial", "optional_failed", "return_late", "reduced_reward"},
                set(),
            ),
            (
                "data/scenarios/tutorial_herb_quest_failure.yaml",
                "failure",
                set(),
                {"max_turn_exceeded", "return_failed", "primary_objective_failed"},
            ),
            (
                "data/scenarios/tutorial_herb_quest_failure_health_zero.yaml",
                "failure",
                set(),
                {"health_zero", "return_failed", "primary_objective_failed"},
            ),
            (
                "data/scenarios/tutorial_herb_quest_failure_max_day.yaml",
                "failure",
                set(),
                {"max_day_exceeded"},
            ),
        )
        reports = {}
        partial_reasons: set[str] = set()
        failure_reasons: set[str] = set()

        for scenario_path, expected_result_type, expected_partial, expected_failure in cases:
            with self.subTest(scenario_path=scenario_path), tempfile.TemporaryDirectory() as tmp:
                # When
                result = subprocess.run(
                    [
                        sys.executable,
                        "tools/console_simulator.py",
                        "--scenario",
                        scenario_path,
                        "--seed",
                        "42",
                        "--runs",
                        "1",
                        "--logs",
                        tmp,
                        "--profile",
                        "balanced",
                    ],
                    check=False,
                    capture_output=True,
                    stdin=subprocess.DEVNULL,
                    text=True,
                    timeout=15,
                )
                json_logs = list(Path(tmp).glob("run_*.json"))
                text_logs = list(Path(tmp).glob("run_*.txt"))
                payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
                text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

                # Then
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual(1, len(json_logs), result.stdout + result.stderr)
                self.assertEqual(1, len(text_logs), result.stdout + result.stderr)
                self.assertEqual(expected_result_type, payload["quest_report"]["result_type"])
                self.assertIsInstance(payload["quest_report"]["score"], int)
                self.assertTrue(payload["quest_report"]["score_breakdown"])
                self.assertIn("completed_objectives", payload["quest_report"])
                self.assertIn("failed_objectives", payload["quest_report"])
                self.assertIn("review_text", payload["quest_report"])
                self.assertIn("result_reason", payload["quest_report"])
                self.assertIn("partial_reasons", payload["quest_report"])
                self.assertIn("failure_reasons", payload["quest_report"])
                self.assertIn("objective_results", payload["quest_report"])
                self.assertIn("reward_status", payload["quest_report"])
                self.assertTrue(expected_partial.issubset(set(payload["quest_report"]["partial_reasons"])))
                self.assertTrue(expected_failure.issubset(set(payload["quest_report"]["failure_reasons"])))
                objective_results = payload["quest_report"]["objective_results"]
                objective_by_id = {item["objective_id"]: item for item in objective_results}
                self.assertIn("collect_herbs", objective_by_id)
                self.assertIn("report_to_apothecary", objective_by_id)
                self.assertIn("survive_expedition", objective_by_id)
                self.assertIn("help_injured_traveler", objective_by_id)
                self.assertIn("objective_completion", payload["quest_report"]["score_breakdown"])
                self.assertIn(f"결과 유형: {expected_result_type}", text_log)
                self.assertIn("결과 이유:", text_log)
                self.assertIn("목표 평가:", text_log)
                self.assertIn("help_injured_traveler", text_log)
                self.assertIn(payload["quest_report"]["review_text"], text_log)
                partial_reasons.update(payload["quest_report"]["partial_reasons"])
                failure_reasons.update(payload["quest_report"]["failure_reasons"])
                reports.setdefault(expected_result_type, payload["quest_report"])
                if scenario_path.endswith("partial_optional_failed.yaml"):
                    reports["partial_optional_failed"] = payload["quest_report"]
                if scenario_path.endswith("failure_health_zero.yaml"):
                    reports["health_zero_failure"] = payload["quest_report"]
                if scenario_path.endswith("failure_max_day.yaml"):
                    reports["max_day_failure"] = payload["quest_report"]
                    self.assertTrue(payload["turns"])
                    self.assertGreater(payload["run_summary"]["final_state"]["health"], 0)

        # Then
        self.assertGreater(int(reports["success"]["score"]), int(reports["partial_success"]["score"]))
        self.assertGreater(int(reports["partial_success"]["score"]), int(reports["failure"]["score"]))
        self.assertEqual(["collect_herbs", "report_to_apothecary"], reports["success"]["completed_objectives"])
        self.assertEqual([], reports["success"]["failed_objectives"])
        self.assertEqual(["collect_herbs"], reports["partial_success"]["completed_objectives"])
        self.assertEqual(["report_to_apothecary"], reports["partial_success"]["failed_objectives"])
        self.assertEqual([], reports["failure"]["completed_objectives"])
        self.assertIn("survive_expedition", reports["health_zero_failure"]["failed_objectives"])
        self.assertEqual("completed", _objective_status(reports["success"], "collect_herbs"))
        self.assertEqual("completed", _objective_status(reports["success"], "report_to_apothecary"))
        self.assertEqual("completed", _objective_status(reports["success"], "survive_expedition"))
        self.assertEqual("completed", _objective_status(reports["partial_success"], "collect_herbs"))
        self.assertEqual("failed", _objective_status(reports["partial_success"], "report_to_apothecary"))
        self.assertEqual("partial", _objective_status(reports["partial_optional_failed"], "collect_herbs"))
        self.assertEqual("failed", _objective_status(reports["partial_optional_failed"], "help_injured_traveler"))
        self.assertEqual("failed", _objective_status(reports["failure"], "collect_herbs"))
        self.assertEqual("failed", _objective_status(reports["failure"], "report_to_apothecary"))
        self.assertEqual("completed", _objective_status(reports["failure"], "survive_expedition"))
        self.assertEqual("failed", _objective_status(reports["health_zero_failure"], "survive_expedition"))
        self.assertIn("max_day_exceeded", reports["max_day_failure"]["failure_reasons"])
        self.assertNotIn("max_turn_exceeded", reports["max_day_failure"]["failure_reasons"])
        self.assertTrue(reports["success"]["rewards"])
        self.assertEqual({}, reports["partial_success"]["rewards"])
        self.assertEqual({}, reports["failure"]["rewards"])
        self.assertLess(int(reports["failure"]["score_breakdown"]["outcome_adjustment"]), 0)
        self.assertGreaterEqual(len(partial_reasons), 2)
        self.assertGreaterEqual(len(failure_reasons), 3)

    def test_gameplay_run_schema_doc_matches_objective_fields(self) -> None:
        # Given
        doc = Path("docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md").read_text(encoding="utf-8")

        # Then
        for field in (
            "id",
            "type",
            "target",
            "required",
            "count",
            "value",
            "progress_key",
            "failure_reason",
            "partial_reason",
            "score_key",
            "reward_weight",
        ):
            self.assertIn(field, doc)
        for output_field in (
            "objective_results",
            "completed_objectives",
            "failed_objectives",
            "partial_reasons",
            "failure_reasons",
            "score_breakdown",
            "reward_status",
            "review_text",
        ):
            self.assertIn(output_field, doc)
        self.assertIn("optional_action", doc)
        self.assertIn("max_day_exceeded", doc)


def _objective_status(report: dict, objective_id: str) -> str:
    for objective in report["objective_results"]:
        if objective["objective_id"] == objective_id:
            return str(objective["status"])
    raise AssertionError(f"missing objective result: {objective_id}")


if __name__ == "__main__":
    unittest.main()
