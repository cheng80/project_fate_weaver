# Completed Objective Choice Refresh Gate Result v0.1

## Summary

Completed Objective Choice Refresh Gate는 PASS다.

이번 변경은 완료된 objective 이후 `presented_cards`에 stale choice가 남는 경로를 `manual_choice_runner` trace로 재현하고, 카드 후보가 presentation으로 확정되기 전 `completed_objective` blocked 판정을 보강했다. 특정 card id를 하드코딩하지 않고 `progress_key`, active quest objective satisfaction, 최근 선택 이력, 기존 frequency penalty를 사용했다.

## Root Cause

기존 `card_blocked_reason`은 `card.progress_key`가 있고 해당 progress가 1 이상이면 stale로 막았다. 이 방식은 objective에 명시적으로 연결된 카드에는 효과가 있었지만, active quest required objectives가 한 번 satisfaction 상태에 도달한 뒤 `quest_ids`가 없는 범용 `quest_progress` 카드가 최근 선택 직후 다시 후보화되는 경로를 막지 못했다.

또한 stale 필터 후 `quest_progress` 슬롯 후보가 부족해질 때 기존 selection은 `MissingCardSlotError`로 떨어질 수 있었다. Manual Choice Runner Robustness Gate의 원칙상 이 상황은 crash가 아니라 3-card surface refresh/fallback으로 처리되어야 한다.

## Implemented Change

- `src/fateweaver/card_staleness.py` 추가
  - `completed_objective_blocked(card, state, quest)` helper를 분리했다.
  - 기존 `progress_key > 0` completed-objective block을 보존했다.
  - `applies_to_quest_objectives`가 이미 satisfied된 objective만 가리키는 카드도 block한다.
  - active quest required objectives가 satisfaction 상태에 도달한 뒤, 최근 선택된 unscoped `quest_progress` 카드가 즉시 다시 노출되는 경로를 block한다.
  - `return_to_region` satisfaction은 report 최종 평가와 별개로 progress key가 이미 달성된 상태를 사용한다. 이는 min-turn 때문에 성공 조건 충족 후에도 runner가 계속 진행되는 기간의 stale refresh를 다루기 위한 presentation-surface 기준이다.
- `src/fateweaver/card_candidates.py`
  - `card_blocked_reason`이 quest id 문자열 대신 `Quest`를 받아 completed-objective helper를 사용한다.
- `src/fateweaver/card_selection.py`
  - stale filtering 이후 특정 slot 후보가 비면 non-blocked 후보에서 deterministic fallback을 사용해 3-card surface를 보충한다.
  - fallback은 이미 선택한 presentation 후보를 제외해 중복 card presentation을 막는다.
  - fallback window는 기존 `frequency_penalty`를 우선 반영해 resource/risk 카드 반복 쏠림을 줄인다.
- `tests/test_manual_choice_runner.py`
  - Manual Choice Runner 기반 회귀 테스트를 추가했다.
  - active quest completion 이후 최근 선택된 unscoped `quest_progress` 카드가 stale로 재노출되지 않는지 검증한다.
  - stale filtering 이후에도 `presented_cards == 3` 및 turn 내 card id 중복 없음도 검증한다.

## Evidence

### Pre-fix Reproduction

- Evidence path: `.omo/ulw-loop/evidence/completed-objective-choice-refresh-20260701/pre-fix/`
- Command: `tools/manual_choice_runner.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --choices 1,1,2,2,1,3,2,2,1,2,3,1,2,1,1,2,3,1,1,1,1,1,1,1,1`
- Result: runner completed, trace showed post-satisfaction card generation could keep presenting recently selected unscoped quest-progress choices.

### Post-fix Manual Trace

- Evidence path: `.omo/ulw-loop/evidence/completed-objective-choice-refresh-20260701/post-fix-all1/`
- Command: `tools/manual_choice_runner.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --choices all-1 x25`
- Result:
  - turns: 25
  - stop_reason: `completed`
  - result_type: `success`
  - ending: `prepared_frontier_route`
  - stale_turns: `[]`
  - duplicate presented cards: `[]`
  - unique presented cards: 18

### Manual Robustness Patterns

Evidence path: `.omo/ulw-loop/evidence/completed-objective-choice-refresh-20260701/patterns/`

| Pattern | Result |
| --- | --- |
| all 1 choices | 25 turns, `completed`, success, `prepared_frontier_route`, trace consistent |
| all 2 choices | 25 turns, `choice_sequence_exhausted`, failure, clean trace |
| all 3 choices | 25 turns, `choice_sequence_exhausted`, failure, clean trace |
| alternating 1/2/3 | 25 turns, `choice_sequence_exhausted`, partial success, clean trace |
| reverse 3/2/1 | 25 turns, `choice_sequence_exhausted`, partial success, clean trace |
| invalid choice | rc 1, clean `invalid manual choice` error |
| choice sequence exhaustion | 1 turn, `choice_sequence_exhausted`, clean trace |
| max turn safety | 5 turns, `max_turn_reached`, trace consistent |

### Autoplayer Baseline

- Evidence path: `.omo/ulw-loop/evidence/completed-objective-choice-refresh-20260701/autoplayer-seed202/`
- Command: `tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --profile balanced`
- Result:
  - turns: 25
  - result_type: `success`
  - ending: `prepared_frontier_route`
  - all turns have 3 presented cards

Seed 42 Standard Run regression also remains within existing test thresholds:

- turns: 25
- result_type: `success`
- ending: `prepared_frontier_route`
- unique presented cards: 18
- top repeat count: 8

## Verification Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_manual_choice_runner tests.test_gameplay_run_standard_run tests.test_gameplay_run_card_candidates tests.test_gameplay_run_optional_action_score tests.test_gameplay_balance_pass
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall -q src tools tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
```

Results:

- focused tests: 31 PASS
- full unittest: 155 PASS
- compileall: PASS
- scenario validation: PASS

Note: this repository currently has no `tools/validate_ontology.py`; ontology-specific validation was therefore not run as a standalone command in this gate.

## Scope Guard

No data files were modified. No Quest/Card/Event/Item/Ending was added. No balance values, reward values, score modifiers, director tuning, ontology rules, Text MUD wording, or random seed flow were changed.

## Remaining Out-of-Scope Issues

- Quest onboarding is still not solved by this gate.
- Suspicious merchant / off-quest relevance noise remains a separate P1 playtest issue.
- Long-run post-completion play can still surface low-stakes risk/resource cards repeatedly; this gate only prevents recently selected stale quest-progress choice refresh failures while preserving Standard Run thresholds.
- A broader “all post-completion quest-progress cards disappear” policy is intentionally out of scope because it collapses Standard Run variety and can break manual all-1 success unless the quest/onboarding lifecycle is redesigned.
