# [Current] Card Rules Category Split Migration Result v0.1

> 상태: [Current] card_rules split-aware loader 기반 위에서 Stable Category별 card rules를 split file로 마이그레이션한 결과 문서.

## 1. 작업 목적

이번 작업은 Data Split / Loader Support Loop의 두 번째 작업이다.

직전 작업에서 `local_problem` split과 split-aware loader가 검증되었으므로, 이번 작업에서는 나머지 Stable Category의 quest-specific card rules를 category split file로 이동했다.

이번 작업에서 하지 않은 것:

- Quest 추가
- Scenario 추가
- Event split
- Quest split
- Scenario directory 이동
- Loader 대규모 변경
- Bulk Fill 2차
- 기존 card id / quest id / scenario 파일명 변경

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/35_Quest_Expansion_Coverage_Audit_v0.1.md`
- `docs/07_reviews/36_Quest_Expansion_Refactor_Gate_v0.1.md`
- `docs/07_reviews/37_Data_Split_Loader_Support_Result_v0.1.md`
- `data/core/card_rules.yaml`
- `data/content/card_rules/local_problem.yaml`
- `src/fateweaver/gameplay_setup.py`
- `tests/test_gameplay_run_split_card_rules.py`

## 3. 변경 파일

데이터:

- `data/core/card_rules.yaml`
- `data/content/card_rules/investigation_mystery.yaml`
- `data/content/card_rules/defense_threat.yaml`
- `data/content/card_rules/travel_delivery_escort.yaml`
- `data/content/card_rules/ruin_dungeon_ritual.yaml`
- `data/content/card_rules/survival_exploration.yaml`

테스트:

- `tests/test_gameplay_run_split_card_rules.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/38_Card_Rules_Category_Split_Migration_Result_v0.1.md`

## 4. Migration 전 구조

Migration 전 구조:

```text
data/core/card_rules.yaml
data/content/card_rules/local_problem.yaml
```

Migration 전 card count:

| 파일 | Card 수 |
|---|---:|
| `data/core/card_rules.yaml` | 98 |
| `data/content/card_rules/local_problem.yaml` | 13 |
| 합계 | 111 |

Core에는 shared/foundation card와 아직 이동하지 않은 stable category card가 섞여 있었다.

## 5. Migration 후 구조

Migration 후 구조:

```text
data/core/card_rules.yaml
data/content/card_rules/local_problem.yaml
data/content/card_rules/investigation_mystery.yaml
data/content/card_rules/defense_threat.yaml
data/content/card_rules/travel_delivery_escort.yaml
data/content/card_rules/ruin_dungeon_ritual.yaml
data/content/card_rules/survival_exploration.yaml
```

Migration 후 card count:

| 파일 | Card 수 |
|---|---:|
| `data/core/card_rules.yaml` | 29 |
| `data/content/card_rules/local_problem.yaml` | 13 |
| `data/content/card_rules/investigation_mystery.yaml` | 20 |
| `data/content/card_rules/defense_threat.yaml` | 13 |
| `data/content/card_rules/travel_delivery_escort.yaml` | 18 |
| `data/content/card_rules/ruin_dungeon_ritual.yaml` | 10 |
| `data/content/card_rules/survival_exploration.yaml` | 8 |
| 합계 | 111 |

## 6. Category별 이동 결과

| Category | 이동 Card 수 | 대상 Quest |
|---|---:|---|
| `local_problem` | 13 | `village_well_trouble`, `beginner_village_wrongness`, `festival_missing_racer` |
| `investigation_mystery` | 20 | `ruin_mark_investigation_intro`, `abandoned_lighthouse_signal`, `painted_portal_canvas`, `vanishing_village` |
| `defense_threat` | 13 | `defend_the_village_night`, `beast_of_zarechka`, `cattle_mutilation_stone_circle` |
| `travel_delivery_escort` | 18 | `ghost_town_medicine_run`, `caravan_to_border_fort`, `winter_wagon_delivery`, `deliver_the_sealed_parcel` |
| `ruin_dungeon_ritual` | 10 | `old_well_awakening`, `activate_the_old_gate` |
| `survival_exploration` | 8 | `survive_the_storm_pass`, `hidden_grove_discovery` |

이번 작업에서 새 card rule은 추가하지 않았다. 기존 card block을 core에서 category split file로 이동했다.

## 7. Core에 남긴 Card Rules

Core에 남긴 Card Rule은 29개다.

남긴 기준:

- `quest_ids`가 없는 shared card
- Foundation Quest에 연결된 card
- `multi_select_rules`

`multi_select_rules`는 계속 `data/core/card_rules.yaml`에 남아 있다.

## 8. Duplicate ID Check

병합 대상:

- `data/core/card_rules.yaml`
- `data/content/card_rules/*.yaml`

검증 결과:

- 전체 loaded card rule 수: 111
- duplicate card id: 없음
- loader의 duplicate id negative test 유지

## 9. quest_ids Gate Check

검증 결과:

- 모든 split file card rule에 `quest_ids` 있음
- 빈 `quest_ids` 없음
- unknown quest id 없음
- loader의 split `quest_ids` negative test 유지

Core shared/foundation card는 기존 호환성을 위해 `quest_ids`가 없을 수 있다.

## 10. 기존 Scenario 회귀 검증

전체 active quest scenario 47개가 `tools/validate_data.py`로 PASS했다.

대표 category loader smoke도 확인했다.

- `abandoned_lighthouse_signal`: `inspect_signal_lamp` 로드
- `beast_of_zarechka`: `identify_beast_tracks` 로드
- `caravan_to_border_fort`: `secure_caravan_manifest` 로드
- `activate_the_old_gate`: `find_gate_runes` 로드
- `hidden_grove_discovery`: `find_hidden_grove` 로드

각 대표 Quest에서 병합된 Card Rule 수는 111개로 유지되었다.

## 11. 실행한 명령

Characterization / RED:

```bash
for f in investigation_mystery defense_threat travel_delivery_escort ruin_dungeon_ritual survival_exploration; do test -f data/content/card_rules/$f.yaml || echo MISSING:$f; done
```

초기 결과:

```text
MISSING:investigation_mystery
MISSING:defense_threat
MISSING:travel_delivery_escort
MISSING:ruin_dungeon_ritual
MISSING:survival_exploration
```

Targeted GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_split_card_rules tests.test_gameplay_run_category_bulk_fill
```

결과:

```text
Ran 12 tests
OK
```

최종 검증 명령은 전체 검증 완료 후 이 문서에 남긴다.

최종 검증:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```

최종 결과:

- active quest scenario validate: 47 PASS
- full unittest: 86 tests OK
- compileall: OK
- git diff check: OK

## 12. 남은 문제

- Quest split은 아직 실행하지 않았다.
- Event split은 아직 실행하지 않았다.
- Scenario directory grouping은 아직 실행하지 않았다.
- 다음 Bulk Fill 2차 전에 새 category card가 올바른 split file로 들어가는지 자동화된 ownership check를 강화할 수 있다.

## 13. 다음 추천 작업

1. Bulk Fill 2차 전에 card ownership check를 validator 또는 dedicated test로 고정한다.
2. 다음 Data Split Loop에서는 Quest split-aware loader 설계를 진행한다.
3. Event split은 scenario `content_sources` 전략 확정 후 별도 작업으로 진행한다.
