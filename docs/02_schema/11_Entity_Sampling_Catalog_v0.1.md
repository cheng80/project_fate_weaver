# Entity Sampling Catalog v0.1

## 1. 문서 목적

이 문서는 Content Expansion Phase 3에서 사용할 entity 후보 카탈로그다.

`docs/07_reviews/13_Entity_Sampling_Review_v0.1.md`가 선별 판단 문서라면, 이 문서는 실행자가 이벤트/아이템/단서/보상/비용 후보를 고를 때 참고하는 목록이다.

이 문서는 data schema를 바꾸지 않는다. 후보는 기존 YAML 구조와 Ontology-lite relation으로 표현 가능한 형태를 우선한다.

---

## 2. 사용 원칙

1. 후보를 고를 때 먼저 `채택 상태`를 확인한다.
2. `즉시 채택` 후보만 Phase 3 YAML 작성 대상으로 삼는다.
3. `조건부 채택` 후보는 같은 batch 안에서 choice/result 연결이 증명될 때만 쓴다.
4. `보류` 후보는 별도 계획 없이는 YAML화하지 않는다.
5. `거부` 조건에 걸리면 이름이 좋아도 사용하지 않는다.
6. NPC, faction, clue, reward, cost는 아직 독립 schema entity가 아니라 event/choice/result의 설계 범주다.

---

## 3. D&D/TRPG 참고 용어 정책

카탈로그 후보명은 FateWeaver 내부에서 안전하게 재사용할 수 있는 일반명이어야 한다.

사용 가능:

- 일반 판타지/민담/장르 공통 명사
- 숲, 폐허, 마을, 덫, 산적, 표식, 부적, 은닉처, 조난자 같은 보편 소재
- 탐험, 거래, 매복, 저주, 휴식, 굶주림, 길 잃음 같은 일반 상황명
- FateWeaver pack 안에서 새로 정의한 일반명

사용 금지:

- D&D/CoC 고유 설정명
- D&D/CoC 캐릭터명, 세계명, 지명, 조직명
- D&D/CoC 고유 몬스터명, 고유 종족명, 고유 신격명
- 원문 문장, 룰 텍스트, flavor text
- 특정 TRPG 시나리오를 식별할 수 있는 사건명, 주문명, 아이템명

재명명 규칙:

```text
애매하면 사용하지 않는다.
고유명은 FateWeaver식 일반 명사로 바꾼다.
역할이 드러나는 이름을 우선한다.
pack 테마인 신호/표식/길 잃음/저주/생존과 연결한다.
```

재명명 예:

| 차용 위험이 있는 방향 | 카탈로그용 일반명 |
|---|---|
| 특정 세계관 조직 | `false_rescuers`, `marker_keeper` |
| 특정 고유 괴물 | `beast_nearby`, `forest_response` |
| 특정 주문/마법명 | `resonance_lens`, `curse_drift` |
| 특정 시나리오명 | `false_signal`, `resource_cache` |

---

## 4. Relation 확장 정책

카탈로그 후보는 기존 Ontology-lite relation으로 표현하는 것을 기본값으로 한다.

기존 relation으로 설명되지 않는 관계가 반복적으로 필요하면 새 relation 추가를 허용한다. 단, 1회성 이벤트 때문에 relation을 추가하지 않는다.

Relation 추가 조건:

| 조건 | 설명 |
|---|---|
| 재사용성 | 2개 이상 이벤트/아이템/시나리오에서 재사용될 가능성이 있다. |
| 분석 가치 | validator, analyzer, export 중 하나 이상에서 의미가 있다. |
| 모호성 감소 | 기존 tag/status/result로 표현하면 의미가 더 모호해진다. |
| 지속성 | Content Expansion Phase 3 이후에도 유지 가능한 구조다. |

Relation 추가 시 함께 수정해야 하는 파일:

```text
data/core/ontology.yaml
docs/02_schema/09_Content_Ontology_Model_v0.1.md
```

Relation 추가를 거부하는 경우:

- 특정 이벤트 하나만 설명한다.
- 기존 relation 조합으로 충분히 설명된다.
- analyzer/export가 사용할 수 없는 장식적 관계다.
- relation 이름이 World Bible 설정을 전제로 한다.
- PRD나 별도 시스템 없이는 의미가 고정되지 않는다.

이번 카탈로그 기준:

```text
현재 후보는 모두 기존 relation으로 우선 표현한다.
새 relation 후보는 Phase 3 실행 후 반복 필요성이 확인될 때 별도 검토한다.
```

