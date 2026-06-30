# FateWeaver Quest Base Research Collection v0.1

## 문서 목적

이 문서는 FateWeaver의 Quest(퀘스트) 제작을 위해 조사한 판타지 TRPG(티알피지) Scenario(시나리오), Hook(도입 갈고리), Adventure Seed(모험 씨앗)를 FateWeaver 제작 양식으로 정리한 자료다.

원본 Scenario(시나리오)를 그대로 복제하는 문서가 아니다. FateWeaver의 구조에 맞게 아래 단위로 재가공한다.

```text
Quest(퀘스트) 목적
+ Region(지역)
+ Objective(목표)
+ Pressure(압박)
+ 3-Card Choice(3장 카드 선택)
+ Storylet Tag(스토리 조각 태그)
+ Resource(자원) 변화
+ Success / Partial Success / Failure(성공 / 부분 성공 / 실패)
+ Reward / Unlock(보상 / 해금)
```

---

## 1. 참고 출처

| Source(출처) | 참고 내용 | URL |
|---|---|---|
| TRPG 시나리오 공작소 | 마을 소문, 숲, 고대 도시, 던전 탐색형 소재 | https://trpg-craft.tistory.com/ |
| 꿀비 TRPG 시나리오 정리 | 서양 판타지, 동양 판타지, 왕실/가문/용 소재 | https://honeyrain0.tistory.com/9 |
| 가나슈 TRPG 시나리오 집필집 | 판타지 중세, 전투 중심, 짧은 로드레일 구조 | https://www.postype.com/@ganashu0 |
| 용사가 되는 방법 | 판타지 중세, 2-3시간 전투 추천 Scenario(시나리오) | https://www.postype.com/@ganashu0/post/8307998 |
| 프로젝트 쿠키 원페이지 던전 | 짧은 Dungeon(던전) 구조 참고 | https://projectkuki.tistory.com/123 |
| 산맥 조사 의뢰 | 산맥 조사, 길드 의뢰형 구조 | https://www.postype.com/@summer9303-sj/post/4094985 |
| Roleplaying Tips - 5 Room Dungeon | 5 Room Dungeon(5방 던전) 구조 | https://www.roleplayingtips.com/5-room-dungeons/ |
| Dungeon World SRD - Fronts | Danger(위협), Grim Portents(불길한 징조), Stakes Questions(이해관계 질문) | https://www.dungeonworldsrd.com/gamemastering/fronts/ |
| Sly Flourish - Adventure Types | Adventure Type(모험 유형) 분류 | https://slyflourish.com/what_separates_adventure_types.html |
| Sly Flourish - Adventure Hooks | 짧은 Hook(도입 갈고리) 설계 | https://slyflourish.com/adventure_hooks.html |
| Sly Flourish - Investigations and Mysteries | Investigation(조사), Mystery(미스터리) 운영 구조 | https://slyflourish.com/running_investigations_and_mysteries.html |
| Adventure Lookup | D&D Adventure(모험) 검색/분류 참고 | https://www.adventurelookup.com/ |
| Ready To Role Forest Seeds | Enchanted Forest(마법 숲) Adventure Seed(모험 씨앗) | https://readytorole.com/2018/06/19/25-enchanted-forest-adventure-seeds/ |
| One Page Adventures | 짧은 단발 Adventure(모험) 구조 | https://onepageadventure.com/pdfs/onePageAdventuresFull.pdf |
| One Page Dungeon Contest | One Page Dungeon(한 장 던전) 설계 참고 | https://www.dungeoncontest.com/opdc-2019 |

---

## 2. FateWeaver 변환 기준

| 기준 | 변환 방식 |
|---|---|
| 긴 줄거리 | 한 문장 Quest Goal(퀘스트 목표)로 압축 |
| 장면 | Storylet(스토리 조각) 후보로 분해 |
| 선택지 | 3-Card Choice(3장 카드 선택)로 정규화 |
| 위험 | risk, health, food, time_pressure로 변환 |
| 단서 | clue, omen, witness, tracks Tag(태그)로 변환 |
| NPC | merchant, porter, child, mage, noble 등 Ontology(존재론) Entity(개체)로 변환 |
| 보상 | money, reputation, score, unlock_quests로 변환 |

---

## 3. 제작 양식

아래 양식을 기준으로 Quest(퀘스트)를 제작한다.

