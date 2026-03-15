# PM Post-Restart Rollout Status V1

> Date: `2026-03-15 20:38:52 +0900`
> Owner: `Codex / Main PM`
> Status: `USER APPROVAL GATE READY`
> Purpose: restart model 승인 이후의 실제 rollout 상태를 정리하고, 다음 승인 게이트를 정의한다.

## 1. What Was Approved

사용자 승인은 개별 batch가 아니라 아래 운영 모델에 대해 주어졌다.

- `Calendar Label Batch-11`은 `Yellow / Runtime Reclassification`
- `publish-only`는 relation overlay only
- green batch는 current live id only / hierarchy reclassification 없음 / duplicate-free surface 위에서만 집행

## 2. What Was Executed After Approval

### Batch A

- `Relative Year Markers Batch-6`
- result: `REPORTED`
- runtime safety:
  - holdout drift `0`
  - reserve drift `0`
  - sentinel drift `0`
  - duplicate ids `0`

### Batch B

- `Temporal Reference Nouns Batch-8`
- result: `REPORTED`
- runtime safety:
  - holdout drift `0`
  - reserve drift `0`
  - sentinel drift `0`
  - duplicate ids `0`

### Batch C

- `Past Day Reference Batch-6`
- result: `REPORTED`
- runtime safety:
  - holdout drift `0`
  - reserve drift `0`
  - sentinel drift `0`
  - duplicate ids `0`

### Batch D

- `Time Point Bulk Batch-65`
- result: `REPORTED`
- runtime safety:
  - holdout drift `0`
  - reserve drift `0`
  - sentinel drift `0`
  - duplicate ids `0`

### Batch E

- `Time Root Bulk Remaining Batch-132`
- result: `REPORTED`
- runtime safety:
  - holdout drift `0`
  - reserve drift `0`
  - sentinel drift `0`
  - duplicate ids `0`

### Batch F

- `Full Live Runtime Mirror V1`
- result: `REPORTED`
- integrity:
  - duplicate ids `0`
  - split/search/chunk mismatch `0`
- notable effect:
  - runtime `related_vocab` totals normalized by duplicate-term dedupe (`-30`)

### Batch G

- `Full Live Node Coverage V1`
- result: `REPORTED`
- coverage:
  - internal canonical node coverage = current live `8094 / 8094`
- integrity:
  - duplicate ids `0`
  - split/search/chunk mismatch `0`

### Batch H

- `Zero Relation Generation V1`
- result: `REPORTED`
- outcome:
  - non-control zero-relation rows `0`
  - intentional holdout zero-relation rows `4`

### Batch I

- `Medical Learner Journey V1`
- result: `REPORTED`
- outcome:
  - `병원 -> 아프다` 류의 richer cross-system learner jump runtime 반영 확인
  - global integrity 유지

## 3. Current Runtime / Graph State

- internal graph status: `manual_zero_completion_v1_draft`
- internal graph nodes: `8094`
- internal graph edges: `30248`
- current live split/search/chunk totals: `8094 / 8094 / 8094`
- split/search/chunk mismatch: `0`
- remaining intentional holdout zero rows: `4`

## 4. PM Judgment

- restart model은 승인 이후 parity sync와 generation seed를 포함한 연속 execution에서 시스템 무결성을 유지했다.
- current live parity + non-control generation은 닫혔다.
- 따라서 현재 open question은 `medical learner journey`와 같은 richer enrichment를 다른 domain/root까지 확장할 것인가다.

## 5. Next Approval Gate

다음 승인 대상은 아래 중 하나다.

1. `다른 domain enrichment 승인`
   - medical learner journey 패턴을 여행/학교/쇼핑 등 다른 domain으로 확장
2. `holdout 해제 승인`
   - `오늘/어제(부사)`, `점심`, `저녁(의미2)`까지 relation generation 대상으로 포함
3. `현재 상태 유지`
   - current live parity + non-control generation + medical enrichment 상태를 기준선으로 두고 여기서 멈춤

이 시점부터는 단순 mirror/sync가 아니라 domain-level richer enrichment 확장 여부가 더 큰 승인 항목이다.
