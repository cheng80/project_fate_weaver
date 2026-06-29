# Console Simulator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Python Console Validation simulator that validates FateWeaver YAML data, runs a seedable event-choice-state loop, writes analyzable JSON logs, and reports Core Loop Validation Metrics before Flutter work begins.
**Architecture:** `src/fateweaver/` contains reusable domain modules. `tools/` contains thin CLI entrypoints. `data/` remains the source of truth. `logs/` stores generated run artifacts. No Flutter/Dart project is created in this phase.
**Tech Stack:** Python 3.12, standard library (`argparse`, `dataclasses`, `json`, `pathlib`, `random`, `unittest`), PyYAML from `requirements.txt`.

---

## 1. 구현 목표

- YAML data contract 검증기를 만든다.
- `data/scenarios/mvp0_console_test.yaml`을 입력으로 받아 Console Validation run을 실행한다.
- event-level eligibility와 choice-level availability를 분리한다.
- unavailable choice는 화면과 로그에 표시하되 선택은 막는다.
- combat은 일반 event + `choice_type: combat_response`로만 처리한다.
- run log와 analysis output으로 아래 Core Loop Validation Metrics를 계산한다.
  - `meaningful_choice_count`
  - `item_unlocked_choice_count`
  - `bad_tradeoff_count`
  - `restart_intent_score`
  - `run_failed_but_interesting`
  - `player_woven_score`

## 2. 구현하지 않을 것

- `fate_weaver/` Flutter 프로젝트 생성.
- Dart, Flame, Flutter UI 작성.
- PRD 또는 World Bible 작성.
- `data/mvp0/` 생성.
- 이벤트 ID별 분기 하드코딩.
- 별도 전투 루프, enemy HP, attack/defense turn, combat UI, `CombatEventResolver` 작성.
- YAML 원본을 Python 코드 상수로 복제.

## 3. 생성/수정 예정 파일

생성:

```text
src/fateweaver/__init__.py
src/fateweaver/models.py
src/fateweaver/data_loader.py
src/fateweaver/scenario_filter.py
src/fateweaver/event_selector.py
src/fateweaver/choice_resolver.py
src/fateweaver/state_manager.py
src/fateweaver/validator.py
src/fateweaver/logger.py
src/fateweaver/analyzer.py
tools/validate_data.py
tools/console_simulator.py
tools/analyze_logs.py
tests/test_data_loader.py
tests/test_validator.py
tests/test_scenario_filter.py
tests/test_choice_resolver.py
tests/test_event_selector.py
tests/test_logger_analyzer.py
tests/test_cli_smoke.py
```

수정 가능:

```text
README.md
docs/00_index/README_Docs_Index.md
docs/05_validation/07_Console_Validation_Checklist_v0.1.md
```

수정 금지:

```text
data/core/*.yaml
data/content/**/*.yaml
data/scenarios/*.yaml
docs/01_foundation/*.md
docs/02_schema/*.md
docs/03_specs/*.md
docs/04_codex/*.md
```

## 4. 모듈별 책임

| Module | Responsibility |
| --- | --- |
| `models.py` | Dataclass와 타입 alias 정의. YAML 구조를 Python 객체로 얇게 표현한다. |
| `data_loader.py` | YAML 로드, content source 병합, scenario 로드. 검증 판단은 하지 않는다. |
| `validator.py` | schema-level contract, 참조 무결성, scenario target 최소 조건 검증. |
| `scenario_filter.py` | scenario include/exclude 규칙으로 eligible event pool 생성. |
| `choice_resolver.py` | choice-level `requires_*` 판정, unavailable reason 생성, result payload 반환. |
| `event_selector.py` | seedable random으로 다음 event 선택. 이벤트별 특수 분기 금지. |
| `state_manager.py` | status, inventory, run tags에 result 적용. min/max clamp와 fail state 판정. |
| `logger.py` | run log JSON 생성과 저장. |
| `analyzer.py` | logs 폴더에서 Core Loop Validation Metrics 계산. |
| `tools/*.py` | CLI argument parsing과 domain module 호출만 담당. |

## 5. 데이터 계약

### Scenario Filter

- `content_sources`와 `include_regions`는 event pool의 기본 입력이다.
- `include_event_ids`와 `include_event_tags`는 선택 필터다.
- `include_event_ids`와 `include_event_tags`가 모두 비어 있으면 `content_sources + include_regions` 기준의 모든 event를 포함한다.
- `include_event_ids`만 있으면 해당 ID event만 포함한다.
- `include_event_tags`만 있으면 해당 tag를 가진 event만 포함한다.
- `include_event_ids`와 `include_event_tags`가 모두 있으면 AND 조건이다. ID에 포함되고 tag 조건도 만족해야 한다.
- `exclude_event_ids`와 `exclude_event_tags`는 마지막에 적용한다.
- filter 결과가 `validation_targets.min_events`보다 작으면 validator error다.

