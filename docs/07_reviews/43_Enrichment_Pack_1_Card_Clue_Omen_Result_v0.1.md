# [Current] Enrichment Pack 1 Card / Clue / Omen Result v0.1

> 상태: [Current] Content Enrichment Pack 1의 Card Candidate / Clue / Omen 데이터 확장 결과 문서.

## 1. 작업 목적

이번 작업은 Content Enrichment 단계의 Pack 1 구현이다.

`docs/06_plans/08_Content_Enrichment_Catalog_v0.1.md`의 Pack 1 후보를 기준으로 실제 데이터에 다음 항목을 반영했다.

| 항목 | 추가 수 | 구현 방식 |
|---|---:|---|
| Card Candidate | 40 | category `card_rules` split files에 `pack1_enrichment` card 추가 |
| Clue | 25 | card `result.gain_clues`로 연결 |
| Omen | 20 | card `result.gain_omens`로 연결 |
| Event Hint | 18 | quest별 `pack1_enrichment` event hint 추가 |

## 2. 하지 않은 것

- Quest 추가
- Item 추가
- Ending 추가
- Standard Run 25~35 Turn 검증
- Bulk Fill 2차
- Storylet Pool 전체 시스템
- Repeat Cooldown 장기 저장
- Flutter / Flame UI

## 3. 변경한 데이터 구조

신규 Card는 기존 split 구조에 맞춰 다음 파일에 추가했다.

| File | Pack 1 Card 수 |
|---|---:|
| `data/content/card_rules/local_problem.yaml` | 7 |
| `data/content/card_rules/investigation_mystery.yaml` | 8 |
| `data/content/card_rules/defense_threat.yaml` | 7 |
| `data/content/card_rules/travel_delivery_escort.yaml` | 7 |
| `data/content/card_rules/ruin_dungeon_ritual.yaml` | 6 |
| `data/content/card_rules/survival_exploration.yaml` | 5 |

신규 Event Hint는 quest별로 단일 `quest_ids` gate를 유지했다.

| File | Pack 1 Event 수 |
|---|---:|
| `data/content/events/local_problem.yaml` | 3 |
| `data/content/events/investigation_mystery.yaml` | 4 |
| `data/content/events/defense_threat.yaml` | 3 |
| `data/content/events/travel_delivery_escort.yaml` | 4 |
| `data/content/events/ruin_dungeon_ritual.yaml` | 2 |
| `data/content/events/survival_exploration.yaml` | 2 |

## 4. Slot Role 분산

| Slot Role | 수 |
|---|---:|
| `quest_progress` | 14 |
| `risk_discovery` | 12 |
| `resource_alternative` | 14 |

권장 범위인 `quest_progress` 12~16, `risk_discovery` 12~16, `resource_alternative` 10~14를 만족한다.

## 5. Post-Pack Inventory

Loader 기준 inventory:

| 항목 | 수 | 변화 |
|---|---:|---|
| Quest | 22 | 유지 |
| Card Rule | 151 | +40 |
| Event | 73 | +18 |
| Ending | 2 | 유지 |

이번 작업에서는 Item Pack을 구현하지 않았고, scenario별 loaded item set도 변경하지 않았다.

## 6. 연결 방식

각 신규 Card는 다음 연결을 가진다.

- `quest_ids`: 단일 Quest id.
- `tags`: `pack1_enrichment` 포함.
- `applies_to_storylet_tags`: Pack 1 Event Hint의 `storylet_tags`와 연결.
- `result.gain_clues` 또는 `result.gain_omens`: Clue/Omen 후보를 실제 결과에 연결.
- `result.quest_progress`: `quest_progress` slot card에서 보조 진행도 기록.
- Event `card_candidate_hints`: 같은 Quest의 Pack 1 Card id를 직접 hint.

이번 작업은 별도 `clues.yaml` / `omens.yaml` 파일을 만들지 않고, 현재 schema가 이미 지원하는 Option A 방식으로 구현했다.

## 7. 검증

추가한 focused test:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_enrichment_pack1
```

검증 기준:

- Pack 1 Card 40개.
- Clue 25개.
- Omen 20개.
- 모든 Pack 1 Card가 같은 Quest의 Event Hint에 연결됨.
- 모든 Pack 1 Event Hint가 단일 `quest_ids` gate를 유지함.

최종 회귀 검증에서는 active quest scenario 47개와 full unittest를 함께 실행한다.

## 8. 다음 작업

1. Pack 2에서 Item +25 / Ending +8을 구현한다.
2. Pack 2 이후 Standard Run 25~35 Turn 검증을 별도 작업으로 수행한다.
3. Standard Run에서 카드 반복도, clue/omen 노출, item 선택지 변화, ending 다양성을 함께 관찰한다.
