# Content Expansion Readiness Checklist

이 체크리스트는 Console Simulator 구현 검수 PASS 이후, 콘텐츠 확장 전에 확인해야 하는 검수 기준이다.

## 검수 상태

Status: PASS
대상: signal_grove_pack + content_expansion_test
evidence: `.omo/ulw-loop/content-expansion-20260629/evidence/`
playtest_review: `docs/07_reviews/11_Playtest_Review_Result_v0.1.md`

## 검수 목적

다음 단계는 PRD나 Flutter 제작이 아니라, 기존 Console Validation과 Ontology-lite 계약을 유지한 채 이벤트, 아이템, 상태, 팩, 시나리오를 안전하게 확장할 수 있는지 확인하는 것이다.

```text
Console Simulator implementation: PASS
Ontology-lite: READY
Next focus: Content Expansion Readiness
```

---

# 1. Event 확장 체크

- [x] 이벤트 추가 시 `data/core/tags.yaml`의 region/event/danger tag enum 누락이 없는지 확인한다. (`forest`, `village`, `ruin`; `exploration`, `survival`, `combat`, `trade`, `magic`, `curse`, `rest`; `lost`, `trap`, `bandit`, `physical`, `hunger`)
- [x] 이벤트 추가 시 `event -> choice -> result` 관계가 `data/core/ontology.yaml` relation으로 설명 가능한지 확인한다. (`signal_grove_pack/events.yaml`의 choice/result 구조)
- [x] 이벤트 추가 시 `event_belongs_to_region`, `event_has_event_tag`, `event_has_danger_tag` relation이 해석 가능한지 확인한다. (4개 이벤트 모두 region/event/danger tag 보유)
- [x] 전투형 이벤트는 여전히 일반 event + `combat_response` choice로만 표현한다. (`bandit_signal_post` + `flash_flare_powder`)

---

# 2. Item 확장 체크

- [x] 아이템 추가 시 `counters_tags` 또는 choice `requires_item` 관계가 명확한지 확인한다. (`signal_whistle`, `flare_powder` counters + requires_item)
- [x] 아이템 role은 `data/core/item_roles.yaml`과 `data/core/tags.yaml`의 `item_role` enum에 모두 존재해야 한다. (`unlock`, `information`, `risk_reduce`, `cost_convert`)
- [x] 아이템 tag는 `data/core/tags.yaml`의 `item_tag` enum에 존재해야 한다. (`tool`, `consumable`)
- [x] 새 아이템이 실제 choice를 unlock하거나 risk를 줄이는지 확인한다. (`blow_signal_whistle`, `inspect_marker`, `flash_flare_powder`, `scatter_flare_powder`)

---

# 3. Status / Result 확장 체크

- [x] 상태 추가 시 `data/core/statuses.yaml`에 min/max/initial/fail_when 필요 여부를 반영한다. (신규 status 없음)
- [x] 상태 추가 시 `data/core/result_rules.yaml`의 allowed status 계약을 갱신한다. (신규 status 없음)
- [x] result가 변경하는 status는 `result_modifies_status` relation으로 설명 가능해야 한다. (`health`, `food`, `money`, `reputation`, `curse`만 사용)
- [x] result가 event weight를 바꾸면 target tag가 `weight_target` enum에 있어야 한다. (`lost`, `forest`, `trade`, `bandit`, `magic`, `village`)

---

# 4. Pack / Scenario 확장 체크

- [x] pack 추가 시 scenario의 `content_sources`에서 참조 가능한 경로인지 확인한다. (`data/content/packs/signal_grove_pack/items.yaml`, `events.yaml`)
- [x] scenario 추가 시 `include_regions`, `include_event_ids`, `include_event_tags` 계약을 지킨다. (`include_event_ids` 4개, `include_event_tags` 미설정)
- [x] scenario 추가 시 `exclude_event_ids`, `exclude_event_tags`가 include 이후 적용되는 계약을 지킨다. (둘 다 빈 배열)
- [x] scenario가 노출하는 event는 `scenario_includes_event` relation으로 설명 가능해야 한다. (`content_expansion_test`가 신규 4개 event ID를 직접 포함)
- [x] scenario가 사용하는 source file은 `scenario_uses_content_source` relation으로 설명 가능해야 한다. (`content_sources`에 base + forest/curse + signal_grove pack 명시)

