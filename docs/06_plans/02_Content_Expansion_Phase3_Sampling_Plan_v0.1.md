# Content Expansion Phase 3 표본 추출 계획 v0.1

> **에이전트 작업자 필수 지침:** 이 계획을 실행할 때는 `superpowers:subagent-driven-development` 사용을 권장한다. 대안으로 `superpowers:executing-plans`를 사용해도 된다. 각 단계는 체크박스(`- [ ]`) 단위로 추적한다.

**목표:** 새 YAML 콘텐츠를 작성하기 전에 FateWeaver Phase 3에서 어떤 이벤트, 아이템, Ontology-lite entity 표본을 어떤 기준으로 뽑을지 고정한다.

**구조:** Phase 3는 scoring weight를 크게 흔들거나 새 런타임 시스템을 만들지 않고, 기존 `signal_grove_pack` 콘텐츠 풀을 확장한다. 표본 추출 기준은 `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`와 `docs/07_reviews/12_TRPG_Content_Research_Notes_v0.1.md`를 따른다. 모든 표본은 event, choice, result, item, status, tag 관계로 설명 가능해야 하며 Console Simulator 로그에서 실제 선택 압력을 만들어야 한다.

**기술 기준:** YAML 콘텐츠 계약, Python 3.12 Console Validation CLI, `PyYAML`, `unittest`, `data/core/ontology.yaml` 기반 Ontology-lite, Markdown 계획 문서.

---

## 1. 범위

이 문서는 구현 패치가 아니라 표본 추출 계획서다.

이번 계획서 작성 단계에서 생성하는 파일:

- 생성: `docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md`

Phase 3 실행 단계에서 수정할 수 있는 파일:

- 수정: `data/content/packs/signal_grove_pack/events.yaml`
  - 선택 다양성을 늘리고 반복 item choice 지배를 낮출 이벤트 표본을 추가한다.
- 수정: `data/content/packs/signal_grove_pack/items.yaml`
  - 선택지 해금, 정보 공개, 위험 완화, 비용 전환, 보상 증폭, future weight 조절 중 하나를 수행하는 아이템만 추가한다.
- 수정: `data/scenarios/content_expansion_test.yaml`
  - Phase 3 이벤트 id와 아이템 id를 검증 slice에 연결한다.
- 수정: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
  - Phase 3 표본 추가와 검증 근거를 기록한다.
- 수정: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
  - metric 변화가 의미 있을 때 Phase 3 playtest 결과를 덧붙인다.

별도 승인 없이 Phase 3 실행에서 수정하지 않을 파일:

- `data/core/*.yaml`
- `src/fateweaver/*.py`
- `tools/*.py`
- `tests/*.py`
- `fate_weaver/`

도입하지 않는 것:

- Flutter 프로젝트 파일
- GraphDB, RDF, OWL, ontology engine
- PRD
- World Bible
- 이벤트별 Python 분기
- 별도 combat subsystem

---

## 2. Phase 3 표본 추출 목표

Phase 3 표본 추출은 Playtest Review와 Scoring Observability에서 확인된 한계를 콘텐츠 측면에서 해결하기 위한 작업이다.

주요 목표:

1. 이벤트 풀을 늘려 profile 차이가 weight 튜닝이 아니라 콘텐츠 다양성에서 나오게 한다.
2. 단일 item-based choice가 반복 지배하는 문제를 줄이기 위해 non-item 대안과 다양한 item 기능을 제공한다.
3. `curious_leaning`이 선택할 만한 조사, 단서, 예고 선택지를 늘리되 profile별 결과를 강제로 만들지 않는다.
4. `safe_leaning`이 낮은 bad tradeoff를 유지할 수 있도록 신뢰 가능한 안전 선택지를 둔다.
5. `greedy_leaning`이 money, item, reputation 보상을 노릴 수 있도록 health, reputation, curse 같은 상태/자원 비용이 붙은 유혹을 둔다.
6. `desperate`가 낮은 health/food 상황에서 의미 있는 회복 tradeoff를 만나게 한다.
7. `requires_item`, `requires_status`는 availability gate로만 사용하고 `unavailable_selected = 0`을 유지한다.
8. 새 콘텐츠는 기존 Ontology-lite relation으로 설명 가능해야 한다.