---

## 5. Entity 범주 카탈로그

| 범주 | schema entity 여부 | 채택 상태 | 표현 방식 |
|---|---:|---|---|
| event | 예 | 즉시 채택 | `events.yaml:events[]` |
| choice | 예 | 즉시 채택 | `events.yaml:choices[]` |
| result | 예 | 즉시 채택 | `choices[].result` |
| item | 예 | 조건부 채택 | `items.yaml:items[]` + `requires_item` |
| status | 예 | 기존만 채택 | `health`, `food`, `money`, `reputation`, `curse` |
| tag | 예 | 기존만 채택 | `tags.yaml`의 기존 tag |
| region | 예 | 기존만 채택 | `forest`, `village`, `ruin` |
| scenario | 예 | 실행 시 갱신 | `data/scenarios/content_expansion_test.yaml` |
| clue | 아니오 | design-only | description, investigate choice, result message, event_weight |
| reward | 아니오 | design-only | result status/item/event_weight |
| cost | 아니오 | design-only | result status/remove_item/event_weight |
| npc/faction | 아니오 | 보류 | description, choice, reputation, tag |
| pack theme | 아니오 | design-only | 반복 tag/item/result 문법 |

---

## 6. 이벤트 후보 카탈로그

| ID | 이름 | 원형 | 권장 태그 | 채택 상태 | YAML화 기준 |
|---|---|---|---|---|---|
| `threshold_crossing` | 문턱/경계 통과 | threshold | exploration, magic, lost | 즉시 채택 | 안전 관찰, 위험 통과, item 고정 선택을 둔다. |
| `route_obstacle` | 길 위의 장애물 | obstacle | exploration, survival, trap | 즉시 채택 | food/health tradeoff와 우회 선택을 둔다. |
| `clue_discovery` | 단서 발견 | discovery | exploration, magic, curse | 즉시 채택 | investigate choice가 future weight를 바꿔야 한다. |
| `false_signal` | 거짓 신호 | omen/trap | exploration, combat, bandit | 즉시 채택 | 확인 선택과 돌진 선택의 결과 차이가 커야 한다. |
| `resource_cache` | 은닉처/보급품 | aftermath/refuge | survival, trade, trap | 즉시 채택 | 보상과 reputation 또는 trap 비용을 묶는다. |
| `curse_contamination` | 오염/저주 접촉 | contamination | curse, magic, ancient | 즉시 채택 | curse 감소/증가 양쪽 선택을 둔다. |
| `refuge_rest` | 피난처/휴식 | refuge | rest, survival, hunger | 즉시 채택 | health 회복과 food/time 비용을 묶는다. |
| `ambush_standoff` | 매복/대치 | ambush | combat, trade, physical | 즉시 채택 | retreat, bribe/negotiate, item response를 둔다. |
| `social_bargain` | 사회적 거래 | bargain | trade, village | 조건부 채택 | money/reputation이 실제 result로 바뀔 때만 쓴다. |
| `long_mystery_chain` | 장기 미스터리 | chain | magic, curse | 보류 | clue 누적 시스템이 필요하다. |
| `boss_duel` | 보스 대결 | combat | combat, physical | 보류 | 별도 전투 루프를 유도한다. |
| `city_politics` | 도시 정치 | social | village, trade | 보류 | faction schema 없이는 설명문이 길어진다. |

---

## 7. Threat 후보 카탈로그

| ID | 이름 | 기존 tag 표현 | 채택 상태 | 대응 방식 |
|---|---|---|---|---|
| `lost_route` | 길 잃음 | `lost` | 즉시 채택 | mark, observe, signal item |
| `snare_trap` | 덫 | `trap`, `physical` | 즉시 채택 | slow safe choice, health risk, tool |
| `bandit_pressure` | 산적 압력 | `bandit`, `physical` | 즉시 채택 | retreat, bribe, smoke/flare item |
| `hunger_clock` | 식량 소모 | `hunger` | 즉시 채택 | forage, ration, detour cost |
| `curse_drift` | 저주 누적 | `curse`, `ancient` | 즉시 채택 | avoid, cleanse, risky reward |
| `darkness_blind` | 시야 제한 | `darkness` | 즉시 채택 | torch, mirror, observe |
| `beast_nearby` | 짐승 접근 | `beast`, `physical` | 조건부 채택 | combat이 아니라 생존/회피 선택으로 쓴다. |
| `false_help` | 거짓 도움 | `lost`, `bandit`, `trap` | 즉시 채택 | investigate로 식별 가능해야 한다. |
| `storm_exposure` | 폭풍 노출 | `storm` | 보류 | signal grove pack 핵심과 약하다. |
| `undead_attack` | 언데드 위협 | `undead` | 보류 | 현재 pack 테마와 거리가 있다. |
| `mental_break` | 정신 붕괴 | 없음 | 거부 | 새 status 또는 원전식 정신력 차용 위험이 있다. |

