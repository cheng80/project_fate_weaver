# [Current] Quest Expansion Refactor Gate v0.1

> 상태: [Current] Phase 3 Bulk Fill과 Phase 4 Coverage Audit 이후, Bulk Fill 2차 전에 데이터/룰/이벤트/시나리오/코드 분리 필요성을 판정한 문서.

## 1. 작업 목적

이번 작업은 실제 리팩터링 실행이 아니라 Refactor Gate 판정이다.

목표는 Bulk Fill 2차 전에 다음을 판단하는 것이다.

- `quests.yaml`, `card_rules.yaml`, `events.yaml`, `scenarios/`가 현재 구조로 더 커져도 되는가
- split file 구조가 필요하다면 어느 영역이 먼저인가
- split 전에 loader 지원이 필요한가
- quest_ids gate 누락과 중복 패턴이 Bulk Fill 2차의 리스크가 되는가
- 관련 code 파일이 지금 리팩터링 대상인가

이번 작업에서는 `data/`, `src/`, `tests/`, `tools/`를 수정하지 않는다.

## 2. 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/34_Quest_Category_Bulk_Fill_Result_v0.1.md`
- `docs/07_reviews/35_Quest_Expansion_Coverage_Audit_v0.1.md`

## 3. 현재 확장 규모

Phase 4 Coverage Audit 이후 현재 확장 규모는 다음과 같다.

| 항목 | 수 |
|---|---:|
| 구현 Quest | 22 |
| Catalog unique 후보 | 56 |
| 구현 coverage | 약 39.3% |
| Scenario 파일 | 51 |
| active quest scenario | 47 |
| Card Rule | 111 |
| `quest_ids` 보유 Card Rule | 100 |
| Event | 55 |
| card candidate hint 보유 Event | 42 |
| `quest_ids` 보유 Event | 24 |
| test 파일 | 20 |

Bulk Fill 2차를 같은 방식으로 진행하면 Quest, Card Rule, Event, Scenario가 모두 선형 증가한다. 특히 Card Rule은 이미 2,000 LOC를 넘었기 때문에 다음 bulk 전에 분리 전략이 필요하다.

## 4. 데이터 파일 현황

| 파일 | LOC | 주요 entry 수 | Gate |
|---|---:|---:|---|
| `data/content/base/quests.yaml` | 1,648 | Quest 22 | Needs Loader Support First |
| `data/core/card_rules.yaml` | 2,134 | Card 111, combo 2, conflict 1 | Split Before Bulk Fill 2 |
| `data/content/base/events.yaml` | 1,317 | Event 55 | Split Recommended Later |
| `data/core/score_rules.yaml` | 24 | `score_rules` 1 block | Keep As-Is |

### quests.yaml

`quests.yaml`은 아직 Quest 22개지만 이미 1,648 LOC다. Catalog에는 non-deferred 후보 34개가 남아 있어 Bulk Fill 2차 이후에는 사람이 특정 Category Quest를 찾는 비용이 커진다.

다만 `src/fateweaver/gameplay_setup.py`의 `load_foundation()`은 현재 `data/content/base/quests.yaml`을 고정 경로로 읽는다. 따라서 Quest split은 실행 자체보다 loader 지원이 선행되어야 한다.

판정: **Needs Loader Support First**.

### card_rules.yaml

`card_rules.yaml`은 2,134 LOC, Card Rule 111개로 가장 큰 리스크다.

현재 Card Rule 분포:

| 항목 | 수 |
|---|---:|
| 전체 Card Rule | 111 |
| `quest_ids` 보유 | 100 |
| shared Card Rule | 11 |
| combo rule | 2 |
| conflict rule | 1 |

Slot 분포:

| slot | 수 |
|---|---:|
| `quest_progress` | 66 |
| `resource_alternative` | 25 |
| `risk_discovery` | 20 |

Bulk Fill 2차가 같은 패턴으로 진행되면 Quest마다 3-5개 rule이 추가된다. 이 파일은 split 우선순위 1순위다.

판정: **Split Before Bulk Fill 2**. 단, `gameplay_setup.py`가 아직 고정 경로로 읽으므로 실제 split 전 loader support가 필요하다.

