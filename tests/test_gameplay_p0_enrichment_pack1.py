from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CLUES = {
    "ashes_without_heat",
    "border_coin_mark",
    "broken_fence_from_inside",
    "cold_lantern_soot",
    "double_printed_footsteps",
    "dry_moss_line",
    "false_signal_interval",
    "hollow_wall_echo",
    "insects_above_clean_water",
    "livestock_refused_gate",
    "matching_salt_on_cloth",
    "missing_market_tally",
    "old_stair_recent_dust",
    "rune_sequence_gap",
    "same_knot_on_three_doors",
    "scraped_symbol_edge",
    "seal_breaths_at_dusk",
    "sealed_thread_shifted",
    "shared_cup_sediment",
    "silent_bird_ring",
    "snow_filled_shortcut",
    "unused_escape_rope",
    "wagon_axle_old_cut",
    "watch_bell_struck_twice",
    "witness_changed_route",
}

EXPECTED_OMENS = {
    "animal_paths_cross_twice",
    "bell_echo_arrives_first",
    "clean_water_tastes_of_smoke",
    "clouds_hold_too_still",
    "dogs_face_the_old_road",
    "dust_moves_without_step",
    "fence_shadow_bends_inward",
    "map_ink_moves_after_rain",
    "market_stalls_close_early",
    "no_crows_on_battlefield",
    "old_water_flows_uphill",
    "rune_glows_before_touch",
    "same_song_from_empty_house",
    "sealed_bag_warms_near_gate",
    "signal_light_skips_count",
    "snow_falls_against_wind",
    "wagon_wheel_sings_low",
    "watch_fire_burns_blue",
    "well_rope_wet_at_dawn",
    "witnesses_avoid_one_word",
}


class GameplayP0EnrichmentPack1Tests(unittest.TestCase):
    def test_pack1_card_clue_omen_counts(self) -> None:
        cards = _pack1_cards()
        clues = {clue for card in cards for clue in card.get("result", {}).get("gain_clues", [])}
        omens = {omen for card in cards for omen in card.get("result", {}).get("gain_omens", [])}
        roles = Counter(str(card["slot_role"]) for card in cards)

        self.assertEqual(40, len(cards))
        self.assertEqual(14, roles["quest_progress"])
        self.assertEqual(12, roles["risk_discovery"])
        self.assertEqual(14, roles["resource_alternative"])
        self.assertEqual(EXPECTED_CLUES, clues)
        self.assertEqual(EXPECTED_OMENS, omens)

    def test_pack1_cards_are_event_hint_connected(self) -> None:
        cards = _pack1_cards()
        event_hints = {
            (quest_id, card_id)
            for event in _pack1_events()
            for quest_id in event.get("quest_ids", [])
            for card_id in event.get("card_candidate_hints", [])
        }

        self.assertEqual(18, len(_pack1_events()))
        for card in cards:
            with self.subTest(card_id=card["id"]):
                self.assertEqual(1, len(card.get("quest_ids", [])))
                quest_id = str(card["quest_ids"][0])
                self.assertIn((quest_id, card["id"]), event_hints)

    def test_pack1_split_events_keep_single_quest_gate(self) -> None:
        for event in _pack1_events():
            with self.subTest(event_id=event["id"]):
                self.assertEqual(1, len(event.get("quest_ids", [])))
                self.assertGreaterEqual(len(event.get("card_candidate_hints", [])), 1)
                self.assertIn("pack1_enrichment", event.get("storylet_tags", []))


def _pack1_cards() -> list[dict[str, object]]:
    return [
        card
        for path in sorted((PROJECT_ROOT / "data/content/card_rules").glob("*.yaml"))
        for card in _raw_list(path, "p0_cards")
        if "pack1_enrichment" in card.get("tags", [])
    ]


def _pack1_events() -> list[dict[str, object]]:
    return [
        event
        for path in sorted((PROJECT_ROOT / "data/content/events").glob("*.yaml"))
        for event in _raw_list(path, "events")
        if "pack1_enrichment" in event.get("storylet_tags", [])
    ]


def _raw_list(path: Path, key: str) -> list[dict[str, object]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(raw.get(key, []))


if __name__ == "__main__":
    unittest.main()
