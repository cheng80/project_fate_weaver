from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


@dataclass(frozen=True, slots=True)
class ManualRunnerArgs:
    project_root: Path
    scenario_path: Path
    seed: int
    output_dir: Path
    choices: tuple[int, ...]
    choice_source: str
    max_turns: int | None


@dataclass(frozen=True, slots=True)
class InvalidManualChoiceError(ValueError):
    raw_choice: str

    def __str__(self) -> str:
        return f"invalid manual choice {self.raw_choice!r}; expected 1, 2, or 3"


class InvalidManualScenarioError(ValueError):
    pass


class TraceEntry(TypedDict):
    turn: int
    day: int
    presented_card_ids: list[str]
    selected_index: int
    selected_card_id: str
    selected_card_slot_role: str
    result_summary: str
    resource_delta: dict[str, int]
    objective_delta: dict[str, int]
    next_event_tags_delta: list[str]
