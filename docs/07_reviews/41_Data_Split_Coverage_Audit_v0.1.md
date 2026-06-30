# [Current] Data Split Coverage Audit v0.1

> 상태: [Current] Card Rules / Quest Data / Event Hint split 이후 loaded inventory와 cross-reference 정합성을 감사한 문서.

## 1. 작업 목적

이번 작업은 Content Enrichment Ultraresearch v0.2의 선행 조건을 충족하기 위한 Data Split Coverage Audit이다.

직전 작업에서 Event Hint Split은 완료되었지만, `docs/07_reviews/41_Data_Split_Coverage_Audit_v0.1.md`가 없어 Content Enrichment Ultraresearch가 PARTIAL로 멈췄다.

이번 감사는 구현 작업이 아니다. `data/`, `src/`, `tests/`를 수정하지 않고, Card Rules / Quest Data / Event Hint split 이후 loaded inventory와 cross-reference 정합성을 수치화한다.

## 2. 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/07_reviews/35_Quest_Expansion_Coverage_Audit_v0.1.md`
- `docs/07_reviews/36_Quest_Expansion_Refactor_Gate_v0.1.md`
- `docs/07_reviews/37_Data_Split_Loader_Support_Result_v0.1.md`
- `docs/07_reviews/38_Card_Rules_Category_Split_Migration_Result_v0.1.md`
- `docs/07_reviews/39_Quest_Data_Split_Loader_Support_Result_v0.1.md`
- `docs/07_reviews/40_Event_Hint_Split_Loader_Support_Result_v0.1.md`
- `/Users/cheng80/Desktop/CODEX_TASK_Data_Split_Coverage_Audit_v0.1.md`

## 3. Split 구조 요약

현재 split 구조는 다음 세 축으로 정리되어 있다.

| 축 | Base/Core | Split 위치 | Loader 동작 |
|---|---|---|---|
| Card Rules | `data/core/card_rules.yaml` | `data/content/card_rules/*.yaml` | core 먼저 읽고 split files를 sorted glob으로 병합 |
| Quest Data | `data/content/base/quests.yaml` | `data/content/quests/*.yaml` | base 먼저 읽고 split files를 sorted glob으로 병합 |
| Event Hint | `data/content/base/events.yaml` | `data/content/events/*.yaml` | scenario가 base events를 포함하면 split events도 sorted glob으로 병합 |

Base/Core 파일은 기존 호환과 shared/foundation 데이터를 맡고, split file은 category별 quest-specific 데이터를 맡는다.

## 4. Loaded Inventory

실제 loader와 raw YAML 병합 기준 inventory는 다음과 같다.

| 항목 | 수 | 기대값 | 결과 |
|---|---:|---:|---|
| Loaded Quest IDs | 22 | 22 | PASS |
| Loaded Card IDs | 111 | 111 | PASS |
| Loaded Event IDs | 55 | 55 | PASS |
| Scenario files | 51 | 51 | PASS |
| Active quest scenarios | 47 | 47 | PASS |
| Card Rule with `quest_ids` | 100 | 100 | PASS |
| Event with `card_candidate_hints` | 42 | 42 | PASS |
| Event with `quest_ids` | 24 | 24 | PASS |

Loader smoke 결과:

- `load_quest_mapping()` merged quests: 22
- `load_card_rule_mapping()` merged card rules: 111
- `load_foundation(..., "hidden_grove_discovery")` card rules: 111
- `load_project_data(..., "data/scenarios/hidden_grove_discovery.yaml")` events: 55

## 5. Quest Split Coverage

Quest split 구조:

```text
data/content/base/quests.yaml
data/content/quests/foundation.yaml
data/content/quests/local_problem.yaml
data/content/quests/investigation_mystery.yaml
data/content/quests/defense_threat.yaml
data/content/quests/travel_delivery_escort.yaml
data/content/quests/ruin_dungeon_ritual.yaml
data/content/quests/survival_exploration.yaml
```

Quest source별 수량:

