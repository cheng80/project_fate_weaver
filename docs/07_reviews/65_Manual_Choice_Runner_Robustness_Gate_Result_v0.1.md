# [Current] Manual Choice Runner Robustness Gate Result v0.1

> 상태: [Current] Manual Choice-Driven Standard Run Runner가 다양한 유효 선택 패턴에서 crash 없이 cleanly continue/end 되는지 검증하고 최소 보강한 결과 문서.

## 1. 작업 목적

이번 작업은 manual runner의 목표를 "항상 성공"으로 바꾸는 작업이 아니다.

목표는 사용자가 `1`, `2`, `3` 중 어떤 유효 선택을 반복해도 runner가 Python exception, missing selected card, no cards, no event, invalid state, infinite loop 없이 계속 진행하거나 정상 종료하는 것이다.

이번 작업에서는 `data/`, gameplay scoring, balance, director, ontology, Text MUD 문구를 변경하지 않았다.

## 2. 변경 요약

변경한 실행 표면:

- `tools/manual_choice_runner.py`
- `tools/manual_choice_runner_types.py`
- `tests/test_manual_choice_runner.py`

Runner 보강:

- `--max-turns` CLI option 추가.
- JSON log와 summary에 `stop_reason` 추가.
- 기존 호환 필드 `manual_stop_reason` 유지.
- sequence exhaustion을 `choice_sequence_exhausted`로 clean stop 처리.
- max turn cap 도달을 `max_turn_reached`로 clean stop 처리.
- card slot 부족 예외를 runner boundary에서 clean error로 변환.

## 3. Stop Reason Contract

이번 gate에서 확인한 stop reason:

- `completed`
- `target_turn_reached`
- `choice_sequence_exhausted`
- `max_turn_reached`

`target_turn_reached`는 success 강제가 아니라 target turn까지 진행했으나 quest report가 failure/partial일 수 있는 정상 종료 상태다.

## 4. RED Evidence

현재 runner의 보강 전 실패 증거:

```text
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/red_current/red_proof.txt
```

RED 결과:

- `--max-turns 5`는 unrecognized argument로 실패했다.
- 성공 run도 `manual_stop_reason`이 빈 문자열이었다.

## 5. Valid Choice Pattern Matrix

Evidence:

```text
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/robustness_cli_matrix.txt
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/robustness_matrix.csv
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/trace_consistency_report.json
```

| Pattern | Exit | Turns | Result | Stop Reason | Trace |
|---|---:|---:|---|---|---|
| all ones | 0 | 25 | success | completed | PASS |
| all twos | 0 | 30 | failure | target_turn_reached | PASS |
| all threes | 0 | 30 | failure | target_turn_reached | PASS |
| alternating 1/2/3 | 0 | 28 | success | completed | PASS |
| reverse 3/2/1 | 0 | 30 | failure | target_turn_reached | PASS |

해석:

- 실패 outcome은 허용된다.
- 모든 유효 패턴에서 runner crash 없이 JSON/Text MUD/trace를 생성했다.
- 모든 produced turn에서 3-card가 유지됐다.

## 6. Edge / Safety Evidence

Evidence:

```text
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/edge_safety_report.txt
```

검증 결과:

- invalid choice `4`: exit 1, clear `MANUAL_RUNNER: ERROR`, no fake success output.
- choice sequence exhaustion: exit 0, `choice_sequence_exhausted`, 1 turn trace 유지.
- `--max-turns 5`: exit 0, `max_turn_reached`, 5 turns에서 clean stop.
- trace consistency report: PASS.

## 7. Autoplayer Baseline

Evidence:

```text
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/autoplayer_baseline.txt
```

Seed 202 Standard Run baseline:

- result_type: `success`
- ending_id: `prepared_frontier_route`
- turn_count: `25`
- card_counts: `[3]`
- `manual_choice_mode`: absent

즉 기존 autoplayer path는 manual runner 보강의 영향을 받지 않았다.

## 8. Verification

Evidence:

```text
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/focused_verification.txt
.omo/ulw-loop/evidence/manual-choice-runner-robustness-20260701/full_verification.txt
```

통과한 검증:

- `tests.test_manual_choice_runner`: 7 tests PASS.
- full unittest discover: 154 tests PASS.
- compileall: PASS.
- scenario validation: PASS.
- ontology validation: PASS.
- no-excuse checker: PASS.
- git diff check: PASS.

## 9. Scope Guard

이번 작업에서 하지 않은 것:

- success 강제 보정.
- card/event scoring 조정.
- resource/balance 조정.
- quest/event/card data 변경.
- ontology/director 조정.
- Text MUD 문구 polish.

## 10. Remaining P1 Issues

아래 문제는 runner robustness 문제가 아니므로 이번 gate에서 다루지 않았다.

- Quest onboarding 부재.
- completed objective 이후 stale choices.
- suspicious merchant relevance noise.

다음 권장 작업은 Quest Intro / Onboarding Gate다.
