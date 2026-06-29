# Entity Sampling Catalog v0.1

## 1. 문서 목적

이 문서는 Content Expansion Phase 3에서 사용할 entity 후보 카탈로그다.

`docs/07_reviews/13_Entity_Sampling_Review_v0.1.md`가 선별 판단 문서라면, 이 문서는 실행자가 이벤트/아이템/단서/보상/비용 후보를 고를 때 참고하는 목록이다.

이 문서는 Phase 3 후보를 고르는 기준이다. v0.2부터는 `clue`, `location`, `omen`, `hazard`를 trial entity로 다루며, 관련 YAML field는 Phase 3에서 사용성을 검증하기 위한 선택 필드다.

---

## 2. 사용 원칙

1. 후보를 고를 때 먼저 `채택 상태`를 확인한다.
2. `즉시 채택` 후보만 Phase 3 YAML 작성 대상으로 삼는다.
3. `조건부 채택` 후보는 같은 batch 안에서 choice/result 연결이 증명될 때만 쓴다.
4. `보류` 후보는 별도 계획 없이는 YAML화하지 않는다.
5. `거부` 조건에 걸리면 이름이 좋아도 사용하지 않는다.
6. NPC, faction, reward, cost는 아직 독립 schema entity가 아니라 event/choice/result의 설계 범주다.
7. `clue`, `location`, `omen`, `hazard`는 v0.2 trial entity이며, Phase 3 이후 유지/제거/통합을 다시 판단한다.

---

## 3. D&D/TRPG 참고 용어 정책

카탈로그 후보명은 FateWeaver 내부에서 안전하게 재사용할 수 있는 일반명이어야 한다.

사용 가능:

