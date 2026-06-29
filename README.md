# Project FateWeaver

## 목적

Project FateWeaver는 **이벤트 중심 판타지 로그라이크**를 만들기 위한 프로젝트다.

현재 단계의 목표는 Flutter/Flame 앱 제작이 아니라, **Console Validation**을 통해 핵심 루프가 재미있는지 확인하는 것이다.

```text
현재 단계: Console Validation 준비 완료
현재 상태: READY_FOR_WRITING_PLANS
다음 단계: SUPERPOWERS - Writing-plans
```

---

# 1. 현재 개발 기준

## 지금 하는 것

```text
Python 콘솔 기반으로 이벤트-선택-상태 변화 루프 검증
YAML 데이터 계약 검증
scenario 기반 테스트 범위 검증
로그/재미 지표 설계
Writing-plans 작성 준비
```

## 아직 하지 않는 것

```text
Flutter 앱 제작
Flame 연출 구현
Dart 코드 작성
PRD 작성
World Bible 작성
실시간 전투 시스템 구현
```

---

# 2. 프로젝트 구조

```text
project_fate_weaver/
  docs/                  # 설계/검증/계획/리뷰 문서
  data/                  # YAML 원천 데이터
  src/                   # Python Console Validation 검증 엔진 영역
  tools/                 # Python 실행 도구 영역
  logs/                  # 콘솔 검증 로그
  archive/               # 이전 문서/폐기 문서 보관

  .python-version        # Python 버전 기준
  requirements.txt       # Python 의존성
  AGENTS.md              # 에이전트 작업 규칙
```

중요:

```text
docs/는 프로젝트 기준 문서 폴더다.
data/는 YAML Single Source of Truth다.
src/는 Flutter 소스가 아니라 Python 검증 엔진 영역이다.
tools/는 Python 실행 스크립트 영역이다.
fate_weaver/는 Console Validation 통과 후 생성할 Flutter + Flame 앱 프로젝트이며, 현재는 만들지 않는다.
```

---

# 3. docs 구조

```text
docs/
  00_index/
    README_Docs_Index.md

  01_foundation/
    00_Project_FateWeaver_Current_Baseline_v0.7.md
    01_Project_Structure_Guide_v0.1.md
    02_Data_Architecture_v0.7.md

  02_schema/
    03_Event_Grammar_Draft_YAML_Schema_v0.7.md
    06_Fixture_Data_Plan_v0.3.md
    08_Flutter_Data_Export_Contract_v0.1.md

  03_specs/
    04_Console_Simulator_Spec_v0.7.md

  04_codex/
    05_Codex_Console_Prototype_Brief_v0.6.md

  05_validation/
    07_Console_Validation_Checklist_v0.1.md

  06_plans/
    .gitkeep

  07_reviews/
    09_Commit_Summary_v0.1.md

  archive/
    .gitkeep
```

문서 탐색은 먼저 아래 파일을 본다.

```text
docs/00_index/README_Docs_Index.md
```

---

# 4. data 구조

```text
data/
  core/
    statuses.yaml
    tags.yaml
    choice_types.yaml
    item_roles.yaml
    result_rules.yaml

  content/
    base/
      regions.yaml
      items.yaml
      events.yaml
      endings.yaml

    packs/
      forest_pack/events.yaml
      curse_pack/events.yaml

  scenarios/
    mvp0_console_test.yaml
    curse_balance_test.yaml
    item_influence_test.yaml
```

원칙:

```text
YAML은 원천 데이터다.
테스트 범위는 data/scenarios/*.yaml로 관리한다.
data/mvp0/ 폴더는 만들지 않는다.
```

---

# 5. Python 실행 환경

Console Validation 제작과 검증은 프로젝트 루트의 `.venv`를 사용한다.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

실행 명령도 전역 `python`이 아니라 `.venv/bin/python`을 사용한다.

---

# 6. Console Validation 핵심 계약

## Scenario filter

```text
include_event_ids: optional
include_event_tags: optional
exclude_event_ids: optional
exclude_event_tags: optional

include_event_ids와 include_event_tags가 둘 다 없으면:
content_sources + include_regions 기준 전체 이벤트를 사용한다.

include_event_ids와 include_event_tags가 둘 다 있으면:
AND 조건으로 필터링한다.
```

## Choice-level requires

```text
choice-level requires_*는 해당 choice의 available 여부를 판단한다.
event-level requires_*는 이벤트 자체의 eligible 여부를 판단한다.
Console Validation에서 대부분의 조건은 choice-level로 둔다.
```

## Unavailable choice

Console Validation 기본 정책은 **show unavailable**이다.

```text
unavailable choice는 표시한다.
단, 선택은 불가능하다.
표시 이유를 함께 보여준다.
```

## 로그와 재미 검증

```text
regret_score = choice-level, int 1-5, player
player_woven_score = run-level, int 1-5, player
```

Analyzer는 최소 아래 지표를 summary에 포함한다.

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
restart_intent_score
run_failed_but_interesting
player_woven_score
```

## Combat policy

```text
combat은 event_tags: [combat]을 가진 일반 이벤트다.
combat_response는 choice_type 중 하나일 뿐이다.
Console Validation에서 CombatEventResolver는 만들지 않는다.
모든 전투형 이벤트는 일반 ChoiceResolver로 처리한다.
```

---

# 7. 현재 금지 사항

```text
fate_weaver/ 생성 금지
Flutter 프로젝트 생성 금지
Flame 코드 작성 금지
Dart 코드 작성 금지
data/mvp0/ 생성 금지
PRD 작성 금지
World Bible 작성 금지
이벤트별 if문 하드코딩 금지
```

---

# 8. 다음 단계

현재 상태는 다음 단계로 넘어갈 수 있다.

```text
READY_FOR_WRITING_PLANS
```

다음 작업:

```text
SUPERPOWERS - Writing-plans
```

Writing-plans 결과물은 아래 폴더에 둔다.

```text
docs/06_plans/
```

예상 산출물:

```text
docs/06_plans/00_Console_Validation_Implementation_Plan_v0.1.md
docs/06_plans/01_Worktree_Strategy_v0.1.md
docs/06_plans/02_SubAgent_Task_Split_v0.1.md
docs/06_plans/03_Review_Agent_Checklist_v0.1.md
```

---

# 9. 권장 진행 순서

```text
1. SUPERPOWERS - Writing-plans
2. 리뷰 에이전트 이중 검증
3. Git worktree 생성
4. Sub-Agent dev로 구현 범위 분리
5. Codex 구현
6. 디자인 리뷰 / AI 슬롭 제거
7. Console Validation 로그 분석
```

---

# 10. 루트 README 역할

이 README는 프로젝트 전체의 진입점이다.

상세 문서의 역할:

```text
기준 문서: docs/01_foundation/
데이터 계약: docs/02_schema/
구현 사양: docs/03_specs/
Codex 지시: docs/04_codex/
검증 기준: docs/05_validation/
구현 계획: docs/06_plans/
리뷰 기록: docs/07_reviews/
```