비목표:

- Phase 3 표본 추출 과정에서 profile weight를 튜닝하지 않는다.
- 기존 `health`, `food`, `money`, `reputation`, `curse`로 표현 가능한 압력에 새 status를 추가하지 않는다.
- 기존 tag로 표현 가능한 이벤트에 새 core tag를 추가하지 않는다.
- combat 이벤트를 별도 전투 모델로 바꾸지 않는다.

---

## 3. 표본 추출 기준

각 이벤트 표본은 아래 최소 구조를 만족해야 한다.

```yaml
id: phase3_specific_event_id
name: "짧은 장면명"
description: "현재 압박이 보이는 한 문장"
region_tags: [forest]
event_tags: [exploration]
danger_tags: [lost]
base_weight: 5
choices:
  - id: safe_or_investigate_choice
    text: "정보를 얻거나 피해를 줄이는 선택"
    type: investigate
    risk_level: low
    result:
      event_weight: {lost: -1}
      message: "다음 선택 판단에 쓸 수 있는 결과"
  - id: risky_or_greedy_choice
    text: "보상을 노리고 위험을 감수하는 선택"
    type: gamble
    risk_level: high
    result:
      status: {curse: +1, money: +2}
      event_weight: {curse: +1}
      message: "보상과 대가가 함께 보이는 결과"
  - id: item_or_survival_choice
    text: "아이템이나 생존 자원을 활용하는 선택"
    type: item_based
    risk_level: low
    requires_item: signal_chalk
    result:
      event_weight: {lost: -2}
      message: "아이템이 비용을 바꾸거나 정보를 드러내는 결과"
```

필수 판정 기준:

- 선택지는 최소 2개, 권장 3개다.
- item choice가 available이어도 의미 있는 non-item choice가 최소 1개 남아야 한다.
- 최소 1개 choice는 `health`, `food`, `money`, `reputation`, `curse`, item availability, future event weight 중 하나를 바꿔야 한다.
- 최소 1개 choice는 safe, greedy, curious, desperate 중 하나의 선택 압력을 검수할 수 있어야 한다.
- 새 schema field를 요구하지 않는다.
- 원문 TRPG 설정, 고유명, 문장을 차용하지 않는다.

---

## 4. 이벤트 표본 매트릭스

Phase 3에서는 `signal_grove_pack`에 10개 이벤트 후보를 표본으로 뽑는다. 후보는 `10_Content_Sampling_Guide`의 event archetype이 골고루 드러나도록 분산한다.

| 후보 ID | 원형 | 핵심 압력 | 태그 | 필수 선택 조합 | 목적 |
|---|---|---|---|---|---|
| `split_bell_threshold` | threshold | 건널지, 기다릴지, 고정할지 | exploration, magic | investigate, gamble, item_use | 타이밍과 경로 선택에 curious 단서 압력을 추가한다. |
| `root_snare_obstacle` | obstacle | trap, hunger | exploration, survival | safe, risky, item_use | food-health tradeoff가 있는 비전투 물리 장애물을 만든다. |
| `river_mirror_discovery` | discovery | reflection clue | magic, exploration | investigate, safe, item_use | 도구 기반 정보로 `curious_leaning`이 반응할 단서 이벤트를 만든다. |
| `hollow_witness_bargain` | bargain | 정보와 비용의 교환 | trade, status-risk | bargain, investigate, exploit | 별도 NPC 시스템 없이 사회적 거래를 추가한다. |
| `ash_wind_ambush` | ambush | bandit, physical | combat, exploration | retreat, combat_response, item_use | combat을 일반 choice로 유지하면서 smoke/visibility 대응을 추가한다. |
| `dry_spring_refuge` | refuge | 휴식, 물, 지연 | rest, survival | rest, risky, item_use | desperate run에서 health/food 회복과 기회비용을 같이 만든다. |
| `black_pollen_contamination` | contamination | 보상을 위한 상태 위험 감수 | curse, magic | cleanse, gamble, item_use | greedy/desperate profile에 명확한 bad tradeoff 유혹을 제공한다. |
| `three_ribbon_fork` | trail fork | future route weighting | exploration, trade | investigate, trade, item_use | future event weight가 보이는 경로 결정을 만든다. |
| `returned_pack_aftermath` | aftermath | 이전 조난 흔적의 후속 | survival, trade | safe, exploit, investigate | reputation과 food 긴장을 만드는 aftermath 구조를 사용한다. |
| `moonless_insect_omen` | omen | darkness, beast warning | magic, survival | observe, retreat, item_use | 정답을 공개하지 않는 foreshadowing을 추가한다. |

