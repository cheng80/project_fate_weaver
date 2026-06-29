# Content Expansion Phase 3 Sampling Plan Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Define the Phase 3 sampling plan for FateWeaver events, items, and Ontology-lite entities before adding any new YAML content.

**Architecture:** Phase 3 should expand the existing `signal_grove_pack` content pool instead of changing scoring weights or introducing new runtime systems. Sampling is driven by `docs/02_schema/10_Content_Sampling_Guide_v0.1.md` and `docs/07_reviews/12_TRPG_Content_Research_Notes_v0.1.md`: each sample must map to event/choice/result/item/status/tag relations and must create real choice pressure in Console Simulator logs. The plan keeps combat as ordinary events, keeps ontology as YAML-lite, and treats status changes as choice pressure rather than decorative values.

**Tech Stack:** YAML content contracts, Python 3.12 Console Validation CLI, `PyYAML`, `unittest`, Ontology-lite via `data/core/ontology.yaml`, Markdown planning documents.

---

## 1. Scope

This document is a sampling plan, not an implementation patch.

Current work creates only this file:

- Create: `docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md`

Phase 3 execution may later touch these files:

- Modify: `data/content/packs/signal_grove_pack/events.yaml`
  - Add sampled events that expand choice diversity and reduce repeated item-choice dominance.
- Modify: `data/content/packs/signal_grove_pack/items.yaml`
  - Add only items that unlock, reveal, mitigate, convert cost, amplify reward, or adjust future weight.
- Modify: `data/scenarios/content_expansion_test.yaml`
  - Add new Phase 3 event ids and item ids to the validation slice.
- Modify: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
  - Record Phase 3 sampling and validation evidence after execution.
- Modify: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
  - Append a Phase 3 playtest note after execution if metrics materially change.

Phase 3 execution should not touch these files unless a separate approved plan changes the scope:

- `data/core/*.yaml`
- `src/fateweaver/*.py`
- `tools/*.py`
- `tests/*.py`
- `fate_weaver/`

Do not introduce:

- Flutter project files
- GraphDB, RDF, OWL, ontology engine
- PRD
- World Bible
- Event-specific Python branches
- Combat subsystem

---

## 2. Phase 3 Sampling Objectives

Phase 3 sampling addresses the limits identified by the playtest review and scoring observability work.

Primary objectives:

1. Increase event pool size so profile differences are produced by content variety, not aggressive weight tuning.
2. Reduce repeated dominance of a single item-based choice by providing non-item alternatives and varied item functions.
3. Give `curious_leaning` more investigation, clue, and foreshadowing choices without forcing profile-specific outcomes.
4. Preserve `safe_leaning` low bad-tradeoff behavior through credible safe options.
5. Preserve `greedy_leaning` reward temptation through money/item/reputation gains tied to curse, health, or reputation costs.
6. Give `desperate` more meaningful health/food recovery tradeoffs.
7. Keep `unavailable_selected = 0` by using `requires_item` and `requires_status` only as availability gates.
8. Keep all new content explainable through existing Ontology-lite relations.

Non-objectives:

- Do not tune profile weights as part of Phase 3 sampling.
- Do not add a new status unless existing `health`, `food`, `money`, `reputation`, and `curse` cannot express the pressure.
- Do not add new core tags unless every sampled event fails to fit existing tags.
- Do not convert combat events into a separate combat model.

---

## 3. Sampling Criteria

Each sampled event must satisfy this minimum shape:

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

Required event checks:

- At least 2 choices, recommended 3 choices.
- At least 1 non-item choice remains meaningful when item choices are available.
- At least 1 choice changes `health`, `food`, `money`, `reputation`, `curse`, item availability, or future event weight.
- At least 1 choice is useful to scoring review as safe, greedy, curious, or desperate pressure.
- No event should require a newly invented schema field.
- No event should rely on original TRPG setting names, proper nouns, or copied text.

---

## 4. Event Sampling Matrix

