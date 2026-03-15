# Work Orchestration Hub V1

> Status: `CURRENT`
> Purpose: 현재 운영 오케스트레이션의 공용 허브. legacy restart 문서와 분리된 현재 기준 요약본.

## 1. Current Source of Truth

현재 운영 문서는 아래 순서로 읽는다.

1. `README.md`
2. `PROJECT_DOCUMENT_MAP.md`
3. `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
4. 필요한 agent workboard
5. `08_expansion/README.md`
6. 필요한 canonical 정책 문서

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
- 승인 상태는 대시보드 또는 workboard에 남긴다.
- 단, 승인 게이트가 아닌 일반 sequencing과 revision 개시는 Codex가 자율적으로 이어간다.
- 즉 사용자 승인 대상이 아닌 경우에는 매번 사용자에게 다시 묻지 않고 다음 work package를 바로 연다.

## 5. Receipt / Start Evidence Rule

- 에이전트가 첫 append-only 로그를 남기면 그것을 `지시접수 / 착수 증거`로 간주한다.
- 에이전트는 상태를 직접 바꾸지 않는다.
- Codex가 해당 로그를 확인한 뒤 대시보드의 `지시접수`, `진행 상태`를 반영한다.

## 6. Workboard Logging Rule

- 현재 workboard는 snapshot이다.
- 세부 보고는 먼저 `.gemini-orchestration/workboard_archive/<agent>/` 아래 append-only 로그로 남긴다.
- workboard에는 최신 상태와 최신 상세 보고 경로만 유지한다.
- 개발 에이전트의 실행 환경이 바뀌어도 동일 규칙을 따른다.
- dashboard와 workboard의 제어 필드(Status, Approval, Current Task)는 Codex/사용자 전용이다.
- 에이전트는 append-only 로그에만 보고하고, snapshot 변경은 Codex가 반영한다.

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