분포 목표:

```text
event 수: 10
threshold/obstacle/discovery/omen/bargain/ambush/refuge/contamination/trail_fork/aftermath: 각 1개
clue 또는 foreshadowing 압력이 있는 이벤트: 최소 4개
survival 회복 또는 survival 비용이 있는 이벤트: 최소 3개
high-risk greedy temptation이 있는 이벤트: 최소 3개
item interaction이 있는 이벤트: 5~6개
item interaction이 item을 consume하는 이벤트: 2~3개
item interaction이 item을 consume하지 않는 이벤트: 3개
non-item safe 또는 investigate 대안이 있는 이벤트: 10개
```

---

## 5. 아이템 표본 매트릭스

Phase 3에서는 최대 3개 아이템 후보만 추가한다. 아이템이 여는 choice가 같은 실행 단위에 없으면 해당 아이템은 추가하지 않는다.

| 후보 ID | 역할 | 태그 | 대응 위험 | 의도 |
|---|---|---|---|---|
| `signal_chalk` | [information, future_weight] | [tool, travel] | [lost, trap] | threshold, fork, obstacle route를 표시하되 보편 안전 해답이 되지 않게 한다. |
| `resonance_lens` | [information, risk_reduce] | [tool] | [curse, ancient, darkness] | magic/status-risk 이벤트의 clue 구조를 드러내고 해석 위험을 낮춘다. |
| `waybread_pouch` | [cost_convert, risk_reduce] | [consumable, travel] | [hunger, lost] | survival 압력을 consumable resource choice로 전환한다. |

아이템 제약:

- `signal_chalk`는 2개 choice를 열고 future weight를 조정하되 health나 상태 위험을 직접 줄이지 않는다.
- `resonance_lens`는 2개 choice에서 단서를 드러내거나 명확히 해야 하며, status-risk pressure를 줄이는 choice는 최대 1개로 둔다.
- `waybread_pouch`는 food 손실을 막거나 health risk를 item loss로 전환할 때 소비된다.
- 새 아이템은 Phase 3에서 최소 2개 choice와 연결되지 않으면 추가하지 않는다.
- 이 후보들은 새 item role 또는 item tag를 요구하지 않는다.

---

## 6. Entity와 Relation 표본 기준

Phase 3는 기존 Ontology-lite entity type만 사용한다.

Entity 목표:

| Entity | Phase 3 표본 규칙 |
|---|---|
| `event` | `signal_grove_pack`에 10개 이벤트 후보를 추가한다. |
| `choice` | 30~32개 choice를 추가한다. 이벤트당 평균 3개를 목표로 한다. |
| `result` | 모든 choice는 `result`를 가진다. `result_pool`은 기존 테스트가 필요한 형태를 이미 보장할 때만 사용한다. |
| `item` | 0~3개 아이템을 추가한다. 각 아이템이 최소 2개 choice와 연결될 때만 추가한다. |
| `status` | 새 status를 추가하지 않는다. 기존 5개 status만 사용한다. |
| `tag` | 새 tag를 추가하지 않는다. 기존 region/event/danger/item/weight tag를 사용한다. |
| `region` | 기존 `forest`, `village`, `ruin`만 사용한다. |
| `scenario` | 실행 단계에서는 `content_expansion_test`만 갱신한다. |
| `file` | 기존 content source 구조를 유지한다. |