---

## 8. 아이템 후보 카탈로그

| ID | 이름 | 역할 | 태그 | 대응 위험 | 채택 상태 | 사용 조건 |
|---|---|---|---|---|---|---|
| `signal_chalk` | 신호 분필 | information, future_weight | tool, travel | lost, trap | 즉시 채택 | 최소 2개 choice를 열고 직접 피해 감소는 하지 않는다. |
| `resonance_lens` | 공명 렌즈 | information, risk_reduce | tool | curse, ancient, darkness | 즉시 채택 | clue reveal 중심으로 쓰고 curse 감소는 제한한다. |
| `waybread_pouch` | 길양식 주머니 | cost_convert, risk_reduce | consumable, travel | hunger, lost | 즉시 채택 | consume_item으로 food/health 비용을 전환한다. |
| `broken_compass_needle` | 부러진 방향침 | information, probability | tool, travel | lost, ancient | 조건부 채택 | probability 역할 검증이 필요할 때만 쓴다. |
| `herbal_bandage` | 말린 약초 붕대 | risk_reduce | consumable, healing | physical, beast | 조건부 채택 | healing item 남용 없이 1회성으로 쓴다. |
| `map_of_every_path` | 만능 지도 | information | tool, travel | lost | 거부 | lost 위험을 지나치게 무력화한다. |
| `perfect_curse_charm` | 완전 정화 부적 | risk_reduce | holy | curse | 거부 | curse 선택을 단순 정답으로 만든다. |
| `named_weapon` | 고유 무기 | risk_reduce | weapon | bandit, beast | 보류 | combat subsystem을 유도할 수 있다. |

---

## 9. Status 후보 카탈로그

| ID | 이름 | 채택 상태 | 표현 방식 | 판단 |
|---|---|---|---|---|
| `health` | 체력 | 즉시 채택 | 기존 status | 물리 피해와 회복을 표현한다. |
| `food` | 식량 | 즉시 채택 | 기존 status | 시간/우회/휴식 비용을 표현한다. |
| `money` | 돈 | 즉시 채택 | 기존 status | 거래/뇌물/욕심 보상을 표현한다. |
| `reputation` | 평판 | 즉시 채택 | 기존 status | 사회적 결과와 약탈 비용을 표현한다. |
| `curse` | 저주 | 즉시 채택 | 기존 status | magic/ancient/forbidden 위험을 표현한다. |
| `fear` | 공포 | 보류 | `curse`로 대체 | 새 심리 수치는 아직 필요 없다. |
| `fatigue` | 피로 | 보류 | `food`, `health`로 대체 | 생존 압력과 역할이 겹친다. |
| `trust` | 신뢰 | 보류 | `reputation`으로 대체 | faction schema가 없으면 좁다. |
| `clue_progress` | 단서 진행도 | 보류 | `event_weight`, item unlock | clue 누적 시스템 전까지 보류한다. |
| `light` | 빛 | 보류 | item + `darkness` tag | 별도 상태보다 item relation이 낫다. |
| `weather_exposure` | 날씨 노출 | 보류 | `storm`, `food`, `health` | 현재 pack 핵심과 약하다. |

---

## 10. Clue 후보 카탈로그

| ID | 이름 | 표현 방식 | 채택 상태 | 쓰임 |
|---|---|---|---|---|
| `repeated_mark` | 반복 표식 | description + investigate result | 즉시 채택 | lost/curse 패턴 판단 |
| `sound_interval` | 소리 간격 | investigate choice | 즉시 채택 | timing/route 판단 |
| `smoke_pattern` | 연기 패턴 | investigate + bandit weight | 즉시 채택 | false signal 판별 |
| `knot_rule` | 매듭 규칙 | investigate + village/trade weight | 즉시 채택 | route/social 연결 |
| `track_depth` | 발자국 깊이 | investigate + survival/lost weight | 즉시 채택 | 생존 경로 판단 |
| `sap_variation` | 수액 차이 | risky investigate + curse/reputation | 즉시 채택 | curse cost와 정보 보상 |
| `insect_pattern` | 벌레 빛 배열 | magic/lost weight | 즉시 채택 | magic clue와 위험 유혹 |
| `mirror_anomaly` | 거울 반사 이상 | item_based reveal | 즉시 채택 | darkness/curse 해석 |
| `long_journal` | 장문 일지 | description | 보류 | 로그 정보량이 과해질 수 있다. |
| `cipher_system` | 암호 체계 | 별도 진행도 필요 | 보류 | clue_progress 없이 단발 설명이 된다. |