```yaml
id: example_quest_id
title: 예시 퀘스트 제목
quest_type: scouting
rank: novice

source_inspiration:
  - source: "출처명"
    url: "https://example.com"
    note: "참고한 구조 또는 소재"

one_sentence_goal: "플레이어가 해야 할 일을 한 문장으로 쓴다."

start_region: village
target_regions:
  - forest

recommended_days: 3
max_days: 5
turns_per_day: 4

primary_objectives:
  - id: primary_objective_id
    type: discover_clue
    target: clue_key
    required: true
    partial_reason: primary_partial
    failure_reason: primary_objective_failed
    score_key: discovery

  - id: return_to_village
    type: return_to_region
    target: village
    required: true
    failure_reason: report_failed
    score_key: report

optional_objectives:
  - id: optional_objective_id
    type: optional_action
    progress_key: optional_progress_key
    required: false
    failure_reason: optional_failed
    score_key: optional_action

card_pattern:
  quest_progress:
    - "필수 목표를 직접 진행하는 카드"
  risk_discovery:
    - "위험 또는 단서를 여는 카드"
  resource_alternative:
    - "자원 관리 또는 우회 카드"

storylet_tags:
  - village
  - forest
  - clue

resource_pressure:
  food: -1
  risk: +1

success:
  - "필수 목표 완료"
  - "귀환 또는 보고 완료"

partial_success:
  - "핵심 단서는 얻었지만 보조 목표 실패"
  - "귀환했지만 보상 감소"

failure:
  - "기한 초과"
  - "체력 0"
  - "필수 목표 미완료"

rewards:
  money: 2
  reputation: 1
  score: 40

unlock_quests:
  - next_quest_id
```

---

## 4. Quest Base(퀘스트 베이스) 후보 50종

