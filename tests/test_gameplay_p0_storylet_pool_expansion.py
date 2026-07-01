from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.data_loader import load_project_data
from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.scenario_filter import filter_events_for_scenario


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = PROJECT_ROOT / "data/scenarios/standard_run_25_35_turn.yaml"
NEW_STORYLET_IDS = {
    "nervous_merchant_revises_story",
    "second_witness_contradicts_merchant",
    "trade_gossip_points_elsewhere",
    "merchant_receipt_marks_old_route",
    "wind_gap_reveals_safe_descent",
    "frost_on_pack_straps",
    "distant_tree_line_breaks_storm",
    "snowmelt_points_to_shelter",
    "ridge_echo_marks_return",
    "wet_charcoal_marks_route",
    "broken_signpost_matches_map",
    "blue_flame_over_old_cut",
    "oil_sheen_points_to_false_signal",
    "silent_birds_circle_ridge",
    "fresh_claw_marks_near_tarp",
    "watchfire_gutters_wrong_way",
    "guide_demands_storm_fee",
    "caravan_rut_avoids_flood",
    "bridge_rope_frays_in_wind",
    "old_rune_matches_storm_scar",
    "sealed_stone_hums_under_rain",
    "ritual_smoke_bends_uphill",
}
STANDARD_RUN_ALTERNATIVES = {
    "nervous_merchant_revises_story",
    "second_witness_contradicts_merchant",
    "trade_gossip_points_elsewhere",
    "merchant_receipt_marks_old_route",
    "wind_gap_reveals_safe_descent",
    "frost_on_pack_straps",
    "distant_tree_line_breaks_storm",
    "snowmelt_points_to_shelter",
    "ridge_echo_marks_return",
}
PROTECTED_STORYLETS = {"suspicious_merchant", "storm_pass_shelter_hint"}
SITUATION_INTENT_TAGS = {
    "reveal_clue",
    "escalate_risk",
    "offer_resource_tradeoff",
    "offer_optional_help",
    "invite_return",
    "introduce_omen",
    "resolve_objective",
    "test_reputation",
    "test_survival",
    "unlock_route",
}


class GameplayP0StoryletPoolExpansionTests(unittest.TestCase):
    def test_storylet_pool_event_count_increased(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)

        self.assertLessEqual(18, len(NEW_STORYLET_IDS))
        self.assertTrue(NEW_STORYLET_IDS.issubset(loaded.bundle.events_by_id))

    def test_new_storylets_have_valid_card_candidate_hints(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)
        card_ids = {card.id for card in load_foundation(PROJECT_ROOT, loaded.scenario.active_quest_id).card_rules.cards}

        for event_id in NEW_STORYLET_IDS:
            event = loaded.bundle.events_by_id[event_id]
            self.assertTrue(event.card_candidate_hints, event_id)
            self.assertTrue(set(event.card_candidate_hints).issubset(card_ids), event_id)

    def test_new_storylets_have_quest_ids_when_gated(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)

        for event_id in NEW_STORYLET_IDS:
            event = loaded.bundle.events_by_id[event_id]
            self.assertTrue(event.quest_ids, event_id)

    def test_new_storylets_have_repeat_group_or_cooldown_tags(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)

        for event_id in NEW_STORYLET_IDS:
            event = loaded.bundle.events_by_id[event_id]
            self.assertTrue(event.repeat_group or event.cooldown_tags, event_id)
            self.assertGreater(event.cooldown_turns or 0, 0, event_id)

    def test_standard_run_includes_alternatives_without_disabling_existing_storylets(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)
        filtered = filter_events_for_scenario(loaded.bundle.events, loaded.scenario)
        filtered_ids = {event.id for event in filtered}

        self.assertTrue(PROTECTED_STORYLETS.issubset(filtered_ids))
        self.assertTrue(STANDARD_RUN_ALTERNATIVES.issubset(filtered_ids))
        self.assertGreaterEqual(len(filtered_ids), 14)

    def test_storylets_expand_situation_intent_surface(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, SCENARIO_PATH)
        tag_counts = {
            tag: sum(1 for event_id in NEW_STORYLET_IDS if tag in loaded.bundle.events_by_id[event_id].storylet_tags)
            for tag in SITUATION_INTENT_TAGS
        }

        missing = [tag for tag, count in tag_counts.items() if count < 2]
        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
