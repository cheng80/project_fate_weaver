# Project FateWeaver Content Ontology Model v0.1

## 1. 목적

이 문서는 FateWeaver 콘텐츠를 관계 중심으로 분석하기 위한 Ontology-lite 계약을 정의한다.

현재 목표는 온톨로지 엔진을 만드는 것이 아니라, 기존 YAML 데이터가 어떤 entity와 relation으로 해석될 수 있는지 고정하는 것이다.

현재 상태:

```text
Console Simulator implementation: PASS
Ontology-lite: READY
Next focus: Content Expansion Readiness
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
description:
source_fields:
future_use:
```

현재 Console Validation은 이 파일을 실행 중에 읽지 않는다. 지금은 문서/데이터 계약이며, 나중에 분석 도구가 읽을 수 있도록 YAML로 둔다.

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
- 예: "저주를 높이고, 성수로만 대응 가능하며, 숲 시나리오에서 3턴 안에 노출될 수 있는 이벤트" 같은 질의가 자주 필요해진다.
- 여러 작가/디자이너가 동시에 콘텐츠 관계를 편집하고 충돌을 분석해야 한다.
- Flutter export, balance analyzer, content generator가 같은 관계 그래프를 실시간으로 공유해야 한다.

그 전까지는 `data/core/ontology.yaml`과 파일 기반 분석으로 유지한다.

---

## 12. 콘텐츠 확장 준비와의 관계

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
