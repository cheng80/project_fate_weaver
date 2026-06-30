# [Current] Gameplay P0 Result Reason Coverage Result v0.1

> 상태: [Current] Gameplay P0 Foundation의 `partial_success` / `failure` reason 구조화와 검증 보강 결과 문서.

## 1. 작업 목적

Gameplay P0 Foundation의 결과 타입 검증을 `success`, `partial_success`, `failure` 수준에서 멈추지 않고, 부분 성공과 실패의 원인이 Quest Report, JSON Log, Text MUD Play Log에 구조적으로 남는지 확인했다.

이번 작업은 새 Gameplay Replan 구조 확장이 아니라, 기존 P0 수직 슬라이스의 결과 판단 근거를 보강하는 작업이다. 저주는 중심 테마가 아니라 체력, 식량, 돈, 평판과 함께 관리되는 상태/위험 요소 중 하나로만 유지했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/16_Gameplay_P0_Foundation_Implementation_Result_v0.1.md`
- `docs/07_reviews/17_Gameplay_P0_Outcome_Coverage_Result_v0.1.md`

## 3. 변경 파일

데이터:

- `data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml`
- `data/scenarios/tutorial_herb_quest_failure_health_zero.yaml`

코드:

- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/text_mud_log.py`

테스트:

- `tests/test_gameplay_p0.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/07_reviews/18_Gameplay_P0_Result_Reason_Coverage_Result_v0.1.md`

## 4. Quest Report 보강

Quest Report에 다음 필드를 추가했다.

- `result_reason`
- `partial_reasons`
- `failure_reasons`
- `reward_status`

기존 필드인 `result_type`, `completed_objectives`, `failed_objectives`, `score`, `score_breakdown`, `rewards`, `review_text`는 유지했다.

## 5. Partial Success Reason Coverage

검증된 partial reason:

- `report_failed`
- `optional_failed`
- `return_late`
- `reduced_reward`
- `primary_partial`

검증 시나리오:

- `data/scenarios/tutorial_herb_quest_partial.yaml`
  - 약초 수집은 달성했지만 보고와 일부 보조 목표를 완료하지 못한 부분 성공.
- `data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml`
  - 약초를 일부 확보했지만 주 목표 수량과 보조 목표를 끝내지 못한 부분 성공.

## 6. Failure Reason Coverage

검증된 failure reason:

- `max_turn_exceeded`
- `return_failed`
- `primary_objective_failed`
- `health_zero`

검증 시나리오:

- `data/scenarios/tutorial_herb_quest_failure.yaml`
  - 제한 turn 안에 주 목표와 보고를 완료하지 못한 실패.
- `data/scenarios/tutorial_herb_quest_failure_health_zero.yaml`
  - 체력이 0인 상태에서 원정이 시작되어 즉시 실패.

## 7. JSON / Text MUD Log 검증

검증 로그:

- Success JSON/Text: `.omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-success/`
- Partial JSON/Text: `.omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-partial/`
- Partial Optional JSON/Text: `.omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-partial-optional/`
- Failure JSON/Text: `.omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-failure/`
- Health Zero Failure JSON/Text: `.omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-health-zero/`

요약 증거:

- `.omo/ulw-loop/result-reason-coverage-20260630/evidence/RED-result-reason-test.txt`
- `.omo/ulw-loop/result-reason-coverage-20260630/evidence/C004-result-reason-summary.txt`

Text MUD Play Log에는 `결과 이유`, `부분 성공 이유`, `실패 이유`, `보상 상태`가 출력된다.

## 8. 실행한 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0.GameplayP0Tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-success --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-partial --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-partial-optional --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-failure --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/result-reason-coverage-20260630/evidence/logs-health-zero --profile balanced
```

## 9. 검증 결과

- `VALIDATION: PASS` 5개 scenario 확인.
- Gameplay P0 test 2개 PASS.
- 전체 unittest 34개 PASS.
- partial reason 5종 확인.
- failure reason 4종 확인.
- 모든 검증 run에서 JSON Log와 Text MUD Play Log 쌍 생성 확인.
- Score breakdown은 기존 `outcome_adjustment`와 세부 점수 구성을 유지한다.

## 10. 남은 문제

- `max_day_exceeded`는 reason 후보로 구조를 열어 두었지만 별도 fixture로 검증하지 않았다.
- Result reason은 P0 tutorial quest 기준의 최소 규칙이며, 후속 Quest가 늘어나면 Quest objective schema와 더 직접 연결해야 한다.
- 이번 작업은 result reason coverage 보강이며, 전체 Quest 10개, Event 60개, Card 후보 150개 확장은 범위 밖이다.

## 11. 다음 추천 작업

1. Quest objective schema와 result reason mapping을 데이터 기반으로 분리한다.
2. `max_day_exceeded` 전용 scenario를 추가해 day 기반 실패도 회귀 검증한다.
3. 후속 P0+ 작업에서 reward status가 economy/reputation/score 선택 의미와 더 강하게 연결되는지 검토한다.
