# Project FateWeaver Docs Index

## 문서 목적

이 문서는 `docs/` 폴더의 역할별 구조와 현재 문서 목록을 정리한다.

현재 단계는 PRD 작성 전이며, Console Simulator 구현 검수 PASS 이후 콘텐츠 확장 준비와 Ontology-lite 유지 관리 기준을 명확히 하는 단계에서, **실게임형 텍스트 모험 시뮬레이터 구조 재정의**를 추가로 반영한다.

새로운 상위 목표는 FateWeaver를 단순 로그 검증기나 YAML/schema 검증 도구가 아니라, **Quest Layer, Expedition Clock, Ontology Director, 3-Card Choice UI, Multi-Select Resolver 기반의 DM형 텍스트 모험 게임 구조**로 확장하는 것이다.

---

## 현재 최상위 기준

현재 FateWeaver의 최신 게임 구조 기준은 다음 문서에서 시작한다.

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`

Gameplay Replan 관련 새 작업을 시작할 때는 위 문서를 먼저 읽고, 다음 문서들을 순서대로 확인한다.

1. `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
2. `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
3. `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
4. `docs/04_codex/14_Codex_Gameplay_Replan_Brief_v0.1.md`
5. `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`
6. `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
7. `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`

기존 Console Validation 문서는 과거 기준선으로 유지한다.  
새 구현/기획 작업의 최상위 기준은 Gameplay Replan 문서들을 따른다.

---

## 문서 상태 표기 기준

문서 제목 또는 문서 상단 안내문에는 필요에 따라 다음 상태 표기를 사용한다.

| 표기 | 의미 |
|---|---|
| `[Current]` | 현재 최상위 기준 문서 |
| `[Baseline]` | 과거 구현 기준선 또는 완료된 기준선 |
| `[Historical]` | 과거 기록, 리뷰, 회고, 커밋 요약 |
| `[Superseded]` | 최신 기준으로 대체되었으나 참고용으로 유지하는 문서 |

파일명은 변경하지 않는다.  
상태 표기는 문서 제목이나 문서 상단 안내문에만 적용한다.

현재 Gameplay Replan 관련 새 작업의 기준은 `[Current]`로 본다.  
기존 Console Validation 문서는 `[Baseline]` 또는 `[Superseded]`로 본다.  
과거 리뷰와 커밋 요약은 `[Historical]`로 본다.

---

# 1. 폴더 구조

```text
docs/
  00_index/
  01_foundation/
  02_schema/
  03_specs/
  04_codex/
  05_validation/
  06_plans/
  07_reviews/
```

---

# 2. 00_index

역할:

- 문서 전체 목록
- 문서 탐색 시작점
- 각 문서의 책임 요약

문서:

- `docs/00_index/README_Docs_Index.md`
  - 전체 문서 구조와 문서별 책임을 정리한다.

---

# 3. 01_foundation

역할:

- 프로젝트 기준선
- 최상위 구조
- 데이터 아키텍처
- Flutter 이전 전제
- 실게임형 텍스트 모험 구조 재정의

문서:

- `docs/01_foundation/00_Project_FateWeaver_Current_Baseline_v0.7.md`
  - 현재 단계가 Console Validation임을 고정한다.
- `docs/01_foundation/01_Project_Structure_Guide_v0.1.md`
  - `docs/`, `data/`, `src/`, `tools/`, `logs/`, `archive/`, 향후 `fate_weaver/`의 역할을 정의한다.
- `docs/01_foundation/02_Data_Architecture_v0.7.md`
  - `data/core`, `data/content`, `data/scenarios` 구조와 장기 데이터 원칙을 정의한다.
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
  - FateWeaver를 Quest Layer, Expedition Clock, Ontology Director, 3-Card Choice UI, Multi-Select Resolver 기반의 실게임형 텍스트 모험 구조로 재정의한다.

---

# 4. 02_schema

역할:

- YAML 원천 데이터 계약
- fixture 데이터 기준
- Flutter export 계약
- 콘텐츠 관계 분석을 위한 Ontology-lite 계약
- Quest / Expedition / Card 기반 게임 구조 데이터 계약

문서:

- `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
  - scenario filter, choice-level requires, unavailable choice, metric, combat policy 계약을 정의한다.
- `docs/02_schema/06_Fixture_Data_Plan_v0.3.md`
  - Console Validation fixture 데이터의 최소 기준을 정의한다.
- `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`
  - YAML에서 Flutter JSON artifact로 이전하는 계약을 정의한다.
