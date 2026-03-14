# 앱 데이터 재배포 표준 절차 (APP_DATA_REDEPLOY_SOP_V1)

> Date: `2026-03-12`
> Purpose: 단어 업데이트, 연관 데이터 갱신, 분류 수정 후 앱 runtime JSON을 일관되게 재배포하기 위한 데이터 에이전트 표준 절차

## 1. 적용 범위

이 문서는 아래 종류의 데이터 변경 후 반드시 적용한다.

- core/split/search 데이터 변경
- `related_vocab` / `refs.cross_links` 변경
- `chunk_id` 재부여 또는 chunk 구조 변경
- 예문/상세 청크 재생성 필요 변경

현재 runtime canonical 대상은 모두 `09_app/public/data/live/` 기준이다.

## 2. 권위 입력 / 출력

### 권위 입력

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`

transition note:

- `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`는 transition period 동안 builder compatibility input으로 유지 가능

### 최종 출력

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/CHUNK_MANIFEST_V1.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_*.json`
- `09_app/public/data/live/APP_READY_CHUNK_EXAMPLES_chunk_*.json`

## 2.1. rebuild trigger matrix

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

## 3. 표준 실행 순서

### Step 1. 관계 publish

`related_vocab` / `cross_links` 변경이 있으면 먼저 아래를 실행한다.

```bash
python3 scripts/mining/run_rev47_xwd_mining.py --publish-only
```

정책:

- 같은 `system/root/category`만 `related_vocab`
- 다른 분류로 넘어가는 연결만 `refs.cross_links`
- `APP_READY_SEARCH_INDEX.json`의 `chunk_id`를 유지할 것

### Step 2. detail chunk 재생성

publish 직후 아래를 실행한다.

```bash
python3 scripts/core/rebuild_rev23_detail_chunks.py
```

주의:

- 순서는 반드시 `publish-only -> chunk rebuild`
- 반대로 실행하면 split/search와 chunk가 서로 다른 값을 가질 수 있다
- chunk rebuild는 현재 live 트리 값을 우선 사용해야 한다

## 4. 필수 검증

### 구조 검증

- split 총합 = search total
- search `chunk_id` 존재 = 전체 term 수
- split `chunk_id` 존재 = 각 파일 전체 term 수

### 관계 검증

- `related_vocab` 타깃 누락 `0`
- `related_vocab` 타분류 오염 `0`
- `cross_links` 동일분류 오염 `0`
- `cross_links` 타깃 누락 `0`
- legacy `target_center_id` 잔존 `0`

### 청크 검증

- `CHUNK_MANIFEST_V1.json` 생성됨
- `APP_READY_CHUNK_RICH_chunk_*.json` 재생성됨
- `APP_READY_CHUNK_EXAMPLES_chunk_*.json` 재생성됨
- 상세 청크의 `related_vocab` / `refs.cross_links`가 live 트리와 일치함

### gate evidence checklist

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

## 5. 보고 문서 갱신

재배포 후 아래 문서를 함께 갱신한다.

- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- 필요 시 `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `08_expansion/rev47/REV47_DEV_HANDOFF_V1.md`
- 리뷰 혼선이 우려되면 `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`

보고에는 아래를 포함한다.

- live 파일별 `related_vocab` / `cross_links` count
- search total / chunk_id total
- 정합성 검증 결과
- 새 정책 변경이 있다면 한 줄 요약

## 6. 금지 사항

- `legacy/`나 `archive/`를 runtime canonical처럼 취급하지 말 것
- chunk만 재생성하고 split/search publish를 건너뛰지 말 것
- split/search만 재생성하고 chunk를 그대로 두지 말 것
- 검증 없이 대시보드에 완료 보고하지 말 것
