# Console Simulator Review Checklist

이 체크리스트는 `docs/06_plans/00_Console_Simulator_Implementation_Plan_v0.1.md` 구현 후 PRD/Flutter 이전에 통과해야 하는 차단 검수 기준이다.

## 1. 구조 위반 체크

- [ ] Python package는 `src/fateweaver/` 아래에만 있다.
- [ ] CLI script는 `tools/` 아래에만 있다.
- [ ] 생성된 run output은 `logs/` 아래에만 있다.
- [ ] `data/core/`, `data/content/`, `data/scenarios/` 원본 YAML은 구현 중 수정되지 않았다.
- [ ] `src/fateweaver/`가 `tools/`를 import하지 않는다.
- [ ] `tools/`는 CLI parsing과 module 호출만 담당한다.

## 2. 금지 작업 체크

- [ ] `fate_weaver/` Flutter 프로젝트가 생성되지 않았다.
- [ ] Dart 또는 Flame 파일이 생성되지 않았다.
- [ ] PRD가 작성되지 않았다.
- [ ] World Bible이 작성되지 않았다.
- [ ] `data/mvp0/`가 생성되지 않았다.
- [ ] `CombatEventResolver`가 없다.
- [ ] 별도 combat loop, enemy HP, attack/defense turn, combat UI가 없다.
- [ ] 특정 event ID를 기준으로 한 Python 분기가 없다.

검증 명령:

```bash
find . -maxdepth 3 -type d \( -name fate_weaver -o -path './data/mvp0' \)
grep -R "CombatEventResolver\|enemy HP\|attack/defense\|event_id ==\|event_id in" src tools
```

## 3. 문서 계약 준수 체크

- [ ] `docs/03_specs/04_Console_Simulator_Spec_v0.7.md`의 CLI 범위와 일치한다.
- [ ] `docs/04_codex/05_Codex_Console_Prototype_Brief_v0.6.md`의 금지 범위를 넘지 않았다.
- [ ] `docs/02_schema/03_Event_Grammar_Draft_YAML_Schema_v0.7.md`의 event/choice/result 구조를 따른다.
- [ ] `docs/02_schema/06_Fixture_Data_Plan_v0.3.md`의 fixture 목적을 runtime logic으로 오해하지 않았다.
- [ ] `docs/02_schema/08_Flutter_Data_Export_Contract_v0.1.md`는 참조만 했고 Flutter export 구현을 시작하지 않았다.

## 4. 데이터 로딩 체크

- [ ] `data/core/statuses.yaml`이 로드된다.
- [ ] `data/core/tags.yaml`이 로드된다.
- [ ] `data/core/choice_types.yaml`이 로드된다.
- [ ] `data/core/item_roles.yaml`이 로드된다.
- [ ] `data/core/result_rules.yaml`이 로드된다.
- [ ] scenario의 `content_sources`가 모두 로드된다.
- [ ] duplicate event ID는 validation failure다.
- [ ] missing item/status/tag/choice_type reference는 validation failure다.

검증 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

## 5. Scenario Filter 체크

- [ ] `content_sources + include_regions`가 기본 event pool을 만든다.
- [ ] `include_event_ids`만 있으면 ID 필터가 적용된다.
- [ ] `include_event_tags`만 있으면 tag 필터가 적용된다.
- [ ] `include_event_ids`와 `include_event_tags`가 모두 있으면 AND 조건이다.
- [ ] `exclude_event_ids`와 `exclude_event_tags`는 include 후 마지막에 적용된다.
- [ ] include ids/tags가 모두 비어 있으면 matching source/region 전체가 사용된다.
- [ ] filter 결과가 scenario validation target보다 작으면 실패한다.

## 6. Choice Availability 체크

- [ ] event-level `requires_*`는 event eligibility만 결정한다.
- [ ] choice-level `requires_*`는 choice availability만 결정한다.
- [ ] missing required item은 choice unavailable이다.
- [ ] missing required status threshold는 choice unavailable이다.
- [ ] missing required run tag는 choice unavailable이다.
- [ ] unavailable choice 선택 시 `ValueError` 또는 CLI-level rejection이 발생한다.
- [ ] available choice만 state transition에 반영된다.

