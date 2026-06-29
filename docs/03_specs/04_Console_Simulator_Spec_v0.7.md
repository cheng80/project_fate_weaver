# Project FateWeaver Console Simulator Spec v0.7

## 문서 목적

이 문서는 Console Validation을 실제로 실행하기 위한 콘솔 시뮬레이터 사양이다.

v0.7에서는 scenario filter, unavailable choice, 로그 metric, 재미 검증 지표, combat policy 계약을 명시한다.

---

# 1. 실행 목표

콘솔 시뮬레이터는 scenario를 입력으로 받는다.

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml
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

Codex는 Console Validation에서 아래 경로만 생성/수정한다.

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

문서 보강이 필요한 경우에만 `docs/`를 수정한다.

---

# 3. 금지 파일 범위

Console Validation에서는 아래를 생성하거나 수정하지 않는다.

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
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

## 단일 Run

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --run-id 001
```

## 여러 Run

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 5
```

## 로그 분석

```bash
.venv/bin/python tools/analyze_logs.py --logs logs
```

---

# 7. Scenario 로드 규칙

시뮬레이터는 다음 순서로 데이터를 로드한다.

```text
1. scenario yaml 로드
2. core yaml 로드
3. scenario.content_sources 로드
4. include_regions로 region 제한
5. include_event_ids/include_event_tags로 이벤트 제한
6. exclude_event_ids/exclude_event_tags로 이벤트 제거
7. initial_status 적용
8. initial_items 적용
9. target_turns 적용
```

Filter 규칙:

```text
include_event_ids: optional
include_event_tags: optional
exclude_event_ids: optional
exclude_event_tags: optional

include_event_ids와 include_event_tags가 둘 다 없으면 content_sources + include_regions 기준 전체 이벤트를 사용한다.
include_event_ids와 include_event_tags가 둘 다 있으면 AND 조건으로 필터링한다.
exclude_*는 include 필터 이후 적용한다.
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

# 10. Unavailable Choice Policy

Console Validation 기본 정책은 **show unavailable**이다.

```text
unavailable choice는 표시한다.
단, 선택은 불가능하다.
표시 이유를 함께 보여준다.
```

표시 예:

```text
[unavailable: requires holy_water]
```

로그 예:

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

`hidden_until_available: true`가 있는 choice는 숨길 수 있다. 단, Console Validation fixture 기본값은 false다.

---

# 11. Choice Requires Policy

```text
choice-level requires_*는 해당 choice의 available 여부만 판단한다.
event-level requires_*는 이벤트 자체의 eligible 여부를 판단한다.
Console Validation에서 대부분의 조건은 choice-level로 둔다.
```

지원 대상:

```yaml
requires_item: string
requires_any_item: list[string]
requires_status: StatusCondition
requires_tag: string
consume_item: bool
hidden_until_available: bool
```

---

# 12. 로그 Metric Contract

## choice-level

```yaml
choice_time_seconds:
  type: int
  source: system

choice_reason:
  type: string
  source: player
  required: true

expected_risk:
  type: string
  source: player
  required: true

influenced_by:
  type: list[string]
  source: player
  allowed_prefix: [item:, status:, unavailable:, event:, risk:]

regret_score:
  type: int
  scale: 1-5
  source: player
```

## run-level

```yaml
run_summary:
  fairness_score: 1-5
  restart_intent_score: 1-5
  player_woven_score: 1-5
  narrative_summary: string
  most_memorable_choice: string
  next_run_intent: string
```

---

# 13. Console Validation 재미 검증 지표

필수 분석 지표:

```text
meaningful_choice_count
item_unlocked_choice_count
bad_tradeoff_count
restart_intent_score
run_failed_but_interesting
player_woven_score
```

정의:

```text
meaningful_choice_count:
choice_reason에 상태/아이템/위험/미래 영향 중 하나 이상이 언급된 선택 수

item_unlocked_choice_count:
available=true라서 실제 선택에 영향을 준 item_based choice 수

bad_tradeoff_count:
플레이어가 손해를 알면서도 선택했다고 기록한 선택 수

run_failed_but_interesting:
Run 실패 후 restart_intent_score가 4 이상이면 true

player_woven_score:
이번 Run이 내가 선택으로 엮은 이야기처럼 느껴졌는지 1-5로 평가
```

---

# 14. Combat Policy

전투형 이벤트는 별도 전투 시스템이 아니다.

```text
combat은 event_tags: [combat]을 가진 일반 이벤트다.
combat_response는 choice_type 중 하나일 뿐이다.
Console Validation에서 CombatEventResolver는 만들지 않는다.
모든 전투형 이벤트는 일반 ChoiceResolver로 처리한다.
별도 전투 루프, 적 HP, 공격/방어 턴, 전투 UI는 금지한다.
```

---

# 15. 금지 구현

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
- CombatEventResolver
- 전투 전용 루프
- 적 HP/공격/방어 턴 시스템

---

# 16. Flutter 이전 계획

Console Validation 통과 후에만 아래를 진행한다.

```text
tools/export_json.py
↓
fate_weaver/assets/data/
↓
Flutter UI
↓
Flame 연출
```


---

# 17. 점수 필드 위치

## 12.1 선택 단위 필드

각 선택 로그에는 `regret_score`를 기록한다.

```yaml
regret_score: 4
```

`regret_score`는 해당 선택을 나중에 후회하거나 다시 생각해볼 여지가 있었는지를 측정한다.

---

## 12.2 Run 종료 필드

`player_woven_score`는 선택 단위가 아니라 Run 종료 회고에 기록한다.

```yaml
run_summary:
  fairness_score: 4
  restart_intent_score: 5
  player_woven_score: 4
  narrative_summary: "성수를 아끼다가 저주가 쌓여 실패한 런"
  most_memorable_choice: "저주받은 우물에서 성수를 아낀 선택"
  next_run_intent: "다음에는 성수를 초반에 쓰지 않고 저주 보상 루트를 실험해보고 싶다."
```

이 기준으로 `regret_score`와 `player_woven_score`를 혼동하지 않는다.

---

# 18. Python 실행 환경

Console Validation Python 실행은 프로젝트 루트의 `requirements.txt`를 사용한다.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

필수 의존성:

```text
PyYAML
```

표준 라이브러리만으로 YAML을 안정적으로 처리하지 않는다.
