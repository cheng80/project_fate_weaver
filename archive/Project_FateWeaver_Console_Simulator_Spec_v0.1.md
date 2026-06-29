# Project FateWeaver Console Simulator Spec v0.1

## 문서 목적

이 문서는 MVP-0 Console Loop Validation을 실제로 실행하기 위한 콘솔 시뮬레이터 사양이다.

목표는 게임을 예쁘게 만드는 것이 아니라, **이벤트-선택-상태 변화 루프의 재미와 문제점을 로그로 검증하는 것**이다.

---

# 1. 실행 목표

콘솔 시뮬레이터는 다음을 수행해야 한다.

```text
Run 시작
초기 상태 표시
초기 아이템 표시
이벤트 표시
선택지 표시
플레이어 선택 입력
결과 적용
상태 변화 출력
로그 저장
다음 이벤트 진행
Run 종료
회고 입력
```

---

# 2. 구현 기준

## 2.1 기술

- Python 우선
- 표준 라이브러리 우선
- YAML 사용 시 `pyyaml` 허용
- 외부 UI 라이브러리 사용 금지
- macOS 터미널 기준

---

## 2.2 실행 명령 예시

```bash
python tools/console_simulator.py --seed 42 --runs 1
```

또는:

```bash
python tools/console_simulator.py --data data/mvp0 --log logs/run_001.yaml
```

---

# 3. 최소 폴더 구조

```text
project_fate_weaver/
  data/
    mvp0/
      events.yaml
      items.yaml
      statuses.yaml
      tags.yaml
  tools/
    console_simulator.py
    validate_data.py
  logs/
    run_001.yaml
```

---

# 4. 화면 출력 형식

## 4.1 Run 시작

```text
=== Project FateWeaver MVP-0 Console Test ===

Run ID: 001
Seed: 42

Status:
Health: 7/10
Food: 5/10
Money: 2
Reputation: 0
Curse: 1/5

Inventory:
- Rope
- Torch
```

---

## 4.2 이벤트 표시

```text
[Turn 04] 저주받은 우물

검은 물이 고인 우물에서 낮은 속삭임이 들린다.

Tags: exploration, well, curse

Choices:
1. 그냥 지나간다                 [safe / risk:none]
2. 물을 마신다                   [gamble / risk:high]
3. 성수로 정화한다               [item_based / unavailable: requires holy_water]
4. 밧줄로 내려간다               [item_based / risk:medium]
```

Unavailable choice는 기본적으로 표시하되 선택 불가로 둔다.

이유:

```text
아이템이 있었다면 다른 선택지가 열렸다는 감각을 주기 위함
```

---

## 4.3 선택 입력

```text
Select choice: 2
Why did you choose this? > 체력이 낮아서 위험하지만 회복을 노렸다.
Expected risk? > 저주가 오를 수 있다.
```

선택 이유 입력은 MVP-0에서 필수다.

---

## 4.4 결과 표시

```text
Result:
Health +1
Curse +1

Message:
물은 차갑고 달콤했지만, 뒤늦게 손끝이 검게 물들었다.

Status:
Health: 8/10
Food: 5/10
Money: 2
Reputation: 0
Curse: 2/5
```

---

# 5. 로그 저장

각 선택은 YAML 로그로 저장한다.

```yaml
run_id: 1
turn: 4
event_id: cursed_well
state_before:
  health: 7
  food: 5
  money: 2
  reputation: 0
  curse: 1
inventory_before:
  - rope
  - torch
choices_seen:
  - id: pass
    available: true
  - id: drink
    available: true
  - id: purify
    available: false
    reason: requires holy_water
  - id: climb_down
    available: true
selected_choice: drink
choice_time_seconds: 11
choice_reason: "체력이 낮아서 위험하지만 회복을 노렸다."
expected_risk: "저주가 오를 수 있다."
result:
  status:
    health: +1
    curse: +1
state_after:
  health: 8
  food: 5
  money: 2
  reputation: 0
  curse: 2
regret_score: 4
notes: "성수가 없어서 아쉬웠다."
```

---

# 6. Run 종료 조건

MVP-0 종료 조건은 단순하게 둔다.

```text
health <= 0
curse >= 5
turn >= target_turns
ending triggered
```

기본 target_turns:

```text
20
```

---

# 7. Run 종료 회고

Run 종료 후 반드시 입력한다.

```text
Run ended: Curse Ending

Fairness score (1-5): 4
Restart intent (1-5): 5
Most interesting choice: 성수가 없어서 우물을 정화하지 못한 선택
Most boring event: 식량 부족
Did any item matter? rope, torch
Did curse affect your strategy? yes
Would you play another run? yes
```

---

# 8. 자동 요약 출력

Run 종료 후 콘솔은 아래 요약을 출력한다.

```text
=== Run Summary ===

Turns survived: 17
Ending: Curse Ending
Restart intent: 5/5
Fairness: 4/5

Choice Stats:
Safe choices: 5
Risky choices: 7
Item-based choices: 3
Unavailable item choices shown: 4

State Impact:
Curse influenced choices: 4
Food influenced choices: 2
Money influenced choices: 1

Item Impact:
Rope mattered: 2
Torch mattered: 1
Holy Water missed: 3

Warnings:
- Event simple_trade selected same choice every time.
- Curse rose quickly but gave few interesting choices.
```

---

# 9. MVP-0 분석 리포트

옵션 명령:

```bash
python tools/console_simulator.py analyze logs/
```

출력해야 할 것:

```text
Average restart intent
Average fairness
Fixed-answer event candidates
Most boring events
Most impactful items
Least useful items
Curse influence count
Combat event quality warnings
Schema warnings
```

---

# 10. 검증 우선순위

콘솔 시뮬레이터는 재미를 완전히 증명하지 않는다.

하지만 아래를 빠르게 확인한다.

1. 선택이 정답 찾기로 흐르는가?
2. 아이템이 의미 있는가?
3. 저주가 런을 바꾸는가?
4. 전투형 이벤트가 손익표처럼 느껴지는가?
5. 다시 하고 싶은가?

---

# 11. Codex 구현 지시 기준

Codex에게 구현을 요청할 때 반드시 지시한다.

```text
Flutter 앱을 만들지 말 것.
Flame 연출을 만들지 말 것.
콘솔 시뮬레이터만 만들 것.
MVP-0 검증 로그를 남길 것.
하드코딩 데이터는 허용하되, data/mvp0 YAML로 쉽게 이관 가능하게 구조화할 것.
룰 엔진과 콘솔 출력 코드를 분리할 것.
```

---

# 12. 최소 모듈 제안

```text
tools/
  console_simulator.py
  validate_data.py

src/
  fateweaver/
    models.py
    event_engine.py
    choice_resolver.py
    state_manager.py
    inventory_manager.py
    logger.py
```

Python 프로젝트로 먼저 만들어도 되고, 이후 Dart로 이식한다.

MVP-0의 목적은 Flutter 구현이 아니라 설계 검증이다.
