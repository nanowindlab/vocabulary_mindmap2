# Roadmap Status Tasklist V2

> Version: `V2`
> Date: `2026-03-09`
> Owner: `Codex`
> Basis: `NEXT_THREAD_HANDOFF_V3.md` snapshot dated `2026-03-09`
> Status: `active`

## 1. 목적

이 문서는 `NEXT_THREAD_HANDOFF_V3.md`를 바탕으로,
현재 프로젝트의 전체 로드맵, 현재 상태, 다음 실행 리스트를 한 번에 볼 수 있도록 정리한 운영 문서다.

운영 메모:

- 이 문서는 `roadmap / status summary` 문서다.
- 현재 마일스톤의 authoritative tasklist/todo는 `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md` 하나로 통합 관리한다.
- 별도 TODO 문서는 authoritative 문서로 두지 않는다.
- 현재 기준 문서:
- authoritative tasklist: `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md`
- roadmap summary: `08_expansion/ROADMAP_STATUS_TASKLIST_V2.md`
- next-thread handoff: `NEXT_THREAD_HANDOFF_V3.md`

## 2. 프로젝트 한 줄 정의

- 이 프로젝트는 `confirmed 283`을 고정 코어로 유지하면서, corpus와 dictionary source를 흡수해 한국어 학습용 마인드맵 / 상세패널 / 플래시카드 구조를 확장하는 작업이다.

## 2-1. 이번 마일스톤의 필수 범위

- scene core와 expression core 모두 실제 mindmap으로 동작해야 한다
- meta learning은 단순 리스트가 아니라 구조화된 탐색/상세 화면을 가져야 한다
- 뜻, 예문, provenance, TOPIK frequency/grade, cross-link, bridge 정보를 실제 UI에 연결해야 한다
- `/05_source/raw_dictionary/한국어 어휘사전(영어판)_사전.json`의 주요 정보는 projection에 반영해야 한다
- corpus 9개 table의 정보는 projection 설계와 상세 화면에 활용돼야 한다
- 플립카드 학습 흐름이 제품 경험 안에 포함돼야 한다
- `PRODUCT_USER_SCENARIOS_V1.md`를 core / expression / meta / flipcard까지 확장해 충족해야 한다
- 이번 범위에서는 `visual_material`은 우선 제외한다

## 3. 고정 원칙

- `06_normalized_lexicon/01_canonical/NORMALIZED_LEXICON_CONFIRMED_283_V1.json` 직접 수정 금지
- `scene core` 유지
- `navigation grouping`은 user-facing grouping이며 center replacement가 아님
- `meta/detail leakage`는 core tree로 새지 않게 유지
- user-facing 구조는 `3단계 인지 구조` 우선
- `expression_core_candidate`는 아직 candidate로 관리

## 4. 현재 상황 요약

### 4-1. 구조 상태

- `scene core`는 `대분류 -> 중분류 -> 단어` 기준의 3단계 구조로 정리됨
- `category/subcenter`는 navigation depth가 아니라 section title로 취급
- `expression core`는 별도 candidate 축으로 분리돼 있음
- 예외 큐는 별도 관리 중이며, 일부 재배치와 재판정이 이미 반영됨

### 4-2. 현재 수치

- original core payload: `993 items / 33 roots`
- latest runtime trees:
  - `Core Tree = 324`
  - `Expression Tree = 43`
  - `Meta Tree = 280`
- exception queue:
  - `Exception Queue = 934`

### 4-3. 확정된 판정

- P0 승인 12개는 scene core 반영 완료
- HOLD:
  - `지금` -> `expression_core_candidate`
  - `오후` -> `meta_learning`
- P1 최종 판정:
  - `도착` -> `scene_core`
  - `위치` -> `core_bridge`
  - `연습` -> `core_bridge`

### 4-4. Scene Core Correction Verification Status

- scene core physical cleanse는 accepted 상태다.
- expression/meta broad map도 accepted 상태다.
- related vocab reciprocity / center-profile policy / `root_id` / `chunk_id` completeness도 accepted 상태다.
- review basis:
  - `REVIEW_MEMO_PHYSICAL_CLEANSE_FINAL_V1.md`
  - `REVIEW_MEMO_BROAD_TREE_RESUME_V1.md`
  - `REVIEW_MEMO_BROAD_MAP_EXPANSION_V1.md`
  - `REVIEW_MEMO_DATA_HARDENING_FINAL_ACCEPTED_V1.md`
- 현재 남은 것은 broad map 존재 여부가 아니라 아래 안정화 항목이다:
  - `cross_links` actual population and quality
  - detail-field runtime preservation
  - remaining source-rich polish

## 5. 지금까지 확정된 것과 미확정인 것

### 확정된 것

