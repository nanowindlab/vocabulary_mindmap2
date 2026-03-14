# Next Thread Handoff V3

> Version: `V3`
> Date: `2026-03-09`
> Owner: `Codex`
> Status: `active handoff`

아래를 그대로 다음 스레드 시작문으로 쓰면 됩니다. 이번 버전은 Gemini가 source-rich projection, Antigravity UI, Review Gemini 검수를 현재 상태 그대로 이어받도록 정리한 최신 handoff입니다.

중요:

- `NEXT_THREAD_HANDOFF_V3.md`를 다음 스레드의 최신 handoff entry point로 사용한다.
- `NEXT_THREAD_HANDOFF_V1.md`, `NEXT_THREAD_HANDOFF_V2.md`는 과거 snapshot이며 새 handoff source로 보지 않는다.
- 에이전트 명칭:
  - `Gemini CLI` = `데이터 검증 에이전트`
  - `Antigravity` = `개발 에이전트`
  - `Review Gemini` = `리뷰 에이전트`
- 모든 에이전트 지시는 `Self-Refine prompt / Iterative Prompting / Reflection Pattern` 방식으로 준다.
- working agent 완료 후에는 same workboard를 review agent에게 넘기고, review agent는 same workboard에 review를 추가한다.
- 사용자가 Codex에게 돌아올 때는 working workboard 하나에 작업 보고 + 리뷰 보고가 함께 들어 있는 상태를 기본으로 한다.
- 관리자와 에이전트는 사용자에게 채팅으로도 간결하고 정확한 상태 보고를 남긴다.

현재 handoff 규칙:

- 기본 전달 문서는 항상 `working workboard` 하나다.
- 현재 기본 handoff 대상은 [DEVELOPMENT_AGENT_WORKBOARD_V1.md](../.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md)다. (`.codex-orchestration` legacy 경로는 현재 사용하지 않음)
- 작업 완료 후 same workboard를 리뷰 에이전트에게 넘기고, 리뷰 에이전트는 same workboard의 `Latest Review`를 채운다.

## 1. 현재 프로젝트의 실제 초점

- 이 프로젝트의 현재 핵심은 `source 자료가 이미 가지고 있는 정보`를 실제 payload와 UI에 끝까지 연결하는 것이다.
- 현재 문제는 source 부족이 아니라 `기존 source 미활용`이 크다.
- 특히 core는 일부 상세 강화가 시작됐지만, `meta learning`, `expression core`, `mindmap UI`, `flipcard`, `search`, `frequency band`, `homonym disambiguation`은 아직 미완료다.

## 2. 가장 먼저 읽을 문서

### 입구 / 운영

- `.gemini-orchestration/archive/WORK_ORCHESTRATION_HUB_RESTART_LEGACY_V1.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/REVIEW_AGENT_WORKBOARD_V1.md`

### 로드맵 / 태스크

- `08_expansion/ROADMAP_STATUS_TASKLIST_V2.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md`

중요:

- `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md`가 현재 마일스톤의 `단일 authoritative tasklist/todo`다.
- 다른 임시 todo를 따로 만들지 말고 여기만 갱신한다.
- 별도 TODO 문서는 authoritative 문서로 유지하지 않는다.

### 제품 / UX 기준

- `PRODUCT_USER_SCENARIOS_V1.md`
- `08_expansion/WEB_MINDMAP_NAVIGATION_SPEC_V1.md`
- `PRODUCT_DIRECTION_V1.md`

### source / data 기준

- `05_source/raw_dictionary/한국어 어휘사전(영어판)_사전.json`
- `90_validation/corpus_db_inventory_v1/SCHEMA_AND_COUNTS_V1.md`
- `05_source/extracted_corpus/snapshot_20260309/SNAPSHOT_MANIFEST_V1.md`
- `08_expansion/ENGLISH_MAPPING_INVENTORY_V1.json`
- `08_expansion/SOURCE_RICH_PROJECTION_AUDIT_V1.md`
- `08_expansion/PROJECTION_BUILDER_REFACTOR_REPORT_V1.md`

## 3. 현재 상태 요약

### 이미 된 것

