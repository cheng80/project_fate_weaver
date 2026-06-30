from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Final, TypedDict

import yaml

from fateweaver.data_loader import load_project_data
from fateweaver.models import JsonMap


PROJECT_ROOT: Final = Path(__file__).resolve().parents[1]
DONE_SCENARIOS: Final = (
    "data/scenarios/tutorial_herb_quest.yaml",
    "data/scenarios/forest_path_scouting_tutorial.yaml",
    "data/scenarios/missing_porter_search_intro.yaml",
    "data/scenarios/merchant_lost_pack_recovery.yaml",
    "data/scenarios/village_well_trouble_success.yaml",
    "data/scenarios/ruin_mark_investigation_intro_success.yaml",
    "data/scenarios/defend_the_village_night_success.yaml",
    "data/scenarios/ghost_town_medicine_run_success.yaml",
    "data/scenarios/old_well_awakening_success.yaml",
    "data/scenarios/survive_the_storm_pass_success.yaml",
)


class BulkQuestDefinition(TypedDict):
    title: str
    cards: set[str]
    objectives: tuple[str, ...]


BULK_QUESTS: Final[dict[str, BulkQuestDefinition]] = {
    "beginner_village_wrongness": {
        "title": "초보 마을의 이상 징후",
        "cards": {"read_village_wrongness", "calm_square_rumors", "report_wrongness_resolved", "share_plain_remedy", "test_village_wrongness_risk"},
        "objectives": ("find_wrongness_sign", "calm_village_square", "report_wrongness_resolved"),
    },
    "festival_missing_racer": {
        "title": "축제의 사라진 주자",
        "cards": {"find_racer_track", "guide_missing_racer", "report_festival_safe", "organize_festival_search", "test_festival_risk"},
        "objectives": ("find_racer_track", "guide_missing_racer", "report_festival_safe"),
    },
    "abandoned_lighthouse_signal": {
        "title": "버려진 등대의 신호",
        "cards": {"inspect_signal_lamp", "decode_lighthouse_signal", "report_lighthouse_warning", "shield_lantern_oil", "test_lighthouse_risk"},
        "objectives": ("inspect_signal_lamp", "decode_lighthouse_signal", "report_lighthouse_warning"),
    },
    "painted_portal_canvas": {
        "title": "그려진 문 너머의 화폭",
        "cards": {"inspect_canvas_paint", "stabilize_portal_canvas", "report_canvas_truth", "cover_canvas_frame", "test_canvas_risk"},
        "objectives": ("inspect_canvas_paint", "stabilize_portal_canvas", "report_canvas_truth"),
    },
    "vanishing_village": {
        "title": "사라지는 마을의 흔적",
        "cards": {"find_vanishing_trace", "anchor_village_memory", "report_vanishing_village", "mark_returning_path", "test_vanishing_risk"},
        "objectives": ("find_vanishing_trace", "anchor_village_memory", "report_vanishing_village"),
    },
    "beast_of_zarechka": {
        "title": "자레치카의 짐승",
        "cards": {"identify_beast_tracks", "drive_beast_back", "reassure_zarechka", "set_beast_watchfire", "test_zarechka_beast_risk"},
        "objectives": ("identify_beast_tracks", "drive_beast_back", "reassure_zarechka"),
    },
    "cattle_mutilation_stone_circle": {
        "title": "돌 원의 소 떼 상처",
        "cards": {"inspect_cattle_circle", "break_stone_circle_lure", "warn_herders", "move_cattle_before_dusk", "test_stone_circle_risk"},
        "objectives": ("inspect_cattle_circle", "break_stone_circle_lure", "warn_herders"),
    },
    "caravan_to_border_fort": {
        "title": "국경 요새로 가는 상단",
        "cards": {"secure_caravan_manifest", "cross_border_road", "deliver_fort_supplies", "ration_caravan_food", "test_caravan_risk"},
        "objectives": ("secure_caravan_manifest", "cross_border_road", "deliver_fort_supplies"),
    },
    "winter_wagon_delivery": {
        "title": "겨울 마차 배송",
        "cards": {"prepare_winter_wagon", "cross_snow_road", "deliver_winter_goods", "warm_wagon_team", "test_winter_wagon_risk"},
        "objectives": ("prepare_winter_wagon", "cross_snow_road", "deliver_winter_goods"),
    },
    "deliver_the_sealed_parcel": {
        "title": "봉인된 소포 배달",
        "cards": {"receive_sealed_parcel", "avoid_parcel_tamper", "deliver_sealed_parcel", "hide_parcel_under_cloak", "test_sealed_parcel_risk"},
        "objectives": ("receive_sealed_parcel", "avoid_parcel_tamper", "deliver_sealed_parcel"),
    },
    "activate_the_old_gate": {
        "title": "오래된 문 작동",
        "cards": {"find_gate_runes", "align_old_gate", "return_gate_report", "brace_gate_stones", "test_old_gate_risk"},
        "objectives": ("find_gate_runes", "align_old_gate", "return_gate_report"),
    },
    "hidden_grove_discovery": {
        "title": "숨은 숲 빈터 발견",
        "cards": {"find_hidden_grove", "map_grove_path", "report_hidden_grove", "forage_grove_edges", "test_hidden_grove_risk"},
        "objectives": ("find_hidden_grove", "map_grove_path", "report_hidden_grove"),
    },
}


