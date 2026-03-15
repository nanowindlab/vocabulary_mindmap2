# Data Batch-14 Runtime Projection Report

> Agent: `데이터 에이전트`
> Revision: `V1-REV-92`
> Logged: `2026-03-15 13:08:30 +0900`
> Scope: `Calendar Continuity Batch-14 runtime projection gate`
> Reporting Rule: `append-only only`

## Skills Used

- `data-validation`
- `multi-agent-orchestration`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV91_batch14_projection_gate_package_report.md`
- `.gemini-orchestration/workboard_archive/review/20260315_REV90_calendar_continuity_batch14_acceptance_report.md`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/APP_READY_*_TREE.json`

## Execution Summary

- executed:
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
- result:
  - success
- publish summary:
  - `mode = internal_canonical_overlay`
  - `graph_status = calendar_continuity_batch14_draft`
  - `graph_edge_count = 44`
  - `overlay_terms = 30`
  - `related_terms = 23`
  - `cross_system_terms = 8`
  - `avg_links_per_overlay_term = 1.47`
- latest report trace:
  - `linked_terms = 26`
  - `link_edges = 44`

## Implementation Note

- current publish script originally overlaid only the pilot include/holdout ids
- to make `REV-92` executable, overlay scope was aligned to `RELATION_GRAPH_CANONICAL_V1.json` `nodes` set
- effect:
  - Batch-14 nodes are now included in runtime projection
  - holdout nodes remain included only as `0/0` overlay targets

## Before Snapshot Evidence

- format:
  - `term_id | related | cross | chunk_id`

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
오늘_일반부사-1|0|0|chunk_019
어제_일반부사-1|0|0|chunk_019
점심_일반명사-1|0|0|chunk_009
저녁_일반명사-2|0|0|chunk_009
가을_일반명사-1|3|2|chunk_001
계절_일반명사-1|5|0|chunk_017
사계절_일반명사-1|5|0|chunk_018
모레_일반명사-1|5|0|chunk_018
정오_일반명사-1|4|0|chunk_020
요일_일반명사-1|4|0|chunk_019
```

## Actual Bucket Vs Expected Proof

- format:
  - `term_id | expected related | actual related | expected cross | actual cross | chunk_id`

```text
그제_일반명사-1|1|1|0|0|chunk_017
그저께_일반명사-1|1|1|0|0|chunk_017
다음날_일반명사-1|1|1|0|0|chunk_017
당일_일반명사-1|1|1|0|0|chunk_017
새벽_일반명사-1|1|1|0|0|chunk_018
오전_일반명사-1|1|1|0|0|chunk_019
낮_일반명사-1|1|1|0|0|chunk_017
오후_일반명사-1|1|1|0|0|chunk_019
화요일_일반명사-1|1|1|0|0|chunk_021
수요일_일반명사-1|1|1|0|0|chunk_019
목요일_일반명사-1|0|0|1|1|chunk_018
토요일_일반명사-1|0|0|1|1|chunk_020
주중_일반명사-1|1|1|0|0|chunk_020
평일_일반명사-1|2|2|0|0|chunk_020
```

- verdict:
  - Batch-14 actual bucket vs expected bucket `14/14` match

## Holdout Runtime Proof

- holdout ids:
  - `오늘_일반부사-1`
  - `어제_일반부사-1`
  - `점심_일반명사-1`
  - `저녁_일반명사-2`
- actual runtime:

```text
오늘_일반부사-1|0|0|chunk_019
어제_일반부사-1|0|0|chunk_019
점심_일반명사-1|0|0|chunk_009
저녁_일반명사-2|0|0|chunk_009
```

- result:
  - holdout 4 actual `0/0` maintained

## Reserve / Sentinel Drift Proof

- reserve candidates:

```text
가을_일반명사-1|3|2|chunk_001
계절_일반명사-1|5|0|chunk_017
사계절_일반명사-1|5|0|chunk_018
```

- sentinel controls:

```text
모레_일반명사-1|5|0|chunk_018
정오_일반명사-1|4|0|chunk_020
요일_일반명사-1|4|0|chunk_019
```

- result:
  - reserve drift `0`
  - sentinel drift `0`

## Tree Reflection Spot Check

- `APP_READY_BASICS_TREE.json`
  - `그제_일반명사-1` -> `1 / 0`
  - `새벽_일반명사-1` -> `1 / 0`
  - `화요일_일반명사-1` -> `1 / 0`
  - `목요일_일반명사-1` -> `0 / 1`
  - `평일_일반명사-1` -> `2 / 0`
  - `오늘_일반부사-1` -> `0 / 0`
- `APP_READY_SITUATIONS_TREE.json`
  - `가을_일반명사-1` -> `3 / 2`

## Target ID Runtime Safety Proof

- new `cross_links` target ids in live runtime:
  - `목요일_일반명사-1 -> 금요일_일반명사-1`
  - `토요일_일반명사-1 -> 금요일_일반명사-1`
- interpretation:
  - intended noun senses remained intact in runtime output

## Chunk Rebuild Pending Evidence

- `chunk rebuild` not executed in this revision
- expected intermediate mismatch remains:
  - `그제_일반명사-1` search `1/0` vs chunk `5/0`
  - `새벽_일반명사-1` search `1/0` vs chunk `4/1`
  - `목요일_일반명사-1` search `0/1` vs chunk `4/0`
  - `평일_일반명사-1` search `2/0` vs chunk `2/0`
- interpretation:
  - runtime projection gate succeeded
  - remaining inconsistency is isolated to chunk layer and should be closed by next gate

## Non-Execution Evidence

- `chunk rebuild` executed: no
- manual `live overwrite` executed: no
- only script-driven `publish-only` was executed

## Next Recommendation

- recommendation:
  - open `chunk rebuild gate`
- why:
  - Batch-14 actual bucket output is correct in live search/tree
  - holdout 4 actual `0/0` is preserved
  - reserve/sentinel drift is `0`
  - remaining open gap is chunk synchronization only

## Conclusion

- `REV-92` Batch-14 runtime projection succeeded.
- actual bucket vs expected bucket matched for all 14 new nodes.
- holdout/reserve/sentinel controls held.
- the next meaningful step is `chunk rebuild gate`, not another projection pass.