- corpus 9개 table snapshot 추출 완료
- source-rich projection builder enrichment 및 후속 보정 진행
- core detail에는 일부 source-rich 필드가 실제 주입됨
  - `phonetic_romanization`
  - `stats.total_frequency / source_count / round_count`
  - `qr_code_url`
  - `attested_sentences`
  - `related_vocab`
- `def_ko` 주입 완료
- expression search coverage mismatch 수정 완료
- flipcard hydration용 runtime manifest 보강(`chunk_id` / 대표 예문) 완료
- search index 생성 및 expression coverage 정리 완료
- core / meta / expression detail panel은 일부 확장 완료
- `08_expansion/MINDMAP_UI_SPEC_DRAFT_V1.md` 초안 작성 완료
- `08_expansion/MINDMAP_UI_SPEC_DRAFT_V2.md` review 반영본 작성 완료
- `08_expansion/MINDMAP_UI_SPEC_LOCK_V1.md` final spec lock 완료
- non-tree UI 확장 구현 완료:
  - 영어 helper label
  - search result density
  - related vocab 탐색 연결
  - top sources 표시
  - meta / expression split detail panel
  - flipcard modal / hydration / previous-next policy
  - list / flipcard mode switch
- scene core physical cleanse accepted
- scene core broad tree / mindmap accepted
- expression/meta broad map accepted
- related vocab reciprocity / center-profile policy / `root_id` / `chunk_id` completeness accepted
- same-workboard review handoff process adopted

### 아직 안 된 것

- `cross_links`는 core에만 실데이터가 일부 들어 있고 expression/meta는 여전히 빈 경우가 많다
- 예문 / romanization / provenance의 실제 런타임 보존은 최근 수정 반영 후 재검수가 필요하다
- `top_sources` / provenance 품질 고도화는 여전히 과제다
- chunk sharding 운영 검증은 남아 있다
- 플립카드 장기 정책(`알아요/몰라요`, 학습 상태형 흐름)은 다음 단계 과제다
- `romanization` 표기법 검증은 미완료다
- `cross_links`는 대부분 `legacy` 기반이라 실질 탐색 연결 품질 검토가 더 필요하다

### Acceptance Snapshot

- accepted:
  - `REVIEW_MEMO_PHYSICAL_CLEANSE_FINAL_V1.md`
  - `REVIEW_MEMO_BROAD_TREE_RESUME_V1.md`
  - `REVIEW_MEMO_BROAD_MAP_EXPANSION_V1.md`
  - `REVIEW_MEMO_DATA_HARDENING_FINAL_ACCEPTED_V1.md`
- still open:
  - cross-link quality / actual population across all surfaces
  - detail-field runtime preservation re-check
  - final UX hardening and scenario walkthrough

## 4. 이번 스레드에서 잊지 말아야 할 사용자 요구

다음은 현재 tasklist에 반드시 반영되어 있어야 하는 항목들이다.

1. 단어 뜻은 core / meta / expression 어디서든 실제로 연결되어야 한다.
2. `related_vocab`가 있으면 빈 표시가 아니라 실제 탐색에 활용돼야 한다.
3. `romanization` 누락 단어는 보충해야 한다.
4. `romanization` 표기법 자체를 검증해야 한다.
5. 출현 예문의 출처는 정책화 대상이지만, `세종한국어` 표기는 사용하지 않는다.
6. 빈도/출처/등장 회차는 나중에 숨길 수 있게 하고, `frequency band 1~5`를 설계한다.
7. `nuri.iksi.or.kr` 링크는 제거 대상이다.
8. TOPIK 실제 예문과 learner example(합쇼체/해요체/해라체 등 6개)을 가능한 한 많이 활용한다.
9. 장기적으로 모든 단어는 필요한 필드를 가진 schema-complete 상태를 목표로 한다.
10. `문화와 명절` 같은 분류 누락 구간을 보정해야 한다.
11. 단어 리스트가 아니라 실제 `mindmap`이 보여야 한다.
12. 플립카드 위치/방식도 UI spec에 포함해야 한다.
13. expression core도 scene core처럼 실제 탐색 구조를 가져야 한다.
14. meta learning map의 정의를 명확히 해야 한다.
15. scene core의 잘못된 분류 / 중복 분기 / meta leakage는 broad tree UI 구현 전에 교정해야 한다.
16. 플립카드는 현재 단계에서 `이전/다음` 중심으로 두고, `알아요/몰라요`와 계정 기반 학습 관리는 다음 단계로 분리한다.
17. 플립카드 카드 풀은 scene core / expression core의 정제된 complete-data 단어로 제한한다.