Relation 목표:

| Relation | 필요한 근거 |
|---|---|
| `event_has_choice` | 모든 새 이벤트가 2~3개 choice를 가진다. |
| `choice_produces_result` | 모든 새 choice가 result message와 기계적 결과를 가진다. |
| `choice_requires_item` | 모든 새 아이템이 최소 2개 choice를 연다. |
| `choice_requires_status` | money/reputation gate에만 쓰며, non-gated 대안이 있을 때만 사용한다. |
| `item_counters_tag` | 모든 새 아이템 counter는 기존 danger tag와 연결된다. |
| `result_modifies_status` | 새 choice의 최소 60%가 status를 바꾼다. |
| `result_changes_event_weight` | 새 choice의 최소 40%가 future weight를 바꾼다. |
| `event_belongs_to_region` | 모든 새 이벤트가 기존 region tag를 사용한다. |
| `event_has_event_tag` | 모든 새 이벤트가 2~3개 event tag를 가진다. |
| `event_has_danger_tag` | 모든 새 이벤트가 1~3개 danger tag를 가진다. |
| `scenario_includes_event` | 새 이벤트 id가 `content_expansion_test`에 포함된다. |
| `scenario_uses_content_source` | 새 content source layout을 만들지 않는다. |

---

## 7. Profile 압력 목표

Phase 3 표본은 profile behavior를 하드코딩하지 않고 관찰 가능한 scoring 차이를 만들어야 한다.

| Profile | 필요한 콘텐츠 압력 | 표본 장치 |
|---|---|---|
| `balanced` | item이 보편 최적해가 되는 상황을 피한다 | 모든 item 이벤트에 신뢰 가능한 non-item choice를 둔다. |
| `safe_leaning` | bad tradeoff를 낮게 유지한다 | safe/retreat/observe choice가 health나 상태 위험을 보존하되 기회비용을 가진다. |
| `greedy_leaning` | 보상 중심성을 유지한다 | 최소 3개 high reward choice가 money, item, reputation을 주고 health, reputation, curse 같은 비용을 요구한다. |
| `curious_leaning` | 단서와 novelty route를 늘린다 | 최소 4개 investigate/reveal choice가 future weight를 바꾸거나 안전한 해석을 드러낸다. |
| `desperate` | 낮은 health/food 회복 선택이 의미 있어야 한다 | 최소 3개 choice가 health 또는 food를 회복하면서 risk, reputation cost, item cost를 추가한다. |

Phase 3 실행 후 기대하는 analyzer 신호:

```text
unavailable_selected = 0
meaningful_choice_count > Phase 2 baseline
item_unlocked_choice_count > 0
choice diversity higher than Phase 2 baseline
repeated choice concentration lower than Phase 2 baseline
bad_tradeoff_count concentrated more in greedy_leaning/desperate than safe_leaning
```

---

## 8. Phase 3 실행 태스크 계획

### 작업 1: Phase 2 기준선 기록

**파일:**
- 읽기: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
- 읽기: `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`
- 읽기: `data/scenarios/content_expansion_test.yaml`
- 수정 없음

- [ ] **단계 1: 현재 validation 기준선 실행**

실행:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

예상:

```text
Validation PASS
```

- [ ] **단계 2: 현재 profile 기준선 실행**

실행:

```bash
rm -rf /tmp/fateweaver_phase3_baseline_logs
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile balanced --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile safe_leaning --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile greedy_leaning --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile curious_leaning --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile desperate --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_phase3_baseline_logs
```

예상:

```text
unavailable_selected: 0
profile metrics printed
choice diversity metrics printed
```

- [ ] **단계 3: 콘텐츠 수정 전 기준선 수치 기록**

