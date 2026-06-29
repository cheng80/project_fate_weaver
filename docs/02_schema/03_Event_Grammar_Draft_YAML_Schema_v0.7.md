# Project FateWeaver Event Grammar Draft YAML Schema v0.7

## 문서 목적

이 문서는 Console Validation 실험을 위한 Draft YAML Schema다.

v0.7에서는 scenario filter 문법, choice-level requires 계약, unavailable choice 표시 정책, 로그 metric 계약을 명시한다.

---

# 1. 전체 데이터 구조

```text
data/
  core/
    statuses.yaml
    tags.yaml
    choice_types.yaml
    item_roles.yaml
    result_rules.yaml
    ontology.yaml

  content/
    base/
      regions.yaml
      items.yaml
      events.yaml
      endings.yaml

    packs/
      <pack_id>/
        events.yaml
        items.yaml

  scenarios/
    <scenario_id>.yaml
```

---

# 2. core/statuses.yaml

```yaml
statuses:
  health:
    type: int
    min: 0
    max: 10
    initial: 7
    fail_when: 0
```

필수 상태:

- health
- food
- money
- reputation
- curse

---

# 2.1 core/ontology.yaml

`data/core/ontology.yaml`은 콘텐츠 관계 분석을 위한 Ontology-lite 계약이다.

이 파일은 이벤트 실행 엔진이 아니며, GraphDB나 온톨로지 엔진을 도입하지 않는다.

정의 대상:

- entity: `event`, `choice`, `result`, `item`, `status`, `tag`, `clue`, `location`, `omen`, `hazard`, `region`, `scenario`, `file`
- relation: `event_has_choice`, `choice_produces_result`, `choice_requires_item`, `choice_requires_status`, `item_counters_tag`, `result_modifies_status`, `result_changes_event_weight`, `event_belongs_to_region`, `event_has_event_tag`, `event_has_danger_tag`, `event_reveals_clue`, `item_reveals_clue`, `event_occurs_at_location`, `omen_warns_about_hazard`, `scenario_includes_event`, `scenario_uses_content_source`

v0.2 trial relation:

```text
event_reveals_clue
item_reveals_clue
event_occurs_at_location
omen_warns_about_hazard
```

이 trial relation은 Phase 3 콘텐츠에서 사용성을 검증하기 위한 계약이다. validator/analyzer/export가 아직 소비하지 않을 수 있으며, Phase 3 이후 사용성이 낮으면 제거하거나 기존 tag/status/result 표현으로 통합할 수 있다.

상세 계약:

```text
docs/02_schema/09_Content_Ontology_Model_v0.1.md
```

---

# 3. content/base/events.yaml

이벤트는 실제 콘텐츠로 관리한다.

이벤트가 테스트용인지 여부는 events.yaml에 넣지 않는다.

테스트에서 사용할지 여부는 scenario가 결정한다.

---

# 4. scenarios/*.yaml

시나리오는 테스트 조건이다.

필수 필드:

```yaml
id: string
name: string
content_sources: list[string]
include_regions: list[string]
initial_status: map
initial_items: list[string]
target_turns: int
seed: int
```

선택 필드:

```yaml
include_event_ids: list[string]
include_event_tags: list[string]
exclude_event_ids: list[string]
exclude_event_tags: list[string]
validation_targets: map
```

Filter 규칙:

```text
include_event_ids와 include_event_tags가 둘 다 없으면 content_sources + include_regions 기준 전체 이벤트를 사용한다.
include_event_ids만 있으면 해당 id에 포함되는 이벤트만 사용한다.
include_event_tags만 있으면 해당 tag 중 하나 이상을 가진 이벤트만 사용한다.
include_event_ids와 include_event_tags가 둘 다 있으면 AND 조건으로 필터링한다.
exclude_event_ids는 include 필터 이후 해당 id를 제거한다.
exclude_event_tags는 include 필터 이후 해당 tag 중 하나 이상을 가진 이벤트를 제거한다.
```

---

# 5. Event Schema

필수 필드:

```yaml
id: string
name: string
description: string
region_tags: list[string]
event_tags: list[string]
base_weight: int
choices: list[Choice]
```

선택 필드:

```yaml
danger_tags: list[string]
location_tags: list[string]
revealed_clue_tags: list[string]
omen_tags: list[string]
hazard_tags: list[string]
requires_status: StatusCondition
requires_item: string
variation_rules: list[VariationRule]
cooldown_turns: int
max_occurrences_per_run: int
```

---

# 6. Choice Schema

필수 필드:

```yaml
id: string
text: string
type: choice_type
risk_level: risk_level
```

선택 필드:

```yaml
requires_item: string
requires_any_item: list[string]
requires_status: StatusCondition
requires_tag: string
consume_item: bool
hidden_until_available: bool
reveals_clue_tags: list[string]
creates_omen_tags: list[string]
result: Result
result_pool: list[ConditionalResult]
```

`result` 또는 `result_pool` 중 하나만 필수다.

Requires 규칙:

```text
choice-level requires_*는 해당 choice의 available 여부를 판단한다.
event-level requires_*는 이벤트 자체의 eligible 여부를 판단한다.
Console Validation에서 대부분의 조건은 choice-level로 둔다.
hidden_until_available 기본값은 false다.
```

Trial clue/omen 규칙:

```text
reveals_clue_tags는 선택 자체가 어떤 단서를 드러내는지 표시한다.
creates_omen_tags는 선택이 어떤 징조를 만들거나 관찰하게 하는지 표시한다.
이 필드는 available 여부를 직접 바꾸지 않는다.
```

---

# 6.1 Result Trial Fields

Result는 상태 변화와 event weight 변화 외에 Phase 3 trial 분석용 clue/omen field를 가질 수 있다.

선택 필드:

```yaml
reveals_clue_tags: list[string]
creates_omen_tags: list[string]
```

규칙:

```text
result.reveals_clue_tags는 선택 결과로 새로 확인된 정보 표식이다.
result.creates_omen_tags는 선택 결과로 생성되거나 확인된 징조 표식이다.
이 필드는 narrative message를 대체하지 않고, analyzer/export 후보 관계를 위한 구조적 표식이다.
```

---

# 6.2 Item Trial Fields

Item은 기존 `counters_tags` 외에 Phase 3 trial 분석용 field를 가질 수 있다.

선택 필드:

```yaml
reveals_clue_tags: list[string]
counters_hazard_tags: list[string]
```

규칙:

```text
reveals_clue_tags는 아이템이 정보 발견에 기여하는 경우 사용한다.
counters_hazard_tags는 구체 hazard에 대응하는 경우 사용한다.
기존 counters_tags는 broad danger/event/item tag 대응이고, counters_hazard_tags는 구체 조우/장애/위험 장치 대응이다.
```

---

# 6.3 danger_tags와 hazard_tags 차이

```text
danger_tags:
  넓은 위험 분류다.
  예: lost, trap, bandit, hunger, curse, darkness
  기존 event_has_danger_tag relation이 사용한다.

hazard_tags:
  구체 조우/장애/위험 장치다.
  예: false_smoke_signal, sinking_mud, thorn_snare, echo_marker
  trial omen_warns_about_hazard relation과 item counters_hazard_tags 검증에 사용한다.
```

`hazard_tags`는 `danger_tags`를 대체하지 않는다. Phase 3 이벤트는 broad 분석을 위해 `danger_tags`를 유지하고, 구체 counterplay나 omen 연결이 필요할 때만 `hazard_tags`를 추가한다.

---

# 7. Event Selector Contract

Event Selector는 scenario를 입력으로 받는다.

```text
1. scenario 로드
2. content_sources 로드
3. include_regions로 region 필터
4. include_event_ids/include_event_tags로 후보 제한
5. exclude_event_ids/exclude_event_tags로 후보 제거
6. event-level requires 조건 필터
7. cooldown_turns 필터
8. max_occurrences_per_run 필터
9. base_weight 계산
10. result.event_weight modifier 적용
11. status/risk modifier 적용
12. weight <= 0 제거
13. seed 기반 random pick
14. repeat_count 증가
```

choice-level requires 조건은 이벤트 후보 제거에 쓰지 않는다.

---

# 8. Unavailable Choice Policy

Console Validation 기본 정책은 **show unavailable**이다.

