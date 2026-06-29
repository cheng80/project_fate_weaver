from __future__ import annotations

import unittest

from fateweaver.choice_scoring import select_weighted_choice
from fateweaver.models import ChoiceSeen


class ChoiceScoringTests(unittest.TestCase):
    def test_repeated_item_choice_loses_bonus_against_viable_choice(self) -> None:
        choices = (
            ChoiceSeen("blow_signal_whistle", "item_based", True, None, False, "low", ("item:signal_whistle",), {"message": "tool"}),
            ChoiceSeen("mark_trail", "safe", True, None, False, "low", (), {"status": {"food": -1}, "message": "mark"}),
        )

        selection = select_weighted_choice(
            choices,
            profile="balanced",
            state={"health": 7, "food": 5},
            seed=42,
            turn=4,
            selected_choice_history=("blow_signal_whistle", "blow_signal_whistle", "blow_signal_whistle"),
        )

        self.assertEqual("mark_trail", selection.choice.choice_id)
        item_score = next(score for score in selection.choice_scores if score["choice_id"] == "blow_signal_whistle")
        self.assertLess(float(item_score["item_usage_score"]), 4.0)

    def test_repeated_item_dampening_does_not_select_unavailable_choice(self) -> None:
        choices = (
            ChoiceSeen("blow_signal_whistle", "item_based", True, None, False, "low", ("item:signal_whistle",), {"message": "tool"}),
            ChoiceSeen("sealed_cache", "item_based", False, "missing item", False, "low", ("item:sealed_key",), {"message": "locked"}),
        )

        selection = select_weighted_choice(
            choices,
            profile="balanced",
            state={},
            seed=42,
            turn=1,
            selected_choice_history=("blow_signal_whistle", "blow_signal_whistle", "blow_signal_whistle"),
        )

        self.assertEqual("blow_signal_whistle", selection.choice.choice_id)
        self.assertTrue(selection.choice.available)

    def test_reason_includes_runner_up_gap_and_top_factors(self) -> None:
        choices = (
            ChoiceSeen("safe_exit", "safe", True, None, False, "low", (), {"message": "safe"}),
            ChoiceSeen("paid_route", "trade", True, None, False, "medium", (), {"status": {"money": +2}, "message": "reward"}),
        )

        selection = select_weighted_choice(choices, profile="greedy_leaning", state={}, seed=7, turn=2)

        self.assertIn("profile=greedy_leaning", selection.reason)
        self.assertIn("selected_score=", selection.reason)
        self.assertIn("runner_up=", selection.reason)
        self.assertIn("runner_up_score=", selection.reason)
        self.assertIn("score_gap=", selection.reason)
        self.assertIn("top_factors=", selection.reason)


if __name__ == "__main__":
    unittest.main()
