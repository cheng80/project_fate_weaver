# Choice Relevance Noise Gate Result v0.1

## Status

PASS.

Standard Run manual trace now explains presented card relevance per card, and selection fallback now prefers active-quest-relevant candidates before off-quest candidates. No quest/card/event data, scoring weights, resource balance, ontology, director tuning, or Text MUD prose was changed.

## Modified Files

- `src/fateweaver/gameplay_p0_card_selection.py`
- `tools/manual_choice_runner_trace.py`
- `tools/manual_choice_runner_types.py`
- `tests/test_gameplay_p0_card_candidates.py`
- `tests/test_manual_choice_runner_relevance.py`
- `docs/07_reviews/68_Choice_Relevance_Noise_Gate_Result_v0.1.md`

## Cause

The selection trace could show which cards were presented, but it did not explain why a card was relevant to the active quest, required objectives, current storylet, or fallback path. Merchant events can hint cards such as `buy_local_hint`; without per-card relevance metadata, the same card looked like unexplained merchant noise even when it was storylet-hinted.

The selection fallback path also ranked remaining candidates by score/tier/frequency only. If a slot window was exhausted or duplicate-blocked, an off-quest candidate could outrank an active-quest candidate in fallback.

## Trace Additions

Each manual trace entry now includes `presented_card_relevance`, aligned with `presented_card_ids`.

Per presented card:

- `active_quest_id`
- `required_objective_ids`
- `active_quest_linked`
- `required_objective_linked`
- `storylet_linked`
- `resource_or_safety`
- `off_quest_candidate`
- `relevance_reason`
- `selection_reason`
- `fallback_reason`

Seed 202 manual surface evidence:

- `buy_local_hint` appears as `off_quest` when it has no quest/storylet linkage.
- `buy_local_hint` appears as `storylet_context` when the current merchant/trade storylet explicitly hints it.
- 12-turn check had no turn where off-quest cards occupied 2+ presented slots.
- 3-card invariant and same-turn uniqueness stayed true.

Evidence:

- `.omo/ulw-loop/choice-relevance-noise-gate-20260702/evidence/red_relevance_tests.txt`
- `.omo/ulw-loop/choice-relevance-noise-gate-20260702/evidence/green_relevance_tests.txt`
- `.omo/ulw-loop/choice-relevance-noise-gate-20260702/evidence/manual_surface_summary.txt`
- `.omo/ulw-loop/choice-relevance-noise-gate-20260702/evidence/manual_surface/manual_seed_202_choice_trace.json`

## Selection Guard

Fallback selection now prefers candidates that are relevant by at least one existing signal:

- card `quest_ids` includes the active quest
- candidate matched objectives
- candidate matched storylet tags
- candidate matched storylet hints
- card is a `resource_alternative`

This guard applies only to fallback candidates. Normal slot seeded-tier selection and score values are unchanged.

Fallback selections are marked as `selected_by: fallback_pick`, and manual trace exposes `fallback_reason: slot_window_fallback` for selected fallback cards.

## Added Tests

- `ManualChoiceRunnerRelevanceTests.test_presented_cards_include_relevance_metadata`
- `ManualChoiceRunnerRelevanceTests.test_off_quest_cards_do_not_occupy_presented_majority`
- `GameplayP0CardCandidateTests.test_fallback_prefers_active_quest_candidate_over_off_quest_noise`

Existing regression coverage retained:

- Manual Choice Runner robustness
- Completed Objective Choice Refresh stale choice filtering
- Quest Onboarding trace visibility
- 3-card invariant
- same-turn duplicate prevention

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner.py
PASS: 8 tests OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner_onboarding.py tests/test_manual_choice_runner_relevance.py
PASS: 5 tests OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests/test_gameplay_p0_card_candidates.py
PASS: 12 tests OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest
PASS: 161 tests OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tools tests
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PASS: VALIDATION: PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PASS: VALIDATION: PASS

.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.14.1/skills/programming/scripts/python/check-no-excuse-rules.py src/fateweaver/gameplay_p0_card_selection.py tools/manual_choice_runner_trace.py tools/manual_choice_runner_types.py tests/test_manual_choice_runner_relevance.py tests/test_gameplay_p0_card_candidates.py
PASS: no violations in 5 file(s)
```

## Seed 202 Autoplayer Baseline

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/choice-relevance-noise-gate-20260702/evidence/autoplayer_seed202 --profile balanced
```

Observed:

- turn_count: `25`
- result_type: `success`
- ending_id: `prepared_frontier_route`
- presented_cards count invariant: `true`
- `manual_choice_mode` absent from autoplayer log

Evidence:

- `.omo/ulw-loop/choice-relevance-noise-gate-20260702/evidence/autoplayer_seed202_summary.txt`

## Regression Status

- Completed objective stale choice regression: maintained by `tests/test_manual_choice_runner.py`, focused tests OK, full unittest OK.
- Quest onboarding trace regression: maintained by `tests/test_manual_choice_runner_onboarding.py`, focused tests OK, full unittest OK.
- Manual runner robustness: focused tests OK, full unittest OK.

## Out Of Scope

- Merchant system redesign remains out of scope.
- Storylet/director tuning remains out of scope.
- Card/event/quest data additions remain out of scope.
- Text MUD wording polish remains out of scope.
- The guard only changes fallback selection, not normal scored slot selection.

## Commit / Working Tree

- Commit hash: recorded in final Codex handoff after commit creation.
- Working tree clean: verified after commit/push in final Codex handoff.
