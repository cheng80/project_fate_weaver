from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import NotRequired, TypedDict


@dataclass(frozen=True, slots=True)
class ManualRunnerArgs:
    project_root: Path
    scenario_path: Path
    seed: int
    output_dir: Path
    choices: tuple[int, ...]
    choice_source: str
    max_turns: int | None
    agent_policy: str | None = None


@dataclass(frozen=True, slots=True)
class InvalidManualChoiceError(ValueError):
    raw_choice: str

    def __str__(self) -> str:
        return f"invalid manual choice {self.raw_choice!r}; expected 1, 2, or 3"


class InvalidManualScenarioError(ValueError):
    pass


class RequiredObjectiveTrace(TypedDict):
    id: str
    objective_type: str
    target: str
    progress_key: str
    required: bool
    before_value: int
    after_value: int
    completed_after: bool


class PresentedCardRelevance(TypedDict):
    card_id: str
    slot_role: str
    active_quest_id: str
    required_objective_ids: list[str]
    active_quest_linked: bool
    required_objective_linked: bool
    storylet_linked: bool
    resource_or_safety: bool
    off_quest_candidate: bool
    relevance_reason: str
    selection_reason: str
    fallback_reason: str


class TraceEntry(TypedDict):
    turn: int
    day: int
    active_quest_id: str
    active_quest_title: str
    quest_onboarding: bool
    onboarding_reason: str
    required_objective_ids: list[str]
    required_objectives: list[RequiredObjectiveTrace]
    presented_card_ids: list[str]
    presented_card_relevance: list[PresentedCardRelevance]
    selected_index: int
    selected_card_id: str
    selected_card_slot_role: str
    result_summary: str
    resource_delta: dict[str, int]
    objective_delta: dict[str, int]
    next_event_tags_delta: list[str]
    quest_lifecycle_event: NotRequired[str]
    quest_completed: NotRequired[bool]
    quest_success: NotRequired[bool]
    completed_quest_id: NotRequired[str]
    completed_required_objective_ids: NotRequired[list[str]]
    reward_granted: NotRequired[bool]
    reward_delta: NotRequired[dict[str, int]]
    reward_score_delta: NotRequired[dict[str, int]]
    resources_before: NotRequired[dict[str, int]]
    resources_after: NotRequired[dict[str, int]]
    reward_reason: NotRequired[str]
    duplicate_reward_prevented: NotRequired[bool]
    next_quest_id: NotRequired[str]
    no_next_quest: NotRequired[bool]
    next_quest_onboarding: NotRequired[bool]
    run_complete: NotRequired[bool]
    completion_blocked_by_min_turns: NotRequired[bool]
    onboarding_turn: NotRequired[int]
