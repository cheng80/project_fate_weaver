# Project FateWeaver Codex Console Prototype Brief v0.5

## 문서 목적

이 문서는 Codex에게 MVP-0 콘솔 프로토타입 제작을 지시하기 위한 작업 브리프다.

---

# 1. 작업 목표

Flutter 앱을 만들지 말고, PRD를 작성하지 말고, 콘솔 시뮬레이터만 만든다.

---

# 2. 반드시 읽을 문서

- `README.md`
- `docs/00_Project_FateWeaver_Current_Baseline_v0.7.md`
- `docs/01_Project_Structure_Guide_v0.1.md`
- `docs/02_Data_Architecture_v0.7.md`
- `docs/03_Event_Grammar_Draft_YAML_Schema_v0.6.md`
- `docs/04_Console_Simulator_Spec_v0.6.md`

---

# 3. 허용 작업 범위

Codex는 아래 경로만 생성/수정한다.

```text
docs/
data/core/
data/content/
data/scenarios/
src/fateweaver/
tools/
logs/
README.md
```

단, `docs/`는 문서 보강이 필요한 경우에만 수정한다.

---

# 4. 금지 작업

```text
data/mvp0/ 생성 금지
fate_weaver/ 생성 금지
Flutter 프로젝트 생성 금지
Flame 코드 작성 금지
Dart 앱 코드 작성 금지
UI 디자인 금지
PRD 작성 금지
World Bible 작성 금지
온디바이스 LLM 실험 금지
실시간 전투 시스템 구현 금지
이벤트별 if문 하드코딩 금지
```

---

# 5. 구현해야 할 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1
.venv/bin/python tools/analyze_logs.py --logs logs
```

---

# 6. 성공 조건

- scenario 기반 로드 가능
- content_sources 로드 가능
- validator 실행 가능
- console simulator 실행 가능
- run log 생성
- summary report 생성
- event selector가 seed 기반으로 동작
- choices_seen에 unavailable choice 기록
- influenced_by 기록 가능
- player_woven_score 기록 가능
- README에 실행법 포함

---

# 7. 작업 전 응답 형식

```text
STATUS: PLAN
작업 범위:
생성/수정 파일:
실행 명령:
금지한 작업:
```

---

# 8. 작업 후 응답 형식

```text
STATUS: DONE
생성/수정 파일:
검증 명령 결과:
남은 리스크:
다음 작업:
```


---

# 9. Python 의존성

Codex는 Python YAML 처리를 위해 `requirements.txt`를 사용한다.

설치 명령:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

임의로 다른 YAML 라이브러리를 추가하지 않는다.

---

# 10. 로그 점수 계약

Codex는 아래 기준을 따른다.

```text
regret_score = 선택 단위 로그
player_woven_score = Run 종료 회고
```

두 값을 같은 위치에 기록하지 않는다.

---

# 11. Flutter export는 구현하지 않음

MVP-0에서는 `tools/export_json.py`를 반드시 구현할 필요는 없다.

단, 구현한다면 `docs/08_Flutter_Data_Export_Contract_v0.1.md`를 따라야 한다.

Flutter 프로젝트 `fate_weaver/`는 생성하지 않는다.
