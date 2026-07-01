# Manual Run Trace Report & Subagent Auto-Play Batch Gate Result v0.1

## Status

DONE.

Manual Choice Runner의 기존 sequence/file/interactive 동작은 유지하면서, 사람이 읽을 수 있는 trace report와 deterministic 5-subagent batch 실행 표면을 추가했다.

## 수정 파일 목록

- `tools/manual_choice_runner.py`
- `tools/manual_choice_runner_types.py`
- `tools/manual_choice_runner_agents.py`
- `tools/manual_choice_runner_report.py`
- `tools/manual_choice_runner_batch.py`
- `tests/test_manual_choice_runner_report.py`
- `tests/test_manual_choice_runner_batch.py`
- `docs/07_reviews/69_Manual_Run_Trace_Report_Subagent_Batch_Gate_Result_v0.1.md`

## Trace Report가 필요했던 이유

Manual runner trace는 onboarding, objective delta, relevance metadata를 이미 기록하고 있었지만 raw JSON 기준이라 playtest 결과를 빠르게 읽기 어려웠다. 특히 turn별 3-card presentation, selected slot/card, objective before/after/completed, resource delta, off-quest/fallback warning을 한 화면에서 감사하기 어려웠다.

## Report Generator 구현 방식

`tools/manual_choice_runner_report.py`를 추가했다.

- 입력: manual runner의 run JSON과 choice trace JSON
- 출력: Markdown report
- 섹션: Run Summary, Quest Onboarding, Turn Timeline, Warnings, Invariant Summary
- 결손 optional field는 `unknown`, `n/a`, `not_recorded`로 표시하고 crash하지 않도록 방어 처리

실제 표면 검증:

```bash
.venv/bin/python tools/manual_choice_runner.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --agent-policy goal_focused --max-turns 25 --output-dir /tmp/fw_manual_report_gate/run
.venv/bin/python tools/manual_choice_runner_report.py --run-json /tmp/fw_manual_report_gate/run/manual_seed_202.json --trace-json /tmp/fw_manual_report_gate/run/manual_seed_202_choice_trace.json --output /tmp/fw_manual_report_gate/manual_run_report.md
```

결과:

- `MANUAL_RUN_REPORT: /tmp/fw_manual_report_gate/manual_run_report.md`
- report에 `# Manual Run Trace Report`, `Run Summary`, `Quest Onboarding`, `Turn Timeline`, `relevance=...`, `manual_stop_reason` 포함 확인
- seed 202 / goal_focused / 25 turns / result `success` / stop_reason `completed`

## 5 Subagent Policy 설계

`tools/manual_choice_runner_agents.py`에 policy interface를 분리했다.

- `AgentDecisionContext`: presented cards, relevance metadata, selected history, turn
- `choose_agent_index(policy_id, context)`: slot 1/2/3 deterministic 선택
- `build_agent_context(...)`: manual runner의 card/candidate/state를 policy context로 변환

정책:

- Goal-Focused: required objective linkage, active quest linkage, quest_progress result 우선
- Safety-First: resource_alternative, health/food 회복, 낮은 risk 우선
- Risk-Seeking: score change, high risk, risk_discovery, 큰 상태 변화 선호
- Explorer: 반복 선택 penalty, relevance reason 다양성, turn 기반 slot 순환
- Contrarian: Goal-Focused가 낮게 평가할 선택을 선호하되 off-quest/fallback 과용은 제한

외부 OpenAI/Codex/LLM API 연결은 추가하지 않았다.

## Batch Runner 구현 방식

`tools/manual_choice_runner_batch.py`를 추가했다.

- 입력: scenario, seed list, agent list, max turns, output dir
- 내부 실행: 각 seed x agent 조합에 대해 `manual_choice_runner.py --agent-policy ...` 호출
- 출력:
  - `batch_summary.json`
  - `batch_report.md`
- 집계:
  - total runs
  - crash count
  - invariant violation count
  - outcome counts
  - agent별 average turns / stop_reason distribution / warning count
  - seed x agent run matrix

실제 표면 검증:

```bash
.venv/bin/python tools/manual_choice_runner_batch.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seeds 202 --max-turns 25 --output-dir /tmp/fw_manual_batch_gate
```

결과:

- total_runs: 5
- crash_count: 0
- invariant_violation_count: 0
- turns: `[25, 25, 25, 25, 25]`
- outcome_counts: `success=1`, `partial_success=2`, `failure=2`
- success 강제 보정 없이 agent 성향별 결과가 갈렸다.

## 추가한 테스트 목록

- `tests/test_manual_choice_runner_report.py`
  - report CLI가 Markdown 필수 섹션을 출력하는지 검증
  - optional trace field 결손 시 crash 없이 `unknown`/`not_recorded`를 출력하는지 검증
- `tests/test_manual_choice_runner_batch.py`
  - 5개 policy id와 valid slot 선택 검증
  - seed 202 x 5 agent batch가 summary/report를 생성하는지 검증

## 실행한 검증 명령과 결과

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_report.py tests/test_manual_choice_runner_batch.py tests/test_manual_choice_runner.py tests/test_manual_choice_runner_onboarding.py tests/test_manual_choice_runner_relevance.py tests/test_gameplay_p0_card_candidates.py
```

- PASS: 29 tests

```bash
PYTHONPATH=src .venv/bin/python -m unittest
```

- PASS: 165 tests

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

## Regression 유지 여부

Seed 202 autoplayer baseline:

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs /tmp/fw_seed202_baseline --profile balanced
```

- result_type: `success`
- ending: `prepared_frontier_route`
- turn_count: 25
- 3-card invariant: true

Completed objective stale choice regression:

- `tests/test_manual_choice_runner.py` PASS
- 기존 stale quest_progress card refresh/filter 테스트 유지

Quest onboarding trace regression:

- `tests/test_manual_choice_runner_onboarding.py` PASS
- Turn 1 onboarding marker, active quest id/title, required objective ids 유지

Choice relevance trace regression:

- `tests/test_manual_choice_runner_relevance.py` PASS
- presented card relevance metadata와 off-quest majority guard 유지

## 남은 범위 밖 이슈

- Batch runner는 deterministic local policy만 제공한다. 실제 Codex/LLM subagent 연결은 이번 Gate 범위 밖이다.
- Agent policy는 playtest coverage 준비용이며 balance/scoring/director 조정은 하지 않았다.
- Off-quest warning은 report/batch에서 관찰 가능하게 집계하지만, merchant/storylet relevance 자체 튜닝은 이번 Gate 범위 밖이다.

## Commit

- commit hash: pending
- working tree clean: pending
