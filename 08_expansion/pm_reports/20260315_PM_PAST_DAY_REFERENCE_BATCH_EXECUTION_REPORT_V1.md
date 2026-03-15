# PM Past Day Reference Batch Execution Report V1

> Date: `2026-03-15 20:51:42 +0900`
> Owner: `Codex / Main PM`
> Status: `REPORTED`
> Scope: `Past Day Reference Batch-6`

## 1. Execution Summary

- internal canonical draft applied
- `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only` executed
- `python3 scripts/core/rebuild_rev23_detail_chunks.py` executed
- final status: `THIRD POST-RESTART GREEN EXECUTION REPORTED`

## 2. Internal Canonical Result

- graph status: `past_day_reference_batch6_draft`
- node count: `61`
- edge count: `139`
- newly added nodes: `6`
- newly added edges: `29`

new nodes:

- `그날_일반명사-1`
- `그때_일반명사-1`
- `전날_일반명사-1`
- `어저께_일반명사-1`
- `어젯밤_일반명사-1`
- `아까_일반명사-1`

## 3. Runtime Output Result

candidate after publish/rebuild:

```text
그날_일반명사-1   related=5 cross=0
그때_일반명사-1   related=5 cross=0
전날_일반명사-1   related=5 cross=0
어저께_일반명사-1 related=5 cross=0
어젯밤_일반명사-1 related=5 cross=0
아까_일반명사-1   related=4 cross=0
```

actual `related_vocab`:

```text
그날   -> 그때, 당시, 전날, 어저께, 어젯밤
그때   -> 그날, 당시, 과거, 전날, 아까
전날   -> 어저께, 어젯밤, 그날, 그제, 그저께
어저께 -> 전날, 어젯밤, 그제, 그저께, 그날
어젯밤 -> 어저께, 전날, 그날, 최근, 아까
아까   -> 방금, 지금, 그때, 어젯밤
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

- `Past Day Reference Batch-6`도 restart model 안에서 runtime-safe하게 닫혔다.
- post-restart green overlay rollout은 현재 3개 batch 연속 통과 상태다.
- 다음 후보는 현재보다 넓은 family contract를 요구한다.

## 6. Next PM Action

- formal `ACCEPT` 또는 다음 scale-up은 사용자 승인 전까지 보류
- 다음 승인 게이트는 “같은 모델로 계속 확장”이 아니라 “더 넓은 time-reference family까지 green으로 볼 것인가”다
