# [Current] P0 Playable Milestone Checklist v0.1

> 상태: [Current] FateWeaver P0 playable 상태를 유지하기 위한 검증 체크리스트.

## 1. Purpose

이 문서는 P0 playable milestone 이후 변경 작업이 현재 playable baseline을 깨뜨리지 않았는지 확인하는 체크리스트다.

## 2. Must Pass Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall -q src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/standard_run --profile balanced
git diff --check
```

## 3. Standard Run Checklist

Seed 202 Standard Run must keep these P0 properties unless a P1 task intentionally updates the baseline:

- Scenario: `standard_run_25_35_turn`
- Profile: `balanced`
- Turn count: `25-35`
- Current frozen count: `25`
- Result type: `success`
- Character outcome: `alive`
- Ending: `prepared_frontier_route`
- 3 cards every turn: `PASS`
- Quest report emitted: `PASS`
- Score breakdown emitted: `PASS`
- Text MUD emitted: `PASS`

Current accepted watch values:

- Unique event count: `11`
- `resource_alternative` selected count: `1`

## 4. Resource Balance Checklist

The current P0 resource baseline is:

- Multi-seed validation size: at least `10` seeds when re-running resource validation.
- Zero-selection seeds: `0`.
- Seeds with `resource_alternative` selected 2-4 times: target majority, current baseline `8/10`.
- Average `resource_alternative` selected count: current baseline `2.9`.
- Ending stability: `prepared_frontier_route` remains the dominant/expected Standard Run ending.
- Standard Run length: current multi-seed baseline `25-26` turns.

Watch but do not block P0:

- Seed `202`: selected count `1`.
- Seed `707`: selected count `1`.

## 5. Text MUD Checklist

Text MUD output should include:

- Run metadata.
- Day/time/turn heading.
- Quest and region.
- Scene/place framing.
- Current resources.
- Inventory.
- Clue/omen state when present.
- Three cards.
- Selected card.
- Choice meaning.
- Risk/reward judgment.
- Result interpretation.
- State change and change meaning.
- Quest progress.
- Score change.
- Final result.
- Quest Report.
- Run Ending.
- Ending interpretation.
- Score detail.
- Objective evaluation.

Text MUD validation is output validation only. It must not mutate gameplay state.

## 6. Regression Checklist

Before accepting a P1 change, verify:

- No quest gate is bypassed.
- No requirements gate is bypassed.
- No cooldown hard block is bypassed.
- No max occurrence or min turn gate is bypassed.
- Random seed determinism is preserved.
- Standard Run still ends in the accepted 25-35 turn band unless a new baseline is approved.
- JSON evidence remains machine-readable.
- Text MUD remains human-readable.

## 7. Scope Guard

For milestone maintenance tasks, this file set is allowed:

- `docs/**`
- `.omo/ulw-loop/evidence/**`

These paths are not allowed unless the task explicitly leaves freeze mode:

- `src/**`
- `data/**`
- `tests/**`
- `tools/**`

## 8. P0 Freeze Rule

P0 is frozen as a playable milestone. Do not opportunistically combine P0 maintenance with:

- Balance tuning.
- Director tuning.
- Ontology changes.
- Quest/Card/Event/Item/Ending additions.
- Text MUD copy polish.
- Storylet Pool expansion.

Any intentional baseline-changing work should be treated as P1 and should create or update a dedicated result document.
