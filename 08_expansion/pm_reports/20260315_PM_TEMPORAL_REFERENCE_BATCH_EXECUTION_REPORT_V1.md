# PM Temporal Reference Batch Execution Report V1

> Date: `2026-03-15 20:38:52 +0900`
> Owner: `Codex / Main PM`
> Status: `REPORTED`
> Scope: `Temporal Reference Nouns Batch-8`

## 1. Execution Summary

- internal canonical draft applied
- `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only` executed
- `python3 scripts/core/rebuild_rev23_detail_chunks.py` executed
- final status: `SECOND POST-RESTART GREEN EXECUTION REPORTED`

## 2. Internal Canonical Result

- graph status: `temporal_reference_batch8_draft`
- node count: `55`
- edge count: `110`
- newly added nodes: `8`
- newly added edges: `28`

new nodes:

- `현재_일반명사-1`
- `과거_일반명사-1`
- `미래_일반명사-1`
- `당시_일반명사-1`
- `최근_일반명사-1`
- `예전_일반명사-1`
- `지금_일반명사-1`
- `이후_일반명사-1`

## 3. Runtime Output Result

candidate after publish/rebuild:

```text
현재_일반명사-1 related=5 cross=0
과거_일반명사-1 related=5 cross=0
미래_일반명사-1 related=3 cross=0
당시_일반명사-1 related=3 cross=0
최근_일반명사-1 related=3 cross=0
예전_일반명사-1 related=3 cross=0
지금_일반명사-1 related=3 cross=0
이후_일반명사-1 related=3 cross=0
```

actual `related_vocab`:

```text
현재 -> 지금, 올해, 최근, 미래, 이후
과거 -> 예전, 당시, 작년, 전년, 최근
미래 -> 이후, 내후년, 올해
당시 -> 과거, 예전, 그날
최근 -> 현재, 작년, 전년
예전 -> 과거, 당시, 작년
지금 -> 현재, 올해, 최근
이후 -> 미래, 내후년, 현재
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

- `Temporal Reference Nouns Batch-8`도 restart gate 안에서 runtime-safe하게 닫혔다.
- 이로써 post-restart green relation-overlay model은 최소 2개 batch 연속으로 통과했다.
- 이제 다음 meaningful gate는 개별 batch 추가 실행보다, restart model 자체를 사용자 승인 대상으로 올리는 것이다.

## 6. Next PM Action

- formal `ACCEPT` 또는 scale-up은 사용자 승인 전까지 보류
- 승인 전 상태는 `REPORTED`로 유지
