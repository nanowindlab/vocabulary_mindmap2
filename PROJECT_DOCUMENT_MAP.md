# 프로젝트 문서 지도 (Project Document Map)

> **안내**: 루트 `README.md`에서 파생되는 프로젝트의 모든 핵심 문서(SSOT)들의 계층적 지도입니다. 
> 에이전트와 관리자는 이 지도를 통해 원하는 문서로 즉시 이동할 수 있습니다.

## 🧭 1. 오케스트레이션 및 운영 (Root & `.gemini-orchestration/`)
- 운영 메모: 사용자는 기본적으로 `ORCHESTRATION_DASHBOARD.md` 한 문서만 보고 모니터링하고 지시한다. 에이전트는 대시보드에서 각 workboard로 내려간다.
- 운영 메모: 개발 에이전트의 실행 환경이 바뀌더라도 아래 오케스트레이션 문서와 workboard 규칙을 동일하게 따른다.
- 운영 메모: 현재 `core 12 + holdout 4` pilot은 runtime projection과 chunk rebuild gate까지 검증 완료되었고, 다음 큰 단계는 `coverage expansion build`다.
- 📄 **[README.md](./README.md)**: 프로젝트의 최초 진입점.
- 📄 **[ORCHESTRATION_DASHBOARD.md](./.gemini-orchestration/ORCHESTRATION_DASHBOARD.md)**: 에이전트 작업 현황 관제탑.
- 📄 **[MAIN_PM_ROLE_DEFINITION_V1.md](./.gemini-orchestration/MAIN_PM_ROLE_DEFINITION_V1.md)**: Main PM의 역할, 권한, 책임, 필수 스킬 정의.
- 📄 **[WORK_ORCHESTRATION_HUB_V1.md](./.gemini-orchestration/WORK_ORCHESTRATION_HUB_V1.md)**: 현재 운영용 공용 허브. SSOT 읽기 순서와 active canonical 문서 요약.
- 📄 **[OPERATING_GUIDE_V1.md](./.gemini-orchestration/OPERATING_GUIDE_V1.md)**: 에이전트 행동 강령 및 폴더 구조 규칙.
- 📄 **[WORKBOARD_TEMPLATE_V1.md](./.gemini-orchestration/WORKBOARD_TEMPLATE_V1.md)**: 표준 workboard snapshot 템플릿. 사용자 승인 게이트와 상세 보고 경로 포함.
- 📄 **[workboard_archive/README.md](./.gemini-orchestration/workboard_archive/README.md)**: workboard overwrite 유실 방지를 위한 append-only 로그 보관 규칙.
- 📄 **[NEXT_MAIN_PM_HANDOFF_V1.md](./.gemini-orchestration/NEXT_MAIN_PM_HANDOFF_V1.md)**: 다음 Main PM이 현재 상태를 이어받기 위한 handoff.
- 운영 메모: 역할별 필수 스킬과 dashboard/workboard 제어 필드 소유권은 `WORK_ORCHESTRATION_HUB_V1.md`, `OPERATING_GUIDE_V1.md`를 기준으로 본다.
- 운영 메모: 모든 에이전트는 solution-first 프로토콜을 따른다. 진단 후 해결안 제시가 기본이며, 독자 결정이 어렵다면 최대 3개 이내의 선택지를 제시한다.
- 운영 메모: 각 에이전트는 자기 역할 안에서만 능동적이어야 하며, PM 역할은 Codex만 수행한다.
  - ↳ 📋 [PLANNING_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/PLANNING_AGENT_WORKBOARD_V1.md)
  - ↳ 📋 [DATA_VALIDATION_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md)
  - ↳ 📋 [REVIEW_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/REVIEW_AGENT_WORKBOARD_V1.md)
  - ↳ 📋 [DEVELOPMENT_AGENT_WORKBOARD_V1.md](./.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md)

