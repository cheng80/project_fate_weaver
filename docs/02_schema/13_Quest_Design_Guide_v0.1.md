# FateWeaver Quest Design Guide v0.1

## 문서 목적

이 문서는 FateWeaver에서 Quest를 어떤 기준으로 설계해야 하는지 정리한 기준 문서다.

FateWeaver의 Quest는 긴 고정 스토리를 쓰기 위한 장치가 아니다.  
Quest는 플레이어에게 모험의 목적을 제공하고, Expedition Clock, 3-Card Choice, Multi-Select, Storylet/Ontology, Economy/Reputation/Score, Quest Report를 연결하는 **게임 구조 단위**다.

---

## 1. Quest의 정의

FateWeaver에서 Quest는 다음과 같이 정의한다.

```text
Quest = 플레이어가 왜 모험을 떠나는지 정하는 목적 프레임
Storylet/Event = 그 목적을 수행하는 중 만나는 상황
Card = 그 상황에서 할 수 있는 선택
Result = 선택의 대가와 다음 사건 변화
```

즉 Quest는 단순한 줄거리 요약이 아니라, 다음 요소를 연결하는 시스템이다.

```text
목적
+ 제한 시간
+ 지역
+ Objective
+ 3-Card 패턴
+ Storylet tag
+ 자원 변화
+ 성공 / 부분 성공 / 실패
+ 보상 / 해금
```

---

## 2. 좋은 Quest의 조건

| 기준 | 설명 |
|---|---|
| 목적이 명확함 | 무엇을 해야 하는지 한 문장으로 설명 가능해야 한다. |
| 장소가 있음 | village, forest, ruin 등 이동 목적이 있어야 한다. |
| 시간 제한이 있음 | Day / Turn 압박이 있어야 한다. |
| 성공/부분 성공/실패가 있음 | 단순 성공/실패가 아니라 결과 단계가 나뉘어야 한다. |
| 자원과 연결됨 | health, food, money, reputation, risk 등에 영향이 있어야 한다. |
| 카드 선택을 만듦 | 매 Turn 3장 카드 구성이 가능해야 한다. |
| 후속 사건을 만듦 | 결과가 next_event_tags 또는 다음 Quest에 영향이 있어야 한다. |
| 반복 플레이 변주가 있음 | 같은 Quest라도 매번 다른 사건이 나올 여지가 있어야 한다. |

---

## 3. Quest 기본 데이터 구조 예시

```yaml
id: forest_path_scouting_tutorial
title: 숲길 안전 조사
quest_type: scouting
rank: novice

start_region: village
target_regions:
  - forest

recommended_days: 3
max_days: 5

primary_objectives:
  - id: scout_forest_path
    type: discover_clue
    target: safe_forest_path
    required: true

  - id: return_to_village
    type: return_to_region
    target: village
    required: true

optional_objectives:
  - id: mark_dangerous_tracks
    type: optional_action
    progress_key: marked_dangerous_tracks
    required: false

failure_conditions:
  - type: health_lte
    value: 0
  - type: max_day_exceeded

rewards:
  money: 2
  reputation: 1
  score: 40

unlock_quests:
  - missing_porter_search_intro
```

---

## 4. Quest Type 기준

처음부터 복잡한 Quest를 만들기보다, 타입별 역할을 나눠야 한다.

| Quest Type | 핵심 플레이 | 좋은 용도 |
|---|---|---|
| `gathering` | 수집, 귀환, 자원 관리 | 튜토리얼 |
| `scouting` | 조사, 단서, 위험 판단 | 두 번째 튜토리얼 |
| `recovery` | 물건 회수, 선택 대가 | 경제/평판 도입 |
| `rescue` | NPC 구조, 시간 압박 | 부분 성공/실패 분기 |
| `delivery` | 이동, 위험 회피, 귀환 | Day/Turn 학습 |
| `investigation` | 단서 해석, 후속 사건 | 폐허/미스터리 |
| `escort` | 보호, 자원 소모, 평판 | 중급 Quest |
| `survival` | 일정 기간 버티기 | 위험/식량 압박 |
| `exploration` | 새 장소 발견 | 지역 확장 |
| `contract` | 보상 중심 위험 의뢰 | 돈/평판/선택 대가 |

---

## 5. 초반 Quest 설계 순서

### Quest 1. 약초 채집 의뢰

이미 P0에 존재하는 기본 튜토리얼 Quest다.

