# 2026-03-14 PRE-REV83 Execution Method Survey Report

## 1. Method (Edge 중복 투영 및 기존 데이터 충돌)
- **우려사항**: REV-83에서 Core 12 대상 2차 Edge 확장 시, 생성된 Edge가 기존 `APP_READY_SEARCH_INDEX.json`의 식별 불가능한 문자열 배열(`related_vocab`, `cross_links`) 데이터와 중복되어 런타임에 이중 투영될 위험이 있음.
- **대안**: Edge 생성 시 기존 live 데이터의 존재 여부를 대조하여, 중복을 배제하거나 덮어쓰기 방식을 명확히 하는 필터링 로직 도입.
- **추천안**: 실행 Method에 '기존 데이터 교집합 대조 및 중복 Edge 생성 차단(Deduplication) 로직' 필수 포함.

## 2. Order (Holdout 무결성 검증 시점)
- **우려사항**: 확장된 Edge를 검토 없이 Projection 준비 단계로 넘길 경우, Holdout 4 노드에 의도치 않은 Edge가 병합되는 Failure Mode 발생 가능.
- **대안**: 생성(Generation) 단계와 투영(Projection) 준비 단계 사이에 격리 상태를 확인하는 강제 검증 게이트 삽입.
- **추천안**: 작업 순서를 `[1] Edge 확장` ➔ `[2] Holdout 4 Edge 개수 0 확인(Gate)` ➔ `[3] Projection Preview`로 엄격히 분리 고정.

## 3. Validation Point (양방향 대칭성 및 스키마 완전성)
- **우려사항**: 편향된 Edge 확장으로 인해 `target -> source` 역방향 Edge가 누락되거나, `jump_purpose`, `display_intent` 등 Required Field 가 누락될 우려.
- **대안**: 파일 저장 전 `RELATION_GRAPH_CANONICAL_V1.json`의 `required_edge_fields` 누락 여부 및 양방향 쌍(Reciprocal Pair) 존재 여부를 기계적으로 검사.
- **추천안**: Acceptance Criteria에 '확장 Edge의 양방향 대칭률 100%' 및 '필수 Field(schema_mode: rich_internal_canonical) 완전성 만족' 항목 명시.
