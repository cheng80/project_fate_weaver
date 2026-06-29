from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.choice_resolver import build_choices_seen, select_available_choice, select_choice
from fateweaver.data_loader import load_project_data
from fateweaver.models import Choice, Event, StatusRequirement


class ChoiceResolverTests(unittest.TestCase):
    def test_balanced_profile_uses_item_usage_score_for_item_gated_choice(self) -> None:
        # Given: a later available choice is gated by an item the player has.
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("wait", "wait", "safe", "none", {"message": "x"}, (), None, {}, None, False, True),
                Choice("use_rope", "use rope", "tool_use", "low", {"message": "x"}, (), "rope", {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )
        choices = build_choices_seen(event, {}, ("rope",), ())

        # When: balanced weighted scoring selects from visible choices.
        selection = select_choice(choices, profile="balanced", state={}, seed=42, turn=1)

        # Then: item usage is one weighted factor, not a hard-coded first choice.
        self.assertEqual("use_rope", selection.choice.choice_id)
        self.assertGreater(float(selection.selected_choice_score["item_usage_score"]), 0)
        self.assertIn("final_score", selection.reason)

    def test_desperate_profile_raises_survival_choice_when_resources_are_low(self) -> None:
        # Given: low health and food make survival recovery urgent.
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("grab_gold", "grab gold", "greedy", "high", {"status": {"money": +3, "health": -1}}, (), None, {}, None, False, True),
                Choice("eat_rations", "eat rations", "safe", "low", {"status": {"health": +2, "food": +1}}, (), None, {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )
        choices = build_choices_seen(event, {}, (), ())

        # When: desperate scoring sees low health and low food.
        selection = select_choice(choices, profile="desperate", state={"health": 2, "food": 1, "curse": 1}, seed=42, turn=1)

        # Then: survival recovery can beat pure reward.
        self.assertEqual("eat_rations", selection.choice.choice_id)
        self.assertGreater(float(selection.selected_choice_score["survival_need_score"]), 0)

    def test_greedy_profile_prefers_reward_when_tradeoff_is_available(self) -> None:
        # Given: a reward-heavy option competes with a safer low-reward option.
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("rest", "rest", "safe", "low", {"status": {"health": +1}}, (), None, {}, None, False, True),
                Choice("loot_cache", "loot cache", "greedy", "medium", {"status": {"money": +3}}, (), None, {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )
        choices = build_choices_seen(event, {}, (), ())

        # When: greedy scoring weighs reward more strongly.
        selection = select_choice(choices, profile="greedy_leaning", state={"health": 8, "food": 5}, seed=42, turn=1)

        # Then: reward can beat pure safety without bypassing scoring.
        self.assertEqual("loot_cache", selection.choice.choice_id)
        self.assertGreater(float(selection.selected_choice_score["reward_score"]), 0)

    def test_weighted_profile_does_not_select_unavailable_item_gated_choice(self) -> None:
        # Given: the preferred item-gated choice is visible but unavailable.
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("use_charm", "use charm", "tool_use", "low", {"message": "x"}, (), "lucky_charm", {}, None, False, True),
                Choice("safe_exit", "safe exit", "safe", "low", {"message": "x"}, (), None, {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )
        choices = build_choices_seen(event, {}, (), ())

        # When: weighted scoring would otherwise value item usage.
        selected = select_available_choice(choices, profile="balanced", state={}, seed=42, turn=1)

        # Then: unavailable choices remain ineligible for selection.
        self.assertFalse(choices[0].available)
        self.assertEqual("safe_exit", selected.choice_id)

    def test_seed_based_tie_break_is_deterministic(self) -> None:
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("left", "left", "safe", "low", {"message": "x"}, (), None, {}, None, False, True),
                Choice("right", "right", "safe", "low", {"message": "x"}, (), None, {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )
        choices = build_choices_seen(event, {}, (), ())

        first = select_choice(choices, profile="balanced", state={}, seed=99, turn=3)
        second = select_choice(choices, profile="balanced", state={}, seed=99, turn=3)

        self.assertEqual(first.choice.choice_id, second.choice.choice_id)
        self.assertEqual(first.selected_choice_score["tie_breaker"], second.selected_choice_score["tie_breaker"])

    def test_unavailable_choice_is_visible_and_not_selected(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))
        event = next(event for event in loaded.bundle.events if event["id"] == "cursed_well")

        choices = build_choices_seen(event, loaded.scenario.initial_status, ("rope", "torch"), ())
        purify = next(choice for choice in choices if choice.choice_id == "purify")
        selected = select_available_choice(choices)

        self.assertFalse(purify.available)
        self.assertEqual("requires item: holy_water", purify.unavailable_reason)
        self.assertNotEqual("purify", selected.choice_id)

    def test_status_and_run_tag_requirements_make_choice_unavailable(self) -> None:
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("locked", "locked", "status_based", "low", {"message": "x"}, (), None, {"reputation": StatusRequirement(minimum=1)}, "flag", False, True),
                Choice("open", "open", "safe", "none", {"message": "x"}, (), None, {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )

        choices = build_choices_seen(event, {"reputation": 0}, (), ())

        self.assertFalse(choices[0].available)
        self.assertEqual("requires reputation >= 1", choices[0].unavailable_reason)
        self.assertEqual("open", select_available_choice(choices).choice_id)

    def test_run_tag_requirement_is_checked_after_status_passes(self) -> None:
        event = Event(
            id="test_event",
            name="test",
            description="",
            source_path=Path("test.yaml"),
            region_tags=("forest",),
            event_tags=("exploration",),
            danger_tags=(),
            base_weight=1,
            choices=(
                Choice("tagged", "tagged", "status_based", "low", {"message": "x"}, (), None, {"reputation": StatusRequirement(minimum=1)}, "flag", False, True),
                Choice("open", "open", "safe", "none", {"message": "x"}, (), None, {}, None, False, True),
            ),
            max_occurrences_per_run=None,
            cooldown_turns=None,
            requires_item=None,
            requires_status={},
            requires_run_tag=None,
        )

        missing_tag = build_choices_seen(event, {"reputation": 1}, (), ())
        with_tag = build_choices_seen(event, {"reputation": 1}, (), ("flag",))

        self.assertFalse(missing_tag[0].available)
        self.assertEqual("requires run tag: flag", missing_tag[0].unavailable_reason)
        self.assertTrue(with_tag[0].available)
        self.assertEqual("tagged", select_available_choice(with_tag).choice_id)


if __name__ == "__main__":
    unittest.main()
