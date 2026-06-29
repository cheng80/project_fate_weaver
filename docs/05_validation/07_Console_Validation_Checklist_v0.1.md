# Project FateWeaver Console Validation Checklist v0.1

## 목적

이 문서는 Console Validation 제작 착수 전 확인할 체크리스트다.

---

# 1. 구조 체크

- [ ] `docs/`가 존재한다.
- [ ] `data/core/`가 존재한다.
- [ ] `data/content/base/`가 존재한다.
- [ ] `data/content/packs/`가 존재한다.
- [ ] `data/scenarios/`가 존재한다.
- [ ] `src/fateweaver/`가 존재한다.
- [ ] `tools/`가 존재한다.
- [ ] `logs/`가 존재한다.
- [ ] `archive/`가 존재한다.
- [ ] `fate_weaver/`는 아직 생성하지 않았다.

---

# 2. 데이터 체크

- [ ] `data/core/statuses.yaml` 존재
- [ ] `data/core/tags.yaml` 존재
- [ ] `data/core/choice_types.yaml` 존재
- [ ] `data/core/item_roles.yaml` 존재
- [ ] `data/core/result_rules.yaml` 존재
- [ ] `data/content/base/regions.yaml` 존재
- [ ] `data/content/base/items.yaml` 존재
- [ ] `data/content/base/events.yaml` 존재
- [ ] `data/content/base/endings.yaml` 존재
- [ ] `data/scenarios/mvp0_console_test.yaml` 존재

---

# 3. 문서 체크

- [ ] README가 현재 구조를 설명한다.
- [ ] Baseline 문서가 현재 단계가 Console Validation임을 명시한다.
- [ ] Structure Guide가 각 폴더 책임을 설명한다.
- [ ] Data Architecture가 core/content/scenarios 구조를 설명한다.
- [ ] Console Simulator Spec이 scenario 기반 실행을 설명한다.
- [ ] Codex Brief가 금지 작업을 명시한다.
- [ ] Event Grammar가 scenario filter 문법을 설명한다.
- [ ] Console Simulator Spec이 unavailable choice 정책을 설명한다.
- [ ] Codex Brief가 combat policy를 설명한다.

---

# 4. Codex 작업 착수 조건

- [ ] Flutter 프로젝트 생성 금지 조건이 명시되어 있다.
- [ ] `fate_weaver/` 생성 금지 조건이 명시되어 있다.
- [ ] `data/mvp0/` 생성 금지 조건이 명시되어 있다.
- [ ] 허용 작업 범위가 명확하다.
- [ ] 실행 명령 3개가 명시되어 있다.


---

# 5. P0/P1 피드백 반영 체크

- [ ] `danger_tags: curse`가 core tag에 존재한다.
- [ ] `event_weight: lost`가 core tag에 존재한다.
- [ ] `regret_score`는 선택 단위 로그로 기록한다.
- [ ] `player_woven_score`는 Run 종료 회고로 기록한다.
- [ ] `requirements.txt`가 존재한다.
- [ ] `PyYAML` 의존성이 명시되어 있다.
- [ ] Flutter export JSON 계약 문서가 존재한다.
- [ ] dagger가 최소 2개 이벤트에서 의미 있게 사용된다.
- [ ] scenario filter의 include/exclude 문법이 문서와 데이터에서 일치한다.
- [ ] choice-level requires와 event-level requires가 분리되어 있다.
- [ ] unavailable choice는 show unavailable 기본 정책을 따른다.
- [ ] `influenced_by`, `regret_score`, `player_woven_score`의 타입/스케일/입력 주체가 명시되어 있다.
- [ ] Console Validation 재미 검증 지표가 summary 대상에 포함되어 있다.
- [ ] 전투형 이벤트는 일반 이벤트 + `combat_response` choice로만 처리한다.
