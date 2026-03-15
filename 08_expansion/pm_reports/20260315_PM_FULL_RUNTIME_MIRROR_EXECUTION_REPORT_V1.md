# PM Full Runtime Mirror Execution Report V1

> Date: `2026-03-15 21:07:45 +0900`
> Owner: `Codex / Main PM`
> Status: `REPORTED / NEXT APPROVAL GATE READY`
> Scope: `Full Live Runtime Mirror V1`

## 1. Execution Summary

- current live rows with runtime relations를 internal canonical로 bulk mirror
- `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only` executed
- `python3 scripts/core/rebuild_rev23_detail_chunks.py` executed

result:

- internal graph status: `full_live_runtime_mirror_v1_draft`
- graph nodes: `7677`
- graph edges: `28162`

## 2. Global Integrity

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

## 3. Important Change

global runtime relation totals after full mirror:

```text
related_total=27101
cross_total=1061
```

관찰점:

- cross total은 유지됐다.
- related total은 기존 local runtime 기준보다 `30` 감소했다.

해석:

- full mirror 과정에서 current live에 남아 있던 duplicate `related_vocab` term들이 `publish-only`의 runtime dedupe rule로 정규화되었다.
- 예:
  - `현재_일반명사-1`: `오늘` 중복 제거
  - `기한_일반명사-1`: `늦다` 중복 제거
  - `방금_일반명사-1`: `방금` self/duplicate parity 정리

즉 global integrity는 유지되지만, runtime relation payload는 이제 “중복 정규화된 상태”가 되었다.

## 4. PM Judgment

- 이 단계는 시스템을 깨뜨린 것은 아니다.
- 그러나 이제부터는 단순 safe overlay 확장이 아니라, **runtime relation normalization을 정식 기준으로 받아들일지**의 문제가 된다.
- 따라서 여기서가 다음 승인 게이트다.
