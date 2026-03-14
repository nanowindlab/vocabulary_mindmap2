# 프로젝트 문서 지도 (Project Document Map)

> **안내**: 루트 `README.md`에서 파생되는 프로젝트의 모든 핵심 문서(SSOT)들의 계층적 지도입니다. 
> 에이전트와 관리자는 이 지도를 통해 원하는 문서로 즉시 이동할 수 있습니다.

## 🧭 1. 오케스트레이션 및 운영 (Root & `.gemini-orchestration/`)
- 📄 **[README.md](./README.md)**: 프로젝트의 최초 진입점.
- 📄 **[ORCHESTRATION_DASHBOARD.md](./.gemini-orchestration/ORCHESTRATION_DASHBOARD.md)**: 에이전트 작업 현황 관제탑.
- 📄 **[OPERATING_GUIDE_V1.md](./.gemini-orchestration/OPERATING_GUIDE_V1.md)**: 에이전트 행동 강령 및 폴더 구조 규칙.
  - ↳ 📋 [PLANNING_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/PLANNING_AGENT_WORKBOARD_V1.md)
  - ↳ 📋 [DATA_VALIDATION_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md)
  - ↳ 📋 [REVIEW_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/REVIEW_AGENT_WORKBOARD_V1.md)
  - ↳ 📋 [DEVELOPMENT_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md)

## 🏗️ 2. 기획 및 아키텍처 (`08_expansion/`)
- 📄 **[MASTER_ROADMAP_V1.md](./08_expansion/MASTER_ROADMAP_V1.md)**: 프로젝트 전체 마일스톤 및 일정.
- 📄 **[SOURCE_RICH_IMPLEMENTATION_TASKLIST_V10.md](./08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V10.md)**: 상세 개발/기획 태스크리스트 (HD).
- 📄 **[PROJECT_DECISION_LOG_V1.md](./08_expansion/PROJECT_DECISION_LOG_V1.md)**: 핵심 의사결정 및 용어 변경 히스토리.
- 📄 **[IA_AND_UX_SCENARIO_SPEC_V8.md](./08_expansion/IA_AND_UX_SCENARIO_SPEC_V8.md)**: 마인드맵 단계별 렌더링 및 횡단 점프 명세.
- 📄 **[IN_APP_TUTORIAL_SPEC_V1.md](./08_expansion/IN_APP_TUTORIAL_SPEC_V1.md)**: 인앱 인터랙티브 가이드 및 툴팁 설계 (Next).
- 📄 **[PROJECT_INFRASTRUCTURE_GUIDE_V1.md](./08_expansion/PROJECT_INFRASTRUCTURE_GUIDE_V1.md)**: 에이전트 오너십 및 폴더 구조 가이드.
- 📄 **[APP_DATA_REDEPLOY_SOP_V1.md](./08_expansion/APP_DATA_REDEPLOY_SOP_V1.md)**: 단어 업데이트 후 앱 runtime JSON 재배포 표준 절차.

## 🛠️ 3. 개발 및 인프라 로직 (`scripts/`)
- 📂 **[scripts/core/](./scripts/core/)**: 마스터 풀 빌드 및 트리 생성 핵심 로직.
- 📂 **[scripts/mining/](./scripts/mining/)**: XWD(맥락적 연관) 마이닝 및 데이터 주입 도구.
- 📂 **[scripts/triage/](./scripts/triage/)**: AI 기반 어휘 분류 및 정제 스크립트.
- 📂 **[scripts/legacy/](./scripts/legacy/)**: 이전 버전 호환용 및 보관용 스크립트.

## 📖 4. 데이터 정책 (`08_expansion/`)
- 📄 **[RELATION_DATA_POLICY_V1.md](./08_expansion/RELATION_DATA_POLICY_V1.md)**: 연관 데이터(Related/Cross) 정의 및 분리 정책 (SSOT).
- 📄 **[APP_DATA_REDEPLOY_SOP_V1.md](./08_expansion/APP_DATA_REDEPLOY_SOP_V1.md)**: 데이터 갱신 및 앱 배포 표준 절차 (SOP).
- 📄 **[VOCAB_LEVEL_BAND_DEFINITION_V3.md](./08_expansion/VOCAB_LEVEL_BAND_DEFINITION_V3.md)**: TOPIK 통계 기반 Band 및 Level 산출 로직.
- 📄 **[XWD_DISCOVERY_FRAMEWORK_V1.md](./08_expansion/XWD_DISCOVERY_FRAMEWORK_V1.md)**: 20종 맥락적 훅(Hooks) 기반 연관 단어 발굴 규칙.
- 📄 **[RELATION_DATA_POLICY_V1.md](./08_expansion/RELATION_DATA_POLICY_V1.md)**: `related_vocab` / `refs.cross_links` 정의, 분리 기준, runtime 정책.
- 📄 **[APP_DATA_REDEPLOY_SOP_V1.md](./08_expansion/APP_DATA_REDEPLOY_SOP_V1.md)**: 단어 업데이트 후 앱 runtime JSON 재배포 표준 절차.

## 🎯 5. 최종 제품 가이드 (`10_product_guide/`)
- 📄 **[CONCEPT_AND_USER_GUIDE_V2.md](./10_product_guide/CONCEPT_AND_USER_GUIDE_V2.md)**: 앱 배포 시 사용자에게 제공되는 통합 튜토리얼 및 철학서.
