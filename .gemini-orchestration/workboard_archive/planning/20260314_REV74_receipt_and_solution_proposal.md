# Planning Receipt And Solution Proposal

> Agent: `기획 에이전트`
> Revision: `V1-REV-74`
> Logged: `2026-03-14 18:01:50`
> Mode: `RECEIPT / START`
> Evidence Rule: `first append-only log counts as receipt/start evidence`

## Resync Basis

- authoritative control source: `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- assigned row: `V1-REV-74`
- workboard used as snapshot only: `.gemini-orchestration/PLANNING_AGENT_WORKBOARD_V1.md`
- control field note: `status`, `approval`, `Current Task`는 직접 수정하지 않음

## Rechecked Items

- Required Skills
  - `doc-state-manager`
  - `korean-lexical-data-curation`
- Read First
  - `README.md`
  - `PROJECT_DOCUMENT_MAP.md`
  - `ORCHESTRATION_DASHBOARD.md`
  - `08_expansion/README.md`

## Task Understanding

- 기준선 산출물 `V1-REV-70`, `V1-REV-72`, `V1-REV-73`을 재독해하는 planning cycle
- 목적은 다음 재빌드 사이클의 재검토 범위와 계획을 정리하는 것
- 이번 보고에서는 진단에만 머무르지 않고 바로 실행 가능한 planning 해결안을 제시함

## Planning Options

### Option 1
- 이름: `Policy Closure First`
- 요지: `SDCP`, `Relation Policy`, `Decision Log`를 먼저 닫고 그 다음 data rebuild를 여는 순서
- 장점:
  - 재빌드 기준이 가장 명확해짐
  - data/review 재작업 가능성이 가장 낮음
  - workboard의 `Validation Rule`과 가장 정합적임
- 리스크:
  - 문서 선행 정리가 필요해 초기 속도는 가장 느릴 수 있음

### Option 2
- 이름: `Parallel Draft`
- 요지: planning이 정책 수정안 초안을 내는 동안 data/review가 재검토 체크리스트를 병렬 준비
- 장점:
  - 총 리드타임이 짧아질 수 있음
  - 다음 handoff가 빠름
- 리스크:
  - policy closure 전 병렬 준비물이 기준 변경으로 다시 쓰일 가능성이 큼
  - control source가 dashboard 하나로 좁아진 현재 운영과는 긴장 관계가 있음

### Option 3
- 이름: `Data-First Probe`
- 요지: 소규모 샘플 재빌드 요구사항을 먼저 가정하고 planning은 그 결과를 보고 정책을 보강
- 장점:
  - 실제 문제 감각을 빠르게 잡을 수 있음
  - 현장성 있는 planning delta가 나올 수 있음
- 리스크:
  - 현재 workboard의 "파일 수정 없이 검토 범위 정의"와 맞지 않음
  - 잘못하면 기준 없는 실험이 되어 재검토 비용이 커짐

## Recommendation

- 추천안: `Option 1 - Policy Closure First`
- 추천 이유:
  - dashboard의 `[BASELINE-REPLAN]`과 workboard의 `Validation Rule`을 가장 보수적으로 만족함
  - planning agent가 먼저 해야 할 일은 재빌드 그 자체가 아니라 재빌드 기준의 closure이기 때문
  - 이후 data/review/dev handoff가 가장 깔끔해짐

## Proposed Default Resolution

1. planning이 먼저 정책 보완 대상 3개를 고정한다
   - `SDCP`
   - `Relation Policy`
   - `Decision Log`
2. 각 문서에 넣을 delta를 한 번에 패치 가능한 수준으로 정리한다
3. 그 결과를 data/review가 그대로 집행 가능한 재빌드 기준으로 넘긴다
4. data rebuild와 review acceptance가 끝난 뒤에만 dev 범위를 다시 연다

## Start Evidence

- 본 로그를 `V1-REV-74`의 지시접수 및 착수 증거로 남김
- 이후 진행 보고도 append-only 로그로만 남김
