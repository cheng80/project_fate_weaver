from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from fateweaver.gameplay_p0_models import CardRule, CardRules, ComboRule, ConflictRule, Foundation, ObjectiveType, Quest, QuestObjective
from fateweaver.models import JsonMap, JsonValue, ProjectData, Scenario


@dataclass(frozen=True, slots=True)
class MissingActiveQuestError(ValueError):
    def __str__(self) -> str:
        return "P0 scenario requires active_quest_id"


@dataclass(frozen=True, slots=True)
class UnknownP0QuestError(ValueError):
    quest_id: str

    def __str__(self) -> str:
        return f"Unknown P0 quest: {self.quest_id}"


@dataclass(frozen=True, slots=True)
class UnknownP0ObjectiveTypeError(ValueError):
    objective_type: str

    def __str__(self) -> str:
        return f"Unknown P0 objective type: {self.objective_type}"


@dataclass(frozen=True, slots=True)
class CardPairCountError(ValueError):
    rule_id: str
    rule_type: str

    def __str__(self) -> str:
        return f"{self.rule_type} rule requires exactly two cards: {self.rule_id}"


@dataclass(frozen=True, slots=True)
class GameplayP0TypeError(TypeError):
    label: str
    expected: str

    def __str__(self) -> str:
        return f"{self.label} must be {self.expected}"


def load_foundation(root: Path, quest_id: str | None) -> Foundation:
    if quest_id is None:
        raise MissingActiveQuestError()
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
                objectives=_load_objectives(quest),
                rewards=_mapping_at(quest, "rewards"),
            )
    raise UnknownP0QuestError(quest_id)


def _load_objectives(quest: JsonMap) -> tuple[QuestObjective, ...]:
    primary = tuple(_load_objective(item, True) for item in _list_at(quest, "primary_objectives"))
    optional = tuple(_load_objective(item, False) for item in _list_at(quest, "optional_objectives"))
    return (*primary, *optional)


def _load_objective(raw_value: JsonValue, default_required: bool) -> QuestObjective:
    raw = _as_mapping(raw_value)
    objective_type = _objective_type(str(raw["type"]))
    return QuestObjective(
        id=str(raw["id"]),
        objective_type=objective_type,
        target=str(raw["target"]),
        required=bool(raw.get("required", default_required)),
        count=int(raw.get("count", raw.get("value", 1))),
        value=int(raw.get("value", raw.get("count", 1))),
        progress_key=str(raw.get("progress_key", raw["target"])),
        failure_reason=str(raw["failure_reason"]),
        partial_reason=str(raw.get("partial_reason", raw["failure_reason"])),
        score_key=str(raw["score_key"]),
        reward_weight=int(raw.get("reward_weight", 1)),
    )


def _objective_type(value: str) -> ObjectiveType:
    match value:  # noqa: MATCH_OK - YAML objective type is parsed from boundary data.
        case "collect_item" | "return_to_region" | "survive_expedition" | "keep_resource_at_least" | "discover_clue" | "optional_action":
            return value
        case _:
            raise UnknownP0ObjectiveTypeError(value)


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
        base_weight=int(raw.get("base_weight", 40)),
        tier_hint=str(raw.get("tier_hint", "normal")),
        tags=_string_tuple(raw.get("tags", [])),
        regions=_string_tuple(raw.get("regions", [])),
        result=_mapping_at(raw, "result"),
        requires_item=_optional_string(raw, "requires_item"),
        requires_progress=_mapping_at(raw, "requires_progress"),
        requires_status=_mapping_at(raw, "requires_status"),
        applies_to_storylet_tags=_string_tuple(raw.get("applies_to_storylet_tags", [])),
        applies_to_quest_objectives=_string_tuple(raw.get("applies_to_quest_objectives", [])),
        progress_key=str(raw.get("progress_key", "")),
        weight_modifiers=_mapping_at(raw, "weight_modifiers"),
        quest_ids=_string_tuple(raw.get("quest_ids", [])),
    )


def _load_combo(raw_value: JsonValue) -> ComboRule:
    raw = _as_mapping(raw_value)
    cards = _string_tuple(raw.get("cards", []))
    if len(cards) != 2:
        raise CardPairCountError(str(raw.get("id", "")), "Combo")
    return ComboRule(id=str(raw["id"]), cards=(cards[0], cards[1]), result=_mapping_at(raw, "result"))


def _load_conflict(raw_value: JsonValue) -> ConflictRule:
    raw = _as_mapping(raw_value)
    cards = _string_tuple(raw.get("cards", []))
    if len(cards) != 2:
        raise CardPairCountError(str(raw.get("id", "")), "Conflict")
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
        raise GameplayP0TypeError(key, "a list")
    return tuple(value)


def _optional_string(raw: JsonMap, key: str) -> str | None:
    value = raw.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise GameplayP0TypeError(key, "a string")
    return value


def _string_tuple(value: JsonValue) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value)


def _as_mapping(value: JsonValue) -> JsonMap:
    if not isinstance(value, dict):
        raise GameplayP0TypeError("value", "a mapping")
    return {str(key): item for key, item in value.items()}
