# Project FateWeaver Open Questions Register v0.1

## 문서 목적

이 문서는 Project FateWeaver의 결정되지 않은 핵심 질문을 추적하는 문서다.

Office Hour 피드백 이후 Constitution v1.2에 반영할지, World Bible로 넘길지, PRD에서 결정할지 관리한다.

---

# 상태 값

| 상태 | 의미 |
|---|---|
| Open | 아직 결정되지 않음 |
| Needs Test | 콘솔 프로토타입 검증 필요 |
| Decided | 결정됨 |
| Deferred | MVP 이후로 연기 |
| Rejected | 폐기 |

---

# 질문 목록

| ID | 질문 | 현재 판단 | 상태 | 우선순위 | 반영 문서 |
|---|---|---|---|---|---|
| Q001 | 1차 검증 목표는 재미인가 데이터 구조인가? | 재미 검증이 우선 | Decided | Critical | Constitution v1.2 |
| Q002 | MVP를 40~50 이벤트로 갈 것인가? | MVP-0은 12~15 이벤트로 축소 | Decided | Critical | Constitution v1.2 |
| Q003 | 저주는 핵심 시스템인가? | 핵심 변형 시스템 후보로 검증 | Needs Test | High | Curse Policy |
| Q004 | 아이템은 선택지 해금만 하는가? | 리스크/확률/정보/미래 이벤트 조작까지 확장 | Decided | High | Item Role Taxonomy |
| Q005 | Event 반복 피로를 줄이는 최소 변주 규칙은? | 상태/아이템/태그 기반 가치 변화 필요 | Needs Test | High | Event Grammar |
| Q006 | 좋은 이벤트의 통과 기준은? | Event Quality Checklist 도입 | Decided | Critical | Constitution v1.2 |
| Q007 | CombatEventResolver는 MVP에 필요한가? | MVP-0에서는 일반 ChoiceResolver 사용 | Decided | Medium | Combat Policy |
| Q008 | World Bible은 전체 세계관인가 MVP 가이드인가? | 우선 MVP 3지역 생산 가이드로 제한 | Open | Medium | World Bible |
| Q009 | Codex 이벤트 reject 기준은? | Reject Criteria 추가 | Decided | Critical | Event Quality Checklist |
| Q010 | PRD 전에 무엇을 검증해야 하는가? | MVP-0 Console Loop Validation | Decided | Critical | MVP Validation Plan |
| Q011 | 플레이어는 누구인가? | 미정 | Open | High | World Bible |
| Q012 | 최종 목표는 귀환인가 성소 도달인가? | 미정 | Open | High | Run System |
| Q013 | 카드와 아이템은 동일 개념인가? | UI는 카드, 내부는 Item 계열로 보는 방향 | Needs Test | Medium | Item Schema |
| Q014 | 전투형 이벤트는 재미를 줄 수 있는가? | 2~3개로 MVP-0 테스트 | Needs Test | Medium | Combat Event Policy |
| Q015 | 합성 이벤트는 실제 생산성을 높이는가? | 런타임 생성 금지, 개발 보조로 제한 | Needs Test | Medium | Event Pipeline |

---

# Office Hour 이후 작업

1. Critical 질문부터 해결한다.
2. Decided 항목은 Constitution에 반영한다.
3. Needs Test 항목은 MVP-0에서 검증한다.
4. Open 항목은 Superpowers Brainstorm으로 넘긴다.
5. Deferred 항목은 PRD 이후 검토한다.