---

# 5. Ontology-lite 체크

- [x] `data/core/ontology.yaml`에 필요한 entity가 누락되지 않았는지 확인한다. (신규 entity type 없음)
- [x] `data/core/ontology.yaml`에 필요한 relation이 누락되지 않았는지 확인한다. (기존 event/choice/result/item/scenario relation만 사용)
- [x] 새 콘텐츠 관계가 기존 relation으로 설명되지 않으면 문서와 ontology 계약을 먼저 갱신한다. (계약 갱신 필요 없음)
- [x] Ontology-lite는 계약 파일이며, 별도 ontology engine을 만들지 않는다. (데이터 파일만 추가)

---

# 6. Console Validation 체크

- [x] 확장 데이터에서도 Console Simulator validator가 통과해야 한다. (`content_expansion_test`, `mvp0_console_test` 모두 PASS)
- [x] 확장 데이터에서도 Core Loop Validation Metrics가 계산되어야 한다. (`analyze_logs` metric JSON 출력)
- [x] `meaningful_choice_count`가 확장 콘텐츠에서 해석 가능해야 한다. (seed 42 AutoPlayer 결과 `0`, 첫 available choice 선택 정책 때문)
- [x] `item_unlocked_choice_count`가 새 item/choice 관계를 반영해야 한다. (item-gated choice는 존재하나 seed 42 AutoPlayer 결과 선택 횟수 `0`)
- [x] `bad_tradeoff_count`, `restart_intent_score_avg`, `run_failed_but_interesting_count`, `player_woven_score_avg`가 계속 출력되어야 한다.
- [x] AutoPlayer profile별 metric 비교가 가능해야 한다. (`profile_metrics` 출력)
- [x] `item_usage_score`가 item-gated choice 선택에 영향을 줘야 한다. (`choice_scores[].item_usage_score`와 selected score 기록)
- [x] `desperate` profile은 health/food가 낮을 때 survival 관련 선택 가중치를 높여야 한다. (`survival_need_score` 기록)
- [x] `greedy_leaning` profile은 reward_score를 더 크게 반영해야 한다.
- [x] 모든 weighted profile에서 unavailable choice가 선택되지 않아야 한다.

