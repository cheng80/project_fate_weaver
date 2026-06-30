from __future__ import annotations

import shutil
import unittest
from pathlib import Path

import yaml

from fateweaver.data_loader import load_project_data
from fateweaver.models import JsonMap


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SPLIT_EVENT_FILES = {
    "defense_threat.yaml",
    "foundation.yaml",
    "investigation_mystery.yaml",
    "local_problem.yaml",
    "ruin_dungeon_ritual.yaml",
    "survival_exploration.yaml",
    "travel_delivery_escort.yaml",
}


class GameplayP0SplitEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = PROJECT_ROOT / f".omo/ulw-loop/tmp/split-events-test-{self._testMethodName}"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        shutil.copytree(PROJECT_ROOT / "data", self.tmp / "data")

    def tearDown(self) -> None:
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def test_loader_reads_base_events(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/village_well_trouble_success.yaml")

        loaded_events = {event.id: event for event in loaded.bundle.events}

        self.assertIn("village_market", loaded_events)
        self.assertEqual(Path("data/content/base/events.yaml"), loaded_events["village_market"].source_path)

    def test_loader_reads_split_events_when_removed_from_base(self) -> None:
        event = _remove_base_event(self.tmp, "village_sick_well_hint")
        _write_split_events(self.tmp, "local_problem.yaml", [event])

        loaded = load_project_data(self.tmp, self.tmp / "data/scenarios/village_well_trouble_success.yaml")
        loaded_events = {event.id: event for event in loaded.bundle.events}

        self.assertIn("village_sick_well_hint", loaded_events)
        self.assertIn("village_market", loaded_events)
        self.assertEqual(Path("data/content/events/local_problem.yaml"), loaded_events["village_sick_well_hint"].source_path)

    def test_duplicate_event_id_raises_clear_error(self) -> None:
        duplicate = _base_event(self.tmp, "village_market")
        _write_split_events(self.tmp, "local_problem.yaml", [duplicate])

        with self.assertRaisesRegex(ValueError, "Duplicate event id.*village_market.*base/events.yaml.*events/local_problem.yaml"):
            load_project_data(self.tmp, self.tmp / "data/scenarios/village_well_trouble_success.yaml")

    def test_loader_reads_all_category_event_splits(self) -> None:
        loaded = load_project_data(PROJECT_ROOT, PROJECT_ROOT / "data/scenarios/hidden_grove_discovery.yaml")

        self.assertEqual(EXPECTED_SPLIT_EVENT_FILES, {path.name for path in _split_event_paths(PROJECT_ROOT)})
        self.assertIn("hidden_grove_hint", {event.id for event in loaded.bundle.events})

    def test_no_duplicate_event_ids_after_category_migration(self) -> None:
        event_ids = [event["id"] for event in _all_raw_events(PROJECT_ROOT)]

        self.assertEqual(len(event_ids), len(set(event_ids)))

    def test_split_event_quest_ids_resolve_against_loaded_quests(self) -> None:
        quest_ids = {quest["id"] for quest in _all_raw_quests(PROJECT_ROOT)}

        unknown_quest_ids = {
            quest_id
            for event in _all_split_events(PROJECT_ROOT)
            for quest_id in event.get("quest_ids", [])
            if quest_id not in quest_ids
        }

        self.assertEqual(set(), unknown_quest_ids)

    def test_split_event_card_candidate_hints_resolve_against_loaded_cards(self) -> None:
        card_ids = {card["id"] for card in _all_raw_cards(PROJECT_ROOT)}

        unknown_card_ids = {
            card_id
            for event in _all_split_events(PROJECT_ROOT)
            for card_id in event.get("card_candidate_hints", [])
            if card_id not in card_ids
        }

        self.assertEqual(set(), unknown_card_ids)


def _base_event(root: Path, event_id: str) -> JsonMap:
    for event in _base_events(root):
        if event["id"] == event_id:
            return event
    raise AssertionError(f"missing event fixture: {event_id}")


def _remove_base_event(root: Path, event_id: str) -> JsonMap:
    path = root / "data/content/base/events.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    events = list(raw["events"])
    target = next(event for event in events if event["id"] == event_id)
    raw["events"] = [event for event in events if event["id"] != event_id]
    path.write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return target


def _write_split_events(root: Path, filename: str, events: list[JsonMap]) -> None:
    split_dir = root / "data/content/events"
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / filename).write_text(yaml.safe_dump({"events": events}, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _base_events(root: Path) -> list[JsonMap]:
    raw = yaml.safe_load((root / "data/content/base/events.yaml").read_text(encoding="utf-8"))
    return list(raw["events"])


def _split_event_paths(root: Path) -> list[Path]:
    return sorted((root / "data/content/events").glob("*.yaml"))


def _all_split_events(root: Path) -> list[JsonMap]:
    events: list[JsonMap] = []
    for path in _split_event_paths(root):
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        events.extend(raw.get("events", []))
    return events


def _all_raw_events(root: Path) -> list[JsonMap]:
    return _base_events(root) + _all_split_events(root)


def _all_raw_quests(root: Path) -> list[JsonMap]:
    quests = _raw_list(root / "data/content/base/quests.yaml", "quests")
    for path in sorted((root / "data/content/quests").glob("*.yaml")):
        quests.extend(_raw_list(path, "quests"))
    return quests


def _all_raw_cards(root: Path) -> list[JsonMap]:
    cards = _raw_list(root / "data/core/card_rules.yaml", "p0_cards")
    for path in sorted((root / "data/content/card_rules").glob("*.yaml")):
        cards.extend(_raw_list(path, "p0_cards"))
    return cards


def _raw_list(path: Path, key: str) -> list[JsonMap]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return list(raw.get(key, []))


if __name__ == "__main__":
    unittest.main()
