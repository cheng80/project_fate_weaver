# [Current] P0 Playable Milestone Freeze Result v0.1

> 상태: [Current] FateWeaver P0 playable 상태를 고정하고, P1 이전에 유지해야 할 검증 기준과 watch item을 정리한 milestone freeze 문서.

## 1. Scope

이 문서는 P0 playable milestone을 고정하기 위한 문서/검증 결과다.

이번 작업에서는 기능, gameplay logic, balance/scoring/selection/director/ontology, Quest/Card/Event/Item/Ending, Text MUD 문구를 변경하지 않았다.

## 2. Evidence Basis

기준 evidence:

- Fresh seed 202 Standard Run:
  - `.omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/standard_run/`
  - `.omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/standard_run_baseline_summary.json`
  - `.omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/p0_milestone_snapshot.md`
- Validation output:
  - `.omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/p0_validation_results.txt`
- Prior baseline documents:
  - `docs/07_reviews/45_Standard_Run_25_35_Turn_Verification_Result_v0.1.md`
  - `docs/07_reviews/47_Ontology_Core_To_Director_Loop_Result_v0.1.md`
  - `docs/07_reviews/48_Card_Candidate_Repetition_Gate_Result_v0.1.md`
  - `docs/07_reviews/49_Standard_Run_Play_Quality_Audit_v0.1.md`
  - `docs/07_reviews/51_Director_Tuning_Second_Pass_Result_v0.1.md`
  - `docs/07_reviews/52_Gameplay_P0_Rules_Refactor_Gate_Result_v0.1.md`
  - `docs/07_reviews/53_Gameplay_Balance_Pass_Result_v0.1.md`
  - `docs/07_reviews/54_Resource_Alternative_Surface_Gate_Result_v0.1.md`
  - `docs/07_reviews/55_Resource_Balance_Validation_Result_v0.1.md`

Evidence caveat:

- `docs/07_reviews/50_Storylet_Pool_Expansion_Result_v0.1.md` is not present in this checkout.
- `docs/07_reviews/56_Text_MUD_Narrative_Polish_Result_v0.1.md` is not present in this checkout.
- Text MUD baseline is therefore frozen from the current executable output and commit history, not from a separate 56 result document.

## 3. P0 Done Summary

P0 is frozen as a playable deterministic text adventure loop with these completed surfaces:

- Quest / Expedition Clock:
  - Scenario-driven quest objective tracking is active.
  - Standard Run uses day/turn progression and stops within the accepted 25-35 turn window.
- 3-Card Choice:
  - Every Standard Run turn presents three cards.
  - Cards preserve availability, risk, reward/cost, and slot role evidence in JSON.
- Multi-Select:
  - Multi-select schema and rendering remain part of the P0 gameplay contract.
- Objective / Optional Objective:
  - Required objectives and survival objectives resolve into the quest report.
  - Optional/resource decisions are available without replacing quest gates.
- Score Breakdown:
  - Quest progress, survival, discovery, reputation, resource management, risk management, ending bonus, and penalties are visible in Text MUD and JSON.
- Quest Report:
  - Result type, failure kind, character outcome, objective status, score, and ending are emitted.
- Failure Outcome Taxonomy:
  - Failure categories are represented separately from normal success/partial paths.
- Data Split / Loader:
  - Card, quest, and event hint split loaders are in place.
- Content Enrichment:
  - Card, clue, omen, item, and ending enrichment has been integrated before this freeze.
- Standard Run 25-35:
  - The current seed 202 baseline ends at 25 turns.
- Ontology Core / Validator / Reasoner-lite:
  - Ontology validation and reasoner-lite inputs support event/card context.
- Situation Director-lite:
  - Situation intent, next event tags, storylet family memory, and event selection scoring are part of the current baseline.
- Card Repetition Gate:
  - Repeat group, cooldown tags, frequency penalty, fallback overuse, and ontology card modifiers are part of candidate scoring.
- Storylet Pool Expansion / Director Tuning 2:
  - Expanded storylet/event variety and second-pass director tuning are assumed from current code/data state.
- Gameplay Balance Pass 1:
  - Resource pressure and reward repetition tuning are reflected in current Standard Run evidence.
- Resource Alternative Surface Gate:
  - Resource alternative is present, presented, and selected at least once in seed 202.
- Resource Balance Validation:
  - 10-seed validation established resource alternative as a real selection axis.
- Text MUD Narrative Polish:
  - Fresh Text MUD output includes scene framing, choice meaning, state change meaning, quest report, score detail, and ending interpretation.

## 4. P0 Gameplay Coverage

P0 currently covers one stable playable expedition loop:

- Start from a scenario fixture.
- Advance through deterministic event/storylet selection.
- Present three card choices per turn.
- Let the autoplayer choose between quest progress, risk discovery, and resource alternative cards.
- Track resources, inventory, clues, omens, score, and quest progress.
- Resolve an ending and quest report.
- Render both JSON evidence and human-readable Text MUD output.

This is a P0 vertical slice, not a broad content product.

## 5. Standard Run Baseline

Fresh baseline command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py \
  --scenario data/scenarios/standard_run_25_35_turn.yaml \
  --seed 202 \
  --runs 1 \
  --logs .omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/standard_run \
  --profile balanced
