# [Current] Ontology Core Model v0.1

> 상태: [Current] FateWeaver의 Ontology-lite를 Entity / Relation / Fact / Rule / Situation Intent 기반으로 확장하기 위한 Core Model 설계 문서.

## 1. 문서 목적

이 문서는 현재 tag matching 중심 Ontology-lite를 깨지 않고, 다음 단계의 Reasoner-lite와 Situation Director-lite가 읽을 수 있는 Ontology Core Model을 정의한다.

이번 문서는 구현 지시가 아니다. `data/core/ontology.yaml`, tag, Quest, Event, Card, Item, Ending 구조를 즉시 바꾸지 않고, 다음 구현 작업의 계약을 먼저 고정한다.

## 2. 현재 Ontology-lite 상태

현재 FateWeaver의 Ontology는 P0 기준으로 Card Candidate Scoring과 Objective 연결에는 정상 작동한다.

현재 작동하는 흐름:

```text
Event tag
Event storylet_tags
Event card_candidate_hints
Card applies_to_storylet_tags
Card applies_to_quest_objectives
Card result next_event_tags
→ Card Candidate score
→ Objective progress
```

구체적으로:

- Event의 `storylet_tags`와 Card의 `applies_to_storylet_tags`가 card scoring에 반영된다.
- Event의 `card_candidate_hints`가 `storylet_hint_bonus`로 카드 후보 점수를 올린다.
- Card의 `applies_to_quest_objectives`가 optional objective 연결에 쓰인다.
- Card result의 `next_event_tags`가 state에 누적되고 이후 storylet context에 일부 섞인다.
- Pack 1/2 이후 `storm_pass`, `shelter`, `pack1_enrichment`, `injured_traveler` 같은 tag가 카드 노출에 실제 영향을 준다.

한계:

- `data/core/ontology.yaml` 자체는 runtime engine이 아니라 관계 계약/문서에 가깝다.
- Event selection은 주로 `quest_ids`, region, requirement, cooldown, `base_weight` 기반이다.
- `next_event_tags`, clue, omen, risk, prior choice를 이용해 다음 Storylet/Event 자체를 능동적으로 고르는 Situation Director 역할은 아직 미완성이다.
- Clue/Omen/Item/Ending이 늘었지만 Entity / Relation / Fact 기반 추론은 아직 없다.

## 3. 목표 Ontology 구조

목표 구조:

```text
Game State
+ Entity
+ Relation
+ Fact
+ Rule
+ Situation Intent
→ Event selection score
→ Card candidate score
→ Result
→ next facts / tags / risk / clue / omen
```

핵심 원칙:

- tag는 빠른 매칭용 표면으로 유지한다.
- Entity / Relation / Fact는 깊은 추론용 레이어로 추가한다.
- Reasoner-lite는 deterministic rule matcher로 시작한다.
- Situation Director-lite는 black-box가 아니라 score modifier와 trace를 남기는 선택 보정기로 시작한다.

## 4. Core Concept

### 4.1 Entity

Entity는 게임 세계의 명사다. 장소, 위험, NPC group, clue source, object, route, item-like affordance를 안정적으로 가리킨다.

초안:

```yaml
entities:
  - id: village_well
    type: location_object
    category: local_problem
    tags: [village, well, water_source]

  - id: poisoned_water
    type: hazard
    category: local_problem
    tags: [poison, water, disease]

  - id: worried_villagers
    type: npc_group
    category: local_problem
    tags: [village, reputation, witness]
```

규칙:

- `id`는 lowercase snake_case를 쓴다.
- `type`은 `location`, `location_object`, `hazard`, `npc_group`, `route`, `resource_source`, `evidence`, `omen_source`, `item_affordance`부터 시작한다.
- `tags`는 기존 `data/core/tags.yaml` vocabulary와 충돌하지 않게 재사용한다.
- `category`는 우선 적용 단위인 `local_problem`, `investigation_mystery`, `survival_exploration` 같은 Quest category와 연결한다.
- Quest/Event/Card는 Entity를 직접 소유하지 않고 `ontology_refs.entities`로 참조한다.

### 4.2 Relation

Relation은 Entity 간 관계다.

초안:

```yaml
relations:
  - subject: village_well
    predicate: contains
    object: poisoned_water

  - subject: poisoned_water
    predicate: threatens
    object: worried_villagers

  - subject: old_well_tunnel
    predicate: connects_to
    object: underground
```

초기 predicate:

```text
contains
connects_to
threatens
protects
reveals
requires
blocks
causes
located_in
owned_by
witnessed_by
foreshadows
```

검증 규칙:

- `subject`와 `object`는 존재하는 Entity여야 한다.
- `predicate`는 허용 목록에 있어야 한다.
- 동일 `(subject, predicate, object)` 중복은 금지한다.
- Relation은 Event/Card weight에 직접 더하지 않고 Rule 입력으로 먼저 사용한다.

### 4.3 Fact

Fact는 현재 run에서 참이거나 seed data에서 참으로 시작하는 명제다.

초안:

```yaml
facts:
  - id: water_quality_poisoned
    entity: village_well
    property: water_quality
    value: poisoned

  - id: villagers_trust_low
    entity: worried_villagers
    property: trust
    value: low
```