## 🏗️ 2. 기획 및 아키텍처 (`08_expansion/`)
- 운영 원칙: 폴더 구조, 문서 위치, archive 정책을 바꾸면 이 섹션과 `08_expansion/PROJECT_INFRASTRUCTURE_GUIDE_V1.md`를 같은 변경 세트에서 함께 갱신한다. 문서 버전업보다 현재 canonical 문서에 즉시 반영하는 것을 우선한다.
- 📄 **[08_expansion/README.md](./08_expansion/README.md)**: `08_expansion` 내부에서 canonical 문서와 실행 산출물 구역을 구분하는 진입 문서.
- 📄 **[MASTER_ROADMAP_V1.md](./08_expansion/MASTER_ROADMAP_V1.md)**: 프로젝트 전체 마일스톤 및 일정.
- 📄 **[SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md](./08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md)**: 상세 개발/기획 태스크리스트.
- 📄 **[PROJECT_DECISION_LOG_V1.md](./08_expansion/PROJECT_DECISION_LOG_V1.md)**: 핵심 의사결정 및 용어 변경 히스토리.
- 📄 **[IA_AND_UX_SCENARIO_SPEC_V8.md](./08_expansion/IA_AND_UX_SCENARIO_SPEC_V8.md)**: 마인드맵 단계별 렌더링 및 횡단 점프 명세.
- 📄 **[PROJECT_INFRASTRUCTURE_GUIDE_V1.md](./08_expansion/PROJECT_INFRASTRUCTURE_GUIDE_V1.md)**: 에이전트 오너십 및 폴더 구조 가이드.
- 📄 **[DOCUMENT_STRUCTURE_MIGRATION_PLAN_V1.md](./08_expansion/DOCUMENT_STRUCTURE_MIGRATION_PLAN_V1.md)**: 단계형 문서 구조 정리 계획. 보호 경로, archive triage, 이동 안전 조건 정의.
- 📄 **[MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md](./08_expansion/MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md)**: 전체 Markdown 문서 연결관계 마인드맵과 링크 무결성 검증 결과.
- 참고: 인앱 튜토리얼 명세 문서는 현재 저장소에 별도 파일로 존재하지 않으며, 관련 TODO는 Tasklist V11의 `T1.16`에서 관리함.

## 🛠️ 3. 개발 및 인프라 로직 (`scripts/`)
- 📂 **[scripts/core/](./scripts/core/)**: 마스터 풀 빌드 및 트리 생성 핵심 로직.
- 📂 **[scripts/mining/](./scripts/mining/)**: XWD(맥락적 연관) 마이닝 및 데이터 주입 도구.
- 📂 **[scripts/triage/](./scripts/triage/)**: AI 기반 어휘 분류 및 정제 스크립트.
- 📂 **[scripts/legacy/](./scripts/legacy/)**: 이전 버전 호환용 및 보관용 스크립트.

## 🖥️ 4. 앱 런타임 및 배포 (`09_app/`)
- 📄 **[09_app/README.md](./09_app/README.md)**: 개발 에이전트용 앱 진입 문서. build, runtime canonical, 배포 민감 자료 위치 안내.
- 📄 **[09_app/public/data/README.md](./09_app/public/data/README.md)**: `live/internal/legacy/archive` 데이터 폴더 역할 안내.
- 📄 **[APP_DATA_REDEPLOY_SOP_V1.md](./08_expansion/APP_DATA_REDEPLOY_SOP_V1.md)**: 데이터 변경 후 앱 runtime JSON 재배포 표준 절차.
- 📄 **[REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md](./08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md)**: 리뷰/개발 에이전트가 runtime canonical을 혼동하지 않기 위한 기준 안내.
- 운영 메모: 현재 live runtime은 internal canonical overlay 기반 pilot projection과 chunk sync가 반영된 상태다.

## 📖 5. 데이터 정책 (`08_expansion/`)
- 📄 **[STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md](./08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md)**: 현재 canonical 분류 프로토콜. 모든 재분류/앵커링 정책 변경의 최종 반영 위치.
- 📄 **[RELATION_DATA_POLICY_V1.md](./08_expansion/RELATION_DATA_POLICY_V1.md)**: 연관 데이터(Related/Cross) 정의 및 분리 정책 (SSOT).
- 참고: 앱 배포와 runtime 재생성 절차는 위 `앱 런타임 및 배포` 섹션의 `APP_DATA_REDEPLOY_SOP_V1.md`를 primary 기준으로 본다.
- 📄 **[VOCAB_LEVEL_BAND_DEFINITION_V3.md](./08_expansion/VOCAB_LEVEL_BAND_DEFINITION_V3.md)**: TOPIK 통계 기반 Band 및 Level 산출 로직.
- 📄 **[XWD_DISCOVERY_FRAMEWORK_V1.md](./08_expansion/XWD_DISCOVERY_FRAMEWORK_V1.md)**: 20종 맥락적 훅(Hooks) 기반 연관 단어 발굴 규칙.

## 🗄️ 6. 히스토리와 아카이브
- 📄 **[08_expansion/archive/README.md](./08_expansion/archive/README.md)**: canonical document history zone 안내.
- 📄 **[archive/README.md](./archive/README.md)**: legacy session history zone 안내. 오래된 handoff는 history-only로 취급.
- 📄 **[WORK_ORCHESTRATION_HUB_RESTART_LEGACY_V1.md](./.gemini-orchestration/archive/WORK_ORCHESTRATION_HUB_RESTART_LEGACY_V1.md)**: restart 시점 orchestration hub. 현재 운영 기준이 아닌 legacy 참고 문서.

## 🎯 7. 최종 제품 가이드
- 현재 `10_product_guide/` 디렉토리는 저장소에 배치되어 있지 않음.
- 배포용 사용자 가이드와 튜토리얼 설계는 Tasklist V11의 `T1.14`, `T1.16` 기준으로 후속 작성 예정.
