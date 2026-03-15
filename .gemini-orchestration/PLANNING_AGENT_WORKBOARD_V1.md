# 기획 에이전트 작업보드 (V1)

> Agent: `기획 에이전트` (Planning Agent)
> Required Skills: `doc-state-manager`, `korean-lexical-data-curation`
> Version: `V1-REV-100`
> Date: `2026-03-15`
> Status: `REPORTED` (Green Batch Autopilot Design Submitted)
> Read First: `README.md` → `PROJECT_DOCUMENT_MAP.md` → `ORCHESTRATION_DASHBOARD.md` → `08_expansion/README.md`
> Latest Detailed Report Path: `.gemini-orchestration/workboard_archive/planning/20260315_REV100_green_batch_autopilot_design_report.md`
> User Approval Gate: `승인됨` (`REV-100` green batch autopilot planning 진행 승인)
> Control Rule: 에이전트는 append-only 로그에만 보고하고, header/status/current task는 Codex/사용자만 변경한다.
> Role Definition: 정책/시나리오/owner map/acceptance input 설계 담당. PM이 아니므로 우선순위, 승인, 상태 확정은 하지 않는다.
> Strong Recommendation: High-Quality Work Standard 6개 기준을 강하게 따를 것.

## Current Task

- PM 관할 아래에서 실행되는 `Green Batch Autopilot` 설계
- green batch가 어디까지 자동으로 흐르고, 언제 Yellow로 승격되는지 운영 규칙으로 정리
- 실제 운영 문서로 쓸 수 있을 만큼 구체적이어야 함
- 새 relation semantics 발명이나 validated contract 재개방은 금지

## Expected Outputs

- Green Batch Autopilot memo
- autopilot step chain
- stop / promote-to-yellow rule
- PM intervention rule
- evidence pack auto-generation spec
- rollout order
- self-review and reflection note

## Validation Rule

- pilot/Batch-14에서 닫힌 contract를 재개방하지 말 것
- 새 정의, 새 개념, 새 relation type 제안 금지
- 독립 앱이 아니라 PM 관할 아래 운영 모델이어야 함
- micro-step TODO 나열로 끝내지 말 것
- 자동화 경계와 예외 승격 조건이 명확해야 함

## Solution Expectation

- 진단만 하지 말고 package-level proposal, 추천안, 장점, 리스크를 제시
- 독자 결정이 어려우면 최대 3개 이내의 planning 방안을 제시
- 각 방안에 추천안 / 장점 / 리스크를 포함
- final report에는 self-critique와 revision reflection을 포함할 것

## High-Quality Standard

- 문제를 planning 과업 수준으로 재정의
- 내용 sufficiency / 구조 sufficiency / 실행 gate를 분리
- 필요 시 외부 비교 근거를 붙임
- owner 문서와 적용 순서를 명시
- 현재 phase와 handoff gate를 넘지 않음
- 남은 리스크와 미결정을 숨기지 않음

## Blocking / Decision Needed

- 현재 blocker 없음
- 이번 revision의 핵심은 green batch를 실제로 어디까지 자동 운영할 수 있는지 닫는 것임
- proposal 제출 완료. green batch autopilot step chain, yellow 승격 규칙, PM 개입 규칙을 제안함

## Latest Snapshot

- pilot relation cycle과 Batch-14 완결, 그리고 운영 모델 정리가 기준 입력임
- 이번 cycle은 `V1-REV-100`
- PM-supervised green batch autopilot memo 제출 완료
- 현재 상태는 `REPORTED / AUTOPILOT MODEL PROPOSAL SUBMITTED`
- 상세 근거는 `20260315_REV100_green_batch_autopilot_design_report.md` 참고

## Latest Review

- baseline reference:
  - `V1-REV-77` canonical architecture 결과와 `V1-REV-82` holdout rule 결과를 함께 유지할 것

## User Approval

- requested: yes
- state: `승인됨`
- evidence: 사용자가 bounded pre-REV-83 survey 진행 승인

## Append-Only Report Log

- `.gemini-orchestration/workboard_archive/planning/20260314_REV72_policy_rework_snapshot.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV74_assignment_only.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV74_relation_model_execution_closure_proposal.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV74_canonical_delta_draft_by_codex.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV77_implementation_architecture_assignment.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV77_implementation_architecture_proposal.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_PRE_REV83_execution_method_survey_assignment.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_PRE_REV83_execution_method_survey_report.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV88_coverage_expansion_build_package_assignment.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV88_coverage_expansion_build_package_report.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV94_batch_agent_operating_model_assignment.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV94_batch_agent_operating_model_report.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV95_next_green_batch_selection_assignment.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV100_green_batch_autopilot_design_assignment.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV95_next_green_batch_selection_report.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_REV100_green_batch_autopilot_design_report.md`
