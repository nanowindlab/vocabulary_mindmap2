# Planning Detailed Report Log

> Agent: `기획 에이전트`
> Revision: `V1-REV-77`
> Logged: `2026-03-14`
> Status: `PROPOSAL ONLY / NOT APPLIED`
> Purpose: `V1-REV-74/75/76`와 Codex draft를 흡수해 relation model의 implementation architecture를 proposal 수준으로 닫기
> Rule: canonical policy / roadmap / tasklist / SOP / runtime guide는 **Codex 검토 + 사용자 승인 전 미반영**
> Reporting Rule: `append-only only`

## Scope

- `V1-REV-74` semantic proposal의 execution architecture 보강
- `V1-REV-75` 구조 리뷰와 `V1-REV-76` 비판 리뷰의 누락 포인트 흡수
- rich internal canonical / thin runtime projection / rebuild trigger matrix / pilot-first 전략 정리
- owner 문서별 patch 방향과 다음 data/review/dev cycle handoff input proposal 작성

## Inputs Absorbed

- `.gemini-orchestration/workboard_archive/planning/20260314_REV74_relation_model_execution_closure_proposal.md`
- `.gemini-orchestration/workboard_archive/data/20260314_REV75_rev74_structure_review.md`
- `.gemini-orchestration/workboard_archive/review/20260314_REV76_planning_review_report.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV74_canonical_delta_draft_by_codex.md`
- `08_expansion/references/relation_model_research/20260314_relation_model_deep_research_report_v1.md`
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `09_app/public/data/README.md`
- `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`

## 문제 진단

### 1. `REV74` proposal의 현재 한계

- semantic redefinition은 충분했지만, data agent가 바로 집행할 implementation owner가 닫히지 않았다.
- 특히 아래 4개가 비어 있었다.
  - richer relation을 어디에 authoritative하게 저장할지
  - thin runtime에 무엇만 투영할지
  - 어떤 변경이 rebuild/redeploy를 강제하는지
  - 8.1K 전면 전환 전 pilot을 어떻게 자를지

### 2. 현재 구현 현실

- runtime canonical:
  - `09_app/public/data/live/APP_READY_*`
- internal support zone:
  - `09_app/public/data/internal/`
  - 역할 정의상 app이 직접 fetch하지 않는 canonical support file zone
- current relation builder input:
  - `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`
  - 현재는 `source_id -> [{target_id, hook_id, reason}]` dict shape
- current live publish:
  - `related_vocab`는 `string[]`
  - `refs.cross_links`는 `target_id/target_term/target_system/target_root/target_category/hook_id`
- current rebuild dependency:
  - relation selection rule이 바뀌면 `publish-only -> chunk rebuild` 전체가 강제됨

### 3. implementation architecture 관점의 핵심 제약

- 현재 app은 non-word node를 직접 소비하지 못한다.
- 따라서 이번 cycle에서 scene/grammar/idiom node를 runtime에 바로 노출하면 dev 범위가 급격히 커진다.
- 동시에 learner-facing relation semantics를 내부적으로 richer하게 저장하지 않으면, 다음 cycle마다 reason/purpose를 다시 잃는다.

## 해결안

### 1. Recommended Architecture

- 추천안:
  - `single rich internal canonical + thin runtime projection + pilot-first rollout`
- 핵심 원칙:
  - semantics는 rich internal graph에서 보존
  - current runtime은 backward-compatible thin projection 유지
  - full 8.1K rebuild 전, anchor-focused pilot로 schema/selection/tie-breaker 검증

### 2. Storage Architecture Options

#### Option 1. Recommended: `internal/`에 신규 rich canonical graph 추가

