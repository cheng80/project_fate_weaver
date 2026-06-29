# Project FateWeaver Content Ontology Model v0.2 Trial

## 1. 목적

이 문서는 FateWeaver 콘텐츠를 관계 중심으로 분석하기 위한 Ontology-lite 계약을 정의한다.

현재 목표는 온톨로지 엔진을 만드는 것이 아니라, 기존 YAML 데이터가 어떤 entity와 relation으로 해석될 수 있는지 고정하는 것이다.

v0.2는 Phase 3에서 실제 콘텐츠로 검증할 최소 trial entity/relation을 추가한다. 이 확장은 GraphDB, RDF, OWL, 별도 ontology engine 도입이 아니다.

현재 상태:

```text
Console Simulator implementation: PASS
Ontology-lite: v0.2 Trial Extension
Next focus: Phase 3 content trial
```

최종 기준:

```text
GraphDB 없음
Ontology engine 없음
YAML 기반 Ontology-lite 계약만 추가
```

---

## 2. 지금 온톨로지를 준비하는 이유

Console Validation 단계에서 이미 이벤트, 선택지, 아이템, 상태, 태그, 시나리오가 서로 영향을 준다.

관계 계약이 없으면 다음 문제가 생긴다.

- 아이템이 실제로 어떤 선택지를 여는지 추적하기 어렵다.
- 위험 태그가 충분한 대응 수단을 갖는지 분석하기 어렵다.
- 특정 상태가 어떤 선택과 결과에 의해 자주 변하는지 보기 어렵다.
- 시나리오가 실제로 어떤 콘텐츠를 노출하는지 설명하기 어렵다.
- 향후 Flutter export와 분석 도구가 서로 다른 관계 해석을 가질 수 있다.

Ontology-lite는 이 문제를 해결하기 위한 최소 관계 사전이다.

---

## 3. 지금 구현하지 않는 것

이번 단계에서는 아래를 만들지 않는다.

```text
ontology_engine.py
content_graph.py
GraphDB
Neo4j
RDF
OWL
LLM 이벤트 생성기
Flutter 연동 구현
```

Ontology-lite는 실행 엔진이 아니다. `data/core/ontology.yaml`은 나중에 분석기나 export 도구가 참조할 수 있는 계약 파일이다.

---

## 4. 현재 YAML 구조와의 관계

Ontology-lite는 기존 YAML 구조를 바꾸지 않는다.

```text
data/core/       공통 enum, 상태, 규칙, 관계 모델
data/content/    실제 이벤트, 아이템, 지역, 엔딩
data/scenarios/  검증 실행 범위와 시작 조건
```

콘텐츠 작성자는 계속 기존 `events.yaml`, `items.yaml`, `statuses.yaml`, `tags.yaml`, `scenarios/*.yaml`을 작성한다.

Ontology-lite는 그 데이터 위에 얹는 해석 규칙이다.

---

## 5. Entity 정의

| Entity | 의미 | 주요 출처 |
| --- | --- | --- |
| `event` | 플레이어가 마주치는 상황 | `data/content/**/events.yaml` |
| `choice` | 이벤트 안의 선택지 | `events.yaml:choices[]` |
| `result` | 선택 결과로 생기는 상태/아이템/가중치 변화 | `choices[].result`, `choices[].result_pool` |
| `item` | 선택지를 열거나 위험을 줄이는 소지품 | `data/content/**/items.yaml` |
| `status` | 체력, 식량, 돈, 평판, 저주 같은 수치 | `data/core/statuses.yaml` |
| `tag` | region, event, danger, item, weight 분류어 | `data/core/tags.yaml` |
| `clue` | 이벤트/선택/아이템이 드러내는 정보 표식 | `event.revealed_clue_tags`, `choice.reveals_clue_tags`, `result.reveals_clue_tags`, `item.reveals_clue_tags` |
| `location` | region보다 작은 trial 장소 표식 | `event.location_tags` |
| `omen` | 현재/미래 hazard를 예고하는 warning 표식 | `event.omen_tags`, `choice.creates_omen_tags`, `result.creates_omen_tags` |
| `hazard` | 구체 조우/장애/위험 장치 | `event.hazard_tags`, `item.counters_hazard_tags` |
| `region` | 이벤트가 속하는 지역 분류 | `regions.yaml`, `event.region_tags` |
| `scenario` | 검증 실행 조건 | `data/scenarios/*.yaml` |
| `file` | scenario가 참조하는 YAML source | `content_sources` |

---

## 6. Relation 정의

