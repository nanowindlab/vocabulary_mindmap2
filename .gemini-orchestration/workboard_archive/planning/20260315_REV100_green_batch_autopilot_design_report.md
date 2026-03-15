# Green Batch Autopilot Memo

> Agent: `기획 에이전트`
> Revision: `V1-REV-100`
> Logged: `2026-03-15`
> Status: `PROPOSAL / NOT YET APPLIED`
> Purpose: PM 관할 아래에서 Green batch가 어디까지 자동으로 흐를 수 있는지 운영 모델로 정리
> Guard: 새 relation semantics / validated contract 재개방 금지

## 문제 재정의

`REV-94`가 batch operating model을 만들었고, `REV-95~98`이 next green batch를 실제로 다시 green path에 올릴 수 있음을 보여 줬다. `REV-100`의 문제는 이제 다음과 같다.

- green batch를 어디까지 자동으로 진행할 수 있는가
- 어떤 조건에서 멈추고 yellow로 승격해야 하는가
- PM은 어디서만 개입하면 되는가

즉 이번 revision은 `one-batch-one-rev`의 상위 버전인 **PM-supervised autopilot**의 경계를 정하는 일이다.

## Web Research Basis

- [Argo Rollouts Canary](https://argo-rollouts.readthedocs.io/en/stable/features/canary/)
- [Argo Rollouts Analysis](https://argo-rollouts.readthedocs.io/en/stable/features/analysis/)

실무 해석:

- rollout은 step chain과 analysis gate를 묶어 자동화하되,
- failure signal이 나오면 즉시 promote/pause/abort 되는 구조가 안전하다.
- 따라서 green batch autopilot도 “무조건 끝까지”가 아니라 **자동 진행 + 조건부 정지 + yellow 승격** 모델이 맞다.

## 추천안

### Final Recommendation

- `PM-supervised Green Batch Autopilot`

### 핵심 원칙

1. PM이 green batch를 명시적으로 arm한다.
2. batch agent는 정해진 chain을 자동 실행한다.
3. stop signal이 하나라도 뜨면 즉시 yellow로 승격하고 자동 실행을 멈춘다.
4. stop signal이 없으면 chunk sync까지 자동으로 닫고, 그 뒤 review verdict를 받는다.

## autopilot step chain

### Step 0. Arm

- owner:
  - PM / Codex
- input:
  - batch id
  - current contract version
  - allowed write target
- check:
  - `Type A + Green` eligibility confirmed

### Step 1. Internal Build

- owner:
  - Green Batch Agent
- action:
  - internal canonical node/edge update
- required self-check:
  - duplicate `0`
  - reciprocal missing `0`
  - required field missing `0`
  - holdout/reserve touch `0`

### Step 2. Projection Gate Auto-Pack

- owner:
  - Green Batch Agent
- action:
  - `dry_run_reserve` update
  - before snapshot generation
  - expected bucket generation
  - holdout/reserve/sentinel baseline generation

### Step 3. Runtime Projection

- owner:
  - Green Batch Agent
- action:
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
- immediate check:
  - actual bucket vs expected
  - holdout/reserve/sentinel drift `0`

### Step 4. Chunk Sync

- owner:
  - Green Batch Agent
- action:
  - `python3 scripts/core/rebuild_rev23_detail_chunks.py`
- immediate check:
  - batch ids search/tree/chunk consistency
  - holdout/reserve/sentinel chunk drift `0`

### Step 5. Consolidated Report + Review Handoff

- owner:
  - Green Batch Agent -> Review Gate Agent
- output:
  - one consolidated autopilot report
  - one review dispatch input

## stop / promote-to-yellow rule

### Yellow Promotion Triggers

autopilot은 아래 중 하나라도 발생하면 즉시 정지하고 `Yellow`로 승격한다.

1. duplicate / reciprocal / required field error
2. holdout touched
3. reserve drift
4. sentinel drift
5. expected bucket vs actual bucket mismatch
6. target_id ambiguity or non-noun target leakage
7. batch envelope 초과
8. 예상하지 않은 script mode 변화
9. search/tree/chunk consistency failure

### Stop Behavior

- current step에서 즉시 정지
- 다음 step 실행 금지
- 상태를 `autopilot_aborted_to_yellow`로 기록
- PM/Codex와 Review 쪽에 yellow handoff memo 생성

## PM intervention rule

### PM Must Intervene

1. Step 0 arm
2. Yellow 승격 시
3. final review verdict 후 next batch 개시 여부 판단

### PM Does Not Need To Intervene

- green batch가 Step 1~4를 문제 없이 통과하는 동안
- 즉, green autopilot은 `build -> projection pack -> publish-only -> chunk rebuild`를 PM 재지시 없이 수행 가능해야 한다

## evidence pack auto-generation spec

### Auto-Generated Artifacts

1. `internal_build_check`
   - node delta
   - edge delta
   - duplicate/reciprocal/result

2. `projection_gate_pack`
   - before snapshot
   - expected bucket table
   - holdout/reserve/sentinel baseline

3. `runtime_projection_check`
   - actual vs expected bucket
   - drift check
   - publish summary

4. `chunk_sync_check`
   - search/tree/chunk consistency
   - chunk drift check

5. `autopilot_summary`
   - step result table
   - final status
   - yellow promotion 여부

### Minimal Format Rule

- human-readable markdown 1종
- machine-check table 1종
- existing JSON/support artifact 재사용
- 새 schema 발명 금지

## first rollout recommendation

### Recommended First Autopilot Trial

- reopen candidate:
  - `REV-99` batch11 runtime projection chain

### Why

- `Calendar Label Batch-11`은 이미
  - `Type A + Green`
  - preview coverage `20/20`
  - before snapshot ready
  - holdout/reserve/sentinel baseline fixed
  상태까지 왔다.

- 즉 autopilot 첫 시험 대상으로 가장 적합하다.

### First Trial Scope

- `REV-99`는 runtime projection까지만 아니라
  - runtime projection
  - chunk sync
  - consolidated report
  까지 one chain으로 묶는 pilot autopilot trial로 승격하는 것이 좋다.

## rollout order

1. `Batch-11`로 autopilot first trial
2. 성공 시, 이후 green batch는 기본적으로 autopilot lane 사용
3. month/date-point/season 계열은 계속 yellow lane 유지
4. red signal이 나오는 family는 PM planning reopen

## self-review and reflection note

### Initial Framing

- 처음에는 autopilot을 `publish-only`까지만 자동화하는 좁은 모델로 볼 수 있었다.

### Self-Critique

- 하지만 그렇게 하면 PM이 여전히 chunk gate를 수동으로 다시 설계해야 해서 운영 이득이 작다.

### Revision

- 그래서 green autopilot의 끝점을 `chunk sync + consolidated report`까지 늘렸다.
- 대신 stop rule을 더 강하게 두고 yellow 승격을 명시했다.

### Reflection

- 현재 evidence만으로 green autopilot 설계는 충분하다.
- 추가 딥 리서치는 아직 필수 아님.
- 다만 yellow/red batch까지 autopilot에 넣으려는 순간에는 별도 리서치와 재설계가 필요하다.

## Conclusion

- green batch autopilot은 `PM arm -> internal build -> projection pack -> runtime projection -> chunk sync -> consolidated report -> review`까지 자동 흐름으로 설계하는 것이 가장 practical하다.
- 단, drift/mismatch/ambiguity 신호가 하나라도 나오면 즉시 yellow로 승격해야 한다.
- 첫 rollout은 `Calendar Label Batch-11` 재개가 가장 적합하다.
