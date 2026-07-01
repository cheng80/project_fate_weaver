# [Current] Standard Run Play Quality Audit v0.1

> 상태: [Current] Standard Run 25~35 Turn 검증 이후, 실제 Text MUD / JSON 로그를 기준으로 플레이 품질을 감사한 문서.

## 1. 작업 목적

이번 감사는 구현 통과 여부가 아니라, `standard_run_25_35_turn`이 실제 텍스트 모험 게임처럼 읽히는지 확인한다.

감사 질문은 다음이다.

- Quest 목적이 25턴 동안 유지되는가?
- 매 Turn 3장 선택지가 의미 있게 다르게 느껴지는가?
- Card 반복은 플레이 감각상 허용 가능한가?
- Clue / Omen / Item / Ending이 자연스럽게 연결되는가?
- Ontology / Situation Director가 상황 전개를 이끄는 느낌이 있는가?
- resource / economy / reputation / score가 선택 압박과 결과 의미를 만드는가?

이번 문서는 감사 문서다. data, src, tests, Quest, Card, Event, Item, Ending, Balance 수치, Text MUD 문구는 수정하지 않았다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/14_Ontology_Core_Model_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/07_reviews/45_Standard_Run_25_35_Turn_Verification_Result_v0.1.md`
- `docs/07_reviews/47_Ontology_Core_To_Director_Loop_Result_v0.1.md`
- `docs/07_reviews/48_Card_Candidate_Repetition_Gate_Result_v0.1.md`
- `data/scenarios/standard_run_25_35_turn.yaml`

## 3. 감사 대상 Evidence

Primary evidence:

- `.omo/ulw-loop/evidence/card-candidate-repetition-gate-20260701/standard_run_after.json`
- `.omo/ulw-loop/evidence/card-candidate-repetition-gate-20260701/standard_run_after_text_mud.txt`
- `.omo/ulw-loop/evidence/card-candidate-repetition-gate-20260701/standard_run_after_summary.json`
- `.omo/ulw-loop/evidence/card-candidate-repetition-gate-20260701/verification.txt`

Reference baseline:

- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/standard_run.json`
- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/standard_run_text_mud.txt`
- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/standard_run_summary.json`

Audit summary artifact:

- `.omo/ulw-loop/evidence/standard-run-play-quality-audit-20260701/evidence_summary.txt`

## 4. Standard Run 요약

| 항목 | 관찰값 |
|---|---:|
| Scenario | `standard_run_25_35_turn` |
| Active Quest | `survive_the_storm_pass` |
| Quest Title | `폭풍 산길 생존 귀환` |
| Turn Count | 25 |
| Final Day | 7 |
| Result Type | `success` |
| Ending ID | `prepared_frontier_route` |
| Score | 649 |
| Final Health | 9 |
| Final Food | 1 |
| Final Money | 24 |
| Final Reputation | 5 |
| Unique Presented Cards | 18 |
| Unique Selected Cards | 10 |
| Ontology Weight Applied Turns | 19 |

Top repeated presented cards after repetition tuning:

| Card | Count |
|---|---:|
| `ration_the_last_supplies` | 10 |
| `buy_local_hint` | 7 |
| `inspect_tracks` | 7 |
| `rest_briefly` | 6 |
| `enter_deep_woods` | 6 |
| `report_to_apothecary` | 6 |
| `ask_apothecary` | 5 |
| `read_departure_signs` | 5 |
| `return_to_village` | 5 |
| `search_herbs` | 4 |

Storylet distribution:

| Storylet | Count |
|---|---:|
| `suspicious_merchant` | 10 |
| `storm_pass_shelter_hint` | 7 |
| `storm_pass_pack1_enrichment` | 4 |
| `hunger_night` | 2 |
| `sudden_storm` | 2 |

Resource delta over the run:

| Resource | Delta |
|---|---:|
| health | 0 |
| food | -8 |
| money | +20 |
| reputation | +4 |
| curse | 0 |

## 5. Quest Purpose Continuity

등급: C+

초반 목적은 명확하다. Turn 1~3에서 `read_storm_pass_sky`, `secure_storm_shelter`, `return_from_storm_pass`가 제시되고 선택되며, 피난처 발견, 생존로 확보, 귀환 목표가 빠르게 연결된다. Text MUD도 Quest, Region, 상태, 발생 사건, 카드, 선택 결과, Quest Progress를 매 Turn 표시한다.

약점은 목적 완결 이후다. Turn 3에 이미 `storm_pass_returned=1`, `storm_shelter_found=1`, `survival_route_secured=1`이 찍힌 뒤에도, min-turn gate 때문에 25턴까지 run이 이어진다. 이후에는 `ask_apothecary`, `search_herbs`, `return_to_village`, `report_to_apothecary`가 반복되며 `폭풍 산길 생존 귀환`보다 약초 튜토리얼 루프처럼 읽힌다.

판정: 기능상 Quest 목적은 유지되지만, 플레이 감각상 중반 이후 목적이 흐려진다.

## 6. Choice Meaningfulness

등급: B-