- `scene core 유지`
- `navigation grouping`은 user-facing only
- `meta/detail leakage` 분리
- 3단계 사용자 인지 구조
- `expression_core_candidate` 별도 축 관리
- `expression_core_candidate`는 별도 운영, 필요 시에만 `core_bridge` 사용

### 아직 잠기지 않은 것

- stronger record-level linkage completeness
- `expression_core_candidate`의 실제 승격 범위
- UI가 최종적으로 어떤 payload를 source of truth로 볼지
- source 자료가 가진 뜻 / 예문 / provenance / TOPIK 정보 / bridge 정보의 실제 UI 연결 범위

## 6. 전체 로드맵

### Phase 1. Schema Contract Freeze

- term-level linkage 기준을 고정
- validator 실패 조건을 명문화
- artifact 간 필드 정의를 동일 기준으로 맞춤

### Phase 2. Validator First Pass

- `scene core`, `expression_core_candidate`, `exception queue`를 한 번에 검사
- failed record를 유형별로 분리
- payload 문제 / 분류표 문제 / route 문제를 구분

### Phase 3. Payload Correction and Regeneration

- validator 결과를 반영해 payload 보정
- 필요한 경우 regenerated payload 재생성
- 검증 재통과 여부 확인

### Phase 4. Promotion and Reclassification Decision

- `expression_core_candidate` 승격 가능 범위 검토
- `exception queue` 재분류 여부 검토
- `core_bridge`와 `expression_core_candidate` 경계 재확인

### Phase 5. UI Source-of-Truth Lock

- 개발팀이 소비할 최종 payload를 확정
- UI가 구조를 다시 임의 해석하지 않도록 계약 고정

### Phase 6. UI Implementation and Review

- Antigravity가 확정 payload 기준으로 구현
- Review Gemini가 구조 / 배치 / 승격 / UX를 검수
- 최종 acceptance decision 수행

### Phase 7. Source-Rich Projection and Detail UX

- core / meta / expression이 source 자료의 의미 정보를 실제로 소비하도록 projection 확장
- 뜻, 예문, provenance, TOPIK frequency/grade, bridge target을 화면에 연결
- meta / expression 전용 detail view와 분류 구조 정리
- 시나리오 3용 TOPIK 빈도 탐색 화면과 시나리오 4용 예문 문체 비교 UI를 별도 구현 단위로 분리
- 플립카드 학습 상태 저장 로직을 포함한 학습 흐름 완성
- expression core 전용 시각화 레이아웃 전략 확정
- corpus 예문 난이도 필터링과 dictionary/corpus 예문 노출 우선순위 정책 확정
- 탐색 컨텍스트 기반 플립카드 deck 생성 로직 확정
- 현재 단계의 플립카드는 `이전/다음` 탐색형으로 고정하고, `알아요/몰라요` 및 계정 기반 학습 진척 관리는 다음 프로젝트 단계 후보로 분리
- 플립카드 카드 풀은 scene core / expression core의 정제된 complete-data 단어로 제한
- 플립카드 대표 예문 / chunk hydration 데이터는 runtime manifest에 직접 공급
- storage adapter 기반 학습 상태 persistence 구조 확정
- 학습자용 UI 레이블 / 문체 용어 / 메타 학습 그룹의 영어 매핑 규칙 확정
- dictionary / corpus 조인 시 동음이의어 분리(disambiguation) 전략 확정
- core / expression / meta를 가로지르는 검색 UI와 검색 결과 deck 연결 전략 확정
- source-rich UI에 대해 재검수 수행

## 7. 지금 가장 중요한 우선순위 (현재 상태: 완료 임박)

현재 우선순위는 아래 순서다.

1. 영어 정의 제어 및 검색 UX 고도화 (Next Goal)
2. final UX hardening and scenario walkthrough
3. review / release readiness
4. remaining source-rich polish

즉, 현재 기준으로는 `broad map acceptance 이후 cross-link + runtime integrity hardening`이 다음 우선순위다.

## 8. 바로 해야 할 일 리스트

### A. Source-Rich Projection Audit

- 현재 core / meta / expression이 각각 어떤 source 정보를 실제로 갖고 있는지 점검
- detail, examples, provenance, grade, bridge_targets, cross_links 노출 범위를 표로 정리
- 앱이 실제로 소비 가능한 필드와 미연결 필드를 구분
- dictionary / corpus 조인 시 homonym / sense collision 위험 레코드 목록화
- 학습자가 이해하지 못할 수 있는 UI 레이블 / 문체 용어 목록화
- `09_app_v2/public/data`와 현재 앱 런타임 로더가 실제로 소비하는 payload/chunk 기준으로 재검증
- `visual_material`은 이번 audit 표와 구현 범위에서 제외
- `APP_READY...`에 없는 필드는 `source 부재`가 아니라 `미투영`인지 먼저 분리
- `related_vocab`와 corpus inventory 예문은 적극 활용 대상으로 본다
- corpus 9개 table은 실제 추출본을 `05_source` 하위 snapshot으로 보관하고 projection 입력으로 사용

