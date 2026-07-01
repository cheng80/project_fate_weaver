# [Current] P1 Human Playtest Findings Audit v0.1

> 상태: [Current] Turn 18에서 중단된 P1 Human Playtest Run 1을 completion evidence가 아니라 critical findings evidence로 감사한 문서.

## 1. 작업 목적

이 문서는 P1 Human Playtest Run 1 attempt를 25턴 완료 playtest로 해석하지 않고, Turn 18에서 중단된 critical findings evidence로 분류한다.

이번 작업은 감사 문서화 작업이다. `src/`, `data/`, `tests/`, `tools/`는 수정하지 않는다.

## 2. 읽은 기준 문서

- `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`
- `docs/06_plans/13_P1_Human_Playtest_Run_1_Plan_v0.1.md`
- `docs/05_validation/20_Human_Playtest_Run_1_Player_Sheet_v0.1.md`
- `docs/05_validation/21_Codex_Facilitated_Human_Playtest_Protocol_v0.3.md`
- `docs/05_validation/18_Human_Playtest_Protocol_v0.1.md`
- `docs/05_validation/19_Human_Playtest_Feedback_Form_v0.1.md`
- `docs/07_reviews/62_P1_Human_Playtest_Run_1_Preparation_Result_v0.1.md`
- `docs/06_plans/12_P1_Human_Playtest_Scenario_Pack_v0.1.md`
- `docs/07_reviews/60_P1_Human_Playtest_Scenario_Pack_Result_v0.1.md`
- `docs/06_plans/11_P1_Planning_After_P0_Playable_v0.1.md`
- `docs/05_validation/17_P0_Playable_Milestone_Checklist_v0.1.md`

Missing at start of task:

- `docs/05_validation/21_Codex_Facilitated_Human_Playtest_Protocol_v0.3.md` was not in the repo and was added by this task.

## 3. Run 1 Status

| 항목 | 값 |
|---|---|
| Scenario | `standard_run_25_35_turn` |
| Primary seed | `202` |
| Intended mode | Codex-facilitated interactive playtest |
| Actual mode | fixed autoplayer log replay attempt |
| Stop turn | Turn 18 |
| Completion evidence | No |
| Critical findings evidence | Yes |
| Ending / Quest Report tested | No |

## 4. 중단 판정

Run 1은 중단된 playtest다. Turn 18 이후를 추정하지 않고, `prepared_frontier_route` ending이나 25턴 completion 품질을 평가하지 않는다.

중단 사유:

- 사용자 선택이 실제 state transition을 구동하지 않았다.
- Quest 목적이 시작 시 충분히 설명되지 않았다.
- 의뢰 해결 후 같은 선택지가 계속 제시됐다.
- 현재 목표와 연결되지 않는 merchant storylet이 반복 noise로 읽혔다.

## 5. Critical Finding 1: Facilitator Runner 부재

문제:

현재 Codex-facilitated interactive playtest가 실제로는 고정 seed 202 autoplayer log replay로 진행됐다. 사용자의 `1/2/3` 선택은 진행자가 설명한 결과에는 반영됐지만, 다음 turn의 event/card selection을 구동하는 state transition에는 반영되지 않았다.

Evidence:

- Run 1 Result: `진행자가 고정된 seed 202 autoplayer evidence를 재생해, 사용자의 실제 1/2/3 선택이 다음 턴 state transition을 구동하지 못했다.`
- 사용자 지적: "답변과 상관 없는 상인은 계속 등장"
- Turn 18 중단 전까지 사용자가 고른 선택과 이후 제시 card/storylet이 안정적으로 연결되지 않았다.

왜 심각한가:

- interactive playtest evidence가 깨진다.
- 사용자 선택 패턴 분석이 실제 게임 상태와 연결되지 않는다.
- 다음 turn의 event/card가 사용자 선택과 무관하게 진행된다.

후속 작업:

```text
CODEX_TASK_Manual_Choice_Driven_Standard_Run_Runner_v0.1.md
```

## 6. Critical Finding 2: Quest Onboarding 부재

문제:

플레이 시작 시 active quest의 의뢰자, 목적, 성공 목표가 충분히 고지되지 않았다.

Evidence:

```text
사용자 지적:
"의뢰가 처음에 약사에게 약초 전달인지도 고지도 안하고"
```

영향:

- 플레이어가 약초, 약사, 보고 선택의 목적을 이해하지 못한다.
- 중반 이후 카드가 갑작스럽게 느껴진다.
- Quest Purpose Continuity가 실패한다.

