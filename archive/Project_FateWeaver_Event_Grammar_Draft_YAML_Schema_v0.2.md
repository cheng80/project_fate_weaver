# Project FateWeaver Event Grammar Draft YAML Schema v0.2

## 문서 목적

이 문서는 MVP-0 실험을 위한 Draft YAML Schema다.

최종 Production Schema가 아니다.

목표는 Codex가 이벤트를 일관되게 생성하고, Python validator가 기본 오류를 검출할 수 있게 하는 것이다.

---

# 1. Schema 상태

| 항목 | 값 |
|---|---|
| 이름 | Event Grammar Draft YAML Schema |
| 버전 | v0.2 |
| 단계 | MVP-0 Draft |
| 목적 | 콘솔 검증용 이벤트 문법 |
| Production 사용 | 금지 |
| Validator 대상 | 예 |

---

# 2. 공통 Enum

## 2.1 status_key

허용 상태 키:

```yaml
status_key:
  - health
  - food
  - money
  - reputation
  - curse
```

---

## 2.2 choice_type

허용 선택지 타입:

```yaml
choice_type:
  - safe
  - risky
  - item_based
  - status_based
  - sacrifice
  - gamble
  - retreat
  - corrupt
  - trade
  - combat_response
  - investigate
  - rest
```

---

## 2.3 risk_level

```yaml
risk_level:
  - none
  - low
  - medium
  - high
  - extreme
```

---

## 2.4 result_mode

선택지는 `result` 또는 `result_pool` 중 하나만 사용할 수 있다.

```yaml
allowed:
  - result
  - result_pool

exclusive: true
```

---

# 3. 상태 범위

| 상태 | 타입 | 최소 | 최대 |
|---|---|---:|---:|
| health | int | 0 | 10 |
| food | int | 0 | 10 |
| money | int | 0 | 99 |
| reputation | int | -5 | 5 |
| curse | int | 0 | 5 |

Validator는 결과 적용 후 범위를 clamp하거나 오류를 보고할 수 있다.

MVP-0에서는 clamp 허용, MVP-1에서는 명시 규칙 필요.

---

# 4. Event Schema

## 4.1 필수 필드

```yaml
id: string
name: string
description: string
region_tags: list[string]
event_tags: list[string]
base_weight: int
choices: list[Choice]
```

---

## 4.2 선택 필드

```yaml
danger_tags: list[string]
requires_status: StatusCondition
requires_item: string
variation_rules: list[VariationRule]
cooldown_turns: int
max_occurrences_per_run: int
```

---

## 4.3 base_weight 범위

```yaml
base_weight:
  type: int
  min: 1
  max: 100
```

권장:

| 이벤트 성격 | 권장 weight |
|---|---:|
| 일반 이벤트 | 8~15 |
| 희귀 이벤트 | 1~5 |
| 휴식 이벤트 | 5~10 |
| 위험 이벤트 | 5~12 |
| 저주 이벤트 | 저주 상태에 따라 가변 |

---

# 5. Choice Schema

## 5.1 필수 필드

```yaml
id: string
text: string
type: choice_type
risk_level: risk_level
```

---

## 5.2 결과 필드

아래 둘 중 하나만 사용한다.

```yaml
result: Result
```

또는:

```yaml
result_pool: list[ConditionalResult]
```

동시 사용 금지.

---

## 5.3 조건 필드

```yaml
requires_item: string
requires_any_item: list[string]
consume_item: bool
requires_status: StatusCondition
requires_tag: string
hidden_until_available: bool
```

---

# 6. Condition Grammar

## 6.1 상태 조건

```yaml
requires_status:
  money:
    min: 2
  curse:
    max: 3
```

허용 연산:

```yaml
min
max
equals
not_equals
```

---

## 6.2 condition 이름 금지

아래처럼 정의 없는 문자열 condition은 금지한다.

```yaml
condition: curse_low
```

대신 명시 조건을 사용한다.

```yaml
condition:
  curse:
    max: 1
```

---

# 7. Result Schema

## 7.1 상태 변화

```yaml
result:
  status:
    health: -1
    money: +3
    curse: +1
```

상태 변화는 반드시 `status` 아래에 둔다.

금지:

```yaml
result:
  health: -1
```

---

## 7.2 아이템 변화

```yaml
result:
  add_item:
    - herb
  remove_item:
    - holy_water
```

---

## 7.3 이벤트 가중치 변화

```yaml
result:
  event_weight:
    undead: +2
    trade: -1
```

`event_weight`는 tag 기반으로 적용한다.

---

## 7.4 태그 변화

```yaml
result:
  add_run_tag:
    - helped_child
  remove_run_tag:
    - wanted
```