| Relation | From | To | 의미 |
| --- | --- | --- | --- |
| `event_has_choice` | `event` | `choice` | 이벤트가 선택지를 가진다. |
| `choice_produces_result` | `choice` | `result` | 선택지가 결과를 만든다. |
| `choice_requires_item` | `choice` | `item` | 선택지가 아이템을 요구한다. |
| `choice_requires_status` | `choice` | `status` | 선택지가 상태 조건을 요구한다. |
| `item_counters_tag` | `item` | `tag` | 아이템이 특정 위험/테마 태그에 대응한다. |
| `result_modifies_status` | `result` | `status` | 결과가 상태를 변경한다. |
| `result_changes_event_weight` | `result` | `tag` | 결과가 향후 이벤트 가중치 태그를 바꾼다. |
| `event_belongs_to_region` | `event` | `region` | 이벤트가 지역에 속한다. |
| `event_has_event_tag` | `event` | `tag` | 이벤트가 이벤트 태그를 가진다. |
| `event_has_danger_tag` | `event` | `tag` | 이벤트가 위험 태그를 가진다. |
| `event_reveals_clue` | `event` | `clue` | 이벤트, 선택, 결과가 clue tag를 드러낸다. |
| `item_reveals_clue` | `item` | `clue` | 아이템이 clue tag를 드러낸다. |
| `event_occurs_at_location` | `event` | `location` | 이벤트가 구체 location tag에서 발생한다. |
| `omen_warns_about_hazard` | `omen` | `hazard` | omen tag가 구체 hazard tag를 경고한다. |
| `scenario_includes_event` | `scenario` | `event` | 시나리오가 필터를 통해 이벤트를 포함한다. |
| `scenario_uses_content_source` | `scenario` | `file` | 시나리오가 콘텐츠 source 파일을 사용한다. |

각 relation의 기계 판독 가능한 정의는 `data/core/ontology.yaml`에 둔다.

---

## 7. data/core/ontology.yaml 역할

`data/core/ontology.yaml`은 Ontology-lite의 source of truth다.

이 파일은 각 relation에 아래 필드를 둔다.

```yaml
id:
from:
to:
status:
description:
source_fields:
future_use:
```

`status`는 선택 필드다. v0.2 trial relation은 `status: trial`로 표시한다.

현재 Console Validation은 이 파일을 실행 중에 읽지 않는다. 지금은 문서/데이터 계약이며, 나중에 분석 도구가 읽을 수 있도록 YAML로 둔다. 따라서 v0.2 trial relation은 validator/analyzer/export가 아직 소비하지 않는 한계를 가진다.

---

## 8. 향후 Content Relationship Analyzer로 확장하는 방법

향후 analyzer는 `ontology.yaml`을 기준으로 기존 YAML을 읽고 관계 테이블을 만들 수 있다.

예상 출력:

```text
event -> choice 개수
choice -> required item/status 목록
item -> unlock하는 choice 목록
danger tag -> counter item 목록
scenario -> 노출 가능한 event 목록
result -> 수정하는 status 목록
```

이 단계에서도 GraphDB는 필수가 아니다. JSON, CSV, SQLite, DuckDB 같은 가벼운 산출물로 충분히 검증할 수 있다.

---

## 9. 향후 Console Simulator, Analyzer, Flutter export와 연결되는 방법

Console Simulator:

- 선택지가 어떤 item/status/tag 때문에 잠기거나 열렸는지 설명할 수 있다.
- run log의 `influenced_by`를 더 일관된 relation 기반 값으로 정리할 수 있다.

Analyzer:

- `item_unlocked_choice_count`가 어떤 item과 choice에서 발생했는지 역추적할 수 있다.
- `bad_tradeoff_count`를 choice type, event tag, danger tag별로 분해할 수 있다.
- scenario coverage를 이벤트 관계 기준으로 측정할 수 있다.

Flutter export:

- Flutter용 JSON export가 어떤 relation을 포함해야 하는지 결정할 수 있다.
- 앱 런타임과 분석 도구가 같은 관계 이름을 사용하게 만들 수 있다.

---

## 10. GraphDB를 지금 도입하지 않는 이유

지금 필요한 것은 그래프 질의 엔진이 아니라 관계 이름과 source field 합의다.

GraphDB를 지금 도입하면 아래 비용이 먼저 생긴다.

- 스키마 마이그레이션 비용
- 운영/설치 비용
- YAML과 GraphDB 사이의 동기화 문제
- 아직 검증되지 않은 콘텐츠 구조에 대한 과한 고정
- Console Validation보다 인프라 설계가 앞서는 문제

따라서 지금은 YAML 기반 계약으로 충분하다.