| # | Quest ID | Type(유형) | 한 문장 목표 | 3-Card Pattern(3장 카드 패턴) | Storylet Tag(스토리 조각 태그) |
|---:|---|---|---|---|---|
| 1 | `forest_path_scouting_tutorial` | `scouting` | 숲길 안전 여부를 조사해 마을에 보고한다 | 표식 조사 / 발자국 추적 / 식량 아껴 우회 | forest, trail, clue |
| 2 | `missing_porter_search_intro` | `rescue` | 실종된 짐꾼의 행방을 확인한다 | 흔적 추적 / 부서진 짐 조사 / 야영 | porter, rescue, old_road |
| 3 | `merchant_lost_pack_recovery` | `recovery` | 상인의 잃어버린 짐을 회수한다 | 짐 회수 / 도적 흔적 조사 / 협상 | merchant, pack, bandit |
| 4 | `village_well_trouble` | `local_problem` | 병든 우물의 원인을 찾는다 | 물 조사 / 지하 통로 진입 / 약재 사용 | village, well, poison |
| 5 | `old_well_awakening` | `dungeon_crawl` | 오래된 우물 아래 깨어난 것을 봉인한다 | 내려간다 / 균열 조사 / 밧줄 확보 | well, underground, omen |
| 6 | `frozen_treasure_cave` | `recovery` | 얼음 동굴 속 보물을 회수한다 | 얼음 절벽 통과 / 흔적 조사 / 온기 보존 | ice, cave, treasure |
| 7 | `white_dragon_battlefield` | `investigation` | 용과 거인의 전투 흔적에서 진실을 찾는다 | 비늘 조사 / 시체 수색 / 위험 회피 | dragon, giant, frozen |
| 8 | `mountain_guild_trial` | `scouting` | 길드 가입 시험 의뢰를 완수한다 | 산길 조사 / 몬스터 회피 / 증표 회수 | mountain, guild, novice |
| 9 | `abandoned_lighthouse_signal` | `investigation` | 사라진 등대 신호의 원인을 밝힌다 | 등대 진입 / 항구 소문 / 불빛 추적 | coast, lighthouse, missing |
| 10 | `haunted_rectory_children` | `rescue` | 버려진 사제관에서 아이들을 찾는다 | 울음소리 추적 / 방 조사 / 안전 귀환 | children, rectory, rescue |
| 11 | `pinecrest_lost_children` | `rescue` | 숲에서 사라진 아이들을 구조한다 | 발자국 추적 / 숲불빛 조사 / 길 표시 | forest, children, fey |
| 12 | `blackwood_manor_child` | `investigation` | 저택과 숲에 얽힌 실종 사건을 푼다 | 저택 조사 / 숲 탐색 / 거래 거절 | manor, hag, missing |
| 13 | `caravan_to_border_fort` | `escort` | 국경 요새로 향하는 상단을 보호한다 | 길 정찰 / 매복 대응 / 보급 조절 | caravan, road, escort |
| 14 | `winter_wagon_delivery` | `delivery` | 겨울 평원을 넘어 짐마차를 배달한다 | 눈길 돌파 / 짐 수리 / 야영 | winter, wagon, delivery |
| 15 | `old_east_trail_rescue` | `rescue` | 납치된 귀족 아이를 폐허에서 구한다 | 동쪽길 추적 / 지하묘 진입 / 인질 보호 | noble, crypt, rescue |
| 16 | `crypt_of_elven_king` | `dungeon_crawl` | 엘프 왕의 무덤을 조사하고 안식을 회복한다 | 봉인 해석 / 유해 조사 / 전투 회피 | tomb, elven, relic |
| 17 | `lost_city_rising_sands` | `exploration` | 모래 속에서 솟은 잃어버린 도시를 탐사한다 | 사막 길찾기 / 피라미드 진입 / 물 보존 | desert, lost_city, survival |
| 18 | `flooded_temple_race` | `recovery` | 침수된 신전의 보물을 경쟁자보다 먼저 찾는다 | 수로 탐색 / 경쟁자 견제 / 보물 판별 | temple, flood, rival |
| 19 | `ruined_island_puzzle_box` | `investigation` | 폐허 섬 요새의 퍼즐 상자를 해석한다 | 상자 조사 / 해안 진입 / 봉인 회피 | island, puzzle, fortress |
| 20 | `burial_site_missing_soldiers` | `investigation` | 매장지에서 사라진 병사들의 행방을 밝힌다 | 무기 흔적 / 핏자국 조사 / 부족 협상 | burial, soldiers, faction |
| 21 | `ghost_town_medicine_run` | `delivery` | 병든 마을을 위해 숲속 마법사에게 소식을 전한다 | 숲 통과 / 약초 확보 / 마법사 설득 | disease, old_forest, mage |
| 22 | `vanishing_village` | `mystery` | 통째로 사라진 마을의 흔적을 찾는다 | 빈집 조사 / 이상한 길 / 생존자 추적 | village, vanish, anomaly |
| 23 | `cattle_mutilation_stone_circle` | `investigation` | 가축 피해와 돌원 의식의 관계를 밝힌다 | 목장 조사 / 돌원 해석 / 야간 감시 | cattle, stone_circle, were |
| 24 | `beast_of_zarechka` | `monster_hunt` | 폐허와 연결된 마을 습격 야수를 추적한다 | 벽화 조사 / 습격 현장 / 덫 설치 | beast, ruin, hunt |
| 25 | `hidden_grove_discovery` | `exploration` | 숲 깊은 숨은 성소를 발견한다 | 요정 흔적 / 덤불 돌파 / 제물 선택 | grove, fey, shrine |
| 26 | `awaken_the_monolith` | `ritual` | 잠든 비석을 깨워 지역의 길을 연다 | 문양 해석 / 재료 수집 / 의식 수행 | monolith, ritual, unlock |
| 27 | `rebuild_the_ruin` | `recovery` | 무너진 초소를 복구해 안전 거점을 만든다 | 목재 확보 / 위험 제거 / 일꾼 보호 | ruin, outpost, rebuild |
| 28 | `defend_the_village_night` | `defense` | 밤새 마을을 습격에서 지킨다 | 방책 보강 / 순찰 / 주민 대피 | defense, village, night |
| 29 | `survive_the_storm_pass` | `survival` | 폭풍 속 산길을 통과해 귀환한다 | 피난처 찾기 / 체온 유지 / 길 표시 | storm, mountain, survival |
| 30 | `infiltrate_the_keep` | `infiltration` | 요새에 잠입해 포로 정보를 얻는다 | 경비 관찰 / 변장 / 탈출로 확보 | keep, stealth, prisoner |
| 31 | `weed_out_the_traitor` | `intrigue` | 마을 의뢰단 안의 배신자를 찾아낸다 | 증언 비교 / 물증 확보 / 공개 추궁 | traitor, village, social |
| 32 | `deliver_the_sealed_parcel` | `delivery` | 봉인된 소포를 열지 않고 전달한다 | 지름길 / 유혹 거절 / 추격 회피 | parcel, oath, road |
| 33 | `destroy_the_crown` | `ritual` | 저주받은 왕관을 파괴할 장소를 찾는다 | 왕관 조사 / 대장장이 설득 / 신전 이동 | crown, cursed_item, temple |
| 34 | `heist_the_crown_jewels` | `contract` | 귀족의 보석을 훔치거나 회수한다 | 경로 조사 / 주의 분산 / 탈출 | heist, noble, stealth |
| 35 | `collect_rare_materials` | `gathering` | 희귀 제작 재료를 제한 시간 안에 모은다 | 채집 / 위험 식별 / 보관 | material, crafting, forest |
| 36 | `train_the_new_recruit` | `escort` | 신입 모험가를 데리고 쉬운 의뢰를 완수한다 | 안전 지시 / 실수 수습 / 격려 | recruit, escort, tutorial |
| 37 | `create_a_new_spell` | `research` | 새 주문 재료와 실험 결과를 확보한다 | 재료 탐색 / 실험 / 폭주 억제 | spell, research, magic |
| 38 | `activate_the_old_gate` | `ritual` | 고대 관문을 다시 작동시킨다 | 룬 맞추기 / 동력 확보 / 위험 감수 | gate, ruin, activation |
| 39 | `bury_the_secret` | `moral_choice` | 위험한 비밀을 공개할지 묻을지 결정한다 | 증거 은닉 / 증언 듣기 / 보고 | secret, reputation, choice |
| 40 | `awaken_the_beast` | `monster_hunt` | 잠든 괴수를 깨울지 봉인할지 선택한다 | 징조 조사 / 봉인 확인 / 의식 방해 | beast, omen, seal |
| 41 | `festival_missing_racer` | `investigation` | 축제 경주 중 사라진 참가자를 찾는다 | 경기 참여 / 목격자 조사 / 방해 추적 | festival, race, missing |
| 42 | `tanglewood_faire_games` | `local_problem` | 축제의 이상한 놀이 뒤 사건을 밝힌다 | 게임 참가 / 상인 조사 / 보스 대면 | festival, fair, clue |
| 43 | `dreamless_king` | `investigation` | 잠들지 못하는 왕의 잃어버린 꿈을 되찾는다 | 궁정 조사 / 약제사 구출 / 밀수굴 추적 | king, dream, palace |
| 44 | `stowaway_without_memory` | `escort` | 기억을 잃은 밀항자를 보호하며 정체를 찾는다 | 선창 조사 / 경비 설득 / 기억 단서 | ship, memory, fugitive |
| 45 | `apothecary_bargain` | `social_contract` | 누명 쓴 약제사와 거래해 진실을 얻는다 | 감옥 접근 / 맹세 선택 / 탈출 지원 | apothecary, bargain, prison |
| 46 | `painted_portal_canvas` | `investigation` | 그림 뒤 고대문자와 차원문을 조사한다 | 캔버스 조사 / 문양 해석 / 진입 여부 | painting, portal, ancient |
| 47 | `mansion_returned_explorer` | `horror_investigation` | 귀환한 탐험가가 정말 본인인지 확인한다 | 저택 방문 / 기록 대조 / 감염 징후 | explorer, parasite, manor |
| 48 | `snowfield_military_school` | `training` | 설원 군사학교의 첫 시험을 통과한다 | 훈련 / 동료 갈등 / 습격 대응 | academy, snow, rival |
| 49 | `dragondew_wine_delivery` | `recovery` | 사라진 특산 와인의 행방을 찾는다 | 양조장 조사 / 운송로 추적 / 거래 | wine, merchant, village |
| 50 | `beginner_village_wrongness` | `local_problem` | 너무 평화로운 초보자 마을의 이상함을 파악한다 | 정보 수집 / 촌장 관찰 / 숲 경계 | starter_village, anomaly, rumor |

