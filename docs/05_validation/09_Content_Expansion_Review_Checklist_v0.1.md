# Content Expansion Review Checklist

이 문서는 Content Expansion 구현 후 PRD/Flutter 이전에 통과해야 하는 검수 체크리스트다.

기준 문서:

- `docs/06_plans/01_Content_Expansion_Implementation_Plan_v0.1.md`
- `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
- `docs/02_schema/09_Content_Ontology_Model_v0.1.md`
- `data/core/ontology.yaml`

검수 목적:

```text
새 콘텐츠가 기존 YAML 구조 안에서 표현되는가
새 콘텐츠 관계가 Ontology-lite relation으로 설명되는가
Console Simulator validator/simulator/analyzer가 계속 통과하는가
금지된 구현 범위로 넘어가지 않았는가
```

---

# 1. 새 이벤트 Schema 검수

- [ ] 모든 새 event는 고유한 `id`를 가진다.
- [ ] 모든 새 event에는 `name`, `description`, `region_tags`, `event_tags`, `base_weight`, `choices`가 있다.
- [ ] `region_tags`는 `data/core/tags.yaml`의 `region` enum에 존재한다.
- [ ] `event_tags`는 `data/core/tags.yaml`의 `event` enum에 존재한다.
- [ ] `danger_tags`가 있으면 `data/core/tags.yaml`의 `danger` enum에 존재한다.
- [ ] `base_weight`는 0보다 큰 정수다.
- [ ] 각 event에는 최소 2개 이상의 choice가 있다. 단, 의도적으로 1개 choice인 경우 검수 기록에 이유를 남긴다.
- [ ] combat event는 일반 event + `event_tags: [combat]` + `choice_type: combat_response`로만 표현된다.
- [ ] event별 Python 분기나 별도 combat resolver가 없다.

검수 근거:

```text
event_has_choice
event_belongs_to_region
event_has_event_tag
event_has_danger_tag
```

---

# 2. 새 아이템 관계 검수

- [ ] 모든 새 item은 고유한 id를 가진다.
- [ ] 모든 새 item에는 `name`, `description`, `roles`, `tags`가 있다.
- [ ] item `roles`는 `data/core/item_roles.yaml`과 `data/core/tags.yaml`의 `item_role` enum에 모두 존재한다.
- [ ] item `tags`는 `data/core/tags.yaml`의 `item_tag` enum에 존재한다.
- [ ] `counters_tags`가 있으면 대응 대상 tag가 실제 이벤트 위험/테마와 연결된다.
- [ ] 새 item은 최소 1개 choice의 `requires_item` 또는 `requires_any_item`과 연결된다.
- [ ] 새 item이 획득만 가능하고 사용처가 없는 dead item으로 남지 않는다.
- [ ] item이 choice를 열거나 위험을 줄이는 방식이 로그/분석에서 추적 가능하다.

검수 근거:

```text
choice_requires_item
item_counters_tag
```

---

# 3. 새 Status / result_rules 검수

- [ ] 새 status는 기존 `health`, `food`, `money`, `reputation`, `curse`로 표현할 수 없을 때만 추가됐다.
- [ ] 새 status는 `data/core/statuses.yaml`에 `type`, `min`, `max`, `initial`을 가진다.
- [ ] 실패 조건이 있는 status는 `fail_when`을 명시한다.
- [ ] 새 status가 result로 변경된다면 `data/core/result_rules.yaml`에도 허용되어 있다.
- [ ] 새 status를 변경하는 event result가 최소 1개 존재한다.
- [ ] 새 status를 요구하는 choice가 있다면 `requires_status` 조건이 validator에서 통과한다.
- [ ] result `status_delta` key가 `statuses.yaml`과 `result_rules.yaml` 양쪽 계약을 모두 만족한다.
- [ ] result `event_weight` target은 `data/core/tags.yaml`의 `weight_target` enum에 존재한다.

검수 근거:

```text
choice_requires_status
result_modifies_status
result_changes_event_weight
```

---

# 4. Pack / Scenario 연결 검수

- [ ] 새 pack은 `data/content/packs/<pack_id>/` 아래에 있다.
- [ ] `<pack_id>`는 소문자 snake_case다.
- [ ] pack event도 base event와 같은 schema를 따른다.
- [ ] pack 전용 item이 없다면 불필요한 `items.yaml`을 만들지 않았다.
- [ ] 새 pack은 최소 1개 scenario의 `content_sources`에 연결되어 있다.
- [ ] 새 scenario는 `id`, `name`, `content_sources`, `include_regions`, `initial_status`, `initial_items`, `target_turns`, `seed`를 가진다.
- [ ] scenario `content_sources` 경로는 실제 파일로 존재한다.
- [ ] scenario filter는 `include_event_ids`, `include_event_tags`, `exclude_event_ids`, `exclude_event_tags` 계약을 지킨다.
- [ ] `include_event_ids`와 `include_event_tags`가 둘 다 있으면 AND 조건으로 해석됨을 전제로 작성됐다.
- [ ] exclude filter는 include filter 이후 적용된다는 계약을 깨지 않는다.
- [ ] scenario `validation_targets`가 새 콘텐츠 규모에 맞게 설정됐다.

검수 근거:

```text
scenario_includes_event
scenario_uses_content_source
```

---

# 5. ontology.yaml Relation 매핑 검수

새 콘텐츠는 아래 relation 중 하나 이상으로 설명되어야 한다.

- [ ] 새 event는 `event_has_choice`로 choice와 연결된다.
- [ ] 새 choice는 `choice_produces_result`로 result와 연결된다.
- [ ] item-gated choice는 `choice_requires_item`으로 설명된다.
- [ ] status-gated choice는 `choice_requires_status`로 설명된다.
- [ ] item의 위험 대응은 `item_counters_tag`로 설명된다.
- [ ] status 변경 result는 `result_modifies_status`로 설명된다.
- [ ] event weight 변경 result는 `result_changes_event_weight`로 설명된다.
- [ ] event region은 `event_belongs_to_region`으로 설명된다.
- [ ] event theme은 `event_has_event_tag`로 설명된다.
- [ ] event risk는 `event_has_danger_tag`로 설명된다.
- [ ] scenario의 event 노출은 `scenario_includes_event`로 설명된다.
- [ ] scenario의 source file 사용은 `scenario_uses_content_source`로 설명된다.

추가 판정:

- [ ] 기존 relation으로 설명되지 않는 새 관계가 있다면, 구현을 멈추고 `docs/02_schema/09_Content_Ontology_Model_v0.1.md`와 `data/core/ontology.yaml` 계약 갱신 필요 여부를 먼저 판단했다.
- [ ] relation 추가가 필요하더라도 GraphDB/RDF/OWL/ontology engine으로 확장하지 않았다.

---

# 6. Validator 통과 여부

필수 검증:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/<content_expansion_scenario>.yaml
```