3장 구조 자체는 안정적이다. 매 Turn `quest_progress`, `risk_discovery`, `resource_alternative` 슬롯이 모두 제시된다. 예를 들어 초반에는 `산길 하늘을 읽는다`, `돈으로 숲길 정보를 산다`, `잠시 쉰다`가 각각 목적 진행, 정보 구매, 회복/식량 비용을 담당한다.

선택의 실제 결과도 JSON에는 충분히 남는다. `selected_cards`, `card_candidate_pool`, `selected_choice_reason`, `state_before`, `state_after`, `score_change`, `next_event_tags`가 있어 디버깅 가능하다. Multi-Select도 Turn 5에서 `search_herbs + use_torch_to_search` 조합이 자연스럽게 동작한 흔적이 있다.

약점은 자동 선택감이다. 선택된 카드 25회 중 25회가 `quest_progress` 슬롯이고, 추가로 한 번만 combo의 `resource_alternative`가 붙었다. 위험 감수 카드와 자원 대체 카드는 의미 있는 옵션으로 보이지만, 실제 autoplayer 선택은 거의 항상 안전한 목적 진행 카드로 수렴한다.

판정: 선택지는 의미가 있으나, 선택 압력과 trade-off 체감은 아직 약하다.

## 7. Narrative Flow

등급: C+

초반 흐름은 좋다. 하늘을 읽어 피난처를 찾고, 피난처를 확보하고, 폭풍 산길에서 귀환하는 1~3턴은 Event → Card → Result → Next Situation이 명확히 이어진다. Item-gated 카드인 `signal_from_high_ground`, `find_dry_refuge`도 storm-pass 문맥을 보강한다.

중반 이후는 루프성이 강하다. `약사에게 의뢰를 확인한다`, `약초를 찾는다`, `마을로 돌아간다`, `약사에게 보고한다`가 반복되며 이미 완료된 보고와 귀환이 다시 진행된다. Text MUD의 결과 문장은 읽을 수 있지만, 사건이 누적되어 새 장면으로 전환된다는 느낌보다 진행 카드 목록을 반복 소비하는 느낌이 강하다.

판정: 로그는 모험 기록 형식을 갖췄지만, 중반 이후 장면 전환과 후속 사건 연결이 약하다.

## 8. Variety / Repetition

등급: B-

반복 튜닝 이후 수치상 개선은 분명하다.

| Metric | Before | After |
|---|---:|---:|
| Unique Presented Cards | 16 | 18 |
| Unique Selected Cards | 10 | 10 |
| Top Repeated Card | 15 | 10 |
| `buy_local_hint` Count | 13 | 7 |

평가기준상 top repeated card 10회는 Acceptable 범위다. `ration_the_last_supplies`가 생존/식량 문맥이라 storm-pass run에서 반복되는 것도 어느 정도 납득 가능하다.

하지만 실제 읽기에서는 카드보다 storylet 반복이 더 크게 보인다. `suspicious_merchant` 10회, `storm_pass_shelter_hint` 7회가 25턴의 대부분을 차지한다. 카드 반복은 낮아졌지만 장면 반복과 quest-progress 카드 반복이 여전히 플레이 피로를 만든다.

판정: Card repetition은 허용선에 들어왔지만, Storylet / objective action 반복은 다음 개선 대상이다.

## 9. Ontology / Director Feel

등급: C+

JSON에는 director 흔적이 있다. `ontology_inference`, `ontology_weight_applied`, `situation_intents`, `next_event_tags`, `repeat_memory_snapshot`, `repeat_memory_after`가 turn마다 남고, ontology weight는 25턴 중 19턴에서 적용된다.

체감은 약하다. Standard Run summary의 `ontology_card_modifier_applied_count`는 0이고, 카드 선택 체감은 ontology rule보다 quest_progress slot과 fallback/shared 후보가 주도한다. `intent.shelter_search`, `intent.mystery_probe` 같은 intent가 반복적으로 보이지만, 플레이어 관점에서는 새로운 상황 연출보다 같은 storylet pool 안에서 반복 선택되는 느낌이 강하다.

판정: 디버그 trace는 생겼으나, DM처럼 상황을 밀어주는 체감은 아직 약하다.

## 10. Resource / Economy / Reputation Pressure

등급: C+

Food 압박은 존재한다. 최종 food는 1이고 run 전체 food delta는 -8이다. `keep_food` optional objective도 1/1로 완료되어 생존 자원 체크가 Quest Report에 반영된다.

Economy와 reputation은 압박보다 보상 누적에 가깝다. money는 4에서 24로 증가했고, reputation은 1에서 5로 증가했다. `buy_local_hint`는 money를 쓰는 risk_discovery 카드지만 실제 선택되지 않았고, `report_to_apothecary` 반복으로 money/reputation 보상이 과하게 누적된다. Score도 `quest_progress=270`, `ending_bonus=132`, `reputation=44`가 커서 반복 보고가 결과 의미를 부풀린다.

판정: food는 압박을 만들지만, money/reputation/score는 아직 결말 의미보다 반복 보상처럼 보인다.

## 11. Ending / Quest Report Quality

등급: B

