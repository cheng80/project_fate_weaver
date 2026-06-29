# Playtest Review Result v0.1

> 상태: [Historical] 이 문서는 과거 검토와 판단 기록을 보관하기 위한 문서다.

## 1. Playtest Review 목적

이 문서는 `Weighted AutoPlayer Scoring`과 `Content Expansion` slice가 기술적으로 통과한 뒤, 실제 플레이 감각 기준으로 Console Simulator의 선택 재미, profile 차이, 아이템 선택지 사용, 위험 선택, 로그 품질을 검수한 결과다.

이번 검수는 구현 작업이 아니라 리뷰다. Python 코드, scenario, content, core data는 수정하지 않았다.

최종 판정:

```text
NEEDS_SCORING_TUNING
```

판정 이유:

- profile별 결과는 완전히 동일하지 않다.
- `item_unlocked_choice_count`와 `meaningful_choice_count`는 충분히 발생한다.
- `bad_tradeoff_count`는 `greedy_leaning`, `desperate`에서만 자연스럽게 발생한다.
- `unavailable_selected`는 0이다.
- 다만 `balanced`와 `curious_leaning`의 선택 결과가 이번 slice에서는 동일했다.
- `blow_signal_whistle` 같은 item-based 선택이 매우 강하게 반복되어, 일부 profile 개성이 아이템 점수에 묻힌다.

---

## 2. 실행 조건

대상 scenario:

```text
data/scenarios/content_expansion_test.yaml
```

profile:

```text
balanced
safe_leaning
greedy_leaning
curious_leaning
desperate
```

seed/runs:

```text
seed: 42
runs: 3 per profile
total runs: 15
target_turns: 12
```

로그 경로:

```text
/tmp/fateweaver_playtest_review_logs
```

실행 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/content_expansion_test.yaml
rm -rf /tmp/fateweaver_playtest_review_logs
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile balanced --logs /tmp/fateweaver_playtest_review_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile safe_leaning --logs /tmp/fateweaver_playtest_review_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile greedy_leaning --logs /tmp/fateweaver_playtest_review_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile curious_leaning --logs /tmp/fateweaver_playtest_review_logs < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/content_expansion_test.yaml --seed 42 --runs 3 --profile desperate --logs /tmp/fateweaver_playtest_review_logs < /dev/null
.venv/bin/python tools/analyze_logs.py --logs /tmp/fateweaver_playtest_review_logs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

검증 결과:

```text
validate_data: PASS
console_simulator: 15 logs generated
analyze_logs: PASS
unittest discover: Ran 26 tests, OK
```

---

## 3. Profile별 metric 비교

`tools/analyze_logs.py` 출력 기준:

| Profile | Runs | Meaningful Choices | Item-unlocked Choices | Bad Tradeoffs | Restart Avg | Woven Avg |
|---|---:|---:|---:|---:|---:|---:|
| balanced | 3 | 36 | 24 | 0 | 4.0 | 4.0 |
| safe_leaning | 3 | 36 | 24 | 0 | 4.0 | 4.0 |
| greedy_leaning | 3 | 36 | 24 | 4 | 4.0 | 4.0 |
| curious_leaning | 3 | 36 | 24 | 0 | 4.0 | 4.0 |
| desperate | 3 | 35 | 23 | 4 | 4.0 | 4.0 |

전체 집계:

```text
runs_analyzed: 15
meaningful_choice_count: 179
item_unlocked_choice_count: 119
bad_tradeoff_count: 8
restart_intent_score_avg: 4.0
run_failed_but_interesting_count: 0
player_woven_score_avg: 4.0
unavailable_selected: 0
```

해석:

- 확장 콘텐츠는 더 이상 `meaningful_choice_count = 0` 문제가 없다.
- item-gated 선택지는 실제 선택된다.
- 위험 선택은 모든 profile에 퍼지지 않고 `greedy_leaning`, `desperate`에 집중된다.
- `player_woven_score_avg`는 자동 산출값이라 실제 감정 품질을 완전히 증명하지는 못한다.

---

## 4. 선택 다양성 평가

선택 분포:

| Profile | 주요 선택 분포 |
|---|---|
| balanced | `blow_signal_whistle` 15, `inspect_marker` 5, `retreat` 5, `leave` 4, `bribe` 3, `scatter_flare_powder` 3, `flash_flare_powder` 1 |
| safe_leaning | `blow_signal_whistle` 15, `retreat` 8, `inspect_marker` 5, `leave` 4, `scatter_flare_powder` 3, `flash_flare_powder` 1 |
| greedy_leaning | `blow_signal_whistle` 15, `answer_echo` 4, `bribe` 4, `inspect_marker` 5, `retreat` 4, `scatter_flare_powder` 3, `flash_flare_powder` 1 |
| curious_leaning | `balanced`와 동일 |
| desperate | `blow_signal_whistle` 15, `answer_echo` 4, `bribe` 4, `inspect_marker` 4, `retreat` 4, `scatter_flare_powder` 3, `forage` 1, `flash_flare_powder` 1 |

