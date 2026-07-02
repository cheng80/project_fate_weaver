# [Current] Ontology Core To Director Loop Result v0.1

> 상태: [Current] Ontology Core Model Replan 이후 O2~O6 ULW Loop 구현 결과.

## 1. 작업 목적

이번 작업은 Ontology-lite/tag matching layer 위에 deterministic Ontology Core, Validator, Reasoner-lite, Situation Director-lite event weighting을 얹는 첫 구현 루프다.

기존 tag 구조, Quest/Card/Event/Item/Ending data, active scenario, Standard Run을 유지하면서 Entity / Relation / Fact / Rule 기반 inference trace를 런타임 로그에 노출했다.

## 2. Phase Gate 결과

| Phase | 결과 | Evidence |
| --- | --- | --- |
| O2 Ontology Seed Data | PASS | `ontology_core` seed: Entity 24, Relation 21, Fact/State Fact 18, Rule 10, Situation Intent 8 |
| O3 Ontology Validator | PASS | `tests.test_ontology_validator` 4 tests PASS, `tools/validate_data.py --ontology` PASS |
| O4 Reasoner-lite | PASS | `tests.test_ontology_reasoner` 3 tests PASS, inference output/trace sample 확인 |
| O5 Situation Director-lite | PASS | `tests.test_situation_director_lite` 4 tests PASS, quest gate/cooldown hard block 보존 |
| O6 Standard Run 재검증 | PASS with risk | 25 turns, Day 7, `prepared_frontier_route`, clues 3, omens 1, ontology trace 25 turns |

## 3. 구현 요약

- `data/core/ontology.yaml`
  - 기존 `ontology`, `entities`, `relations` Ontology-lite 구조는 유지했다.
  - 새 `ontology_core` 섹션을 추가했다.
  - category seed는 `local_problem`, `investigation_mystery`, `survival_exploration`을 포함한다.

- `src/fateweaver/ontology_validator.py`
  - duplicate id, relation subject/object, fact subject/object, rule ref, rule weight tag, situation intent tag를 검증한다.
  - `tools/validate_data.py --ontology`로 실행 가능하다.

- `src/fateweaver/ontology_reasoner.py`
  - `OntologyReasonerContext`와 `run_reasoner`를 추가했다.
  - output은 `event_weight_modifiers`, `card_weight_modifiers`, `situation_intents`, `next_facts`, `trace`다.
  - LLM reasoning, OWL/RDF/SPARQL은 사용하지 않았다.

- `src/fateweaver/gameplay_rules.py`
  - `select_storylet`에 optional `ontology_inference`를 추가했다.
  - ontology event weight는 quest/region gate 이후, requirements/cooldown/max occurrence hard block 이후에만 적용된다.
  - 실제 selection weight 반영은 `+1` cap으로 제한했다.

- `src/fateweaver/gameplay_run.py`
  - 각 turn마다 reasoner를 먼저 실행하고 event selection에 제한 반영한다.
  - run JSON turn log에 `ontology_inference`와 `ontology_weight_applied`를 기록한다.

## 4. Standard Run 결과

실행:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/standard_run_25_35_turn.yaml --seed 42 --runs 1 --logs .omo/ulw-loop/evidence/ontology-core-to-director-20260701/standard-run --profile balanced
```

결과:

- turn count: 25
- final day: 7
- ending: `prepared_frontier_route`
- clues: 3
- omens: 1
- ontology trace turns: 25
- ontology weight applied nonzero turns: 19
- top repeated cards:
  - `ration_the_last_supplies`: 15
  - `buy_local_hint`: 13
  - `enter_deep_woods`: 7

판정:

- Standard Run은 깨지지 않았다.
- Event selection에 ontology trace와 제한 weight가 붙었다.
- 카드 반복도는 기존 baseline의 `ration_the_last_supplies` 15/25, `buy_local_hint` 13/25에서 의미 있게 개선되지 않았다.
- 이번 O5는 Event weighting만 제한 반영했기 때문에 Card Candidate repetition 개선까지 책임지지 않는다.

## 5. Hard Block 보존

다음 조건은 ontology weight가 우회하지 못하게 테스트로 고정했다.

- `quest_ids` gate
- event requirement gate
- `cooldown_turns`
- `max_occurrences_per_run`

`select_storylet`는 먼저 quest/region pool을 만들고, inference가 있을 때도 동일한 event eligibility 조건을 통과한 이벤트에만 weight를 적용한다.

## 6. 하지 않은 작업

- Quest/Card/Event/Item/Ending 추가 없음.
- 기존 tag 구조 폐기 없음.
- Storylet Pool 대규모 재작성 없음.
- LLM runtime reasoning 없음.
- OWL/RDF/SPARQL 없음.
- card selection score에는 ontology output을 아직 반영하지 않음.

## 7. 남은 리스크

1. Card repetition 개선 미달
   - O5 event weighting만으로는 top repeated card가 15에서 내려가지 않았다.
   - 다음 루프는 Card Candidate repetition memory 또는 Reasoner-lite card modifier를 별도 gate로 다뤄야 한다.

2. `ontology_core` seed coverage
   - 현재 seed는 Standard Run과 세 category 중심이다.
   - 전체 Quest category coverage는 아직 아니다.

3. Rule vocabulary 안정성
   - validator는 현재 seed schema 기준이다.
   - 후속으로 `add_facts`, `remove_facts`, `ontology_refs`를 추가하면 validator rule grammar를 확장해야 한다.

## 8. 검증 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_ontology_validator
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_ontology_reasoner
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_situation_director_lite
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```
