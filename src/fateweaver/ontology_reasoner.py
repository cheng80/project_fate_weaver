from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from fateweaver.game_semantics import SemanticContext, evaluate_semantic_rules
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
    return evaluate_semantic_rules(core, _semantic_context(context))


def _semantic_context(context: OntologyReasonerContext) -> SemanticContext:
    return SemanticContext(
        active_entities=(
            f"quest.{context.quest_id}",
            f"region.{context.region}",
            *(f"item.{item_id}" for item_id in context.inventory),
        ),
        active_tags=context.next_event_tags,
        resources=context.status,
        inventory=context.inventory,
        markers=(*context.clues, *context.omens),
        counters={**context.quest_progress, "omen_count": len(context.omens)},
    )


def _read_mapping(path: Path) -> JsonMap:
    with path.open("r", encoding="utf-8") as handle:
        return _mapping(yaml.safe_load(handle) or {})


def _mapping(value: JsonValue | None) -> JsonMap:
    return {str(key): item for key, item in value.items()} if isinstance(value, dict) else {}