체크:

- [ ] base scenario가 `VALIDATION: PASS`를 출력한다.
- [ ] content expansion scenario가 `VALIDATION: PASS`를 출력한다.
- [ ] duplicate event ID 오류가 없다.
- [ ] missing item/status/tag/choice_type reference 오류가 없다.
- [ ] result status/result_rules 불일치 오류가 없다.
- [ ] event_weight target 오류가 없다.
- [ ] scenario filter 결과가 validation target을 만족한다.

---

# 7. Console Simulator 재검증 여부

필수 검증:

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_base_regression_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/<content_expansion_scenario>.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_content_expansion_logs < /dev/null
```

체크:

- [ ] base scenario simulator가 exit code 0으로 끝난다.
- [ ] content expansion scenario simulator가 exit code 0으로 끝난다.
- [ ] non-TTY 모드에서 입력 대기하지 않는다.
- [ ] simulator가 `LOG: <path>`를 출력한다.
- [ ] 생성된 로그에 `schema_version`, `scenario_id`, `seed`, `run_id`가 있다.
- [ ] 각 turn log에 `event_id`, `choices_seen`, `selected_choice_id`, `state_before`, `state_after`, `regret_score`가 있다.
- [ ] unavailable choice가 있으면 `available: false`와 `unavailable_reason`이 기록된다.
- [ ] run summary에 `restart_intent_score`, `player_woven_score`, `run_failed`, `run_failed_but_interesting`이 있다.

---

# 8. analyze_logs Metric 출력 여부

필수 검증:

```bash
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_base_regression_logs
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_expansion_logs
```

체크:

- [ ] base logs analyzer가 exit code 0으로 끝난다.
- [ ] content expansion logs analyzer가 exit code 0으로 끝난다.
- [ ] analyzer output은 JSON이다.
- [ ] `meaningful_choice_count`가 출력된다.
- [ ] `item_unlocked_choice_count`가 출력된다.
- [ ] `bad_tradeoff_count`가 출력된다.
- [ ] `restart_intent_score_avg`가 출력된다.
- [ ] `run_failed_but_interesting_count`가 출력된다.
- [ ] `player_woven_score_avg`가 출력된다.
- [ ] 확장 콘텐츠의 item/choice/status 관계가 metric 해석을 왜곡하지 않는다.

---

# 9. 금지 작업 위반 여부

금지 작업 확인:

```bash
git diff --name-only -- src tools fate_weaver data/mvp0
find . -maxdepth 2 -type d | grep "fate_weaver\|data/mvp0" || true
grep -R "GraphDB\|Neo4j\|RDF\|OWL\|ontology_engine\|content_graph" README.md docs data || true
```

체크:

- [ ] Python 구현을 하지 않았다.
- [ ] `src/fateweaver/*.py`를 수정하지 않았다.
- [ ] `tools/*.py`를 수정하지 않았다.
- [ ] Flutter 프로젝트를 생성하지 않았다.
- [ ] `fate_weaver/`를 생성하지 않았다.
- [ ] `data/mvp0/`를 생성하지 않았다.
- [ ] GraphDB를 도입하지 않았다.
- [ ] RDF/OWL을 도입하지 않았다.
- [ ] `ontology_engine.py`를 만들지 않았다.
- [ ] `content_graph.py`를 만들지 않았다.
- [ ] PRD를 작성하지 않았다.
- [ ] World Bible을 작성하지 않았다.
- [ ] 이벤트별 Python if문 하드코딩을 추가하지 않았다.

---

# 10. 완료 판정 기준

## PASS

아래 조건을 모두 만족하면 PASS다.

- [ ] Section 1-9가 모두 통과한다.
- [ ] 새 콘텐츠가 기존 YAML 구조 안에 있다.
- [ ] 새 콘텐츠 관계가 Ontology-lite relation으로 설명된다.
- [ ] base scenario와 expansion scenario가 validator를 통과한다.
- [ ] base scenario와 expansion scenario가 Console Simulator non-TTY 실행을 통과한다.
- [ ] analyzer가 Core Loop Validation Metrics를 출력한다.
- [ ] 금지 작업 위반이 없다.

판정:

```text
CONTENT_EXPANSION_REVIEW_PASS
```

## NEEDS_SMALL_FIX

아래 중 하나라도 있으면 소폭 보강 후 재검수다.

- [ ] 콘텐츠는 실행되지만 relation mapping 근거가 일부 부족하다.
- [ ] scenario validation target이 너무 약해 확장 콘텐츠 노출을 충분히 증명하지 못한다.
- [ ] analyzer metric은 출력되지만 item/status 영향 해석이 불명확하다.
- [ ] 문서 참조 경로가 일부 누락됐다.

판정:

```text
NEEDS_SMALL_FIX
```

## BLOCKED

아래 중 하나라도 있으면 차단이다.

- [ ] validator가 실패한다.
- [ ] Console Simulator가 입력 대기하거나 실패한다.
- [ ] analyzer가 metric JSON을 출력하지 못한다.
- [ ] 새 event/item/status가 core enum 또는 ontology relation으로 설명되지 않는다.
- [ ] `src/`, `tools/`, Flutter, GraphDB/RDF/OWL 등 금지 범위를 건드렸다.
- [ ] `data/content` 구조를 기존 계약 밖으로 바꿨다.

판정:

```text
BLOCKED
```
