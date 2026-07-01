# [Current] Ontology Core and Director Roadmap v0.1

> 상태: [Current] Ontology Core Model을 기반으로 Reasoner-lite와 Situation Director-lite까지 확장하기 위한 실행 로드맵.

## 1. 문서 목적

이 문서는 `docs/02_schema/14_Ontology_Core_Model_v0.1.md`를 실행 흐름으로 나눈다. 목표는 현재 Ontology-lite/tag matching layer를 유지하면서 Entity / Relation / Fact / Rule 기반 Situation Director-lite까지 단계적으로 확장하는 것이다.

이번 roadmap은 구현 문서가 아니다. 다음 Codex 작업들이 data, validator, reasoner, director, standard run 검증을 어떤 순서로 다룰지 고정한다.

## 2. 현재 문제

현재 구조는 다음에 강하다.

- Event `storylet_tags`와 Card `applies_to_storylet_tags` 기반 card score.
- Event `card_candidate_hints` 기반 `storylet_hint_bonus`.
- Card `applies_to_quest_objectives` 기반 objective 연결.
- Card result `next_event_tags` 누적.
- Pack 1/2 이후 clue, omen, item-gated card, ending surface.

현재 구조는 다음에 약하다.

- `data/core/ontology.yaml`은 runtime engine이 아니라 관계 계약이다.
- Event selection은 아직 Entity / Relation / Fact / Rule 추론을 쓰지 않는다.
- clue/omen은 획득/표시되지만 다음 상황 역할을 안정적으로 고르지는 못한다.
- Standard Run에서 `ration_the_last_supplies`, `buy_local_hint` 반복이 남았다.

## 3. 목표

목표:

```text
Game State + Ontology Core
→ Reasoner-lite inference_result
→ Situation Director-lite Event weighting
→ Card Candidate scoring bridge
→ Result
→ facts/tags/resources/objectives update
```

비목표:

- 기존 tag 구조 폐기
- runtime LLM reasoning
- GraphDB/OWL/RDF/SPARQL 도입
- Storylet Pool 전체 재작성
- Quest/Card/Event 대량 재작성

## 4. 단계별 계획

### Phase O1. Ontology Core Model

상태: 이번 작업.

산출물:

- `docs/02_schema/14_Ontology_Core_Model_v0.1.md`
- `docs/06_plans/09_Ontology_Core_And_Director_Roadmap_v0.1.md`
- `docs/07_reviews/46_Ontology_Core_Model_Replan_Result_v0.1.md`

완료 기준:

- 현재 Ontology-lite 상태와 한계가 명확하다.
- Entity / Relation / Fact / State Fact / Rule / Situation Intent / Inference Result가 정의된다.
- 기존 Quest / Event / Card / Clue / Omen / Item / Ending과의 호환 전략이 있다.
- 금지할 설계가 명시된다.

### Phase O2. Ontology Seed Data

목표:

- 작은 seed data로 Entity / Relation / Fact vocabulary를 검증한다.
- 기존 tag, Quest, Event, Card를 삭제하거나 대량 수정하지 않는다.

우선 category:

| Category | 이유 |
|---|---|
| `local_problem` | Entity/Relation이 명확하다. 예: well, villagers, contamination. |
| `investigation_mystery` | clue/fact 연결이 중요하다. |
| `survival_exploration` | risk/resource/omen 연결 검증에 좋다. |

권장 산출물:

```text
data/core/ontology_core.yaml
또는
data/content/ontology/local_problem.yaml
data/content/ontology/investigation_mystery.yaml
data/content/ontology/survival_exploration.yaml
```

Seed 범위:

- Entity 15~25개.
- Relation 20~35개.
- Static Fact 10~20개.
- Rule 후보는 validator 전에는 문서/disabled 상태로 둔다.

### Phase O3. Ontology Validator

목표:

- runtime 사용 전 data contract 오류를 잡는다.

필수 검증:

- duplicate entity id.
- relation subject/object 존재.
- unknown predicate.
- rule fact 참조 존재.
- rule relation 참조 존재.
- event/card `ontology_refs` 존재.
- rule output tag/intent 존재.
- category seed file 중복/충돌.

성공 기준:

- validator가 bad reference fixture에서 실패한다.
- 현재 active scenario validation을 깨뜨리지 않는다.
- `data/core/ontology.yaml`의 legacy relation과 새 Ontology Core가 역할 충돌 없이 공존한다.

### Phase O4. Reasoner-lite

목표:

- deterministic rule matcher로 inference result를 만든다.

입력:

- active quest.
- current region.
- run clock.
- player state.
- known facts.
- state facts.
- missing objective facts.
- recent storylet memory.
- next_event_tags.

출력:

```text
event_weight_modifiers
card_weight_modifiers
situation_intents
next_facts
trace/debug reason
```

구현 원칙:

- pure function으로 시작한다.
- Event/Card 선택을 직접 수행하지 않는다.
- weight modifier와 trace만 만든다.
- 기존 Card Candidate scoring은 그대로 두고 modifier bridge만 추가한다.

### Phase O5. Situation Director-lite Event Weighting

목표:

- 기존 Event selection 후보군에 inference result를 추가 weight로 반영한다.

입력:

- Event `quest_ids`, region, requirement, cooldown, `base_weight`.
- Reasoner-lite `event_weight_modifiers`.
- Situation Intent.
- recent event memory.

출력:

- selected Event / Storylet.
- score reason trace.
- JSON/Text MUD evidence에서 읽을 수 있는 director explanation.

성공 기준:

- `next_event_tags`만으로 설명하기 어려운 clue/omen/fact 상황이 Event selection score에 보인다.
- 같은 category standard run에서 event variety가 증가한다.
- 기존 active scenario가 깨지지 않는다.

### Phase O6. Standard Run 재검증

목표:

- Ontology Core + Reasoner-lite + Director-lite가 실제 run 품질을 올렸는지 확인한다.

검증 질문:

- 25~35 Turn 유지?
- Event variety 증가?
- 반복 카드 감소?
- clue/omen이 다음 상황 선택에 의미 있게 반영?
- item/fact가 risk나 route 선택에 의미 있게 반영?
- JSON trace로 왜 선택됐는지 설명 가능?

필수 비교:

| 항목 | Baseline | Target |
|---|---|---|
| Top repeated card | `ration_the_last_supplies` 15/25 | 감소 |
| Shared repeated card | `buy_local_hint` 13/25 | 감소 |
| Unique events | 6 | 증가 |
| Run turn count | 25~35 | 유지 |
| Trace readability | limited | rule/intention reason 포함 |

## 5. 우선 적용 Category

1. `local_problem`
   - well, village, witness, contamination 같은 entity가 명확하다.
   - reputation/resource/fact 연결을 작게 검증하기 좋다.

2. `investigation_mystery`
   - clue redundancy, missing fact, reveal_clue intent가 핵심이다.
   - clue가 정답 열쇠가 아니라 위험 판단 재료인지 검증한다.

3. `survival_exploration`
   - resource pressure, omen, route, shelter, risk mitigation 연결이 좋다.
   - Standard Run 반복도 개선과 직접 연결된다.

## 6. 성공 기준

- 기존 tag matching layer가 그대로 유지된다.
- 새 Ontology Core seed data는 validator로 검증된다.
- Reasoner-lite는 deterministic inference result와 trace를 낸다.
- Situation Director-lite는 Event selection weight에 inference result를 반영한다.
- JSON Log 또는 evidence에서 rule/intent/reason을 확인할 수 있다.
- Standard Run 25~35 Turn은 유지된다.
- `data/`, `src/`, `tests/` 변경은 각 phase에서 명시적 목적과 검증을 가진다.

## 7. 리스크

| 리스크 | 완화 |
|---|---|
| Ontology Core가 World Bible처럼 커짐 | category seed와 validator 중심으로 제한한다. |
| tag 구조와 중복됨 | tag는 fast matching, entity/fact는 inference로 역할 분리한다. |
| Director가 black-box가 됨 | every modifier에 `reason`과 `trace`를 둔다. |
| Event selection을 한 번에 재작성함 | 기존 candidate pool 뒤에 weight modifier만 추가한다. |
| clue가 hard gate가 됨 | clue는 route/risk/partial 판단 자료로 쓴다. |
| item이 항상 정답이 됨 | cost, consume, opportunity loss를 유지한다. |
| Standard Run 반복이 content 부족 탓인데 rule로 덮음 | 반복도는 content surface와 director weighting을 분리해 비교한다. |

## 8. 다음 Codex 작업 제안

1. `CODEX_TASK_Ontology_Seed_Data_v0.1.md`
   - 세 category에 최소 Entity / Relation / Fact seed data 작성.

2. `CODEX_TASK_Ontology_Validator_v0.1.md`
   - duplicate/ref/predicate/rule output validator 추가.

3. `CODEX_TASK_Reasoner_Lite_v0.1.md`
   - facts/rules를 inference result로 변환하는 pure function 추가.

4. `CODEX_TASK_Situation_Director_Lite_Event_Weighting_v0.1.md`
   - Event selection score에 inference result 반영.

5. `CODEX_TASK_Standard_Run_Ontology_Director_Verification_v0.1.md`
   - baseline과 비교해 25~35 Turn, event variety, card repeat, clue/omen trace 검증.
