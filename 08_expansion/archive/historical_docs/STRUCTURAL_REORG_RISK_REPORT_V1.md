# [X-CLEAN] 구조 정리 리스크 감사 및 오너십 매핑 보고서 (V1)

> **목적**: 프로젝트 폴더 구조 최신화 및 파일 이동 시 발생하는 참조 무결성 리스크를 진단하고, 에이전트별 편집 오너십을 명확히 정의하여 데이터 오염을 방지함.

---

## 1. 참조 무결성 감사 결과 (Reference Audit)

현재 문서 간 버전 불일치 및 링크 파손 위험이 감지된 주요 항목입니다.

| 인용 문서 (Source) | 참조 대상 (Target) | 리스크 유형 | 진단 내용 |
| :--- | :--- | :--- | :--- |
| `MASTER_ROADMAP_V1.md` | `IA_AND_UX_SCENARIO_SPEC_V6.md` | **Version Mismatch** | 최신본인 V8이 존재함에도 구버전 V6를 참조 중. |
| `SOURCE_RICH_..._TASKLIST_V9.md` | `IA_AND_UX_SCENARIO_SPEC_V8.md` | **Implicit Link** | 텍스트로는 언급되나 마크다운 링크가 없어 추적이 어려움. |
| `08_expansion/` 폴더 전체 | `05_source/`, `09_app/` 등 | **Relative Path Risk** | 대부분 `../` 경로를 사용 중이며, 폴더 depth 변경 시 전체 링크 파손 가능성 높음. |
| `PROJECT_DECISION_LOG_V1.md` | `V1-REV-28` 이후 기록 | **Outdated Log** | 대시보드는 REV-61이나 로그는 REV-28에서 멈춰 있어 정합성 결여. |

---

## 2. 파일 및 폴더 오너십 매핑 (Ownership Mapping)

에이전트별 주 편집 권한(Primary Ownership)을 아래와 같이 정의하여 임의 수정을 차단합니다.

| 분류 (Category) | 해당 경로/파일명 | 주 오너 (Primary Owner) | 관리 지침 |
| :--- | :--- | :--- | :--- |
| **기획 및 명세 (Spec)** | `08_expansion/IA_AND_UX_*`, `VOCAB_LEVEL_*`, `10_product_guide/` | **기획 에이전트** | UI 로직 및 데이터 정책 문서 독점 편집. |
| **데이터 및 로직 (Data)** | `05_source/`, `08_expansion/*.json`, `scripts/`, `build_*.py` | **데이터 에이전트** | 원본 데이터 및 JSON 빌드 스크립트 전담. |
| **애플리케이션 (App)** | `09_app/src/`, `09_app/public/data/` | **개발 에이전트** | UI 구현체 및 배포용 런타임 데이터 관리. |
| **검수 및 품질 (QC)** | `08_expansion/DATA_QC_*`, `REVIEW_MEMO_*` | **리뷰 에이전트** | 품질 검수 결과 및 비판적 분석 보고서 관리. |
| **운영 및 대시보드** | `.gemini-orchestration/` | **공통 (매니저 지휘)** | 각 에이전트는 본인 행/워크보드만 수정. |

---

## 3. 구조 정리(Clean-up) 및 아카이빙 전략

### 3.1. 아카이빙 기준 (Archive Rules)
- **대상**: 최신 버전(Latest)을 제외한 모든 구버전(`V1`~`V(n-1)`) 문서.
- **방법**: `08_expansion/archive/` (신설 예정) 폴더로 일괄 이동.
- **예외**: `PROJECT_DECISION_LOG`와 같이 히스토리 추적이 필수인 문서는 루트 유지.

### 3.2. 리팩토링 시 링크 복구 프로세스
1. **[Dry Run]**: `grep`을 통해 이동 대상 파일명을 포함하는 모든 파일 리스트 확보.
2. **[Path Update]**: 파일 이동 직후, 확보된 리스트 내의 상대 경로를 신규 경로로 일괄 치환 (`sed` 또는 스크립트 활용).
3. **[Validation]**: `Markdown Link Check` 툴을 사용하여 깨진 링크 전수 검증.

---

## 4. 기획자 제안: README.md 워크플로우 (Sync Strategy)

문서의 파편화를 막기 위해 **'README 중심 운영'**을 제안합니다.
- **지침**: 주요 명세서의 `V` 버전이 올라갈 때마다, 즉시 루트 `README.md`의 목차 정보를 업데이트함.
- **효과**: 에이전트들이 파일 시스템을 뒤지는 대신 README에서 즉시 최신 SSOT 문서로 접근 가능.

---
**보고자**: 기획 에이전트
**일시**: 2026-03-11
**상태**: 리스크 분석 완료 (Next: 데이터 에이전트 실행 대기)
