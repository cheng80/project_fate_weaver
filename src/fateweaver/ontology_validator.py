from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from fateweaver.models import JsonMap, JsonValue


MINIMUM_COUNTS = {
    "entities": 20,
    "relations": 20,
    "facts": 15,
    "rules": 10,
    "situation_intents": 8,
}


def validate_ontology_core(project_root: Path) -> list[str]:
    raw = _read_mapping(project_root / "data/core/ontology.yaml")
    core = _mapping(raw.get("ontology_core", {}))
    errors: list[str] = []
    if not core:
        return ["Missing ontology_core"]

    entities = _list_of_maps(core, "entities")
    relations = _list_of_maps(core, "relations")
    facts = _list_of_maps(core, "facts")
    state_facts = _list_of_maps(core, "state_facts")
    rules = _list_of_maps(core, "rules")
    intents = _list_of_maps(core, "situation_intents")
    predicates = _list_of_maps(core, "predicates")

    errors.extend(_validate_minimum_counts(entities, relations, facts, state_facts, rules, intents))
    entity_ids = _ids(entities, "entity", errors)
    intent_ids = _ids(intents, "situation_intent", errors)
    relation_ids = _ids(relations, "relation", errors)
    fact_ids = _ids(facts, "fact", errors)
    state_fact_ids = _ids(state_facts, "state_fact", errors)
    predicate_ids = _ids(predicates, "predicate", errors)
    known_subjects = entity_ids | intent_ids

    for relation in relations:
        relation_id = str(relation.get("id", "<missing>"))
        predicate = str(relation.get("predicate", ""))
        subject = str(relation.get("subject", ""))
        object_id = str(relation.get("object", ""))
        if predicate not in predicate_ids:
            errors.append(f"Unknown relation predicate {predicate} in {relation_id}")
        if subject not in known_subjects:
            errors.append(f"Unknown relation subject {subject} in {relation_id}")
        if object_id not in known_subjects:
            errors.append(f"Unknown relation object {object_id} in {relation_id}")

    for fact in facts:
        fact_id = str(fact.get("id", "<missing>"))
        subject = str(fact.get("subject", ""))
        object_id = str(fact.get("object", ""))
        if subject not in known_subjects:
            errors.append(f"Unknown fact subject {subject} in {fact_id}")
        if object_id not in known_subjects:
            errors.append(f"Unknown fact object {object_id} in {fact_id}")

    known_tags = _known_tags(project_root, entities, intents)
    for intent in intents:
        for tag in _strings(intent.get("tags", [])):
            if tag not in known_tags:
                errors.append(f"Unknown situation intent tag {tag} in {intent.get('id')}")

    known_rule_refs = fact_ids | state_fact_ids
    for rule in rules:
        rule_id = str(rule.get("id", "<missing>"))
        errors.extend(_validate_rule_when(rule_id, _mapping(rule.get("when", {})), known_rule_refs, relation_ids))
        errors.extend(_validate_rule_then(rule_id, _mapping(rule.get("then", {})), intent_ids, known_tags))

    return errors


def _validate_minimum_counts(
    entities: list[JsonMap],
    relations: list[JsonMap],
    facts: list[JsonMap],
    state_facts: list[JsonMap],
    rules: list[JsonMap],
    intents: list[JsonMap],
) -> list[str]:
    counts = {
        "entities": len(entities),
        "relations": len(relations),
        "facts": len(facts) + len(state_facts),
        "rules": len(rules),
        "situation_intents": len(intents),
    }
    return [
        f"Ontology core {key} count {count} below minimum {MINIMUM_COUNTS[key]}"
        for key, count in counts.items()
        if count < MINIMUM_COUNTS[key]
    ]


def _ids(items: list[JsonMap], label: str, errors: list[str]) -> set[str]:
    ids: set[str] = set()
    for item in items:
        item_id = str(item.get("id", ""))
        if not item_id:
            errors.append(f"Missing ontology {label} id")
            continue
        if item_id in ids:
            errors.append(f"Duplicate ontology {label} id: {item_id}")
        ids.add(item_id)
    return ids


def _validate_rule_when(rule_id: str, when: JsonMap, known_refs: set[str], relation_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for key in ("fact", "state_fact"):
        ref = when.get(key)
        if ref is not None and str(ref) not in known_refs:
            errors.append(f"Unknown rule {key} {ref} in {rule_id}")
    relation = when.get("relation")
    if relation is not None and str(relation) not in relation_ids:
        errors.append(f"Unknown rule relation {relation} in {rule_id}")
    for group_key in ("all", "any"):
        for child in _list_of_values(when.get(group_key, [])):
            errors.extend(_validate_rule_when(rule_id, _mapping(child), known_refs, relation_ids))
    if "not" in when:
        errors.extend(_validate_rule_when(rule_id, _mapping(when["not"]), known_refs, relation_ids))
    return errors


def _validate_rule_then(rule_id: str, then: JsonMap, intent_ids: set[str], known_tags: set[str]) -> list[str]:
    errors: list[str] = []
    intent = then.get("suggest_intent")
    if intent is not None and str(intent) not in intent_ids:
        errors.append(f"Unknown rule situation intent {intent} in {rule_id}")
    for key in ("add_event_weight", "add_card_weight"):
        weight = _mapping(then.get(key, {}))
        for tag in _strings(weight.get("tags", [])):
            if tag not in known_tags:
                errors.append(f"Unknown rule weight tag {tag} in {rule_id}")
    return errors


def _known_tags(project_root: Path, entities: list[JsonMap], intents: list[JsonMap]) -> set[str]:
    raw = _read_mapping(project_root / "data/core/tags.yaml")
    tags = _mapping(raw.get("tags", {}))
    known: set[str] = set()
    for values in tags.values():
        known.update(_strings(values))
    for item in (*entities, *intents):
        known.update(_strings(item.get("tags", [])))
    return known


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
