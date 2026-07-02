# [Current] Text MUD Log Section Refactor Result v0.1

> 상태: [Current] `text_mud_log.py`의 출력 섹션을 분리하고 LOC warning band를 해소한 결과 문서.

## 1. 작업 목적

`src/fateweaver/text_mud_log.py`가 246 pure LOC로 warning band에 들어간 상태를 해소했다.

이번 작업은 새 Quest 추가가 아니라 Text MUD Play Log 출력 레이어의 책임 분리다. Gameplay rule, JSON schema, `result_type`, `failure_kind`, `character_outcome` 의미는 변경하지 않았다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/30_Failure_Outcome_Taxonomy_Result_v0.1.md`
- `src/fateweaver/text_mud_log.py`

## 3. 변경 파일

- `src/fateweaver/text_mud_log.py`
- `src/fateweaver/text_mud_sections.py`
- `src/fateweaver/text_mud_turns.py`
- `src/fateweaver/text_mud_report.py`
- `src/fateweaver/text_mud_values.py`
- `tests/test_text_mud_log.py`
- `docs/00_index/README_Docs_Index.md`
- `docs/07_reviews/31_Text_MUD_Log_Section_Refactor_Result_v0.1.md`

## 4. 분리 전 문제

`text_mud_log.py`가 run 저장, 전체 렌더링 orchestration, turn 출력, Quest Report 출력, JSON value formatting helper를 한 파일에서 모두 담당했다.

Pure LOC는 246이었다. 다음 Quest나 `failure_kind` / `character_outcome` / economy / score 표시를 늘리면 250 LOC defect band에 들어가기 쉬운 상태였다.

## 5. 분리 후 구조

- `text_mud_log.py`: public API와 전체 출력 순서 조립.
- `text_mud_sections.py`: 기존 section helper import 호환용 facade.
- `text_mud_turns.py`: run header, turn, card, choice, resource/status 변화 출력.
- `text_mud_report.py`: run summary, Quest Report, score breakdown 출력.
- `text_mud_values.py`: JSON value를 Text MUD 문자열과 typed map/list로 변환.

## 6. 유지한 외부 API

기존 외부 import 경로를 유지했다.

- `save_text_mud_log(log, json_path)`
- `render_text_mud_log(log)`

`src/fateweaver/gameplay_run.py`와 `src/fateweaver/simulator.py`의 import 경로는 변경하지 않았다.

## 7. Text MUD 출력 호환성

기존 Text MUD Play Log의 핵심 섹션을 유지했다.

- `[Run 시작]`
- Day / Turn heading
- `Quest`
- `카드`
- `선택`
- `결과`
- `Quest Report`
- `결과 유형`
- `실패 종류`
- `캐릭터 결과`
- `[Run 종료]`

`score_breakdown`은 기존 JSON Quest Report 구조를 바꾸지 않고 Text MUD Quest Report에 `점수 상세`로 표시했다.

## 8. Failure Taxonomy 표시 검증

Text MUD Quest Report에서 다음 표시를 유지했다.

- `결과 유형`
- `실패 종류`
- `캐릭터 결과`
- `실패 이유`
- `목표 평가`

Simulator evidence에서 merchant objective failure와 health_zero failure가 구분됐다.

- objective failure: `result_type=failure`, `failure_kind=objective_failed`, `character_outcome=alive`
- health_zero failure: `result_type=failure`, `failure_kind=death_or_incapacitated`, `character_outcome=incapacitated`

Evidence 경로:

- `.omo/ulw-loop/evidence/text-mud-section-refactor-20260630/merchant-objective/`
- `.omo/ulw-loop/evidence/text-mud-section-refactor-20260630/merchant-health-zero/`

## 9. LOC 결과

Pure LOC 결과:

- `src/fateweaver/text_mud_log.py`: 15
- `src/fateweaver/text_mud_sections.py`: 13
- `src/fateweaver/text_mud_turns.py`: 149
- `src/fateweaver/text_mud_report.py`: 37
- `src/fateweaver/text_mud_values.py`: 53
- `tests/test_text_mud_log.py`: 105

`text_mud_log.py`는 warning band 밖으로 내려갔다. 신규 helper 파일도 모두 200 LOC 이하에 있다.

## 10. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_text_mud_log
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/scripts/python/check-no-excuse-rules.py src/fateweaver/text_mud_log.py src/fateweaver/text_mud_sections.py src/fateweaver/text_mud_turns.py src/fateweaver/text_mud_report.py src/fateweaver/text_mud_values.py tests/test_text_mud_log.py
```

Scenario validator:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_optional_completed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_partial_optional_failed.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_health_zero.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest_failure_max_day.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/forest_path_scouting_tutorial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/forest_path_scouting_tutorial_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/forest_path_scouting_tutorial_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/missing_porter_search_intro.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/missing_porter_search_intro_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/missing_porter_search_intro_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_partial.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_failure.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml
```

Simulator evidence:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_failure.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/merchant-objective --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_failure_health_zero.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/merchant-health-zero --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/merchant-success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/merchant_lost_pack_recovery_partial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/merchant-partial --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/missing_porter_search_intro.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/porter-success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/forest_path_scouting_tutorial.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/forest-success --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/text-mud-section-refactor-20260630/herb-success --profile balanced
```

## 11. 남은 문제

- Text MUD output formatter는 아직 `JsonMap` 기반이다. JSON log 호환 렌더러라 boundary parsing은 기존 모델 구조를 유지했다.
- Text MUD 섹션 단위 golden snapshot은 없다. 현재는 핵심 행과 simulator evidence로 회귀를 검증한다.

## 12. 다음 추천 작업

1. 다음 출력 필드 추가 전에 `text_mud_turns.py` 또는 `text_mud_report.py` 단위 테스트를 먼저 추가한다.
2. Text MUD 로그 전체 snapshot이 필요해지면 whitespace에 취약한 전체 문자열 비교보다 section-level contract test를 추가한다.
