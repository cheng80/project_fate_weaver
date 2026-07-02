from __future__ import annotations

from fateweaver.gameplay_models import CardCandidate, CardRule
from fateweaver.models import JsonMap


def card_candidate_pool_json(pool: tuple[CardCandidate, ...]) -> list[JsonMap]:
    return [
        {
            "card_id": candidate.card.id,
            "slot_role": candidate.card.slot_role,
            "score": candidate.score,
            "tier": candidate.tier,
            "matched_tags": list(candidate.matched_tags),
            "matched_objectives": list(candidate.matched_objectives),
            "matched_storylet_hints": list(candidate.matched_storylet_hints),
            "blocked_reason": candidate.blocked_reason,
            "selection_seed_key": candidate.selection_seed_key,
            "variety_window": candidate.variety_window,
            "selected_by": candidate.selected_by,
            "repeat_penalty": candidate.repeat_penalty,
            "cooldown_penalty": candidate.cooldown_penalty,
            "frequency_penalty": candidate.frequency_penalty,
            "fallback_penalty": candidate.fallback_penalty,
            "ontology_modifier_applied": candidate.ontology_modifier_applied,
        }
        for candidate in pool
    ]


def card_json(card: CardRule) -> JsonMap:
    return {
        "choice_id": card.id,
        "card_id": card.id,
        "choice_text": card.title,
        "title": card.title,
        "description": card.description,
        "slot_role": card.slot_role,
        "choice_type": card.slot_role,
        "quest_ids": list(card.quest_ids),
        "available": True,
        "unavailable_reason": None,
        "hidden": False,
        "expected_risk": "low" if card.slot_role != "risk_discovery" else "medium",
        "influenced_by": card_influences(card),
        "result": card.result,
    }


def card_influences(card: CardRule) -> list[str]:
    values = [f"slot:{card.slot_role}"]
    values.extend(f"tag:{tag}" for tag in card.tags)
    values.extend(f"storylet_tag:{tag}" for tag in card.applies_to_storylet_tags)
    values.extend(f"objective:{objective_id}" for objective_id in card.applies_to_quest_objectives)
    if card.progress_key:
        values.append(f"progress:{card.progress_key}")
    return values
