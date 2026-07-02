# [Current] Gameplay P0 Objective Schema Doc and Fixture Result v0.1

> 상태: [Current] Gameplay P0 Objective Schema 문서 정렬과 optional_action / max_day_exceeded fixture 검증 결과 문서.

## 1. 작업 목적

Gameplay P0 Objective Schema 정규화 이후 남아 있던 문서와 fixture 간 불일치를 정리했다.

이번 작업은 새 Quest나 대량 콘텐츠를 추가하는 작업이 아니라, 이미 구현된 objective 평가 필드와 Quest Report 출력 구조를 문서에 맞추고, `optional_action`과 `max_day_exceeded`가 실제 fixture와 로그에서 검증되도록 보강하는 작업이다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/19_Gameplay_P0_Objective_Schema_Normalization_Result_v0.1.md`

## 3. 변경 파일

데이터:

- `data/content/base/quests.yaml`
- `data/scenarios/tutorial_herb_quest_failure_max_day.yaml`

코드:

- `src/fateweaver/gameplay_run.py`
- `src/fateweaver/quest_objectives.py`

테스트:

- `tests/test_gameplay_run.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/20_Gameplay_P0_Objective_Schema_Doc_And_Fixture_Result_v0.1.md`

## 4. Schema 문서 정렬 내용

`docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`의 Quest objective 예시를 실제 구현 필드 기준으로 정렬했다.

반영한 objective 필드는 다음과 같다.

- `id`
- `type`
- `target`
- `required`
- `count`
- `value`
- `progress_key`
- `failure_reason`
- `partial_reason`
- `score_key`
- `reward_weight`

Quest Report 예시에는 `objective_results`, `completed_objectives`, `failed_objectives`, `partial_reasons`, `failure_reasons`, `score_breakdown`, `reward_status`, `review_text`를 반영했다.

## 5. optional_action Fixture 검증

`herb_gathering_tutorial`의 optional objective에 `help_injured_traveler`를 추가했다.

- type: `optional_action`
- target: `help_injured_traveler`
- required: `false`
- failure_reason / partial_reason: `optional_failed`
- score_key: `objective_aid`

현재 fixture에서는 해당 optional action이 진행되지 않으므로 `objective_results`에 failed로 남는다. 이 상태는 optional objective 실패가 JSON Quest Report와 Text MUD Play Log에 표시되는지 확인하기 위한 최소 fixture다.

## 6. max_day_exceeded Fixture 검증

`data/scenarios/tutorial_herb_quest_failure_max_day.yaml`를 추가했다.

이 fixture는 시작 시점의 `day`가 `max_days`를 초과하도록 구성해 `max_day_exceeded` reason을 독립적으로 검증한다. `max_turns`와 `target_turns`는 충분히 크게 두어 생존과 주 목표 달성이 가능한 상태에서도 기한 초과 Quest Report가 생성되는지 확인한다.

`src/fateweaver/gameplay_run.py`는 scenario의 `target_turns`를 P0 run budget으로 사용하도록 보강했다. `max_days`는 생존 강제 종료 조건이 아니라 Quest Report의 deadline failure reason으로 유지한다.

`src/fateweaver/quest_objectives.py`는 `max_day_exceeded`가 result type을 failure로 만들도록 판정 경로를 보강했다. 기존 partial fixture에서 사용하는 `max_turn_exceeded`는 `return_late` reason과 함께 partial_success 흐름을 유지한다.

## 7. Quest Report / JSON / Text MUD Log 검증

JSON Quest Report에서 확인한 항목:

- `objective_results`에 `help_injured_traveler` 포함
- `help_injured_traveler` status가 `failed`
- `failure_reasons`에 `max_day_exceeded` 포함
- max-day fixture에서 주 목표 `collect_herbs`, `report_to_apothecary`는 completed
- max-day fixture에서 final health는 0보다 큼
- max-day fixture에서 `max_turn_exceeded` 미포함

Text MUD Play Log에서 확인한 항목:

- `목표 평가:` 섹션 유지
- `help_injured_traveler` objective 표시
- `결과 이유: max_day_exceeded` 표시

## 8. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run.GameplayP0Tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml --seed 42 --runs 1 --logs .omo/objective-schema-doc-fixture-20260630/logs-optional --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml --seed 42 --runs 1 --logs .omo/objective-schema-doc-fixture-20260630/logs-max-day --profile balanced
```

로그 위치:

- `.omo/objective-schema-doc-fixture-20260630/logs-optional/`
- `.omo/objective-schema-doc-fixture-20260630/logs-max-day/`

## 9. 남은 문제

- `optional_action`은 현재 최소 fixture에서 failed 경로만 검증한다. completed 경로는 후속 Storylet/Card 확장 시 별도 fixture로 추가하는 편이 좋다.
- Objective score rule은 여전히 P0용 단순 `reward_weight` 계산이다. 후속 Quest 확장 시 score rule 데이터 분리를 검토한다.

## 10. 다음 추천 작업

1. `optional_action` completed 경로를 실제 카드 결과와 연결한다.
2. Objective score rule을 `data/core/score_rules.yaml` 기준으로 더 명확히 분리한다.
3. Quest가 2개 이상이 되는 시점에 objective type별 fixture matrix를 분리한다.