- 일반 판타지/민담/장르 공통 명사
- 숲, 폐허, 마을, 덫, 산적, 표식, 부적, 은닉처, 조난자 같은 보편 소재
- 탐험, 거래, 매복, 상태 악화, 휴식, 굶주림, 길 잃음 같은 일반 상황명
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
pack 테마인 장소 탐험, 신호/표식, 길 잃음, 생존 압박, 상태 위험과 연결한다.
```

재명명 예:

| 차용 위험이 있는 방향 | 카탈로그용 일반명 |
|---|---|
| 특정 세계관 조직 | `false_rescuers`, `marker_keeper` |
| 특정 고유 괴물 | `beast_nearby`, `forest_response` |
| 특정 주문/마법명 | `resonance_lens`, `status_drift` |
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
기존 relation으로 충분한 후보는 기존 relation으로 표현한다.
clue, location, omen, hazard 계열은 v0.2 trial field로 최소 검증한다.
trial relation은 Phase 3 이후 반복 필요성이 낮으면 제거하거나 통합한다.
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
| clue | v0.2 trial | trial 채택 | `revealed_clue_tags`, `reveals_clue_tags` |
| location | v0.2 trial | trial 채택 | `location_tags` |
| omen | v0.2 trial | trial 채택 | `omen_tags`, `creates_omen_tags` |
| hazard | v0.2 trial | trial 채택 | `hazard_tags`, `counters_hazard_tags` |
| region | 예 | 기존만 채택 | `forest`, `village`, `ruin` |
| scenario | 예 | 실행 시 갱신 | `data/scenarios/content_expansion_test.yaml` |
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
| `clue_discovery` | 단서 발견 | discovery | exploration, magic, hazard | 즉시 채택 | investigate choice가 future weight를 바꿔야 한다. |
| `false_signal` | 거짓 신호 | omen/trap | exploration, combat, bandit | 즉시 채택 | 확인 선택과 돌진 선택의 결과 차이가 커야 한다. |
| `resource_cache` | 은닉처/보급품 | aftermath/refuge | survival, trade, trap | 즉시 채택 | 보상과 reputation 또는 trap 비용을 묶는다. |
| `status_contamination` | 상태 오염 접촉 | contamination | curse, magic, ancient | 즉시 채택 | curse 같은 위험 상태의 증감 선택을 둔다. |
| `refuge_rest` | 피난처/휴식 | refuge | rest, survival, hunger | 즉시 채택 | health 회복과 food/time 비용을 묶는다. |
| `ambush_standoff` | 매복/대치 | ambush | combat, trade, physical | 즉시 채택 | retreat, bribe/negotiate, item response를 둔다. |
| `social_bargain` | 사회적 거래 | bargain | trade, village | 조건부 채택 | money/reputation이 실제 result로 바뀔 때만 쓴다. |
| `long_mystery_chain` | 장기 미스터리 | chain | magic, hazard | 보류 | clue 누적 시스템이 필요하다. |
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
| `status_drift` | 위험 상태 누적 | `curse`, `ancient` | 즉시 채택 | avoid, cleanse, risky reward |
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
| `resonance_lens` | 공명 렌즈 | information, risk_reduce | tool | curse, ancient, darkness | 즉시 채택 | clue reveal 중심으로 쓰고 상태 위험 감소는 제한한다. |
| `waybread_pouch` | 길양식 주머니 | cost_convert, risk_reduce | consumable, travel | hunger, lost | 즉시 채택 | consume_item으로 food/health 비용을 전환한다. |
| `broken_compass_needle` | 부러진 방향침 | information, probability | tool, travel | lost, ancient | 조건부 채택 | probability 역할 검증이 필요할 때만 쓴다. |
| `herbal_bandage` | 말린 약초 붕대 | risk_reduce | consumable, healing | physical, beast | 조건부 채택 | healing item 남용 없이 1회성으로 쓴다. |
| `map_of_every_path` | 만능 지도 | information | tool, travel | lost | 거부 | lost 위험을 지나치게 무력화한다. |
| `perfect_purifying_charm` | 완전 정화 부적 | risk_reduce | holy | curse | 거부 | 상태 위험 선택을 단순 정답으로 만든다. |
| `named_weapon` | 고유 무기 | risk_reduce | weapon | bandit, beast | 보류 | combat subsystem을 유도할 수 있다. |

---

## 9. Status 후보 카탈로그

| ID | 이름 | 채택 상태 | 표현 방식 | 판단 |
|---|---|---|---|---|
| `health` | 체력 | 즉시 채택 | 기존 status | 물리 피해와 회복을 표현한다. |
| `food` | 식량 | 즉시 채택 | 기존 status | 시간/우회/휴식 비용을 표현한다. |
| `money` | 돈 | 즉시 채택 | 기존 status | 거래/뇌물/욕심 보상을 표현한다. |
| `reputation` | 평판 | 즉시 채택 | 기존 status | 사회적 결과와 약탈 비용을 표현한다. |
| `curse` | 저주(위험 상태) | 즉시 채택 | 기존 status | 여러 상태 압력 중 magic/ancient/forbidden 위험을 표현한다. |
| `fear` | 공포 | 보류 | 기존 위험 상태로 대체 | 새 심리 수치는 아직 필요 없다. |
| `fatigue` | 피로 | 보류 | `food`, `health`로 대체 | 생존 압력과 역할이 겹친다. |
| `trust` | 신뢰 | 보류 | `reputation`으로 대체 | faction schema가 없으면 좁다. |
| `clue_progress` | 단서 진행도 | 보류 | `event_weight`, item unlock | clue 누적 시스템 전까지 보류한다. |
| `light` | 빛 | 보류 | item + `darkness` tag | 별도 상태보다 item relation이 낫다. |
| `weather_exposure` | 날씨 노출 | 보류 | `storm`, `food`, `health` | 현재 pack 핵심과 약하다. |

---

## 10. Clue 후보 카탈로그

| ID | 이름 | 표현 방식 | 채택 상태 | 쓰임 |
|---|---|---|---|---|
| `repeated_mark` | 반복 표식 | description + investigate result | 즉시 채택 | lost/status-risk 패턴 판단 |
| `sound_interval` | 소리 간격 | investigate choice | 즉시 채택 | timing/route 판단 |
| `smoke_pattern` | 연기 패턴 | investigate + bandit weight | 즉시 채택 | false signal 판별 |
| `knot_rule` | 매듭 규칙 | investigate + village/trade weight | 즉시 채택 | route/social 연결 |
| `track_depth` | 발자국 깊이 | investigate + survival/lost weight | 즉시 채택 | 생존 경로 판단 |
| `sap_variation` | 수액 차이 | risky investigate + status/reputation | 즉시 채택 | 상태 비용과 정보 보상 |
| `insect_pattern` | 벌레 빛 배열 | magic/lost weight | 즉시 채택 | magic clue와 위험 유혹 |
| `mirror_anomaly` | 거울 반사 이상 | item_based reveal | 즉시 채택 | darkness/status-risk 해석 |
| `long_journal` | 장문 일지 | description | 보류 | 로그 정보량이 과해질 수 있다. |
| `cipher_system` | 암호 체계 | 별도 진행도 필요 | 보류 | clue_progress 없이 단발 설명이 된다. |

---

## 11. Reward 후보 카탈로그

| ID | 이름 | YAML 표현 | 채택 상태 | 주의 |
|---|---|---|---|---|
| `food_gain` | 식량 회복 | `status: {food: +1}` | 즉시 채택 | 너무 자주 주면 survival 압력이 약해진다. |
| `health_gain` | 체력 회복 | `status: {health: +1}` | 즉시 채택 | rest 비용과 묶는다. |
| `money_gain` | 돈 획득 | `status: {money: +1}` | 즉시 채택 | status/health/reputation 비용과 묶는다. |
| `reputation_gain` | 평판 획득 | `status: {reputation: +1}` | 즉시 채택 | 사회적 후속 weight와 연결하면 좋다. |
| `status_risk_reduce` | 위험 상태 감소 | `status: {curse: -1}` | 즉시 채택 | 항상 정답이 되지 않게 비용을 둔다. |
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
| `status_risk_cost` | 위험 상태 증가 | `status: {curse: +1}` | 즉시 채택 | forbidden/gamble choice |
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
| `forest_response` | 숲의 반응 | 즉시 채택 | magic/status-risk/lost tag | NPC 없이 mystery 압력 |
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
| `status_risk_interpretation` | 상태 위험과 해석 실패 | 즉시 채택 | curse, ancient, forbidden, magic clue | `event_has_danger_tag`, `result_changes_event_weight` |
| `light_and_visibility` | 빛과 시야 | 즉시 채택 | darkness, mirror, flare, insects | `item_counters_tag`, item reveal |
| `city_intrigue` | 도시 정치극 | 보류 | named NPC, faction | 현재 pack과 멀다. |
| `mega_dungeon` | 거대 던전 | 보류 | floors, map, boss | 별도 구조가 필요하다. |
| `mythic_entity` | 고유 신화 존재 | 거부 | unique lore | World Bible과 원전 차용 위험 |

---

## 15. YAML화 우선순위

Phase 3 실행 시 우선순위:

1. `threshold_crossing`, `route_obstacle`, `clue_discovery`, `false_signal`
2. `resource_cache`, `status_contamination`, `refuge_rest`, `ambush_standoff`
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

## 16. Ontology-lite v0.2 Trial 후보 카탈로그

이 섹션은 Phase 3 작성 전에 검토한 entity/relation gap 후보 중 v0.2 trial로 채택한 항목과 계속 보류할 항목을 구분한다.

### 16.1 Entity 후보 판정

| Entity 후보 | Catalog 사용 방식 | 현재 표현 | 판정 |
| --- | --- | --- | --- |
| `clue` | 조사/아이템/징조 선택의 정보 단위 | `revealed_clue_tags`, `reveals_clue_tags` | v0.2 trial 채택 |
| `foreshadowing` | 후속 위험이나 보상을 미리 암시 | result message, future event weight | Phase 3 trial |
| `location` | region보다 작은 반복 장소 | `location_tags` | v0.2 trial 채택 |
| `hazard` | 구체 조우/장애/위험 장치 | `hazard_tags`, `counters_hazard_tags` | v0.2 trial 채택 |
| `faction` | 집단 이해관계 | reputation, event description | 문서상 보류 |
| `npc_role` | 목격자, 안내자, 경쟁자 같은 사건 역할 | choice text, event description | 문서상 보류 |
| `resource_pressure` | 체력/식량/돈/평판/저주 같은 상태/자원 압박 | status delta | 기존 relation으로 충분 |
| `mystery_thread` | 여러 단서를 잇는 장기 사건 줄기 | event weight, result message | 문서상 보류 |
| `sanctuary` | 회복/피난/재정비 장소 | recovery event, safety tag | Phase 3 trial |
| `omen` | 위험을 예고하는 징조 | `omen_tags`, `creates_omen_tags` | v0.2 trial 채택 |
| `rumor` | 사회적 정보 단서 | reputation event, result message | Phase 3 trial |
| `route` | 장소 연결 선택 | event weight, region 암시 | Phase 3 trial |
| `encounter_role` | 사건의 기능적 역할 | event tag, choice type | 기존 relation으로 충분 |

### 16.2 Relation 후보 판정

| Relation 후보 | 현재 대체 표현 | 판정 | 승격 조건 |
| --- | --- | --- | --- |
| `event_reveals_clue` | `revealed_clue_tags`, `reveals_clue_tags` | v0.2 trial 채택 | Phase 3에서 2개 이상 이벤트가 사용할 때 유지 |
| `clue_foreshadows_event` | result message, later event weight | Phase 3 trial | 경고와 후속 사건 연결이 2회 이상 반복될 때 |
| `event_occurs_at_location` | `location_tags` | v0.2 trial 채택 | Phase 3에서 2개 이상 이벤트가 같은 location 축을 공유할 때 유지 |
| `location_has_hazard` | `event_has_danger_tag`, region context | 문서상 보류 | location entity가 먼저 안정화될 때 |
| `choice_interacts_with_npc_role` | choice text, event description | 문서상 보류 | NPC role 분석이 analyzer/export에 필요할 때 |
| `choice_affects_faction` | `result_modifies_status`의 reputation 변화 | 문서상 보류 | faction별 상태나 평판이 필요할 때 |
| `result_changes_resource_pressure` | `result_modifies_status` | 기존 relation으로 충분 | 현재는 승격하지 않음 |
| `event_advances_mystery_thread` | event weight, result message | 문서상 보류 | 장기 thread 진행도 시스템이 필요할 때 |
| `item_reveals_clue` | `items[].reveals_clue_tags` | v0.2 trial 채택 | Phase 3에서 item clue payoff가 2회 이상 발생할 때 유지 |
| `item_mitigates_hazard` | `item_counters_tag` | 기존 relation으로 충분 | 현재는 승격하지 않음 |
| `route_leads_to_location` | event weight, region 암시 | Phase 3 trial | route 선택지가 location 이동을 반복적으로 만든 때 |
| `omen_warns_about_hazard` | `omen_tags`, `creates_omen_tags`, `hazard_tags` | v0.2 trial 채택 | Phase 3에서 omen-hazard payoff가 2회 이상 확인될 때 유지 |

### 16.3 v0.2 trial source field

Phase 3 콘텐츠는 아래 field를 선택적으로 사용할 수 있다.

```yaml
event:
  location_tags: list[string]
  revealed_clue_tags: list[string]
  omen_tags: list[string]
  hazard_tags: list[string]

