# [V1-REV-55] 프로젝트 폴더 구조 및 파일 관리 체계 정밀 감사 보고서 (V1)

> 작성일: 2026-03-11
> 작성자: 리뷰 에이전트 (Review Agent)
> 상태: **PROPOSAL** (제안됨)

## 1. 개요 (Executive Summary)
본 보고서는 `vocabulary-mindmap2` 프로젝트의 급격한 데이터 확장 및 기획 고도화 과정에서 발생한 **'파일 및 디렉토리 관리의 무질서'**를 해소하기 위한 정밀 감사 결과와 최적화 방안을 제시함. 현재 루트에 산재된 25개 이상의 스크립트와 `08_expansion/` 내의 파편화된 버전들을 정리하여 장기적인 유지보수 안정성을 확보하는 것이 목표임.

---

## 2. 현황 진단 (Current Diagnosis)

### 2.1. 루트 디렉토리 (Root)
- **스크립트 범람**: 25개 이상의 `.py` 파일이 루트에 노출되어 있어 어떤 스크립트가 현재 유효한지 파악하기 어려움.
- **성격 혼재**: 데이터 처리(`classify_and_hydrate.py`), 마이닝(`run_rev47_xwd_mining.py`), 배포 전처리(`rebuild_core_tree_and_search_index.py`) 등이 혼재됨.
- **가독성 저하**: `.gitignore`, `.env` 등 핵심 설정 파일들이 수십 개의 스크립트 사이에 묻혀 있음.

### 2.2. 08_expansion/ 폴더
- **버전 파편화**: `IA_AND_UX_SCENARIO_SPEC_V1`부터 `V8`까지 모든 중간 버전이 루트에 노출됨.
- **데이터와 문서의 혼재**: 정적 명세서(`MD`)와 동적 감사 데이터(`JSON`)가 한 폴더에 섞여 있어 '단일 진실 공급원(SSOT)' 확인이 지연됨.
- **오딧 결과물 적체**: `PAYLOAD_136_AUDIT_*` 등 특정 시점의 검증 결과물이 정리되지 않고 누적됨.

### 2.3. 기타 폴더
- `scripts/`: 기존에 존재하나 `weather_kakao.py` 1개만 포함되어 있어 제 역할을 수행하지 못함.
- `archive/`: 구버전 데이터는 존재하나, 기획 문서 및 스크립트 아카이빙 체계는 부재함.

---

## 3. 최적화 표준 안 (Proposed Standard Structure)

### 3.1. [STEP 1] 스크립트 계층화 (`/scripts/`)
루트의 스크립트를 기능별로 분류하여 격리함.
- `scripts/core/`: 마스터 풀 생성, 트리 구축, 검색 인덱스 재생성 등 핵심 빌드 로직.
- `scripts/triage/`: AI 기반 분류(Triage), 데이터 정제, 정밀 감사 스크립트.
- `scripts/mining/`: XWD 마이닝, 연관 데이터 추출, 외부 사전 연동 로직.
- `scripts/utils/`: 공통 유틸리티 및 일회성 패치 스크립트.

### 3.2. [STEP 2] 문서 및 데이터 재배치 (`/08_expansion/` 리팩토링)
- **`08_expansion/final_spec/`**: 최종 승인된 IA, UX 시나리오, 프로토콜만 보관 (SSOT).
- **`08_expansion/audit_reports/`**: 마이닝 및 분류 감사 결과 리포트(MD) 보관.
- **`08_expansion/raw_data/`**: 중간 과정의 JSON 데이터 보관.
- **`10_product_guide/`**: 개발자 및 사용자 최종 사용 가이드 (Release Ready).

### 3.3. [STEP 3] 아카이빙 강화 (`/archive/`)
- `archive/legacy_scripts/`: 더 이상 사용하지 않거나 참조용으로만 남겨둔 스크립트.
- `archive/historical_docs/`: `V1~V7` 등 최종본 이전의 명세서 및 보고서.
- `archive/audit_logs/`: 과거 완료된 배치 작업의 상세 JSON 로그.

---

## 4. 실행 계획 (Action Plan)

1. **[Phase 1] 즉시 격리 (Immediate Isolation)**
    - 루트의 모든 `.py` 파일을 `scripts/` 폴더로 이동 (기능별 분류).
    - `08_expansion/`의 `V1~V7` 문서들을 `archive/historical_docs/`로 이동.

2. **[Phase 2] 경로 정규화 (Path Normalization)**
    - 이동된 스크립트 내부의 상대 경로(Relative Path)를 새 구조에 맞게 일괄 수정.
    - `ORCHESTRATION_DASHBOARD.md` 및 `WORKBOARD` 내의 파일 참조 경로 갱신.

3. **[Phase 3] 정기 청소 자동화 (Hygiene Automation)**
    - 작업 종료된 `batch_inputs/`, `batch_runs/` 파일들을 자동으로 아카이빙하는 간단한 유틸리티 도입 검토.

---

## 5. 결론 (Conclusion)
위 구조를 적용할 경우, 루트 디렉토리는 90% 이상 슬림화되며, 작업자는 `scripts/`에서 로직을, `08_expansion/final_spec/`에서 기준을 명확히 찾을 수 있게 됨. 이는 프로젝트의 인지 부하를 줄이고 협업 효율을 극대화할 것으로 기대됨.
