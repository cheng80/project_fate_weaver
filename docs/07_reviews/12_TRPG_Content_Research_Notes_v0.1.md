# TRPG Content Research Notes v0.1

> 상태: [Historical] 이 문서는 과거 검토와 판단 기록을 보관하기 위한 문서다.

## 1. 문서 목적

이 문서는 FateWeaver의 다음 Content Expansion 단계 전에 사용할 콘텐츠 표본 추출 근거를 정리한다.

목표는 TRPG 자료를 그대로 이식하는 것이 아니라, 이벤트 중심 판타지 로그라이크인 FateWeaver에 맞는 추상 패턴으로 변환하는 것이다. 이 문서는 신규 이벤트, 아이템, 상태, pack을 만들기 전 "어떤 종류의 상황을 표본으로 뽑을 것인가"를 정하는 리서치 노트다.

이번 작업에서는 Python 구현, YAML 콘텐츠 추가, core schema 변경을 하지 않았다.

---

## 2. 저작권 및 차용 경계

이 문서는 아래 원칙을 따른다.

- 원문 설정, 고유명, 문장, 룰 텍스트를 직접 차용하지 않는다.
- 특정 TRPG의 세계관, 몬스터, 주문, 직업, 조직명을 FateWeaver 콘텐츠로 옮기지 않는다.
- 참고 자료의 절차와 설계 의도를 FateWeaver의 `상황 -> 선택 -> 대가 -> 다음 상태 변화` 구조로 추상화한다.
- 전투는 별도 전투 시스템으로 만들지 않고 일반 이벤트와 choice로 유지한다.
- 단서와 예고는 정답 공개가 아니라 다음 선택의 판단 재료로 사용한다.

---

## 3. 참고한 자료 목록

### 3.1 로컬 제공 자료

- `/Users/cheng80/Desktop/룰북/크툴루의부름_간편입문가이드.pdf`
  - 미스터리 도입, 조사 장면, 단서, 공포/정신적 압박, 생존형 결말 구조를 참고했다.
- `/Users/cheng80/Desktop/룰북/CoC 룰북 종합 v0.5.1.pdf`
  - 사건 목표, 단서 접근, 공포 압력, 위험한 전투, 지식의 양면성을 추상 패턴으로 참고했다.
- `/Users/cheng80/Desktop/룰북/D&D_베이직룰북.pdf`
  - 상황 제시, 행동 선언, 판정/결과, 탐험 시간, 자원 소모, 위험 조우, 함정/위험물 구조를 참고했다.

### 3.2 FateWeaver 내부 자료

- `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
- `docs/02_schema/09_Content_Ontology_Model_v0.1.md`
- `docs/06_plans/01_Content_Expansion_Implementation_Plan_v0.1.md`
- `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
- `data/core/ontology.yaml`

### 3.3 공개 자료

- The Alexandrian, Three Clue Rule: https://thealexandrian.net/wordpress/1118/roleplaying-games/three-clue-rule
- The Alexandrian, Node-Based Scenario Design: https://thealexandrian.net/wordpress/7949/roleplaying-games/node-based-scenario-design-part-1-the-plotted-approach
- Pelgrane Press, How I Prep Adventures in GUMSHOE: https://pelgranepress.com/2018/02/01/how-i-prep-adventures-in-gumshoe/
- Pelgrane Press, A Taxonomy of Investigations: https://pelgranepress.com/2023/03/08/a-taxonomy-of-investigations/
- Old-School Essentials SRD, Dungeon Adventuring: https://oldschoolessentials.necroticgnome.com/srd/index.php/Dungeon_Adventuring
- Old-School Essentials SRD, Encounters: https://oldschoolessentials.necroticgnome.com/srd/index.php/Encounters
- Old-School Essentials SRD, Hazards and Challenges: https://oldschoolessentials.necroticgnome.com/srd/index.php/Hazards_and_Challenges
- Necropraxis, Overloading the Encounter Die: https://necropraxis.com/2014/02/03/overloading-the-encounter-die/
- Necropraxis, Hazard System v0.2: https://necropraxis.com/2014/12/23/hazard-system-v0-2/
- All Dead Generations, A Structure for Classic Exploration: https://alldeadgenerations.blogspot.com/2021/10/a-structure-for-classic-exploration.html
- All Dead Generations, Time Risk Economy: https://alldeadgenerations.blogspot.com/2019/07/time-risk-economy-part-ii.html

---

## 4. TRPG에서 사건이 작동하는 기본 구조

TRPG 사건은 보통 아래 흐름으로 작동한다.

```text
상황 제시
-> 플레이어 의도 선언
-> 위험/불확실성 판단
-> 비용 또는 판정
-> 결과 서술
-> 다음 선택 조건 변화
```

FateWeaver에서는 이를 YAML 이벤트 단위로 축소한다.