검증 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_content_expansion_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --profile balanced --logs /tmp/fateweaver_profile_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --profile greedy_leaning --logs /tmp/fateweaver_profile_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --profile curious_leaning --logs /tmp/fateweaver_profile_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 1 --profile desperate --logs /tmp/fateweaver_profile_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_expansion_logs
```

검증 결과:

```text
content_expansion_test: VALIDATION: PASS
mvp0_console_test: VALIDATION: PASS
console_simulator: LOG 생성 PASS
analyze_logs: metric JSON 출력 PASS
profile_metrics: weighted profile별 비교 PASS
```

---

# 7. 금지 작업 유지 체크

- [x] GraphDB 도입 금지를 유지한다.
- [x] RDF/OWL 도입 금지를 유지한다.
- [x] `data/content` 구조 변경 금지를 유지한다. (기존 pack 구조 아래 `signal_grove_pack`만 추가)
- [x] `data/mvp0/` 생성 금지를 유지한다.
- [x] Flutter 프로젝트 생성을 하지 않는다.
- [x] `fate_weaver/` 생성을 하지 않는다.
- [x] PRD 작성 전에 콘텐츠 확장 계약을 먼저 검증한다.
- [x] World Bible 작성 전에 이벤트/아이템/상태 관계 검증을 먼저 수행한다.

---

# 8. 완료 판정

`Content Expansion Readiness` 통과 조건:

- [x] Section 1-7 체크가 모두 통과한다.
- [x] 새 콘텐츠가 기존 YAML 구조 안에서 표현된다.
- [x] 새 콘텐츠 관계가 Ontology-lite relation으로 설명된다.
- [x] Console Simulator validator와 analyzer가 확장 데이터에서도 작동한다.

판정:

```text
CONTENT_EXPANSION_READY
```

추가 Playtest Review 판정:

```text
NEEDS_SCORING_TUNING
```

의미:

- Content Expansion Readiness 자체는 유지된다.
- 실제 플레이 감각 검수에서는 profile별 차이가 일부 확인됐지만, `balanced`와 `curious_leaning` 결과가 동일하고 item-based choice가 과도하게 강해 scoring tuning이 필요하다.
- 후속 Weighted AutoPlayer Scoring Tuning에서는 profile weight를 크게 흔들지 않고, 반복 item-based choice 감쇠와 runner-up/gap/top_factors reason 출력, profile별 choice diversity/repeat bias 분석을 추가했다.
- 현재 이벤트 수가 적어 profile별 선택 차이는 Content Expansion 2차 이후 다시 검증해야 한다.

---

# 9. Content Expansion Phase 2 검증 결과

검증 일자:

```text
2026-06-30
```

변경 범위:

- `signal_grove_pack/events.yaml`: 신규 이벤트 9개 추가
- `signal_grove_pack/items.yaml`: 신규 아이템 4개 추가
- `content_expansion_test.yaml`: 신규 이벤트 9개를 include 범위에 추가하고 target_turns를 18로 확대
- `data/core` 변경 없음. 기존 enum과 relation으로 표현 가능

신규 이벤트:

```text
whispering_bark_marks
abandoned_watch_post
mist_guide_call
survivor_tracks
false_rescue_signal
cursed_tree_ward
old_hunter_cache
glowing_insect_swarm
crossroads_flags
```

신규 아이템:

```text
signal_mirror
forest_charm
trail_ribbon
smoke_pellet
```

Phase 2 체크:

- [x] 신규 이벤트는 6~10개 범위 안이다. (`9`)
- [x] 신규 아이템은 2~4개 범위 안이다. (`4`)
- [x] 모든 신규 이벤트는 choice 3개를 가진다.
- [x] item 없이 선택 가능한 `investigate`/curiosity choice를 여러 이벤트에 추가했다.
- [x] 위험/보상 tradeoff와 curse 증가 선택지를 추가했다.
- [x] `signal_whistle` 외에 `signal_mirror`, `forest_charm`, `trail_ribbon`, `smoke_pellet` item route를 추가했다.
- [x] `content_expansion_test`가 신규 이벤트 9개를 직접 include한다.
- [x] `src`, `tools`, `tests`, `data/core`는 변경하지 않았다.

검증 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile balanced --logs /tmp/fateweaver_content_phase2_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile safe_leaning --logs /tmp/fateweaver_content_phase2_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile greedy_leaning --logs /tmp/fateweaver_content_phase2_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile curious_leaning --logs /tmp/fateweaver_content_phase2_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile desperate --logs /tmp/fateweaver_content_phase2_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_content_phase2_logs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

검증 결과:

```text
validate_data: PASS
console_simulator: 15 logs generated
analyze_logs: PASS
unittest discover: PASS
unavailable_selected: 0
```

Phase 2 profile metric:

| Profile | Meaningful Choices | Item-unlocked Choices | Bad Tradeoffs | Choice Diversity | Most Repeated Choice | Repeat Bias Ratio |
|---|---:|---:|---:|---:|---|---:|
| balanced | 48 | 40 | 3 | 21 | `blow_signal_whistle` x8 | 0.15 |
| safe_leaning | 48 | 40 | 0 | 19 | `blow_signal_whistle` x7 | 0.13 |
| greedy_leaning | 38 | 34 | 10 | 19 | `blow_signal_whistle` x7 | 0.14 |
| curious_leaning | 50 | 42 | 1 | 19 | `blow_signal_whistle` x9 | 0.17 |
| desperate | 48 | 40 | 8 | 21 | `blow_signal_whistle` x8 | 0.15 |

Phase 2 판정:

```text
CONTENT_EXPANSION_PHASE2_READY
```

남은 리스크:

- `blow_signal_whistle`은 반복 지배가 완화됐지만 여전히 최다 반복 choice다.
- 신규 아이템 route가 item choice 다양성을 넓혔으므로, 다음 단계에서는 scoring weight 확정 튜닝을 다시 판단할 수 있다.
