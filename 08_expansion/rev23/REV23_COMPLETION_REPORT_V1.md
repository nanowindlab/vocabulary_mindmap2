# REV23 Completion Report V1

> Date: `2026-03-11`
> Scope: `V1-REV-23` 마스터 풀 3 Depth 전수 재분류 및 분할 산출물 생성 완료 보고

## 1. Final Classification Snapshot

- 마스터 풀 입력: `8,744`
  - `CORE 8,545`
  - `SYSTEM_CAND 54`
  - `CAT_CAND 145`
- 최종 3 Depth 재분류 결과:
  - `CORE 8,092`
  - `SYSTEM_CAND 73`
  - `CAT_CAND 578`
  - `EXCLUDED 1`

## 2. Split Outputs

- `09_app/public/data/APP_READY_SITUATIONS_TREE.json`: `4,541`
- `09_app/public/data/APP_READY_EXPRESSIONS_TREE.json`: `1,829`
- `09_app/public/data/APP_READY_BASICS_TREE.json`: `1,722`
- `09_app/public/data/APP_READY_SEARCH_INDEX.json`: `8,092`

합계 검증:

- `4,541 + 1,829 + 1,722 = 8,092`
- 통합 검색 인덱스도 `8,092`건으로 일치

## 3. Stats Schema Hydration

최종 split 파일 및 통합 검색 인덱스의 `stats`는 아래 스키마로 정리했다.

- `frequency`
- `rank`
- `round_count`
- `band`
- `level`

적용 결과:

- `band` 비-null: `6,727`
- `level` 분포:
  - `Beginner 1,563`
  - `Intermediate 2,883`
  - `Unrated 3,646`

운영 메모:

- `band`는 실측 TOPIK 통계가 있는 경우만 부여했다.
- 통계 부재 항목은 `frequency/rank/band = null` 원칙을 유지했다.
- `level`은 원본 grade를 우선 사용했고, 등급 정보가 안정적으로 복구되지 않는 항목은 `Unrated`로 남겼다.

## 4. Runtime State

- `rev23_3depth_checkpoint.json` 없음
- 실행 프로세스 없음
- live quarantine 없음
- archive quarantine만 보존

## 5. Output References

- `08_expansion/rev23/REV23_CORE_WITH_CATEGORY_V1.json`
- `08_expansion/rev23/REV23_SYSTEM_CANDIDATES_V1.json`
- `08_expansion/rev23/REV23_CATEGORY_CANDIDATES_V1.json`
- `08_expansion/rev23/REV23_EXCLUDED_V1.json`
- `08_expansion/rev23/REV23_PUBLISH_SUMMARY_V1.json`
- `08_expansion/rev23/triage_reports/rev23_3depth_latest_report.json`
