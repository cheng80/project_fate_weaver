# Quest / Expedition / Card Schema v0.1

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
  - type: collect_item
    item_id: moonleaf_herb
    count: 3
  - type: return_to_region
    region_id: village

optional_objectives:
  - type: discover_clue
    clue_id: old_hunter_trail
  - type: keep_resource_at_least
    resource: food
    value: 2
  - type: help_npc
    npc_tag: injured_traveler

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
  completed_objectives:
    - collect_item: moonleaf_herb
  failed_objectives:
    - keep_food_at_least
  discovered_clues:
    - old_hunter_trail
  rewards:
    money: 1
    reputation: 1
  unlocked_quests:
    - missing_porter_search
  score: 42
  review_text: 약초는 부족했지만 숲속의 표식을 발견했다.
```
