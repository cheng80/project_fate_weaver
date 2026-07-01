# Project FateWeaver Project Structure Guide v0.1

## 문서 목적

이 문서는 Project FateWeaver의 최상위 폴더 구조와 각 폴더의 책임을 정의한다.

앞으로 모든 답변, Codex 작업, 문서 작성, 데이터 추가는 이 구조를 기준으로 한다.

---

# 1. 최상위 구조

```text
project_fate_weaver/
  docs/
  data/
  src/
  tools/
  logs/

  fate_weaver/
```

---

# 2. docs/

## 역할

`docs/`는 프로젝트 기준 문서 폴더다.

이 폴더는 선택이 아니라 필수다.

## 포함 대상

```text
헌법 문서
검증 계획
데이터 아키텍처
이벤트 스키마
콘솔 시뮬레이터 사양
Codex 작업 브리프
Fixture 데이터 계획
Office Hour 결과
Brainstorm 결과
```

## 금지

```text
실제 YAML 콘텐츠 원본 저장 금지
Python 실행 코드 저장 금지
Flutter 코드 저장 금지
```

---

# 3. data/

## 역할

`data/`는 YAML 원천 데이터 폴더다.

## 구조

```text
data/
  core/
  content/
    base/
    packs/
  scenarios/
```

## 원칙

```text
YAML은 Single Source of Truth다.
테스트 데이터도 실제 콘텐츠 구조와 분리한다.
mvp0 폴더를 콘텐츠 저장소로 만들지 않는다.
```

---

# 4. src/

## 역할

`src/`는 Python Console Validation 검증 엔진이다.

Flutter 프로젝트의 소스 폴더가 아니다.

## 구조

```text
src/
  fateweaver/
    models.py
    data_loader.py
    event_selector.py
    choice_resolver.py
    state_manager.py
    inventory_manager.py
    validator.py
    logger.py
    analyzer.py
```

## 금지

```text
Flutter/Dart 코드 저장 금지
UI 코드 저장 금지
프로젝트 앱 소스 저장 금지
```

---

# 5. tools/

## 역할

`tools/`는 터미널에서 실행하는 Python 스크립트 폴더다.

## 예시

```text
validate_data.py
console_simulator.py
analyze_logs.py
export_json.py
```

`tools/`는 `src/fateweaver/`의 로직을 호출한다.

---

# 6. logs/

## 역할

Console Validation 결과를 저장한다.

```text
run_001.yaml
summary.yaml
summary.md
```

---

# 7. fate_weaver/

## 역할

이후 생성할 Flutter + Flame 앱 프로젝트다.

Console Validation 단계에서는 생성하지 않는다.

## 예상 구조

```text
fate_weaver/
  pubspec.yaml
  lib/
  assets/
    data/
  test/
```

---

# 8. 단계별 폴더 사용

## Console Validation

사용:

```text
docs/
data/
src/
tools/
logs/
```

사용 금지:

```text
fate_weaver/
```

## Flutter 앱 단계

사용:

```text
fate_weaver/
```

Flutter 앱 단계에서는 `tools/export_json.py`를 통해 YAML 원천 데이터를 Flutter assets로 변환한다.

---

# 9. 구조 변경 원칙

새 폴더나 구조 변경 제안은 반드시 아래 질문을 통과해야 한다.

```text
기존 역할을 침범하지 않는가?
장기 확장에 유리한가?
Codex가 오해하지 않는가?
Flutter 프로젝트와 충돌하지 않는가?
YAML Single Source of Truth 원칙을 깨지 않는가?
```