class GameplayP0CategoryBulkFillTests(unittest.TestCase):
    def test_bulk_fill_scenarios_validate_and_run_success(self) -> None:
        for quest_id, definition in BULK_QUESTS.items():
            with self.subTest(quest_id=quest_id):
                scenario_path = f"data/scenarios/{quest_id}.yaml"

                _validate_scenario(scenario_path)
                payload = _run_scenario(scenario_path)

                self.assertEqual(quest_id, payload["quest"]["id"])
                self.assertEqual("success", payload["quest_report"]["result_type"])
                self.assertTrue(payload["turns"])
                self.assertTrue(all(len(turn["presented_cards"]) == 3 for turn in payload["turns"]))
                self.assertIn("score_breakdown", payload["quest_report"])
                self.assertIn("objective_results", payload["quest_report"])
                self.assertIn("card_candidate_pool", payload["turns"][0])
                self.assertIn("storylet_tags", payload["turns"][0])
                self.assertIn("storylet_id", payload["turns"][0])
                self.assertIn(f"Quest: {definition['title']}", payload["_text_log"])
                self.assertIn("Quest Report:", payload["_text_log"])
                self.assertIn("결과 유형: success", payload["_text_log"])
                for objective_id in definition["objectives"]:
                    self.assertEqual("completed", _objective_status(payload["quest_report"], objective_id))

    def test_bulk_fill_quest_ids_gate_done_quest_regression(self) -> None:
        raw_quests = _load_all_quests()
        raw_cards = _load_all_card_rules()
        raw_events = yaml.safe_load((PROJECT_ROOT / "data/content/base/events.yaml").read_text(encoding="utf-8"))["events"]
        quest_ids = {quest["id"] for quest in raw_quests}
        bulk_cards = set().union(*(definition["cards"] for definition in BULK_QUESTS.values()))

        for quest_id, definition in BULK_QUESTS.items():
            with self.subTest(quest_id=quest_id):
                self.assertIn(quest_id, quest_ids)
                scoped_cards = [card for card in raw_cards if quest_id in card.get("quest_ids", [])]
                scoped_events = [event for event in raw_events if quest_id in event.get("quest_ids", [])]
                self.assertGreaterEqual(len(scoped_cards), 5)
                self.assertGreaterEqual(len(scoped_events), 2)
                self.assertTrue(definition["cards"].issubset({card["id"] for card in scoped_cards}))
                self.assertTrue(all(card.get("quest_ids") == [quest_id] for card in scoped_cards))
                self.assertTrue(all(event.get("quest_ids") == [quest_id] for event in scoped_events))
                self.assertTrue(all(len(event.get("card_candidate_hints", [])) >= 2 for event in scoped_events))

        for scenario_path in DONE_SCENARIOS:
            with self.subTest(regression=scenario_path):
                payload = _run_scenario(scenario_path)
                self.assertFalse(bulk_cards.intersection(_all_presented_and_selected_cards(payload)))

    def test_bulk_fill_event_quest_ids_runtime_gate(self) -> None:
        # Given
        scenario = "data/scenarios/tutorial_herb_quest.yaml"
        loaded = load_project_data(PROJECT_ROOT, PROJECT_ROOT / scenario)
        bulk_event_ids = {
            event["id"]
            for event in yaml.safe_load((PROJECT_ROOT / "data/content/base/events.yaml").read_text(encoding="utf-8"))["events"]
            if event.get("quest_ids")
        }

        # When
        payload = _run_scenario(scenario)
        loaded_bulk_events = {event.id for event in loaded.bundle.events if event.quest_ids}

        # Then
        self.assertTrue(bulk_event_ids)
        self.assertEqual(bulk_event_ids, loaded_bulk_events)
        self.assertFalse(bulk_event_ids.intersection({turn["event_id"] for turn in payload["turns"]}))


def _validate_scenario(scenario_path: str) -> None:
    result = subprocess.run(
        [sys.executable, "tools/validate_data.py", "--scenario", scenario_path],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)


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


def _load_all_card_rules() -> list[JsonMap]:
    raw_cards = list(yaml.safe_load((PROJECT_ROOT / "data/core/card_rules.yaml").read_text(encoding="utf-8"))["p0_cards"])
    split_dir = PROJECT_ROOT / "data/content/card_rules"
    for path in sorted(split_dir.glob("*.yaml")):
        raw_cards.extend(yaml.safe_load(path.read_text(encoding="utf-8"))["p0_cards"])
    return raw_cards


def _load_all_quests() -> list[JsonMap]:
    raw_quests = list(yaml.safe_load((PROJECT_ROOT / "data/content/base/quests.yaml").read_text(encoding="utf-8"))["quests"])
    split_dir = PROJECT_ROOT / "data/content/quests"
    for path in sorted(split_dir.glob("*.yaml")):
        raw_quests.extend(yaml.safe_load(path.read_text(encoding="utf-8"))["quests"])
    return raw_quests


if __name__ == "__main__":
    unittest.main()
