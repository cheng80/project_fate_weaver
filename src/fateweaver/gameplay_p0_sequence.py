from __future__ import annotations

from pathlib import Path

from fateweaver.gameplay_p0_data import load_foundation
from fateweaver.gameplay_p0_models import Foundation
from fateweaver.models import Scenario


def next_quest_id(scenario: Scenario, current_quest_id: str) -> str:
    sequence = scenario.quest_sequence
    if not sequence:
        return ""
    try:
        index = sequence.index(current_quest_id)
    except ValueError:
        return ""
    next_index = index + 1
    return sequence[next_index] if next_index < len(sequence) else ""


def load_next_foundation(root: Path, scenario: Scenario, current_quest_id: str) -> Foundation | None:
    quest_id = next_quest_id(scenario, current_quest_id)
    return None if not quest_id else load_foundation(root, quest_id)