Phase 3 should sample 10 new event candidates for `signal_grove_pack`. These candidates are intentionally distributed across the archetypes from `10_Content_Sampling_Guide`.

| Candidate ID | Archetype | Primary Pressure | Tags | Required Choice Mix | Purpose |
|---|---|---|---|---|---|
| `split_bell_threshold` | threshold | cross / wait / anchor | exploration, magic | investigate, gamble, item_use | Adds curious clue pressure around timing and route choice. |
| `root_snare_obstacle` | obstacle | trap / hunger | exploration, survival | safe, risky, item_use | Creates non-combat physical obstacle with food-health tradeoff. |
| `river_mirror_discovery` | discovery | reflection clue | magic, exploration | investigate, safe, item_use | Gives `curious_leaning` a clue-forward event using tool-based information. |
| `hollow_witness_bargain` | bargain | information for cost | trade, curse | bargain, investigate, exploit | Adds social exchange without requiring a full NPC system. |
| `ash_wind_ambush` | ambush | bandit / physical | combat, exploration | retreat, combat_response, item_use | Keeps combat as event choices and adds smoke/visibility response. |
| `dry_spring_refuge` | refuge | rest / water / delay | rest, survival | rest, risky, item_use | Gives desperate runs health/food recovery with opportunity cost. |
| `black_pollen_contamination` | contamination | curse for reward | curse, magic | cleanse, gamble, item_use | Adds a clear bad tradeoff for greedy/desperate profiles. |
| `three_ribbon_fork` | trail fork | future route weighting | exploration, trade | investigate, trade, item_use | Makes future event weight a visible route decision. |
| `returned_pack_aftermath` | aftermath | previous survivor trace | survival, trade | safe, exploit, investigate | Uses aftermath to create reputation and food tension. |
| `moonless_insect_omen` | omen | darkness / beast warning | magic, survival | observe, retreat, item_use | Adds foreshadowing without revealing a single correct answer. |

Distribution target:

```text
event count: 10
threshold/obstacle/discovery/omen/bargain/ambush/refuge/contamination/trail_fork/aftermath: 1 each
events with clue or foreshadowing pressure: at least 4
events with survival recovery or survival cost: at least 3
events with high-risk greedy temptation: at least 3
events with item interaction: 5 to 6
events where item interaction consumes item: 2 to 3
events where item interaction does not consume item: 3
events with non-item safe or investigate alternative: 10
```

---

## 5. Item Sampling Matrix

Phase 3 should add at most 3 item candidates. Do not add items unless their choices are also added in the same execution.

| Candidate ID | Roles | Tags | Counters | Intended Use |
|---|---|---|---|---|
| `signal_chalk` | [information, future_weight] | [tool, travel] | [lost, trap] | Marks thresholds, forks, and obstacle routes without becoming universal safety. |
| `resonance_lens` | [information, risk_reduce] | [tool] | [curse, ancient, darkness] | Reveals clue structure in magic/curse events and reduces interpretation risk. |
| `waybread_pouch` | [cost_convert, risk_reduce] | [consumable, travel] | [hunger, lost] | Converts survival pressure into a consumable resource choice for desperate runs. |

Item constraints:

- `signal_chalk` should unlock 2 choices and adjust future weight, but should not reduce health or curse directly.
- `resonance_lens` should reveal or clarify a clue in 2 choices, and at most 1 choice should reduce curse pressure.
- `waybread_pouch` should be consumed when it prevents food loss or converts health risk into item loss.
- Each new item must connect to at least 2 choices in Phase 3, or it should not be added.
- No new item role or item tag is required for these candidates.

---

## 6. Entity and Relation Sampling

Phase 3 should use existing Ontology-lite entity types only.

Entity targets:

| Entity | Phase 3 Sampling Rule |
|---|---|
| `event` | Add 10 event candidates in `signal_grove_pack`. |
| `choice` | Add 30 to 32 choices, averaging 3 per event. |
| `result` | Every choice has `result`; use `result_pool` only if an existing test already covers the needed shape. |
| `item` | Add 0 to 3 items; add only if each item has at least 2 linked choices. |
| `status` | Add no new status; use existing five statuses. |
| `tag` | Add no new tag; use existing region/event/danger/item/weight tags. |
| `region` | Use existing `forest`, `village`, `ruin`. |
| `scenario` | Update only `content_expansion_test` during execution. |
| `file` | Use existing content source structure. |

