# Gameplay Balance Pass Result v0.1

## 목적

`CODEX_TASK_Gameplay_Balance_Pass_v0.1.md` 기준으로 Standard Run의 1차 밸런스 조정을 수행했다.

이번 pass는 구조 리팩터링, Quest/Card/Event/Item/Ending 추가, Storylet Pool 확장, Director 구조 변경 없이 다음 문제를 작게 조정하는 데 한정했다.

- `balanced` autoplayer의 `quest_progress` 선택 편중 완화
- money / reputation reward 반복 완화
- resource pressure와 risk 선택의 체감 강화
- score breakdown이 실제 선택 차이를 더 잘 설명하는지 점검
- `prepared_frontier_route` ending threshold 유지 여부 검토

## 구현 요약

수정 범위는 `src/fateweaver/gameplay_p0_rules.py`의 `select_cards`에 제한했다.

- Combo rule은 기존처럼 최우선으로 유지했다.
- `balanced` profile에서 아직 ending 안정 구간에 들어가기 전이면:
  - food / health / money가 낮을 때 `resource_alternative`를 우선 선택한다.
  - 이미 여러 quest progress가 쌓였을 때 `risk_discovery`를 선택해 clue/risk surface를 노출한다.
- 같은 선택지가 이미 선택된 경우에는 기존 history guard를 존중한다.
- ending 안정성을 해치지 않도록 마지막 5턴 구간에서는 기존 return/resolve 흐름을 우선한다.

테스트는 `tests/test_gameplay_balance_pass.py`를 추가해 다음 경계를 고정했다.

- progress가 충분히 쌓인 상태에서는 `quest_progress`만 계속 고르지 않는다.
- resource가 낮으면 `resource_alternative`를 우선한다.
- money/reputation 보상이 붙은 `quest_progress`가 무조건 선택되지 않는다.
- combo rule은 balance selection보다 우선한다.

기존 `tests/test_gameplay_p0.py`의 `max_day_failure` 기대는 업데이트했다. 현재 objective evaluator는 `max_day_exceeded`와 함께 미완료 필수 목표의 실패 사유도 보존하므로, 테스트는 `max_day_exceeded` 포함과 `max_turn_exceeded` 제외를 확인하도록 정렬했다.

## Before / After

Evidence:

- Before JSON: `.omo/ulw-loop/evidence/gameplay-balance-pass-20260701/before/run_standard_run_25_35_turn_balanced_202_20260701T051705385121Z_0001.json`
- After JSON: `.omo/ulw-loop/evidence/gameplay-balance-pass-20260701/after/run_standard_run_25_35_turn_balanced_202_20260701T052843642877Z_0001.json`
- Diff report: `.omo/ulw-loop/evidence/gameplay-balance-pass-20260701/balance_diff_report.json`

| Metric | Before | After | 판단 |
|---|---:|---:|---|
| turn_count | 25 | 25 | 유지 |
| ending_id | prepared_frontier_route | prepared_frontier_route | 유지 |
| result_type | success | success | 유지 |
| score_total | 649 | 576 | 반복 보상/무위험 진행 점수 완화 |
| quest_progress_selected_count | 24 | 21 | 개선 |
| risk_discovery_selected_count | 0 | 4 | 개선 |
| resource_alternative_selected_count | 0 | 0 | Standard Run에서는 미노출 |
| money_reward_count | 7 | 6 | 소폭 개선 |
| money_spend_count | 0 | 1 | 개선 |
| reputation_reward_count | 12 | 10 | 개선 |
| health_loss_count | 1 | 2 | pressure 증가 |
| food_loss_count | 2 | 1 | 과도한 food drain은 완화 |
| unique_event_count | 12 | 11 | 보존 선호 미충족 |

Resource deltas:

- health: `0 -> -1`
- food: `-8 -> -7`
- money: `+20 -> +16`
- reputation: `+4 -> +4`

Score breakdown 변화:

- discovery: `19 -> 32`
- quest_progress: `270 -> 222`
- reputation: `44 -> 36`
- resource_management: `-3 -> -6`
- penalty: `0 -> -2`

이 변화는 선택이 단순 progress/reward 누적에서 risk discovery와 resource pressure 쪽으로 일부 이동했음을 보여준다.

## Ending Threshold 검토

After run은 25턴, `prepared_frontier_route`, `success`를 유지했다.

중간 검증에서 ending 안정 구간 없이 risk/resource 선택을 늦은 턴까지 밀어 넣으면 `survival_return`으로 밀리는 경로가 확인됐다. 따라서 이번 pass에서는 ending condition 자체를 바꾸지 않고, 마지막 5턴에는 기존 return/resolve 흐름을 유지하도록 했다.

판정:

- `prepared_frontier_route`는 현재 Standard Run 내용과 계속 맞는다.
- ending threshold를 넓히거나 좁히는 데이터 변경은 이번 1차 pass 범위에서는 하지 않았다.
- 후속 pass에서 ending 다양성을 다룰 경우, late-run 선택 policy와 함께 별도 검증해야 한다.

## 잔여 리스크

- Standard Run의 `resource_alternative_selected_count`는 여전히 0이다. 다만 low-resource unit test에서는 resource 선택이 활성화된다. seed 202 Standard Run은 resource threshold에 늦게 도달하기 때문에 ending 안정성을 우선했다.
- `unique_event_count`는 12에서 11로 내려갔다. 필수 유지 조건은 통과하지만, "12 이상 또는 유지" 선호 기준은 만족하지 못했다.
- reward 반복은 완화됐지만 `report_to_apothecary`, `ask_apothecary` 반복은 아직 남아 있다. 특정 card id hardcode 없이 더 줄이려면 reward diminishing return 또는 family-level reward cap이 후속 pass에 적합하다.

## 검증

모두 PASS:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_balance_pass tests.test_gameplay_p0 tests.test_gameplay_p0_standard_run tests.test_gameplay_p0_card_repetition_gate
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
git diff --check
```

Full unittest 결과:

```text
Ran 145 tests in 71.988s
OK
```

## 판정

PASS.

Gameplay Balance Pass 1은 Standard Run 25~35 Turn과 `prepared_frontier_route` ending을 유지하면서, `quest_progress` 선택 편중과 reward 반복을 소폭 완화했다. 변경은 작은 autoplayer policy 조정과 테스트 보강에 제한했으며, 구조/데이터/콘텐츠 확장은 하지 않았다.