---

## 11. 나중에 GraphDB가 필요해지는 조건

아래 조건이 실제로 발생하면 GraphDB 도입을 다시 검토한다.

- 콘텐츠 수가 수백 개 이상으로 늘어 수동 관계 추적이 불가능해진다.
- multi-hop 질의가 핵심 워크플로가 된다.
- 예: "특정 상태 위험이 높아졌고, 특정 아이템으로만 완화 가능하며, 숲 시나리오에서 3턴 안에 노출될 수 있는 이벤트" 같은 질의가 자주 필요해진다.
- 여러 작가/디자이너가 동시에 콘텐츠 관계를 편집하고 충돌을 분석해야 한다.
- Flutter export, balance analyzer, content generator가 같은 관계 그래프를 실시간으로 공유해야 한다.

그 전까지는 `data/core/ontology.yaml`과 파일 기반 분석으로 유지한다.

---

## 12. Relation 확장 정책

기존 relation으로 설명되지 않는 관계가 반복적으로 필요해지면 relation 추가를 허용한다.

단, 1회성 이벤트 때문에 relation을 추가하지 않는다. Ontology-lite는 콘텐츠를 과하게 고정하는 장치가 아니라, 반복되는 관계를 분석 가능하게 만드는 최소 계약이다.

Relation 추가 조건:

- 2개 이상 이벤트/아이템/시나리오에서 재사용될 가능성이 있다.
- validator, analyzer, export 중 하나 이상에서 의미가 있다.
- 기존 tag/status/result로 표현하면 오히려 의미가 모호해진다.
- Content Expansion Phase 3 이후에도 유지 가능한 구조다.

Relation 추가 시 반드시 함께 갱신해야 하는 파일:

```text
data/core/ontology.yaml
docs/02_schema/09_Content_Ontology_Model_v0.1.md
```

Relation 추가를 보류해야 하는 경우:

- 특정 이벤트 하나만 설명한다.
- description이나 기존 tag 조합으로 충분히 설명된다.
- analyzer/export가 사용할 수 없는 장식적 관계다.
- PRD, World Bible, 별도 시스템이 있어야만 의미가 고정된다.

---

## 13. Ontology-lite v0.2 Trial Extension

Entity Sampling Review에서 보류했던 후보 중 Phase 3에서 실제 검증할 수 있는 최소 relation을 trial 상태로 추가한다.

Trial entity:

| Entity | 의미 | Source field | 유지 조건 |
| --- | --- | --- | --- |
| `clue` | 정보 표식 | `revealed_clue_tags`, `reveals_clue_tags` | Phase 3에서 2개 이상 이벤트/아이템이 사용 |
| `location` | region보다 작은 장소 표식 | `location_tags` | 반복 장소 분석이 region보다 유용함 |
| `omen` | hazard를 예고하는 표식 | `omen_tags`, `creates_omen_tags` | 경고와 payoff 분석이 가능함 |
| `hazard` | 구체 조우/장애/위험 장치 | `hazard_tags`, `counters_hazard_tags` | broad `danger_tags`보다 구체 counterplay 분석이 필요함 |

Trial relation:

| Relation | Source field | 역할 | 유지 조건 |
| --- | --- | --- | --- |
| `event_reveals_clue` | `event.revealed_clue_tags`, `choice.reveals_clue_tags`, `result.reveals_clue_tags` | 이벤트 단위 clue 노출 추적 | 2개 이상 이벤트에서 clue 노출이 선택 판단에 영향 |
| `item_reveals_clue` | `item.reveals_clue_tags` | item 기반 정보 payoff 추적 | 2개 이상 아이템/선택에서 item clue payoff 발생 |
| `event_occurs_at_location` | `event.location_tags` | region보다 작은 장소 coverage 추적 | 2개 이상 이벤트가 같은 location 축을 공유 |
| `omen_warns_about_hazard` | `event.omen_tags`, `event.hazard_tags`, `choice/result.creates_omen_tags` | omen과 구체 hazard의 warning/payoff 연결 | 2개 이상 이벤트에서 omen-hazard 연결이 읽힘 |

Trial source field:

```yaml
event:
  location_tags: list[string]
  revealed_clue_tags: list[string]
  omen_tags: list[string]
  hazard_tags: list[string]

choice:
  reveals_clue_tags: list[string]
  creates_omen_tags: list[string]

result:
  reveals_clue_tags: list[string]
  creates_omen_tags: list[string]

item:
  reveals_clue_tags: list[string]
  counters_hazard_tags: list[string]
```

기존 relation과의 차이:

