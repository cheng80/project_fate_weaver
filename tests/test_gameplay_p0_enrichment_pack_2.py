from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from fateweaver.data_loader import load_project_data
from fateweaver.card_candidates import card_available
from fateweaver.gameplay_setup import load_foundation
from fateweaver.gameplay_models import RepeatMemory, RunClock, RunState
from fateweaver.quest_objectives import QuestReportRequest, build_quest_report
from fateweaver.text_mud_report import format_quest_report
from fateweaver.validator import validate_scenario_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PACK2_ITEMS = {
    "ash_salt_pouch",
    "beast_scent_tar",
    "camp_tarp",
    "chalk_marker_set",
    "clear_water_vial",
    "copper_listening_cup",
    "dried_bitterroot",
    "folding_probe_rod",
    "ink_fixing_powder",
    "iron_nail_bundle",
    "mirror_shard",
    "oath_coin",
    "oilcloth_map_case",
    "red_thread_charm",
    "reed_whistle",
    "sealed_letter_copy",
    "small_signal_bell",
    "smoke_cord",
    "soft_boot_wraps",
    "spare_ration_cache",
    "spare_wheel_pin",
    "tarred_rope_hook",
    "village_token",
    "warm_lantern_oil",
    "waxed_thread_spool",
}

PACK2_ENDINGS = {
    "clear_report_return",
    "costly_truth_return",
    "prepared_frontier_route",
    "rescued_but_hunted",
    "rich_but_distrusted",
    "ritual_interrupted_not_understood",
    "sealed_danger_left_behind",
    "survivor_without_answer",
}


