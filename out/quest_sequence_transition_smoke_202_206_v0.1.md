# Subagent Auto-Play Batch Report

## Batch Summary
- seeds: 202, 203, 204, 205, 206
- agents: goal_focused, safety_first, risk_seeking, explorer, contrarian
- max turns safety cap: 25
- total runs: 25
- crash count: 0
- invariant violation count: 0
- same turn duplicate count: 0
- outcome counts: {'success': 15, 'failure': 10}
- stop reason counts: {'completed': 15, 'max_turn_reached': 9, 'failure': 1}

## Quest Lifecycle Summary
- quest completion count: 30
- reward granted count: 30
- reward missing after success count: 0
- duplicate reward detected count: 0
- duplicate reward prevention count: 0
- next quest transition count: 15
- next quest onboarding count: 15
- run complete count: 15
- no next quest count: 15
- stale previous quest card after transition count: 0
- completion blocked by min turns count: 0
- completed quest dragged to max turn count: 0
- completion turn distribution: {'3': 10, '6': 10, '4': 4, '10': 2, '11': 2, '9': 1, '5': 1}

## Agent Summary
- goal_focused: runs=5 avg_turns=6.0 warnings=12 stop_reasons={'completed': 5}
- safety_first: runs=5 avg_turns=25.0 warnings=87 stop_reasons={'max_turn_reached': 5}
- risk_seeking: runs=5 avg_turns=6.0 warnings=12 stop_reasons={'completed': 5}
- explorer: runs=5 avg_turns=10.2 warnings=18 stop_reasons={'completed': 5}
- contrarian: runs=5 avg_turns=24.6 warnings=97 stop_reasons={'max_turn_reached': 4, 'failure': 1}

## Run Matrix
- seed 202 / goal_focused: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=2
- seed 202 / safety_first: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=14
- seed 202 / risk_seeking: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=2
- seed 202 / explorer: outcome=success turns=10 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 202 / contrarian: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=22
- seed 203 / goal_focused: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 203 / safety_first: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=18
- seed 203 / risk_seeking: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 203 / explorer: outcome=success turns=11 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=4
- seed 203 / contrarian: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=18
- seed 204 / goal_focused: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=2
- seed 204 / safety_first: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=19
- seed 204 / risk_seeking: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=2
- seed 204 / explorer: outcome=success turns=9 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 204 / contrarian: outcome=failure turns=23 stop_reason=failure quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=21
- seed 205 / goal_focused: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=2
- seed 205 / safety_first: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=18
- seed 205 / risk_seeking: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=2
- seed 205 / explorer: outcome=success turns=10 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 205 / contrarian: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=21
- seed 206 / goal_focused: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 206 / safety_first: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=18
- seed 206 / risk_seeking: outcome=success turns=6 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=3
- seed 206 / explorer: outcome=success turns=11 stop_reason=completed quest_complete=2 reward=2 run_complete=1 no_next_quest=1 stale_previous=0 warnings=5
- seed 206 / contrarian: outcome=failure turns=25 stop_reason=max_turn_reached quest_complete=0 reward=0 run_complete=0 no_next_quest=0 stale_previous=0 warnings=15