### events.yaml

`events.yaml`은 1,317 LOC, Event 55개다. `card_candidate_hints`를 가진 Event는 42개이고, `quest_ids` gate를 가진 Event는 24개다.

`src/fateweaver/data_loader.py`는 scenario `content_sources`를 순회해 여러 content YAML을 읽을 수 있다. 따라서 Event split 자체는 Quest/Card보다 자연스럽다. 하지만 현재 scenario 파일이 어떤 content source를 포함하는지에 의존하므로, 무계획 split은 scenario 수정 비용을 만든다.

판정: **Split Recommended Later**.

### score_rules.yaml

`score_rules.yaml`은 24 LOC로 작고 책임도 명확하다.

판정: **Keep As-Is**.

## 5. Scenario 현황

현재 `data/scenarios/`는 flat 구조이며 파일 수는 51개다.

| 구분 | 수 |
|---|---:|
| 전체 scenario | 51 |
| active quest scenario | 47 |
| non-quest scenario | 4 |
| success 또는 general success | 23 |
| partial | 11 |
| failure | 13 |

그룹별 active quest scenario:

| 그룹 | 수 |
|---|---:|
| Foundation | 17 |
| Probe | 18 |
| Bulk | 12 |

Quest별 scenario filename은 현재 일관성이 있다. naming issue는 발견되지 않았다.

`tools/validate_data.py`는 단일 `--scenario` 파일을 받는다. 즉 `data/scenarios/foundation/`, `data/scenarios/probe/`, `data/scenarios/bulk/` 같은 계층 구조로 이동하려면 기존 테스트/검증 명령의 path 업데이트가 필요하다.

판정: **Split Recommended Later**. Bulk Fill 2차 전 필수는 아니지만, 75개 전후에 도달하기 전에 group 기준을 정해야 한다.

## 6. Code 파일 현황

| 파일 | LOC | 함수 | 클래스 | Any/type ignore/cast | Gate |
|---|---:|---:|---:|---|---|
| `src/fateweaver/data_loader.py` | 284 | 22 | 2 | 없음 | Keep As-Is |
| `src/fateweaver/gameplay_setup.py` | 218 | 21 | 5 | ignore 1 | Needs Loader Support First |
| `src/fateweaver/card_candidates.py` | 284 | 21 | 1 | 없음 | Keep As-Is |
| `src/fateweaver/card_selection.py` | 86 | 8 | 0 | 없음 | Keep As-Is |
| `src/fateweaver/quest_objectives.py` | 270 | 23 | 2 | 없음 | Keep As-Is |
| `src/fateweaver/objective_scoring.py` | 57 | 3 | 0 | 없음 | Keep As-Is |
| `src/fateweaver/text_mud_turns.py` | 192 | 21 | 0 | 없음 | Keep As-Is |
| `src/fateweaver/text_mud_report.py` | 44 | 3 | 0 | 없음 | Keep As-Is |

코드 파일은 현재 LOC warning의 주 원인이 아니다. 실제 split을 막는 핵심 지점은 `gameplay_setup.py`의 fixed-path 로딩이다.

현재 로딩 구조:

- `data_loader.py`: scenario `content_sources`를 통해 여러 content YAML을 순회한다.
- `gameplay_setup.py`: `data/content/base/quests.yaml`, `data/core/card_rules.yaml`, `data/core/score_rules.yaml`을 직접 읽는다.

따라서 code refactor 우선순위는 대규모 분리가 아니라 `gameplay_setup.py`에 split-aware loading을 추가할지 결정하는 것이다.

## 7. quest_ids Gate 리스크

Card Rule gate:

| 항목 | 수 |
|---|---:|
| 전체 Card Rule | 111 |
| `quest_ids` 보유 Card Rule | 100 |
| shared Card Rule | 11 |

`herb_gathering_tutorial`은 shared foundation card를 사용하므로 quest_ids 기반 Card Rule coverage에서 비어 있다. 이는 현재 의도된 legacy/shared 구조로 볼 수 있다.

Event gate:

| 항목 | 수 |
|---|---:|
| 전체 Event | 55 |
| card candidate hint 보유 Event | 42 |
| `quest_ids` 보유 Event | 24 |

