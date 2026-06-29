# [Current] Gameplay P0 Foundation Implementation Plan v0.1

> 상태: [Current] Gameplay Replan P0 Foundation 구현 전 계획 문서.

## 1. 문서 목적

이 문서는 Gameplay Replan의 P0 Foundation 구현 순서와 변경 범위를 정리한다.

P0는 전체 게임 완성이 아니다. P0의 목적은 기존 Console Validation 구조를 보존하면서, Quest 기반 Expedition이 최소 수직 슬라이스로 실제 실행될 수 있는 기반을 만드는 것이다.

## 2. 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/07_reviews/15_Content_Volume_Audit_Result_v0.1.md`

## 3. Content Volume Audit 요약

직전 감사 결과 기준 현재 명시 수량은 다음과 같다.

| 항목 | 현재 수량 | 목표 수량 | 상태 |
|---|---:|---:|---|
| Quest | 0 | 10 | MISSING |
| Tutorial Quest | 0 | 2 | MISSING |
| Region | 3 | 3 | READY |
| Storylet/Event | 28 | 60 | BELOW TARGET |
| Card/Choice Candidate | 86 | 150 | PARTIAL |
| Item | 12 | 25 | BELOW TARGET |
| Clue | 0 | 25 | MISSING |
| Omen | 0 | 20 | MISSING |
| Status/Resource | 5 | 8~12 | BELOW TARGET |
| Ending | 2 | 8 | BELOW TARGET |
| Event Chain | 명시 0 / 추정 24 | 12 | PARTIAL |

현재 데이터는 Event, Choice, Item 검증 재료는 있으나 Quest, Expedition Clock, Card Candidate Pool, Multi-Select, Score, Quest Report가 명시 구조로 존재하지 않는다.

## 4. P0 부족분 정의

P0에서 해결해야 할 부족분은 다음이다.

- Quest 없음
- Expedition Clock 없음
- 명시 Card Candidate / 3-Card Pool 없음
- Multi-Select 합성 규칙 없음
- Clue/Omen 실사용 필드 없음
- Score / Quest Report 없음

이 부족분은 단순 콘텐츠 수량 추가로 해결되지 않는다. 먼저 실행 구조가 Quest, Clock, Card, Result, Report를 연결해야 한다.

## 5. P0 구현 목표

P0 목표는 실게임형 전체 콘텐츠 확장이 아니라, 기존 데이터와 최소 신규 fixture를 이용해 Quest 기반 Expedition 1개가 Day/Turn 구조로 진행되는 최소 수직 슬라이스를 만드는 것이다.

P0 완료 시 기대 상태:

- Tutorial Quest 1개가 존재한다.
- Short Expedition이 Day / Turn / Time of Day를 가진다.
- 매 Turn 3장의 카드가 제시된다.
- 기본 1장 선택이 처리된다.
- 최소 1개 조건부 2장 조합이 처리된다.
- 선택 결과가 resource/status/score/quest_progress/next_event_tags에 반영된다.
- JSON Log와 Text MUD Play Log가 기존처럼 유지된다.
- Quest Report가 success / partial_success / failure 중 하나로 생성된다.
- 저주는 상태/위험 요소 중 하나로만 처리된다.

## 6. 구현하지 않을 것

P0에서는 다음을 하지 않는다.

- 전체 이벤트 60개 확장
- 전체 카드 후보 150개 확장
- 전체 Quest 10개 확장
- Tutorial Quest 2개 전체 완성
- Flutter UI 구현
- Flame 렌더링 구현
- 대규모 World Bible 작성
- 기존 데이터 전체 구조 갈아엎기
- 저주 중심 콘텐츠 확장
- 기존 Console Validation 로그 구조 제거

P0는 전체 게임 완성이 아니라 새 구조가 실제로 작동하는 최소 수직 슬라이스다.

## 7. P0 시스템 범위

### 7.1 Quest Layer

P0에서는 Tutorial Quest 1개만 도입한다.

권장 Quest:

```text
id: herb_gathering_tutorial
title: 약초 채집 의뢰
start_region: village
target_regions: [forest]
max_days: 3
max_turns: 12
```

최소 목표:

- 숲에서 약초 또는 동등한 quest item을 획득한다.
- 마을로 귀환하거나 보고 조건을 만족한다.
- 식량, 체력, 평판, 단서 중 일부가 결과 평가에 반영된다.

Quest는 단순 설명 텍스트가 아니라 Event/Card 후보 가중치에 영향을 줘야 한다.

### 7.2 Expedition Clock

P0에서는 Short Expedition만 지원한다.

```text
3 Day
4 Turn per Day
max 12 Turn
time_of_day: morning / afternoon / evening / night
```

Clock은 다음에 영향을 줘야 한다.

