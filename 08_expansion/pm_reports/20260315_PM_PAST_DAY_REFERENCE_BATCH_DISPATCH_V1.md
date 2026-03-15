# PM Past Day Reference Batch Dispatch V1

> Date: `2026-03-15 20:49:58 +0900`
> Owner: `Codex / Main PM`
> Status: `READY FOR EXECUTION`
> Purpose: current rollout model 안에서 다음 safe green overlay batch를 집행한다.

## 1. Batch Identity

- batch name: `Past Day Reference Batch-6`
- batch type: `Green / Relation Overlay Only`
- runtime owner: `current live hierarchy`

target ids:

- `그날_일반명사-1`
- `그때_일반명사-1`
- `전날_일반명사-1`
- `어저께_일반명사-1`
- `어젯밤_일반명사-1`
- `아까_일반명사-1`

## 2. Gate Proof

- missing in live: `0`
- already in graph: `0`
- holdout overlap: `0`
- reserve overlap: `0`
- sentinel overlap: `0`

all targets share:

```text
구조와 기초 > 시간과 흐름 > 시점
```

## 3. Dispatch Intent

- day-reference / near-past reference nouns를 same-category overlay로 묶는다.
- hierarchy reclassification은 하지 않는다.
- current live id만 사용한다.

## 4. Suggested Overlay Direction

- `그날 -> 그때, 당시, 전날, 어저께, 어젯밤`
- `그때 -> 그날, 당시, 과거, 전날, 아까`
- `전날 -> 어저께, 어젯밤, 그날, 그제, 그저께`
- `어저께 -> 전날, 어젯밤, 그제, 그저께, 그날`
- `어젯밤 -> 어저께, 전날, 그날, 최근, 아까`
- `아까 -> 방금, 지금, 그때, 어젯밤`

## 5. PM Note

이 batch까지는 현재 승인된 rollout model 안의 자연스러운 연장이다.
이 다음부터는 `날/기한/공휴일/주말/연휴`처럼 더 넓은 family contract로 넘어가게 되므로,
이번 batch 이후가 다음 승인 게이트 후보가 될 가능성이 높다.
