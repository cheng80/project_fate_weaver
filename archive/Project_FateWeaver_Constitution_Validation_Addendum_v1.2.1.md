# Project FateWeaver Constitution Validation Addendum v1.2.1

## 문서 목적

이 문서는 `Project_FateWeaver_Constitution_v1.2.md`를 대체하지 않는다.

본 문서는 Office Hour 2차 피드백을 반영하여 Constitution v1.2에 추가되어야 할 **검증 강화 조항**을 정의한다.

> 목표: Project FateWeaver를 PRD-ready로 만들기 전에 반드시 Test-ready 상태로 만든다.

---

# 1. 현재 판정

| 항목 | 판정 |
|---|---|
| PRD 직행 | 불가 |
| Constitution 방향성 | 유효 |
| 검증 가능성 | 부족 |
| 다음 목표 | PRD-ready가 아니라 Test-ready |
| 우선 작업 | MVP-0 콘솔 검증 패키지 완성 |

---

# 2. 헌법 개정 원칙

Constitution v1.2는 방향 헌법으로는 유효하다.

그러나 PRD, World Bible, YAML Schema, Codex 구현 지시의 상위 기준이 되려면 다음을 반드시 보강해야 한다.

1. **측정 가능한 검증 기준**
2. **실패 판정 기준**
3. **MVP-0 예외 규정**
4. **Codex 콘텐츠 거절 기준**
5. **Open Question의 가설/검증/결정 분리**
6. **Validator-ready Schema**
7. **Console Simulator 실험 프로토콜**

---

# 3. 핵심 개정 선언

## 3.1 PRD 금지 조건

아래 조건을 만족하기 전에는 PRD를 작성하지 않는다.

```text
MVP-0 콘솔 검증 미완료
Event Grammar v0.2 미정의
Open Questions 핵심 항목 미정리
PRD Entry Gate 미통과
```

---

## 3.2 World Bible 대형 작성 금지

MVP-0 전에는 대형 World Bible을 작성하지 않는다.

허용:

```text
MVP 1~2개 지역에 필요한 최소 World Seed
```

금지:

```text
전체 세계관, 대륙사, 종족사, 장기 서사, 대규모 지역 백과
```

이유:

```text
재미 검증 전에 세계관 제작으로 도망가는 것을 방지한다.
```

---

## 3.3 하드코딩 예외 규정

Constitution은 콘텐츠 하드코딩을 금지한다.

단, MVP-0에서는 예외를 허용한다.

### 허용 범위

```text
콘솔 실험용 임시 이벤트 데이터
콘솔 실험용 임시 아이템 데이터
콘솔 실험용 임시 상태값
```

### 금지 범위

```text
Flutter MVP에 하드코딩 데이터 이월
PRD 이후 하드코딩 유지
콘텐츠 로직과 룰 엔진 로직 결합
```

### 폐기 조건

MVP-0 종료 후 하드코딩 데이터는 다음 중 하나로 처리한다.

1. YAML로 이관
2. 폐기
3. 테스트 fixture로만 보존

---

# 4. PRD Entry Gate

다음 조건을 모두 만족해야 PRD 작성으로 넘어갈 수 있다.

## 4.1 실행 조건

| 항목 | 기준 |
|---|---|
| 테스트 방식 | MVP-0 Console Simulator |
| 최소 실행 회차 | 5회 |
| 권장 실행 회차 | 10회 |
| 최소 이벤트 수 | 12개 |
| 권장 이벤트 수 | 15개 |
| 최소 아이템 수 | 5개 |
| 최소 상태 수 | 5개 |
| 저주 관련 이벤트 | 최소 4개 또는 전역 modifier 1개 |
| 전투형 이벤트 | 2~3개 |

---

## 4.2 정량 통과 기준

아래 중 7개 이상 통과해야 PRD 진입 가능.

| ID | 기준 | 통과 조건 |
|---|---|---|
| G01 | 반복 의향 | 테스트 후 재시작 의향 평균 4/5 이상 |
| G02 | 죽음 납득도 | 사망/실패 원인 납득도 평균 4/5 이상 |
| G03 | 정답 고정 방지 | 항상 같은 선택이 최선인 이벤트 50% 이하 |
| G04 | 아이템 영향 | 아이템이 선택 가치에 영향 준 이벤트 30% 이상 |
| G05 | 상태 영향 | 상태가 선택 가치에 영향 준 이벤트 30% 이상 |
| G06 | 저주 영향 | 저주가 전략을 바꾼 사례 3회 이상 |
| G07 | 선택 후회 | 선택 후회/대안 고민 기록 3회 이상 |
| G08 | 미래 영향 | 선택 결과가 다음 이벤트/상태에 영향 준 사례 30% 이상 |
| G09 | 이벤트 피로 | 같은 이벤트 재등장 시 지루함 점수 평균 3/5 이하 |
| G10 | 전투형 이벤트 | 전투형 이벤트가 단순 손익표라는 평가 50% 이하 |

---

## 4.3 정성 통과 기준

테스트 로그에 아래 반응 중 3개 이상이 기록되어야 한다.

