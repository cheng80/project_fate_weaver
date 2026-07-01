# Resource Alternative Surface Gate Result v0.1

## 목적

Gameplay Balance Pass 1 이후 남은 seed 202 Standard Run의 `resource_alternative_selected_count = 0` 문제를 turn-level evidence로 진단하고, 최소 보정으로 실제 선택을 1회 이상 표면화했다.

금지 범위는 지켰다.

- Quest/Card/Event/Item/Ending 추가 없음
- seed 202 전용 분기 없음
- 특정 card/event id 강제 선택 없음
- `quest_ids` / requirements / cooldown / min_turn gate 변경 없음
- Director 구조 변경 없음
- Text MUD 문구 변경 없음

## 원인 진단

Baseline evidence:

- `.omo/ulw-loop/evidence/resource-alternative-surface-gate-20260701/before_resource_surface_summary.json`
- `.omo/ulw-loop/evidence/resource-alternative-surface-gate-20260701/before_resource_alternative_turn_trace.json`

진단 결과:

| Metric | Before |
|---|---:|
| resource_alternative_candidate_count | 975 |
| resource_alternative_presented_count | 25 |
| resource_alternative_selected_count | 0 |
| turn_count | 25 |
| ending_id | `prepared_frontier_route` |
| result_type | `success` |
| unique_event_count | 11 |

`resource_alternative`는 후보 풀에 충분히 들어왔고 매 turn 3-card에도 제시됐다. 문제는 후보 생성이나 presentation이 아니라 선택 정책이었다.

구체적으로 food가 3인 caution 상태는 turn 21부터 발생했지만, 기존 `balanced` profile은 food <= 2만 resource emergency로 보았다. food <= 2는 turn 25에야 도달했고, 이 시점은 late-run ending 안정 구간이라 resource 선택 정책이 발동하지 않았다.

## 적용한 최소 보정

`src/fateweaver/gameplay_p0_rules.py`의 `balanced` 선택 조건에서 food caution threshold만 `2 -> 3`으로 올렸다.

의미:

- food 3은 즉시 실패 수준은 아니지만 장기 run에서 보급 선택이 합리적인 상태다.
- health/money threshold와 combo 우선순위는 변경하지 않았다.
- card id나 event id를 보지 않는다.
- late-run guard는 유지한다.

## Before / After

Evidence:

- `.omo/ulw-loop/evidence/resource-alternative-surface-gate-20260701/after_resource_surface_summary.json`
- `.omo/ulw-loop/evidence/resource-alternative-surface-gate-20260701/resource_alternative_turn_trace.json`
- `.omo/ulw-loop/evidence/resource-alternative-surface-gate-20260701/resource_surface_diff_report.json`

| Metric | Before | After |
|---|---:|---:|
| turn_count | 25 | 25 |
| ending_id | `prepared_frontier_route` | `prepared_frontier_route` |
| result_type | `success` | `success` |
| resource_alternative_candidate_count | 975 | 975 |
| resource_alternative_presented_count | 25 | 25 |
| resource_alternative_selected_count | 0 | 1 |
| quest_progress_selected_count | 21 | 20 |
| risk_discovery_selected_count | 4 | 4 |
| unique_event_count | 11 | 11 |

Resource selection occurred at turn 21:

```text
turn: 21
event_id: second_witness_contradicts_merchant
selected_card_id: ration_the_last_supplies
resource_state_before: health=8, food=3, money=17, reputation=5
```

## unique_event_count

`unique_event_count`는 11로 유지됐다. 이번 보정은 event/storylet selection이나 Director scoring을 건드리지 않고, 이미 presented 된 세 카드 중 선택 우선순위만 바꿨기 때문이다.

Top event distribution도 before/after가 동일했다.

```text
merchant_receipt_marks_old_route: 4
suspicious_merchant: 4
storm_pass_shelter_hint: 4
wind_gap_reveals_safe_descent: 2
snowmelt_points_to_shelter: 2
```

따라서 unique_event_count 12 회복은 이 Surface Gate의 자연스러운 범위를 벗어난다. 후속 Play Quality Re-Audit 또는 Director/Event rotation pass에서 다루는 것이 맞다.

## 검증

RED:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_resource_alternative_surface_gate tests.test_gameplay_balance_pass
FAILED: food=3 caution selected risk_discovery
```

GREEN:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_resource_alternative_surface_gate tests.test_gameplay_balance_pass
Ran 5 tests
OK
```

Full verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
Ran 146 tests
OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
VALIDATION: PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
VALIDATION: PASS

git diff --check
PASS
```

## 판정

PASS.

`resource_alternative`는 seed 202 Standard Run에서 후보와 3-card presentation에는 이미 충분히 올라오고 있었다. 이번 gate는 선택 정책의 food caution threshold만 일반화된 방식으로 조정해, Standard Run 25턴과 `prepared_frontier_route` ending을 유지하면서 `resource_alternative_selected_count >= 1`을 달성했다.
