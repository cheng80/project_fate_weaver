# Subagent Batch Quality Baseline Gate Result v0.2

## Status

DONE.

Quest Completion Lifecycle & Reward Gate 이후 기준으로 30 seeds x 5 deterministic agents, 총 150 runs의 Standard Run batch baseline을 실행했다. `max_turns: 25`는 완료 목표가 아니라 safety cap으로 적용했다.

## 수정 파일 목록

- `tools/manual_choice_runner_batch.py`
- `tools/manual_choice_runner_batch_report.py`
- `tests/test_manual_choice_runner_batch.py`
- `docs/07_reviews/71_Subagent_Batch_Quality_Baseline_Gate_Result_v0.2.md`
- `out/subagent_batch_quality_baseline_v0.2/batch_summary.json`
- `out/subagent_batch_quality_baseline_v0.2/batch_report.md`
- `out/subagent_batch_quality_baseline_202_231_v0.2.md`

Gameplay logic, balance, selection, director, ontology, data는 수정하지 않았다.

## v0.2로 재작성된 이유

이전 기준은 `min_turns_before_completion: 25`가 quest success를 지연하던 시기의 25-turn run을 전제로 했다. 현재는 required objectives가 satisfied되면 즉시 quest success/reward/run_complete로 종료하는 lifecycle이 기준이다.

따라서 이번 baseline은 25턴 완료를 목표로 보지 않고, completion/reward lifecycle이 여러 seed와 agent 정책에서 안정적으로 기록되는지 확인하는 품질 기준선이다.

## Baseline 측정 범위

- scenario: `data/scenarios/standard_run_25_35_turn.yaml`
- seeds: `202-231`
- agents: `goal_focused`, `safety_first`, `risk_seeking`, `explorer`, `contrarian`
- max_turns: `25` safety cap
- total runs: `150`

Batch output:

- summary: `out/subagent_batch_quality_baseline_v0.2/batch_summary.json`
- generated report: `out/subagent_batch_quality_baseline_v0.2/batch_report.md`
- requested report copy: `out/subagent_batch_quality_baseline_202_231_v0.2.md`

150개 per-run raw directory는 209MB라 커밋하지 않았다. Batch hard gate 판단과 문서 재검증에 필요한 aggregate JSON/Markdown만 남겼다.

## Batch Runner 보강

`tools/manual_choice_runner_batch.py`에 v0.2 baseline 문서화에 필요한 aggregate fields를 추가했다.

- seed range 입력: `202-231`
- optional report path: `--report-md`
- outcome / stop_reason distribution
- same-turn duplicate count
- no_next_quest count
- reward missing after success count
- duplicate reward detected count
- completed quest dragged to max_turn count
- completion turn distribution
- agent별 lifecycle/warning summary
- seed x agent matrix

## 전체 지표

| Metric | Value |
| --- | ---: |
| total runs | 150 |
| total seeds | 30 |
| total agents | 5 |
| max_turns | 25 |
| crash count | 0 |
| invariant violation count | 0 |
| same turn duplicate count | 0 |
| clean end count | 90 |
| clean error count | 49 |
| max_turn_reached count | 49 |
| quest success count | 90 |
| reward granted count | 90 |
| run_complete count | 90 |
| no_next_quest count | 90 |
| min-turn blocked count | 0 |
| average completion turn | 3.42 |
| min completion turn | 3 |
| max completion turn | 5 |
| average turns | 11.78 |
| min turns | 3 |
| max turns observed | 25 |

## Quest Lifecycle 지표

| Metric | Value |
| --- | ---: |
| quest_success count | 90 |
| quest_success missing count | 60 |
| reward_granted count | 90 |
| reward_missing_after_success count | 0 |
| duplicate_reward_detected count | 0 |
| duplicate_reward_prevention count | 0 |
| run_complete count | 90 |
| no_next_quest count | 90 |
| next_quest_transition count | 0 |
| completion_blocked_by_min_turns count | 0 |
| completed quest dragged to max_turn count | 0 |

`next_quest_transition count`는 현재 P0 Standard Run에 후속 quest sequence data가 없으므로 0이 정상이다. 성공 run은 `no_next_quest: true`, `run_complete: true`로 clean end한다.

## Outcome / Stop Reason Distribution

Outcome distribution:

```text
success: 90
failure: 60
```

Stop reason distribution:

```text
completed: 90
max_turn_reached: 49
failure: 11
```

Completion turn distribution:

```text
turn 3: 60
turn 4: 22
turn 5: 8
```

## Agent Summary

| Agent | Runs | Outcomes | Stop reasons | Avg turns | Avg completion | Quest success | Reward | Run complete | Min-turn blocked | Off-quest warnings | Fallback warnings | Invariant violations | Crash |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| goal_focused | 30 | success 30 | completed 30 | 3.00 | 3.00 | 30 | 30 | 30 | 0 | 73 | 0 | 0 | 0 |
| safety_first | 30 | failure 30 | max_turn_reached 30 | 25.00 | 0.00 | 0 | 0 | 0 | 0 | 529 | 0 | 0 | 0 |
| risk_seeking | 30 | success 30 | completed 30 | 3.00 | 3.00 | 30 | 30 | 30 | 0 | 73 | 0 | 0 | 0 |
| explorer | 30 | success 30 | completed 30 | 4.27 | 4.27 | 30 | 30 | 30 | 0 | 111 | 0 | 0 | 0 |
| contrarian | 30 | failure 30 | failure 11, max_turn_reached 19 | 23.63 | 0.00 | 0 | 0 | 0 | 0 | 568 | 0 | 0 | 0 |

