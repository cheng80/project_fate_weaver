# Content Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand FateWeaver content safely while preserving the Console Simulator PASS baseline and Ontology-lite relationship contract.

> 기준 구분: 이 계획은 Console Simulator PASS 이후 콘텐츠 확장 계획이다. Gameplay Replan 관련 새 구현/기획에서는 `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`와 `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`를 우선한다.

**Architecture:** Content remains YAML-first: `data/core/` owns enums and rules, `data/content/` owns reusable event/item packs, and `data/scenarios/` owns validation slices. The Python Console Simulator is a verifier, not a content authoring target, so expansion work must be validated through existing CLI commands instead of changing `src/` or `tools/`.

**Tech Stack:** YAML content contracts, Python 3.12 Console Validation CLI, `PyYAML`, `unittest`, Ontology-lite via `data/core/ontology.yaml`.

---

## 1. Content Expansion 목표

Content Expansion의 목표는 새 이벤트, 아이템, 상태, 콘텐츠 pack, scenario를 추가하되 아래 기준을 깨지 않는 것이다.

```text
Console Simulator implementation: PASS
Ontology-lite: READY
Next focus: Content Expansion Readiness
```

확장 결과는 반드시 다음을 만족해야 한다.

- 이벤트 중심 판타지 로그라이크 정체성을 유지한다.
- `data/core`, `data/content`, `data/scenarios` 역할을 섞지 않는다.
- 새 콘텐츠 관계가 `data/core/ontology.yaml`의 entity/relation으로 설명된다.
- 기존 Console Simulator validator, simulator, analyzer 명령이 계속 통과한다.
- Flutter, PRD, World Bible, GraphDB, RDF/OWL 작업으로 넘어가지 않는다.

---

## 2. File Structure

Content Expansion 구현 시 예상 파일 책임은 아래와 같다.

- Modify: `data/core/tags.yaml`
  - 새 region/event/danger/item/weight tag enum이 필요할 때만 수정한다.
- Modify: `data/core/item_roles.yaml`
  - 새 item role이 기존 role로 설명되지 않을 때만 수정한다.
- Modify: `data/core/statuses.yaml`
  - 새 status가 실제 run state로 필요할 때만 수정한다.
- Modify: `data/core/result_rules.yaml`
  - 새 status가 result로 변경될 수 있을 때 함께 수정한다.
- Modify: `data/core/ontology.yaml`
  - 새 콘텐츠 관계가 기존 relation으로 설명되지 않을 때만 수정한다.
- Modify: `data/content/base/events.yaml`
  - 기본 공용 이벤트를 추가한다.
- Modify: `data/content/base/items.yaml`
  - 기본 공용 아이템을 추가한다.
- Create or Modify: `data/content/packs/<pack_id>/events.yaml`
  - 특정 테마 pack 이벤트를 추가한다.
- Create or Modify: `data/content/packs/<pack_id>/items.yaml`
  - 특정 테마 pack 아이템이 필요할 때만 추가한다.
- Create or Modify: `data/scenarios/<scenario_id>.yaml`
  - 확장 콘텐츠 검증용 scenario를 추가하거나 기존 scenario의 source/filter를 갱신한다.
- Modify: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
  - 확장 완료 후 체크 상태와 근거를 갱신한다.

Do not modify:

- `src/fateweaver/*.py`
- `tools/*.py`
- `fate_weaver/`
- `data/mvp0/`
- PRD 문서
- World Bible 문서

---

## 3. 이벤트 추가 기준

새 이벤트는 `Event Schema`를 지켜야 한다.

필수 필드:

```yaml
id: string
name: string
description: string
region_tags: [forest]
event_tags: [exploration]
danger_tags: [lost]
base_weight: 10
choices:
  - id: safe_choice
    text: "상황을 관찰한다"
    type: safe
    risk_level: low
    result:
      status_delta:
        food: -1
```

기준:

- `id`는 전체 content source 안에서 중복되면 안 된다.
- `region_tags`는 `data/core/tags.yaml:tags.region`에 있어야 한다.
- `event_tags`는 `data/core/tags.yaml:tags.event`에 있어야 한다.
- `danger_tags`는 `data/core/tags.yaml:tags.danger`에 있어야 한다.
- `base_weight`는 0보다 큰 정수로 둔다.
- `choices`는 최소 2개 이상 권장한다.
- 전투형 이벤트는 `event_tags: [combat]`을 가진 일반 이벤트로만 표현한다.
- 별도 combat loop, enemy HP, attack/defense turn을 만들지 않는다.

