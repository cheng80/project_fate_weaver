# [Current] Content Volume Audit Result v0.1

> 상태: [Current] Gameplay Replan 구현 전 현재 콘텐츠 볼륨과 구조 부족분을 감사한 결과 문서.

## 1. 감사 목적

현재 `data/`와 `docs/`가 Gameplay Replan 기준의 실게임형 텍스트 모험 시뮬레이터로 확장되기에 충분한지 확인한다.

이 감사는 구현 작업이 아니다. 새 Quest, Event, Card, Item, schema를 추가하지 않고, 현재 존재하는 YAML과 문서 기준으로 부족분을 드러내는 것이 목적이다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/07_reviews/14_Content_Volume_Audit_Template_v0.1.md`

## 3. 조사 대상 파일

- `data/content/base/endings.yaml`
- `data/content/base/events.yaml`
- `data/content/base/items.yaml`
- `data/content/base/regions.yaml`
- `data/content/packs/curse_pack/events.yaml`
- `data/content/packs/forest_pack/events.yaml`
- `data/content/packs/signal_grove_pack/events.yaml`
- `data/content/packs/signal_grove_pack/items.yaml`
- `data/core/choice_types.yaml`
- `data/core/item_roles.yaml`
- `data/core/ontology.yaml`
- `data/core/result_rules.yaml`
- `data/core/statuses.yaml`
- `data/core/tags.yaml`
- `data/scenarios/content_expansion_test.yaml`
- `data/scenarios/curse_balance_test.yaml`
- `data/scenarios/item_influence_test.yaml`
- `data/scenarios/mvp0_console_test.yaml`
- `docs/00_index/README_Docs_Index.md`
- `docs/01_foundation/`
- `docs/02_schema/`
- `docs/03_specs/`
- `docs/04_codex/`
- `docs/05_validation/`
- `docs/06_plans/`
- `docs/07_reviews/`

## 4. 전체 결론

### 4.1 현재 상태 요약

현재 데이터는 Console Validation 이후 확장된 이벤트/선택지/아이템 검증 데이터에 가깝다. Gameplay Replan이 요구하는 Quest Layer, Expedition Clock, 3-Card Choice, Multi-Select, Score/Quest Report 구조는 문서 목표와 스키마 초안에는 있으나, 실제 `data/`에는 아직 명시 구조로 존재하지 않는다.

현재 명시 수량은 Event 28개, Choice 86개, Item 12개, Region 3개, Ending 2개, Status/Resource 5개다. 기존 선택지는 Card 후보의 재료로 쓸 수 있지만, 아직 Card Candidate Pool이나 슬롯 역할 기반 3장 제시는 아니다.

### 4.2 가장 큰 부족분

- Quest 데이터가 없다.
- Day / Turn / Time of Day / Act를 가진 Expedition Clock 데이터가 없다.
- 명시 Card Candidate 구조와 3-Card Choice Pool이 없다.
- Multi-Select combo/conflict/cost 규칙이 없다.
- Clue/Omen 명시 콘텐츠가 없다.
- Score와 Quest Report가 현재 YAML 결과 구조에 없다.

### 4.3 바로 구현 가능한 영역

- 기존 Event 28개와 Choice 86개를 Storylet/Card 후보의 초기 재료로 재분류할 수 있다.
- `region_tags`, `event_tags`, `danger_tags`, `event_weight`는 Situation Director 후보군 구성의 초기 신호로 사용할 수 있다.
- `requires_item`, `requires_status`, item role, status 변화는 아이템/상태 기반 카드 해금의 초기 근거로 사용할 수 있다.
- health, food, money, reputation, curse 변화는 Result Engine의 최소 resource/status 변화로 이미 검증 가능하다.

### 4.4 구조 확장이 필요한 영역

- Quest YAML 또는 동등한 Quest source
- run_clock / expedition state
- Storylet과 Card Candidate 분리
- 3장 카드 슬롯 역할
- Multi-Select 규칙
- clue / omen / hazard / location 실사용 필드
- score_changes / quest_progress / quest_report

## 5. 콘텐츠 볼륨 현황

| 항목 | 현재 수량 | 목표 수량 | 상태 | 비고 |
|---|---:|---:|---|---|
| Quest | 0 | 10 | MISSING | 문서 스키마 초안은 있으나 실제 Quest YAML 없음 |
| Tutorial Quest | 0 | 2 | MISSING | 튜토리얼 Quest 구조 없음 |
| Region | 3 | 3 | READY | `forest`, `village`, `ruin` 존재 |
| Storylet/Event | 28 | 60 | BELOW TARGET | 현재는 Storylet이 아니라 Event YAML 구조 |
| Card/Choice Candidate | 86 | 150 | PARTIAL | 기존 `choices` 수량. 명시 Card Candidate는 없음 |
| Item | 12 | 25 | BELOW TARGET | base 6개, signal_grove_pack 6개 |
| Clue | 0 | 25 | MISSING | ontology에는 trial entity가 있으나 YAML 실사용 필드 0개 |
| Omen | 0 | 20 | MISSING | ontology에는 trial entity가 있으나 YAML 실사용 필드 0개 |
| Status/Resource | 5 | 8~12 | BELOW TARGET | `health`, `food`, `money`, `reputation`, `curse` |
| Ending | 2 | 8 | BELOW TARGET | 생존/실패 분기는 부족 |
| Event Chain | 명시 0 / 추정 24 | 12 | PARTIAL | `event_weight`가 있는 Event 24개. `next_event_tags` 명시 필드 0개 |

## 6. Region별 분포

Event가 여러 `region_tags`를 가질 수 있으므로 아래 수량은 중복 포함 수량이다.

| Region | 현재 Event 수 | 목표 Event 수 | 상태 | 비고 |
|---|---:|---:|---|---|
| forest | 26 | 20 | READY | 현재 콘텐츠가 forest에 크게 치우침 |
| ruin | 14 | 20 | BELOW TARGET | ruin 전용 밀도 부족 |
| village | 7 | 20 | BELOW TARGET | economy/reputation/NPC 반응을 만들기엔 부족 |
| common | 0 | 별도 목표 없음 | MISSING | 공용 이벤트 풀 구조 없음 |

현재 Region 분포는 forest 중심이다. `ruin`과 `village`는 태그가 붙은 이벤트가 있으나, Gameplay Replan 기준의 지역별 Storylet Pool로 보기에는 얕다.

## 7. Quest Layer 감사

상태: MISSING

문서에는 Quest Layer와 Quest Schema가 정의되어 있다. 그러나 현재 `data/`에는 Quest 파일, active quest, primary/optional objectives, recommended_days, max_days, quest reward, quest event_bias가 없다.

현재 시나리오 YAML은 테스트 입력과 필터 역할을 한다. Quest 목적을 가진 실게임 Run의 대체물로 보기 어렵다.

## 8. Expedition Clock 감사

상태: MISSING

문서에는 Day / Turn / Time of Day / Act가 요구된다. 현재 시나리오는 `target_turns`만 가진다. `day`, `turns_today`, `time_of_day`, `act`, `max_days`, `turns_per_day` 같은 명시 clock 구조는 없다.

따라서 현재 Run은 제한된 원정 시간이 아니라 일정 turn 수의 검증 실행에 가깝다.

## 9. 3-Card Choice 구조 감사

상태: PARTIAL

현재 Event는 평균 3개 안팎의 `choices`를 가진다. 전체 선택지는 86개다. 이 점은 Card 후보 재료로 사용할 수 있다.

하지만 현재 구조는 Event 내부 선택지 목록이다. Situation Director가 후보군을 만들고, 슬롯 역할에 따라 매 Turn 3장 카드를 고르는 구조는 없다. Quest 진행 / 위험 발견 / 보존 경제 우회 슬롯도 데이터로 분리되어 있지 않다.

## 10. Multi-Select 구조 감사

상태: MISSING

현재 `requires_item`, `requires_status`, `consume_item`, `result_pool`은 일부 존재한다. 그러나 다중 선택의 핵심인 combo, conflict, max_selected_cards, extra cost, 합성 결과 규칙은 없다.

따라서 현재 선택지는 조건부 해금은 가능하지만, 카드 2장 이상을 조합해 하나의 결과로 합성하는 구조는 아니다.

## 11. Economy / Reputation / Score 감사

상태: PARTIAL

`money`와 `reputation`은 status/resource로 존재하며 선택 결과에서도 변한다. 선택 결과 기준으로 `money`는 13개 choice, `reputation`은 15개 choice에서 변경된다. `trade` 타입 choice는 6개다.

그러나 money가 거래, 정보 구매, 치료, 고용, 뇌물 같은 economy action으로 체계화되어 있지는 않다. reputation도 NPC/faction 반응 구조와 직접 연결되어 있지 않다.

Score는 문서와 과거 AutoPlayer 분석에는 나오지만, Gameplay Replan의 `score_changes`, `quest_progress`, `quest_report` 구조로 현재 YAML에 존재하지 않는다.

## 12. Ontology 관계 감사

| 관계 | 상태 | 근거 | 필요한 작업 |
|---|---|---|---|
| Quest -> Region | MISSING | Quest 데이터 없음 | Quest source와 target_regions 추가 |
| Quest -> Event Bias | MISSING | Quest event_bias 없음 | Quest별 tag bias 추가 |
| Region -> Storylet/Event Pool | EXISTS | 모든 Event가 `region_tags` 보유 | Storylet Pool로 의미 재정렬 |
| Storylet/Event -> Card/Choice Candidate | PARTIAL | Event `choices` 86개 | Card Candidate 분리 또는 매핑 |
| Card/Choice -> Result | EXISTS | result 84개, result_pool 2개 | Card 결과 계약으로 정규화 |
| Result -> Resource/Status | EXISTS | `result.status` 61개 | `status_delta`/resource_changes 명칭 정렬 검토 |
| Result -> Item/Clue/Omen | PARTIAL | `add_item` 1개, `remove_item` 8개. clue/omen 0개 | clue/omen gain/reveal 필드 추가 |
| Result -> Next Event Tags | PARTIAL | `event_weight` 48개. `next_event_tags` 0개 | delayed tag와 direct next tag 구분 |
| Item -> Card Unlock | PARTIAL | `requires_item` 28개, unlock role item 4개 | item 기반 modifier card로 확장 |
| Clue -> Risk Reveal | MISSING | clue 실사용 필드 0개 | clue entity와 reveal/payoff 추가 |
| Omen -> Danger Bias | MISSING | omen 실사용 필드 0개 | omen tag와 hazard/danger 연결 추가 |
| Money -> Economy Action | PARTIAL | money 변화 13개, trade choice 6개 | economy action type 정의 |
| Reputation -> NPC Reaction | PARTIAL | reputation 변화 15개 | NPC/faction 반응 필드 추가 |
| Score -> Run Review | MISSING | `score_changes`와 quest report 0개 | score rule과 run review 결과 추가 |

## 13. 저주 비중 감사

상태: PARTIAL

`curse`는 현재 `health`, `food`, `money`, `reputation`과 함께 5개 status/resource 중 하나로 정의되어 있다. 선택 결과에서도 `curse`는 18개 choice에서 변화한다.

전체 Event 28개 중 9개가 id, name, description, event_tags, danger_tags 중 하나에서 curse를 포함한다. 전체 Choice 86개 중 23개가 curse 관련 표현이나 결과를 포함한다. 수량상 저주가 유의미하게 보이지만, 전체를 지배하는 단일 구조는 아니다.

혼동 위험은 남아 있다. `curse_pack`, `curse_balance_test`, `cursed_*` 명칭은 후속 작업자가 저주를 메인 테마로 오해할 수 있다. 현재 문서 기준으로는 `curse_balance_test`를 상태/위험 반영 보조 시나리오로 다루고 있으나, 데이터 경로명은 아직 legacy 상태다.

## 14. 우선순위별 부족분

### P0. 구현 전 반드시 필요한 것

- 최소 Quest source 추가
- Expedition Clock 구조 추가
- Event를 Storylet/Card 후보로 매핑하는 기준 추가
- 3-Card Choice 후보군 생성 기준 추가
- Result에 `quest_progress`, `score_changes`, `next_event_tags` 계열을 둘지 결정

### P1. 실게임형 Run을 위해 필요한 것

- Tutorial Quest 2개 이상
- 지역별 Storylet/Event 확장, 특히 `village`, `ruin`
- Multi-Select combo/conflict/cost/result 합성 규칙
- Economy action과 reputation reaction 구조
- Quest Report / Run Review 출력 구조

### P2. 콘텐츠 볼륨 확장을 위해 필요한 것

- 전체 Event 60개 이상
- 전체 Card/Choice 후보 150개 이상
- Item 25개 이상
- Clue 25개 이상
- Omen 20개 이상
- Ending 8개 이상
- named Event Chain 또는 `next_event_tags` 기반 후속 사건 구조

## 15. 다음 작업 제안

1. Quest / Expedition Clock / Card Candidate의 최소 YAML 계약을 확정한다.
2. 기존 Event 28개와 Choice 86개를 Storylet/Card 후보로 임시 매핑한다.
3. 3-Card Choice가 단순 선택지 3개 출력이 아니라 Quest/Region/State/Item/Clue/Omen/Economy 신호를 반영하도록 후보군 규칙을 만든다.
4. `event_weight`와 `next_event_tags`의 역할을 분리한다.
5. `curse_pack`과 `curse_balance_test`는 legacy 명칭으로 남기더라도 문서와 후속 migration 계획에서 상태/위험 보조 검증으로 계속 낮춰 표현한다.

## 16. 감사 결론

현재 프로젝트는 Gameplay Replan 구현을 시작할 재료는 있다. 하지만 Acceptance Gate를 통과할 구조는 아직 없다.

가장 큰 문제는 콘텐츠 수량 부족보다 구조 공백이다. Quest, Expedition Clock, 3-Card Choice, Multi-Select, Score/Quest Report가 먼저 잡히지 않으면, Event와 Item을 더 추가해도 실게임형 Run으로 검증하기 어렵다.

저주는 현재 상태/위험 요소 중 하나로 다룰 수 있지만, legacy pack/scenario 명칭 때문에 중심 테마로 오해될 위험은 계속 관리해야 한다.