평가:

- profile 간 선택 결과는 완전히 동일하지 않다.
- `safe_leaning`은 `bribe` 대신 `retreat`를 더 자주 택해 안전 성향이 보인다.
- `greedy_leaning`은 `answer_echo`를 선택해 보상/위험 tradeoff가 드러난다.
- `desperate`는 `forage`까지 선택해 생존 압박 상황의 선택 차이가 일부 보인다.
- `curious_leaning`은 `balanced`와 결과가 동일해 profile 분리력이 약하다.

---

## 5. 아이템 선택지 사용 평가

아이템 기반 선택은 활발하다.

대표 선택:

- `blow_signal_whistle`
- `scatter_flare_powder`
- `flash_flare_powder`
- `inspect_marker`

긍정:

- `signal_whistle`, `flare_powder`가 dead item이 아니다.
- `item_usage_score`가 실제 선택에 영향을 준다.
- item-gated choice가 story route를 여는 느낌은 있다.

부족:

- `blow_signal_whistle`이 모든 profile에서 15회 선택되어 지나치게 지배적이다.
- 아이템 선택이 안전, 호기심, 보상 차이를 덮어버리는 구간이 있다.
- `curious_leaning`은 novelty가 강해야 하지만, 현재 slice에서는 item choice dominance 때문에 `balanced`와 분리되지 않는다.

---

## 6. 위험 선택 / bad tradeoff 발생 평가

Risk 분포:

| Profile | High Risk | Medium Risk | Low/None |
|---|---:|---:|---:|
| balanced | 0 | 3 | 33 |
| safe_leaning | 0 | 0 | 36 |
| greedy_leaning | 4 | 4 | 28 |
| curious_leaning | 0 | 3 | 33 |
| desperate | 4 | 5 | 27 |

평가:

- 위험 선택은 무작위로 흩어지지 않는다.
- `greedy_leaning`은 `answer_echo`를 선택하면서 curse 같은 상태 위험 증가와 money 보상을 감수한다.
- `desperate`는 `answer_echo`, `forage`를 통해 위험 감수와 생존 회복 선택이 같이 발생한다.
- `safe_leaning`은 high risk를 피하고 low/none 선택만 한다.

이 부분은 playtest 기준으로 긍정적이다.

---

## 7. 선택 이유 로그 품질 평가

`selected_choice_reason` 예:

```text
profile=balanced: final_score=9.15 (safety=4.0, reward=0.0, item=4.0, risk=1.0, survival=0.0, novelty=1.0, curse_penalty=0.0)
profile=greedy_leaning: final_score=8.15 (safety=4.0, reward=0.0, item=4.0, risk=1.0, survival=0.0, novelty=1.0, curse_penalty=0.0)
profile=safe_leaning: final_score=9.7 (safety=4.0, reward=0.0, item=4.0, risk=1.0, survival=0.0, novelty=1.0, curse_penalty=0.0)
```

긍정:

- profile 이름이 남는다.
- final_score와 구성 score가 남는다.
- 사람이 디버깅할 수 있는 형태다.
- 선택 근거가 단순 "first available"보다 훨씬 낫다.

부족:

- 수치 중심이라 플레이어 관점의 자연어 이유는 약하다.
- 선택된 choice가 다른 후보를 왜 이겼는지 비교 설명은 없다.
- `choice_scores`를 같이 보면 추적 가능하지만, review reader가 바로 이해하기에는 다소 기계적이다.

---

## 8. 현재 콘텐츠의 재미 가능성 평가

재미 가능성은 있다.

좋은 신호:

- `signal_whistle`은 길 찾기, 마을 표식, 산적 대응과 연결되어 "내가 가진 도구가 세계를 해석한다"는 느낌을 준다.
- `flare_powder`는 산적 대응과 상태 위험 완화에 쓰여 risk-reduction item 역할이 분명하다.
- `answer_echo`는 상태 위험 증가와 money 보상을 묶어 명확한 유혹을 만든다.
- `forage`는 food 회복과 health 손실을 묶어 survival tradeoff를 만든다.

약한 신호:

- 4개 이벤트를 12턴 동안 반복하므로 같은 선택이 많이 반복된다.
- `blow_signal_whistle`이 너무 자주 최적해가 되어 선택 고민이 줄어든다.
- profile 차이는 보이지만, narrative arc 차이는 아직 얕다.

