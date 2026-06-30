from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fateweaver.models import JsonMap


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MISSING_PORTER_CARDS = {
    "track_porter_footprints",
    "inspect_broken_cart",
    "rescue_injured_porter",
    "recover_lost_pack",
    "return_with_porter_report",
    "buy_hunter_information",
}


class GameplayP0MissingPorterSearchTests(unittest.TestCase):
    def test_missing_porter_search_success_partial_failure(self) -> None:
        # Given
        cases = (
            ("data/scenarios/missing_porter_search_intro.yaml", "success"),
            ("data/scenarios/missing_porter_search_intro_partial.yaml", "partial_success"),
            ("data/scenarios/missing_porter_search_intro_failure.yaml", "failure"),
        )

        # When
        reports = {expected: _run_scenario(path)["quest_report"] for path, expected in cases}

        # Then
        self.assertEqual("success", reports["success"]["result_type"])
        self.assertEqual("partial_success", reports["partial_success"]["result_type"])
        self.assertEqual("failure", reports["failure"]["result_type"])
        self.assertGreater(int(reports["success"]["score"]), int(reports["partial_success"]["score"]))
        self.assertGreater(int(reports["partial_success"]["score"]), int(reports["failure"]["score"]))
        self.assertEqual("completed", _objective_status(reports["success"], "find_porter_trace"))
        self.assertEqual("completed", _objective_status(reports["success"], "resolve_porter_fate"))
        self.assertEqual("completed", _objective_status(reports["success"], "return_to_village"))
        self.assertEqual("completed", _objective_status(reports["success"], "survive_expedition"))
        self.assertEqual("completed", _objective_status(reports["partial_success"], "find_porter_trace"))
        self.assertEqual("completed", _objective_status(reports["partial_success"], "resolve_porter_fate"))
        self.assertEqual("failed", _objective_status(reports["partial_success"], "return_to_village"))
        self.assertIn("report_failed", reports["partial_success"]["partial_reasons"])
        self.assertEqual("failed", _objective_status(reports["failure"], "find_porter_trace"))
        self.assertEqual("failed", _objective_status(reports["failure"], "resolve_porter_fate"))
        self.assertEqual("failed", _objective_status(reports["failure"], "return_to_village"))
        self.assertIn("health_zero", reports["failure"]["failure_reasons"])
        self.assertTrue(reports["success"]["rewards"])
        self.assertEqual({}, reports["partial_success"]["rewards"])
        self.assertEqual({}, reports["failure"]["rewards"])

    def test_missing_porter_storylet_hints_and_logs(self) -> None:
        # Given
        payload = _run_scenario("data/scenarios/missing_porter_search_intro.yaml")
        text_log = payload["_text_log"]

        # Then
        self.assertEqual("missing_porter_search_intro", payload["quest"]["id"])
        self.assertTrue(payload["turns"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        hinted_turns = [turn for turn in payload["turns"] if turn["card_candidate_hints"]]
        self.assertTrue(hinted_turns)
        hinted_ids = {card_id for turn in hinted_turns for card_id in turn["card_candidate_hints"]}
        self.assertIn("track_porter_footprints", hinted_ids)
        self.assertIn("rescue_injured_porter", hinted_ids)
        self.assertIn("recover_lost_pack", hinted_ids)
        self.assertTrue(any(turn["repeat_memory_snapshot"] is not None for turn in payload["turns"]))
        self.assertTrue(any("matched_storylet_hints" in card for turn in payload["turns"] for card in turn["card_candidate_pool"]))
        self.assertIn("Quest: 실종된 짐꾼 수색", text_log)
        self.assertIn("카드:", text_log)
        self.assertIn("선택:", text_log)
        self.assertIn("Quest Report:", text_log)
        self.assertIn("결과 유형: success", text_log)

    def test_missing_porter_quest_id_gate_preserves_existing_tutorials(self) -> None:
        # Given
        herb_payload = _run_scenario("data/scenarios/tutorial_herb_quest.yaml")
        forest_payload = _run_scenario("data/scenarios/forest_path_scouting_tutorial.yaml")

        # Then
        self.assertEqual("success", herb_payload["quest_report"]["result_type"])
        self.assertEqual("success", forest_payload["quest_report"]["result_type"])
        herb_cards = _all_presented_and_selected_cards(herb_payload)
        forest_cards = _all_presented_and_selected_cards(forest_payload)
        self.assertFalse(MISSING_PORTER_CARDS.intersection(herb_cards))
        self.assertFalse(MISSING_PORTER_CARDS.intersection(forest_cards))


def _run_scenario(scenario_path: str) -> JsonMap:
    with tempfile.TemporaryDirectory() as tmp:
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
            cwd=PROJECT_ROOT,
            check=False,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            text=True,
            timeout=15,
        )
        json_logs = list(Path(tmp).glob("run_*.json"))
        text_logs = list(Path(tmp).glob("run_*.txt"))
        payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
        payload["_text_log"] = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    if len(json_logs) != 1:
        raise AssertionError(result.stdout + result.stderr)
    if len(text_logs) != 1:
        raise AssertionError(result.stdout + result.stderr)
    return payload


def _objective_status(report: JsonMap, objective_id: str) -> str:
    for objective in report["objective_results"]:
        if objective["objective_id"] == objective_id:
            return str(objective["status"])
    raise AssertionError(f"missing objective result: {objective_id}")


def _all_presented_and_selected_cards(payload: JsonMap) -> set[str]:
    presented = {card["card_id"] for turn in payload["turns"] for card in turn["presented_cards"]}
    selected = {card_id for turn in payload["turns"] for card_id in turn["selected_cards"]}
    return presented.union(selected)


if __name__ == "__main__":
    unittest.main()
