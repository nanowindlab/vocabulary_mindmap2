# Patch Draft For Canonical Docs

> Source:
> - `.gemini-orchestration/workboard_archive/planning/20260314_REV77_implementation_architecture_proposal.md`
> - `.gemini-orchestration/workboard_archive/data/20260314_REV75_rev74_structure_review.md`
> - `.gemini-orchestration/workboard_archive/review/20260314_REV76_planning_review_report.md`
>
> Status: `DRAFT / NOT APPLIED`
> Purpose: `REV-77` implementation architecture proposal을 canonical 문서에 반영하기 위한 patch-level 초안

## 1. RELATION_DATA_POLICY_V1.md Patch Draft

### Add after `## 2. 핵심 정의`

```md
### learner-facing relation 재정의

현재 relation 정책은 분류 경계만으로는 충분하지 않다.
relation은 학습자가 현재 단어에서 무엇을 비교하고, 무엇으로 점프하며, 왜 이동해야 하는지를 설명하는 학습 장치여야 한다.

#### `related_vocab`

`related_vocab`는 현재 단어를 **같은 화면 안에서 비교, 대체, 대조, 국소 확장**하는 learner-neighborhood다.

기본 질문:

- 이 단어와 같이 보여 줄 때 학습자의 이해/선택/생산이 쉬워지는가?

대표 역할:

- `compare`
- `substitute`
- `contrast_lite`
- `scope_expand`

#### `refs.cross_links`

`refs.cross_links`는 현재 단어를 이해한 뒤 **다음 학습 단계로 이동시키는 next-step jump**다.

기본 질문:

- 이 단어를 알았을 때 어디로 이동하면 실제 사용이 쉬워지는가?

대표 역할:

- `scene_jump`
- `grammar_anchor`
- `usage_route`
- `sense_disambiguation`
```

### Add new section before current runtime rule

```md
## 4. internal canonical relation layer

이번 cycle에서는 learner-facing relation semantics를 richer internal canonical layer에 보존하고, runtime live에는 thin projection만 내보낸다.

권장 authoritative 저장 위치:

- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`

최소 필드:

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

이번 cycle의 runtime-safe 제한:

- internal canonical은 richer schema를 허용
- runtime projection은 `word_to_word` 관계만 대상으로 유지
- `word_to_scene`, `word_to_grammar`, `word_to_idiom`은 schema reserve만 하고 live runtime에는 직접 노출하지 않는다
```

### Add projection rule

```md
## 5. thin runtime projection rule

### `related_vocab`

- source: internal canonical edges with `display_intent = related_widget`
- destination: `APP_READY_*_TREE.json`, `APP_READY_SEARCH_INDEX.json`, detail chunk
- projection shape: `string[]`
- rule:
  - `target_term`만 추출
  - same target dedupe
  - max `5`

### `refs.cross_links`

- source: internal canonical edges with `display_intent = jump_link`
- destination: `APP_READY_*_TREE.json`, `APP_READY_SEARCH_INDEX.json`, detail chunk
- projection shape: current object shape 유지
- projected fields:
  - `target_id`
  - `target_term`
  - `target_system`
  - `target_root`
  - `target_category`
  - `hook_id`

### optional field note

- `jump_purpose_label` 등 learner-purpose 라벨은 후속 dev gate에서 검토한다
```

### Add tie-breaker / duplicate rule

```md
## 6. tie-breaker / duplicate rule

같은 source-target pair에 복수 semantic role이 있어도 runtime projection은 1회만 노출한다.

display intent precedence:

1. `sense_disambiguation`
2. `grammar_anchor`
3. `scene_jump`
4. `collocation_expand`
5. `compare`
6. `substitute`
7. `contrast_lite`
8. `scope_expand`

중복 저장 금지:

- 같은 source-target pair를 `related_vocab`와 `refs.cross_links`에 동시에 중복 저장하지 않는다
- secondary role은 internal canonical의 `constraints.secondary_roles`에만 보존 가능
```

### Add time-anchor obligation

```md
## 7. time-anchor / grammar-anchor obligation

`Basics`로 이관된 시간, 계절, 요일, 시점 anchor는 learner scene로 이어지는 `Situations` jump를 최소 1개 이상 가져야 한다.

단, 단순 분류 차이만으로 jump를 만들지 않고 아래를 만족해야 한다.

- `jump_purpose`가 명시됨
- learner가 왜 이동해야 하는지 `reason`이 있음
- scene/grammar/usage 중 하나의 학습 과업을 실제로 열어 줌
```

## 2. APP_DATA_REDEPLOY_SOP_V1.md Patch Draft

### Replace authoritative input section with internal canonical note

```md
### 권위 입력

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`

transition note:

- `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`는 transition period 동안 builder compatibility input으로 유지 가능
```

### Add rebuild trigger matrix

```md
## 3.1. rebuild trigger matrix

아래 변경은 runtime redeploy mandatory다.

- `related_vocab` selection rule 변경
- `refs.cross_links` selection rule 변경
- `target_id` 또는 target path metadata 변경
- `display_intent` 변경
- `chunk_id` partition 영향 변경

아래 변경은 internal canonical만 갱신하고 redeploy를 생략할 수 있다.

- `reason`
- `provenance`
- `secondary_roles`
- `relation_role` 변경(단, runtime projection 결과 불변일 때)
```

### Add stronger acceptance evidence

```md
## 4.1. gate evidence checklist

data -> review gate 전 아래 증거를 모두 남긴다.

- split 총합 = search total
- search `chunk_id` 존재 = 전체 term 수
- split `chunk_id` 존재 = 각 파일 전체 term 수
- `related_vocab` target 누락 `0`
- `related_vocab` 타분류 오염 `0`
- `cross_links` 동일분류 오염 `0`
- `cross_links` 타깃 누락 `0`
- legacy `target_center_id` 잔존 `0`
- `CHUNK_MANIFEST_V1.json` 생성 확인
- detail chunk와 live tree relation 일치 확인
```

## 3. 09_app/public/data/README.md Patch Draft

### Add internal relation graph explanation

```md
- `internal/`
  - rebuild 및 검증 보조용 내부 파일
  - relation semantics의 richer canonical support file을 둘 수 있는 zone
  - 예: `RELATION_GRAPH_CANONICAL_V1.json`

주의:

- `internal/`은 app이 직접 fetch하는 runtime source가 아니다
- learner-facing relation semantics를 풍부하게 저장하더라도, current live runtime에는 thin projection만 보낸다
```

## 4. SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md Patch Draft

### Tighten `T1.34`

```md
- [ ] `rich internal canonical`, `thin runtime projection`, `rebuild trigger matrix`, `pilot-first 전략`을 implementation architecture acceptance로 포함할 것.
```

### Add data execution gating note near `T2.16`, `T2.17`

```md
- [ ] 선행 조건: `T1.34` implementation architecture proposal 승인 후 착수.
```

## 5. MASTER_ROADMAP_V1.md Patch Draft

### Small wording extension only

```md
- **implementation architecture planning**: policy proposal을 data/review cross-check 후 implementation 구조와 projection 전략 수준까지 닫는다.
```

## 6. Recommended Apply Order

1. `RELATION_DATA_POLICY_V1.md`
2. `APP_DATA_REDEPLOY_SOP_V1.md`
3. `09_app/public/data/README.md`
4. `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
5. `MASTER_ROADMAP_V1.md`

## 7. Apply Timing Advice

- 지금은 바로 canonical 반영보다, 위 patch draft를 사용자 승인 전 검토용으로 유지하는 것이 맞다.
- 특히 `RELATION_GRAPH_CANONICAL_V1.json`의 authoritative 위치와 transition note는 data/review 재확인 후 반영하는 것이 안전하다.
