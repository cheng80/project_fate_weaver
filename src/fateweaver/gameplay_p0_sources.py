from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fateweaver.models import JsonMap
from fateweaver.yaml_utils import as_mapping, list_at, read_mapping, string_tuple


@dataclass(frozen=True, slots=True)
class DuplicateQuestIdError(ValueError):
    quest_id: str
    first_source: Path
    duplicate_source: Path

    def __str__(self) -> str:
        return f"Duplicate quest id {self.quest_id}: {self.first_source} and {self.duplicate_source}"


@dataclass(frozen=True, slots=True)
class DuplicateCardRuleIdError(ValueError):
    card_id: str
    first_source: Path
    duplicate_source: Path

    def __str__(self) -> str:
        return f"Duplicate card rule id {self.card_id}: {self.first_source} and {self.duplicate_source}"


@dataclass(frozen=True, slots=True)
class SplitCardRuleQuestIdsError(ValueError):
    card_id: str
    source: Path

    def __str__(self) -> str:
        return f"Split card rule requires quest_ids: {self.card_id} in {self.source}"


def load_quest_mapping(root: Path) -> JsonMap:
    core_path = root / "data/content/base/quests.yaml"
    raw = read_mapping(core_path)
    quests = list(list_at(raw, "quests"))
    quest_sources: dict[str, Path] = {}
    for quest_value in quests:
        quest = as_mapping(quest_value)
        quest_id = str(quest["id"])
        if quest_id in quest_sources:
            raise DuplicateQuestIdError(quest_id, quest_sources[quest_id], core_path)
        quest_sources[quest_id] = core_path

    split_dir = root / "data/content/quests"
    if not split_dir.exists():
        return raw

    for split_path in sorted(split_dir.glob("*.yaml")):
        split_raw = read_mapping(split_path)
        for quest_value in list_at(split_raw, "quests"):
            quest = as_mapping(quest_value)
            quest_id = str(quest["id"])
            if quest_id in quest_sources:
                raise DuplicateQuestIdError(quest_id, quest_sources[quest_id], split_path)
            quest_sources[quest_id] = split_path
            quests.append(quest_value)

    merged = dict(raw)
    merged["quests"] = quests
    return merged


def load_card_rule_mapping(root: Path) -> JsonMap:
    core_path = root / "data/core/card_rules.yaml"
    raw = read_mapping(core_path)
    cards = list(list_at(raw, "p0_cards"))
    card_sources: dict[str, Path] = {}
    for card_value in cards:
        card = as_mapping(card_value)
        card_id = str(card["id"])
        if card_id in card_sources:
            raise DuplicateCardRuleIdError(card_id, card_sources[card_id], core_path)
        card_sources[card_id] = core_path

    split_dir = root / "data/content/card_rules"
    if not split_dir.exists():
        return raw

    for split_path in sorted(split_dir.glob("*.yaml")):
        split_raw = read_mapping(split_path)
        for card_value in list_at(split_raw, "p0_cards"):
            card = as_mapping(card_value)
            card_id = str(card["id"])
            if not string_tuple(card.get("quest_ids", []), strict=True):
                raise SplitCardRuleQuestIdsError(card_id, split_path)
            if card_id in card_sources:
                raise DuplicateCardRuleIdError(card_id, card_sources[card_id], split_path)
            card_sources[card_id] = split_path
            cards.append(card_value)

    merged = dict(raw)
    merged["p0_cards"] = cards
    return merged