Relation targets:

| Relation | Required Evidence |
|---|---|
| `event_has_choice` | Every new event has 2 or 3 choices. |
| `choice_produces_result` | Every new choice has a result message and a mechanical result. |
| `choice_requires_item` | Every new item unlocks at least 2 choices. |
| `choice_requires_status` | Use for money/reputation gates only when a non-gated alternative exists. |
| `item_counters_tag` | Every new item counter maps to an existing danger tag. |
| `result_modifies_status` | At least 60 percent of new choices modify status. |
| `result_changes_event_weight` | At least 40 percent of new choices modify future weight. |
| `event_belongs_to_region` | Every new event uses existing region tags. |
| `event_has_event_tag` | Every new event has 2 to 3 event tags. |
| `event_has_danger_tag` | Every new event has 1 to 3 danger tags. |
| `scenario_includes_event` | New event ids are included in `content_expansion_test`. |
| `scenario_uses_content_source` | No new content source layout is introduced. |

---

## 7. Profile Pressure Targets

Phase 3 sampling should create observable scoring differences without hardcoding profile behavior.

| Profile | Content Pressure Needed | Sampling Mechanism |
|---|---|---|
| `balanced` | Avoid universal item optimum | Every item event has a credible non-item choice. |
| `safe_leaning` | Keep bad tradeoff low | Safe/retreat/observe choices preserve health or curse with visible opportunity cost. |
| `greedy_leaning` | Preserve reward center | At least 3 high reward choices give money, item, or reputation while costing curse, health, or reputation. |
| `curious_leaning` | Increase clue and novelty routes | At least 4 investigate/reveal choices adjust future weight or expose safer interpretation. |
| `desperate` | Make low health/food recovery meaningful | At least 3 choices recover health or food while adding risk, reputation cost, or item cost. |

Expected analyzer signals after Phase 3 execution:

```text
unavailable_selected = 0
meaningful_choice_count > Phase 2 baseline
item_unlocked_choice_count > 0
choice diversity higher than Phase 2 baseline
repeated choice concentration lower than Phase 2 baseline
bad_tradeoff_count concentrated more in greedy_leaning/desperate than safe_leaning
```

---

## 8. Task Plan for Phase 3 Execution

### Task 1: Capture Phase 2 Baseline

**Files:**
- Read: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
- Read: `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`
- Read: `data/scenarios/content_expansion_test.yaml`
- No file modifications

- [ ] **Step 1: Run current validation baseline**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
Validation PASS
```

- [ ] **Step 2: Run current profile baseline**

Run:

```bash
rm -rf /tmp/fateweaver_phase3_baseline_logs
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile balanced --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile safe_leaning --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile greedy_leaning --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile curious_leaning --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile desperate --logs /tmp/fateweaver_phase3_baseline_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_phase3_baseline_logs
```

Expected:

```text
unavailable_selected: 0
profile metrics printed
choice diversity metrics printed
```

- [ ] **Step 3: Record baseline notes before editing content**

Append the observed baseline numbers to the execution work notes or final PR summary. Required numbers:

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
unavailable_selected
top repeated choice ids
profile choice diversity
```

Do not modify source files in this task.

---

### Task 2: Add Event Samples in Two Small Batches

