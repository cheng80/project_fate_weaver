from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from fateweaver.gameplay_p0_cards import build_card_candidate_pool, present_cards
from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.gameplay_p0_models import CardCandidate, CardCandidateContext, Foundation, RunState
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
        expected_keys = {"card_id", "slot_role", "score", "tier", "matched_tags", "matched_objectives", "blocked_reason"}
        self.assertTrue(expected_keys <= set(pool[0]))


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
