# [Current] Quest Type Catalog v0.1

> 상태: [Current] Quest Design Guide와 Quest Base Research Collection에 나열된 Quest 후보를 Type별로 분류한 계획 문서.

## 1. 문서 목적

이 문서는 Quest를 추가 구현하기 전에 Quest 후보를 Type별로 정리하기 위한 Catalog다.

목표는 다음 Quest Batch를 감이 아니라 기준으로 고르는 것이다.

- 이미 구현된 Quest Type을 확인한다.
- 아직 검증하지 않은 Quest Type을 드러낸다.
- 현재 P0 구조로 구현 가능한 후보와 보류해야 할 후보를 나눈다.
- 다음 1-3개 Quest Batch의 후보를 제안한다.

이번 문서는 구현 작업이 아니다. `data/`, `src/`, `tests/`, `tools/`는 수정하지 않는다.

## 2. 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`
- `data/content/base/quests.yaml`

## 3. Type 분류 기준

Quest Design Guide의 기본 Type은 다음 10개다.

| Type | 핵심 플레이 | 좋은 용도 |
|---|---|---|
| `gathering` | 수집, 귀환, 자원 관리 | 튜토리얼 |
| `scouting` | 조사, 단서, 위험 판단 | 두 번째 튜토리얼 |
| `recovery` | 물건 회수, 선택 대가 | 경제/평판 도입 |
| `rescue` | NPC 구조, 시간 압박 | 부분 성공/실패 분기 |
| `delivery` | 이동, 위험 회피, 귀환 | Day/Turn 학습 |
| `investigation` | 단서 해석, 후속 사건 | 폐허/미스터리 |
| `escort` | 보호, 자원 소모, 평판 | 중급 Quest |
| `survival` | 일정 기간 버티기 | 위험/식량 압박 |
| `exploration` | 새 장소 발견 | 지역 확장 |
| `contract` | 보상 중심 위험 의뢰 | 돈/평판/선택 대가 |

Quest Base Research Collection에서 확장된 Type은 다음과 같다.

| Type | 핵심 플레이 | 대표 용도 |
|---|---|---|
| `local_problem` | 마을 내부 문제 해결 | 마을 이벤트 확장 |
| `dungeon_crawl` | 좁은 위험 공간 진입과 단계적 탐색 | 지하/무덤/우물 확장 |
| `defense` | 제한 Turn 동안 지역 방어 | 야간 습격과 주민 보호 |
| `ritual` | 재료, 장소, 순서, 실패 위험 | 관문/비석/저주 해소 |
| `mystery` | 이상 현상, 모순된 증언, 실종 | 조사보다 큰 미스터리 구조 |
| `infiltration` | 전투 회피, 잠입, 탈출로 확보 | 요새/귀족/포로 정보 |
| `social_contract` | 거래, 맹세, 평판 중심 선택 | NPC와 위험한 계약 |
| `monster_hunt` | 추적, 덫, 교전, 귀환 보고 | 야수/괴물 처리 |
| `research` | 실험, 재료, 폭주 억제 | 마법/학술형 Quest |
| `moral_choice` | 공개, 은닉, 배신, 보고 선택 | 평판과 윤리 선택 |
| `training` | 튜토리얼 또는 신입 NPC 보호 | 훈련/동료 성장 |
| `intrigue` | 증언 비교와 배신자 색출 | 사회 추리와 정치 |
| `horror_investigation` | 감염/정체 의심/불안 증거 | 공포형 조사 |

구현 상태 값은 다음 기준으로 사용한다.

| 상태 | 기준 |
|---|---|
| Done | `data/content/base/quests.yaml`에 구현됨 |
| Recommended | 다음 1-2 Batch에서 구현하기 좋음 |
| Candidate | 후보는 좋지만 우선순위가 낮음 |
| Deferred | 현재 P0 구조보다 크거나 별도 시스템이 필요함 |

## 4. 현재 구현된 Quest Type Coverage

`data/content/base/quests.yaml` 기준 현재 구현 완료 Quest는 4개다.

