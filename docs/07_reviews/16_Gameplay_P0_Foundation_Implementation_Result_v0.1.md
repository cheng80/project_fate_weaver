# [Current] Gameplay P0 Foundation Implementation Result v0.1

> 상태: [Current] Gameplay Replan P0 Foundation 최소 수직 슬라이스 구현 결과 문서.

## 1. 구현 목적

`docs/06_plans/04_Gameplay_P0_Foundation_Implementation_Plan_v0.1.md` 기준으로 Tutorial Quest 1개가 Quest 기반 Expedition, 3-Card Choice, Multi-Select, Score, Quest Report까지 실제 실행되는지 검증했다.

## 2. 구현 범위

- `herb_gathering_tutorial` Quest 추가
- `tutorial_herb_quest` Scenario 추가
- Short Expedition Clock 추가
- P0 Card Rule / Multi-Select Rule / Score Rule 추가
- 기존 Console Simulator에서 `gameplay_mode: p0_foundation`일 때 P0 엔진으로 위임
- 기존 JSON Log와 Text MUD Play Log 유지 및 P0 필드 확장

## 3. 구현한 P0 요소

| 항목 | 결과 |
|---|---|
| Quest Layer | `herb_gathering_tutorial` active quest 로딩 |
| Expedition Clock | 3 Day / 4 Turn per Day / max 12 Turn |
| 3-Card Choice | 매 Turn Quest Progress / Risk Discovery / Resource Alternative 카드 3장 출력 |
| Multi-Select | `torch_plus_search` 2장 조합 처리 |
| Combo / Conflict / Cost | combo 1개, conflict 1개, default extra cost 적용 |
| Score | quest_progress, discovery, resource_management, survival, reputation, ending_bonus 반영 |
| Quest Report | success / partial_success / failure 구조 생성 |
| JSON Log | quest, run_clock, presented_cards, selected_cards, multi_select, quest_report 포함 |
| Text MUD Play Log | Day/Time/Turn, Quest, 카드, 선택, Progress, Score, Report 출력 |

## 4. 실행 검증

실행한 명령:

```bash
.venv/bin/python tools/validate_data.py --scenario data/scenarios/mvp0_console_test.yaml
.venv/bin/python tools/validate_data.py --scenario data/scenarios/tutorial_herb_quest.yaml
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/mvp0_console_test.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_mvp0_regression_logs --profile balanced < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 42 --runs 1 --logs /tmp/fateweaver_p0_logs --profile balanced < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 77 --runs 1 --logs /tmp/fateweaver_p0_logs --profile curious_leaning < /dev/null
.venv/bin/python tools/console_simulator.py --scenario data/scenarios/tutorial_herb_quest.yaml --seed 123 --runs 1 --logs /tmp/fateweaver_p0_logs --profile safe_leaning < /dev/null
```

결과:

- validator PASS
- unittest 33개 PASS
- 기존 mvp0 Console Validation 실행 PASS
- P0 Tutorial Quest 3개 run 실행 PASS
- 각 P0 run에서 JSON Log와 Text MUD Play Log 생성 확인

## 5. Sample Run 결과

| Seed / Profile | Turns | Quest Result | 주요 사건 흐름 | 선택 흐름 |
|---|---:|---|---|---|
| 42 / balanced | 5 | success | 마을 장터 -> 폭우 -> 폭우 -> 폭우 -> 마을 장터 | 의뢰 확인 -> 약초+횃불 combo -> 약초 -> 귀환 -> 보고 |
| 77 / curious_leaning | 6 | success | 마을 장터 -> 굶주린 밤 -> 폭우 -> 상인 -> 폭우 -> 상인 | 의뢰 확인 -> 약초+횃불 combo -> 발자국 조사 -> 약초 -> 귀환 -> 보고 |
| 123 / safe_leaning | 5 | success | 상인 -> 폭우 -> 굶주린 밤 -> 폭우 -> 마을 장터 | 의뢰 확인 -> 약초+횃불 combo -> 약초 -> 귀환 -> 보고 |

## 6. Acceptance Gate 대응

| Acceptance Gate 항목 | P0 결과 |
|---|---|
| Quest Layer 존재 | 충족 |
| Expedition Clock 존재 | 충족 |
| Day / Turn / Time of Day 출력 | 충족 |
| 매 Turn 3장의 카드 제시 | 충족 |
| 1장 선택과 조건부 다중 선택 처리 | 충족 |
| resource/status/economy/reputation/score/quest_progress/next_event_tags 반영 | P0 범위에서 충족 |
| Situation Director가 Quest/Region/Clock/State/Item/Clue/Omen/Economy/Reputation 입력을 봄 | P0 범위에서 부분 충족 |
| Weighted Candidate Pool 후보군 기반 작동 | 기존 event selector와 P0 카드 후보군으로 부분 충족 |
| JSON Log와 Text MUD Play Log 유지 | 충족 |
| 저주는 상태/위험 요소 중 하나로만 다룸 | 충족 |

## 7. 남은 문제

- P0는 Tutorial Quest 1개만 구현했다.
- 전체 Quest 10개, Event 60개, Card 후보 150개 확장은 아직 하지 않았다.
- Clue/Omen은 P0 card result에서 실사용되지만 독립 콘텐츠 볼륨은 아직 부족하다.
- Situation Director는 P0 후보군 중심이며, 완전한 ontology director는 아니다.
- 모든 sample run이 success로 끝난다. 실패/부분 성공 전용 QA scenario는 후속으로 분리하는 편이 좋다.

## 8. 다음 추천 작업

1. P0 실패/부분 성공 seed 또는 scenario를 추가한다.
2. Quest/Card/Score YAML 계약을 `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`와 정렬한다.
3. P0 engine을 ontology relation 분석과 연결한다.
4. Tutorial Quest 2번째 slice를 추가하기 전에 current P0 로그를 리뷰한다.
