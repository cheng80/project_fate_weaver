# [Current] Director Tuning Second Pass Result v0.1

> 상태: [Current] Storylet Pool Expansion 이후 늘어난 Storylet/Event 후보를 Situation Director가 더 잘 활용하도록 조정한 결과 문서.

## 1. 작업 목적

Storylet/Event 후보를 더 추가하지 않고, 기존 Situation Director의 event scoring을 조정해 Standard Run에서 후보 회전과 후속 상황 연결을 개선했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/02_schema/14_Ontology_Core_Model_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/07_reviews/47_Ontology_Core_To_Director_Loop_Result_v0.1.md`
- `docs/07_reviews/48_Card_Candidate_Repetition_Gate_Result_v0.1.md`
- `docs/07_reviews/49_Standard_Run_Play_Quality_Audit_v0.1.md`

참고: `docs/07_reviews/50_Storylet_Pool_Expansion_Result_v0.1.md`는 작업 문서에는 기준 문서로 적혀 있었지만 현재 repo에는 없었다. 직전 Storylet Pool Expansion의 수치는 `.omo/ulw-loop/storylet-pool-expansion-20260701b/evidence/` evidence를 기준으로 확인했다.

## 3. 문제 정의

Storylet Pool Expansion으로 후보는 늘었지만, Director scoring이 `next_event_tags`, recently used family, clue/omen follow-up, return/resolve timing을 충분히 활용하지 못하면 같은 family가 계속 선택될 수 있었다.

## 4. 적용한 Director 튜닝

- `director_event_score`를 추가해 eligible event 사이의 우선순위만 조정했다.
- 기존 `quest_ids`, region, requirements, cooldown, max occurrence hard gate 이후에만 score를 계산한다.
- 특정 event id penalty는 추가하지 않았다.
- `suspicious_merchant`, `storm_pass_shelter_hint`는 disable하지 않았다.

## 5. Situation Intent Rotation

`situation_intents`의 `intent.` 접두어를 제거하고 underscore token을 event/storylet tag와 비교해 capped bonus를 준다. 최근 같은 storylet id가 반복되면 penalty를 적용한다.

## 6. next_event_tags 반영

event tags, danger tags, storylet tags, card hints가 `next_event_tags`와 맞으면 tag당 +2, cap +4로 반영한다.

## 7. Recently Used Storylet Family Penalty

- 최근 4턴 동일 event id penalty
- `RepeatMemory.recent_storylets` 기반 동일 storylet penalty
- active repeat_group cooldown penalty
- active cooldown_tags overlap penalty

## 8. Clue / Omen Follow-up Priority

clue가 있으면 `clue_followup` / `reveal_clue` storylet에 bonus를 준다. omen이 있으면 `omen`, `omen_escalation`, `escalate_risk`, `introduce_omen` 계열에 bonus를 준다.

## 9. Aftermath / Return Timing

quest progress가 2개 이상 완료되었거나 max turn 후반이면 `aftermath`, `invite_return`, `resolve_objective`, `return_report`, `secure_evidence` 계열에 bonus를 준다. 같은 시점의 pure progress 성격인 `test_survival`, `unlock_route`, `reveal_clue`에는 penalty를 준다.

## 10. Standard Run 재검증

Before 기준은 Storylet Pool Expansion 직후 seed 202 evidence다.

| Metric | Before | After |
|---|---:|---:|
| Turn Count | 25 | 25 |
| Ending | `prepared_frontier_route` | `prepared_frontier_route` |
| Unique Event Count | 12 | 12 |
| Top Repeated Event Count | 5 | 5 |
| `suspicious_merchant` | 5 | 5 |
| `storm_pass_shelter_hint` | 4 | 4 |
| New Alternatives Seen | 9 | 9 |
| Clue Follow-up Count | n/a | 5 |
| Omen Escalation Count | n/a | 2 |

After top events:

```text
suspicious_merchant: 5
storm_pass_shelter_hint: 4
wind_gap_reveals_safe_descent: 3
merchant_receipt_marks_old_route: 2
trade_gossip_points_elsewhere: 2
nervous_merchant_revises_story: 2
second_witness_contradicts_merchant: 2
```

## 11. 기존 Scenario 회귀

Standard Run은 25턴과 `prepared_frontier_route` ending을 유지했다. 기존 `test_gameplay_p0_standard_run`의 card repeat cap도 유지했다.

## 12. Evidence / Debug Trace

Evidence directory:

```text
.omo/ulw-loop/evidence/director-tuning-second-pass-20260701/
```

Key artifacts:

- `C001-red-director-tests.txt`
- `C001-director-tests.txt`
- `C002-verification.txt`
- `C003-standard-run-cli.txt`
- `C003-standard-run-summary.json`
- `standard_run_before_director_summary.json`
- `standard_run_after.json`
- `standard_run_after_text_mud.txt`
- `director_score_trace.json`
- `targeted-after-card-regression-fix.txt`

## 13. 실행한 명령

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_director_tuning_second_pass
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_situation_director_lite
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest tests.test_gameplay_p0_standard_run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --scenario data/scenarios/standard_run_25_35_turn.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python tools/validate_data.py --ontology
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m compileall src tests tools
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
git diff --check
```

## 14. 남은 문제

- `situation_intents` 자체의 distribution은 Reasoner-lite 출력 구조상 아직 넓게 반복된다. 이번 작업은 intent 출력을 바꾸지 않고 event scoring에만 반영했다.
- `gameplay_p0_rules.py`는 pure LOC 250으로 warning band에 도달했다. 다음 코드 추가 전 분리가 필요하다.

## 15. 다음 추천 작업

Gameplay Balance Pass에서 money/reputation reward 반복과 autoplayer의 quest_progress 편중을 별도 조정한다.
