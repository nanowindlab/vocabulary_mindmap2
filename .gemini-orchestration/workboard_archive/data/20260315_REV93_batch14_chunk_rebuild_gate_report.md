# Data Batch-14 Chunk Rebuild Gate Report

> Agent: `데이터 에이전트`
> Revision: `V1-REV-93`
> Logged: `2026-03-15 13:20:05 +0900`
> Scope: `Batch-14 chunk rebuild gate`
> Reporting Rule: `append-only only`

## Execution Summary

- executed:
  - `python3 scripts/core/rebuild_rev23_detail_chunks.py`
- result:
  - success

## Rebuild Summary Evidence

- `tree_total = 8092`
- `chunk_count = 21`
- `related_non_empty = 7625`
- `examples_non_empty = 8087`

## Batch-14 Search / Chunk Consistency Proof

- Batch-14 ids `14/14` search vs chunk relation count 일치

## Holdout / Reserve / Sentinel Chunk Proof

- holdout drift `0`
- reserve drift `0`
- sentinel drift `0`

## Conclusion

- `REV-93` chunk rebuild gate succeeded.
- Batch-14 is now consistent across search/tree/chunk.
- next meaningful step is the batch-agent operating model and/or the next expansion batch design.
