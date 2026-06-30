# [Current] Quest Expansion Roadmap v0.1

> 상태: [Current] Gameplay P0 이후 Quest 추가 순서와 첫 추가 Quest 설계 방향을 정리한 계획 문서.

## 1. 문서 목적

이 문서는 Gameplay P0 이후 Quest(퀘스트)를 어떤 순서로 확장할지 정리한다.

이번 단계의 목적은 새 Quest(퀘스트)를 바로 구현하는 것이 아니라, Quest(퀘스트) 추가 전에 문서 기준, 후보 우선순위, 구현 전 점검 항목을 고정하는 것이다.

## 2. 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`

## 3. 현재 P0 상태 요약

현재 Gameplay P0는 다음을 가진다.

- Quest Layer(퀘스트 계층)
- Expedition Clock(원정 시계)
- 3-Card Choice(3장 카드 선택)
- Multi-Select(다중 선택)
- Objective Evaluation(목표 평가)
- Card Candidate Score / Tier / Weight(카드 후보 점수 / 등급 / 가중치)
- Seeded Tier Variety(시드 기반 등급 내 다양성)
- Result Reason Mapping(결과 이유 매핑)
- Score Breakdown(점수 분해)
- Quest Report(퀘스트 보고서)
- JSON/Text MUD Logs(JSON/텍스트 MUD 로그)

## 4. Quest 추가를 시작할 수 있는 이유

첫 추가 Quest(퀘스트)를 1개씩 구현할 수 있는 최소 기반은 갖춰졌다.

- Objective(목표) 유형이 `collect_item`, `discover_clue`, `return_to_region`, `keep_resource_at_least`, `optional_action`을 처리한다.
- 3-Card Choice(3장 카드 선택)가 slot role 균형을 유지한다.
- Card Candidate Pool(카드 후보 풀)이 Tier(등급), Weight(가중치), Seeded Variety(시드 기반 다양성)를 가진다.
- success / partial_success / failure(성공 / 부분 성공 / 실패) 결과를 Quest Report(퀘스트 보고서)에 남긴다.
- optional_action(선택 행동) completed / failed(완료 / 실패) 경로가 검증됐다.

## 5. 아직 Quest 대량 확장을 하지 않는 이유

Quest(퀘스트) 10개 대량 확장은 아직 이르다.

- Storylet/Event(스토리 조각/이벤트)가 직접 card candidate hints(카드 후보 힌트)를 공급하는 구조가 막 도입되는 단계다.
- Repeat Cooldown Memory(반복 쿨다운 기억)는 P0 수준이며 장기 기억 시스템은 아니다.
- 각 Quest(퀘스트)는 success / partial_success / failure fixture(성공 / 부분 성공 / 실패 픽스처)를 따로 검증해야 한다.
- 새 Quest(퀘스트)가 기존 `herb_gathering_tutorial`을 깨뜨리지 않는지 한 개씩 확인해야 한다.

따라서 Quest(퀘스트)는 한 번에 1개씩 추가한다.

## 6. Quest 제작 기준 요약

Quest(퀘스트)는 고정 줄거리가 아니라 게임 구조 단위다.

```text
목적
+ 제한 시간
+ 지역
+ Objective(목표)
+ 3-Card 패턴
+ Storylet tag(스토리 조각 태그)
+ 자원 변화
+ 성공 / 부분 성공 / 실패
+ 보상 / 해금
```

좋은 Quest(퀘스트)는 다음 조건을 만족한다.

- 한 문장 목표가 명확하다.
- 시작 지역과 목표 지역이 있다.
- Day / Turn(일차 / 턴) 압박이 있다.
- 3-Card slot role을 만들 수 있다.
- Objective(목표)가 기존 evaluator(평가기)로 처리 가능하다.
- 보상과 다음 Quest(퀘스트) 해금 방향이 있다.

## 7. Quest 추가 우선순위

1. `forest_path_scouting_tutorial`
2. `missing_porter_search_intro`
3. `merchant_lost_pack_recovery`
4. `ruin_mark_investigation_intro`
5. `village_well_trouble`

실제 구현은 한 번에 1개 Quest(퀘스트)씩 한다.

현재 구현 상태:

- `forest_path_scouting_tutorial`: data fixture(데이터 고정물) 구현 및 success / partial_success / failure(성공 / 부분 성공 / 실패) scenario(시나리오) 검증 완료.
- `missing_porter_search_intro`: data fixture(데이터 고정물) 구현 및 rescue / time pressure / partial_success(구조 / 시간 압박 / 부분 성공) scenario(시나리오) 검증 완료.
- 다음 후보: `merchant_lost_pack_recovery`.