- candidate path:
  - `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- 이유:
  - `internal/`은 이미 canonical support file zone으로 정의되어 있음
  - `live/`와 분리되어 runtime-safe
  - `rev47/`처럼 실행 회차 이름에 묶이지 않아 장기 owner가 안정적
- 장점:
  - 문서 owner와 저장 위치가 더 잘 맞는다
  - future graph expansion에 유리하다
  - runtime/live와 internal canonical을 명확히 분리할 수 있다
- 리스크:
  - SOP와 builder input path를 함께 바꿔야 한다
  - 초기 스크립트 수정 범위가 생긴다

#### Option 2. Minimal Change: `REV47_RELATED_LINKS_V1.json`을 rich canonical로 승격

- candidate path:
  - `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`
- 장점:
  - 현재 pipeline과 가장 가깝다
  - builder input을 새로 배선할 필요가 적다
- 리스크:
  - run-specific path가 canonical owner처럼 오해될 수 있다
  - 문서 구조 원칙상 장기 SSOT로는 부자연스럽다

#### Option 3. Big Bang Runtime Uplift

- 내용:
  - rich record를 곧바로 `live/`에 싣고 app이 바로 소비하게 함
- 장점:
  - learner-purpose 정보가 즉시 UI에 노출된다
- 리스크:
  - `App.jsx`, `TermDetail.jsx`, chunk rebuild, review contract가 동시에 흔들린다
  - 이번 phase gate를 넘는다

### 3. Final Recommendation

- 추천안: `Option 1`
- 운영 결론:
  - authoritative rich relation storage는 `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`에 둔다
  - 현재 `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`는 transition period 동안
    - derived builder artifact 또는 compatibility export
    로 다룬다

## Rich Internal Canonical Contract

### 1. Data Model Principle

- internal canonical은 `edge-first graph`로 저장
- runtime projection은 이 graph에서 role/display intent에 따라 생성
- source-target pair는 한 개 이상의 semantic role을 가질 수 있지만, runtime projection에는 primary display intent 하나만 보낸다

### 2. Proposed Schema

```json
{
  "schema_version": "RELATION_GRAPH_V1",
  "source_basis": "pilot_or_full",
  "relations_by_source": {
    "아침_일반명사-1": [
      {
        "edge_id": "아침_일반명사-1__scene_jump__아침식사_일반명사-1",
        "target_id": "아침식사_일반명사-1",
        "target_term": "아침식사",
        "target_system": "상황과 장소",
        "target_root": "식생활",
        "target_category": "식사 메뉴와 종류",
        "display_intent": "jump_link",
        "relation_role": "topic_expand",
        "jump_purpose": "scene_jump",
        "reason": "시간 anchor를 실제 일상 장면으로 확장",
        "hook_id": "H04",
        "scope": "sense",
        "constraints": {
          "source_anchor_type": "time_coordinate",
          "priority_bucket": "A",
          "node_type_pair": "word_to_word"
        },
        "provenance": {
          "method": "pilot_curation",
          "review_state": "proposal"
        }
      }
    ]
  }
}
```

### 3. Required Fields

- `edge_id`
- `target_id`
- `target_term`
- `target_system`
- `target_root`
- `target_category`
- `display_intent`
- `relation_role`
- `jump_purpose`
- `reason`
- `hook_id`
- `scope`
- `constraints`
- `provenance`

### 4. Enum Proposal

- `display_intent`
  - `related_widget`
  - `jump_link`
- `relation_role`
  - `compare`
  - `substitute`
  - `contrast_lite`
  - `scope_expand`
  - `topic_expand`
  - `pattern_anchor`
  - `collocation`
  - `sociopragmatic_variant`
  - `sense_bridge`
- `jump_purpose`
  - `scene_jump`
  - `grammar_anchor`
  - `usage_route`
  - `sense_disambiguation`
  - `collocation_expand`
  - `pragmatics_shift`
- `scope`
  - `lemma`
  - `sense`

### 5. Runtime-Safe Constraint

- 이번 cycle의 pilot / rebuild에서는 `constraints.node_type_pair = word_to_word`만 허용
- `word_to_scene`, `word_to_grammar`, `word_to_idiom`은 schema reserve만 하고 runtime projection에는 사용하지 않음
- 이유:
  - current frontend는 word node만 안정적으로 소비 가능

## Thin Runtime Projection Rule

### 1. Projection Goal

- current `live/` schema와 UI contract는 이번 cycle에서 최대한 유지
- richer semantics는 internal canonical에만 저장
- runtime에는 navigation-safe minimum만 투영

### 2. Projection Mapping

#### `related_vocab`

- source:
  - internal graph edges where `display_intent = related_widget`
- destination:
  - `APP_READY_*_TREE.json`
  - `APP_READY_SEARCH_INDEX.json`
  - chunk rebuild output
- projection shape:
  - `string[]`
- projection rule:
  - `target_term`만 추출
  - same target dedupe
  - max `5`

#### `refs.cross_links`

- source:
  - internal graph edges where `display_intent = jump_link`
- destination:
  - `APP_READY_*_TREE.json`
  - `APP_READY_SEARCH_INDEX.json`
  - chunk rebuild output
- projection shape:
  - current object shape 유지
- projected fields:
  - `target_id`
  - `target_term`
  - `target_system`
  - `target_root`
  - `target_category`
  - `hook_id`

### 3. Optional Display Extension

- `jump_purpose_label`는 이번 cycle 기본 scope에서 제외
- dev gate reopen 후 optional field로 별도 검토
- 이유:
  - current UI field contract 유지가 우선

## Tie-Breaker / Conflict Rule

### 1. Primary Rule

- 같은 source-target pair에 복수 semantic role이 있어도 runtime projection은 1회만 노출

### 2. Precedence

1. `sense_disambiguation`
2. `grammar_anchor`
3. `scene_jump`
4. `collocation_expand`
5. `compare`
6. `substitute`
7. `contrast_lite`
8. `scope_expand`

### 3. Display Intent Resolution

- learner가 현재 화면에서 바로 비교해야 하면 `related_widget`
- learner가 다른 장면/기능/문형으로 이동해야 하면 `jump_link`
- 아래는 항상 `jump_link` 우선
  - `grammar_anchor`
  - `scene_jump`
  - `sense_disambiguation`
- 아래는 기본적으로 `related_widget` 우선
  - `compare`
  - `substitute`
  - `contrast_lite`
  - `scope_expand`

### 4. Duplicate Storage Rule

- internal graph에는 secondary role을 `constraints.secondary_roles`로 보존 가능
- runtime에는 source-target pair를 `related_vocab`와 `cross_links`에 동시에 중복 저장하지 않음

## Rebuild Trigger Matrix

| change type | internal canonical only | publish-only | chunk rebuild | review mandatory | dev mandatory |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `reason`, `provenance`, `secondary_roles`만 수정 | yes | no | no | targeted | no |
| `relation_role` 변경 but `display_intent`/target unchanged | yes | no | no | targeted | no |
| `display_intent` 변경 | no | yes | yes | yes | no |
| `target_id` / target path / selection set 변경 | no | yes | yes | yes | no |
| `related_vocab` selection rule 변경 | no | yes | yes | yes | no |
| `cross_links` selection rule 변경 | no | yes | yes | yes | no |
| `jump_purpose_label` 등 runtime thin field 추가 | no | yes | yes | yes | yes |
| new node type(`word_to_scene`, `word_to_grammar`) runtime 노출 | no | yes | yes | yes | yes |
| `chunk_id` partition 영향 변경 | no | yes | yes | yes | yes |

### Mandatory Apply Order

1. internal canonical update
2. `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
3. `python3 scripts/core/rebuild_rev23_detail_chunks.py`
4. validation evidence collection
5. review acceptance
6. optional dev reopen