```

Frozen seed 202 baseline:

- Scenario: `standard_run_25_35_turn`
- Seed/Profile: `202` / `balanced`
- Turn count: `25`
- Result: `success`
- Character outcome: `alive`
- Ending: `prepared_frontier_route`
- 3 cards each turn: `PASS`
- Unique event count: `11`
- Resource alternative:
  - Candidate count: `975`
  - Presented count: `25`
  - Selected count: `1`
  - Selected turns: `21`
- Selected choice type counts:
  - `quest_progress`: `20`
  - `risk_discovery`: `4`
  - `resource_alternative`: `1`

The seed 202 baseline is accepted for P0 because it remains within 25-35 turns, keeps the target ending, and proves resource alternative reaches selection at least once.

## 6. Multi-Seed Resource Balance Baseline

From `docs/07_reviews/55_Resource_Balance_Validation_Result_v0.1.md`:

- Seeds validated: `10`
- Seeds with resource alternative selected 2-4 times: `8/10`
- Zero-selection seeds: `0`
- Average selected count: `2.9`
- Ending: `prepared_frontier_route` in `10/10`
- Standard Run length: `25-26` turns
- Watch seeds:
  - `202`: selected count `1`
  - `707`: selected count `1`

P0 freezes this as sufficient. Balance Pass 2 is not part of P0 unless a P1 planning task explicitly reopens it.

## 7. Text MUD Baseline

Fresh seed 202 Text MUD output includes:

- Run start metadata.
- Per-turn scene framing.
- Current state/resources.
- Three cards with availability, risk, and reward/cost.
- Selected card.
- Choice meaning.
- Risk/reward judgment.
- Result message and interpretation.
- State change and change meaning.
- Item/clue/omen interpretation.
- Quest progress.
- Score change.
- Final result block.
- Quest Report.
- Run Ending and ending interpretation.
- Score detail.
- Objective evaluation.

Text MUD P0 freeze rule: renderer output may be improved only in a future Text MUD task. P0 milestone maintenance must not polish text opportunistically while changing gameplay, balance, director, or data.

## 8. Validation Command Set

P0 validation commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall -q src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/evidence/p0-playable-milestone-freeze-20260701/standard_run --profile balanced
git diff --check
```

Current run result:

- `unittest discover`: PASS, 147 tests.
- `compileall`: PASS.
- `validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml`: PASS.
- `validate_data.py --ontology`: PASS.
- `console_simulator.py` seed 202: PASS.
- `git diff --check`: PASS.

## 9. P0 Watch Items

These are known watch items, not P0 blockers:

- `resource_alternative` selected count is low for seed 202 and seed 707.
- Seed 202 unique event count is `11`, not `12`.
- Situation intents and storylet families can still repeat under deterministic pressure.
- Storylet Pool Expansion result document is absent in this checkout.
- Text MUD Narrative Polish result document is absent in this checkout.
- Balance Pass 2 may be useful after human playtest evidence, but is not part of this freeze.
- Human playtest is still needed before P1 content expansion.

## 10. P0 Out Of Scope

The following are explicitly outside P0 after this freeze:

- Additional Quest/Card/Event/Item/Ending content.
- Large Storylet Pool expansion.
- New director architecture.
- New ontology model expansion.
- Balance Pass 2.
- LLM runtime narration.
- Text MUD polish 2.
- UI/UX product shell.
- Save/load system.
- Production packaging.
- Human-authored content campaign scale-up.

## 11. P1 Backlog Candidates

Recommended P1 candidates:

- P1 planning after P0 playable.
- Human playtest scenario pack.
- Multi-seed qualitative play audit.
- Storylet variety pass based on human play evidence.
- Resource Balance Pass 2 if the watch seeds become blockers.
- Text MUD Narrative Polish 2 after human transcript review.
- Quest expansion with acceptance gates.
- Scenario pack expansion.
- Manual player-facing UI shell.

First recommended task:

- `CODEX_TASK_P1_Planning_After_P0_Playable_v0.1.md`

Reason: P0 is now frozen. The next safest step is to decide P1 scope and gates before adding more content or tuning balance.

## 12. Freeze Decision

P0 playable is frozen as a stable milestone.

Future work should treat the baseline values in this document and `docs/05_validation/17_P0_Playable_Milestone_Checklist_v0.1.md` as the regression surface. Changes that intentionally alter these baselines should be framed as P1 work and should update the milestone checklist or create a new baseline document.

## 13. Release Note Draft

### FateWeaver P0 Playable Milestone

FateWeaver now has a deterministic playable P0 text adventure loop.

Highlights:

- Scenario-driven quest progression with expedition clock.
- Three meaningful card choices per turn.
- Resource, risk, clue, omen, inventory, and reputation tracking.
- Objective-based quest report and ending resolution.
- Ontology/reasoner/director-lite support for contextual event flow.
- Candidate repetition and resource alternative balancing sufficient for P0.
- Human-readable Text MUD logs with scene, choice meaning, consequence, report, and ending interpretation.

Frozen baseline:

- Standard Run seed 202: 25 turns, success, alive, `prepared_frontier_route`.
- Resource balance validation: 10 seeds, 0 zero-selection seeds, 8/10 seeds selecting resource alternative 2-4 times.
- Text MUD: seed 202 Standard Run renders readable turn-by-turn and final report output.

Known watch items:

- Low resource alternative selection on seed 202 and 707.
- Seed 202 unique event count remains 11.
- Human playtest is required before P1 expansion.
