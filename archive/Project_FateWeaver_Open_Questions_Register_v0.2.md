# Project FateWeaver Open Questions Register v0.2

## 문서 목적

이 문서는 Project FateWeaver의 핵심 질문, 현재 가설, 검증 방법, 되돌림 조건을 추적하는 문서다.

v0.2부터 `Decided`를 신중하게 사용한다.

---

# 1. 상태 값

| 상태 | 의미 |
|---|---|
| Open | 아직 명확한 가설 없음 |
| Provisional | 현재 가설은 있으나 검증 전 |
| Needs Test | MVP-0 또는 후속 실험 필요 |
| Decided | 검증 후 결정 |
| Deferred | MVP 이후로 연기 |
| Rejected | 폐기 |

---

# 2. 우선순위

| 우선순위 | 의미 |
|---|---|
| Critical | PRD 전 반드시 해결 |
| High | MVP-0 전 해결 또는 실험 필요 |
| Medium | MVP-1 전 해결 가능 |
| Low | 이후 검토 |

---

# 3. 질문 목록

| ID | 질문 | 현재 가설 | 상태 | 근거 | 검증 방법 | 되돌림 조건 | 우선순위 | 반영 문서 |
|---|---|---|---|---|---|---|---|---|
| Q001 | 1차 검증 목표는 재미인가 데이터 구조인가? | 재미 검증이 우선 | Decided | Office Hour 피드백에서 문서/온톨로지 제작 도피 위험 지적 | MVP-0을 콘솔 루프 검증으로 정의 | 재미 검증 없이 Schema/World Bible이 우선될 경우 재검토 | Critical | Constitution Addendum |
| Q002 | MVP를 40~50 이벤트로 갈 것인가? | MVP-0은 12~15 이벤트로 축소 | Decided | 40~50개는 제작 단계로 흐를 위험 | MVP-0 테스트 후 확장 판단 | 12~15개로 의미 있는 판단이 전혀 안 나오면 재검토 | Critical | MVP Validation Plan |
| Q003 | 저주는 핵심 시스템인가? | 핵심 변형 시스템 후보 | Needs Test | 독특한 축이지만 현재 검증 부족 | 저주 이벤트 4개 또는 전역 modifier로 테스트 | 저주가 무조건 회피 대상이면 보조 상태로 축소 | High | Curse Policy |
| Q004 | 아이템은 선택지 해금만 하는가? | 해금 + 리스크/확률/정보/미래 이벤트 조작 | Provisional | 단순 열쇠는 수집 욕구 약함 | 아이템 역할별 이벤트에서 선택 변화 기록 | 정보/확률 조작이 과복잡하면 해금/완화 중심으로 축소 | High | Item Role Taxonomy |
| Q005 | Event 반복 피로를 줄이는 최소 변주 규칙은? | 상태/아이템/저주에 따라 선택 가치가 변해야 함 | Needs Test | Reigns식 카드 암기화 위험 | 같은 이벤트 재등장 시 선택 변화 로그 확인 | 재등장 시 항상 같은 선택이면 Variation Rule 강화 | High | Event Grammar |
| Q006 | 좋은 이벤트의 통과 기준은? | Event Quality Checklist 사용 | Provisional | Codex 콘텐츠 품질 통제 필요 | 12~15개 이벤트에 적용 후 통과/거절 비율 확인 | 모든 이벤트가 같은 구조가 되면 예외 규칙 추가 | Critical | Event Quality Checklist |
| Q007 | CombatEventResolver는 MVP에 필요한가? | MVP-0은 일반 ChoiceResolver로 처리 | Provisional | 별도 전투 시스템은 Core Fun 흐릴 위험 | 전투형 이벤트 2~3개 테스트 | 일반 Resolver로 전투 감각 표현 불가 시 재검토 | Medium | Combat Policy |
| Q008 | World Bible은 전체 세계관인가 MVP 가이드인가? | 우선 MVP 1~3개 지역 생산 가이드 | Provisional | 대형 World Bible은 검증 전 과투자 | MVP-0 이후 필요 범위 재검토 | 세계 톤 부족으로 이벤트 품질이 낮으면 보강 | Medium | World Bible |
| Q009 | Codex 이벤트 reject 기준은? | Reject Criteria 사용 | Provisional | AI 양산 품질 저하 위험 | Codex 생성 이벤트 10개에 적용 | 좋은 이벤트까지 과도하게 거절하면 기준 완화 | Critical | Event Grammar |
| Q010 | PRD 전에 무엇을 검증해야 하는가? | PRD Entry Gate 통과 | Provisional | PRD 직행은 위험 | MVP-0 로그로 Gate 측정 | Gate가 비현실적으로 높거나 낮으면 조정 | Critical | Validation Addendum |
| Q011 | 플레이어는 누구인가? | 미정 | Open | UX/톤/이벤트 관점 결정 필요 | Superpowers Brainstorm 또는 World Seed에서 결정 | MVP-0에 영향 크면 우선 결정 | High | World Seed |
| Q012 | 최종 목표는 귀환인가 성소 도달인가? | 미정 | Open | 엔딩/튜토리얼/런 목표에 영향 | MVP-0에서 1개 목표 임시 설정 | 목표 부재로 테스트 몰입이 낮으면 우선 결정 | High | Run System |
| Q013 | 카드와 아이템은 동일 개념인가? | UI는 카드, 내부는 Item 계열 | Provisional | 카드 UI와 데이터 타입 분리 필요 | Schema v0.2 작성 시 검증 | 데이터가 과복잡하면 단일 Item으로 축소 | Medium | Item Schema |
| Q014 | 전투형 이벤트는 재미를 줄 수 있는가? | 2~3개로 MVP-0 테스트 | Needs Test | 판타지 감각에 필요하지만 별도 시스템은 위험 | Combat Event 로그 별도 기록 | 손익표 느낌이 강하면 전투형 이벤트 문법 보강 | Medium | Combat Policy |
| Q015 | 합성 이벤트는 실제 생산성을 높이는가? | 개발 보조로만 제한 | Needs Test | 런타임 생성은 밸런스/문체 위험 | Codex 초안 생성 워크플로우에서 테스트 | 초안 품질이 낮으면 수동 이벤트 중심으로 전환 | Medium | Content Pipeline |
| Q016 | Console Simulator가 PRD 전 필수인가? | 필수 | Decided | 측정 가능한 루프 검증 필요 | Simulator Spec 작성 후 실행 | 콘솔이 오히려 판단 재미를 왜곡하면 단순 Flutter text UI로 대체 | Critical | Console Simulator Spec |
| Q017 | Schema는 언제 production-ready인가? | Validator 통과 후 | Provisional | 현재는 Draft 수준 | validate_data.py 구현 후 통과 여부 확인 | Validator가 너무 느슨하면 Schema 강화 | High | Schema v0.2 |
| Q018 | 저주 전역 modifier를 넣을 것인가? | MVP-0에 1개 이상 추천 | Needs Test | 이벤트 4개만으로 저주 체감 부족 가능 | 저주 수치별 이벤트 weight 변화 테스트 | 과복잡하면 저주 이벤트 4개로 대체 | High | Curse Policy |
| Q019 | 선택지 3개 규칙은 항상 강제인가? | 기본 3개, 예외 허용 | Provisional | 모든 이벤트 획일화 위험 | 예외 이벤트 비율 25% 이하로 테스트 | 예외가 재미를 흐리면 3개 고정 | Medium | Event Grammar |
| Q020 | 혼자 테스트로 충분한가? | MVP-0 1차는 Solo Heuristic 허용, 이후 외부 2명 권장 | Provisional | 초기 비용 절감 | Solo 로그 후 외부 2인 비교 | 자기확증이 심하면 외부 테스트 우선 | High | Validation Plan |

---

# 4. 다음 액션

1. Critical 항목은 MVP-0 전 모두 정리한다.
2. Provisional은 검증 로그가 생기기 전까지 Decided로 올리지 않는다.
3. Needs Test는 MVP-0 로그 항목과 연결한다.
4. Open 항목은 Superpowers Brainstorm으로 넘길 수 있다.
5. PRD 작성 전 Q001, Q002, Q006, Q009, Q010, Q016은 반드시 Decided여야 한다.
