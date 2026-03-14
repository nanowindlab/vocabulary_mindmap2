# Data Pilot Preparation Proposal

> Agent: `데이터 에이전트`
> Revision: `V1-REV-79`
> Logged: `2026-03-14 22:58:00`
> Scope: `RELATION_GRAPH_CANONICAL_V1.json skeleton / pilot anchor batch / dry-run prep checklist`
> Reporting Rule: `append-only only`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260314_REV79_pilot_preparation_assignment.md`

## Supporting Contract Read

- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `09_app/public/data/README.md`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`

## Proposal Summary

- recommendation:
  - 이번 revision에서는 `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`의 **empty skeleton + field contract**만 준비한다.
  - pilot anchor batch는 **12개 core anchors + 4개 ambiguity holdout**로 제한한다.
  - dry-run은 **실제 publish/rebuild 없이** baseline inventory, field resolution, projection rule, gate evidence 준비까지만 수행하도록 설계한다.

## Proposed Empty Skeleton

```json
{
  "version": "V1",
  "status": "pilot_skeleton",
  "schema_mode": "rich_internal_canonical",
  "generated_at": null,
  "authority": {
    "canonical_path": "09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json",
    "runtime_projection_mode": "thin_runtime",
    "runtime_targets": [
      "09_app/public/data/live/APP_READY_SITUATIONS_TREE.json",
      "09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json",
      "09_app/public/data/live/APP_READY_BASICS_TREE.json",
      "09_app/public/data/live/APP_READY_SEARCH_INDEX.json"
    ]
  },
  "field_contract": {
    "node_key": "id",
    "edge_key": "edge_id",
    "runtime_safe_relation_types": [
      "word_to_word"
    ],
    "reserved_relation_types": [
      "word_to_scene",
      "word_to_grammar",
      "word_to_idiom"
    ],
    "required_node_fields": [
      "id",
      "word",
      "pos",
      "system",
      "root",
      "category",
      "chunk_id",
      "anchor_family"
    ],
    "required_edge_fields": [
      "edge_id",
      "source_id",
      "target_id",
      "target_term",
      "target_system",
      "target_root",
      "target_category",
      "display_intent",
      "relation_role",
      "jump_purpose",
      "reason",
      "hook_id",
      "scope",
      "constraints",
      "provenance"
    ],
    "optional_edge_fields": [
      "secondary_roles",
      "priority_bucket",
      "review_state",
      "notes"
    ]
  },
  "pilot": {
    "batch_id": "pilot_anchor_batch_v1",
    "selection_rule": "coordinate_time_anchors_only",
    "dry_run_only": true,
    "include_term_ids": [],
    "holdout_term_ids": [],
    "excluded_relation_types": [
      "word_to_scene",
      "word_to_grammar",
      "word_to_idiom"
    ]
  },
  "nodes": {},
  "edges": [],
  "dry_run_reserve": {
    "pre_publish_checks": [],
    "projection_preview": [],
    "gate_evidence": []
  }
}
```

## Skeleton Design Notes

- `source_id`를 edge 필수 필드로 추가 제안:
  - 정책 문서의 최소 필드는 target 중심이지만, canonical graph skeleton에는 source 없이 edge를 독립적으로 검증하기 어렵다.
- `nodes`와 `edges`를 분리:
  - live thin projection은 edge만으로 만들 수 있어도, pilot 단계의 anchor batch 검증에는 node inventory와 edge inventory를 분리하는 편이 안전하다.
- `word_to_scene`, `word_to_grammar`, `word_to_idiom`은 reserve only:
  - policy가 허용하는 richer canonical 방향은 유지하되, 이번 pilot은 runtime-safe `word_to_word` 범위로 제한한다.

## Recommended Pilot Anchor Batch

### Core 12 anchors

- relative-day:
  - `오늘_일반명사-1`
  - `내일_일반명사-1`
  - `어제_일반명사-1`
- day-part:
  - `아침_일반명사-1`
  - `저녁_일반명사-1`
  - `밤_일반명사-1`