실행 노트 또는 최종 PR 요약에 아래 값을 기록한다.

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
unavailable_selected
top repeated choice ids
profile choice diversity
```

이 태스크에서는 source file을 수정하지 않는다.

---

### 작업 2: 이벤트 표본을 두 배치로 추가

**파일:**
- 수정: `data/content/packs/signal_grove_pack/events.yaml`
- 읽기: `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
- 읽기: `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`

- [ ] **단계 1: Batch A 이벤트 skeleton 추가**

`data/content/packs/signal_grove_pack/events.yaml`에 아래 5개 이벤트를 추가한다.

```text
split_bell_threshold
root_snare_obstacle
river_mirror_discovery
hollow_witness_bargain
ash_wind_ambush
```

각 이벤트는 정확히 3개 choice를 가진다.

```text
choice 1: safe 또는 investigate, risk_level low 또는 none
choice 2: risky/gamble/trade, risk_level medium 또는 high
choice 3: item_based 또는 combat_response, risk_level low 또는 medium
```

기존 tag만 사용한다.

```text
region: forest, village, ruin
event: exploration, survival, trade, curse, combat, rest, magic
danger: darkness, beast, bandit, trap, hunger, physical, ancient, curse, lost
weight_target: forest, village, ruin, survival, trade, curse, combat, magic, rest, bandit, beast, ancient, lost
```

- [ ] **단계 2: Batch A YAML 검증**

실행:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

예상:

```text
Validation PASS
```

실패하면 `data/content/packs/signal_grove_pack/events.yaml`의 schema 또는 enum 문제만 수정한다.

- [ ] **단계 3: Batch B 이벤트 skeleton 추가**

`data/content/packs/signal_grove_pack/events.yaml`에 아래 5개 이벤트를 추가한다.

```text
dry_spring_refuge
black_pollen_contamination
three_ribbon_fork
returned_pack_aftermath
moonless_insect_omen
```

각 이벤트는 status를 바꾸는 result를 최소 1개 가진다.

```text
health, food, money, reputation, curse
```

Batch B의 5개 이벤트 중 최소 4개는 future event weight를 바꾼다.

```text
event_weight: {lost: -1}
event_weight: {curse: +1}
event_weight: {survival: +1}
event_weight: {village: +1}
```

- [ ] **단계 4: Batch B YAML 검증**

실행:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

예상:

```text
Validation PASS
```

- [ ] **단계 5: 이벤트 배치 커밋**

실행:

```bash
git add data/content/packs/signal_grove_pack/events.yaml
git commit -m "content: sample phase3 signal grove events"
```

예상:

```text
[branch commit] content: sample phase3 signal grove events
```

---

### 작업 3: 연결된 아이템 표본만 추가

**파일:**
- 수정: `data/content/packs/signal_grove_pack/items.yaml`
- 수정: `data/content/packs/signal_grove_pack/events.yaml`
- 읽기: `data/core/item_roles.yaml`
- 읽기: `data/core/tags.yaml`

- [ ] **단계 1: 아이템 후보 추가**

연결될 event choice가 `events.yaml`에 존재할 때만 아래 아이템을 추가한다.

```yaml
items:
  - id: signal_chalk
    name: 신호 분필
    roles: [information, future_weight]
    tags: [tool, travel]
    counters: [lost, trap]
  - id: resonance_lens
    name: 공명 렌즈
    roles: [information, risk_reduce]
    tags: [tool]
    counters: [curse, ancient, darkness]
  - id: waybread_pouch
    name: 길양식 주머니
    roles: [cost_convert, risk_reduce]
    tags: [consumable, travel]
    counters: [hunger, lost]
```

- [ ] **단계 2: 각 아이템이 최소 2개 choice를 여는지 확인**

`events.yaml`에 아래 `requires_item` 연결을 추가하거나 확인한다.

```text
signal_chalk:
  - split_bell_threshold item choice
  - three_ribbon_fork item choice

resonance_lens:
  - river_mirror_discovery item choice
  - black_pollen_contamination item choice

waybread_pouch:
  - root_snare_obstacle item choice
  - dry_spring_refuge item choice
```

