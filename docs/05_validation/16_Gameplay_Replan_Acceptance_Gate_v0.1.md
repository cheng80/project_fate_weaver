# Gameplay Replan Acceptance Gate v0.1

> 상태: [Current] 현재 Gameplay Replan 작업의 기준 문서.

## Gate 목적

Gameplay Replan 구현 또는 콘텐츠 확장 작업이 완료되었다고 판단하기 위한 최소 승인 기준이다.

이 Gate는 단순 Console Validation PASS, JSON/Text 로그 생성, 3회 run 성공을 최종 완료로 보지 않는다. 최신 완료 판단은 Quest 목적, Expedition Clock, 3-Card Choice UI, Multi-Select, Situation Director, Economy/Reputation/Score, Quest Report가 실제 선택 의미를 만드는지에 둔다.

---

## 필수 통과 조건

- Quest Layer가 존재한다.
- Expedition Clock이 존재한다.
- 표준 Run이 Day / Turn / Time of Day를 가진다.
- 매 Turn 3장의 카드가 제시된다.
- 1장 선택과 조건부 다중 선택이 처리된다.
- 선택 결과가 resource/status/economy/reputation/score/quest_progress/next_event_tags에 반영된다.
- Situation Director가 현재 Quest, Region, Day/Turn, State, Item, Clue, Omen, Economy, Reputation을 보고 후보를 만든다.
- Weighted Candidate Pool이 단일 최고 가중치 선택이 아니라 후보군 기반으로 작동한다.
- JSON Log와 Text MUD Play Log가 모두 유지된다.
- 저주는 상태/위험 요소 중 하나로만 다뤄진다.

---

## 완료로 보지 않는 경우

- 3회 run PASS만 있음
- JSON/Text 로그만 생성됨
- 카드가 3장으로 고정 출력되지만 온톨로지와 연결되지 않음
- Multi-Select가 UI/로그에만 있고 실제 결과 합성이 없음
- money/reputation/score가 숫자 변화만 하고 선택 의미를 만들지 않음