| 구현 상태 | Quest ID | 한글명 | Type | 핵심 검증 | 비고 |
|---|---|---|---|---|---|
| Done | `herb_gathering_tutorial` | 약초 채집 의뢰 | `gathering` | 수집 / 귀환 / 식량 / optional_action | P0 기본 튜토리얼 |
| Done | `forest_path_scouting_tutorial` | 숲길 안전 조사 | `scouting` | 조사 / 단서 / 위험 판단 | Research 후보 #1 |
| Done | `missing_porter_search_intro` | 실종된 짐꾼 수색 | `rescue` | 구조 / 시간 압박 / partial_success | Research 후보 #2 |
| Done | `merchant_lost_pack_recovery` | 상인의 잃어버린 짐 | `recovery` | 회수 / 돈 / 평판 / 협상 | Research 후보 #3 |

현재 Coverage는 `gathering`, `scouting`, `rescue`, `recovery`에 집중되어 있다.

아직 직접 구현하지 않은 핵심 Type은 `delivery`, `investigation`, `escort`, `survival`, `exploration`, `contract`, `local_problem`, `dungeon_crawl`, `defense`다.

## 5. Type별 Quest Catalog

Quest Base Research Collection의 50개 후보와 Quest Design Guide의 Guide-only 후보를 함께 정리했다. Research 후보 번호가 없는 항목은 Quest Design Guide 또는 Roadmap에서만 나온 후보다.

### 5.1 gathering

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Done | `herb_gathering_tutorial` | 약초 채집 의뢰 | 수집 / 귀환 / 식량 보존 | 1 | 구현 완료, Guide 기준 |
| Candidate | `collect_rare_materials` | 희귀 재료 채집 | 제작 재료 / 제한 시간 / 위험 식별 | 3 | Research #35 |

### 5.2 scouting

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Done | `forest_path_scouting_tutorial` | 숲길 안전 조사 | 단서 / 위험 판단 / 보고 | 1 | 구현 완료, Research #1 |
| Candidate | `mountain_guild_trial` | 길드 가입 시험 의뢰 | 산길 조사 / 몬스터 회피 / 증표 회수 | 3 | Research #8 |
| Candidate | `forest_edge_camp_safety` | 숲 가장자리 야영 안전 확인 | 위험 표시 / 야영 / 귀환 보고 | 3 | Guide-only Frontier 후보 |

### 5.3 recovery

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Done | `merchant_lost_pack_recovery` | 상인의 잃어버린 짐 | 회수 / 돈 / 평판 / 협상 | 1 | 구현 완료, Research #3 |
| Candidate | `frozen_treasure_cave` | 얼음 동굴 보물 회수 | 자원 압박 / 보물 판별 / 온기 보존 | 3 | Research #6 |
| Candidate | `flooded_temple_race` | 침수된 신전 보물 경쟁 | 경쟁자 / 수로 탐색 / 보물 판별 | 3 | Research #18 |
| Candidate | `rebuild_the_ruin` | 무너진 초소 복구 | 목재 확보 / 위험 제거 / 일꾼 보호 | 4 | Research #27 |
| Candidate | `dragondew_wine_delivery` | 사라진 특산 와인 추적 | 양조장 조사 / 운송로 추적 / 거래 | 4 | Research #49 |

### 5.4 rescue

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Done | `missing_porter_search_intro` | 실종된 짐꾼 수색 | 구조 / 시간 압박 / 부분 성공 | 1 | 구현 완료, Research #2 |
| Candidate | `haunted_rectory_children` | 사제관 아이들 수색 | 방 조사 / 안전 귀환 / 공포 단서 | 3 | Research #10 |
| Candidate | `pinecrest_lost_children` | 숲에서 사라진 아이들 | 발자국 / 숲불빛 / 길 표시 | 3 | Research #11 |
| Candidate | `old_east_trail_rescue` | 동쪽길 귀족 아이 구조 | 추적 / 지하묘 / 인질 보호 | 3 | Research #15 |

### 5.5 delivery

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `ghost_town_medicine_run` | 유령 마을 약 전달 | 질병 / 숲 통과 / 마법사 설득 | 2 | Research #21, 우선 추천 15개 |
| Candidate | `winter_wagon_delivery` | 겨울 짐마차 배달 | 눈길 / 짐 수리 / 야영 | 3 | Research #14 |
| Candidate | `deliver_the_sealed_parcel` | 봉인된 소포 전달 | 맹세 / 유혹 거절 / 추격 회피 | 3 | Research #32 |
| Candidate | `night_return_contract` | 야간 귀환 계약 | 고위험 귀환 / 강한 보상 / 실패 가능성 | 4 | Guide-only Dangerous 후보 |

