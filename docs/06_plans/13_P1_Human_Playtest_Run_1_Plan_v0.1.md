# P1 Human Playtest Run 1 Plan v0.1

Status: `[Ready]`  
Date: 2026-07-01

## 문서 목적

이 문서는 P1 Human Playtest Scenario Pack 이후 첫 실제 human playtest를 바로 실행하기 위한 Run 1 준비 계획이다. 구현, 밸런스, 데이터, Text MUD 문구는 변경하지 않고, 기존 P0 playable baseline의 Standard Run evidence를 사람이 읽고 선택할 수 있는 테스트 단위로 고정한다.

## 기준 문서

- `docs/06_plans/12_P1_Human_Playtest_Scenario_Pack_v0.1.md`
- `docs/05_validation/18_Human_Playtest_Protocol_v0.1.md`
- `docs/05_validation/19_Human_Playtest_Feedback_Form_v0.1.md`
- `docs/05_validation/20_Human_Playtest_Run_1_Player_Sheet_v0.1.md`
- `docs/07_reviews/59_Human_Playtest_Run_1_Result_Template_v0.1.md`
- `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`

## Run 1 목표

Run 1의 목표는 P0 playable baseline이 실제 사람에게 다음 항목을 전달하는지 확인하는 것이다.

- Quest 목적을 잃지 않고 25턴 로그를 따라갈 수 있는가.
- 3-card 선택지가 단순 정답 고르기가 아니라 의미 있는 갈림길로 읽히는가.
- resource, clue, omen, reputation 변화가 플레이어에게 감지되는가.
- 반복 storylet이 테스트를 방해할 정도인지, 혹은 같은 사건군의 후속 전개로 받아들여지는지 확인한다.
- prepared_frontier_route ending과 Quest Report가 모험의 마무리처럼 읽히는지 확인한다.

## 선택한 Run

Run 1은 Primary run을 먼저 사용한다. 플레이 시간이 남거나 Primary run의 resource pressure가 너무 약하게 읽히면 Optional Secondary run을 이어서 사용한다.

| 역할 | Seed | Scenario | Profile | Quest | Turn | Ending | 목적 |
|---|---:|---|---|---|---:|---|---|
| Primary | 202 | `standard_run_25_35_turn` | `balanced` | `survive_the_storm_pass` | 25 | `prepared_frontier_route` | P0 baseline 직접 검증 |
| Optional Secondary | 101 | `standard_run_25_35_turn` | `balanced` | `survive_the_storm_pass` | 25 | `prepared_frontier_route` | resource_alternative 선택축 보조 검증 |

## Primary Run

Primary run은 seed 202를 사용한다. 이 run은 P0 playable milestone과 Resource Alternative Surface Gate 이후 baseline으로 쓰인 Standard Run이다.

Evidence:

- JSON: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run.json`
- Text MUD: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run_text_mud.txt`
- Summary: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run_summary.json`

Observed baseline:

- Turn count: 25
- 3-card presentation: all turns true
- Ending: `prepared_frontier_route`
- Result type: `success`
- Character outcome: `alive`
- Completed objectives: `find_storm_shelter`, `secure_survival_route`, `return_from_storm_pass`
- Unique event count: 11
- Resource alternative: candidate 79, presented 25, selected 1, selected turn 21
- Final state: health 8, food 3, money 17, reputation 5, curse 1

Primary run 선정 이유:

- P0 baseline을 그대로 읽히는 첫 human test로 사용한다.
- Standard Run 25 to 35 turn guard를 유지한다.
- prepared_frontier_route ending을 유지한다.
- resource_alternative가 최소 1회 실제 선택되어, 선택축이 완전히 사라진 run은 아니다.

## Optional Secondary Run

Optional Secondary run은 seed 101을 사용한다. Primary run과 같은 quest, scenario, ending을 유지하되 resource_alternative 선택이 2회 발생한다.

Evidence:

- JSON: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run.json`
- Text MUD: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run_text_mud.txt`
- Summary: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run_summary.json`

Observed baseline:

