from __future__ import annotations

import shutil
import unittest
from pathlib import Path

from fateweaver.gameplay_p0_data import load_foundation


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GameplayP0SplitCardRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = PROJECT_ROOT / ".omo/ulw-loop/tmp/split-card-rules-test"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        shutil.copytree(PROJECT_ROOT / "data", self.tmp / "data")

    def tearDown(self) -> None:
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def test_loader_reads_core_card_rules(self) -> None:
        foundation = load_foundation(self.tmp, "herb_gathering_tutorial")

        self.assertIn("search_herbs", {card.id for card in foundation.card_rules.cards})

    def test_loader_reads_split_card_rules(self) -> None:
        _write_split_card(
            self.tmp,
            """
p0_cards:
  - id: split_local_problem_probe
    title: Split Local Probe
    description: Split card loaded from category file.
    slot_role: quest_progress
    base_weight: 95
    tier_hint: story
    tags: [local_problem]
    regions: [village]
    quest_ids: [village_well_trouble]
    applies_to_storylet_tags: [quest_related]
    applies_to_quest_objectives: [inspect_well]
    progress_key: inspect_well
    result:
      quest_progress: {inspect_well: 1}
""",
        )

        foundation = load_foundation(self.tmp, "village_well_trouble")

        self.assertIn("split_local_problem_probe", {card.id for card in foundation.card_rules.cards})

    def test_loader_merges_core_and_split_card_rules(self) -> None:
        _write_split_card(
            self.tmp,
            """
p0_cards:
  - id: split_local_problem_probe
    title: Split Local Probe
    description: Split card loaded from category file.
    slot_role: quest_progress
    base_weight: 95
    tier_hint: story
    tags: [local_problem]
    regions: [village]
    quest_ids: [village_well_trouble]
    applies_to_storylet_tags: [quest_related]
    applies_to_quest_objectives: [inspect_well]
    progress_key: inspect_well
    result:
      quest_progress: {inspect_well: 1}
""",
        )

        foundation = load_foundation(self.tmp, "village_well_trouble")
        card_ids = {card.id for card in foundation.card_rules.cards}

        self.assertIn("search_herbs", card_ids)
        self.assertIn("split_local_problem_probe", card_ids)

    def test_duplicate_card_id_raises_clear_error(self) -> None:
        _write_split_card(
            self.tmp,
            """
p0_cards:
  - id: search_herbs
    title: Duplicate Search Herbs
    description: Duplicate id for negative test.
    slot_role: quest_progress
    quest_ids: [village_well_trouble]
    result:
      quest_progress: {inspect_well: 1}
""",
        )

        with self.assertRaisesRegex(ValueError, "Duplicate card rule id.*search_herbs.*card_rules.yaml.*local_problem.yaml"):
            load_foundation(self.tmp, "village_well_trouble")

    def test_split_card_rules_require_quest_ids(self) -> None:
        _write_split_card(
            self.tmp,
            """
p0_cards:
  - id: missing_split_quest_ids
    title: Missing Quest Ids
    description: Split cards must be scoped.
    slot_role: quest_progress
    result:
      quest_progress: {inspect_well: 1}
""",
        )

        with self.assertRaisesRegex(ValueError, "Split card rule requires quest_ids.*missing_split_quest_ids.*local_problem.yaml"):
            load_foundation(self.tmp, "village_well_trouble")


def _write_split_card(root: Path, content: str) -> None:
    split_dir = root / "data/content/card_rules"
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / "local_problem.yaml").write_text(content.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
