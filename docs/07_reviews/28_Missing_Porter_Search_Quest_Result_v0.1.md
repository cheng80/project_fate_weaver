# [Current] Missing Porter Search Quest Result v0.1

> 상태: [Current] `missing_porter_search_intro` Quest를 실제 data fixture로 추가하고 rescue / time pressure / partial_success 경로를 검증한 결과 문서.

## 1. 작업 목적

`forest_path_scouting_tutorial` 다음 Quest(퀘스트)로 `missing_porter_search_intro` 1개만 실제 data fixture(데이터 고정물)로 추가했다.

범위는 Quest(퀘스트) 1개, Quest 전용 Card Rule(카드 규칙), 최소 Storylet/Event Hint(스토리 조각/이벤트 힌트), success / partial_success / failure scenario(성공 / 부분 성공 / 실패 시나리오) 검증으로 제한했다.

## 2. 변경 파일

- `data/content/base/quests.yaml`
- `data/content/base/events.yaml`
- `data/core/card_rules.yaml`
- `data/scenarios/missing_porter_search_intro.yaml`
- `data/scenarios/missing_porter_search_intro_partial.yaml`
- `data/scenarios/missing_porter_search_intro_failure.yaml`
- `tests/test_gameplay_p0_missing_porter_search.py`
- `docs/00_index/README_Docs_Index.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/28_Missing_Porter_Search_Quest_Result_v0.1.md`

## 3. Quest 데이터

추가 Quest(퀘스트):

- id: `missing_porter_search_intro`
- title: `실종된 짐꾼 수색`
- type: `rescue`
- start region(시작 지역): `village`
- target regions(대상 지역): `forest`
- max days(최대 일수): 5
- max turns(최대 턴): 10

Objectives(목표):

- `find_porter_trace`: `discover_clue`, required(필수), target `porter_trace`
- `resolve_porter_fate`: `optional_action`, required(필수), progress key `porter_fate_resolved`
- `return_to_village`: `return_to_region`, required(필수), progress key `porter_reported`
- `survive_expedition`: `survive_expedition`, required(필수)
- `recover_lost_pack`: `optional_action`, optional(선택)
- `keep_food`: `keep_resource_at_least`, optional(선택)

Rewards(보상):

- money: 2
- reputation: 2
- score: 45
- unlock_quests: `merchant_lost_pack_recovery`

## 4. Card Rule 추가

추가 Card Rule(카드 규칙):

- `track_porter_footprints`: `porter_trace` clue(단서) 발견 및 forest(숲) 이동.
- `inspect_broken_cart`: 부서진 수레 조사, health(체력) 비용과 추가 clue/omen(단서/징조) 제공.
- `rescue_injured_porter`: `porter_fate_resolved` 진행도를 올리는 rescue(구조) 핵심 카드.
- `recover_lost_pack`: `recover_lost_pack` optional_action(선택 행동) 완료.
- `return_with_porter_report`: `porter_reported` 진행도와 village(마을) 귀환/보고 완료.
- `buy_hunter_information`: money(돈)를 써서 `porter_trace`를 얻는 대체 진입 카드.

새 카드는 모두 `quest_ids: [missing_porter_search_intro]`를 가진다. 따라서 active Quest(활성 퀘스트)가 다르면 3-Card 후보에 포함되지 않는다.

## 5. Storylet/Event Hint 추가

추가 Event Hint(이벤트 힌트):

- `old_road_footprints_hint`: `track_porter_footprints`, `inspect_broken_cart`, `buy_hunter_information` 후보를 밀어준다.
- `broken_cart_near_forest_hint`: `inspect_broken_cart`, `recover_lost_pack`, `rescue_injured_porter` 후보를 밀어준다.
- `injured_porter_call_hint`: `rescue_injured_porter`, `recover_lost_pack` 후보를 밀어준다.
- `lost_pack_under_roots_hint`: `recover_lost_pack`, `return_with_porter_report` 후보를 밀어준다.

