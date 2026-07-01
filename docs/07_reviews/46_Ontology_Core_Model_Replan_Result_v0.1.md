# [Current] Ontology Core Model Replan Result v0.1

> 상태: [Current] Ontology-lite에서 Ontology Core Model로 확장하기 위한 재설계 결과 문서.

## 1. 작업 목적

이번 작업은 FateWeaver의 현재 Ontology-lite/tag matching layer를 진짜 Ontology 기반 Situation Director로 발전시키기 위한 재설계 문서 작업이다.

구현은 하지 않았다. Schema, roadmap, review 문서만 작성했다.

## 2. 읽은 기준 문서

- `docs/04_codex/00_START_HERE_Gameplay_Replan_v0.1.md`
- `docs/06_plans/03_Playable_Text_Adventure_Replan_v0.1.md`
- `docs/01_foundation/03_Game_Structure_Replan_v0.1.md`
- `docs/02_schema/09_Content_Ontology_Model_v0.1.md`
- `docs/02_schema/10_Content_Sampling_Guide_v0.1.md`
- `docs/02_schema/11_Entity_Sampling_Catalog_v0.1.md`
- `docs/02_schema/12_Quest_Expedition_Card_Schema_v0.1.md`
- `docs/03_specs/13_Text_MUD_Gameplay_Simulator_Spec_v0.1.md`
- `docs/07_reviews/41_Data_Split_Coverage_Audit_v0.1.md`
- `docs/07_reviews/42_Content_Enrichment_Ultraresearch_Notes_v0.1.md`
- `docs/06_plans/08_Content_Enrichment_Catalog_v0.1.md`
- `docs/07_reviews/43_Enrichment_Pack_1_Card_Clue_Omen_Result_v0.1.md`
- `docs/07_reviews/44_Enrichment_Pack_2_Item_Ending_Result_v0.1.md`
- `docs/07_reviews/45_Standard_Run_25_35_Turn_Verification_Result_v0.1.md`
- `/Users/cheng80/Desktop/CODEX_TASK_Ontology_Core_Model_Replan_v0.1.md`

추가 확인:

- `data/core/ontology.yaml`
- `data/core/tags.yaml`
- `data/content/base/quests.yaml`
- `data/content/quests/*.yaml`
- `data/core/card_rules.yaml`
- `data/content/card_rules/*.yaml`
- `data/content/base/events.yaml`
- `data/content/events/*.yaml`
- `data/content/base/items.yaml`
- `data/content/base/endings.yaml`
- `src/fateweaver/gameplay_p0.py`
- `src/fateweaver/gameplay_p0_cards.py`
- `src/fateweaver/gameplay_p0_card_selection.py`
- `src/fateweaver/gameplay_p0_data.py`
- `src/fateweaver/gameplay_p0_sources.py`
- `src/fateweaver/gameplay_p0_objectives.py`

## 3. 현재 Ontology 판정

현재 FateWeaver의 Ontology는 P0 기준으로 Card Candidate Scoring과 Objective 연결에는 정상 작동한다.

현재 구조:

```text
Event tag → Card score
Event hint → Card score
Card objective match → Objective progress
Card result → next_event_tags 일부 누적
```

미완성 지점:

- `data/core/ontology.yaml`은 runtime engine이 아니라 계약/문서에 가깝다.
- Event selection은 주로 `quest_ids`, region, requirement, cooldown, `base_weight` 기반이다.
- `next_event_tags`, clue, omen, risk, prior choice를 이용해 다음 Storylet/Event 자체를 능동적으로 선택하는 Situation Director 역할은 아직 미완성이다.
- Entity / Relation / Fact / Rule 기반 runtime 추론은 아직 없다.

## 4. 작성한 문서

- `docs/02_schema/14_Ontology_Core_Model_v0.1.md`
  - Ontology-lite를 Entity / Relation / Fact / Rule / Situation Intent 기반 Ontology Core로 확장하기 위한 schema 설계 문서.

- `docs/06_plans/09_Ontology_Core_And_Director_Roadmap_v0.1.md`
  - Ontology Core Model에서 Reasoner-lite, Situation Director-lite, Standard Run 재검증까지 가는 실행 로드맵.

- `docs/07_reviews/46_Ontology_Core_Model_Replan_Result_v0.1.md`
  - 이번 replan 작업의 기준 문서, 판정, 설계 결정, 하지 않은 작업, 다음 추천 작업 기록.

- `docs/00_index/README_Docs_Index.md`
  - 새 schema/plan/review 문서 등록.

## 5. 핵심 설계 결정

