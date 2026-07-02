# [Current] Gameplay P0 Rules Refactor Gate Result v0.1

> 상태: [Current] Director Tuning 2차 이후 warning band에 도달한 `gameplay_rules.py`를 기능 변경 없이 분리한 결과 문서.

## 1. 작업 목적

다음 Gameplay Balance Pass 전에 `src/fateweaver/gameplay_rules.py`의 Director scoring / trace helper 성격 로직을 작은 모듈로 분리했다.

이번 작업은 behavior-preserving refactor로 진행했다.

금지 사항은 유지했다.

- Gameplay Balance 조정 없음.
- score / reward / penalty / bonus cap 수치 변경 없음.
- Quest / Card / Event / Item / Ending 추가 없음.
- Director tuning 추가 없음.
- `quest_ids`, requirements, cooldown, max occurrence, min turn gate 변경 없음.
- random seed / deterministic 흐름 변경 없음.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/14_Ontology_Core_Model_v0.1.md`
- `docs/07_reviews/47_Ontology_Core_To_Director_Loop_Result_v0.1.md`
- `docs/07_reviews/48_Card_Candidate_Repetition_Gate_Result_v0.1.md`
- `docs/07_reviews/49_Standard_Run_Play_Quality_Audit_v0.1.md`
- `docs/07_reviews/51_Director_Tuning_Second_Pass_Result_v0.1.md`

참고: `docs/07_reviews/50_Storylet_Pool_Expansion_Result_v0.1.md`는 작업 문서에 언급되어 있었지만 현재 repo에는 없었다.

## 3. 변경 요약

- `src/fateweaver/director_scoring.py`를 추가했다.
  - `ontology_event_weight`
  - `director_event_score`
  - event tag aggregation helper
  - ontology modifier parsing helper
- `src/fateweaver/run_json.py`를 추가했다.
  - `clock_json`
  - `multi_select_json`
  - `influences`
- `src/fateweaver/gameplay_rules.py`는 기존 public API를 유지하도록 위 함수들을 import/re-export한다.

## 4. LOC 결과

| File | Before pure LOC | After pure LOC |
|---|---:|---:|
| `src/fateweaver/gameplay_rules.py` | 250 | 195 |
| `src/fateweaver/director_scoring.py` | n/a | 65 |
| `src/fateweaver/run_json.py` | n/a | 33 |

목표였던 `gameplay_rules.py` pure LOC 200 이하를 달성했다.

## 5. Public API 호환

기존 import surface는 유지했다.

```python
from fateweaver.gameplay_rules import director_event_score
from fateweaver.gameplay_rules import ontology_event_weight
from fateweaver.gameplay_rules import select_storylet
```

기존 `tests.test_director_tuning_second_pass`, `tests.test_situation_director_lite`, `tests.test_gameplay_run_standard_run`가 리팩터 전후 모두 통과했다.

## 6. Standard Run 재검증

Seed 202, balanced profile 기준 결과:

| Metric | After Refactor |
|---|---:|
| Turn Count | 25 |
| Ending | `prepared_frontier_route` |
| Result Type | `success` |
| Unique Event Count | 12 |
| Unique Presented Cards | 18 |
| Unique Selected Cards | 10 |
| Clue Follow-up Event Count | 5 |
| Omen Escalation Event Count | 2 |

Top events:

```text
suspicious_merchant: 5
storm_pass_shelter_hint: 4
wind_gap_reveals_safe_descent: 3
merchant_receipt_marks_old_route: 2
trade_gossip_points_elsewhere: 2
nervous_merchant_revises_story: 2
second_witness_contradicts_merchant: 2
```

Director Tuning 2차 결과 문서의 Standard Run surface와 동일하게 유지됐다.

## 7. Evidence

Evidence directory:

```text
.omo/ulw-loop/evidence/gameplay-p0-rules-refactor-gate-20260701/
```

Key artifacts:

- `C001-characterization-before.txt`
- `C001-characterization-after-final.txt`
- `C002-compileall-final.txt`
- `C002-data-validation.txt`
- `C002-diff-check-final.txt`
- `C002-full-unittest-final.txt`
- `C002-final-loc.txt`
- `C003-standard-run-cli-final.txt`
- `C003-standard-run-summary-final.json`
- `standard-run-final/*.json`
- `standard-run-final/*.txt`

## 8. Verification

Passed:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_director_tuning_second_pass tests.test_situation_director_lite tests.test_gameplay_run_standard_run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/evidence/gameplay-p0-rules-refactor-gate-20260701/standard-run-final --profile balanced
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
for scenario in data/scenarios/*.yaml; do PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario "$scenario"; done
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
git diff --check
```

Full unittest:

```text
Ran 141 tests in 70.460s
OK
```

## 9. 다음 작업 준비 상태

Gameplay Balance Pass에서 money / reputation reward 반복, autoplayer quest_progress 편중, resource pressure, score / reward / penalty 수치 조정을 진행할 때 `gameplay_rules.py` orchestration과 Director scoring helper diff가 분리되어 회귀 원인 추적이 쉬워졌다.