- 현재 Turn 표시
- time_of_day 표시
- max_days / max_turns 종료 조건
- 야간 위험 또는 귀환 판단 같은 후속 확장 지점

### 7.3 Storylet / Event Compatibility

기존 `events.yaml` 구조는 바로 폐기하지 않는다. P0에서는 기존 Event를 Storylet의 호환 source로 사용한다.

호환 원칙:

- 기존 Event `id`, `name`, `description`은 Storylet 표시 정보로 사용한다.
- `region_tags`는 Region Pool 필터로 사용한다.
- `event_tags`와 `danger_tags`는 후보 가중치와 risk hint의 입력으로 사용한다.
- 기존 Event 내부 `choices`는 초기 Card Candidate 재료로 사용한다.
- 기존 `event_weight`는 후속 후보 가중치로 유지하되, 직접 후속 사건을 뜻하는 `next_event_tags`와 분리한다.

### 7.4 Card Candidate Pool

P0에서는 기존 choice를 Card Candidate로 변환하는 adapter를 먼저 둔다.

Card Candidate 최소 필드:

- `id`
- `title`
- `description`
- `slot_role`
- `source_event_id`
- `choice_id`
- `requires`
- `effects`
- `risk_hint`

P0 슬롯 역할:

| Slot | 역할 | 예시 |
|---|---|---|
| A | Quest Progress | 약초를 찾는다 |
| B | Risk / Discovery | 수상한 흔적을 조사한다 |
| C | Resource / Alternative | 우회하거나 거래한다 |

### 7.5 3-Card Choice Selection

P0에서는 매 Turn 최종 3장 카드를 제시한다.

선정 규칙:

1. active quest와 current region에 맞는 Event 후보를 만든다.
2. Event 후보에서 Choice/Card 후보를 만든다.
3. slot_role 기준으로 A/B/C 역할을 우선 채운다.
4. 부족한 슬롯은 region 또는 fallback 카드로 채운다.
5. 동일 카드 반복을 줄이기 위해 최근 선택 history를 반영한다.

완료로 보지 않는 경우:

- 기존 Event 선택지 3개를 그대로 출력만 하는 경우
- 카드가 Quest, Region, State, Item, Clue, Omen, Economy 중 어떤 신호와도 연결되지 않는 경우

### 7.6 Multi-Select Resolver

P0에서는 2장 조합 1개 이상만 처리한다.

최소 규칙:

- `max_selected_cards: 2`
- combo rule 1개 이상
- conflict rule 1개 이상
- extra cost 1개 이상

예시:

```text
[횃불을 켠다] + [어두운 숲길을 조사한다]
=> food 또는 torch durability 비용을 내고 risk를 낮춘 뒤 clue 또는 quest_progress를 얻는다.
```

Multi-Select는 로그 표시만으로 끝나면 안 된다. 합성 결과가 resource/status/quest_progress/score/next_event_tags 중 하나 이상을 실제로 바꿔야 한다.

### 7.7 Clue / Omen 실사용 필드

P0에서는 Clue와 Omen을 대량 추가하지 않는다. 단, 실사용 필드가 0개인 상태는 벗어난다.

최소 목표:

- clue 1~2개
- omen 1개
- clue가 risk reveal 또는 card unlock에 영향을 주는 사례 1개
- omen이 danger/event candidate bias에 영향을 주는 사례 1개

후보 필드:

```text
gain_clues
gain_omens
requires_clue
requires_omen
reveals_risk_tags
next_event_tags
```

### 7.8 Score System

P0 Score는 Run Review용 최소 점수다.

최소 구성:

- quest_progress 점수
- survival 점수
- resource management 점수
- reputation 점수
- clue 발견 점수
- failure penalty

Score는 단순 숫자 증가가 아니라 Quest Report의 판단 근거로 쓰여야 한다.

### 7.9 Quest Report

P0 Quest Report는 Run 종료 시 생성된다.

필수 항목:

- `quest_id`
- `result_type`: success / partial_success / failure
- `completed_objectives`
- `failed_objectives`
- `final_state`
- `score`
- `review_text`

Text MUD Play Log에는 사람이 읽을 수 있는 Run Review로 출력한다. JSON Log에는 자동 검증 가능한 구조로 저장한다.

## 8. 데이터 변경 계획

이번 문서 작업에서는 data를 수정하지 않는다. 아래는 실제 구현 시 후보 파일이다.

