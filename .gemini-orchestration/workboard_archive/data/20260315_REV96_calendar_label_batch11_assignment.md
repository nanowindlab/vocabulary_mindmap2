# Data Assignment Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-96`
> Logged: `2026-03-15 13:47:18`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-95` next green batch selection memo를 기준으로, 다음 green batch인 `Calendar Label Batch-11` internal build를 수행한다.
- 이번 revision은 validated contract를 재사용하는 `Type A + Green` batch다.

## Batch Definition

- batch name:
  - `Calendar Label Batch-11`
- include nodes:
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

## Fixed Invariants

- holdout 4 unchanged
- reserve queue unchanged
- existing green batches unchanged

## Allowed Scope

- internal canonical node/edge build
- `dry_run_reserve` update
- append-only build report 작성

## Forbidden Scope

- `publish` 실행 금지
- `chunk rebuild` 실행 금지
- reserve / yellow candidate touch 금지
- 새 relation semantics 제안 금지

## Required Outcome

- Batch-11 internal build report
- internal graph delta
- holdout / reserve proof
- family-level reason consistency proof
- next internal acceptance recommendation
