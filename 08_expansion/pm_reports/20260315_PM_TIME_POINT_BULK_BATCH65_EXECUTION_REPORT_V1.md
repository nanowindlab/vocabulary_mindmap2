# PM Time Point Bulk Batch-65 Execution Report V1

> Date: `2026-03-15 21:00:16 +0900`
> Owner: `Codex / Main PM`
> Status: `REPORTED`
> Scope: `Time Point Bulk Batch-65`

## 1. Execution Summary

- bulk mirror import executed
- `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only` executed
- `python3 scripts/core/rebuild_rev23_detail_chunks.py` executed
- final status: `TIME POINT BULK GREEN EXECUTION REPORTED`

## 2. Internal Canonical Result

- graph status: `time_point_bulk_batch65_draft`
- created nodes: `65`
- created edges: `212`

## 3. Runtime Safety Checks

```text
split_total=8094
search_total=8094
manifest_sum=8094
split/search/chunk duplicate ids=0
split/search mismatch=0
search/chunk mismatch=0
```

control set:

```text
모레_일반명사-1=5/0
정오_일반명사-1=4/0
오늘_일반부사-1=0/0
어제_일반부사-1=0/0
점심_일반명사-1=0/0
저녁_일반명사-2=0/0
가을_일반명사-1=3/2
계절_일반명사-1=5/0
사계절_일반명사-1=5/0
```

## 4. PM Verdict

- current live `시점` 명사군의 large-scale mirror absorption도 runtime-safe하게 통과했다.
- 이는 manual micro-batch보다 bulk mirror 방식이 coverage acceleration에 더 적합함을 보여 준다.
