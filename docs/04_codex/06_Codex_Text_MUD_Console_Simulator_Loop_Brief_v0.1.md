# Codex 텍스트 MUD형 콘솔 시뮬레이터 루프 작업 지시서 v0.1

## 문서 목적

이 문서는 LazyCodex `ulw-loop` 작업을 위한 기준 문서다.

목표는 Project FateWeaver의 Console Simulator를 단순 YAML/schema 검증기가 아니라, **텍스트 MUD형 게임성 검증 도구**로 보강하는 것이다.

> 기준 구분: 이 문서는 기존 Console Simulator를 Text MUD Play Log 검증 도구로 보강한 단계의 브리프다. 최신 Gameplay Replan 작업에서는 `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`를 먼저 읽고 Quest Layer, Expedition Clock, 3-Card Choice UI, Multi-Select, Economy/Reputation/Score 기준을 우선한다.

이 작업은 Flutter UI나 Flame 렌더링 구현을 시작하라는 의미가 아니다.  
또한 YAML 문법만 검사하는 단순 검증기를 만드는 작업도 아니다.

Console Simulator는 검증 도구가 맞다.  
다만 검증 대상은 YAML 문법만이 아니라, FateWeaver의 핵심 게임 루프와 게임성이다.

---

## 프로젝트 목표 상기

FateWeaver는 단서, 징조, 아이템, 상태 변화를 바탕으로 위험한 판타지 세계를 살아남으며, 플레이어가 자기만의 여정을 엮어가는 선택형 생존/탐험 로그라이크다.

플레이어는 매 선택마다 위험과 보상을 판단해야 한다.  
그 선택은 이후 사건, 생존 가능성, 상태 변화, 자원 변화, 엔딩 가능성에 영향을 줘야 한다.

---

## Console Simulator의 올바른 역할

Console Simulator는 최종 게임 클라이언트가 아니다.

하지만 단순 YAML/schema 검증기도 아니다.

Console Simulator는 Flutter 기반 비주얼 구현 없이도 다음 항목들을 텍스트 MUD처럼 검증할 수 있어야 한다.

- 현재 위치
- 현재 상태
- 보유 자원
- 보유 아이템
- 감지된 단서
- 불길한 징조
- 현재 위험도
- 발생 사건
- 선택지
- 선택별 위험/보상 힌트
- 선택 결과
- 아이템 효과
- 상태 변화
- 다음 사건 변화
- 생존, 실패, 탈출, 엔딩 결과

즉, Console Simulator는 시각적 게임 클라이언트를 만들기 전에 FateWeaver의 핵심 생존/탐험 로그라이크 루프가 실제로 재미있게 작동하는지 확인하는 실험실이다.

---

## 로그 출력 구조 기준

현재 Console Simulator가 JSON 로그 저장 중심이고 stdout에는 `LOG:` 기술 로그만 남는 구조일 수 있다.  
이 경우 JSON 로그 구조를 제거하지 않고, 사람이 읽을 수 있는 Text MUD Play Log 출력 레이어를 추가한다.

### JSON 로그의 역할

JSON 로그는 다음 목적을 위해 유지한다.

- 자동 검증
- 회귀 테스트
- seed/run 비교
- 시뮬레이션 결과 분석
- 추후 Flutter/Flame 클라이언트 연동 준비

JSON 로그 저장 구조는 Project FateWeaver의 검증 자동화와 장기 확장에 필요하므로 제거하지 않는다.

### Text MUD Play Log의 역할

Text MUD Play Log는 사람이 직접 게임성을 확인하기 위한 출력이다.

Text MUD Play Log는 다음 목적을 가진다.

- 사람이 직접 플레이 흐름을 읽고 이해하기
- 사건, 선택, 위험, 보상, 상태 변화를 확인하기
- 단서, 징조, 아이템, 상태가 선택 판단에 영향을 주는지 확인하기
- Flutter 비주얼 구현 없이도 생존/탐험 로그라이크의 재미를 검증하기

### 권장 출력 구조

권장 구조는 다음과 같다.

```text
Simulator Core
├── JSON Log Writer       # 기계 검증용
└── Text MUD Log Renderer # 사람 검증용
```

가능하다면 CLI에 다음 중 하나의 출력 옵션을 추가한다.

```text
--output json
--output mud
--output both
```

또는 다음과 같은 옵션도 허용한다.

```text
--playlog
--pretty
--mud-log
```

CLI 옵션 추가가 현재 구조에 과하다면, 기본 실행에서 요약형 Text MUD Play Log를 stdout에 출력하고 JSON 로그는 기존 경로에 저장한다.

### 중요한 기준

