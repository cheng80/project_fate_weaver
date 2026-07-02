# Quest Sequence Transition Gate Result v0.1

## Status

DONE.

Standard Run에 최소 2-quest sequence를 추가하고, quest success/reward 이후 다음 quest가 있으면 active quest foundation이 전환되도록 보강했다. Sequence 마지막 quest에서만 `no_next_quest: true` / `run_complete: true`가 기록된다.

## 수정 파일 목록

- `data/scenarios/standard_run_25_35_turn.yaml`
- `src/fateweaver/models.py`
- `src/fateweaver/data_loader.py`
- `src/fateweaver/gameplay_run.py`
- `src/fateweaver/quest_lifecycle.py`
- `src/fateweaver/quest_sequence.py`
- `tools/manual_choice_runner.py`
- `tools/manual_choice_runner_output.py`
- `tools/manual_choice_runner_trace.py`
- `tools/manual_choice_runner_types.py`
- `tools/manual_choice_runner_report.py`
- `tools/manual_choice_runner_batch.py`
- `tools/manual_choice_runner_batch_metrics.py`
- `tools/manual_choice_runner_batch_report.py`
- `tests/test_quest_sequence_transition.py`
- `tests/test_quest_completion_lifecycle.py`
- `tests/test_manual_choice_runner_report.py`
- `tests/test_manual_choice_runner_batch.py`
- `docs/07_reviews/72_Quest_Sequence_Transition_Gate_Result_v0.1.md`
- `out/quest_sequence_transition_smoke_v0.1/batch_summary.json`
- `out/quest_sequence_transition_smoke_v0.1/batch_report.md`
- `out/quest_sequence_transition_smoke_202_206_v0.1.md`

## 후속 quest sequence 부재 원인

이전 lifecycle은 `complete_quest_lifecycle(...)`에서 항상 아래 값을 반환했다.

```text
next_quest_id: ""
no_next_quest: true
next_quest_onboarding: false
run_complete: true
```

또한 run loop는 lifecycle event가 생기면 즉시 break했다. 따라서 required objectives가 완료되면 reward 후 다음 quest를 확인하지 않고 run이 종료됐다.

## Quest Sequence Contract

P0 최소 contract는 scenario data의 `quest_sequence`이다.

```yaml
quest_sequence:
  - survive_the_storm_pass
  - hidden_grove_discovery
```

`active_quest_id`는 sequence 첫 quest여야 한다. Validation에서 sequence 내 quest id가 로드 가능한지도 확인한다.

## 추가/사용한 Quest Sequence

새 quest/card는 추가하지 않았다.

기존 content를 재사용했다.

- quest 1: `survive_the_storm_pass`
- quest 2: `hidden_grove_discovery`
- quest 2 event 후보: `hidden_grove_hint`, `hidden_grove_followup`

## Quest Transition Lifecycle

다음 quest가 있을 때:

```text
quest_success
=> reward_granted
=> quest_transition true
=> previous_quest_id recorded
=> next_quest_id recorded
=> next_required_objective_ids recorded
=> next_quest_onboarding true
=> run loop continues with next foundation
```

다음 quest가 없을 때:

```text
quest_success
=> reward_granted
=> no_next_quest true
=> run_complete true
=> clean stop
```

## Reward / 중복 방지 유지

기존 reward tag 방식은 유지했다.

- reward tag: `quest_reward:<quest_id>`
- quest 1 reward와 quest 2 reward는 각각 1회 지급
- duplicate reward detected: 0
- reward missing after success: 0

## Next Quest Onboarding Trace

Manual trace에서 onboarding은 두 번 확인된다.

- turn 1: `survive_the_storm_pass`, `onboarding_reason: run_start`
- turn 4: `hidden_grove_discovery`, `onboarding_reason: quest_transition`

Transition lifecycle entry에는 아래 필드가 기록된다.

- `quest_transition`
- `previous_quest_id`
- `next_quest_id`
- `transition_reason: quest_success`
- `next_required_objective_ids`
- `previous_quest_completed_objective_ids`
- `next_quest_onboarding`

## Required Objective Refresh

Run loop는 transition 후 `load_foundation(next_quest_id)`로 foundation을 교체한다.

그 결과 다음 turn의 trace에서:

- `active_quest_id: hidden_grove_discovery`
- `required_objective_ids: find_hidden_grove, map_grove_path, report_hidden_grove, survive_expedition`

가 기록된다.

## Presented Cards Refresh

Card selection context는 매 turn 현재 `foundation.quest`를 사용한다. Transition 후 foundation이 `hidden_grove_discovery`로 바뀌기 때문에 다음 turn의 card pool과 relevance도 새 quest 기준으로 생성된다.

Goal-focused manual run에서 transition 직후 presented cards는 `hidden_grove_discovery` quest ids를 가진 card로 refresh됐다.

## Previous Quest Stale Card 방지

Trace relevance에 `card_quest_ids`를 추가했다. Batch summary는 transition 이후 이전 quest id가 포함된 presented card를 `stale_previous_quest_card_after_transition_count`로 집계한다.

