# Quest / Expedition / Card Schema v0.1

> 상태: [Current] 현재 Gameplay Replan 작업의 기준 문서.

## 1. 문서 목적

이 문서는 FateWeaver의 실게임형 텍스트 모험 구조를 데이터로 표현하기 위한 스키마 초안을 정의한다.

대상 범위:

- Quest
- Expedition Clock
- Storylet
- Card Candidate
- Multi-Select Rule
- Result
- Economy
- Score
- Quest Report

---

## 2. Quest Schema

```yaml
id: herb_gathering_tutorial
title: 약초 채집 의뢰
rank: novice
quest_type: gathering
start_region: village
target_regions:
  - forest

recommended_days: 3
max_days: 5

primary_objectives:
  - id: collect_herbs
    type: collect_item
    target: herbs_collected
    required: true
    count: 3
    failure_reason: primary_objective_failed
    partial_reason: primary_partial
    score_key: objective_collect
    reward_weight: 3
  - id: report_to_apothecary
    type: return_to_region
    target: village
    progress_key: reported_to_apothecary
    required: true
    value: 1
    failure_reason: return_failed
    partial_reason: report_failed
    score_key: objective_return
    reward_weight: 2
  - id: survive_expedition
    type: survive_expedition
    target: health
    required: true
    value: 1
    failure_reason: health_zero
    partial_reason: health_zero
    score_key: objective_survival
    reward_weight: 3

optional_objectives:
  - id: discover_old_hunter_trail
    type: discover_clue
    target: old_hunter_trail
    required: false
    value: 1
    failure_reason: optional_failed
    partial_reason: optional_failed
    score_key: objective_discovery
    reward_weight: 1
  - id: preserve_food
    type: keep_resource_at_least
    target: food
    required: false
    value: 2
    failure_reason: optional_failed
    partial_reason: optional_failed
    score_key: objective_resource
    reward_weight: 1
  - id: help_injured_traveler
    type: optional_action
    target: helped_injured_traveler
    progress_key: helped_injured_traveler
    required: false
    value: 1
    failure_reason: optional_failed
    partial_reason: optional_failed
    score_key: objective_aid
    reward_weight: 1

failure_conditions:
  - type: resource_lte
    resource: health
    value: 0
  - type: day_gt
    value: 5

rewards:
  money: 3
  reputation: 1
  score: 50
  unlock_quests:
    - missing_porter_search

event_bias:
  tags:
    herb: 20
    forest: 10
    tutorial: 10
```

현재 P0 Objective 필드는 실제 구현 기준으로 다음을 사용한다.

- `id`: Quest Report와 로그에 남는 objective 식별자.
- `type`: `collect_item`, `return_to_region`, `survive_expedition`, `keep_resource_at_least`, `discover_clue`, `optional_action`.
- `target`: 진행도, 지역, 상태, 단서, optional action을 가리키는 기준 값.
- `required`: 성공 판정에 필요한 주 목표 여부.
- `count`: `collect_item` 목표 수량.
- `value`: `return_to_region`, `survive_expedition`, `keep_resource_at_least`, `discover_clue`, `optional_action`의 목표 값.
- `progress_key`: `return_to_region`처럼 별도 진행도 키를 확인할 때 사용한다.
- `failure_reason`: objective 실패 시 Quest Report reason 후보.
- `partial_reason`: objective partial 또는 partial_success reason 후보.
- `score_key`: score breakdown에서 objective 의미를 추적하기 위한 키.
- `reward_weight`: objective 완료, partial, 실패 점수 계산 가중치.

`optional_action`은 `progress_key`가 있으면 해당 quest progress 값을 우선 보고 completed / partial / failed를 평가한다.
예를 들어 `help_injured_traveler` objective는 `helped_injured_traveler` 진행도가 카드 결과로 1 이상이 되면 completed가 된다.

---

## 3. Expedition Clock Schema

```yaml
run_clock:
  day: 1
  turn: 1
  turns_today: 0
  time_of_day: morning
  act: 1
  max_days: 7
  max_turns: 35
  turns_per_day: 5
```

---

## 4. Storylet Schema

```yaml
id: forest_wounded_messenger
title: 다친 전령
region: forest

act_range: [1, 3]
day_range: [1, 4]
time_of_day:
  - morning
  - afternoon

tags:
  - npc
  - clue
  - reputation
  - quest_related

requires:
  active_quest_tags:
    - gathering
    - scouting
  min_reputation: -1

blocks:
  seen_storylets:
    - messenger_dead

base_cards:
  - investigate_messenger
  - help_messenger
  - ignore_messenger

next_event_tags:
  - messenger_followup
  - hidden_path
```

