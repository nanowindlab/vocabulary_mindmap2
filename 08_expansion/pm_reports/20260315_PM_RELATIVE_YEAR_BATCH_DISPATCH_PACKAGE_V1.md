# PM Relative Year Batch Dispatch Package V1

> Date: `2026-03-15`
> Owner: `Codex / Main PM`
> Status: `READY FOR DATA DISPATCH`
> Scope: `Relative Year Markers Batch-6`

## 1. Batch Identity

- batch name: `Relative Year Markers Batch-6`
- batch type: `Green / Relation Overlay Only`
- runtime owner: `current live hierarchy`

target ids:

- `올해_일반명사-1`
- `작년_일반명사-1`
- `전년_일반명사-1`
- `재작년_일반명사-1`
- `내후년_일반명사-1`
- `새해_일반명사-1`

## 2. Runtime Contract

- current live `system/root/category`를 그대로 유지한다.
- new runtime id admission 금지
- hierarchy reclassification 금지
- relation overlay only

current live hierarchy:

```text
구조와 기초 > 시간과 흐름 > 시점
```

## 3. Suggested Family Templates

### `relative_year_marker`

- `올해`
- `작년`
- `전년`
- `재작년`
- `내후년`

purpose:

- adjacent year navigation
- learner comparison of present/past/further-past/further-future markers

### `year_boundary_marker`

- `새해`

purpose:

- year-start boundary anchor
- bridge to existing graph nodes `금년`, `연도`, `연말`

## 4. Recommended Edge Design Direction

- same-category year markers 사이 연결은 `related_vocab` 우선
- existing graph nodes와의 category-consistent 연결도 `related_vocab` 우선
- cross-system jump는 이번 batch에서 필수 아님

recommended first overlay targets:

- `올해 -> 금년, 연도, 새해`
- `작년 -> 전년, 올해`
- `전년 -> 작년, 올해`
- `재작년 -> 작년, 전년`
- `내후년 -> 내년, 올해`
- `새해 -> 금년, 올해, 연말`

이 문서는 relation family template와 방향만 고정한다.
실제 source-target pair 확정은 data dispatch에서 current graph와 live counts를 보며 닫는다.

## 5. Before Snapshot Controls

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

batch-local targets before snapshot:

```text
올해_일반명사-1|3|0
작년_일반명사-1|5|0
전년_일반명사-1|3|0
재작년_일반명사-1|0|0
내후년_일반명사-1|5|0
새해_일반명사-1|4|0
```

## 6. Expected Gate Chain

1. internal canonical drafting
2. projection gate package
3. `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
4. `python3 scripts/core/rebuild_rev23_detail_chunks.py`
5. search/tree/chunk consistency proof

## 7. Acceptance Checklist

- all 6 ids remain on current live hierarchy
- holdout/reserve/sentinel drift `0`
- split/search/chunk duplicate ids `0`
- split/search/chunk count mismatch `0`
- batch ids search/tree/chunk relation count match `100%`

## 8. Decision

- 이 package는 restart-ready 이후 바로 dispatch 가능한 수준으로 본다.
- 다음 data dispatch는 이 package를 기준으로 열면 된다.
