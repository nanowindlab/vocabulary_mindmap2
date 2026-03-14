# Data Assignment Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-86`
> Logged: `2026-03-15 01:05:34`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-85`까지는 internal build와 projection-ready evidence를 닫았다.
- 이번 revision은 그 pilot을 실제 runtime으로 내려 검증하는 **pilot runtime projection** package다.
- 목적은 전체 구축이 아니라, 현재 `core 12 + holdout 4` pilot이
  - thin projection을 거쳐 live runtime에서 의도대로 내려가는지
  - holdout 4 exclusion이 실제 runtime에서도 유지되는지
  - target anchor 12개가 기대 bucket(`related_vocab` / `cross_links`)에 맞게 반영되는지
  를 한 번에 검증하는 것이다.

## Required Inputs

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV83_core12_edge_execution_report.md`
- `.gemini-orchestration/workboard_archive/review/20260315_REV84_core12_edge_package_acceptance_report.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV85_projection_gate_package_report.md`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/`

## Package Goal

- `core 12 + holdout 4` pilot의 runtime projection을 실제로 실행하고,
  그 결과를 artifact 기준으로 검증한다.
- 단, 이번 revision은 **projection까지만** 포함한다.
- `chunk rebuild`는 후속 gate로 분리한다.

## Allowed Scope

- publish-only 실행
- publish 직전 before snapshot 재고정
- live search/tree 결과 대조
- holdout 4 exclusion 역추적 검증
- append-only runtime projection report 작성

## Forbidden Scope

- `chunk rebuild` 실행 금지
- live projection 검증이 끝나기 전에 다음 coverage expansion으로 넘어가기 금지
- 새 개념 / 새 relation type / 새 runtime contract 제안 금지

## Work Package Expectation

- 이 revision은 단순 실행이 아니라 아래를 한 번에 닫는 big step이다:
  - before snapshot 재고정
  - actual pilot runtime projection
  - target anchor 12개 projected bucket 대조
  - holdout 4 exclusion 역추적
  - publish success / failure interpretation
  - chunk rebuild 전까지 남은 후속 gate 제안

## Required Outcome

- pilot runtime projection report
- before / after snapshot evidence
- target anchor 12개 projected bucket actual vs expected 비교
- holdout 4 exclusion proof in live runtime
- publish-only executed evidence
- chunk rebuild not executed evidence
- next recommendation:
  - chunk rebuild gate를 열어도 되는지
  - coverage expansion build로 넘어가기 전 필요한 조건이 무엇인지