---

## 9. 반복 플레이 가능성 평가

현재 반복 플레이 가능성은 "기술 검증 slice로는 양호, 실제 플레이 slice로는 부족"이다.

긍정:

- 동일 seed/run에서도 profile별 final state가 달라진다.
- `safe_leaning`은 money를 보존하고 상태 위험을 낮게 유지한다.
- `greedy_leaning`, `desperate`는 상태 위험과 money 변동이 커진다.

부족:

- `balanced`와 `curious_leaning`이 같은 선택 sequence를 만든다.
- event pool이 작아 반복 run에서 새 느낌이 빨리 줄어든다.
- 자동 `player_woven_score_avg = 4.0`은 실제 플레이어 감정 검증으로 보기 어렵다.

---

## 10. 아직 부족한 점

1. `curious_leaning`의 선택 결과가 `balanced`와 분리되지 않는다.
2. item-based choice가 너무 강해 profile별 의도 차이를 덮는다.
3. `selected_choice_reason`은 디버깅용으로는 좋지만 플레이 감각 리뷰용으로는 비교 설명이 부족하다.
4. 4-event / 12-turn slice는 반복 체감 검수에 작다.
5. `player_woven_score_avg`가 non-interactive 자동값이라 실제 재미 지표로는 제한적이다.

---

## 11. 다음 개선 후보

Scoring tuning 후보:

- `curious_leaning`에서 `novelty_score`가 실제로 `investigate`, `magic`, `unknown`, 정보성 choice를 더 끌어올리도록 조정한다.
- `item_usage_score`가 모든 profile에서 같은 방식으로 압도하지 않게 profile별 cap 또는 diminishing return을 검토한다.
- `selected_choice_reason`에 top competing choice와 점수 차이를 추가한다.

Content tuning 후보:

- `signal_grove_pack`에 item 없이도 매력적인 curiosity choice를 추가한다.
- `blow_signal_whistle`의 반복 최적화를 줄이기 위해 cost, cooldown, consume, run_tag 조건 중 하나를 검토한다.
- `content_expansion_test`에 같은 pack의 추가 이벤트를 더 넣어 반복 run의 사건 폭을 넓힌다.

Validation 후보:

- `profile_choice_divergence_count` 같은 analyzer metric을 추가한다.
- `selected_choice_reason` readability check를 review checklist에 추가한다.
- non-interactive 자동 `player_woven_score`와 실제 manual playtest score를 분리한다.

---

## 12. 최종 판정

```text
NEEDS_SCORING_TUNING
```

세부 판정:

- Technical validation: PASS
- Content expansion readiness: PASS
- Profile metric comparison: PASS
- Unavailable choice safety: PASS
- Playtest fun potential: PARTIAL PASS
- Profile differentiation: PARTIAL PASS
- Reason log readability: PARTIAL PASS

다음 단계는 PRD/Flutter가 아니라 scoring tuning과 소규모 content tuning이다.

---

## 13. Scoring Tuning Result

정리 일자:

```text
2026-06-30
```

이번 조정 범위:

- profile weight preset은 크게 변경하지 않았다.
- 동일 run에서 같은 item-based choice를 반복하면 `item_usage_score` 보너스가 점진적으로 줄어들게 했다.
- `selected_choice_reason`에 runner-up, runner-up score, score gap, top factors를 추가했다.
- analyzer에 profile별 choice diversity와 repeated choice bias metric을 추가했다.

검증 조건:

```text
scenario: data/scenarios/content_expansion_test.yaml
profiles: balanced, safe_leaning, greedy_leaning, curious_leaning, desperate
seed: 42
runs: 3 per profile
```

조정 후 5 profiles x 3 runs 결과:

| Profile | Meaningful Choices | Item-unlocked Choices | Bad Tradeoffs | Choice Diversity | Most Repeated Choice | Repeat Bias Ratio |
|---|---:|---:|---:|---:|---|---:|
| balanced | 30 | 18 | 0 | 8 | `blow_signal_whistle` x9 | 0.25 |
| safe_leaning | 29 | 17 | 0 | 7 | `blow_signal_whistle` x8 | 0.22 |
| greedy_leaning | 30 | 18 | 4 | 8 | `blow_signal_whistle` x9 | 0.25 |
| curious_leaning | 32 | 20 | 0 | 9 | `blow_signal_whistle` x11 | 0.31 |
| desperate | 29 | 17 | 4 | 9 | `blow_signal_whistle` x9 | 0.25 |

주요 선택 분포:

| Profile | Top Choices |
|---|---|
| balanced | `blow_signal_whistle` 9, `mark_trail` 6, `inspect_marker` 5 |
| safe_leaning | `blow_signal_whistle` 8, `retreat` 8, `mark_trail` 7 |
| greedy_leaning | `blow_signal_whistle` 9, `mark_trail` 6, `inspect_marker` 5 |
| curious_leaning | `blow_signal_whistle` 11, `inspect_marker` 5, `retreat` 5 |
| desperate | `blow_signal_whistle` 9, `shortcut` 6, `answer_echo` 4 |

확인:

- `unavailable_selected = 0`
- item 선택은 계속 발생한다. 전체 `item_unlocked_choice_count = 90`.
- `blow_signal_whistle` 반복은 줄었지만 여전히 최다 반복 choice다.
- profile별 `choice_diversity_count`, `most_repeated_choice_id`, `most_repeated_choice_count`, `repeat_bias_ratio`를 analyzer output에서 직접 비교할 수 있다.
- `bad_tradeoff_count`는 `greedy_leaning`, `desperate` 쪽에서만 4회 발생했다.
- 선택 이유는 `runner_up`, `runner_up_score`, `score_gap`, `top_factors`를 포함한다.
- `balanced`와 `curious_leaning` 차이는 콘텐츠 풀이 좁은 현재 slice에서는 확정 판단하지 않는다.

선택 이유 예:

```text
profile=balanced: selected_score=9.15 final_score=9.15 runner_up=leave runner_up_score=4.0 score_gap=5.15 top_factors=safety:4.0,item:4.0,novelty:0.7 (safety=4.0, reward=0.0, item=4.0, risk=1.0, survival=0.0, novelty=1.0, curse_penalty=0.0)
```

조정 후 판정:

```text
SCORING_OBSERVABILITY_READY
```

남은 리스크:

- 현재 이벤트 수가 적어 profile별 선택 차이를 완전히 검증하기 어렵다.
- scoring weight 확정 튜닝은 Content Expansion 2차 이후 다시 해야 한다.
- `blow_signal_whistle`은 반복 완화 이후에도 최다 반복 choice로 남아 있다. 이는 현재 content slice에서 item choice와 경쟁할 동급 선택지가 부족하기 때문이다.
- 다음 개선은 weight 정밀 튜닝보다 Content Expansion 2차와 그 이후의 재검증이 더 효율적이다.

---

## 14. Content Expansion Phase 2 Recheck

정리 일자:

```text
2026-06-30
```

Phase 2 변경:

- `signal_grove_pack` 신규 이벤트 9개 추가
- 신규 아이템 4개 추가
- `content_expansion_test` 검증 범위를 13개 signal grove 이벤트, 18턴으로 확대
- `src`, `tools`, `tests`, `data/core` 변경 없음

재검증 조건:

```text
scenario: data/scenarios/content_expansion_test.yaml
profiles: balanced, safe_leaning, greedy_leaning, curious_leaning, desperate
seed: 42
runs: 3 per profile
target_turns: 18
```

Phase 2 profile metric:

| Profile | Meaningful Choices | Item-unlocked Choices | Bad Tradeoffs | Choice Diversity | Most Repeated Choice | Repeat Bias Ratio |
|---|---:|---:|---:|---:|---|---:|
| balanced | 48 | 40 | 3 | 21 | `blow_signal_whistle` x8 | 0.15 |
| safe_leaning | 48 | 40 | 0 | 19 | `blow_signal_whistle` x7 | 0.13 |
| greedy_leaning | 38 | 34 | 10 | 19 | `blow_signal_whistle` x7 | 0.14 |
| curious_leaning | 50 | 42 | 1 | 19 | `blow_signal_whistle` x9 | 0.17 |
| desperate | 48 | 40 | 8 | 21 | `blow_signal_whistle` x8 | 0.15 |

선택 분포 변화:

- 기존 4-event slice에서는 `blow_signal_whistle`이 profile별 8~11회 반복됐다.
- Phase 2에서는 turn 수가 18로 늘었는데도 profile별 7~9회로 유지되어 상대 반복 편향이 낮아졌다.
- `signal_mirror`, `forest_charm`, `smoke_pellet` 기반 선택지가 상위 선택에 진입했다.
- `greedy_leaning`과 `desperate`에서 bad tradeoff가 더 뚜렷하게 발생한다.
- `safe_leaning`은 bad tradeoff 0을 유지한다.

재검증 판정:

```text
CONTENT_EXPANSION_PHASE2_READY
```

남은 리스크:

- `blow_signal_whistle`은 더 이상 독점적이지 않지만 여전히 most repeated choice다.
- 이번 결과는 seed 42, profile별 3 runs 기준 smoke 재검증이다.
- 다음 단계에서 scoring weight 확정 튜닝을 다시 판단할 수 있다.
