# [Current] Quest Data Split Loader Support Result v0.1

> 상태: [Current] Quest split 구조와 split-aware quest loader 지원을 도입한 결과 문서.

## 1. 작업 목적

이번 작업은 Data Split / Loader Support Loop의 세 번째 작업이다.

Card Rules category split이 완료된 뒤, Bulk Fill 2차 전에 Quest data도 category split 구조로 읽을 수 있게 만들었다.

이번 작업에서 하지 않은 것:

- Quest 추가
- Scenario 추가
- Event split
- Card Rule 추가
- Scenario directory 이동
- Bulk Fill 2차
- 기존 quest id / card id / scenario 파일명 변경

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/35_Quest_Expansion_Coverage_Audit_v0.1.md`
- `docs/07_reviews/36_Quest_Expansion_Refactor_Gate_v0.1.md`
- `docs/07_reviews/37_Data_Split_Loader_Support_Result_v0.1.md`
- `docs/07_reviews/38_Card_Rules_Category_Split_Migration_Result_v0.1.md`
- `data/content/base/quests.yaml`
- `data/content/card_rules/`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/data_loader.py`
- `tests/test_gameplay_p0_split_card_rules.py`

## 3. 변경 파일

데이터:

- `data/content/base/quests.yaml`
- `data/content/quests/foundation.yaml`
- `data/content/quests/local_problem.yaml`
- `data/content/quests/investigation_mystery.yaml`
- `data/content/quests/defense_threat.yaml`
- `data/content/quests/travel_delivery_escort.yaml`
- `data/content/quests/ruin_dungeon_ritual.yaml`
- `data/content/quests/survival_exploration.yaml`

코드:

- `src/fateweaver/gameplay_p0_data.py`

테스트:

- `tests/test_gameplay_p0_split_quests.py`
- `tests/test_gameplay_p0_category_bulk_fill.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/39_Quest_Data_Split_Loader_Support_Result_v0.1.md`

## 4. Loader 변경

기존 `load_foundation()`은 다음 파일만 읽었다.

```text
data/content/base/quests.yaml
```

이번 작업 후 loader는 다음 순서로 Quest를 읽는다.

1. `data/content/base/quests.yaml`
2. `data/content/quests/*.yaml` sorted glob
3. `quests` 병합
4. duplicate quest id 검사

기존 public API인 `load_foundation(root, quest_id)`는 유지했다.

## 5. Quest Split 구조

Migration 후 구조:

```text
data/content/base/quests.yaml
data/content/quests/foundation.yaml
data/content/quests/local_problem.yaml
data/content/quests/investigation_mystery.yaml
data/content/quests/defense_threat.yaml
data/content/quests/travel_delivery_escort.yaml
data/content/quests/ruin_dungeon_ritual.yaml
data/content/quests/survival_exploration.yaml
```

Foundation Quest 4개는 기존 base 호환성을 위해 `data/content/base/quests.yaml`에 남겼다. `foundation.yaml`은 Category 구조 고정을 위한 빈 split file이다.

## 6. Category별 이동 결과

| Category | 이동 Quest 수 | 대상 Quest |
|---|---:|---|
| Foundation | 0 | base file에 `herb_gathering_tutorial`, `forest_path_scouting_tutorial`, `missing_porter_search_intro`, `merchant_lost_pack_recovery` 유지 |
| `local_problem` | 3 | `village_well_trouble`, `beginner_village_wrongness`, `festival_missing_racer` |
| `investigation_mystery` | 4 | `ruin_mark_investigation_intro`, `abandoned_lighthouse_signal`, `painted_portal_canvas`, `vanishing_village` |
| `defense_threat` | 3 | `defend_the_village_night`, `beast_of_zarechka`, `cattle_mutilation_stone_circle` |
| `travel_delivery_escort` | 4 | `ghost_town_medicine_run`, `caravan_to_border_fort`, `winter_wagon_delivery`, `deliver_the_sealed_parcel` |
| `ruin_dungeon_ritual` | 2 | `old_well_awakening`, `activate_the_old_gate` |
| `survival_exploration` | 2 | `survive_the_storm_pass`, `hidden_grove_discovery` |

전체 loaded Quest 수는 22개로 유지된다.

## 7. Duplicate ID Check

검사 기준:

- base file과 split file을 모두 병합한 전체 Quest id가 유일해야 한다.
- 중복 발견 시 `Duplicate quest id` error를 낸다.
- error message에는 중복 id, 최초 source path, 중복 source path가 포함된다.

검증:

- `tests.test_gameplay_p0_split_quests.GameplayP0SplitQuestTests.test_duplicate_quest_id_raises_clear_error`

## 8. 불변성 확인

이번 작업은 data 위치만 바꿨고 다음 항목을 변경하지 않았다.

- Quest id
- Card id
- Scenario filename
- Scenario directory
- Event file
- Card Rule file
- `result_type` / `failure_kind` / `character_outcome` 의미

## 9. 실행한 명령

RED proof:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_quests
```

초기 결과:

```text
FAILED (failures=2, errors=1)
```

주요 실패:

- split quest 미로드: `Unknown P0 quest: village_well_trouble`
- duplicate quest id: `ValueError not raised`
- split quest file 부재

Targeted GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_quests tests.test_gameplay_p0_split_card_rules tests.test_gameplay_p0_category_bulk_fill
```

결과:

```text
Ran 16 tests
OK
```

최종 검증:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```

최종 결과:

- targeted split / card split / category bulk tests: 16 tests OK
- active quest scenario validate: 47 PASS
- full unittest: 90 tests OK
- compileall: OK
- git diff check: OK
- inventory compare: Quest id / Card id / Scenario filename unchanged

## 10. 남은 문제

- Event split은 아직 실행하지 않았다.
- Scenario directory grouping은 아직 실행하지 않았다.
- Bulk Fill 2차는 아직 실행하지 않았다.
- Foundation Quest는 base 호환성 때문에 split file로 이동하지 않았다.

## 11. 다음 추천 작업

1. Bulk Fill 2차 전에 Event split 전략을 별도 Refactor Gate로 확정한다.
2. Scenario 파일 수가 더 늘기 전에 scenario grouping 기준을 문서화한다.
3. Quest/Card/Event split ownership check를 validator 또는 dedicated test로 확장한다.
