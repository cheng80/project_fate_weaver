from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fateweaver.models import JsonMap


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROBES = {
    "village_well_trouble": {
        "title": "병든 우물",
        "cards": {"inspect_sick_well", "purify_well_with_herbs", "report_well_restored"},
        "objectives": ("find_well_contamination", "restore_well_safety", "report_to_village"),
        "hints": {"inspect_sick_well", "purify_well_with_herbs"},
    },
    "ruin_mark_investigation_intro": {
        "title": "폐허 표식 조사",
        "cards": {"copy_ruin_mark", "interpret_omen_pattern", "report_ruin_mark"},
        "objectives": ("discover_ruin_mark", "interpret_ruin_omen", "report_to_sage"),
        "hints": {"copy_ruin_mark", "interpret_omen_pattern"},
    },
    "defend_the_village_night": {
        "title": "마을 방어의 밤",
        "cards": {"raise_village_barricade", "evacuate_border_homes", "hold_night_watch"},
        "objectives": ("identify_night_threat", "hold_village_defense", "protect_village_morale"),
        "hints": {"raise_village_barricade", "hold_night_watch"},
    },
    "ghost_town_medicine_run": {
        "title": "유령 마을 약 전달",
        "cards": {"take_medicine_bundle", "cross_silent_road", "deliver_ghost_town_medicine"},
        "objectives": ("secure_medicine_bundle", "find_ghost_town_route", "deliver_medicine"),
        "hints": {"cross_silent_road", "deliver_ghost_town_medicine"},
    },
    "old_well_awakening": {
        "title": "오래된 우물 각성",
        "cards": {"descend_old_well", "read_cracked_seal", "reseal_well_awakening"},
        "objectives": ("discover_well_seal", "reseal_well_depths", "return_with_seal_report"),
        "hints": {"descend_old_well", "reseal_well_awakening"},
    },
    "survive_the_storm_pass": {
        "title": "폭풍 산길 생존 귀환",
        "cards": {"read_storm_pass_sky", "secure_storm_shelter", "return_from_storm_pass"},
        "objectives": ("find_storm_shelter", "secure_survival_route", "survive_expedition"),
        "hints": {"read_storm_pass_sky", "secure_storm_shelter"},
    },
}


class GameplayP0CategoryProbeTests(unittest.TestCase):
    def test_category_probe_success_partial_failure(self) -> None:
        # Given
        suffixes = {
            "success": "success",
            "partial": "partial_success",
            "failure": "failure",
        }

        for quest_id, definition in PROBES.items():
            with self.subTest(quest_id=quest_id):
                # When
                reports = {
                    expected: _run_scenario(f"data/scenarios/{quest_id}_{suffix}.yaml")["quest_report"]
                    for suffix, expected in suffixes.items()
                }

                # Then
                self.assertEqual("success", reports["success"]["result_type"])
                self.assertEqual("partial_success", reports["partial_success"]["result_type"])
                self.assertEqual("failure", reports["failure"]["result_type"])
                self.assertGreater(int(reports["success"]["score"]), int(reports["partial_success"]["score"]))
                self.assertGreater(int(reports["partial_success"]["score"]), int(reports["failure"]["score"]))
                self.assertEqual("none", reports["success"]["failure_kind"])
                self.assertEqual("alive", reports["success"]["character_outcome"])
                self.assertIn(reports["failure"]["failure_kind"], {"objective_failed", "death_or_incapacitated", "time_expired"})
                self.assertIn(reports["failure"]["character_outcome"], {"alive", "incapacitated"})
                for objective_id in definition["objectives"]:
                    self.assertIn(_objective_status(reports["success"], objective_id), {"completed"})

    def test_category_probe_storylet_hints_logs_and_gates(self) -> None:
        # Given
        regression_payloads = (
            _run_scenario("data/scenarios/tutorial_herb_quest.yaml"),
            _run_scenario("data/scenarios/forest_path_scouting_tutorial.yaml"),
            _run_scenario("data/scenarios/missing_porter_search_intro.yaml"),
            _run_scenario("data/scenarios/merchant_lost_pack_recovery.yaml"),
        )

        for quest_id, definition in PROBES.items():
            with self.subTest(quest_id=quest_id):
                # When
                payload = _run_scenario(f"data/scenarios/{quest_id}_success.yaml")
                text_log = payload["_text_log"]

                # Then
                self.assertEqual(quest_id, payload["quest"]["id"])
                self.assertTrue(payload["turns"])
                self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
                hinted_ids = {card_id for turn in payload["turns"] for card_id in turn["card_candidate_hints"]}
                self.assertTrue(definition["hints"].issubset(hinted_ids))
                self.assertTrue(any(turn["repeat_memory_snapshot"] is not None for turn in payload["turns"]))
                self.assertTrue(any("matched_storylet_hints" in card for turn in payload["turns"] for card in turn["card_candidate_pool"]))
                self.assertIn(f"Quest: {definition['title']}", text_log)
                self.assertIn("Quest Report:", text_log)
                self.assertIn("결과 유형: success", text_log)

                probe_cards = definition["cards"]
                for regression_payload in regression_payloads:
                    self.assertFalse(probe_cards.intersection(_all_presented_and_selected_cards(regression_payload)))


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
