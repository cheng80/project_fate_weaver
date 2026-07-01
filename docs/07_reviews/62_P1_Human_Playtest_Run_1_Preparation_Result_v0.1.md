# P1 Human Playtest Run 1 Preparation Result v0.1

Status: `[Complete]`  
Date: 2026-07-01

## 작업 목적

P1 Human Playtest Scenario Pack 이후, 첫 human playtest를 바로 실행할 수 있도록 run selection, player sheet, result draft, preparation review, Text MUD/JSON evidence를 준비했다.

이번 작업은 문서와 evidence만 생성했다. `src/`, `data/`, `tests/`, `tools/`는 수정하지 않았다.

## 읽은 기준 문서

- `CODEX_TASK_P1_Human_Playtest_Run_1_v0.1.md`
- `docs/06_plans/12_P1_Human_Playtest_Scenario_Pack_v0.1.md`
- `docs/05_validation/18_Human_Playtest_Protocol_v0.1.md`
- `docs/05_validation/19_Human_Playtest_Feedback_Form_v0.1.md`
- `docs/07_reviews/59_Human_Playtest_Run_1_Result_Template_v0.1.md`
- `docs/05_validation/17_P0_Playable_Milestone_Checklist_v0.1.md`
- `docs/07_reviews/57_P0_Playable_Milestone_Freeze_Result_v0.1.md`

## 선택한 Run

Primary run:

- Seed: 202
- Scenario: `standard_run_25_35_turn`
- Profile: `balanced`
- Quest: `survive_the_storm_pass`
- Turn count: 25
- Ending: `prepared_frontier_route`
- Resource alternative selected count: 1
- Unique event count: 11

Optional Secondary run:

- Seed: 101
- Scenario: `standard_run_25_35_turn`
- Profile: `balanced`
- Quest: `survive_the_storm_pass`
- Turn count: 25
- Ending: `prepared_frontier_route`
- Resource alternative selected count: 2
- Unique event count: 11

선정 판단:

- seed 202는 P0 playable baseline을 직접 확인하는 Primary run으로 적합하다.
- seed 101은 같은 scenario와 ending을 유지하면서 resource_alternative 선택축을 더 많이 보여 주므로 Optional Secondary run으로 적합하다.

## 생성한 플레이어용 자료

- `docs/05_validation/20_Human_Playtest_Run_1_Player_Sheet_v0.1.md`

Player Sheet는 플레이어가 내부 seed, score, event id를 몰라도 선택 이유, 헷갈림, 흥미, 반복감을 기록할 수 있도록 구성했다.

## 생성한 결과 기록 문서

- `docs/06_plans/13_P1_Human_Playtest_Run_1_Plan_v0.1.md`
- `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`
- `docs/07_reviews/62_P1_Human_Playtest_Run_1_Preparation_Result_v0.1.md`

Run 1 Result 문서는 `[Ready]` 상태의 draft로 만들었다. 실제 플레이어 feedback은 아직 수집하지 않았으며, 이후 session에서 빈 항목을 채운다.

## P0 Baseline Guard

확인한 guard:

- Standard Run 25 to 35 turn 유지: seed 202와 seed 101 모두 25턴
- Ending 유지: 두 run 모두 `prepared_frontier_route`
- Quest 유지: 두 run 모두 `survive_the_storm_pass`
- 3-card presentation 유지: 두 run 모두 모든 turn에서 3개 선택지 제시
- Quest objectives 유지: 두 run 모두 `find_storm_shelter`, `secure_survival_route`, `return_from_storm_pass` completed
- Run failure 없음: 두 run 모두 `run_failed: false`
- 구현 변경 없음: `src/`, `data/`, `tests/`, `tools/` 수정 없음

## Simulator Output

Evidence root:

- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/`

Primary evidence:

- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run.json`
- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run_text_mud.txt`
- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run_summary.json`

Optional Secondary evidence:

- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run.json`
- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run_text_mud.txt`
- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run_summary.json`

Selection notes:

- `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/run_selection_notes.md`

## 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 101 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run --profile balanced
```

Verification commands are recorded in `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/verification.txt`.

## Evidence

Primary summary:

| Metric | Value |
|---|---:|
| Turn count | 25 |
| Unique event count | 11 |
| Resource alternative candidate count | 79 |
| Resource alternative presented count | 25 |
| Resource alternative selected count | 1 |
| Resource alternative selected/presented ratio | 0.04 |

Optional Secondary summary:

| Metric | Value |
|---|---:|
| Turn count | 25 |
| Unique event count | 11 |
| Resource alternative candidate count | 77 |
| Resource alternative presented count | 25 |
| Resource alternative selected count | 2 |
| Resource alternative selected/presented ratio | 0.08 |

## 실제 playtest 전 남은 작업

- 플레이어 1명을 정한다.
- `docs/05_validation/20_Human_Playtest_Run_1_Player_Sheet_v0.1.md`를 테스트 중 기록지로 사용한다.
- `docs/05_validation/18_Human_Playtest_Protocol_v0.1.md` 순서대로 session을 진행한다.
- session 후 `docs/05_validation/19_Human_Playtest_Feedback_Form_v0.1.md` 항목을 채운다.
- 실제 결과를 `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`에 반영한다.

## 다음 추천 작업

다음 추천 작업은 Human Playtest Run 1 Execution이다. 실제 플레이어 feedback을 수집한 뒤, 별도 Findings Audit에서 gameplay 변경 후보와 문서만으로 해결 가능한 issue를 분리한다.
