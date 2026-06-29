# Entity Sampling Review v0.1

> 상태: [Historical] 이 문서는 과거 검토와 판단 기록을 보관하기 위한 문서다.

## 1. 문서 목적

이 문서는 Content Expansion Phase 3를 바로 실행하기 전에, FateWeaver에 필요한 entity 후보를 선별한 리뷰 결과다.

목표는 TRPG 자료를 그대로 따르는 것이 아니다. 판타지/대화형 선택 게임의 기본 재료를 참고하되, FateWeaver의 현재 구조인 `event -> choice -> result -> status/item/event_weight` 관계 안에서 표현 가능한 후보만 우선 채택한다.

v0.2 Trial Extension에서는 `data/core/ontology.yaml`에 최소 trial entity/relation을 추가한다. `data/content`, `data/scenarios`, `src`, `tools`는 수정하지 않는다.

---

## 2. 참고 기준

참고 문서:

- `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`
- `docs/07_reviews/12_TRPG_Content_Research_Notes_v0.1.md`
- `docs/02_schema/09_Content_Ontology_Model_v0.1.md`
- `data/core/ontology.yaml`
- `data/content/packs/signal_grove_pack/events.yaml`
- `data/content/packs/signal_grove_pack/items.yaml`

핵심 기준:

- 이벤트는 `상황 -> 선택 -> 대가 -> 다음 상태 변화`를 가져야 한다.
- entity 후보는 기존 Ontology-lite relation으로 설명 가능해야 한다.
- 아이템은 선택지를 열거나, 위험을 줄이거나, 비용을 전환하거나, 정보를 드러내야 한다.
- 상태는 다음 선택을 바꿀 때만 의미가 있다.
- NPC/세력/faction은 아직 독립 schema가 아니라 event/choice/result/tag/reputation으로 표현한다.
- D&D/CoC 원문 설정, 고유명, 문장, 룰 텍스트를 직접 차용하지 않는다.

---

## 3. D&D/TRPG 참고 용어 정책

FateWeaver는 판타지/대화형 선택 게임의 장르 공통 재료를 참고할 수 있다. 단, 특정 TRPG의 고유 설정을 가져오지 않는다.

사용 가능:

- 숲, 폐허, 마을, 신호, 표식, 부적, 덫, 산적, 은닉처 같은 일반 판타지/민담/장르 공통 명사
- 탐험, 매복, 거래, 휴식, 상태 악화, 굶주림, 길 잃음 같은 일반 상황/위협 명사
- 단서, 예고, 위험-보상, 선택 비용 같은 설계 용어
- FateWeaver 내부에서 새로 붙인 일반명

사용 금지:

- D&D/CoC의 고유 설정명
- D&D/CoC의 캐릭터명, 세계명, 지명, 조직명
- D&D/CoC의 고유 몬스터명이나 고유 종족/신격명
- 원문 룰 문장, flavor text, 시나리오 문장
- 특정 출판물에서만 식별되는 사건명, 주문명, 아이템명

애매한 경우:

```text
고유명처럼 보이면 사용하지 않는다.
장르 공통 명사로 바꾼다.
FateWeaver pack 테마에 맞는 일반명으로 재명명한다.
```

예:

| 피할 방향 | FateWeaver식 재명명 방향 |
|---|---|
| 특정 룰북의 고유 괴물명 | `숲의 비인격적 반응`, `어둠 속 짐승 흔적` |
| 특정 세계관의 조직명 | `가짜 구조 신호를 내는 무리`, `표식 관리자` |
| 특정 주문/마법명 | `공명 렌즈`, `검은 수액 표식`, `메아리 오염` |
| 특정 시나리오 사건명 | `거짓 구조 신호`, `되돌아오는 표식`, `위험한 경계` |

---

## 4. Relation 확장 정책

기본 원칙은 기존 `data/core/ontology.yaml` relation을 우선 사용하는 것이다.

