# Work Orchestration Hub V1

> Status: `CURRENT`
> Purpose: 현재 운영 오케스트레이션의 공용 허브. legacy restart 문서와 분리된 현재 기준 요약본.

## 1. Current Source of Truth

현재 운영 문서는 아래 순서로 읽는다.

1. `README.md`
2. `PROJECT_DOCUMENT_MAP.md`
3. `.gemini-orchestration/MAIN_PM_ROLE_DEFINITION_V1.md`
4. `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
5. `08_expansion/PM_STATE_MANAGEMENT_PROTOCOL_V1.md`
6. `08_expansion/pm_reports/20260315_PM_RUNTIME_RECOVERY_AND_RESTART_PLAN_V1.md`
7. `.gemini-orchestration/NEXT_MAIN_PM_HANDOFF_V1.md`
8. `08_expansion/README.md`
9. 필요한 canonical 정책 문서

사용자 기준 단일 control plane은 `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`다.
사용자는 대시보드만 보고 현재 상태를 모니터링하고 에이전트에게 지시한다.

## 2. Active Canonical Documents

- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `08_expansion/MASTER_ROADMAP_V1.md`
- `08_expansion/PROJECT_DECISION_LOG_V1.md`
- `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`

## 3. Active Runtime / App Path

- app code: `09_app/`
- runtime canonical: `09_app/public/data/live/`
- app entry guide: `09_app/README.md`

## 4. Approval Rule

- Codex 검증 완료만으로는 최종 승인되지 않는다.
- `ACCEPT`, `DONE`, 다음 단계 승격, 배포 진행은 반드시 사용자 승인 기록이 있어야 한다.
- 승인 상태는 대시보드와 handoff에 남긴다.
- 단, 승인 게이트가 아닌 일반 sequencing과 revision 개시는 Codex가 자율적으로 이어간다.
- 즉 사용자 승인 대상이 아닌 경우에는 매번 사용자에게 다시 묻지 않고 다음 work package를 바로 연다.

## 5. Active State Update Rule

- 현재 상태는 대시보드가 소유한다.
- 세부 근거와 중간 산출물은 `08_expansion/pm_reports/`가 소유한다.
- 다음 스레드 재진입 상태는 handoff가 소유한다.
- 개발 에이전트의 실행 환경이 바뀌어도 동일 규칙을 따른다.
- dashboard, handoff, decision log, tasklist의 제어 필드는 Codex/사용자 전용이다.

## 6. Legacy Workboard Rule

- `.gemini-orchestration/*WORKBOARD*.md`와 `.gemini-orchestration/workboard_archive/`는 history-only다.
- 기존 증거를 읽는 용도로는 유지할 수 있지만, 현재 상태 갱신 경로로는 사용하지 않는다.

## 7. Solution-First Rule

- 모든 에이전트는 진단 후 반드시 해결안을 제시한다.
- 독자 결정이 가능한 문제는 해결안 + 후속 작업 제안까지 남긴다.
- 독자 결정이 어려운 경우에도 질문만 남기지 않고, 최대 3개 이내의 선택지를 제시한다.
- 각 선택지에는 추천안, 장점, 리스크를 포함한다.

## 8. Role-Based Skill Assignment

- **메인 PM / Codex**: `multi-agent-orchestration` + `doc-state-manager` + `data-validation`
- **기획 에이전트**: `doc-state-manager` + `korean-lexical-data-curation`
- **데이터 에이전트**: `data-validation`
- **리뷰 에이전트**: `report-verifier` + `data-validation`
- **개발 에이전트**: 기본은 코드베이스 우선, UI/UX 작업 시 `design-principles`

## 9. Legacy Reference

restart 시점의 legacy 허브는 아래로 이동했다.

- `.gemini-orchestration/archive/WORK_ORCHESTRATION_HUB_RESTART_LEGACY_V1.md`

오래된 handoff와 restart 메모는 history-only로 취급한다.
