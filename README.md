# Project FateWeaver Pre-PRD Validation Pack v0.7

## 목적

이 패키지는 **PRD 작성 전 MVP-0 콘솔 검증**을 준비하기 위한 기준 문서, 데이터 구조, fixture 데이터, Codex 작업 기준을 포함한다.

현재 목표는 Flutter/Flame 앱 제작이 아니다.

현재 목표는:

```text
MVP-0 Console Loop Validation
```

이다.

---

# v0.7 핵심 변경

v0.7에서는 최상위 프로젝트 구조와 Codex 제작 전 검증 기준을 다시 맞췄다.

```text
project_fate_weaver/
  docs/                  # 설계/검증/기준 문서
  data/                  # YAML 원천 데이터
  src/                   # Python MVP-0 검증 엔진
  tools/                 # Python 실행 도구
  logs/                  # 콘솔 검증 로그
  archive/               # 이전 문서/폐기 문서 보관

  fate_weaver/           # 이후 생성할 Flutter + Flame 앱 프로젝트
```

중요:

```text
docs/는 선택 폴더가 아니라 최상위 필수 폴더다.
src/는 Flutter 소스가 아니라 Python 검증 엔진이다.
tools/는 Python 실행 스크립트다.
fate_weaver/는 MVP-0 통과 후 별도로 생성할 Flutter + Flame 앱 프로젝트다.
```

---

# 현재 패키지에 포함된 폴더

```text
docs/
data/
  core/
  content/
    base/
    packs/
  scenarios/
src/
  fateweaver/
tools/
logs/
archive/
```

`fate_weaver/` 폴더는 포함하지 않는다.  
MVP-0 검증 통과 후 MVP-1 단계에서 생성한다.

---

# docs/ 포함 문서

```text
docs/00_index/README_Docs_Index.md
docs/01_foundation/00_Project_FateWeaver_Current_Baseline_v0.7.md
docs/01_foundation/01_Project_Structure_Guide_v0.1.md
docs/01_foundation/02_Data_Architecture_v0.7.md
docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md
docs/02_schema/06_Fixture_Data_Plan_v0.3.md
docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md
docs/03_specs/04_Console_Simulator_Spec_v0.7.md
docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md
docs/05_validation/07_MVP0_Validation_Checklist_v0.1.md
docs/07_reviews/09_Commit_Summary_v0.1.md
```

---

# data/ 포함 데이터

```text
data/core/
  statuses.yaml
  tags.yaml
  choice_types.yaml
  item_roles.yaml
  result_rules.yaml

data/content/base/
  regions.yaml
  items.yaml
  events.yaml
  endings.yaml

data/content/packs/
  forest_pack/events.yaml
  curse_pack/events.yaml

data/scenarios/
  mvp0_console_test.yaml
  curse_balance_test.yaml
  item_influence_test.yaml
```

---

# Python 실행 환경

MVP-0 콘솔 제작과 검증은 프로젝트 루트의 `.venv`를 사용한다.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

실행 명령도 전역 `python`이 아니라 `.venv/bin/python`을 사용한다.

---

# MVP-0 계약 보강

Writing-plans 진입 전 아래 계약을 고정한다.

## Scenario filter

```text
include_event_ids: optional
include_event_tags: optional
exclude_event_ids: optional
exclude_event_tags: optional

include_event_ids와 include_event_tags가 둘 다 없으면 content_sources + include_regions 기준 전체 이벤트를 사용한다.
include_event_ids와 include_event_tags가 둘 다 있으면 AND 조건으로 필터링한다.
```

## Unavailable choice

MVP-0 기본 정책은 **show unavailable**이다.

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
MVP-0에서 CombatEventResolver는 만들지 않는다.
모든 전투형 이벤트는 일반 ChoiceResolver로 처리한다.
```

---

# 추천 Office Hour 질문

```text
$office-hour "첨부한 Project FateWeaver Pre-PRD Validation Pack v0.7 전체를 읽고, docs/data/src/tools/logs/archive/fate_weaver 역할 분리가 명확한지 비판적으로 검토해줘. 특히 docs가 최상위 기준 문서 폴더로 충분히 정리되어 있는지, data/core-content-scenarios 구조가 장기 업데이트에 적합한지, src/tools가 Python MVP-0 검증용으로 명확한지, 향후 fate_weaver Flutter 프로젝트로 확장할 때 구조 충돌이 없는지 평가하고 '바로 콘솔 제작 가능 / 소폭 보강 후 가능 / 아직 불가' 중 하나로 판정해줘."
```
