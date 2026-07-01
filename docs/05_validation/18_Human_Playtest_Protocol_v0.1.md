# [Current] Human Playtest Protocol v0.1

> 상태: [Current] FateWeaver Text MUD / console playtest를 사람이 진행할 때 사용할 절차와 관찰 기준 문서.

## 1. 목적

이 protocol은 FateWeaver P1 human playtest를 같은 방식으로 진행하기 위한 운영 절차다.

## 2. 테스트 전 준비

- 선택할 run을 [P1 Human Playtest Scenario Pack](../06_plans/12_P1_Human_Playtest_Scenario_Pack_v0.1.md)에서 고른다.
- 해당 run의 Text MUD log를 준비한다.
- JSON log는 진행자 참고용으로만 둔다.
- [Human Playtest Feedback Form](19_Human_Playtest_Feedback_Form_v0.1.md)을 준비한다.
- 플레이어에게 내부 seed, slot_role, score rule은 설명하지 않는다.

## 3. 테스트 진행 순서

1. 플레이어 안내문을 읽어 준다.
2. Run 시작 정보와 첫 turn을 보여 준다.
3. 플레이어가 각 turn에서 선택하고 싶은 카드를 말하게 한다.
4. 진행자는 선택 이유, 헷갈린 점, 반복감, 흥미로운 순간을 짧게 기록한다.
5. 중간에 막히면 "지금 무엇을 하려는지 말해 달라"고만 묻는다.
6. Ending과 Quest Report까지 읽힌다.
7. Feedback Form을 작성하게 한다.
8. 진행자는 Run 1 Result Template에 요약한다.

## 4. 진행자 역할

진행자는 관찰자다.

해야 할 일:

- 플레이어가 이해한 Quest 목적을 기록한다.
- 선택 이유를 플레이어의 말로 기록한다.
- 반복감이나 지루함이 나온 turn을 기록한다.
- 자원 변화, clue/omen, ending 반응을 기록한다.

하지 말아야 할 일:

- 정답 선택을 유도하지 않는다.
- 내부 score, seed, director, ontology 설명을 먼저 하지 않는다.
- 문구를 즉석에서 고쳐 읽지 않는다.
- gameplay/balance 변경 제안을 테스트 중에 토론하지 않는다.

## 5. 플레이어 안내문

```text
이 테스트는 완성된 게임이 아니라 텍스트 기반 플레이어블 프로토타입입니다.
각 턴마다 3개의 선택지가 제시됩니다.
정답을 고르려 하지 말고, 현재 상황에서 가장 하고 싶은 선택을 골라 주세요.
읽으면서 헷갈리는 부분, 반복적으로 느껴지는 부분, 흥미로운 순간을 짧게 말해 주세요.
게임 시스템을 분석하려 하기보다 모험을 읽는 느낌으로 진행해 주세요.
```

## 6. 기록할 항목

- Run id / scenario / seed / profile.
- Turn count.
- Ending.
- Player-selected card per turn.
- 선택 이유.
- 헷갈린 용어나 장면.
- 반복적으로 느껴진 card/event/storylet.
- 자원 압박을 느낀 순간.
- clue/omen을 기억한 순간.
- Ending / Quest Report 반응.

## 7. 중단 조건

테스트를 중단하고 기록한다:

- 플레이어가 Quest 목적을 전혀 이해하지 못해 진행이 불가능하다.
- 3장 선택지를 읽는 방식이 명확하지 않다.
- Text MUD log가 누락되거나 turn 순서가 깨져 있다.
- 진행자가 설명을 계속 보충해야만 진행된다.
- 플레이어 피로가 커져 의미 있는 피드백이 어렵다.

## 8. 피드백 수집 방식

- 정량 점수는 1-5 scale로 받는다.
- 정성 답변은 플레이어 표현을 그대로 적는다.
- 진행자 해석은 별도 "facilitator note"로 분리한다.
- 같은 불만이 여러 번 나오면 turn 번호와 함께 반복 기록한다.

## 9. 테스트 후 정리

테스트 후 작성한다:

- [Human Playtest Run 1 Result Template](../07_reviews/59_Human_Playtest_Run_1_Result_Template_v0.1.md)
- 선택 패턴 요약.
- 가장 강한 문제 1-3개.
- 다음 작업 추천:
  - Balance Pass 2.
  - Storylet Variety Expansion 2.
  - Text MUD Narrative Polish 2.
  - UI Prototype Prep.
  - 추가 playtest.

## 10. 금지 사항

- 테스트 중 gameplay/data를 수정하지 않는다.
- 테스트 중 Text MUD 문구를 고쳐 읽지 않는다.
- 새 scenario를 즉석에서 만들지 않는다.
- 플레이어에게 내부 구현 의도를 설명해 반응을 유도하지 않는다.
- 한 명의 반응만으로 balance를 바로 조정하지 않는다.