### Choice-Level Requires

- event-level `requires_*`는 event eligibility만 결정한다.
- choice-level `requires_*`는 choice availability만 결정한다.
- 대부분의 조건은 choice-level에 둔다.
- unavailable choice는 `available: false`, `reason: <human readable reason>`으로 반환한다.
- unavailable choice는 화면과 로그에는 남기지만 선택 입력으로는 허용하지 않는다.

### Combat Policy

- combat은 `event_tags: [combat]`을 가진 일반 event다.
- `combat_response`는 `choice_type` 중 하나다.
- `event_selector`, `choice_resolver`, `state_manager`는 combat 전용 class를 만들지 않는다.
- combat 선택지는 다른 선택지와 같은 `requires_*`와 `results` 규칙으로 처리한다.

## 6. 로그 출력 계약

`logger.py`는 run마다 `logs/run_<scenario_id>_<seed>_<timestamp>.json` 파일을 쓴다.

```json
{
  "schema_version": "console_validation_log_v0.1",
  "scenario_id": "mvp0_console_test",
  "seed": 42,
  "run_id": "mvp0_console_test-42-0001",
  "turns": [
    {
      "turn": 1,
      "event_id": "forest_ambush_01",
      "event_tags": ["combat"],
      "state_before": {"health": 7, "food": 5, "money": 2, "reputation": 0, "curse": 1},
      "inventory_before": ["rope", "torch"],
      "choices_seen": [
        {
          "choice_id": "fight_with_torch",
          "choice_type": "combat_response",
          "available": true,
          "unavailable_reason": null
        }
      ],
      "selected_choice_id": "fight_with_torch",
      "selected_choice_type": "combat_response",
      "was_available": true,
      "choice_reason": "auto: selected first available non-hidden choice",
      "expected_risk": "medium",
      "influenced_by": ["item:torch", "tag:combat"],
      "result": {"status": {"health": -1}},
      "state_after": {"health": 6, "food": 5, "money": 2, "reputation": 0, "curse": 1},
      "inventory_after": ["rope", "torch"],
      "regret_score": 3
    }
  ],
  "run_summary": {
    "final_state": {"health": 4, "food": 1, "money": 0, "reputation": 1, "curse": 4},
    "final_inventory": ["rope", "torch"],
    "restart_intent_score": 4,
    "player_woven_score": 4,
    "run_failed": false,
    "run_failed_but_interesting": false
  }
}
```

필드 규칙:

- `regret_score`: choice-level integer 1-5. Interactive mode에서는 player input, non-interactive mode에서는 deterministic AutoPlayer mapping을 사용한다.
- `player_woven_score`: run-level integer 1-5. Interactive mode에서는 player input, non-interactive mode에서는 deterministic AutoPlayer mapping을 사용한다.
- `influenced_by`: 선택 판단에 영향을 준 item/status/tag/unavailable signal을 문자열 배열로 기록한다.
- unavailable 선택지도 `choices_seen`에 반드시 포함한다.

## 7. Core Loop Validation Metrics 계산 방식

`analyzer.py`는 log JSON들을 읽어 아래 기준으로 metrics를 계산한다.

| Metric | Calculation |
| --- | --- |
| `meaningful_choice_count` | `influenced_by`가 비어 있지 않은 selected choice 수 |
| `item_unlocked_choice_count` | selected choice 중 `influenced_by`에 `item:` prefix가 있는 수 |
| `bad_tradeoff_count` | selected choice 중 `expected_risk`가 `high`이거나 `regret_score >= 4`인 수 |
| `restart_intent_score` | 각 run의 `run_summary.restart_intent_score` 평균 |
| `run_failed_but_interesting` | `run_summary.run_failed == true`이고 `restart_intent_score >= 4`인 run 수 |
| `player_woven_score` | 각 run의 `run_summary.player_woven_score` 평균 |

Analyzer output:

```json
{
  "runs_analyzed": 1,
  "meaningful_choice_count": 12,
  "item_unlocked_choice_count": 3,
  "bad_tradeoff_count": 4,
  "restart_intent_score_avg": 4.0,
  "run_failed_but_interesting_count": 0,
  "player_woven_score_avg": 4.0
}
```

## 8. 구현 순서

### Step 1: Baseline Package and Unit Test Skeleton

- [ ] Create `src/fateweaver/__init__.py`.
- [ ] Create `tests/` with import smoke tests.
- [ ] Run:

```bash
.venv/bin/python -m unittest discover -s tests
```

Completion criteria:

- `python -m unittest discover` runs.
- `import fateweaver` succeeds with `PYTHONPATH=src`.

Commit:

```bash
git add src/fateweaver/__init__.py tests
git commit -m "test: add console validation test skeleton"
```

### Step 2: Models and Data Loader

- [ ] Add dataclasses in `models.py`.
- [ ] Add YAML loading and content source merging in `data_loader.py`.
- [ ] Cover with `tests/test_data_loader.py`.

Expected public API:

```python
from pathlib import Path

from fateweaver.data_loader import load_project_data

bundle, scenario = load_project_data(
    project_root=Path("."),
    scenario_path=Path("data/scenarios/mvp0_console_test.yaml"),
)
```

Completion criteria:

- Scenario id is `mvp0_console_test`.
- At least one core status, item, event, and ending load.
- Duplicate event IDs raise `ValueError("Duplicate event id: <id>")`.

Commit:

```bash
git add src/fateweaver/models.py src/fateweaver/data_loader.py tests/test_data_loader.py
git commit -m "feat: load console validation YAML data"
```

### Step 3: Validator and `tools/validate_data.py`

- [ ] Implement `validator.py`.
- [ ] Implement CLI wrapper `tools/validate_data.py`.
- [ ] Cover valid scenario and broken reference fixtures inside tests using temporary files.

Validation checks:

- Scenario path exists.
- `content_sources` folders exist.
- `include_regions` values exist in `data/core/tags.yaml`.
- All scenario `initial_status` keys exist in `data/core/statuses.yaml`.
- All `initial_items` exist in loaded items.
- All event IDs are unique.
- All choice types exist in `data/core/choice_types.yaml`.
- All `requires_items` references exist.
- All result status keys exist.
- Filtered event count satisfies `validation_targets.min_events`.
- Filtered combat event count satisfies `validation_targets.min_combat_events`.
- Filtered curse-tagged event count satisfies `validation_targets.min_curse_events`.

Required command:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
```

Completion criteria:

- Valid scenario exits `0` and prints `VALIDATION: PASS`.
- Invalid data exits non-zero and prints each failure as `VALIDATION: ERROR <message>`.

Commit:

```bash
git add src/fateweaver/validator.py tools/validate_data.py tests/test_validator.py
git commit -m "feat: validate console scenario data"
```

### Step 4: Scenario Filter

- [ ] Implement `scenario_filter.py`.
- [ ] Cover include-id, include-tag, include-id+tag AND, exclude-id, exclude-tag.

Expected API:

```python
from fateweaver.scenario_filter import filter_events_for_scenario

events = filter_events_for_scenario(bundle.events, scenario)
```

Completion criteria:

- Empty include ids/tags returns all events from matching sources and regions.
- ID + tag include uses AND.
- Excludes are applied after includes.
- No event-specific branch exists in code.

Commit:

```bash
git add src/fateweaver/scenario_filter.py tests/test_scenario_filter.py
git commit -m "feat: apply scenario event filters"
```

### Step 5: Choice Availability and Result Resolution

- [ ] Implement `choice_resolver.py`.
- [ ] Cover item, status, run tag, and unavailable reason cases.

Expected API:

```python
from fateweaver.choice_resolver import build_choices_seen, select_available_choice

choices_seen = build_choices_seen(event, state, inventory, run_tags)
selected = select_available_choice(choices_seen, policy="auto")
```

Availability rules:

- Missing required item returns unavailable reason `requires item: <item_id>`.
- Missing required status threshold returns `requires <status> >= <value>` or `requires <status> <= <value>`.
- Missing required run tag returns `requires run tag: <tag>`.
- Hidden choices can be shown as unavailable when the source YAML marks them as visible-unavailable; otherwise keep them out of `choices_seen`.
- Selecting unavailable choice raises `ValueError("Choice is unavailable: <choice_id>")`.

Completion criteria:

- Unavailable choices are logged in `choices_seen`.
- Auto selection never selects unavailable choices.
- `combat_response` receives no special resolver.

Commit:

```bash
git add src/fateweaver/choice_resolver.py tests/test_choice_resolver.py
git commit -m "feat: resolve choice availability"
```

### Step 6: State Manager and Event Selector

- [ ] Implement `state_manager.py`.
- [ ] Implement `event_selector.py`.
- [ ] Cover status clamp, inventory add/remove, run tags, seed determinism.

Expected API:

```python
from random import Random

from fateweaver.event_selector import select_event
from fateweaver.state_manager import apply_choice_result