| 항목 | 역할 |
|---|---|
| 타입 | `gathering` |
| 학습 | 수집, 귀환, 식량, 카드 선택 |
| 주요 자원 | food, health, reputation |
| 선택 | 채집 / 조사 / 우회 / 도움 |
| 결과 | 성공 / 부분 성공 / 실패 |

---

### Quest 2. 숲길 안전 조사

다음으로 추가하기 좋은 Quest다.

| 항목 | 역할 |
|---|---|
| 타입 | `scouting` |
| 학습 | 단서, 징조, 위험 판단 |
| 주요 자원 | food, risk, reputation |
| 선택 | 표식 조사 / 발자국 추적 / 우회 / 귀환 |
| 결과 | 안전 경로 발견 / 위험 표시 / 조사 실패 |

이 Quest가 좋은 이유는 다음과 같다.

```text
약초 채집은 “수집과 귀환”을 가르치고,
숲길 안전 조사는 “단서와 위험 판단”을 가르친다.
```

---

### Quest 3. 실종된 짐꾼 수색

| 항목 | 역할 |
|---|---|
| 타입 | `rescue` |
| 학습 | 추적, 시간 압박, 부분 성공 |
| 주요 자원 | health, food, reputation |
| 선택 | 흔적 추적 / 야영 / 구조 / 포기 |
| 결과 | 구조 성공 / 단서만 발견 / 실종 확인 / 실패 |

---

### Quest 4. 상인의 잃어버린 짐 회수

| 항목 | 역할 |
|---|---|
| 타입 | `recovery` |
| 학습 | money, trade, reputation |
| 주요 자원 | money, reputation, risk |
| 선택 | 회수 / 일부 보관 / 상인과 협상 / 숨김 |
| 결과 | 돈 증가 / 평판 변화 / 후속 거래 해금 |

---

### Quest 5. 폐허 표식 조사

| 항목 | 역할 |
|---|---|
| 타입 | `investigation` |
| 학습 | clue, omen, ruin |
| 주요 자원 | risk, clue, item |
| 선택 | 문양 해석 / 횃불 사용 / 귀환 / 깊이 진입 |
| 결과 | 폐허 진입 해금 / 위험 증가 / 단서 획득 |

---

## 6. Quest마다 반드시 있어야 하는 3개 축

### 6.1 목적 축

플레이어가 이해할 수 있어야 한다.

좋은 예:

```text
숲길이 안전한지 확인하고 마을에 보고한다.
```

나쁜 예:

```text
숲에서 여러 사건을 경험한다.
```

---

### 6.2 압박 축

시간이나 자원이 줄어야 한다.

예시:

```text
Day 제한
Turn 제한
food 감소
health 위험
risk 증가
```

---

### 6.3 변주 축

매번 같은 진행이 아니어야 한다.

예시:

```text
다른 단서
다른 위험
다른 optional objective
다른 카드 후보
다른 partial_success 이유
```

---

## 7. Quest 제작 체크리스트

Quest 하나를 만들기 전에 아래 질문에 답해야 한다.

```text
1. 이 Quest의 한 문장 목표는 무엇인가?
2. 시작 지역과 목표 지역은 어디인가?
3. 제한 Day / Turn은 얼마인가?
4. 필수 Objective는 무엇인가?
5. 선택 Objective는 무엇인가?
6. 어떤 자원을 소모하게 하는가?
7. 어떤 보상을 주는가?
8. 어떤 3장 카드 패턴이 반복되는가?
9. 어떤 Storylet/Event tag가 필요한가?
10. success / partial_success / failure 조건은 무엇인가?
11. 다음 Quest 또는 다음 사건으로 무엇을 해금하는가?
```

---

## 8. Quest와 3-Card 구조 연결

각 Quest는 매 Turn 카드 슬롯을 만들 수 있어야 한다.

기본 카드 슬롯:

```text
A. Quest Progress
B. Risk / Discovery
C. Resource / Alternative
```

### 예: 숲길 안전 조사

| Slot | 카드 예시 |
|---|---|
| Quest Progress | 숲길 표식을 조사한다 |
| Risk / Discovery | 발자국을 따라간다 |
| Resource / Alternative | 식량을 아끼며 우회한다 |

### 예: 실종된 짐꾼 수색

