# [Current] Enrichment Pack 2 Item Ending Result v0.1

> 상태: [Current] Content Enrichment Catalog의 Pack 2 후보를 기반으로 Item / Ending 콘텐츠를 확장한 결과 문서.

## 1. 작업 목적

이번 작업은 Content Enrichment 단계의 Pack 2 구현이다.

`docs/06_plans/08_Content_Enrichment_Catalog_v0.1.md`의 Pack 2 후보를 기준으로 실제 데이터에 다음 항목을 반영했다.

| 항목 | 추가 수 | 구현 방식 |
|---|---:|---|
| Item | 25 | `data/content/base/items.yaml`에 Pack 2 item 추가 |
| Ending | 8 | `data/content/base/endings.yaml`에 report/run review 조건 기반 ending 추가 |
| Item-gated Card | 12 | Pack 1 card 일부에 `requires_item` 연결 |
| Quest Report Ending surface | 1 | Quest Report에 matching `ending` 필드와 Text MUD 출력 추가 |

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/13_Quest_Design_Guide_v0.1.md`
- `docs/06_plans/06_Quest_Type_Catalog_v0.1.md`
- `docs/06_plans/07_Quest_Category_Probe_And_Bulk_Loop_Plan_v0.1.md`
- `docs/07_reviews/41_Data_Split_Coverage_Audit_v0.1.md`
- `docs/07_reviews/42_Content_Enrichment_Ultraresearch_Notes_v0.1.md`
- `docs/06_plans/08_Content_Enrichment_Catalog_v0.1.md`
- `docs/07_reviews/43_Enrichment_Pack_1_Card_Clue_Omen_Result_v0.1.md`
- `/Users/cheng80/Desktop/CODEX_TASK_Enrichment_Pack_2_Item_Ending_v0.1.md`

## 3. 변경 파일

데이터:

- `data/content/base/items.yaml`
- `data/content/base/endings.yaml`
- `data/content/card_rules/local_problem.yaml`
- `data/content/card_rules/defense_threat.yaml`
- `data/content/card_rules/travel_delivery_escort.yaml`
- `data/content/card_rules/ruin_dungeon_ritual.yaml`
- `data/content/card_rules/survival_exploration.yaml`

코드:

- `src/fateweaver/quest_objectives.py`
- `src/fateweaver/text_mud_report.py`

테스트:

- `tests/test_gameplay_run_enrichment_pack_2.py`

문서:

- `docs/07_reviews/44_Enrichment_Pack_2_Item_Ending_Result_v0.1.md`
- `docs/00_index/README_Docs_Index.md`

## 4. 추가한 Item

Pack 2 신규 Item 25개:

| Item | Role | 주요 연결 |
|---|---|---|
| `waxed_thread_spool` | unlock | `secure_the_sealed_bag`, `copy_the_rune_sequence` |
| `chalk_marker_set` | future_weight | `leave_a_return_marker`, `prepared_frontier_route` |
| `folding_probe_rod` | information | `tap_the_hollow_wall` |
| `oilcloth_map_case` | risk_reduce | `read_weather_marks`, storm/lost 대응 |
| `village_token` | cost_convert | `interview_reluctant_witness`, `offer_public_help` |
| `small_signal_bell` | unlock | `prepare_quiet_signal`, `raise_night_watch` |
| `dried_bitterroot` | risk_reduce | `inspect_shared_water_source`, poison/hunger 대응 |
| `mirror_shard` | information | `test_the_false_signal` |
| `ash_salt_pouch` | risk_reduce | `test_the_ritual_component`, curse 대응 |
| `spare_wheel_pin` | unlock | `repair_load_straps` |
| `warm_lantern_oil` | cost_convert | `listen_beyond_the_seal` |
| `reed_whistle` | unlock | `signal_from_high_ground` |
| `tarred_rope_hook` | unlock | `brace_the_old_stairs` |
| `sealed_letter_copy` | information | `secure_the_sealed_bag`, `listen_to_border_gossip` |
| `soft_boot_wraps` | risk_reduce | `reconstruct_last_known_path` |
| `camp_tarp` | risk_reduce | `find_dry_refuge` |
| `copper_listening_cup` | information | `listen_beyond_the_seal` |
| `red_thread_charm` | cost_convert | `follow_water_insects` |
| `spare_ration_cache` | cost_convert | `ration_the_last_supplies` |
| `beast_scent_tar` | risk_reduce | `bait_the_threat_path` |
| `ink_fixing_powder` | information | `map_conflicting_testimony` |
| `smoke_cord` | future_weight | `burn_false_trail` |
| `iron_nail_bundle` | unlock | `mark_weak_fence_line`, `move_children_to_cellar` |
| `clear_water_vial` | information | `inspect_shared_water_source`, `follow_water_insects` |
| `oath_coin` | cost_convert | `negotiate_safe_passage` |

## 5. 추가한 Ending

Pack 2 신규 Ending 8개:

| Ending | 조건 방향 |
|---|---|
| `clear_report_return` | success + alive + clue + reputation |
| `costly_truth_return` | partial_success + clue + low food + partial reason |
| `sealed_danger_left_behind` | success/partial + unresolved omen |
| `rescued_but_hunted` | success/partial + rescue/escort objective + omen |
| `rich_but_distrusted` | money high + reputation low |
| `prepared_frontier_route` | success + clue + frontier route item |
| `ritual_interrupted_not_understood` | ritual/ruin partial + omen + partial reason |
| `survivor_without_answer` | failure + alive + no clue |

## 6. Item과 Card / Result 연결

연결 방식은 두 층이다.

- 모든 신규 Item은 `unlocks_cards`, `modifies_results`, `resource_effects`, `risk_effects`, `ending_links` 중 하나 이상을 가진다.
- 다음 12개 Pack 1 Card는 실제 runtime availability가 바뀌도록 `requires_item`을 가진다.

| Card | Required Item |
|---|---|
| `inspect_shared_water_source` | `clear_water_vial` |
| `bait_the_threat_path` | `beast_scent_tar` |
| `repair_load_straps` | `spare_wheel_pin` |
| `secure_the_sealed_bag` | `waxed_thread_spool` |
| `negotiate_safe_passage` | `oath_coin` |
| `tap_the_hollow_wall` | `folding_probe_rod` |
| `brace_the_old_stairs` | `tarred_rope_hook` |
| `listen_beyond_the_seal` | `copper_listening_cup` |
| `leave_a_return_marker` | `chalk_marker_set` |
| `find_dry_refuge` | `camp_tarp` |
| `ration_the_last_supplies` | `spare_ration_cache` |
| `signal_from_high_ground` | `reed_whistle` |

## 7. Ending과 Quest Report / Run Review 연결

`quest_objectives.build_quest_report()`는 기존 `result_type`, `failure_kind`, `character_outcome` 계산 후 `bundle.endings`의 조건을 순서대로 평가한다.

새 `ending` 필드는 다음을 포함한다.

```yaml
ending:
  id: clear_report_return
  name: 납득된 보고
  condition: {...}
