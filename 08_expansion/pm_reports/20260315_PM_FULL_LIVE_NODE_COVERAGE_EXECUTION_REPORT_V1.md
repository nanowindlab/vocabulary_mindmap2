# PM Full Live Node Coverage Execution Report V1

> Date: `2026-03-15 21:14:01 +0900`
> Owner: `Codex / Main PM`
> Status: `REPORTED / NEXT APPROVAL GATE READY`
> Scope: `Full Live Node Coverage V1`

## 1. Execution Summary

- internal canonical node coverage expanded to all current live rows
- `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only` executed
- `python3 scripts/core/rebuild_rev23_detail_chunks.py` executed

result:

- graph status: `full_live_node_coverage_v1_draft`
- graph nodes: `8094`
- graph edges: `28162`
- missing graph nodes vs current live: `0`

## 2. Global Integrity

```text
split_total=8094
search_total=8094
manifest_sum=8094
split/search/chunk duplicate ids=0
split/search mismatch=0
search/chunk mismatch=0
related_total=27101
cross_total=1061
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

## 3. Coverage Result

- current live rows with relation payload: `7672`
- current live rows with zero relation payload: `422`
- internal canonical now covers all `8094` current live rows, even when relation payload is empty

## 4. PM Verdict

- 이제 `current app runtime parity` 기준의 internal canonical coverage는 닫혔다.
- 다음 단계부터는 단순 mirror가 아니라, relation이 비어 있는 `422`개 단어에 새 relation을 생성하거나, live에 없는 더 rich relation을 추가하는 단계다.
- 따라서 여기서가 다음 실제 승인 게이트다.
