# Data Review Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-75`
> Logged: `2026-03-14 18:18:00`
> Scope: `V1-REV-74 planning proposal structure / implementation impact / rebuild requirements review`
> Reporting Rule: `append-only only`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/PLANNING_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV74_relation_model_execution_closure_proposal.md`

## Evidence Surfaces Checked

- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `scripts/mining/run_rev47_xwd_mining.py`
- `scripts/core/rebuild_rev23_detail_chunks.py`
- `09_app/src/App.jsx`
- `09_app/src/components/TermDetail.jsx`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`

## Review Result

- verdict: `proposal directionally sound but structurally incomplete for execution handoff`
- summary:
  - `V1-REV-74` proposal은 learner-facing relation 재정의 방향은 타당하다.
  - 하지만 데이터 에이전트가 바로 집행할 수 있을 정도로 `어느 산출물에 richer relation을 저장할지`, `thin runtime으로 어떻게 투영할지`, `언제 어떤 재빌드를 강제할지`가 아직 닫히지 않았다.

## Confirmed Implementation Reality

- current publish reality:
  - `scripts/mining/run_rev47_xwd_mining.py`는 upstream relation에서 `reason`을 읽지만, live publish 시 `related_vocab`는 `string[]`, `cross_links`는 `target_id/target_term/target_system/target_root/target_category/hook_id`만 남긴다.
- current rebuild reality:
  - `scripts/core/rebuild_rev23_detail_chunks.py`는 live tree/search의 `related_vocab` / `refs.cross_links`를 다시 청크 파일로 전파한다.
  - 즉 relation semantics 변경은 `split/search publish -> chunk rebuild` 전체 재배포를 동반한다.
- current UI reality:
  - `TermDetail.jsx`는 `related_vocab`를 문자열 칩으로 렌더링한다.
  - `cross_links`는 `target_term`와 `target_category`를 라벨로 사용한다.
  - `App.jsx`는 `cross_links` 클릭 시 `target_id` 우선, 실패 시 `target_term` fallback을 유지한다.

## Missing Requirements That Must Be Added To Planning

### 1. Rich relation canonical storage contract

- planning 문서에 반드시 추가할 것:
  - richer relation layer의 authoritative 저장 위치
  - 권장 필드:
    - `target_id`
    - `target_term`
    - `relation_role`
    - `jump_purpose`
    - `reason`
    - `hook_id`
    - `target_system`
    - `target_root`
    - `target_category`
    - optional `rank` or `priority_bucket`
- why:
  - 현재 proposal은 “internal canonical relation layer를 richer하게 유지”하자고 했지만, 실제 어떤 artifact가 그 역할을 맡는지 지정하지 않았다.
  - 이게 없으면 data 단계에서 canonical owner가 불명확해지고 publish 결과만 덮어쓰게 된다.

### 2. Thin runtime projection contract

- planning 문서에 반드시 추가할 것:
  - runtime live는 이번 cycle에서 backward-compatible thin projection을 유지할지 여부
  - projection rule:
    - `related_vocab`: 우선 `string[]` 유지
    - `refs.cross_links`: 현재 object shape 유지, 필요 시 `jump_purpose_label` 같은 optional display field만 검토
  - projection source and destination:
    - source: richer internal relation artifact
    - destination: `09_app/public/data/live/APP_READY_*_TREE.json`, `APP_READY_SEARCH_INDEX.json`, chunk files
- why:
  - 현재 UI는 richer record를 직접 소비하지 못한다.
  - runtime shape를 바로 바꾸면 `TermDetail.jsx`와 `App.jsx`가 함께 바뀌어야 하므로, planning에 data-only cycle인지 dev-coupled cycle인지 구분이 필요하다.

### 3. Rebuild trigger matrix