| Slot | 카드 예시 |
|---|---|
| Quest Progress | 짐꾼의 흔적을 추적한다 |
| Risk / Discovery | 부서진 수레를 조사한다 |
| Resource / Alternative | 마을 사람에게 정보를 산다 |

---

## 9. Quest와 결과 분기 기준

Quest는 반드시 3가지 결과를 가져야 한다.

### Success

```text
필수 목표 완료
귀환 또는 보고 완료
생존
```

### Partial Success

```text
일부 목표만 완료
귀환은 했지만 목표 부족
보조 목표 실패
기한 초과 직전 귀환
보상 감소
```

### Failure

```text
체력 0
기한 초과
귀환 실패
필수 목표 전부 실패
```

---

## 10. 좋은 Quest 예시: 숲길 안전 조사

```yaml
id: forest_path_scouting_tutorial
title: 숲길 안전 조사
quest_type: scouting
rank: novice

start_region: village
target_regions:
  - forest

recommended_days: 3
max_days: 5
turns_per_day: 4

primary_objectives:
  - id: discover_safe_path
    type: discover_clue
    target: safe_forest_path
    required: true
    partial_reason: primary_partial
    failure_reason: primary_objective_failed
    score_key: discovery

  - id: return_to_village
    type: return_to_region
    target: village
    required: true
    failure_reason: report_failed
    score_key: report

optional_objectives:
  - id: mark_beast_tracks
    type: optional_action
    progress_key: marked_beast_tracks
    required: false
    failure_reason: optional_failed
    score_key: optional_action

  - id: keep_food
    type: keep_resource_at_least
    target: food
    value: 2
    required: false
    failure_reason: optional_failed
    score_key: resource_management

success_conditions:
  - discover_safe_path
  - return_to_village

rewards:
  money: 2
  reputation: 1
  score: 40

unlock_quests:
  - missing_porter_search_intro
```

---

## 11. Quest 추가 순서

Quest 추가는 아래 순서로 진행하는 것이 좋다.

### 단계 1. Tutorial Quest 2개

```text
herb_gathering_tutorial
forest_path_scouting_tutorial
```

목표:

```text
수집 / 조사 / 귀환 / optional objective / partial / failure
```

---

### 단계 2. Local Quest 3개

```text
missing_porter_search_intro
merchant_lost_pack_recovery
village_well_trouble
```

목표:

```text
rescue / recovery / economy / reputation
```

---

### 단계 3. Frontier Quest 3개

```text
ruin_mark_investigation_intro
old_hunter_trail_followup
forest_edge_camp_safety
```

목표:

```text
clue / omen / ruin / 위험 증가
```

---

### 단계 4. Dangerous Quest 2개

```text
sealed_ruin_entry
night_return_contract
```

목표:

```text
고위험 선택 / 강한 보상 / 실패 가능성
```

---

## 12. Quest 제작 우선순위

| 우선순위 | Quest | 이유 |
|---:|---|---|
| 1 | `forest_path_scouting_tutorial` | 현재 시스템 재사용성이 가장 좋음 |
| 2 | `missing_porter_search_intro` | rescue / partial_success 검증에 좋음 |
| 3 | `merchant_lost_pack_recovery` | money / reputation 도입에 좋음 |
| 4 | `ruin_mark_investigation_intro` | clue / omen / ruin 확장에 좋음 |
| 5 | `village_well_trouble` | village 지역 이벤트 확장에 좋음 |

---

## 13. Quest 작성 시 금지할 것

- 긴 고정 스토리부터 쓰지 않는다.
- 목적 없는 랜덤 이벤트 묶음으로 만들지 않는다.
- success / partial_success / failure 없이 만들지 않는다.
- 자원 변화 없이 만들지 않는다.
- 3-Card 패턴을 만들 수 없는 Quest는 보류한다.
- 저주를 메인 테마로 삼지 않는다.
- 특정 Quest 전용 하드코딩 reason을 늘리지 않는다.
- Objective Schema를 우회하지 않는다.

---

## 14. 최종 정리

FateWeaver의 Quest는 서사 문장으로 만드는 것이 아니라, 아래를 모두 연결하는 **게임 구조 단위**로 만든다.

```text
목적
+ 제한 시간
+ 지역
+ Objective
+ 3-Card 패턴
+ Storylet tag
+ 자원 변화
+ 성공/부분 성공/실패
+ 보상/해금
```

다음 실제 추가 Quest는 **`forest_path_scouting_tutorial`**이 가장 적합하다.
