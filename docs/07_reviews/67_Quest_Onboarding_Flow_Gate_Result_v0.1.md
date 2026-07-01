# Quest Onboarding Flow Gate Result v0.1

## Status

PASS.

Standard Run manual choice trace now exposes quest onboarding context at run start without changing autoplayer selection, card/event scoring, resource balance, quest data, or Text MUD wording.

## Problem Cause

Manual Choice Runner already used `scenario.active_quest_id` to load the active quest before turn 1, and each full JSON turn already carried `quest_id` / `quest_title`. The separate `manual_choice_trace` did not carry that quest context. It only exposed presented cards, selected card, resource delta, objective delta, and next-event tag delta, so a facilitator replay could not identify the active quest, required objective list, or onboarding turn from the trace alone.

## Modified Files

- `tools/manual_choice_runner.py`
- `tools/manual_choice_runner_types.py`
- `tools/manual_choice_runner_trace.py`
- `tests/test_manual_choice_runner_onboarding.py`
- `docs/07_reviews/67_Quest_Onboarding_Flow_Gate_Result_v0.1.md`

## Applied Onboarding Flow

- Added a dedicated manual trace builder in `tools/manual_choice_runner_trace.py`.
- Manual Choice Runner now passes the active quest plus before/after `RunState` into trace construction.
- Turn 1 is marked as the run-start onboarding turn.
- Required objective status is computed from the actual objective type and current `RunState`.
- No card/event/quest data was added.
- No selection score, balance, resource delta, cooldown, objective gate, or autoplayer path was changed.

## Trace Information

Each manual choice trace entry now includes:

- `active_quest_id`
- `active_quest_title`
- `quest_onboarding`
- `onboarding_reason`
- `onboarding_turn` on the onboarding turn
- `required_objective_ids`
- `required_objectives`

For seed 202 Standard Run, the run-start trace shows:

- active quest: `survive_the_storm_pass` / `폭풍 산길 생존 귀환`
- onboarding reason: `run_start`
- required objectives:
  - `find_storm_shelter`
  - `secure_survival_route`
  - `return_from_storm_pass`
  - `survive_expedition`
- presented card counts after onboarding: `[3, 3, 3]`
- duplicate presented cards in checked turns: none

Evidence:

- `.omo/ulw-loop/quest-onboarding-flow-gate-20260702/evidence/red_onboarding_tests.txt`
- `.omo/ulw-loop/quest-onboarding-flow-gate-20260702/evidence/green_onboarding_tests.txt`
- `.omo/ulw-loop/quest-onboarding-flow-gate-20260702/evidence/manual_surface_final_summary.txt`
- `.omo/ulw-loop/quest-onboarding-flow-gate-20260702/evidence/manual_surface_final/manual_seed_202_choice_trace.json`

## Added Tests

- `ManualChoiceRunnerOnboardingTests.test_quest_onboarding_trace_marks_active_quest_at_run_start`
- `ManualChoiceRunnerOnboardingTests.test_quest_onboarding_trace_exposes_required_objectives`
- `ManualChoiceRunnerOnboardingTests.test_quest_onboarding_preserves_three_card_invariant_and_unique_cards`

Existing manual runner robustness and completed objective stale choice tests remain in `tests/test_manual_choice_runner.py`.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests/test_manual_choice_runner.py tests/test_manual_choice_runner_onboarding.py
PASS: 11 tests OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest
PASS: 158 tests OK

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tools tests
PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PASS: VALIDATION: PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PASS: VALIDATION: PASS

.venv/bin/python /Users/cheng80/.codex/plugins/cache/sisyphuslabs/omo/4.14.1/skills/programming/scripts/python/check-no-excuse-rules.py tools/manual_choice_runner.py tools/manual_choice_runner_trace.py tools/manual_choice_runner_types.py tests/test_manual_choice_runner.py tests/test_manual_choice_runner_onboarding.py
PASS: no violations in 5 file(s)
```

## Seed 202 Autoplayer Baseline

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 202 --runs 1 --logs .omo/ulw-loop/quest-onboarding-flow-gate-20260702/evidence/autoplayer_seed202_final --profile balanced
```

Observed:

- turn_count: `25`
- result_type: `success`
- ending_id: `prepared_frontier_route`
- presented_cards count invariant: `true`
- `manual_choice_mode` absent from autoplayer log

Evidence:

- `.omo/ulw-loop/quest-onboarding-flow-gate-20260702/evidence/autoplayer_seed202_final_summary.txt`

## Completed Objective Stale Choice Regression

Maintained by:

- `tests/test_manual_choice_runner.py`
- `ManualChoiceRunnerTests.test_completed_objective_refresh_filters_stale_quest_progress_cards`
- focused manual runner suite: 11 tests OK
- full unittest: 158 tests OK

## Out Of Scope

- Suspicious merchant / off-quest relevance noise remains out of scope for this Gate.
- No quest lifecycle redesign was attempted.
- No onboarding card/event data was inserted.
- No Text MUD prose polish was performed.
- No gameplay success coercion was added.

## Commit / Working Tree

- Commit hash: recorded in final Codex handoff after commit creation.
- Working tree clean: verified after commit/push in final Codex handoff.
