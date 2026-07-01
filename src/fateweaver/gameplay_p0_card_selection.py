from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from typing import Final

from fateweaver.gameplay_p0_errors import MissingCardSlotError
from fateweaver.gameplay_p0_models import CardCandidate, CardSelectionContext, CardSelectionResult, CardRule


SLOT_ROLES: Final = ("quest_progress", "risk_discovery", "resource_alternative")
TIER_RANK: Final = {"critical": 4, "strong": 3, "normal": 2, "flavor": 1, "blocked": 0}
VARIETY_WINDOW_SIZE: Final = 3
SCORE_TOLERANCE: Final = 10


def select_cards_from_pool(pool: tuple[CardCandidate, ...], context: CardSelectionContext) -> CardSelectionResult:
    available = tuple(candidate for candidate in _ranked_candidates(pool) if candidate.tier != "blocked")
    picks = tuple(_pick_for_slot(available, slot, context) for slot in SLOT_ROLES)
    windows = {slot: _variety_window(_deprioritize_overused(available, slot), slot) for slot in SLOT_ROLES}
    return CardSelectionResult(
        cards=(picks[0].card, picks[1].card, picks[2].card),
        candidate_pool=_with_selection_evidence(pool, picks, windows, context),
    )


def _pick_for_slot(candidates: tuple[CardCandidate, ...], slot: str, context: CardSelectionContext) -> CardCandidate:
    window = _variety_window(_deprioritize_overused(candidates, slot), slot)
    if not window:
        raise MissingCardSlotError(slot)
    return min(window, key=lambda candidate: _weighted_seed_value(candidate, _selection_seed_key(context, slot)))


def _deprioritize_overused(candidates: tuple[CardCandidate, ...], slot: str) -> tuple[CardCandidate, ...]:
    slot_candidates = tuple(candidate for candidate in candidates if candidate.card.slot_role == slot)
    fresh = tuple(candidate for candidate in slot_candidates if not _overused(candidate))
    if not fresh:
        return candidates
    fresh_ids = {candidate.card.id for candidate in fresh}
    return tuple(candidate for candidate in candidates if candidate.card.slot_role != slot or candidate.card.id in fresh_ids)


def _overused(candidate: CardCandidate) -> bool:
    return candidate.frequency_penalty <= -36


def _variety_window(candidates: tuple[CardCandidate, ...], slot: str) -> tuple[CardCandidate, ...]:
    slot_candidates = tuple(candidate for candidate in candidates if candidate.card.slot_role == slot)
    if not slot_candidates:
        return ()
    top = slot_candidates[0]
    return tuple(
        candidate
        for candidate in slot_candidates
        if candidate.tier == top.tier and top.score - candidate.score <= SCORE_TOLERANCE
    )[:VARIETY_WINDOW_SIZE]


def _with_selection_evidence(
    pool: tuple[CardCandidate, ...],
    picks: tuple[CardCandidate, ...],
    windows: dict[str, tuple[CardCandidate, ...]],
    context: CardSelectionContext,
) -> tuple[CardCandidate, ...]:
    selected_ids = {candidate.card.id for candidate in picks}
    window_ids = {candidate.card.id: _selection_seed_key(context, slot) for slot, candidates in windows.items() for candidate in candidates}
    return tuple(
        replace(
            candidate,
            selection_seed_key=window_ids.get(candidate.card.id, ""),
            variety_window=candidate.card.id in window_ids,
            selected_by="seeded_tier_pick" if candidate.card.id in selected_ids else _window_label(candidate.card.id, window_ids),
        )
        for candidate in pool
    )


def _window_label(card_id: str, window_ids: dict[str, str]) -> str:
    if card_id in window_ids:
        return "seeded_tier_window"
    return ""


def _ranked_candidates(pool: tuple[CardCandidate, ...]) -> tuple[CardCandidate, ...]:
    return tuple(sorted(pool, key=lambda candidate: (TIER_RANK[candidate.tier], candidate.score, candidate.card.id), reverse=True))


def _weighted_seed_value(candidate: CardCandidate, seed_key: str) -> float:
    digest = sha256(f"{seed_key}:{candidate.card.id}".encode("utf-8")).hexdigest()
    raw_value = int(digest[:16], 16) / 0xFFFFFFFFFFFFFFFF
    return raw_value / max(candidate.score, 1)


def _selection_seed_key(context: CardSelectionContext, slot: str) -> str:
    return (
        f"{context.scenario_id}:{context.seed}:run{context.run_number}:"
        f"day{context.day}:turn{context.turn}:{slot}:"
        f"{context.current_region}:{context.active_quest_id}"
    )
