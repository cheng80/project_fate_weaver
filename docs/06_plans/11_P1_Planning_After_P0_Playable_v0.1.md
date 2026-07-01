# [Current] P1 Planning After P0 Playable v0.1

> 상태: [Current] FateWeaver P0 playable milestone 이후 P1의 목표, 우선순위, 첫 실행 작업을 정리한 planning 문서.

## 1. 문서 목적

P0 playable milestone은 하나의 안정적인 자동 검증 가능한 vertical slice를 고정했다. 이 문서는 P1에서 무엇을 먼저 검증하고 확장할지 정한다.

## 2. P0 Baseline

Standard Run baseline:

- Seed/Profile: `202` / `balanced`
- Turn count: `25`
- Result: `success`
- Ending: `prepared_frontier_route`
- 3-card every turn: `PASS`
- Resource alternative selected: `1`
- Unique event count: `11`

Resource Balance baseline:

- 10 seed validation.
- `resource_alternative` selected 2-4 times: `8/10` seeds.
- Zero-selection seeds: `0/10`.
- Average selected count: `2.9`.
- `prepared_frontier_route` ending: `10/10`.
- Standard Run length: `25-26` turns.
- Watch item: seed `202` and seed `707` select `resource_alternative` once.

Text MUD baseline:

- Seed 202 Standard Run Text MUD generation: `PASS`.
- 25 turns.
- 3 cards each turn.
- `prepared_frontier_route`.
- Choice meaning, Quest Report, Run Ending, and score detail are present.

## 3. P1 Goal

P1 should turn the P0 playable loop from an autoplayer-proven slice into a human-evaluable playtest loop.

Primary P1 goal:

- Prepare human playtest evidence before adding broad content, UI, or balance changes.

Secondary P1 goal:

- Preserve the P0 Standard Run as the regression baseline while adding P1 surfaces in isolated packs, scenarios, or documents.

## 4. P1 Design Principles

- Reconfirm P0 baseline before P1 work.
- Do one surface per task.
- Prefer new scenario/pack boundaries over editing the P0 Standard Run directly.
- Do not mix content expansion and balance tuning in one task.
- Let human playtest evidence decide whether Balance Pass 2, Storylet Variety 2, or Text MUD Polish 2 is needed.
- Keep CLI/Text MUD evidence authoritative until a player-facing UI contract is explicit.

## 5. P1 Candidate Epics

- Human Playtest Loop:
  - Prepare 3-5 playtest-ready runs.
  - Capture player choice meaning, repetition, resource pressure, and narrative comprehension.
- P1 Scenario / Quest Pack:
  - Add a small, gated scenario pack after playtest format is fixed.
  - Exercise different quest categories and endings.
- Storylet Variety Expansion 2:
  - Use playtest logs to identify repeated family pressure.
  - Avoid single-id disabling.
- Director Intent Diversity:
  - Improve repeated situation intent feel only if human evidence shows it matters.
- Resource Balance Pass 2:
  - Conditional on seed 202/707 watch items becoming a real playtest problem.
- Text MUD Narrative Polish 2:
  - Conditional on transcript review showing readability gaps.
- Flutter / Flame UI Prototype Prep:
  - Convert stable CLI/Text MUD contracts into UI contracts after human playtest needs are known.
- Save / Load Runtime Contract:
  - Defer until a UI or manual runtime loop needs persistence.
- Authoring Tool / Content Validator 강화:
  - Improve authoring feedback once P1 content work starts.
- Ontology Reasoner v2:
  - Defer until P1 logs prove Reasoner-lite cannot support intended follow-ups.

## 6. Epic Priority

1. Human Playtest Loop.
2. Playtest Findings Audit.
3. P1 Scenario / Quest Pack.
4. Storylet Variety Expansion 2.
5. Resource Balance Pass 2, if evidence supports it.
6. Text MUD Narrative Polish 2, if evidence supports it.
7. Flutter / Flame UI Prototype Prep.
8. Save / Load Runtime Contract.
9. Authoring Tool / Content Validator 강화.
10. Ontology Reasoner v2.

## 7. Recommended P1 Path

Recommended path:

```text
P1 Planning
-> P1 Human Playtest Scenario Pack
-> Human Playtest Run 1
-> Playtest Findings Audit
-> P1 Scenario/Storylet Expansion
-> UI Prototype Prep
```

Reason:

- P0 is already automatically playable.
- The next unknown is whether humans understand and care about the choices.
- UI or broad content work before playtest evidence risks scaling the wrong loop.

## 8. First P1 Task Recommendation

Recommended first task:

```text
CODEX_TASK_P1_Human_Playtest_Scenario_Pack_v0.1.md
```

Why this first:

- It does not require changing gameplay logic.
- It can preserve the P0 Standard Run baseline.
- It creates evidence for later balance, storylet, narrative, and UI work.
- It defines how humans will evaluate the loop before the project adds more systems.

Why not the alternatives yet:

- `CODEX_TASK_P1_Scenario_Pack_1_v0.1.md`: useful, but scenario expansion should follow the playtest format.
- `CODEX_TASK_P1_Flutter_UI_Prototype_Prep_v0.1.md`: important, but UI should inherit from a human-validated loop.

## 9. P1 Scope Guard

P1 work should:

- Keep P0 Standard Run regression intact.
- Add P1 content through separate scenario/pack boundaries when possible.
- Avoid direct overwrite of P0 data.
- Extend validation before relying on new surfaces.
- Keep task scope narrow enough to verify in one run.

P1 work should not start with:

- Full campaign system.
- Production save/load.
- Procedural generation.
- LLM runtime storyteller.
- Flutter full UI build.
- Advanced economy.
- Multi-region progression.

## 10. P0 Regression Guard

Every P1 implementation task should re-run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall -q src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs <evidence-dir>/standard_run --profile balanced
git diff --check
```

Expected P0 regression result:

- 25-35 turns.
- Current seed 202 baseline remains 25 turns unless a new baseline is approved.
- `success`.
- `prepared_frontier_route`.
- Three cards every turn.
- Text MUD and JSON logs generated.

## 11. P1 Success Criteria

P1 should be considered successful when:

- At least 3 human playtest-ready runs exist.
- Each playtest run has seed/scenario setup, expected observation, and feedback questions.
- P0 Standard Run regression remains green.
- Human playtest findings identify whether choice meaning, repetition, resource pressure, and narrative flow need P1 changes.
- The first P1 playtest result is documented before broad content or UI work starts.

## 12. Deferred Items

- Scenario Pack 1 implementation.
- Balance Pass 2.
- Storylet Variety Expansion 2.
- Director Intent Diversity tuning.
- Text MUD Narrative Polish 2.
- Flutter / Flame UI prototype.
- Save/load runtime contract.
- Ontology Reasoner v2.

## 13. Not Recommended Yet

Do not start these before human playtest evidence:

- Full Flutter UI build.
- Runtime LLM storytelling.
- Large content bulk fill.
- Full campaign progression.
- Advanced economy systems.
- Save/load persistence.