Ontology-lite 확인:

- `event_has_choice`
- `event_belongs_to_region`
- `event_has_event_tag`
- `event_has_danger_tag`

---

## 4. 아이템 추가 기준

새 아이템은 실제 선택지나 위험 대응과 연결되어야 한다.

권장 형식:

```yaml
items:
  new_item_id:
    name: "새 아이템"
    description: "어떤 위험이나 선택지를 바꾸는지 설명한다."
    roles: [unlock]
    tags: [tool]
    counters_tags: [trap]
```

기준:

- `roles`는 `data/core/item_roles.yaml`과 `data/core/tags.yaml:tags.item_role`에 모두 있어야 한다.
- `tags`는 `data/core/tags.yaml:tags.item_tag`에 있어야 한다.
- `counters_tags`가 있으면 대상 tag는 `data/core/tags.yaml`의 danger/event/weight 의미와 충돌하지 않아야 한다.
- 새 아이템은 최소 1개 choice의 `requires_item` 또는 `requires_any_item`과 연결되어야 한다.
- dead item을 만들지 않는다. 즉, 아이템은 획득/소모/해금/위험 완화 중 하나 이상의 쓰임이 있어야 한다.

Ontology-lite 확인:

- `choice_requires_item`
- `item_counters_tag`

---

## 5. 상태/status 추가 기준

새 status는 매우 보수적으로 추가한다.

추가 조건:

- 기존 `health`, `food`, `money`, `reputation`, `curse`로 표현할 수 없어야 한다.
- Console Validation에서 선택 결과나 실패 조건에 실제 영향을 줘야 한다.
- Flutter UI를 상상해서 미리 추가하지 않는다.

필요 파일:

```text
data/core/statuses.yaml
data/core/result_rules.yaml
```

권장 형식:

```yaml
statuses:
  new_status:
    type: int
    min: 0
    max: 10
    initial: 0
```

검증 기준:

- `statuses.yaml`에 min/max/initial이 있다.
- failure state라면 `fail_when`을 명시한다.
- `result_rules.yaml`에서 result가 해당 status를 변경할 수 있도록 허용한다.
- 새 status를 변경하는 이벤트 result가 최소 1개 있어야 한다.

Ontology-lite 확인:

- `choice_requires_status`
- `result_modifies_status`

---

## 6. Pack 추가 기준

Pack은 테마성 콘텐츠 묶음이다. `data/content` 구조를 바꾸지 않고 기존 구조 안에 추가한다.

허용 구조:

```text
data/content/packs/<pack_id>/events.yaml
data/content/packs/<pack_id>/items.yaml
```

기준:

- `<pack_id>`는 소문자 snake_case로 둔다.
- pack 이벤트도 base 이벤트와 동일한 Event Schema를 따른다.
- pack 전용 아이템이 없으면 `items.yaml`을 만들지 않는다.
- pack은 scenario의 `content_sources`에서 명시적으로 참조되어야 검증된다.
- pack 추가만 하고 scenario에 연결하지 않는 상태로 끝내지 않는다.

---

## 7. Scenario 추가/갱신 기준

Scenario는 테스트 조건이지 콘텐츠 본문이 아니다.

필수 필드:

```yaml
id: content_expansion_test
name: "Content Expansion Test"
content_sources:
  - data/content/base/events.yaml
  - data/content/packs/<pack_id>/events.yaml
include_regions: [forest]
initial_status:
  health: 7
  food: 5
  money: 2
  reputation: 0
  curse: 1
initial_items: [rope, torch]
target_turns: 20
seed: 42
validation_targets:
  min_events: 10
  min_combat_events: 1
  min_curse_events: 1
```

`min_curse_events`는 메인 QA 목표가 아니라 curse가 상태/위험 요소 중 하나로 필터와 검증에 반영되는지 확인하는 보조 coverage다.

Filter 기준:

