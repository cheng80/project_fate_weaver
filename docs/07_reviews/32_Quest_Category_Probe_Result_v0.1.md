# [Review] Quest Category Probe Result v0.1

> 상태: Phase 1 Category Probe 구현 결과. Bulk Fill 전 대표 Quest 검증 기록.

## 1. 요약

Quest Type Catalog 기반으로 6개 Category의 대표 Probe Quest를 구현했다.

| 순서 | Category | Probe Quest | 결과 |
|---:|---|---|---|
| 1 | Local Problem | `village_well_trouble` | PASS |
| 2 | Investigation / Mystery | `ruin_mark_investigation_intro` | PASS |
| 3 | Defense / Threat | `defend_the_village_night` | PASS |
| 4 | Travel / Delivery / Escort | `ghost_town_medicine_run` | PASS |
| 5 | Ruin / Dungeon / Ritual | `old_well_awakening` | PASS |
| 6 | Survival / Exploration | `survive_the_storm_pass` | PASS |

각 Probe는 success / partial_success / failure fixture를 가진다.

## 2. 구현 범위

추가된 범위는 다음에 한정한다.

- Quest data
- Card Rule
- Storylet/Event Hint
- Scenario fixture
- Category Probe test
- Review 문서

다음은 구현하지 않았다.

- Storylet Pool 전체 시스템
- Repeat Cooldown 장기 저장
- Flutter/Flame UI
- Stability Review 전 Bulk Fill

## 3. Probe별 검증 포인트

| Probe Quest | Success | Partial | Failure | JSON/Text MUD | Storylet Hint / Cooldown |
|---|---|---|---|---|---|
| `village_well_trouble` | PASS | PASS | PASS | PASS | PASS |
| `ruin_mark_investigation_intro` | PASS | PASS | PASS | PASS | PASS |
| `defend_the_village_night` | PASS | PASS | PASS | PASS | PASS |
| `ghost_town_medicine_run` | PASS | PASS | PASS | PASS | PASS |
| `old_well_awakening` | PASS | PASS | PASS | PASS | PASS |
| `survive_the_storm_pass` | PASS | PASS | PASS | PASS | PASS |

## 4. 기존 Done Quest 회귀

기존 Done Quest는 Category Probe card가 섞이지 않도록 `quest_ids` gate로 격리했다.

| 기존 Quest | 회귀 상태 |
|---|---|
| `herb_gathering_tutorial` | PASS |
| `forest_path_scouting_tutorial` | PASS |
| `missing_porter_search_intro` | PASS |
| `merchant_lost_pack_recovery` | PASS |

## 5. Evidence

| 항목 | Evidence |
|---|---|
| RED | `.omo/ulw-loop/evidence/quest-category-probe-20260630/phase1-red.txt` |
| GREEN | `.omo/ulw-loop/evidence/quest-category-probe-20260630/phase1-green.txt` |
| Baseline regression | `.omo/ulw-loop/evidence/quest-category-probe-20260630/baseline-regression.txt` |
| Probe scenario validation | `.omo/ulw-loop/evidence/quest-category-probe-20260630/validate-probe-scenarios.txt` |
| Manual tmux surface | `.omo/ulw-loop/evidence/quest-category-probe-20260630/tmux-probe-runs.txt` |
| Full regression | `.omo/ulw-loop/evidence/quest-category-probe-20260630/regression.txt` |

## 6. 주의점

Probe는 Category 대표 1개씩만 깊게 검증했다.

Bulk Fill은 이 문서만으로 진행하지 않는다. `docs/07_reviews/33_Quest_Category_Stability_Review_v0.1.md`의 판정 이후에만 진행한다.
