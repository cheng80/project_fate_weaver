# Project FateWeaver Current Baseline v0.5

## 문서 목적

이 문서는 Project FateWeaver의 현재 기준선을 정리한다.

v0.5의 핵심 변경점은 `src/`, `tools/`, `fate_weaver/`의 역할을 명확히 분리한 것이다.

---

# 1. 최종 정체성

Project FateWeaver의 장르는 다음으로 유지한다.

> **이벤트 중심 판타지 로그라이크**

자동 완성형 시스템은 장르가 아니라 **콘텐츠 제작/확장 파이프라인**이다.

---

# 2. 현재 개발 단계

현재는 PRD 단계가 아니다.

현재는 Flutter 앱 제작 단계도 아니다.

현재 목표는:

```text
MVP-0 Console Loop Validation
```

이다.

즉, Python 콘솔 환경에서 이벤트-선택-상태 변화 루프가 재미있는지 검증한다.

---

# 3. 폴더 역할

## 3.1 docs/

설계 문서, 검증 문서, 스키마 문서, Codex 작업 기준 문서를 저장한다.

```text
docs/
  00_Project_FateWeaver_Current_Baseline_v0.5.md
  01_Data_Architecture_v0.5.md
  02_Event_Grammar_Draft_YAML_Schema_v0.4.md
  03_Console_Simulator_Spec_v0.4.md
  04_Codex_Console_Prototype_Brief_v0.3.md
  05_Fixture_Data_Plan_v0.2.md
```

---

## 3.2 data/

YAML 원천 데이터다.

```text
data/
  core/
  content/
    base/
    packs/
  scenarios/
```

- `core/`: 상태, 태그, 선택지 타입, 아이템 역할 등 전역 규칙
- `content/base/`: 실제 게임 기본 콘텐츠
- `content/packs/`: 확장 콘텐츠팩
- `scenarios/`: 테스트/밸런스 검증 시나리오

---

## 3.3 src/

`src/`는 Flutter 소스 폴더가 아니다.

`src/`는 MVP-0 콘솔 검증을 위한 **Python 도메인 로직 패키지**다.

```text
src/
  fateweaver/
    models.py
    event_engine.py
    event_selector.py
    choice_resolver.py
    state_manager.py
    inventory_manager.py
    validator.py
    logger.py
    analyzer.py
```

역할:

- YAML 데이터 로드
- 이벤트 후보 필터링
- 이벤트 선택
- 선택지 처리
- 상태 변화 계산
- 로그 데이터 구성
- 분석 지표 계산

---

## 3.4 tools/

`tools/`는 사람이 터미널에서 실행하는 Python 스크립트 폴더다.

```text
tools/
  validate_data.py
  console_simulator.py
  analyze_logs.py
  export_json.py
```

역할:

- 데이터 검증 실행
- 콘솔 시뮬레이터 실행
- 로그 분석 실행
- 향후 Flutter용 JSON export

---

## 3.5 logs/

MVP-0 콘솔 테스트 결과를 저장한다.

```text
logs/
  run_001.yaml
  summary.yaml
  summary.md
```

---

## 3.6 archive/

이전 문서와 폐기된 초안을 보관한다.

---

## 3.7 fate_weaver/

`fate_weaver/`는 이후 생성할 Flutter + Flame 앱 프로젝트 폴더다.

MVP-0 단계에서는 생성하지 않는다.

MVP-0 검증 통과 후 MVP-1 단계에서 생성한다.

예상 구조:

```text
fate_weaver/
  pubspec.yaml
  lib/
  assets/
    data/
  test/
```

---

# 4. 실행 흐름

현재 단계에서는 다음 흐름만 구현한다.

```text
data/core + data/content + data/scenarios
↓
Python src/fateweaver 도메인 로직
↓
tools/console_simulator.py
↓
logs/run_001.yaml
↓
tools/analyze_logs.py
↓
logs/summary.md
```

Flutter는 아직 개입하지 않는다.

---

# 5. 향후 Flutter 이전 흐름

MVP-0 검증 통과 후:

```text
YAML 원천 데이터
↓
tools/export_json.py
↓
fate_weaver/assets/data/*.json
↓
Flutter UI
↓
Flame 연출
```

---

# 6. 금지 사항

MVP-0 단계에서 금지한다.

```text
Flutter 프로젝트 생성
Flame 컴포넌트 구현
fate_weaver/ 폴더 생성
Dart 앱 코드 작성
이벤트별 if문 하드코딩
data/mvp0/ 폴더 생성
```

---

# 7. 현재 목표

현재 목표는 Codex가 아래를 만들 수 있는 상태로 문서를 정리하는 것이다.

```text
Python 콘솔 시뮬레이터
YAML validator
Event selector
Choice resolver
Run logger
Log analyzer
```

한 줄 요약:

> **지금은 게임 앱을 만드는 단계가 아니라, 게임 루프가 재미있는지 검증하는 Python 실험 엔진을 만드는 단계다.**