```text
event.description: 지금 벌어진 상황
choices[].text: 플레이어가 취할 수 있는 의도
choices[].risk_level/type: 선택의 성격과 위험
choices[].requires_*: 선택 가능 조건
choices[].result: 비용, 보상, 상태 변화, 향후 이벤트 가중치 변화
```

핵심은 결과가 단발 보상으로 끝나지 않는 것이다. 좋은 사건은 다음 턴의 choice availability, status pressure, event weight, item usefulness 중 하나를 바꾼다.

---

## 5. CoC식 미스터리/생존/단서/공포 압력 패턴

CoC류 조사 구조에서 FateWeaver에 유용한 패턴은 "정답 맞히기"가 아니라 "불완전한 정보로 다음 위험을 고르는 구조"다.

### 5.1 미스터리 패턴

- 핵심 진실은 직접 공개하지 않고 여러 관찰 조각으로 나눈다.
- 한 단서가 막히면 진행이 멈추는 구조를 피한다.
- 단서는 장소, 물건, 증언, 반복 문양, 몸 상태, 소문, 실패한 번역, 훼손된 기록처럼 서로 다른 매체로 분산한다.
- 단서는 `무엇을 해야 하는가`보다 `무엇을 조심해야 하는가`를 알려줄 때 FateWeaver에 잘 맞는다.

### 5.2 생존 패턴

- 공포는 즉시 사망보다 선택 폭 감소, 비용 증가, 잘못된 보상 유혹으로 표현한다.
- 회피, 지연, 임시 봉합, 도구 사용, 후퇴가 모두 유효한 선택이어야 한다.
- 위험한 대면은 영웅적 승리보다 `피해를 줄이고 무엇을 얻어 나오는가`에 초점을 둔다.

### 5.3 공포 압력 패턴

- `curse` 같은 상태 위험은 단순 벌점이 아니라 앞으로의 사건 해석을 바꾸는 압력이어야 한다.
- 공포는 낮은 빈도의 큰 충격보다 작은 징후의 누적이 더 효과적이다.
- 설명되지 않은 현상은 다음 선택의 정보 부족을 만들고, 뒤늦은 확인은 이전 선택을 다시 해석하게 만든다.

---

## 6. D&D식 상황 제시/행동 선언/결과 서술 구조

D&D류 모험 구조에서 FateWeaver에 유용한 부분은 `GM이 장면을 제시하고, 플레이어가 의도를 선언하고, 결과가 다음 상태를 만든다`는 운영 절차다.

FateWeaver 변환 기준:

- 상황 제시: 이벤트 description은 배경 설명보다 현재 압박을 먼저 드러낸다.
- 행동 선언: choice text는 도구, 태도, 비용, 위험을 암시한다.
- 결과 서술: result는 status/item/event weight 중 하나 이상을 바꾼다.
- 시간 압력: 탐험 이벤트는 food, health, curse 같은 status, future weight로 지연 비용을 만든다.
- 조우: 적대/중립/기회가 섞인 event로 만들고, combat tag가 있어도 일반 choice로 해결한다.
- 함정/위험물: trigger, 대응 choice, 실패 비용, 우회 보상이 있어야 한다.

---

## 7. 탐험/사회적 교류/전투의 FateWeaver 변환 기준

### 7.1 탐험 이벤트

탐험 이벤트는 길 찾기보다 `자원과 정보의 교환`이어야 한다.

좋은 탐험 이벤트는 아래 중 최소 2개를 가진다.

- food/health 감소 또는 보존
- 다음 지역/위험 태그에 대한 단서
- item 사용으로 비용 전환
- event weight 변화
- 낮은 보상이지만 안전한 선택과, 큰 보상이지만 위험한 선택의 대비

### 7.2 사회적 교류 이벤트

사회적 이벤트는 단순 설득 성공/실패가 아니라 `태도, 평판, 돈, 정보, 의심`의 교환이어야 한다.

변환 기준:

- reputation 또는 money를 실제 선택 조건/결과와 연결한다.
- 뇌물, 위협, 도움 요청, 거래, 침묵 유지 같은 choice archetype을 섞는다.
- NPC는 이름/설정보다 기능이 중요하다. 예: 정보 제공자, 비용 청구자, 경고자, 유혹자, 배신 가능 중개자.

### 7.3 전투 이벤트

전투는 별도 루프가 아니라 일반 event/choice로 표현한다.

변환 기준:

- 공격 선택은 high risk / high reward가 될 수 있다.
- 방어, 도주, 도구 사용, 협상, 미끼 던지기가 모두 선택지가 될 수 있다.
- health 손실만 반복하지 않고 item 소모, 상태 위험 증가, reputation 변화, 향후 위험 감소를 섞는다.

---

## 8. 위험-보상 tradeoff 패턴

FateWeaver에 맞는 tradeoff는 숫자 손익보다 다음 선택의 모양을 바꿔야 한다.