Event `quest_ids`가 없는 active Quest:

- `herb_gathering_tutorial`
- `forest_path_scouting_tutorial`
- `missing_porter_search_intro`
- `merchant_lost_pack_recovery`
- `village_well_trouble`
- `ruin_mark_investigation_intro`
- `defend_the_village_night`
- `ghost_town_medicine_run`
- `old_well_awakening`
- `survive_the_storm_pass`

해석:

- Phase 3 Bulk Event는 gate 적용이 되어 있다.
- Foundation/Probe 쪽은 older/shared event 구조가 남아 있다.
- Bulk Fill 2차 전에 새 Bulk Quest에 `quest_ids` gate를 강제하는 check가 필요하다.

판정: **Small Cleanup Needed**. 데이터 변경이 아니라 validator/test 또는 audit check 설계가 먼저다.

## 8. 중복 패턴 / 유지보수 리스크

현재 중복 리스크는 코드보다 데이터에 있다.

주요 반복 패턴:

- Bulk Quest마다 success-only scenario 1개
- Quest마다 `quest_progress`, `risk_discovery`, `resource_alternative` card set 반복
- Bulk Event마다 `card_candidate_hints`, `cooldown_tags`, `repeat_group`, `quest_ids` 반복
- Category별 tag/region/quest_id naming 패턴이 단일 파일에 혼재

중복 자체는 현재 gameplay rule 변경 없이 작동한다. 문제는 Bulk Fill 2차 이후 누락 탐지가 어려워지는 것이다.

## 9. Split 후보

### Quest

권장 후보:

```text
data/content/quests/foundation.yaml
data/content/quests/local_problem.yaml
data/content/quests/investigation_mystery.yaml
data/content/quests/defense_threat.yaml
data/content/quests/travel_delivery_escort.yaml
data/content/quests/ruin_dungeon_ritual.yaml
data/content/quests/survival_exploration.yaml
```

필수 선행:

- `gameplay_setup.py`가 `data/content/base/quests.yaml` 단일 파일과 `data/content/quests/*.yaml` 병합을 모두 지원해야 한다.
- duplicate quest id check가 필요하다.

### Card Rule

권장 후보:

```text
data/core/card_rules.yaml
data/content/card_rules/foundation.yaml
data/content/card_rules/local_problem.yaml
data/content/card_rules/investigation_mystery.yaml
data/content/card_rules/defense_threat.yaml
data/content/card_rules/travel_delivery_escort.yaml
data/content/card_rules/ruin_dungeon_ritual.yaml
data/content/card_rules/survival_exploration.yaml
```

`data/core/card_rules.yaml`에는 shared cards, combo rules, conflict rules만 남기고, quest-specific cards는 category 파일로 옮기는 구조가 가장 낫다.

필수 선행:

- card rule 병합 순서 정의
- duplicate card id check
- shared card와 quest-scoped card의 위치 규칙
- `quest_ids` gate 누락 check

### Event

권장 후보:

```text
data/content/base/events.yaml
data/content/events/local_problem.yaml
data/content/events/investigation_mystery.yaml
data/content/events/defense_threat.yaml
data/content/events/travel_delivery_escort.yaml
data/content/events/ruin_dungeon_ritual.yaml
data/content/events/survival_exploration.yaml
```

Event split은 `data_loader.py`의 `content_sources` 구조와 잘 맞지만, scenario source 목록을 어떻게 유지할지 결정해야 한다.

### Scenario

권장 후보:

```text
data/scenarios/foundation/
data/scenarios/probe/
data/scenarios/bulk/
```

현재는 flat 구조 유지가 더 안전하다. 이동은 검증 명령과 테스트 path 정렬이 필요하다.

## 10. Gate 판정

