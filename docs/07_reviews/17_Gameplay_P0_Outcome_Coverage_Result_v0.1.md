# [Current] Gameplay P0 Outcome Coverage Result v0.1

> 상태: [Current] Gameplay P0 Foundation의 success / partial_success / failure 결과 분기 검증 결과 문서.

## 1. 작업 목적

Gameplay P0 Foundation의 기존 success 중심 검증을 보강해 `success`, `partial_success`, `failure`가 실제 Console Simulator run에서 모두 발생하는지 확인했다.

이번 작업은 새 Gameplay Replan 구조 확장이 아니라, 기존 P0 수직 슬라이스의 결과 분기 커버리지를 보강하는 작업이다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/15_Content_Volume_Audit_Result_v0.1.md`
- `docs/07_reviews/16_Gameplay_P0_Foundation_Implementation_Result_v0.1.md`

## 3. 변경 파일

데이터:

- `data/scenarios/tutorial_herb_quest_partial.yaml`
- `data/scenarios/tutorial_herb_quest_failure.yaml`

코드:

- `src/fateweaver/gameplay_p0.py`

테스트:

- `tests/test_gameplay_p0.py`

문서:

- `docs/07_reviews/17_Gameplay_P0_Outcome_Coverage_Result_v0.1.md`

## 4. 결과 타입별 검증

### 4.1 Success

- Scenario: `data/scenarios/tutorial_herb_quest.yaml`
- JSON result_type: `success`
- Completed objectives: `collect_herbs`, `report_to_apothecary`
- Failed objectives: 없음
- Rewards: `money`, `reputation`, `score`, `unlock_quests`
- Text MUD Play Log: `결과 유형: success`와 성공 review text 출력 확인

### 4.2 Partial Success

- Scenario: `data/scenarios/tutorial_herb_quest_partial.yaml`
- JSON result_type: `partial_success`
- Completed objectives: `collect_herbs`
- Failed objectives: `report_to_apothecary`
- Rewards: 없음
- Text MUD Play Log: `결과 유형: partial_success`와 부분 성공 review text 출력 확인

부분 성공은 약초 수집 목표는 달성했지만 약사 보고를 완료하지 못한 run으로 검증한다.

### 4.3 Failure

- Scenario: `data/scenarios/tutorial_herb_quest_failure.yaml`
- JSON result_type: `failure`
- Completed objectives: 없음
- Failed objectives: `collect_herbs`, `report_to_apothecary`, `survive_expedition`
- Rewards: 없음
- Text MUD Play Log: `결과 유형: failure`와 실패 review text 출력 확인

실패는 Quest primary objective를 달성하지 못한 채 제한 turn에 도달하는 run으로 검증한다.

## 5. Score 차등 검증

결과별 score는 `data/core/score_rules.yaml`의 `ending_bonus`를 Quest Report score breakdown에 `outcome_adjustment`로 반영한다.

검증 결과:

| Outcome | Score | 주요 score_breakdown |
|---|---:|---|
| success | 127 | `outcome_adjustment: 30`, `ending_bonus: 20`, `quest_progress: 58` |
| partial_success | 51 | `outcome_adjustment: 10`, `quest_progress: 30` |
| failure | -11 | `outcome_adjustment: -20`, `quest_progress: 5` |

확인:

- `success > partial_success > failure`
- failure에는 음수 outcome penalty가 반영된다.
- partial_success는 success보다 낮은 보정과 무보상 상태로 구분된다.

## 6. Quest Report 검증

Quest Report는 outcome별로 다음 필드를 구분해 저장한다.

- `result_type`
- `completed_objectives`
- `failed_objectives`
- `score`
- `score_breakdown`
- `rewards`
- `review_text`

`tests/test_gameplay_p0.py`에서 세 outcome의 result_type, objectives, rewards, score ordering, failure penalty, Text MUD review text 출력을 함께 검증한다.

## 7. JSON / Text MUD Log 검증

검증 로그:

- Success JSON: `.omo/ulw-loop/outcome-coverage-20260630/evidence/logs-success/run_tutorial_herb_quest_balanced_42_20260630T002342236120Z_0001.json`
- Success Text: `.omo/ulw-loop/outcome-coverage-20260630/evidence/logs-success/run_tutorial_herb_quest_balanced_42_20260630T002342236120Z_0001.txt`
- Partial JSON: `.omo/ulw-loop/outcome-coverage-20260630/evidence/logs-partial/run_tutorial_herb_quest_partial_balanced_42_20260630T002342342661Z_0001.json`
- Partial Text: `.omo/ulw-loop/outcome-coverage-20260630/evidence/logs-partial/run_tutorial_herb_quest_partial_balanced_42_20260630T002342342661Z_0001.txt`
- Failure JSON: `.omo/ulw-loop/outcome-coverage-20260630/evidence/logs-failure/run_tutorial_herb_quest_failure_balanced_42_20260630T002342445033Z_0001.json`
- Failure Text: `.omo/ulw-loop/outcome-coverage-20260630/evidence/logs-failure/run_tutorial_herb_quest_failure_balanced_42_20260630T002342445033Z_0001.txt`

요약 증거:

- `.omo/ulw-loop/outcome-coverage-20260630/evidence/C004-outcome-summary.txt`

## 8. 실행한 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0.GameplayP0Tests.test_tutorial_herb_quest_cli_covers_success_partial_and_failure_outcomes
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/outcome-coverage-20260630/evidence/logs-success --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/outcome-coverage-20260630/evidence/logs-partial --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/outcome-coverage-20260630/evidence/logs-failure --profile balanced
```

## 9. 남은 문제

- failure scenario는 P0 outcome coverage용 최소 fixture이며, 아직 health 0, day 초과, 귀환 실패 같은 다양한 실패 원인을 모두 커버하지는 않는다.
- partial_success도 약초 수집 후 보고 실패 경로 1개만 검증한다.
- 전체 Quest 10개, Event 60개, Card 후보 150개 확장은 이번 작업 범위가 아니다.

## 10. 다음 추천 작업

1. failure reason을 `max_turn_exceeded`, `health_zero`, `return_failed`처럼 구조화한다.
2. partial_success 원인을 optional objective 실패, 보상 감소, 늦은 귀환 등으로 확장한다.
3. outcome별 score rule을 문서 스키마와 더 명시적으로 정렬한다.
