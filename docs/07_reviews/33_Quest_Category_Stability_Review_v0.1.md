# [Review] Quest Category Stability Review v0.1

> 상태: Phase 1 Probe 결과 기반 Category 안정성 판정.

## 1. 판정 기준

| 판정 | 의미 |
|---|---|
| Stable | 기존 Objective/Card/Event/Scenario 구조로 반복 구현 가능 |
| Needs Small Schema Extension | 작은 schema/code 확장이 있어야 자연스럽게 확장 가능 |
| Needs New System | 새 evaluator 또는 별도 시스템 필요 |
| Deferred | 현재 P0 이후가 적합 |

## 2. Category별 판정

| Category | Probe Quest | 판정 | Bulk Fill |
|---|---|---|---|
| Local Problem | `village_well_trouble` | Stable | 허용 |
| Investigation / Mystery | `ruin_mark_investigation_intro` | Stable | 허용 |
| Defense / Threat | `defend_the_village_night` | Stable | 허용 |
| Travel / Delivery / Escort | `ghost_town_medicine_run` | Stable | 허용 |
| Ruin / Dungeon / Ritual | `old_well_awakening` | Stable | 허용 |
| Survival / Exploration | `survive_the_storm_pass` | Stable | 허용 |

## 3. 안정성 근거

모든 Category는 기존 P0 구조로 표현 가능했다.

- `discover_clue`
- `optional_action`
- `return_to_region`
- `keep_resource_at_least`
- `survive_expedition`
- `quest_ids` Card Gate
- `card_candidate_hints`
- `cooldown_tags`
- `repeat_group`

새 evaluator는 추가하지 않았다.

## 4. Category별 Bulk 후보

Bulk Fill은 다음 후보에 한해 다음 Phase에서 진행할 수 있다.

| Category | Bulk 후보 |
|---|---|
| Local Problem | `beginner_village_wrongness`, `tanglewood_faire_games`, `festival_missing_racer` |
| Investigation / Mystery | `vanishing_village`, `abandoned_lighthouse_signal`, `painted_portal_canvas`, `mansion_returned_explorer`, `dreamless_king` |
| Defense / Threat | `beast_of_zarechka`, `awaken_the_beast`, `cattle_mutilation_stone_circle` |
| Travel / Delivery / Escort | `winter_wagon_delivery`, `deliver_the_sealed_parcel`, `stowaway_without_memory`, `old_east_trail_rescue` |
| Ruin / Dungeon / Ritual | `crypt_of_elven_king`, `activate_the_old_gate`, `awaken_the_monolith`, `sealed_ruin_entry`, `ruined_island_puzzle_box` |
| Survival / Exploration | `frozen_treasure_cave`, `hidden_grove_discovery`, `lost_city_rising_sands` |

## 5. Bulk Fill 전 조건

다음 Phase에서 Bulk Fill을 시작하기 전에 지켜야 할 조건이다.

1. 각 Bulk Quest는 success scenario 1개 이상을 가진다.
2. Category당 대표 partial/failure는 Probe 결과를 재사용한다.
3. 새 Card Rule은 `quest_ids`로 격리한다.
4. 기존 Done Quest 회귀를 계속 통과한다.
5. Storylet Pool 전체 시스템과 장기 cooldown 저장은 추가하지 않는다.

## 6. 결론

6개 Probe Category는 모두 Stable로 판정한다.

다음 작업은 Stable Category의 Bulk Fill이다. 단, Bulk Fill은 별도 ULW evidence와 회귀 검증을 가진 독립 단계로 진행한다.
