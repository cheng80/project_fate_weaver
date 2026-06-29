# Project FateWeaver Flutter Data Export Contract v0.1

## 문서 목적

이 문서는 YAML 원천 데이터가 이후 Flutter + Flame 앱 프로젝트인 `fate_weaver/`로 이동하는 방식을 정의한다.

현재 Console Validation 단계에서는 Flutter 프로젝트를 만들지 않는다.

그러나 데이터 구조는 향후 Flutter 이전을 해치지 않아야 한다.

---

# 1. 기본 원칙

```text
YAML = Single Source of Truth
JSON = generated artifact
Flutter = generated JSON만 읽음
```

Flutter 앱은 YAML을 직접 수정하지 않는다.

---

# 2. 데이터 흐름

```text
data/core/*.yaml
data/content/**/*.yaml
data/scenarios/*.yaml
        ↓
tools/export_json.py
        ↓
fate_weaver/assets/data/*.json
        ↓
Flutter Runtime
```

---

# 3. export_json.py 역할

`tools/export_json.py`는 다음을 수행한다.

1. core 데이터 로드
2. content source 로드
3. scenario 로드
4. validator 통과 여부 확인
5. Flutter용 JSON 생성
6. schema_version 포함
7. generated_at 포함
8. source hash 또는 source list 포함

---

# 4. 생성 파일 위치

Flutter 앱 단계 이후 예상 위치:

```text
fate_weaver/
  assets/
    data/
      manifest.json
      core.json
      items.json
      events.json
      regions.json
      endings.json
      scenarios.json
```

---

# 5. manifest.json

```json
{
  "schema_version": "0.1.0",
  "generated_at": "2026-01-01T00:00:00Z",
  "source": {
    "core": [
      "data/core/statuses.yaml",
      "data/core/tags.yaml"
    ],
    "content": [
      "data/content/base/events.yaml"
    ],
    "scenarios": [
      "data/scenarios/mvp0_console_test.yaml"
    ]
  },
  "files": {
    "core": "core.json",
    "events": "events.json",
    "items": "items.json",
    "regions": "regions.json",
    "endings": "endings.json",
    "scenarios": "scenarios.json"
  }
}
```

---

# 6. ID 안정성 규칙

아래 ID는 한 번 출시되면 변경하지 않는다.

- event.id
- item.id
- region.id
- ending.id
- scenario.id
- status key
- tag value

ID를 변경해야 할 경우 migration map을 둔다.

```json
{
  "migrations": {
    "old_event_id": "new_event_id"
  }
}
```

---

# 7. generated artifact 정책

`fate_weaver/assets/data/*.json`은 생성물이다.

직접 수정하지 않는다.

수정은 반드시 YAML에서 한다.

금지:

```text
Flutter assets JSON 직접 수정
YAML과 JSON 동시 수동 관리
앱 코드 안에 이벤트 하드코딩
```

---

# 8. Flutter pubspec 예상 등록

Flutter 앱 단계에서 Flutter 프로젝트가 생성되면 아래처럼 등록한다.

```yaml
flutter:
  assets:
    - assets/data/manifest.json
    - assets/data/core.json
    - assets/data/events.json
    - assets/data/items.json
    - assets/data/regions.json
    - assets/data/endings.json
    - assets/data/scenarios.json
```

---

# 9. Console Validation 단계에서의 금지

Console Validation에서는 아래를 하지 않는다.

```text
fate_weaver/ 생성
assets/data 생성
Flutter pubspec 수정
Dart 모델 작성
```

Console Validation은 Python 콘솔 검증만 수행한다.