---

## 5. 우선 제작 추천 15개

| 우선순위 | Quest ID | 이유 |
|---:|---|---|
| 1 | `forest_path_scouting_tutorial` | 기존 Quest Design Guide(퀘스트 설계 지침)와 완전 정합 |
| 2 | `missing_porter_search_intro` | Rescue(구조), Partial Success(부분 성공), Time Pressure(시간 압박) 검증 |
| 3 | `village_well_trouble` | Village(마을), Resource(자원), Clue(단서) 연결이 쉬움 |
| 4 | `merchant_lost_pack_recovery` | Money(돈), Reputation(평판), Recovery(회수) 도입 |
| 5 | `old_well_awakening` | Village(마을)에서 Dungeon(던전)으로 자연스럽게 확장 |
| 6 | `ghost_town_medicine_run` | Delivery(배달), Disease(질병), Forest(숲) 압박 |
| 7 | `caravan_to_border_fort` | Escort(호위) 기본형 |
| 8 | `defend_the_village_night` | Defense(방어) Type(유형) 검증 |
| 9 | `burial_site_missing_soldiers` | Faction(세력), Misunderstanding(오해), Negotiation(협상) 추가 가능 |
| 10 | `frozen_treasure_cave` | Resource Pressure(자원 압박)가 명확함 |
| 11 | `pinecrest_lost_children` | Forest Rescue(숲 구조)로 감정 동기가 강함 |
| 12 | `old_east_trail_rescue` | Road(길), Crypt(지하묘), Rescue(구조) 결합 |
| 13 | `ruined_island_puzzle_box` | Puzzle(퍼즐), Clue(단서), Fortress(요새) 확장 |
| 14 | `festival_missing_racer` | 전투 없는 Investigation(조사) 가능 |
| 15 | `painted_portal_canvas` | Portal(차원문), Unlock(해금)용으로 좋음 |

