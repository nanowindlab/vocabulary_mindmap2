# Green Batch Autopilot Trial Report: Batch-11

## 1. 개요
- **배치명:** Calendar Label Batch-11
- **유형:** Type A (Coverage Expansion)
- **등급:** Green (Validated Template)
- **일시:** 2026-03-15 15:40
- **상태:** 완료 (SUCCESS)

## 2. 작업 단계별 결과

### 2.1 Projection Gate Final Check
- **대상:** `08_expansion/batch_runs/BATCH_011M_validated.json` (31 ids)
- **검증 내용:** SDCP V2 준수 여부 및 Holdout 침범 확인
- **결과:** **PASS** (모두 가이드라인 준수)

### 2.2 Publish-only (Runtime Projection)
- **반영 파일:** 
    - `APP_READY_SITUATIONS_TREE.json` (+23 ids)
    - `APP_READY_EXPRESSIONS_TREE.json` (+1 id)
    - `APP_READY_BASICS_TREE.json` (+7 ids)
    - `APP_READY_SEARCH_INDEX.json` (+31 ids)
- **결과:** **SUCCESS**

### 2.3 Actual Bucket Verification
- **검증 항목:** 파일별 항목 개수 정합성
- **결과:** **MATCH**
    - SITUATIONS: 4,564
    - EXPRESSIONS: 1,830
    - BASICS: 1,729
    - SEARCH_INDEX: 8,123 (Total consistent)

### 2.4 Chunk Rebuild
- **반영 파일:**
    - `APP_READY_CHUNK_RICH_chunk_021.json` (+31 entries)
    - `APP_READY_CHUNK_EXAMPLES_chunk_021.json` (+31 entries, empty sentences)
- **결과:** **SUCCESS**

### 2.5 Consistency Check
- **검증 항목:** Search/Tree/Chunk 3자 정합성
- **결과:** **PASS** (31 ids 전수 대조 완료)

## 3. 중단 규칙 (Stop Rules) 확인
- Validated contract 위반: 없음
- Holdout/reserve invariants 위반: 없음
- 데이터 유실 또는 깨짐: 없음 (SITUATIONS 누락 발생 후 즉시 교정 완료)

## 4. 특이사항
- SITUATIONS 트리 반영 중 15개 항목이 누락되는 현상 발생하였으나, `replace` 정밀 재실행을 통해 4,564건으로 정상 복구 완료함.
- 향후 대량 데이터 `replace` 시 분할 삽입 권고.

## 5. 최종 판정
**GREEN - ACCEPTABLE**
런타임에 즉시 노출 가능한 상태임.
