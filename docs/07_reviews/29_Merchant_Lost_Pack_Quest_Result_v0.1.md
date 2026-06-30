# [Current] Merchant Lost Pack Quest Result v0.1

> 상태: [Current] `merchant_lost_pack_recovery` Quest를 실제 data fixture로 추가하고 economy / reputation / recovery / negotiation 경로를 검증한 결과 문서.

## 1. 작업 목적

`missing_porter_search_intro` 다음 Quest(퀘스트)로 `merchant_lost_pack_recovery` 1개만 실제 data fixture(데이터 고정물)로 추가했다.

범위는 Quest(퀘스트) 1개, Quest 전용 Card Rule(카드 규칙), 최소 Storylet/Event Hint(스토리 조각/이벤트 힌트), success / partial_success / failure scenario(성공 / 부분 성공 / 실패 시나리오) 검증으로 제한했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`
- `docs/07_reviews/26_Gameplay_P0_Storylet_Hints_Repeat_Cooldown_Result_v0.1.md`
- `docs/07_reviews/27_Forest_Path_Scouting_Quest_Result_v0.1.md`
- `docs/07_reviews/28_Missing_Porter_Search_Quest_Result_v0.1.md`
- `data/content/base/quests.yaml`
- `data/content/base/events.yaml`
- `data/core/card_rules.yaml`
- `data/core/score_rules.yaml`
- `data/core/ontology.yaml`

## 3. 변경 파일

- `data/content/base/quests.yaml`
- `data/content/base/events.yaml`
- `data/core/card_rules.yaml`
- `data/scenarios/merchant_lost_pack_recovery.yaml`
- `data/scenarios/merchant_lost_pack_recovery_partial.yaml`
- `data/scenarios/merchant_lost_pack_recovery_failure.yaml`
- `tests/test_gameplay_p0_merchant_lost_pack.py`
- `docs/00_index/README_Docs_Index.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/29_Merchant_Lost_Pack_Quest_Result_v0.1.md`

## 4. Quest 데이터

추가 Quest(퀘스트):

- id: `merchant_lost_pack_recovery`
- title: `상인의 잃어버린 짐`
- type: `recovery`
- start region(시작 지역): `village`
- target regions(대상 지역): `forest`
- max days(최대 일수): 5
- max turns(최대 턴): 10

Objectives(목표):

- `locate_lost_pack`: `discover_clue`, required(필수), target `lost_pack_location`
- `resolve_pack_ownership`: `optional_action`, required(필수), progress key `pack_ownership_resolved`
- `return_to_village`: `return_to_region`, required(필수), progress key `pack_returned_to_village`
- `survive_expedition`: `survive_expedition`, required(필수)
- `negotiate_bonus_payment`: `optional_action`, optional(선택)
- `preserve_merchant_trust`: `keep_resource_at_least`, optional(선택), target `reputation`

Rewards(보상):

- money: 3
- reputation: 1
- score: 40
- unlock_quests: `caravan_to_border_fort`

## 5. Card Rule 추가

추가 Card Rule(카드 규칙):

- `question_merchant_about_pack`: money(돈)를 써서 상인의 짐 정보와 보상 조건을 확인.
- `inspect_lost_pack_tracks`: `lost_pack_location` clue(단서) 발견 및 forest(숲) 이동.
- `follow_bandit_scuff_marks`: 도적 흔적 조사, health(체력) 비용과 omen(징조) 제공.
- `recover_lost_merchant_pack`: 잃어버린 상단 짐 회수.
- `return_pack_honestly`: `pack_ownership_resolved`와 `pack_returned_to_village` 완료, reputation(평판) 상승.
- `negotiate_bonus_payment`: `bonus_payment_negotiated` optional_action(선택 행동) 완료, money(돈) 증가.
- `hide_valuable_trinket`: money(돈)는 늘지만 reputation(평판)이 내려가고 ownership(소유권 해결)은 실패하는 partial_success(부분 성공) 경로.

`honest_return_plus_bonus` combo(조합)를 추가해 `return_pack_honestly`와 `negotiate_bonus_payment`가 함께 제시되면 둘을 동시에 선택한다.

새 카드는 모두 `quest_ids: [merchant_lost_pack_recovery]`를 가진다. 따라서 active Quest(활성 퀘스트)가 다르면 3-Card 후보에 포함되지 않는다.

## 6. Storylet/Event Hint 추가

추가 Event Hint(이벤트 힌트):

- `merchant_missing_pack_hint`: `question_merchant_about_pack`, `inspect_lost_pack_tracks`, `negotiate_bonus_payment` 후보를 밀어준다.
- `road_scuff_marks_hint`: `inspect_lost_pack_tracks`, `follow_bandit_scuff_marks` 후보를 밀어준다.
- `bandit_cache_near_roots_hint`: `follow_bandit_scuff_marks`, `recover_lost_merchant_pack`, `hide_valuable_trinket` 후보를 밀어준다.
- `merchant_reward_dispute_hint`: `return_pack_honestly`, `negotiate_bonus_payment`, `hide_valuable_trinket` 후보를 밀어준다.

각 Event(이벤트)는 `storylet_tags`, `card_candidate_hints`, `cooldown_tags`, `repeat_group`을 가진다.

## 7. Scenario Fixture

추가 Scenario(시나리오):

- success: `data/scenarios/merchant_lost_pack_recovery.yaml`
- partial_success: `data/scenarios/merchant_lost_pack_recovery_partial.yaml`
- failure: `data/scenarios/merchant_lost_pack_recovery_failure.yaml`

## 8. Success 검증

`merchant_lost_pack_recovery.yaml` 실행 결과:

- result_type: `success`
- selected cards: `inspect_lost_pack_tracks` -> `recover_lost_merchant_pack` -> `return_pack_honestly` + `negotiate_bonus_payment`
- completed objectives: `locate_lost_pack`, `resolve_pack_ownership`, `return_to_village`
- failed objectives: 없음
- money: 7
- reputation: 2
- score: 247

## 9. Partial Success 검증

`merchant_lost_pack_recovery_partial.yaml` 실행 결과:

- result_type: `partial_success`
- selected cards: `inspect_lost_pack_tracks` -> `recover_lost_merchant_pack` -> `hide_valuable_trinket`
- completed objectives: `locate_lost_pack`, `return_to_village`
- failed objectives: `resolve_pack_ownership`
- money: 4
- reputation: -1
- score: 91

## 10. Failure 검증

`merchant_lost_pack_recovery_failure.yaml` 실행 결과:

- result_type: `failure`
- selected cards: 없음
- failed objectives: `locate_lost_pack`, `resolve_pack_ownership`, `return_to_village`, `survive_expedition`
- failure reasons: `return_failed`, `health_zero`, `primary_objective_failed`
- score: -120

## 11. Economy / Reputation 검증

Success run(성공 실행)은 정직한 반환과 협상으로 money(돈)가 7, reputation(평판)이 2가 됐다.

Partial run(부분 성공 실행)은 장신구를 숨겨 money(돈)는 4로 남았지만 reputation(평판)이 -1로 떨어졌고, `preserve_merchant_trust` optional objective(선택 목표)가 failed(실패)로 기록됐다.

`score_breakdown`에는 `resource_management`, `reputation`, `penalty`가 반영됐다.

## 12. Storylet Hint / Repeat Cooldown 검증

Success run(성공 실행)에서 확인한 내용:

- `merchant_missing_pack_hint`가 `inspect_lost_pack_tracks`를 hint(힌트)로 제공했다.
- `merchant_reward_dispute_hint`가 `return_pack_honestly`와 `negotiate_bonus_payment`를 hint(힌트)로 제공했다.
- JSON log(JSON 로그)에 `repeat_memory_snapshot`, `repeat_memory_after`, `cooldown_tags`, `repeat_group`이 기록됐다.

## 13. JSON / Text MUD Log 검증

Evidence(증거) 경로:

- `.omo/ulw-loop/evidence/merchant-lost-pack-20260630/success/`
- `.omo/ulw-loop/evidence/merchant-lost-pack-20260630/partial/`
- `.omo/ulw-loop/evidence/merchant-lost-pack-20260630/failure/`
- `.omo/ulw-loop/evidence/merchant-lost-pack-20260630/herb-regression/`
- `.omo/ulw-loop/evidence/merchant-lost-pack-20260630/forest-regression/`
- `.omo/ulw-loop/evidence/merchant-lost-pack-20260630/porter-regression/`

JSON log(JSON 로그)에서 확인:

- `quest_id = merchant_lost_pack_recovery`
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

Text MUD log(텍스트 MUD 로그)에서 카드 3장, 선택 카드, money/reputation(돈/평판) 변화, Quest Report(퀘스트 보고서), result_type(결과 유형)을 확인했다.

## 14. 기존 Herb / Forest / Porter 회귀 검증

기존 주요 success scenario(성공 시나리오)는 계속 `success`를 반환했다.

- `tutorial_herb_quest.yaml`: score 217
- `forest_path_scouting_tutorial.yaml`: score 170
- `missing_porter_search_intro.yaml`: score 221

`tests/test_gameplay_p0_merchant_lost_pack.py`에서 merchant lost pack 전용 카드가 기존 Quest(퀘스트)의 presented/selected cards(제시/선택 카드)에 섞이지 않는 것을 확인했다.

## 15. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_merchant_lost_pack
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_failure.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py tests/test_gameplay_p0_merchant_lost_pack.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/merchant-lost-pack-20260630/success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/merchant-lost-pack-20260630/partial --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/merchant-lost-pack-20260630/failure --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/merchant-lost-pack-20260630/herb-regression --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/merchant-lost-pack-20260630/forest-regression --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/missing_porter_search_intro.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/merchant-lost-pack-20260630/porter-regression --profile balanced
```

## 16. 남은 문제

- Quest(퀘스트) 10개 대량 확장은 하지 않았다.
- Storylet Pool(스토리 조각 풀) 전체 시스템은 구현하지 않았다.
- Repeat Cooldown Memory(반복 쿨다운 기억) 장기 저장은 구현하지 않았다.
- 상점/거래 UI(사용자 인터페이스)는 구현하지 않았다.
- Failure(실패) 시나리오는 health_zero(체력 0) 기반이라 turn(턴) 없이 Quest Report(퀘스트 보고서)를 검증한다.

## 17. 다음 추천 작업

1. `ruin_mark_investigation_intro` Quest(퀘스트)를 1개만 추가한다.
2. Clue / Omen / Ruin(단서 / 징조 / 폐허) 경로를 기존 evaluator(평가기)로 검증한다.
3. 기존 네 Quest(퀘스트)의 3-Card 후보 격리와 success / partial_success / failure(성공 / 부분 성공 / 실패) 회귀 검증을 계속 유지한다.
