# V1-PRE-REV-83-REVIEW 지시접수 및 Bounded Survey 보고

- **일시**: 2026-03-15
- **대상 Revision**: V1-PRE-REV-83-REVIEW
- **상태**: REVIEW_COMPLETED (Bounded Survey 완료)

## 1. 지시사항 재확인 (Sync Check)
- **Authoritative Source**: ORCHESTRATION_DASHBOARD.md
- **Required Skills**: report-verifier, data-validation (확인 완료)
- **작업 목표**: `REV-82` 결론(`node seeded / edge held` 유지)을 고정값으로 두고, 다음 `REV-83` (Core 12 anchor pilot execution) 직전에 Acceptance / Validation blind spot만 점검. 새 정의, 개념 도입, 과거 논의 회귀 금지.

## 2. 리뷰 관점 우려사항 및 대안/추천안 (Blind Spot Check)

`REV-83`에서 진행될 "Core 12 anchor 중심 pilot execution"의 실행 방법과 검증 포인트를 리뷰 에이전트 관점에서 점검한 결과, 아래 3가지의 주요 우려사항(Blind Spot)과 대안을 제시합니다.

### 🔴 우려사항 1: Thin Projection 덮어쓰기로 인한 검증(Diff) 증발 위험
**문제 진단:** `REV-83`에서 Data Agent가 Internal Graph를 업데이트한 후, Publish Script(`run_rev47_xwd_mining.py --publish-only`)와 Chunk Rebuild(`rebuild_rev23_detail_chunks.py`)를 실행하면, 기존 Live 디렉토리의 데이터가 덮어씌워집니다. 이 때 변경된 `related_vocab`과 `cross_links`의 Before/After(Diff)를 정밀하게 추적하고 검증(Review)할 Evidence Artifact가 누락될 수 있습니다.

- **대안 A (수동 백업):** 실행 전 `09_app/public/data/live/` 전체를 임시 폴더에 압축 복사한 뒤 비교. (단점: 용량이 크고 비교 자동화가 불편함)
- **대안 B (스크립트 레벨 Diff 로그):** Publish Script가 실행될 때 기존 값과 새 값의 차이점만 별도의 JSON/Markdown(예: `PILOT_DIFF_REPORT.json`)으로 뱉어내도록 수정. (단점: 스크립트 수정 리스크)
- **대안 C [추천안] (Dry-Run / Snapshot 생성):** Data Agent가 Script를 실행하기 직전에 Target Anchor 12개에 대한 "현재 Runtime Live 상태 스냅샷"을 Append-only 로그에 명시적으로 기록(Text 덤프)한 뒤 실행. 실행 후 해당 로그에 "After" 결과를 추가 기록하여 비교 증거로 삼음. (장점: 기존 스크립트 수정 없이 안전한 리뷰 증거 확보 가능)

### 🔴 우려사항 2: Holdout Node의 검색/UI 노출 제어 (Schema Contract 유지)
**문제 진단:** `REV-82` 결정에 따라 Holdout 4개 노드(`오늘_일반부사-1`, `어제_일반부사-1`, `점심_일반명사-1`, `저녁_일반명사-2`)는 Edge 연결은 되지 않지만 Node 자체는 Internal Canonical에 존재하게 됩니다. 이 Holdout 노드들이 의도치 않게 Live Projection에 유입되거나, 검색 인덱스(`APP_READY_SEARCH_INDEX.json`)의 Relation 카운트를 오염시킬 수 있는지에 대한 방어 로직 확인이 필요합니다.

- **대안 A (하드코딩 배제):** Publish Script 내부에 Holdout ID 목록을 하드코딩하여 Skip 처리. (단점: 유지보수 악몽)
- **대안 B [추천안] (의도 기반 필터링):** Internal Canonical의 `display_intent`가 할당되지 않았거나(Null) Edge가 비어있는 Node는 Runtime Projection Rule에 따라 자연스럽게 무시(Skip)되는지 Data Agent가 사전 검증(Dry-run) 단계에서 입증하도록 Gate Evidence Checklist에 추가. (장점: 기존 Projection Rule을 유지하면서 부작용 방지)

### 🔴 우려사항 3: UI Fallback 메커니즘 붕괴 리스크
**문제 진단:** 새 Relation Data가 주입될 때, 현재 App UI가 `target_term`이 아닌 `target_id`를 우선 참조하는 방식(App.jsx fallback 로직)에 의존하고 있습니다. 그러나 동음이의어(예: 명사/부사 오늘)가 완벽히 통제되지 않은 상태에서, UI가 엉뚱한 Sense(의미)로 튕겨 나갈(Jump) 가능성이 존재합니다.

- **대안 A (UI 코드 선행 수정):** `REV-83` 실행 전 Development Agent가 먼저 UI Fallback 로직을 강화. (단점: Phase Gate 위반, Data 완료 전 UI 개입 금지 원칙 위배)
- **대안 B [추천안] (안전한 Target ID 매핑 검증):** `REV-83` 데이터 주입 시, 12개 Anchor가 가리키는 `cross_links`의 `target_id`가 정확히 우리가 의도한 "명사형" Sense ID와 1:1로 매칭되는지, Review Agent가 최종 산출물을 보고 전수 확인(Manual Inspection)하는 단계를 Handoff Gate(Data -> Review)에 필수로 삽입. (장점: UI 수정 없이 데이터 레벨에서 안전성 보장)

---

## 3. REV-83 실행 전 필수 확인 Checklist (Method, Order, Validation)

위의 점검을 바탕으로 `REV-83` 착수 시 준수해야 할 필수 항목을 정리합니다.

1. **[Method] Before/After Snapshot 기록**: Data Agent는 `rebuild` 실행 전, 대상 12개 단어의 Live Runtime 상태를 로그에 박제해야 합니다.
2. **[Order] Internal 먼저, Live는 나중**: `RELATION_GRAPH_CANONICAL_V1.json` (Skeleton)에 12개 Node/Edge를 먼저 완벽히 구성한 뒤 -> 스크립트를 통한 Thin Projection을 실행해야 합니다.
3. **[Validation] Holdout 유출 제로 확인**: `점심_일반명사-1` 등 Holdout 노드들이 `APP_READY_SITUATIONS_TREE.json`이나 Detail Chunk에 잘못된 엣지(Edge)로 튀어나오지 않았는지 grep/search로 교차 검증해야 합니다.
4. **[Validation] Target ID 정확성 검증**: 생성된 엣지의 `target_id`가 의도하지 않은 품사(부사 등)로 잘못 매핑되지 않았는지 확인해야 합니다.

해당 Survey 리포트를 제출하며, 사용자의 최종 판단 및 `REV-83` 지시를 대기합니다.