# Content Enrichment Catalog v0.1

> 상태: [Plan] Card Candidate / Clue / Omen / Item / Ending 확장을 위한 구현 후보 카탈로그.

## 1. 목적

이 문서는 `CODEX_TASK_Content_Enrichment_Ultraresearch_v0.2.md` 기준의 Catalog 산출물이다.

이번 문서는 data 구현이 아니다. 다음 흐름의 입력 자료다.

```text
1. Event Hint Split 완료
2. Data Split Coverage Audit
3. Content Enrichment Catalog 작성
4. Card + Clue + Omen Pack 확장
5. Item + Ending Pack 확장
6. Standard Run 25~35 Turn 검증
```

선행 조건은 충족됐다.

- Event Hint Split: `docs/07_reviews/40_Event_Hint_Split_Loader_Support_Result_v0.1.md`
- Data Split Coverage Audit: `docs/07_reviews/41_Data_Split_Coverage_Audit_v0.1.md`
- Research Notes: `docs/07_reviews/42_Content_Enrichment_Ultraresearch_Notes_v0.1.md`

## 2. 구현 공통 규칙

- 새 Quest를 추가하지 않는다.
- 새 Card Rule은 Pack 작업에서만 추가한다.
- 새 quest-specific Card Rule은 category split file에 두고 `quest_ids`를 반드시 가진다.
- 새 quest-specific Event Hint는 category split file에 두고 `card_candidate_hints`와 `quest_ids`를 검증한다.
- Clue/Omen은 진행을 막는 열쇠가 아니라 선택 판단, partial_success, future event weight, ending residue에 쓰인다.
- Item은 항상 최적해가 아니어야 한다. item choice에는 소모, 기회비용, 대체 선택 중 하나가 있어야 한다.
- Ending은 `result_type`, `failure_kind`, `character_outcome` 의미를 변경하지 않는다.

## 3. Pack 1 Card Candidate +40