- `docs/02_schema/09_Content_Ontology_Model_v0.1.md`
  - `data/core/ontology.yaml` 기반의 Ontology-lite v0.2 trial 콘텐츠 관계 모델을 정의한다.
- `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`
  - TRPG 리서치에서 추출한 이벤트, 선택지, 위험, 보상, 단서, 아이템 상호작용 표본 추출 기준을 정의한다.
- `docs/02_schema/11_Entity_Sampling_Catalog_v0.1.md`
  - Phase 3 entity 후보와 Ontology-lite v0.2 trial entity/relation 채택 기준을 정의한다.
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
  - Quest, Expedition Clock, Storylet, Card Candidate, Multi-Select, Result, Score, Quest Report를 데이터 계약으로 정의한다.
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
  - FateWeaver Quest를 목적, 제한 시간, 지역, Objective, 3-Card 패턴, Storylet tag, 자원 변화, 성공/부분 성공/실패, 보상/해금으로 설계하기 위한 제작 기준 문서다.
---

# 5. 03_specs

역할:

- 실제 실행 사양
- 콘솔 시뮬레이터 동작 계약
- 로그 출력 계약
- 실게임형 텍스트 모험 시뮬레이터 실행 계약

문서:

- `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`
  - Console Validation 시뮬레이터의 로드, 선택, 로그, 분석, 금지 구현 범위를 정의한다.
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
  - Console Simulator가 단순 로그 검증기가 아니라 텍스트 기반 실게임 프로토타입으로 작동하기 위한 실행 사양을 정의한다.

---

# 6. 04_codex

역할:

- Codex 구현 지시 기준
- 허용/금지 작업 범위
- 구현 전후 응답 형식
- 게임 구조 재정의 후속 구현 브리프

문서:

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
  - Codex가 Gameplay Replan 관련 작업을 시작하기 전에 반드시 먼저 읽어야 하는 최신 기준 문서다.
- `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`
  - Codex가 Console Validation 프로토타입을 만들 때 따라야 할 작업 브리프다.
- `docs/04_codex/14_Codex_Gameplay_Replan_Brief_v0.1.md`
  - Codex가 기존 구조를 해치지 않고 게임 구조 재정의와 후속 구현 계획을 수행하기 위한 작업 브리프다.

---

# 7. 05_validation

역할:

- 착수 전/확장 전 체크리스트
- 검증 게이트
- P0/P1 반영 확인
- 콘텐츠 확장 readiness 기준
- Quest / Day-Turn / 3-Card UI / Multi-Select / 경제·점수·평판 연결 검증
- Gameplay Replan 완료 승인 기준

문서:

- `docs/05_validation/07_Console_Validation_Checklist_v0.1.md`
  - Writing-plans와 구현 착수 전에 확인해야 할 구조, 데이터, 계약 체크리스트다.