### 5.6 investigation

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `ruin_mark_investigation_intro` | 폐허 표식 조사 | clue / omen / ruin / 후속 해금 | 1 | Guide/Roadmap 다음 후보 |
| Candidate | `white_dragon_battlefield` | 용과 거인의 전장 흔적 | 비늘 / 시체 / 위험 회피 | 4 | Research #7 |
| Candidate | `abandoned_lighthouse_signal` | 사라진 등대 신호 | 항구 소문 / 등대 진입 / 불빛 추적 | 3 | Research #9 |
| Candidate | `blackwood_manor_child` | 저택과 숲 실종 사건 | 저택 조사 / 숲 탐색 / 거래 거절 | 4 | Research #12 |
| Candidate | `ruined_island_puzzle_box` | 폐허 섬 퍼즐 상자 | 퍼즐 / 해안 진입 / 봉인 회피 | 3 | Research #19 |
| Candidate | `burial_site_missing_soldiers` | 매장지 실종 병사 | 세력 / 협상 / 오해 해소 | 3 | Research #20 |
| Candidate | `cattle_mutilation_stone_circle` | 가축 피해와 돌원 의식 | 목장 / 돌원 / 야간 감시 | 3 | Research #23 |
| Candidate | `festival_missing_racer` | 축제 경주 실종자 | 경기 참여 / 목격자 / 방해 추적 | 3 | Research #41 |
| Candidate | `dreamless_king` | 잠들지 못하는 왕 | 궁정 조사 / 약제사 / 밀수굴 | 4 | Research #43 |
| Candidate | `painted_portal_canvas` | 그림 뒤 차원문 조사 | 고대문자 / 진입 여부 / 해금 | 3 | Research #46 |
| Candidate | `old_hunter_trail_followup` | 오래된 사냥꾼 길 후속 조사 | trail / clue / 위험 증가 | 4 | Guide-only Frontier 후보 |

### 5.7 escort

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `caravan_to_border_fort` | 국경 요새 상단 호위 | 길 정찰 / 매복 대응 / 보급 조절 | 2 | Research #13 |
| Candidate | `train_the_new_recruit` | 신입 모험가 훈련 호위 | 실수 수습 / 격려 / 튜토리얼 | 3 | Research #36 |
| Candidate | `stowaway_without_memory` | 기억 잃은 밀항자 보호 | 선창 조사 / 경비 설득 / 기억 단서 | 4 | Research #44 |

### 5.8 survival

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `survive_the_storm_pass` | 폭풍 산길 생존 귀환 | 피난처 / 체온 / 길 표시 | 2 | Research #29, 새 Type 검증 |

### 5.9 exploration

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `hidden_grove_discovery` | 숨은 성소 발견 | 요정 흔적 / 덤불 돌파 / 제물 선택 | 2 | Research #25 |
| Candidate | `lost_city_rising_sands` | 모래 속 잃어버린 도시 | 사막 길찾기 / 물 보존 / 피라미드 | 4 | Research #17 |

### 5.10 contract

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Candidate | `heist_the_crown_jewels` | 왕관 보석 절도/회수 | 경로 조사 / 주의 분산 / 탈출 | 4 | Research #34, stealth 의존 |

### 5.11 local_problem

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `village_well_trouble` | 병든 우물 | 마을 / 지하 통로 / 약재 사용 | 1 | Research #4, Guide/Roadmap 상위 후보 |
| Candidate | `tanglewood_faire_games` | 축제의 이상한 놀이 | 게임 참가 / 상인 조사 / 보스 대면 | 4 | Research #42 |
| Candidate | `beginner_village_wrongness` | 초보자 마을의 이상함 | 정보 수집 / 촌장 관찰 / 숲 경계 | 3 | Research #50 |

### 5.12 dungeon_crawl

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `old_well_awakening` | 오래된 우물 각성 | 우물 하강 / 균열 조사 / 봉인 | 2 | Research #5 |
| Candidate | `crypt_of_elven_king` | 엘프 왕의 무덤 | 봉인 해석 / 유해 조사 / 전투 회피 | 4 | Research #16 |
| Candidate | `sealed_ruin_entry` | 봉인된 폐허 진입 | 고위험 선택 / 강한 보상 / 실패 가능성 | 4 | Guide-only Dangerous 후보 |