---

## 6. 상세 제작안

### 6.1 숲길 안전 조사

```yaml
id: forest_path_scouting_tutorial
title: 숲길 안전 조사
quest_type: scouting
rank: novice

source_inspiration:
  - source: "TRPG 시나리오 공작소"
    url: "https://trpg-craft.tistory.com/"
    note: "마을 소문, 숲길, 고대 도시 단서형 구조"

one_sentence_goal: "숲길이 안전한지 조사하고 마을에 보고한다."

start_region: village
target_regions:
  - forest

recommended_days: 3
max_days: 5
turns_per_day: 4

primary_objectives:
  - id: discover_safe_path
    type: discover_clue
    target: safe_forest_path
    required: true
    partial_reason: primary_partial
    failure_reason: primary_objective_failed
    score_key: discovery

  - id: return_to_village
    type: return_to_region
    target: village
    required: true
    failure_reason: report_failed
    score_key: report

optional_objectives:
  - id: mark_beast_tracks
    type: optional_action
    progress_key: marked_beast_tracks
    required: false
    failure_reason: optional_failed
    score_key: optional_action

card_pattern:
  quest_progress:
    - "숲길 표식을 조사한다"
  risk_discovery:
    - "짐승 발자국을 따라간다"
  resource_alternative:
    - "식량을 아끼며 우회한다"

storylet_tags:
  - forest
  - trail
  - clue
  - beast_tracks
  - return_report

rewards:
  money: 2
  reputation: 1
  score: 40

unlock_quests:
  - missing_porter_search_intro
```

### 6.2 실종된 짐꾼 수색

```yaml
id: missing_porter_search_intro
title: 실종된 짐꾼 수색
quest_type: rescue
rank: novice

source_inspiration:
  - source: "TRPG 시나리오 공작소"
    url: "https://trpg-craft.tistory.com/"
    note: "이전에 떠난 모험가 또는 운반자가 돌아오지 않는 구조"

one_sentence_goal: "실종된 짐꾼의 흔적을 찾아 생사와 짐의 행방을 확인한다."

start_region: village
target_regions:
  - old_road
  - forest

recommended_days: 3
max_days: 5
turns_per_day: 4

primary_objectives:
  - id: find_porter_trace
    type: discover_clue
    target: porter_trace
    required: true
    partial_reason: primary_partial
    failure_reason: primary_objective_failed
    score_key: tracking

  - id: resolve_porter_fate
    type: optional_action
    progress_key: porter_fate_resolved
    required: true
    failure_reason: rescue_failed
    score_key: rescue

optional_objectives:
  - id: recover_lost_pack
    type: optional_action
    progress_key: recovered_lost_pack
    required: false
    failure_reason: optional_failed
    score_key: recovery

card_pattern:
  quest_progress:
    - "짐꾼의 발자국을 추적한다"
  risk_discovery:
    - "부서진 수레를 조사한다"
  resource_alternative:
    - "마을 사냥꾼에게 정보를 산다"

storylet_tags:
  - porter
  - old_road
  - forest
  - rescue
  - broken_cart
  - tracks

rewards:
  money: 2
  reputation: 2
  score: 45

unlock_quests:
  - merchant_lost_pack_recovery
```

