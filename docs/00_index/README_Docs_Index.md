# Project FateWeaver Docs Index

## 문서 목적

이 문서는 `docs/` 폴더의 역할별 구조와 현재 문서 목록을 정리한다.

현재 단계는 PRD 작성 전이며, Console Simulator 구현 검수 PASS 이후 콘텐츠 확장 준비와 Ontology-lite 유지 관리 기준을 명확히 하는 것이다.

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

---

# 3. 01_foundation

역할:

- 프로젝트 기준선
- 최상위 구조
- 데이터 아키텍처
- Flutter 이전 전제

문서:

- `docs/01_foundation/00_Project_FateWeaver_Current_Baseline_v0.7.md`
  - 현재 단계가 Console Validation임을 고정한다.
- `docs/01_foundation/01_Project_Structure_Guide_v0.1.md`
  - `docs/`, `data/`, `src/`, `tools/`, `logs/`, `archive/`, 향후 `fate_weaver/`의 역할을 정의한다.
- `docs/01_foundation/02_Data_Architecture_v0.7.md`
  - `data/core`, `data/content`, `data/scenarios` 구조와 장기 데이터 원칙을 정의한다.

---

# 4. 02_schema

역할:

- YAML 원천 데이터 계약
- fixture 데이터 기준
- Flutter export 계약
- 콘텐츠 관계 분석을 위한 Ontology-lite 계약

문서:

- `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
  - scenario filter, choice-level requires, unavailable choice, metric, combat policy 계약을 정의한다.
- `docs/02_schema/06_Fixture_Data_Plan_v0.3.md`
  - Console Validation fixture 데이터의 최소 기준을 정의한다.
- `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`
  - YAML에서 Flutter JSON artifact로 이전하는 계약을 정의한다.
- `docs/02_schema/09_Content_Ontology_Model_v0.1.md`
  - `data/core/ontology.yaml` 기반의 최소 콘텐츠 관계 모델을 정의한다.

---

# 5. 03_specs

역할:

- 실제 실행 사양
- 콘솔 시뮬레이터 동작 계약
- 로그 출력 계약

문서:

- `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`
  - Console Validation 시뮬레이터의 로드, 선택, 로그, 분석, 금지 구현 범위를 정의한다.

---

# 6. 04_codex

역할:

- Codex 구현 지시 기준
- 허용/금지 작업 범위
- 구현 전후 응답 형식

문서:

- `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`
  - Codex가 Console Validation 프로토타입을 만들 때 따라야 할 작업 브리프다.

---

# 7. 05_validation

역할:

- 착수 전/확장 전 체크리스트
- 검증 게이트
- P0/P1 반영 확인
- 콘텐츠 확장 readiness 기준

문서:

- `docs/05_validation/07_Console_Validation_Checklist_v0.1.md`
  - Writing-plans와 구현 착수 전에 확인해야 할 구조, 데이터, 계약 체크리스트다.
- `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`
  - Console Simulator PASS 이후 콘텐츠 확장 전에 확인해야 할 이벤트, 아이템, 상태, 팩, 시나리오, Ontology-lite 체크리스트다.
- `docs/05_validation/09_Content_Expansion_Review_Checklist_v0.1.md`
  - Content Expansion 구현 후 새 이벤트, 아이템, status/result_rules, pack/scenario, ontology relation, validator/simulator/analyzer 통과 여부를 검수한다.

---

# 8. 06_plans

역할:

- 향후 계획 문서 보관
- 구현 계획 문서 보관

현재 문서:

- `docs/06_plans/00_Console_Simulator_Implementation_Plan_v0.1.md`
  - 완료된 Console Simulator 구현 계획이다.
- `docs/06_plans/01_Content_Expansion_Implementation_Plan_v0.1.md`
  - Console Simulator PASS 이후 콘텐츠 확장을 구현할 때 따라야 할 이벤트, 아이템, 상태, pack, scenario, Ontology-lite 검증 계획이다.

---

# 9. 07_reviews

역할:

- Office Hour, Brainstorming, Commit Summary 등 리뷰성 문서
- 구현 전후 판단 근거 보관
- 완료된 구현 검수 결과 보관

문서:

- `docs/07_reviews/09_Commit_Summary_v0.1.md`
  - Console Validation 패키지 기준선 커밋 내용을 요약한다.
- `docs/07_reviews/10_Console_Simulator_Review_Result_v0.1.md`
  - Console Simulator 구현 후 검수 PASS와 최종 재리뷰 승인 결과를 보관한다.
- `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`
  - Weighted AutoPlayer Scoring과 Content Expansion slice의 실제 플레이 감각, profile 차이, 선택/로그 품질 리뷰 결과를 보관한다.
