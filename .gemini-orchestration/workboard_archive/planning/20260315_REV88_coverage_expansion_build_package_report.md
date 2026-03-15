# Coverage Expansion Build Package Memo

> Agent: `기획 에이전트`
> Revision: `V1-REV-88`
> Logged: `2026-03-15`
> Status: `PROPOSAL / NOT YET APPLIED`
> Purpose: pilot relation cycle 이후 첫 `coverage expansion build`를 data agent가 바로 집행 가능한 big-step package로 설계
> Guard: 새 relation semantics / pilot contract 재개방 / 과거 planning 회귀 금지

## 문제 재정의

pilot은 relation 구조가 동작한다는 것을 증명했다. `REV-88`의 문제는 relation model의 타당성을 다시 논하는 것이 아니라, **pilot에서 검증된 build-projection-rebuild chain을 더 큰 범위로 확장할 때 어디까지를 한 package로 묶어도 품질이 유지되는가**를 정하는 것이다.

이번 planning이 닫아야 하는 것은 다음이다.

- 첫 expansion batch를 어떤 원칙으로 자를지
- ambiguity / holdout / family drift를 어떻게 동시에 통제할지
- internal build -> projection -> chunk rebuild를 어떤 gate로 반복할지
- review/dev handoff를 어디서 열고 어디서 닫을지

## 왜 expansion이 hardest stage인지

pilot에서는 `core 12 + holdout 4`라는 bounded package 덕분에

- write target 고정
- holdout mask 유지
- before/after snapshot
- projection proof
- chunk sync proof

를 상대적으로 작은 비용으로 닫을 수 있었다.

expansion에서는 이 5가지가 동시에 어려워진다.

1. **coverage difficulty**
   - 단어 수만 늘리는 것이 아니라, learner navigation value가 높은 family를 골라야 한다.
2. **ambiguity difficulty**
   - surface duplication, family drift, missing inventory가 batch 중간에 섞이기 시작한다.
3. **validation difficulty**
   - batch가 커질수록 holdout leak, non-target spillover, search/tree/chunk mismatch를 놓치기 쉬워진다.
4. **reason consistency difficulty**
   - pilot 이후에는 edge 수보다 family-level reason consistency가 더 중요해진다.

## Web Research Basis

