# [Current] Manual Choice-Driven Standard Run Runner Result v0.1

> 상태: [Current] P1 Human Playtest Run 1 중단의 최우선 원인인 facilitator runner 부재를 해결하기 위해 manual choice-driven runner를 추가한 결과 문서.

## 1. 작업 목적

사용자의 `1/2/3` 선택을 실제 presented card index로 적용하고, 선택된 card result가 기존 P0 state transition에 반영되도록 manual runner를 추가했다.

이번 작업은 runner 구현이다. `data/`는 수정하지 않았고, card/event scoring, resource/balance, ontology/director, Text MUD 문구 polish는 변경하지 않았다.

## 2. 읽은 기준 문서

- `docs/07_reviews/63_P1_Human_Playtest_Findings_Audit_v0.1.md`
- `docs/04_codex/16_Codex_P1_Post_Playtest_Critical_Fixes_Brief_v0.1.md`
- `docs/05_validation/21_Codex_Facilitated_Human_Playtest_Protocol_v0.3.md`
- `docs/07_reviews/61_Human_Playtest_Run_1_Result_v0.1.md`
- `docs/06_plans/13_P1_Human_Playtest_Run_1_Plan_v0.1.md`
- `docs/05_validation/20_Human_Playtest_Run_1_Player_Sheet_v0.1.md`
- `docs/05_validation/17_P0_Playable_Milestone_Checklist_v0.1.md`
- `docs/07_reviews/57_P0_Playable_Milestone_Freeze_Result_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`

## 3. 문제 정의

Run 1 attempt는 고정 seed 202 autoplayer log replay였기 때문에, 사용자의 `1/2/3` 선택이 실제 selected card나 다음 turn state transition을 구동하지 못했다.

## 4. 구현한 Runner

추가 runner:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/manual_choice_runner.py \
  --scenario data/scenarios/standard_run_25_35_turn.yaml \
  --seed 202 \
  --choices 1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1 \
  --output-dir .omo/ulw-loop/evidence/manual-choice-driven-runner-20260701
```

지원 input mode:

- `--choices`
- `--choice-file`
- `--interactive`

## 5. Manual Choice Flow

Flow:

1. Scenario와 active quest foundation을 load한다.
2. 기존 Situation Director / card candidate selection으로 3장의 presented card를 만든다.
3. manual choice `1/2/3`을 `presented_cards[0..2]`에 매핑한다.
4. 선택된 card 하나를 `combined_result(..., combo=None, ...)`로 result화한다.
5. 기존 `apply_turn_result()`로 state/resource/objective/next_event_tags를 갱신한다.
6. 갱신된 state로 다음 turn의 event/card selection을 진행한다.

기존 autoplayer path인 `tools/console_simulator.py`와 `run_gameplay_p0()`는 변경하지 않았다.

## 6. Choice Trace

Trace file:

```text
.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_seed_202_choice_trace.json
```

Trace fields:

- `turn`
- `day`
- `presented_card_ids`
- `selected_index`
- `selected_card_id`
- `selected_card_slot_role`
- `result_summary`
- `resource_delta`
- `objective_delta`
- `next_event_tags_delta`

Smoke assertion:

```text
trace_result_consistency PASS
updated_state_carries_to_next_turn PASS
```

## 7. JSON / Text MUD Output

Generated files:

- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_seed_202.json`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_seed_202_text_mud.txt`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_seed_202_choice_trace.json`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_seed_202_summary.json`

The JSON log records:

```text
manual_choice_mode: true
choice_source: sequence
manual_choice_trace: [...]
```

## 8. P0 Autoplayer Baseline 보호

Baseline path remains:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py \
  --scenario data/scenarios/standard_run_25_35_turn.yaml \
  --seed 42 \
  --runs 1 \
  --profile balanced
```

Expected baseline:

- `result_type: success`
- `ending.id: prepared_frontier_route`
- 3-card every turn

## 9. 테스트 결과

Focused test:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_manual_choice_runner
```

Full validation transcript:

```text
.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/verification.txt
```

## 10. 실행한 명령

See:

- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_runner_smoke.txt`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/invalid_choice.txt`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/verification.txt`

## 11. Evidence

Primary evidence:

- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/manual_runner_smoke.txt`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/invalid_choice.txt`
- `.omo/ulw-loop/evidence/manual-choice-driven-runner-20260701/verification.txt`

## 12. 남은 문제

Manual runner는 facilitator state transition 문제만 해결한다. Quest onboarding 부재, completed objective 이후 stale choices, merchant storylet relevance/noise는 별도 후속 작업으로 남아 있다.

## 13. 다음 추천 작업

```text
CODEX_TASK_Quest_Intro_Onboarding_Gate_v0.1.md
```
