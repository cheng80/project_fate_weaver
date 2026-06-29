# Project FateWeaver Fixture Data Plan v0.3

## 문서 목적

이 문서는 Console Validation 시뮬레이터 제작을 시작하기 위한 최소 fixture 데이터 기준을 정의한다.

v0.3에서는 fixture 데이터를 `data/mvp0`에 두지 않고 실제 콘텐츠 구조에 배치한다.

---

# 1. Fixture 구조

```text
data/
  core/
  content/
    base/
    packs/
      forest_pack/
      curse_pack/
  scenarios/
    mvp0_console_test.yaml
```

---

# 2. Scenario 방식

Console Validation은 별도 폴더가 아니라 시나리오로 관리한다.

```text
data/scenarios/mvp0_console_test.yaml
```

이 파일이 다음을 지정한다.

- 사용할 content source
- 포함할 region
- 포함할 event id
- 초기 상태
- 초기 아이템
- 목표 턴 수
- seed

---

# 3. Fixture 통과 기준

- core/statuses.yaml 존재
- core/tags.yaml 존재
- content/base/items.yaml 존재
- content/base/events.yaml 존재
- scenarios/mvp0_console_test.yaml 존재
- scenario 기준 이벤트 12개 이상
- scenario 기준 저주 이벤트 4개 이상
- scenario 기준 전투형 이벤트 2개 이상
- 각 필수 아이템은 2개 이상 이벤트와 연결
