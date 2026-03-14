# 연관 데이터 정책 문서 (RELATION_DATA_POLICY_V1)

> Date: `2026-03-12`
> Purpose: `related_vocab`와 `refs.cross_links`의 정의, 분리 기준, runtime 반영 규칙을 고정하기 위한 권위 문서

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

`related_vocab`는 **같은 분류권 안의 가까운 단어**만 담는다.

현재 판정 기준:

- source와 target의 `system`
- `root`
- `category`

가 모두 같을 때만 `related_vocab`로 유지한다.

즉 `related_vocab`는 다음 용도다.

- 동류어
- 가까운 하위/상위 개념
- 같은 category 내부의 인접 어휘
- 사용자에게 “이 단어 주변 어휘”를 보여 주는 탐색용 목록

### `refs.cross_links`

`refs.cross_links`는 **다른 분류로 넘어가는 연결**만 담는다.

현재 판정 기준:

- source와 target의 `system/root/category`가 하나라도 다르면
- `refs.cross_links`로 보낸다

즉 `cross_links`는 다음 용도다.

- 다른 category로 이동
- 다른 root로 이동
- 다른 system으로 이동
- 사용자에게 “다른 관점으로 점프”를 제공하는 횡단 링크

## 3. XWD와의 관계

XWD는 단순 유의어망이 아니라, 단어 간 맥락적 연결을 발굴하는 프레임워크다.

하지만 runtime 노출 단계에서는 XWD 결과를 그대로 한 바구니에 담지 않는다.

- 같은 분류권 안의 연결 → `related_vocab`
- 분류를 넘는 연결 → `refs.cross_links`

즉 XWD는 원천 relation graph이고,
앱 runtime에서는 이 graph를 정책적으로 두 레이어로 분리해 사용한다.

## 4. canonical runtime 규칙

현재 canonical runtime 파일은 모두 아래 경로 기준이다.

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_*.json`
- `09_app/public/data/live/APP_READY_CHUNK_EXAMPLES_chunk_*.json`

이 파일들 사이에서 `related_vocab`, `refs.cross_links`, `chunk_id`는 동일한 의미를 가져야 한다.

## 5. 구현 반영 파일

현재 정책은 아래 코드에 반영되어 있다.

- `scripts/mining/run_rev47_xwd_mining.py`
  - XWD relation publish 단계
  - 같은 `system/root/category`만 `related_vocab`
  - 나머지는 `refs.cross_links`
- `scripts/core/rebuild_rev23_detail_chunks.py`
  - detail chunk 재생성 단계
  - live 트리 기준 relation 값을 우선 사용
  - legacy relation 재유입 방지

## 6. 2026-03-12 기준 검증 결과

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

## 7. 개발/리뷰 해석 지침

개발 에이전트는 아래처럼 해석해야 한다.

- `related_vocab` = 가까운 단어 칩
- `refs.cross_links` = 다른 분류로 넘어가는 점프 링크

리뷰 에이전트는 아래를 확인해야 한다.

- `related_vocab`에 다른 분류 단어가 섞이지 않았는가
- `cross_links`가 같은 분류 단어를 다시 담고 있지 않은가
- search / split / detail chunk가 같은 값을 공유하는가

## 8. 재배포 연동 문서

실제 재배포 절차는 아래 SOP를 따른다.

- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`

이 문서는 “정의와 정책”의 권위 문서이고,
SOP는 “실행 절차”의 권위 문서다.