choice:
  reveals_clue_tags: list[string]
  creates_omen_tags: list[string]

result:
  reveals_clue_tags: list[string]
  creates_omen_tags: list[string]

item:
  reveals_clue_tags: list[string]
  counters_hazard_tags: list[string]
```

`danger_tags`와 `hazard_tags` 차이:

```text
danger_tags = 넓은 위험 분류
hazard_tags = 구체 조우/장애/위험 장치
```

### 16.4 Phase 3 trial 유지 기준

v0.2 trial relation은 아래 조건을 만족할 때 유지 후보가 된다.

- Phase 3에서 최소 2개 이상 이벤트/아이템이 해당 relation을 사용한다.
- 단순 장식이 아니라 선택 판단, 아이템 payoff, 위험 예고, 장소 coverage 중 하나를 설명한다.
- 기존 `danger_tags`, `event_weight`, `result_modifies_status`만으로 표현하면 의미가 흐려진다.
- analyzer/export가 추후 별도 metric으로 소비할 가치가 있다.

사용성이 낮으면 Phase 3 이후 제거하거나 기존 `tag`, `danger_tags`, `event_weight` 표현으로 통합한다.

---

## 17. Reject 기준

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

## 18. Phase 3 작성 전 체크리스트

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
[ ] 새 relation 후보가 Phase 3 trial 목록에 있다면 source field와 target field를 명확히 지정할 수 있는가?
[ ] analyzer/export가 새 relation을 실제로 사용할 수 있는가?
[ ] relation 추가 시 `data/core/ontology.yaml`과 `09_Content_Ontology_Model` 갱신 계획이 있는가?
[ ] 원전 설정/고유명/문장을 차용하지 않았는가?
```
