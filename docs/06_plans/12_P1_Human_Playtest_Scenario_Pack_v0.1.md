# [Current] P1 Human Playtest Scenario Pack v0.1

> 상태: [Current] P0 playable milestone 이후 사람이 직접 읽고 선택할 수 있는 P1 human playtest용 scenario pack 문서.

## 1. 문서 목적

이 문서는 FateWeaver P1 첫 human playtest를 바로 실행할 수 있도록 run 후보, 관찰 목표, 진행자 체크리스트, 완료 기준을 고정한다.

이번 pack은 문서/운영 자료다. 새 `data/scenarios/` 파일이나 Quest/Card/Event/Item/Ending을 추가하지 않는다.

## 2. Playtest 목표

- 사람이 Quest 목적을 이해하는지 확인한다.
- 매 turn 3-card 선택이 서로 다르게 느껴지는지 확인한다.
- resource pressure와 `resource_alternative` 선택이 의미 있게 읽히는지 확인한다.
- clue/omen이 다음 판단으로 이어지는지 확인한다.
- storylet/event 반복감과 25턴 피로도를 확인한다.
- Quest Report와 Ending이 납득되는지 확인한다.

## 3. P0 Baseline Reference

P0 baseline guard:

- Scenario: `data/scenarios/standard_run_25_35_turn.yaml`
- Profile: `balanced`
- Baseline seed: `202`
- Turn count: `25`
- Result: `success`
- Ending: `prepared_frontier_route`
- Three cards every turn: `PASS`
- `resource_alternative` selected: at least `1`

Resource balance reference:

- 10 seed validation.
- `resource_alternative` selected 2-4 times: `8/10` seeds.
- 0 selected seeds: `0/10`.
- Watch seeds: `202`, `707`.

## 4. Playtest 대상자

대상:

- 텍스트 RPG나 TRPG 로그를 읽을 수 있는 플레이어.
- FateWeaver 내부 구조를 모르는 사람.
- 정답 찾기보다 "현재 상황에서 고르고 싶은 선택"을 말할 수 있는 사람.

제외:

- 현재 gameplay/data 구현 세부를 알고 있어 선택 이유가 오염될 수 있는 사람.
- 자동화 검증만 수행하는 reviewer.

## 5. Playtest 준비물

- Text MUD log for selected run.
- JSON log for facilitator reference.
- [Human Playtest Protocol](../05_validation/18_Human_Playtest_Protocol_v0.1.md).
- [Human Playtest Feedback Form](../05_validation/19_Human_Playtest_Feedback_Form_v0.1.md).
- [Human Playtest Run 1 Result Template](../07_reviews/59_Human_Playtest_Run_1_Result_Template_v0.1.md).

Fresh evidence generated for this pack:

- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/playtest_seed_summary.json`
- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/playtest_seed_summary.csv`
- `.omo/ulw-loop/evidence/p1-human-playtest-scenario-pack-20260701/standard_run/`

## 6. Playtest Run 목록

All runs use:

```text
scenario: data/scenarios/standard_run_25_35_turn.yaml
profile: balanced
```

| Run | Name | Seed | Turn | Ending | Resource selections | Unique events | Primary observation |
|---:|---|---:|---:|---|---:|---:|---|
| 1 | Baseline Standard Run | 202 | 25 | prepared_frontier_route | 1 | 11 | P0 baseline readability |
| 2 | Resource Pressure Run | 101 | 25 | prepared_frontier_route | 2 | 11 | resource choice meaning |
| 3 | Clue / Omen Follow-up Run | 303 | 25 | prepared_frontier_route | 4 | 14 | clue/omen and event follow-up |
| 4 | Storylet Variety Run | 808 | 25 | prepared_frontier_route | 4 | 12 | variety under resource pressure |
| 5 | Optional Extended Watch Run | 707 | 25 | prepared_frontier_route | 1 | 12 | low-resource-choice watch sample |

## 7. Run 1. Baseline Standard Run

Configuration:

```text
scenario: data/scenarios/standard_run_25_35_turn.yaml
seed: 202
profile: balanced
```

Expected:

- 25 turns.
- `prepared_frontier_route`.
- `resource_alternative` selected at least once.
- Three cards every turn.

Observation goals:

- Does the player understand the Quest purpose?
- Do the choices read like actions in an adventure?
- Does 25 turns feel too long?
- Does the ending feel earned?
- Does the Quest Report explain what happened?

## 8. Run 2. Resource Pressure Run

Configuration:

```text
scenario: data/scenarios/standard_run_25_35_turn.yaml
seed: 101
profile: balanced
```

Expected:

- 25 turns.
- `prepared_frontier_route`.
- `resource_alternative` selected 2 times in autoplayer evidence.

Observation goals:

- Do supply/rest/resource choices feel meaningful?
- Are resource choices tempting, annoying, or invisible?
- Does resource pressure appear early enough to matter?
- Does the player notice food/health/money/reputation changes?

## 9. Run 3. Clue / Omen Follow-up Run

Configuration:

```text
scenario: data/scenarios/standard_run_25_35_turn.yaml
seed: 303
profile: balanced
```

Expected:

- 25 turns.
- `prepared_frontier_route`.
- `resource_alternative` selected 4 times in autoplayer evidence.
- Unique event count 14.

Observation goals:

- Do clues feel connected to later choices?
- Do omens feel like danger signals rather than decoration?
- Does the player remember earlier clue/omen information?
- Does the log make follow-up consequences legible?

## 10. Run 4. Storylet Variety Run

Configuration:

```text
scenario: data/scenarios/standard_run_25_35_turn.yaml
seed: 808
profile: balanced
```

Expected:

- 25 turns.
- `prepared_frontier_route`.
- `resource_alternative` selected 4 times in autoplayer evidence.
- Unique event count 12.

Observation goals:

- Does the player feel the same situation repeats?
- Does event/card/result sequencing feel connected?
- Does the middle of the run drag?
- Are repeated resource choices acceptable or noisy?

## 11. Run 5. Optional Extended Run

Configuration:

```text
scenario: data/scenarios/standard_run_25_35_turn.yaml
seed: 707
profile: balanced
```

Expected:

- 25 turns.
- `prepared_frontier_route`.
- `resource_alternative` selected 1 time in autoplayer evidence.
- Unique event count 12.

Purpose:

- Use only if the facilitator wants a second lower-bound watch sample.
- This is not a new P0 regression baseline.

Observation goals:

- Does low resource-alternative selection still feel playable to a human?
- Does the run feel too quest-progress dominant?
- Does the player still perceive resource pressure?

## 12. 관찰 지표

Quantitative:

- Turn count.
- Selected card slot_role distribution.
- `resource_alternative` selected count.
- Clue/omen follow-up appearance.
- Ending.
- Result type.
- Repeated card/event family notes.

Qualitative:

- Quest purpose clarity.
- Choice meaning.
- Repetition.
- Tension.
- Resource management meaning.
- Clue/omen readability.
- Text MUD readability.
- Ending acceptance.

## 13. 진행자 체크리스트

Before:

- Pick one run from this pack.
- Generate or open the Text MUD log.
- Keep JSON log available for after-session analysis.
- Give the player the protocol intro.
- Do not explain hidden mechanics before play.

During:

- Let the player read each turn.
- Ask the player to choose what they want to do, not what seems optimal.
- Record confusion, hesitation, excitement, and repeated complaints.
- Do not correct the player's interpretation unless the test is blocked.

After:

- Fill the feedback form.
- Summarize choice pattern and pain points.
- Record whether the run should feed Balance, Storylet, Director, Narrative, or UI work.

## 14. 완료 기준

This scenario pack is ready when:

- At least 3 run options are documented.
- Each run has seed/scenario/profile and observation goals.
- Protocol exists.
- Feedback form exists.
- Run 1 result template exists.
- P0 baseline guard is explicit.
- The next task can execute Human Playtest Run 1 without adding new gameplay/data.

## 15. 다음 작업

Recommended next task:

```text
CODEX_TASK_P1_Human_Playtest_Run_1_v0.1.md
```

That task should run one selected playtest, collect the feedback form, and fill the Run 1 result template.