다만 Content Expansion이 진행되면서 기존 relation으로 설명되지 않는 관계가 반복적으로 필요해지면 relation 추가를 허용한다. 이때도 1회성 이벤트 때문에 relation을 추가하지 않는다.

Relation 추가 허용 조건:

1. 2개 이상 이벤트/아이템/시나리오에서 재사용될 가능성이 있다.
2. validator, analyzer, export 중 하나 이상에서 의미 있는 분석 값이 된다.
3. 기존 tag/status/result로 표현하면 오히려 의미가 모호해진다.
4. Content Expansion Phase 3 이후에도 유지 가능한 구조다.

Relation 추가 시 필수 동시 갱신:

```text
data/core/ontology.yaml
docs/02_schema/09_Content_Ontology_Model_v0.1.md
```

Relation 추가를 보류해야 하는 경우:

- 특정 이벤트 하나만 설명한다.
- 사람이 읽는 description만으로 충분하다.
- 기존 `event_has_danger_tag`, `choice_requires_item`, `result_modifies_status`, `result_changes_event_weight`로 설명 가능하다.
- 새 relation을 추가해도 validator/analyzer/export가 사용할 수 없다.
- World Bible 또는 PRD 없이는 의미가 고정되지 않는다.

이번 리뷰 판정:

```text
clue, location, omen, hazard는 v0.2 trial entity로 추가한다.
event_reveals_clue, item_reveals_clue, event_occurs_at_location, omen_warns_about_hazard는 v0.2 trial relation으로 추가한다.
Phase 3 이후 반복 필요성이 낮으면 제거하거나 기존 relation으로 통합한다.
```

---

## 5. FateWeaver에 필요한 Entity 범주

현재 Ontology-lite 기준으로 FateWeaver에 필요한 entity 범주는 아래처럼 나뉜다.

| 범주 | 현재 schema entity | Phase 3 사용 방식 | 판단 |
|---|---|---|---|
| 이벤트 | `event` | 플레이어가 마주치는 압박 상황 | 즉시 사용 |
| 선택지 | `choice` | 안전/위험/거래/조사/아이템/생존 선택 | 즉시 사용 |
| 결과 | `result` | status, item, event_weight 변화 | 즉시 사용 |
| 아이템 | `item` | unlock, information, risk_reduce, cost_convert | 즉시 사용 |
| 상태 | `status` | health, food, money, reputation, curse | 기존 5개 유지 |
| 태그 | `tag` | region/event/danger/item/weight 분류 | 기존 tag 우선 |
| 단서 | `clue` trial | 정보 표식과 item clue payoff | Phase 3 trial |
| 장소 | `location` trial | region보다 작은 반복 장소 | Phase 3 trial |
| 징조 | `omen` trial | hazard warning/payoff | Phase 3 trial |
| 구체 위험 | `hazard` trial | 구체 조우/장애/위험 장치 | Phase 3 trial |
| 지역 | `region` | forest, village, ruin 조합 | 기존 3개 유지 |
| 시나리오 | `scenario` | 검증 노출 범위 | Phase 3 실행 시 갱신 |
| 파일 | `file` | content source 추적 | 기존 구조 유지 |
| 보상 | 별도 entity 없음 | result의 status/item/event_weight로 표현 | design-only |
| 비용 | 별도 entity 없음 | result의 status/item/remove_item/event_weight로 표현 | design-only |
| NPC/세력 | 별도 entity 없음 | event description, choice, reputation, tag로 표현 | 보류 |
| Pack 테마 | 별도 entity 없음 | 반복 tag/item/result 문법으로 표현 | design-only |

판정:

```text
새 status, NPC, faction, route graph는 지금 필요하지 않다.
Phase 3는 기존 relation과 v0.2 trial relation을 함께 사용해 최소 검증한다.
```

---

## 6. 이벤트 Entity 후보

즉시 YAML화 후보:

