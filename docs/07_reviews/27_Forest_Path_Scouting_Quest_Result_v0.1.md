# [Current] Forest Path Scouting Quest Result v0.1

> 상태: [Current] `forest_path_scouting_tutorial` Quest를 실제 data fixture로 추가하고 success / partial_success / failure 시나리오를 검증한 결과 문서.

## 1. 작업 목적

Gameplay P0 기반 정리 이후 첫 번째 신규 Quest(퀘스트)인 `forest_path_scouting_tutorial`을 실제 data fixture(데이터 고정물)로 추가했다.

범위는 Quest(퀘스트) 1개, 최소 Card Rule(카드 규칙), 최소 Storylet/Event Hint(스토리 조각/이벤트 힌트), success / partial_success / failure scenario(성공 / 부분 성공 / 실패 시나리오) 검증으로 제한했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/24_Gameplay_P0_Seeded_Tier_Variety_Result_v0.1.md`
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`
- `docs/07_reviews/26_Gameplay_P0_Storylet_Hints_Repeat_Cooldown_Result_v0.1.md`
- `data/content/base/quests.yaml`
- `data/content/base/events.yaml`
- `data/core/card_rules.yaml`
- `data/core/score_rules.yaml`
- `data/core/ontology.yaml`

## 3. 변경 파일

- `data/content/base/quests.yaml`
- `data/content/base/events.yaml`
- `data/core/card_rules.yaml`
- `data/scenarios/forest_path_scouting_tutorial.yaml`
- `data/scenarios/forest_path_scouting_tutorial_partial.yaml`
- `data/scenarios/forest_path_scouting_tutorial_failure.yaml`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/gameplay_p0_cards.py`
- `src/fateweaver/gameplay_p0_models.py`
- `tests/test_gameplay_p0_forest_path_scouting.py`
- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/27_Forest_Path_Scouting_Quest_Result_v0.1.md`

## 4. Quest 데이터

추가 Quest(퀘스트):

- id: `forest_path_scouting_tutorial`
- title: `숲길 안전 조사`
- type: `scouting`
- start region(시작 지역): `village`
- target regions(대상 지역): `forest`
- max days(최대 일수): 5
- max turns(최대 턴): 10

Objectives(목표):

- `discover_safe_path`: `discover_clue`, required(필수), target `safe_forest_path`
- `return_to_village`: `return_to_region`, required(필수), progress key `reported_safe_path`
- `survive_expedition`: `survive_expedition`, required(필수)
- `mark_beast_tracks`: `optional_action`, optional(선택)
- `keep_food`: `keep_resource_at_least`, optional(선택)

Rewards(보상):

- money: 2
- reputation: 1
- score: 40
- unlock_quests: `missing_porter_search_intro`

## 5. Card Rule 추가

추가 Card Rule(카드 규칙):

- `inspect_forest_marker`: 안전한 숲길 단서 `safe_forest_path` 발견.
- `follow_beast_tracks`: 위험 단서와 health(체력) 비용을 주는 risk discovery(위험 발견).
- `mark_beast_tracks`: `mark_beast_tracks` optional_action(선택 행동) 완료.
- `conserve_food_on_trail`: food(식량) 보존.
- `return_to_village_report`: `reported_safe_path` 진행도와 village(마을) 귀환/보고 완료.

새 카드에는 `quest_ids: [forest_path_scouting_tutorial]`를 추가했다. 이 값이 있는 카드는 active Quest(활성 퀘스트)가 일치할 때만 후보가 된다.

## 6. Storylet/Event Hint 추가

추가 Event Hint(이벤트 힌트):

- `forest_trail_marker_hint`: `inspect_forest_marker`, `follow_beast_tracks`, `conserve_food_on_trail` 후보를 밀어준다.
- `forest_beast_tracks_hint`: `follow_beast_tracks`, `mark_beast_tracks`, `conserve_food_on_trail` 후보를 밀어준다.
- `forest_return_report_hint`: `return_to_village_report`, `conserve_food_on_trail` 후보를 밀어준다.

각 Event(이벤트)는 `storylet_tags`, `card_candidate_hints`, `cooldown_tags`, `repeat_group`을 가진다.

## 7. Scenario Fixture

추가 Scenario(시나리오):

- success: `data/scenarios/forest_path_scouting_tutorial.yaml`
- partial_success: `data/scenarios/forest_path_scouting_tutorial_partial.yaml`
- failure: `data/scenarios/forest_path_scouting_tutorial_failure.yaml`

