# [Current] Gameplay P0 Seeded Tier Variety Result v0.1

> 상태: [Current] Gameplay P0 Card Candidate Pool에 seed 기반 tier variety를 도입한 결과 문서.

## 1. 작업 목적

Gameplay P0의 Card Candidate Pool(카드 후보 풀)이 Tier(등급)와 Weight(가중치)를 유지하면서도, 같은 Tier(등급) 안에서 Seeded Variety(시드 기반 다양성)를 제공하도록 했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/07_reviews/23_Gameplay_P0_Card_Candidate_Tier_Weight_Result_v0.1.md`
- `data/core/card_rules.yaml`

## 3. 변경 파일

- `src/fateweaver/gameplay_p0_card_selection.py`
- `src/fateweaver/gameplay_p0_cards.py`
- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_models.py`
- `tests/test_gameplay_p0_card_candidates.py`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/00_index/README_Docs_Index.md`
- `docs/07_reviews/24_Gameplay_P0_Seeded_Tier_Variety_Result_v0.1.md`

## 4. Seeded Variety 정책

Selection Seed Key(선택 시드 키)는 다음 요소를 포함한다.

- `scenario_id`
- `seed`
- `run_number`
- `day`
- `turn`
- `slot_role`
- `current_region`
- `active_quest_id`

같은 Selection Seed Key(선택 시드 키)는 같은 3-Card 결과를 재현한다. 다른 seed에서는 같은 Tier(등급)와 가까운 Score(점수)의 후보 중 다른 카드가 선택될 수 있다.

## 5. Tier별 선택 방식

slot별 후보를 Tier(등급), Score(점수), card id 기준으로 정렬한다.

- `critical`: 최우선 후보로 유지한다. 여러 critical 후보가 같은 slot에 있으면 seed 기반 Weighted Pick(가중 선택)을 한다.
- `strong`: 같은 Tier(등급)의 상위 Variety Window(다양성 창) 안에서 seed 기반 Weighted Pick(가중 선택)을 한다.
- `normal`: strong 후보가 없는 slot에서 같은 방식으로 선택한다.
- `flavor`: 상위 후보가 flavor일 때 fallback으로만 선택된다.
- `blocked`: Variety Window(다양성 창)에서 제외된다.

P0 기준값:

- `variety_window_size: 3`
- `score_tolerance: 10`

## 6. 최근 반복 방지

기존 `recent_repeat_penalty`를 유지했다. 최근 선택 이력에 있는 카드는 Score(점수)에 패널티를 받으며, JSON Evidence(JSON 증거)에 `repeat_penalty`가 남는다.

completed optional objective 카드인 `help_injured_traveler`는 `completed_objective`로 blocked 처리되어 3-Card에 다시 나오지 않는다.

## 7. 같은 seed 재현성 검증

Unit Test(단위 테스트)에서 같은 Candidate Pool(카드 후보 풀), 같은 CardSelectionContext(카드 선택 컨텍스트), 같은 seed를 두 번 적용해 같은 3-Card 결과가 나오는 것을 확인했다.

## 8. 다른 seed 다양성 검증

동일 조건에서 seed별 샘플 결과:

- seed 42: `search_herbs`, `inspect_tracks`, `conserve_food`
- seed 43: `search_herbs`, `inspect_tracks`, `use_torch_to_search`
- seed 99: `search_herbs`, `enter_deep_woods`, `conserve_food`

slot role은 `quest_progress`, `risk_discovery`, `resource_alternative` 순서를 유지한다.

## 9. JSON Evidence 변경

`card_candidate_pool`의 각 후보에 다음 필드를 추가했다.

- `selection_seed_key`
- `variety_window`
- `selected_by`
- `repeat_penalty`

선택된 후보는 `selected_by: seeded_tier_pick`으로 남고, Variety Window(다양성 창)에 있었지만 선택되지 않은 후보는 `selected_by: seeded_tier_window`로 남는다.

## 10. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_card_candidates
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_card_candidates tests.test_gameplay_p0_optional_action_score
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py src/fateweaver/gameplay_p0.py src/fateweaver/gameplay_p0_cards.py src/fateweaver/gameplay_p0_card_selection.py src/fateweaver/gameplay_p0_errors.py src/fateweaver/gameplay_p0_models.py src/fateweaver/gameplay_p0_rules.py tests/test_gameplay_p0_card_candidates.py
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/seeded-tier-variety-verified-20260630/same-seed-a --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/seeded-tier-variety-verified-20260630/same-seed-b --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 43 --runs 1 --logs .omo/ulw-loop/evidence/seeded-tier-variety-verified-20260630/different-seed --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/seeded-tier-variety-verified-20260630/optional-completed --profile curious_leaning
```

## 11. 남은 문제

- Storylet(스토리 조각)이 직접 card candidate hints를 제공하는 구조는 아직 없다.
- Repeat Memory(반복 기억)는 P0의 선택 이력 기반 패널티이며, 장기 cooldown 시스템은 아니다.

## 12. 다음 추천 작업

1. Storylet(스토리 조각) 데이터에 직접 card candidate hints를 연결한다.
2. Candidate Score Breakdown(후보 점수 분해)을 JSON Evidence(JSON 증거)에 더 세분화한다.
3. Repeat Memory(반복 기억)를 최근 2~3 turn 단위로 구조화한다.
