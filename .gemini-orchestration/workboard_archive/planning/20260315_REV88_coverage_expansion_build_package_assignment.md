# Planning Assignment Log

> Agent: `기획 에이전트`
> Revision: `V1-REV-88`
> Logged: `2026-03-15 01:31:51`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- pilot relation cycle은 `REV-87`까지 검증 완료되었다.
- 다음 큰 단계는 더 많은 단어에 같은 relation structure를 확장하는 `coverage expansion build`다.
- 이번 revision의 역할은 단순 TODO 분해가 아니라,
  - 어떤 범위를 첫 expansion batch로 잡을지
  - ambiguity / holdout / family consistency를 어떻게 통제할지
  - expansion build 이후 projection / rebuild gate를 어떤 단위로 묶을지
  를 하나의 planning package로 설계하는 것이다.

## Required Inputs

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/PLANNING_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV87_chunk_rebuild_gate_report.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV86_pilot_runtime_projection_report.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `08_expansion/MASTER_ROADMAP_V1.md`
- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`

## Package Goal

- `coverage expansion build`를 실행 가능한 work package로 설계한다.
- 아래를 한 번에 닫아야 한다:
  - expansion batch selection rule
  - ambiguity / holdout control strategy
  - family-level reason consistency rule
  - expansion build -> runtime projection -> chunk rebuild gate sequence
  - acceptance / evidence requirements

## Required Planning Depth

- `REV-77` implementation architecture proposal처럼, 단순 범위 정리가 아니라
  **"다음 hardest stage를 어떤 구조로 집행할지"**를 닫는 수준의 planning이 필요하다.
- 따라서 아래를 모두 포함해야 한다:
  1. 왜 pilot 다음에 expansion이 어려운지에 대한 package-level diagnosis
  2. expansion batch를 자르는 원칙
  3. 추천 first batch와 그 이유
  4. ambiguity / holdout / exception queue 운영 방식
  5. build -> pilot runtime projection -> chunk rebuild gate의 반복 구조
  6. owner 문서별 반영 위치
  7. data / review / development handoff 순서

## Required Output Structure

- 아래 섹션을 가진 memo로 제출할 것:
  - `문제 재정의`
  - `왜 expansion이 hardest stage인지`
  - `batching strategy options (최대 3개)`
  - `추천안`
  - `first expansion batch definition`
  - `ambiguity / holdout / exception handling`
  - `gate sequence and evidence plan`
  - `owner documents and patch targets`
  - `data/review/dev handoff design`
  - `남은 리스크와 reflection`

## Required Reasoning Cycle

- 단일 초안으로 끝내지 말 것
- 최소 아래 순서를 거친 뒤 최종안 제출:
  1. initial package framing
  2. self-critique
  3. revision
  4. reflection note

## Hard Guard

- 새 relation semantics 발명 금지
- pilot에서 닫힌 contract를 다시 흔드는 것 금지
- micro-step TODO 나열로 끝내지 말 것
- planning package는 data agent가 바로 집행 가능한 big-step이어야 함
- 의미 없는 “단어 수만 늘리기”식 배치 제안 금지
- batch는 learner navigation / ambiguity risk / validation cost를 함께 고려해 설계할 것

## Required Outcome

- coverage expansion build package memo
- 첫 expansion batch 제안
- batch selection rationale
- ambiguity / holdout handling plan
- build/projection/rebuild gate sequence
- acceptance criteria and evidence plan
- 추천안 / 장점 / 리스크가 포함된 package-level proposal
- self-review와 reflection note
