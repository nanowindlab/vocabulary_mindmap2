# PM Relative Year Batch Execution Report V1

> Date: `2026-03-15 20:21:50 +0900`
> Owner: `Codex / Main PM`
> Status: `REPORTED`
> Scope: `Relative Year Markers Batch-6`

## 1. Execution Summary

- internal canonical draft applied
- `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only` executed
- `python3 scripts/core/rebuild_rev23_detail_chunks.py` executed
- final status: `GREEN EXECUTION REPORTED`

## 2. Internal Canonical Result

- graph status: `relative_year_markers_batch6_draft`
- node count: `47`
- edge count: `82`
- newly added nodes: `6`
- newly added edges: `18`

new nodes:

- `올해_일반명사-1`
- `작년_일반명사-1`
- `전년_일반명사-1`
- `재작년_일반명사-1`
- `내후년_일반명사-1`
- `새해_일반명사-1`

## 3. Runtime Output Result

candidate after publish/rebuild:

```text
올해_일반명사-1   related=5 cross=0
작년_일반명사-1   related=3 cross=0
전년_일반명사-1   related=2 cross=0
재작년_일반명사-1 related=2 cross=0
내후년_일반명사-1 related=3 cross=0
새해_일반명사-1   related=3 cross=0
```

actual `related_vocab`:

```text
올해   -> 금년, 작년, 전년, 내후년, 새해
작년   -> 전년, 올해, 재작년
전년   -> 작년, 올해
재작년 -> 작년, 전년
내후년 -> 내년, 올해, 새해
새해   -> 올해, 금년, 연말
```

## 4. Runtime Safety Checks

global integrity:

```text
split_total=8094
search_total=8094
manifest_sum=8094
split/search/chunk duplicate ids=0
split/search mismatch=0
search/chunk mismatch=0
```

batch id consistency:

```text
올해_일반명사-1   search=5/0 chunk=5/0
작년_일반명사-1   search=3/0 chunk=3/0
전년_일반명사-1   search=2/0 chunk=2/0
재작년_일반명사-1 search=2/0 chunk=2/0
내후년_일반명사-1 search=3/0 chunk=3/0
새해_일반명사-1   search=3/0 chunk=3/0
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

result:

- holdout drift `0`
- reserve drift `0`
- sentinel drift `0`

## 5. PM Verdict

- `Relative Year Markers Batch-6`는 restart-ready 이후 첫 green relation-overlay execution으로 runtime-safe하게 반영되었다.
- 이 결과는 `Calendar Label Batch-11`과 달리 hierarchy reclassification이나 duplicate live input 없이 닫혔다.
- formal `ACCEPT` 또는 phase 승격은 사용자 승인 전까지 기록하지 않는다.

## 6. Next PM Action

- user approval 전 상태는 `REPORTED`로 유지
- 다음 후보를 바로 여는 것보다, 현재 green restart model이 유효하다는 점을 기준으로 portfolio를 다시 확장한다
