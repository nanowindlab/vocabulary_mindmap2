# Gemini Orchestration Hub V1 (RESTART MODE)

> Version: `V1-RESTART`
> Date: `2026-03-10`
> Owner: `Gemini Orchestrator (Manager)`
> Mode: `RESTART - Fragmented Artifact Recovery & Rebuilding`

## 1. Project Reset Notice (CRITICAL)

- 이 프로젝트는 이전 에이전트(Codex/Gemini)의 오케스트레이션 실패와 데이터 오염으로 인해 **완전 재시작(Reset)**되었습니다.
- 워크보드 상의 이전 `Revision 1~22` 및 `ACCEPT` 기록은 실제 파일과 일치하지 않는 파편화된 기록이므로 신뢰하지 않습니다.
- 모든 작업은 `05_source`의 원본 데이터를 기반으로 `08_expansion`에서 새로 정의하고, `09_app`에서 다시 구현합니다.
- `_v2` 접미사가 붙은 폴더는 오염된 히스토리 참고용으로만 사용합니다.

## 2. Updated Principles

- **Source Integrity First:** `05_source`만이 유일한 진실의 원천(Source of Truth)이다.
- **Incremental Expansion:** `08_expansion`에서 데이터 구조를 다시 정의하고, `08_expansion_v2`는 참고만 하되 그대로 복사하지 않는다.
- **Clean Implementation:** `09_app`은 보일러플레이트부터 새로 작성하며, `09_app_v2`의 오염된 코드는 로직 참고용으로만 사용한다.
- **Strict Verification:** 워크보드의 "장부상 완료"가 아닌, 실제 동작하는 `09_app`과 검증된 `08_expansion` 산출물만 "완료"로 인정한다.
- **Simplified Tracking:** 불필요한 과거 히스토리는 남기되, 현재 작업은 `Revision 1 (Restart)`부터 다시 시작한다.

## 2. Guardrails

- `06_normalized_lexicon/01_canonical/NORMALIZED_LEXICON_CONFIRMED_283_V1.json` 직접 수정 금지
- `scene core` 유지
- `navigation grouping`은 user-facing grouping이며 center replacement가 아님
- `meta/detail leakage`는 core tree로 되돌리지 않음
- schema validator pass 전에는 추가 구조 구현을 밀지 않음
- `display_path_ko`와 `primary_placement_id`는 `payload 필수 필드`로 고정
- `expression_core_candidate`는 별도 계층으로 운영하고, 필요할 때만 `core_bridge`로 연결

## 3. Shared Source of Truth

