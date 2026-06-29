# Content Sampling Guide v0.1

## 1. 문서 목적

이 문서는 Content Expansion Phase 3부터 사용할 FateWeaver 콘텐츠 표본 추출 기준이다.

새 이벤트, choice, 아이템, status, pack을 만들기 전에 이 문서의 절차로 표본을 뽑는다. 목적은 "그럴듯한 문장"을 많이 쓰는 것이 아니라, Console Simulator에서 선택 차이와 로그 품질을 검증할 수 있는 관계형 콘텐츠를 만드는 것이다.

적용 기준:

```text
이벤트 = 상황 -> 선택 -> 대가 -> 다음 상태 변화
아이템 = 위험 완화 / 정보 공개 / 비용 전환 / 보상 증폭
상태 = 다음 선택을 바꾸는 압력
pack = 반복되는 테마/위험/보상 문법
combat = 일반 event/choice
```

---

## 2. 이벤트 추가 전 표본 추출 절차

새 이벤트를 쓰기 전에 아래 순서로 표본을 정한다.

1. Pack theme를 고른다.
2. 이번 이벤트의 primary pressure를 고른다.
3. 이벤트 archetype을 1개 고른다.
4. choice archetype을 최소 2개, 권장 3개 고른다.
5. threat archetype과 reward/cost archetype을 연결한다.
6. item interaction이 필요한지 판단한다.
7. clue/foreshadowing이 필요한지 판단한다.
8. status 변화가 다음 선택에 영향을 주는지 확인한다.
9. Ontology-lite relation으로 설명 가능한지 확인한다.
10. reject 기준에 걸리면 폐기하거나 다시 설계한다.

권장 최소 형식:

```text
theme:
primary_pressure:
event_archetype:
choices:
  - safe / cost / result
  - risky / cost / result
  - item_or_info / requirement / result
relations:
  - event_has_choice
  - choice_produces_result
  - result_modifies_status
```

---

## 3. Event Archetype 목록

| Archetype | 핵심 질문 | 권장 tag 성격 |
|---|---|---|
| threshold | 지금 넘어갈 것인가, 돌아갈 것인가 | exploration, danger |
| obstacle | 비용을 내고 통과할 것인가, 우회할 것인가 | exploration, survival |
| discovery | 발견한 정보를 해석할 것인가, 무시할 것인가 | mystery, exploration |
| omen | 아직 닥치지 않은 위험을 어떻게 받아들일 것인가 | hazard, mystery |
| bargain | 자원/평판/위험을 무엇과 교환할 것인가 | social |
| ambush | 즉시 피해를 줄일 것인가, 반격해 보상을 노릴 것인가 | combat |
| refuge | 쉬어 갈 것인가, 시간이 아까워 이동할 것인가 | survival |
| contamination | 오염이나 상태 악화를 감수하고 얻을 것인가 | hazard |
| trail fork | 어느 위험을 택해 다음 사건 풀을 바꿀 것인가 | exploration |
| aftermath | 이전 선택의 결과를 수습할 것인가, 이용할 것인가 | mystery, survival |

이 목록은 고정 enum이 아니다. 콘텐츠 표본을 뽑기 위한 작성 기준이다.

---

## 4. Choice Archetype 목록

| Archetype | 기능 | 일반 비용 | 일반 보상 |
|---|---|---|---|
| observe | 정보를 얻고 위험을 낮춘다 | food/time | clue, lower risk |
| press_forward | 빠르게 전진한다 | health/status risk | event progress, money |
| retreat | 큰 피해를 피한다 | opportunity loss | health/status 보존 |
| bargain | 사회적/경제적 비용을 낸다 | money/reputation | 접근권, clue |
| exploit | 위험한 이득을 노린다 | status/health | money/item |
| cleanse | 오염이나 위험을 줄인다 | item/money | 위험 상태 감소 |
| improvise | 도구 없이 임시 해결한다 | health/food | survival |
| item_use | 아이템으로 비용을 전환한다 | item consume/opportunity | damage prevention, clue |
| share/help | 타자와 협력한다 | resource/reputation | safety, future leverage |
| investigate | 단서를 깊게 본다 | time/food/status risk | mystery signal |

Choice는 `type`과 `risk_level`만으로 충분하지 않다. result가 실제로 archetype의 비용/보상을 보여줘야 한다.

---

## 5. Threat Archetype 목록

