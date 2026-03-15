# Green Batch Agent Workboard (V1)

> Agent: `Green Batch Agent`
> Required Skills: `data-validation`, `korean-lexical-data-curation`, `multi-agent-orchestration`
> Version: `V1-REV-101`
> Date: `2026-03-15`
> Status: `REPORTED` (Batch-11 Autopilot Trial Completed)
> Read First: `README.md` → `PROJECT_DOCUMENT_MAP.md` → `ORCHESTRATION_DASHBOARD.md` → `.gemini-orchestration/BATCH_AGENT_OPERATING_MODEL_V1.md`
> Latest Detailed Report Path: `.gemini-orchestration/workboard_archive/green_batch/20260315_REV101_batch11_green_autopilot_trial_report.md`
> User Approval Gate: `승인됨` (`REV-101` green batch autopilot trial 진행 승인)
> Control Rule: 에이전트는 append-only 로그에만 보고하고, header/status/current task는 Codex/사용자만 변경한다.

## Current Task

- `Calendar Label Batch-11`의 green autopilot trial 수행
- internal build 완료 상태를 입력으로 받아
  - projection gate
  - runtime projection
  - chunk sync
  - consolidated report
  를 한 흐름으로 닫기
- stop signal이 하나라도 뜨면 즉시 yellow로 승격하고 자동 실행을 멈출 것

## Expected Outputs

- consolidated autopilot report
- step result table
- before/after snapshots
- expected vs actual bucket
- holdout / reserve / sentinel proof
- search/tree/chunk consistency proof
- final autopilot status

## Validation Rule

- `Type A + Green` contract를 벗어나지 말 것
- stop signal 발생 시 이후 step 실행 금지
- `publish-only` 이후 `chunk rebuild`까지 자동으로 이어가되, 예외 시 yellow 승격
- final report는 한 문서로 통합할 것

## Blocking / Decision Needed

- 현재 blocker 없음
- stop signal 발생 시 PM/Codex가 yellow 승격 여부를 확정함

## Latest Snapshot

- first autopilot trial target은 `Calendar Label Batch-11`
- current stage는 runtime projection + chunk sync를 하나의 흐름으로 묶는 실험
- 현재 상태는 `DISPATCHED / NOT STARTED`

## User Approval

- requested: yes
- state: `승인됨`
- evidence: 사용자가 개입 최소화와 배치 에이전트 운영 방향을 승인

## Append-Only Report Log

- `.gemini-orchestration/workboard_archive/green_batch/20260315_REV101_batch11_green_autopilot_trial_assignment.md`
- `.gemini-orchestration/workboard_archive/green_batch/20260315_REV101_batch11_green_autopilot_trial_report.md` (REV-101 완료 보고)