## 8. 첫 추가 Quest: forest_path_scouting_tutorial

첫 추가 Quest(퀘스트)는 `forest_path_scouting_tutorial`로 정한다.

이유:

- 기존 `herb_gathering_tutorial` 다음 단계로 자연스럽다.
- 수집에서 조사/위험 판단으로 학습 범위를 확장한다.
- 현재 forest(숲), clue(단서), risk(위험), food(식량), reputation(평판) 구조를 재사용할 수 있다.
- 3-Card Choice(3장 카드 선택), Card Candidate Pool(카드 후보 풀), Tier(등급), Seeded Variety(시드 기반 다양성) 검증에 적합하다.
- Quest(퀘스트) 10개 확장 전에 시스템 재사용성을 검증하기 좋다.

설계 초안:

```yaml
id: forest_path_scouting_tutorial
title: 숲길 안전 조사
quest_type: scouting
rank: novice

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

  - id: keep_food
    type: keep_resource_at_least
    target: food
    value: 2
    required: false
    failure_reason: optional_failed
    score_key: resource_management

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

위 YAML은 설계 초안이었고, 이후 `data/content/base/quests.yaml`에 실제 fixture(고정 데이터)로 추가됐다.

## 9. 두 번째 Quest: missing_porter_search_intro

두 번째 Quest(퀘스트)는 `missing_porter_search_intro`로 구현했다.

이유:

- `forest_path_scouting_tutorial` 다음 단계로 rescue(구조)와 time pressure(시간 압박)를 검증하기 좋다.
- 기존 `discover_clue`, `optional_action`, `return_to_region`, `keep_resource_at_least` objective(목표)를 재사용한다.
- Storylet/Event Hint(스토리 조각/이벤트 힌트)가 Quest(퀘스트) 전용 Card Candidate(카드 후보)를 밀어주는 구조를 검증한다.
- `quest_ids` gate(퀘스트 ID 게이트)로 기존 herb/forest tutorial(약초/숲길 튜토리얼)을 오염시키지 않는다.

구현 결과:

- `find_porter_trace`: `porter_trace` clue(단서) 발견.
- `resolve_porter_fate`: `porter_fate_resolved` optional_action(선택 행동)을 required(필수) objective(목표)로 사용.
- `return_to_village`: `porter_reported` progress(진행도)로 마을 보고 완료.
- `recover_lost_pack`: optional_action(선택 행동) 보조 목표.
- success / partial_success / failure(성공 / 부분 성공 / 실패) scenario(시나리오)를 각각 검증했다.

## 10. 세 번째 Quest 이후 후보

- `merchant_lost_pack_recovery`: Money(돈), Reputation(평판), Recovery(회수) 도입.
- `ruin_mark_investigation_intro`: Clue(단서), Omen(징조), Ruin(폐허) 확장.
- `village_well_trouble`: Village(마을) 지역 이벤트 확장과 local problem(지역 문제) 검증.

## 11. Quest 구현 전 필요한 점검

- 새로운 Quest(퀘스트)가 기존 objective evaluator(목표 평가기)로 처리 가능한가?
- `discover_clue` objective(목표)가 실제 progress/clue(진행도/단서)와 연결 가능한가?
- `keep_resource_at_least` objective(목표)가 현재 resource snapshot(자원 스냅샷)과 연결 가능한가?
- 신규 optional_action(선택 행동)을 card_rules로 만들 수 있는가?
- forest/trail/beast_tracks storylet/context tag(스토리 조각/컨텍스트 태그)를 공급할 수 있는가?
- 3-card slot이 `quest_progress` / `risk_discovery` / `resource_alternative`로 구성 가능한가?
- success / partial_success / failure fixture(성공 / 부분 성공 / 실패 픽스처)를 만들 수 있는가?
- 기존 `herb_gathering_tutorial`이 깨지지 않는가?
- 기존 `forest_path_scouting_tutorial`이 깨지지 않는가?

## 12. 다음 Codex 작업 제안

1. `merchant_lost_pack_recovery` Quest(퀘스트)를 data fixture(데이터 픽스처)로 1개만 추가한다.
2. Money / Reputation / Recovery(돈 / 평판 / 회수) 흐름이 기존 evaluator(평가기)로 충분한지 검증한다.
3. `herb_gathering_tutorial`, `forest_path_scouting_tutorial`, `missing_porter_search_intro`가 깨지지 않는지 회귀 검증한다.