| Threat | FateWeaver 표현 | 좋은 대응 |
|---|---|---|
| attrition | food/health 점진 감소 | retreat, refuge, item_use |
| sudden harm | health 큰 감소 가능성 | observe, defend, item_use |
| status pressure | curse 같은 위험 상태 증가, future weight 악화 | cleanse, avoid, bargain |
| misinformation | 잘못된 판단 유도 | investigate, clue redundancy |
| social hostility | reputation/money 압박 | bargain, help, retreat |
| blocked path | 이동/진행 비용 증가 | tool, detour, risk |
| resource temptation | 위험한 보상 | exploit, safe alternative |
| delayed consequence | 지금은 이득, 나중에 위험 | event weight change |
| item dependency | 특정 선택이 아이템에 의해 열림 | alternate non-item path |

Threat는 단순 피해가 아니라 플레이어가 어떤 기준으로 선택해야 하는지를 만든다.

---

## 6. Reward/Cost Archetype 목록

### 6.1 Reward

- health 회복
- food 회복
- money 획득
- reputation 획득
- curse 같은 위험 상태 감소
- item 획득
- clue 획득 또는 mystery 해석 가능성 증가
- future danger weight 감소
- future reward weight 증가
- unavailable choice를 다음 run/turn에서 available하게 만드는 조건 획득

### 6.2 Cost

- health 감소
- food 감소
- money 지출
- reputation 손상
- curse 같은 위험 상태 증가
- item 소모
- future danger weight 증가
- safer event weight 감소
- high risk event 노출 가능성 증가

좋은 reward/cost 조합은 profile별 선택 차이를 만든다. 예를 들어 안전 profile은 health/status 비용을 싫어하고, greedy profile은 money/item 보상을 더 선호하며, desperate profile은 낮은 health/food 상태에서 회복 선택을 더 선호할 수 있어야 한다.

---

## 7. Clue/Foreshadowing 패턴

단서는 정답이 아니라 다음 선택의 판단 재료다.

권장 패턴:

- 반복 징후: 같은 문양, 소리, 냄새, 소문이 다른 이벤트에서 변형되어 등장한다.
- 비용 있는 확인: 정보를 얻으려면 food, money, health, curse 같은 상태/자원 중 하나를 지불한다.
- 도구 기반 확인: item이 있으면 더 안전하거나 더 명확하게 정보를 얻는다.
- 사회적 단서: reputation/money를 통해 증언이나 경고를 얻는다.
- 실패한 해석: 단서가 완전하지 않아 위험 선택을 유혹한다.
- 사후 재해석: 나중 이벤트가 이전 단서의 의미를 바꾼다.

Reject:

- 단서 하나를 못 보면 진행이 멈추는 구조
- choice 없이 description만 긴 설명문
- 정답을 직접 알려줘 선택 판단을 없애는 단서
- red herring만 많고 유효한 판단 재료가 부족한 구조

---

## 8. Item Interaction 패턴

아이템은 아래 중 하나 이상의 기능을 해야 한다.

| 패턴 | 설명 | YAML 연결 |
|---|---|---|
| unlock | 선택지를 연다 | `requires_item`, `requires_any_item` |
| mitigate | 위험 피해를 줄인다 | result status_delta 완화 |
| convert_cost | health/status 비용을 item/money 비용으로 바꾼다 | consume_item, status_delta |
| amplify_reward | 보상을 키운다 | result reward 증가 |
| reveal | 숨겨진 정보나 안전 경로를 드러낸다 | item choice result |
| counter_tag | 특정 danger/event tag 대응성을 갖는다 | `counters_tags` |

주의:

- item choice가 항상 최적해면 profile 차이가 사라진다.
- 같은 item-based choice가 반복될 때는 콘텐츠 측면에서 대체 선택 또는 소모 비용을 검토한다.
- item은 최소 하나의 choice와 연결되어야 하며 dead item을 만들지 않는다.

---

## 9. 상태 압력/Mystery/Survival 패턴

### 9.1 상태 압력

- curse는 여러 상태/위험 압력 중 하나이며, 다음 사건과 선택을 왜곡하는 방식으로만 의미가 있다.
- curse 같은 위험 상태 증가는 즉시 보상과 묶을 때 tradeoff가 선명하다.
- 위험 상태 감소는 비용이 있어야 하며, 항상 정답이어서는 안 된다.

### 9.2 Mystery

- mystery는 정답 추리가 아니라 불완전한 정보로 위험을 고르는 구조다.
- 하나의 결론에는 여러 clue route가 있어야 한다.
- clue는 item, status, social cost, exploration cost와 연결될수록 좋다.

### 9.3 Survival

- survival은 food/health를 깎는 것만으로 충분하지 않다.
- 낮은 health/food 상황에서 다른 선택이 매력적으로 보여야 한다.
- 회복 선택은 위험/기회비용이 있어야 desperate profile의 의미가 생긴다.

---

## 10. Relation Mapping 기준

새 콘텐츠는 작성 전에 아래 relation으로 설명 가능해야 한다.