Quest Report는 이해 가능하다. result type, failure kind, character outcome, completed objectives, score breakdown, resource summary, ending id가 모두 표시된다. `prepared_frontier_route`는 alive, clue, 준비 아이템 조건과 연결되어 storm-pass 생존 귀환 결과로 납득된다.

약점은 결말까지의 여정이다. Ending 자체는 맞지만, Turn 3 이후 반복 보고와 약초 루프가 길게 이어져 최종 `prepared_frontier_route`가 "25턴 동안 준비한 변경의 길"이라기보다 이미 성공한 run을 min-turn까지 연장한 결산처럼 느껴진다.

판정: Report 형식과 Ending 조건은 좋다. Ending의 체감 설득력은 중반부 narrative/director polish에 의존한다.

## 12. 종합 평가

| 항목 | 등급 | 근거 |
|---|---|---|
| Quest Purpose Continuity | C+ | 초반 목적은 강하지만 Turn 3 이후 목적이 흐려진다. |
| Choice Meaningfulness | B- | 3-slot 선택지는 유지되나 실제 선택은 quest_progress로 수렴한다. |
| Narrative Flow | C+ | 초반 flow는 좋고 중후반은 반복 장면이 강하다. |
| Variety / Repetition | B- | top repeated card 10회로 허용선이나 storylet 반복이 남는다. |
| Ontology / Director Feel | C+ | trace는 있으나 플레이 체감 변화는 약하다. |
| Resource / Economy / Reputation Pressure | C+ | food 압박은 있으나 money/reputation은 보상 누적으로 보인다. |
| Ending / Quest Report Quality | B | Report와 Ending은 이해 가능하나 여정 설득력이 약하다. |

종합 판정: Playable but needs polish

현재 Standard Run은 기능 검증용으로는 충분하다. 실제 플레이 품질 기준에서는 "플레이 가능한 로그"까지 왔지만, 25턴 모험으로 읽히려면 Storylet Pool Expansion과 Director Tuning 2차가 먼저 필요하다.

## 13. 주요 문제

1. Quest completion 이후 반복 진행
   - Turn 3에 storm-pass 핵심 목표가 완료되지만, min-turn gate 때문에 완료 카드와 보고 카드가 반복된다.

2. Storylet 반복이 card 반복보다 더 크게 느껴짐
   - `suspicious_merchant` 10회, `storm_pass_shelter_hint` 7회는 Text MUD에서 장면 피로를 만든다.

3. Autoplayer 선택이 quest_progress로 과도하게 수렴
   - 25턴 모두 quest_progress 카드가 선택되어 risk_discovery/resource_alternative의 체감 선택 의미가 약하다.

4. Ontology / Director가 trace에 비해 체감 약함
   - ontology event weighting은 보이지만, card modifier는 Standard Run에서 0회이며 situation intent 변화가 장면 전환으로 충분히 느껴지지 않는다.

5. Economy / reputation 보상 반복
   - `report_to_apothecary` 반복으로 money와 score가 과하게 증가해 결과 의미를 흐린다.

## 14. 다음 개선 우선순위

1. Option B. Storylet Pool Expansion
   - 가장 먼저 필요하다. 현재 반복 피로의 핵심은 card 수보다 25턴을 지탱할 storylet follow-up 부족이다.
   - 우선 대상: post-shelter follow-up, post-return village consequence, storm escalation, safe path consequence, clue/omen follow-up.

2. Option D. Director Tuning 2차
   - Storylet 후보가 늘어난 뒤 director가 completed objective, repeat_group, next_event_tags, situation_intents를 보고 다음 장면을 더 강하게 회전시켜야 한다.
   - 우선 대상: quest_complete 이후 반복 보고 억제, completed objective follow-up 전환, ontology card modifier seed coverage.

3. Option A. Gameplay Balance Pass
   - money/reputation/score 반복 보상과 food 압박을 조정한다.
   - 단, 수치 조정만으로 장면 반복은 해결되지 않으므로 3순위가 적절하다.

4. Option C. Text MUD Narrative Polish
   - 문구 polish는 효과가 있지만, 현재 문제는 문장보다 사건 구조 반복이 먼저다.
   - Storylet/Director 개선 후 반복 문장과 Quest Report wording을 다듬는 편이 낫다.

## 15. 추천 후속 작업

- `CODEX_TASK_Storylet_Pool_Expansion_Post_Standard_Run_v0.1`
  - Standard Run 25턴을 위한 storm-pass post-completion / village consequence / clue follow-up storylet을 소량 추가한다.

- `CODEX_TASK_Director_Tuning_Completed_Objective_Rotation_v0.1`
  - completed objective와 quest_complete tag가 반복 진행 카드를 다시 고르지 않도록 Director-lite event/card rotation을 조정한다.

- `CODEX_TASK_Economy_Reputation_Score_Pressure_Audit_v0.1`
  - 반복 보고 보상 누적, money sink 부족, score breakdown 과대 누적을 별도 감사한다.

- `CODEX_TASK_Text_MUD_Report_Polish_After_Director_v0.1`
  - 구조 반복이 줄어든 뒤 Quest Report와 Ending 문구를 실제 playtest 로그 기준으로 다듬는다.