Smoke batch 결과:

```text
stale_previous_quest_card_after_transition_count: 0
```

## Smoke Batch 실행 결과

- seeds: `202-206`
- agents: `goal_focused`, `safety_first`, `risk_seeking`, `explorer`, `contrarian`
- total runs: `25`
- max_turns: `25`
- quest completion count: `30`
- reward granted count: `30`
- quest transition count: `15`
- next quest onboarding count: `15`
- no_next_quest count: `15`
- run_complete count: `15`
- reward missing after success count: `0`
- duplicate reward detected count: `0`
- stale previous quest card after transition count: `0`
- min-turn blocked count: `0`
- crash count: `0`
- invariant violation count: `0`
- same-turn duplicate count: `0`
- fallback warning count: `0`
- off-quest warning count: `226`

Output:

- `out/quest_sequence_transition_smoke_v0.1/batch_summary.json`
- `out/quest_sequence_transition_smoke_v0.1/batch_report.md`
- `out/quest_sequence_transition_smoke_202_206_v0.1.md`

Raw per-run directories were removed after aggregate evidence was generated.

## Seed 202 Baseline 변화 여부

변경됨. 의도된 변화다.

이전 기준:

```text
survive_the_storm_pass success
=> reward
=> no_next_quest/run_complete
=> 3 turns
```

새 기준, autoplayer balanced seed 202:

```text
survive_the_storm_pass success
=> reward
=> quest_transition hidden_grove_discovery
=> hidden_grove_discovery success
=> reward
=> no_next_quest/run_complete
=> 8 turns
=> ending prepared_frontier_route
```

확인값:

- result_type: `success`
- ending: `prepared_frontier_route`
- turn_count: `8`
- quest_ids: `survive_the_storm_pass` then `hidden_grove_discovery`
- transition_count: `1`
- reward_count: `2`
- final_completed_quest: `hidden_grove_discovery`
- run_complete: `true`
- no_next_quest: `true`
- completion_blocked_by_min_turns: `false`

## 기존 Gate Regression 유지 여부

- Manual Choice Runner Robustness Gate: PASS
- Completed Objective Choice Refresh Gate: PASS
- Quest Onboarding Flow Gate: PASS
- Choice Relevance Noise Gate: PASS
- Manual Run Trace Report & Subagent Auto-Play Batch Gate: PASS
- Quest Completion Lifecycle & Reward Gate: PASS
- Subagent Batch Quality Baseline Gate v0.2 hard metrics preserved for smoke scope: crash 0, invariant 0, duplicate 0, min-turn blocked 0, reward missing 0, duplicate reward 0

## 추가 테스트

- `tests/test_quest_sequence_transition.py`
  - Standard Run이 최소 2개 quest sequence를 갖는지 검증
  - quest 1 success 후 quest 2 transition/reward/onboarding/required objective refresh 검증
  - transition 후 previous quest card stale presentation이 없는지 검증
  - 마지막 quest success 후 `no_next_quest/run_complete` 검증
- `tests/test_quest_completion_lifecycle.py`
  - sequence 기준으로 reward 2회, 각 quest reward 1회 검증
- `tests/test_manual_choice_runner_report.py`
  - report에 `Quest Transitions` 섹션 검증
- `tests/test_manual_choice_runner_batch.py`
  - next quest onboarding count / stale previous quest card count 검증

## 실행한 검증 명령과 결과

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_onboarding.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_relevance.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_report.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_batch.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_gameplay_run_card_candidates.py
```

- PASS: `8`, `3`, `2`, `2`, `3`, `12` tests.

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests/test_quest_sequence_transition.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_quest_completion_lifecycle.py
PYTHONPATH=src .venv/bin/python -m unittest tests/test_gameplay_run_standard_run.py
```

- PASS: `2`, `2`, `2` tests.

```bash
PYTHONPATH=src .venv/bin/python -m unittest
```

- PASS: 170 tests.

```bash
PYTHONPATH=src .venv/bin/python -m compileall src tools tests
```

- PASS.

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
```

- PASS: `VALIDATION: PASS`

```bash
PYTHONPATH=src .venv/bin/python tools/manual_choice_runner_batch.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seeds 202-206 --agents goal_focused,safety_first,risk_seeking,explorer,contrarian --max-turns 25 --output-dir out/quest_sequence_transition_smoke_v0.1 --report-md out/quest_sequence_transition_smoke_202_206_v0.1.md
```

- PASS: 25 runs.

Ontology/no-excuse checker:

- `tools/validate_ontology.py`: repo에 없음
- `tools/no_excuse_checker.py`: repo에 없음

## 남은 범위 밖 이슈

- 복잡한 branching quest graph는 구현하지 않았다.
- 후속 quest는 scenario-local linear sequence만 지원한다.
- `safety_first`와 `contrarian`은 여전히 objective progression을 피해서 failure/max_turn으로 갈 수 있다. 성공 강제 보정은 하지 않았다.
- off-quest warning은 관찰 지표로 남겼고, director/storylet tuning은 하지 않았다.

## Commit

- commit hash: pending
- working tree clean: pending