### 5.13 defense

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `defend_the_village_night` | 마을 방어의 밤 | 방책 / 순찰 / 주민 대피 | 2 | Research #28, Defense Type 첫 검증 |

### 5.14 ritual

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Candidate | `awaken_the_monolith` | 잠든 비석 깨우기 | 문양 / 재료 / 의식 수행 | 4 | Research #26 |
| Candidate | `destroy_the_crown` | 저주받은 왕관 파괴 | 왕관 조사 / 대장장이 / 신전 이동 | 4 | Research #33 |
| Candidate | `activate_the_old_gate` | 고대 관문 작동 | 룬 / 동력 / 위험 감수 | 4 | Research #38 |

### 5.15 mystery

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Recommended | `vanishing_village` | 사라진 마을 | 빈집 / 이상한 길 / 생존자 추적 | 3 | Research #22, Batch C 후보 |

### 5.16 infiltration

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Deferred | `infiltrate_the_keep` | 요새 잠입 | 경비 관찰 / 변장 / 탈출로 | 5 | Research #30, stealth 시스템 필요 |

### 5.17 social_contract

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Candidate | `apothecary_bargain` | 약제사의 거래 | 감옥 접근 / 맹세 / 탈출 지원 | 4 | Research #45 |

### 5.18 monster_hunt

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Candidate | `beast_of_zarechka` | 자레치카의 야수 | 벽화 / 습격 현장 / 덫 설치 | 4 | Research #24 |
| Candidate | `awaken_the_beast` | 잠든 괴수 | 징조 / 봉인 / 의식 방해 | 4 | Research #40 |

### 5.19 research

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Deferred | `create_a_new_spell` | 새 주문 실험 | 재료 / 실험 / 폭주 억제 | 5 | Research #37, 실험/마법 시스템 필요 |

### 5.20 moral_choice

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Candidate | `bury_the_secret` | 위험한 비밀 | 증거 은닉 / 증언 / 보고 선택 | 4 | Research #39 |

### 5.21 training

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Candidate | `snowfield_military_school` | 설원 군사학교 시험 | 훈련 / 동료 갈등 / 습격 대응 | 4 | Research #48 |

### 5.22 intrigue

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Deferred | `weed_out_the_traitor` | 배신자 색출 | 증언 비교 / 물증 / 공개 추궁 | 5 | Research #31, 사회 추리 상태 필요 |

### 5.23 horror_investigation

| 구현 상태 | Quest ID | 한글명 | 핵심 검증 | 우선순위 | 비고 |
|---|---|---|---|---:|---|
| Deferred | `mansion_returned_explorer` | 귀환 탐험가 정체 확인 | 기록 대조 / 감염 징후 / 저택 방문 | 5 | Research #47, 공포/감염 표현 필요 |

## 6. Type별 구현 우선순위

다음 우선순위는 "재미있어 보이는 순서"가 아니라 다음 기준으로 매겼다.

1. 아직 검증하지 않은 Quest Type인가?
2. 현재 Objective evaluator로 처리 가능한가?
3. 새 resource/status가 필요한가?
4. Storylet/Event Hint만 추가하면 되는가?
5. 3-Card pattern이 명확한가?
6. success / partial_success / failure fixture를 만들 수 있는가?
7. 기존 Quest Type과 중복되지 않는가?
8. 다음 시스템 검증에 도움이 되는가?

