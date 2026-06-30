# [Current] Quest Expansion Coverage Audit v0.1

> 상태: [Current] Phase 3 Bulk Fill 이후 Quest / Scenario / Card Rule / Event Hint / Type Coverage를 수치화한 감사 결과.

## 1. 작업 목적

이번 감사는 새 Quest를 추가하지 않고, 현재 구현된 Quest 확장 상태를 숫자로 고정하기 위한 문서다.

판단 대상은 다음 세 가지다.

1. Phase 5 Refactor Gate로 이동할지
2. Stable Category Bulk Fill 2차를 계속할지
3. Small Schema Extension이 먼저 필요한지

이번 작업에서는 `data/`, `src/`, `tests/`, `tools/`를 수정하지 않는다.

## 2. 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/32_Quest_Category_Probe_Result_v0.1.md`
- `docs/07_reviews/33_Quest_Category_Stability_Review_v0.1.md`
- `docs/07_reviews/34_Quest_Category_Bulk_Fill_Result_v0.1.md`

## 3. 현재 Quest 총량

`data/content/base/quests.yaml` 기준 현재 구현 Quest는 22개다.

| 구분 | Quest 수 | 비고 |
|---|---:|---|
| P0 Foundation | 4 | 초기 Quest vertical slice |
| Category Probe | 6 | Local, Investigation, Defense, Travel, Ruin-Dungeon, Survival 대표 Quest |
| Phase 3 Bulk Fill | 12 | Stable Category의 lightweight success Quest |
| 합계 | 22 | 현재 구현 총량 |

Quest Type Catalog 기준 unique 후보는 56개다. 따라서 구현량은 22 / 56, 약 39.3%다.

Catalog 문서의 상태 표기는 Phase 3 이후 최신 구현 상태를 모두 반영하지 않는다. 이 감사에서는 실제 구현 여부는 `data/content/base/quests.yaml`을 기준으로 삼고, Catalog는 전체 후보군과 Type 분포 기준으로만 사용한다.

## 4. Type별 Coverage

### 4.1 Runtime quest_type Coverage

현재 구현 파일의 `quest_type` 기준 분포는 다음과 같다.

| Runtime Type | 구현 Quest 수 |
|---|---:|
| `delivery` | 4 |
| `investigation` | 4 |
| `defense` | 3 |
| `local_problem` | 3 |
| `dungeon_crawl` | 2 |
| `exploration` | 1 |
| `gathering` | 1 |
| `recovery` | 1 |
| `rescue` | 1 |
| `scouting` | 1 |
| `survival` | 1 |

현재 runtime type은 11개다. Phase 3 이후 구현은 Foundation 4개 type에서 stable category 중심의 11개 runtime type으로 넓어졌다.

### 4.2 Catalog Type Coverage

Catalog Type 기준으로는 23개 type 중 17개 type에 최소 1개 구현 Quest가 연결되어 있다. 단, 일부 Quest는 Catalog type과 runtime `quest_type`이 다르다. 예를 들어 `beast_of_zarechka`는 Catalog에서는 `monster_hunt`지만 runtime에서는 `defense`로 구현되어 있다.

| Coverage 상태 | Type |
|---|---|
| Fully Covered 또는 단일 후보 구현 완료 | `survival`, `defense`, `mystery` |
| Partially Covered | `gathering`, `scouting`, `recovery`, `rescue`, `delivery`, `investigation`, `escort`, `exploration`, `local_problem`, `dungeon_crawl`, `ritual`, `monster_hunt` |
| Not Covered | `contract`, `social_contract`, `moral_choice`, `training` |
| Deferred | `infiltration`, `research`, `intrigue`, `horror_investigation` |

Catalog의 미구현 non-deferred 후보는 34개다. Deferred 후보는 4개다.

Deferred 후보:

- `infiltrate_the_keep`
- `create_a_new_spell`
- `weed_out_the_traitor`
- `mansion_returned_explorer`

## 5. Category별 Coverage

Phase 1 Probe에서 Stable 판정된 6개 Category는 Phase 3에서 모두 Bulk Fill을 받았다.

| Category | 구현 Quest 수 | 상태 |
|---|---:|---|
| Foundation | 4 | Baseline 유지 |
| Local Problem | 3 | Stable + Bulk Fill 반영 |
| Investigation / Mystery | 4 | Stable + Bulk Fill 반영 |
| Defense / Threat | 3 | Stable + Bulk Fill 반영 |
| Travel / Delivery / Escort | 4 | Stable + Bulk Fill 반영 |
| Ruin / Dungeon / Ritual | 2 | Stable + Bulk Fill 반영 |
| Survival / Exploration | 2 | Stable + Bulk Fill 반영 |

Category 기준으로는 계획된 stable category가 모두 최소 2개 이상의 Quest를 갖는다. 가장 얇은 Category는 Ruin / Dungeon / Ritual과 Survival / Exploration이다.

## 6. Scenario Coverage

현재 `data/scenarios` 파일은 51개다. 그중 active quest scenario는 47개다.