**Files:**
- Modify: `data/content/packs/signal_grove_pack/events.yaml`
- Read: `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
- Read: `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`

- [ ] **Step 1: Add Batch A event skeletons**

Add these 5 events to `data/content/packs/signal_grove_pack/events.yaml`:

```text
split_bell_threshold
root_snare_obstacle
river_mirror_discovery
hollow_witness_bargain
ash_wind_ambush
```

Each event must have exactly 3 choices:

```text
choice 1: safe or investigate, risk_level low or none
choice 2: risky/gamble/trade, risk_level medium or high
choice 3: item_based or combat_response, risk_level low or medium
```

Use existing tags only:

```text
region: forest, village, ruin
event: exploration, survival, trade, curse, combat, rest, magic
danger: darkness, beast, bandit, trap, hunger, physical, ancient, curse, lost
weight_target: forest, village, ruin, survival, trade, curse, combat, magic, rest, bandit, beast, ancient, lost
```

- [ ] **Step 2: Validate Batch A YAML**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
Validation PASS
```

If validation fails, fix only schema or enum issues in `data/content/packs/signal_grove_pack/events.yaml`.

- [ ] **Step 3: Add Batch B event skeletons**

Add these 5 events to `data/content/packs/signal_grove_pack/events.yaml`:

```text
dry_spring_refuge
black_pollen_contamination
three_ribbon_fork
returned_pack_aftermath
moonless_insect_omen
```

Each event must have at least one result that modifies status:

```text
health, food, money, reputation, or curse
```

At least 4 of the 5 Batch B events must modify future event weight:

```text
event_weight: {lost: -1}
event_weight: {curse: +1}
event_weight: {survival: +1}
event_weight: {village: +1}
```

- [ ] **Step 4: Validate Batch B YAML**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
Validation PASS
```

- [ ] **Step 5: Commit event batch**

Run:

```bash
git add data/content/packs/signal_grove_pack/events.yaml
git commit -m "content: sample phase3 signal grove events"
```

Expected:

```text
[branch commit] content: sample phase3 signal grove events
```

---

### Task 3: Add Only Connected Item Samples

**Files:**
- Modify: `data/content/packs/signal_grove_pack/items.yaml`
- Modify: `data/content/packs/signal_grove_pack/events.yaml`
- Read: `data/core/item_roles.yaml`
- Read: `data/core/tags.yaml`

- [ ] **Step 1: Add item candidates**

Add these items only if their linked event choices exist in `events.yaml`:

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

- [ ] **Step 2: Ensure each item unlocks at least two choices**

Add or verify these `requires_item` links in `events.yaml`:

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

- [ ] **Step 3: Make consumable item behavior explicit**

For `waybread_pouch`, set `consume_item: true` and remove the item in the result where it prevents food loss or converts health risk:

```yaml
consume_item: true
result:
  remove_item: [waybread_pouch]
  status: {food: +1}
```

Use `consume_item: true` only where the item is actually spent.

- [ ] **Step 4: Validate item links**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
Validation PASS
```

- [ ] **Step 5: Commit item batch**

Run:

```bash
git add data/content/packs/signal_grove_pack/items.yaml data/content/packs/signal_grove_pack/events.yaml
git commit -m "content: add phase3 connected item samples"
```

Expected:

```text
[branch commit] content: add phase3 connected item samples
```

---

### Task 4: Update Scenario Coverage

**Files:**
- Modify: `data/scenarios/content_expansion_test.yaml`
- Read: `data/content/packs/signal_grove_pack/events.yaml`
- Read: `data/content/packs/signal_grove_pack/items.yaml`

- [ ] **Step 1: Add Phase 3 event ids to scenario**

Add these event ids to `include_event_ids`:

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

- [ ] **Step 2: Add Phase 3 initial items**

Add these item ids to `initial_items` only after they exist in `items.yaml`:

```yaml
  - signal_chalk
  - resonance_lens
  - waybread_pouch
```

- [ ] **Step 3: Raise validation targets to match expanded pool**

Update `validation_targets` to reflect the larger sample:

```yaml
validation_targets:
  min_events: 22
  min_combat_events: 3
  min_curse_events: 6
  min_item_count: 14
```

