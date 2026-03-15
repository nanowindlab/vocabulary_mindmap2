# Next Green Batch Selection Memo

> Agent: `기획 에이전트`
> Revision: `V1-REV-95`
> Logged: `2026-03-15`
> Status: `PROPOSAL / NOT YET APPLIED`
> Purpose: `REV-94` 운영 모델을 실제 next batch 선정에 적용
> Guard: 새 relation semantics / validated contract 재개방 금지

## 문제 재정의

`REV-94`가 운영 규칙을 닫았으므로, 이번 revision의 목적은 “후보를 많이 나열하는 것”이 아니라 **실제로 바로 data dispatch가 가능한 다음 green batch를 하나 고르는 것**이다.

판정 기준은 이미 고정되어 있다.

- `Type A/B/C`
- `Green/Yellow/Red`
- one-batch-one-rev eligibility

## Web Research Basis

- [한국어기초사전 주제 및 상황 범주](https://krdict.korean.go.kr/kor/dicSearchDetail/searchDetailWords)
- [한국어기초사전 OpenAPI subject_cat](https://krdict.korean.go.kr/openApi/openApiInfo)

실무 해석:

- 공식 learner resource는 `시간 표현하기`, `날짜 표현하기`, `요일 표현하기`, `약속하기`를 별도 topic cluster로 다룬다.
- 따라서 Batch-14 이후의 다음 green 후보는 `date/calendar labels`처럼 **같은 시간 cluster 안에서 learner navigation value가 높고 ambiguity가 낮은 명사군**이 적합하다.

## next batch candidate table

| candidate | scope | Type | Gate | 판정 이유 |
| :--- | :--- | :--- | :--- | :--- |
| `Calendar Label Batch-11` | `날짜`, `달력`, `요일`, `월`, `연도`, `금년`, `내년`, `이달`, `내달`, `연말`, `월말` | `Type A` | `Green` | 전부 current live 실재, noun-sense 명확, holdout/reserve 미접촉, 동일 `시간과 흐름` cluster 안에서 설명 가능 |
| `Month Unit Batch` | `삼월`, `유월`, `칠월`, `팔월`, `구월`, `시월`, `십이월` 등 | `Type B` | `Yellow` | inventory gap 다수(`일월`, `이월`, `사월`, `오월`, `십일월` missing), month system 설계가 덜 닫힘 |
| `Date Point Batch` | `그날`, `그때`, `날`, `기한`, `공휴일` 등 | `Type B` | `Yellow` | `날` duplicate surface 존재, `시점`/`시간 단위`/`시작과 끝` 섞임, family reason template가 아직 분산됨 |

## recommended next green batch

### Recommendation

- `Calendar Label Batch-11`

### Included Nodes

- `날짜_일반명사-1`
- `달력_일반명사-1`
- `요일_일반명사-1`
- `월_일반명사-1`
- `연도_일반명사-1`
- `금년_일반명사-1`
- `내년_일반명사-1`
- `이달_일반명사-1`
- `내달_일반명사-1`
- `연말_일반명사-1`
- `월말_일반명사-1`

### Why This Is Green

1. 모두 current live inventory에 존재한다.
2. 모두 noun-sense가 단일하거나 현재 contract 안에서 ambiguity가 없다.
3. holdout 4를 건드리지 않는다.
4. reserve family(`가을`, `계절`, `사계절`, `일요일`)를 건드리지 않는다.
5. 공식 learner topic cluster의 `날짜/요일/시간 표현`과 직접 정렬된다.
6. current graph에 아직 node seeded 되어 있지 않아, batch value가 분명하다.

## reserve / yellow candidate list

### Keep As Yellow

- `Month Unit Batch`
  - 이유: missing inventory가 많아 `Type B / Yellow`
- `Date Point Batch`
  - 이유: `날` duplicate surface, family template 분산

### Keep As Reserve

- current holdout 4
  - `오늘_일반부사-1`
  - `어제_일반부사-1`
  - `점심_일반명사-1`
  - `저녁_일반명사-2`
- current reserve
  - `가을_일반명사-1`
  - `계절_일반명사-1`
  - `사계절_일반명사-1`
  - `일요일`

## next data dispatch outline

### Dispatch Shape

- revision type:
  - `Type A + Green`
- recommended package name:
  - `Calendar Label Batch-11`

### Build Scope

- write target:
  - `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- required actions:
  - node seed
  - family-consistent edge package 작성
  - `dry_run_reserve` preview 준비
- forbidden:
  - holdout 해제
  - reserve family touch
  - semantics/contract 변경

### Family Reason Templates

- `calendar_reference`
  - 예: 날짜, 달력, 요일, 월, 연도
  - rationale: `calendar system reference / labeling`
- `relative_period_marker`
  - 예: 금년, 내년, 이달, 내달
  - rationale: `named calendar offset navigation`
- `period_boundary_marker`
  - 예: 연말, 월말
  - rationale: `calendar boundary marker`

### Expected Gate Chain

1. internal build
2. internal acceptance review
3. projection gate package
4. runtime projection gate
5. chunk rebuild gate

### Expected Evidence Pack

- before snapshot
- holdout / reserve / sentinel proof
- expected bucket table
- actual bucket table
- search/tree/chunk consistency

## self-review and reflection note

### Initial Framing

- 처음에는 `Month Unit Batch`를 next green으로 올릴 수 있는지 먼저 봤다.

### Self-Critique

- 하지만 missing inventory가 많아서 one-batch-one-rev green 기준을 통과하지 못했다.
- `Date Point Batch`도 `날` duplicate 때문에 green으로 올리기엔 이르다.

### Revision

- 그래서 가장 clean한 `Calendar Label Batch-11`을 추천안으로 고정했다.

### Reflection

- 현재 evidence와 공식 learner topic cluster만으로 next green batch 선정까지는 충분하다.
- 추가 딥 리서치는 아직 필수 아님.
- 다만 `Month Unit Batch`를 yellow에서 green으로 내리기 전에는 inventory normalization 쪽 별도 조사 또는 정리가 필요할 수 있다.

## Conclusion

- 다음 green batch 추천안은 `Calendar Label Batch-11`이다.
- `Month Unit Batch`, `Date Point Batch`는 아직 `Yellow`로 유지하는 것이 맞다.
- 따라서 next dispatch는 `Calendar Label Batch-11 internal build`가 가장 practical하다.
