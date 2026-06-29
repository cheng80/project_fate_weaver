# Project FateWeaver Current Baseline v0.7

## 문서 목적

이 문서는 Project FateWeaver의 현재 기준선을 정리한다.

v0.7의 핵심은 **프로젝트 최상위 구조를 명확히 고정**하는 것이다.

---

# 1. 프로젝트 정체성

Project FateWeaver의 장르는 다음으로 유지한다.

> **이벤트 중심 판타지 로그라이크**

자동 완성형 시스템은 장르가 아니라 **콘텐츠 제작/확장 파이프라인**이다.

---

# 2. 현재 단계

현재는 PRD 단계가 아니다.

현재는 Flutter 앱 제작 단계도 아니다.

현재 목표는:

```text
MVP-0 Console Loop Validation
```

이다.

즉, Python 콘솔 환경에서 이벤트-선택-상태 변화 루프가 재미있는지 검증한다.

---

# 3. 최상위 프로젝트 구조

```text
project_fate_weaver/
  docs/
  data/
  src/
  tools/
  logs/
  archive/

  fate_weaver/
```

단, `fate_weaver/`는 MVP-0 단계에서는 생성하지 않는다.  
MVP-0 검증 통과 후 MVP-1 단계에서 생성한다.

---

# 4. 폴더 역할

## docs/

프로젝트 기준 문서다.

역할:

- 프로젝트 방향 고정
- 구조 기준 정의
- Codex 작업 지시 기준
- Office Hour 검증 기준
- PRD 이전 판단 기준
- 문서 변경 이력의 기준점

---

## data/

YAML 원천 데이터다.

역할:

- 게임 규칙 데이터
- 이벤트 콘텐츠
- 아이템 콘텐츠
- 테스트 시나리오
- 향후 콘텐츠팩 확장

---

## src/

Python MVP-0 검증 엔진이다.

역할:

- 이벤트 선택
- 선택지 처리
- 상태 변화 계산
- 룰 엔진
- 검증 로직
- 로그 분석 로직

Flutter 앱 코드가 아니다.

---

## tools/

Python 실행 도구다.

역할:

- 데이터 검증 실행
- 콘솔 시뮬레이터 실행
- 로그 분석
- Flutter용 JSON export

---

## logs/

MVP-0 테스트 결과 저장소다.

---

## archive/

이전 문서와 폐기된 구조를 보관한다.

---

## fate_weaver/

나중에 생성할 Flutter + Flame 앱 프로젝트다.

MVP-0 단계에서는 생성하지 않는다.

---

# 5. 현재 금지 사항

MVP-0 단계에서 금지한다.

```text
Flutter 프로젝트 생성
Flame 컴포넌트 구현
fate_weaver/ 폴더 생성
Dart 앱 코드 작성
이벤트별 if문 하드코딩
data/mvp0/ 폴더 생성
```

---

# 6. 현재 목표

현재 목표는 Codex가 아래를 만들 수 있는 상태로 문서를 정리하는 것이다.

```text
Python 콘솔 시뮬레이터
YAML validator
Event selector
Choice resolver
Run logger
Log analyzer
```

한 줄 요약:

> **지금은 게임 앱을 만드는 단계가 아니라, 게임 루프가 재미있는지 검증하는 Python 실험 엔진을 만드는 단계다.**


---

# v0.7 보강 사항

- core tag enum과 실제 이벤트 데이터 충돌을 수정한다.
- Python YAML 처리를 위해 requirements.txt를 사용한다.
- Flutter 이전 경로는 `docs/08_Flutter_Data_Export_Contract_v0.1.md`를 따른다.
- `regret_score`와 `player_woven_score`의 위치를 분리한다.
