# Console Simulator Review Result

이 문서는 `docs/06_plans/00_Console_Simulator_Implementation_Plan_v0.1.md` 구현 후 PRD/Flutter 이전에 통과한 Console Simulator 구현 검수 결과다.

완료된 검수 기록으로 보관하며, 다음 작업 체크리스트는 `docs/05_validation/08_Content_Expansion_Readiness_Checklist_v0.1.md`를 기준으로 한다.

## 검수 상태

```text
Status: PASS
검수일: 2026-06-29
대상: Console Validation Python implementation
판정: 구현 후 리뷰 차단 이슈 수정 완료, 최종 재리뷰 승인
```

근거:

- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C001-validate-data.txt`
- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C002-console-simulator.txt`
- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C003-analyze-logs.txt`
- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C004-unit-tests.txt`
- `.omo/evidence/console-validation-qa.md`
- `.omo/evidence/final-choice-resolver-re-review-code-review.md`

통과 기준:

- required CLI 3개 통과
- unittest 18개 통과
- generated log에 unavailable choice와 run summary metric 필드 존재
- 1차 review blocker 수정 후 `UNCONDITIONAL APPROVAL`

## 1. 구조 위반 체크

- [x] Python package는 `src/fateweaver/` 아래에만 있다.
- [x] CLI script는 `tools/` 아래에만 있다.
- [x] 생성된 run output은 `logs/` 아래에만 있다.
- [x] `data/core/`, `data/content/`, `data/scenarios/` 원본 YAML은 구현 중 수정되지 않았다.
- [x] `src/fateweaver/`가 `tools/`를 import하지 않는다.
- [x] `tools/`는 CLI parsing과 module 호출만 담당한다.

## 2. 금지 작업 체크

- [x] `fate_weaver/` Flutter 프로젝트가 생성되지 않았다.
- [x] Dart 또는 Flame 파일이 생성되지 않았다.
- [x] PRD가 작성되지 않았다.
- [x] World Bible이 작성되지 않았다.
- [x] `data/mvp0/`가 생성되지 않았다.
- [x] `CombatEventResolver`가 없다.
- [x] 별도 combat loop, enemy HP, attack/defense turn, combat UI가 없다.
- [x] 특정 event ID를 기준으로 한 Python 분기가 없다.

검증 명령:

```bash
find . -maxdepth 3 -type d \( -name fate_weaver -o -path './data/mvp0' \)
grep -R "CombatEventResolver\|enemy HP\|attack/defense\|event_id ==\|event_id in" src tools
```

## 3. 문서 계약 준수 체크

- [x] `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`의 CLI 범위와 일치한다.
- [x] `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`의 금지 범위를 넘지 않았다.
- [x] `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`의 event/choice/result 구조를 따른다.
- [x] `docs/02_schema/06_Fixture_Data_Plan_v0.3.md`의 fixture 목적을 runtime logic으로 오해하지 않았다.
- [x] `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`는 참조만 했고 Flutter export 구현을 시작하지 않았다.

## 4. 데이터 로딩 체크

- [x] `data/core/statuses.yaml`이 로드된다.
- [x] `data/core/tags.yaml`이 로드된다.
- [x] `data/core/choice_types.yaml`이 로드된다.
- [x] `data/core/item_roles.yaml`이 로드된다.
- [x] `data/core/result_rules.yaml`이 로드된다.
- [x] scenario의 `content_sources`가 모두 로드된다.
- [x] duplicate event ID는 validation failure다.
- [x] missing item/status/tag/choice_type reference는 validation failure다.
- [x] malformed scenario/schema 입력은 traceback이 아니라 `VALIDATION: ERROR`로 실패한다.
- [x] item `roles`는 `data/core/item_roles.yaml`과 `data/core/tags.yaml`의 `item_role` enum 양쪽에 존재해야 한다.
- [x] item `tags`는 `data/core/tags.yaml`의 `item_tag` enum에 존재해야 한다.
- [x] event `region_tags`, `event_tags`, `danger_tags`는 `data/core/tags.yaml`의 각 enum에 존재해야 한다.
- [x] result `status` key는 `data/core/statuses.yaml`과 `data/core/result_rules.yaml`의 allowed status 양쪽에서 허용되어야 한다.
- [x] result `event_weight` target은 `data/core/tags.yaml`의 `weight_target` enum에 존재해야 한다.

검증 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

## 5. Scenario Filter 체크

- [x] `content_sources + include_regions`가 기본 event pool을 만든다.
- [x] `include_event_ids`만 있으면 ID 필터가 적용된다.
- [x] `include_event_tags`만 있으면 tag 필터가 적용된다.
- [x] `include_event_ids`와 `include_event_tags`가 모두 있으면 AND 조건이다.
- [x] `exclude_event_ids`와 `exclude_event_tags`는 include 후 마지막에 적용된다.
- [x] include ids/tags가 모두 비어 있으면 matching source/region 전체가 사용된다.
- [x] filter 결과가 scenario validation target보다 작으면 실패한다.

## 6. Choice Availability 체크

- [x] event-level `requires_*`는 event eligibility만 결정한다.
- [x] choice-level `requires_*`는 choice availability만 결정한다.
- [x] missing required item은 choice unavailable이다.
- [x] missing required status threshold는 choice unavailable이다.
- [x] missing required run tag는 choice unavailable이다.
- [x] run tag requirement는 status requirement가 통과한 상태에서도 독립적으로 테스트된다.
- [x] run tag가 존재하면 같은 choice가 available로 바뀌는 positive case가 테스트된다.
- [x] unavailable choice 선택 시 `ValueError` 또는 CLI-level rejection이 발생한다.
- [x] available choice만 state transition에 반영된다.