```

Text MUD Quest Report에는 다음 줄이 추가된다.

```text
Run Ending: clear_report_return / 납득된 보고
```

기존 outcome taxonomy 의미는 바꾸지 않았다.

## 8. Category별 분배

Item 역할 분포:

| Role | 수 |
|---|---:|
| `unlock` | 6 |
| `risk_reduce` | 6 |
| `cost_convert` | 5 |
| `information` | 6 |
| `future_weight` | 2 |

Category 연결은 Local / Investigation / Defense / Travel / Ruin-Dungeon / Survival 전반에 분산했다.

## 9. 데이터 정합성 검증

Post-Pack inventory:

| 항목 | 수 | 변화 |
|---|---:|---|
| Base Item | 31 | +25 |
| Base Ending | 10 | +8 |
| Loaded Card Rule | 151 | 유지 |
| Item-gated Card | 13 | +12 |

Duplicate check:

| Check | 결과 |
|---|---|
| duplicate item id | 0 |
| duplicate ending id | 0 |
| unknown item card references | 0 |
| unknown item ending references | 0 |

## 10. 기존 Scenario 회귀 검증

`tests/test_gameplay_run_enrichment_pack_2.py`에서 active quest scenario 47개에 대해 `validate_scenario_file()`을 실행했고 PASS했다.

이번 작업은 Standard Run 25~35 Turn 검증을 실행하지 않았다. 해당 검증은 다음 단계의 별도 작업 범위다.

## 11. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_enrichment_pack_2
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs /tmp/fateweaver-pack2-smoke-final --profile balanced
git diff --check
```

## 12. 남은 문제

- Item split loader는 아직 없다. 이번 작업은 기존 loader 안정성을 우선해 `data/content/base/items.yaml`에 추가했다.
- Ending split loader는 아직 없다. 이번 작업은 `data/content/base/endings.yaml`에 추가했다.
- Ending matcher는 Quest Report / Run Review용 최소 조건 평가기다. Save/Run Archive나 장기 campaign residue 시스템은 구현하지 않았다.

## 13. 다음 추천 작업

1. Standard Run 25~35 Turn 검증에서 item availability, item-gated card 노출, ending 다양성을 관찰한다.
2. Item / Ending 파일이 더 커지기 전에 split loader 도입 여부를 별도 Refactor Gate에서 판단한다.
3. 필요하면 Ending condition schema를 문서화해 data authoring 기준을 고정한다.