- JSON 로그를 Text MUD 로그로 대체하지 않는다.
- Text MUD 로그를 JSON 로그로 대체하지 않는다.
- 두 출력은 서로 다른 목적을 가진다.
- JSON 로그만 생성되고 stdout에 `LOG:` 중심의 기술 로그만 출력되는 상태는 완료 기준을 만족하지 않는다.
- `LOG:` prefix 문구만 바꾸는 것으로 Text MUD Play Log를 구현했다고 보지 않는다.

---

## 작업 범위

### 1. 현재 프로젝트 상태 파악

수정 전에 현재 프로젝트 구조를 먼저 확인한다.

중요 확인 대상:

- `README.md`
- `docs/00_index/README_Docs_Index.md`
- `docs/01_foundation/`
- `docs/02_schema/`
- `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`
- `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`
- `docs/05_validation/`
- `docs/06_plans/`
- `data/core/`
- `data/content/base/`
- `data/content/packs/`
- `data/scenarios/`
- 기존 simulator 또는 validation 코드

새로운 폴더 구조를 임의로 만들지 않는다.  
현재 프로젝트 구조를 따른다.

---

## 핵심 목표

Console Simulator를 **텍스트 MUD형 생존/탐험 로그라이크 게임성 검증 도구**로 개선한다.

시뮬레이터 출력은 단순 기술 로그가 아니라, 사람이 읽었을 때 짧은 생존 이야기처럼 보여야 한다.

유효한 시뮬레이터 실행은 다음 요소를 포함해야 한다.

- 의미 있는 사건
- 선택지
- 위험과 보상 판단
- 단서 또는 징조에 따른 판단 근거
- 아이템 또는 상태의 영향
- 선택 결과
- 다음 사건 변화
- 생존, 실패, 탈출, 엔딩 가능성

---

## 엔티티 보강 기준

엔티티는 실제 시뮬레이션 동작에 연결될 때만 보강한다.

보강 가능한 엔티티 예시:

- 지역
- 장소
- 사건
- 선택지
- 결과
- 단서
- 징조
- 아이템
- 아이템 역할
- 상태
- 위험
- 자원
- 엔딩
- 시나리오 메타데이터
- seed/run 메타데이터

단순히 개수를 늘리는 것이 목적이 아니다.  
추가 또는 수정한 엔티티는 반드시 선택, 결과, 상태 변화, 위험 판단, 반복 플레이성 중 하나 이상에 연결되어야 한다.

---

## 릴레이션십 보강 기준

엔티티 간 관계를 실제 시뮬레이션에 의미 있게 반영한다.

중요한 관계 예시:

- 지역 → 등장 가능한 사건
- 지역 → 기본 위험도
- 징조 → 앞으로 발생할 수 있는 위험 암시
- 단서 → 선택 판단 보조
- 아이템 → 위험 완화
- 아이템 → 선택지 해금
- 상태 → 위험도 보정
- 상태 → 자원 압박
- 선택 → 즉시 결과
- 선택 → 후속 사건 후보 변화
- 사건 → 후속 사건
- 실패 누적 → 런 종료 위험
- 생존 조건 충족 → 탈출 또는 임시 성공
- 시나리오 → 사용할 콘텐츠 팩

필요한 경우, 시뮬레이터 출력에서 이러한 관계가 드러나야 한다.

---

## Console Simulator 요구사항

Console Simulator는 다음 흐름을 지원해야 한다.

1. run 시작
2. seed 설정 또는 표시
3. scenario와 content pack 로딩
4. 초기 플레이어 상태 설정
5. 현재 지역 또는 위치 표시
6. 현재 상태와 자원 표시
7. 사건 제시
8. 단서, 징조, 위험 힌트 표시
9. 선택지 제시
10. 선택 결과 처리
11. 아이템, 상태, 자원 효과 적용
12. 위험도 또는 생존 압박 갱신
13. 다음 사건으로 진행
14. 생존, 실패, 탈출, 미해결 런 결과 출력

현재 구조가 완전한 대화형 터미널 게임을 지원하지 않아도 괜찮다.  
다만 자동 실행 또는 샘플 실행이라도 결과가 텍스트 MUD형 플레이 로그처럼 읽혀야 한다.

---

## Text MUD Play Log 요구사항

Text MUD Play Log에는 다음 정보가 사람이 읽을 수 있는 형태로 포함되어야 한다.

- run 시작 정보
- seed
- scenario
- 현재 지역 또는 위치
- 현재 상태와 자원
- 보유 아이템
- 감지된 단서
- 불길한 징조
- 현재 위험도
- 발생 사건
- 선택지
- 선택별 위험/보상 힌트
- 선택 결과
- 아이템, 상태, 단서, 징조의 영향
- 다음 사건 변화
- 생존, 실패, 탈출, 엔딩 결과

Text MUD Play Log는 기술 로그가 아니라 플레이 로그여야 한다.

