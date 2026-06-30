from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final, Literal, Protocol

from fateweaver.models import Event, JsonMap, ProjectData, Scenario, StatusMap


TIME_OF_DAY: Final = ("morning", "afternoon", "evening", "night")
ObjectiveType = Literal["collect_item", "return_to_region", "survive_expedition", "keep_resource_at_least", "discover_clue", "optional_action"]


class InputPort(Protocol):
    def isatty(self) -> bool: ...

    def readline(self) -> str: ...


class OutputPort(Protocol):
    def write(self, text: str) -> int: ...


@dataclass(frozen=True, slots=True)
class GameplayRunRequest:
    bundle: ProjectData
    scenario: Scenario
    events: tuple[Event, ...]
    seed: int
    run_number: int
    logs_dir: Path
    stdin: InputPort
    stdout: OutputPort
    profile: str


@dataclass(frozen=True, slots=True)
class RunClock:
    day: int
    turn: int
    turns_today: int
    time_of_day: str
    act: int
    max_days: int
    max_turns: int
    turns_per_day: int


@dataclass(frozen=True, slots=True)
class Quest:
    id: str
    title: str
    start_region: str
    max_days: int
    max_turns: int
    objectives: tuple["QuestObjective", ...]
    rewards: JsonMap


@dataclass(frozen=True, slots=True)
class QuestObjective:
    id: str
    objective_type: ObjectiveType
    target: str
    required: bool
    count: int
    value: int
    progress_key: str
    failure_reason: str
    partial_reason: str
    score_key: str
    reward_weight: int


@dataclass(frozen=True, slots=True)
class CardRule:
    id: str
    title: str
    description: str
    slot_role: str
    regions: tuple[str, ...]
    result: JsonMap
    requires_item: str | None
    requires_progress: JsonMap
    requires_status: JsonMap


@dataclass(frozen=True, slots=True)
class ComboRule:
    id: str
    cards: tuple[str, str]
    result: JsonMap


@dataclass(frozen=True, slots=True)
class ConflictRule:
    id: str
    cards: tuple[str, str]
    message: str


@dataclass(frozen=True, slots=True)
class CardRules:
    cards: tuple[CardRule, ...]
    default_extra_cost: JsonMap
    combos: tuple[ComboRule, ...]
    conflicts: tuple[ConflictRule, ...]


@dataclass(frozen=True, slots=True)
class Foundation:
    quest: Quest
    card_rules: CardRules
    score_rules: JsonMap


@dataclass(frozen=True, slots=True)
class RunState:
    clock: RunClock
    status: StatusMap
    inventory: tuple[str, ...]
    run_tags: tuple[str, ...]
    region: str
    quest_progress: dict[str, int]
    clues: tuple[str, ...]
    omens: tuple[str, ...]
    score: dict[str, int]
    next_event_tags: tuple[str, ...]
    recent_event_ids: tuple[str, ...]
    selected_choice_history: tuple[str, ...]
    combo_used: bool
