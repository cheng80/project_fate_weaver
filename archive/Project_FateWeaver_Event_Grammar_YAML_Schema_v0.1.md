# Project FateWeaver Event Grammar + YAML Schema v0.1

## 문서 목적

이 문서는 이벤트 콘텐츠를 작성하기 위한 최소 문법과 YAML 구조를 정의한다.

Codex가 이벤트를 생성할 때도 이 문서를 기준으로 삼는다.

---

# 1. 이벤트 기본 구조

이벤트는 다음 요소를 가진다.

```yaml
id: abandoned_well
name: 버려진 우물
description: 오래된 우물이 숲길 옆에 버려져 있다. 물은 검게 고여 있고, 아래에서는 희미한 속삭임이 들린다.

region_tags:
  - forest

event_tags:
  - exploration
  - well

danger_tags:
  - darkness
  - curse

base_weight: 10

choices:
  - id: ignore
    text: 지나간다
    result:
      food: -1
```

---

# 2. 필수 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| id | 예 | 고유 ID |
| name | 예 | 표시 이름 |
| description | 예 | 이벤트 설명 |
| region_tags | 예 | 등장 가능 지역 |
| event_tags | 예 | 이벤트 성격 |
| danger_tags | 아니오 | 위험 태그 |
| base_weight | 예 | 기본 등장 가중치 |
| choices | 예 | 선택지 목록 |

---

# 3. 선택지 구조

```yaml
choices:
  - id: drink
    text: 물을 마신다
    risk_level: medium
    cost:
      none: true
    result_pool:
      - condition: curse_low
        result:
          health: +1
      - condition: default
        result:
          curse: +1
```

---

# 4. 선택지 필수 조건

이벤트 하나는 최소 조건을 만족해야 한다.

- 선택지 3개 이상
- 최소 1개 안전 선택지
- 최소 1개 위험 보상 선택지
- 최소 1개 조건부 선택지 또는 아이템 상호작용
- 최소 1개 결과가 다음 이벤트나 상태에 영향

---

# 5. 선택지 유형

| 유형 | 설명 |
|---|---|
| safe | 안전하지만 보상 낮음 |
| risky | 위험하지만 보상 큼 |
| item_based | 아이템 요구 |
| status_based | 상태 요구 |
| sacrifice | 현재 자원 희생 |
| gamble | 결과 풀 기반 |
| retreat | 후퇴/회피 |
| corrupt | 저주 관련 선택 |

---

# 6. Result 구조

Result는 다음을 바꿀 수 있다.

```yaml
result:
  health: -1
  food: +1
  money: +2
  reputation: -1
  curse: +1
  add_item:
    - herb
  remove_item:
    - holy_water
  event_weight:
    undead: +2
    trade: -1
  add_tag:
    - helped_child
```

---

# 7. Result 원칙

좋은 결과는 즉시 수치 변화로 끝나지 않는다.

가능하면 다음 중 하나를 포함한다.

- 상태 변화
- 아이템 변화
- 이벤트 가중치 변화
- 태그 추가
- 미래 선택지 변화
- 엔딩 조건 변화

---

# 8. 아이템 조건

```yaml
requires_item: rope
consume_item: true
```

또는:

```yaml
requires_any_item:
  - rope
  - hook

consume_item: false
```

---

# 9. 상태 조건

```yaml
requires_status:
  money:
    min: 2
```

또는:

```yaml
condition:
  curse:
    min: 3
```

---

# 10. 전투형 이벤트

전투형 이벤트도 일반 이벤트 문법을 사용한다.

```yaml
event_tags:
  - combat
  - ambush

danger_tags:
  - physical
  - group_enemy
```

전투형 이벤트는 반드시 아래를 포함해야 한다.

- 회피 또는 협상 선택지
- 대응 아이템 선택지
- 손실 가능성
- 후유증 또는 미래 영향

---

# 11. Codex 생성 이벤트 Reject 기준

Codex가 만든 이벤트는 아래 조건이면 거절한다.

- 선택지 3개 미만
- 대가 없는 보상 선택지 2개 이상
- 모든 선택지가 같은 상태만 변경
- 아이템 또는 상태 조건이 전혀 없음
- 미래 영향이 없음
- 이벤트 태그와 결과가 불일치
- 전투형 이벤트가 단순 수치 교환으로만 구성
- 설명만 길고 게임적 차이가 없음

---

# 12. 좋은 이벤트 예시

```yaml
id: cursed_well
name: 저주받은 우물
description: 검은 물이 고인 우물에서 낮은 속삭임이 들린다.

region_tags:
  - forest
  - ruin

event_tags:
  - exploration
  - well

danger_tags:
  - curse
  - darkness

base_weight: 10

choices:
  - id: pass
    text: 그냥 지나간다
    type: safe
    result:
      food: -1

  - id: drink
    text: 물을 마신다
    type: gamble
    result_pool:
      - condition: curse_low
        result:
          health: +1
          curse: +1
      - condition: default
        result:
          curse: +2

  - id: purify
    text: 성수로 정화한다
    type: item_based
    requires_item: holy_water
    consume_item: true
    result:
      curse: -1
      reputation: +1
      event_weight:
        holy: +1

  - id: climb_down
    text: 밧줄로 내려간다
    type: item_based
    requires_item: rope
    result:
      money: +3
      health: -1
      event_weight:
        ancient: +1
```
