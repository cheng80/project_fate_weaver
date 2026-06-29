# Project FateWeaver Codex Console Prototype Brief v0.6

## 문서 목적

이 문서는 Codex에게 Console Validation 프로토타입 제작을 지시하기 위한 작업 브리프다.

> 기준 구분: 이 문서는 과거 Console Validation 프로토타입 브리프다. Gameplay Replan 관련 새 작업은 `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`를 먼저 읽고 `docs/04_codex/14_Codex_Gameplay_Replan_Brief_v0.1.md`를 따른다.

---

# 1. 작업 목표

Flutter 앱을 만들지 말고, PRD를 작성하지 말고, 콘솔 시뮬레이터만 만든다.

---

# 2. 반드시 읽을 문서

- `README.md`
- `docs/01_foundation/00_Project_FateWeaver_Current_Baseline_v0.7.md`
- `docs/01_foundation/01_Project_Structure_Guide_v0.1.md`
- `docs/01_foundation/02_Data_Architecture_v0.7.md`
- `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`
- `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`

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
- meaningful_choice_count 기록 가능
- item_unlocked_choice_count 기록 가능
- bad_tradeoff_count 기록 가능
- restart_intent_score 기록 가능
- run_failed_but_interesting 기록 가능
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

# 11. Scenario Filter 계약

Codex는 아래 문법을 지원한다.

```text
include_event_ids: optional
include_event_tags: optional
exclude_event_ids: optional
exclude_event_tags: optional

include_event_ids와 include_event_tags가 둘 다 없으면 content_sources + include_regions 기준 전체 이벤트를 사용한다.
include_event_ids와 include_event_tags가 둘 다 있으면 AND 조건으로 필터링한다.
```

---

# 12. Choice Requires 계약

```text
choice-level requires_*는 choice available 여부를 판단한다.
event-level requires_*는 event eligible 여부를 판단한다.
Console Validation에서 대부분의 조건은 choice-level로 둔다.
```

지원 필드:

```text
requires_item
requires_any_item
requires_status
requires_tag
consume_item
hidden_until_available
```

---

# 13. Unavailable Choice 계약

Console Validation 기본 정책은 **show unavailable**이다.

```text
unavailable choice는 표시한다.
단, 선택은 불가능하다.
표시 이유를 함께 보여준다.
```

로그에는 최소 아래를 남긴다.

```yaml
choices_seen:
  - id: purify
    available: false
    hidden: false
    reason: requires_item:holy_water

unavailable_choice_count: 1
missing_items_noticed:
  - holy_water
```

---

# 14. 로그 Metric 계약

choice-level:

```text
choice_time_seconds: int, system
choice_reason: string, player, required
expected_risk: string, player, required
influenced_by: list[string], player, prefix item:/status:/unavailable:/event:/risk:
regret_score: int 1-5, player
```

run-level:

```text
fairness_score: int 1-5, player
restart_intent_score: int 1-5, player
player_woven_score: int 1-5, player
narrative_summary: string, player
most_memorable_choice: string, player
next_run_intent: string, player
```

---

# 15. Console Validation 재미 검증 지표

Analyzer는 아래 지표를 summary에 포함한다.

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
restart_intent_score
run_failed_but_interesting
player_woven_score
```

---

# 16. Combat policy

전투형 이벤트는 별도 전투 시스템이 아니다.

```text
combat은 event_tags: [combat]을 가진 일반 이벤트다.
combat_response는 choice_type 중 하나일 뿐이다.
Console Validation에서 CombatEventResolver는 만들지 않는다.
모든 전투형 이벤트는 일반 ChoiceResolver로 처리한다.
별도 전투 루프, 적 HP, 공격/방어 턴, 전투 UI는 금지한다.
```

---

# 17. Flutter export는 구현하지 않음

Console Validation에서는 `tools/export_json.py`를 반드시 구현할 필요는 없다.

단, 구현한다면 `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`를 따라야 한다.

Flutter 프로젝트 `fate_weaver/`는 생성하지 않는다.