후속 작업:

```text
CODEX_TASK_Quest_Intro_Onboarding_Gate_v0.1.md
```

## 7. Critical Finding 3: Completed Objective 이후 Stale Choices

문제:

이미 보고/해결한 뒤에도 같은 의뢰 확인, 보고, 탐색 선택지가 계속 제시됐다.

Evidence:

- Run 1 Result Turn 16 to 18: 보고 이후에도 `약사에게 의뢰를 확인한다`, `약사에게 보고한다`, 반복 탐색 선택지가 다시 제시됐다.
- 사용자 지적: "이미 의뢰 해결 하고도 계속 같은 선택을 제시"

영향:

- 선택 의미가 무너진다.
- 해결감이 없다.
- 플레이어가 시스템이 현재 상태를 기억하지 못한다고 느낀다.

후속 작업:

```text
CODEX_TASK_Completed_Objective_Stale_Choice_Gate_Audit_v0.1.md
```

## 8. Critical Finding 4: Storylet Relevance / Merchant Noise

문제:

현재 목표와 직접 연결되지 않는 suspicious merchant / merchant social family가 반복적으로 등장했다.

Evidence:

- Run 1 Result: 사용자 선택과 관계없는 상인 storylet이 반복적으로 등장했다.
- 사용자 지적: "답변과 상관 없는 상인은 계속 등장"

영향:

- Director가 현재 목표/상태에 반응하지 않는 것처럼 보인다.
- storylet variety가 있어도 relevance가 낮으면 noise가 된다.
- 플레이어가 반복을 후속 단서가 아니라 무관한 방해로 읽는다.

후속 작업:

```text
CODEX_TASK_Storylet_Relevance_Merchant_Noise_Audit_v0.1.md
```

## 9. Secondary Finding: Resource Choice는 선택됐으나 stateful 검증 필요

Run 1 attempt에서 resource_alternative 선택은 발생했다.

Observed attempt:

- resource_alternative 선택 turn: 6, 11, 17
- 선택 자체는 플레이어가 고를 수 있었다.

하지만 fixed autoplayer replay 때문에 이 선택들이 실제 stateful run의 다음 event/card selection을 구동했다는 증거는 없다.

판정:

- resource choice surface는 promising signal이다.
- manual choice-driven runner 구현 후 다시 검증해야 한다.

## 10. Completion Evidence로 쓰면 안 되는 이유

Run 1을 completion evidence로 쓰면 안 되는 이유:

- 25턴을 완료하지 않았다.
- Ending / Quest Report를 테스트하지 않았다.
- 사용자 선택이 실제 state transition에 반영되지 않았다.
- 고정 autoplayer log의 ending을 user-driven 결과처럼 해석하게 된다.
- 핵심 사용자 feedback이 완료 품질이 아니라 중단 사유에 해당한다.

따라서 Run 1의 올바른 상태는 다음이다.

```text
status: aborted
stopped_at: Turn 18
completion_evidence: false
critical_findings_evidence: true
```

## 11. 후속 작업 우선순위

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

## 12. Human Playtest Run 1 재시도 조건

재시도 전 필수 조건:

- 사용자 `1/2/3` 선택이 실제 state transition에 반영되는 runner가 있다.
- Run 시작 시 quest intro/onboarding이 표시된다.
- completed objective 이후 stale choice audit 또는 최소 gate가 완료됐다.
- Codex Facilitated Human Playtest Protocol v0.3을 사용한다.
- seed 202 baseline이 다시 검증된다.

재시도 전 검증:

- 3-card every turn.
- user-selected card가 selected card로 기록됨.
- state/resource/objective 변화가 사용자 선택 기준으로 적용됨.
- next event/card selection이 변경된 state를 기반으로 진행됨.

## 13. 실행한 명령

Verification transcript:

- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/verification.txt`

## 14. Evidence

Primary source:

- `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`

Audit evidence:

- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/findings_summary.md`
- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/critical_findings_table.md`
- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/run_1_abort_reference.md`
- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/next_tasks_priority.md`
- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/docs_presence_and_content.txt`
- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/scope_guard.txt`
- `.omo/ulw-loop/evidence/p1-human-playtest-findings-audit-20260701/verification.txt`

## 15. 다음 추천 작업

```text
CODEX_TASK_Manual_Choice_Driven_Standard_Run_Runner_v0.1.md
```

이 작업이 먼저인 이유는 facilitator runner가 없으면 다음 interactive playtest도 사용자 선택과 state transition이 분리되기 때문이다.