```text
이번엔 다른 아이템으로 시작해보고 싶다.
이번엔 저주를 일부러 쌓아보고 싶다.
이번엔 평판을 버리고 돈을 모아보고 싶다.
이번 선택을 나중에 후회할 것 같다.
다음 이벤트가 궁금하다.
한 이벤트만 더 보고 싶다.
```

---

# 5. Open Questions 상태 규칙

기존 `Decided`는 너무 빠르게 사용되었다.

앞으로 상태는 다음을 사용한다.

| 상태 | 의미 |
|---|---|
| Open | 아직 명확한 가설 없음 |
| Provisional | 현재 가설은 있으나 검증 전 |
| Needs Test | MVP-0 또는 후속 실험 필요 |
| Decided | 검증 후 결정 |
| Deferred | MVP 이후로 연기 |
| Rejected | 폐기 |

## 5.1 Decided 조건

아래 중 하나를 만족해야 `Decided`로 둘 수 있다.

1. MVP-0 로그로 검증됨
2. Constitution에서 철학적으로 고정됨
3. 기술적 제약으로 결정됨
4. 명시적 trade-off 기록이 있음

그 외에는 `Provisional` 또는 `Needs Test`로 둔다.

---

# 6. Codex 콘텐츠 생성 제한

Codex는 이벤트 초안을 생성할 수 있다.

그러나 다음 기준을 통과하지 못하면 게임 데이터로 편입하지 않는다.

## 6.1 자동 거절 조건

- 선택지 3개 미만
- 모든 선택지가 같은 상태만 변경
- 대가 없는 보상 선택지 2개 이상
- 조건부 선택지 없음
- 미래 영향 없음
- 존재하지 않는 태그 사용
- condition grammar 위반
- result와 result_pool 동시 사용
- 전투형 이벤트가 단순 `health -1 / money +N`로 끝남
- 저주 이벤트가 단순 패널티만 제공
- 같은 이벤트 재등장 시 변주 규칙 없음

---

# 7. 저주 시스템 검증 강화

저주는 핵심 시스템 후보로 둔다.

그러나 검증 전에는 `핵심 시스템 확정`으로 선언하지 않는다.

## 7.1 MVP-0 저주 검증 조건

MVP-0에는 아래 중 하나를 반드시 포함한다.

1. 저주 관련 이벤트 최소 4개
2. 저주 전역 modifier 1개 이상
3. 저주 수치에 따라 선택지가 변하는 이벤트 2개 이상

## 7.2 저주 실패 조건

아래 중 하나라도 발생하면 저주 시스템을 축소 또는 재설계한다.

- 저주는 무조건 낮추는 것이 정답
- 저주가 단순 HP/식량 패널티와 다르지 않음
- 저주가 다음 이벤트 풀을 체감 가능하게 바꾸지 않음
- 저주 선택지가 항상 회피 대상
- 저주가 재미보다 관리 부담만 늘림

---

# 8. 이벤트 문법 예외 규정

Event Quality Checklist는 기본 규칙이다.

하지만 모든 이벤트가 같은 구조가 되면 반복 피로가 생긴다.

따라서 다음 예외를 허용한다.

## 8.1 예외 이벤트 유형

| 유형 | 설명 |
|---|---|
| Mood Event | 분위기와 세계감을 주는 가벼운 이벤트 |
| Relief Event | 회복/휴식 중심 이벤트 |
| Foreshadow Event | 미래 위험을 예고하는 이벤트 |
| Chain Seed Event | 후속 이벤트 가능성을 여는 이벤트 |
| Curse Twist Event | 저주 수치에 따라 의미가 바뀌는 이벤트 |

단, 예외 이벤트도 전체 이벤트의 25%를 넘지 않는다.

---

# 9. Schema 명명 규칙

현재 Schema는 최종 스키마가 아니다.

따라서 이름은 다음으로 고정한다.

```text
Event Grammar Draft YAML Schema v0.2
```

금지:

```text
Final Schema
Production Schema
PRD Schema
```

---

# 10. 다음 작업

이 Addendum을 반영하여 다음 문서를 기준 문서로 둔다.

1. `Project_FateWeaver_Open_Questions_Register_v0.2.md`
2. `Project_FateWeaver_MVP_Loop_Validation_Plan_v0.2.md`
3. `Project_FateWeaver_Event_Grammar_Draft_YAML_Schema_v0.2.md`
4. `Project_FateWeaver_Console_Simulator_Spec_v0.1.md`

---

# 11. 최종 개정 조항

## 제17조

PRD는 MVP-0 콘솔 검증과 PRD Entry Gate를 통과하기 전까지 작성하지 않는다.

## 제18조

Open Questions의 `Decided` 상태는 검증 또는 명시적 trade-off 없이는 사용할 수 없다.

## 제19조

MVP-0에서는 하드코딩 데이터를 허용하되, 이는 실험용 예외이며 MVP-1 이전에 폐기 또는 YAML 이관해야 한다.

## 제20조

저주는 핵심 시스템 후보이나, MVP-0 검증 전까지 확정 시스템으로 선언하지 않는다.

## 제21조

Schema는 validator-ready가 되기 전까지 Draft로 표기한다.
