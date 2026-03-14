# [V1-REV-60] 프로젝트 표준 구조 정의 및 에이전트 합의안 (V1)

> 작성일: 2026-03-11
> 작성자: 리뷰 에이전트 (Review Agent)
> 합의 대상: 매니저, 기획, 데이터, 개발 에이전트
> 상태: **FINAL_PROPOSAL** (최종 제안)

## 1. 개요 (Executive Summary)
본 합의안은 `Project X-CLEAN`의 최종 단계로, 기획 에이전트의 리스크 분석(V61)을 수용하여 프로젝트의 물리적 구조를 최적화하고 에이전트 간의 편집 오너십을 확립함. 이를 통해 참조 무결성을 회복하고 장기적 유지보수성을 극대화함.

---

## 2. 표준 디렉토리 구조 (Standard Structure)

### 2.1. [ROOT] 프로젝트 진입점 및 핵심 자산
- **`README.md`**: 프로젝트 전체 개요 및 최신 SSOT 문서 링크 (신규 생성).
- **`MASTER_ROADMAP_V1.md`**: 프로젝트 전체 일정 및 마일스톤 (최신본 V8 링크 반영).
- **`PROJECT_DECISION_LOG_V1.md`**: 핵심 의사결정 이력 (상시 최신화).
- **`.env.weather.example`, `.gitignore`**: 필수 시스템 설정 파일.

### 2.2. [/scripts/] 로직 및 도구 격리
- **`scripts/core/`**: 마스터 풀 빌드, 트리 생성, 검색 인덱스 갱신.
- **`scripts/mining/`**: XWD 마이닝, 외부 사전 연동, 연관 데이터 추출.
- **`scripts/triage/`**: 데이터 정제, AI 분류, QC 자동화 스크립트.
- **`scripts/ops/`**: 배포 보조, 일회성 패치, 유틸리티.

### 2.3. [/08_expansion/] 데이터 및 명세 관리
- **`08_expansion/final_spec/`**: 최종 승인된 IA, UX 시나리오, 프로토콜 (SSOT).
- **`08_expansion/raw_data/`**: 시스템 참조용 기초 데이터 (Json/MD).
- **`08_expansion/audit_reports/`**: 마이닝 및 분류 감사 결과 리포트.
- **`08_expansion/archive/`**: 완료된 작업의 구버전(`V1~V(n-1)`) 및 임시 파일.

---

## 3. 에이전트별 편집 오너십 (Ownership Matrix)

| 에이전트 (Agent) | 전담 관리 영역 (Primary Ownership) | 책임 범위 |
| :--- | :--- | :--- |
| **기획 (Planning)** | `final_spec/`, `roadmap/`, `product_guide/` | 비즈니스 로직, UI 정책, 사용자 가이드 최신화. |
| **데이터 (Data)** | `raw_data/`, `scripts/`, `05_source/` | 데이터 무결성 보존, 마이닝 로직 고도화. |
| **개발 (Dev)** | `09_app/`, `dist/`, `vite.config.js` | UI 구현, 빌드 안정성, 런타임 성능 최적화. |
| **리뷰 (Review)** | `audit_reports/`, `archive/`, `DASHBOARD` | 구조 무결성 감시, 아카이빙 승인, 품질 보증. |

---

## 4. 실행 시퀀스 (Execution Sequence)

1. **[Step 1] 아카이빙 실행**: 리뷰 에이전트가 `08_expansion/` 내 구버전 파일들을 `archive/`로 이동 처리.
2. **[Step 2] 스크립트 이동**: 데이터 에이전트가 루트의 스크립트를 `scripts/` 하위로 이동하고 내부 경로 수정.
3. **[Step 3] 링크 복구**: 기획 에이전트가 `README.md`를 생성하고 문서 간 깨진 마크다운 링크를 전수 수정.
4. **[Step 4] 최종 검증**: 리뷰 에이전트가 `Markdown Link Check` 및 빌드 테스트를 통해 무결성 최종 승인.

---

## 5. 결론 및 향후 방안
본 합의안은 프로젝트의 '인지 부하'를 줄이고 에이전트 간의 '권한 충돌'을 원천 차단하는 장치임. 매니저 승인 즉시 **Step 1(아카이빙)**부터 착수하며, 모든 파일 이동은 `Dry Run` 과정을 거쳐 리스크를 최소화함.