| 질문 | 필요한 relation |
|---|---|
| 이벤트가 어떤 선택을 제공하는가 | `event_has_choice` |
| 선택이 어떤 결과를 만드는가 | `choice_produces_result` |
| 선택이 아이템을 요구하는가 | `choice_requires_item` |
| 선택이 상태 조건을 요구하는가 | `choice_requires_status` |
| 아이템이 어떤 위험/태그에 대응하는가 | `item_counters_tag` |
| 결과가 어떤 status를 바꾸는가 | `result_modifies_status` |
| 결과가 향후 이벤트 풀을 바꾸는가 | `result_changes_event_weight` |
| 이벤트가 어떤 지역/태그에 속하는가 | `event_belongs_to_region`, `event_has_event_tag`, `event_has_danger_tag` |
| scenario가 어떤 이벤트와 source를 검증하는가 | `scenario_includes_event`, `scenario_uses_content_source` |

Relation으로 설명되지 않는 콘텐츠는 지금 단계에서 추가하지 않는다. 먼저 기존 relation으로 표현할 수 있는지 확인한다.

---

## 11. Content Expansion Phase 3 샘플링 절차

Phase 3에서는 아래 순서를 따른다.

1. 기존 Playtest Review에서 반복/편향이 심한 선택 유형을 확인한다.
2. 새 pack 또는 기존 pack 확장 범위를 정한다.
3. 이 문서의 event archetype에서 최소 5종 이상을 고른다.
4. 각 이벤트에 choice archetype을 최소 2개 이상 배치한다.
5. item interaction을 전체 이벤트 중 일부에만 배치해 item dominance를 피한다.
6. clue/foreshadowing은 최소 3개 route로 분산한다.
7. reward/cost는 safe/greedy/curious/desperate profile이 다르게 평가할 여지를 만든다.
8. status 변화가 다음 choice availability 또는 scoring에 영향을 주는지 확인한다.
9. Ontology-lite relation checklist를 채운다.
10. Console Simulator와 analyzer로 profile별 diversity, repeated choice, unavailable_selected를 확인한다.

Phase 3의 목표는 weight를 정밀 튜닝하는 것이 아니라, 콘텐츠 풀 자체가 선택 차이를 만들 수 있는지 검증하는 것이다.

---

## 12. 좋은 이벤트 판정 기준

좋은 이벤트는 아래 조건을 만족한다.

- description만 읽어도 현재 압박이 보인다.
- choice가 최소 2개 이상이고 둘 다 실제 선택 가능성이 있다.
- 하나 이상의 choice가 명확한 비용을 가진다.
- 하나 이상의 choice가 다음 상태나 다음 이벤트 가능성을 바꾼다.
- item choice가 있다면 non-item 대안도 존재한다.
- high risk choice는 보상이 충분하지만 항상 정답은 아니다.
- low risk choice는 안전하지만 기회비용이 있다.
- clue가 있다면 다음 선택 판단에 사용된다.
- 결과가 `health`, `food`, `money`, `reputation`, `curse`, item, event weight 중 하나 이상을 의미 있게 바꾼다.
- relation mapping으로 설명 가능하다.

---

## 13. 나쁜 이벤트 Reject 기준

아래에 해당하면 추가하지 않는다.

- 선택지가 사실상 하나뿐이다.
- unavailable choice만 흥미롭고 available choice는 의미가 없다.
- item이 없으면 진행이 막힌다.
- item이 있으면 항상 같은 선택이 최적해가 된다.
- status 변화가 다음 선택에 영향을 주지 않는다.
- 보상/비용이 숫자만 다르고 이야기 기능이 없다.
- combat을 별도 전투 시스템처럼 만들려고 한다.
- 원문 TRPG 설정, 고유명, 문장을 직접 가져온다.
- pack theme가 설명문에만 있고 tag/item/result 관계로 증명되지 않는다.
- Ontology-lite relation으로 설명할 수 없다.

---

## 14. 작성 전 간단 체크리스트

```text
[ ] 이 이벤트의 primary pressure가 명확한가?
[ ] 선택지가 최소 2개 이상인가?
[ ] safe/risky/item/info/survival 중 어떤 choice archetype인지 설명되는가?
[ ] 비용과 보상이 모두 있는가?
[ ] result가 다음 선택이나 이벤트 풀에 영향을 주는가?
[ ] item이 있다면 unlock/mitigate/convert/reveal/amplify 중 하나인가?
[ ] clue가 있다면 다음 선택의 판단 재료인가?
[ ] 새 status 없이 기존 status로 표현 가능한가?
[ ] combat이면 일반 event/choice로 유지했는가?
[ ] relation mapping이 가능한가?
[ ] 원문 설정/고유명/문장을 차용하지 않았는가?
```