## 7. Unavailable Choice 표시 체크

- [ ] unavailable choice가 console output에 보인다.
- [ ] unavailable choice가 `choices_seen` log에 남는다.
- [ ] unavailable choice에는 `available: false`가 있다.
- [ ] unavailable choice에는 `unavailable_reason`이 있다.
- [ ] AutoPlayer가 unavailable choice를 선택하지 않는다.

## 8. 로그 필드 체크

- [ ] run log는 JSON이다.
- [ ] run log에 `schema_version`이 있다.
- [ ] run log에 `scenario_id`, `seed`, `run_id`가 있다.
- [ ] 각 turn에 `event_id`, `event_tags`, `state_before`, `inventory_before`가 있다.
- [ ] 각 turn에 `choices_seen`이 있다.
- [ ] 각 turn에 `selected_choice_id`, `selected_choice_type`, `was_available`가 있다.
- [ ] 각 turn에 `choice_reason`, `expected_risk`, `influenced_by`가 있다.
- [ ] 각 turn에 `state_after`, `inventory_after`, `regret_score`가 있다.
- [ ] run summary에 `restart_intent_score`, `player_woven_score`, `run_failed`, `run_failed_but_interesting`이 있다.

## 9. Core Loop Validation Metrics 체크

- [ ] `meaningful_choice_count`가 계산된다.
- [ ] `item_unlocked_choice_count`가 계산된다.
- [ ] `bad_tradeoff_count`가 계산된다.
- [ ] `restart_intent_score_avg`가 계산된다.
- [ ] `run_failed_but_interesting_count`가 계산된다.
- [ ] `player_woven_score_avg`가 계산된다.
- [ ] analyzer가 비어 있는 `logs/`에 대해 실패를 반환한다.
- [ ] analyzer가 malformed JSON에 대해 실패 위치를 출력한다.

검증 명령:

```bash
.venv/bin/python tools/analyze_logs.py --logs logs
```

## 10. Combat Policy 체크

- [ ] combat event는 `event_tags`에 `combat`이 있는 일반 event로 처리된다.
- [ ] combat choice는 `choice_type: combat_response`인 일반 choice로 처리된다.
- [ ] combat 전용 state transition이 없다.
- [ ] combat 전용 selector가 없다.
- [ ] combat 전용 logger field가 없다.
- [ ] combat count는 tag 기반으로 계산된다.

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

- [ ] 모든 명령이 exit code `0`으로 끝난다.
- [ ] simulator command가 자동 실행 환경에서 입력 대기하지 않는다.
- [ ] simulator command가 생성한 log를 analyzer command가 읽는다.

## 12. 완료 판정 기준

`바로 PRD/Flutter 이전 검증 통과`로 볼 수 있는 조건:

- [ ] Section 1-11 체크가 모두 통과한다.
- [ ] required CLI 3개가 모두 통과한다.
- [ ] analyzer output에 six Core Loop Validation Metrics가 모두 있다.
- [ ] generated log를 사람이 읽었을 때 선택, unavailable choice, result, regret/player-woven 입력 경로가 추적된다.

`보강 후 재검수` 조건:

- [ ] CLI는 실행되지만 metrics 중 하나라도 비어 있거나 의미가 불명확하다.
- [ ] unavailable choice가 표시되지만 log에 reason이 없다.
- [ ] combat이 돌아가지만 일반 event contract로 설명되지 않는다.

`차단` 조건:

- [ ] simulator가 입력 대기 때문에 자동 검증 명령에서 멈춘다.
- [ ] scenario filter가 ID+tag AND 조건을 지키지 않는다.
- [ ] unavailable choice를 선택할 수 있다.
- [ ] `CombatEventResolver` 또는 별도 combat loop가 생겼다.
- [ ] Flutter/Dart 영역이 생성됐다.
