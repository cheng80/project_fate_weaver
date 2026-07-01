# [Current] Codex P1 Post-Playtest Critical Fixes Brief v0.1

> 상태: [Current] 중단된 Human Playtest Run 1에서 발견된 critical findings를 후속 구현 작업으로 분리하기 위한 brief.

## 1. 문서 목적

이 문서는 Turn 18에서 중단된 P1 Human Playtest Run 1의 문제를 바로 구현하지 않고, 다음 작업 단위로 분리한다.

Run 1은 completion evidence가 아니다. Run 1은 critical findings evidence다.

## 2. Critical Findings 요약

| Finding | 우선순위 | 요약 |
|---|---|---|
| Facilitator Runner 부재 | P0 | 사용자 `1/2/3` 선택이 실제 state transition을 구동하지 못했다. |
| Quest Intro / Onboarding 부재 | P0 | 플레이 시작 시 의뢰자와 목적이 충분히 고지되지 않았다. |
| Completed Objective Stale Choices | P0 | 보고/해결 후에도 의뢰 확인, 보고, 반복 탐색 선택지가 남았다. |
| Storylet Relevance / Merchant Noise | P1 | 현재 목표와 무관한 merchant family가 반복 noise로 읽혔다. |

## 3. Task 1. Manual Choice-Driven Standard Run Runner

Task brief:

```text
CODEX_TASK_Manual_Choice_Driven_Standard_Run_Runner_v0.1.md
```

목표:

- 매 turn 사용자의 `1/2/3` 선택 index를 실제 selected card로 적용한다.
- 선택 결과를 `apply_turn_result` 또는 equivalent state transition에 반영한다.
- 다음 event/card selection이 사용자 선택 이후 state를 기반으로 진행된다.
- facilitator mode에서 hidden score나 ending 조건은 노출하지 않는다.
- JSON evidence에 user-selected card가 명확히 기록된다.

Scope guard:

- random seed determinism 변경 금지.
- quest_ids / requirements / cooldown / max occurrence / min_turn gate 우회 금지.
- Text MUD polish, balance tuning, storylet addition 금지.

Acceptance gate:

- 사용자 선택 `1`, `2`, `3`이 각각 selected card로 기록되는 최소 smoke evidence.
- state/resource/objective 변화가 선택 card 기준으로 적용되는 evidence.
- 다음 turn 후보가 변경된 state를 사용한다는 evidence.

## 4. Task 2. Quest Intro / Onboarding Gate

Task brief:

```text
CODEX_TASK_Quest_Intro_Onboarding_Gate_v0.1.md
```

목표:

- Run 시작 시 active quest의 의뢰자, 목적, 현재 목표를 spoiler 없이 표시한다.
- hidden score, ending condition, 최적 선택은 노출하지 않는다.
- Text MUD와 facilitator mode에서 같은 quest intro 정보를 확인할 수 있다.

Scope guard:

- Quest/Card/Event/Item/Ending 추가 금지.
- balance/scoring/selection/director/ontology 변경 금지.
- 문구 추가는 onboarding surface에만 제한한다.

Acceptance gate:

- seed 202 Run 시작 전에 의뢰자와 목적이 표시된다.
- 플레이어가 약사/약초/보고 선택의 맥락을 알 수 있다.
- ending 조건은 노출되지 않는다.

## 5. Task 3. Completed Objective Stale Choice Gate Audit

Task brief:

```text
CODEX_TASK_Completed_Objective_Stale_Choice_Gate_Audit_v0.1.md
```

목표:

- completed objective 이후에도 남는 card candidate를 turn-level evidence로 파악한다.
- report/confirm/gather/progress 계열 stale card를 분류한다.
- gate, penalty, suppression 후보를 제안한다.

Scope guard:

- 특정 card id만 하드코딩해 숨기지 않는다.
- quest_ids / requirements / cooldown hard block을 우회하지 않는다.
- 구현 전 audit evidence를 먼저 작성한다.

Acceptance gate:

- 보고 완료 이후 stale card 목록과 발생 turn이 문서화된다.
- general rule 후보가 특정 id workaround보다 우선 제안된다.
- Run 1 retry 전에 필요한 최소 gate가 명확해진다.

## 6. Task 4. Storylet Relevance / Merchant Noise Audit

Task brief:

```text
CODEX_TASK_Storylet_Relevance_Merchant_Noise_Audit_v0.1.md
```

목표:

- suspicious merchant / merchant social / trade gossip family의 등장 조건과 반복을 분석한다.
- current quest state, completed objective, next_event_tags와 무관한 반복인지 확인한다.
- repeat_group / relevance / current objective 기반 개선 후보를 제안한다.

Scope guard:

- suspicious_merchant 직접 disable 금지.
- 특정 event id 하드코딩 penalty 금지.
- Storylet/Event 대량 추가 금지.
- Director 구조 변경 전 audit evidence 우선.

Acceptance gate:

- merchant family 반복 turn과 현재 objective state가 함께 기록된다.
- noise와 useful follow-up을 구분한다.
- general relevance rule 후보가 제안된다.

## 7. Recommended Order

권장 순서:

1. Manual Choice-Driven Standard Run Runner
2. Quest Intro / Onboarding Gate
3. Completed Objective Stale Choice Gate Audit
4. Storylet Relevance / Merchant Noise Audit
5. Human Playtest Run 1 Retry

이유:

- runner가 없으면 interactive evidence가 계속 깨진다.
- onboarding이 없으면 플레이어는 목적을 이해하지 못한다.
- stale choice와 merchant noise는 runner/onboarding 이후에도 남을 가능성이 높다.
- Run 1 retry는 위 조건을 만족한 뒤에만 의미가 있다.

## 8. Run 1 Retry Gate

Run 1을 다시 시작하기 전에 아래 조건을 모두 만족해야 한다.

- 사용자 `1/2/3` 선택이 실제 state transition에 반영되는 runner가 있다.
- Run 시작 시 quest intro/onboarding이 표시된다.
- completed objective 이후 stale choice audit 또는 최소 gate가 완료됐다.
- Codex Facilitated Human Playtest Protocol v0.3을 사용한다.
- seed 202 baseline이 다시 검증된다.

Retry 전 필수 확인:

- 3-card every turn.
- user-selected card가 selected card로 기록됨.
- state/resource/objective 변화가 사용자 선택 기준으로 적용됨.
- next event/card selection이 변경된 state를 기반으로 진행됨.
