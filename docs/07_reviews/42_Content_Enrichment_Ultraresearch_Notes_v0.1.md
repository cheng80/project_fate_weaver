# [Research] Content Enrichment Ultraresearch Notes v0.1

> 상태: [Research] FateWeaver Content Enrichment Catalog 작성을 위한 외부 자료 조사와 변환 원칙 기록.

## 1. 작업 목적

이번 작업은 Content Enrichment Pack 구현이 아니다. `data/`, `src/`, `tests/`를 수정하지 않고, 다음 단계에서 Card Candidate / Clue / Omen / Item / Ending 후보를 확장할 수 있도록 조사 근거와 변환 원칙을 정리한다.

선행 조건:

| 조건 | 확인 문서 | 판정 |
|---|---|---|
| Event Hint Split 완료 | `docs/07_reviews/40_Event_Hint_Split_Loader_Support_Result_v0.1.md` | PASS |
| Data Split Coverage Audit 완료 | `docs/07_reviews/41_Data_Split_Coverage_Audit_v0.1.md` | PASS |

Data Split Coverage Audit 기준 현재 inventory:

| 항목 | 수 |
|---|---:|
| Loaded Quest IDs | 22 |
| Loaded Card IDs | 111 |
| Loaded Event IDs | 55 |
| Scenario files | 51 |
| Active quest scenarios | 47 |
| Unknown cross-reference | 0 |

추가 read-only inventory:

| 항목 | 수 | 해석 |
|---|---:|---|
| Item data | 12 | Pack 2 확장 여지 큼 |
| Ending data | 2 | Run review 다양성 부족 |
| P0 Card Rule | 111 | Pack 1에서 반복 감소와 clue/omen payoff 보강 가능 |

## 2. 리서치 경계

외부 자료는 구조, 패턴, 소재 역할만 참고한다.

- 고유 시나리오명, 장소명, NPC명, 문장, 대사, 세계관 설정은 복제하지 않는다.
- FateWeaver 후보는 기존 Category, Quest Type, slot_role, `quest_ids` gate, split file 구조에 맞춰 새로 작성한다.
- 이번 문서는 구현 후보를 준비하지만 실제 data/schema/code/test를 추가하지 않는다.
- `result_type`, `failure_kind`, `character_outcome` 의미는 건드리지 않는다.

## 3. 참고 출처

기존 Quest 리서치에서 사용한 외부 자료를 적극 재사용했다.

| Source | 이번 작업에서 참고한 구조 |
|---|---|
| Dungeon World SRD - Fronts: https://www.dungeonworldsrd.com/gamemastering/fronts/ | Danger, Grim Portent, Stakes Question을 Omen 후보와 Ending residue로 변환 |
| The Alexandrian - Three Clue Rule: https://thealexandrian.net/wordpress/1118/roleplaying-games/three-clue-rule | 한 결론에 여러 단서 route를 배치하는 Clue redundancy |
| The Alexandrian - Node-Based Scenario Design: https://thealexandrian.net/wordpress/7949/roleplaying-games/node-based-scenario-design-part-1-the-plotted-approach | clue가 다음 node/route를 여는 구조 |
| Sly Flourish - Adventure Hooks: https://slyflourish.com/adventure_hooks.html | Card Candidate를 짧은 decision hook으로 압축 |
| Sly Flourish - Running Investigations and Mysteries: https://slyflourish.com/running_investigations_and_mysteries.html | mystery를 정답 맞히기가 아니라 위험 판단 루프로 취급 |
| Sly Flourish - What Separates Adventure Types: https://slyflourish.com/what_separates_adventure_types.html | Quest Category별 플레이 압력 분류 |
| Old-School Essentials SRD - Dungeon Adventuring: https://oldschoolessentials.necroticgnome.com/srd/index.php/Dungeon_Adventuring | 탐험 turn, 문/함정/자원 소모, 후퇴 판단 |
| Old-School Essentials SRD - Encounters: https://oldschoolessentials.necroticgnome.com/srd/index.php/Encounters | 조우 반응, 거리, surprise를 card risk로 변환 |
| Old-School Essentials SRD - Hazards and Challenges: https://oldschoolessentials.necroticgnome.com/srd/index.php/Hazards_and_Challenges | hazard와 counterplay item 후보 |
| Pelgrane Press - How I Prep Adventures in GUMSHOE: https://pelgranepress.com/2018/02/01/how-i-prep-adventures-in-gumshoe/ | 핵심 정보는 막지 않고 비용/위험으로 차등화 |
| Pelgrane Press - A Taxonomy of Investigations: https://pelgranepress.com/2023/03/08/a-taxonomy-of-investigations/ | 조사 유형별 clue role 분리 |
| Roleplaying Tips - 5 Room Dungeons: https://www.roleplayingtips.com/5-room-dungeons/ | 입구/퍼즐/후퇴/보상/반전 구조를 5-turn motif로 변환 |
| One Page Dungeon Contest: https://www.dungeoncontest.com/ | 짧은 공간, 명확한 obstacle, compact reward loop |
| RogueBasin: https://www.roguebasin.com/index.php/Main_Page | roguelike 반복 run에서 item과 위험의 systemic role |
| NetHack Wiki - Identification: https://nethackwiki.com/wiki/Identification | item 정보 불확실성과 reveal/cost tradeoff |

