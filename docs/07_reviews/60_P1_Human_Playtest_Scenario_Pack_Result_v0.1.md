# [Current] P1 Human Playtest Scenario Pack Result v0.1

> 상태: [Current] P1 첫 작업으로 human playtest scenario pack, protocol, feedback form, result template을 구성한 결과 문서.

## 1. 작업 목적

P1 첫 실행 작업으로 사람이 직접 읽고 선택할 수 있는 human playtest pack을 문서화했다.

이번 작업은 docs/evidence 중심으로 진행했으며 gameplay, data, tests, tools, balance, Text MUD 문구를 변경하지 않았다.

## 2. 읽은 기준 문서

- `docs/04_codex/15_Codex_P1_First_Task_Brief_v0.1.md`
- `docs/06_plans/11_P1_Planning_After_P0_Playable_v0.1.md`
- `docs/06_plans/10_P1_Backlog_After_P0_Playable_v0.1.md`
- `docs/07_reviews/58_P1_Planning_After_P0_Playable_Result_v0.1.md`
- `docs/07_reviews/57_P0_Playable_Milestone_Freeze_Result_v0.1.md`
- `docs/05_validation/17_P0_Playable_Milestone_Checklist_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/07_reviews/55_Resource_Balance_Validation_Result_v0.1.md`
- `docs/07_reviews/49_Standard_Run_Play_Quality_Audit_v0.1.md`
- `docs/07_reviews/53_Gameplay_Balance_Pass_Result_v0.1.md`
- `docs/07_reviews/54_Resource_Alternative_Surface_Gate_Result_v0.1.md`

Missing reference documents:

- `docs/07_reviews/56_Text_MUD_Narrative_Polish_Result_v0.1.md`
- `docs/07_reviews/50_Storylet_Pool_Expansion_Result_v0.1.md`

## 3. 작성한 문서

- `docs/06_plans/12_P1_Human_Playtest_Scenario_Pack_v0.1.md`
- `docs/05_validation/18_Human_Playtest_Protocol_v0.1.md`
- `docs/05_validation/19_Human_Playtest_Feedback_Form_v0.1.md`
- `docs/07_reviews/59_Human_Playtest_Run_1_Result_Template_v0.1.md`
- `docs/07_reviews/60_P1_Human_Playtest_Scenario_Pack_Result_v0.1.md`
- `docs/00_index/README_Docs_Index.md`

## 4. Playtest Run 구성

All runs use `data/scenarios/standard_run_25_35_turn.yaml` and `balanced` profile.

| Run | Seed | Turn | Ending | Resource selections | Unique events | Purpose |
|---:|---:|---:|---|---:|---:|---|
| 1 | 202 | 25 | prepared_frontier_route | 1 | 11 | P0 baseline readability |
| 2 | 101 | 25 | prepared_frontier_route | 2 | 11 | Resource pressure |
| 3 | 303 | 25 | prepared_frontier_route | 4 | 14 | Clue/omen follow-up |
| 4 | 808 | 25 | prepared_frontier_route | 4 | 12 | Storylet variety |
| 5 | 707 | 25 | prepared_frontier_route | 1 | 12 | Optional watch sample |

## 5. P0 Baseline Guard

P0 baseline remains:

- Seed `202`.
- 25 turns.
- `success`.
- `prepared_frontier_route`.
- Three cards every turn.
- `resource_alternative` selected at least once.

No `src/`, `data/`, `tests/`, or `tools/` files were modified.

## 6. Feedback Form 요약

Feedback form captures:

- Overall impression.
- Quest purpose.
- Choice meaning.
- Repetition.
- Resource pressure.
- Clue/omen understanding.
- Text MUD readability.
- Ending acceptance.
- Best and dullest moments.
- 1-5 score table.

## 7. Protocol 요약

Protocol defines:

- Pre-test setup.
- Player intro.
- Facilitator role.
- Per-turn observation.
- Stop conditions.
- Feedback collection.
- Post-test result template.
- No-explanation/no-polish/no-data-change rules.

## 8. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 101 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 303 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 808 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 707 --runs 1 --logs .omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall -q src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
git diff --check
```

## 9. Evidence

- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/playtest_seed_summary.json`
- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/playtest_seed_summary.csv`
- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run/`
- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/unittest_discover.txt`
- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/verification.txt`

## 10. 다음 추천 작업

```text
CODEX_TASK_P1_Human_Playtest_Run_1_v0.1.md
```

Recommended run:

- Run 1, seed `202`.

Reason:

- It is the P0 baseline and should be tested by a human before watch/variant seeds are interpreted.