- planning 문서에 반드시 추가할 것:
  - 아래 변경은 모두 runtime redeploy mandatory로 명시
    - `related_vocab` meaning/selection rule 변경
    - `refs.cross_links` meaning/selection rule 변경
    - `target_id`/path metadata 변경
    - `chunk_id` 재부여 또는 chunk partition 영향 변경
  - required execution order:
    1. `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
    2. `python3 scripts/core/rebuild_rev23_detail_chunks.py`
- why:
  - proposal에는 `rebuild gate`는 나오지만, SOP 수준의 강제 순서와 트리거 표가 없다.
  - 이 누락은 split/search와 chunk 불일치 리스크를 그대로 남긴다.

### 4. Validation and acceptance evidence contract

- planning 문서에 반드시 추가할 것:
  - data -> review gate에 아래 증거를 필수화
    - split 총합 = search total
    - search `chunk_id` 존재 = 전체 term 수
    - split `chunk_id` 존재 = 각 파일 전체 term 수
    - `related_vocab` target 누락 `0`
    - `related_vocab` 타분류 오염 `0`
    - `cross_links` 동일분류 오염 `0`
    - `cross_links` 타깃 누락 `0`
    - legacy `target_center_id` 잔존 `0`
    - `CHUNK_MANIFEST_V1.json` 및 chunk rich/examples 재생성 확인
    - detail chunk와 live tree의 relation 일치 확인
- why:
  - proposal은 gate 구조는 제시했지만, 실제 acceptance evidence가 SOP 수준으로 수치화돼 있지 않다.

### 5. UI impact boundary

- planning 문서에 반드시 추가할 것:
  - 이번 cycle에서 UI 문구/라벨만 조정하는지, field contract까지 바꾸는지 분리
  - current fallback deprecation plan:
    - short-term: `target_id` canonical 유지, `target_term` fallback 유지
    - long-term: review acceptance 후 fallback 제거 후보로 분리
- why:
  - 현재 proposal은 `cross_links`를 learner-purpose label로 보강하자고 하지만, runtime/UI 영향 범위를 닫지 않았다.
  - data cycle과 dev cycle 경계를 문서에 고정하지 않으면 승인 후 범위가 불어나기 쉽다.

## Recommended Solution

- 추천안: `rich internal canonical + thin runtime projection + explicit rebuild gate`
- reasoning:
  - learner-facing semantics는 풍부하게 정의하되, 현재 live schema와 UI 소비 계약은 이번 cycle에서 최대한 유지한다.
  - 즉 planning 문서에는 “정책/내부 canonical은 richer하게”, “runtime live는 투영된 thin schema로”를 명시하고, UI 확장은 후속 dev gate로 분리한다.
- advantages:
  - data/review 단계가 지금 파이프라인 위에서 바로 집행 가능하다.
  - runtime/UI 회귀 리스크를 낮춘다.
  - proposal의 semantic ambition은 살리면서 재배포 절차를 통제할 수 있다.
- risk:
  - learner-purpose 정보가 live runtime에 즉시 다 노출되지는 않는다.
  - richer field 활용은 후속 dev cycle이 필요하다.

## Planning Delta Patch Request

- `RELATION_DATA_POLICY_V1.md`에 추가:
  - richer internal relation schema 정의
  - thin runtime projection rule
  - time-anchor/grammar-anchor relation obligation
- `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`에 추가:
  - relation publish + chunk rebuild를 하나의 mandatory work package로 묶기
  - validation evidence checklist를 done criteria에 삽입
- `MASTER_ROADMAP_V1.md`에 추가:
  - `Policy Closure -> Data Publish/Rebuild -> Review Acceptance -> UI Optional Upgrade` 순서 명시
- planning appendix에 추가:
  - rebuild trigger matrix
  - runtime-safe field contract
  - fallback deprecation note

## Closing Note

- 이번 검토는 상태 필드 수정 없이 append-only 로그로만 남김
- `V1-REV-74` proposal은 폐기 대상이 아니라, 위 data structure / rebuild requirement를 추가하면 execution-ready proposal로 승격 가능
