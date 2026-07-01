# Quest Completion Lifecycle & Reward Gate Result v0.1

## Status

DONE.

Quest required objectives가 satisfied되면 `min_turns_before_completion`에 막히지 않고 즉시 quest success로 처리되며, P0 quest reward가 state/trace/report/batch 표면에 기록되도록 보강했다.

## 수정 파일 목록

- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_lifecycle.py`
- `tools/manual_choice_runner.py`
- `tools/manual_choice_runner_trace.py`
- `tools/manual_choice_runner_types.py`
- `tools/manual_choice_runner_report.py`
- `tools/manual_choice_runner_batch.py`
- `tests/test_quest_completion_lifecycle.py`
- `tests/test_gameplay_p0_standard_run.py`
- `tests/test_manual_choice_runner_report.py`
- `tests/test_manual_choice_runner_batch.py`
- `docs/07_reviews/70_Quest_Completion_Lifecycle_Reward_Gate_Result_v0.1.md`

## min_turns_before_completion 문제 원인

`quest_completed(...)`는 이미 objective satisfaction 기준으로 success를 판정하고 있었다. 문제는 `src/fateweaver/gameplay_p0.py`와 `tools/manual_choice_runner.py`가 success break 조건에 `state.clock.turn >= _minimum_completion_turn(...)`을 hard gate로 붙인 점이었다.

그 결과 required objectives가 3턴에 완료되어도 Standard Run은 25턴까지 남은 선택을 반복할 수 있었다.

## Quest Completion Lifecycle 적용 방식

`quest_completed(...)`가 true가 되는 즉시 lifecycle을 처리한다.

- quest success는 objective satisfaction 기준
- `min_turns_before_completion`은 quest success/reward/run complete를 막지 않음
- 다음 quest system이 없는 현재 P0에서는 `no_next_quest: true`, `run_complete: true`로 clean end

## Reward Contract 정의

기존 quest data의 `rewards` field를 P0 reward contract로 사용했다.

`survive_the_storm_pass` reward:

```yaml
rewards:
  money: 2
  reputation: 1
  score: 45
```

대규모 economy/balance tuning은 하지 않았다.

## Reward 지급 방식

`src/fateweaver/gameplay_p0_lifecycle.py`를 추가했다.

- status reward: `money`, `reputation`처럼 `bundle.statuses`에 있는 key만 status delta로 지급
- score reward: `score`는 `score["quest_reward"]`로 지급
- reward 지급 후 `resources_before`, `resources_after`, `reward_delta`, `reward_score_delta`를 lifecycle trace에 기록

## Reward 중복 지급 방지 방식

reward 지급 시 `run_tags`에 `quest_reward:<quest_id>`를 추가한다. 같은 quest lifecycle 경로가 다시 호출되면 state를 변경하지 않고 `duplicate_reward_prevented: true`로 기록할 수 있다.

현재 정상 run은 quest success 직후 종료되므로 duplicate reward는 0건이다.

## Next Quest Transition 방식

현재 P0 Standard Run에는 quest sequence/campaign transition data가 없다. 따라서 이번 Gate에서는 새 quest를 만들지 않고:

- `next_quest_id: ""`
- `no_next_quest: true`
- `next_quest_onboarding: false`
- `run_complete: true`

로 clean end를 명시했다.

## Trace / Report / Batch 보강

Trace에 추가:

- `quest_lifecycle_event`
- `quest_completed`
- `quest_success`
- `completed_quest_id`
- `completed_required_objective_ids`
- `reward_granted`
- `reward_delta`
- `reward_score_delta`
- `resources_before`
- `resources_after`
- `reward_reason`
- `duplicate_reward_prevented`
- `next_quest_id`
- `no_next_quest`
- `next_quest_onboarding`
- `run_complete`
- `completion_blocked_by_min_turns`

Manual Run Trace Report에 `Quest Completion` 섹션 추가.

Subagent batch summary/report에 lifecycle 집계 추가:

- quest completion count
- reward granted count
- duplicate reward prevention count
- next quest transition count
- run complete count
- completion blocked by min turns count

## 추가 테스트 목록

- `tests/test_quest_completion_lifecycle.py`
  - required objectives satisfied 후 25턴 이전 success 종료 검증
  - quest success reward가 1회 지급되고 trace에 기록되는지 검증
- `tests/test_gameplay_p0_standard_run.py`
  - 기존 25턴 baseline을 quest lifecycle baseline으로 갱신
- `tests/test_manual_choice_runner_report.py`
  - report completion/reward 섹션 검증
- `tests/test_manual_choice_runner_batch.py`
  - batch lifecycle aggregate fields 검증

## 실행한 검증 명령과 결과

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_onboarding.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_relevance.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_report.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_batch.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_gameplay_p0_card_candidates.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_quest_completion_lifecycle.py
```

- PASS

```bash
PYTHONPATH=src .venv/bin/python -m unittest
```

- PASS: 167 tests

```bash
PYTHONPATH=src .venv/bin/python -m compileall src tools tests
```

- PASS

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
```

- PASS: `VALIDATION: PASS`

Ontology/no-excuse checker:

- `tools/validate_ontology.py` 없음
- `tools/no_excuse_checker.py` 없음

## Seed 202 Autoplayer Baseline 영향

기존 25턴 baseline은 의도적으로 변경되었다.

새 baseline:

- result_type: `success`
- ending: `prepared_frontier_route`
- turn_count: 3
- quest_success: true
- reward_granted: true
- completion_blocked_by_min_turns: false
- final_state: `money=8`, `reputation=3`

즉 `min_turns_before_completion`으로 완료된 quest를 지연하지 않는다.

## 기존 Gate Regression 유지 여부

- Manual Choice Runner Robustness Gate: PASS
- Completed Objective Choice Refresh Gate: PASS
- Quest Onboarding Flow Gate: PASS
- Choice Relevance Noise Gate: PASS
- Manual Run Trace Report & Subagent Batch Gate: PASS
- 3-card invariant: maintained before quest completion
- same-turn duplicate presentation guard: maintained

## 남은 범위 밖 이슈

- 실제 next quest transition은 아직 campaign/quest sequence data가 없으므로 구현하지 않았다.
- 다음 Gate에서 multi-quest Standard Run을 원하면 quest sequence data와 onboarding 전환 규칙이 먼저 필요하다.
- reward 수치 튜닝은 하지 않았다.

## Commit

- commit hash: pending
- working tree clean: pending
