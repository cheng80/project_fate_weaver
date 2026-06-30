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
    target: help_injured_traveler
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
title: 전령을 돕는다
description: 식량을 나누어 전령을 안정시킨다.
source:
  type: storylet
  id: forest_wounded_messenger

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
