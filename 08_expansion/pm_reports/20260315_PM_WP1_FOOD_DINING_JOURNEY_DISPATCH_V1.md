# PM WP-1 Food & Dining Journey Dispatch V1

> Date: `2026-03-15`
> Owner: `Codex / Main PM`
> Status: `DISPATCHED`
> Target Agent: `데이터 에이전트`

## 1. 목적 (Purpose)
- 승인된 `WP-1. 식당/음식 (Food & Dining Learner Journey)`의 learner-facing richer enrichment 확장을 실행한다.
- `상황` 축의 음식/식당 관련 노드와 `마음` 축의 미각/포만감/평가 노드 간의 유의미한 교차 점프(cross-links)를 구축한다.

## 2. 작업 범위 (Scope)
다음 타겟 그룹 간의 양방향 또는 단방향 relation을 발굴하고 주입한다. 
*Note: 일부 단어(예: 주문하다, 먹다, 맛있다, 맛없다)가 현재 graph에 없거나 다른 형태(주문, 맛)로 존재하는 경우, 존재하는 ID를 기준으로 매핑한다.*

- **Scene -> State/Action:** `식당`, `밥`, `메뉴`, `음식점`, `카페` -> `배고프다`, `목마르다`, `주문`, `마시다`
- **Object -> Sensation/Evaluation:** `음식`, `찌개`, `반찬`, `물`, `커피` -> `맛`, `맵다`, `짜다`, `달다`, `뜨겁다`, `차갑다`, `시원하다`
- **State -> Resolution Route:** `배고프다`, `목마르다` -> `식당`, `카페`, `편의점`, `물`, `음료수`

## 3. 실행 지침 (Execution Guidelines)
1. **Target IDs 식별:** 현재 `8094`개의 라이브 노드 중에서 위 타겟 단어들의 정확한 ID를 추출한다.
2. **Relation 부여:** 내부 canonical(`09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`)에 Edge를 추가한다.
3. **Jump Purpose 명시:** 가능하면 추가되는 `cross_links`의 맥락적 목적(예: `scene-jump`, `usage-route`, `sensation-jump`)을 append-only 로그나 내부 메모로 함께 기록한다 (런타임에 노출되지 않더라도 내부 데이터의 가치 향상을 위해).
4. **Safety Guards:**
   - 기존의 `split/search/chunk mismatch`가 `0`으로 유지되어야 한다.
   - `duplicate ids`가 발생해서는 안 된다.
   - Holdout 노드 (`오늘(부사)`, `어제(부사)`, `점심`, `저녁(의미2)`)의 zero-relation 상태(`0/0`)를 침범하지 않는다. (단, `점심/저녁`이 식사 의미로 쓰이는 노드가 따로 있다면 그 노드는 확장에 포함 가능).

## 4. 예상 산출물 (Expected Output)
- 대상 ID 목록 및 추가된 엣지 수 (Before / After 카운트)
- 정합성 검사 결과 (Safety Check)
- 데이터 에이전트의 실행 결과 보고서