### B. Projection Regeneration

- meta / expression 전용 projection 또는 manifest 확장
- core detail chunk와의 연결 규칙 재정리
- TOPIK provenance / frequency를 UI용 필드로 정규화
- corpus 예문 난이도 / source type / 노출 우선순위 필드를 projection에 포함
- homonym disambiguation key와 source join rule을 projection 계약에 포함
- learner-facing localization label 세트를 projection 또는 app contract에 포함
- dictionary `related_vocab`를 detail / 추천 탐색 / bridge 후보에 반영
- corpus inventory 예문을 learner example과 구분된 source example layer로 반영
- provenance `top_sources` / `detailed_frequency`와 chunk sharding 규칙까지 포함

### C. UI 연결 작업

- meta learning 전용 detail view 연결
- expression core 전용 detail / grouping UI 연결
- bridge target / cross-link / fallback state 정리
- TOPIK 빈도 탐색 전용 리스트 / 구간 뷰 구현
- 예문 문체 비교 전용 탭 / 필터 UI 구현
- 현재 탐색 컨텍스트 기반 deck 생성 및 진입 흐름 연결
- 현재 단계 플립카드 조작을 `이전/다음` 중심으로 정리하고, 추후 학습 상태형 플로우는 별도 단계로 분리
- scene core / expression core에서 `리스트 보기 / 플립카드 보기` mode 선택 UI 추가
- detail panel의 current surface/context 명확화와 same-sense 중복 chip 제거
- 전역 검색 바 / 검색 결과 패널 / 결과에서 detail 및 flipcard 진입 구현
- learner-facing 영어 보조 라벨 / 설명 UI 적용
- attested sentence와 provenance 정보를 실제로 이해 가능한 방식으로 노출

### D. Information Design 정리

- expression 분류 체계 정리
- meta 표시 라벨을 사용자 친화적으로 정리
- source-derived grade / rank / provenance 표시 규칙 정리
- expression core의 시각화 전략을 트리 / 버블 / 하이브리드 중 하나로 명시
- 플립카드 학습 상태 표시 규칙 정리
- dictionary 예문과 corpus 예문의 기본 노출 순서와 난이도 필터 규칙 명시
- 문체명(`합쇼체`, `해요체`, `해라체`)과 메타 그룹의 learner-facing 영어/설명 표기 규칙 명시
- 검색 결과에서 homonym이 충돌할 때 사용자에게 구분해 보여주는 규칙 명시

### E. Source-Rich Review

- 구현 결과가 실제 source 정보를 충분히 노출하는지 검수
- core / meta / expression 간 정보 밀도 차이를 점검
- 남은 미연결 source 정보 목록 정리
- attested sentence 적절성과 provenance 품질, chunk 분리 전략을 별도 점검

## 9. 역할별 다음 액션

### Gemini

- source-rich projection audit
- meta / expression / detail projection 확장안 작성
- UI용 필드 정규화안 생성
- localization label 세트와 homonym disambiguation 규칙안 생성

### Antigravity

- source-rich projection 수령 후 detail / provenance / bridge UI 구현
- meta / expression 전용 detail UX 구현
- learner-facing localization과 검색 UI 구현

### Review Gemini

- source-rich UI 구현 검수
- verdict는 `ACCEPT`, `PARTIAL_ACCEPT`, `REJECT` 중 하나로 고정
- 외국인 학습자 관점에서 라벨 이해도와 검색/동음이의어 구분 UX 검수

## 10. 완료 기준

아래가 충족돼야 다음 단계로 넘어간다.

- 세 artifact가 같은 linkage 기준으로 검사됨
- failed type이 유형별로 정리됨
- payload 보정 또는 분류표 수정 필요 지점이 구분됨
- `expression_core_candidate` 처리 원칙이 재판정됨
- UI source-of-truth가 확정됨
- source 자료의 뜻 / 예문 / provenance / grade / bridge 정보가 실제 UI에 연결됨
- 학습자용 영어 매핑 / homonym 구분 / 검색 UX가 실제 제품 흐름에 연결됨

## 11. 참조 문서

- `NEXT_THREAD_HANDOFF_V3.md`
- `PRODUCT_USER_SCENARIOS_V1.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md`
- `08_expansion/SCHEMA_LINKAGE_VALIDATION_PLAN_V1.md`
- `08_expansion/THREE_LEVEL_RESTRUCTURE_TASKLIST_V1.md`
- `08_expansion/THREE_LEVEL_CLASSIFICATION_TABLE_V1.md`
- `08_expansion/THREE_LEVEL_CORE_PAYLOAD_V1.json`
- `08_expansion/EXCEPTION_QUEUE_V1.json`
- `08_expansion/EXPRESSION_CORE_CANDIDATES_V1.json`
