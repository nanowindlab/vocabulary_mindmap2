# 어휘 마인드맵 (Vocabulary Mindmap) 프로젝트

> **지능형 한국어 어휘 탐색 플랫폼 (Intelligent Korean Vocabulary Exploration Platform)**
> 8,500여 건의 데이터를 '상황', '마음', '기초' 3대 축으로 연결한 탐색형 학습 서비스입니다.

---

## 🗺️ 프로젝트 전체 문서 지도 (Document Map)
가장 빠르게 원하는 문서를 찾으려면 아래 지도를 확인하십시오.
*   **[PROJECT_DOCUMENT_MAP.md](./PROJECT_DOCUMENT_MAP.md)**

---

## 🧭 프로젝트 관제탑 및 운영 (Governance)
프로젝트에 합류한 모든 에이전트(기획/데이터/리뷰/개발)는 작업 전 반드시 아래 운영 가이드와 대시보드를 확인해야 합니다.

> 참고: 개발 에이전트의 실행 환경이 바뀌더라도 동일한 오케스트레이션 문서, 사용자 승인 게이트, append-only 로그 규칙을 그대로 적용합니다.
> 참고: 각 에이전트는 자기 역할 안에서만 능동적이어야 하며, PM 역할은 Codex만 수행합니다.

1. **[오케스트레이션 대시보드 (Dashboard)](./.gemini-orchestration/ORCHESTRATION_DASHBOARD.md)**: 현재 진행 중인 미션과 에이전트별 워크보드 링크.
2. **[Main PM 역할 정의](./.gemini-orchestration/MAIN_PM_ROLE_DEFINITION_V1.md)**: Main PM의 권한, 책임, 필수 스킬, control field 소유권 정의.
3. **[오케스트레이션 허브 (Hub)](./.gemini-orchestration/WORK_ORCHESTRATION_HUB_V1.md)**: 현재 SSOT 읽기 순서와 active canonical 문서 요약.
4. **[운영 프로세스 가이드 (Rules)](./.gemini-orchestration/OPERATING_GUIDE_V1.md)**: 작업 시작/완료 시 대시보드 상태 변경 규칙 (DISPATCHED ➔ RUNNING ➔ REPORTED).
5. **[워크보드 템플릿 및 로그 규칙](./.gemini-orchestration/WORKBOARD_TEMPLATE_V1.md)**: 사용자 승인 게이트와 append-only 보고 방식의 기준 문서.
6. **[다음 Main PM handoff](./.gemini-orchestration/NEXT_MAIN_PM_HANDOFF_V1.md)**: 현재 상태(`REV-87` chunk rebuild gate까지) 기준 handoff 문서.

> 현재 상태 메모: `core 12 + holdout 4` pilot은 internal build, runtime projection, chunk rebuild gate까지 검증 완료되었습니다. 다음 큰 단계는 `coverage expansion build`입니다.

> 기본 프로토콜: 사용자는 대시보드 한 문서만 보고 현재 상태를 모니터링하고 지시합니다. 에이전트는 대시보드에서 자기 workboard로 내려가 상세 지시를 읽습니다.
> 운영 메모: 역할별 필수 스킬과 dashboard/workboard 제어 필드 소유권은 운영 가이드와 허브 문서를 기준으로 합니다.
> 운영 메모: 모든 에이전트는 진단에서 멈추지 않고 기본적으로 해결안을 제시해야 합니다. 독자 결정이 어려우면 최대 3개 이내의 선택지를 제안합니다.

---

## 📚 단일 진실의 원천 (SSOT Documents)
본 프로젝트의 뼈대가 되는 최종 승인 문서들입니다. 구버전은 참조하지 마십시오.

*   **[최종 태스크리스트 (Tasklist V11)](./08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md)**: 전체 개발/기획 항목 및 완료 체크리스트.
*   **[마스터 로드맵 (Roadmap)](./08_expansion/MASTER_ROADMAP_V1.md)**: 프로젝트 Phase별 목표와 비전.
*   **[프로젝트 결정 로그 (Decision Log)](./08_expansion/PROJECT_DECISION_LOG_V1.md)**: 용어, 아키텍처 등 중요 의사결정 히스토리.
*   **[IA 및 UX 시나리오 (Spec V8)](./08_expansion/IA_AND_UX_SCENARIO_SPEC_V8.md)**: 단계별 렌더링 및 횡단 점프 인터랙션 명세.

## 📐 핵심 정책 및 런타임 기준
현재 운영에서 자주 쓰는 정책/런타임 기준 문서입니다.

*   **[엄격한 분류 프로토콜 (SDCP)](./08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md)**: 재분류와 정책 보완의 최종 반영 위치.
*   **[연관 데이터 정책 (Relation Policy)](./08_expansion/RELATION_DATA_POLICY_V1.md)**: `related_vocab`와 `refs.cross_links` 분리 기준.
*   **[앱 데이터 재배포 SOP](./08_expansion/APP_DATA_REDEPLOY_SOP_V1.md)**: runtime JSON 재배포 절차.
*   **[앱 런타임 가이드](./09_app/README.md)**: 개발 에이전트용 앱 진입 문서와 runtime canonical 안내.

> 참고: `10_product_guide/` 및 별도 `IN_APP_TUTORIAL_SPEC` 문서는 현재 저장소에 배치되어 있지 않습니다. 사용자 경험 기준 문서는 현재 `IA_AND_UX_SCENARIO_SPEC_V8.md`와 태스크리스트를 우선 참조하십시오.

---

## 🧹 폴더 구조 및 파일 위치 안내
프로젝트 클리닝(X-CLEAN) 작업으로 구버전 문서들의 위치가 변경되었습니다. 파일 위치와 오너십은 아래 인프라 가이드를 확인하십시오.
*   **[프로젝트 인프라 및 구조 가이드 (Infrastructure Guide)](./08_expansion/PROJECT_INFRASTRUCTURE_GUIDE_V1.md)**
*   **[문서 구조 단계형 정리 계획 (Migration Plan)](./08_expansion/DOCUMENT_STRUCTURE_MIGRATION_PLAN_V1.md)**: 개발 에이전트 경로를 보호하면서 문서/archive 구조를 단계적으로 정리하는 기준 문서.
*   **[`08_expansion/README.md`](./08_expansion/README.md)**: `08_expansion` 내부의 canonical 문서 구역과 실행 산출물 구역을 구분해 주는 진입 문서.
*   **[Markdown 문서 연결 마인드맵](./08_expansion/MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md)**: 전체 `*.md` 연결관계와 구조 변경 후 링크 무결성 검증 결과.

---
*Last Updated: 2026-03-15 by Codex*
