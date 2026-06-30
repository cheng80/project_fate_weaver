# [Current] Gameplay P0 Card Candidate Tier Weight Result v0.1

> 상태: [Current] Gameplay P0 Card Candidate Pool에 tier / weight 기반 후보 선택 구조를 도입한 결과 문서.

## 1. 작업 목적

3-Card Choice가 slot 고정 선택에 머물지 않도록, Card Rule 후보를 수집한 뒤 context tag, quest objective, region, availability, 반복, objective 완료 여부를 점수화하고 tier로 분류해 최종 3장을 고르게 했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/22_Gameplay_P0_Optional_Action_Ontology_Link_Result_v0.1.md`
- `data/core/card_rules.yaml`
- `data/core/ontology.yaml`
- `data/content/base/quests.yaml`

## 3. 변경 파일

- `data/core/card_rules.yaml`
- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_cards.py`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/gameplay_p0_models.py`
- `tests/test_gameplay_p0_card_candidates.py`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/00_index/README_Docs_Index.md`
- `docs/07_reviews/23_Gameplay_P0_Card_Candidate_Tier_Weight_Result_v0.1.md`

## 4. Card Rule 변경

`data/core/card_rules.yaml`의 P0 card에 `base_weight`와 `tier_hint`를 추가했다.

`help_injured_traveler`에는 다음 `weight_modifiers`를 명시했다.

- `quest_objective_match: 30`
- `storylet_tag_match: 20`
- `region_match: 10`
- `slot_role_bonus: 5`
- `already_completed: -999`
- `unavailable: -999`
- `recent_repeat_penalty: -25`
- `low_food_penalty: -10`

## 5. Candidate Score 계산 방식

`build_card_candidate_pool`이 모든 Card Rule을 `CardCandidate`로 변환한다.

점수는 다음 요소를 반영한다.

- `base_weight`
- active quest optional objective match
- storylet/context tag match
- region match
- slot role bonus
- recent repeat penalty
- low food penalty
- completed objective penalty
- unavailable requirement penalty

예: optional completed run의 turn 3에서 `help_injured_traveler`는 storylet tags와 objective가 모두 맞아 `score: 70`, `tier: strong`으로 3-Card에 포함됐다.

## 6. Tier 분류 방식

runtime tier 기준:

- `critical`: 90 이상
- `strong`: 70 이상 90 미만
- `normal`: 40 이상 70 미만
- `flavor`: 0 이상 40 미만
- `blocked`: 0 미만 또는 unavailable/completed objective

`report_to_apothecary`처럼 현재 region/progress에서 불가능한 카드는 `blocked_reason: unavailable_requirement`로 남는다.

## 7. 3-Card 선택 방식

최종 3장은 candidate pool에서 tier/score/id 정렬을 거친 뒤 slot balance를 유지해 뽑는다.

- `quest_progress` 1장
- `risk_discovery` 1장
- `resource_alternative` 1장

blocked 후보는 제외된다. 이 구조로 같은 slot이 3장 나오는 일을 막고, slot 안에서는 높은 score/tier 후보가 선택된다.

## 8. optional_action 유지 검증

`help_injured_traveler`는 조건 충족 시 `resource_alternative` 슬롯에 포함된다.

optional completed run:

- turn 3 `presented_cards`: `search_herbs`, `inspect_tracks`, `help_injured_traveler`
- turn 3 `selected_cards`: `help_injured_traveler`
- `quest_progress.helped_injured_traveler = 1`
- Quest Report: `help_injured_traveler` completed, `score_delta = 10`

optional failed run:

- `help_injured_traveler` selected 없음
- Quest Report: `help_injured_traveler` failed, `score_delta = 0`

## 9. JSON / Text MUD Log 변경

JSON turn log에 `card_candidate_pool`을 추가했다.

각 후보는 다음을 포함한다.

- `card_id`
- `slot_role`
- `score`
- `tier`
- `matched_tags`
- `matched_objectives`
- `blocked_reason`

Text MUD는 사용자용 3장 카드 표시를 유지한다. 전체 candidate pool은 JSON/evidence에서 확인한다.

로그 위치:

- `.omo/ulw-loop/evidence/card-tier-weight-20260630/success/`
- `.omo/ulw-loop/evidence/card-tier-weight-20260630/partial/`
- `.omo/ulw-loop/evidence/card-tier-weight-20260630/failure/`
- `.omo/ulw-loop/evidence/card-tier-weight-20260630/optional-completed/`
- `.omo/ulw-loop/evidence/card-tier-weight-20260630/optional-failed/`

## 10. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_card_candidates
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_card_candidates tests.test_gameplay_p0_optional_action_score
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
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/card-tier-weight-20260630/success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/card-tier-weight-20260630/partial --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/card-tier-weight-20260630/failure --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/card-tier-weight-20260630/optional-completed --profile curious_leaning
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/card-tier-weight-20260630/optional-failed --profile balanced
```

## 11. 남은 문제

- P0 selection은 slot별 best candidate를 deterministic하게 고른다. 같은 tier 안의 seeded variety는 아직 없다.
- Storylet 데이터가 직접 `base_cards` 또는 candidate hints를 공급하는 구조는 아직 후속 작업이다.

## 12. 다음 추천 작업

1. 같은 tier 안에서 seed 기반 deterministic variety를 추가한다.
2. Storylet/Event 데이터에 card candidate hints를 붙인다.
3. Candidate score breakdown을 더 세분화해 balance tuning evidence로 쓴다.