| 후보 | 역할 | 필요한 choice 구조 | 이유 |
|---|---|---|---|
| 갈림길/문턱 이벤트 | 경로 선택과 future weight 변화 | observe, risk, item_use | 탐험 선택 다양성을 늘린다. |
| 장애물 이벤트 | 우회/돌파/도구 사용 | safe, risky, item_based | health/food tradeoff를 만들기 쉽다. |
| 단서 발견 이벤트 | 정보 해석과 위험 예고 | investigate, ignore, item_reveal | `curious_leaning`에 필요한 판단 재료를 준다. |
| 거짓 구조 신호 이벤트 | 도움/함정/확인 선택 | investigate, gamble, item_based | 기존 pack의 신호 테마와 맞다. |
| 은신처/은닉처 이벤트 | 보상과 평판 비용 | safe_open, exploit, mark | greedy/desperate 압력을 만든다. |
| 상태 오염 이벤트 | 위험 상태 감소/증가 tradeoff | cleanse, gamble, item_based | bad tradeoff를 자연스럽게 만든다. |
| 피난처/휴식 이벤트 | 회복과 시간/식량 비용 | rest, forage, move_on | survival 압력을 만든다. |
| 매복/대치 이벤트 | combat을 일반 choice로 표현 | retreat, negotiate, item_response | 별도 combat system 없이 전투감을 준다. |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 장기 추리 사건 | 현재 scenario/run 길이에서는 단서 누적 검증이 어렵다. |
| 다단계 보스전 | combat subsystem으로 흐를 위험이 있다. |
| 특정 도시 정치 사건 | faction schema 없이 표현하면 설명문만 길어질 수 있다. |
| 전용 던전 층 구조 | 현재 region/tag 구조보다 큰 구조 변경이 필요하다. |

---

## 7. 위협/Threat Entity 후보

즉시 YAML화 후보:

| 후보 | 기존 tag 표현 | 좋은 대응 | 이유 |
|---|---|---|---|
| 길 잃음 | `lost` | mark, observe, signal item | 기존 pack 핵심 테마와 가장 잘 맞는다. |
| 덫 | `trap` | slow safe choice, tool, health risk | health/food tradeoff가 선명하다. |
| 산적/매복 | `bandit`, `physical` | retreat, bribe, smoke/flare item | combat을 choice로 처리하기 좋다. |
| 굶주림/소모 | `hunger` | forage, ration, rest | desperate profile 검증에 필요하다. |
| 상태 위험 압력 | `curse`, `ancient`, `forbidden` | avoid, cleanse, risky reward | greedy와 safe 차이를 만든다. |
| 어둠/시야 제한 | `darkness` | light/tool/observe | 단서와 위험 예고에 좋다. |
| 짐승 흔적 | `beast`, `physical` | avoid, decoy, item response | combat이 아닌 생존 위협으로 쓸 수 있다. |
| 거짓 정보 | `lost`, `bandit`, `status-risk` 조합 | investigate, item reveal | 단서 기반 선택을 강화한다. |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 정신력/광기 전용 위협 | 새 status를 유혹하므로 지금은 기존 위험 상태와 event_weight로 표현한다. |
| 날씨 시스템 | `storm` tag는 있으나 현재 pack 테마와 직접 연결이 약하다. |
| 대규모 전쟁/군대 | 현재 소규모 event 중심 루프와 맞지 않는다. |
| 불사/언데드 중심 위협 | `undead` tag는 있으나 signal grove pack의 핵심 테마가 아니다. |

---

## 8. 아이템 Entity 후보

현재 pack 아이템은 `signal_whistle`, `flare_powder`, `signal_mirror`, `forest_charm`, `trail_ribbon`, `smoke_pellet`이다. Phase 3에서는 아이템 수를 늘리는 것보다 아이템 역할이 겹치지 않게 만드는 것이 중요하다.

즉시 YAML화 후보:

| 후보 | 역할 | 대응 위험 | 채택 이유 |
|---|---|---|---|
| 신호 분필 | information, future_weight | lost, trap | 표식/갈림길/문턱 이벤트에 잘 맞고 직접 피해 감소가 아니라 경로 판단을 바꾼다. |
| 공명 렌즈 | information, risk_reduce | curse, ancient, darkness | magic/status-risk 단서 해석을 돕되 보편 안전 해답이 되지 않는다. |
| 길양식 주머니 | cost_convert, risk_reduce | hunger, lost | desperate profile의 food/health 압력을 item 소비로 전환한다. |
| 부러진 방향침 | information, probability | lost, ancient | 단서 해석에는 좋지만 효과가 넓어지지 않게 제한이 필요하다. |
| 말린 약초 붕대 | risk_reduce, healing | physical, beast | health 회복 아이템 후보지만 healing tag 남용을 조심해야 한다. |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 만능 지도 | `lost` 위험을 너무 넓게 무력화할 수 있다. |
| 상태 위험 완전 해제 부적 | 상태 위험 선택을 단순 정답으로 만들 위험이 크다. |
| 전투 무기 중심 아이템 | combat subsystem을 유도할 수 있다. |
| 금화 주머니 같은 순수 재화 | 선택 구조를 바꾸지 못하면 dead item이 된다. |

---

## 9. 상태/Status 후보

즉시 채택:

| Status | 유지 이유 |
|---|---|
| `health` | physical, trap, beast, risky movement 비용을 표현한다. |
| `food` | time, detour, rest, survival 압력을 표현한다. |
| `money` | bribe, trade, greedy reward를 표현한다. |
| `reputation` | 도움/약탈/거래 결과와 사회적 후속을 표현한다. |
| `curse` | 여러 상태 압력 중 forbidden/magic/ancient 위험과 bad tradeoff를 표현한다. |

보류 후보:

| 후보 | 보류 이유 | 현재 대체 표현 |
|---|---|---|
| fear | 새 심리 수치보다 기존 위험 상태와 event_weight로 충분하다. | `curse`, `event_weight: {curse: +1}` |
| fatigue | food/health와 역할이 겹친다. | `food`, `health` |
| trust | faction schema가 없으면 적용 범위가 좁다. | `reputation` |
| clue_progress | 단서 누적 시스템이 아직 없다. | `event_weight`, item unlock |
| light | torch/item과 darkness tag로 표현 가능하다. | item, `darkness` |
| weather_exposure | 현재 pack 핵심 테마가 아니다. | `food`, `health`, `storm` tag |

판정:

```text
Phase 3에서는 새 status를 추가하지 않는다.
상태 후보는 모두 기존 5개 status와 event_weight, item relation으로 우선 표현한다.
```

---

## 10. 단서/Clue 후보

단서는 별도 YAML entity가 아니다. Phase 3에서는 이벤트 description, investigate choice, item_based choice, result message, event_weight 변화를 통해 표현한다.

즉시 YAML화 후보:

| 후보 | 표현 방식 | 기능 |
|---|---|---|
| 반복 표식 | description + investigate result | 같은 위험이 반복된다는 판단 재료 |
| 소리 간격 | investigate choice | 안전한 타이밍/경로 판단 |
| 연기 패턴 | investigate 또는 item reveal | 진짜 구조 신호와 함정 구분 |
| 매듭 규칙 | investigate result + event_weight | village/trade/lost weight 변화 |
| 발자국 깊이 | investigate result | survival/lost 판단 |
| 검은 수액 차이 | risky investigate | reputation reward와 상태 비용 연결 |
| 벌레 빛 배열 | investigate/gamble | magic/lost tradeoff |
| 거울 반사 이상 | item_based reveal | darkness/status-risk 해석 보조 |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 장문 문서/일지 | Console log에서 정보량이 과해질 수 있다. |
| 암호 해독 체계 | 별도 clue_progress 없이 구현하면 단발 설명문이 된다. |
| 살인 사건식 추리 단서 | 현재 FateWeaver의 탐험/생존 루프와 결이 다르다. |