---

## 5. Card Candidate Schema

```yaml
id: help_messenger
card_type: aid
slot_role: risk_discovery
base_weight: 50
tier_hint: strong
title: 전령을 돕는다
description: 식량을 나누어 전령을 안정시킨다.
tags:
  - aid
  - npc
  - optional_objective
  - reputation
source:
  type: storylet
  id: forest_wounded_messenger
applies_to_storylet_tags:
  - wounded_messenger
  - aid_opportunity
applies_to_quest_objectives:
  - help_messenger
progress_key: helped_messenger
weight_modifiers:
  quest_objective_match: 30
  storylet_tag_match: 20
  region_match: 10
  already_completed: -999
  unavailable: -999
  recent_repeat_penalty: -25

requires:
  min_food: 1

effects:
  resource_changes:
    food: -1
    reputation: 1
  gain_clues:
    - blood_marked_trail
  next_event_tags:
    - messenger_followup

risk_hint: 식량을 소모하지만 평판과 단서를 얻을 수 있다.
```

현재 P0 구현의 `data/core/card_rules.yaml`은 위 스키마의 최소 실행형 subset을 사용한다.

- `tags`: 카드의 온톨로지식 의미 태그다. 예: `aid`, `npc`, `optional_objective`, `reputation`, `forest`, `quest_related`.
- `applies_to_storylet_tags`: 현재 Storylet/Event 또는 P0 situation context tag와 하나 이상 겹치면 후보로 올라올 수 있다.
- `applies_to_quest_objectives`: active quest의 optional objective id와 연결한다.
- `progress_key`: 카드 선택 후 갱신되는 quest progress key다. 이미 1 이상이면 같은 optional action 카드는 다시 후보 우선권을 갖지 않는다.
- `base_weight`: 후보 pool에서 기본 점수로 쓰는 값이다.
- `tier_hint`: 데이터 작성자가 의도한 대략적 tier다. 실제 tier는 runtime score로 다시 계산한다.
- `weight_modifiers`: quest objective, storylet tag, region, 반복, 완료, unavailable 상태가 점수에 주는 보정값이다.

예를 들어 `help_injured_traveler` 카드는 `injured_traveler` 또는 `aid_opportunity` context tag가 있고, active quest에 `help_injured_traveler` optional objective가 있으며, `helped_injured_traveler` 진행도가 아직 0일 때 3-Card 후보에 포함된다.

P0 JSON Log의 각 turn은 `card_candidate_pool`을 남긴다.

```yaml
card_candidate_pool:
  - card_id: help_injured_traveler
    slot_role: resource_alternative
    score: 70
    tier: strong
    matched_tags:
      - injured_traveler
      - aid_opportunity
    matched_objectives:
      - help_injured_traveler
    blocked_reason: ""
    selection_seed_key: "tutorial_herb_quest:42:run1:day1:turn3:resource_alternative:forest:herb_gathering_tutorial"
    variety_window: true
    selected_by: seeded_tier_pick
    repeat_penalty: 0
```

Tier 기준:

- `critical`: 90 이상
- `strong`: 70 이상 90 미만
- `normal`: 40 이상 70 미만
- `flavor`: 0 이상 40 미만
- `blocked`: 0 미만 또는 unavailable/completed objective

Seeded Tier Variety(시드 기반 등급 내 다양성) 기준:

- 같은 `scenario_id`, `seed`, `turn`, `day`, `slot_role`, `current_region`, `active_quest_id`에서는 같은 3-Card 구성이 재현된다.
- slot별 후보는 `tier`와 `score`로 정렬한 뒤, 같은 Tier(등급) 안에서 상위 `variety_window_size: 3` 또는 `score_tolerance: 10` 안의 후보를 Variety Window(다양성 창)로 묶는다.
- Variety Window(다양성 창) 안에서는 `selection_seed_key` 기반 Weighted Pick(가중 선택)을 수행한다.
- `critical` 후보는 우선권을 유지하며, 여러 critical 후보가 있을 때만 seed 기반 선택이 개입한다.
- `blocked` 후보는 Variety Window(다양성 창)에 들어가지 않으며 3-Card에 선택되지 않는다.
- 직전 또는 최근 선택 이력에 있는 카드는 `recent_repeat_penalty`가 `repeat_penalty` evidence로 남는다.

---

## 6. Modifier Card Schema

