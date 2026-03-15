# Data Assignment Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-89`
> Logged: `2026-03-15 12:34:21`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-88` planning package를 기준으로 첫 실제 `coverage expansion build`를 수행한다.
- 이번 revision은 `Calendar Continuity Batch-14`를 한 번에 internal canonical에 구축하는 big-step data package다.
- 목표는 pilot contract를 유지한 채 아래를 동시에 닫는 것이다:
  - new nodes 14 추가
  - family-consistent edge package 구축
  - holdout / reserve / exception queue 유지
  - next projection/rebuild gate로 넘길 수 있는 내부 산출물과 evidence 작성

## Required Inputs

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV88_coverage_expansion_build_package_report.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV87_chunk_rebuild_gate_report.md`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`

## Batch Definition

- batch name:
  - `Calendar Continuity Batch-14`
- include new nodes:
  - `그제_일반명사-1`
  - `그저께_일반명사-1`
  - `다음날_일반명사-1`
  - `당일_일반명사-1`
  - `새벽_일반명사-1`
  - `오전_일반명사-1`
  - `낮_일반명사-1`
  - `오후_일반명사-1`
  - `화요일_일반명사-1`
  - `수요일_일반명사-1`
  - `목요일_일반명사-1`
  - `토요일_일반명사-1`
  - `주중_일반명사-1`
  - `평일_일반명사-1`

## Fixed Invariants

- existing holdout 4는 계속 `node exists / edge 0` 유지
- reserve queue는 이번 revision에서 건드리지 않음
- family templates:
  - `relative_day`: `today-centered relative offset`
  - `day_part`: `within-day sequence / boundary transition`
  - `week_frame`: `weekly schedule progression / weekday-weekend segmentation`

## Allowed Scope

- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json` update
- new nodes and edges for Batch-14
- `dry_run_reserve` update
- append-only build report 작성

## Forbidden Scope

- `publish-only` 실행 금지
- `chunk rebuild` 실행 금지
- `live overwrite` 금지
- reserve queue 해제 금지
- 새 relation semantics / 새 runtime contract 제안 금지

## Required Outcome

- Batch-14 internal build report
- internal graph delta summary
- holdout / reserve proof
- family-level reason consistency proof
- duplicate / reciprocal / required field evidence
- next recommendation:
  - internal acceptance review gate 개시 여부