---

## 11. Reward 후보 카탈로그

| ID | 이름 | YAML 표현 | 채택 상태 | 주의 |
|---|---|---|---|---|
| `food_gain` | 식량 회복 | `status: {food: +1}` | 즉시 채택 | 너무 자주 주면 survival 압력이 약해진다. |
| `health_gain` | 체력 회복 | `status: {health: +1}` | 즉시 채택 | rest 비용과 묶는다. |
| `money_gain` | 돈 획득 | `status: {money: +1}` | 즉시 채택 | curse/health/reputation 비용과 묶는다. |
| `reputation_gain` | 평판 획득 | `status: {reputation: +1}` | 즉시 채택 | 사회적 후속 weight와 연결하면 좋다. |
| `curse_reduce` | 저주 감소 | `status: {curse: -1}` | 즉시 채택 | 항상 정답이 되지 않게 비용을 둔다. |
| `danger_weight_down` | 위험 weight 감소 | `event_weight: {lost: -1}` | 즉시 채택 | safe/investigate 보상에 적합하다. |
| `route_weight_up` | route weight 증가 | `event_weight: {village: +1}` | 즉시 채택 | 다음 이벤트 풀을 바꾼다. |
| `item_unlock` | 아이템 해금 | item result 또는 requires 연결 | 조건부 채택 | dead item이 되지 않아야 한다. |
| `xp_level` | 경험치/레벨 | 새 시스템 필요 | 거부 | 현재 Console Validation 범위를 넘는다. |
| `permanent_power` | 영구 능력 | 새 성장 시스템 필요 | 거부 | Phase 3에 과하다. |

---

## 12. Cost 후보 카탈로그

| ID | 이름 | YAML 표현 | 채택 상태 | 쓰임 |
|---|---|---|---|---|
| `food_cost` | 시간/우회 비용 | `status: {food: -1}` | 즉시 채택 | safe/detour choice |
| `health_cost` | 부상 | `status: {health: -1}` | 즉시 채택 | risky/physical choice |
| `curse_cost` | 저주 증가 | `status: {curse: +1}` | 즉시 채택 | forbidden/gamble choice |
| `money_cost` | 돈 지출 | `status: {money: -1}` | 즉시 채택 | trade/bribe choice |
| `reputation_cost` | 평판 손상 | `status: {reputation: -1}` | 즉시 채택 | exploit/steal choice |
| `item_consume` | 아이템 소모 | `consume_item: true`, `remove_item` | 즉시 채택 | 강한 item choice 제한 |
| `danger_weight_up` | 미래 위험 증가 | `event_weight: {curse: +1}` | 즉시 채택 | delayed consequence |
| `lost_weight_up` | 길 잃음 증가 | `event_weight: {lost: +1}` | 즉시 채택 | shortcut/rush choice |
| `instant_death` | 즉사 | fail state | 거부 | profile 비교와 반복 검증을 망친다. |
| `permanent_lock` | 영구 잠금 | 장기 상태 필요 | 거부 | 현재 run loop에 과하다. |

---

## 13. NPC/세력/Faction 후보 카탈로그

| ID | 이름 | 채택 상태 | 표현 방식 | 쓰임 |
|---|---|---|---|---|
| `marker_keeper` | 표식 관리자 | 즉시 채택 | trade choice + reputation | 길값, 경고, village weight |
| `false_rescuers` | 가짜 구조 무리 | 즉시 채택 | bandit/trap tag | 함정, 매복, 거짓 단서 |
| `lost_survivor_trace` | 조난자 흔적 | 즉시 채택 | aftermath event | 도움/약탈/reputation tradeoff |
| `cache_owner` | 은닉처 주인 | 즉시 채택 | cache event result | food reward와 reputation cost |
| `village_signal_network` | 마을 구조망 | 즉시 채택 | village/trade weight | signal item payoff |
| `forest_response` | 숲의 반응 | 즉시 채택 | magic/curse/lost tag | NPC 없이 mystery 압력 |
| `named_mentor` | 명명된 안내자 | 보류 | 별도 설정 필요 | World Bible로 확장될 위험 |
| `faction_reputation_table` | 세력 평판표 | 보류 | 새 schema 필요 | core/status 확장 유혹 |
| `long_term_companion` | 장기 동료 | 거부 | companion system 필요 | 현재 범위 초과 |