| 우선순위 | Type | 추천 Quest | 이유 |
|---:|---|---|---|
| 1 | `investigation` | `ruin_mark_investigation_intro` | Roadmap의 다음 후보이며 clue / omen / ruin 확장에 좋다. |
| 1 | `local_problem` | `village_well_trouble` | 마을 내부 문제, 단서, 지하 진입을 현재 구조로 검증하기 쉽다. |
| 2 | `defense` | `defend_the_village_night` | 아직 없는 Defense Type을 제한 Turn 구조로 검증한다. |
| 2 | `delivery` | `ghost_town_medicine_run` | 이동, 위험 회피, 설득, 질병 압박을 한 Quest로 묶는다. |
| 2 | `escort` | `caravan_to_border_fort` | 보호, 보급, 매복 대응을 현재 resource/reputation 구조로 검증한다. |
| 2 | `dungeon_crawl` | `old_well_awakening` | village에서 underground로 확장하는 작은 던전 진입형이다. |
| 2 | `survival` | `survive_the_storm_pass` | health/food/risk/time pressure를 전면 검증한다. |
| 3 | `exploration` | `hidden_grove_discovery` | 새 장소 발견과 shrine/fey tag를 검증한다. |
| 3 | `mystery` | `vanishing_village` | 이상 현상과 생존자 추적은 좋지만 storylet 다양성이 더 필요하다. |
| 4 | `ritual` | `activate_the_old_gate` | 재료와 순서 의식 구조가 필요해 P0 이후에 적합하다. |
| 4 | `monster_hunt` | `beast_of_zarechka` | 덫/교전 표현이 필요해 combat-lite 기준 정리 후가 낫다. |
| 5 | `infiltration` | `infiltrate_the_keep` | stealth / disguise / alarm 같은 별도 규칙이 필요하다. |
| 5 | `research` | `create_a_new_spell` | 실험 폭주와 마법 연구 시스템이 더 필요하다. |
| 5 | `intrigue` | `weed_out_the_traitor` | 증언 비교와 사회 추리 상태가 필요하다. |

## 7. 추천 Batch 구성

각 Batch는 3개 내외로 잡고, 같은 Batch 안에서 Type이 겹치지 않게 구성한다.

### Batch A: Local / Investigation / Defense

| Quest ID | Type | 이유 |
|---|---|---|
| `village_well_trouble` | `local_problem` | 마을 문제 해결과 단서/지하 통로를 현재 P0로 구현하기 쉽다. |
| `ruin_mark_investigation_intro` | `investigation` | Roadmap 다음 후보이며 clue / omen / ruin 확장에 직접 연결된다. |
| `defend_the_village_night` | `defense` | 아직 없는 Defense Type을 제한 Turn과 주민 보호로 검증한다. |

### Batch B: Delivery / Escort / Dungeon Entry

| Quest ID | Type | 이유 |
|---|---|---|
| `ghost_town_medicine_run` | `delivery` | 이동, 위험 회피, 설득, 질병 압박을 검증한다. |
| `caravan_to_border_fort` | `escort` | 보호와 보급 조절을 money/reputation/resource로 검증한다. |
| `old_well_awakening` | `dungeon_crawl` | village에서 underground로 확장하는 작은 진입형 Quest다. |

### Batch C: Survival / Exploration / Mystery

| Quest ID | Type | 이유 |
|---|---|---|
| `survive_the_storm_pass` | `survival` | food/health/risk 압박을 직접 검증한다. |
| `hidden_grove_discovery` | `exploration` | 새 장소 발견과 shrine/fey tag를 검증한다. |
| `vanishing_village` | `mystery` | anomaly와 생존자 추적으로 중기 Storylet 구조를 넓힌다. |

## 8. 다음 Codex 작업 제안

1. Batch A를 한 번에 구현하지 말고 `village_well_trouble` 또는 `ruin_mark_investigation_intro` 중 하나만 먼저 구현한다.
2. 구현 전 해당 Quest의 success / partial_success / failure fixture 설계를 문서로 고정한다.
3. 새 Quest는 기존 `herb_gathering_tutorial`, `forest_path_scouting_tutorial`, `missing_porter_search_intro`, `merchant_lost_pack_recovery` 회귀 검증을 반드시 통과해야 한다.
4. `defense`, `delivery`, `escort`, `dungeon_crawl`은 각 Type당 1개씩만 추가해 Type coverage를 먼저 넓힌다.

## 9. Catalog 집계

| 항목 | 수 |
|---|---:|
| Research Collection 후보 | 50 |
| Design Guide-only 후보 | 6 |
| 구현 완료 Quest | 4 |
| Type 수 | 23 |
| Done | 4 |
| Recommended | 9 |
| Candidate | 39 |
| Deferred | 4 |

Design Guide-only 후보는 `herb_gathering_tutorial`, `ruin_mark_investigation_intro`, `old_hunter_trail_followup`, `forest_edge_camp_safety`, `sealed_ruin_entry`, `night_return_contract`다.

`old_hunter_trail_followup`은 `ruin_mark_investigation_intro` 이후 후속 조사/추적 Quest로 보고 현재 Catalog에서는 `investigation` 후보군의 후속 슬롯으로 둔다. 이름만 있고 Type 상세가 부족하므로 추천 Batch에는 넣지 않는다.
