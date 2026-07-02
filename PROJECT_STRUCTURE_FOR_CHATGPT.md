# FateWeaver Project Structure for ChatGPT

이 문서는 ChatGPT나 다른 코드 보조 도구가 FateWeaver의 현재 구조를 빠르게 파악하도록 만든 단일 진입 문서다.  
세부 설계는 `docs/00_index/README_Docs_Index.md`에서 이어서 확인한다.

## 1. 현재 프로젝트 한 줄 요약

FateWeaver는 YAML 기반 퀘스트/이벤트/카드 데이터를 읽어, Standard Run 시나리오에서 3장 카드 선택, 온톨로지-lite 의미 추론, 상황 디렉터, 퀘스트 완료/전환, Text MUD 로그를 생성하는 텍스트 모험 게임 프로토타입이다.

현재 핵심 검증 시나리오는 `data/scenarios/standard_run_25_35_turn.yaml`이다.

- `gameplay_mode: p0_foundation`은 아직 데이터 계약 이름으로 남아 있다.
- Python 모듈명은 최근 역할 중심 이름으로 정리되었다.
- 과거 테스트/문서명에는 `gameplay_p0`가 많이 남아 있는데, 이는 P0 마일스톤 기록명이다.

## 2. 루트 폴더 역할

```text
data/      YAML 원천 데이터. core 규칙, content 데이터, scenario 설정.
docs/      설계, 스키마, 계획, 검증 결과 문서.
src/       Python 패키지 소스. fateweaver 런타임 로직.
tests/     unittest 기반 회귀 테스트.
tools/     CLI 실행기, manual runner, batch runner, report generator.
logs/      실행 결과 JSON/Text MUD/trace/report 출력 위치. 보통 git 추적 대상 아님.
```

## 3. 코드 구조: `src/fateweaver/`

### 런 실행과 상태 전이

- `gameplay_run.py`: Standard Run 자동 실행의 메인 엔진. storylet 선택, 카드 후보 생성, 카드 선택, 결과 적용, 퀘스트 완료/전환, JSON/Text MUD 로그 저장을 연결한다.
- `gameplay_setup.py`: active quest 기준으로 퀘스트/카드/스코어 규칙 foundation을 로드한다.
- `gameplay_models.py`: `RunState`, `Quest`, `Card`, trace request 등 gameplay dataclass/type 정의.
- `gameplay_rules.py`: 초기 상태, clock 진행, 카드 결과 적용, 결과 합성, storylet/card 선택 helper.
- `gameplay_sources.py`: split YAML content source를 하나의 foundation 입력으로 합친다.
- `gameplay_errors.py`: gameplay pipeline 전용 예외.

### 카드 후보, 선택, 반복/스테일 방지

- `card_candidates.py`: 현재 state/event/objective 기준 card candidate pool을 만든다.
- `card_candidate_modifiers.py`: repeat/frequency/fallback/ontology 등 후보 점수 modifier 상수와 계산.
- `card_candidate_json.py`: candidate/card trace를 JSON에 기록 가능한 형태로 변환.
- `card_selection.py`: candidate pool에서 실제 presented card 3장을 고른다.
- `card_staleness.py`: 완료된 objective에 묶인 stale choice를 필터링한다.
- `repeat_memory.py`: repeat group, cooldown tag, long-run frequency memory를 관리한다.

### 퀘스트, objective, lifecycle

- `quest_objectives.py`: objective 완료 여부, quest report, required objective 상태 계산.
- `quest_lifecycle.py`: quest 완료 reward, run 종료, 다음 quest 전환 lifecycle 처리.
- `quest_sequence.py`: scenario의 `quest_sequence`를 따라 다음 foundation quest를 로드한다.
- `objective_scoring.py`: objective 상태에 따른 score delta 계산.

### 디렉터와 온톨로지

- `director_scoring.py`: storylet/event scoring, situation intent rotation, next event tag bonus, recency penalty, clue/omen follow-up 우선순위.
- `game_semantics.py`: FateWeaver에 너무 묶이지 않은 범용 semantic rule evaluator 계층.
- `ontology_reasoner.py`: `data/core/ontology.yaml`을 읽고 FateWeaver state에 맞춘 ontology-lite inference를 수행하는 adapter.
- `ontology_validator.py`: ontology YAML 구조 검증.

### 기존 콘솔/시뮬레이션 계층

