# [Current] Failure Outcome Taxonomy Result v0.1

> 상태: [Current] Gameplay P0의 failure 의미를 정리하고 merchant failure fixture를 생존 실패와 Quest 고유 실패로 분리한 결과 문서.

## 1. 작업 목적

`result_type=failure` 안에 섞여 있던 Quest 실패와 character survival(캐릭터 생존) 실패를 구분했다.

이번 작업은 새 Quest(퀘스트)를 추가하지 않았다. 기존 `merchant_lost_pack_recovery` failure fixture(실패 고정 데이터)를 Quest 고유 실패와 health_zero(체력 0) 실패로 분리했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/27_Forest_Path_Scouting_Quest_Result_v0.1.md`
- `docs/07_reviews/28_Missing_Porter_Search_Quest_Result_v0.1.md`
- `docs/07_reviews/29_Merchant_Lost_Pack_Quest_Result_v0.1.md`

## 3. 변경 파일

- `src/fateweaver/quest_objectives.py`
- `src/fateweaver/text_mud_log.py`
- `data/scenarios/merchant_lost_pack_recovery_failure.yaml`
- `data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml`
- `tests/test_gameplay_run_failure_outcomes.py`
- `tests/test_gameplay_run_merchant_lost_pack.py`
- `docs/00_index/README_Docs_Index.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/07_reviews/29_Merchant_Lost_Pack_Quest_Result_v0.1.md`
- `docs/07_reviews/30_Failure_Outcome_Taxonomy_Result_v0.1.md`

## 4. result_type 의미 정리

`result_type`은 계속 기존 3값을 유지한다.

- `success`: Quest Expedition Run(퀘스트 원정 실행)이 주요 목표를 달성했다.
- `partial_success`: 의미 있는 성과는 있지만 목표/귀환/보조 목표/보상이 부족하다.
- `failure`: 해당 Quest Expedition Run(퀘스트 원정 실행)이 Quest 성공으로 인정되지 않는다.

`result_type=failure`는 캐릭터 사망을 뜻하지 않는다.

## 5. failure_kind

Quest Report(JSON)에 `failure_kind`를 추가했다.

- `none`: success 또는 partial_success.
- `death_or_incapacitated`: `health_zero` 기반 생존 실패.
- `objective_failed`: 주 목표 미완료.
- `return_failed`: 귀환/보고 실패.
- `time_expired`: turn/day 제한 초과.
- `reputation_collapse`: 평판 붕괴형 실패.
- `quest_specific_failure`: `recovery_failed`, `rescue_failed` 같은 Quest별 핵심 행위 실패.
- `unknown`: 분류되지 않은 failure.

P0 우선순위는 `health_zero`를 최우선으로 두고, 그 외에는 주 목표 실패를 우선 분류한다.

## 6. character_outcome

Quest Report(JSON)에 `character_outcome`을 추가했다.

- `alive`: health가 1 이상.
- `incapacitated`: health가 0 이하.

`injured`, `dead_or_lost`, `unknown`은 향후 부상/사망 시스템 확장용 예약 값이다.

## 7. Merchant objective_failed fixture

`data/scenarios/merchant_lost_pack_recovery_failure.yaml`은 health_zero(체력 0)가 아니라 Quest 고유 실패를 검증하도록 바꿨다.

검증 기대:

- result_type: `failure`
- failure_kind: `objective_failed`
- character_outcome: `alive`
- failure_reasons: `max_turn_exceeded`, `return_failed`, `primary_objective_failed` 유지
- health_zero 없음
- score: -60

## 8. Merchant health_zero fixture

`data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml`을 추가했다.

검증 기대:

- result_type: `failure`
- failure_kind: `death_or_incapacitated`
- character_outcome: `incapacitated`
- failure_reasons: `health_zero`, `primary_objective_failed` 유지
- score: -120

## 9. JSON / Text MUD Log 검증

JSON Quest Report(퀘스트 보고서)에 다음 필드가 추가됐다.

- `failure_kind`
- `character_outcome`

Text MUD Log(텍스트 MUD 로그)의 Quest Report 섹션에도 다음 줄을 추가했다.

- `실패 종류`
- `캐릭터 결과`

Evidence(증거) 경로:

- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-objective/`
- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-health-zero/`
- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-success/`
- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-partial/`
- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/herb-health-zero/`
- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/forest-failure/`
- `.omo/ulw-loop/evidence/failure-taxonomy-20260630/porter-failure/`

## 10. 기존 Quest 회귀 검증

기존 `failure_reasons`는 제거하지 않았다.

기존 herb / forest / missing porter / merchant success / partial / failure scenario(약초 / 숲길 / 짐꾼 / 상인 성공 / 부분 성공 / 실패 시나리오)는 계속 검증 대상이다.

## 11. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_failure_outcomes tests.test_gameplay_run_merchant_lost_pack
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py src/fateweaver/quest_objectives.py src/fateweaver/text_mud_log.py tests/test_gameplay_run_failure_outcomes.py tests/test_gameplay_run_merchant_lost_pack.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-objective --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-health-zero --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/merchant-partial --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/herb-health-zero --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/forest-failure --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/missing_porter_search_intro_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/failure-taxonomy-20260630/porter-failure --profile balanced
```

## 12. 남은 문제

- `time_expired` 전용 merchant fixture(고정 데이터)는 아직 없다.
- `character_outcome`은 P0 최소 규칙이라 `alive`와 `incapacitated`만 실제로 사용한다.
- 사망, 부상, 실종, 전투불능의 세부 구분은 아직 없다.

## 13. 다음 추천 작업

1. `merchant_lost_pack_recovery_failure_time_expired.yaml`을 추가해 time_expired(시간 초과) 실패를 따로 검증한다.
2. `character_outcome`을 health 외 상태나 향후 injury(부상) 시스템과 연결한다.
