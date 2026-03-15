# Data Batch-14 Projection Gate Package Report

> Agent: `데이터 에이전트`
> Revision: `V1-REV-91`
> Logged: `2026-03-15 13:08:30 +0900`
> Scope: `Calendar Continuity Batch-14 projection gate package`
> Reporting Rule: `append-only only`

## Skills Used

- `data-validation`
- `multi-agent-orchestration`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV89_calendar_continuity_batch14_report.md`
- `.gemini-orchestration/workboard_archive/review/20260315_REV90_calendar_continuity_batch14_acceptance_report.md`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/APP_READY_*_TREE.json`

## Package Summary

- action taken:
  - `RELATION_GRAPH_CANONICAL_V1.json`의 `dry_run_reserve` 보강
  - Batch-14 before snapshot 작성
  - holdout / reserve / sentinel baseline 작성
- no-execution guard:
  - `publish` not executed
  - `chunk rebuild` not executed
  - `live overwrite` not executed

## Preview Coverage Proof

- target range:
  - `pilot_edge_017 ~ pilot_edge_044`
- result:
  - preview coverage `28/28`
  - missing preview edge ids: `0`
- current total preview entries:
  - `44`

## Batch-14 Expected Runtime Bucket Summary

- `pilot_edge_017~044` expected bucket split:
  - `related_vocab`: `24`
  - `cross_links`: `4`
- node-level expected counts:

```text
그제_일반명사-1|1|0
그저께_일반명사-1|1|0
다음날_일반명사-1|1|0
당일_일반명사-1|1|0
새벽_일반명사-1|1|0
오전_일반명사-1|1|0
낮_일반명사-1|1|0
오후_일반명사-1|1|0
화요일_일반명사-1|1|0
수요일_일반명사-1|1|0
목요일_일반명사-1|0|1
토요일_일반명사-1|0|1
주중_일반명사-1|1|0
평일_일반명사-1|2|0
```

## Before Snapshot Evidence For Batch-14 Nodes

- format:
  - `term_id | current related | current cross | chunk_id`

```text
그제_일반명사-1|5|0|chunk_017
그저께_일반명사-1|5|0|chunk_017
다음날_일반명사-1|5|0|chunk_017
당일_일반명사-1|5|0|chunk_017
새벽_일반명사-1|4|1|chunk_018
오전_일반명사-1|5|0|chunk_019
낮_일반명사-1|4|1|chunk_017
오후_일반명사-1|4|0|chunk_019
화요일_일반명사-1|0|0|chunk_021
수요일_일반명사-1|5|0|chunk_019
목요일_일반명사-1|4|0|chunk_018
토요일_일반명사-1|1|1|chunk_020
주중_일반명사-1|5|0|chunk_020
평일_일반명사-1|2|0|chunk_020
```

## Holdout Baseline Evidence

- format:
  - `term_id | current related | current cross | chunk_id`

```text
오늘_일반부사-1|0|0|chunk_019
어제_일반부사-1|0|0|chunk_019
점심_일반명사-1|0|0|chunk_009
저녁_일반명사-2|0|0|chunk_009
```

- interpretation:
  - holdout 4는 pilot 이후 현재 live baseline에서도 이미 `0/0`
  - projection gate 이후에도 동일 baseline 유지가 검증 포인트다

## Reserve Baseline Evidence

- reserve candidates:
  - `가을_일반명사-1`
  - `계절_일반명사-1`
  - `사계절_일반명사-1`
- current baseline:

```text
가을_일반명사-1|3|2|chunk_001
계절_일반명사-1|5|0|chunk_017
사계절_일반명사-1|5|0|chunk_018
```

## Sentinel Baseline Evidence

- non-target sentinel controls:
  - `모레_일반명사-1`
  - `정오_일반명사-1`
  - `요일_일반명사-1`
- current baseline:

```text
모레_일반명사-1|5|0|chunk_018
정오_일반명사-1|4|0|chunk_020
요일_일반명사-1|4|0|chunk_019
```

## `dry_run_reserve` Update Summary

- added pre-publish checks:
  - Batch-14 28 edge preview coverage check
  - holdout/reserve/sentinel baseline capture check
- added gate evidence:
  - `pilot_edge_017~044` projection preview coverage 기록
  - holdout / reserve / sentinel baseline capture 기록

## Runtime Projection Gate Recommendation

- recommendation:
  - `runtime projection gate` can open
- reason:
  - internal acceptance is already `ACCEPT`
  - 신규 28 edge preview coverage가 `100%`로 채워짐
  - before snapshot과 control baseline이 모두 고정됨
- minimum guard set for next gate:
  - publish 직전 snapshot 재확인
  - Batch-14 actual bucket vs expected bucket 즉시 대조
  - holdout 4 actual `0/0` 검증
  - reserve/sentinel drift `0` 검증

## Conclusion

- `REV-91` projection gate package completed.
- Batch-14 is now projection-ready up to publish boundary.
- 다음 단계는 publish/rebuild가 아니라, 먼저 `runtime projection gate`를 여는 revision이 적절하다.