예시는 다음 방향이다.

```text
[Run 시작]
Seed: 1042
Scenario: 상태/위험 보조 검증
Region: 신호의 숲

당신은 축축한 숲길에서 오래된 종소리를 듣는다.
불길한 징조: 나뭇가지가 바람 없이 흔들린다.
현재 위험도: 높음

선택:
1. 종소리가 들리는 쪽으로 이동한다. 위험: 높음 / 보상: 단서 가능성
2. 숲 가장자리로 우회한다. 위험: 낮음 / 보상: 자원 보존
3. 부적을 사용해 주변을 살핀다. 위험: 중간 / 보상: 단서와 상태 위험 완화 가능성

선택 결과:
부적이 희미하게 빛나며 숨겨진 발자국을 드러냈다.
아이템 효과: 낡은 부적 → 숨은 단서 확인, 상태 위험 감소
상태 변화: 식량 -1, 저주 -1
다음 사건 후보가 변경되었다.
```

위 예시는 방향성일 뿐이며, 실제 프로젝트 데이터와 구조에 맞춰 출력한다.

---

## 게임성 요구사항

시뮬레이터 출력은 다음 기준을 만족해야 한다.

- 선택지가 장식처럼 느껴지면 안 된다.
- 일부 선택지는 명확한 위험/보상 구조를 가져야 한다.
- 단서 또는 징조는 플레이어의 판단에 도움을 줘야 한다.
- 아이템은 결정이나 결과에 영향을 줘야 한다.
- 상태 변화는 이후 선택이나 위험도에 영향을 줘야 한다.
- seed, scenario, content pack에 따라 다른 흐름이 나와야 한다.
- 실패 가능성이 있어야 한다.
- 생존 또는 부분 성공 가능성도 있어야 한다.
- 출력은 사람이 읽을 수 있는 플레이 로그여야 한다.
- 출력이 단순 schema 검증 로그에 머물면 안 된다.

---

## 검증 요구사항

주요 변경 후에는 가능한 검증과 시뮬레이터 실행을 수행한다.

필수 검증:

- YAML/schema 검증 통과
- Console Simulator 실행 성공
- 기존 JSON 로그 저장 확인
- Text MUD Play Log 생성 확인
- 최소 3개 이상의 샘플 run 실행
- 3개 run은 서로 다른 seed, scenario, content 조합 중 하나 이상을 사용
- 3개 run은 의미 있는 차이를 보여야 함
- 최소 3개 seed/run에 대해 JSON 로그와 Text MUD Play Log가 모두 확인되어야 함
- 다음 항목 중 최소 2개 이상이 실제 결과에 영향을 줘야 함
  - 단서
  - 징조
  - 아이템
  - 상태
  - 위험도
  - 지역
  - 이전 선택

---

## 샘플 run 증거 형식

최종 보고에는 다음 형식의 요약을 포함한다.

```text
Sample Run 1:
- seed:
- scenario:
- JSON 로그 경로:
- Text MUD Play Log 경로 또는 stdout 확인:
- 주요 사건:
- 의미 있는 선택:
- 단서/징조/아이템/상태 영향:
- 결과:

Sample Run 2:
- seed:
- scenario:
- JSON 로그 경로:
- Text MUD Play Log 경로 또는 stdout 확인:
- 주요 사건:
- 의미 있는 선택:
- 단서/징조/아이템/상태 영향:
- 결과:

Sample Run 3:
- seed:
- scenario:
- JSON 로그 경로:
- Text MUD Play Log 경로 또는 stdout 확인:
- 주요 사건:
- 의미 있는 선택:
- 단서/징조/아이템/상태 영향:
- 결과:
```

---

## 금지 사항

다음 작업은 하지 않는다.

- Flutter UI 구현 금지
- Flame 렌더링 구현 금지
- 시각적 게임 클라이언트 작업 시작 금지
- 대규모 PRD 작성 금지
- 대규모 World Bible 작성 금지
- 전체 프로젝트 구조 재작성 금지
- 기존 docs 구조를 새 구조로 이동 금지
- 시뮬레이션 동작에 연결되지 않은 데이터 대량 추가 금지
- simulator 개선 없이 docs만 늘리는 작업 금지
- 검증 증거 없이 YAML 수량만 늘리는 작업 금지
- 임시 simulator 구조를 장기 아키텍처처럼 고정 금지
- 검증 실패를 조용히 무시 금지
- JSON 로그 저장 구조 제거 금지
- 구조화된 JSON 로그를 사람용 문장 로그로만 대체 금지
- `LOG:` prefix 문구만 바꾸고 Text MUD Play Log 구현으로 처리 금지

---

## 권장 작업 순서

