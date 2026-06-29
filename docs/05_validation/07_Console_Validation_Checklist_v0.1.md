# Project FateWeaver Console Validation Checklist v0.1

## 목적

이 문서는 Console Validation 제작 착수 전 확인할 체크리스트다.

## 검수 상태

```text
Status: PASS
검수일: 2026-06-29
대상: Console Validation preflight + implementation readiness
판정: Console Validation 구현 착수/검증 기준 충족
```

근거:

- `docs/07_reviews/10_Console_Simulator_Review_Result_v0.1.md`
- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C001-validate-data.txt`
- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C002-console-simulator.txt`
- `.omo/ulw-loop/019f1277-b56b-7563-9d98-8ea17d567042/evidence/C003-analyze-logs.txt`
- `.omo/evidence/final-choice-resolver-re-review-code-review.md`

---

# 1. 구조 체크

- [x] `docs/`가 존재한다.
- [x] `data/core/`가 존재한다.
- [x] `data/content/base/`가 존재한다.
- [x] `data/content/packs/`가 존재한다.
- [x] `data/scenarios/`가 존재한다.
- [x] `src/fateweaver/`가 존재한다.
- [x] `tools/`가 존재한다.
- [x] `logs/`가 존재한다.
- [x] `archive/`가 존재한다.
- [x] `fate_weaver/`는 아직 생성하지 않았다.

---

# 2. 데이터 체크

- [x] `data/core/statuses.yaml` 존재
- [x] `data/core/tags.yaml` 존재
- [x] `data/core/choice_types.yaml` 존재
- [x] `data/core/item_roles.yaml` 존재
- [x] `data/core/result_rules.yaml` 존재
- [x] `data/content/base/regions.yaml` 존재
- [x] `data/content/base/items.yaml` 존재
- [x] `data/content/base/events.yaml` 존재
- [x] `data/content/base/endings.yaml` 존재
- [x] `data/scenarios/mvp0_console_test.yaml` 존재

---

# 3. 문서 체크

- [x] README가 현재 구조를 설명한다.
- [x] Baseline 문서가 현재 단계가 Console Validation임을 명시한다.
- [x] Structure Guide가 각 폴더 책임을 설명한다.
- [x] Data Architecture가 core/content/scenarios 구조를 설명한다.
- [x] Console Simulator Spec이 scenario 기반 실행을 설명한다.
- [x] Codex Brief가 금지 작업을 명시한다.
- [x] Event Grammar가 scenario filter 문법을 설명한다.
- [x] Console Simulator Spec이 unavailable choice 정책을 설명한다.
- [x] Codex Brief가 combat policy를 설명한다.

---

# 4. Codex 작업 착수 조건

- [x] Flutter 프로젝트 생성 금지 조건이 명시되어 있다.
- [x] `fate_weaver/` 생성 금지 조건이 명시되어 있다.
- [x] `data/mvp0/` 생성 금지 조건이 명시되어 있다.
- [x] 허용 작업 범위가 명확하다.
- [x] 실행 명령 3개가 명시되어 있다.


---

# 5. P0/P1 피드백 반영 체크

- [x] `danger_tags: curse`가 core tag에 존재한다.
- [x] `event_weight: lost`가 core tag에 존재한다.
- [x] `regret_score`는 선택 단위 로그로 기록한다.
- [x] `player_woven_score`는 Run 종료 회고로 기록한다.
- [x] `requirements.txt`가 존재한다.
- [x] `PyYAML` 의존성이 명시되어 있다.
- [x] Flutter export JSON 계약 문서가 존재한다.
- [x] dagger가 최소 2개 이벤트에서 의미 있게 사용된다.
- [x] scenario filter의 include/exclude 문법이 문서와 데이터에서 일치한다.
- [x] choice-level requires와 event-level requires가 분리되어 있다.
- [x] unavailable choice는 show unavailable 기본 정책을 따른다.
- [x] `influenced_by`, `regret_score`, `player_woven_score`의 타입/스케일/입력 주체가 명시되어 있다.
- [x] Console Validation 재미 검증 지표가 summary 대상에 포함되어 있다.
- [x] 전투형 이벤트는 일반 이벤트 + `combat_response` choice로만 처리한다.

---

# 6. 구현 후 리뷰 차단 이슈 반영 체크

- [x] malformed scenario/schema 입력은 traceback이 아니라 `VALIDATION: ERROR`로 실패해야 한다.
- [x] validator는 `statuses`, `tags`, `choice_types`, `item_roles`, `result_rules`를 모두 로드하고 참조 무결성을 검사해야 한다.
- [x] `event_weight` target은 `weight_target` enum에 존재해야 한다.
- [x] item role/tag, event region/event/danger tag는 core enum과 일치해야 한다.
- [x] `tools/*.py`는 얇은 CLI wrapper로 유지하고, simulator loop는 `src/fateweaver/`에 둔다.
- [x] TTY mode는 choice-level/player-level 입력을 받고, non-TTY mode는 입력 대기 없이 AutoPlayer 값을 기록한다.
- [x] run tag requirement는 status requirement와 독립적으로 테스트한다.
- [x] Console Validation 테스트는 invalid fixture, filter include/exclude/default, unavailable choice, state transition, analyzer empty logs, combat-as-ordinary-event를 포함해야 한다.