```yaml
id: use_torch_to_scare_beast
card_type: use_item
slot_role: resource_modifier
title: 횃불을 켠다
description: 주변의 그림자를 밀어내고 짐승의 접근을 막는다.

source:
  type: item
  id: torch

applies_to_tags:
  - beast_risk
  - forest
  - darkness

effects:
  risk_delta: -2
  item_durability:
    torch: -1

combo_with:
  - gather_herbs
  - enter_ruin

conflicts_with:
  - avoid_area
  - return_to_village

multi_select_cost:
  fatigue: 1
```

---

## 7. Multi-Select Rule Schema

```yaml
multi_select_rules:
  max_selected_cards: 2
  allow_three_cards_when_tags:
    - prepared
    - safe_camp
  default_extra_cost:
    fatigue: 1

conflict_rules:
  - id: avoid_vs_force
    cannot_combine:
      - avoid
      - force

combo_rules:
  - id: torch_plus_gather
    cards:
      - use_torch_to_scare_beast
      - gather_herbs
    effects:
      risk_delta: -1
      bonus_item_gain:
        moonleaf_herb: 1
```

---

## 8. Result Schema

```yaml
result:
  resource_changes:
    health: -1
    food: -1
    money: 1
    reputation: 1

  status_changes:
    fatigue: 1
    injury: 0
    curse: 0

  gain_items:
    - moonleaf_herb

  lose_items:
    - torch

  gain_clues:
    - old_hunter_trail

  gain_omens:
    - silent_birds

  next_event_tags:
    - hidden_path
    - return_to_village

  score_changes:
    quest_progress: 10
    exploration: 5
    reputation: 3
```

---

## 9. Score Schema

```yaml
score_rules:
  survival_bonus: 30
  quest_success: 50
  partial_success: 20
  discovered_clue: 5
  solved_storylet: 3
  preserved_food: 2
  reputation_point: 4
  objective_scoring:
    completed_required: 10
    completed_optional: 10
    partial_required: 5
    partial_optional: 5
    failed_required: -10
    failed_optional: 0
    survival_failed: -30
    return_failed: -20
  ending_bonus:
    success: 30
    discovery: 20
    retreat: 5
    death: -30
  penalties:
    injury: -5
    fatigue: -2
    curse: -3
    reckless_choice: -4
```

---

## 10. Quest Report Schema

```yaml
quest_report:
  quest_id: herb_gathering_tutorial
  result_type: partial_success
  result_reason: primary_partial
  objective_results:
    - objective_id: collect_herbs
      objective_type: collect_item
      status: partial
      reason: primary_partial
      progress_value: 2
      target_value: 3
      required: true
      score_key: objective_collect
      score_delta: 15
    - objective_id: help_injured_traveler
      objective_type: optional_action
      status: failed
      reason: optional_failed
      progress_value: 0
      target_value: 1
      required: false
      score_key: objective_aid
      score_delta: 0
  completed_objectives:
    - collect_herbs
  failed_objectives:
    - report_to_apothecary
  partial_reasons:
    - primary_partial
    - optional_failed
    - return_late
    - reduced_reward
  failure_reasons: []
  discovered_clues:
    - old_hunter_trail
  rewards: {}
  unlocked_quests:
    - retry_herb_gathering
  score: 42
  score_breakdown:
    quest_progress: 10
    objective_completion: 35
    outcome_adjustment: 20
  reward_status: reduced_reward
  review_text: 약초는 부족했지만 숲속의 표식을 발견했다.
```

`objective_results`는 JSON Log와 Text MUD Play Log 양쪽에서 objective 평가를 사람이 추적할 수 있게 하는 최소 출력 계약이다.

`score_delta`는 `data/core/score_rules.yaml`의 `objective_scoring` 값을 기준으로 계산한다.
`reward_weight`는 objective별 중요도 가중치로 사용한다.

현재 P0 result reason은 Quest별 하드코딩이 아니라 objective evaluation과 clock constraint에서 유도한다.

- `primary_partial`: required `collect_item`이 partial인 경우.
- `report_failed`: partial_success에서 `return_to_region`이 failed인 경우.
- `optional_failed`: optional objective가 failed인 경우.
- `health_zero`: `survive_expedition`이 failed인 경우.
- `return_failed`: failure에서 `return_to_region`이 failed인 경우.
- `primary_objective_failed`: required objective가 failed인 경우.
- `max_turn_exceeded`: turn 제한을 초과한 경우.
- `max_day_exceeded`: day 제한을 초과한 경우.
- `reduced_reward`: partial_success에서 보상이 축소되는 경우.