| # | Candidate ID Stem | Category | Slot Role | 연결 Quest Type | 효과 의도 |
|---:|---|---|---|---|---|
| 1 | `ask_old_vendor_about_pattern` | Local | risk_discovery | local_problem | money 또는 reputation 비용으로 clue 획득 |
| 2 | `inspect_shared_water_source` | Local | quest_progress | local_problem | progress + clue, time/food 비용 |
| 3 | `compare_household_rumors` | Local | risk_discovery | local_problem/investigation | false clue 위험 감소 |
| 4 | `offer_public_help` | Local | resource_alternative | local_problem/defense | reputation 상승, time 비용 |
| 5 | `search_back_alley_marks` | Local | quest_progress | local_problem | hidden route tag 획득 |
| 6 | `quiet_the_crowd` | Local | resource_alternative | local_problem | social hostility 완화 |
| 7 | `follow_the_small_witness` | Local | risk_discovery | local_problem | clue 획득, health/status 위험 |
| 8 | `map_conflicting_testimony` | Investigation | quest_progress | investigation/mystery | 핵심 단서 route 하나 확보 |
| 9 | `reconstruct_last_known_path` | Investigation | quest_progress | investigation | trail clue + progress |
| 10 | `test_the_false_signal` | Investigation | risk_discovery | mystery | omen 확인, risk 증가 가능 |
| 11 | `consult_old_case_notes` | Investigation | resource_alternative | investigation | time 비용으로 false lead 제거 |
| 12 | `trace_symbol_repetition` | Investigation | quest_progress | ruin/investigation | repeated mark clue |
| 13 | `interview_reluctant_witness` | Investigation | risk_discovery | social/investigation | reputation 비용, clue 획득 |
| 14 | `stage_a_small_decoy` | Investigation | resource_alternative | mystery | danger weight를 reveal로 전환 |
| 15 | `preserve_uncertain_evidence` | Investigation | resource_alternative | investigation | partial_success 방지 후보 |
| 16 | `raise_night_watch` | Defense | quest_progress | defense | defense progress + fatigue |
| 17 | `mark_weak_fence_line` | Defense | risk_discovery | defense/threat | attack omen 확인 |
| 18 | `move_children_to_cellar` | Defense | resource_alternative | defense | reputation/optional objective |
| 19 | `bait_the_threat_path` | Defense | risk_discovery | monster_hunt | clue + health risk |
| 20 | `count_missing_livestock` | Defense | quest_progress | investigation/threat | threat pattern clue |
| 21 | `prepare_quiet_signal` | Defense | resource_alternative | defense | future warning weight |
| 22 | `burn_false_trail` | Defense | resource_alternative | threat | danger weight 감소, money/food 비용 |
| 23 | `choose_sheltered_detour` | Travel | resource_alternative | travel/delivery/escort | food/time 비용으로 risk 감소 |
| 24 | `repair_load_straps` | Travel | quest_progress | delivery | progress + item loss 방지 |
| 25 | `listen_to_border_gossip` | Travel | risk_discovery | escort/delivery | social clue, reputation 비용 |
| 26 | `split_the_caravan_watch` | Travel | resource_alternative | escort | fatigue 비용, ambush omen 감소 |
| 27 | `read_weather_marks` | Travel | risk_discovery | survival/travel | storm omen 확인 |
| 28 | `secure_the_sealed_bag` | Travel | quest_progress | delivery | oath/parcel progress |
| 29 | `negotiate_safe_passage` | Travel | resource_alternative | escort | money 비용, path unlock |
| 30 | `tap_the_hollow_wall` | Ruin | risk_discovery | dungeon/ritual | hazard clue, trap risk |
| 31 | `copy_the_rune_sequence` | Ruin | quest_progress | ritual/investigation | ritual progress + clue |
| 32 | `brace_the_old_stairs` | Ruin | resource_alternative | dungeon | item/food 비용, health risk 감소 |
| 33 | `listen_beyond_the_seal` | Ruin | risk_discovery | ritual | omen 획득, curse risk |
| 34 | `test_the_ritual_component` | Ruin | quest_progress | ritual | progress + possible status cost |
| 35 | `leave_a_return_marker` | Ruin | resource_alternative | dungeon | future lost hazard 감소 |
| 36 | `find_dry_refuge` | Survival | resource_alternative | survival/exploration | health/food 보존 |
| 37 | `read_animal_silence` | Survival | risk_discovery | exploration | beast/weather omen |
| 38 | `ration_the_last_supplies` | Survival | resource_alternative | survival | food 보존, progress 지연 |
| 39 | `follow_water_insects` | Survival | quest_progress | exploration | hidden grove/path clue |
| 40 | `signal_from_high_ground` | Survival | quest_progress | exploration/travel | route progress + exposure risk |

## 4. Pack 1 Clue +25

| # | Clue ID Stem | Category | 연결 카드 예시 | 쓰임 |
|---:|---|---|---|---|
| 1 | `shared_cup_sediment` | Local | `inspect_shared_water_source` | well/poison 계열 판단 |
| 2 | `same_knot_on_three_doors` | Local | `compare_household_rumors` | repeated mark |
| 3 | `missing_market_tally` | Local | `ask_old_vendor_about_pattern` | 사회적 이상 징후 |
| 4 | `witness_changed_route` | Local | `follow_the_small_witness` | false signal 구분 |
| 5 | `cold_lantern_soot` | Investigation | `reconstruct_last_known_path` | lighthouse/ruin signal |
| 6 | `double_printed_footsteps` | Investigation | `trace_symbol_repetition` | 실종/변장 단서 |
| 7 | `scraped_symbol_edge` | Investigation | `preserve_uncertain_evidence` | ritual clue |
| 8 | `matching_salt_on_cloth` | Investigation | `interview_reluctant_witness` | travel/coast link |
| 9 | `unused_escape_rope` | Investigation | `consult_old_case_notes` | 선택지 unlock |
| 10 | `false_signal_interval` | Investigation | `test_the_false_signal` | omen payoff |
| 11 | `broken_fence_from_inside` | Defense | `mark_weak_fence_line` | threat direction |
| 12 | `ashes_without_heat` | Defense | `burn_false_trail` | unnatural threat |
| 13 | `livestock_refused_gate` | Defense | `count_missing_livestock` | animal warning |
| 14 | `watch_bell_struck_twice` | Defense | `prepare_quiet_signal` | attack timing |
| 15 | `wagon_axle_old_cut` | Travel | `repair_load_straps` | sabotage clue |
| 16 | `snow_filled_shortcut` | Travel | `read_weather_marks` | detour risk |
| 17 | `sealed_thread_shifted` | Travel | `secure_the_sealed_bag` | parcel temptation/payoff |
| 18 | `border_coin_mark` | Travel | `negotiate_safe_passage` | social route clue |
| 19 | `hollow_wall_echo` | Ruin | `tap_the_hollow_wall` | hidden hazard |
| 20 | `rune_sequence_gap` | Ruin | `copy_the_rune_sequence` | ritual partial 방지 |
| 21 | `old_stair_recent_dust` | Ruin | `brace_the_old_stairs` | ambush/trap clue |
| 22 | `seal_breaths_at_dusk` | Ruin | `listen_beyond_the_seal` | timed omen |
| 23 | `dry_moss_line` | Survival | `find_dry_refuge` | refuge path |
| 24 | `silent_bird_ring` | Survival | `read_animal_silence` | beast/storm omen |
| 25 | `insects_above_clean_water` | Survival | `follow_water_insects` | resource route |