1. 현재 프로젝트 상태 확인
2. simulator 진입점과 검증 명령 확인
3. 현재 데이터 모델과 content pack 확인
4. 현재 JSON 로그 저장 방식 확인
5. 현재 stdout 출력 방식 확인
6. JSON 로그 저장 구조는 유지
7. Text MUD Play Log 출력 레이어 추가
8. 시뮬레이션 개선에 필요한 최소 데이터 관계 보강
9. Console Simulator 출력 개선
10. YAML/schema 검증 실행
11. 최소 3개 샘플 시뮬레이션 실행
12. JSON 로그와 Text MUD Play Log 모두 확인
13. 충돌, 누락 참조, 실행 오류 수정
14. 의미 없는 선택지 제거 또는 조정
15. 변경 파일과 검증 증거 보고

---

## 완료 기준

다음 조건을 모두 만족해야 작업 완료로 본다.

- Console Simulator가 실행된다.
- YAML/schema 검증이 통과하거나, 실패 원인이 명확히 문서화된다.
- 기존 JSON 로그 저장 구조가 유지된다.
- 사람이 읽을 수 있는 Text MUD Play Log가 stdout 또는 별도 `.txt` / `.md` 파일로 생성된다.
- 최소 3개 이상의 샘플 run이 실행된다.
- 최소 3개 seed/run에 대해 JSON 로그와 Text MUD Play Log가 모두 확인된다.
- 샘플 run들이 의미 있게 다르다.
- Text MUD Play Log가 텍스트 MUD형 생존/탐험 플레이 로그처럼 읽힌다.
- Text MUD Play Log는 `LOG:` 중심 기술 로그가 아니라 사건, 선택, 위험/보상, 상태 변화, 아이템/단서/징조 영향, 생존/실패 결과를 읽을 수 있는 플레이 로그여야 한다.
- 선택이 결과에 영향을 준다.
- 단서, 징조, 아이템, 상태, 위험도, 지역, 이전 선택 중 최소 2개 이상이 시뮬레이션 결과에 영향을 준다.
- Flutter/Flame 비주얼 구현이 추가되지 않았다.
- 수정 파일 목록이 정리되어 있다.
- 남은 문제가 기록되어 있다.

---

## 최종 출력 형식

작업 종료 시 다음 형식으로 보고한다.

```text
STATUS: DONE 또는 PARTIAL

수정한 파일:
- ...

추가/보강한 엔티티:
- ...

추가/보강한 릴레이션십:
- ...

Simulator 변경:
- ...

로그 출력 구조 변경:
- JSON 로그:
- Text MUD Play Log:

실행한 검증 명령:
- ...

샘플 run 증거:
- Run 1:
  - seed:
  - scenario:
  - JSON 로그:
  - Text MUD Play Log:
  - 결과:
- Run 2:
  - seed:
  - scenario:
  - JSON 로그:
  - Text MUD Play Log:
  - 결과:
- Run 3:
  - seed:
  - scenario:
  - JSON 로그:
  - Text MUD Play Log:
  - 결과:

남은 문제:
- ...

다음 추천 작업:
- ...
```

---

## ulw-loop 실행 예시

문서를 추가한 뒤, 다음 명령으로 작업을 시작한다.

```bash
$ulw-loop "docs/04_codex/06_Codex_Text_MUD_Console_Simulator_Loop_Brief_v0.1.md 문서를 기준으로 Project FateWeaver의 Console Simulator를 텍스트 MUD형 게임성 검증 도구로 보강해줘. 특히 브리프의 로그 출력 구조 기준을 반드시 지켜라. 기존 JSON 로그 저장 구조는 자동 검증/회귀 테스트/seed 비교/추후 Flutter 연동용으로 유지하고, 사람이 읽을 수 있는 Text MUD Play Log 출력 레이어를 추가해라. stdout이 LOG: 기술 로그만 남는 상태는 완료로 보지 않는다. 최소 3개 이상의 seed/run을 실행해 JSON 로그와 Text MUD Play Log가 모두 생성되는지 확인하고, 각 run에서 서로 다른 사건 흐름, 선택 결과, 상태 변화, 아이템/단서/징조 영향, 생존 또는 실패 결과가 드러나는지 검증해라. Flutter UI, Flame 렌더링, PRD 대량 작성, World Bible 대량 작성, 기존 구조 대규모 변경은 금지한다." --strategy=continue --completion-promise="기존 JSON 로그 저장 구조를 유지하면서 사람이 읽을 수 있는 Text MUD Play Log 출력이 추가되고, 최소 3개 seed/run에서 JSON 로그와 Text MUD 로그가 모두 확인되며, 각 로그에 사건, 선택, 위험/보상 판단, 상태 변화, 아이템/단서/징조 영향, 생존 또는 실패 결과가 드러난다."
```
