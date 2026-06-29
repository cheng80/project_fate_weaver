# FateWeaver Game Structure Replan v0.1

> 상태: [Current] 현재 Gameplay Replan 작업의 기준 문서.

## 1. 문서 목적

이 문서는 FateWeaver의 게임 구조를 다시 정의한다.

현재까지의 Console Simulator는 YAML/schema 검증, JSON 로그 저장, Text MUD 로그 출력 검증 중심으로 발전했다. 그러나 최종 목표는 단순히 몇 회 실행하고 로그를 남기는 도구가 아니다.

FateWeaver의 목표는 **퀘스트 목적을 가진 모험가가 제한된 Day/Turn 안에서 3장의 카드를 선택하거나 조합하며, 온톨로지 기반 Situation Director가 던전 마스터처럼 계속 상황을 제시하는 텍스트 기반 생존/탐험 로그라이크**를 만드는 것이다.

---

## 2. 한 줄 정의

FateWeaver는 고정 스토리를 따라가는 게임이 아니라, Quest, Expedition Clock, Player State, Ontology Relation을 바탕으로 매 Turn 3장의 선택 카드를 제시하고, 플레이어의 선택 조합이 다음 사건과 생존 가능성을 바꾸는 DM형 텍스트 모험 게임이다.

---

## 3. 핵심 구조

```text
FateWeaver
├── Quest Layer
├── Expedition Clock
├── Ontology Layer
├── Situation Director
├── Storylet Pool
├── Card Candidate Pool
├── 3-Card Choice UI
├── Multi-Select Resolver
├── Result Engine
├── Economy / Reputation / Score System
└── Quest Report / Run Review
```

---

## 4. Quest Layer

Quest Layer는 모험의 목적을 제공한다.

플레이어가 단순히 숲, 폐허, 마을을 헤매는 것이 아니라, “왜 이 모험을 떠나는가”를 명확히 해야 한다.

### Quest가 제공해야 하는 것

- 주 목표
- 보조 목표
- 추천 일수
- 제한 일수
- 대상 지역
- 실패 조건
- 성공 / 부분 성공 / 실패 기준
- 보상
- 다음 퀘스트 해금 가능성
- 사건 가중치 변화

### 초반 퀘스트 예시

```text
약초 채집 의뢰

목표:
- 숲에서 달빛잎 약초 3개를 모은다.
- 마을로 돌아와 약사에게 보고한다.

보조 목표:
- 숲길의 이상한 표식을 조사한다.
- 부상자를 도울 수 있다.
- 식량을 2 이상 남긴다.

실패 조건:
- health <= 0
- day > 5
- 귀환 실패
```

---

## 5. Expedition Clock

FateWeaver는 명확한 시간/턴 구조를 가진다.

```text
1 Run = Expedition
1 Expedition = 여러 Day
1 Day = 여러 Turn
1 Turn = 하나의 상황 카드 선택
```

### 기본 기준

| 항목 | 기준 |
|---|---:|
| Standard Expedition | 5~7일 |
| 1 Day당 Turn | 4~6턴 |
| 1 Run 전체 Turn | 25~35턴 |
| Short Expedition | 12~15턴 |
| Long Expedition | 45~60턴 |

### 시간대

- morning
- afternoon
- evening
- night

시간대는 등장 사건, 위험도, 귀환 판단, 야영 이벤트에 영향을 준다.

---

## 6. Act 구조

Act는 고정 스토리 챕터가 아니다.

Act는 사건 종류, 위험도, 보상 수준, 자원 압박, 엔딩 접근도를 조절하는 진행 압력 단계다.

| Act | 역할 |
|---|---|
| Act 1 | 출발, 의뢰, 초기 징조 |
| Act 2 | 외곽 탐험, 첫 선택 결과 |
| Act 3 | 심층 진입, 단서와 위험 확대 |
| Act 4 | 자원, 평판, 상태 압박 |
| Act 5 | 귀환, 탈출, 성공, 실패, 결말 |

---

## 7. Ontology Layer

FateWeaver의 핵심은 온톨로지 기반 관계다.

각 데이터는 독립 목록이 아니라 서로 연결되어야 한다.

### 핵심 엔티티

- Quest
- Region
- Location
- Storylet/Event
- Card
- Choice
- Result
- Resource
- Status
- Item
- Clue
- Omen
- NPC/Faction
- Economy
- Score
- Ending

### 핵심 관계

| 관계 | 의미 |
|---|---|
| Quest → Region | 퀘스트가 주요 지역을 지정 |
| Quest → Event Bias | 관련 사건 가중치 증가 |
| Region → Storylet Pool | 지역별 사건 후보 |
| Storylet → Card Candidates | 사건이 카드 후보를 만듦 |
| Card → Result | 카드 선택이 결과를 만듦 |
| Result → Resource/Status | 체력, 식량, 돈, 피로 등 변화 |
| Result → Clue/Item | 단서나 아이템 획득/소모 |
| Result → Next Event Tags | 다음 사건 후보 변화 |
| Item → Card Unlock | 아이템이 카드 해금 |
| Clue → Risk Reveal | 단서가 위험 정보를 드러냄 |
| Omen → Danger Bias | 징조가 위험 사건 확률을 조정 |
| Money → Economy Action | 거래, 뇌물, 정보 구매 |
| Reputation → NPC Reaction | 도움, 할인, 거절, 구조 |
| Score → Run Review | 최종 평가 |