### 6.3 병든 우물

```yaml
id: village_well_trouble
title: 병든 우물
quest_type: local_problem
rank: novice

source_inspiration:
  - source: "One Page Dungeon Contest"
    url: "https://www.dungeoncontest.com/opdc-2019"
    note: "마을 내부의 작은 장소를 던전 입구로 쓰는 구조"

one_sentence_goal: "마을 우물이 오염된 원인을 찾고 물길을 회복한다."

start_region: village
target_regions:
  - village
  - underground

recommended_days: 2
max_days: 4
turns_per_day: 4

primary_objectives:
  - id: identify_well_poison
    type: discover_clue
    target: well_poison_source
    required: true
    partial_reason: primary_partial
    failure_reason: primary_objective_failed
    score_key: investigation

  - id: restore_well_water
    type: optional_action
    progress_key: well_water_restored
    required: true
    failure_reason: restore_failed
    score_key: repair

optional_objectives:
  - id: calm_villagers
    type: optional_action
    progress_key: villagers_calmed
    required: false
    failure_reason: optional_failed
    score_key: reputation

card_pattern:
  quest_progress:
    - "우물물을 조사한다"
  risk_discovery:
    - "우물 아래 통로로 내려간다"
  resource_alternative:
    - "약재로 임시 정화수를 만든다"

storylet_tags:
  - village
  - well
  - poison
  - underground
  - clue

rewards:
  money: 1
  reputation: 2
  score: 35

unlock_quests:
  - old_well_awakening
```

### 6.4 상인의 잃어버린 짐

```yaml
id: merchant_lost_pack_recovery
title: 상인의 잃어버린 짐
quest_type: recovery
rank: novice

source_inspiration:
  - source: "Sly Flourish - Adventure Hooks"
    url: "https://slyflourish.com/adventure_hooks.html"
    note: "짧은 의뢰형 Hook(도입 갈고리) 구조"

one_sentence_goal: "상인의 잃어버린 짐을 찾아 회수하거나 정당한 처분을 결정한다."

start_region: village
target_regions:
  - road
  - forest_edge

recommended_days: 3
max_days: 5
turns_per_day: 4

primary_objectives:
  - id: locate_lost_pack
    type: discover_clue
    target: lost_pack_location
    required: true
    partial_reason: primary_partial
    failure_reason: primary_objective_failed
    score_key: tracking

  - id: resolve_pack_ownership
    type: optional_action
    progress_key: pack_ownership_resolved
    required: true
    failure_reason: recovery_failed
    score_key: recovery

optional_objectives:
  - id: negotiate_bonus_payment
    type: optional_action
    progress_key: bonus_payment_negotiated
    required: false
    failure_reason: optional_failed
    score_key: economy

card_pattern:
  quest_progress:
    - "짐이 떨어진 지점을 조사한다"
  risk_discovery:
    - "도적의 흔적을 따라간다"
  resource_alternative:
    - "상인과 보상 조건을 다시 협상한다"

storylet_tags:
  - merchant
  - road
  - lost_pack
  - bandit
  - negotiation

rewards:
  money: 3
  reputation: 1
  score: 40

unlock_quests:
  - caravan_to_border_fort
```

### 6.5 마을 방어의 밤

