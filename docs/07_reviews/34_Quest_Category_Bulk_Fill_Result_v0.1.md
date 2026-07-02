# [Current] Quest Category Bulk Fill Result v0.1

> 상태: [Current] Stable 판정된 Quest Category의 나머지 Quest를 lightweight success fixture 중심으로 Bulk Fill한 결과 문서.

## 1. 작업 목적

Phase 1 Probe와 Phase 2 Stability Review에서 Stable 판정된 6개 Category를 대상으로, 각 Category의 나머지 Quest를 success fixture 중심으로 일괄 추가했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/32_Quest_Category_Probe_Result_v0.1.md`
- `docs/07_reviews/33_Quest_Category_Stability_Review_v0.1.md`

## 3. Bulk Fill 기준

- 각 Bulk Quest는 Quest data, 최소 5개 Card Rule, 2개 Event Hint, success scenario 1개를 가진다.
- 각 Bulk Quest에는 partial/failure fixture를 만들지 않았다.
- Category 대표 Probe Quest의 success/partial/failure 검증은 기존 Probe 결과를 유지한다.
- Storylet Pool 전체 시스템, 장기 Repeat Cooldown 저장, Flutter/Flame UI는 구현하지 않았다.

## 4. 추가한 Quest 요약

총 12개 Bulk Quest를 추가했다.

| Category | Quest |
|---|---|
| Local | `beginner_village_wrongness`, `festival_missing_racer` |
| Investigation | `abandoned_lighthouse_signal`, `painted_portal_canvas`, `vanishing_village` |
| Defense | `beast_of_zarechka`, `cattle_mutilation_stone_circle` |
| Travel | `caravan_to_border_fort`, `winter_wagon_delivery`, `deliver_the_sealed_parcel` |
| Ruin-Dungeon | `activate_the_old_gate` |
| Survival | `hidden_grove_discovery` |

## 5. Category별 추가 결과

Stable Category 전체에 lightweight coverage를 확보했다.

- Local: 마을 내부 이상과 축제 실종 문제.
- Investigation: 등대 신호, 포털 화폭, 사라지는 마을.
- Defense: 짐승 위협과 돌 원 주변 가축 피해.
- Travel: 상단 호위, 겨울 배송, 봉인 소포 배달.
- Ruin-Dungeon: 오래된 문 작동.
- Survival: 숨은 숲 빈터 발견.

## 6. Quest Data 변경

`data/content/base/quests.yaml`에 12개 Quest를 추가했다.

각 Quest는 다음 objective 구조를 공유한다.

- 핵심 단서 발견: `discover_clue`
- 문제 처리: `optional_action`
- 결과 보고/귀환: `return_to_region`
- 생존: `survive_expedition`
- 선택 보조 목표: `keep_resource_at_least`

## 7. Card Rule 변경

`data/core/card_rules.yaml`에 각 Quest별 5개 Card Rule을 추가했다.

- 3개 `quest_progress` 카드.
- 1개 `risk_discovery` 카드.
- 1개 `resource_alternative` 카드.
- 모든 신규 Card Rule에는 해당 Quest의 `quest_ids`를 지정했다.

## 8. Storylet/Event Hint 변경

`data/content/base/events.yaml`에 각 Quest별 2개 Event Hint를 추가했다.

- 모든 신규 Event Hint에는 `quest_ids`를 명시했다.
- P0 Event 모델과 Storylet selection은 `quest_ids`를 런타임 필터로 사용한다.
- 실제 오염 방지는 Event `quest_ids`, Card Rule `quest_ids`, scenario include gate로 검증했다.

## 9. Scenario Fixture

`data/scenarios/<quest_id>.yaml` 규칙으로 12개 success scenario를 추가했다.

## 10. quest_ids Gate 검증

`tests/test_gameplay_run_category_bulk_fill.py`에서 다음을 검증했다.

- 신규 Bulk Card Rule은 모두 `quest_ids == [quest_id]`를 가진다.
- 신규 Bulk Event Hint는 모두 `quest_ids == [quest_id]`를 가진다.
- 신규 Bulk Event Hint는 active Quest가 다르면 Storylet selection에서 제외된다.
- 기존 Done Quest success scenario에서 신규 Bulk card가 presented/selected 되지 않는다.

## 11. JSON / Text MUD Log 검증

Batch 테스트와 simulator evidence에서 다음을 확인했다.

- JSON: `quest.id`, `presented_cards`, `selected_cards`, `card_candidate_pool`, `storylet_tags`, `storylet_id`, `objective_results`, `quest_report.result_type`, `score_breakdown`.
- Text MUD: Quest 제목, 카드, 선택, 결과, Quest Report, `결과 유형: success`.

## 12. 기존 Done Quest 회귀 검증

기존 Done Quest 10개를 회귀 표면으로 유지했다.

- `herb_gathering_tutorial`
- `forest_path_scouting_tutorial`
- `missing_porter_search_intro`
- `merchant_lost_pack_recovery`
- `village_well_trouble`
- `ruin_mark_investigation_intro`
- `defend_the_village_night`
- `ghost_town_medicine_run`
- `old_well_awakening`
- `survive_the_storm_pass`

## 13. 실행한 명령

최종 검증 명령은 ULW evidence에 기록했다.

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_category_bulk_fill`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests`
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools`
- `git diff --check`
- `.venv/bin/python tools/check-no-excuse-rules.py`
- 신규 Bulk scenario `validate_data.py`
- 신규 Bulk scenario simulator/Text MUD sample

## 14. 줄이거나 보류한 Quest

이번 batch에서는 12개 권장 목록을 우선했다.

보류:

- `tanglewood_faire_games`
- `dreamless_king`
- `mansion_returned_explorer`
- `awaken_the_beast`
- `stowaway_without_memory`
- `old_east_trail_rescue`
- `crypt_of_elven_king`
- `awaken_the_monolith`
- `sealed_ruin_entry`
- `ruined_island_puzzle_box`
- `frozen_treasure_cave`
- `lost_city_rising_sands`

보류 이유는 P0 lightweight bulk 범위보다 분기, 후속 해금, 장소 확장, 또는 던전/의식 규모가 커질 가능성이 높기 때문이다.

## 15. 남은 문제

- 없음.

## 16. 다음 추천 작업

- Bulk Fill 보류 Quest는 다음 batch에서 Category별 1~2개만 추가 검토한다.