| Source | Quest 수 |
|---|---:|
| `data/content/base/quests.yaml` | 4 |
| `data/content/quests/foundation.yaml` | 0 |
| `data/content/quests/local_problem.yaml` | 3 |
| `data/content/quests/investigation_mystery.yaml` | 4 |
| `data/content/quests/defense_threat.yaml` | 3 |
| `data/content/quests/travel_delivery_escort.yaml` | 4 |
| `data/content/quests/ruin_dungeon_ritual.yaml` | 2 |
| `data/content/quests/survival_exploration.yaml` | 2 |
| 합계 | 22 |

판정:

- Foundation Quest 4개는 base file에 남아 있다.
- `foundation.yaml`은 category 구조 고정을 위한 빈 split file이다.
- Stable Category split files는 전체 18개 Quest를 보유한다.
- 전체 loaded Quest 수는 기대값 22개를 유지한다.

## 6. Card Rules Split Coverage

Card Rules split 구조:

```text
data/core/card_rules.yaml
data/content/card_rules/local_problem.yaml
data/content/card_rules/investigation_mystery.yaml
data/content/card_rules/defense_threat.yaml
data/content/card_rules/travel_delivery_escort.yaml
data/content/card_rules/ruin_dungeon_ritual.yaml
data/content/card_rules/survival_exploration.yaml
```

Card source별 수량:

| Source | Card Rule 수 |
|---|---:|
| `data/core/card_rules.yaml` | 29 |
| `data/content/card_rules/local_problem.yaml` | 13 |
| `data/content/card_rules/investigation_mystery.yaml` | 20 |
| `data/content/card_rules/defense_threat.yaml` | 13 |
| `data/content/card_rules/travel_delivery_escort.yaml` | 18 |
| `data/content/card_rules/ruin_dungeon_ritual.yaml` | 10 |
| `data/content/card_rules/survival_exploration.yaml` | 8 |
| 합계 | 111 |

판정:

- Core file에는 shared/foundation card와 multi-select rule이 남아 있다.
- Split card rules는 모두 category별 quest-specific card로 분리되어 있다.
- 전체 loaded Card Rule 수는 기대값 111개를 유지한다.
- `quest_ids`가 있는 Card Rule은 100개다.
- shared/core Card Rule 11개는 기존 호환상 `quest_ids`가 없을 수 있다.

## 7. Event Hint Split Coverage

Event Hint split 구조:

```text
data/content/base/events.yaml
data/content/events/foundation.yaml
data/content/events/local_problem.yaml
data/content/events/investigation_mystery.yaml
data/content/events/defense_threat.yaml
data/content/events/travel_delivery_escort.yaml
data/content/events/ruin_dungeon_ritual.yaml
data/content/events/survival_exploration.yaml
```

Event source별 수량:

| Source | Event 수 |
|---|---:|
| `data/content/base/events.yaml` | 31 |
| `data/content/events/foundation.yaml` | 0 |
| `data/content/events/local_problem.yaml` | 4 |
| `data/content/events/investigation_mystery.yaml` | 6 |
| `data/content/events/defense_threat.yaml` | 4 |
| `data/content/events/travel_delivery_escort.yaml` | 6 |
| `data/content/events/ruin_dungeon_ritual.yaml` | 2 |
| `data/content/events/survival_exploration.yaml` | 2 |
| 합계 | 55 |

Event Hint 속성 coverage:

| 항목 | 수 | 비율 |
|---|---:|---:|
| 전체 Event | 55 | 100.0% |
| `card_candidate_hints` 보유 Event | 42 | 76.4% |
| `quest_ids` 보유 Event | 24 | 43.6% |

판정:

- Base events는 shared/foundation/probe Event와 기존 호환 Event를 보유한다.
- Split events는 Bulk Fill 이후 추가된 quest-specific Event Hint를 보유한다.
- `foundation.yaml`은 category 구조 고정을 위한 빈 split file이다.
- 전체 loaded Event 수는 기대값 55개를 유지한다.

## 8. Scenario Coverage

Scenario inventory:

| 항목 | 수 | 결과 |
|---|---:|---|
| 전체 scenario file | 51 | PASS |
| active quest scenario | 47 | PASS |
| non-quest scenario | 4 | PASS |