- [ ] **Step 4: Validate scenario**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
Validation PASS
```

- [ ] **Step 5: Commit scenario coverage**

Run:

```bash
git add data/scenarios/content_expansion_test.yaml
git commit -m "content: expand phase3 validation scenario"
```

Expected:

```text
[branch commit] content: expand phase3 validation scenario
```

---

### Task 5: Run Profile Playtest and Review Metrics

**Files:**
- Read: `tools/console_simulator.py`
- Read: `tools/analyze_logs.py`
- Modify: `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
- Modify: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`

- [ ] **Step 1: Run full Phase 3 validation**

Run:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
```

Expected:

```text
Validation PASS
```

- [ ] **Step 2: Run profile logs**

Run:

```bash
rm -rf /tmp/fateweaver_phase3_sampling_logs
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile balanced --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile safe_leaning --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile greedy_leaning --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile curious_leaning --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile desperate --logs /tmp/fateweaver_phase3_sampling_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_phase3_sampling_logs
```

Expected:

```text
runs_analyzed: 15
unavailable_selected: 0
profile metrics printed
choice diversity metrics printed
repeated choice metrics printed
```

- [ ] **Step 3: Run unit tests**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

Expected:

```text
OK
```

- [ ] **Step 4: Update readiness checklist**

In `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`, add a Phase 3 Sampling section with these exact fields:

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

- [ ] **Step 5: Update playtest review**

In `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`, append a Phase 3 Sampling Result section with this exact structure:

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

- [ ] **Step 6: Commit validation documents**

Run:

```bash
git add docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md docs/07_reviews/11_Playtest_Review_Result_v0.1.md
git commit -m "docs: record phase3 sampling validation"
```

Expected:

```text
[branch commit] docs: record phase3 sampling validation
```

---

## 9. Acceptance Criteria

Phase 3 sampling is ready to proceed when this plan exists and the future execution work can satisfy these criteria:

```text
10 new event candidates are sampled across at least 8 archetypes.
0 to 3 item candidates are added, and every new item has at least 2 linked choices.
No new status is introduced.
No new core tag is introduced unless separately justified.
Every new event has at least 2 meaningful choices.
Every item event has a non-item alternative.
At least 4 events include clue or foreshadowing pressure.
At least 3 events include greedy high-risk reward pressure.
At least 3 events include health/food survival pressure.
Every new event maps to existing Ontology-lite relations.
Console validation passes.
Profile simulation generates logs for all five profiles.
Analyzer reports unavailable_selected = 0.
Repeated item-choice concentration is lower than the Phase 2 baseline.
Unit tests pass.
```

---

## 10. Verification Commands for This Planning Step

Use these commands to verify that this planning step only created the plan document and did not modify forbidden implementation paths:

```bash
find docs/06_plans -maxdepth 1 -type f | sort
grep -R "Content Expansion Phase 3 Sampling Plan" docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md
git diff --name-only -- data src tools fate_weaver
```

Expected:

```text
docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md appears in the docs plan list.
grep prints the plan title.
git diff --name-only -- data src tools fate_weaver prints nothing for this planning step.
```

---

## 11. Self-Review

Spec coverage:

- The plan is based on `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`.
- The plan is based on `docs/07_reviews/12_TRPG_Content_Research_Notes_v0.1.md`.
- The plan defines event sampling criteria.
- The plan defines item sampling criteria.
- The plan defines entity and relation sampling criteria.
- The plan avoids implementation during the planning step.
- The plan lists forbidden paths and systems.

Placeholder scan:

- No unresolved placeholder markers.
- No open-ended deferred-detail instructions.
- Future execution tasks list concrete candidate ids, files, commands, and expected outputs.

Type and schema consistency:

- Event fields match the documented event schema: `id`, `name`, `description`, `region_tags`, `event_tags`, `danger_tags`, `base_weight`, `choices`.
- Choice fields match the documented choice schema: `id`, `text`, `type`, `risk_level`, `requires_item`, `requires_status`, `consume_item`, `result`.
- Item fields match existing pack format: `id`, `name`, `roles`, `tags`, `counters`.
- Status references use existing statuses only: `health`, `food`, `money`, `reputation`, `curse`.
- Tags use existing tags from `data/core/tags.yaml`.
