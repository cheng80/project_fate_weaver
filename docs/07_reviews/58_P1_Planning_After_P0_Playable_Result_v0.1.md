# [Current] P1 Planning After P0 Playable Result v0.1

> 상태: [Current] P0 playable milestone freeze 이후 P1 planning을 수행하고 첫 P1 작업 후보를 정리한 결과 문서.

## 1. 작업 목적

P0 playable milestone 이후 P1 목표, epic 우선순위, scope guard, regression guard, success criteria, 첫 실행 작업을 정리했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/17_P0_Playable_Milestone_Checklist_v0.1.md`
- `docs/06_plans/10_P1_Backlog_After_P0_Playable_v0.1.md`
- `docs/07_reviews/57_P0_Playable_Milestone_Freeze_Result_v0.1.md`
- `docs/07_reviews/49_Standard_Run_Play_Quality_Audit_v0.1.md`
- `docs/07_reviews/55_Resource_Balance_Validation_Result_v0.1.md`

Missing reference in this checkout:

- `docs/07_reviews/56_Text_MUD_Narrative_Polish_Result_v0.1.md`

## 3. P0 Baseline 재확인

Fresh evidence:

- `.omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/p0_baseline_reference.json`
- `.omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/standard_run/`

Observed seed 202 baseline:

- Scenario: `standard_run_25_35_turn`
- Profile: `balanced`
- Turn count: `25`
- Result type: `success`
- Character outcome: `alive`
- Ending: `prepared_frontier_route`
- 3-card every turn: `PASS`
- Unique event count: `11`
- `resource_alternative` selected count: `1`
- Text MUD checks:
  - Choice meaning: `PASS`
  - Quest Report: `PASS`
  - Run Ending: `PASS`
  - Score detail: `PASS`

## 4. P1 목표

P1의 첫 목표는 P0 playable loop를 사람이 읽고 선택할 수 있는 playtest surface로 전환하는 것이다.

P1은 아직 대규모 content expansion이나 UI build가 아니라, human feedback을 얻기 위한 scenario/brief/evidence 구조를 먼저 고정해야 한다.

## 5. P1 Candidate Epics

- Human Playtest Loop.
- P1 Scenario / Quest Pack.
- Storylet Variety Expansion 2.
- Director Intent Diversity.
- Resource Balance Pass 2.
- Text MUD Narrative Polish 2.
- Flutter / Flame UI Prototype Prep.
- Save / Load Runtime Contract.
- Authoring Tool / Content Validator 강화.
- Ontology Reasoner v2.

## 6. 우선순위 결정

우선순위:

1. Human Playtest Loop.
2. Playtest Findings Audit.
3. P1 Scenario / Quest Pack.
4. Storylet Variety Expansion 2.
5. Resource Balance Pass 2, conditional.
6. Text MUD Narrative Polish 2, conditional.
7. Flutter / Flame UI Prototype Prep.
8. Save / Load Runtime Contract.
9. Authoring Tool / Content Validator 강화.
10. Ontology Reasoner v2.

## 7. 추천 첫 P1 작업

추천:

```text
CODEX_TASK_P1_Human_Playtest_Scenario_Pack_v0.1.md
```

선택 이유:

- P0 baseline을 직접 바꾸지 않는다.
- P1 content/balance/UI 작업의 판단 근거를 만든다.
- 자동 검증으로는 확인할 수 없는 선택 의미, 반복감, resource pressure, narrative flow를 사람이 평가하게 한다.

미룬 작업:

- Scenario Pack 1: playtest format 고정 후 진행.
- Flutter UI Prototype Prep: human feedback 이후 UI contract를 정리한 뒤 진행.
- Balance Pass 2: seed 202/707 watch item이 실제 문제로 확인될 때 진행.

## 8. P1 Scope Guard

- P0 Standard Run을 직접 덮어쓰지 않는다.
- P1 content는 별도 scenario/pack으로 추가한다.
- Content expansion과 balance tuning을 한 작업에 섞지 않는다.
- Director/Ontology 구조 변경은 human evidence 이후로 미룬다.
- Text MUD polish는 transcript review 이후 별도 작업으로 분리한다.

## 9. P0 Regression Guard

P1 작업은 다음 baseline을 깨뜨리면 안 된다.

- Standard Run 25-35 turns.
- Seed 202 current baseline 25 turns unless intentionally rebaselined.
- `success`.
- `prepared_frontier_route`.
- Three cards every turn.
- JSON/Text MUD evidence generation.
- Scenario validation PASS.
- Ontology validation PASS.

## 10. 생성/수정 문서

- `docs/06_plans/11_P1_Planning_After_P0_Playable_v0.1.md`
- `docs/07_reviews/58_P1_Planning_After_P0_Playable_Result_v0.1.md`
- `docs/04_codex/15_Codex_P1_First_Task_Brief_v0.1.md`
- `docs/00_index/README_Docs_Index.md`

## 11. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/standard_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall -q src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
git diff --check
```

## 12. Evidence

- `.omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/p0_baseline_reference.json`
- `.omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/standard_run_cli.txt`
- `.omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/unittest_discover.txt`
- `.omo/ulw-loop/evidence/p1-planning-after-p0-playable-20260701/verification.txt`

## 13. 다음 추천 작업

```text
CODEX_TASK_P1_Human_Playtest_Scenario_Pack_v0.1.md
```

이 작업에서 3-5개 playtest-ready run, expected observation, feedback questions, P0 regression guard를 정의한다.