| 대상 | 판정 | 이유 |
|---|---|---|
| `quests.yaml` | Needs Loader Support First | 1,648 LOC, 22 Quest. split 필요성은 있으나 loader가 fixed path다. |
| `card_rules.yaml` | Split Before Bulk Fill 2 | 2,134 LOC, 111 cards. 다음 bulk에서 가장 먼저 관리 한계가 온다. |
| `events.yaml` | Split Recommended Later | 1,317 LOC, 55 events. split 가능성은 높지만 scenario source 전략이 먼저다. |
| `score_rules.yaml` | Keep As-Is | 24 LOC. 책임이 작고 안정적이다. |
| `scenarios/` | Split Recommended Later | 51 files, naming consistent. 이동 전 validate/test path 전략 필요. |
| `data_loader.py` | Keep As-Is | content source 순회가 이미 있어 event split 기반은 있다. |
| `gameplay_setup.py` | Needs Loader Support First | Quest/Card split의 병목이다. |
| `card_candidates.py` | Keep As-Is | 284 LOC, 책임이 candidate scoring/presentation으로 명확하다. |
| `card_selection.py` | Keep As-Is | 86 LOC, 책임 작음. |
| `quest_objectives.py` | Keep As-Is | 270 LOC, 현재 split gate의 병목은 아니다. |
| `objective_scoring.py` | Keep As-Is | 57 LOC. |
| `text_mud_turns.py` / `text_mud_report.py` | Keep As-Is | 직전 refactor 이후 LOC와 책임이 안정적이다. |

최종 판정:

```text
Bulk Fill 2차 전에 실제 split을 바로 실행하지 않는다.
먼저 gameplay_setup split loader support와 gate 검사를 설계/구현한 뒤,
card_rules.yaml부터 category split을 실행한다.
```

## 11. Bulk Fill 2차 전 필수 작업

Bulk Fill 2차 전에 반드시 필요한 작업:

1. `gameplay_setup.py`의 Quest/Card Rule split-aware loader 설계
2. `card_rules.yaml` split migration plan 작성
3. duplicate quest id / card id 검증 기준 추가
4. 새 Bulk Quest의 Card Rule `quest_ids` gate 필수 check 정의
5. 새 Bulk Event Hint의 `quest_ids` gate 필수 check 정의
6. 기존 flat scenario 구조를 유지할지, group path를 도입할지 결정

Bulk Fill 2차 전에 아직 필수는 아닌 작업:

- Event 파일 category split 실행
- Scenario 파일 실제 이동
- Text MUD 출력 리팩터링
- Gameplay rule 변경
- Small Schema Extension

## 12. 권장 후속 작업

추천 순서:

1. Refactor Plan 문서 작성: Quest/Card/Event/Scenario split 순서와 rollback 기준 고정
2. Loader support 구현: 기존 단일 파일 경로와 새 split 경로를 동시에 지원
3. Card Rule split: shared/core와 category-specific card 분리
4. Quest split: category별 Quest 파일 분리
5. Event split: scenario content source 전략 확정 후 진행
6. Scenario grouping: 파일 수가 75개 전후가 되기 전에 group path 도입 여부 결정
7. Bulk Fill 2차: 위 gate 통과 후 lightweight success fixture 중심으로 재개

## 13. 실행한 검증

이번 문서 작성 전에 read-only 측정으로 다음을 확인했다.

- 데이터 파일 LOC
- Quest / Card / Event / Scenario entry 수
- Card Rule slot 분포
- Card Rule `quest_ids` 적용 수
- Event `quest_ids` 적용 수
- Scenario filename consistency
- Code file LOC / 함수 수 / 클래스 수 / Any 및 ignore 사용 여부
- `data_loader.py`와 `gameplay_setup.py`의 loading 책임 차이

Evidence:

- `.omo/ulw-loop/evidence/quest-expansion-refactor-gate-metrics.txt`
- `.omo/ulw-loop/evidence/quest-expansion-refactor-gate-metrics.py`

## 14. 남은 문제

- `gameplay_setup.py`가 split-aware loader를 아직 지원하지 않는다.
- `card_rules.yaml`은 2,134 LOC로 Bulk Fill 2차 전에 가장 먼저 분리 계획이 필요하다.
- Event `quest_ids` gate는 Bulk 쪽 중심으로 적용되어 있고 Foundation/Probe 쪽은 older/shared 구조가 남아 있다.
- Scenario flat 구조는 지금은 유지 가능하지만 Bulk Fill이 한 번 더 진행되면 탐색성이 떨어질 수 있다.
- Type Catalog의 구현 상태 drift는 별도 갱신이 필요하다.