- `event_belongs_to_region`은 넓은 지역 분류이고, `event_occurs_at_location`은 반복 가능한 구체 장소 표식이다.
- `event_has_danger_tag`는 넓은 위험 분류이고, `hazard_tags`/`omen_warns_about_hazard`는 구체 조우/장애/위험 장치와 그 경고 관계다.
- `item_counters_tag`는 broad tag 대응이고, `counters_hazard_tags`는 trial hazard 대응이다.
- `result_changes_event_weight`는 미래 이벤트 가중치 변화이고, `event_reveals_clue`/`item_reveals_clue`는 정보 노출 자체를 기록한다.

한계:

- v0.2 trial field는 아직 validator/analyzer/export가 소비하지 않을 수 있다.
- Phase 3 이후 사용성이 낮으면 제거하거나 기존 `tag`, `danger_tags`, `event_weight` 표현으로 통합할 수 있다.
- trial field는 고유 세계관 설정이 아니라 일반 태그이며, D&D/CoC 고유 설정명이나 원문 문장을 담지 않는다.

---

## 14. Entity/Ontology Gap 후보 상태 목록

v0.2에서 일부 후보는 trial relation으로 승격했고, 나머지는 계속 보류한다.

보류 원칙:

- source field와 target field가 YAML에서 안정적으로 지정되지 않으면 relation으로 승격하지 않는다.
- validator, analyzer, export가 소비하지 않는 관계는 문서상 후보로만 둔다.
- 기존 tag/status/result로 의미가 충분하면 새 relation을 만들지 않는다.
- Phase 3에서 2개 이상 이벤트/아이템/시나리오에 반복 사용되는지 확인한 뒤 승격한다.

| Relation 후보 | 현재 대체 표현 | 현재 판정 | 승격 조건 |
| --- | --- | --- | --- |
| `event_reveals_clue` | result message, event weight 변화 | v0.2 trial 추가 | Phase 3 이후 유지/제거 판단 |
| `clue_foreshadows_event` | warning message, later event weight 변화 | Phase 3 trial | 단서와 후속 event 연결이 반복될 때 |
| `event_occurs_at_location` | `event_belongs_to_region`, event tag | v0.2 trial 추가 | Phase 3 이후 유지/제거 판단 |
| `location_has_hazard` | `event_has_danger_tag`, region context | 보류 | location entity가 안정화된 뒤 |
| `choice_interacts_with_npc_role` | choice text, event description | 보류 | NPC role별 선택 분석이 필요할 때 |
| `choice_affects_faction` | reputation status 변화 | 보류 | faction별 상태나 평판 축이 생길 때 |
| `result_changes_resource_pressure` | `result_modifies_status` | 기존 relation으로 충분 | 현재 승격하지 않음 |
| `event_advances_mystery_thread` | event weight, result message | 보류 | 장기 mystery thread 진행도를 추적할 때 |
| `item_reveals_clue` | item-based choice result message | v0.2 trial 추가 | Phase 3 이후 유지/제거 판단 |
| `item_mitigates_hazard` | `item_counters_tag` | 기존 relation으로 충분 | 현재 승격하지 않음 |
| `route_leads_to_location` | event weight, region 암시 | Phase 3 trial | route 선택지가 location 이동을 반복적으로 만들 때 |
| `omen_warns_about_hazard` | warning message, danger tag | v0.2 trial 추가 | Phase 3 이후 유지/제거 판단 |

계속 보류하는 이유:

- `route`, `npc_role`, `faction`, `mystery_thread`는 아직 core entity나 안정적 source field가 아니다.
- source field 없는 relation은 validator/analyzer/export에서 사용할 수 없다.
- Phase 3 콘텐츠가 작성되기 전에는 보류 후보의 반복 사용 가능성을 검증할 수 없다.
- `item_mitigates_hazard`, `result_changes_resource_pressure`처럼 기존 relation으로 충분한 후보도 있다.

---

## 15. 콘텐츠 확장 준비와의 관계

Ontology-lite는 콘텐츠 확장 전에 관계 누락을 찾기 위한 기준으로 사용한다.

다음 단계 체크리스트:

```text
docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md
```

확장할 콘텐츠는 최소한 아래 질문에 답할 수 있어야 한다.

- 새 이벤트는 어떤 region/event/danger tag를 가지는가?
- 새 선택지는 어떤 item/status를 요구하는가?
- 새 아이템은 어떤 tag에 대응하거나 어떤 choice를 여는가?
- 새 result는 어떤 status 또는 event weight를 바꾸는가?
- 새 scenario는 어떤 source file과 event pool을 포함하는가?
