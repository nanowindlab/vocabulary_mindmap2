# 09_app Guide

> Scope: 프론트엔드 개발, 앱 runtime 데이터 확인, 빌드/배포 전 확인용 진입 문서

## 1. App Role

`09_app/`는 이 프로젝트의 실제 React + Vite 프론트엔드 앱이다.

- 앱 엔트리: `09_app/src/main.jsx`
- 메인 화면 로직: `09_app/src/App.jsx`
- runtime 데이터 로더: `09_app/src/data/loaderAdapter.js`
- 정적 runtime 데이터: `09_app/public/data/live/`

## 2. Developer First-Read

개발 에이전트가 작업 시작 전에 우선 확인할 문서:

1. 루트 프로젝트 진입점: `README.md`
2. 운영 상태: `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
3. 개발 지시문: `.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md`
4. 앱 runtime 데이터 구조: `09_app/public/data/README.md`
5. 데이터 재배포 절차: `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
6. runtime canonical 판별 기준: `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`

## 3. Runtime Canonical

현재 앱이 실제 fetch하는 canonical 데이터는 아래 경로 기준이다.

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/CHUNK_MANIFEST_V1.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_*.json`
- `09_app/public/data/live/APP_READY_CHUNK_EXAMPLES_chunk_*.json`

주의:

- `legacy/`와 `archive/`는 비교/복구용이다.
- 앱 배포 검증이나 UI 연동 확인 시 `live/`를 우선 기준으로 본다.

현재 운영 메모:

- `REV-86` pilot runtime projection과 `REV-87` chunk rebuild gate를 통해 `core 12 + holdout 4` pilot relation이 `live/` runtime과 detail chunk까지 반영되었다.
- 현재 live는 전체 coverage build 완료 상태가 아니라, pilot relation package가 검증된 상태다.

## 4. Build Commands

```bash
npm install
npm run dev
npm run build
npm run preview
```

작업 디렉토리:

```bash
cd 09_app
```

## 5. Deployment-Sensitive Materials

아래 파일은 개발 에이전트가 찾기 쉬워야 하므로 현재 경로를 유지한다.

- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
- `.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `09_app/public/data/README.md`

문서 구조를 정리하더라도 위 경로들은 바로 없애거나 이동하지 않는다.

## 6. Orchestration Rule For Development Agent

개발 에이전트는 이 프로젝트에서 아래 운영 규칙을 따른다.

- `.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md`를 현재 snapshot 기준으로 읽는다.
- 세부 구현 보고는 `.gemini-orchestration/workboard_archive/development/` 아래 append-only 로그로 먼저 남긴다.
- 최종 승인, 배포 진행, 다음 단계 승격은 사용자 승인 기록이 있어야 한다.
