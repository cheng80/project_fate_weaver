# Content Expansion Readiness Checklist

이 체크리스트는 Console Simulator 구현 검수 PASS 이후, 콘텐츠 확장 전에 확인해야 하는 검수 기준이다.

## 검수 목적

다음 단계는 PRD나 Flutter 제작이 아니라, 기존 Console Validation과 Ontology-lite 계약을 유지한 채 이벤트, 아이템, 상태, 팩, 시나리오를 안전하게 확장할 수 있는지 확인하는 것이다.

```text
Console Simulator implementation: PASS
Ontology-lite: READY
Next focus: Content Expansion Readiness
```

---

# 1. Event 확장 체크

- [ ] 이벤트 추가 시 `data/core/tags.yaml`의 region/event/danger tag enum 누락이 없는지 확인한다.
- [ ] 이벤트 추가 시 `event -> choice -> result` 관계가 `data/core/ontology.yaml` relation으로 설명 가능한지 확인한다.
- [ ] 이벤트 추가 시 `event_belongs_to_region`, `event_has_event_tag`, `event_has_danger_tag` relation이 해석 가능한지 확인한다.
- [ ] 전투형 이벤트는 여전히 일반 event + `combat_response` choice로만 표현한다.

---

# 2. Item 확장 체크

- [ ] 아이템 추가 시 `counters_tags` 또는 choice `requires_item` 관계가 명확한지 확인한다.
- [ ] 아이템 role은 `data/core/item_roles.yaml`과 `data/core/tags.yaml`의 `item_role` enum에 모두 존재해야 한다.
- [ ] 아이템 tag는 `data/core/tags.yaml`의 `item_tag` enum에 존재해야 한다.
- [ ] 새 아이템이 실제 choice를 unlock하거나 risk를 줄이는지 확인한다.

---

# 3. Status / Result 확장 체크

- [ ] 상태 추가 시 `data/core/statuses.yaml`에 min/max/initial/fail_when 필요 여부를 반영한다.
- [ ] 상태 추가 시 `data/core/result_rules.yaml`의 allowed status 계약을 갱신한다.
- [ ] result가 변경하는 status는 `result_modifies_status` relation으로 설명 가능해야 한다.
- [ ] result가 event weight를 바꾸면 target tag가 `weight_target` enum에 있어야 한다.

---

# 4. Pack / Scenario 확장 체크

- [ ] pack 추가 시 scenario의 `content_sources`에서 참조 가능한 경로인지 확인한다.
- [ ] scenario 추가 시 `include_regions`, `include_event_ids`, `include_event_tags` 계약을 지킨다.
- [ ] scenario 추가 시 `exclude_event_ids`, `exclude_event_tags`가 include 이후 적용되는 계약을 지킨다.
- [ ] scenario가 노출하는 event는 `scenario_includes_event` relation으로 설명 가능해야 한다.
- [ ] scenario가 사용하는 source file은 `scenario_uses_content_source` relation으로 설명 가능해야 한다.

---

# 5. Ontology-lite 체크

- [ ] `data/core/ontology.yaml`에 필요한 entity가 누락되지 않았는지 확인한다.
- [ ] `data/core/ontology.yaml`에 필요한 relation이 누락되지 않았는지 확인한다.
- [ ] 새 콘텐츠 관계가 기존 relation으로 설명되지 않으면 문서와 ontology 계약을 먼저 갱신한다.
- [ ] Ontology-lite는 계약 파일이며, 별도 ontology engine을 만들지 않는다.

---

# 6. Console Validation 체크

- [ ] 확장 데이터에서도 Console Simulator validator가 통과해야 한다.
- [ ] 확장 데이터에서도 Core Loop Validation Metrics가 계산되어야 한다.
- [ ] `meaningful_choice_count`가 확장 콘텐츠에서 해석 가능해야 한다.
- [ ] `item_unlocked_choice_count`가 새 item/choice 관계를 반영해야 한다.
- [ ] `bad_tradeoff_count`, `restart_intent_score_avg`, `run_failed_but_interesting_count`, `player_woven_score_avg`가 계속 출력되어야 한다.

검증 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1
.venv/bin/python tools/analyze_logs.py --logs logs
```

---

# 7. 금지 작업 유지 체크

- [ ] GraphDB 도입 금지를 유지한다.
- [ ] RDF/OWL 도입 금지를 유지한다.
- [ ] `data/content` 구조 변경 금지를 유지한다.
- [ ] `data/mvp0/` 생성 금지를 유지한다.
- [ ] Flutter 프로젝트 생성을 하지 않는다.
- [ ] `fate_weaver/` 생성을 하지 않는다.
- [ ] PRD 작성 전에 콘텐츠 확장 계약을 먼저 검증한다.
- [ ] World Bible 작성 전에 이벤트/아이템/상태 관계 검증을 먼저 수행한다.

---

# 8. 완료 판정

`Content Expansion Readiness` 통과 조건:

- [ ] Section 1-7 체크가 모두 통과한다.
- [ ] 새 콘텐츠가 기존 YAML 구조 안에서 표현된다.
- [ ] 새 콘텐츠 관계가 Ontology-lite relation으로 설명된다.
- [ ] Console Simulator validator와 analyzer가 확장 데이터에서도 작동한다.

판정:

```text
CONTENT_EXPANSION_READY
NEEDS_SMALL_FIX
BLOCKED
```