## 8. Success 검증

`forest_path_scouting_tutorial.yaml` 실행 결과:

- result_type: `success`
- completed objectives: `discover_safe_path`, `return_to_village`
- failed objectives: 없음
- rewards: 존재
- score: 170

## 9. Partial Success 검증

`forest_path_scouting_tutorial_partial.yaml` 실행 결과:

- result_type: `partial_success`
- completed objectives: `discover_safe_path`
- failed objectives: `return_to_village`
- partial reasons: `report_failed`, `optional_failed`, `return_late`, `reduced_reward`
- rewards: 없음
- score: 78

## 10. Failure 검증

`forest_path_scouting_tutorial_failure.yaml` 실행 결과:

- result_type: `failure`
- failed objectives: `discover_safe_path`, `return_to_village`, `survive_expedition`
- failure reasons: `return_failed`, `health_zero`, `primary_objective_failed`
- rewards: 없음
- score: -90

## 11. Storylet Hint / Repeat Cooldown 검증

Success run(성공 실행)에서 확인한 내용:

- Turn 1: `forest_trail_marker_hint`가 `inspect_forest_marker`를 hint(힌트)로 제공했다.
- Turn 2: `forest_beast_tracks_hint`가 `mark_beast_tracks`를 hint(힌트)로 제공했다.
- JSON log(JSON 로그)에 `repeat_memory_snapshot`, `repeat_memory_after`, `cooldown_tags`, `repeat_groups`가 기록됐다.

## 12. JSON / Text MUD Log 검증

Evidence(증거) 경로:

- `.omo/ulw-loop/evidence/forest-path-scouting-20260630/success2/`
- `.omo/ulw-loop/evidence/forest-path-scouting-20260630/partial2/`
- `.omo/ulw-loop/evidence/forest-path-scouting-20260630/failure2/`
- `.omo/ulw-loop/evidence/forest-path-scouting-20260630/herb-regression2/`

JSON log(JSON 로그)에서 확인:

- `quest_id = forest_path_scouting_tutorial`
- `presented_cards`
- `selected_cards`
- `card_candidate_pool`
- `storylet_id`
- `storylet_tags`
- `card_candidate_hints`
- `repeat_memory_snapshot`
- `objective_results`
- `score_breakdown`
- `quest_report.result_type`

Text MUD log(텍스트 MUD 로그)에서 success / partial run(성공 / 부분 성공 실행)의 카드 3장, 선택 카드, Quest Report(퀘스트 보고서), objective result(목표 결과)를 확인했다.

## 13. 기존 Herb Tutorial 회귀 검증

`tutorial_herb_quest.yaml`은 계속 `success`를 반환했다.

추가로 `quest_ids` gate(퀘스트 ID 게이트)를 도입해 forest path 전용 카드가 `herb_gathering_tutorial`의 3-Card 후보에 섞이지 않게 했다.

## 14. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_forest_path_scouting
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_forest_path_scouting tests.test_gameplay_p0 tests.test_gameplay_p0_card_candidates tests.test_gameplay_p0_storylet_cooldown
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/forest_path_scouting_tutorial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/forest_path_scouting_tutorial_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/forest_path_scouting_tutorial_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py src/fateweaver/gameplay_p0_data.py src/fateweaver/gameplay_p0_cards.py src/fateweaver/gameplay_p0_models.py tests/test_gameplay_p0_forest_path_scouting.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/forest-path-scouting-20260630/success2 --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/forest-path-scouting-20260630/partial2 --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/forest-path-scouting-20260630/failure2 --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/forest-path-scouting-20260630/herb-regression2 --profile balanced
```

## 15. 남은 문제

- Quest(퀘스트) 10개 대량 확장은 하지 않았다.
- Storylet Pool(스토리 조각 풀) 전체 시스템은 구현하지 않았다.
- Repeat Cooldown Memory(반복 쿨다운 기억) 장기 저장은 구현하지 않았다.
- Failure(실패) 시나리오는 health_zero(체력 0) 기반이라 turn(턴) 없이 Quest Report(퀘스트 보고서)를 검증한다.

## 16. 다음 추천 작업

1. `missing_porter_search_intro` Quest(퀘스트)를 1개만 추가한다.
2. rescue(구조), time pressure(시간 압박), partial success(부분 성공) 경로를 기존 evaluator(평가기)로 먼저 검증한다.
3. `herb_gathering_tutorial`과 `forest_path_scouting_tutorial` 회귀 검증을 계속 함께 실행한다.
