# Text MUD Gameplay Simulator Spec v0.1

## 1. 문서 목적

이 문서는 Console Simulator가 실게임형 텍스트 모험 프로토타입으로 작동하기 위한 실행 사양을 정의한다.

기존 JSON 로그와 Text MUD 로그는 유지한다. 그러나 완료 기준은 단순 PASS가 아니라, Quest 목적, Day/Turn 진행, 3-Card 선택, 다중 선택, 경제/점수/평판/후속 사건 연결이 실제로 작동하는 것이다.

---

## 2. 실행 단위

```text
1 Run = 1 Quest Expedition
```

Run은 다음을 포함한다.

- active quest
- run_clock
- player_state
- current_region
- storylet history
- card selection history
- resource/status/economy changes
- quest progress
- score
- ending / quest report

---

## 3. 매 Turn 처리

1. 현재 Quest 확인
2. Expedition Clock 확인
3. 현재 Region 확인
4. Player State 확인
5. Situation Director가 Storylet 후보 추출
6. Weighted Candidate Pool에서 Storylet 선택
7. Card Candidate Pool 생성
8. 최종 3장 카드 선정
9. 가능한 Multi-Select 조합 표시
10. 선택 처리
11. Result Engine 적용
12. Quest Progress 갱신
13. Score 갱신
14. Turn / Day 진행
15. 종료 조건 확인

---

## 4. 출력 요구사항

### JSON Log

기계 검증용으로 유지한다.

필수 포함:

- seed
- scenario
- quest
- run_clock
- selected storylet
- presented cards
- selected cards
- result
- state snapshots
- score changes
- next_event_tags
- quest report

### Text MUD Play Log

사람이 읽는 플레이 로그로 출력한다.

필수 포함:

- Day / Turn / Time
- Quest
- Region
- 현재 상태
- 상황 설명
- 3장 카드
- 다중 선택 가능 여부
- 선택 결과
- 자원/상태/평판/점수 변화
- 다음 사건 변화
- Quest 진행도
- Run Review

---

## 5. 표준 Run 기준

| 항목 | 기준 |
|---|---:|
| Standard Run | 25~35 Turn |
| Day | 5~7일 |
| Turn per Day | 4~6 |
| Cards per Turn | 3 |
| Selected Cards | 기본 1장, 조건부 2장 이상 |
| Sample Runs | 최소 10회 |

---

## 6. 완료 기준

- Quest 목적이 명확하다.
- Day/Turn이 진행된다.
- 매 Turn 3장 카드가 제시된다.
- 1장 선택과 다중 선택이 처리된다.
- 선택 결과가 자원, 상태, 경제, 평판, 점수, 다음 사건에 반영된다.
- Storylet 후보가 온톨로지 관계에 따라 선택된다.
- 같은 가중치 Tier 안에서도 후보 다양성이 있다.
- 최근 반복 방지 또는 태그 쿨다운이 있다.
- JSON Log와 Text MUD Play Log가 모두 생성된다.
- 저주는 여러 상태/위험 요소 중 하나로만 다뤄진다.