Scenario directory는 아직 flat 구조다. 이번 작업은 audit-only 작업이므로 scenario file 이동이나 추가를 하지 않았다.

## 9. Cross-reference 정합성

Cross-reference check 결과:

| Check | 수 | 결과 |
|---|---:|---|
| Unknown Card Rule `quest_ids` | 0 | PASS |
| Unknown Event `quest_ids` | 0 | PASS |
| Unknown Event `card_candidate_hints` | 0 | PASS |

해석:

- 모든 Card Rule `quest_ids`는 loaded Quest id에 존재한다.
- 모든 Event `quest_ids`는 loaded Quest id에 존재한다.
- 모든 Event `card_candidate_hints`는 loaded Card Rule id에 존재한다.
- shared/core Card와 shared/base Event는 기존 호환상 `quest_ids`가 없을 수 있다.

## 10. Duplicate ID Check

Duplicate ID check 결과:

| Check | 중복 수 | 결과 |
|---|---:|---|
| Duplicate Quest ID | 0 | PASS |
| Duplicate Card ID | 0 | PASS |
| Duplicate Event ID | 0 | PASS |

Loader에서도 다음 duplicate check가 유지된다.

- duplicate quest id: 최초 source path와 중복 source path를 포함한 error
- duplicate card rule id: 최초 source path와 중복 source path를 포함한 error
- duplicate event id: 최초 source path와 중복 source path를 포함한 error

## 11. Validator / Test 결과

실행한 검증:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python - <<'PY'
# active quest scenario 47개에 대해 tools/validate_data.py --scenario 실행
PY
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
git diff -- data
git diff -- src
git diff -- tests
```

결과:

| 검증 | 결과 |
|---|---|
| active quest scenario validate | 47 PASS |
| full unittest | 97 tests OK |
| `git diff -- data` | no diff |
| `git diff -- src` | no diff |
| `git diff -- tests` | no diff |

## 12. Content Enrichment 선행 조건 판정

Content Enrichment Ultraresearch v0.2의 선행 조건은 충족된다.

| 선행 조건 | 상태 |
|---|---|
| Event Hint Split 완료 | PASS |
| Data Split Coverage Audit 완료 | PASS |
| Loaded Quest 수 유지 | PASS |
| Loaded Card Rule 수 유지 | PASS |
| Loaded Event 수 유지 | PASS |
| Scenario 수 유지 | PASS |
| duplicate quest/card/event id 0 | PASS |
| unknown quest/card/event cross-reference 0 | PASS |
| validate_data 전체 PASS | PASS |
| unittest PASS | PASS |

따라서 다음 작업은 `CODEX_TASK_Content_Enrichment_Ultraresearch_v0.2.md` 기준의 Content Enrichment Catalog 작성으로 넘어갈 수 있다.

## 13. 리스크

- `data/content/quests/foundation.yaml`과 `data/content/events/foundation.yaml`은 현재 빈 split file이다. 이는 category 구조 고정을 위한 의도된 상태다.
- Event Hint의 `quest_ids` 적용률은 24 / 55다. Shared/foundation/probe Event는 기존 호환성을 위해 base file에 남아 있고 `quest_ids`가 없을 수 있다.
- Scenario directory는 아직 flat 구조다. Scenario 수가 더 늘기 전에 grouping 기준을 별도 작업으로 정하는 것이 좋다.
- Content Enrichment Pack 확장 시 새 quest-specific Card/Event는 반드시 해당 category split file에 추가해야 한다.

## 14. 다음 작업

1. `CODEX_TASK_Content_Enrichment_Ultraresearch_v0.2.md`를 다시 실행해 Content Enrichment Catalog를 작성한다.
2. Pack 1에서 Card Candidate / Clue / Omen 후보를 구현 후보로 좁힌다.
3. Pack 2에서 Item / Ending 후보를 구현 후보로 좁힌다.
4. Pack 확장 이후 Standard Run 25~35 Turn 검증으로 반복도와 run review 품질을 확인한다.