- week-anchor:
  - `월요일_일반명사-1`
  - `금요일_일반명사-1`
  - `주말_일반명사-1`
- season-anchor:
  - `봄_일반명사-1`
  - `여름_일반명사-1`
  - `겨울_일반명사-1`

### Ambiguity holdout 4

- `오늘_일반부사-1`
- `어제_일반부사-1`
- `점심_일반명사-1`
- `저녁_일반명사-2`

## Why This Batch

- current live evidence:
  - 시간 관련 대형 루트는 `구조와 기초 > 시간과 흐름`에 `405`개 항목이 있음
  - pilot은 그중 learner-facing anchor 성격이 강한 소규모 코어만 뽑아야 함
- current link evidence:
  - `내일`, `오늘`, `월요일`, `주말`, `여름`, `겨울` 등은 현재 cross-link가 `0`이거나 매우 적어 gap 확인에 적합함
  - `아침`, `저녁`, `금요일`, `봄`, `가을`처럼 일부 link가 이미 있는 anchor도 포함해 기존 projection과의 비교가 가능함
- ambiguity control:
  - 부사 sense와 식생활 sense는 첫 pilot에 섞지 않고 holdout으로 분리하는 편이 skeleton 검증에 유리함

## Proposed Pilot Boundaries

- in-scope:
  - `word_to_word` anchor relation only
  - `display_intent`가 `related_vocab` 또는 `cross_links`로 투영 가능한 edge만 준비
  - `hook_id`, `reason`, `jump_purpose`가 최소 내부 canonical 수준에서 채워질 수 있는 구조 설계
- out-of-scope for REV79:
  - actual publish
  - actual chunk rebuild
  - runtime live overwrite
  - full 8.5K anchor expansion
  - UI label 변경

## Dry-Run Preparation Checklist

### A. file / contract readiness

- `09_app/public/data/internal/` 경로 존재 확인
- skeleton top-level contract 확정
- node 필수 필드와 edge 필수 필드 이름 고정
- runtime projection mode가 `thin_runtime`로 고정되어 있는지 확인

### B. pilot inventory readiness

- core 12 / holdout 4의 term id 목록 확정
- 각 anchor의 current system/root/category/chunk_id baseline 캡처
- 각 anchor의 current `related_vocab` count / `cross_links` count baseline 캡처
- duplicate sense 충돌 여부 확인

### C. projection rule readiness

- `display_intent -> related_vocab/cross_links` 매핑 규칙 명시
- same-classification edge는 `related_vocab` projection 후보인지 확인
- cross-classification edge는 `refs.cross_links` projection 후보인지 확인
- `reason`, `provenance`, `secondary_roles`는 internal-only 유지인지 명시

### D. dry-run evidence package

- pilot batch inventory table
- empty skeleton JSON proposal
- projection preview 표
- rebuild trigger matrix 복기
- publish/rebuild 금지 범위 명시

### E. pre-execution safety gate

- 이번 revision에서 `run_rev47_xwd_mining.py --publish-only` 실행 금지 확인
- 이번 revision에서 `rebuild_rev23_detail_chunks.py` 실행 금지 확인
- live/runtime 파일 overwrite 금지 확인
- review handoff용 evidence 항목 초안만 준비하고 실제 검증 수치 보고는 보류

## Next Execution Recommendation

- 추천안:
  - `REV79`는 skeleton + pilot scope + dry-run packet까지만 마감
  - 그 다음 revision에서 승인 후 pilot batch만 relation graph canonical에 채우고 projection preview를 만든 뒤, 별도 승인 후에만 publish/rebuild로 넘어간다
- 장점:
  - canonical contract를 먼저 고정할 수 있다
  - anchor ambiguity를 작은 배치에서 통제할 수 있다
  - live runtime 오염 없이 다음 단계 증거를 준비할 수 있다
- 리스크:
  - pilot 결과를 보기 전까지는 전수 확장 추정이 보수적으로 남는다

## Non-Execution Note

- 이번 revision에서는 실제 publish/rebuild를 실행하지 않는다
- control field 수정 없이 append-only 로그로만 제안안을 남긴다
