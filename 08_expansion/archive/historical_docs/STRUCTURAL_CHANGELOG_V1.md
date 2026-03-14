# [X-CLEAN] 프로젝트 구조 변경 및 파일 이동 이력 (Changelog)

> **안내**: 프로젝트의 장기적인 유지보수와 배포 안정성을 위해(V1-REV-60 합의 기반), 구버전 문서들과 일시적 감사 로그들을 전용 아카이브 폴더로 이동시켰습니다. 
> 파일이 보이지 않는다면 아래의 이동 경로를 확인해 주십시오.

## 1. 아카이빙 폴더 신설
- `08_expansion/archive/historical_docs/`: 구버전 기획서, 명세서, 과거 태스크리스트 보관.
- `08_expansion/archive/audit_logs/`: 과거 완료된 1회성 데이터 감사(Audit) 결과 및 리뷰 메모 보관.

## 2. 파일 이동 내역 (Mapping Table)

| 기존 파일명 (Old Location: `08_expansion/`) | 이동된 위치 (New Location) | 비고 |
| :--- | :--- | :--- |
| `IA_AND_UX_SCENARIO_SPEC_V1~V7.md` | `archive/historical_docs/` | 최신 **V8**만 원본 위치에 유지 |
| `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V3~V4.md` | `archive/historical_docs/` | 최신 **V9**만 원본 위치에 유지 |
| `VOCAB_LEVEL_BAND_DEFINITION_V1~V2.md` | `archive/historical_docs/` | 최신 **V3**만 원본 위치에 유지 |
| `STRICT_DATA_CLASSIFICATION_PROTOCOL_V1.md` | `archive/historical_docs/` | 최신 **V2**만 원본 위치에 유지 |
| `REVIEW_MEMO_*.md` (전체) | `archive/audit_logs/` | 과거 리뷰 로그 |
| `PAYLOAD_136_*.md/json` (전체) | `archive/audit_logs/` | 초기 136개 샘플 감사 로그 |
| `ABSTRACT_ROOT_BOUNDARY_PRIORITY_AUDIT_V1.md` | `archive/audit_logs/` | V19 감사 완료 건 |
| `FULL_INVENTORY_AUDIT_COMPLETION_V1.md` | `archive/audit_logs/` | 재분류 완료 감사 건 |

## 3. 에이전트 지침 (Agent Guidelines)
- **기획/리뷰 에이전트**: 과거의 맥락(왜 이렇게 바뀌었는가?)을 파악해야 할 경우에만 `archive/` 폴더를 참조하십시오.
- **데이터/개발 에이전트**: 빌드 및 개발 시에는 절대 `archive/` 폴더 내의 문서를 참조 지점으로 삼지 마십시오. 오직 `08_expansion/` 최상단에 있는 최신 버전(V)만 SSOT로 간주하십시오.

## 4. scripts/ 폴더 신설 및 루트 스크립트 격리

- `scripts/core/`: 빌드, 재구축, 파서, 추출, 감사 등 프로젝트 데이터 조립용 핵심 스크립트.
- `scripts/mining/`: 관계 마이닝, 배치 마이닝, 모니터링 등 장시간 탐색/발굴 계열 스크립트.
- `scripts/triage/`: LLM triage, augmentation, 3-depth 재분류 등 분류 파이프라인 스크립트.
- `scripts/legacy/`: 현재 canonical 흐름에서는 직접 쓰지 않지만, 과거 실험/변환 참고용으로 남겨둔 구형 스크립트.

## 5. 루트 → scripts/ 이동 내역 (Mapping Table)

