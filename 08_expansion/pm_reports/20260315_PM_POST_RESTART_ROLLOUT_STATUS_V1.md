# PM Post-Restart Rollout Status V1

> Date: `2026-03-15`
> Owner: `Codex / Main PM`
> Status: `USER APPROVAL GATE READY`
> Purpose: restart model 승인 이후의 실제 rollout 상태를 정리하고, 다음 승인 게이트를 정의한다.

## 1. What Was Approved

사용자 승인은 개별 batch가 아니라 아래 운영 모델에 대해 주어졌다.

- `Calendar Label Batch-11`은 `Yellow / Runtime Reclassification`
- `publish-only`는 relation overlay only
- green batch는 current live id only / hierarchy reclassification 없음 / duplicate-free surface 위에서만 집행

## 2. What Was Executed After Approval

### Batch A ~ H (Previous Executions)
- (See previous reports for details on Batch A through H, which included parity syncs and zero-relation generation).

### Batch I
- `Medical Learner Journey V1`
- result: `REPORTED`
- outcome:
  - `병원 -> 아프다` 류의 richer cross-system learner jump runtime 반영 확인
  - global integrity 유지

### Batch J (Current)
- `Food & Dining Learner Journey WP-1`
- result: `REPORTED`
- outcome:
  - `식당 -> 배고프다`, `카페 -> 목마르다`, `음식 -> 맛` 등의 상황 ➔ 마음/상태 교차 점프 28건 반영 완료.
  - zero-relation holdout은 여전히 의도된 4개 유지 (`오늘/어제(부사), 점심/저녁(의미2)`).
  - global integrity 유지 (`search/chunk mismatch 0`).

## 3. Current Runtime / Graph State

- internal graph status: `wp1_food_dining_learner_journey_v1`
- internal graph nodes: `8094`
- current live split/search/chunk totals: `8094 / 8094 / 8094`
- split/search/chunk mismatch: `0`
- remaining intentional holdout zero rows: `4`

## 4. PM Judgment

- WP-1 (식당/음식)의 학습자 여정 교차 점프(상황 -> 상태/행동)가 성공적으로 라이브 런타임 파일에 오버레이되었습니다.

## 5. Next Approval Gate

다음 승인 대상은 아래 중 하나입니다.

1. **다른 domain enrichment 승인**
   - WP-2 (쇼핑/물건 구매)
   - WP-3 (교통/이동)
   - WP-4 (학교/학습)
2. **holdout 해제 승인**
   - `오늘/어제(부사)`, `점심`, `저녁(의미2)`까지 relation generation 대상으로 포함
