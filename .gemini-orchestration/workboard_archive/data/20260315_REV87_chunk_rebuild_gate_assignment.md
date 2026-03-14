# Data Assignment Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-87`
> Logged: `2026-03-15 01:05:34`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-86` pilot runtime projection이 성공했으므로, 이번 revision은 그 결과를 detail chunk까지 동기화하는
  **chunk rebuild gate**를 하나의 의미 있는 work package로 수행한다.
- 목적은 `core 12 + holdout 4` pilot이
  - search
  - split tree
  - detail chunk
  세 레이어에서 모두 같은 relation 상태를 갖는지 닫는 것이다.

## Required Inputs

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV86_pilot_runtime_projection_report.md`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/APP_READY_*_TREE.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_*.json`

## Package Goal

- `chunk rebuild`를 실행하고, pilot ids에 대해 search/tree/chunk 정합성이 닫혔음을 입증한다.
- holdout 4가 chunk rich files에서도 `0/0`으로 유지되는지 확인한다.
- 이후 단계는 coverage expansion build로 넘어갈지 판단 가능한 상태로 만든다.

## Allowed Scope

- `python3 scripts/core/rebuild_rev23_detail_chunks.py` 실행
- search/tree/chunk 비교 검증
- append-only rebuild gate report 작성

## Forbidden Scope

- 새 coverage expansion build 시작 금지
- 새 relation semantics / 새 runtime contract 제안 금지
- unrelated live data 수정 금지

## Required Outcome

- chunk rebuild gate report
- rebuild summary evidence
- pilot ids search/tree/chunk consistency proof
- holdout 4 chunk exclusion proof
- next recommendation:
  - coverage expansion build package로 넘어가도 되는지