| Scenario 구분 | 수 |
|---|---:|
| 전체 scenario 파일 | 51 |
| active quest scenario | 47 |
| non-quest scenario | 4 |
| success 또는 general success | 23 |
| partial | 11 |
| failure | 13 |
| health_zero failure 파일 | 2 |
| max_day failure 파일 | 1 |

Quest별 scenario 분포는 다음과 같다.

| Quest 그룹 | Coverage |
|---|---|
| P0 Foundation | success / partial_success / failure 중심의 다중 fixture |
| Category Probe 6개 | 각 대표 Quest가 success / partial_success / failure 보유 |
| Phase 3 Bulk 12개 | 각 Quest가 lightweight success scenario 1개 보유 |

Bulk Quest에 partial/failure fixture를 만들지 않는다는 Phase 3 원칙은 지켜졌다.

## 7. Outcome Coverage

47개 active quest scenario를 simulator로 실행한 결과는 다음과 같다.

| result_type | 수 |
|---|---:|
| `success` | 23 |
| `partial_success` | 11 |
| `failure` | 13 |

`result_type` 의미 변경은 없었다. 기존 Done Quest와 Probe Quest의 success / partial_success / failure 회귀도 유지된다.

## 8. Failure Taxonomy Coverage

47개 실행 로그의 `failure_kind` 분포는 다음과 같다.

| failure_kind | 수 | 상태 |
|---|---:|---|
| `none` | 34 | success / partial_success 경로 |
| `objective_failed` | 8 | 일반 Quest 실패 |
| `death_or_incapacitated` | 4 | health zero / incapacitated 실패 |
| `time_expired` | 1 | max day 초과 실패 |

`character_outcome` 분포는 다음과 같다.

| character_outcome | 수 |
|---|---:|
| `alive` | 43 |
| `incapacitated` | 4 |

Top-level `failure_kind`로는 `return_failed`, `quest_specific_failure`, `reputation_collapse`가 이번 실행 세트에서 관측되지 않았다. 이는 의미 변경이 아니라 fixture coverage 공백이다.

## 9. Card Rule Coverage

현재 Card Rule 총량은 111개다.

| 항목 | 수 | 비율 |
|---|---:|---:|
| 전체 Card Rule | 111 | 100.0% |
| `quest_ids`가 있는 Card Rule | 100 | 90.1% |
| shared Card Rule | 11 | 9.9% |

Slot 분포는 다음과 같다.

| card slot | 수 |
|---|---:|
| `quest_progress` | 66 |
| `resource_alternative` | 25 |
| `risk_discovery` | 20 |

Phase 3 Bulk Quest는 각 Quest별 success fixture 중심으로 추가되었고, Bulk 관련 Card Rule은 `quest_ids` gate를 갖는 구조로 들어갔다.

## 10. Storylet/Event Hint Coverage

현재 base event 총량은 55개다.

| 항목 | 수 | 비율 |
|---|---:|---:|
| 전체 Event | 55 | 100.0% |
| `card_candidate_hints` 보유 Event | 42 | 76.4% |
| `quest_ids` gate 보유 Event | 24 | 43.6% |
| `cooldown_tags` 보유 Event | 42 | 76.4% |
| `repeat_group` 보유 Event | 42 | 76.4% |

Phase 3 이후 Event loader/runtime의 `quest_ids` gate는 적용되어 있다. 다만 모든 기존 Event가 `quest_ids`를 갖는 것은 아니다. Bulk Fill에서 추가된 Event Hint 쪽은 quest gate 적용률이 높고, 기존 shared 또는 older event는 공용 후보로 남아 있다.

## 11. quest_ids Gate Coverage

| 대상 | gate 적용 상태 |
|---|---|
| Quest | 구현 Quest 22개가 scenario `active_quest_id`로 실행됨 |
| Scenario | 47개 active quest scenario가 명시 Quest를 대상으로 실행됨 |
| Card Rule | 100 / 111개가 `quest_ids` 보유 |
| Event Hint | 24 / 55개 event가 `quest_ids` 보유 |
| Bulk Fill Quest | success 중심 fixture와 scoped Card Rule / Event Hint 사용 |

Gate coverage는 Bulk Fill을 계속할 수 있을 정도로 작동하지만, shared card/event와 quest-scoped card/event가 한 파일에 누적되어 유지보수 부담이 커졌다.

## 12. Test / Validator Coverage

현재 test 파일은 20개다. Phase 3 Bulk Fill 결과 문서 기준 전체 unittest suite는 77개 테스트 통과 상태였다.

이번 감사에서 별도 구현 변경은 하지 않았고, active quest 47개 scenario를 simulator로 실행해 JSON/Text MUD surface와 outcome taxonomy를 재확인했다.

| 검증 항목 | 상태 |
|---|---|
| active quest scenario 실행 | 47개 실행 |
| simulator result_type 집계 | success 23 / partial_success 11 / failure 13 |
| JSON Quest Report field | 47개 로그에서 확인 |
| Text MUD log surface | 대부분 유지, 즉시 실패형 11개 txt 로그는 카드 선택 전 종료라 `Quest:` / `카드:` / `선택:` 라인이 없음 |

