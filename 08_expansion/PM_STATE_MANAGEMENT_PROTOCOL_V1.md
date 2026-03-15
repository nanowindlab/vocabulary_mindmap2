# PM State Management Protocol V1

> Date: `2026-03-15`
> Owner: `Codex / Main PM`
> Purpose: workboard 없는 PM 중심 운영에서 프로젝트 경과, 중간 산출물, 다음 스레드 재진입 상태를 어디에 어떻게 남길지 고정한다.

## 1. Active State Surfaces

현재 운영에서 상태를 남기는 문서는 아래 5개다.

1. `README.md`
   - 프로젝트 전체 진입점
   - 현재 phase 한 줄 메모만 유지
2. `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
   - 사용자 기준 단일 control plane
   - 현재 active milestone, 현재 verdict, 승인 상태만 유지
3. `.gemini-orchestration/NEXT_MAIN_PM_HANDOFF_V1.md`
   - 다음 스레드 재진입 문서
   - 무엇이 검증되었고 무엇이 남았는지 요약
4. `08_expansion/PROJECT_DECISION_LOG_V1.md`
   - 운영 원칙, runtime contract, batch 분류 기준 같은 durable decision 기록
5. `08_expansion/pm_reports/*.md`
   - milestone별 중간 산출물, 조사 결과, evidence-backed closure 보고

## 2. Authoritative Ownership

- 현재 상태: `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- 다음 스레드 handoff: `.gemini-orchestration/NEXT_MAIN_PM_HANDOFF_V1.md`
- 승인된 규칙/결정: `08_expansion/PROJECT_DECISION_LOG_V1.md`
- 현재 cycle의 조사/복구/재분류 증거: `08_expansion/pm_reports/*.md`
- 남은 todo: `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`

같은 내용을 여러 문서에 풀텍스트로 반복하지 않는다.
상태는 대시보드가, 근거는 pm report가, 결정은 decision log가 각각 소유한다.

## 3. Artifact Management Rule

- 코드 변경: `scripts/`
- runtime/output 변경: `09_app/public/data/live/`, `09_app/public/data/internal/`
- milestone 보고: `08_expansion/pm_reports/`
- canonical 정책 변경: `08_expansion/*.md`

채팅에만 남은 내용은 다음 스레드 기준의 state로 인정하지 않는다.
이어져야 하는 판단과 증거는 반드시 위 경로 중 하나에 남긴다.

## 4. Legacy Handling

- `.gemini-orchestration/*WORKBOARD*.md`
- `.gemini-orchestration/workboard_archive/`

위 경로는 history-only로 취급한다.
기존 증거를 읽는 용도로는 유지할 수 있지만, 현재 운영 상태를 갱신하는 경로로는 더 이상 사용하지 않는다.

## 5. Reporting Rule

- milestone이 열리면 `08_expansion/pm_reports/`에 보고서를 만든다.
- 대시보드에는 그 milestone의 현재 verdict만 남긴다.
- handoff에는 다음 스레드가 바로 이어받을 최소 상태만 남긴다.
- 최종 승인이나 phase 승격은 사용자 승인 전까지 decision이 아니라 recommendation으로 기록한다.

## 6. Current Active Report

- `08_expansion/pm_reports/20260315_PM_RUNTIME_RECOVERY_AND_RESTART_PLAN_V1.md`

이 문서가 현재 cycle의 Yellow closure, Batch-11 contract redefinition, runtime projection hardening, batch portfolio reclassification, restart gate를 소유한다.
