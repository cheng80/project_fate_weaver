# Project FateWeaver Data Architecture v0.5

## 문서 목적

이 문서는 Project FateWeaver의 장기 데이터 구조와 코드 영역 역할을 정의한다.

v0.5에서는 Python 검증 영역과 Flutter 앱 프로젝트 영역을 명확히 분리한다.

---

# 1. 핵심 결론

`mvp0/`는 콘텐츠 폴더가 아니다.

MVP-0는 `data/scenarios/mvp0_console_test.yaml`이라는 **시나리오 파일**로 관리한다.

또한 `src/`는 Flutter 프로젝트가 아니다.

`src/`는 Python MVP-0 검증 엔진이다.

Flutter 앱은 이후 별도 `fate_weaver/` 폴더로 생성한다.

---

# 2. 데이터 구조

```text
data/
  core/
  content/
    base/
    packs/
  scenarios/
```

---

# 3. data/core

게임 전체의 불변 규칙과 enum을 관리한다.

```text
data/core/
  statuses.yaml
  tags.yaml
  choice_types.yaml
  item_roles.yaml
  result_rules.yaml
```

---

# 4. data/content/base

기본 게임 콘텐츠를 관리한다.

```text
data/content/base/
  regions.yaml
  items.yaml
  events.yaml
  endings.yaml
```

여기는 테스트용이 아니라 실제 게임의 기본 콘텐츠다.

---

# 5. data/content/packs

업데이트나 확장 콘텐츠를 팩 단위로 관리한다.

```text
data/content/packs/
  forest_pack/
    events.yaml
    items.yaml

  curse_pack/
    events.yaml
    items.yaml
```

---

# 6. data/scenarios

테스트, 밸런스, 실험에 사용할 콘텐츠 범위를 지정한다.

```text
data/scenarios/
  mvp0_console_test.yaml
  curse_balance_test.yaml
  item_influence_test.yaml
```

시나리오는 콘텐츠를 직접 담지 않는다.

시나리오는 어떤 데이터를 사용할지 지정한다.

---

# 7. src/ 역할

`src/`는 Python 패키지 영역이다.

Flutter의 `lib/`와 같은 역할이 아니다.

```text
src/
  fateweaver/
    models.py
    event_engine.py
    event_selector.py
    choice_resolver.py
    state_manager.py
    inventory_manager.py
    validator.py
    logger.py
    analyzer.py
```

목적:

```text
MVP-0 콘솔 검증용 룰 엔진
```

---

# 8. tools/ 역할

`tools/`는 실행 스크립트 영역이다.

```text
tools/
  validate_data.py
  console_simulator.py
  analyze_logs.py
  export_json.py
```

`tools/`는 `src/fateweaver/`의 로직을 호출한다.

---

# 9. fate_weaver/ 역할

`fate_weaver/`는 Flutter + Flame 앱 프로젝트 폴더다.

MVP-0에서는 만들지 않는다.

MVP-1에서 생성한다.

```text
fate_weaver/
  pubspec.yaml
  lib/
  assets/
    data/
  test/
```

---

# 10. 경계 규칙

## MVP-0에서 허용

```text
src/fateweaver/ Python 코드
tools/ Python 스크립트
data/ YAML
logs/ 테스트 로그
```

## MVP-0에서 금지

```text
fate_weaver/ 생성
Flutter 코드 작성
Flame 코드 작성
Dart 앱 코드 작성
```

---

# 11. 향후 데이터 export

MVP-1 단계에서 Flutter로 갈 때는 다음 흐름을 사용한다.

```text
data/core + data/content + data/scenarios
↓
tools/export_json.py
↓
fate_weaver/assets/data/
```

Flutter 앱은 YAML을 직접 수정하지 않는다.

YAML은 계속 Single Source of Truth로 유지한다.
