from __future__ import annotations

import unittest
from pathlib import Path

from fateweaver.data_loader import load_project_data
from fateweaver.models import Scenario
from fateweaver.scenario_filter import filter_events_for_scenario


class ScenarioFilterTests(unittest.TestCase):
    def test_id_and_tag_filters_use_and(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))
        scenario = Scenario(
            id="test",
            name="test",
            content_sources=(),
            include_regions=("forest", "ruin"),
            include_event_ids=("cursed_well", "broken_bridge"),
            include_event_tags=("curse",),
            exclude_event_ids=(),
            exclude_event_tags=(),
            initial_status={},
            initial_items=(),
            target_turns=1,
            seed=1,
        )

        events = filter_events_for_scenario(loaded.bundle.events, scenario)

        self.assertEqual(["cursed_well"], [event["id"] for event in events])

    def test_empty_include_ids_and_tags_uses_region_pool(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))
        scenario = Scenario(
            id="test",
            name="test",
            content_sources=(),
            include_regions=("village",),
            include_event_ids=(),
            include_event_tags=(),
            exclude_event_ids=(),
            exclude_event_tags=(),
            initial_status={},
            initial_items=(),
            target_turns=1,
            seed=1,
        )

        events = filter_events_for_scenario(loaded.bundle.events, scenario)

        self.assertIn("village_market", [event.id for event in events])

    def test_excludes_apply_after_includes(self) -> None:
        loaded = load_project_data(Path("."), Path("data/scenarios/mvp0_console_test.yaml"))
        scenario = Scenario(
            id="test",
            name="test",
            content_sources=(),
            include_regions=("forest",),
            include_event_ids=(),
            include_event_tags=("combat",),
            exclude_event_ids=("wolf_pack",),
            exclude_event_tags=(),
            initial_status={},
            initial_items=(),
            target_turns=1,
            seed=1,
        )

        events = filter_events_for_scenario(loaded.bundle.events, scenario)

        self.assertNotIn("wolf_pack", [event.id for event in events])


if __name__ == "__main__":
    unittest.main()
