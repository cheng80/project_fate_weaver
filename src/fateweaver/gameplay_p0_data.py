from __future__ import annotations

from pathlib import Path

import yaml

from fateweaver.gameplay_p0_models import CardRule, CardRules, ComboRule, ConflictRule, Foundation, Quest
from fateweaver.models import JsonMap, JsonValue, ProjectData, Scenario


def load_foundation(root: Path, quest_id: str | None) -> Foundation:
    if quest_id is None:
        raise ValueError("P0 scenario requires active_quest_id")
    quests = _read_mapping(root / "data/content/base/quests.yaml")
    cards = _read_mapping(root / "data/core/card_rules.yaml")
    score_rules = _read_mapping(root / "data/core/score_rules.yaml")
    return Foundation(
        quest=_load_quest(quests, quest_id),
        card_rules=_load_card_rules(cards),
        score_rules=_mapping_at(score_rules, "score_rules"),
    )


def validate_gameplay_p0_setup(project_root: Path, scenario: Scenario, bundle: ProjectData) -> list[str]:
    if scenario.gameplay_mode != "p0_foundation":
        return []
    errors: list[str] = []
    if scenario.active_quest_id is None:
        errors.append("P0 scenario requires active_quest_id")
        return errors
    try:
        foundation = load_foundation(project_root, scenario.active_quest_id)
    except (OSError, TypeError, ValueError, KeyError) as error:
        return [str(error)]
    for card in foundation.card_rules.cards:
        if card.requires_item is not None and card.requires_item not in bundle.items:
            errors.append(f"Unknown P0 card required item {card.requires_item} in {card.id}")
    if not foundation.card_rules.combos:
        errors.append("P0 card rules require at least one combo rule")
    if not foundation.card_rules.conflicts:
        errors.append("P0 card rules require at least one conflict rule")
    return errors


def _load_quest(raw: JsonMap, quest_id: str) -> Quest:
    for item in _list_at(raw, "quests"):
        quest = _as_mapping(item)
        if quest.get("id") == quest_id:
            return Quest(
                id=str(quest["id"]),
                title=str(quest["title"]),
                start_region=str(quest["start_region"]),
                max_days=int(quest["max_days"]),
                max_turns=int(quest["max_turns"]),
                rewards=_mapping_at(quest, "rewards"),
            )
    raise ValueError(f"Unknown P0 quest: {quest_id}")


def _load_card_rules(raw: JsonMap) -> CardRules:
    rules = _mapping_at(raw, "multi_select_rules")
    return CardRules(
        cards=tuple(_load_card(item) for item in _list_at(raw, "p0_cards")),
        default_extra_cost=_mapping_at(rules, "default_extra_cost"),
        combos=tuple(_load_combo(item) for item in _list_at(rules, "combo_rules")),
        conflicts=tuple(_load_conflict(item) for item in _list_at(rules, "conflict_rules")),
    )


def _load_card(raw_value: JsonValue) -> CardRule:
    raw = _as_mapping(raw_value)
    return CardRule(
        id=str(raw["id"]),
        title=str(raw["title"]),
        description=str(raw.get("description", "")),
        slot_role=str(raw["slot_role"]),
        regions=_string_tuple(raw.get("regions", [])),
        result=_mapping_at(raw, "result"),
        requires_item=_optional_string(raw, "requires_item"),
        requires_progress=_mapping_at(raw, "requires_progress"),
        requires_status=_mapping_at(raw, "requires_status"),
    )


def _load_combo(raw_value: JsonValue) -> ComboRule:
    raw = _as_mapping(raw_value)
    cards = _string_tuple(raw.get("cards", []))
    if len(cards) != 2:
        raise ValueError(f"Combo rule requires exactly two cards: {raw.get('id')}")
    return ComboRule(id=str(raw["id"]), cards=(cards[0], cards[1]), result=_mapping_at(raw, "result"))


def _load_conflict(raw_value: JsonValue) -> ConflictRule:
    raw = _as_mapping(raw_value)
    cards = _string_tuple(raw.get("cards", []))
    if len(cards) != 2:
        raise ValueError(f"Conflict rule requires exactly two cards: {raw.get('id')}")
    return ConflictRule(id=str(raw["id"]), cards=(cards[0], cards[1]), message=str(raw.get("message", "")))


def _read_mapping(path: Path) -> JsonMap:
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    return _as_mapping(loaded)


def _mapping_at(raw: JsonMap, key: str) -> JsonMap:
    return _as_mapping(raw.get(key, {}))


def _list_at(raw: JsonMap, key: str) -> tuple[JsonValue, ...]:
    value = raw.get(key, [])
    if not isinstance(value, list):
        raise TypeError(f"{key} must be a list")
    return tuple(value)


def _optional_string(raw: JsonMap, key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{key} must be a string")
    return value


def _string_tuple(value: JsonValue) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value)


def _as_mapping(value: JsonValue) -> JsonMap:
    if not isinstance(value, dict):
        raise TypeError("value must be a mapping")
    return {str(key): item for key, item in value.items()}
