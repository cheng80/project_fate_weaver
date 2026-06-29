# Codex Gameplay Replan Brief v0.1

## 작업 목적

현재 FateWeaver는 Console Validation 중심 구조에서 실게임형 텍스트 모험 시뮬레이터 구조로 재정렬이 필요하다.

Codex의 목표는 바로 대량 구현에 들어가는 것이 아니라, 기존 문서와 데이터 구조를 해치지 않고 다음 상위 구조를 반영하는 것이다.

```text
Quest Layer
+ Expedition Clock
+ Ontology Layer
+ Situation Director
+ Storylet Pool
+ Card Candidate Pool
+ 3-Card Choice UI
+ Multi-Select Resolver
+ Result Engine
+ Economy / Reputation / Score System
+ Quest Report
```

---

## 핵심 방향

- FateWeaver는 단순 로그 검증기가 아니다.
- FateWeaver는 고정 스토리 게임도 아니다.
- FateWeaver는 퀘스트 목적을 가진 DM형 텍스트 모험 게임이다.
- 플레이어는 매 Turn 3장의 카드를 받는다.
- 플레이어는 1장 또는 조건부 다중 카드를 선택한다.
- 상황은 온톨로지 관계와 현재 상태에 따라 선택된다.
- 저주는 메인 테마가 아니라 상태/위험 요소 중 하나다.

---

## 우선 작업

1. 기존 문서와 데이터 구조 파악
2. 현재 이벤트/선택지/아이템/상태/엔딩 볼륨 감사
3. Quest / Expedition / Card 구조를 문서에 반영
4. 필요한 schema 확장 후보 정리
5. 구현 범위 분리
6. 작은 튜토리얼 Quest 1개부터 설계

---

## 금지 사항

- Flutter UI 구현 금지
- Flame 렌더링 구현 금지
- 기존 docs 구조 대규모 변경 금지
- data 대량 추가 금지
- simulator 코드 대규모 재작성 금지
- PRD/World Bible 대량 작성 금지
- 저주 중심 게임으로 확장 금지
- 3회 로그 PASS를 완료 기준으로 삼는 것 금지

---

## 완료 출력

```text
STATUS: DONE 또는 PARTIAL

수정한 파일:
- ...

구조 반영 요약:
- Quest Layer:
- Expedition Clock:
- 3-Card UI:
- Multi-Select:
- Ontology Director:
- Economy/Score:

남은 문제:
- ...

다음 추천 작업:
- ...
```
