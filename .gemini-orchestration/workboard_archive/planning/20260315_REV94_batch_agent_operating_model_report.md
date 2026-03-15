# Batch-Agent Operating Model Memo

> Agent: `기획 에이전트`
> Revision: `V1-REV-94`
> Logged: `2026-03-15`
> Status: `PROPOSAL / NOT YET APPLIED`
> Purpose: pilot + Batch-14로 검증된 build chain을 더 효율적으로 운영하기 위한 batch-agent operating model 제안
> Guard: 새 relation semantics / validated contract 재개방 / 아이디어 나열 금지

## 문제 재정의

pilot과 Batch-14는 아래를 증명했다.

- internal canonical write target 고정
- holdout / reserve / sentinel control 가능
- projection gate와 chunk rebuild gate 분리 가능
- batch 단위 evidence pack이 실제로 유효함

`REV-94`의 문제는 이제 “다음 batch를 또 같은 5개 revision 묶음으로 수동 sequencing할 것인가”가 아니라, **어떤 batch는 축약 가능하고 어떤 batch는 예외 gate를 반드시 거쳐야 하는지**를 운영 규칙으로 고정하는 것이다.

## Web Research Basis

- [Argo Rollouts Canary](https://argo-rollouts.readthedocs.io/en/stable/features/canary/)
- [Oxford 3000/5000 Wordlists](https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000)

실무 해석:

- rollout은 “한 번에 다 넘기기”보다 promotion gate와 analysis를 단계적으로 두는 방식이 더 안전하다.
- learner vocabulary도 core-first progression이 기본이므로, batch 역시 high-value / low-ambiguity부터 green lane으로 흘려야 한다.

## batch type taxonomy

### Type A. Template-Extension Batch

- 정의:
  - 이미 검증된 family template 안에서 node/edge coverage만 확장하는 batch
- 예:
  - `core12`
  - `Calendar Continuity Batch-14`
- 특징:
  - semantics unchanged
  - node type unchanged
  - holdout/reserve untouched
  - projection rule unchanged

### Type B. Exception-Resolution Batch

- 정의:
  - ambiguity, holdout, reserve, inventory gap, family drift를 다루는 batch
- 예:
  - `REV-82` holdout disambiguation
  - season/weather drift 처리
  - missing inventory(`일요일`) 보강
- 특징:
  - build보다 boundary 판정이 먼저
  - one-batch-one-rev 비대상

### Type C. Projection-Sync Batch

- 정의:
  - internal canonical을 runtime과 chunk에 실제 반영하는 execution gate batch
- 예:
  - projection gate package
  - runtime projection gate
  - chunk rebuild gate
- 특징:
  - relation semantics는 안 바꿈
  - evidence pack의 품질이 핵심

## exception-based gate model

### Green Gate

- 조건:
  - Type A
  - validated family template reuse
  - holdout/reserve mutation 없음
  - node type / projection rule unchanged
  - target_id ambiguity 없음
- 처리:
  - compressed flow 허용

### Yellow Gate

- 조건:
  - reserve touched
  - mixed-system family drift 존재
  - inventory gap 존재
  - target surface duplication 있지만 current contract 안에서 처리 가능
- 처리:
  - planning or review gate 선행
  - publish/rebuild 직행 금지

### Red Gate

- 조건:
  - semantics reopening 필요
  - new relation type 필요
  - new node type 필요
  - runtime contract 변경 필요
- 처리:
  - batch agent 자동 진행 금지
  - PM/Codex planning reopen

## one-batch-one-rev eligibility rule

### Definition

- one-batch-one-rev는 **하나의 data revision이 하나의 batch를 internal build부터 projection/chunk sync 직전 또는 완료까지 일관되게 처리할 수 있는 상태**를 뜻한다.
- review verdict는 별도 revision으로 남겨도 된다.

### Eligibility Conditions

1. batch type이 `Template-Extension Batch`일 것
2. validated family template를 그대로 재사용할 것
3. holdout / reserve / sentinel rule이 이미 고정돼 있을 것
4. write target이 `RELATION_GRAPH_CANONICAL_V1.json` + script-driven outputs로 제한될 것
5. batch size가 현재 proven envelope 안에 있을 것
   - 기준:
     - new nodes `<= 14`
     - new edges `<= 28`
     - 또는 마지막 accepted green batch와 동급
6. before snapshot / expected bucket / sentinel baseline을 자동 생성 가능할 것
7. publish-only 후 chunk rebuild까지의 검증표를 기존 checklist로 커버할 수 있을 것

### Non-Eligible Conditions

- holdout 해제 필요
- reserve family 진입 필요
- family drift가 아직 정리되지 않음
- preview bucket을 새로 정의해야 함
- batch size가 proven envelope를 넘음

## batch agent skill map

### Green Batch Agent

- required:
  - `data-validation`
  - `korean-lexical-data-curation`
  - `multi-agent-orchestration`
- mission:
  - internal build
  - projection evidence
  - publish-only
  - chunk rebuild
  - evidence pack 작성

### Yellow Exception Agent

- required:
  - `doc-state-manager`
  - `korean-lexical-data-curation`
  - `data-validation`
- mission:
  - ambiguity / reserve / drift를 먼저 정리
  - green batch로 내릴 수 있을지 판단

### Review Gate Agent

- required:
  - `report-verifier`
  - `data-validation`
- mission:
  - package-level acceptance
  - residual risk 판정
  - next gate 개시 여부 판정

## PM sequencing rule

### Rule 1. PM은 batch definition과 verdict에만 집중

- PM이 매번 `build -> review -> projection -> chunk`를 수동 설계하지 않는다.
- PM은 아래 두 가지만 결정한다.
  - 이 batch가 `A/B/C` 중 무엇인가
  - Green / Yellow / Red 중 어느 gate인가

### Rule 2. Green은 압축, Yellow는 분리

- Green:
  - data batch를 크게 묶는다
  - review는 package-level verdict만 분리
- Yellow:
  - planning/review를 먼저 연다
  - data build는 그 뒤에 연다

### Rule 3. Red는 운영 모델 바깥

- Red는 batch agent로 처리하지 않는다
- PM/Codex가 planning reopen

## recommended rollout order

### Stage 1. Green batch 연속 구간

- current validated contract를 그대로 재사용할 수 있는 family부터 확장
- 기준:
  - high learner navigation value
  - low ambiguity
  - low validation cost

### Stage 2. Yellow batch 구간

- reserve / family drift / missing inventory 처리
- 예:
  - `season/weather`
  - `일요일`

### Stage 3. Coverage program

- green과 yellow를 반복 가능한 cadence로 운영
- batch별 baseline을 박제하며 coverage를 넓힘

### Stage 4. Full-scale T2.16 / T2.17

- 충분한 family coverage와 exception policy가 쌓인 뒤 전수 재분류와 anchor 확장으로 진입

## practical operating rule set

### Default Rule

- 새 batch는 먼저 `Type A/B/C`로 분류한다.
- `Type A + Green`이면 one-batch-one-rev 후보로 본다.
- 그 외는 분리 revision으로 처리한다.

### Evidence Rule

- 모든 batch는 아래 4종을 남긴다.
  - before snapshot
  - holdout/reserve proof
  - expected vs actual bucket
  - search/tree/chunk consistency

### Stop Rule

- 아래 중 하나면 즉시 yellow/red로 승격
  - holdout touched
  - reserve drift
  - sentinel drift
  - target_id ambiguity
  - batch envelope 초과

## owner documents and patch targets

### Primary

- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
  - `T1.35` owner
- `.gemini-orchestration/workboard_archive/planning/`
  - execution memo owner

### Secondary

- `08_expansion/MASTER_ROADMAP_V1.md`
  - green/yellow batch cadence가 장기 운영 축으로 자리잡으면 status note 반영 가능

### No Patch Target In This Revision

- `RELATION_DATA_POLICY_V1.md`
- `APP_DATA_REDEPLOY_SOP_V1.md`

사유:

- 이번 revision은 semantics나 runtime 절차를 다시 바꾸는 단계가 아니라, 이미 검증된 절차를 어떤 batch에 압축 적용할지 정하는 단계다.

## self-review and reflection note

### Initial Framing

- 처음에는 batch type을 build/review/publish/chunk 기준으로 더 세분화하려 했다.

### Self-Critique

- 하지만 그러면 운영 모델이 다시 micro-step checklist로 퇴행한다.
- 이번 revision의 목적은 오히려 PM sequencing을 줄이는 데 있다.

### Revision

- 그래서 batch type은 `A/B/C`
- gate는 `Green/Yellow/Red`
- sequencing rule은 `Green 압축 / Yellow 분리 / Red reopen`
  으로 단순화했다.

### Reflection

- 현재 evidence만으로 `REV-94` 운영 모델을 닫는 데 추가 딥 리서치는 필수 아님.
- 다만 red gate 비율이 늘거나, non-word node 운영이 시작되면 그때는 추가 딥 리서치가 유의미하다.

## Conclusion

- `REV-94`의 핵심 결론은
  - `Type A/B/C batch taxonomy`
  - `Green/Yellow/Red gate model`
  - `one-batch-one-rev eligibility`
  - `PM sequencing simplification`
  이 네 가지다.
- 이 모델이 있으면 다음 batch부터는 매번 full custom sequencing을 다시 쓰지 않고도 운영 가능하다.