| 패턴 | 비용 | 보상 | 좋은 사용처 |
|---|---|---|---|
| 안전한 손실 | food/money 소량 감소 | status/health 보존 | safe choice |
| 위험한 획득 | status/health 악화 | money/item/정보 획득 | greedy/risky choice |
| 도구로 비용 전환 | item 소모 | health/status 피해 감소 | item-based choice |
| 지연 비용 | food 감소 또는 event weight 악화 | 더 많은 정보 | exploration choice |
| 평판 거래 | reputation 변화 | 가격/정보/접근권 변화 | social choice |
| 생존 압박 | health/food 낮을 때 위험 감수 | food/health 회복 | desperate 상황 |

---

## 9. 아이템이 의미 있어지는 조건

아이템은 인벤토리에 있는 물건이 아니라 선택 구조를 바꾸는 관계여야 한다.

의미 있는 아이템 조건:

- 최소 1개 choice의 `requires_item` 또는 `requires_any_item`과 연결된다.
- 위험 완화, 정보 공개, 비용 전환, 보상 증폭 중 하나를 수행한다.
- 특정 danger/event tag에 대응하는 이유가 `counters_tags`로 설명된다.
- 반복 사용 시 항상 최적해가 되지 않도록 소모, 기회비용, 좁은 적용 범위 중 하나를 가진다.
- 같은 아이템이 서로 다른 이벤트에서 다른 방식으로 작동하면 pack 테마가 강해진다.

반대로 나쁜 아이템은 아래와 같다.

- 한 번도 선택지를 열지 않는다.
- 이름만 다르고 역할이 기존 아이템과 같다.
- 어떤 위험을 완화하는지 설명되지 않는다.
- 사용하면 항상 손해가 없어서 profile 차이를 덮는다.

---

## 10. 상태/status가 의미 있어지는 조건

상태는 UI 숫자가 아니라 선택 압력이다.

의미 있는 status 조건:

- choice availability에 영향을 준다.
- result로 증감한다.
- 낮거나 높을 때 선택 가중치가 달라진다.
- 하나 이상의 실패/위험/보상 구조와 연결된다.
- 기존 `health`, `food`, `money`, `reputation`, `curse`로 표현할 수 없을 때만 새 status를 만든다.

현재 단계에서는 새 status 추가를 보수적으로 유지한다. 대부분의 생존/공포/사회 압력은 기존 다섯 status와 item/requires/event weight로 표현할 수 있다.

---

## 11. Pack 테마가 살아나는 조건

Pack은 이벤트 파일 묶음이 아니라 반복되는 문법이어야 한다.

좋은 pack은 아래를 가진다.

- 반복되는 danger tag
- 그 위험을 일부 완화하는 item
- 같은 clue motif가 여러 이벤트에서 다른 기능으로 등장
- 안전 선택, 욕심 선택, 호기심 선택, 생존 선택이 모두 들어 있는 choice 분포
- 하나 이상의 bad tradeoff 유혹
- 반복 플레이에서 같은 사건도 다른 status/item 상태 때문에 다른 선택이 되게 하는 연결

Pack 테마는 설명 텍스트가 아니라 관계로 증명되어야 한다.

```text
event_has_danger_tag
choice_requires_item
item_counters_tag
result_modifies_status
result_changes_event_weight
```

---

## 12. FateWeaver에 적용 가능한 샘플링 원칙

1. 이벤트는 장면 요약이 아니라 압박이 있는 선택 단위로 샘플링한다.
2. 단서는 정답이 아니라 다음 선택의 판단 재료로 샘플링한다.
3. 아이템은 수집품이 아니라 선택 비용을 바꾸는 장치로 샘플링한다.
4. 상태는 분위기 값이 아니라 이후 선택을 바꾸는 압력으로 샘플링한다.
5. 위험은 피해량이 아니라 회피/감수/전환/지연 중 어떤 결정을 요구하는지로 샘플링한다.
6. 보상은 즉시 이득과 향후 선택권을 구분해 샘플링한다.
7. Combat은 별도 시스템이 아니라 `combat` tag가 붙은 일반 이벤트로 샘플링한다.
8. Pack은 고유명/설정이 아니라 반복되는 위험, 단서, 아이템 상호작용 문법으로 샘플링한다.
9. 한 이벤트 안에는 최소 2개 이상의 실질 선택을 둔다.
10. 새 콘텐츠는 Ontology-lite relation으로 설명 가능해야 한다.

---

## 13. 현재 한계

- 이번 리서치는 문서화 단계이며 실제 콘텐츠 수를 늘리지 않았다.
- 현재 이벤트 풀이 작기 때문에 profile별 선택 차이는 콘텐츠 확장 이후 다시 검증해야 한다.
- 로컬 PDF 자료는 저작권 경계 때문에 직접 인용하지 않고 추상 패턴만 사용했다.
- 외부 자료도 FateWeaver의 자동 플레이/로그 구조에 맞게 다시 검증해야 한다.
