# [Current] Gameplay P0 Storylet Hints and Repeat Cooldown Result v0.1

> 상태: [Current] Gameplay P0에 Storylet/Event card candidate hints와 repeat cooldown memory를 도입한 결과 문서.

## 1. 작업 목적

Quest(퀘스트) 추가 전에 문서 기준을 정리하고, Storylet/Event(스토리 조각/이벤트)가 Card Candidate Pool(카드 후보 풀)에 직접 hint(힌트)를 줄 수 있는 최소 구조를 도입했다.

또한 Repeat Cooldown Memory(반복 쿨다운 기억)를 P0 수준으로 추가해 같은 card/storylet/tag/repeat group 반복을 점수 패널티로 줄이도록 했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/07_reviews/23_Gameplay_P0_Card_Candidate_Tier_Weight_Result_v0.1.md`
- `docs/07_reviews/24_Gameplay_P0_Seeded_Tier_Variety_Result_v0.1.md`
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`
- `data/core/card_rules.yaml`
- `data/core/ontology.yaml`
- `data/content/base/events.yaml`
- `data/content/base/quests.yaml`

## 3. 변경 파일

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/26_Gameplay_P0_Storylet_Hints_Repeat_Cooldown_Result_v0.1.md`
- `data/content/base/events.yaml`
- `data/scenarios/tutorial_herb_quest.yaml`
- `data/core/card_rules.yaml`
- `src/fateweaver/models.py`
- `src/fateweaver/data_loader.py`
- `src/fateweaver/gameplay_run.py`
- `src/fateweaver/card_candidates.py`
- `src/fateweaver/gameplay_models.py`
- `src/fateweaver/gameplay_rules.py`
- `tests/test_gameplay_run_card_candidates.py`
- `tests/test_gameplay_run_storylet_cooldown.py`
- `tests/test_validator.py`

## 4. Quest 문서 정리

`docs/00_index/README_Docs_Index.md`에서 다음 문서 역할을 정렬했다.

- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`: Quest(퀘스트) 제작 기준 문서.
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`: FateWeaver 제작 양식으로 재가공한 Quest(퀘스트) 후보 리서치 자료.

## 5. Quest Expansion Roadmap

`docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`를 추가했다.

우선순위:

1. `forest_path_scouting_tutorial`
2. `missing_porter_search_intro`
3. `merchant_lost_pack_recovery`
4. `ruin_mark_investigation_intro`
5. `village_well_trouble`

`forest_path_scouting_tutorial`은 설계 초안으로만 문서화했다. 이번 작업에서는 실제 Quest(퀘스트)를 `data/`에 추가하지 않았다.

## 6. Storylet/Event Hint 구조

Event(이벤트)에 다음 필드를 추가했다.

- `storylet_tags`
- `card_candidate_hints`
- `cooldown_tags`
- `repeat_group`

P0 검증용으로 `forest_injured_traveler_hint` Event(이벤트)를 추가했다.

기본 tutorial scenario(튜토리얼 시나리오)에는 이 Event(이벤트)를 include list(포함 목록)에 추가했다. Quest(퀘스트)는 추가하지 않았다.

## 7. Card Candidate Context 변경

`CardCandidateContext(카드 후보 컨텍스트)`가 다음을 포함한다.

- `storylet_id`
- `storylet_tags`
- `card_candidate_hints`
- `cooldown_tags`
- `repeat_group`

P0 run은 Event(이벤트)에서 이 값을 읽어 Candidate Score(후보 점수)와 JSON Evidence(JSON 증거)에 반영한다.

## 8. Hint Score Bonus

`card_candidate_hints`에 명시된 card id는 `storylet_hint_bonus: +25`를 받는다.

다만 hint(힌트)는 candidate score만 올린다. `requires_*`, `completed_objective`, `blocked` 조건은 우회하지 않는다.

## 9. Repeat Cooldown Memory

`RepeatMemory(반복 기억)`는 run 내부에서 다음을 유지한다.

- recent presented cards
- recent selected cards
- recent storylets
- cooldown tags
- repeat groups

P0 cooldown은 2턴 기준이다.

## 10. Cooldown Penalty

Candidate Score(후보 점수)에 다음 penalty(패널티)를 적용한다.

- 같은 card recent penalty: 기존 `recent_repeat_penalty`
- 같은 repeat group: `repeat_group_penalty: -30`
- 같은 cooldown tag: `cooldown_tag_penalty: -15`

Cooldown(쿨다운)은 hard block(강제 차단)이 아니라 score penalty(점수 패널티)다.

## 11. JSON Evidence 변경

Turn log에 다음 필드를 추가했다.

- `storylet_id`
- `card_candidate_hints`
- `cooldown_tags`
- `repeat_group`
- `repeat_memory_snapshot`
- `repeat_memory_after`

Card candidate pool(카드 후보 풀) 항목에는 다음 필드를 추가했다.

- `matched_storylet_hints`
- `cooldown_penalty`

## 12. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_card_candidates
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_card_candidates tests.test_gameplay_run_storylet_cooldown tests.test_gameplay_run_optional_action_score tests.test_event_selector
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py src/fateweaver/models.py src/fateweaver/data_loader.py src/fateweaver/gameplay_run.py src/fateweaver/card_candidates.py src/fateweaver/gameplay_models.py src/fateweaver/gameplay_rules.py tests/test_validator.py tests/test_gameplay_run_card_candidates.py tests/test_gameplay_run_storylet_cooldown.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/storylet-hints-cooldown-20260630/same-seed-a2 --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/storylet-hints-cooldown-20260630/same-seed-b2 --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 43 --runs 1 --logs .omo/ulw-loop/evidence/storylet-hints-cooldown-20260630/different-seed2 --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 1 --runs 1 --logs .omo/ulw-loop/evidence/storylet-hints-cooldown-20260630/storylet-selected-cooldown --profile curious_leaning
```