- [Korean-English Learners' Dictionary](https://krdict.korean.go.kr/eng)
- [Korean Basic Dictionary feature reference](https://krdict.korean.go.kr/kor/dicSearch/SearchView?ParaWordNo=83940)
- [Nuri-King Sejong Institute learning dictionary](https://nuri.iksi.or.kr/front/cms/contents/layout2/learningdictionary/contentsList.do)

실무 해석:

- 공식 학습자용 사전/서비스는 `시간 표현`, `날짜`, `요일`, `약속`을 한 덩어리의 navigation hub로 다룬다.
- 반면 `날씨/계절`은 separate hub로 분리되는 경향이 강하다.
- 따라서 first expansion batch는 **schedule/calendar continuity**를 먼저 확장하고, `season/weather drift`는 reserve로 두는 것이 learner value와 validation cost의 균형이 가장 좋다.

## batching strategy options (최대 3개)

### Option 1. Recommended: Calendar Continuity Batch

- 범위:
  - `relative_day`
  - `day_part`
  - `week_frame`
- 장점:
  - pilot과 같은 `시간과 흐름` 축 안에서 확장되므로 runtime-safe
  - learner navigation value가 높다
  - family reason template를 통일하기 쉽다
  - holdout 4와 직접 충돌이 적다
- 리스크:
  - `일요일` missing inventory가 남는다
  - season family는 다음 batch로 미뤄진다

### Option 2. Season-Inclusive Time Batch

- 범위:
  - Option 1 + `season_anchor`
- 장점:
  - coverage 체감이 크다
  - 계절/날씨 쪽 learner interest를 빠르게 잡을 수 있다
- 리스크:
  - `봄/여름`은 `구조와 기초`, `가을/겨울`은 `상황과 장소`에 있어 family drift가 크다
  - projection/review cost가 pilot 대비 급증한다

### Option 3. Broad Time-Root Sweep

- 범위:
  - `시간과 흐름` 루트 잔여 후보를 대량 확장
- 장점:
  - coverage를 가장 빨리 늘릴 수 있다
- 리스크:
  - micro ambiguity와 validation cost가 한 번에 폭증한다
  - big-step처럼 보이지만 실제로는 data/review가 다시 micro triage를 해야 한다

## 추천안

### Final Recommendation

- `Option 1: Calendar Continuity Batch`

### 추천 이유

pilot에서 이미 닫힌 contract는

- noun-sense target 안전성
- holdout exclusion
- `internal_canonical_overlay`
- publish -> chunk rebuild gate

이다.

이를 그대로 유지하면서 가장 큰 coverage gain을 얻는 범위는 **relative day / day part / week frame**이다.

이 범위는

- 같은 `시간과 흐름` root에 주로 머물고
- 공식 learner resource의 `시간/날짜/요일/약속` navigation cluster와도 맞으며
- season/weather처럼 system drift가 큰 family를 건드리지 않는다.

## first expansion batch definition

### Batch Name

- `Calendar Continuity Batch-14`

### Included New Nodes

#### relative_day_add (4)

- `그제_일반명사-1`
- `그저께_일반명사-1`
- `다음날_일반명사-1`
- `당일_일반명사-1`

#### day_part_add (4)

- `새벽_일반명사-1`
- `오전_일반명사-1`
- `낮_일반명사-1`
- `오후_일반명사-1`

#### week_frame_add (6)

- `화요일_일반명사-1`
- `수요일_일반명사-1`
- `목요일_일반명사-1`
- `토요일_일반명사-1`
- `주중_일반명사-1`
- `평일_일반명사-1`

### Explicit Reserve For Batch 2+

- holdout 유지:
  - `오늘_일반부사-1`
  - `어제_일반부사-1`
  - `점심_일반명사-1`
  - `저녁_일반명사-2`
- family drift reserve:
  - `가을_일반명사-1`
  - `겨울_일반명사-1`
  - `계절_일반명사-1`
  - `사계절_일반명사-1`
- inventory gap reserve:
  - `일요일` (current live index missing)

### Batch Selection Rule

- new node는 아래를 모두 만족해야 한다.
  1. current live에 actual node가 존재
  2. noun-sense 단위가 분명함
  3. holdout family에 속하지 않음
  4. 기존 pilot node와 최소 1개 이상 의미 있는 family 연결이 가능함
  5. family drift가 system-level로 터지지 않음

## ambiguity / holdout / exception handling

### 1. Holdout Rule

- existing holdout 4는 그대로 유지
- `node exists / edge 0`를 current invariant로 고정
- 이번 batch에서 holdout 해제 금지

### 2. Exception Queue Rule

- 아래 항목은 `exception_queue`로 분리
  - missing inventory
  - mixed-system family drift
  - duplicate surface with unresolved alternative sense
  - 신규 edge가 current pilot family template로 설명되지 않는 후보

### 3. Family-Level Reason Consistency Rule

- family마다 reason template를 1개로 묶는다.

#### relative_day

- template:
  - `today-centered relative offset`

#### day_part

- template:
  - `within-day sequence / boundary transition`

#### week_frame

- template:
  - `weekly schedule progression / weekday-weekend segmentation`

- 금지:
  - 한 family 안에 unrelated scene rationale를 섞는 것
  - 같은 family 내 일부 edge만 ad-hoc reason을 쓰는 것

### 4. Edge Budget Rule

- first expansion batch는 `new nodes 14`, `new edges 20~28` 범위로 제한
- 이유:
  - pilot(12 nodes / 16 edges)의 검증 비용을 넘어가되
  - review가 package-level reason consistency를 아직 읽을 수 있는 범위여야 함

## gate sequence and evidence plan

### Gate 0. Batch Freeze

- output:
  - included 14 nodes
  - reserve queue
  - family templates
- evidence:
  - batch roster appendix
  - reserve appendix

### Gate 1. Internal Build

- write target:
  - `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- actions:
  - node add
  - edge add
  - dry_run_reserve update
- evidence:
  - before/after internal graph counts
  - holdout outgoing/incoming `0`
  - exception queue untouched

### Gate 2. Internal Acceptance Review

- review checks:
  - duplicate pair `0`
  - reciprocal pair missing `0`
  - required field missing `0`
  - family template mismatch `0`
  - holdout leak `0`

### Gate 3. Projection Gate Package

- actions:
  - batch ids before snapshot
  - expected runtime bucket preview
  - non-target sentinel snapshot
- evidence:
  - `batch_id | before related/cross | expected related/cross`
  - sentinel control unchanged baseline

### Gate 4. Publish-Only Overlay

- command:
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
- evidence:
  - overlay mode success
  - batch ids actual bucket == expected bucket
  - reserve/holdout actual `0/0`
  - sentinel non-target sample unchanged

### Gate 5. Chunk Rebuild

- command:
  - `python3 scripts/core/rebuild_rev23_detail_chunks.py`
- evidence:
  - batch ids search/tree/chunk relation count 일치
  - holdout 4 search/tree/chunk `0/0`
  - chunk manifest regenerated

### Gate 6. Expansion Review Acceptance

- review checks:
  - batch package가 pilot contract를 깨지 않았는가
  - family-level reason consistency가 유지되는가
  - non-target spillover가 없는가
  - next batch로 넘어갈 만큼 validation cost가 통제 가능한가

## acceptance criteria and evidence plan

### Mandatory Acceptance Criteria

- included batch nodes만 신규 edge-bearing 대상
- holdout 4 unchanged
- reserve queue untouched
- reciprocal completeness `100%`
- duplicate pair `0`
- family template mismatch `0`
- batch ids expected/actual bucket match `100%`
- batch ids search/tree/chunk consistency `100%`
- non-target sentinel drift `0`

### Evidence Pack

- internal graph delta summary
- holdout proof
- reserve queue proof
- before/after snapshot table
- expected bucket table
- publish summary
- search/tree/chunk comparison table
- sentinel control table

## owner documents and patch targets

### Primary

- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
  - `T2.23`를 `coverage expansion build package` 수준으로 구체화
- `.gemini-orchestration/workboard_archive/planning/`
  - current execution brief owner

### Secondary

- `08_expansion/MASTER_ROADMAP_V1.md`
  - current hardest stage가 `coverage expansion build`임을 status note로 반영 가능
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
  - expansion package용 `sentinel control evidence`를 추가할지 검토 가능

### No Patch Target In This Revision

- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`

사유:

- 이번 revision은 semantics나 contract를 바꾸는 단계가 아니라, validated contract 위에서 batch execution package를 설계하는 단계다.

## data/review/dev handoff design

### Planning -> Data

- 전달물:
  - batch roster
  - reserve queue
  - family reason templates
  - edge budget
  - gate sequence
  - evidence pack template

### Data -> Review

- 전달물:
  - internal graph delta
  - family-level reason summary
  - holdout/reserve proof
  - before/after batch snapshot
  - sentinel control diff

### Review -> Development

- 기본값:
  - no dev reopen
- reopen 조건:
  - batch runtime projection이 current UI contract에서 의미 손실 또는 regress를 만들었을 때만
- current recommendation:
  - `REV-88` package는 data/review loop로 닫고 dev는 열지 않는다

## self-review and reflection note

### Initial Framing

- 처음에는 season family까지 함께 넣는 broad time pack을 고려했다.

### Self-Critique

- 하지만 `봄/여름`과 `가을/겨울`의 current system drift를 first batch에 넣으면
  - family consistency
  - ambiguity control
  - projection validation
  비용이 동시에 뛰어오른다.

### Revision

- 따라서 first batch를 `calendar continuity`로 줄이고
- season/weather는 reserve로 남겼다.

### Reflection

- 현재 evidence만으로 `REV-88`을 여는 데 외부 딥 리서치는 필요하지 않다.
- official learner resource의 시간/날짜/요일/약속 cluster 근거와 local pilot proof로 practical build package를 충분히 설계할 수 있다.
- 다만 season/weather family를 열거나 non-word scene/grammar node를 operational type으로 올릴 때는 추가 딥 리서치가 다시 유의미해질 수 있다.

## Conclusion

- first expansion batch는 `Calendar Continuity Batch-14`가 가장 practical하다.
- 이 batch는 pilot contract를 유지하면서 coverage를 넓히고, ambiguity/validation cost를 통제할 수 있다.
- `REV-88`의 핵심은 semantics가 아니라 **family-consistent expansion + gated execution**이며, 위 package는 그 조건을 충족한다.