- `data_loader.py`: `data/core`, `data/content`, `data/scenarios`를 로드해 bundle/scenario를 만든다.
- `validator.py`: bundle/scenario validation.
- `scenario_filter.py`: scenario include/exclude 조건에 맞게 event를 필터링한다.
- `simulator.py`, `choice_resolver.py`, `choice_scoring.py`, `event_selector.py`, `state_manager.py`: 초기 console simulator 계층과 choice/event/state 보조 로직.
- `logger.py`, `analyzer.py`: run log 저장/분석.
- `models.py`: 공통 모델 타입.
- `yaml_utils.py`: YAML 로딩 유틸리티.

### Text MUD 출력

- `text_mud_log.py`: JSON run log에서 Text MUD 파일 저장.
- `text_mud_turns.py`: turn-by-turn 문장 구성.
- `text_mud_objectives.py`: objective/quest 상태 문장 구성.
- `text_mud_report.py`: quest report/ending 요약 문장 구성.
- `text_mud_values.py`: resource delta 등 값 표현 helper.

## 4. 데이터 구조: `data/`

### `data/core/`

- `card_rules.yaml`: 카드 규칙의 core 계약, 기본 비용, combo/conflict, `p0_cards` 루트.
- `choice_types.yaml`: 선택 타입 정의.
- `item_roles.yaml`: item role 분류.
- `ontology.yaml`: entity/relation/fact/rule/situation intent 기반 ontology-lite 원천.
- `result_rules.yaml`: 결과 적용 규칙.
- `score_rules.yaml`: score/objective/ending 관련 규칙.
- `statuses.yaml`: health, food, money, reputation, curse 등 상태 정의.
- `tags.yaml`: event/card/objective tag vocabulary.

### `data/content/`

- `base/`: 공통 endings, events, items, quests, regions.
- `quests/`: 카테고리별 quest 정의.
- `events/`: 카테고리별 storylet/event hint 정의.
- `card_rules/`: 카테고리별 card rule split 파일.

대표 카테고리:

- `survival_exploration`
- `travel_delivery_escort`
- `local_problem`
- `investigation_mystery`
- `defense_threat`
- `ruin_dungeon_ritual`

### `data/scenarios/`

실행 가능한 scenario YAML 모음이다. 핵심 baseline은:

- `standard_run_25_35_turn.yaml`: 현재 Standard Run 검증 기준. `survive_the_storm_pass`에서 시작하고 `hidden_grove_discovery`로 이어지는 quest sequence를 가진다.

그 외 파일은 tutorial, success/partial/failure fixture, category probe, regression scenario다.

## 5. 도구 구조: `tools/`

- `console_simulator.py`: 초기 console simulator 실행기.
- `validate_data.py`: data/scenario validation CLI.
- `analyze_logs.py`: 저장된 run log 분석.
- `manual_choice_runner.py`: 1/2/3 수동 선택 또는 choice sequence/agent policy로 Standard Run을 실제 state transition과 함께 실행한다.
- `manual_choice_runner_types.py`: manual runner argument/error 타입.
- `manual_choice_runner_trace.py`: manual choice trace entry 생성.
- `manual_choice_runner_output.py`: manual runner JSON/Text MUD/trace/summary 출력.
- `manual_choice_runner_report.py`: 사람이 읽는 manual run report 생성.
- `manual_choice_runner_agents.py`: deterministic 5 subagent policy. goal-focused, safety-first, risk-seeking, explorer, contrarian.
- `manual_choice_runner_batch.py`: seed x agent batch 실행.
- `manual_choice_runner_batch_metrics.py`: batch 결과 metric 집계.
- `manual_choice_runner_batch_report.py`: batch summary/report 생성.

## 6. 테스트 구조: `tests/`

테스트는 `python -m unittest` 기준이다.

핵심 테스트 그룹:

- `test_gameplay_p0_standard_run.py`, `test_gameplay_p0.py`: Standard Run과 gameplay baseline.
- `test_gameplay_p0_card_candidates.py`, `test_gameplay_p0_card_repetition_gate.py`: card candidate/repetition 회귀.
- `test_manual_choice_runner.py`: manual choice runner 안정성, invalid choice, exhaustion, max turn.
- `test_manual_choice_runner_onboarding.py`: quest onboarding trace와 3-card invariant.
- `test_manual_choice_runner_relevance.py`: card relevance/off-quest/fallback trace.
- `test_manual_choice_runner_report.py`, `test_manual_choice_runner_batch.py`: report/batch/subagent policy.
- `test_quest_completion_lifecycle.py`, `test_quest_sequence_transition.py`: quest 완료, 보상, 종료, 전환 lifecycle.
- `test_game_semantics.py`, `test_ontology_reasoner.py`, `test_ontology_validator.py`: semantic layer와 ontology-lite.
- `test_text_mud_log.py`: Text MUD 출력.
- `test_data_loader.py`, `test_validator.py`, `test_scenario_filter.py`: 데이터 로딩/검증.

주의: 테스트 파일명에는 과거 P0 작업명 때문에 `gameplay_p0`가 남아 있다. 현재 소스 모듈명과 1:1로 대응하지 않을 수 있다.

## 7. 문서 구조: `docs/`

문서 전체 색인은 `docs/00_index/README_Docs_Index.md`다.

- `docs/01_foundation/`: 프로젝트 기준선, 구조 가이드, 데이터 아키텍처, 게임 구조 재정의.
- `docs/02_schema/`: YAML schema, Flutter export contract, quest/card schema, ontology core model.
- `docs/03_specs/`: console simulator, Text MUD simulator spec.
- `docs/04_codex/`: Codex 작업 시작 문서와 task brief.
- `docs/05_validation/`: validation checklist, human playtest protocol, feedback form.
- `docs/06_plans/`: 구현 계획, content expansion, ontology/director roadmap, P1 backlog.
- `docs/07_reviews/`: 작업 결과, audit, gate result, milestone freeze 기록.

최근 중요한 review/gate 결과:

- `docs/07_reviews/64_Manual_Choice_Driven_Standard_Run_Runner_Result_v0.1.md`
- `docs/07_reviews/65_Manual_Choice_Runner_Robustness_Gate_Result_v0.1.md`
- `docs/07_reviews/66_Completed_Objective_Choice_Refresh_Gate_Result_v0.1.md`
- `docs/07_reviews/67_Quest_Onboarding_Flow_Gate_Result_v0.1.md`
- `docs/07_reviews/68_Choice_Relevance_Noise_Gate_Result_v0.1.md`
- `docs/07_reviews/69_Manual_Run_Trace_Report_Subagent_Batch_Gate_Result_v0.1.md`
- `docs/07_reviews/70_Quest_Completion_Lifecycle_Reward_Gate_Result_v0.1.md`
- `docs/07_reviews/71_Subagent_Batch_Quality_Baseline_Gate_Result_v0.2.md`
- `docs/07_reviews/72_Quest_Sequence_Transition_Gate_Result_v0.1.md`

## 8. 자주 쓰는 검증 명령

```bash
python -m unittest
python -m compileall src tools tests
python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
```

Manual choice runner 예시:

```bash
python tools/manual_choice_runner.py \
  --scenario data/scenarios/standard_run_25_35_turn.yaml \
  --seed 202 \
  --choices 1,2,3,1,2,3 \
  --output-dir logs/manual_runs
```

Subagent batch 예시:

```bash
python tools/manual_choice_runner_batch.py \
  --scenario data/scenarios/standard_run_25_35_turn.yaml \
  --seeds 202,303,404 \
  --output-dir logs/manual_batch
```

## 9. ChatGPT가 먼저 읽으면 좋은 순서

1. 이 파일: `PROJECT_STRUCTURE_FOR_CHATGPT.md`
2. 전체 문서 색인: `docs/00_index/README_Docs_Index.md`
3. 현재 baseline: `docs/01_foundation/00_Project_FateWeaver_Current_Baseline_v0.7.md`
4. 게임 구조: `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
5. quest/card 계약: `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
6. Standard Run scenario: `data/scenarios/standard_run_25_35_turn.yaml`
7. 실행 엔진: `src/fateweaver/gameplay_run.py`
8. manual runner: `tools/manual_choice_runner.py`
9. 최신 gate 결과: `docs/07_reviews/70_Quest_Completion_Lifecycle_Reward_Gate_Result_v0.1.md`, `docs/07_reviews/71_Subagent_Batch_Quality_Baseline_Gate_Result_v0.2.md`, `docs/07_reviews/72_Quest_Sequence_Transition_Gate_Result_v0.1.md`

