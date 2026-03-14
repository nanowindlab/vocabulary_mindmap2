# 연관 데이터 정책 문서 (RELATION_DATA_POLICY_V1)

> Date: `2026-03-12`
> Purpose: `related_vocab`와 `refs.cross_links`의 learner-facing 정의, 분리 기준, internal canonical / runtime projection 규칙을 고정하기 위한 권위 문서

## 1. 정책 배경

기존 연관 데이터는 아래 세 층이 혼재되어 있었다.

- 과거 `related_vocab`
- legacy `cross_links`
- XWD 기반 새 relation mining 결과

이로 인해 앱 UI에서

- 가까운 단어 묶음
- 다른 분류로 넘어가는 점프

가 같은 레이어로 섞여 보이는 문제가 있었다.

따라서 현재 정책은 아래처럼 고정한다.

## 2. 핵심 정의

### `related_vocab`

`related_vocab`는 현재 단어를 **같은 화면 안에서 비교, 대체, 대조, 국소 확장**하는 learner-neighborhood다.

기본 질문:

- 이 단어와 같이 보여 줄 때 학습자의 이해/선택/생산이 쉬워지는가?

대표 역할:

- `compare`
- `substitute`
- `contrast_lite`
- `scope_expand`

현재 cycle의 runtime 판정 기준:

- source와 target의 `system`
- `root`
- `category`

가 모두 같을 때 `related_vocab` 우선 후보로 본다.

### `refs.cross_links`

`refs.cross_links`는 현재 단어를 이해한 뒤 **다음 학습 단계로 이동시키는 next-step jump**다.

기본 질문:

- 이 단어를 알았을 때 어디로 이동하면 실제 사용이 쉬워지는가?

대표 역할:

- `scene_jump`
- `grammar_anchor`
- `usage_route`
- `sense_disambiguation`

현재 cycle의 runtime 판정 기준:

- source와 target의 `system/root/category`가 하나라도 다르면
- `refs.cross_links` 우선 후보로 본다

## 3. XWD와의 관계

XWD는 단순 유의어망이 아니라, 단어 간 맥락적 연결을 발굴하는 프레임워크다.

하지만 runtime 노출 단계에서는 XWD 결과를 그대로 한 바구니에 담지 않는다.

- 같은 분류권 안의 연결 → `related_vocab`
- 분류를 넘는 연결 → `refs.cross_links`

즉 XWD는 원천 relation graph이고,
앱 runtime에서는 이 graph를 정책적으로 두 레이어로 분리해 사용한다.

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

runtime-safe 제한:

- internal canonical은 richer schema를 허용
- runtime projection은 `word_to_word` 관계만 대상으로 유지
- `word_to_scene`, `word_to_grammar`, `word_to_idiom`은 schema reserve만 하고 live runtime에는 직접 노출하지 않는다
## 5. canonical runtime 규칙

현재 canonical runtime 파일은 모두 아래 경로 기준이다.

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_*.json`
- `09_app/public/data/live/APP_READY_CHUNK_EXAMPLES_chunk_*.json`

이 파일들 사이에서 `related_vocab`, `refs.cross_links`, `chunk_id`는 동일한 의미를 가져야 한다.

## 6. thin runtime projection rule

### `related_vocab`

- source: internal canonical edges where `display_intent = related_widget`
- destination: `APP_READY_*_TREE.json`, `APP_READY_SEARCH_INDEX.json`, detail chunk
- projection shape: `string[]`
- rule:
  - `target_term`만 추출
  - same target dedupe
  - max `5`

### `refs.cross_links`

- source: internal canonical edges where `display_intent = jump_link`
- destination: `APP_READY_*_TREE.json`, `APP_READY_SEARCH_INDEX.json`, detail chunk
- projection shape: current object shape 유지
- projected fields:
  - `target_id`
  - `target_term`
  - `target_system`
  - `target_root`
  - `target_category`
  - `hook_id`

optional note:

- `jump_purpose_label` 등 learner-purpose 라벨은 후속 dev gate에서 검토한다

## 7. tie-breaker / duplicate rule

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
- secondary role은 internal canonical에서만 보존 가능하다

## 8. time-anchor / grammar-anchor obligation

`Basics`로 이관된 시간, 계절, 요일, 시점 anchor는 learner scene로 이어지는 `Situations` jump를 최소 1개 이상 가져야 한다.

단, 단순 분류 차이만으로 jump를 만들지 않고 아래를 만족해야 한다.

- `jump_purpose`가 명시됨
- learner가 왜 이동해야 하는지 `reason`이 있음
- scene/grammar/usage 중 하나의 학습 과업을 실제로 열어 줌

## 9. 구현 반영 파일

현재 정책은 아래 코드에 반영되어 있다.

- `scripts/mining/run_rev47_xwd_mining.py`
  - XWD relation publish 단계
  - 같은 `system/root/category`만 `related_vocab`
  - 나머지는 `refs.cross_links`
- `scripts/core/rebuild_rev23_detail_chunks.py`
  - detail chunk 재생성 단계
  - live 트리 기준 relation 값을 우선 사용
  - legacy relation 재유입 방지

## 10. 2026-03-12 기준 검증 결과

- `related_vocab` 타깃 누락 `0`
- `related_vocab` 타분류 오염 `0`
- `cross_links` 동일분류 오염 `0`
- `cross_links` 타깃 누락 `0`
- `chunk_id` 존재 `8092 / 8092`
- live chunk 내 legacy `target_center_id` 잔존 `0`

현재 live count:

- `APP_READY_SITUATIONS_TREE.json`: `related 4289 / xlink 559`
- `APP_READY_EXPRESSIONS_TREE.json`: `related 1724 / xlink 100`
- `APP_READY_BASICS_TREE.json`: `related 1618 / xlink 146`
- `APP_READY_SEARCH_INDEX.json`: `related 7631 / xlink 805`

## 11. 개발/리뷰 해석 지침

개발 에이전트는 아래처럼 해석해야 한다.

- `related_vocab` = 같은 화면 안에서 비교/대체/국소 확장을 돕는 learner-neighborhood
- `refs.cross_links` = 다음 학습 단계로 이동시키는 jump 링크

리뷰 에이전트는 아래를 확인해야 한다.

- `related_vocab`에 다른 분류 단어가 섞이지 않았는가
- `cross_links`가 같은 분류 단어를 다시 담고 있지 않은가
- search / split / detail chunk가 같은 값을 공유하는가

## 12. 재배포 연동 문서

실제 재배포 절차는 아래 SOP를 따른다.

- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`

이 문서는 “정의와 정책”의 권위 문서이고,
SOP는 “실행 절차”의 권위 문서다.