| 후보 파일 | 작업 | 장점 | 단점 |
|---|---|---|---|
| `data/content/base/quests.yaml` | 신규 | Quest를 명시 source로 분리 | loader/schema 추가 필요 |
| `data/core/expedition_clock.yaml` | 신규 | 기본 clock preset 재사용 가능 | scenario별 override 규칙 필요 |
| `data/core/card_rules.yaml` | 신규 | slot, combo, conflict, cost를 중앙 관리 | P0에는 다소 추상적일 수 있음 |
| `data/core/score_rules.yaml` | 신규 | Score 계산 근거 분리 | result_rules와 역할 중복 위험 |
| `data/scenarios/tutorial_herb_quest.yaml` | 신규 | P0 검증 실행점 명확 | scenario가 Quest 대체물처럼 비칠 위험 |
| 기존 `events.yaml` 확장 | 수정 | 기존 데이터 재사용 쉬움 | 기존 Console Validation과 충돌 가능 |

권장 방향:

1. Quest와 Scenario는 분리한다.
2. Scenario는 active quest와 seed/run 설정만 지정한다.
3. 기존 Event는 유지하고, P0 adapter에서 Storylet/Card Candidate로 변환한다.
4. Score와 Card Rule은 P0에서는 작게 시작하되, 파일은 분리하는 방향을 우선 검토한다.

## 9. 실행 구조 변경 계획

실제 구현 시 실행 흐름은 다음 순서로 바꾼다.

1. content loader가 quest 데이터를 로드한다.
2. scenario가 active quest를 지정한다.
3. run state에 expedition clock을 초기화한다.
4. run state에 quest_progress, clues, omens, score를 초기화한다.
5. Situation Director가 quest / region / day / turn / state / item / clue / omen을 읽는다.
6. Storylet 후보를 region, quest bias, next_event_tags, recent history로 필터링한다.
7. Card 후보를 Event choice, quest action, item modifier, clue/omen modifier에서 만든다.
8. slot_role 기준으로 3장 카드를 선택한다.
9. 가능한 2장 조합을 계산해 Text MUD Play Log와 JSON Log에 남긴다.
10. selected card 또는 selected cards를 처리한다.
11. Result Engine이 resource/status/item/clue/omen/quest_progress/score를 갱신한다.
12. next_event_tags와 event_weight를 갱신한다.
13. turn/day/time_of_day를 진행한다.
14. 종료 조건을 검사한다.
15. quest report를 생성한다.
16. 기존 JSON Log와 Text MUD Play Log를 모두 저장한다.

## 10. 검증 계획

P0 구현 완료 후 최소 검증 기준:

- YAML/schema validation PASS
- Tutorial Quest scenario 실행 가능
- Run에 day/turn/time_of_day가 출력됨
- 매 Turn 3장 카드가 출력됨
- 1장 선택이 처리됨
- 2장 조합 선택이 최소 1개 처리됨
- combo/conflict/cost 중 최소 2개 이상 확인됨
- score가 계산됨
- quest report가 생성됨
- JSON Log와 Text MUD Play Log가 유지됨
- data 변경은 계획에 따른 신규/수정 파일로 제한됨

권장 seed/run 검증:

- seed A: quest_progress 우선 선택으로 success 또는 partial_success 확인
- seed B: risk/discovery 선택으로 clue/omen과 next_event_tags 변화 확인
- seed C: resource/alternative 선택으로 money/reputation/score 변화 확인

완료로 보지 않는 경우:

- 3회 run PASS만 있음
- JSON/Text 로그만 생성됨
- 카드가 3장으로 보이지만 ontology와 연결되지 않음
- Multi-Select가 실제 결과 합성 없이 로그에만 있음
- Score가 Run Review 의미 없이 숫자만 변함

## 11. 단계별 구현 순서

### Step 1. P0 데이터 계약 확정

- Quest 최소 필드 확정
- run_clock 최소 필드 확정
- Card Candidate 최소 필드 확정
- Multi-Select rule 최소 필드 확정
- score_rules와 quest_report 최소 필드 확정

산출물 후보:

- `data/content/base/quests.yaml`
- `data/core/card_rules.yaml`
- `data/core/score_rules.yaml`

### Step 2. Tutorial Quest fixture 추가

- `herb_gathering_tutorial` 1개 추가
- `village` 시작, `forest` 탐험, `village` 귀환 흐름
- 기존 Event/Item을 최대한 재사용
- 새 콘텐츠는 P0 검증에 필요한 최소량만 추가

### Step 3. Loader와 scenario 연결

- quest loader 추가
- scenario에 active quest 지정
- run state에 quest, clock, progress, score 필드 추가
- 기존 scenario와 Console Validation 호환성 확인

### Step 4. Situation Director 최소 구현

- quest / region / clock / state / item / clue / omen 입력 사용
- Storylet 후보군 생성
- 단일 최고 가중치 선택이 아니라 후보군 기반 선택 유지
- recent history 반복 완화 유지

### Step 5. Card Candidate Pool과 3장 선정

- 기존 choice를 Card Candidate로 변환
- Quest / Risk / Resource 슬롯 채우기
- 매 Turn 정확히 3장 출력
- 카드별 위험/보상 판단 로그 출력