## 5. Pack 1 Omen +20

| # | Omen ID Stem | Category | Warns About | Payoff 방향 |
|---:|---|---|---|---|
| 1 | `market_stalls_close_early` | Local | social_hostility | crowd card 가중치 변화 |
| 2 | `well_rope_wet_at_dawn` | Local | hidden_route | well/dungeon clue |
| 3 | `same_song_from_empty_house` | Local | anomaly | investigation event weight |
| 4 | `signal_light_skips_count` | Investigation | false_signal | direct progress risk |
| 5 | `witnesses_avoid_one_word` | Investigation | social_fear | bargain/interview payoff |
| 6 | `map_ink_moves_after_rain` | Investigation | route_shift | item/info card payoff |
| 7 | `dogs_face_the_old_road` | Defense | incoming_threat | watch/evacuate payoff |
| 8 | `fence_shadow_bends_inward` | Defense | breach | fortify card payoff |
| 9 | `no_crows_on_battlefield` | Defense | predator_or_curse | trap/scout payoff |
| 10 | `watch_fire_burns_blue` | Defense | ritual_threat | holy/info item payoff |
| 11 | `wagon_wheel_sings_low` | Travel | sabotage | repair/inspect payoff |
| 12 | `snow_falls_against_wind` | Travel | storm | detour/refuge payoff |
| 13 | `sealed_bag_warms_near_gate` | Travel | temptation | oath/parcel choice |
| 14 | `rune_glows_before_touch` | Ruin | trap_or_activation | copy/test payoff |
| 15 | `dust_moves_without_step` | Ruin | unseen_guardian | torch/listen payoff |
| 16 | `old_water_flows_uphill` | Ruin | seal_failure | ritual urgency |
| 17 | `bell_echo_arrives_first` | Ruin | time_loop | route/retreat payoff |
| 18 | `animal_paths_cross_twice` | Survival | lost | marker/map payoff |
| 19 | `clouds_hold_too_still` | Survival | sudden_weather | shelter payoff |
| 20 | `clean_water_tastes_of_smoke` | Survival | distant_fire | route pressure |

## 6. Pack 2 Item +25