- `include_event_ids`만 있으면 ID 필터다.
- `include_event_tags`만 있으면 tag 필터다.
- 둘 다 있으면 AND 조건이다.
- `exclude_event_ids`와 `exclude_event_tags`는 include 이후 적용한다.
- include ids/tags가 모두 없으면 `content_sources + include_regions` 기준 전체 이벤트를 사용한다.

Ontology-lite 확인:

- `scenario_includes_event`
- `scenario_uses_content_source`

---

## 8. ontology.yaml relation 유지 기준

기존 relation으로 설명 가능한 콘텐츠만 추가하는 것이 기본이다.

필수 relation:

```text
event_has_choice
choice_produces_result
choice_requires_item
choice_requires_status
item_counters_tag
result_modifies_status
result_changes_event_weight
event_belongs_to_region
event_has_event_tag
event_has_danger_tag
scenario_includes_event
scenario_uses_content_source
```

수정 기준:

- 새 콘텐츠 관계가 위 relation으로 설명되면 `data/core/ontology.yaml`을 수정하지 않는다.
- 설명되지 않는 관계가 실제로 필요하면 먼저 `docs/02_schema/09_Content_Ontology_Model_v0.1.md`와 `data/core/ontology.yaml`의 relation 계약을 갱신한다.
- GraphDB, RDF, OWL, ontology engine은 만들지 않는다.

---

## 9. Validator로 확인해야 할 항목

Content Expansion 구현 후 validator는 최소 아래를 확인해야 한다.

- content source 경로가 실제 존재한다.
- duplicate event ID가 없다.
- event region/event/danger tag가 core enum에 존재한다.
- choice type이 `data/core/choice_types.yaml`에 존재한다.
- required item이 실제 item 목록에 존재한다.
- required status가 `statuses.yaml`에 존재한다.
- item role이 `item_roles.yaml`과 `tags.yaml:item_role`에 존재한다.
- item tag가 `tags.yaml:item_tag`에 존재한다.
- result status가 `statuses.yaml`과 `result_rules.yaml`에서 허용된다.
- event_weight target이 `tags.yaml:weight_target`에 존재한다.
- scenario filter 결과가 validation target을 만족한다.

---

## 10. Console Simulator 재검증 명령

기본 smoke:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1 < /dev/null
.venv/bin/python tools/analyze_logs.py --logs logs
```

확장 scenario 추가 시:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/<scenario_id>.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/<scenario_id>.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_content_expansion_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_expansion_logs
```

Regression suite:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

Expected:

```text
VALIDATION: PASS
console_simulator prints LOG: <path>
analyze_logs prints JSON with Core Loop Validation Metrics
unittest exits 0
```

---

## 11. 금지 작업

Content Expansion 중 금지한다.

```text
Python 구현 금지
src/fateweaver/*.py 수정 금지
tools/*.py 수정 금지
data/content 구조 변경 금지
data/mvp0/ 생성 금지
Flutter 프로젝트 생성 금지
fate_weaver/ 생성 금지
GraphDB 도입 금지
RDF/OWL 도입 금지
ontology_engine.py 생성 금지
content_graph.py 생성 금지
PRD 작성 금지
World Bible 작성 금지
이벤트별 Python if문 하드코딩 금지
```

---

## 12. Task Plan

### Task 1: Expansion Scope Lock

**Files:**
- Read: `README.md`
- Read: `docs/00_index/README_Docs_Index.md`
- Read: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
- Modify: no files

- [ ] **Step 1: Confirm target expansion slice**

Write a short local note in the task output, not in repo files:

```text
Expansion slice:
- new events:
- new items:
- new statuses:
- new packs:
- new scenarios:
Forbidden:
- no Python
- no Flutter
- no GraphDB/RDF/OWL
```

- [ ] **Step 2: Check current git state**

Run:

```bash
git status --short --branch
```

Expected:

```text
No unrelated dirty files that overlap data/core, data/content, data/scenarios, docs.
```

- [ ] **Step 3: Commit checkpoint if needed**

If the worktree already has unrelated changes, stop and separate them before content expansion.

---

### Task 2: Core Enum Impact Audit

**Files:**
- Read: `data/core/tags.yaml`
- Read: `data/core/item_roles.yaml`
- Read: `data/core/statuses.yaml`
- Read: `data/core/result_rules.yaml`
- Modify: only the required `data/core/*.yaml` files

