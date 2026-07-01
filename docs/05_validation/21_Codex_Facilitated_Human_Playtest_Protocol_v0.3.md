# [Current] Codex Facilitated Human Playtest Protocol v0.3

> 상태: [Current] Codex가 진행자 역할을 하고, 사용자는 오직 1/2/3 번호만 선택하는 대화형 human playtest protocol이다.

## 1. 문서 목적

이 문서는 FateWeaver P1 human playtest를 Codex-facilitated 방식으로 진행할 때의 운영 규칙을 정의한다.

v0.3의 핵심은 플레이 중 사용자가 피드백, 선택 이유, 점수 평가를 입력하지 않는다는 점이다. 사용자는 매 turn `1`, `2`, `3` 중 번호만 선택한다.

## 2. 역할

Codex는 다음 역할을 맡는다.

- 진행자
- 룰 설명자
- 턴 진행자
- 선택지 제시자
- 결과 설명자
- 관찰자
- 기록자
- 테스트 종료 후 요약자

사용자는 다음 역할만 맡는다.

- 플레이어
- 선택자

## 3. 사용자 입력 규칙

플레이 중 사용자 입력은 아래 중 하나뿐이다.

```text
1
2
3
```

Codex는 플레이 중 아래를 요구하지 않는다.

- 선택 이유
- 1-5점 평가
- 한 줄 피드백
- 결과 납득도
- 자유 의견

사용자가 이유를 덧붙이면 선택 번호만 진행에 사용하고, 이유는 마지막 summary에서 참고 메모로만 다룬다.

## 4. 매 턴 표시 형식

```md
## Day {day} / Turn {turn}

### 현재 상황
{event_summary}

### 현재 상태
- Health: {health}
- Food: {food}
- Money: {money}
- Reputation: {reputation}
- Risk: {risk}
- Progress: {progress}

### 선택지

1. **{card_1_title}**
   - 의도: {card_1_intent}
   - 부담/위험: {card_1_cost_or_risk}

2. **{card_2_title}**
   - 의도: {card_2_intent}
   - 부담/위험: {card_2_cost_or_risk}

3. **{card_3_title}**
   - 의도: {card_3_intent}
   - 부담/위험: {card_3_cost_or_risk}

선택 번호만 입력해 주세요.
```

주의:

- 내부 점수나 hidden scoring은 공개하지 않는다.
- 결과를 미리 확정적으로 말하지 않는다.
- 정답처럼 유도하지 않는다.
- 선택 이유를 묻지 않는다.

## 5. 선택 후 결과 형식

```md
### 선택
{selected_card_title}

### 결과
{result_summary}

### 변화
- Health: {health_delta}
- Food: {food_delta}
- Money: {money_delta}
- Reputation: {reputation_delta}
- Risk: {risk_delta}
- Progress: {progress_delta}
- Clue/Omen/Item: {special_change}

---
다음 턴으로 진행합니다.
```

결과 직후 플레이어에게 질문하지 않는다.

## 6. Codex 기록 방식

Codex는 플레이 중 다음을 내부 기록한다.

- turn
- day
- situation summary
- presented cards
- selected card
- result summary
- resource changes
- selection type
- possible observed issue

## 7. 관찰 항목

Codex는 사용자에게 묻지 않고 선택 패턴으로 관찰한다.

- quest_progress만 계속 고르는가.
- risk_discovery를 피하는가.
- resource_alternative를 고르는가.
- clue/omen 선택을 고르는가.
- 반복 선택 패턴이 있는가.
- 특정 카드 유형을 계속 무시하는가.
- resource가 낮아졌는데도 자원 선택을 하지 않는가.
- ending 직전 return/resolve 계열을 고르는가.

## 8. 질문 가능한 경우

플레이 중 질문은 사용자의 입력이 선택 번호로 해석되지 않을 때만 허용한다.

```text
1, 2, 3 중 하나로 다시 입력해 주세요.
```

그 외 피드백 질문은 플레이 종료 후에만 한다.

## 9. 중단 조건

다음 조건 중 하나가 발생하면 playtest를 중단하고 결과 문서에 기록한다.

- Quest 목적을 이해할 수 없어 선택 의미가 사라진다.
- 이미 해결한 목적의 선택지가 계속 반복된다.
- 사용자 선택이 실제 다음 state transition에 반영되지 않는다.
- 현재 목표와 무관한 storylet 반복이 플레이를 방해한다.
- 진행자가 보충 설명을 계속 해야만 진행된다.

## 10. 실제 시작 프롬프트

```text
FateWeaver Human Playtest Run 1을 Codex-facilitated 방식으로 진행하자.

너는 진행자 역할을 맡는다.
매 턴 현재 상황과 3개의 선택지/Card를 제시하고, 내가 번호로 선택하면 결과를 설명해줘.
그 다음 바로 다음 턴으로 진행해줘.

사용자는 플레이 중 피드백하지 않는다.
사용자는 선택 이유도 입력하지 않는다.
사용자는 오직 1, 2, 3 중 번호만 선택한다.

사용할 기준:
- Scenario: standard_run_25_35_turn
- Primary seed: 202
- 목표: 25턴 interactive playtest
- hidden score나 ending 조건은 스포일러하지 말 것
- 선택을 유도하지 말 것
- 각 턴 설명은 짧게 유지할 것
- 플레이 중 1~5점 평가, 한 줄 피드백, 선택 이유를 요구하지 말 것
- Codex는 선택 패턴과 결과를 내부적으로 기록할 것
- 마지막에만 전체 요약과 선택적 피드백 질문을 제시할 것

시작 전에 테스트 목적과 진행 방식을 간단히 설명한 뒤 Turn 1부터 시작해줘.
```

## 11. Run 1 적용 결과

2026-07-01 Run 1 attempt에서는 이 protocol의 입력 규칙은 확인됐지만, 진행자가 고정 seed 202 autoplayer log를 재생해 사용자의 `1/2/3` 선택이 실제 state transition을 구동하지 못했다.

따라서 v0.3 protocol을 다시 사용하려면 먼저 manual choice-driven Standard Run runner가 필요하다.