| 기존 파일명 (Old Location: `/`) | 이동된 위치 (New Location) | 비고 |
| :--- | :--- | :--- |
| `build_inventory_ledger.py` | `scripts/core/` | inventory ledger 생성 |
| `build_master_pool_v1.py` | `scripts/core/` | REV-23 마스터 풀 생성 |
| `build_new_tree.py` | `scripts/core/` | V1 legacy tree/search 생성 |
| `check_missing_words.py` | `scripts/core/` | raw dictionary 누락 탐지 |
| `classify_and_hydrate.py` | `scripts/core/` | 구형 hydration 참고 스크립트 |
| `data_optimizer.py` | `scripts/core/` | 구형 chunk 분할 스크립트 |
| `extract_missing_raw_dictionary_candidates.py` | `scripts/core/` | REV-21 augmentation 후보 추출 |
| `parse_3depth_category_dictionary.py` | `scripts/core/` | 3 Depth 사전 JSON화 |
| `parse_xwd_framework.py` | `scripts/core/` | XWD 훅 사전 JSON화 |
| `prepare_inventory_batch.py` | `scripts/core/` | inventory batch 입력 생성 |
| `rebuild_core_tree_and_search_index.py` | `scripts/core/` | legacy core tree/search 재구축 |
| `rebuild_rev23_detail_chunks.py` | `scripts/core/` | REV-42 detail chunk 재생성 |
| `run_inventory_audit.py` | `scripts/core/` | inventory audit 실행 |
| `gemini_batch_refiner.py` | `scripts/mining/` | batch refiner |
| `run_gemini_batch.py` | `scripts/mining/` | 배치 실행 유틸리티 |
| `run_rev47_xwd_mining.py` | `scripts/mining/` | REV-47 XWD 전수 마이닝 |
| `monitor_rev47.py` | `scripts/mining/` | REV-47 3분 감시/재시작/마감 자동화 |
| `llm_data_triage.py` | `scripts/triage/` | 메인 triage 엔진 |
| `run_missing_raw_dictionary_augmentation.py` | `scripts/triage/` | REV-21 augmentation triage |
| `run_rev23_3depth_triage.py` | `scripts/triage/` | REV-23 3 Depth triage |
| `enhance_english.py` 외 legacy 변환 스크립트 | `scripts/legacy/` | 직접 runtime source로 쓰지 않음 |

## 6. 09_app/public/data 폴더 역할 분리

- `09_app/public/data/live/`: 프론트엔드가 실제 fetch하는 runtime canonical 파일.
- `09_app/public/data/internal/`: rebuild와 검증에 쓰는 내부 지원 파일.
- `09_app/public/data/legacy/`: 구세대 산출물. 비교/복구/회귀 확인용.
- `09_app/public/data/archive/`: obsolete backup 및 retired chunk 보관.

## 7. data/ 하위 폴더 성격 (Folder Roles)

| 폴더 | 역할 | 포함 예시 |
| :--- | :--- | :--- |
| `live/` | 앱 runtime canonical | `APP_READY_SITUATIONS_TREE.json`, `APP_READY_EXPRESSIONS_TREE.json`, `APP_READY_BASICS_TREE.json`, `APP_READY_SEARCH_INDEX.json`, `CHUNK_MANIFEST_V1.json`, `APP_READY_CHUNK_RICH_*`, `APP_READY_CHUNK_EXAMPLES_*`, `ENGLISH_MAPPING_INVENTORY_V1.json` |
| `internal/` | 재생성/검증 보조 | `APP_READY_CORE_PAYLOAD_V1.json`, `APP_READY_PROJECTION_V2_DETAIL_LITE.json`, `APP_READY_SCHEMA_COMPLETE_V1.json` |
| `legacy/` | 구버전 비교/복구 참조 | `APP_READY_CORE_TREE_V1.json`, `APP_READY_META_TREE_V1.json`, `APP_READY_EXPRESSION_TREE_V1.json`, `APP_READY_SEARCH_INDEX_V1.json`, `APP_READY_SEARCH_INDEX_V2.json`, `APP_READY_MAPPING_V1.json`, `APP_READY_MAPPING_V2.json`, `APP_READY_SCHEMA_COMPLETE_V2.json` |
| `archive/` | 완전 보관용 | `.bak`, 구형 `chunks/` 디렉토리 |

## 8. 에이전트 지침 추가 (Updated Guidelines)

- **데이터/개발 에이전트**: 현재 앱이 읽는 JSON은 반드시 `09_app/public/data/live/`를 기준으로 보십시오.
- **legacy 참조 규칙**: `legacy/`는 비교/복구 참고용이며, runtime fetch path로 직접 쓰지 않습니다.
- **internal 참조 규칙**: `internal/`은 rebuild source로만 사용하고 UI loader 경로에 직접 연결하지 않습니다.
- **archive 참조 규칙**: `archive/`는 보관 목적이므로 일반적인 빌드/검증 경로에서 제외합니다.

> **작성일**: 2026-03-11
> **주체**: Gemini Orchestrator (Manager Approved)
