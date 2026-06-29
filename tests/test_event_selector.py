from __future__ import annotations

import unittest
from pathlib import Path
from random import Random

from fateweaver.data_loader import load_project_data
from fateweaver.event_selector import select_event
from fateweaver.scenario_filter import filter_events_for_scenario


class EventSelectorTests(unittest.TestCase):
    def test_seeded_selection_is_repeatable(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))
        events = filter_events_for_scenario(loaded.bundle.events, loaded.scenario)

        first = select_event(events, loaded.scenario.initial_status, loaded.scenario.initial_items, {}, 1, Random(42))
        second = select_event(events, loaded.scenario.initial_status, loaded.scenario.initial_items, {}, 1, Random(42))

        self.assertEqual(first["id"], second["id"])

    def test_combat_is_selected_as_ordinary_tagged_event(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))
        events = tuple(event for event in loaded.bundle.events if "combat" in event.event_tags)

        selected = select_event(events, loaded.scenario.initial_status, loaded.scenario.initial_items, (), Random(1), ())

        self.assertIn("combat", selected.event_tags)


if __name__ == "__main__":
    unittest.main()
