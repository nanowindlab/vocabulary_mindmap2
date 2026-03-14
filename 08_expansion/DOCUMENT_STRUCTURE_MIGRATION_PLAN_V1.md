# Document Structure Migration Plan V1

> Purpose: 문서 폴더 구조를 단계적으로 정리하되, 개발 에이전트의 앱 작업 경로와 runtime/deploy 자료 접근성을 절대 훼손하지 않기 위한 authoritative migration plan
>
> Status: `ACTIVE - Phase 1 Complete / Phase 2 Defined`

## 1. Core Rule

문서 구조를 정리할 때 아래 두 원칙을 동시에 지킨다.

1. 문서형 SSOT와 history 구역을 더 명확히 분리한다.
2. 개발 에이전트가 앱 runtime, 재배포, 검증 자료를 찾는 기존 경로는 유지한다.

## 2. Protected Paths (Do Not Move Yet)

아래 경로는 개발/데이터/리뷰 에이전트의 현재 작업 동선에 직접 연결되므로, 대체 경로와 재링크가 끝나기 전까지 이동하지 않는다.

- `09_app/README.md`
- `09_app/public/data/README.md`
- `09_app/public/data/live/`
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`

## 3. Current Canonical Document Relations

### 3.1. Root Entry

- `README.md`
  - 프로젝트 진입점
  - `PROJECT_DOCUMENT_MAP.md`와 `08_expansion/PROJECT_INFRASTRUCTURE_GUIDE_V1.md`로 연결

### 3.2. Operational SSOT

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
  - 현재 미션 상태
- 각 workboard
  - 에이전트별 현재 task

### 3.3. Planning / Policy SSOT

- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
  - authoritative tasklist
- `08_expansion/PROJECT_DECISION_LOG_V1.md`
  - 핵심 결정 기록
- `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
  - canonical classification policy
- `08_expansion/RELATION_DATA_POLICY_V1.md`
  - relation policy

### 3.4. Runtime / Deploy SSOT

- `09_app/public/data/live/`
  - app runtime canonical data
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
  - runtime 재배포 절차
- `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
  - runtime canonical 검토 기준
- `09_app/README.md`
  - 개발 에이전트용 앱 진입 문서

## 4. Archive Zone Policy

### 4.1. Canonical Document History

- `08_expansion/archive/`
  - 문서형 history의 canonical archive
  - `historical_docs/`, `audit_logs/` 포함

### 4.2. Legacy Session History

- `archive/`
  - 오래된 handoff, restart 메모, `_v2` 스냅샷 보관
  - 현재 상태 판단용 SSOT가 아님

## 5. Phase Plan

### Phase 1. Zone Definition [Completed]

완료 내용:

- `08_expansion/archive/`와 top-level `archive/`의 역할 분리
- app runtime/deploy 민감 경로 보호 원칙 명시
- `09_app/README.md`를 프로젝트 전용 앱 가이드로 교체
- `08_expansion/README.md`를 추가하여 canonical 문서와 실행 산출물의 구역을 분리 안내
- `MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md`로 전체 Markdown 링크 그래프와 구조 변경 후 무결성 검증 결과를 문서화
- legacy `WORK_ORCHESTRATION_HUB_V1.md`를 `.gemini-orchestration/archive/WORK_ORCHESTRATION_HUB_RESTART_LEGACY_V1.md`로 분리하고, 현재 운영용 slim hub를 같은 파일명으로 재정의

### Phase 2. Top-Level Archive Triage [Current]

목표:

- top-level `archive/`의 각 항목을 `keep as legacy snapshot` vs `move candidate`로 분류
- 개발/데이터/리뷰 에이전트가 잘못 참조할 가능성이 있는 항목에 설명을 추가

현재 분류:

| Path | Type | Decision | Reason |
| :--- | :--- | :--- | :--- |
| `archive/NEXT_THREAD_HANDOFF_V3.md` | legacy handoff | keep | history-only session memo |
| `archive/NEXT_THREAD_HANDOFF_V4.md` | legacy handoff | keep | history-only session memo |
| `archive/NEXT_THREAD_HANDOFF_V5.md` | legacy handoff | keep | history-only session memo |
| `archive/restart_QA.md` | restart memo | keep | reset context reference |
| `archive/08_expansion_v2/` | old snapshot | keep | old folder snapshot, not single-doc archive |
| `archive/09_app_v2/` | old snapshot | keep | old app snapshot, not current runtime |

현재 판단:

- top-level `archive/`에는 당장 `08_expansion/archive/`로 옮겨야 할 문서형 spec/audit가 많지 않다.
- 대부분이 “세션 흐름” 또는 “구세대 폴더 스냅샷”이라 현재는 legacy zone에 두는 편이 더 안전하다.

### Phase 3. Canonical Spec Segmentation [Pending]

목표:

- `08_expansion/` 루트의 canonical 문서를 장기적으로 더 명확한 구역으로 재배치할지 판단

선행 조건:

- `APP_DATA_REDEPLOY_SOP_V1.md`
- `REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
- `RELATION_DATA_POLICY_V1.md`
- `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`

위 문서들의 인용 관계와 개발/데이터 에이전트 사용 빈도를 먼저 검토해야 한다.

### Phase 4. Optional Physical Moves [Pending]

조건:

- 이동 대상이 문서형 history여야 한다
- 현재 workboard, dashboard, app guide, runtime SOP에서 직접 인용되지 않아야 한다
- 이동 후 링크를 즉시 전수 교정할 수 있어야 한다

## 6. Change Safety Checklist

문서 이동 또는 폴더 재배치 전에 반드시 확인:

- 개발 에이전트가 `09_app/README.md`만 읽고도 build/runtime/deploy 문서를 찾을 수 있는가
- 데이터 에이전트가 `APP_DATA_REDEPLOY_SOP_V1.md`와 `REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`를 그대로 찾을 수 있는가
- `PROJECT_DOCUMENT_MAP.md`와 `README.md`가 최신 경로를 가리키는가
- `.gemini-orchestration/` 현재 작업 문서에서 경로 혼선이 발생하지 않는가

## 7. Current Decision

이번 단계에서는 실제 파일 이동보다 “보호 경로 유지 + 역할 정의 + triage 기준 명문화”가 우선이다.
다음 물리 이동은 이 문서의 Phase 2, Phase 4 기준을 만족하는 항목만 대상으로 진행한다.