각 Event(이벤트)는 `storylet_tags`, `card_candidate_hints`, `cooldown_tags`, `repeat_group`을 가진다.

## 6. Scenario Fixture

추가 Scenario(시나리오):

- success: `data/scenarios/missing_porter_search_intro.yaml`
- partial_success: `data/scenarios/missing_porter_search_intro_partial.yaml`
- failure: `data/scenarios/missing_porter_search_intro_failure.yaml`

## 7. 실행 결과

Success run(성공 실행):

- result_type: `success`
- selected cards: `track_porter_footprints` -> `rescue_injured_porter` -> `return_with_porter_report`
- completed objectives: `find_porter_trace`, `resolve_porter_fate`, `return_to_village`
- failed objectives: 없음
- score: 221

Partial success run(부분 성공 실행):

- result_type: `partial_success`
- selected cards: `track_porter_footprints` -> `rescue_injured_porter`
- completed objectives: `find_porter_trace`, `resolve_porter_fate`
- failed objectives: `return_to_village`
- partial reasons: `report_failed`, `optional_failed`, `return_late`, `reduced_reward`
- score: 129

Failure run(실패 실행):

- result_type: `failure`
- selected cards: 없음
- failed objectives: `find_porter_trace`, `resolve_porter_fate`, `return_to_village`, `survive_expedition`
- failure reasons: `return_failed`, `health_zero`, `primary_objective_failed`
- score: -120

## 8. 회귀 검증

`tests/test_gameplay_p0_missing_porter_search.py`에서 다음을 확인했다.

- `missing_porter_search_intro`의 success / partial_success / failure(성공 / 부분 성공 / 실패) 결과.
- Storylet/Event Hint(스토리 조각/이벤트 힌트)가 새 카드 후보를 노출하는지.
- JSON/Text MUD Log(JSON/텍스트 MUD 로그)에 카드 후보, 선택 카드, Quest Report(퀘스트 보고서)가 기록되는지.
- `herb_gathering_tutorial`과 `forest_path_scouting_tutorial`에 missing porter 전용 카드가 섞이지 않는지.

## 9. Evidence

Evidence(증거) 경로:

- `.omo/ulw-loop/evidence/missing-porter-search-20260630/success/`
- `.omo/ulw-loop/evidence/missing-porter-search-20260630/partial/`
- `.omo/ulw-loop/evidence/missing-porter-search-20260630/failure/`
- `.omo/ulw-loop/evidence/missing-porter-search-20260630/herb-regression/`
- `.omo/ulw-loop/evidence/missing-porter-search-20260630/forest-regression/`

## 10. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_missing_porter_search
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/missing_porter_search_intro.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/missing_porter_search_intro_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/missing_porter_search_intro_failure.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py tests/test_gameplay_p0_missing_porter_search.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/missing_porter_search_intro.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/missing-porter-search-20260630/success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/missing_porter_search_intro_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/missing-porter-search-20260630/partial --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/missing_porter_search_intro_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/missing-porter-search-20260630/failure --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/missing-porter-search-20260630/herb-regression --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/missing-porter-search-20260630/forest-regression --profile balanced
```

## 11. 남은 문제

- Quest(퀘스트) 10개 대량 확장은 하지 않았다.
- Storylet Pool(스토리 조각 풀) 전체 시스템은 구현하지 않았다.
- Repeat Cooldown Memory(반복 쿨다운 기억) 장기 저장은 구현하지 않았다.
- Failure(실패) 시나리오는 health_zero(체력 0) 기반이라 turn(턴) 없이 Quest Report(퀘스트 보고서)를 검증한다.

## 12. 다음 추천 작업

1. `merchant_lost_pack_recovery` Quest(퀘스트)를 1개만 추가한다.
2. Money / Reputation / Recovery(돈 / 평판 / 회수) 경로를 기존 evaluator(평가기)로 검증한다.
3. 기존 세 Quest(퀘스트)의 3-Card 후보 격리와 success / partial_success / failure(성공 / 부분 성공 / 실패) 회귀 검증을 계속 유지한다.
