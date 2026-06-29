# Playable Text Adventure Replan v0.1

> 상태: [Current] 현재 Gameplay Replan 작업의 기준 문서.

## 1. 문서 목적

이 문서는 FateWeaver를 Console Validation 중심 구조에서 실게임형 텍스트 모험 시뮬레이터로 전환하기 위한 단계별 계획이다.

---

## 2. 현재 한계

현재 구조는 다음을 일정 수준 달성했다.

- YAML/schema 검증
- JSON 로그 저장
- Text MUD 로그 출력
- 제한된 sample run

하지만 다음이 부족하다.

- Quest 목적
- Day/Turn 기반 진행감
- 3장 카드 선택 구조
- 다중 선택 조합
- 충분한 콘텐츠 볼륨
- 경제/점수/평판 연계
- 온톨로지 기반 Situation Director
- 실게임 수준의 모험 길이

---

## 3. 목표 구조

```text
Quest Layer
+ Expedition Clock
+ Ontology Layer
+ Situation Director
+ 3-Card Choice UI
+ Multi-Select Resolver
+ Result Engine
+ Economy / Score / Reputation
+ Quest Report
```

---

## 4. 단계별 계획

### Phase 1. 문서 재정렬

목표:

- Game Structure Replan 문서 확정
- Quest / Expedition / Card Schema 문서 추가
- Gameplay Simulator Spec 추가
- Checklist 추가

산출물:

- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`

---

### Phase 2. 현재 콘텐츠 감사

목표:

- events 수량 확인
- choices/cards 수량 확인
- items 수량 확인
- statuses 수량 확인
- endings 수량 확인
- quest 구조 부재 확인
- economy/score 연결 현황 확인

산출물:

- `docs/07_reviews/14_Content_Volume_Audit_v0.1.md`

---

### Phase 3. 튜토리얼 Quest 설계

목표:

- 약초 채집 의뢰
- 숲길 안전 조사

각 퀘스트는 다음을 포함한다.

- Quest 목적
- Day 제한
- 10~15 Turn 구성
- 3장 카드 제시
- 성공/부분 성공/실패
- 보상/해금

---

### Phase 4. Expedition Clock 구현

목표:

- day
- turn
- turns_today
- time_of_day
- act
- day_end processing

---

### Phase 5. 3-Card Choice 구현

목표:

- Card Candidate Pool
- slot role
- 3장 카드 선정
- 카드 표시
- 1장 선택

---

### Phase 6. Multi-Select 구현

목표:

- 2장 조합 선택
- combo
- conflict
- cost
- unlock
- risk modifier

---

### Phase 7. 경제/점수/평판 연계

목표:

- money 사용처 구현
- reputation 반응 구현
- score/run review 구현
- food/health 장기 탐험 연계

---

### Phase 8. 콘텐츠 볼륨 확장

목표:

- Quest 10개 이상
- Storylet 60개 이상
- Card 후보 150개 이상
- Item 25개 이상
- Clue 25개 이상
- Omen 20개 이상
- Ending 8개 이상

---

## 5. 완료 기준

- 표준 Run이 25~35 Turn 진행된다.
- Quest 목적이 명확하다.
- 매 Turn 3장의 카드가 제시된다.
- 1장 선택과 다중 선택이 가능하다.
- 결과가 다음 사건과 Quest 진행에 영향을 준다.
- 경제, 평판, 점수가 실제 선택 의미를 만든다.
- JSON Log와 Text MUD Play Log가 유지된다.