### Step 6. Multi-Select Resolver 추가

- 1장 선택 유지
- 2장 조합 1개 이상 처리
- combo/conflict/cost 적용
- 합성 결과가 실제 상태와 score에 반영되는지 검증

### Step 7. Result Engine 확장

- resource/status 변화 유지
- item/clue/omen 변화 추가
- quest_progress 반영
- score_changes 반영
- next_event_tags 반영

### Step 8. Quest Report와 로그 확장

- JSON Log에 quest, run_clock, presented_cards, selected_cards, quest_report 추가
- Text MUD Play Log에 Day/Turn/Time, Quest, 3장 카드, Multi-Select, Run Review 출력
- 기존 JSON 로그 저장 구조는 제거하지 않음

### Step 9. P0 검증 실행

- Tutorial Quest scenario 3개 seed/run 실행
- JSON Log와 Text MUD Play Log 모두 확인
- success / partial_success / failure 중 2개 이상 결과 확인
- Acceptance Gate 매핑표 갱신 또는 리뷰 문서 작성

## 12. Acceptance Gate 매핑

| Acceptance Gate 항목 | P0 대응 방식 | 상태 |
|---|---|---|
| Quest Layer 존재 | `herb_gathering_tutorial` 1개 도입 | Planned |
| Expedition Clock 존재 | day/turn/time_of_day/act/run limits 추가 | Planned |
| 표준 Run이 Day / Turn / Time of Day를 가짐 | P0 Short Expedition 3 Day / 4 Turn 구조 | Planned |
| 매 Turn 3장의 카드 제시 | slot_role 기반 3장 출력 | Planned |
| 1장 선택과 조건부 다중 선택 처리 | 기본 1장, 2장 combo 1개 이상 | Planned |
| resource/status/economy/reputation/score/quest_progress/next_event_tags 반영 | Result Engine 확장 | Planned |
| Situation Director가 Quest, Region, Day/Turn, State, Item, Clue, Omen, Economy, Reputation을 봄 | P0 입력 목록에 포함 | Planned |
| Weighted Candidate Pool이 후보군 기반으로 작동 | 기존 weight와 recent history를 유지하며 확장 | Planned |
| JSON Log와 Text MUD Play Log 유지 | 기존 로그를 제거하지 않고 필드 확장 | Planned |
| 저주는 상태/위험 요소 중 하나로만 다룸 | curse 전용 QA를 P0 메인 목표로 두지 않음 | Planned |

## 13. 위험 요소와 완화책

| 위험 | 영향 | 완화 |
|---|---|---|
| 기존 Console Validation 구조와 충돌 | 기존 검증 run이 깨질 수 있음 | 신규 구조는 P0 scenario 중심으로 추가하고 기존 scenario를 보존 |
| 단순 선택지 출력만 3장 카드로 포장될 위험 | Acceptance Gate 미통과 | slot_role, source, effects, risk_hint를 Card Candidate에 포함 |
| Multi-Select가 로그만 남을 위험 | 실제 게임성 검증 실패 | combo/conflict/cost가 Result Engine 결과를 바꾸게 함 |
| Quest가 목적 텍스트만 있고 Event Pool과 연결되지 않는 위험 | Quest Layer가 의미 없어짐 | quest event_bias와 objective progress를 Storylet/Card 후보에 연결 |
| Score가 단순 숫자만 될 위험 | Run Review 의미 없음 | score breakdown을 quest_report에 포함 |
| P0 범위가 과도해질 위험 | 구현이 콘텐츠 확장 작업으로 번짐 | Tutorial Quest 1개, 3 Day, max 12 Turn으로 제한 |
| 저주가 다시 메인 테마처럼 보일 위험 | 프로젝트 중심축 혼동 | curse는 status/risk 항목 중 하나로만 유지 |

## 14. 다음 작업 지시 후보

다음 구현 작업은 아래 범위로 시작하는 것이 적절하다.

```text
docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md를 기준으로
Project FateWeaver의 Gameplay Replan P0 Foundation 최소 수직 슬라이스를 구현한다.

범위:
- Tutorial Quest 1개
- Short Expedition 3 Day / 4 Turn
- Quest loader 또는 최소 Quest source
- Expedition Clock
- 기존 Event/Choice 호환 Card Candidate adapter
- 매 Turn 3장 카드 출력
- 1장 선택과 2장 Multi-Select 조합 1개 이상
- quest_progress / score / next_event_tags / quest_report
- JSON Log와 Text MUD Play Log 유지

금지:
- 전체 콘텐츠 볼륨 확장
- Flutter UI 구현
- Flame 렌더링 구현
- World Bible 대량 작성
- 기존 Console Validation 구조 대규모 변경
- 저주 중심 콘텐츠 확장
```
