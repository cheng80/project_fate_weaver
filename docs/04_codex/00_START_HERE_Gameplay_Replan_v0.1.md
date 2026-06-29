# Codex Start Here - Gameplay Replan v0.1

> 상태: [Current] 현재 Gameplay Replan 작업의 기준 문서.

## 문서 목적

이 문서는 Codex가 Project FateWeaver의 Gameplay Replan 관련 작업을 시작하기 전에 반드시 먼저 읽어야 하는 최신 기준 문서다.

현재 프로젝트에는 기존 Console Validation 기준 문서와 새 Gameplay Replan 기준 문서가 함께 존재한다.  
따라서 작업을 시작하기 전에 이 문서를 먼저 읽고, 현재 최상위 기준이 무엇인지 확인한다.

---

## 반드시 먼저 읽을 문서

새 작업을 시작하기 전에 아래 문서를 순서대로 읽는다.

1. `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
2. `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
3. `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
4. `docs/04_codex/14_Codex_Gameplay_Replan_Brief_v0.1.md`
5. `docs/05_validation/15_Gameplay_Replan_Checklist_v0.1.md`
6. `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`

---

## 현재 최상위 목표

FateWeaver의 현재 목표는 단순 Console Validation, YAML/schema 검증, JSON/Text 로그 출력 검증이 아니다.

현재 최상위 목표는 다음 구조를 갖춘 실게임형 텍스트 모험 시뮬레이터다.

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

## 핵심 게임 구조

플레이어는 Quest 목적을 가지고 Expedition을 시작한다.

Expedition은 Day / Turn / Time of Day / Act를 가진다.

매 Turn마다 Situation Director가 현재 Quest, Region, Day/Turn, Player State, Item, Clue, Omen, Economy, Reputation, 이전 선택 결과를 바탕으로 Storylet과 Card 후보를 만든다.

사용자에게는 매 Turn 3장의 카드가 제시된다.

플레이어는 기본적으로 1장의 카드를 선택하지만, 조건이 맞으면 2장 이상의 카드를 조합해 선택할 수 있다.

선택 결과는 다음 항목에 반영된다.

- health
- food
- money
- reputation
- risk
- status
- item
- clue
- score
- next_event_tags
- quest_progress

---

## 현재 기준과 과거 기준 구분

기존 Console Validation 문서는 과거 기준선이다.

다음 문서는 기존 단계의 기준으로 유지하되, 최신 Gameplay Replan 작업의 최상위 기준으로 사용하지 않는다.

- `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`
- `docs/04_codex/06_Codex_Text_MUD_Console_Simulator_Loop_Brief_v0.1.md`

현재 새 작업 기준은 다음 문서다.

- `docs/04_codex/14_Codex_Gameplay_Replan_Brief_v0.1.md`

---

## 작업 전 확인 규칙

Gameplay Replan 관련 작업을 시작하기 전에 다음을 수행한다.

1. 이 문서를 먼저 읽는다.
2. 반드시 먼저 읽을 문서 목록을 순서대로 확인한다.
3. 작업 전, 최신 게임 구조를 10줄 이내로 요약한다.
4. 기존 Console Validation 기준과 새 Gameplay Replan 기준이 충돌할 경우, 새 Gameplay Replan 기준을 우선한다.
5. 단, 기존 구현과 데이터 구조를 대규모로 갈아엎지 않는다.

---

## 금지 사항

- 단순히 3회 run PASS를 완료로 보지 않는다.
- JSON/Text 로그 생성만으로 완료로 보지 않는다.
- 저주를 메인 테마로 만들지 않는다.
- Flutter UI 구현으로 넘어가지 않는다.
- Flame 렌더링 구현으로 넘어가지 않는다.
- 기존 구조를 대규모로 갈아엎지 않는다.
- PRD나 World Bible을 대량 작성하지 않는다.
- Quest, Expedition Clock, 3-Card Choice UI, Multi-Select, Economy/Score/Reputation 구조를 무시하지 않는다.

---

## 완료 출력 기준

이 문서를 기준으로 작업을 시작한 경우, 작업 결과 보고에 다음 항목을 포함한다.

```text
STATUS: DONE 또는 PARTIAL

읽은 기준 문서:
- ...

이해한 최신 게임 구조 요약:
- ...

수정한 파일:
- ...

변경 요약:
- ...

검증 결과:
- ...

남은 문제:
- ...
```
