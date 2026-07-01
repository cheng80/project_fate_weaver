from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from fateweaver.models import JsonMap, JsonValue, StatusMap


@dataclass(frozen=True, slots=True)
class OntologyReasonerContext:
    quest_id: str
    region: str
    status: StatusMap
    inventory: tuple[str, ...]
    clues: tuple[str, ...]
    omens: tuple[str, ...]
    quest_progress: dict[str, int]
    next_event_tags: tuple[str, ...]


def load_ontology_core(project_root: Path) -> JsonMap:
    raw = _read_mapping(project_root / "data/core/ontology.yaml")
    return _mapping(raw.get("ontology_core", {}))


def run_reasoner(core: JsonMap, context: OntologyReasonerContext) -> JsonMap:
    facts = _list_of_maps(core, "facts")
    state_facts = _list_of_maps(core, "state_facts")
    rules = _list_of_maps(core, "rules")
    relations = _list_of_maps(core, "relations")

    active_facts = {str(fact.get("id")) for fact in facts if _fact_relevant(fact, context)}
    active_state_facts = {
        str(state_fact.get("id"))
        for state_fact in state_facts
        if _state_fact_active(state_fact, context)
    }
    relation_ids = {str(relation.get("id")) for relation in relations}
    event_modifiers: list[JsonMap] = []
    card_modifiers: list[JsonMap] = []
    intents: list[str] = []
    next_facts: list[str] = []
    trace: list[JsonMap] = []

    for rule in rules:
        rule_id = str(rule.get("id", ""))
        when = _mapping(rule.get("when", {}))
        matched, reasons = _when_matches(when, active_facts, active_state_facts, relation_ids)
        if not matched:
            continue
        then = _mapping(rule.get("then", {}))
        intent = str(then.get("suggest_intent", ""))
        if intent:
            intents.append(intent)
            next_facts.append(f"fact.inferred.{intent}")
        event_weight = _weight_modifier("event", rule_id, then.get("add_event_weight"))
        if event_weight is not None:
            event_modifiers.append(event_weight)
        card_weight = _weight_modifier("card", rule_id, then.get("add_card_weight"))
        if card_weight is not None:
            card_modifiers.append(card_weight)
        trace.append(
            {
                "rule_id": rule_id,
                "matched": True,
                "reasons": reasons,
                "suggest_intent": intent,
                "event_weight": event_weight or {},
                "card_weight": card_weight or {},
            }
        )

    return {
        "active_facts": sorted(active_facts),
        "active_state_facts": sorted(active_state_facts),
        "event_weight_modifiers": event_modifiers,
        "card_weight_modifiers": card_modifiers,
        "situation_intents": _dedupe(intents),
        "next_facts": _dedupe(next_facts),
        "trace": trace,
    }


def _fact_relevant(fact: JsonMap, context: OntologyReasonerContext) -> bool:
    subject = str(fact.get("subject", ""))
    object_id = str(fact.get("object", ""))
    if subject == f"quest.{context.quest_id}":
        return True
    if subject == f"region.{context.region}":
        return True
    if object_id == f"region.{context.region}":
        return True
    if subject.startswith("item.") and subject.removeprefix("item.") in context.inventory:
        return True
    return False


def _state_fact_active(state_fact: JsonMap, context: OntologyReasonerContext) -> bool:
    source = str(state_fact.get("source", ""))
    key = str(state_fact.get("key", ""))
    op = str(state_fact.get("op", ""))
    raw_value = state_fact.get("value")
    if source == "status":
        return _compare(context.status.get(key, 0), op, int(raw_value or 0))
    if source == "inventory":
        return key in context.inventory if op == "contains" else key not in context.inventory
    if source == "clue":
        has_clue = key in context.clues
        return not has_clue if op == "missing" else has_clue
    if source == "omen_count":
        return _compare(len(context.omens), op, int(raw_value or 0))
    if source == "next_event_tag":
        return key in context.next_event_tags if op == "contains" else key not in context.next_event_tags
    if source == "quest_progress":
        return _compare(context.quest_progress.get(key, 0), op, int(raw_value or 0))
    return False


def _when_matches(
    when: JsonMap,
    active_facts: set[str],
    active_state_facts: set[str],
    relation_ids: set[str],
) -> tuple[bool, list[str]]:
    if "all" in when:
        reasons: list[str] = []
        for child in _list_of_values(when["all"]):
            matched, child_reasons = _when_matches(_mapping(child), active_facts, active_state_facts, relation_ids)
            if not matched:
                return False, []
            reasons.extend(child_reasons)
        return True, reasons
    if "any" in when:
        for child in _list_of_values(when["any"]):
            matched, child_reasons = _when_matches(_mapping(child), active_facts, active_state_facts, relation_ids)
            if matched:
                return True, child_reasons
        return False, []
    if "not" in when:
        matched, _ = _when_matches(_mapping(when["not"]), active_facts, active_state_facts, relation_ids)
        return (not matched, ["not"]) if not matched else (False, [])
    if "fact" in when:
        fact_id = str(when["fact"])
        return (fact_id in active_facts, [fact_id] if fact_id in active_facts else [])
    if "state_fact" in when:
        fact_id = str(when["state_fact"])
        return (fact_id in active_state_facts, [fact_id] if fact_id in active_state_facts else [])
    if "relation" in when:
        relation_id = str(when["relation"])
        return (relation_id in relation_ids, [relation_id] if relation_id in relation_ids else [])
    return False, []


def _weight_modifier(target: str, rule_id: str, raw: JsonValue | Any) -> JsonMap | None:
    weight = _mapping(raw)
    tags = _strings(weight.get("tags", []))
    if not tags:
        return None
    return {
        "target": target,
        "rule_id": rule_id,
        "tags": list(tags),
        "amount": int(weight.get("amount", 0)),
    }


def _compare(value: int, op: str, target: int) -> bool:
    if op == "lte":
        return value <= target
    if op == "gte":
        return value >= target
    if op == "lt":
        return value < target
    if op == "gt":
        return value > target
    if op == "eq":
        return value == target
    return False


def _read_mapping(path: Path) -> JsonMap:
    with path.open("r", encoding="utf-8") as handle:
        return _mapping(yaml.safe_load(handle) or {})


def _list_of_maps(raw: JsonMap, key: str) -> list[JsonMap]:
    return [_mapping(item) for item in _list_of_values(raw.get(key, []))]


def _mapping(value: JsonValue | Any) -> JsonMap:
    return {str(key): item for key, item in value.items()} if isinstance(value, dict) else {}


def _list_of_values(value: JsonValue | Any) -> list[JsonValue]:
    return list(value) if isinstance(value, list) else []


def _strings(value: JsonValue | Any) -> tuple[str, ...]:
    return tuple(str(item) for item in value) if isinstance(value, list) else ()


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))
