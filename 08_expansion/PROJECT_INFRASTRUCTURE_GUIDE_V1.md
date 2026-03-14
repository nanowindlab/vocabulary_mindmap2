# 프로젝트 인프라 및 구조 가이드 (Project Infrastructure Guide V1)

> **목적**: `Project X-CLEAN`을 통해 정립된 프로젝트의 물리적 디렉토리 표준, 에이전트별 관리 권한(Ownership), 그리고 파일 이동에 따른 변경 이력(Changelog)을 단일 진실 공급원(SSOT)으로 통합 제공합니다.

---

## 1. 프로젝트 디렉토리 표준 구조 (Standard Architecture)

프로젝트의 장기적 유지보수와 배포 안정성을 위해 데이터의 생명주기와 성격에 따라 폴더를 격리합니다.

### 1.1. [ROOT] 핵심 자산 (Core Assets)
루트 디렉토리는 누구나 프로젝트를 한눈에 파악할 수 있도록 최소한의 필수 자산만 유지합니다.
- **[`README.md`](../README.md)**: 프로젝트 통합 진입점. (핵심 문서 수정 시 반드시 동기화)
- **[`MASTER_ROADMAP_V1.md`](./MASTER_ROADMAP_V1.md)**: 마일스톤 및 전체 일정.
- **`.gemini-orchestration/`**: 에이전트 운영 가이드 및 대시보드 관리 폴더.
- *원칙*: 이 외의 1회성 스크립트나 결과물은 루트에 배치할 수 없습니다.

### 1.2. [/scripts/] 로직 및 도구 격리
루트에 산재했던 20여 개의 Python 스크립트를 기능별로 분리 보관합니다.
- **`scripts/core/`**: 마스터 풀 빌드, 트리 생성, 검색 인덱스 갱신.
- **`scripts/mining/`**: XWD 마이닝, 외부 사전 연동, 연관 데이터 추출.
- **`scripts/triage/`**: 데이터 정제, AI 분류, QC 자동화.

### 1.3. [/08_expansion/] 데이터 및 명세 관리
데이터의 속성(Raw/Audit/Final)에 따라 논리적 저장소를 분리합니다.
- 운영 원칙: `08_expansion/` 내부 문서 구조나 archive 정책을 수정하면 `PROJECT_DOCUMENT_MAP.md`와 이 문서를 반드시 같은 변경 세트에서 함께 갱신한다. 구조 관련 변경은 새 버전 문서를 추가하기보다 현재 canonical 문서에 즉시 반영한다.
- 실무 진입 문서: `08_expansion/README.md`
- 구조 검증 참고 문서: `08_expansion/MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md`
- **`final_spec/`** (예정): 최종 승인된 IA, UX 시나리오, 프로토콜.
- **`raw_data/`** (예정): 시스템 참조용 기초 데이터 (예: `05_source`).
- **`08_expansion/archive/`**: 완료된 작업의 구버전(`V1~V(n-1)`) 명세서 및 1회성 검증 로그(Audit)를 보관하는 canonical document history zone.

### 1.4. [/10_product_guide/] 배포용 제품 문서
- 사용자와 개발자를 위한 최종 매뉴얼, 브랜딩 가이드, 튜토리얼 보관소.

### 1.5. Current Practical Note
- 현재 canonical 기획/정책 문서는 `08_expansion/` 루트에 직접 배치되어 있다.
- 앱 배포와 runtime 검증에 필요한 민감 문서는 다음 현재 경로를 유지한다:
  - `09_app/README.md`
  - `09_app/public/data/README.md`
  - `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
  - `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`
- 향후 폴더 재구성 시에도 위 경로들은 대체 경로가 충분히 고지되기 전까지 바로 이동하지 않는다.
- top-level `archive/`는 현재 canonical document archive가 아니다. 오래된 handoff와 legacy session history를 보관하는 참고 구역으로만 유지한다.
- 현재 Markdown 링크 그래프와 입구 문서 검증 결과는 `08_expansion/MARKDOWN_DOCUMENT_RELATION_MINDMAP_V1.md`를 기준으로 확인한다.

---

## 2. 에이전트 오너십 및 거버넌스 (Ownership Matrix)

파일 오염 및 권한 충돌을 막기 위해 도메인별 '주 편집 권한(Primary Ownership)'을 엄격히 규정합니다.

| 에이전트 | 전담 관리 영역 | 책임 범위 및 관리 지침 |
| :--- | :--- | :--- |
| **기획** | `Spec/`, `roadmap/`, `10_product_guide/` | 비즈니스 로직 및 UI 정책 최신화. (메타데이터 임의 수정 금지) |
| **데이터** | `raw_data/`, `scripts/`, `05_source/` | 데이터 무결성 보존. **스크립트 내부 상대 경로(`../`) 파손 방지 및 보정 의무.** |
| **개발** | `09_app/`, `dist/`, 빌드 설정 파일 | 런타임 데이터 로드 경로 및 UI 프론트엔드 성능 최적화. |
| **리뷰** | `audit_reports/`, `archive/`, `DASHBOARD` | 프로젝트 구조 무결성 감시 및 **모든 구버전 문서의 최종 아카이빙 권한 보유**. |

---

## 3. 구조 변경 및 파일 이동 이력 (Structural Changelog)

기존 `08_expansion/` 루트에 혼재되어 있던 구버전 문서와 오딧 결과물들은 무결성 보증(링크 교정 완료) 후 아래와 같이 `08_expansion/archive/` 폴더로 영구 격리되었습니다. (실행일: 2026-03-11)

### 3.1. 히스토리 명세서 (`08_expansion/archive/historical_docs/`)
최신 버전의 SSOT 문서를 제외한 모든 이전 기획안이 이동되었습니다.
- `IA_AND_UX_SCENARIO_SPEC_V1~V7.md` (최신 V8 유지)
- `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V3~V4.md` (초기 구버전 아카이빙 완료, 현재 canonical은 V11)
- `VOCAB_LEVEL_BAND_DEFINITION_V1~V2.md` (최신 V3 유지)
- `STRICT_DATA_CLASSIFICATION_PROTOCOL_V1.md` (최신 V2 유지)

### 3.2. 일시적 감사 로그 (`08_expansion/archive/audit_logs/`)
특정 시점의 데이터 검증을 위해 생성된 후 효력이 다한 보고서들입니다.
- `REVIEW_MEMO_*.md` (과거 리뷰어 메모 전수)
- `PAYLOAD_136_*` (초기 136개 샘플 감사 로그)
- `ABSTRACT_ROOT_BOUNDARY_PRIORITY_AUDIT_V1.md`
- `FULL_INVENTORY_AUDIT_COMPLETION_V1.md`
- `DATA_QC_PROTOCOL_V1.md` 및 `DATA_REFINEMENT_REPORT_V1.md`

### 3.3. Legacy Session History (`archive/`)
top-level `archive/`는 별도 역할을 가진다.

- `NEXT_THREAD_HANDOFF_V*.md`
- `restart_QA.md`
- `_v2` 시기 구세대 폴더 스냅샷

이 영역은 현재 운영 handoff나 canonical 문서 보관소가 아니라, 과거 세션 흐름을 복기하기 위한 history-only 참고 구역이다.

---
*참조 무결성 원칙*: 본 문서의 내용이 변경될 경우 반드시 루트 `README.md`에 반영되어야 하며, 문서 간 링크(Markdown Link)는 항상 최신 `V` 번호를 가리키도록 상시 교정되어야 합니다.
