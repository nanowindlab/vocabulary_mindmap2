# Data Pilot Runtime Projection Report

> Agent: `데이터 에이전트`
> Revision: `V1-REV-86`
> Logged: `2026-03-15 00:47:48 +0900`
> Scope: `core12 + holdout4 pilot runtime projection`
> Reporting Rule: `append-only only`

## Skills Used

- `data-validation`
- `multi-agent-orchestration`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV83_core12_edge_execution_report.md`
- `.gemini-orchestration/workboard_archive/review/20260315_REV84_core12_edge_package_acceptance_report.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV85_projection_gate_package_report.md`

## Execution Summary

- runtime projection executed:
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
- result:
  - success
  - publish mode = `internal_canonical_overlay`
- important implementation note:
  - current publish script still pointed at legacy `REV47_RELATED_LINKS_V1.json`
  - for this revision, publish path was updated to read `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json` and overlay only the pilot ids instead of wiping non-pilot runtime relations

## Publish-Only Evidence

- `08_expansion/rev47/REV47_PUBLISH_SUMMARY_V1.json`:
  - `mode = internal_canonical_overlay`
  - `graph_status = core12_edge_package_draft`
  - `graph_edge_count = 16`
  - `overlay_terms = 16`
  - `related_terms = 9`
  - `cross_system_terms = 6`
  - `avg_links_per_overlay_term = 1.0`
- latest report trace:
  - `linked_terms = 12`
  - `link_edges = 16`

## Before Snapshot Evidence

- baseline source:
  - `REV-85` projection gate package snapshot
- baseline counts before publish:

```text
오늘_일반명사-1|5|0
내일_일반명사-1|5|0
어제_일반명사-1|4|0
아침_일반명사-1|3|2
저녁_일반명사-1|3|2
밤_일반명사-1|3|2
월요일_일반명사-1|1|0
금요일_일반명사-1|4|1
주말_일반명사-1|5|0
봄_일반명사-1|2|1
여름_일반명사-1|3|0
겨울_일반명사-1|4|0
오늘_일반부사-1|3|0
어제_일반부사-1|3|0
점심_일반명사-1|3|0
저녁_일반명사-2|3|0
```

## After Projection Evidence

- source:
  - current live `APP_READY_SEARCH_INDEX.json`
- format:
  - `term_id | expected related | actual related | expected cross | actual cross`

```text
오늘_일반명사-1|2|2|0|0
내일_일반명사-1|1|1|0|0
어제_일반명사-1|1|1|0|0
아침_일반명사-1|1|1|0|0
저녁_일반명사-1|1|1|1|1
밤_일반명사-1|0|0|1|1
월요일_일반명사-1|0|0|1|1
금요일_일반명사-1|1|1|1|1
주말_일반명사-1|1|1|0|0
봄_일반명사-1|1|1|1|1
여름_일반명사-1|1|1|0|0
겨울_일반명사-1|0|0|1|1
오늘_일반부사-1|0|0|0|0
어제_일반부사-1|0|0|0|0
점심_일반명사-1|0|0|0|0
저녁_일반명사-2|0|0|0|0
```

## Anchor Bucket Verification

- verdict:
  - core 12 actual bucket counts match expected bucket counts in search runtime `12/12`
- tree alignment spot-check:
  - `APP_READY_BASICS_TREE.json`
    - `오늘_일반명사-1` -> `related 2 / cross 0`
    - `월요일_일반명사-1` -> `related 0 / cross 1`
    - `봄_일반명사-1` -> `related 1 / cross 1`
  - `APP_READY_SITUATIONS_TREE.json`
    - `겨울_일반명사-1` -> `related 0 / cross 1`
    - `점심_일반명사-1` -> `related 0 / cross 0`
    - `저녁_일반명사-2` -> `related 0 / cross 0`

## Holdout 4 Exclusion Proof In Live Runtime

- live search values:
  - `오늘_일반부사-1` -> `[] / []`
  - `어제_일반부사-1` -> `[] / []`
  - `점심_일반명사-1` -> `[] / []`
  - `저녁_일반명사-2` -> `[] / []`
- result:
  - holdout 4 exclusion preserved in actual live runtime

## Target ID Runtime Proof

- live `cross_links` target ids stayed on intended noun senses:
  - `저녁_일반명사-1 -> 밤_일반명사-1`
  - `밤_일반명사-1 -> 저녁_일반명사-1`
  - `월요일_일반명사-1 -> 금요일_일반명사-1`
  - `금요일_일반명사-1 -> 월요일_일반명사-1`
  - `봄_일반명사-1 -> 겨울_일반명사-1`
  - `겨울_일반명사-1 -> 봄_일반명사-1`

## Structural Integrity After Publish-Only

- `APP_READY_SEARCH_INDEX.json` total:
  - `8092`
- search `chunk_id` present:
  - `8092`
- split files:
  - `APP_READY_SITUATIONS_TREE.json` = `4541`, chunk_id present `4541`
  - `APP_READY_EXPRESSIONS_TREE.json` = `1829`, chunk_id present `1829`
  - `APP_READY_BASICS_TREE.json` = `1722`, chunk_id present `1722`

## Chunk Rebuild Pending Evidence

- `publish-only` executed, but `chunk rebuild` not executed
- therefore search/tree vs chunk mismatch already visible:
  - `오늘_일반명사-1` search `2/0` vs chunk `5/0`
  - `저녁_일반명사-1` search `1/1` vs chunk `3/2`
  - `월요일_일반명사-1` search `0/1` vs chunk `1/0`
  - `오늘_일반부사-1` search `0/0` vs chunk `3/0`
  - `점심_일반명사-1` search `0/0` vs chunk `3/0`
- interpretation:
  - pilot runtime projection은 성공했지만 detail chunk는 아직 pre-REV86 상태다
  - 이 불일치는 현재 revision scope상 허용된 중간 상태이며, 다음 gate에서 `chunk rebuild`로 닫아야 한다

## Non-Execution Evidence

- `chunk rebuild` executed: no
- manual `live overwrite` executed: no
- only script-driven `publish-only` was executed

## Next Recommendation

- recommendation:
  - next revision should open `chunk rebuild gate`
- why:
  - search/tree runtime is now correct for the pilot package
  - holdout exclusion is proven in live runtime
  - remaining inconsistency is isolated to detail chunk artifacts
- minimum next guard set:
  - run `python3 scripts/core/rebuild_rev23_detail_chunks.py`
  - immediately compare pilot ids across search/tree/chunk
  - confirm holdout 4 remains `0/0` in chunk rich files too

## Conclusion

- `REV-86` pilot runtime projection succeeded.
- core12 expected buckets matched actual runtime output.
- holdout 4 exclusion held in live runtime.
- the remaining open issue is expected and isolated: chunk rebuild is still pending.
