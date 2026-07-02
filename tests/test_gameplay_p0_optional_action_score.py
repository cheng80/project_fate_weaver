from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import yaml

from fateweaver.card_candidates import present_cards
from fateweaver.gameplay_setup import load_foundation
from fateweaver.gameplay_models import CardCandidateContext
from fateweaver.gameplay_rules import initial_state
from fateweaver.models import Scenario


class GameplayP0OptionalActionScoreTests(unittest.TestCase):
    def test_optional_action_card_uses_card_rules(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        help_card = next(card for card in foundation.card_rules.cards if card.id == "help_injured_traveler")

        # When
        storylet_tags = help_card.applies_to_storylet_tags
        objective_ids = help_card.applies_to_quest_objectives

        # Then
        self.assertIn("injured_traveler", storylet_tags)
        self.assertIn("aid_opportunity", storylet_tags)
        self.assertIn("help_injured_traveler", objective_ids)
        self.assertEqual("helped_injured_traveler", help_card.progress_key)

    def test_optional_action_card_generated_from_storylet_tags(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        scenario = Scenario(
            id="unit_optional_storylet_tags",
            name="Unit Optional Storylet Tags",
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

        # When
        context = CardCandidateContext(foundation.quest, ("forest", "npc", "aid_opportunity", "injured_traveler", "quest_related"))
        cards = present_cards(foundation.card_rules.cards, state, context)

        # Then
        presented_ids = [card.id for card in cards]
        self.assertEqual(3, len(presented_ids))
        self.assertIn("help_injured_traveler", presented_ids)
        self.assertEqual("resource_alternative", cards[2].slot_role)

    def test_optional_action_card_not_repeated_after_progress_completed(self) -> None:
        # Given
        foundation = load_foundation(Path("."), "herb_gathering_tutorial")
        scenario = Scenario(
            id="unit_optional_storylet_tags_completed",
            name="Unit Optional Storylet Tags Completed",
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
        state.quest_progress["helped_injured_traveler"] = 1

        # When
        context = CardCandidateContext(foundation.quest, ("forest", "npc", "aid_opportunity", "injured_traveler", "quest_related"))
        cards = present_cards(foundation.card_rules.cards, state, context)

        # Then
        self.assertNotEqual("help_injured_traveler", cards[2].id)

    def test_optional_action_completed_when_help_card_selected(self) -> None:
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
            text_logs = list(Path(tmp).glob("run_*.txt"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
            text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        presented = _presented_card_ids(payload)
        selected = _selected_card_ids(payload)
        self.assertIn("help_injured_traveler", presented)
        self.assertIn("help_injured_traveler", selected)
        self.assertEqual(1, _max_quest_progress(payload, "helped_injured_traveler"))
        optional = _objective(payload["quest_report"], "help_injured_traveler")
        self.assertEqual("optional_action", optional["objective_type"])
        self.assertEqual("completed", optional["status"])
        self.assertGreater(int(optional["score_delta"]), 0)
        self.assertIn("help_injured_traveler", text_log)
        self.assertIn("성공", text_log)

    def test_optional_action_failed_when_not_selected(self) -> None:
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            # When
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/console_simulator.py",
                    "--scenario",
                    "data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml",
                    "--seed",
                    "42",
                    "--runs",
                    "1",
                    "--logs",
                    tmp,
                    "--profile",
                    "balanced",
                ],
                check=False,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=15,
            )
            json_logs = list(Path(tmp).glob("run_*.json"))
            text_logs = list(Path(tmp).glob("run_*.txt"))
            payload = json.loads(json_logs[0].read_text(encoding="utf-8")) if json_logs else {}
            text_log = text_logs[0].read_text(encoding="utf-8") if text_logs else ""

        # Then
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("help_injured_traveler", _selected_card_ids(payload))
        optional = _objective(payload["quest_report"], "help_injured_traveler")
        self.assertEqual("failed", optional["status"])
        self.assertIn("help_injured_traveler", text_log)
        self.assertIn("실패", text_log)

    def test_objective_score_uses_score_rules_yaml(self) -> None:
        # Given
        raw = yaml.safe_load(Path("data/core/score_rules.yaml").read_text(encoding="utf-8"))
        objective_scoring = raw["score_rules"]["objective_scoring"]

        # When
        with tempfile.TemporaryDirectory() as tmp:
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
        optional = _objective(payload["quest_report"], "help_injured_traveler")
        expected_optional_score = int(objective_scoring["completed_optional"])
        self.assertEqual(expected_optional_score, optional["score_delta"])
        self.assertGreaterEqual(payload["quest_report"]["score_breakdown"]["objective_completion"], expected_optional_score)


def _objective(report: dict, objective_id: str) -> dict:
    for objective in report["objective_results"]:
        if objective["objective_id"] == objective_id:
            return objective
    raise AssertionError(f"missing objective result: {objective_id}")


def _presented_card_ids(payload: dict) -> list[str]:
    ids: list[str] = []
    for turn in payload["turns"]:
        ids.extend(str(card["card_id"]) for card in turn["presented_cards"])
    return ids


def _selected_card_ids(payload: dict) -> list[str]:
    ids: list[str] = []
    for turn in payload["turns"]:
        ids.extend(str(card_id) for card_id in turn["selected_cards"])
    return ids


def _max_quest_progress(payload: dict, key: str) -> int:
    values = [int(turn["quest_progress"].get(key, 0)) for turn in payload["turns"]]
    return max(values) if values else 0
