from __future__ import annotations

from fateweaver.gameplay_models import CardRule, ComboRule, RunClock
from fateweaver.models import JsonMap


def multi_select_json(combo: ComboRule | None, selected_ids: list[str]) -> JsonMap:
    if combo is None:
        return {"selected": False, "selected_cards": selected_ids}
    return {
        "selected": True,
        "rule_id": combo.id,
        "selected_cards": selected_ids,
        "cost_applied": True,
        "combo_applied": True,
    }


def influences(selected: tuple[CardRule, ...], combo: ComboRule | None) -> list[str]:
    values: list[str] = []
    for card in selected:
        values.append(f"card:{card.id}")
        values.append(f"slot:{card.slot_role}")
    if combo is not None:
        values.append(f"combo:{combo.id}")
        values.append("cost:default_extra_cost")
    return values


def clock_json(clock: RunClock) -> JsonMap:
    return {
        "day": clock.day,
        "turn": clock.turn,
        "turns_today": clock.turns_today,
        "time_of_day": clock.time_of_day,
        "act": clock.act,
        "max_days": clock.max_days,
        "max_turns": clock.max_turns,
        "turns_per_day": clock.turns_per_day,
    }