- Turn count: 25
- 3-card presentation: all turns true
- Ending: `prepared_frontier_route`
- Result type: `success`
- Character outcome: `alive`
- Completed objectives: `find_storm_shelter`, `secure_survival_route`, `return_from_storm_pass`
- Unique event count: 11
- Resource alternative: candidate 77, presented 25, selected 2, selected turns 17 and 21
- Final state: health 8, food 3, money 23, reputation 5, curse 1

Optional Secondary run 선정 이유:

- Primary run보다 resource_alternative 선택축이 더 분명하다.
- 같은 quest와 ending을 유지하므로 비교 부담이 낮다.
- 첫 human test가 baseline 이해 확인에만 머무를 경우, 두 번째 짧은 비교 읽기로 resource pressure를 확인할 수 있다.

## 플레이어 안내문

플레이어에게는 `docs/05_validation/20_Human_Playtest_Run_1_Player_Sheet_v0.1.md`만 전달한다. 진행자는 테스트 전에 아래 내용을 짧게 말한다.

```text
이 테스트는 완성된 게임 평가가 아니라 텍스트 모험 한 run이 읽히는지 확인하는 테스트입니다.
정답을 찾으려 하지 말고, 매 turn에서 실제로 고르고 싶은 선택지를 골라 주세요.
헷갈리거나 반복처럼 느껴지는 순간은 바로 표시해 주세요.
```

## 진행자 체크리스트

- Protocol 문서의 순서대로 소개, 플레이, 사후 질문을 진행한다.
- 플레이어에게 내부 score, event id, seed 선정 이유는 먼저 설명하지 않는다.
- Primary run을 먼저 사용한다.
- Optional Secondary run은 시간이 남거나 resource pressure 비교가 필요할 때만 사용한다.
- 플레이어의 선택 이유와 멈칫한 지점을 turn 단위로 기록한다.
- 실제 feedback은 `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`에 채운다.

## 관찰 지표

| 지표 | 관찰 질문 |
|---|---|
| Quest Purpose Continuity | 플레이어가 "왜 이 행동을 하는지"를 계속 이해하는가 |
| Choice Meaningfulness | 선택지가 서로 다른 비용, 위험, 기대를 가진 것으로 읽히는가 |
| Narrative Flow | turn log가 사건의 흐름으로 읽히는가 |
| Variety / Repetition | 반복 family가 지루함으로 느껴지는가, 후속 단서로 느껴지는가 |
| Ontology / Director Feel | 단서, 징조, 후속 사건이 상황에 반응하는 것처럼 보이는가 |
| Resource Pressure | health, food, money, reputation 변화가 선택에 영향을 주는가 |
| Ending / Quest Report Quality | ending과 report가 플레이 결과를 정리한다고 느껴지는가 |

## 기록 방식

- 플레이어 선택과 한 줄 이유는 Player Sheet에 기록한다.
- 진행자는 헷갈림, 반복감, 흥미 지점을 turn number와 함께 메모한다.
- 플레이 후 Feedback Form 항목을 채운다.
- 결과 문서는 `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`를 사용한다.

## 중단 조건

다음 조건 중 하나가 발생하면 run을 끝까지 강행하지 않고 중단 사유를 기록한다.

- 플레이어가 Quest 목적을 5턴 이상 연속으로 설명하지 못한다.
- 선택지 3개 중 무엇을 고르는지 판단할 정보가 없다고 반복적으로 말한다.
- 같은 사건이 버그처럼 반복된다고 명확히 판단한다.
- 로그 문장 이해가 어려워 선택 자체가 불가능하다.

## 완료 기준

- Primary run에 대해 최소 1명의 플레이어 선택 기록이 남는다.
- Feedback Form이 채워진다.
- Run 1 Result 문서가 `[Ready]`에서 실제 결과가 반영된 상태로 갱신된다.
- P0 baseline guard를 깨뜨리는 코드 또는 데이터 변경 없이 결과가 문서화된다.

## 다음 작업

다음 작업은 실제 사람 플레이 세션을 진행하고 `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`를 실측 feedback으로 채우는 것이다. 그 이후 별도 Findings Audit에서 반복감, 선택 의미, resource pressure 문제를 gameplay/data 변경 후보로 분리한다.