구분:

- Static Fact: seed data에 존재하는 배경 사실이다.
- Runtime Fact: run 중 Card result, clue, omen, objective progress, item use가 만든 사실이다.

### 4.4 State Fact

State Fact는 runtime state에서 계산되는 Fact다.

예:

```yaml
state_facts:
  - id: low_food_pressure
    from_state:
      resource: food
      lte: 1

  - id: clue_missing_for_primary_objective
    from_objective:
      type: discover_clue
      status: missing
```

State Fact는 저장 데이터가 아니라 Reasoner-lite 입력이다. 매 turn 계산하고 inference trace에 남긴다.

### 4.5 Rule

Rule은 Fact / Relation / State Fact를 보고 event/card weight와 situation intent를 만든다.

초안:

```yaml
rules:
  - id: poisoned_water_requires_investigation
    when:
      all:
        - fact: water_quality_poisoned
        - missing_fact: poison_source_identified
    then:
      add_event_weight:
        tags: [investigation, well, clue]
        weight: 25
      add_card_weight:
        tags: [inspect, clue]
        weight: 15
      suggest_intent: reveal_clue
```

`when` 지원 범위:

- `all`
- `any`
- `not`
- `fact`
- `missing_fact`
- `relation`
- `state_fact`

`then` 지원 범위:

- `add_event_weight`
- `add_card_weight`
- `suggest_intent`
- `add_fact`
- `emit_trace`

`next_event_tags`는 폐기하지 않는다. Rule output의 `add_event_weight.tags`와 함께 다음 Event 후보를 보정하는 legacy bridge로 유지한다.

### 4.6 Situation Intent

Situation Intent는 Director가 다음 상황의 역할을 판단하는 층이다.

초기 intent:

```yaml
situation_intents:
  - id: reveal_clue
    purpose: "플레이어에게 원인 단서를 제공한다"

  - id: escalate_risk
    purpose: "위험을 높이고 후퇴 판단을 압박한다"

  - id: offer_resource_tradeoff
    purpose: "자원 손실과 진행 사이의 선택을 만든다"

  - id: invite_return
    purpose: "귀환/보고 선택을 제시한다"
```

권장 목록:

```text
reveal_clue
escalate_risk
offer_resource_tradeoff
offer_optional_help
invite_return
introduce_omen
resolve_objective
test_reputation
test_survival
unlock_route
```

연결:

- Event selection은 intent에 맞는 `storylet_tags`, `event_tags`, `danger_tags`, `ontology_refs`에 weight를 더한다.
- Card slot role은 intent를 slot pressure로 해석한다.
- 최근 intent memory로 같은 intent 반복을 줄인다.

### 4.7 Inference Result

Reasoner-lite는 turn마다 다음 결과를 낸다.

```yaml
inference_result:
  event_weight_modifiers:
    - tags: [well, investigation]
      weight: 25
      reason: poisoned_water_requires_investigation

  card_weight_modifiers:
    - tags: [inspect, clue]
      weight: 15
      reason: reveal_clue_intent

  situation_intents:
    - reveal_clue

  next_facts:
    - investigation_pressure_active

  trace:
    - rule: poisoned_water_requires_investigation
      matched: true
      inputs: [water_quality_poisoned]
```

Inference Result는 JSON Log와 evidence에 남길 수 있어야 한다. 디버깅 불가능한 director는 금지한다.

## 5. 기존 구조와의 연결

### 5.1 Quest 연결

```text
Quest objective
→ required facts / target facts
→ Situation Intent
```

예:

```text
discover_clue objective
→ missing clue fact
→ reveal_clue intent
```

Quest에는 나중에 `ontology_objectives` 또는 objective-level `target_facts`를 추가할 수 있다. 기존 `discover_clue`, `optional_action`, `keep_resource_at_least`는 유지한다.

### 5.2 Event / Storylet 연결

```text
Event tags
→ ontology entity/relation/fact references
→ event weight modifier
```

초안:

```yaml
event:
  id: well_sediment_hint
  ontology_refs:
    entities: [village_well, poisoned_water]
    facts: [water_quality_poisoned]
```

기존 `storylet_tags`, `card_candidate_hints`, `cooldown_tags`, `repeat_group`, `base_weight`는 유지한다. Ontology refs는 weight 보정 입력이다.

### 5.3 Card 연결

```text
Card applies_to_storylet_tags
→ 기존 tag matching 유지
Card effects
→ add/update facts
```

초안:

```yaml
card:
  id: inspect_bitter_sediment
  ontology_refs:
    entities: [village_well]
  effects:
    add_facts:
      - poison_source_suspected
```

기존 `result.gain_clues`, `gain_omens`, `quest_progress`, `next_event_tags`는 유지한다. `add_facts`는 Reasoner-lite 단계에서 추가한다.

### 5.4 Clue 연결

```text
Clue
→ fact 또는 evidence entity
```

예:

```text
clue_bitter_well_sediment
→ fact: poison_source_suspected
```

Clue는 진행 차단 열쇠가 아니라 판단 재료다. 한 결론은 여러 clue route로 도달할 수 있어야 한다.

