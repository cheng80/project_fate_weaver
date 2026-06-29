# Project FateWeaver Commit Summary v0.1

## 문서 목적

이 문서는 이번 커밋에서 정리한 Project FateWeaver의 현재 상태를 한국어로 요약한다.

이번 커밋의 목적은 Flutter 앱 구현이 아니라, **Console Validation 프로토타입 제작 직전의 기준선**을 저장하는 것이다.

---

# 1. 커밋 요약

이번 변경은 Project FateWeaver를 PRD 이전 검증 패키지 형태로 재정리한다.

핵심 방향은 다음과 같다.

```text
지금 만들 것은 Flutter 앱이 아니라 Python 콘솔 검증 엔진이다.
YAML 데이터가 원천이고, Python은 루프 검증용 도구다.
Flutter 프로젝트는 Console Validation 통과 후 fate_weaver/에 별도로 생성한다.
```

---

# 2. 구조 정리

최상위 구조를 아래 기준으로 고정했다.

```text
docs/      설계, 검증, Codex 작업 기준 문서
data/      YAML 원천 데이터
src/       Python Console Validation 검증 엔진 영역
tools/     Python 실행 도구 영역
logs/      콘솔 검증 로그 영역
archive/   이전 문서와 폐기 문서 보관
```

`fate_weaver/`는 아직 만들지 않는다.

---

# 3. 문서 패키지

`docs/`에는 Console Validation을 시작하기 위한 기준 문서를 둔다.

주요 문서는 다음 역할을 가진다.

- 현재 기준선 정의
- 프로젝트 구조 가이드
- 데이터 아키텍처 정의
- YAML 이벤트 문법 초안
- 콘솔 시뮬레이터 스펙
- Codex 구현 브리프
- fixture 데이터 계획
- Console Validation 체크리스트
- Flutter 데이터 export 계약

---

# 4. 데이터 패키지

`data/`는 세 계층으로 나눈다.

```text
data/core/       전역 enum, status, rule 정의
data/content/    실제 게임 콘텐츠
data/scenarios/  검증용 실행 범위와 초기 조건
```

테스트 전용 콘텐츠 폴더인 `data/mvp0/`는 만들지 않는다.

Console Validation은 `data/scenarios/mvp0_console_test.yaml` 시나리오로 관리한다.

---

# 5. Python 실행 환경

Console Validation 제작과 검증은 프로젝트 루트의 `.venv`를 기준으로 실행한다.

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

YAML 처리는 `PyYAML`만 사용한다.

---

# 6. Codex 작업 기준

Codex는 다음 범위 안에서만 Console Validation 프로토타입을 만든다.

```text
src/fateweaver/
tools/
logs/
data/
docs/
README.md
```

금지 사항은 다음과 같다.

```text
Flutter 프로젝트 생성 금지
fate_weaver/ 생성 금지
Dart 코드 작성 금지
Flame 코드 작성 금지
PRD 작성 금지
이벤트별 if문 하드코딩 금지
```

---

# 7. 현재 검증 결과

현재 기준선에서 확인한 내용은 다음과 같다.

```text
Python: 3.12.10
PyYAML: 6.0.3
YAML 파싱: schema_errors=none
문서 참조: missing 없음
오래된 실행 명령: 없음
```

---

# 8. 다음 작업

다음 커밋의 목적은 문서 작성이 아니라 Console Validation 프로토타입 구현이다.

구현 대상은 다음이다.

- `tools/validate_data.py`
- `tools/console_simulator.py`
- `tools/analyze_logs.py`
- `src/fateweaver/` 내부 검증 엔진

최종 목표는 시나리오 기반으로 이벤트를 불러오고, 선택지를 처리하고, 상태 변화를 로그로 남기는 것이다.
