from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fateweaver.models import JsonMap


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GameplayP0ForestPathScoutingTests(unittest.TestCase):
    def test_forest_path_scouting_success_partial_failure(self) -> None:
        # Given
        cases = (
            ("data/scenarios/forest_path_scouting_tutorial.yaml", "success"),
            ("data/scenarios/forest_path_scouting_tutorial_partial.yaml", "partial_success"),
            ("data/scenarios/forest_path_scouting_tutorial_failure.yaml", "failure"),
        )

        # When
        reports = {expected: _run_scenario(path)["quest_report"] for path, expected in cases}

        # Then
        self.assertEqual("success", reports["success"]["result_type"])
        self.assertEqual("partial_success", reports["partial_success"]["result_type"])
        self.assertEqual("failure", reports["failure"]["result_type"])
        self.assertGreater(int(reports["success"]["score"]), int(reports["partial_success"]["score"]))
        self.assertGreater(int(reports["partial_success"]["score"]), int(reports["failure"]["score"]))
        self.assertEqual("completed", _objective_status(reports["success"], "discover_safe_path"))
        self.assertEqual("completed", _objective_status(reports["success"], "return_to_village"))
        self.assertEqual("completed", _objective_status(reports["success"], "survive_expedition"))
        self.assertEqual("completed", _objective_status(reports["partial_success"], "discover_safe_path"))
        self.assertEqual("failed", _objective_status(reports["partial_success"], "return_to_village"))
        self.assertEqual("failed", _objective_status(reports["failure"], "discover_safe_path"))
        self.assertEqual("failed", _objective_status(reports["failure"], "return_to_village"))
        self.assertIn("health_zero", reports["failure"]["failure_reasons"])
        self.assertTrue(reports["success"]["rewards"])
        self.assertEqual({}, reports["partial_success"]["rewards"])
        self.assertEqual({}, reports["failure"]["rewards"])

    def test_forest_path_scouting_storylet_hints_and_logs(self) -> None:
        # Given
        payload = _run_scenario("data/scenarios/forest_path_scouting_tutorial.yaml")
        text_log = payload["_text_log"]

        # Then
        self.assertEqual("forest_path_scouting_tutorial", payload["quest"]["id"])
        self.assertTrue(payload["turns"])
        self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
        hinted_turns = [turn for turn in payload["turns"] if turn["card_candidate_hints"]]
        self.assertTrue(hinted_turns)
        hinted_ids = {card_id for turn in hinted_turns for card_id in turn["card_candidate_hints"]}
        self.assertIn("inspect_forest_marker", hinted_ids)
        self.assertTrue(any("mark_beast_tracks" in turn["card_candidate_hints"] for turn in hinted_turns))
        self.assertTrue(any(turn["repeat_memory_snapshot"] is not None for turn in payload["turns"]))
        self.assertTrue(any("matched_storylet_hints" in card for turn in payload["turns"] for card in turn["card_candidate_pool"]))
        self.assertIn("Quest: 숲길 안전 조사", text_log)
        self.assertIn("카드:", text_log)
        self.assertIn("선택:", text_log)
        self.assertIn("Quest Report:", text_log)
        self.assertIn("결과 유형: success", text_log)

    def test_forest_path_scouting_does_not_break_herb_tutorial(self) -> None:
        # Given
        payload = _run_scenario("data/scenarios/tutorial_herb_quest.yaml")

        # Then
        self.assertEqual("herb_gathering_tutorial", payload["quest"]["id"])
        self.assertEqual("success", payload["quest_report"]["result_type"])
        forest_cards = {
            "inspect_forest_marker",
            "follow_beast_tracks",
            "mark_beast_tracks",
            "conserve_food_on_trail",
            "return_to_village_report",
        }
        presented = {card["card_id"] for turn in payload["turns"] for card in turn["presented_cards"]}
        selected = {card_id for turn in payload["turns"] for card_id in turn["selected_cards"]}
        self.assertFalse(forest_cards.intersection(presented))
        self.assertFalse(forest_cards.intersection(selected))


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


if __name__ == "__main__":
    unittest.main()