---

## 11. 보상/Reward 후보

즉시 YAML화 후보:

| 후보 | YAML 표현 | 좋은 사용처 |
|---|---|---|
| 식량 회복 | `status: {food: +1}` 또는 `+2` | desperate/survival choice |
| 체력 회복 | `status: {health: +1}` | rest/refuge choice |
| 돈 획득 | `status: {money: +1}` 또는 `+2` | greedy/gamble choice |
| 평판 획득 | `status: {reputation: +1}` | rescue/help/trade choice |
| 위험 상태 감소 | `status: {curse: -1}` | cleanse/item choice |
| 위험 weight 감소 | `event_weight: {lost: -1}` | safe/investigate/item choice |
| 보상 weight 증가 | `event_weight: {village: +1}` 또는 `{trade: +1}` | route/social choice |
| 아이템 해금 | `requires_item`로 미래 choice 연결 | item usefulness 검증 |
| 단서 획득 | result message + future weight | curious choice |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 경험치/레벨 | 현재 core status가 아니며 로그라이크 성장 시스템을 앞당긴다. |
| 영구 능력치 | Console Validation 단계에서 과한 확장이다. |
| 대량 재화 | money 압력을 무력화할 수 있다. |

---

## 12. 비용/Cost 후보

즉시 YAML화 후보:

| 후보 | YAML 표현 | 좋은 사용처 |
|---|---|---|
| 시간/우회 비용 | `status: {food: -1}` | safe/detour choice |
| 부상 | `status: {health: -1}` 또는 `-2` | risky/combat/obstacle choice |
| 위험 상태 증가 | `status: {curse: +1}` | gamble/magic/forbidden choice |
| 돈 지출 | `status: {money: -1}` 또는 `-2` | trade/bribe choice |
| 평판 손상 | `status: {reputation: -1}` | exploit/steal choice |
| 아이템 소모 | `consume_item: true`, `remove_item` | powerful item choice |
| 위험 weight 증가 | `event_weight: {curse: +1}` 또는 `{bandit: +1}` | delayed consequence |
| 안전 route 감소 | `event_weight: {lost: +1}` | shortcut/rush choice |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 즉사 비용 | 선택 검수와 profile 비교를 망친다. |
| 장비 파괴 다중 처리 | inventory relation이 아직 단순하다. |
| 영구 curse lock | 반복 플레이 검증 전에 과하다. |

---

## 13. NPC/세력/Faction 후보

현재는 NPC와 faction을 독립 entity로 만들지 않는다. 대신 사건 안의 역할로 사용한다.

즉시 YAML화 후보:

| 후보 | 표현 방식 | 쓰임 |
|---|---|---|
| 숲지기/표식 관리자 | trade choice + reputation 변화 | 길값, 경고, route weight 변화 |
| 가짜 구조 신호를 내는 무리 | bandit/trap danger tag | 함정/매복 이벤트 |
| 조난자 흔적의 주인 | aftermath event | 도움/약탈/평판 tradeoff |
| 낡은 은닉처의 주인 | cache event | food reward와 reputation cost |
| 마을 구조망 | village/trade weight | signal item의 정보 payoff |
| 숲의 비인격적 반응 | magic/status-risk/lost tag | NPC 없이도 mystery 압력 제공 |

보류 후보:

| 후보 | 보류 이유 |
|---|---|
| 명명된 주요 NPC | World Bible로 확장될 위험이 있다. |
| 복수 faction 평판표 | 새 schema와 UI를 요구할 가능성이 높다. |
| 장기 동료 NPC | Console Validation의 event 루프보다 큰 시스템이다. |
| 고유 조직/교단 | TRPG 원전식 설정 차용으로 흐를 위험이 있다. |

판정:

```text
Phase 3에서는 NPC/세력을 독립 YAML entity로 만들지 않는다.
event description과 choice/result에서 역할만 드러낸다.
```