- `PRODUCT_DIRECTION_V1.md`
- `01_architecture/00_indexes/SESSION_INDEX_V1.md`
- `NEXT_THREAD_HANDOFF_V3.md` (`current next-thread handoff`)
- `.gemini-orchestration/references/06_taxonomy review/` (IA 재설계 핵심 가이드라인)
- `08_expansion/ROADMAP_STATUS_TASKLIST_V2.md` (`roadmap / status summary only`)
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V3.md` (`single authoritative tasklist / todo`)
- `08_expansion/THREE_LEVEL_RESTRUCTURE_TASKLIST_V1.md`
- `08_expansion/SCHEMA_LINKAGE_VALIDATION_PLAN_V1.md`
- `08_expansion/THREE_LEVEL_CLASSIFICATION_TABLE_V1.md`
- `08_expansion/THREE_LEVEL_CORE_PAYLOAD_V1.json`
- `08_expansion/EXCEPTION_QUEUE_V1.json`
- `08_expansion/EXPRESSION_CORE_CANDIDATES_V1.json`
- `08_expansion/PROJECTION_APP_CONTRACT_EXPANSION_DRAFT_V1.md`
- `08_expansion/WEB_MINDMAP_NAVIGATION_SPEC_V1.md`

## 4. Roles

에이전트 명칭 기준:

- `Gemini CLI` = `데이터 검증 에이전트`
- `Antigravity` = `개발 에이전트`
- `Review Gemini` = `리뷰 에이전트`

## 4. Roles (Updated for RESTART)

- **Gemini Orchestrator (Manager)**: 최종 방향성 소유자 및 산출물 검증자.
- **데이터 에이전트 (Gemini CLI)**: 05_source 분석, 3단계 분류 체계 수립, 런타임 JSON 설계 및 생성 담당.
- **개발 에이전트 (Antigravity)**: 09_app 기반 UI 구현, 마인드맵 캔버스 및 플립카드 기능 구현 담당.
- **리뷰 에이전트 (Review Gemini)**: 구현 및 데이터의 비판적 검수, 외국인 학습자 관점 피드백 담당.

## 5. Instruction Standard (Self-Refinement)

모든 작업 지시는 아래 3대 규칙을 기반으로 에이전트 스스로 완결성을 확보해야 한다.

1. **`tool_persistence_rules`**: 단일 오류나 예외 발생 시 중단하지 말고, 데이터 전체의 패턴을 분석하여 근본적인 해결책이나 대응 로직을 찾아낼 것.
2. **`completeness_contract`**: 보고서 본문뿐만 아니라, 실제 파일 존재 여부, 데이터 샘플 증거, 빌드 성공 결과가 모두 일치할 때만 완료로 간주함.
3. **`verification_loop`**: (Draft -> Self-Review -> Revision -> Reflection)의 4단계 사이클을 거쳐 최종 결과물을 도출할 것.

## 5. Current Program Position

현재 기준:

- `scene core` 3단계 구조 정리 완료
- `THREE_LEVEL_CORE_PAYLOAD_V1.json`: `338`
- `EXCEPTION_QUEUE_V1.json`: `934`
- `EXPRESSION_CORE_CANDIDATES_V1.json`: `43`
- schema validator / review / UI shell 구현은 한 사이클 완료
- expression core는 별도 계층 운영 기준이 확정됨
- 현재 미완료는 source-rich data connection이다
- 뜻, 예문, provenance, TOPIK frequency/grade, bridge target의 실제 UI 연결은 아직 불완전하다
- `Gemini CLI`가 payload 보강 트랙을 먼저 진행하고 있다
- `08_expansion/MINDMAP_UI_SPEC_DRAFT_V1.md` 초안 작성과 `Review Gemini` round 1 검토가 완료됐다
- `08_expansion/MINDMAP_UI_SPEC_DRAFT_V2.md`에 review 반영본이 작성됐다
- `.gemini-orchestration/UI_FEASIBILITY_FEEDBACK_V1.md` 기준 Antigravity feasibility feedback도 완료됐다
- `08_expansion/MINDMAP_UI_SPEC_LOCK_V1.md`로 현재 spec lock이 확정됐다
- 스크린샷 기준 scene core runtime tree의 meta leakage evidence(`방법`, `물음` 등)가 확인됐다
- current critical path is `scene core classification correction before broad tree implementation`
- `APP_READY_CORE_TREE_V1.json` 생성과 `loaderAdapter.js` 연동까지 반영되었고, review round 3 final 기준 scene core physical cleanse is accepted 상태다
- 리뷰 에이전트는 구현 보고뿐 아니라 데이터 검증 에이전트 보고에도 적극 투입한다

## 6. Active Tracks (RESTART-V1)

### Track G1: 데이터 에이전트 (Gemini CLI)
- **Status**: `STANDBY - Awaiting Feedback`
- **Current Objective**: `[T1.4] Chunk Sharding & Remaining Taxonomy Adjustment`
- **Board**: `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`

### Track A1: 개발 에이전트 (Antigravity)
- **Status**: `RUNNING`
- **Current Objective**: `[T3.2] Data Integration (Connecting APP_READY_CORE_TREE_V1.json)`
- **Board**: `.gemini-orchestration/DEVELOPMENT_AGENT_WORKBOARD_V1.md`

### Track R1: 리뷰 에이전트 (Review Gemini)
- **Status**: `RUNNING`
- **Current Objective**: `[T5.2] Verification of 14 Core Roots in New Payload`
- **Board**: `.gemini-orchestration/REVIEW_AGENT_WORKBOARD_V1.md`

## 7. Polling Protocol

1. 각 에이전트는 자기 workboard를 `2분마다` 확인한다.
2. `Revision`, `Status`, `Current Task`, `Blocking / Decision Needed`, `Latest Report` 변경 여부를 본다.
3. 완료 또는 blocker 발생 시 handoff template 기준으로 보고한다.
4. 채팅 보고만 하고 workboard를 갱신하지 않은 작업은 미보고로 본다.

## 8. Handoff Rule

- 보고 템플릿: `.gemini-orchestration/HANDOFF_REPORT_TEMPLATE_V1.md`
- 상세 보고가 있으면 workboard의 `Latest Report`에 링크를 남긴다.
- Gemini Orchestrator는 보고를 읽은 뒤 실제 파일과 산출물을 직접 검증한다.
- review-only 보고는 채팅 요약만으로 완료로 보지 않는다.
- Review agent는 반드시 review memo 파일을 남기고, workboard `Latest Report`에 verdict와 파일 경로를 함께 기록해야 한다.
- review memo는 가능하면 `3 expert lenses` 기준으로 findings를 구분하거나 최소한 그 관점이 드러나야 한다.
- 데이터 검증 에이전트와 개발 에이전트의 핵심 보고는 가능하면 리뷰 에이전트 검수를 먼저 거친다.
- 작업 에이전트의 보고와 리뷰 에이전트의 verdict는 가능하면 같은 working workboard 안에 함께 남긴다.
- Gemini Orchestrator의 보고 검토는 장점 요약보다 `누락 / 약한 점 / 추가 개선점`을 우선한다.
- 다음 단계가 자연스럽게 정해지면, 그 누락 사항을 바로 다음 agent instruction으로 연결한다.
- Gemini Orchestrator는 보고를 받을 때마다 `실제 산출물 검증`을 필수로 수행한다.
- 검증이 불완전하면 완료로 처리하지 않고, 그 사실과 남은 확인 항목을 명시한다.
- 각 에이전트는 초안 1회로 끝내지 말고 `초안 -> 자기검토 -> 수정 -> 재검토 -> 최종 보고` 순서로 움직인다.
- 최종 보고에는 최소한 `무엇을 다시 점검했고 무엇이 약점이었는지`를 짧게 남긴다.

운영 순서:

1. Gemini Orchestrator가 working workboard를 갱신한다.
2. 사용자가 그 workboard를 working agent에게 전달한다.
3. working agent가 같은 workboard에 `Latest Work Report`를 남긴다.
4. 사용자가 그 same working workboard를 review agent에게 전달한다.
5. review agent가 same workboard에 `Latest Review`를 추가한다.
6. 사용자가 Gemini Orchestrator에게 그 workboard를 알려준다.
7. Gemini Orchestrator가 same workboard + 실제 산출물을 검증한다.

중요:

- 기본 전달 문서는 항상 `working workboard` 하나다.
- `REVIEW_AGENT_WORKBOARD_V1.md`는 review queue / 상태 관리용이며, 기본 handoff 문서가 아니다.
- 사용자에게는 각 단계마다 1~3줄 수준의 짧은 상태/핵심 finding/다음 handoff만 보고한다.

예외:

- review-only 작업은 Gemini Orchestrator가 리뷰 에이전트와 직접 진행할 수 있다.
- 그 경우에는 리뷰 에이전트 workboard 자체를 해당 cycle의 primary 문서로 사용한다.

## 9. Conflict Rule

아래는 Gemini Orchestrator 승인 없이 바꾸지 않는다.

- canonical touch
- contract field change
- promotion decision
- work priority reversal

충돌 시:

1. 해당 workboard의 `Blocking / Decision Needed`에 기록
2. 필요한 문서 링크 추가
3. Gemini Orchestrator decision 대기

## 10. Current Recommended Flow

1. `Review Gemini` broad tree acceptance 결과를 잠근다.
2. `Gemini Orchestrator`가 authoritative tasklist와 handoff를 갱신한다.
3. 그 다음 `Gemini CLI`가 expression/meta broad tree payload를 생성한다.
4. `Antigravity`가 그 payload를 받아 expression/meta broad map 구현을 이어간다.
5. 그 다음 `Review Gemini`가 확장 구현을 검수한다.

운영 메모:

- review round 기록은 계속 유지하되, 현재 실행 초점은 scene core 분류 교정 필요 여부 판단과, 필요 시 교정을 선행하는 것이다.
- tasklist/todo는 `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V3.md` 하나를 authoritative source로 본다.
- broad tree/mindmap 재개는 `D28`과 `E15`가 runtime evidence로 잠기기 전까지 허용하지 않는다.