- [ ] **Step 1: List every new tag/status/role needed**

Use this table in the task output:

```text
new region tags:
new event tags:
new danger tags:
new item roles:
new item tags:
new weight targets:
new statuses:
```

- [ ] **Step 2: Reject speculative core additions**

For each proposed core addition, keep only entries used by at least one planned event, item, result, or scenario.

- [ ] **Step 3: Edit core YAML only if required**

If no core additions are required, do not touch `data/core`.

- [ ] **Step 4: Validate base scenario still passes**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

Expected:

```text
VALIDATION: PASS
```

---

### Task 3: Event Content Expansion

**Files:**
- Modify: `data/content/base/events.yaml`
- Create or Modify: `data/content/packs/<pack_id>/events.yaml`

- [ ] **Step 1: Add events using the Event Schema**

Each new event must include:

```yaml
id: unique_event_id
name: "Readable Event Name"
description: "One concrete situation the player can understand."
region_tags: [forest]
event_tags: [exploration]
danger_tags: [lost]
base_weight: 10
choices:
  - id: observe
    text: "주변을 살핀다"
    type: safe
    risk_level: low
    result:
      status_delta:
        food: -1
  - id: take_risk
    text: "위험을 감수한다"
    type: gamble
    risk_level: high
    result:
      status_delta:
        health: -1
        reputation: 1
```

- [ ] **Step 2: Verify relation coverage**

For every new event, map it to:

```text
event_has_choice:
choice_produces_result:
event_belongs_to_region:
event_has_event_tag:
event_has_danger_tag:
choice_requires_item:
choice_requires_status:
result_modifies_status:
result_changes_event_weight:
```

- [ ] **Step 3: Validate**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

Expected:

```text
VALIDATION: PASS
```

---

### Task 4: Item Content Expansion

**Files:**
- Modify: `data/content/base/items.yaml`
- Create or Modify: `data/content/packs/<pack_id>/items.yaml`
- Modify: event files that reference new items

- [ ] **Step 1: Add item only when it affects choices**

Each new item must map to at least one choice:

```yaml
items:
  signal_whistle:
    name: "Signal Whistle"
    description: "A tool that helps avoid ambush or call aid."
    roles: [unlock]
    tags: [tool]
    counters_tags: [bandit]
```

- [ ] **Step 2: Add choice requirement**

Reference the item from an event choice:

```yaml
requires_item: signal_whistle
```

or:

```yaml
requires_any_item: [signal_whistle, torch]
```

- [ ] **Step 3: Verify relation coverage**

For every new item, map it to:

```text
choice_requires_item:
item_counters_tag:
```

- [ ] **Step 4: Validate**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

Expected:

```text
VALIDATION: PASS
```

---

### Task 5: Scenario Coverage Expansion

**Files:**
- Create or Modify: `data/scenarios/<scenario_id>.yaml`

- [ ] **Step 1: Create scenario for the new content slice**

Use this structure:

```yaml
id: content_expansion_test
name: "Content Expansion Test"
content_sources:
  - data/content/base/events.yaml
  - data/content/packs/<pack_id>/events.yaml
include_regions: [forest]
initial_status:
  health: 7
  food: 5
  money: 2
  reputation: 0
  curse: 1
initial_items: [rope, torch]
target_turns: 20
seed: 42
validation_targets:
  min_events: 10
  min_combat_events: 1
  min_curse_events: 1
```

`min_curse_events`는 메인 QA 목표가 아니라 curse가 상태/위험 요소 중 하나로 필터와 검증에 반영되는지 확인하는 보조 coverage다.

- [ ] **Step 2: Apply filters intentionally**

If using filters, document which rule applies:

```text
include_event_ids only: ID filter
include_event_tags only: tag filter
include_event_ids + include_event_tags: AND filter
exclude filters: applied after include filters
```

- [ ] **Step 3: Verify relation coverage**

Map scenario to:

```text
scenario_includes_event:
scenario_uses_content_source:
```

- [ ] **Step 4: Validate new scenario**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
VALIDATION: PASS
```

---

### Task 6: Console Simulator Regression

**Files:**
- Read: generated log files only
- Do not modify: `src/`, `tools/`

- [ ] **Step 1: Run base scenario**

Run:

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_base_regression_logs < /dev/null
```

