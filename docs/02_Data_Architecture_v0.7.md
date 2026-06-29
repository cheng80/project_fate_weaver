# Project FateWeaver Data Architecture v0.7

## 문서 목적

이 문서는 Project FateWeaver의 장기 데이터 구조와 코드 영역 역할을 정의한다.

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

# 7. 시나리오 파일 예시

```yaml
id: mvp0_console_test
name: MVP-0 Console Loop Validation

content_sources:
  - data/content/base/regions.yaml
  - data/content/base/items.yaml
  - data/content/base/events.yaml
  - data/content/base/endings.yaml

include_regions:
  - forest
  - village
  - ruin

include_event_ids:
  - cursed_well
  - broken_bridge

initial_status:
  health: 7
  food: 5
  money: 2
  reputation: 0
  curse: 1

initial_items:
  - rope
  - torch
```

---

# 8. Validator 기준

Validator는 다음 순서로 검사한다.

```text
1. core 로드
2. content source 로드
3. scenario 로드
4. scenario가 참조하는 content source 존재 여부 검사
5. event id 존재 여부 검사
6. item id 존재 여부 검사
7. tag/status/choice enum 검사
8. scenario 기준 이벤트 개수 검사
```

---

# 9. 금지

아래 구조는 금지한다.

```text
data/mvp0/
data/test_content_as_real_content/
data/temp_events.yaml
```

테스트는 scenario로 관리한다.

콘텐츠는 content로 관리한다.


---

# v0.7 보강 사항

- core tag enum과 실제 이벤트 데이터 충돌을 수정한다.
- Python YAML 처리를 위해 requirements.txt를 사용한다.
- Flutter 이전 경로는 `docs/08_Flutter_Data_Export_Contract_v0.1.md`를 따른다.
- `regret_score`와 `player_woven_score`의 위치를 분리한다.
