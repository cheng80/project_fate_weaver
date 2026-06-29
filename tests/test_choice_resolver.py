from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.choice_resolver import build_choices_seen, select_available_choice
from fateweaver.data_loader import load_project_data
from fateweaver.models import Choice, Event, StatusRequirement


class ChoiceResolverTests(unittest.TestCase):
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
