# [Current] Gameplay P0 Optional Action and Score Rule Result v0.1

> 상태: [Current] Gameplay P0의 optional_action completed 경로와 score rule 정렬 결과 문서.

## 1. 작업 목적

Gameplay P0에서 `optional_action` objective가 failed 경로만 검증되던 상태를 보강했다.

이번 작업은 대량 콘텐츠 확장이 아니라, 기존 `herb_gathering_tutorial` 수직 슬라이스 안에서 선택 카드 결과가 optional objective progress를 실제로 갱신하고, objective score가 `data/core/score_rules.yaml`의 `objective_scoring` 규칙을 사용하도록 정렬하는 작업이다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/19_Gameplay_P0_Objective_Schema_Normalization_Result_v0.1.md`
- `docs/07_reviews/20_Gameplay_P0_Objective_Schema_Doc_And_Fixture_Result_v0.1.md`
- `data/core/score_rules.yaml`
- `data/content/base/quests.yaml`
- `data/core/card_rules.yaml`

## 3. 변경 파일

데이터:

- `data/content/base/quests.yaml`
- `data/core/card_rules.yaml`
- `data/core/score_rules.yaml`
- `data/scenarios/tutorial_herb_quest_optional_completed.yaml`

코드:

- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_objectives.py`
- `src/fateweaver/gameplay_p0_rules.py`
- `src/fateweaver/gameplay_p0_scoring.py`

테스트:

- `tests/test_gameplay_p0_optional_action_score.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/21_Gameplay_P0_Optional_Action_And_Score_Rule_Result_v0.1.md`

## 4. optional_action completed 구현

`data/core/card_rules.yaml`에 `help_injured_traveler` 카드를 추가했다.

- slot_role: `risk_discovery`
- regions: `forest`
- requires_progress: `herbs_collected >= 2`
- result quest_progress: `helped_injured_traveler: 1`

`data/content/base/quests.yaml`의 `help_injured_traveler` objective는 `progress_key: helped_injured_traveler`를 보고 completed를 판정한다.

## 5. optional_action failed 유지 검증

기존 `tutorial_herb_quest_partial_optional_failed.yaml` 흐름은 유지했다.

해당 fixture에서는 `helped_injured_traveler` progress가 발생하지 않으므로 `help_injured_traveler` objective는 failed로 남는다.

## 6. Score Rule 정렬 내용

`data/core/score_rules.yaml`에 `objective_scoring` 섹션을 추가했다.

- `completed_required`
- `completed_optional`
- `partial_required`
- `partial_optional`
- `failed_required`
- `failed_optional`
- `survival_failed`
- `return_failed`

`src/fateweaver/gameplay_p0_scoring.py`는 위 규칙을 사용해 objective별 `score_delta`를 계산한다.
`reward_weight`는 objective 중요도 가중치로 유지했다.

## 7. Quest Report / JSON / Text MUD Log 검증

JSON Quest Report에서 확인할 항목:

- optional completed fixture에서 `help_injured_traveler` status가 `completed`
- optional failed fixture에서 `help_injured_traveler` status가 `failed`
- optional completed fixture에서 `help_injured_traveler.score_delta`가 `objective_scoring.completed_optional`과 일치
- `score_breakdown.objective_completion`에 optional completed 점수가 반영

Text MUD Play Log에서 확인할 항목:

- `목표 평가:` 섹션 유지
- `help_injured_traveler` objective 표시
- completed fixture에서는 `성공`
- failed fixture에서는 `실패`

## 8. 실행한 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/optional-score-20260630/logs-completed --profile curious_leaning
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/optional-score-20260630/logs-failed --profile balanced
```

로그 위치:

- `.omo/ulw-loop/evidence/optional-score-20260630/logs-completed/`
- `.omo/ulw-loop/evidence/optional-score-20260630/logs-failed/`
- `.omo/ulw-loop/evidence/optional-score-20260630/optional_action_surface.txt`
- `.omo/ulw-loop/evidence/optional-score-20260630/verification.txt`

## 9. 남은 문제

- optional action 카드는 P0 fixture용 최소 카드다. 후속 콘텐츠 확장에서는 Storylet 후보와 온톨로지 태그 기반 등장 조건으로 더 자연스럽게 옮기는 편이 좋다.
- objective scoring은 `score_rules.yaml`로 분리됐지만 아직 P0용 단순 규칙이다.

## 10. 다음 추천 작업

1. optional action 카드를 Storylet/Ontology 후보군과 연결한다.
2. objective type별 score rule matrix를 별도 schema 문서에 더 세분화한다.
3. Quest가 늘어나는 시점에 objective fixture matrix를 Quest별로 분리한다.