## 5. 현재 authoritative tasklist에서 중요한 트랙

문서:

- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md`

핵심 트랙:

- `Track A`: source audit / extraction
- `Track B`: projection / contract
- `Track C`: IA / UX
- `Track D`: implementation
- `Track E`: review / acceptance

이번 스레드에서 특히 중요한 미완료 항목:

- `D38` `cross_links` source-rich population
- `D39` detail-field runtime integrity hardening
- `D35 / E20` detail panel context / same-sense clarity
- `B17 / E10` provenance quality
- `D32 / D33 / E14 / E19` 플립카드 현재 단계 UX / 카드 풀

## 6. 에이전트 상태와 다음 순서

### Gemini CLI (`데이터 검증 에이전트`)

현재 역할:

- payload / projection hardening
- cross-links / detail completeness

현재 남은 핵심:

- `cross_links` actual population and quality
- `top_sources` / provenance 고도화
- chunk sharding 운영 검증
- romanization completeness / notation rule

### Antigravity (`개발 에이전트`)

현재 역할:

- accepted broad map 기반 UX hardening

현재 남은 핵심:

- cross-link 시각화의 실제 UX 연결
- 예문 / romanization / related vocab / center-profile의 실제 런타임 확인
- flipcard 현재 단계 정책 반영 마감
- scene / expression / meta 최종 UX polish

### Review Gemini (`리뷰 에이전트`)

현재 역할:

- review-only
- 비판적 관점
- 외국인 학습자 관점 + 3 expert lenses

## 7. 마인드맵 UI/spec 작업 순서

이건 구현 전에 순서를 지켜야 한다.

1. `Review Gemini`가 `08_expansion/MINDMAP_UI_SPEC_DRAFT_V1.md`를 비판적으로 검토
2. `Codex`가 `08_expansion/MINDMAP_UI_SPEC_DRAFT_V2.md`로 반영
3. `Antigravity`가 구현 가능성과 UI 제약 관점에서 피드백
4. `Codex`가 `08_expansion/MINDMAP_UI_SPEC_LOCK_V1.md`로 최종 spec을 잠금
5. 그 다음 payload blocker 해결
6. 그 뒤 구현

중요:

- `Gemini CLI가 지금 대상`이라는 말은 `payload 보강 트랙` 기준이다.
- `mindmap UI/spec 플로우` 기준으로는 spec lock이 끝났고, 지금 다음 순서는 `Gemini CLI`의 payload blocker 해결이다.
- 즉, `어느 트랙을 진행 중인지`에 따라 다음 에이전트가 달라진다.

## 8. 현재 추천 작업 순서

1. authoritative tasklist 기준으로 열린 항목 재확인
2. `DEVELOPMENT_AGENT_WORKBOARD_V1.md`를 working handoff 문서로 사용해 cross-link / final UX hardening 진행
3. 완료되면 same workboard를 리뷰 에이전트에게 전달
4. review verdict가 same workboard에 붙은 뒤 Codex가 검증

중요:

- authoritative tasklist는 `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V2.md` 하나만 본다.
- working agent와 review agent의 보고는 same working workboard에 함께 남긴다.
- 다음 회차도 `verified / unverified / contradicted` 방식으로 보고하고 검증한다.
- 리뷰 에이전트를 적극 활용한다. 핵심 구현 보고와 핵심 데이터 검증 보고는 가능하면 먼저 리뷰 에이전트 검수를 거친다.

## 9. 추가 메모

- `visual_material`은 현재 범위에서 제외
- 보고를 검토할 때는 장점보다 `누락`, `약한 가정`, `개선점`을 먼저 본다
- 보고 확인만 하지 말고, 실제 파일 / JSON / build 결과까지 직접 검증해야 한다
- 다음 단계가 자연스럽게 정해지면, 사용자 승인 대기 없이 에이전트 작업을 바로 이어가고 사용자에게는 짧게 보고한다
- `multi-agent orchestration` 기준으로 계속 운영한다