## Pilot-First Execution Strategy

### 1. Why Pilot First

- `REV76`가 지적한 대로 8.1K 전체 big bang은 migration cost와 review cost가 크다
- current runtime은 word node only라 pilot으로 runtime-safe path를 먼저 검증하는 편이 맞다

### 2. Recommended Pilot Scope

- batch size:
  - `200~500` source terms
- priority buckets:
  - `P1` time/calendar anchors
  - `P2` temporal grammar anchors
  - `P3` scene bridge words directly attached to P1/P2

### 3. Pilot Candidate Families

- time/calendar anchors:
  - 요일
  - 계절
  - 시점
  - 날짜/기간
- temporal grammar anchors:
  - `부터`
  - `까지`
  - `전`
  - `후`
  - `-ㄴ/은 지`
  - `무렵`
  - `월말`
  - `주말`
- scene bridge words:
  - 약속
  - 일정
  - 수업
  - 출근
  - 영업
  - 식사

### 4. Pilot Acceptance Questions

- richer internal schema가 current build pipeline과 양립하는가
- tie-breaker가 실제 ambiguous pair를 안정적으로 정리하는가
- 시간 anchor jump가 learner scenario를 실제로 개선하는가
- runtime thin projection이 current UI를 깨지 않는가

## Owner 문서

