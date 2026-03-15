# Batch Agent Operating Model V1

> Purpose: relation expansion/build work를 `한 배치 = 하나의 의미 있는 작업 단위`로 운영하기 위한 표준 모델
> Owner: Codex / Main PM
> Status: CURRENT

## 1. 왜 개선이 필요한가

지금까지의 흐름은 안전했지만, 다음 문제가 있었다.

- 같은 배치를 `planning -> data -> review -> projection -> chunk`로 매번 수동 sequencing해야 했다.
- 위험이 낮은 batch도 동일한 밀도의 revision을 사용해 revision 수가 빠르게 증가했다.
- PM이 매번 같은 종류의 gate를 다시 설계해야 했다.

따라서 개선 방향은 `사람을 빼는 자동화`가 아니라, 먼저 **반복 가능한 batch 타입과 예외 gate를 표준화**하는 것이다.

## 2. 핵심 개선 아이디어

현재 프로세스보다 더 효율적인 방법은 아래 두 가지를 함께 쓰는 것이다.

1. `batch type`을 먼저 분류한다.
2. `예외 기반 gate`로 어떤 batch를 압축할지 결정한다.

즉 모든 batch를 같은 절차로 처리하지 않고,

- 안전한 batch는 `one-batch-one-rev` 후보로 압축
- 애매한 batch는 planning/review gate를 먼저 통과
- 계약 자체를 흔드는 batch는 PM이 직접 재설계

로 나눈다.

## 3. Batch Type Taxonomy

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
  - ambiguity, holdout, reserve, inventory gap, family drift를 먼저 정리해야 하는 batch
- 예:
  - holdout disambiguation
  - season/weather drift
  - missing inventory(`일요일`) 처리
- 특징:
  - build보다 boundary 판정이 먼저
  - `one-batch-one-rev` 기본 비대상

### Type C. Projection-Sync Batch

- 정의:
  - internal canonical을 runtime/search/chunk에 실제 반영하는 execution gate batch
- 예:
  - projection gate
  - runtime projection
  - chunk rebuild gate
- 특징:
  - relation semantics는 바꾸지 않음
  - evidence 품질이 핵심

## 4. Gate Model

### Green Gate

- 조건:
  - `Type A`
  - validated family template reuse
  - holdout/reserve mutation 없음
  - node type / projection rule unchanged
  - target_id ambiguity 없음
- 처리:
  - 압축 운영 가능

### Yellow Gate

- 조건:
  - reserve touched
  - mixed-system family drift
  - inventory gap
  - unresolved surface duplication
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
  - batch agent 자동 운영 금지
  - PM/Codex planning reopen

## 5. One-Batch-One-Rev Rule

`one-batch-one-rev`는 하나의 data revision이 한 batch를 internal build부터 projection/chunk sync 직전 또는 완료까지 일관되게 처리할 수 있는 상태를 뜻한다.

적합 조건:

- `Type A`
- validated family template 재사용
- holdout / reserve / sentinel rule 고정
- write target 고정
- batch size가 proven envelope 안
- expected bucket / before snapshot 자동 생성 가능
- acceptance check가 기계 검증식으로 표현 가능

비적합 조건:

- holdout 해제 필요
- reserve family 진입 필요
- family drift 미정리
- preview bucket 새 정의 필요
- batch size가 proven envelope 초과

## 6. Agent Types And Skills

### Green Batch Agent

- role:
  - safe batch를 한 번에 처리하는 기본 실행 에이전트
- required skills:
  - `data-validation`
  - `korean-lexical-data-curation`
  - `multi-agent-orchestration`

### Yellow Exception Agent

- role:
  - ambiguity / reserve / drift를 먼저 정리해 green batch로 내릴 수 있게 만드는 에이전트
- required skills:
  - `doc-state-manager`
  - `korean-lexical-data-curation`
  - `data-validation`

### Review Gate Agent

- role:
  - package-level verdict와 residual risk를 판정
- required skills:
  - `report-verifier`
  - `data-validation`

## 7. PM Sequencing Rule

PM은 매번 `build -> review -> projection -> chunk`를 새로 설계하지 않는다.

PM이 먼저 결정할 것은 두 가지다.

1. 이 batch가 `Type A/B/C` 중 무엇인가
2. Green / Yellow / Red 중 어느 gate인가

기본 운영:

- `Type A + Green`
  - 가능한 한 압축 운영
- `Type B + Yellow`
  - planning/review 선행
- `Red`
  - PM 직접 재설계

## 8. Evidence Pack Standard

모든 batch는 아래 증거를 기본으로 남긴다.

- before snapshot
- holdout / reserve proof
- expected vs actual bucket
- search/tree/chunk consistency

추가:

- projection batch는 sentinel baseline
- exception batch는 ambiguity decision table

## 9. Recommended Rollout Order

1. `Type A + Green` batch를 먼저 반복
2. `Type B + Yellow` batch로 reserve/drift 해소
3. coverage를 점진적으로 넓힘
4. 충분한 coverage 이후 대규모 전수 단계(`T2.16`, `T2.17`) 진입

## 10. Current Recommendation

현재 프로젝트에는 아래 운영이 적합하다.

- `Calendar Continuity Batch-14`까지는 proven green path
- 다음 time-anchor 확장도 동일 조건이면 green batch 후보
- season/weather, missing inventory, surface ambiguity는 yellow batch로 먼저 분리

## 11. Operational Rule

다음 batch를 열 때 PM은 아래만 보면 된다.

1. `Type A/B/C`
2. Green / Yellow / Red
3. evidence pack requirements
4. current holdout / reserve impact

이 네 가지가 정해지면, 그 이후 sequencing은 최대한 표준화한다.
