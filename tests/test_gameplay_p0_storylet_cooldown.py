from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from fateweaver.data_loader import load_project_data
from fateweaver.gameplay_p0_cards import build_card_candidate_pool, cards_from_pool
from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.gameplay_p0_models import (
    CardCandidate,
    CardCandidateContext,
    CardSelectionContext,
    CooldownCounter,
    Foundation,
    RepeatMemory,
    RunState,
)
from fateweaver.gameplay_p0_rules import initial_state
from fateweaver.models import Scenario


class GameplayP0StoryletCooldownTests(unittest.TestCase):
    def test_storylet_hints_add_candidate_bonus(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        plain_context = CardCandidateContext(foundation.quest, ("forest",))
        hint_context = CardCandidateContext(
            foundation.quest,
            ("forest",),
            storylet_id="forest_injured_traveler_hint",
            card_candidate_hints=("help_injured_traveler",),
        )

        # When
        plain = _candidate_score(build_card_candidate_pool(foundation.card_rules.cards, state, plain_context), "help_injured_traveler")
        hinted = _candidate(build_card_candidate_pool(foundation.card_rules.cards, state, hint_context), "help_injured_traveler")

        # Then
        self.assertGreater(hinted.score, plain)
        self.assertIn("help_injured_traveler", hinted.matched_storylet_hints)

    def test_storylet_hint_card_can_enter_three_card(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        context = CardCandidateContext(
            foundation.quest,
            ("forest",),
            storylet_id="forest_injured_traveler_hint",
            card_candidate_hints=("help_injured_traveler",),
        )

        # When
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        cards = cards_from_pool(pool, _selection_context(foundation, state, 42))

        # Then
        self.assertIn("help_injured_traveler", [card.id for card in cards])

    def test_storylet_hint_does_not_bypass_blocked(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        state = _forest_state(foundation)
        state.quest_progress["helped_injured_traveler"] = 1
        context = CardCandidateContext(
            foundation.quest,
            ("forest", "injured_traveler"),
            storylet_id="forest_injured_traveler_hint",
            card_candidate_hints=("help_injured_traveler",),
        )

        # When
        pool = build_card_candidate_pool(foundation.card_rules.cards, state, context)
        cards = cards_from_pool(pool, _selection_context(foundation, state, 42))

        # Then
        self.assertEqual("blocked", _candidate(pool, "help_injured_traveler").tier)
        self.assertNotIn("help_injured_traveler", [card.id for card in cards])

    def test_repeat_group_applies_cooldown_penalty(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        memory = RepeatMemory(repeat_groups=(CooldownCounter("forest_npc_aid", 2),))
        state = replace(_forest_state(foundation), repeat_memory=memory)
        context = CardCandidateContext(
            foundation.quest,
            ("forest", "injured_traveler"),
            storylet_id="forest_injured_traveler_hint",
            card_candidate_hints=("help_injured_traveler",),
            cooldown_tags=("npc_aid",),
            repeat_group="forest_npc_aid",
        )

        # When
        candidate = _candidate(build_card_candidate_pool(foundation.card_rules.cards, state, context), "help_injured_traveler")

        # Then
        self.assertLess(candidate.cooldown_penalty, 0)

    def test_event_loader_reads_storylet_hint_fields(self) -> None:
        # Given
        scenario_path = Path("data/scenarios/tutorial_herb_quest.yaml")

        # When
        bundle = load_project_data(Path("."), scenario_path).bundle
        event = bundle.events_by_id["forest_injured_traveler_hint"]

        # Then
        self.assertIn("help_injured_traveler", event.card_candidate_hints)
        self.assertEqual("forest_npc_aid", event.repeat_group)

    def test_repeat_memory_snapshot_logged(self) -> None:
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
        first_turn = payload["turns"][0]
        self.assertIn("repeat_memory_snapshot", first_turn)
        self.assertIn("card_candidate_hints", first_turn)
        self.assertIn("cooldown_penalty", first_turn["card_candidate_pool"][0])


def _forest_state(foundation: Foundation) -> RunState:
    scenario = Scenario(
        id="unit_storylet_cooldown",
        name="Unit Storylet Cooldown",
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
        scenario_id="unit_storylet_cooldown",
        seed=seed,
        run_number=1,
        active_quest_id=foundation.quest.id,
        day=state.clock.day,
        turn=state.clock.turn,
        current_region=state.region,
    )