class GameplayP0EnrichmentPack2Tests(unittest.TestCase):
    def test_pack_2_item_count_increased(self) -> None:
        self.assertTrue(PACK2_ITEMS.issubset(_base_item_ids()))
        self.assertEqual(25, len(PACK2_ITEMS))

    def test_pack_2_ending_count_increased(self) -> None:
        self.assertTrue(PACK2_ENDINGS.issubset(_base_ending_ids()))
        self.assertEqual(8, len(PACK2_ENDINGS))

    def test_pack_2_item_ids_are_unique(self) -> None:
        ids = [str(item["id"]) for item in _all_items()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_pack_2_ending_ids_are_unique(self) -> None:
        ids = [str(ending["id"]) for ending in _base_endings()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_pack_2_items_connect_to_cards_or_effects(self) -> None:
        cards = _all_card_ids()
        endings = _base_ending_ids()
        for item in _pack2_item_defs():
            with self.subTest(item_id=item["id"]):
                self.assertTrue(
                    item.get("unlocks_cards")
                    or item.get("modifies_results")
                    or item.get("resource_effects")
                    or item.get("risk_effects")
                    or item.get("ending_links")
                )
                for card_id in item.get("unlocks_cards", []):
                    self.assertIn(card_id, cards)
                for ending_id in item.get("ending_links", []):
                    self.assertIn(ending_id, endings)

    def test_pack_2_endings_connect_to_report_conditions(self) -> None:
        report_keys = {
            "result_type",
            "failure_kind",
            "character_outcome",
            "reward_status",
            "required_partial_reasons",
            "required_failure_reasons",
            "required_completed_objectives",
            "required_failed_objectives",
        }
        run_review_keys = {
            "min_score",
            "max_score",
            "min_reputation",
            "max_reputation",
            "min_money",
            "max_money",
            "min_clues",
            "max_clues",
            "min_omens",
            "max_omens",
            "required_any_clues",
            "required_all_clues",
            "required_any_omens",
            "required_all_omens",
            "required_any_items",
            "required_all_items",
        }
        for ending in _pack2_ending_defs():
            condition = dict(ending["condition"])
            with self.subTest(ending_id=ending["id"]):
                self.assertTrue(report_keys.intersection(condition))
                self.assertTrue(run_review_keys.intersection(condition))

    def test_pack_2_item_requirement_changes_card_availability(self) -> None:
        foundation = load_foundation(PROJECT_ROOT, "village_well_trouble")
        card = next(card for card in foundation.card_rules.cards if card.id == "inspect_shared_water_source")
        state_without_item = _state(inventory=())
        state_with_item = _state(inventory=("clear_water_vial",))

        self.assertFalse(card_available(card, state_without_item, "village_well_trouble"))
        self.assertTrue(card_available(card, state_with_item, "village_well_trouble"))

    def test_pack_2_text_mud_report_can_surface_ending(self) -> None:
        bundle = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/tutorial_herb_quest.yaml").bundle
        foundation = load_foundation(PROJECT_ROOT, "herb_gathering_tutorial")
        state = _state(
            inventory=("clear_water_vial",),
            clues=("shared_cup_sediment",),
            status={"health": 7, "food": 3, "money": 2, "reputation": 1, "curse": 0},
            quest_progress={"herbs_collected": 3, "reported_to_apothecary": 1},
        )

        report = build_quest_report(QuestReportRequest(foundation.quest, state, bundle, foundation.score_rules))
        lines = format_quest_report(report)

        self.assertEqual("clear_report_return", report["ending"]["id"])
        self.assertIn("Run Ending: clear_report_return / 납득된 보고", lines)

    def test_pack_2_ending_can_match_resource_bound(self) -> None:
        bundle = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/tutorial_herb_quest.yaml").bundle
        foundation = load_foundation(PROJECT_ROOT, "herb_gathering_tutorial")
        state = _state(
            inventory=(),
            clues=("shared_cup_sediment",),
            status={"health": 7, "food": 1, "money": 1, "reputation": 0, "curse": 0},
            quest_progress={"herbs_collected": 1, "reported_to_apothecary": 1},
        )

        report = build_quest_report(QuestReportRequest(foundation.quest, state, bundle, foundation.score_rules))

        self.assertEqual("partial_success", report["result_type"])
        self.assertEqual("costly_truth_return", report["ending"]["id"])

    def test_pack_2_existing_active_scenarios_still_pass(self) -> None:
        for scenario_path in _active_scenario_paths():
            with self.subTest(scenario=scenario_path.name):
                self.assertEqual([], validate_scenario_file(PROJECT_ROOT, scenario_path))


def _state(
    *,
    inventory: tuple[str, ...],
    clues: tuple[str, ...] = (),
    status: dict[str, int] | None = None,
    quest_progress: dict[str, int] | None = None,
) -> RunState:
    return RunState(
        clock=RunClock(day=1, turn=1, turns_today=0, time_of_day="morning", act=1, max_days=3, max_turns=12, turns_per_day=4),
        status=status or {"health": 7, "food": 5, "money": 2, "reputation": 0, "curse": 0},
        inventory=inventory,
        run_tags=(),
        region="village",
        quest_progress=quest_progress or {},
        clues=clues,
        omens=(),
        score={},
        next_event_tags=(),
        recent_event_ids=(),
        recent_presented_card_ids=(),
        selected_choice_history=(),
        repeat_memory=RepeatMemory(),
        combo_used=False,
    )


def _pack2_item_defs() -> list[dict[str, object]]:
    return [item for item in _base_items() if item["id"] in PACK2_ITEMS]


def _pack2_ending_defs() -> list[dict[str, object]]:
    return [ending for ending in _base_endings() if ending["id"] in PACK2_ENDINGS]


def _base_item_ids() -> set[str]:
    return {str(item["id"]) for item in _base_items()}


def _base_ending_ids() -> set[str]:
    return {str(ending["id"]) for ending in _base_endings()}


def _all_card_ids() -> set[str]:
    return {
        str(card["id"])
        for path in (PROJECT_ROOT / "data/content/card_rules").glob("*.yaml")
        for card in _raw_list(path, "p0_cards")
    } | {str(card["id"]) for card in _raw_list(PROJECT_ROOT / "data/core/card_rules.yaml", "p0_cards")}


def _all_items() -> list[dict[str, object]]:
    return [
        item
        for path in ((PROJECT_ROOT / "data/content/base/items.yaml"), *(PROJECT_ROOT / "data/content/packs").glob("*/items.yaml"))
        for item in _raw_list(path, "items")
    ]


def _base_items() -> list[dict[str, object]]:
    return _raw_list(PROJECT_ROOT / "data/content/base/items.yaml", "items")


def _base_endings() -> list[dict[str, object]]:
    return _raw_list(PROJECT_ROOT / "data/content/base/endings.yaml", "endings")


def _active_scenario_paths() -> list[Path]:
    paths: list[Path] = []
    for path in sorted((PROJECT_ROOT / "data/scenarios").glob("*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if raw.get("active_quest_id"):
            paths.append(path)
    return paths


def _raw_list(path: Path, key: str) -> list[dict[str, object]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(raw.get(key, []))


if __name__ == "__main__":
    unittest.main()