---

## 14. Pack 테마 후보

즉시 채택할 pack 테마:

| 테마 | 반복 재료 | 관계로 증명할 방식 |
|---|---|---|
| 신호와 표식 | 호루라기, 거울, 리본, 분필, 매듭 | `choice_requires_item`, `result_changes_event_weight` |
| 길 잃음과 되돌아옴 | lost, fork, marker, trail | `event_has_danger_tag`, `event_weight: {lost: ...}` |
| 거짓 구조 신호 | smoke, bandit, trap, reputation | `event_has_danger_tag`, `result_modifies_status` |
| 생존의 윤리 | ration, cache, survivor, reputation | `result_modifies_status` |
| 상태 위험과 해석 실패 | curse, ancient, forbidden, magic clue | `event_has_danger_tag`, `result_changes_event_weight` |
| 빛과 시야 | darkness, mirror, flare, insects | `item_counters_tag`, item-based reveal |

보류할 pack 테마:

| 테마 | 보류 이유 |
|---|---|
| 대도시 정치극 | 현재 forest/village/ruin pack과 멀다. |
| 거대 던전 탐험 | 별도 구조와 장기 맵이 필요하다. |
| 신화적 고유 존재 중심 사건 | World Bible과 원전 차용 위험이 있다. |
| 전투 캠페인 | combat subsystem으로 흐를 위험이 있다. |

---

## 15. 즉시 YAML화할 후보와 보류할 후보

즉시 YAML화할 후보:

```text
event:
  - 갈림길/문턱
  - 장애물
  - 단서 발견
  - 거짓 구조 신호
  - 은신처/은닉처
  - 상태 오염/위험
  - 피난처/휴식
  - 매복/대치

threat:
  - lost
  - trap
  - bandit
  - physical
  - hunger
  - curse
  - ancient
  - darkness
  - beast
  - false signal

item:
  - signal_chalk
  - resonance_lens
  - waybread_pouch
  - broken_compass_needle
  - herbal_bandage

clue:
  - 반복 표식
  - 소리 간격
  - 연기 패턴
  - 매듭 규칙
  - 발자국 깊이
  - 검은 수액 차이
  - 벌레 빛 배열
  - 거울 반사 이상
```

보류할 후보:

```text
status:
  - fear
  - fatigue
  - trust
  - clue_progress
  - light
  - weather_exposure

npc/faction:
  - 명명된 주요 NPC
  - 복수 faction 평판표
  - 장기 동료 NPC
  - 고유 조직/교단

system:
  - 장기 추리 사건
  - 다단계 보스전
  - 대도시 정치 사건
  - 던전 층 구조
```

---

## 16. Entity/Ontology Gap Review

Phase 3 콘텐츠 작성 전에 현재 Entity Sampling Catalog가 기존 Ontology-lite에만 과하게 맞춰진 것은 아닌지 재검토했다. v0.2 결론은 `clue`, `location`, `omen`, `hazard`를 trial entity로 추가하고, Phase 3에서 검증 가능한 최소 relation 4개를 trial 상태로 추가하는 것이다.

### 16.1 Entity 후보별 의미 손실 평가

