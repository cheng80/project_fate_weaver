# [Current] Gameplay P0 Objective Schema Normalization Result v0.1

> 상태: [Current] Gameplay P0의 Quest Objective Schema 정규화 결과 문서.

## 1. 작업 목적

Gameplay P0의 `success`, `partial_success`, `failure`, `quest_report`, reason, score 판단을 Quest별 하드코딩에서 objective 평가 기반으로 옮겼다.

이번 작업은 새 Quest나 콘텐츠 볼륨을 늘리는 작업이 아니라, 기존 `herb_gathering_tutorial` 수직 슬라이스가 후속 Quest 확장에 견딜 수 있도록 objective schema와 평가 결과를 일반화하는 작업이다. 저주는 중심 테마가 아니라 상태/위험 요소 중 하나로만 유지했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
- `docs/07_reviews/16_Gameplay_P0_Foundation_Implementation_Result_v0.1.md`
- `docs/07_reviews/17_Gameplay_P0_Outcome_Coverage_Result_v0.1.md`
- `docs/07_reviews/18_Gameplay_P0_Result_Reason_Coverage_Result_v0.1.md`

## 3. 변경 파일

데이터:

- `data/content/base/quests.yaml`

코드:

- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/gameplay_p0_models.py`
- `src/fateweaver/gameplay_p0_objectives.py`
- `src/fateweaver/text_mud_log.py`
- `src/fateweaver/text_mud_objectives.py`

테스트:

- `tests/test_gameplay_p0.py`

문서:

- `docs/00_index/README_Docs_Index.md`
- `docs/07_reviews/19_Gameplay_P0_Objective_Schema_Normalization_Result_v0.1.md`

## 4. Objective Schema 변경

`data/content/base/quests.yaml`의 `herb_gathering_tutorial` objective에 다음 필드를 명시했다.

- `id`
- `type`
- `target`
- `required`
- `count` 또는 `value`
- `progress_key`
- `failure_reason`
- `partial_reason`
- `score_key`
- `reward_weight`

기존 Quest ID와 scenario ID는 유지했다.

## 5. Objective Type별 평가 기준

- `collect_item`
  - `quest_progress[target] >= count`이면 completed.
  - `0 < quest_progress[target] < count`이면 partial.
  - `quest_progress[target] == 0`이면 failed.
- `return_to_region`
  - 최종 region이 target이고 `quest_progress[progress_key] >= value`이면 completed.
  - 아니면 failed.
- `survive_expedition`
  - `status[target] >= value`이면 completed.
  - 아니면 failed.
- `keep_resource_at_least`
  - `status[target] >= value`이면 completed.
  - 아니면 failed.
- `discover_clue`
  - `target` clue가 있으면 completed.
  - 없으면 failed.
- `optional_action`
  - `quest_progress[target]` 기준으로 completed / partial / failed를 판정할 수 있게 열어 두었다.

## 6. Quest Outcome Resolver 변경

`src/fateweaver/gameplay_p0_objectives.py`에서 objective evaluation을 기반으로 `result_type`을 계산한다.

- `survive_expedition` failed이면 failure.
- required objective가 모두 completed이면 success.
- survival만 제외한 primary objective 중 completed 또는 partial이 있으면 partial_success.
- 그 외는 failure.

기존 P0의 success / partial_success / failure scenario 결과는 유지했다.

## 7. Reason Mapping 변경

기존 reason 문자열은 유지하되 source를 objective evaluation으로 옮겼다.

- `primary_partial`: required `collect_item` partial.
- `report_failed`: partial_success에서 `return_to_region` failed.
- `optional_failed`: optional objective failed.
- `health_zero`: `survive_expedition` failed.
- `return_failed`: failure에서 `return_to_region` failed.
- `primary_objective_failed`: required objective failed.
- `max_turn_exceeded`, `max_day_exceeded`: clock constraint failed.
- `reduced_reward`: partial_success에서 objective miss가 있을 때 reward status와 함께 부여.

## 8. Score Breakdown 변경

Quest Report의 `score_breakdown`에 `objective_completion`을 추가했다.

- completed objective는 `reward_weight` 기반 보너스를 준다.
- partial objective는 줄어든 보너스를 준다.
- failed required objective는 penalty를 준다.
- optional failed objective는 이번 P0에서는 별도 penalty 없이 reason만 제공한다.
- 기존 `outcome_adjustment`는 유지했다.

검증 결과 score 순서는 유지된다.

```text
success > partial_success > failure
```

## 9. JSON / Text MUD Log 변경

JSON `quest_report`에 `objective_results`를 추가했다.

각 objective result는 다음 정보를 가진다.

- `objective_id`
- `objective_type`
- `status`
- `reason`
- `progress_value`
- `target_value`
- `required`
- `score_key`
- `score_delta`

Text MUD Play Log에는 `목표 평가:` 섹션을 추가했다.

## 10. 실행한 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/objective-schema-normalization-20260630/evidence/logs-success --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml --seed 42 --runs 1 --logs .omo/objective-schema-normalization-20260630/evidence/logs-partial --profile balanced
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml --seed 42 --runs 1 --logs .omo/objective-schema-normalization-20260630/evidence/logs-failure --profile balanced
```

## 11. 남은 문제

- `optional_action` type은 evaluator support는 있지만 현재 `herb_gathering_tutorial` fixture에서는 사용하지 않는다.
- `max_day_exceeded` reason은 clock 평가 경로에 남아 있지만 별도 scenario fixture로 검증하지 않았다.
- Objective score rule은 P0용 단순 weight 계산이다. 후속 Quest가 늘어나면 `data/core/score_rules.yaml`과 더 직접 연결하는 편이 좋다.

## 12. 다음 추천 작업

1. Objective schema를 `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`에 실제 구현 필드 기준으로 반영한다.
2. `max_day_exceeded`와 `optional_action` 전용 최소 fixture를 추가한다.
3. Objective별 score rule을 data-driven score rule로 분리한다.