## 4. FateWeaver 변환 원칙

| 외부 패턴 | FateWeaver 변환 |
|---|---|
| Adventure hook | 1-turn Card Candidate title/effect/risk_hint |
| Grim portent | Omen tag + future danger weight + ending residue |
| Dungeon room | Event Hint + 3-card slot pressure |
| Core clue | 진행 차단이 아니라 safer route, partial_success 방지, reward 증폭 |
| Hazard counter | Item 역할 `unlock`, `risk_reduce`, `cost_convert`, `information`, `future_weight` |
| Fail forward | `partial_success` reason과 ending note를 풍부하게 하되 의미 변경 금지 |
| One-page dungeon | 5개 이하 motif로 쪼개어 repeated turn fatigue 감소 |
| Roguelike identification | item이 항상 정답이 아니라 정보/위험/소모 tradeoff를 만든다 |

## 5. Pack 1 설계 원칙

Pack 1은 Card Candidate +40, Clue +25, Omen +20을 목표로 한다.

권장 분배:

| Category | Card | Clue | Omen | 목적 |
|---|---:|---:|---:|---|
| Local Problem | 7 | 4 | 3 | 마을 정보, 사회적 비용, 평판 판단 |
| Investigation / Mystery | 8 | 6 | 4 | 단서 redundancy와 잘못된 해석 위험 |
| Defense / Threat | 7 | 4 | 4 | 위협 예고, 준비/대피/덫 선택 |
| Travel / Delivery / Escort | 7 | 4 | 3 | 길, 보급, 우회, 동행자 압박 |
| Ruin / Dungeon / Ritual | 6 | 4 | 4 | 봉인, 룬, hazard counterplay |
| Survival / Exploration | 5 | 3 | 2 | 자원 보존, 길찾기, 은신처 발견 |
| 합계 | 40 | 25 | 20 | 25-35 turn 반복 감소 |

작성 규칙:

- 새 quest-specific Card Rule은 해당 category split file에 둔다.
- 모든 새 quest-specific Card Rule은 `quest_ids`를 가진다.
- 새 Event Hint는 category split file에 두고 `card_candidate_hints`와 `quest_ids` 정합성을 유지한다.
- Clue/Omen은 진행 차단 조건이 아니라 선택 평가 자료로 먼저 쓴다.

## 6. Pack 2 설계 원칙

Pack 2는 Item +25, Ending +8을 목표로 한다.

권장 Item 역할 분배:

| 역할 | 후보 수 | 용도 |
|---|---:|---|
| `unlock` | 5 | 특정 route/choice 개방 |
| `risk_reduce` | 5 | hazard 피해 완화 |
| `cost_convert` | 5 | health/status 비용을 item/money/time 비용으로 전환 |
| `information` | 5 | clue reveal, false signal 구분 |
| `future_weight` | 5 | 다음 Event 후보 가중치 변화 |

Ending 확장 원칙:

- Ending은 Quest outcome 의미를 재정의하지 않는다.
- Ending은 run residue를 설명한다: 생존 상태, 주요 clue 수, omen 방치, reputation/money, item 사용, optional objective.
- Ending 조건은 기존 `success`, `partial_success`, `failure`, `character_outcome`와 충돌하지 않게 둔다.

## 7. Standard Run 25-35 Turn 연결

Catalog는 다음 검증을 전제로 작성한다.

| 검증 질문 | 관찰 surface |
|---|---|
| 같은 카드가 반복 노출되는가 | JSON `card_candidate_pool`, Text MUD turn log |
| clue가 partial_success를 다양하게 만드는가 | Quest Report `objective_results`, `result_reason` |
| omen이 위험 예고와 payoff를 가지는가 | `gain_omens`, Event Hint, next event tags |
| item이 선택지와 결과를 바꾸는가 | unavailable/available card, item delta, status delta |
| ending이 run review를 풍부하게 하는가 | final report / ending id / text log |

## 8. EXPAND 결과

조사 중 남은 lead는 구현 단계로만 의미가 있다.

| Lead | 판정 |
|---|---|
| clue accumulation system 추가 | 이번 범위 밖. Pack 1은 현재 schema의 `gain_clues`, tag, objective progress로 제한 |
| long-term repeat cooldown 저장 | 이번 범위 밖. Standard Run 검증에서 반복도만 관찰 |
| Storylet Pool 전체 시스템 | 이번 범위 밖. Event Hint + card_candidate_hints 기반으로 제한 |
| Item/Ending split 구조 | 이번 범위 밖. Pack 2 전에 별도 Refactor Gate 필요 시 판단 |

## 9. 결론

Content Enrichment 선행 조건은 충족됐다. 다음 작업은 `docs/06_plans/08_Content_Enrichment_Catalog_v0.1.md`를 입력으로 사용해 Pack 1을 먼저 실행하는 것이 적절하다.

권장 순서:

1. Pack 1: Card + Clue + Omen 확장.
2. Pack 1 후 Data/Scenario 검증.
3. Pack 2: Item + Ending 확장.
4. Standard Run 25-35 Turn 검증.