| Entity 후보 | 현재 표현 방식 | 의미 손실 | 판정 | 이유 |
| --- | --- | --- | --- | --- |
| `clue` | `revealed_clue_tags`, `reveals_clue_tags` | 단서 노출량과 회수 여부를 analyzer가 직접 세기 어렵다. | v0.2 trial 채택 | clue가 2개 이상 이벤트/아이템에서 반복되면 유지 후보다. |
| `foreshadowing` | result message, later event weight 변화 | 경고와 후속 payoff 연결이 로그에서 흐려진다. | Phase 3 trial | omen/clue와 함께 반복되면 `clue_foreshadows_event` 검토 가치가 있다. |
| `location` | `location_tags` | 숲 안의 특정 장소 반복 방문이나 route 연결을 표현하기 어렵다. | v0.2 trial 채택 | region보다 작은 장소 coverage를 검증한다. |
| `hazard` | `hazard_tags`, `counters_hazard_tags` | 넓은 위험 분류와 구체 장애가 섞이면 counterplay 분석이 흐려진다. | v0.2 trial 채택 | `danger_tags`는 broad 위험, `hazard_tags`는 구체 조우/장애로 분리한다. |
| `faction` | reputation status, event description | faction별 관계 변화와 선택 선호 분석은 불가능하다. | 문서상 보류 | Phase 3 규모에서는 faction schema가 과하다. |
| `npc_role` | event description, choice text | 협상 대상/목격자/구조자 같은 역할 분석은 어렵다. | 문서상 보류 | 독립 NPC 시스템 없이 사건 역할로 처리한다. |
| `resource_pressure` | health, food, money, reputation, curse status | 압박의 원인과 서사적 명칭은 잃지만 수치 변화는 분석 가능하다. | 기존 relation으로 충분 | `result_modifies_status`가 직접 대응한다. |
| `mystery_thread` | event weight 변화, clue성 message | 장기 사건 줄기의 진행도를 직접 추적하기 어렵다. | 문서상 보류 | 장기 추리 시스템은 Phase 3 범위를 넘는다. |
| `sanctuary` | rest/recovery event archetype, safety tag | 안전지대의 위치성이나 재방문성은 약하다. | Phase 3 trial | 반복 쉼터가 생길 때 location/route 후보와 함께 본다. |
| `omen` | `omen_tags`, `creates_omen_tags` | 어떤 hazard를 경고했는지 구조적으로 남지 않는다. | v0.2 trial 채택 | `omen_warns_about_hazard`로 최소 warning/payoff를 검증한다. |
| `rumor` | social event message, reputation result | 정보 신뢰도와 출처가 구조화되지 않는다. | Phase 3 trial | clue의 하위 표현으로 먼저 사용하고 독립 entity는 보류한다. |
| `route` | event weight 변화, region 이동 암시 | 어느 길이 어느 location으로 이어지는지 분석할 수 없다. | Phase 3 trial | route 선택지가 반복되면 `route_leads_to_location` 후보가 된다. |
| `encounter_role` | event tag, choice type, danger tag | 역할별 통계는 제한되지만 현재 slice 분석에는 충분하다. | 기존 relation으로 충분 | combat/social/exploration 구분을 새 entity로 만들 필요는 아직 없다. |

### 16.2 Relation 후보별 gap 판정

| Relation 후보 | 기존 relation으로 충분한가 | 의미 손실 | 판정 | 지금 추가 여부 |
| --- | --- | --- | --- | --- |
| `event_reveals_clue` | 부분 충분 | clue 노출량과 회수 흐름이 직접 집계되지 않는다. | v0.2 trial 채택 | 추가 |
| `clue_foreshadows_event` | 부족 | 경고와 후속 이벤트 연결이 message에 묻힌다. | Phase 3 trial | 추가 안 함 |
| `event_occurs_at_location` | 부분 충분 | region보다 작은 장소 반복성이 사라진다. | v0.2 trial 채택 | 추가 |
| `location_has_hazard` | 부분 충분 | hazard가 장소 고유 속성인지 사건 속성인지 구분이 흐리다. | 문서상 보류 | 추가 안 함 |
| `choice_interacts_with_npc_role` | 부족 | NPC 역할 기반 선택 분석이 어렵다. | 문서상 보류 | 추가 안 함 |
| `choice_affects_faction` | 부족 | faction별 관계 변화가 reputation 하나로 합쳐진다. | 문서상 보류 | 추가 안 함 |
| `result_changes_resource_pressure` | 충분 | 압박의 이름은 잃지만 상태 변화는 보존된다. | 기존 relation으로 충분 | 추가 안 함 |
| `event_advances_mystery_thread` | 부족 | 장기 thread 진행도는 분석할 수 없다. | 문서상 보류 | 추가 안 함 |
| `item_reveals_clue` | 부분 충분 | item 사용이 clue 발견으로 이어졌는지 직접 집계되지 않는다. | v0.2 trial 채택 | 추가 |
| `item_mitigates_hazard` | 충분 | hazard가 tag로 표현될 때 대응 관계가 유지된다. | 기존 relation으로 충분 | 추가 안 함 |
| `route_leads_to_location` | 부족 | route graph를 만들 수 없다. | Phase 3 trial | 추가 안 함 |
| `omen_warns_about_hazard` | 부족 | 징조와 위험의 대응이 message에만 남는다. | v0.2 trial 채택 | 추가 |