---

## 7.5 결과 문장

```yaml
result:
  message: "당신은 우물 아래에서 오래된 은화를 발견했다."
```

MVP-0에서는 기본 문장을 사용한다.

LLM 윤문은 사용하지 않는다.

---

# 8. Result Pool

`result_pool`은 조건부 결과 목록이다.

```yaml
result_pool:
  - when:
      curse:
        max: 1
    result:
      status:
        health: +1
        curse: +1

  - when:
      default: true
    result:
      status:
        curse: +2
```

규칙:

1. 위에서 아래 순서로 평가한다.
2. 첫 번째로 매칭되는 결과를 적용한다.
3. `default: true`는 마지막에만 허용한다.
4. `result_pool`과 `result`는 동시에 사용할 수 없다.

---

# 9. Variation Rules

반복 이벤트 피로를 줄이기 위해 이벤트는 선택적으로 `variation_rules`를 가진다.

```yaml
variation_rules:
  - when:
      curse:
        min: 3
    override_description: "우물 속 속삭임이 이제는 당신의 이름을 부른다."
    add_choice:
      id: listen_to_whisper
      text: 속삭임에 귀를 기울인다
      type: corrupt
      risk_level: high
      result:
        status:
          curse: +1
          money: +5

  - when:
      has_item: holy_water
    reveal_hint: "성수로 정화할 수 있을 것 같다."
```

Variation Rule은 다음을 할 수 있다.

- description 변경
- choice 추가
- hint 표시
- risk_level 변경
- base_weight 보정

MVP-0에서는 최소 3개 이벤트에 variation_rules를 포함한다.

---

# 10. Event Quality Rules for Validator

Validator는 아래를 검사한다.

## 10.1 Hard Error

- id 없음
- name 없음
- description 없음
- choices 3개 미만
- base_weight 범위 초과
- 존재하지 않는 status_key 사용
- 존재하지 않는 choice_type 사용
- result와 result_pool 동시 사용
- condition 문자열 shortcut 사용
- 존재하지 않는 tag 참조
- combat 이벤트에 combat 대응 선택지 없음

---

## 10.2 Warning

- 조건부 선택지 없음
- 미래 영향 없음
- 모든 선택지가 같은 status만 변경
- safe 선택지 없음
- risky 선택지 없음
- item_based 선택지 없음
- description 30자 미만
- result message 없음
- variation_rules 없음

---

# 11. 전투형 이벤트 규칙

전투형 이벤트는 다음 태그를 가진다.

```yaml
event_tags:
  - combat
```

전투형 이벤트는 아래 중 최소 2개 선택지 유형을 가져야 한다.

```yaml
combat_response
retreat
trade
item_based
status_based
```

또한 최소 1개 결과는 후유증 또는 미래 영향이 있어야 한다.

예:

```yaml
result:
  status:
    health: -1
  add_run_tag:
    - wounded
  event_weight:
    bandit: +1
```

---

# 12. 저주 이벤트 규칙

저주 관련 이벤트는 아래 중 하나를 포함해야 한다.

- curse 증가
- curse 감소
- curse에 따라 선택지 변화
- curse에 따라 result_pool 변화
- curse에 따라 event_weight 변화
- curse가 높을 때 위험하지만 큰 보상

금지:

```text
저주 +1만 주고 끝나는 이벤트
```

---

# 13. 예시 이벤트

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
max_occurrences_per_run: 2

choices:
  - id: pass
    text: 그냥 지나간다
    type: safe
    risk_level: none
    result:
      status:
        food: -1
      message: "당신은 우물을 지나쳤지만, 먼 길을 돌아가며 식량을 조금 소모했다."

  - id: drink
    text: 물을 마신다
    type: gamble
    risk_level: high
    result_pool:
      - when:
          curse:
            max: 1
        result:
          status:
            health: +1
            curse: +1
          message: "물은 차갑고 달콤했지만, 뒤늦게 손끝이 검게 물들었다."
      - when:
          default: true
        result:
          status:
            curse: +2
          message: "우물의 물은 이미 당신 안의 저주에 반응했다."

  - id: purify
    text: 성수로 정화한다
    type: item_based
    risk_level: low
    requires_item: holy_water
    consume_item: true
    result:
      status:
        curse: -1
        reputation: +1
      remove_item:
        - holy_water
      event_weight:
        holy: +1
      message: "성수가 검은 물결을 잠재웠고, 그 소문은 곧 마을까지 퍼질 것이다."

variation_rules:
  - when:
      curse:
        min: 3
    override_description: "검은 물이 고인 우물에서 이제는 당신의 이름이 들려온다."
```
