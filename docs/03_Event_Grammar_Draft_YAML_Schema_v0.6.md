# Project FateWeaver Event Grammar Draft YAML Schema v0.6

## 문서 목적

이 문서는 MVP-0 실험을 위한 Draft YAML Schema다.

v0.6에서는 전체 프로젝트 구조에 맞춰 `docs/`, `data/`, `src/`, `tools/`, `fate_weaver/` 역할 분리를 전제한다.

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
include_event_ids: list[string]
initial_status: map
initial_items: list[string]
target_turns: int
seed: int
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

`result` 또는 `result_pool` 중 하나만 필수다.

---

# 7. Event Selector Contract

Event Selector는 scenario를 입력으로 받는다.

```text
1. scenario 로드
2. content_sources 로드
3. include_event_ids로 이벤트 후보 제한
4. include_regions로 region 필터
5. requires 조건 필터
6. cooldown_turns 필터
7. max_occurrences_per_run 필터
8. base_weight 계산
9. result.event_weight modifier 적용
10. curse modifier 적용
11. weight <= 0 제거
12. seed 기반 random pick
13. repeat_count 증가
```

---

# 8. Validator 기준

## Hard Error

- scenario가 없는 content source를 참조
- scenario가 없는 event id를 참조
- event가 없는 tag를 참조
- item이 없는 role/tag를 참조
- choices 3개 미만
- result/result_pool 동시 사용
- result/result_pool 둘 다 없음
- 상태 변화가 status 아래에 없음

## Warning

- scenario event 수 12개 미만
- scenario curse event 수 4개 미만
- scenario combat event 수 2개 미만
- item이 2개 미만 이벤트에서 사용됨
- variation_rules가 있는 이벤트 3개 미만


---

# 9. Tag enum 보강 규칙

모든 `danger_tags`, `event_tags`, `region_tags`, `event_weight` 대상은 `data/core/tags.yaml`의 master enum 안에 있어야 한다.

특히 아래 태그는 MVP-0 fixture에서 사용되므로 반드시 존재해야 한다.

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

# 10. Flutter Export 연계

이 Schema는 YAML 원천 데이터 기준이다.

Flutter 앱은 이 YAML을 직접 읽지 않는다.

MVP-1에서는 `tools/export_json.py`가 본 Schema를 검증한 뒤 JSON artifact를 생성한다.

자세한 내용은 `docs/08_Flutter_Data_Export_Contract_v0.1.md`를 따른다.