즉시 실패형 로그의 Text MUD surface 차이는 기존 실패 fixture 동작에서 나온 관측값이며, 이번 작업에서 새로 만든 회귀는 아니다.

## 13. JSON / Text MUD Surface Coverage

실행 로그 47개에서 JSON에는 다음 surface가 유지된다.

- `quest`
- `turns`
- `quest_report`
- `quest_report.result_type`
- `quest_report.failure_kind`
- `quest_report.character_outcome`
- `quest_report.objective_results`
- `quest_report.score_breakdown`

Text MUD 로그는 일반 성공/부분 성공/진행형 실패 로그에서 Quest, 카드, 선택, 결과, Quest Report 섹션을 유지한다. 즉시 실패형 fixture는 health/time/objective precondition 때문에 카드 선택 전에 종료되므로 카드 UI 관련 라인이 없다. 이 차이는 다음 Refactor Gate에서 명시적인 surface contract로 분리해 두는 편이 좋다.

## 14. 남은 Candidate / Deferred Quest

Catalog 기준 남은 non-deferred 후보는 34개다.

Phase 3 결과 문서에서 명시한 tactical deferred 후보는 다음 12개다.

- `tanglewood_faire_games`
- `dreamless_king`
- `mansion_returned_explorer`
- `awaken_the_beast`
- `stowaway_without_memory`
- `old_east_trail_rescue`
- `crypt_of_elven_king`
- `awaken_the_monolith`
- `sealed_ruin_entry`
- `ruined_island_puzzle_box`
- `frozen_treasure_cave`
- `lost_city_rising_sands`

이 중 `mansion_returned_explorer`는 Catalog에서도 Deferred다. 나머지는 난이도, 시스템 요구, 또는 fixture 폭증 가능성 때문에 Bulk Fill 2차 전에 재검토가 필요하다.

## 15. 리스크

현재 주요 데이터 파일 크기는 다음과 같다.

| 파일 | LOC |
|---|---:|
| `data/content/base/quests.yaml` | 1,648 |
| `data/core/card_rules.yaml` | 2,134 |
| `data/content/base/events.yaml` | 1,317 |

주요 리스크:

- `card_rules.yaml`에 111개 rule이 누적되어 다음 Bulk Fill에서 중복과 drift 위험이 커진다.
- Quest, Card Rule, Event Hint가 모두 단일 base 파일 중심이라 Category별 변경 영향 범위를 보기 어렵다.
- Catalog 상태 표기가 Phase 3 구현 결과와 어긋나기 시작했다.
- Catalog Type과 runtime `quest_type`이 일부 다르다.
- Failure taxonomy fixture가 `objective_failed`, `death_or_incapacitated`, `time_expired` 중심이라 일부 failure_kind는 아직 표면 검증이 없다.
- 즉시 실패형 Text MUD 로그의 section surface가 일반 진행 로그와 다르다.

## 16. 다음 단계 판단

판단: **Option A - Phase 5 Refactor Gate로 이동**.

이유:

1. Stable Category 6개는 이미 Probe와 Bulk Fill을 모두 통과했다.
2. 구현 Quest는 22개, active quest scenario는 47개까지 늘었다.
3. Card Rule은 111개, Event는 55개까지 늘어 단순 Bulk Fill 2차를 계속하면 YAML 유지보수 비용이 먼저 커진다.
4. Small Schema Extension이 당장 필수는 아니다. 현재 stable category는 기존 schema로 표현 가능하다.
5. Bulk Fill 2차는 Refactor Gate 이후에 category-scoped 파일 분리, validator surface 정리, Catalog status 갱신을 끝낸 뒤 진행하는 편이 안전하다.

따라서 다음 작업은 Bulk Fill 2차가 아니라 Refactor Gate다.

## 17. 추천 후속 작업

1. `quests.yaml`, `card_rules.yaml`, `events.yaml`의 category 또는 pack 단위 분리 가능성을 검토한다.
2. Card Rule 중 shared rule과 quest-scoped rule의 위치를 분리한다.
3. Event Hint의 `quest_ids` gate 적용 기준을 문서화한다.
4. 즉시 실패형 Text MUD 로그 surface를 별도 contract로 명시한다.
5. Quest Type Catalog의 Done / Candidate / Deferred 상태를 Phase 3 이후 실제 구현 기준으로 갱신한다.
6. Refactor Gate 통과 후 Bulk Fill 2차 후보를 다시 고른다.

## 18. 감사 Evidence

이번 감사에서 생성한 로컬 evidence는 다음 위치에 있다.

- `.omo/ulw-loop/evidence/quest-expansion-coverage-audit-metrics.txt`
- `.omo/ulw-loop/evidence/quest-expansion-coverage-audit-outcomes.txt`
- `.omo/ulw-loop/evidence/quest-expansion-coverage-audit-catalog.txt`
- `.omo/ulw-loop/evidence/quest-expansion-coverage-audit-surface.txt`
- `.omo/ulw-loop/evidence/quest-expansion-coverage-audit-sim-logs/`
