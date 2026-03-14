# 08_expansion Guide

> Scope: 기획/정책 SSOT와 데이터 실행 산출물이 함께 모여 있는 작업 구역의 진입 문서

## 1. How To Read This Folder

`08_expansion/`은 현재 두 종류의 자산을 함께 담고 있다.

1. 현재 canonical 문서
2. 데이터 실행 과정에서 생긴 배치/리포트/중간 산출물

작업자는 먼저 문서형 SSOT를 읽고, 그다음 필요한 실행 산출물 구역으로 내려가야 한다.

## 2. Canonical Documents At Root

아래 파일들은 현재 `08_expansion/` 루트에서 직접 관리되는 canonical 문서다.

- `MASTER_ROADMAP_V1.md`
- `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `PROJECT_DECISION_LOG_V1.md`
- `IA_AND_UX_SCENARIO_SPEC_V8.md`
- `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
- `RELATION_DATA_POLICY_V1.md`
- `APP_DATA_REDEPLOY_SOP_V1.md`
- `REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
- `PROJECT_INFRASTRUCTURE_GUIDE_V1.md`
- `DOCUMENT_STRUCTURE_MIGRATION_PLAN_V1.md`

아래 두 문서는 active secondary policy reference로 함께 본다.

- `VOCAB_LEVEL_BAND_DEFINITION_V3.md`
- `XWD_DISCOVERY_FRAMEWORK_V1.md`

아래 문서는 현재 구조 변경의 링크 검증 reference다.

- `MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md`

원칙:

- 구조 변경 시 문서 버전업보다 현재 canonical 문서에 바로 반영한다.
- 구조/위치/archive 정책 변경 시 `PROJECT_DOCUMENT_MAP.md`와 `PROJECT_INFRASTRUCTURE_GUIDE_V1.md`를 함께 갱신한다.

## 3. Folder Zones

### 3.1. `archive/`

- canonical document history zone
- 구버전 spec, tasklist, protocol, audit log 보관

### 3.2. `references/`

- 참고 자료 전용
- 현재 SSOT 아님

### 3.3. `master_pool/`, `inventory/`

- 데이터 기준 원장/집계 산출물
- 문서형 정책보다 실행 근거에 가까움

### 3.4. `rev23/`, `rev47/`, `augmentation/`

- 특정 실행 라운드 산출물과 보고 자료
- 현재 정책/배포 경로를 이해할 때만 선택적으로 참조

### 3.5. `batch_inputs/`, `batch_runs/`, `triage_reports/`, `triage_quarantine/`

- 배치 실행/검토/격리 산출물
- 운영 문서보다 생성물 성격이 강함

## 4. Developer Safety

개발 에이전트가 자주 찾는 배포 민감 자료는 현재 위치를 유지한다.

- `APP_DATA_REDEPLOY_SOP_V1.md`
- `REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
- `RELATION_DATA_POLICY_V1.md`

앱 runtime canonical은 `08_expansion/` 안이 아니라 `09_app/public/data/live/`다.

## 5. Recommended Reading Order

1. `README.md`
2. `PROJECT_DOCUMENT_MAP.md`
3. `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
4. `08_expansion/README.md`
5. 필요한 canonical 문서
6. 그다음에만 하위 실행 산출물 폴더
