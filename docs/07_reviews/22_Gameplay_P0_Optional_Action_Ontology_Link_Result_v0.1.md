# [Current] Gameplay P0 Optional Action Ontology Link Result v0.1

> 상태: [Current] Gameplay P0 optional_action 카드를 Storylet/Ontology 후보군과 연결한 결과 문서.

## 1. 작업 목적

`help_injured_traveler` optional_action 카드가 fixture 전용 카드로만 남지 않도록, active quest의 optional objective와 P0 situation/storylet tag를 통해 3-Card 후보에 포함되게 연결했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/21_Gameplay_P0_Optional_Action_And_Score_Rule_Result_v0.1.md`
- `data/core/ontology.yaml`
- `data/core/card_rules.yaml`
- `data/content/base/quests.yaml`

## 3. 변경 파일

- `data/core/card_rules.yaml`
- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_cards.py`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/gameplay_p0_models.py`
- `src/fateweaver/gameplay_p0_rules.py`
- `src/fateweaver/text_mud_log.py`
- `tests/test_gameplay_p0_optional_action_score.py`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/00_index/README_Docs_Index.md`
- `docs/07_reviews/22_Gameplay_P0_Optional_Action_Ontology_Link_Result_v0.1.md`

## 4. optional_action 후보 생성 구조

P0 runtime이 매 turn `CardCandidateContext`를 만든다. 이 context는 active quest와 현재 event/region/danger/next-event/P0 situation tag를 담는다.

`present_cards`는 visible card 중 `resource_alternative` 슬롯을 고를 때 다음을 확인한다.

- 카드의 `applies_to_storylet_tags`가 현재 context tag와 겹친다.
- 카드의 `applies_to_quest_objectives`가 active quest optional objective id와 겹친다.
- 카드의 `progress_key`가 아직 완료되지 않았다.

조건이 맞으면 `help_injured_traveler`가 3장 카드 중 resource alternative 슬롯에 들어간다. 완료 후에는 일반 resource alternative 카드로 fallback되어 반복 노출되지 않는다.

## 5. Card Rule 변경

`help_injured_traveler`에 다음 metadata를 추가했다.

- `slot_role: resource_alternative`
- `tags: [aid, npc, optional_objective, reputation, forest, quest_related]`
- `applies_to_storylet_tags: [injured_traveler, aid_opportunity]`
- `applies_to_quest_objectives: [help_injured_traveler]`
- `progress_key: helped_injured_traveler`

결과에는 `food: -1`, `reputation: 1`, `quest_progress.helped_injured_traveler: 1`이 반영된다.

## 6. Storylet/Context Tag 연결

대규모 Storylet 시스템은 만들지 않았다. P0 situation rule로 forest에서 `herbs_collected >= 2`이면 다음 context tag를 붙인다.

- `npc`
- `aid_opportunity`
- `injured_traveler`
- `quest_related`

이 tag가 card rule metadata와 매칭되어 optional action 후보가 된다.

## 7. 3-Card 노출 검증

completed simulator run의 turn 3에서 다음이 확인됐다.

- `storylet_tags`: `injured_traveler`, `aid_opportunity`, `quest_related` 포함
- `presented_cards`: `search_herbs`, `inspect_tracks`, `help_injured_traveler`
- `selected_cards`: `help_injured_traveler`

## 8. Quest Progress / Objective Result 검증

completed run에서 turn 3 선택 후 `quest_progress.helped_injured_traveler = 1`이 기록됐다.

Quest Report의 `help_injured_traveler` objective는 다음으로 평가됐다.

- `objective_type`: `optional_action`
- `status`: `completed`
- `score_delta`: `10`

failed fixture에서는 `help_injured_traveler`가 선택되지 않았고 objective status가 `failed`로 유지됐다.

## 9. Score Rule 검증

`score_rules.yaml`의 `objective_scoring.completed_optional` 값이 `help_injured_traveler.score_delta = 10`으로 반영됐다.

completed run의 `score_breakdown.objective_completion`은 `110`, failed run은 `35`로 확인됐다.

## 10. JSON / Text MUD Log 검증

JSON completed log에는 `presented_cards`, `selected_cards`, `storylet_tags`, `quest_progress`, `objective_results`, `score_breakdown`이 모두 기대대로 남았다.

Text MUD completed log에는 다음이 표시됐다.

- 카드: `부상자를 돕는다`
- 선택: `부상자를 돕는다`
- 상태 변화: `food: 4 -> 3`, `reputation: 1 -> 2`
- 목표 평가: `help_injured_traveler: 성공`

로그 위치:

- `.omo/ulw-loop/evidence/optional-ontology-link-20260630/logs-completed/`
- `.omo/ulw-loop/evidence/optional-ontology-link-20260630/logs-failed/`

## 11. 실행한 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_optional_action_score
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/optional-ontology-link-20260630/logs-completed --profile curious_leaning
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/optional-ontology-link-20260630/logs-failed --profile balanced
```

## 12. 남은 문제

- P0 situation tag rule은 아직 최소 구현이다. 실제 Storylet Pool이 커지면 `injured_traveler` 같은 tag는 event/storylet 데이터에서 직접 공급되는 편이 좋다.
- Card Candidate ranking은 아직 deterministic slot selection이다. 후보 pool이 커지면 tier/weight 기반 ranking이 필요하다.

## 13. 다음 추천 작업

1. Quest/objective fixture matrix를 만들어 objective type별 completed/partial/failed를 고정한다.
2. Card Candidate Pool을 slot별 first-match에서 tier/weight ranking으로 확장한다.
3. Storylet 데이터에 `base_cards` 또는 equivalent card candidate hints를 추가한다.