- [ ] **단계 3: consumable item 동작 명시**

`waybread_pouch`가 food 손실을 막거나 health risk를 item loss로 전환하는 result에서는 `consume_item: true`와 `remove_item`을 명시한다.

```yaml
consume_item: true
result:
  remove_item: [waybread_pouch]
  status: {food: +1}
```

실제로 소비되는 choice에만 `consume_item: true`를 사용한다.

- [ ] **단계 4: 아이템 연결 검증**

실행:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

예상:

```text
Validation PASS
```

- [ ] **단계 5: 아이템 배치 커밋**

실행:

```bash
git add data/content/packs/signal_grove_pack/items.yaml data/content/packs/signal_grove_pack/events.yaml
git commit -m "content: add phase3 connected item samples"
```

예상:

```text
[branch commit] content: add phase3 connected item samples
```

---

### 작업 4: Scenario coverage 갱신

**파일:**
- 수정: `data/scenarios/content_expansion_test.yaml`
- 읽기: `data/content/packs/signal_grove_pack/events.yaml`
- 읽기: `data/content/packs/signal_grove_pack/items.yaml`

- [ ] **단계 1: Phase 3 event id를 scenario에 추가**

`include_event_ids`에 아래 id를 추가한다.

```yaml
  - split_bell_threshold
  - root_snare_obstacle
  - river_mirror_discovery
  - hollow_witness_bargain
  - ash_wind_ambush
  - dry_spring_refuge
  - black_pollen_contamination
  - three_ribbon_fork
  - returned_pack_aftermath
  - moonless_insect_omen
```

- [ ] **단계 2: Phase 3 initial item 추가**

아이템이 `items.yaml`에 실제로 존재할 때만 `initial_items`에 아래 id를 추가한다.

```yaml
  - signal_chalk
  - resonance_lens
  - waybread_pouch
```

- [ ] **단계 3: 확장된 pool에 맞춰 validation target 상향**

`validation_targets`를 아래 기준으로 갱신한다.

```yaml
validation_targets:
  min_events: 22
  min_combat_events: 3
  min_curse_events: 6
  min_item_count: 14
```

`min_curse_events`는 메인 QA 시나리오가 아니라 상태/위험 보조 coverage가 확장된 event pool에서도 유지되는지 확인하는 기준이다.

- [ ] **단계 4: Scenario 검증**

실행:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

예상:

```text
Validation PASS
```

- [ ] **단계 5: Scenario coverage 커밋**

실행:

```bash
git add data/scenarios/content_expansion_test.yaml
git commit -m "content: expand phase3 validation scenario"
```

예상:

```text
[branch commit] content: expand phase3 validation scenario
```

---

### 작업 5: Profile playtest와 metric 검토

**파일:**
- 읽기: `tools/console_simulator.py`
- 읽기: `tools/analyze_logs.py`
- 수정: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
- 수정: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`

- [ ] **단계 1: Phase 3 전체 validation 실행**

실행:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

예상:

```text
Validation PASS
```

- [ ] **단계 2: Profile별 로그 생성**

실행:

```bash
rm -rf /tmp/fateweaver_phase3_sampling_logs
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile balanced --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile safe_leaning --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile greedy_leaning --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile curious_leaning --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile desperate --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_phase3_sampling_logs
```

예상:

```text
runs_analyzed: 15
unavailable_selected: 0
profile metrics printed
choice diversity metrics printed
repeated choice metrics printed
```

- [ ] **단계 3: Unit test 실행**

실행:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

예상:

```text
OK
```

- [ ] **단계 4: Readiness checklist 갱신**

`docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`에 Phase 3 Sampling 섹션을 추가하고 아래 필드를 기록한다.

```text
Phase 3 sampled events:
Phase 3 sampled items:
unavailable_selected:
meaningful_choice_count:
item_unlocked_choice_count:
bad_tradeoff_count by profile:
top repeated choice ids:
choice diversity by profile:
Final readiness note:
```

- [ ] **단계 5: Playtest review 갱신**

`docs/07_reviews/11_Playtest_Review_Result_v0.1.md`에 아래 구조로 Phase 3 Sampling Result 섹션을 추가한다.

```text
## Phase 3 Sampling Result

