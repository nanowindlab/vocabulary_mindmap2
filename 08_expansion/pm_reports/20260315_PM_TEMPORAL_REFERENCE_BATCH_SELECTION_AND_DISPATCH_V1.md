# PM Temporal Reference Batch Selection And Dispatch V1

> Date: `2026-03-15 20:36:07 +0900`
> Owner: `Codex / Main PM`
> Status: `READY FOR EXECUTION`
> Purpose: second post-restart green relation-overlay batch를 선정하고 즉시 dispatch 가능한 package로 고정한다.

## 1. Batch Identity

- batch name: `Temporal Reference Nouns Batch-8`
- batch type: `Green / Relation Overlay Only`
- runtime owner: `current live hierarchy`

target ids:

- `현재_일반명사-1`
- `과거_일반명사-1`
- `미래_일반명사-1`
- `당시_일반명사-1`
- `최근_일반명사-1`
- `예전_일반명사-1`
- `지금_일반명사-1`
- `이후_일반명사-1`

## 2. Restart Gate Proof

- missing in live: `0`
- already in internal graph nodes: `0`
- holdout overlap: `0`
- reserve overlap: `0`
- sentinel overlap: `0`

all targets share current live hierarchy:

```text
구조와 기초 > 시간과 흐름 > 시점
```

## 3. Why This Batch Is Green

- 모든 id가 current live에 이미 존재한다.
- 모두 same root/category라서 runtime reclassification이 필요 없다.
- `Relative Year Markers Batch-6`와 자연스럽게 연결되지만 control set을 건드리지 않는다.
- relation overlay only로 집행 가능하다.

## 4. Suggested Family Templates

### `present_reference`

- `현재`
- `지금`
- `최근`

### `past_reference`

- `과거`
- `당시`
- `예전`

### `future_reference`

- `미래`
- `이후`

## 5. Recommended Overlay Direction

- `현재 -> 지금, 올해, 최근, 미래, 이후`
- `과거 -> 예전, 당시, 작년, 전년, 최근`
- `미래 -> 이후, 내후년, 올해`
- `당시 -> 과거, 예전, 그날`
- `최근 -> 현재, 작년, 전년`
- `예전 -> 과거, 당시, 작년`
- `지금 -> 현재, 올해, 최근`
- `이후 -> 미래, 내후년, 현재`

## 6. Before Snapshot Controls

holdout:

```text
오늘_일반부사-1|0|0
어제_일반부사-1|0|0
점심_일반명사-1|0|0
저녁_일반명사-2|0|0
```

reserve:

```text
가을_일반명사-1|3|2
계절_일반명사-1|5|0
사계절_일반명사-1|5|0
```

sentinel:

```text
모레_일반명사-1|5|0
정오_일반명사-1|4|0
```

## 7. Decision

- `Temporal Reference Nouns Batch-8`는 second post-restart green candidate로 바로 실행 가능하다.
- 이 batch까지 runtime-safe하게 통과하면, 이후 단계는 개별 batch dispatch보다 restart model 자체에 대한 사용자 승인 게이트로 보는 것이 맞다.
