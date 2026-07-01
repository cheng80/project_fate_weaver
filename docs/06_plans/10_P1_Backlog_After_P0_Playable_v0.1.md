# [Current] P1 Backlog After P0 Playable v0.1

> 상태: [Current] P0 playable milestone 이후 P1에서 다룰 후보 작업을 정리한 backlog 문서.

## 1. Purpose

P0 playable milestone은 하나의 안정적인 vertical slice를 고정한다. 이 문서는 그 다음에 다룰 P1 후보를 우선순위와 guardrail 중심으로 정리한다.

## 2. P1 Planning Principles

P1 작업은 다음 원칙을 따라야 한다.

- P0 baseline을 먼저 재검증한다.
- 한 번에 하나의 surface만 바꾼다.
- Content expansion과 balance tuning을 같은 작업에 섞지 않는다.
- Human playtest evidence 없이 대규모 balance pass를 시작하지 않는다.
- Standard Run baseline 변경은 의도와 근거를 문서화한다.

## 3. Recommended Order

1. `CODEX_TASK_P1_Planning_After_P0_Playable_v0.1.md`
2. `CODEX_TASK_P1_Human_Playtest_Scenario_Pack_v0.1.md`
3. P1 Human Play Quality Audit
4. P1 Scenario / Quest Pack Planning
5. P1 Content Expansion Slice
6. Resource Balance Pass 2, only if playtest evidence supports it
7. Text MUD Narrative Polish 2, only after transcript review

## 4. Candidate Epics

P1 candidate epics:

- Human Playtest Loop:
  - Create deterministic playtest packs.
  - Compare autoplayer and human decision patterns.
  - Capture friction around choices, resource pressure, and quest purpose.
- Scenario Pack Expansion:
  - Add a small number of scenario fixtures after planning.
  - Keep acceptance gates strict.
  - Avoid bulk content before evidence.
- Quest Expansion:
  - Add new quest shapes only after P1 scope is approved.
  - Keep objective schema compatibility.
- Variety / Repetition Improvement:
  - Use playtest logs to identify repeated storylet families.
  - Avoid disabling one specific storylet as a shortcut.
- Balance Pass 2:
  - Focus on resource pressure only if P0 watch seeds prove problematic in P1 evidence.
- Text MUD Polish 2:
  - Use human transcript review rather than polishing in the abstract.
- Player-Facing Shell:
  - Consider a minimal UI only after the CLI/Text MUD loop remains stable.

## 5. Deferred From P0

Deferred items from P0:

- Human playtest evidence.
- P1 scenario breadth.
- Larger quest/content catalog.
- Resource Balance Pass 2.
- Text MUD Narrative Polish 2.
- Manual player UI.
- Save/load.
- Production packaging.
- Runtime LLM narration.

## 6. Watch Items Feeding P1

Known P0 watch items to feed into P1:

- Seed 202 resource alternative selected count is `1`.
- Seed 707 resource alternative selected count is `1`.
- Seed 202 unique event count is `11`.
- Situation intents and storylet families may still repeat under deterministic conditions.
- Human play may reveal different choice pressure than the balanced autoplayer.

## 7. First Task Recommendation

Recommended next task:

```text
CODEX_TASK_P1_Planning_After_P0_Playable_v0.1.md
```

Reason:

P0 is now frozen. The next task should define P1 scope, acceptance gates, playtest evidence requirements, and which watch items are worth reopening. Starting with content expansion or Balance Pass 2 would risk changing the baseline before deciding what P1 is trying to prove.
