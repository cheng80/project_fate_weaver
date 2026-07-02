# [Current] Standard Run 25-35 Turn Verification Result v0.1

> 상태: [Current] Content Enrichment Pack 1/2 이후 표준 Run 25~35 Turn 검증 결과 문서.

## 1. 작업 목적

이번 작업은 Content Enrichment Pack 1/2 이후 `standard_run_25_35_turn` scenario가 25~35 Turn 동안 JSON Log와 Text MUD Log를 모두 생성하고, Run Ending까지 표시하는지 확인한다.

이번 작업에서 하지 않은 것:

- Quest 대량 추가
- Card / Item / Ending 대량 추가
- Campaign 시스템 구현
- Bulk Fill 2차
- active scenario 파괴

## 2. 변경 요약

| 영역 | 변경 |
|---|---|
| Scenario | `data/scenarios/standard_run_25_35_turn.yaml` 추가 |
| Runtime | `run_clock.min_turns_before_completion`가 있을 때만 조기 quest success 종료를 최소 턴까지 지연 |
| Test | `tests/test_gameplay_run_standard_run.py` 추가 |
| Evidence | `.omo/ulw-loop/evidence/standard-run-25-35-20260701/` 생성 |

`min_turns_before_completion` 기본값은 0이므로 기존 scenario의 조기 success 종료 동작은 유지된다.

## 3. Standard Scenario

| 항목 | 값 |
|---|---|
| Scenario | `standard_run_25_35_turn` |
| Active Quest | `survive_the_storm_pass` |
| Target Turns | 30 |
| Completion Gate | 25 |
| Max Turns | 30 |
| Turns Per Day | 4 |
| Initial Items | `torch`, `camp_tarp`, `spare_ration_cache`, `reed_whistle`, `clear_water_vial`, `red_thread_charm` |
| Included Events | `storm_pass_shelter_hint`, `storm_pass_pack1_enrichment`, `suspicious_merchant`, `quiet_camp`, `sudden_storm`, `hunger_night` |

이 scenario는 새 Quest/Card/Item/Ending을 추가하지 않고 기존 Pack 1/2 데이터를 표준 run 표면으로 노출한다.

## 4. Evidence Summary

Seed 42, balanced profile 기준 관찰 결과:

| 항목 | 결과 |
|---|---:|
| Turn Count | 25 |
| Final Day | 7 |
| Presented Cards Per Turn | 3 |
| Unique Presented Cards | 16 |
| Unique Selected Cards | 10 |
| Unique Events | 6 |
| Clues Surfaced | 3 |
| Omens Surfaced | 1 |
| Item-gated Cards Surfaced | 3 |
| Result Type | `success` |
| Ending ID | `prepared_frontier_route` |
| Text MUD `Run Ending` | PASS |

Surfaced item-gated cards:

- `find_dry_refuge`
- `ration_the_last_supplies`
- `signal_from_high_ground`

Final clue / omen surface:

- Clues: `storm_shelter`, `moonleaf_glow`, `dry_moss_line`
- Omens: `clouds_hold_too_still`

## 5. Repetition Review

반복도는 PASS지만 개선 여지가 남아 있다.

| 항목 | 결과 |
|---|---:|
| Top Repeated Presented Card | `ration_the_last_supplies` |
| Top Repeat Count | 15 / 25 turns |
| Top Repeated Shared Card | `buy_local_hint` |
| Shared Card Repeat Count | 13 / 25 turns |

해석:

- 25턴 표준 run은 성립한다.
- Pack 1/2의 clue, omen, item-gated card, ending은 실제 로그에 표시된다.
- 다만 단일 Quest run 구조에서는 category-specific Pack 카드 수가 제한되어 후반부에 shared/resource card 반복이 커진다.
- 다음 단계에서 Storylet Pool 전체 시스템이나 장기 cooldown을 구현하지 않는 한, 반복도 개선은 category별 추가 surface 또는 card candidate filtering 정책을 별도 작업으로 다루는 것이 적절하다.

## 6. JSON / Text MUD 확인

생성 evidence:

- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/standard_run.json`
- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/standard_run_text_mud.txt`
- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/standard_run_summary.json`
- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/verification.txt`
- `.omo/ulw-loop/evidence/standard-run-25-35-20260701/tmux_transcript.txt`

Text MUD 확인:

```text
Run Ending: prepared_frontier_route / 준비된 변경의 길
[Run 종료]
```

## 7. 검증 명령

실행한 검증:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_run_standard_run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
git diff --check
```

최종 회귀 결과:

| 검증 | 결과 |
|---|---|
| Standard scenario validate | PASS |
| Focused standard run test | PASS |
| Full unittest | PASS |
| Compileall | PASS |
| Diff check | PASS |
| JSON Log 생성 | PASS |
| Text MUD Log 생성 | PASS |
| Run Ending 표시 | PASS |

## 8. 판정

Content Enrichment Pack 1/2 이후 Standard Run 25~35 Turn 검증은 PASS다.

다음 추천 작업:

1. Storylet Pool 전체 시스템 없이 반복도를 더 낮출 수 있는 candidate filtering / category surface 개선 여부를 별도 Refactor Gate에서 판단한다.
2. Item / Ending split loader 필요성은 콘텐츠 추가 전 별도 gate에서 다룬다.
3. 25~35턴 run을 category별로 확장 검증하려면 새 Quest 대량 추가가 아니라 기존 category 대표 scenario별 표준 run fixture를 먼저 정의한다.
