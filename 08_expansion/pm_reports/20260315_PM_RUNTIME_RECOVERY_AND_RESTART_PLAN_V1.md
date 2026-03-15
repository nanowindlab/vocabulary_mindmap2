# PM Runtime Recovery And Restart Plan V1

> Date: `2026-03-15`
> Owner: `Codex / Main PM`
> Scope: `REV-102` abort 이후 runtime consistency 복구, Batch-11 contract 재정의, runtime projection hardening, batch portfolio 재분류, coverage restart gate 정의
> Status: `COMPLETE / RESTART-READY`

## 1. Milestone 1: Yellow Runtime Consistency Closure

### Authoritative Inputs

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/CHUNK_MANIFEST_V1.json`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `scripts/mining/run_rev47_xwd_mining.py`
- `scripts/core/rebuild_rev23_detail_chunks.py`
- `.gemini-orchestration/workboard_archive/green_batch/20260315_REV102_batch11_green_autopilot_trial_report_rerun01.md`

### Verified Findings

- duplicate-id는 `rebuild_rev23_detail_chunks.py`가 생성한 것이 아니었다.
- root cause는 duplicate live split/search 입력이었다.
- chunk rebuild는 duplicated live tree를 읽어 chunk dict key overwrite를 일으키며 `search total != manifest sum` 문제를 드러내는 위치였다.
- local repair 후 runtime canonical은 아래 상태로 복구되었다.
  - split total `8094`
  - search total `8094`
  - manifest sum `8094`
  - split/search/chunk duplicate ids `0`

### Closure Decision

- duplicate input이 다시 들어오면 rebuild를 즉시 실패시키는 guard를 추가했다.
- 현재 baseline/runtime/chunk 정합성은 local artifact 기준으로 복구 완료로 본다.

## 2. Milestone 2: Batch-11 Contract Redefinition

### Prior Assumption That Broke

- `Calendar Label Batch-11`은 `Type A + Green`으로 간주되었다.
- 그러나 comparison autopilot과 artifact inspection 결과, 이 batch는 thin runtime projection batch가 아니라 runtime reclassification batch에 가까웠다.

### Evidence

- `요일_일반명사-1`는 Batch-11 expected change surface에 포함되는데도 no-drift sentinel로 사용되었다.
- `REV-102` rerun에서 `요일_일반명사-1`가 `4|0 -> 1|0`로 바뀐 것은 runtime corruption보다 control-set 설계 오류를 먼저 의미한다.
- Batch-11 duplicate incident에서 중복된 id는 기존 live에 이미 존재하던 runtime ids의 재분류본이었다.

### New Contract

- `Calendar Label Batch-11`은 더 이상 `Green autopilot` 대상이 아니다.
- 새 분류는 `Yellow / Runtime Reclassification`.
- 이 batch는 아래 작업을 포함할 수 있으므로 thin runtime projection으로 취급하지 않는다.
  - current live node hierarchy 재분류
  - current live control set 재해석
  - relation overlay 외의 runtime admission 또는 replacement

### Control Rule Fix

- active batch change surface에 포함된 id는 no-drift sentinel로 둘 수 없다.
- `요일_일반명사-1`는 sentinel에서 제외하고, change-surface reference id로 재분류한다.
- stable sentinel은 현재 cycle에서 `모레_일반명사-1`, `정오_일반명사-1` 중심으로 유지한다.

## 3. Milestone 3: Runtime Projection Model Hardening

### Hardening Decision

- `publish-only`는 relation overlay only다.
- `publish-only`는 아래 작업에 사용할 수 없다.
  - new runtime id admission
  - live hierarchy(`system/root/category`) reclassification
  - duplicate split/search surface 위에서의 실행

### Implemented Guards

- `scripts/mining/run_rev47_xwd_mining.py`
  - split/search duplicate preflight
  - split/search count mismatch preflight
  - overlay ids missing from live runtime preflight
  - internal canonical node hierarchy vs live runtime drift preflight
- `scripts/core/rebuild_rev23_detail_chunks.py`
  - duplicate live input hard-fail

### Operational Implication

- 앞으로 thin runtime projection green batch는 “현재 live에 이미 존재하는 id의 relation overlay”만 허용한다.
- id admission이나 hierarchy change가 필요한 batch는 별도 yellow reclassification cycle로 분리한다.

## 4. Milestone 4: Batch Portfolio Reclassification

| Portfolio Item | Current Classification | Evidence Basis | Verdict |
| :--- | :--- | :--- | :--- |
| `core12 + holdout4 pilot` | `Green Closed` | runtime projection + chunk rebuild gate 완료, holdout exclusion 유지 | validated |
| `Calendar Continuity Batch-14` | `Green Closed` | build -> acceptance -> projection -> chunk rebuild까지 완결, reserve/sentinel drift `0` | validated |
| `Calendar Label Batch-11` | `Yellow / Runtime Reclassification` | `REV-102` abort, sentinel set 오류, duplicate live input incident | not restartable as green |
| `Month Unit Batch` | `Yellow Hold` | inventory gap 다수, month system normalization 미완 | keep yellow |
| `Date Point Batch` | `Yellow Hold` | `날` duplicate surface, family template 분산 | keep yellow |

### Portfolio Rule

- green batch는 “relation overlay only + runtime-safe existing ids + control-set clean” 3조건을 모두 만족해야 한다.
- 위 조건을 하나라도 깨면 yellow로 본다.

## 5. Milestone 5: Coverage Expansion Restart

### Restart State

- 현재 상태는 `RESTART-READY`다.
- 의미:
  - expansion을 지금 바로 다시 dispatch했다는 뜻이 아니다.
  - restart gate와 운영 규칙이 다시 고정되었고, 다음 dispatch를 열 수 있는 상태라는 뜻이다.

### Mandatory Restart Gates

1. live split/search/chunk duplicate ids `0`
2. split/search/chunk count mismatch `0`
3. `publish-only` preflight/postflight guard 통과
4. active batch change surface와 sentinel/no-drift control set 분리
5. green 후보 batch는 current live id admission 없이 relation overlay만 수행
6. hierarchy reclassification 또는 id admission이 필요한 batch는 yellow track으로 명시

### Restart Policy

- next restart는 `green autopilot 확대`가 아니라 `green relation-overlay batch만 제한적으로 재개`다.
- `Calendar Label Batch-11`은 restart queue가 아니라 yellow investigation queue로 남긴다.
- 다음 green dispatch는 위 gate를 만족하는 새 batch를 다시 선정한 뒤 여는 것이 맞다.

## 6. PM-Centric Operating Model

현재 cycle부터 상태 관리와 중간 산출물은 아래 surface에만 남긴다.

- 현재 상태: `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- 다음 스레드 handoff: `.gemini-orchestration/NEXT_MAIN_PM_HANDOFF_V1.md`
- durable decisions: `08_expansion/PROJECT_DECISION_LOG_V1.md`
- current cycle evidence: `08_expansion/pm_reports/*.md`

workboard/workboard_archive는 history-only다.

## 7. Final Result

- Yellow runtime consistency closure: complete
- Batch-11 contract redefinition: complete
- runtime projection hardening: complete
- batch portfolio reclassification: complete
- coverage expansion restart gate definition: complete

다음 단계는 green candidate를 다시 dispatch하는 것이 아니라, 이 restart gate를 기준으로 후보를 새로 고르는 일이다.