```text
unavailable choice는 표시한다.
단, 선택은 불가능하다.
표시 이유를 함께 보여준다.
```

표시 예:

```text
[unavailable: requires holy_water]
```

로그 예:

```yaml
choices_seen:
  - id: purify
    available: false
    hidden: false
    reason: requires_item:holy_water

unavailable_choice_count: 1
missing_items_noticed:
  - holy_water
```

추후 UX 테스트에서는 `hidden_until_available: true`로 숨김 정책을 비교할 수 있다.

---

# 9. Log Metric Contract

## choice-level log

```yaml
choice_time_seconds:
  type: int
  source: system

choice_reason:
  type: string
  source: player
  required: true

expected_risk:
  type: string
  source: player
  required: true

influenced_by:
  type: list[string]
  source: player
  allowed_prefix: [item:, status:, unavailable:, event:, risk:]

regret_score:
  type: int
  scale: 1-5
  source: player
```

## run-level summary

```yaml
fairness_score:
  type: int
  scale: 1-5
  source: player

restart_intent_score:
  type: int
  scale: 1-5
  source: player

player_woven_score:
  type: int
  scale: 1-5
  source: player

narrative_summary:
  type: string
  source: player

most_memorable_choice:
  type: string
  source: player

next_run_intent:
  type: string
  source: player
```

중요:

```text
regret_score = choice-level
player_woven_score = run-level
```

---

# 10. Console Validation Metrics

실행 가능 여부만 Console Validation 성공으로 보지 않는다.

필수 분석 지표:

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
restart_intent_score
run_failed_but_interesting
player_woven_score
```

정의:

```text
meaningful_choice_count:
choice_reason에 상태/아이템/위험/미래 영향 중 하나 이상이 언급된 선택 수

item_unlocked_choice_count:
available=true라서 실제 선택에 영향을 준 item_based choice 수

bad_tradeoff_count:
플레이어가 손해를 알면서도 선택했다고 기록한 선택 수

run_failed_but_interesting:
Run 실패 후 restart_intent_score가 4 이상이면 true

player_woven_score:
이번 Run이 내가 선택으로 엮은 이야기처럼 느껴졌는지 1-5로 평가
```

---

# 11. Validator 기준

## Hard Error

- scenario가 없는 content source를 참조
- scenario가 없는 event id/tag를 참조
- event가 없는 tag를 참조
- item이 없는 role/tag를 참조
- choices 3개 미만
- result/result_pool 동시 사용
- result/result_pool 둘 다 없음
- 상태 변화가 status 아래에 없음
- choice-level requires_*와 event-level requires_*를 혼동한 구조

## Warning

- scenario event 수 12개 미만
- scenario 상태/위험 보조 coverage의 curse-tagged event 수가 목표 미만
- scenario combat event 수 2개 미만
- item이 2개 미만 이벤트에서 사용됨
- variation_rules가 있는 이벤트 3개 미만
- validation_targets 미충족


---

# 12. Tag enum 보강 규칙

모든 `danger_tags`, `event_tags`, `region_tags`, `event_weight` 대상은 `data/core/tags.yaml`의 master enum 안에 있어야 한다.

특히 아래 태그는 Console Validation fixture에서 사용되므로 반드시 존재해야 한다.

```text
curse
lost
holy
undead
bandit
beast
ancient
survival
```

---

# 13. Combat Policy

전투형 이벤트는 별도 전투 시스템이 아니다.

```text
combat은 event_tags: [combat]을 가진 일반 이벤트다.
combat_response는 choice_type 중 하나일 뿐이다.
Console Validation에서 CombatEventResolver는 만들지 않는다.
모든 전투형 이벤트는 일반 ChoiceResolver로 처리한다.
별도 전투 루프, 적 HP, 공격/방어 턴, 전투 UI는 금지한다.
```

---

# 14. Flutter Export 연계

이 Schema는 YAML 원천 데이터 기준이다.

Flutter 앱은 이 YAML을 직접 읽지 않는다.

Flutter 앱 단계에서는 `tools/export_json.py`가 본 Schema를 검증한 뒤 JSON artifact를 생성한다.

자세한 내용은 `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`를 따른다.