---

## 14. Pack 테마 후보 카탈로그

| ID | 테마 | 채택 상태 | 반복 재료 | 검증 관계 |
|---|---|---|---|---|
| `signals_and_marks` | 신호와 표식 | 즉시 채택 | 호루라기, 거울, 리본, 분필, 매듭 | `choice_requires_item`, `result_changes_event_weight` |
| `lost_and_return` | 길 잃음과 되돌아옴 | 즉시 채택 | lost, fork, marker, trail | `event_has_danger_tag`, `event_weight` |
| `false_rescue` | 거짓 구조 신호 | 즉시 채택 | smoke, bandit, trap, reputation | `event_has_danger_tag`, `result_modifies_status` |
| `survival_ethics` | 생존의 윤리 | 즉시 채택 | ration, cache, survivor, reputation | `result_modifies_status` |
| `curse_interpretation` | 저주와 해석 실패 | 즉시 채택 | curse, ancient, forbidden, magic clue | `event_has_danger_tag`, `result_changes_event_weight` |
| `light_and_visibility` | 빛과 시야 | 즉시 채택 | darkness, mirror, flare, insects | `item_counters_tag`, item reveal |
| `city_intrigue` | 도시 정치극 | 보류 | named NPC, faction | 현재 pack과 멀다. |
| `mega_dungeon` | 거대 던전 | 보류 | floors, map, boss | 별도 구조가 필요하다. |
| `mythic_entity` | 고유 신화 존재 | 거부 | unique lore | World Bible과 원전 차용 위험 |

---

## 15. YAML화 우선순위

Phase 3 실행 시 우선순위:

1. `threshold_crossing`, `route_obstacle`, `clue_discovery`, `false_signal`
2. `resource_cache`, `curse_contamination`, `refuge_rest`, `ambush_standoff`
3. `signal_chalk`, `resonance_lens`, `waybread_pouch`
4. clue 후보 중 `repeated_mark`, `sound_interval`, `smoke_pattern`, `knot_rule`
5. survival/greedy cost-reward 조합

우선순위에서 제외:

```text
새 status
새 core tag
명명된 주요 NPC
복수 faction 평판표
별도 combat system
장기 clue_progress system
World Bible이 필요한 고유 설정
```

---

## 16. Reject 기준

후보가 아래 조건 중 하나라도 만족하면 Phase 3에서는 reject한다.

- `event_has_choice`, `choice_produces_result`, `result_modifies_status` 중 하나도 설명하지 못한다.
- 새 core status 또는 새 core tag가 선행되어야 한다.
- 새 relation을 요구하지만 relation 추가 조건을 만족하지 못한다.
- item이 없으면 진행이 막힌다.
- item이 있으면 항상 최적해가 된다.
- 단서가 다음 선택 판단에 쓰이지 않는다.
- 보상과 비용이 result에 반영되지 않는다.
- combat을 별도 턴제 전투로 만들게 한다.
- NPC/faction schema를 만들지 않으면 의미가 없다.
- 원문 TRPG 설정, 고유명, 문장, 룰을 차용해야만 설명된다.
- PRD 또는 World Bible 작성이 선행되어야 한다.

---

## 17. Phase 3 작성 전 체크리스트

```text
[ ] 선택한 후보가 즉시 채택 또는 조건부 채택 상태인가?
[ ] 기존 status 5개로 표현 가능한가?
[ ] 기존 tag로 표현 가능한가?
[ ] 이벤트마다 최소 2개 meaningful choice가 있는가?
[ ] item choice에 non-item 대안이 있는가?
[ ] clue가 다음 선택 판단에 쓰이는가?
[ ] reward와 cost가 result에 반영되는가?
[ ] NPC/세력은 독립 schema가 아니라 사건 역할로 표현되는가?
[ ] Ontology-lite relation으로 설명 가능한가?
[ ] 새 relation이 필요하다면 2개 이상 콘텐츠에서 재사용되는가?
[ ] relation 추가 시 `data/core/ontology.yaml`과 `09_Content_Ontology_Model` 갱신 계획이 있는가?
[ ] 원전 설정/고유명/문장을 차용하지 않았는가?
```