```yaml
id: defend_the_village_night
title: 마을 방어의 밤
quest_type: defense
rank: novice

source_inspiration:
  - source: "Dungeon World SRD - Fronts"
    url: "https://www.dungeonworldsrd.com/gamemastering/fronts/"
    note: "Danger(위협), Grim Portents(불길한 징조)를 단계적 압박으로 활용"

one_sentence_goal: "밤이 끝날 때까지 마을을 습격에서 지킨다."

start_region: village
target_regions:
  - village

recommended_days: 1
max_days: 2
turns_per_day: 6

primary_objectives:
  - id: hold_village_until_dawn
    type: optional_action
    progress_key: village_held_until_dawn
    required: true
    partial_reason: defense_partial
    failure_reason: defense_failed
    score_key: defense

  - id: prevent_civilian_loss
    type: keep_resource_at_least
    target: reputation
    value: 1
    required: true
    failure_reason: civilian_loss
    score_key: reputation

optional_objectives:
  - id: capture_raider_scout
    type: optional_action
    progress_key: raider_scout_captured
    required: false
    failure_reason: optional_failed
    score_key: discovery

card_pattern:
  quest_progress:
    - "방책을 보강한다"
  risk_discovery:
    - "어둠 속 움직임을 추적한다"
  resource_alternative:
    - "주민을 대피시켜 피해를 줄인다"

storylet_tags:
  - village
  - defense
  - night
  - raider
  - civilian
  - omen

rewards:
  money: 2
  reputation: 3
  score: 50

unlock_quests:
  - weed_out_the_traitor
```

---

## 7. Type(유형) 확장 후보

| Type(유형) | 설명 | 대표 Quest(퀘스트) |
|---|---|---|
| `local_problem` | 마을 내부 문제 해결 | `village_well_trouble` |
| `defense` | 일정 Turn(턴) 동안 지역 방어 | `defend_the_village_night` |
| `ritual` | 재료, 장소, 순서, 실패 위험 중심 | `activate_the_old_gate` |
| `mystery` | 실종, 이상 현상, 모순된 증언 중심 | `vanishing_village` |
| `infiltration` | 전투 회피, 잠입, 탈출로 확보 중심 | `infiltrate_the_keep` |
| `training` | 튜토리얼 또는 신입 NPC 보호 | `train_the_new_recruit` |
| `social_contract` | 거래, 맹세, 평판 중심 | `apothecary_bargain` |
| `monster_hunt` | 추적, 덫, 교전, 귀환 보고 중심 | `beast_of_zarechka` |
| `research` | 주문, 실험, 재료, 실패 폭주 중심 | `create_a_new_spell` |
| `moral_choice` | 공개/은닉/배신/보고 선택 중심 | `bury_the_secret` |

---

## 8. 재사용 Storylet Tag(스토리 조각 태그)

```text
village, forest, old_road, road, ruin, well, crypt, temple, shrine, manor
mountain, coast, lighthouse, desert, island, fortress, palace, ship
missing, rescue, escort, delivery, recovery, scouting, investigation
defense, ritual, infiltration, survival, gathering, training
clue, omen, rumor, witness, tracks, broken_cart, blood_trace
merchant, porter, child, noble, mage, apothecary, guard, recruit
beast, dragon, giant, hag, undead, bandit, cult, fey, raider
food, health, money, reputation, risk, time_pressure
return_report, unlock_region, sealed_gate, faction_tension
```

---

## 9. 추천 제작 순서

초반 10개만 실제 구현한다면 아래 순서가 좋다.

```text
1. forest_path_scouting_tutorial
2. missing_porter_search_intro
3. village_well_trouble
4. merchant_lost_pack_recovery
5. old_well_awakening
6. ghost_town_medicine_run
7. caravan_to_border_fort
8. defend_the_village_night
9. burial_site_missing_soldiers
10. frozen_treasure_cave
```

이 조합으로 Gathering(채집), Scouting(정찰), Rescue(구조), Recovery(회수), Local Problem(마을 문제), Dungeon Crawl(던전 탐색), Delivery(배달), Escort(호위), Defense(방어), Investigation(조사)를 대부분 검증할 수 있다.

---

## 10. 제작 시 주의

- 출처 Scenario(시나리오)의 고유 줄거리, 이름, 대사를 그대로 복제하지 않는다.
- FateWeaver에서는 Story(서사)보다 Objective(목표), Pressure(압박), Card Pattern(카드 패턴)을 먼저 만든다.
- 모든 Quest(퀘스트)는 Success(성공), Partial Success(부분 성공), Failure(실패)를 가져야 한다.
- 3-Card Choice(3장 카드 선택)가 만들기 어려운 소재는 보류한다.
- 저주를 메인 Theme(테마)로 과용하지 않는다.
- 특정 Quest(퀘스트) 전용 하드코딩 reason(이유)을 늘리지 않는다.
- Optional Objective(선택 목표)는 Card Candidate Pool(카드 후보 풀)과 Storylet/Ontology(스토리 조각/존재론) Tag(태그)로 연결한다.

