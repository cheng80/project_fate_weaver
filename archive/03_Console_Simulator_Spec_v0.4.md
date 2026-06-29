# Project FateWeaver Console Simulator Spec v0.4

## 문서 목적

이 문서는 MVP-0 Console Loop Validation을 실제로 실행하기 위한 콘솔 시뮬레이터 사양이다.

v0.4에서는 `src/`, `tools/`, `fate_weaver/`의 역할 분리를 명확히 한다.

---

# 1. 실행 목표

콘솔 시뮬레이터는 scenario를 입력으로 받는다.

```bash
python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml
```

목표:

```text
scenario 로드
core/content 로드
이벤트 선택
선택지 표시
선택 입력
결과 적용
로그 저장
분석 리포트 생성
```

---

# 2. 허용 파일 범위

Codex는 MVP-0에서 아래 경로만 생성/수정한다.

```text
data/core/
data/content/
data/scenarios/
src/fateweaver/
tools/
logs/
README.md
```

---

# 3. 금지 파일 범위

MVP-0에서는 아래를 생성하거나 수정하지 않는다.

```text
fate_weaver/
lib/
android/
ios/
pubspec.yaml
Flutter 프로젝트
Flame 코드
data/mvp0/
```

---

# 4. src/ 역할

`src/fateweaver/`는 Python 도메인 로직 패키지다.

예상 모듈:

```text
src/fateweaver/
  __init__.py
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

---

# 5. tools/ 역할

`tools/`는 실행 스크립트 폴더다.

```text
tools/
  validate_data.py
  console_simulator.py
  analyze_logs.py
  export_json.py
```

각 스크립트는 `src/fateweaver/`의 코드를 호출한다.

---

# 6. 실행 명령

## 데이터 검증

```bash
python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

## 단일 Run

```bash
python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --run-id 001
```

## 여러 Run

```bash
python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 5
```

## 로그 분석

```bash
python tools/analyze_logs.py --logs logs
```

---

# 7. Scenario 로드 규칙

시뮬레이터는 다음 순서로 데이터를 로드한다.

```text
1. scenario yaml 로드
2. core yaml 로드
3. scenario.content_sources 로드
4. include_event_ids로 이벤트 제한
5. include_regions로 region 제한
6. initial_status 적용
7. initial_items 적용
8. target_turns 적용
```

---

# 8. Output Contract

각 Run은 다음 파일을 생성한다.

```text
logs/run_001.yaml
```

분석은 다음 파일을 생성한다.

```text
logs/summary.yaml
logs/summary.md
```

---

# 9. 로그 필드

각 선택 로그는 최소 아래 필드를 포함한다.

```yaml
run_id:
turn:
scenario_id:
event_id:
repeat_count:
state_before:
inventory_before:
choices_seen:
selected_choice:
choice_time_seconds:
choice_reason:
expected_risk:
influenced_by:
was_available:
was_hidden:
result:
state_after:
regret_score:
notes:
```

---

# 10. 금지 구현

- Flutter 앱
- Flame 연출
- GUI
- 저장/로드 시스템
- 광고/상점
- 온디바이스 LLM
- 실시간 전투
- 이벤트별 하드코딩 분기
- data/mvp0 폴더 생성
- fate_weaver 폴더 생성

---

# 11. Flutter 이전 계획

MVP-0 통과 후에만 아래를 진행한다.

```text
tools/export_json.py
↓
fate_weaver/assets/data/
↓
Flutter UI
↓
Flame 연출
```
