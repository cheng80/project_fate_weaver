# [Current] Event Hint Split Loader Support Result v0.1

> 상태: [Current] Bulk Fill 2차 전에 Event / Storylet Hint split 구조와 split-aware event loader 지원을 도입한 결과 문서.

## 1. 작업 목적

이번 작업은 Data Split / Loader Support Loop의 네 번째 작업이다.

Card Rules split과 Quest Data split이 완료된 뒤, Bulk Fill 2차 전에 Event / Storylet Hint도 category split 구조로 읽을 수 있게 만들었다.

이번 작업에서 하지 않은 것:

- Quest 추가
- Scenario 추가
- Card Rule 추가
- Scenario directory 이동
- Bulk Fill 2차
- 기존 event id / quest id / card id / scenario 파일명 변경

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
- `docs/07_reviews/39_Quest_Data_Split_Loader_Support_Result_v0.1.md`
- `data/content/base/events.yaml`
- `data/content/quests/`
- `data/content/card_rules/`
- `src/fateweaver/data_loader.py`
- `tests/test_gameplay_p0_category_bulk_fill.py`

## 3. 변경 파일

데이터:

- `data/content/base/events.yaml`
- `data/content/events/foundation.yaml`
- `data/content/events/local_problem.yaml`
- `data/content/events/investigation_mystery.yaml`
- `data/content/events/defense_threat.yaml`
- `data/content/events/travel_delivery_escort.yaml`
- `data/content/events/ruin_dungeon_ritual.yaml`
- `data/content/events/survival_exploration.yaml`

코드:

- `src/fateweaver/data_loader.py`

테스트:

- `tests/test_gameplay_p0_split_events.py`
- `tests/test_gameplay_p0_category_bulk_fill.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/40_Event_Hint_Split_Loader_Support_Result_v0.1.md`

## 4. 기존 Event Loader 구조

기존 `load_project_data()`는 scenario의 `content_sources`를 순회하면서 해당 YAML 파일 안의 `events`만 읽었다.

대부분의 active scenario는 다음 source를 포함한다.

```text
data/content/base/events.yaml
```

따라서 Event Hint를 category split file로 이동하면 기존 loader는 새 파일을 읽지 못했다. 또한 duplicate event id error는 event id만 보여 주고 충돌 source path를 알려 주지 않았다.

## 5. Split File 구조

Migration 후 구조:

```text
data/content/base/events.yaml
data/content/events/foundation.yaml
data/content/events/local_problem.yaml
data/content/events/investigation_mystery.yaml
data/content/events/defense_threat.yaml
data/content/events/travel_delivery_escort.yaml
data/content/events/ruin_dungeon_ritual.yaml
data/content/events/survival_exploration.yaml
```

Loader는 scenario `content_sources`가 `data/content/base/events.yaml`을 포함할 때 다음 순서로 Event를 읽는다.

1. `data/content/base/events.yaml`
2. `data/content/events/*.yaml` sorted glob
3. Event list 병합
4. duplicate event id 검사

기존 public API인 `load_project_data(project_root, scenario_path)`는 유지했다.

## 6. Event Migration

이번 migration은 `quest_ids`가 있는 Bulk Fill Event Hint 24개를 category split file로 이동했다.

| Category | 이동 Event 수 | 대상 Quest |
|---|---:|---|
| `foundation` | 0 | 빈 split file 유지 |
| `local_problem` | 4 | `beginner_village_wrongness`, `festival_missing_racer` |
| `investigation_mystery` | 6 | `abandoned_lighthouse_signal`, `painted_portal_canvas`, `vanishing_village` |
| `defense_threat` | 4 | `beast_of_zarechka`, `cattle_mutilation_stone_circle` |
| `travel_delivery_escort` | 6 | `caravan_to_border_fort`, `winter_wagon_delivery`, `deliver_the_sealed_parcel` |
| `ruin_dungeon_ritual` | 2 | `activate_the_old_gate` |
| `survival_exploration` | 2 | `hidden_grove_discovery` |

`data/content/base/events.yaml`에는 31개 Event가 남았다.

남긴 기준:

- shared Event
- foundation/tutorial Event
- probe Event
- `quest_ids`가 아직 없는 기존 호환 Event

이번 작업에서 새 Event는 추가하지 않았다. 기존 event block을 base에서 category split file로 이동했다.

## 7. Duplicate Event ID Check

병합 대상:

- `data/content/base/events.yaml`
- `data/content/events/*.yaml`

검사 기준:

- 전체 loaded Event id가 유일해야 한다.
- 중복 발견 시 `Duplicate event id` error를 낸다.
- error message에는 중복 id, 최초 source path, 중복 source path가 포함된다.

검증:

- `tests.test_gameplay_p0_split_events.GameplayP0SplitEventTests.test_duplicate_event_id_raises_clear_error`

## 8. quest_ids / card_candidate_hints 정합성

검증 결과:

- split Event `quest_ids` unknown: 0
- split Event `card_candidate_hints` unknown: 0
- 전체 loaded Event 수: 55
- `quest_ids` 보유 Event 수: 24

Core/base shared/foundation/probe Event는 기존 호환성을 위해 `quest_ids`가 없을 수 있다.

## 9. 기존 Scenario 회귀 검증

전체 active quest scenario 47개가 `tools/validate_data.py`로 PASS했다.

대표 runtime source path smoke:

- `village_market`: `data/content/base/events.yaml`
- `hidden_grove_hint`: `data/content/events/survival_exploration.yaml`
- `hidden_grove_followup`: `data/content/events/survival_exploration.yaml`

Inventory compare:

- Event id set: 55개 유지
- Quest id set: 22개 유지
- Card id set: 111개 유지
- Scenario filename set: 51개 유지

## 10. 실행한 명령

RED proof:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_events
```

초기 결과:

```text
FAILED (failures=3)
```

주요 실패:

- duplicate event id negative test에서 `ValueError not raised`
- `data/content/events/*.yaml` category split file 부재
- base에서 제거한 split event 미로드

Targeted GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_events tests.test_gameplay_p0_category_bulk_fill
```

결과:

```text
Ran 10 tests
OK
```

최종 검증:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario <47 active quest scenarios>
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```

최종 결과:

- active quest scenario validate: 47 PASS
- full unittest: 97 tests OK
- compileall: PASS
- git diff check: PASS

## 11. 남은 문제

- Foundation/probe Event 중 `quest_ids`가 없는 항목은 기존 호환을 위해 base file에 남아 있다.
- Scenario directory grouping은 아직 실행하지 않았다.
- Bulk Fill 2차는 아직 실행하지 않았다.
- `data/content/events/foundation.yaml`은 현재 빈 split file이다.

## 12. 다음 추천 작업

1. Bulk Fill 2차에서 새 quest-specific Event Hint는 category split file에 추가하고 `quest_ids`를 유지한다.
2. Foundation/probe Event에 `quest_ids`를 부여할지 별도 cleanup gate에서 판단한다.
3. Scenario 파일 수가 더 늘기 전에 scenario grouping 기준을 문서화한다.