| # | Item ID Stem | Role | Counters | 연결 후보 |
|---:|---|---|---|---|
| 1 | `waxed_thread_spool` | unlock | seal, parcel, trap | sealed bag / rune copy |
| 2 | `chalk_marker_set` | future_weight | lost, ruin, maze | return marker |
| 3 | `folding_probe_rod` | information | trap, hollow_wall | tap hollow wall |
| 4 | `oilcloth_map_case` | risk_reduce | rain, map_damage | weather/travel |
| 5 | `village_token` | cost_convert | social_hostility | reluctant witness |
| 6 | `small_signal_bell` | unlock | watch, ambush | defense warning |
| 7 | `dried_bitterroot` | risk_reduce | poison, hunger | well/survival |
| 8 | `mirror_shard` | information | darkness, false_signal | signal light |
| 9 | `ash_salt_pouch` | risk_reduce | curse, undead, ritual | blue fire/seal |
| 10 | `spare_wheel_pin` | unlock | wagon_break | repair straps |
| 11 | `warm_lantern_oil` | cost_convert | cold, darkness | ruin/travel |
| 12 | `reed_whistle` | unlock | lost, escort | high ground signal |
| 13 | `tarred_rope_hook` | unlock | cliff, well, wall | old stairs/well |
| 14 | `sealed_letter_copy` | information | intrigue, parcel | sealed parcel |
| 15 | `soft_boot_wraps` | risk_reduce | stealth, trap | investigation/ruin |
| 16 | `camp_tarp` | risk_reduce | storm, cold | dry refuge |
| 17 | `copper_listening_cup` | information | wall, seal | listen beyond seal |
| 18 | `red_thread_charm` | cost_convert | lost, fey | hidden grove |
| 19 | `spare_ration_cache` | cost_convert | hunger, delay | ration supplies |
| 20 | `beast_scent_tar` | risk_reduce | beast, predator | bait threat path |
| 21 | `ink_fixing_powder` | information | moving_map, rain | map ink omen |
| 22 | `smoke_cord` | future_weight | pursuit, bandit | burn false trail |
| 23 | `iron_nail_bundle` | unlock | door, barricade | fence/cellar |
| 24 | `clear_water_vial` | information | poison, smoke | water source |
| 25 | `oath_coin` | cost_convert | bargain, passage | safe passage |

## 7. Pack 2 Ending +8

| # | Ending ID Stem | 조건 방향 | 의미 |
|---:|---|---|---|
| 1 | `clear_report_return` | success + key clue + alive | 마을/의뢰자가 납득할 report |
| 2 | `costly_truth_return` | partial_success + clue + low resource | 진실은 얻었지만 대가가 큼 |
| 3 | `sealed_danger_left_behind` | success/partial + unresolved omen | 위협 예고가 남은 귀환 |
| 4 | `rescued_but_hunted` | rescue/escort + omen | 대상은 구했지만 추격이 붙음 |
| 5 | `rich_but_distrusted` | money high + reputation low | 보상은 크지만 평판 손상 |
| 6 | `prepared_frontier_route` | travel/exploration + future_weight item/clue | 다음 run에 안전 route 암시 |
| 7 | `ritual_interrupted_not_understood` | ruin/ritual partial + missing clue | 봉인은 막았지만 원리 미해석 |
| 8 | `survivor_without_answer` | failure/retreat + alive + no key clue | 생존했지만 사건은 미해결 |

## 8. Pack 실행 순서

1. Pack 1에서 Category별 Card Candidate를 먼저 추가한다.
2. 각 Card에 연결되는 Clue/Omen tag를 붙이고, Event Hint `card_candidate_hints`를 갱신한다.
3. active Quest scenario 중 대표 6개를 골라 Text MUD와 JSON에서 반복도, clue/omen 표시, partial_success reason을 확인한다.
4. Pack 2에서 Item을 추가한다.
5. Item choice가 항상 최적해가 아닌지 unavailable/available surface와 결과 비용으로 확인한다.
6. Ending 후보 8개를 조건별로 추가한다.
7. Standard Run 25-35 Turn으로 카드 반복, item 사용, ending 다양성을 검증한다.

## 9. Acceptance Gate

Pack 1 완료 조건:

- Card Candidate +40.
- Clue +25.
- Omen +20.
- 새 quest-specific Card/Event는 split file과 `quest_ids` gate 준수.
- 기존 Done Quest 회귀 통과.

Pack 2 완료 조건:

- Item +25.
- Ending +8.
- item choice는 item delta 또는 status/resource/event weight 차이를 만든다.
- ending은 기존 outcome 의미를 변경하지 않는다.

Standard Run 완료 조건:

- 25-35 Turn 동안 같은 카드 반복이 체감상 줄어든다.
- Clue/Omen이 Text MUD turn log와 Quest Report에서 판단 재료로 보인다.
- Item이 최소 5회 이상 선택지 availability나 결과를 바꾼다.
- Ending이 success/partial/failure run review를 분리한다.
