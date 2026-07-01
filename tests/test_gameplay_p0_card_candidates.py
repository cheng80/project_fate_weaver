from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from fateweaver.gameplay_p0_card_selection import select_cards_from_pool
from fateweaver.gameplay_p0_cards import build_card_candidate_pool, cards_from_pool, present_cards
from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.gameplay_p0_models import (
    CardCandidate,
    CardCandidateContext,
    CardRule,
    CardSelectionContext,
    Foundation,
    RunState,
)
from fateweaver.gameplay_p0_rules import initial_state
from fateweaver.models import Scenario


class GameplayP0CardCandidateTests(unittest.TestCase):
    def test_card_candidate_score_uses_storylet_tags(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        matching_context = CardCandidateContext(foundation.quest, ("forest", "injured_traveler", "aid_opportunity"))
        plain_context = CardCandidateContext(foundation.quest, ("forest",))

        # When
        matching = _candidate_score(build_card_candidate_pool(foundation.card_rules.cards, state, matching_context), "help_injured_traveler")
        plain = _candidate_score(build_card_candidate_pool(foundation.card_rules.cards, state, plain_context), "help_injured_traveler")

        # Then
        self.assertGreater(matching, plain)

    def test_card_candidate_score_uses_quest_objective(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(foundation.quest, ("forest", "injured_traveler", "aid_opportunity"))

        # When
        candidate = _candidate(build_card_candidate_pool(foundation.card_rules.cards, state, context), "help_injured_traveler")

        # Then
        self.assertIn("help_injured_traveler", candidate.matched_objectives)
        self.assertGreaterEqual(candidate.score, 70)

    def test_card_candidate_tier_classification(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(foundation.quest, ("forest", "injured_traveler", "aid_opportunity"))

        # When
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)

        # Then
        self.assertEqual("strong", _candidate(pool, "help_injured_traveler").tier)
        self.assertEqual("blocked", _candidate(pool, "report_to_apothecary").tier)

    def test_three_card_selection_balances_slot_roles(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(foundation.quest, ("forest", "injured_traveler", "aid_opportunity"))

        # When
        cards = present_cards(foundation.card_rules.cards, state, context)

        # Then
        self.assertEqual(("quest_progress", "risk_discovery", "resource_alternative"), tuple(card.slot_role for card in cards))

    def test_completed_optional_card_not_repeated(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        state.quest_progress["helped_injured_traveler"] = 1
        context = CardCandidateContext(foundation.quest, ("forest", "injured_traveler", "aid_opportunity"))

        # When
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        cards = present_cards(foundation.card_rules.cards, state, context)

        # Then
        self.assertEqual("blocked", _candidate(pool, "help_injured_traveler").tier)
        self.assertNotIn("help_injured_traveler", [card.id for card in cards])

    def test_candidate_pool_logged_to_json(self) -> None:
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            # When
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest_optional_completed.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "curious_leaning",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            json_logs = list(Path(tmp).glob("run_*.json"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        pool = payload["turns"][0]["card_candidate_pool"]
        expected_keys = {
            "card_id",
            "slot_role",
            "score",
            "tier",
            "matched_tags",
            "matched_objectives",
            "blocked_reason",
            "selection_seed_key",
            "selected_by",
            "variety_window",
            "repeat_penalty",
        }
        self.assertTrue(expected_keys <= set(pool[0]))

    def test_same_seed_same_three_cards(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(foundation.quest, ("forest", "hidden_path"))
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        selection = _selection_context(foundation, state, 42)

        # When
        first = cards_from_pool(pool, selection)
        second = cards_from_pool(pool, selection)

        # Then
        self.assertEqual([card.id for card in first], [card.id for card in second])

    def test_different_seed_can_change_same_tier_card(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(foundation.quest, ("forest", "hidden_path"))
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)

        # When
        seed_42_cards = cards_from_pool(pool, _selection_context(foundation, state, 42))
        seed_43_cards = cards_from_pool(pool, _selection_context(foundation, state, 43))

        # Then
        self.assertNotEqual([card.id for card in seed_42_cards], [card.id for card in seed_43_cards])

    def test_seeded_variety_preserves_slot_roles(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(foundation.quest, ("forest", "hidden_path"))
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)

        # When
        cards = cards_from_pool(pool, _selection_context(foundation, state, 43))

        # Then
        self.assertEqual(("quest_progress", "risk_discovery", "resource_alternative"), tuple(card.slot_role for card in cards))

    def test_blocked_candidates_never_selected_by_seeded_variety(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        state.quest_progress["helped_injured_traveler"] = 1
        context = CardCandidateContext(foundation.quest, ("forest", "injured_traveler", "aid_opportunity"))
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)

        # When
        cards = cards_from_pool(pool, _selection_context(foundation, state, 43))

        # Then
        self.assertNotIn("help_injured_traveler", [card.id for card in cards])

    def test_previous_presented_card_gets_repeat_penalty(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = replace(_forest_state(foundation), recent_presented_card_ids=("inspect_tracks",))
        context = CardCandidateContext(foundation.quest, ("forest", "hidden_path"))

        # When
        candidate = _candidate(build_card_candidate_pool(foundation.card_rules.cards, state, context), "inspect_tracks")

        # Then
        self.assertLess(candidate.repeat_penalty, 0)

    def test_fallback_prefers_active_quest_candidate_over_off_quest_noise(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = _selection_context(foundation, state, 42)
        relevant = _candidate_fixture("relevant_fallback", "quest_progress", 30, quest_ids=(foundation.quest.id,))
        off_quest = _candidate_fixture("off_quest_noise", "quest_progress", 90)
        first_slot = _candidate_fixture("first_slot", "quest_progress", 120, quest_ids=(foundation.quest.id,))

        # When
        selection = select_cards_from_pool((first_slot, off_quest, relevant), context)

        # Then
        self.assertEqual(["first_slot", "relevant_fallback", "off_quest_noise"], [card.id for card in selection.cards])
        selected = {candidate.card.id: candidate.selected_by for candidate in selection.candidate_pool}
        self.assertEqual("fallback_pick", selected["relevant_fallback"])

def _forest_state(foundation: Foundation) -> RunState:
    scenario = Scenario(
        id="unit_candidate_pool",
        name="Unit Candidate Pool",
        content_sources=(),
        include_regions=("forest",),
        include_event_ids=(),
        include_event_tags=(),
        exclude_event_ids=(),
        exclude_event_tags=(),
        initial_status={"health": 7, "food": 5, "money": 2, "reputation": 0, "curse": 1},
        initial_items=("torch",),
        target_turns=1,
        seed=42,
        gameplay_mode="p0_foundation",
        active_quest_id="herb_gathering_tutorial",
    )
    state = replace(initial_state(scenario, foundation.quest), region="forest")
    state.quest_progress["herbs_collected"] = 2
    return state


def _candidate(pool: tuple[CardCandidate, ...], card_id: str) -> CardCandidate:
    for candidate in pool:
        if candidate.card.id == card_id:
            return candidate
    raise AssertionError(f"missing candidate: {card_id}")


def _candidate_score(pool: tuple[CardCandidate, ...], card_id: str) -> int:
    return _candidate(pool, card_id).score


def _selection_context(foundation: Foundation, state: RunState, seed: int) -> CardSelectionContext:
    return CardSelectionContext(
        scenario_id="unit_candidate_pool",
        seed=seed,
        run_number=1,
        active_quest_id=foundation.quest.id,
        day=state.clock.day,
        turn=state.clock.turn,
        current_region=state.region,
    )


def _candidate_fixture(card_id: str, slot_role: str, score: int, quest_ids: tuple[str, ...] = ()) -> CardCandidate:
    card = CardRule(
        id=card_id,
        title=card_id,
        description=card_id,
        slot_role=slot_role,
        base_weight=score,
        tier_hint="normal",
        tags=(),
        regions=("forest",),
        result={},
        requires_item=None,
        requires_progress={},
        requires_status={},
        applies_to_storylet_tags=(),
        applies_to_quest_objectives=(),
        progress_key="",
        weight_modifiers={},
        quest_ids=quest_ids,
    )
    return CardCandidate(card=card, score=score, tier="normal", matched_tags=(), matched_objectives=(), blocked_reason="")