Scenario:
Seed/runs:
Profiles:
Metric change from Phase 2:
Choice diversity result:
Item dominance result:
Bad tradeoff distribution:
Unavailable selected:
Playtest judgment:
Remaining risks:
```

- [ ] **단계 6: 검증 문서 커밋**

실행:

```bash
git add docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md docs/07_reviews/11_Playtest_Review_Result_v0.1.md
git commit -m "docs: record phase3 sampling validation"
```

예상:

```text
[branch commit] docs: record phase3 sampling validation
```

---

## 9. 완료 기준

Phase 3 표본 추출 실행은 아래 기준을 만족해야 한다.

```text
10개 새 이벤트 후보가 최소 8개 archetype에 걸쳐 샘플링된다.
0~3개 아이템 후보가 추가되며, 모든 새 아이템은 최소 2개 choice와 연결된다.
새 status를 추가하지 않는다.
별도 근거 없이 새 core tag를 추가하지 않는다.
모든 새 이벤트는 최소 2개 meaningful choice를 가진다.
모든 item 이벤트는 non-item 대안을 가진다.
최소 4개 이벤트가 clue 또는 foreshadowing 압력을 포함한다.
최소 3개 이벤트가 greedy high-risk reward 압력을 포함한다.
최소 3개 이벤트가 health/food survival 압력을 포함한다.
모든 새 이벤트는 기존 Ontology-lite relation으로 설명된다.
Console validation이 통과한다.
5개 profile 모두 simulator log를 생성한다.
Analyzer가 unavailable_selected = 0을 보고한다.
반복 item-choice 집중도가 Phase 2 기준선보다 낮아진다.
Unit test가 통과한다.
```

---

## 10. 이번 계획서 작성 단계 검증 명령

이번 계획서 작성 단계가 문서만 생성하고 금지된 구현 경로를 건드리지 않았는지 아래 명령으로 확인한다.

```bash
find docs/06_plans -maxdepth 1 -type f | sort
grep -R "Content Expansion Phase 3 표본 추출 계획" docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md
git diff --name-only -- data src tools fate_weaver
```

예상:

```text
docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md가 docs plan 목록에 포함된다.
grep이 계획서 제목을 출력한다.
git diff --name-only -- data src tools fate_weaver 출력이 비어 있다.
```

---

## 11. 자체 검토

요구사항 반영 확인:

- 이 계획서는 `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`를 기준으로 작성됐다.
- 이 계획서는 `docs/07_reviews/12_TRPG_Content_Research_Notes_v0.1.md`를 기준으로 작성됐다.
- 이벤트 표본 기준을 정의한다.
- 아이템 표본 기준을 정의한다.
- entity와 relation 표본 기준을 정의한다.
- 계획서 작성 단계에서는 구현하지 않는다.
- 금지 경로와 금지 시스템을 명시한다.

Placeholder 확인:

- 미해결 placeholder marker가 없다.
- 세부 사항을 뒤로 미루는 개방형 지시가 없다.
- 향후 실행 태스크는 구체적인 후보 id, 파일, 명령, 예상 출력을 포함한다.

Type과 schema 일관성 확인:

- Event field는 문서화된 event schema인 `id`, `name`, `description`, `region_tags`, `event_tags`, `danger_tags`, `base_weight`, `choices`와 맞는다.
- Choice field는 문서화된 choice schema인 `id`, `text`, `type`, `risk_level`, `requires_item`, `requires_status`, `consume_item`, `result`와 맞는다.
- Item field는 현재 pack 형식인 `id`, `name`, `roles`, `tags`, `counters`와 맞는다.
- Status reference는 기존 `health`, `food`, `money`, `reputation`, `curse`만 사용한다.
- Tag는 `data/core/tags.yaml`의 기존 tag를 사용한다.
