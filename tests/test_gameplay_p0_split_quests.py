from __future__ import annotations

import shutil
import unittest
from pathlib import Path

import yaml

from fateweaver.gameplay_setup import load_foundation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SPLIT_QUEST_FILES = {
    "defense_threat.yaml",
    "foundation.yaml",
    "investigation_mystery.yaml",
    "local_problem.yaml",
    "ruin_dungeon_ritual.yaml",
    "survival_exploration.yaml",
    "travel_delivery_escort.yaml",
}


class GameplayP0SplitQuestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = PROJECT_ROOT / f".omo/ulw-loop/tmp/split-quests-test-{self._testMethodName}"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        shutil.copytree(PROJECT_ROOT / "data", self.tmp / "data")

    def tearDown(self) -> None:
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def test_loader_reads_split_quest_when_removed_from_base(self) -> None:
        quest = _remove_base_quest(self.tmp, "herb_gathering_tutorial")
        _write_split_quests(self.tmp, "foundation.yaml", [quest])

        foundation = load_foundation(self.tmp, "herb_gathering_tutorial")

        self.assertEqual("herb_gathering_tutorial", foundation.quest.id)
        self.assertEqual("약초 채집 의뢰", foundation.quest.title)

    def test_duplicate_quest_id_raises_clear_error(self) -> None:
        duplicate = _base_quest(self.tmp, "herb_gathering_tutorial")
        _write_split_quests(self.tmp, "local_problem.yaml", [duplicate])

        with self.assertRaisesRegex(ValueError, "Duplicate quest id.*herb_gathering_tutorial.*quests.yaml.*local_problem.yaml"):
            load_foundation(self.tmp, "herb_gathering_tutorial")

    def test_loader_reads_all_category_quest_splits(self) -> None:
        foundation = load_foundation(PROJECT_ROOT, "hidden_grove_discovery")

        self.assertEqual(EXPECTED_SPLIT_QUEST_FILES, {path.name for path in _split_quest_paths(PROJECT_ROOT)})
        self.assertEqual("hidden_grove_discovery", foundation.quest.id)

    def test_no_duplicate_quest_ids_after_category_migration(self) -> None:
        quest_ids = [quest["id"] for quest in _all_raw_quests(PROJECT_ROOT)]

        self.assertEqual(len(quest_ids), len(set(quest_ids)))


def _base_quest(root: Path, quest_id: str) -> dict[str, object]:
    for quest in _base_quests(root):
        if quest["id"] == quest_id:
            return quest
    raise AssertionError(f"missing quest fixture: {quest_id}")


def _remove_base_quest(root: Path, quest_id: str) -> dict[str, object]:
    path = root / "data/content/base/quests.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    quests = list(raw["quests"])
    target = next(quest for quest in quests if quest["id"] == quest_id)
    raw["quests"] = [quest for quest in quests if quest["id"] != quest_id]
    path.write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return target


def _write_split_quests(root: Path, filename: str, quests: list[dict[str, object]]) -> None:
    split_dir = root / "data/content/quests"
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / filename).write_text(yaml.safe_dump({"quests": quests}, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _base_quests(root: Path) -> list[dict[str, object]]:
    raw = yaml.safe_load((root / "data/content/base/quests.yaml").read_text(encoding="utf-8"))
    return list(raw["quests"])


def _split_quest_paths(root: Path) -> list[Path]:
    return sorted((root / "data/content/quests").glob("*.yaml"))


def _all_raw_quests(root: Path) -> list[dict[str, object]]:
    quests = _base_quests(root)
    for path in _split_quest_paths(root):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        quests.extend(raw["quests"])
    return quests


if __name__ == "__main__":
    unittest.main()