### 16.3 v0.2 trial source field

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

한계:

- validator/analyzer/export가 아직 이 trial field를 소비하지 않을 수 있다.
- Phase 3 콘텐츠가 최소 2개 이상 이벤트/아이템에서 사용하지 않으면 제거 또는 통합 후보다.
- `danger_tags`는 넓은 위험 분류로 유지하고, `hazard_tags`는 구체 조우/장애/위험 장치에만 사용한다.

### 16.4 Phase 3 trial 기준

Phase 3에서 아래 조건이 확인되면 v0.2 trial relation을 유지 후보로 본다.

- 같은 후보 relation이 2개 이상 이벤트/아이템/시나리오에서 반복된다.
- 기존 tag/status/result로 표현했을 때 analyzer metric 이름이 모호해진다.
- Console Simulator 로그나 export에서 해당 관계를 별도 집계해야 한다.
- relation의 source field와 target field를 YAML에서 명확히 지정할 수 있다.
- Phase 3 이후에도 계속 유지될 콘텐츠 구조다.

v0.2 trial relation은 `event_reveals_clue`, `item_reveals_clue`, `event_occurs_at_location`, `omen_warns_about_hazard` 네 가지다. `clue_foreshadows_event`, `route_leads_to_location`, `location_has_hazard`는 계속 보류한다.

---

## 17. Reject 기준

아래 후보는 Phase 3에서 채택하지 않는다.

- 기존 Ontology-lite relation으로 설명할 수 없는 후보
- 새 status/core tag를 먼저 요구하는 후보
- 새 relation을 요구하지만 relation 추가 조건을 만족하지 못하는 후보
- item이 있으면 항상 정답이 되는 후보
- item이 없으면 진행이 막히는 후보
- 단서가 다음 선택 판단에 쓰이지 않고 설명문으로만 존재하는 후보
- 보상/비용이 status나 event_weight에 반영되지 않는 후보
- combat을 별도 전투 시스템처럼 만들게 하는 후보
- NPC/faction schema를 요구하는 후보
- TRPG 원문 설정, 고유명, 문장, 룰 텍스트를 직접 차용하는 후보
- World Bible 또는 PRD 작성으로 넘어가야만 설명되는 후보

---

## 18. 최종 판정

```text
ONTOLOGY_LITE_V0_2_TRIAL_READY
```

판정 이유:

- 현재 FateWeaver는 GraphDB나 별도 ontology engine 없이 v0.2 trial entity/relation만으로 Phase 3 콘텐츠 표본을 검증할 수 있다.
- 즉시 YAML화 후보는 기존 event/choice/result/item/status/tag 구조와 v0.2 trial field 안에서 표현 가능하다.
- 보류 후보는 새 schema, 새 시스템, World Bible, 원전 차용 위험이 있어 지금 단계에 맞지 않는다.
- gap review 결과, `event_reveals_clue`, `item_reveals_clue`, `event_occurs_at_location`, `omen_warns_about_hazard`는 Phase 3에서 최소 검증할 가치가 있어 trial relation으로 추가했다.
- Phase 3는 먼저 채택 후보를 작은 batch로 YAML화하고 Console Simulator metric으로 검증하는 순서가 맞다.