event = select_event(events, state, inventory, run_tags, rng=Random(42), recent_event_ids=[])
next_state = apply_choice_result(state, inventory, run_tags, selected.result, bundle.statuses)
```

Completion criteria:

- Same seed and same inputs choose the same sequence.
- Status values are clamped to configured min/max.
- Failure states are derived from `data/core/statuses.yaml`.
- Event-level `requires_*` affects selection eligibility only.

Commit:

```bash
git add src/fateweaver/state_manager.py src/fateweaver/event_selector.py tests/test_event_selector.py
git commit -m "feat: run seedable event state loop"
```

### Step 7: Logger and Console Simulator CLI

- [ ] Implement `logger.py`.
- [ ] Implement `tools/console_simulator.py`.
- [ ] Cover one-run smoke execution with temporary log directory.

Required command:

```bash
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1
```

CLI behavior:

- If stdin is TTY, prompt for choice, choice reason, expected risk, regret score, restart intent, and player-woven score.
- If stdin is not TTY, use deterministic AutoPlayer:
  - choose first available non-hidden choice in YAML order;
  - `choice_reason = "auto: selected first available non-hidden choice"`;
  - `expected_risk` from choice metadata when present, otherwise `medium`;
  - `regret_score`: `low -> 1`, `medium -> 3`, `high -> 4`;
  - `restart_intent_score`: `4` unless run has fewer than 3 meaningful choices, then `2`;
  - `player_woven_score`: `4` when at least one item/status influenced choice exists, otherwise `2`.
- Print the log path at the end.

Completion criteria:

- Command exits `0` without waiting for input in automated shell execution.
- A JSON log is created under `logs/`.
- Log contains unavailable choices when unavailable choices are present.
- No `tools/*.py` file contains game-specific event ID branches.

Commit:

```bash
git add src/fateweaver/logger.py tools/console_simulator.py tests/test_logger_analyzer.py tests/test_cli_smoke.py
git commit -m "feat: run console validation simulator"
```

### Step 8: Analyzer CLI

- [ ] Implement `analyzer.py`.
- [ ] Implement `tools/analyze_logs.py`.
- [ ] Cover metric calculations from fixture logs in tests.

Required command:

```bash
.venv/bin/python tools/analyze_logs.py --logs logs
```

Completion criteria:

- Empty logs directory exits non-zero with `ANALYSIS: ERROR no run logs found`.
- Valid logs print JSON metrics.
- Metric calculations match section 7.

Commit:

```bash
git add src/fateweaver/analyzer.py tools/analyze_logs.py tests/test_logger_analyzer.py
git commit -m "feat: analyze console validation logs"
```

### Step 9: Documentation and Final Verification

- [ ] Update README command list if needed.
- [ ] Update docs index if new plan/checklist links are missing.
- [ ] Run all required checks.

Commands:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1
.venv/bin/python tools/analyze_logs.py --logs logs
grep -R "CombatEventResolver\|enemy HP\|attack/defense\|data/mvp0\|fate_weaver/" README.md docs src tools data/scenarios
```

Completion criteria:

- Unit tests pass.
- Required three CLI commands pass.
- Generated analyzer output contains all six Core Loop Validation Metrics.
- Grep command returns no implementation-scope violations.

Commit:

```bash
git add README.md docs src tools tests
git commit -m "docs: document console validation execution"
```

## 9. 단계별 완료 기준

- Loader complete: project YAML loads without duplicating schema logic in CLI.
- Validator complete: broken references fail before simulator run.
- Filter complete: scenario pool is deterministic and contract-compliant.
- Choice resolver complete: availability and eligibility are separate.
- Simulator complete: non-interactive verification command does not hang.
- Analyzer complete: logs produce the six named metrics.
- Final complete: all commands in section 8 step 9 pass.

## 10. 실행 명령

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1
.venv/bin/python tools/analyze_logs.py --logs logs
```

Optional full local verification:

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

## 11. 테스트/검증 기준

- Tests use `unittest` and standard library temporary directories.
- Tests do not mutate committed YAML data.
- CLI smoke tests call subprocess with `PYTHONPATH=src`.
- Every module-level public function has at least one direct test.
- Regression tests cover:
  - scenario filter AND behavior;
  - unavailable choice visibility and selection block;
  - combat as ordinary event;
  - deterministic seed behavior;
  - analyzer metric math.

## 12. 최종 완료 조건

- The three required CLI commands run successfully.
- Unit tests pass.
- New logs can be analyzed immediately.
- No Python implementation exists outside `src/fateweaver/` and `tools/`.
- No Flutter/Dart project exists.
- No event-specific branch appears in Python source.
- Review checklist in `docs/06_plans/01_Review_Checklist_v0.1.md` passes.

## 13. Self-Review

- Spec coverage: all required plan topics are represented in sections 1-12.
- Scope control: prohibited Flutter, PRD, World Bible, `data/mvp0`, and combat-system work are explicitly excluded.
- Data path consistency: plan uses existing `data/scenarios/mvp0_console_test.yaml`.
- Verification consistency: required commands match the current Console Validation contract.
- Type consistency: `regret_score`, `restart_intent_score`, and `player_woven_score` are integers on a 1-5 scale.
