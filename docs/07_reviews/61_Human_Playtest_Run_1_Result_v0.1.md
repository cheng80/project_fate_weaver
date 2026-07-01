# Human Playtest Run 1 Result v0.1

Status: `[Aborted - Critical Findings]`
Date: 2026-07-01

## 테스트 개요

이 문서는 P1 Human Playtest Run 1의 Codex-facilitated 진행 결과를 기록한다. Run 1은 Turn 18에서 중단했다.

중단 사유:

- Quest 목적이 플레이 시작 시 충분히 고지되지 않았다.
- 사용자 선택과 관계없는 상인 storylet이 반복적으로 등장했다.
- 의뢰 해결 후에도 같은 의뢰 확인/보고/탐색 선택지가 계속 제시됐다.
- 진행자가 고정된 seed 202 autoplayer evidence를 재생해, 사용자의 실제 1/2/3 선택이 다음 턴 state transition을 구동하지 못했다.

판정:

- 이번 세션은 완성된 25턴 playtest evidence로 사용하지 않는다.
- 이번 세션은 Human Playtest Findings Audit의 critical finding evidence로 사용한다.
- 다음 interactive run 전에 manual choice-driven Standard Run runner가 필요하다.

## 사용한 Run

Primary run:

- Seed: 202
- Scenario: `standard_run_25_35_turn`
- Profile: `balanced`
- Quest: `survive_the_storm_pass`
- Turn count: 25
- Ending: `prepared_frontier_route`
- Result type: `success`
- Text MUD evidence: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run_text_mud.txt`
- JSON evidence: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run.json`
- Summary evidence: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/primary_run_summary.json`

Optional Secondary run:

- Seed: 101
- Scenario: `standard_run_25_35_turn`
- Profile: `balanced`
- Quest: `survive_the_storm_pass`
- Turn count: 25
- Ending: `prepared_frontier_route`
- Result type: `success`
- Text MUD evidence: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run_text_mud.txt`
- JSON evidence: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run.json`
- Summary evidence: `.omo/ulw-loop/evidence/p1-human-playtest-run-1-20260701/optional_secondary_run_summary.json`

## 플레이어 정보

To be filled after the session.

| 항목 | 기록 |
|---|---|
| 플레이어 ID | project owner |
| TRPG/Text adventure 경험 | not collected |
| 세션 날짜 | 2026-07-01 |
| 진행자 | Codex |
| 사용한 run | Primary seed 202, Codex-facilitated replay attempt |
| 총 소요 시간 | Turn 18에서 중단 |

## 진행 로그 요약

| 구간 | 관찰 요약 |
|---|---|
| Turn 1 to 5 | 폭풍 산길 피난처로 시작했지만, 약사/약초 의뢰 목적이 사전에 고지되지 않아 이후 약초 선택이 갑작스럽게 느껴질 수 있는 구조가 드러났다. |
| Turn 6 to 10 | 보급/정보/탐색 선택은 작동했지만, 수상한 상인과 영수증 계열 사건이 사용자 선택과 직접 연결되지 않은 반복처럼 보였다. |
| Turn 11 to 15 | 약초 확보와 귀환/보고가 진행됐지만, "의뢰 해결"의 의미가 플레이어에게 명확히 준비되지 않았다. |
| Turn 16 to 18 | 보고 이후에도 `약사에게 의뢰를 확인한다`, `약사에게 보고한다`, 반복 탐색 선택지가 다시 제시되어 stale choice 문제가 드러났다. |
| Turn 21 to 25 | 진행하지 않음. |
| Ending / Quest Report | 진행하지 않음. |

## 선택 패턴

| 항목 | Primary baseline | Player observed |
|---|---:|---|
| Quest progress 중심 선택 | 20 | 6 |
| Risk discovery 중심 선택 | 4 | 8 |
| Resource alternative 중심 선택 | 1 | 4 |
| Resource alternative 선택 turn | 21 | 6, 11, 17 |
| 헷갈림 표시 turn |  | 18 |
| 반복감 표시 turn |  | 7, 10, 16, 17 |

Optional Secondary baseline:

- Quest progress 중심 선택: 18
- Risk discovery 중심 선택: 4
- Multi-select 선택: 1
- Resource alternative 중심 선택: 2
- Resource alternative 선택 turn: 17, 21

## 피드백 요약

| 항목 | 플레이어 반응 |
|---|---|
| Quest Purpose Continuity | Fail. 사용자는 "의뢰가 처음에 약사에게 약초 전달인지도 고지도 안하고"라고 지적했다. |
| Choice Meaningfulness | Mixed. 개별 선택은 가능했지만, 해결 후 같은 선택이 반복되어 의미가 무너졌다. |
| Narrative Flow | Fail. 초반 폭풍 산길과 중반 약사/약초 의뢰가 자연스럽게 연결되지 않았다. |
| Variety / Repetition | Fail. 상인 storylet과 같은 선택지가 사용자의 답변과 무관하게 반복됐다. |
| Ontology / Director Feel | Fail. 현재 목표와 무관한 상인이 반복 등장해 director가 상황을 반응적으로 운영한다는 느낌이 약했다. |
| Resource / Economy / Reputation Pressure | Inconclusive. 돈/식량/체력 변화는 있었지만 narrative confusion이 먼저 발생했다. |
| Ending / Quest Report Quality | Not tested. Run was aborted before ending. |

## 문제점

| 우선순위 | 문제 | Evidence | 후보 후속 작업 |
|---|---|---|---|
| P0 | Codex-facilitated 방식이 실제 사용자 선택으로 state를 구동하지 못함 | 진행자가 seed 202 autoplayer log를 순차 재생했고, 사용자가 고른 번호가 다음 턴 event/card selection에 반영되지 않음 | `manual choice-driven Standard Run runner` 추가 또는 facilitator용 stateful run harness 작성 |
| P0 | Quest onboarding 부재 | 사용자 지적: "의뢰가 처음에 약사에게 약초 전달인지도 고지도 안하고" | Run 시작 전 quest objective/introduction surface 추가 |
| P0 | Quest 해결 후 stale choices | 보고 완료 후에도 의뢰 확인/보고/탐색 선택지가 계속 제시됨 | completed objective 이후 card candidate suppression/gating audit |
| P1 | 상인 storylet 반복 노이즈 | 사용자 지적: "답변과 상관 없는 상인은 계속 등장" | director/storylet relevance audit, repeat family timing review |

## 긍정적 반응

| 구간 | 반응 | 유지해야 할 점 |
|---|---|---|
| Turn 1 to 4 | 사용자는 번호 입력 방식 자체는 따를 수 있었다. | 플레이 중 피드백을 요구하지 않는 v0.3 입력 방식은 유지한다. |
| Turn 6, 11, 17 | resource_alternative 선택이 실제로 발생했다. | 자원 선택축은 유지하되, 실제 stateful runner에서 재검증한다. |
| N/A | 긍정 반응 수집은 중단으로 인해 제한적이다. | 다음 run은 ending까지 갈 수 있는 구조를 먼저 마련한다. |

## 개선 우선순위

| 우선순위 | 개선 후보 | Scope guard |
|---|---|---|
| P0 | Codex-facilitated manual runner: 매 turn 사용자의 `1/2/3` 선택을 실제 `apply_turn_result`와 다음 event/card selection에 반영한다. | gameplay behavior 변경이므로 별도 implementation task에서 검증 포함 |
| P0 | Quest intro/onboarding: 시작 전에 active quest 목적, 현재 의뢰자, 성공 목표를 spoiler 없이 표시한다. | Text MUD/facilitator surface 변경, ending 조건 노출 금지 |
| P0 | completed objective 후 stale card 제거: 이미 해결한 report/confirm/gather 계열 카드가 반복 제시되는지 gate audit한다. | quest_ids/requirements/cooldown hard block 우회 금지 |
| P1 | storylet relevance/repetition audit: 상인 family가 현재 quest state와 무관하게 반복되는 문제를 evidence로 분리한다. | 특정 event id disable 대신 repeat group/relevance 기준 검토 |

## 다음 액션

다음 액션은 `CODEX_TASK_P1_Human_Playtest_Findings_Audit_v0.1.md` 성격의 감사 작업이다. 감사에서 다음을 분리한다.

- facilitator 진행 오류: 고정 autoplayer log replay를 interactive playtest로 사용한 문제
- gameplay surface 오류: quest onboarding 부재
- card candidate 오류: 해결 후 stale choice 반복
- director/storylet 오류: 현재 목표와 무관한 상인 family 반복

감사 전까지 이번 세션은 25턴 completion evidence로 쓰지 않는다.