## Notable Cases
- seed 202 / goal_focused: ["turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']"]
- seed 202 / safety_first: ["turn 3: off-quest ['read_departure_signs']", "turn 4: off-quest ['buy_local_hint']", "turn 5: off-quest ['read_departure_signs']", "turn 6: off-quest ['buy_local_hint']", "turn 8: off-quest ['buy_local_hint']", "turn 9: off-quest ['read_departure_signs']", "turn 13: off-quest ['buy_local_hint']", "turn 14: off-quest ['read_departure_signs']", "turn 16: off-quest ['read_departure_signs']", "turn 17: off-quest ['ask_apothecary', 'buy_local_hint']", "turn 18: off-quest ['read_departure_signs']", "turn 20: off-quest ['read_departure_signs']", "turn 22: off-quest ['read_departure_signs']", "turn 25: off-quest ['buy_local_hint']"]
- seed 202 / risk_seeking: ["turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']"]
- seed 202 / explorer: ["turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']", "turn 4: off-quest ['inspect_tracks']"]
- seed 202 / contrarian: ["turn 3: off-quest ['buy_local_hint']", "turn 4: off-quest ['buy_local_hint']", "turn 6: off-quest ['inspect_tracks']", "turn 7: off-quest ['enter_deep_woods']", "turn 8: off-quest ['inspect_tracks']", "turn 9: off-quest ['inspect_tracks']", "turn 10: off-quest ['enter_deep_woods']", "turn 11: off-quest ['search_herbs', 'enter_deep_woods']", "turn 12: off-quest ['inspect_tracks']", "turn 13: off-quest ['enter_deep_woods']", "turn 14: off-quest ['inspect_tracks']", "turn 15: off-quest ['inspect_tracks']", "turn 16: off-quest ['enter_deep_woods']", "turn 17: off-quest ['search_herbs', 'enter_deep_woods']", "turn 18: off-quest ['inspect_tracks']", "turn 19: off-quest ['inspect_tracks']", "turn 20: off-quest ['inspect_tracks']", "turn 21: off-quest ['inspect_tracks']", "turn 22: off-quest ['search_herbs', 'inspect_tracks']", "turn 23: off-quest ['enter_deep_woods']", "turn 24: off-quest ['enter_deep_woods']", "turn 25: off-quest ['enter_deep_woods']"]
- seed 203 / goal_focused: ["turn 1: off-quest ['buy_local_hint']", "turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']"]
- seed 203 / safety_first: ["turn 1: off-quest ['buy_local_hint']", "turn 2: off-quest ['read_departure_signs']", "turn 4: off-quest ['read_departure_signs']", "turn 5: off-quest ['buy_local_hint']", "turn 7: off-quest ['buy_local_hint']", "turn 10: off-quest ['buy_local_hint']", "turn 11: off-quest ['read_departure_signs']", "turn 12: off-quest ['buy_local_hint']", "turn 13: off-quest ['ask_apothecary', 'buy_local_hint']", "turn 14: off-quest ['buy_local_hint']", "turn 16: off-quest ['read_departure_signs']", "turn 17: off-quest ['ask_apothecary', 'buy_local_hint']", "turn 18: off-quest ['buy_local_hint']", "turn 20: off-quest ['buy_local_hint']", "turn 21: off-quest ['buy_local_hint']", "turn 22: off-quest ['ask_apothecary']", "turn 23: off-quest ['read_departure_signs']", "turn 25: off-quest ['read_departure_signs']"]
- seed 203 / risk_seeking: ["turn 1: off-quest ['buy_local_hint']", "turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']"]
- seed 203 / explorer: ["turn 1: off-quest ['buy_local_hint']", "turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']", "turn 4: off-quest ['inspect_tracks']"]
- seed 203 / contrarian: ["turn 1: off-quest ['buy_local_hint']", "turn 2: off-quest ['read_departure_signs']", "turn 4: off-quest ['buy_local_hint']", "turn 5: off-quest ['read_departure_signs']", "turn 7: off-quest ['read_departure_signs']", "turn 9: off-quest ['ask_apothecary']", "turn 10: off-quest ['buy_local_hint']", "turn 11: off-quest ['read_departure_signs']", "turn 12: off-quest ['read_departure_signs']", "turn 13: off-quest ['buy_local_hint']", "turn 14: off-quest ['ask_apothecary', 'read_departure_signs']", "turn 16: off-quest ['read_departure_signs']", "turn 17: off-quest ['ask_apothecary', 'read_departure_signs']", "turn 18: off-quest ['read_departure_signs']", "turn 20: off-quest ['read_departure_signs']", "turn 21: off-quest ['read_departure_signs']", "turn 23: off-quest ['read_departure_signs']", "turn 25: off-quest ['read_departure_signs']"]
- seed 204 / goal_focused: ["turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']"]
- seed 204 / safety_first: ["turn 2: off-quest ['buy_local_hint']", "turn 3: off-quest ['read_departure_signs']", "turn 4: off-quest ['buy_local_hint']", "turn 6: off-quest ['buy_local_hint']", "turn 7: off-quest ['read_departure_signs']", "turn 8: off-quest ['buy_local_hint']", "turn 9: off-quest ['buy_local_hint']", "turn 10: off-quest ['read_departure_signs']", "turn 11: off-quest ['buy_local_hint']", "turn 13: off-quest ['buy_local_hint']", "turn 14: off-quest ['buy_local_hint']", "turn 16: off-quest ['buy_local_hint']", "turn 17: off-quest ['read_departure_signs']", "turn 19: off-quest ['ask_apothecary', 'buy_local_hint']", "turn 21: off-quest ['ask_apothecary']", "turn 22: off-quest ['buy_local_hint']", "turn 23: off-quest ['read_departure_signs']", "turn 24: off-quest ['read_departure_signs']", "turn 25: off-quest ['buy_local_hint']"]
- seed 204 / risk_seeking: ["turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']"]
- seed 204 / explorer: ["turn 2: off-quest ['inspect_tracks']", "turn 3: off-quest ['enter_deep_woods']", "turn 4: off-quest ['inspect_tracks']"]
- seed 204 / contrarian: ["turn 2: off-quest ['buy_local_hint']", "turn 4: off-quest ['inspect_tracks']", "turn 5: off-quest ['enter_deep_woods']", "turn 6: off-quest ['inspect_tracks']", "turn 7: off-quest ['enter_deep_woods']", "turn 8: off-quest ['inspect_tracks']", "turn 9: off-quest ['enter_deep_woods']", "turn 10: off-quest ['inspect_tracks']", "turn 11: off-quest ['inspect_tracks']", "turn 12: off-quest ['enter_deep_woods']", "turn 13: off-quest ['inspect_tracks']", "turn 14: off-quest ['enter_deep_woods']", "turn 15: off-quest ['inspect_tracks']", "turn 16: off-quest ['enter_deep_woods']", "turn 17: off-quest ['enter_deep_woods']", "turn 18: off-quest ['search_herbs', 'enter_deep_woods']", "turn 19: off-quest ['inspect_tracks']", "turn 20: off-quest ['enter_deep_woods']", "turn 21: off-quest ['search_herbs', 'inspect_tracks']", "turn 22: off-quest ['inspect_tracks']", "turn 23: off-quest ['enter_deep_woods']"]
- seed 205 / goal_focused: ["turn 2: off-quest ['enter_deep_woods']", "turn 3: off-quest ['inspect_tracks']"]
- seed 205 / safety_first: ["turn 2: off-quest ['buy_local_hint']", "turn 4: off-quest ['buy_local_hint']", "turn 5: off-quest ['read_departure_signs']", "turn 6: off-quest ['buy_local_hint']", "turn 7: off-quest ['read_departure_signs']", "turn 9: off-quest ['buy_local_hint']", "turn 10: off-quest ['read_departure_signs']", "turn 12: off-quest ['read_departure_signs']", "turn 14: off-quest ['ask_apothecary', 'read_departure_signs']", "turn 15: off-quest ['read_departure_signs']", "turn 17: off-quest ['read_departure_signs']", "turn 18: off-quest ['buy_local_hint']", "turn 19: off-quest ['ask_apothecary']", "turn 20: off-quest ['buy_local_hint']", "turn 21: off-quest ['buy_local_hint']", "turn 23: off-quest ['read_departure_signs']", "turn 24: off-quest ['ask_apothecary']", "turn 25: off-quest ['read_departure_signs']"]
- seed 205 / risk_seeking: ["turn 2: off-quest ['enter_deep_woods']", "turn 3: off-quest ['inspect_tracks']"]
- seed 205 / explorer: ["turn 2: off-quest ['enter_deep_woods']", "turn 3: off-quest ['inspect_tracks']", "turn 4: off-quest ['enter_deep_woods']"]
- seed 205 / contrarian: ["turn 2: off-quest ['buy_local_hint']", "turn 3: off-quest ['ask_apothecary']", "turn 4: off-quest ['buy_local_hint']", "turn 5: off-quest ['read_departure_signs']", "turn 6: off-quest ['buy_local_hint']", "turn 7: off-quest ['buy_local_hint']", "turn 9: off-quest ['read_departure_signs']", "turn 10: off-quest ['read_departure_signs']", "turn 12: off-quest ['read_departure_signs']", "turn 14: off-quest ['read_departure_signs']", "turn 15: off-quest ['read_departure_signs']", "turn 16: off-quest ['ask_apothecary']", "turn 17: off-quest ['inspect_tracks']", "turn 18: off-quest ['search_herbs', 'enter_deep_woods']", "turn 19: off-quest ['enter_deep_woods']", "turn 20: off-quest ['search_herbs', 'inspect_tracks']", "turn 21: off-quest ['search_herbs', 'inspect_tracks']", "turn 22: off-quest ['enter_deep_woods']", "turn 23: off-quest ['search_herbs', 'inspect_tracks']", "turn 24: off-quest ['inspect_tracks']", "turn 25: off-quest ['inspect_tracks']"]
- seed 206 / goal_focused: ["turn 1: off-quest ['read_departure_signs']", "turn 2: off-quest ['enter_deep_woods']", "turn 3: off-quest ['inspect_tracks']"]
- seed 206 / safety_first: ["turn 1: off-quest ['read_departure_signs']", "turn 3: off-quest ['read_departure_signs']", "turn 4: off-quest ['buy_local_hint']", "turn 6: off-quest ['buy_local_hint']", "turn 7: off-quest ['buy_local_hint']", "turn 9: off-quest ['buy_local_hint']", "turn 10: off-quest ['read_departure_signs']", "turn 11: off-quest ['buy_local_hint']", "turn 12: off-quest ['buy_local_hint']", "turn 14: off-quest ['ask_apothecary']", "turn 15: off-quest ['buy_local_hint']", "turn 16: off-quest ['read_departure_signs']", "turn 18: off-quest ['ask_apothecary', 'read_departure_signs']", "turn 20: off-quest ['buy_local_hint']", "turn 21: off-quest ['read_departure_signs']", "turn 23: off-quest ['buy_local_hint']", "turn 24: off-quest ['read_departure_signs']", "turn 25: off-quest ['ask_apothecary', 'buy_local_hint']"]
- seed 206 / risk_seeking: ["turn 1: off-quest ['read_departure_signs']", "turn 2: off-quest ['enter_deep_woods']", "turn 3: off-quest ['inspect_tracks']"]
- seed 206 / explorer: ["turn 1: off-quest ['read_departure_signs']", "turn 2: off-quest ['enter_deep_woods']", "turn 3: off-quest ['inspect_tracks']", "turn 4: off-quest ['enter_deep_woods']", "turn 5: off-quest ['inspect_tracks']"]
- seed 206 / contrarian: ["turn 1: off-quest ['read_departure_signs']", "turn 3: off-quest ['read_departure_signs']", "turn 4: off-quest ['buy_local_hint']", "turn 6: off-quest ['buy_local_hint']", "turn 7: off-quest ['buy_local_hint']", "turn 9: off-quest ['buy_local_hint']", "turn 10: off-quest ['ask_apothecary']", "turn 11: off-quest ['read_departure_signs']", "turn 12: off-quest ['read_departure_signs']", "turn 16: off-quest ['ask_apothecary', 'read_departure_signs']", "turn 20: off-quest ['read_departure_signs']", "turn 21: off-quest ['read_departure_signs']", "turn 23: off-quest ['ask_apothecary', 'read_departure_signs']", "turn 24: off-quest ['read_departure_signs']", "turn 25: off-quest ['read_departure_signs']"]
