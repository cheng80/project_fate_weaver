from __future__ import annotations

from fateweaver.gameplay_p0_models import RunState
from fateweaver.models import Event, JsonMap, JsonValue


def ontology_event_weight(event: Event, ontology_inference: JsonMap | None) -> int:
    if not ontology_inference:
        return 0
    event_tags = _event_tags(event)
    total = 0
    for modifier in _modifier_maps(ontology_inference.get("event_weight_modifiers", [])):
        tags = set(_string_tuple(modifier.get("tags", [])))
        if event_tags & tags:
            total += int(modifier.get("amount", 0))
    return total


def director_event_score(event: Event, state: RunState, ontology_inference: JsonMap | None) -> int:
    tags = _event_tags(event)
    score = event.base_weight + min(1, ontology_event_weight(event, ontology_inference))
    score += min(4, 2 * len(tags & set(state.next_event_tags)))
    intent_terms = {
        part
        for intent in _string_tuple((ontology_inference or {}).get("situation_intents", []))
        for part in str(intent).removeprefix("intent.").split("_")
    }
    score += min(3, len(tags & intent_terms))
    if state.clues and tags & {"clue_followup", "reveal_clue"}:
        score += 3
    if state.omens and tags & {"omen", "omen_escalation", "escalate_risk", "introduce_omen"}:
        score += 3
    completed = sum(1 for value in state.quest_progress.values() if value > 0)
    if completed >= 2 or state.clock.turn >= state.clock.max_turns - 5:
        score += (
            4
            if tags & {"aftermath", "invite_return", "resolve_objective", "return_report", "secure_evidence"}
            else 0
        )
        score -= 4 if tags & {"test_survival", "unlock_route", "reveal_clue"} else 0
    score -= min(4, 2 * state.recent_event_ids[-4:].count(event.id))
    score -= min(3, state.repeat_memory.recent_storylets.count(event.id))
    score -= (
        3
        if event.repeat_group and any(counter.key == event.repeat_group for counter in state.repeat_memory.repeat_groups)
        else 0
    )
    score -= min(
        3,
        len(set(event.cooldown_tags) & {counter.key for counter in state.repeat_memory.cooldown_tags}),
    )
    return max(1, score)


def _event_tags(event: Event) -> set[str]:
    return set(
        (
            *event.region_tags,
            *event.event_tags,
            *event.danger_tags,
            *event.storylet_tags,
            *event.card_candidate_hints,
        ),
    )


def _modifier_maps(raw: JsonValue) -> tuple[JsonMap, ...]:
    if not isinstance(raw, list):
        return ()
    return tuple(item for item in raw if isinstance(item, dict))


def _string_tuple(value: JsonValue) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(str(item) for item in value)