## 7. Unavailable Choice 표시 체크

- [x] unavailable choice가 console output에 보인다.
- [x] unavailable choice가 `choices_seen` log에 남는다.
- [x] unavailable choice에는 `available: false`가 있다.
- [x] unavailable choice에는 `unavailable_reason`이 있다.
- [x] AutoPlayer가 unavailable choice를 선택하지 않는다.

## 8. 로그 필드 체크

- [x] run log는 JSON이다.
- [x] run log에 `schema_version`이 있다.
- [x] run log에 `scenario_id`, `seed`, `run_id`가 있다.
- [x] 각 turn에 `event_id`, `event_tags`, `state_before`, `inventory_before`가 있다.
- [x] 각 turn에 `choices_seen`이 있다.
- [x] 각 turn에 `selected_choice_id`, `selected_choice_type`, `was_available`가 있다.
- [x] 각 turn에 `choice_reason`, `expected_risk`, `influenced_by`가 있다.
- [x] 각 turn에 `state_after`, `inventory_after`, `regret_score`가 있다.
- [x] run summary에 `restart_intent_score`, `player_woven_score`, `run_failed`, `run_failed_but_interesting`이 있다.
- [x] TTY mode는 choice 단위 `choice_reason`, `expected_risk`, `regret_score` 입력을 받는다.
- [x] TTY mode는 run 종료 `fairness_score`, `restart_intent_score`, `player_woven_score`, `narrative_summary`, `most_memorable_choice`, `next_run_intent` 입력을 받는다.
- [x] non-interactive mode는 입력 대기 없이 deterministic AutoPlayer 값으로 동일 필드를 채운다.

## 9. Core Loop Validation Metrics 체크

- [x] `meaningful_choice_count`가 계산된다.
- [x] `item_unlocked_choice_count`가 계산된다.
- [x] `bad_tradeoff_count`가 계산된다.
- [x] `restart_intent_score_avg`가 계산된다.
- [x] `run_failed_but_interesting_count`가 계산된다.
- [x] `player_woven_score_avg`가 계산된다.
- [x] analyzer가 비어 있는 `logs/`에 대해 실패를 반환한다.
- [x] analyzer가 malformed JSON에 대해 실패 위치를 출력한다.

검증 명령:

```bash
.venv/bin/python tools/analyze_logs.py --logs logs
```

## 10. Combat Policy 체크

- [x] combat event는 `event_tags`에 `combat`이 있는 일반 event로 처리된다.
- [x] combat choice는 `choice_type: combat_response`인 일반 choice로 처리된다.
- [x] combat 전용 state transition이 없다.
- [x] combat 전용 selector가 없다.
- [x] combat 전용 logger field가 없다.
- [x] combat count는 tag 기반으로 계산된다.

## 11. 실행 명령 체크

필수 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1
.venv/bin/python tools/analyze_logs.py --logs logs
```

추가 검증:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

Pass criteria:

- [x] 모든 명령이 exit code `0`으로 끝난다.
- [x] simulator command가 자동 실행 환경에서 입력 대기하지 않는다.
- [x] simulator command가 생성한 log를 analyzer command가 읽는다.
- [x] `tools/*.py`는 argparse와 domain module 호출만 담당한다.
- [x] simulator loop, log payload 구성, player feedback 처리는 `src/fateweaver/` domain module에 있다.
- [x] malformed scenario fixture에 대한 CLI smoke test가 존재한다.
- [x] console simulator는 temporary logs directory를 대상으로 smoke test된다.

## 12. 완료 판정 기준

`바로 PRD/Flutter 이전 검증 통과`로 볼 수 있는 조건:

- [x] Section 1-11 체크가 모두 통과한다.
- [x] required CLI 3개가 모두 통과한다.
- [x] analyzer output에 six Core Loop Validation Metrics가 모두 있다.
- [x] generated log를 사람이 읽었을 때 선택, unavailable choice, result, regret/player-woven 입력 경로가 추적된다.

`보강 후 재검수` 조건:

- [x] CLI는 실행되지만 metrics 중 하나라도 비어 있거나 의미가 불명확하다.
- [x] unavailable choice가 표시되지만 log에 reason이 없다.
- [x] combat이 돌아가지만 일반 event contract로 설명되지 않는다.

`차단` 조건:

- [x] simulator가 입력 대기 때문에 자동 검증 명령에서 멈춘다.
- [x] scenario filter가 ID+tag AND 조건을 지키지 않는다.
- [x] unavailable choice를 선택할 수 있다.
- [x] `CombatEventResolver` 또는 별도 combat loop가 생겼다.
- [x] Flutter/Dart 영역이 생성됐다.

## 13. Review Blocker Regression 체크

1차 구현 리뷰에서 BLOCK으로 확인된 항목은 이후 회귀 방지 대상이다.

- [x] `validate_data`는 missing `id` 같은 malformed YAML에서도 traceback을 노출하지 않는다.
- [x] validator는 core contract 전체를 검증한다: statuses, tags, choice_types, item_roles, result_rules.
- [x] TTY와 non-TTY simulator 동작이 모두 문서 계약과 일치한다.
- [x] CLI wrapper와 domain logic 경계가 유지된다.
- [x] 테스트는 happy path만이 아니라 invalid fixture, scenario filter 조합, choice availability 독립 조건, state transition, analyzer empty logs, combat-as-ordinary-event를 포함한다.
- [x] 리뷰어가 지적한 테스트 허점은 별도 regression test로 잠근다.