- `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
  - Console Simulator PASS 이후 콘텐츠 확장 전에 확인해야 할 이벤트, 아이템, 상태, 팩, 시나리오, Ontology-lite 체크리스트다.
- `docs/05_validation/09_Content_Expansion_Review_Checklist_v0.1.md`
  - Content Expansion 구현 후 새 이벤트, 아이템, status/result_rules, pack/scenario, ontology relation, validator/simulator/analyzer 통과 여부를 검수한다.
- `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`
  - Quest, Day/Turn, 3-Card UI, Multi-Select, 경제/점수/평판/후속 사건 연결 검증 체크리스트다.
- `docs/05_validation/16_Gameplay_Replan_Acceptance_Gate_v0.1.md`
  - Gameplay Replan 구현 또는 콘텐츠 확장 작업을 완료로 판단하기 위한 최소 승인 기준이다.

---

# 8. 06_plans

역할:

- 향후 계획 문서 보관
- 구현 계획 문서 보관
- Console Validation 이후 실게임형 텍스트 모험 구조 전환 계획 보관

문서:

- `docs/06_plans/00_Console_Simulator_Implementation_Plan_v0.1.md`
  - 완료된 Console Simulator 구현 계획이다.
- `docs/06_plans/01_Content_Expansion_Implementation_Plan_v0.1.md`
  - Console Simulator PASS 이후 콘텐츠 확장을 구현할 때 따라야 할 이벤트, 아이템, 상태, pack, scenario, Ontology-lite 검증 계획이다.
- `docs/06_plans/02_Content_Expansion_Phase3_Sampling_Plan_v0.1.md`
  - TRPG 리서치와 콘텐츠 샘플링 가이드를 기준으로 Phase 3 이벤트, 아이템, entity 표본 추출 계획을 정의한다.
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
  - 현재 Console Validation 중심 구조에서 실게임형 텍스트 모험 시뮬레이터로 전환하기 위한 단계별 계획이다.
- `docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md`
  - Content Volume Audit 결과를 바탕으로 Quest, Expedition Clock, 3-Card Choice, Multi-Select, Score, Quest Report를 도입하기 위한 P0 구현 계획이다.
- `docs/06_plans/05_Quest_Expansion_Roadmap_v0.1.md`
  - Gameplay P0 이후 Quest 추가 순서와 첫 추가 Quest 설계 방향을 정리한 계획 문서다.
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
  - Quest Design Guide와 Quest Base Research Collection에 나열된 Quest 후보를 Type별로 분류하고, 다음 Batch 구성 기준을 정리한 계획 문서다.
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
  - Quest Type Catalog 기반 Category Probe, Stability Review, Bulk Fill의 실행 순서와 게이트를 잠근 ULW Loop 계획 문서다.

---

# 9. 07_reviews

역할:

- Office Hour, Brainstorming, Commit Summary 등 리뷰성 문서
- 구현 전후 판단 근거 보관
- 완료된 구현 검수 결과 보관
- 콘텐츠 볼륨, 카드 후보, Quest, Storylet, Economy/Score 연결 감사 결과 보관

문서:

- `docs/07_reviews/09_Commit_Summary_v0.1.md`
  - Console Validation 패키지 기준선 커밋 내용을 요약한다.
- `docs/07_reviews/10_Console_Simulator_Review_Result_v0.1.md`
  - Console Simulator 구현 후 검수 PASS와 최종 재리뷰 승인 결과를 보관한다.
- `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
  - Weighted AutoPlayer Scoring과 Content Expansion slice의 실제 플레이 감각, profile 차이, 선택/로그 품질 리뷰 결과를 보관한다.
- `docs/07_reviews/12_TRPG_Content_Research_Notes_v0.1.md`
  - CoC, D&D, 공개 TRPG 설계 자료를 FateWeaver용 추상 콘텐츠 샘플링 원칙으로 변환한 리서치 노트를 보관한다.
- `docs/07_reviews/13_Entity_Sampling_Review_v0.1.md`
  - Entity Sampling Review와 Ontology-lite v0.2 trial extension 판단 결과를 보관한다.
- `docs/07_reviews/14_Content_Volume_Audit_Template_v0.1.md`
  - 현재 이벤트, 선택지, 아이템, 단서, 징조, 퀘스트, 엔딩 볼륨을 감사하기 위한 리뷰 템플릿이다.
- `docs/07_reviews/15_Content_Volume_Audit_Result_v0.1.md`
  - Gameplay Replan 구현 전 현재 콘텐츠 볼륨과 구조 부족분을 감사한 결과 문서다.
- `docs/07_reviews/16_Gameplay_P0_Foundation_Implementation_Result_v0.1.md`
  - Gameplay Replan P0 Foundation 최소 수직 슬라이스 구현 결과와 검증 결과를 보관한다.
- `docs/07_reviews/17_Gameplay_P0_Outcome_Coverage_Result_v0.1.md`
  - Gameplay P0 Foundation의 success, partial_success, failure outcome coverage 보강 결과를 보관한다.
- `docs/07_reviews/18_Gameplay_P0_Result_Reason_Coverage_Result_v0.1.md`
  - Gameplay P0 Foundation의 partial_success / failure reason 구조화와 JSON/Text MUD 로그 검증 결과를 보관한다.
- `docs/07_reviews/19_Gameplay_P0_Objective_Schema_Normalization_Result_v0.1.md`
  - Gameplay P0의 Quest Objective Schema 정규화 결과를 보관한다.
- `docs/07_reviews/20_Gameplay_P0_Objective_Schema_Doc_And_Fixture_Result_v0.1.md`
  - Gameplay P0 Objective Schema 문서 정렬과 optional_action / max_day_exceeded fixture 검증 결과를 보관한다.
- `docs/07_reviews/21_Gameplay_P0_Optional_Action_And_Score_Rule_Result_v0.1.md`
  - Gameplay P0의 optional_action completed 경로와 score rule 정렬 결과를 보관한다.
- `docs/07_reviews/22_Gameplay_P0_Optional_Action_Ontology_Link_Result_v0.1.md`
  - Gameplay P0 optional_action 카드를 Storylet/Ontology 후보군과 연결한 결과를 보관한다.