## 13. 검증 결과

- Unit Test(단위 테스트): 58개 통과.
- Scenario Validation(시나리오 검증): 7개 tutorial herb quest scenario(튜토리얼 약초 퀘스트 시나리오) 통과.
- Compile/Diff/Hook(컴파일/차이/검사 도구): 통과.
- 같은 seed(시드): `same-seed-a2`와 `same-seed-b2`의 3-Card 후보 순서가 동일했다.
- 다른 seed(시드): `different-seed2`의 Event(이벤트) 및 3-Card 후보 순서가 달랐다.
- Storylet Hint(스토리 조각 힌트): `forest_injured_traveler_hint` turn(턴)에서 `card_candidate_hints: [help_injured_traveler]`가 JSON에 기록됐다.
- Blocked 유지: 같은 turn(턴)에서 `help_injured_traveler`는 hint(힌트)를 받았지만 requirement(요구조건) 미충족 시 `blocked` 후보로 남았다.
- Repeat Cooldown Memory(반복 쿨다운 기억): `storylet-selected-cooldown` 로그에서 `help_injured_traveler` 선택 후 `cooldown_tags`와 `repeat_groups` counter(카운터)가 `repeat_memory_after`에 기록됐다.

## 14. 남은 문제

- Storylet Pool(스토리 조각 풀) 전체 구현은 아직 아니다.
- Repeat Cooldown Memory(반복 쿨다운 기억)는 P0 run 내부 메모리이며 저장/장기 기억은 아니다.
- `forest_path_scouting_tutorial` 실제 Quest(퀘스트)는 아직 구현하지 않았다.

## 15. 다음 추천 작업

1. `forest_path_scouting_tutorial` Quest(퀘스트)를 data fixture(데이터 픽스처)로 1개만 추가한다.
2. success / partial_success / failure scenario(성공 / 부분 성공 / 실패 시나리오)를 함께 만든다.
3. Storylet/Event card candidate hints(스토리 조각/이벤트 카드 후보 힌트)가 새 Quest(퀘스트)에서도 충분히 작동하는지 검증한다.
