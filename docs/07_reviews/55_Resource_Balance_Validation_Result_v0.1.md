# Resource Balance Validation Result v0.1

Status: PASS with watch item

## Scope

This audit validates whether `resource_alternative` now works as a real Standard Run choice axis after Resource Alternative Surface Gate.

No gameplay balance, autoplayer scoring, threshold, quest, card, event, item, ending, Text MUD, or Director changes were made.

Evidence was generated from Standard Run balanced profile logs for 10 seeds:

- Seeds: `101`, `202`, `303`, `404`, `505`, `606`, `707`, `808`, `909`, `1001`
- Scenario: `data/scenarios/standard_run_25_35_turn.yaml`
- Raw evidence: `.omo/ulw-loop/evidence/resource-balance-validation-20260701/seed_samples/`
- Parsed summary: `.omo/ulw-loop/evidence/resource-balance-validation-20260701/multi_seed_resource_balance_summary.json`
- Parsed table: `.omo/ulw-loop/evidence/resource-balance-validation-20260701/multi_seed_resource_balance_table.csv`
- Seed 202 turn trace: `.omo/ulw-loop/evidence/resource-balance-validation-20260701/seed_202_resource_trace.json`

## Result Summary

`resource_alternative` is now consistently present and usually selected enough to count as an active choice axis.

| Metric | Result |
|---|---:|
| Seed count | 10 |
| Candidate count per 25-turn run | 975 |
| Presented count per 25-turn run | 25 |
| Selected count average | 2.9 |
| Average selected / presented ratio | 11.57% |
| Seeds with 0 selected | 0 / 10 |
| Seeds with 1 selected | 2 / 10 |
| Seeds with 2-4 selected | 8 / 10 |
| Seeds with 5+ selected | 0 / 10 |
| Standard Run turn range | 25-26 |
| `prepared_frontier_route` ending | 10 / 10 |
| Unique event count range | 11-14 |

Target range coverage is 80% of sampled seeds. That is enough to defer Balance Pass 2 for this surface.

## Seed Table

| Seed | Turns | Candidate | Presented | Selected | Selected turns | Selected / presented | Min health | Min food | Min money | End money | Unique events |
|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 101 | 25 | 975 | 25 | 2 | 17, 21 | 8.00% | 8 | 3 | 4 | 23 | 11 |
| 202 | 25 | 975 | 25 | 1 | 21 | 4.00% | 8 | 3 | 4 | 17 | 11 |
| 303 | 25 | 975 | 25 | 4 | 17, 19, 22, 23 | 16.00% | 8 | 1 | 4 | 14 | 14 |
| 404 | 25 | 975 | 25 | 4 | 17, 19, 22, 23 | 16.00% | 8 | 1 | 4 | 23 | 11 |
| 505 | 25 | 975 | 25 | 4 | 17, 21, 23, 24 | 16.00% | 8 | 1 | 4 | 17 | 12 |
| 606 | 25 | 975 | 25 | 3 | 17, 21, 22 | 12.00% | 8 | 2 | 4 | 26 | 13 |
| 707 | 25 | 975 | 25 | 1 | 21 | 4.00% | 8 | 3 | 4 | 17 | 12 |
| 808 | 25 | 975 | 25 | 4 | 21, 22, 23, 24 | 16.00% | 8 | 1 | 4 | 14 | 12 |
| 909 | 26 | 1014 | 26 | 2 | 17, 22 | 7.69% | 8 | 1 | 4 | 20 | 14 |
| 1001 | 25 | 975 | 25 | 4 | 17, 19, 20, 22 | 16.00% | 8 | 1 | 4 | 17 | 12 |

## Candidate / Presented / Selected

Candidate generation is not the bottleneck. Every sampled run produced a large resource alternative candidate pool, and every turn presented one resource alternative card.

The remaining variation is selection pressure:

- Low-selection seeds: `202`, `707` each selected 1 time.
- Target-range seeds: `101`, `303`, `404`, `505`, `606`, `808`, `909`, `1001`.
- Over-selection seeds: none.

This is a healthy shape for the current balanced profile. `resource_alternative` is visible every turn but does not dominate quest progress or optional actions.

## Turn Timing

Selections mostly occur in the late run:

- Earliest selected turn: 17
- Latest selected turn: 24
- Common selected turns: 17, 21, 22, 23

This timing matches the intended role after Resource Alternative Surface Gate: resource alternatives become attractive once food pressure is visible, without forcing early-run detours.

Seed 202 remains the lower-bound watch sample. It selected `resource_alternative` once on turn 21, which satisfies the previous surface gate but stays below the desired 2-4 range.

## Resource / Economy / Risk Pressure

The JSON state has no explicit `risk` key. This audit treats `curse` plus low-water marks for health, food, and money as risk-pressure evidence.

Observed pressure:

- Health remained stable: minimum health was 8 in all sampled runs.
- Food pressure is real: 6 / 10 seeds reached minimum food 1, 1 / 10 reached minimum food 2, and 3 / 10 stayed at minimum food 3.
- Money pressure did not become a hard constraint: minimum money stayed at 4, while ending money ranged from 14 to 26.
- Curse stayed present but bounded: max curse was 1 in all sampled runs.
- Reputation ended at 5 across sampled runs.

Food is currently the main driver for resource-alternative selection. Money pressure is still mild, but this validation task should not tune economy values.

## Standard Run Quality

Standard Run quality remained within the required envelope:

- 10 / 10 runs ended with `prepared_frontier_route`.
- 10 / 10 runs stayed inside the 25-35 turn target.
- Turn count was 25 for 9 seeds and 26 for 1 seed.
- Unique event count stayed at 11-14.
- Every turn presented 3 cards.

The unique event count floor of 11 remains acceptable here because the task is resource-axis validation, not storylet expansion. The 11-event seeds still preserve the required ending and choice surface.

## Balance Pass 2 Decision

Do not run Balance Pass 2 now.

Reason:

- `resource_alternative` selected count is in the 2-4 target range for 8 / 10 seeds.
- There are no zero-selection seeds.
- There are no over-selection seeds.
- The previous seed 202 failure mode is no longer a zero-selection case.
- Standard Run length, ending, and card presentation constraints remain intact.

Watch item:

- Seeds `202` and `707` selected only once.
- If future content changes push the 2-4 seed ratio below 70%, or reintroduce 0-selection seeds, reopen a narrow Balance Pass 2 focused on selection pressure evidence rather than broad economy tuning.

## Verification

This task intentionally changed documentation only. Source data, gameplay rules, content data, tests, Text MUD strings, and Director structure were not modified.

Verification evidence is stored at `.omo/ulw-loop/evidence/resource-balance-validation-20260701/verification.txt`.