---

## 8. Situation Director

Situation Director는 FateWeaver의 던전 마스터다.

매 Turn마다 현재 상태를 읽고 다음 상황과 카드 후보를 만든다.

### 입력

- active quest
- day / turn / act / time_of_day
- region
- health / food / money / reputation / risk
- statuses
- items
- clues
- omens
- previous choices
- next_event_tags
- recent storylet memory

### 출력

- selected storylet
- 3 card candidates
- available multi-select combinations
- risk/reward hints
- expected result categories

---

## 9. Weighted Candidate Pool

가중치가 가장 높은 사건 하나만 선택하지 않는다.

현재 조건에 맞는 Storylet 후보군을 만들고, 가중치 Tier별로 여러 후보를 유지한다.

| Tier | 의미 |
|---|---|
| Critical | 퀘스트 필수, 위기, 후속 사건 |
| Strong | 현재 상황과 잘 맞음 |
| Normal | 일반 등장 가능 |
| Flavor | 분위기, 작은 변주 |
| Blocked | 등장 불가 |

같은 Tier 안에서는 랜덤성과 최근 반복 방지 규칙을 적용해 매 Run 다른 모험이 나오도록 한다.

---

## 10. 3-Card Choice UI

FateWeaver의 기본 선택 UI는 매 Turn 3장의 카드를 제시한다.

플레이어는 기본적으로 1장의 카드를 선택한다. 조건이 맞으면 2장 이상의 카드를 조합해 선택할 수 있다.

### 카드 슬롯 원칙

| 슬롯 | 역할 |
|---|---|
| A | 퀘스트 진행 |
| B | 위험 / 발견 |
| C | 보존 / 경제 / 우회 |

예시:

```text
[약초를 캔다]
[짐승 발자국을 조사한다]
[안전한 길로 우회한다]
```

---

## 11. Multi-Select Resolver

다중 선택은 단순 복수 선택이 아니다.

카드 간 combo, conflict, cost, unlock, risk_modifier 규칙을 처리해야 한다.

예시:

```text
[횃불을 켠다] + [폐허에 진입한다]
→ 위험 감소 후 진입
```

```text
[돈으로 정보를 산다] + [숲길을 조사한다]
→ 안전 경로 단서 획득
```

---

## 12. Choice / Card Composition

카드는 고정 선택지가 아니라 현재 상태에 따라 합성된다.

```text
최종 카드 후보 =
Quest 카드
+ Region 카드
+ Storylet 카드
+ Item 카드
+ Clue 카드
+ Omen 카드
+ Economy 카드
+ Reputation 카드
+ Status 카드
+ Time 카드
```

이 구조로 같은 사건이라도 보유 아이템, 단서, 피로, 돈, 평판, 시간대에 따라 다른 카드가 등장한다.

---

## 13. Result Engine

Result Engine은 카드 선택 결과를 처리한다.

처리 순서:

1. 선택 카드 유효성 검사
2. 충돌 여부 확인
3. 비용 선차감
4. modifier 카드 효과 적용
5. main action 카드 효과 적용
6. combo bonus / penalty 적용
7. resource/status/item/clue/reputation 갱신
8. score 갱신
9. next_event_tags 생성
10. day/turn 진행

---

## 14. Economy / Reputation / Score

### Money

Money는 단순 숫자가 아니라 선택지를 만든다.

- 거래
- 정보 구매
- 뇌물
- 치료
- 길잡이 고용
- 장비 구매
- 평판 행동

### Reputation

Reputation은 NPC 반응과 마을 기반 선택지에 영향을 준다.

- 도움
- 할인
- 구조
- 의심
- 거절
- 위험한 선택 강제

### Score

Score는 Run Review를 위한 평가 지표다.

```text
Run Score =
생존 보너스
+ 퀘스트 달성 점수
+ 탐험 점수
+ 단서 발견 점수
+ 사건 해결 점수
+ 자원 관리 점수
+ 평판 점수
+ 엔딩 보너스
- 부상/피로/저주/실패/무모한 선택 패널티
```

---

## 15. Curse Scope

저주는 메인 테마가 아니다.

저주는 health, food, money, reputation, risk, fatigue, injury와 함께 다루는 여러 상태/위험 요소 중 하나다.

문서와 콘텐츠는 저주 중심 게임으로 읽히지 않아야 한다.

---

## 16. 실게임형 목표

| 항목 | 목표 |
|---|---:|
| 퀘스트 | 최소 10개 |
| 튜토리얼 퀘스트 | 최소 2개 |
| 지역 | 3개 이상 |
| 지역별 Storylet | 최소 20개 |
| 전체 Storylet/Event | 최소 60개 |
| 전체 Card 후보 | 최소 150개 |
| 아이템 | 최소 25개 |
| 단서 | 최소 25개 |
| 징조 | 최소 20개 |
| 상태/자원 | 8~12개 |
| 엔딩 | 8개 이상 |
| 사건 체인 | 최소 12개 |
| 표준 Run 길이 | 25~35턴 |