## Seed x Agent Matrix 요약

전체 matrix는 `batch_summary.json`의 `seed_agent_matrix`에 저장되어 있다.

Seed 202 matrix:

| Agent | Outcome | Stop reason | Turns | Completion turn | Quest success | Reward | Run complete | no_next_quest | Warnings | Invariant | Min-turn blocked |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | ---: | --- | --- |
| goal_focused | success | completed | 3 | 3 | true | true | true | true | 2 | pass | false |
| safety_first | failure | max_turn_reached | 25 | n/a | false | false | false | false | 14 | pass | false |
| risk_seeking | success | completed | 3 | 3 | true | true | true | true | 2 | pass | false |
| explorer | success | completed | 4 | 4 | true | true | true | true | 3 | pass | false |
| contrarian | failure | max_turn_reached | 25 | n/a | false | false | false | false | 22 | pass | false |

## Off-quest / Fallback Warning Summary

- off_quest_warning_count: `1354`
- fallback_warning_count: `0`

Soft observation:

- `safety_first`와 `contrarian`은 objective completion으로 이어지는 선택을 피하면서 safety cap 또는 failure로 종료되는 경향이 강하다.
- 두 agent의 off-quest warning이 높다: `safety_first=529`, `contrarian=568`.
- fallback warning은 0이므로 no-card fallback overuse가 아니라 agent policy와 active objective progression의 불일치가 주된 관찰점이다.

## Hard Gate 판정

PASS.

- crash count = 0
- invariant violation count = 0
- same turn duplicate presented card = 0
- unexpected no cards/no event/invalid state crash = 0
- min-turn blocked count = 0
- reward missing after quest_success count = 0
- duplicate reward detected count = 0
- completed quest dragged to max_turn count = 0
- completed objective stale choice regression = PASS
- quest onboarding trace regression = PASS
- choice relevance trace regression = PASS
- quest completion/reward lifecycle regression = PASS

## Seed 202 Autoplayer Baseline 유지 여부

PASS.

Autoplayer baseline은 focused/full unittest에서 유지된다.

현재 기준:

- result_type: `success`
- ending: `prepared_frontier_route`
- turn_count: `3`
- quest_success: true
- reward_granted: true
- completion_blocked_by_min_turns: false
- run_complete: true
- no_next_quest: true

## Regression 유지 여부

- Manual Choice Runner Robustness Gate: PASS
- Completed Objective Choice Refresh Gate: PASS
- Quest Onboarding Flow Gate: PASS
- Choice Relevance Noise Gate: PASS
- Manual Run Trace Report & Subagent Auto-Play Batch Gate: PASS
- Quest Completion Lifecycle & Reward Gate: PASS

## 추가 테스트 목록

- `tests/test_manual_choice_runner_batch.py`
  - batch summary에 v0.2 필수 지표가 포함되는지 검증
- seed range `202-203` 입력을 받는지 검증
- `--report-md` 경로에 Markdown report를 생성하는지 검증
- report에 quest lifecycle summary가 포함되는지 검증

## 실행한 검증 명령과 결과

```bash
PYTHONPATH=src .venv/bin/python tools/manual_choice_runner_batch.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seeds 202-231 --agents goal_focused,safety_first,risk_seeking,explorer,contrarian --max-turns 25 --output-dir out/subagent_batch_quality_baseline_v0.2 --report-md out/subagent_batch_quality_baseline_202_231_v0.2.md
```

- PASS: 150 runs completed, batch summary/report generated.

```bash
PYTHONPATH=src .venv/bin/python - <<'PY'
...
PY
```

- PASS: `BASELINE_GATE: PASS`
- 확인 항목: `total_runs=150`, `crash_count=0`, `invariant_violation_count=0`, `same_turn_duplicate_count=0`, `completion_blocked_by_min_turns_count=0`, `reward_missing_after_success_count=0`, `duplicate_reward_detected_count=0`, `completed_quest_dragged_to_max_turn_count=0`

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_batch.py
```

- PASS: 3 tests.

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
PYTHONPATH=src .venv/bin/python -m unittest
```

- PASS: 168 tests.

```bash
PYTHONPATH=src .venv/bin/python -m compileall src tools tests
```

- PASS.

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
```

- PASS: `VALIDATION: PASS`

```bash
PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs /tmp/fw_seed202_autoplayer --profile balanced
```

- PASS: result_type `success`, ending `prepared_frontier_route`, turn_count `3`, quest_success `true`, reward_granted `true`, completion_blocked_by_min_turns `false`, run_complete `true`, no_next_quest `true`.

Ontology/no-excuse checker:

- `tools/validate_ontology.py` 없음
- `tools/no_excuse_checker.py` 없음

## 남은 범위 밖 이슈

- `safety_first` / `contrarian` policy가 quest objective progression을 피하는 경향은 이번 Gate에서 success로 보정하지 않았다.
- 현재 P0에는 후속 quest sequence가 없으므로 successful run은 `no_next_quest/run_complete`로 종료한다.
- off-quest warning이 높은 agent별 pattern은 다음 Director/agent-policy quality pass의 후보지만, 이번 Gate에서는 측정 기준선으로만 기록했다.

## Commit

- commit hash: pending
- working tree clean: pending
