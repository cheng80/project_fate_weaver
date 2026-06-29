# Project FateWeaver Docs Index

## 문서 목적

이 문서는 `docs/` 폴더의 역할별 구조와 현재 문서 목록을 정리한다.

현재 단계는 PRD 작성 전이며, 목표는 MVP-0 콘솔 검증 프로토타입 제작 전 문서 계약을 명확히 하는 것이다.

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
  archive/
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
  - 현재 단계가 MVP-0 Console Loop Validation임을 고정한다.
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

문서:

- `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
  - scenario filter, choice-level requires, unavailable choice, metric, combat policy 계약을 정의한다.
- `docs/02_schema/06_Fixture_Data_Plan_v0.3.md`
  - MVP-0 fixture 데이터의 최소 기준을 정의한다.
- `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`
  - YAML에서 Flutter JSON artifact로 이전하는 계약을 정의한다.

---

# 5. 03_specs

역할:

- 실제 실행 사양
- 콘솔 시뮬레이터 동작 계약
- 로그 출력 계약

문서:

- `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`
  - MVP-0 콘솔 시뮬레이터의 로드, 선택, 로그, 분석, 금지 구현 범위를 정의한다.

---

# 6. 04_codex

역할:

- Codex 구현 지시 기준
- 허용/금지 작업 범위
- 구현 전후 응답 형식

문서:

- `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`
  - Codex가 MVP-0 콘솔 프로토타입을 만들 때 따라야 할 작업 브리프다.

---

# 7. 05_validation

역할:

- 착수 전 체크리스트
- 검증 게이트
- P0/P1 반영 확인

문서:

- `docs/05_validation/07_MVP0_Validation_Checklist_v0.1.md`
  - Writing-plans와 구현 착수 전에 확인해야 할 구조, 데이터, 계약 체크리스트다.

---

# 8. 06_plans

역할:

- 향후 Writing-plans 결과물 보관
- 구현 계획 문서 보관

현재 문서:

- 없음

---

# 9. 07_reviews

역할:

- Office Hour, Brainstorming, Commit Summary 등 리뷰성 문서
- 구현 전후 판단 근거 보관

문서:

- `docs/07_reviews/09_Commit_Summary_v0.1.md`
  - MVP-0 검증 패키지 기준선 커밋 내용을 요약한다.

---

# 10. archive

역할:

- docs 내부에서 폐기되거나 대체된 문서 보관
- 현재 기준 문서와 혼동되지 않도록 분리

현재 문서:

- 없음