- `docs/07_reviews/23_Gameplay_P0_Card_Candidate_Tier_Weight_Result_v0.1.md`
  - Gameplay P0 Card Candidate Pool에 tier / weight 기반 후보 선택 구조를 도입한 결과를 보관한다.
- `docs/07_reviews/24_Gameplay_P0_Seeded_Tier_Variety_Result_v0.1.md`
  - Gameplay P0 Card Candidate Pool에 seed 기반 tier variety를 도입한 결과를 보관한다.
- `docs/07_reviews/25_Quest_Base_Research_Collection_v0.1.md`
  - 판타지 TRPG 시나리오, 모험 Hook, Adventure Seed를 FateWeaver Quest 제작 양식으로 재가공한 리서치 자료다.
- `docs/07_reviews/26_Gameplay_P0_Storylet_Hints_Repeat_Cooldown_Result_v0.1.md`
  - Gameplay P0에 Storylet/Event card candidate hints와 repeat cooldown memory를 도입한 결과를 보관한다.
- `docs/07_reviews/27_Forest_Path_Scouting_Quest_Result_v0.1.md`
  - `forest_path_scouting_tutorial` Quest를 실제 data fixture로 추가하고 success / partial_success / failure 시나리오를 검증한 결과를 보관한다.
- `docs/07_reviews/28_Missing_Porter_Search_Quest_Result_v0.1.md`
  - `missing_porter_search_intro` Quest를 실제 data fixture로 추가하고 rescue / time pressure / partial_success 경로를 검증한 결과를 보관한다.
- `docs/07_reviews/29_Merchant_Lost_Pack_Quest_Result_v0.1.md`
  - `merchant_lost_pack_recovery` Quest를 실제 data fixture로 추가하고 economy / reputation / recovery / negotiation 경로를 검증한 결과를 보관한다.
- `docs/07_reviews/30_Failure_Outcome_Taxonomy_Result_v0.1.md`
  - Gameplay P0의 failure 의미를 정리하고 merchant failure fixture를 생존 실패와 Quest 고유 실패로 분리한 결과를 보관한다.
- `docs/07_reviews/31_Text_MUD_Log_Section_Refactor_Result_v0.1.md`
  - `text_mud_log.py`의 출력 섹션을 분리하고 LOC warning band를 해소한 결과를 보관한다.
- `docs/07_reviews/32_Quest_Category_Probe_Result_v0.1.md`
  - Quest Category별 대표 Probe 구현 결과와 success / partial_success / failure, 로그, storylet hint 회귀 검증을 보관한다.
- `docs/07_reviews/33_Quest_Category_Stability_Review_v0.1.md`
  - Category Probe 결과를 바탕으로 Bulk Fill 가능 여부와 Stable 판정을 보관한다.
- `docs/07_reviews/34_Quest_Category_Bulk_Fill_Result_v0.1.md`
  - Stable 판정된 Quest Category의 나머지 Quest를 lightweight success fixture 중심으로 Bulk Fill한 결과를 보관한다.
- `docs/07_reviews/35_Quest_Expansion_Coverage_Audit_v0.1.md`
  - Phase 3 Bulk Fill 이후 Quest / Scenario / Card Rule / Event Hint / Type Coverage를 수치화한 감사 결과를 보관한다.
- `docs/07_reviews/36_Quest_Expansion_Refactor_Gate_v0.1.md`
  - Phase 3 Bulk Fill과 Phase 4 Coverage Audit 이후, Bulk Fill 2차 전에 데이터/룰/이벤트/시나리오/코드 분리 필요성을 판정한 결과를 보관한다.
- `docs/07_reviews/37_Data_Split_Loader_Support_Result_v0.1.md`
  - Bulk Fill 2차 전에 card_rules split 구조와 split-aware loader 지원을 도입한 결과를 보관한다.
---

# 10. 신규 게임 구조 재정의 문서 적용 원칙

- 기존 Console Validation 문서는 과거 기준선으로 유지한다.
- 신규 문서는 v0.1로 추가한다.
- 기존 문서를 즉시 덮어쓰기보다 신규 문서 기준으로 후속 정렬 작업을 수행한다.
- 새 문서는 “실게임형 텍스트 모험 시뮬레이터” 목표를 정의하는 상위 재정렬 문서로 사용한다.
- FateWeaver의 중심은 저주가 아니라 Quest, Expedition, 3-Card Choice, 선택 합성, 경제/평판/점수, 후속 사건 변화다.
- 저주는 여러 상태/위험 요소 중 하나로만 다룬다.
