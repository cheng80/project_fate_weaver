from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from fateweaver.models import JsonMap, JsonValue


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


@dataclass(frozen=True, slots=True)
class GameplayP0SourceTypeError(TypeError):
    label: str
    expected: str

    def __str__(self) -> str:
        return f"{self.label} must be {self.expected}"


def load_quest_mapping(root: Path) -> JsonMap:
    core_path = root / "data/content/base/quests.yaml"
    raw = _read_mapping(core_path)
    quests = list(_list_at(raw, "quests"))
    quest_sources: dict[str, Path] = {}
    for quest_value in quests:
        quest = _as_mapping(quest_value)
        quest_id = str(quest["id"])
        if quest_id in quest_sources:
            raise DuplicateQuestIdError(quest_id, quest_sources[quest_id], core_path)
        quest_sources[quest_id] = core_path

    split_dir = root / "data/content/quests"
    if not split_dir.exists():
        return raw

    for split_path in sorted(split_dir.glob("*.yaml")):
        split_raw = _read_mapping(split_path)
        for quest_value in _list_at(split_raw, "quests"):
            quest = _as_mapping(quest_value)
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
    raw = _read_mapping(core_path)
    cards = list(_list_at(raw, "p0_cards"))
    card_sources: dict[str, Path] = {}
    for card_value in cards:
        card = _as_mapping(card_value)
        card_id = str(card["id"])
        if card_id in card_sources:
            raise DuplicateCardRuleIdError(card_id, card_sources[card_id], core_path)
        card_sources[card_id] = core_path

    split_dir = root / "data/content/card_rules"
    if not split_dir.exists():
        return raw

    for split_path in sorted(split_dir.glob("*.yaml")):
        split_raw = _read_mapping(split_path)
        for card_value in _list_at(split_raw, "p0_cards"):
            card = _as_mapping(card_value)
            card_id = str(card["id"])
            if not _string_tuple(card.get("quest_ids", [])):
                raise SplitCardRuleQuestIdsError(card_id, split_path)
            if card_id in card_sources:
                raise DuplicateCardRuleIdError(card_id, card_sources[card_id], split_path)
            card_sources[card_id] = split_path
            cards.append(card_value)

    merged = dict(raw)
    merged["p0_cards"] = cards
    return merged


def _read_mapping(path: Path) -> JsonMap:
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    return _as_mapping(loaded)


def _list_at(raw: JsonMap, key: str) -> tuple[JsonValue, ...]:
    value = raw.get(key, [])
    if not isinstance(value, list):
        raise GameplayP0SourceTypeError(key, "a list")
    return tuple(value)


def _as_mapping(value: JsonValue) -> JsonMap:
    if not isinstance(value, dict):
        raise GameplayP0SourceTypeError("value", "a mapping")
    return {str(key): item for key, item in value.items()}


def _string_tuple(value: JsonValue) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise GameplayP0SourceTypeError("value", "a list")
    return tuple(str(item) for item in value)