### Primary Patch Directions

#### `08_expansion/RELATION_DATA_POLICY_V1.md`

- add:
  - learner-facing semantics
  - rich internal canonical contract
  - thin runtime projection rule
  - tie-breaker and duplicate rule
  - pilot node-type restriction

#### `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`

- add:
  - new internal canonical input path
  - rebuild trigger matrix
  - validation evidence checklist
  - optional dev-coupled trigger note

#### `09_app/public/data/README.md`

- add:
  - `internal/RELATION_GRAPH_CANONICAL_V1.json` role 설명
  - live vs internal relation owner boundary

#### `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`

- add:
  - pilot-first work package
  - `rich internal canonical -> thin runtime projection -> review acceptance` chain
  - done criteria for pilot and full rollout 분리

#### `08_expansion/MASTER_ROADMAP_V1.md`

- adjust:
  - phase 3 wording to include
    - policy closure
    - pilot validation
    - full rebuild only after pilot accept

#### `08_expansion/PROJECT_DECISION_LOG_V1.md`

- add:
  - storage architecture 결정
  - thin runtime 유지 결정
  - pilot-first 전략 결정

### Secondary Dependent Patch Directions

#### `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`

- add:
  - reviewer가 internal canonical과 live projection을 구분해 읽도록 안내

#### `09_app/README.md`

- add:
  - runtime canonical은 계속 `live/`
  - relation semantic authority는 `internal/` support graph에서 온다는 안내

## 다음 순서

### Apply Order Proposal

1. Codex 검토
2. 사용자 승인
3. owner 문서 patch 확정
4. internal canonical schema template 생성
5. pilot batch 선정
6. data publish/rebuild
7. review acceptance
8. optional dev reopen

### Handoff Input By Team

#### To Data Agent

- approved internal schema
- pilot term list
- tie-breaker table
- projection rule
- rebuild trigger matrix
- validation checklist

#### To Review Agent

- pilot target inventory
- before/after relation diff
- validation evidence template
- pilot-specific acceptance questions

#### To Development Agent

- current cycle에서는 기본적으로 no-op
- reopen 조건:
  - runtime thin field 추가 승인
  - 또는 `target_term` fallback deprecation 승인

## 완료 기준

### REV77 Planning Done Criteria

- rich internal canonical 저장 위치가 제안됨
- thin runtime projection rule이 제안됨
- rebuild trigger matrix가 작성됨
- pilot-first 전략이 작성됨
- owner 문서별 patch 방향이 정리됨
- data/review/dev handoff input이 정리됨
- canonical 미반영 상태가 명시됨

### Next Cycle Open Gate

- Codex 검토 완료
- 사용자 승인 완료
- owner docs patch 확정
- pilot batch 범위 합의

## Open Risks

- `internal/` 신규 canonical 도입 시 script path 변경 범위가 생긴다
- scene/grammar/idiom non-word node는 current runtime에서 아직 직접 처리 불가
- pilot과 full rollout 사이에 transition artifact 관리 규칙이 추가로 필요하다
- `REV47_RELATED_LINKS_V1.json`의 deprecation timing은 별도 결정이 필요하다

## Recommendation

- 이번 cycle은 `semantic ambition`보다 `runtime-safe execution architecture`를 우선한다
- 즉,
  - internal은 rich
  - runtime은 thin
  - rollout은 pilot-first
  - dev reopen은 review acceptance 뒤
- 이 순서가 현재 phase gate와 가장 잘 맞는다
