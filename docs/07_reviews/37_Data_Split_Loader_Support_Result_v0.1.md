# [Current] Data Split Loader Support Result v0.1

> 상태: [Current] Bulk Fill 2차 전에 card_rules split 구조와 split-aware loader 지원을 도입한 결과 문서.

## 1. 작업 목적

이번 작업은 Quest Expansion ULW Loop Phase 5 이후 Data Split / Loader Support Loop의 시작 작업이다.

목표는 Bulk Fill 2차 전에 `card_rules.yaml` 비대화 리스크를 줄이기 위해 다음을 도입하는 것이다.

- 기존 `data/core/card_rules.yaml` 호환 유지
- 신규 `data/content/card_rules/*.yaml` split file 지원
- core + split card rules 병합
- duplicate card id check
- split card rule `quest_ids` gate check
- 최소 1개 category split migration

이번 작업에서는 Quest 추가, Scenario 추가, Event split, Quest split, Scenario directory 이동, Bulk Fill 2차를 하지 않았다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/35_Quest_Expansion_Coverage_Audit_v0.1.md`
- `docs/07_reviews/36_Quest_Expansion_Refactor_Gate_v0.1.md`
- `data/core/card_rules.yaml`
- `data/content/base/quests.yaml`
- `data/content/base/events.yaml`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/gameplay_p0_cards.py`
- `tests/test_gameplay_p0_category_bulk_fill.py`

## 3. 변경 파일

데이터:

- `data/core/card_rules.yaml`
- `data/content/card_rules/local_problem.yaml`

코드:

- `src/fateweaver/gameplay_p0_data.py`

테스트:

- `tests/test_gameplay_p0_split_card_rules.py`
- `tests/test_gameplay_p0_category_bulk_fill.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/37_Data_Split_Loader_Support_Result_v0.1.md`

## 4. 기존 Loader 구조

기존 `load_foundation()`은 다음 파일을 고정 경로로 읽었다.

- `data/content/base/quests.yaml`
- `data/core/card_rules.yaml`
- `data/core/score_rules.yaml`

이 구조에서는 Card Rule을 category 파일로 분리해도 runtime이 읽지 못한다. 따라서 split migration 전에 loader support가 먼저 필요했다.

## 5. Split File 구조

이번 작업에서 추가한 split file 구조:

```text
data/content/card_rules/local_problem.yaml
```

loader는 다음 순서로 Card Rule을 읽는다.

1. `data/core/card_rules.yaml`
2. `data/content/card_rules/*.yaml` sorted glob
3. `p0_cards` 병합
4. 기존 `multi_select_rules`는 core file에서 유지

현재 split file은 `p0_cards`만 포함한다. combo/conflict rule은 shared rule로 보고 core file에 남긴다.

## 6. Card Rule Migration

이번 migration은 최소 범위로 `local_problem` category만 이동했다.

이동한 card rule 수: 13개.

대상 Quest:

- `village_well_trouble`
- `beginner_village_wrongness`
- `festival_missing_racer`

이동한 card ids:

- `inspect_sick_well`
- `purify_well_with_herbs`
- `report_well_restored`
- `read_village_wrongness`
- `calm_square_rumors`
- `report_wrongness_resolved`
- `share_plain_remedy`
- `find_racer_track`
- `guide_missing_racer`
- `report_festival_safe`
- `organize_festival_search`
- `test_village_wrongness_risk`
- `test_festival_risk`

Migration 후 line 수:

| 파일 | LOC |
|---|---:|
| `data/core/card_rules.yaml` | 1,901 |
| `data/content/card_rules/local_problem.yaml` | 234 |

기존 card id, quest id, scenario 파일명은 변경하지 않았다.

## 7. Duplicate ID Check

`gameplay_p0_data.py`에 duplicate card id 검사를 추가했다.

검사 기준:

- core file과 split file을 모두 병합한 전체 Card Rule id가 유일해야 한다.
- 중복 발견 시 `Duplicate card rule id` error를 낸다.
- error message에는 중복 id, 최초 source path, 중복 source path가 포함된다.

검증:

- `tests/test_gameplay_p0_split_card_rules.py::test_duplicate_card_id_raises_clear_error`

## 8. quest_ids Gate Check

split file에 들어간 card rule은 quest-specific rule로 본다.

검사 기준:

- `data/content/card_rules/*.yaml`의 모든 `p0_cards`는 `quest_ids`를 가져야 한다.
- core/shared card rule은 기존 호환성을 위해 `quest_ids`가 없을 수 있다.

검증:

- `tests/test_gameplay_p0_split_card_rules.py::test_split_card_rules_require_quest_ids`

## 9. 기존 Scenario 회귀 검증

검증 대상:

- local_problem split 대상 scenario
- 기존 category bulk regression tests
- 전체 active scenario validate
- 전체 unittest suite

Local problem scenario validate:

- `data/scenarios/village_well_trouble_success.yaml`
- `data/scenarios/beginner_village_wrongness.yaml`
- `data/scenarios/festival_missing_racer.yaml`

전체 active scenario validate는 47개 scenario PASS로 확인했다.

## 10. 실행한 명령

RED proof:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_card_rules
```

초기 결과:

```text
FAILED (failures=4)
```

GREEN / regression:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_card_rules
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_split_card_rules tests.test_gameplay_p0_category_bulk_fill
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/village_well_trouble_success.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/beginner_village_wrongness.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/festival_missing_racer.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```

최종 결과:

- split loader tests: 5 tests OK
- split loader + category bulk tests: 8 tests OK
- active quest scenario validate: 47 PASS
- full unittest: 82 tests OK
- compileall: OK
- git diff check: OK

## 11. 남은 문제

- Quest split은 아직 실행하지 않았다.
- Event split은 아직 실행하지 않았다.
- Scenario directory grouping은 아직 실행하지 않았다.
- `data/content/card_rules/`에는 현재 `local_problem.yaml`만 있다.
- 다음 category split을 진행하기 전에 category별 card ownership 표를 고정하는 것이 좋다.

## 12. 다음 추천 작업

1. `investigation_mystery` 또는 `travel_delivery_escort` Card Rule split을 다음 migration으로 진행한다.
2. split file별 card count와 quest_ids coverage를 자동 점검하는 validator/test를 확장한다.
3. `quests.yaml` split-aware loader는 Card Rule split 안정화 후 별도 작업으로 처리한다.
4. Event split은 scenario `content_sources` 전략을 먼저 확정한 뒤 진행한다.
