# [Current] Quest Category Probe and Bulk Loop Plan v0.1

> 상태: [Current] Quest Type Catalog 기반 Category Probe와 Bulk Fill의 실행 범위를 잠근 ULW Loop 계획 문서.

## 1. 문서 목적

이 문서는 Quest를 1개씩 추가하는 방식에서 벗어나 Category별 안정성을 먼저 검증한 뒤, 안정 Category만 Bulk Fill하는 연속 작업의 범위를 고정한다.

이번 Plan Lock은 구현 산출물이 아니라 실행 기준이다.

- Category별 Probe Quest를 먼저 구현한다.
- Probe는 success / partial_success / failure를 모두 검증한다.
- Category Stability Review 전에는 Bulk Fill을 하지 않는다.
- 기존 Done Quest 회귀를 유지한다.
- 새 대형 시스템을 끼워 넣지 않는다.

## 2. 기준 문서

- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`
- `/Users/cheng80/Desktop/ULW_PLAN_Quest_Category_Probe_And_Bulk_Loop_v0.1.md`

## 3. 고정 제약

이번 ULW Loop에서 지켜야 할 제약은 다음과 같다.

| 제약 | 적용 |
|---|---|
| 기존 Done Quest 회귀 유지 | `herb_gathering_tutorial`, `forest_path_scouting_tutorial`, `missing_porter_search_intro`, `merchant_lost_pack_recovery` |
| Probe 검증 강도 | 각 대표 Quest는 success / partial_success / failure 모두 검증 |
| Stability Review | Category별 `Stable`, `Needs Small Schema Extension`, `Needs New System`, `Deferred` 판정 |
| Bulk Fill | Stability Review 이후 `Stable` Category에만 허용 |
| 금지 구현 | Storylet Pool 전체 시스템, Repeat Cooldown 장기 저장, Flutter/Flame UI |

## 4. Category Probe 순서

Phase 1은 다음 순서를 고정한다.

| 순서 | Category | Probe Quest | Catalog Type | 목적 |
|---:|---|---|---|---|
| 1 | Local Problem | `village_well_trouble` | `local_problem` | 마을 내부 문제, 주민 반응, 평판, 복구/정화 검증 |
| 2 | Investigation / Mystery | `ruin_mark_investigation_intro` | `investigation` | 단서, 징조, 해석 실패, 후속 해금 검증 |
| 3 | Defense / Threat | `defend_the_village_night` | `defense` | 방어, 야간 압박, 민간인 보호 검증 |
| 4 | Travel / Delivery / Escort | `ghost_town_medicine_run` | `delivery` | 이동, 배송, 보급, 질병 압박 검증 |
| 5 | Ruin / Dungeon / Ritual | `old_well_awakening` | `dungeon_crawl` | 던전 진입, 봉인, 지하 위험 검증 |
| 6 | Survival / Exploration | `survive_the_storm_pass` | `survival` | 환경 위험, 자원 압박, 생존 판단 검증 |

## 5. Probe 최소 구현 기준

각 Probe Quest는 다음 항목을 포함해야 한다.

| 항목 | 기준 |
|---|---|
| Quest data | 기존 `quests.yaml` schema 안에서 표현 |
| Card Rule | 기존 Card Rule schema 안에서 quest gate로 격리 |
| Storylet/Event Hint | 기존 event hint와 cooldown 필드 사용 |
| Scenario | success, partial_success, failure fixture |
| Result semantics | `result_type`, `failure_kind`, `character_outcome` 의미 유지 |
| Logs | JSON log와 Text MUD log에서 결과 의미 확인 |
| Regression | 기존 Done Quest 테스트 유지 |

## 6. Category Stability Gate

Probe 완료 후 Category는 다음 기준으로 판정한다.

| 판정 | 기준 | Bulk Fill |
|---|---|---|
| Stable | 기존 Objective/Card/Event/Scenario 구조로 표현 가능 | 허용 |
| Needs Small Schema Extension | 작은 schema/code 확장 없이는 반복 구현이 부자연스러움 | 보류 |
| Needs New System | 새 evaluator, 새 Storylet Pool, 장기 저장 등 별도 시스템 필요 | 금지 |
| Deferred | P0 이후가 적합하거나 현재 검증 비용이 큼 | 금지 |

Stability Review 전에는 Bulk Fill을 실행하지 않는다.

## 7. Bulk Fill 후보

Bulk Fill은 Phase 2 Stability Review 이후에만 진행한다.

| Category | Bulk 후보 |
|---|---|
| Local Problem | `beginner_village_wrongness`, `tanglewood_faire_games`, `festival_missing_racer` |
| Investigation / Mystery | `vanishing_village`, `abandoned_lighthouse_signal`, `painted_portal_canvas`, `mansion_returned_explorer`, `dreamless_king` |
| Defense / Threat | `beast_of_zarechka`, `awaken_the_beast`, `cattle_mutilation_stone_circle` |
| Travel / Delivery / Escort | `winter_wagon_delivery`, `deliver_the_sealed_parcel`, `stowaway_without_memory`, `old_east_trail_rescue` |
| Ruin / Dungeon / Ritual | `crypt_of_elven_king`, `activate_the_old_gate`, `awaken_the_monolith`, `sealed_ruin_entry`, `ruined_island_puzzle_box` |
| Survival / Exploration | `frozen_treasure_cave`, `hidden_grove_discovery`, `lost_city_rising_sands` |

## 8. Phase 산출물

| Phase | 산출물 | 검증 |
|---|---|---|
| Phase 0 Plan Lock | `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md` | 문서 존재, index 등록, `data/src/tests` diff 없음 |
| Phase 1 Category Probe | `docs/07_reviews/32_Quest_Category_Probe_Result_v0.1.md` | 6개 Probe success/partial/failure, 로그, 회귀 |
| Phase 2 Stability Review | `docs/07_reviews/33_Quest_Category_Stability_Review_v0.1.md` | Category별 판정과 Bulk 가능 여부 |
| Phase 3 Bulk Fill | 안정 Category별 data/scenario/test 추가 | Stability Review 이후에만 실행 |

## 9. Phase 1 검증 명령

Phase 1의 기본 검증 표면은 CLI와 pytest다.

```bash
PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0 tests.test_gameplay_p0_forest_path_scouting tests.test_gameplay_p0_missing_porter_search tests.test_gameplay_p0_merchant_lost_pack
PYTHONPATH=src .venv/bin/python -m unittest tests.test_text_mud_log tests.test_gameplay_p0_failure_outcomes
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

Probe 구현 중에는 각 Category별 targeted pytest와 simulator/tmux transcript를 evidence로 남긴다.

## 10. 명시적 비목표

이번 ULW Loop는 다음을 하지 않는다.

- Storylet Pool 전체 시스템 구현
- Repeat Cooldown 장기 저장 구현
- Flutter/Flame UI 구현
- Stability Review 전 Bulk Fill
- Quest 후보 외 새 Quest 창작
- `result_type`, `failure_kind`, `character_outcome` 의미 변경
- 기존 JSON/Text MUD log 호환성 파괴
