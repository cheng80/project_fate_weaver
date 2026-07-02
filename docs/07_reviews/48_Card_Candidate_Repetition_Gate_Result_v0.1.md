# [Current] Card Candidate Repetition Gate Result v0.1

> 상태: [Current] Ontology Reasoner-lite / Situation Director-lite 이후 Standard Run card 반복률 개선 결과.

## 1. 작업 목적

이번 작업은 Standard Run에서 남은 card candidate 반복 문제를 일반화된 방식으로 낮추는 작업이다.

금지 사항은 유지했다.

- Quest 추가 없음.
- Card 대량 추가 없음.
- 특정 card id 하드코딩 penalty 없음.
- `quest_ids`, requirements, cooldown hard block 우회 없음.
- Standard Run 25~35 Turn과 `prepared_frontier_route` ending 유지.

## 2. 변경 요약

- `RepeatMemory`에 long-run card count와 repeat group count를 추가했다.
- Card score에 long-run frequency penalty, repeat-group frequency penalty, shared/fallback overuse penalty를 반영했다.
- Reasoner-lite의 `card_weight_modifiers`를 card score에 `+3` cap으로 반영했다.
- 과다 노출된 card는 같은 slot에 대안이 있으면 selection window에서 뒤로 보낸다.
- village `risk_discovery` 후보 부족을 줄이기 위해 shared card 1개를 추가했다: `read_departure_signs`.

## 3. Before / After

| Metric | Before | After |
|---|---:|---:|
| Turn Count | 25 | 25 |
| Ending | `prepared_frontier_route` | `prepared_frontier_route` |
| Unique Presented Cards | 16 | 18 |
| Unique Selected Cards | 10 | 10 |
| Top Repeated Card | `ration_the_last_supplies` | `ration_the_last_supplies` |
| Top Repeat Count | 15 | 10 |
| `buy_local_hint` Count | 13 | 7 |

After top repeated cards:

```text
ration_the_last_supplies: 10
buy_local_hint: 7
inspect_tracks: 7
rest_briefly: 6
enter_deep_woods: 6
```

## 4. Evidence

Evidence directory:

```text
.omo/ulw-loop/evidence/card-candidate-repetition-gate-20260701/
```

Key artifacts:

- `standard_run_before_summary.json`
- `standard_run_after_summary.json`
- `standard_run_after.json`
- `standard_run_after_text_mud.txt`
- `test_card_repetition_gate_red.txt`
- `verification.txt`

## 5. Verification

Passed:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_card_repetition_gate
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_standard_run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```

## 6. Remaining Risk

`ontology_card_modifier_applied_count` is still 0 in the Standard Run because current ontology rules do not emit card modifiers matching the surfaced Standard Run card tags. Unit coverage proves the bridge works and respects hard gates; future ontology seed expansion should add matching card rules only when content coverage needs it.