Expected:

```text
LOG: /tmp/fateweaver_base_regression_logs/run_mvp0_console_test_...
```

- [ ] **Step 2: Analyze base logs**

Run:

```bash
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_base_regression_logs
```

Expected JSON keys:

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
restart_intent_score_avg
run_failed_but_interesting_count
player_woven_score_avg
```

- [ ] **Step 3: Run expanded scenario**

Run:

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_content_expansion_logs < /dev/null
```

Expected:

```text
LOG: /tmp/fateweaver_content_expansion_logs/run_content_expansion_test_...
```

- [ ] **Step 4: Analyze expanded logs**

Run:

```bash
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_expansion_logs
```

Expected JSON keys:

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
restart_intent_score_avg
run_failed_but_interesting_count
player_woven_score_avg
```

---

### Task 7: Readiness Checklist Update

**Files:**
- Modify: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`

- [ ] **Step 1: Mark only verified checklist items**

Change `[ ]` to `[x]` only when a command or relation map proves the item.

- [ ] **Step 2: Add evidence commands**

Record exact commands under the relevant checklist section:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_content_expansion_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_expansion_logs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

- [ ] **Step 3: Keep final 판정 honest**

Use one of:

```text
CONTENT_EXPANSION_READY
NEEDS_SMALL_FIX
BLOCKED
```

---

### Task 8: Final Verification and Commit

**Files:**
- Stage only files changed for Content Expansion.

- [ ] **Step 1: Verify forbidden paths are untouched**

Run:

```bash
git diff --name-only -- src tools fate_weaver data/mvp0
```

Expected:

```text
No output
```

- [ ] **Step 2: Verify no structure drift**

Run:

```bash
find data -maxdepth 4 -type f | sort
find docs -maxdepth 3 -type f | sort
```

Expected:

```text
New content files and scenario files appear only in approved locations.
```

- [ ] **Step 3: Run full regression**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_content_expansion_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_expansion_logs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

Expected:

```text
VALIDATION: PASS
simulator exits 0
analyzer emits metric JSON
unittest exits 0
```

- [ ] **Step 4: Commit**

Use a focused commit message:

```bash
git add data docs
git commit -m "feat(content): expand validation content"
```

---

## 13. 완료 조건

Content Expansion은 아래 조건을 모두 만족해야 완료다.

- 새 이벤트가 Event Schema와 tag enum을 지킨다.
- 새 아이템이 item role/tag enum을 지키고 최소 1개 choice와 연결된다.
- 새 status가 있다면 `statuses.yaml`과 `result_rules.yaml`이 함께 갱신된다.
- 새 pack이 있다면 scenario `content_sources`에 연결된다.
- 새 scenario가 filter 계약을 지킨다.
- 새 관계가 Ontology-lite relation으로 설명된다.
- `validate_data`가 base scenario와 expansion scenario에서 통과한다.
- `console_simulator`가 non-TTY 모드에서 입력 대기 없이 완료된다.
- `analyze_logs`가 Core Loop Validation Metrics를 출력한다.
- `unittest discover -s tests`가 통과한다.
- `src/`, `tools/`, `fate_weaver/`, `data/mvp0/` 변경이 없다.
- GraphDB/RDF/OWL/PRD/World Bible 작업이 없다.

Final 판정:

```text
CONTENT_EXPANSION_READY
NEEDS_SMALL_FIX
BLOCKED
```

---

## 14. Self-Review

Spec coverage:

- Content Expansion 목표: Section 1
- 이벤트 추가 기준: Section 3
- 아이템 추가 기준: Section 4
- 상태/status 추가 기준: Section 5
- pack 추가 기준: Section 6
- scenario 추가/갱신 기준: Section 7
- ontology.yaml relation 유지 기준: Section 8
- validator 확인 항목: Section 9
- Console Simulator 재검증 명령: Section 10
- 금지 작업: Section 11
- 완료 조건: Section 13

Placeholder scan:

```text
No placeholder red flags or unspecified validation steps.
```

Type and contract consistency:

```text
All relation names match data/core/ontology.yaml.
All scenario filter rules match docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md.
All validation commands use .venv/bin/python.
```