1. 기존 tag 구조는 폐기하지 않는다.
2. `data/core/ontology.yaml`의 Ontology-lite 계약은 유지한다.
3. Entity / Relation / Fact는 tag 위에 얹는 추론 레이어로 추가한다.
4. Reasoner-lite는 deterministic rule matcher로 시작한다.
5. Situation Director-lite는 기존 Event selection을 대체하지 않고 weight modifier로 시작한다.
6. 모든 inference 결과는 trace/debug reason을 남긴다.
7. 첫 적용 category는 `local_problem`, `investigation_mystery`, `survival_exploration`으로 제한한다.

## 6. 기존 구조와의 호환성

- Quest:
  - 기존 objective type을 유지한다.
  - missing objective fact를 Situation Intent로 연결하는 방향을 문서화했다.

- Event / Storylet:
  - 기존 `storylet_tags`, `card_candidate_hints`, `cooldown_tags`, `repeat_group`, `base_weight`를 유지한다.
  - `ontology_refs`는 나중에 추가 가능한 참조 레이어로 둔다.

- Card:
  - 기존 `applies_to_storylet_tags`, `applies_to_quest_objectives`, `result` 구조를 유지한다.
  - `add_facts`는 Reasoner-lite 단계 후보로만 문서화했다.

- Clue:
  - fact 또는 evidence entity로 승격 가능하게 설계했다.
  - 진행을 막는 hard gate로 쓰지 않는 원칙을 명시했다.

- Omen:
  - foreshadow/risk/event weight modifier와 연결했다.

- Item:
  - enables card, modifies result, blocks/mitigates risk fact로 연결했다.
  - 항상 정답이 되지 않도록 cost/consume/opportunity loss 원칙을 유지했다.

- Ending:
  - fact/resource/outcome conditions로 확장 가능하게 정리했다.
  - 기존 `result_type`, `failure_kind`, `character_outcome` 의미는 유지한다.

## 7. 하지 않은 작업

- `data/` 수정 없음.
- `src/` 수정 없음.
- `tests/` 수정 없음.
- runtime reasoner 구현 없음.
- Situation Director 구현 없음.
- Quest/Card/Event/Item/Ending 추가 없음.
- 기존 tag 구조 폐기 없음.
- `data/core/ontology.yaml` 수정 없음.

## 8. 다음 추천 작업

1. Ontology Seed Data v0.1
   - 세 category의 Entity / Relation / Fact seed data를 작게 추가한다.

2. Ontology Validator v0.1
   - duplicate entity id, relation refs, rule refs, event/card ontology refs를 검증한다.

3. Reasoner-lite v0.1
   - facts + rules를 inference result로 변환하는 pure function을 추가한다.

4. Situation Director-lite Event Weighting v0.1
   - Event selection score에 inference result를 반영한다.

5. Standard Run Ontology Director Verification v0.1
   - 25~35 Turn 유지, event variety 증가, 반복 카드 감소, clue/omen trace를 baseline과 비교한다.

## 9. 리뷰 리스크

- 문서가 Reasoner-lite 또는 Situation Director 구현 완료처럼 읽히면 안 된다.
- `data/core/ontology.yaml`을 새 active runtime source of truth로 재정의하면 안 된다.
- tag matching layer를 대체한다고 읽히면 안 된다. tag는 fast matching layer로 유지한다.
- Validator와 inference trace 없이 Event weighting으로 바로 넘어가면 안 된다.
- commit에는 요청 문서 외 변경이 들어가면 안 된다.

## 10. 검증

요청 검증 명령:

```bash
git status --short

test -f docs/02_schema/14_Ontology_Core_Model_v0.1.md
test -f docs/06_plans/09_Ontology_Core_And_Director_Roadmap_v0.1.md
test -f docs/07_reviews/46_Ontology_Core_Model_Replan_Result_v0.1.md

grep -n "Ontology Core Model" docs/02_schema/14_Ontology_Core_Model_v0.1.md
grep -n "Entity" docs/02_schema/14_Ontology_Core_Model_v0.1.md
grep -n "Relation" docs/02_schema/14_Ontology_Core_Model_v0.1.md
grep -n "Situation Intent" docs/02_schema/14_Ontology_Core_Model_v0.1.md
grep -n "Reasoner-lite" docs/06_plans/09_Ontology_Core_And_Director_Roadmap_v0.1.md
grep -n "Situation Director-lite" docs/06_plans/09_Ontology_Core_And_Director_Roadmap_v0.1.md
grep -n "46_Ontology_Core_Model_Replan" docs/00_index/README_Docs_Index.md

git diff -- data
git diff -- src
git diff -- tests
```

기대:

- 새 문서 3개 존재.
- grep 항목 모두 존재.
- `data/`, `src/`, `tests/` diff 없음.