### 5.5 Omen 연결

```text
Omen
→ foreshadow / risk / event weight modifier
```

예:

```text
omen_cold_wind_from_well
→ add_event_weight: underground, danger
```

Omen은 `introduce_omen`, `escalate_risk`, `invite_return` intent와 연결한다.

### 5.6 Item 연결

```text
Item
→ enables card
→ modifies result
→ blocks/mitigates risk fact
```

예:

```text
rope
→ enables descend_well_safely
```

Item은 항상 최적해가 아니어야 한다. `unlock`, `risk_reduce`, `cost_convert`, `information`, `future_weight` 역할을 Fact/Rule 입력으로 연결한다.

### 5.7 Ending 연결

```text
Ending
→ fact/resource/outcome conditions
```

예:

```yaml
ending_ominous_truth_carrier:
  requires:
    - result_type: success
    - fact: omen_interpreted
    - risk_gte: 3
```

Ending은 기존 `result_type`, `failure_kind`, `character_outcome` 의미를 바꾸지 않는다. Fact는 run residue를 더 잘 설명하는 조건으로만 쓴다.

## 6. Data Model 초안

초기 파일 구성 후보:

```text
data/core/ontology.yaml              기존 Ontology-lite 계약 유지
data/core/ontology_core.yaml         Entity / Relation / Fact / Rule seed 후보
data/content/ontology/*.yaml         category별 seed data 후보
```

초기 schema:

```yaml
ontology_core:
  version: 0.1

entities: []
relations: []
facts: []
rules: []
situation_intents: []
```

P0에서는 하나의 새 core 파일로 시작하고, category seed가 커질 때 split을 판단한다.

## 7. Runtime Flow 초안

```text
1. Load Quest / Event / Card / Item / Ending / Ontology
2. Build current game state
3. Collect known facts
4. Collect missing objective facts
5. Run Reasoner-lite rules
6. Produce situation intents
7. Score Event candidates
8. Select Event / Storylet
9. Score Card candidates
10. Player selects Card
11. Apply result
12. Update facts / tags / resources / objectives
13. Repeat
```

## 8. Validator 요구사항

Validator는 implementation보다 먼저 추가한다.

필수 검증:

- duplicate entity id
- relation subject/object 존재
- unknown predicate
- duplicate relation
- rule fact 참조 존재
- rule relation 참조 존재
- rule output tag가 기존 tag vocabulary 또는 local ontology tag에 존재
- event/card `ontology_refs` 존재
- cycle 또는 self-relation warning
- inference trace reason id 유효성

## 9. Reasoner-lite 단계

Reasoner-lite v0.1 범위:

```text
facts + state_facts + rules
→ event_weight_modifiers
→ card_weight_modifiers
→ situation_intents
→ next_facts
→ trace
```

금지:

- LLM runtime reasoning
- OWL/RDF/SPARQL engine
- hidden random director
- Quest/Event/Card 전체 재작성

## 10. Situation Director-lite 단계

Situation Director-lite는 기존 Event selection을 대체하지 않는다. 기존 후보군을 만든 뒤 inference result를 추가 weight로 반영한다.

초기 score 입력:

- active quest id / quest tags
- current region
- day / turn / time_of_day / act
- current resources
- known facts
- missing objective facts
- next_event_tags
- recent storylet memory
- situation intents

출력:

- Event candidate score modifier
- selected storylet reason trace
- Card candidate modifier bridge

## 11. Migration 전략

한 번에 바꾸지 않는다.

Phase O1:

- 이 문서와 roadmap 작성.

Phase O2:

- `local_problem`, `investigation_mystery`, `survival_exploration`에 seed Entity / Relation / Fact를 최소 추가한다.

Phase O3:

- validator를 먼저 추가한다.

Phase O4:

- Reasoner-lite를 card/event score modifier만 만드는 pure function으로 시작한다.

Phase O5:

- Event selection에 inference result를 반영한다.

Phase O6:

- Standard Run 25~35 Turn으로 반복도, event variety, clue/omen 의미, turn length를 재검증한다.

## 12. 금지할 설계

- 기존 tag 구조 폐기 금지
- Quest/Card/Event 전체 재작성 금지
- 복잡한 OWL/RDF/SPARQL 엔진 도입 금지
- LLM runtime reasoning 의존 금지
- 디버깅 불가능한 black-box director 금지
- storylet pool 전체 시스템을 한 번에 재작성 금지
- 기존 active scenario를 깨뜨리는 migration 금지
- clue 하나를 못 보면 진행이 막히는 구조 금지
- item이 항상 정답이 되는 구조 금지

## 13. 다음 작업

1. Ontology Seed Data v0.1 작업에서 세 category의 Entity / Relation / Fact 후보를 작성한다.
2. Ontology Validator 작업에서 refs와 rule input/output 검증을 추가한다.
3. Reasoner-lite 작업에서 deterministic inference result를 JSON trace로 남긴다.
4. Situation Director-lite 작업에서 Event selection weight에 inference result를 작게 반영한다.
5. Standard Run 재검증에서 카드 반복과 event variety 변화를 비교한다.
