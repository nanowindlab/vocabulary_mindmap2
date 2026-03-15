# PM Next Green Batch Selection V1

> Date: `2026-03-15`
> Owner: `Codex / Main PM`
> Status: `PROPOSAL / NOT YET DISPATCHED`
> Purpose: restart-ready gate를 통과하는 다음 green relation-overlay batch를 선정한다.

## 1. Restart Gate Used

다음 green batch는 아래 조건을 모두 만족해야 한다.

1. current live id에 이미 존재
2. current live `system/root/category`를 바꾸지 않음
3. relation overlay only로 집행 가능
4. holdout / reserve / sentinel control set과 충돌하지 않음
5. current internal relation graph node set에 아직 포함되지 않음

## 2. Recommended Batch

### Batch Name

- `Relative Year Markers Batch-6`

### Candidate IDs

- `올해_일반명사-1`
- `작년_일반명사-1`
- `전년_일반명사-1`
- `재작년_일반명사-1`
- `내후년_일반명사-1`
- `새해_일반명사-1`

### Live Runtime Evidence

모든 항목이 현재 live runtime에 이미 존재하며, 공통적으로 아래 hierarchy를 가진다.

- `system = 구조와 기초`
- `root = 시간과 흐름`
- `category = 시점`

current live counts:

```text
올해_일반명사-1   related=3  cross=0
작년_일반명사-1   related=5  cross=0
전년_일반명사-1   related=3  cross=0
재작년_일반명사-1 related=0  cross=0
내후년_일반명사-1 related=5  cross=0
새해_일반명사-1   related=4  cross=0
```

### Control Safety Evidence

- missing in live: `0`
- already in internal graph nodes: `0`
- holdout overlap: `0`
- reserve overlap: `0`
- sentinel overlap: `0`

## 3. Why This Batch Fits Green

- 모두 current live hierarchy가 이미 안정적으로 존재한다.
- `Calendar Label Batch-11`처럼 runtime reclassification이나 new id admission이 필요하지 않다.
- 같은 `시간과 흐름 > 시점` 안에서 묶여 learner-facing relation overlay를 만들 수 있다.
- 기존 graph의 `금년`, `내년`, `연도`, `연말`과 자연스럽게 연결되지만, control set을 재오염시키지 않는다.
- `재작년_일반명사-1`처럼 relation coverage가 약한 항목이 있어 overlay value가 분명하다.

## 4. Why Other Nearby Candidates Are Not First

### `Calendar Label Batch-11`

- 현재 분류가 `Yellow / Runtime Reclassification`이다.
- restart-ready 이후의 first green candidate로 재사용하면 restart gate 의미가 약해진다.

### `주말 / 연휴 / 공휴일` cluster

- current live category가 `시간 단위`, `기간과 경과`, `시점`으로 갈린다.
- relation design 자체는 가능하지만, first restart green batch로 쓰기엔 family contract가 덜 단순하다.

### `Month Unit Batch`

- 기존 planning에서도 inventory normalization gap 때문에 yellow로 유지되었다.
- restart first batch로 쓰기엔 여전히 설계 비용이 남아 있다.

## 5. Reference Evidence From Prior Batch Files

batch-run classification evidence는 runtime owner가 아니라 inventory support evidence로만 사용한다.

- `BATCH_014M_validated.json`
  - `올해_일반명사-1 -> 시간과 흐름 / 현재 연도`
  - `작년_일반명사-1 -> 시간과 흐름 / 과거 연도`
- `BATCH_089M_validated.json`
  - `새해_일반명사-1 -> 시간과 흐름 / 연간 시점`
- `BATCH_107M_validated.json`
  - `전년_일반명사-1 -> 시간과 흐름 / 과거 시점`

현재 green qualification은 위 batch category를 그대로 runtime에 반영하는 것이 아니라,
current live hierarchy를 유지한 채 relation overlay만 집행할 수 있는지로 판단한다.

## 6. Recommended Next Gate Chain

1. planning confirmation
2. internal canonical node/edge drafting
3. projection gate package
4. publish-only
5. chunk rebuild
6. search/tree/chunk consistency check

## 7. Conclusion

- next green recommendation은 `Relative Year Markers Batch-6`이다.
- 이 batch는 현재 restart gate를 통과하는 첫 relation-overlay candidate로 보기 가장 적절하다.
- 아직 dispatch 전이며, dispatch 시에는 current live hierarchy를 runtime owner로 고정해야 한다.
