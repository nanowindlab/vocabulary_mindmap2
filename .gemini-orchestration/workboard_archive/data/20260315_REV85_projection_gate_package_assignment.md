# Data Assignment Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-85`
> Logged: `2026-03-15 00:43:33`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-83` internal edge package는 `REV-84`에서 `ACCEPT`되었다.
- 다음 단계는 곧바로 publish가 아니라, **projection gate package**를 하나의 의미 있는 작업 단위로 수행하는 것이다.
- 데이터 에이전트는 이번 revision에서
  - 현재 internal canonical edge package가 thin projection으로 어떻게 내려갈지
  - holdout 4가 실제 projection에서도 계속 누락 없이 제외되는지
  - publish/rebuild 전 어떤 증거와 guard가 필요한지
  를 스스로 설계하고 입증해야 한다.

## Required Inputs

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV83_core12_edge_execution_report.md`
- `.gemini-orchestration/workboard_archive/review/20260315_REV84_core12_edge_package_acceptance_report.md`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/`

## Package Goal

- `REV-83` edge package를 **projection-ready** 상태로 끌고 간다.
- publish/rebuild는 하지 않되, 다음 publish gate에서 무엇이 어떻게 내려갈지와 어떤 위험이 남는지를
  artifact 기준으로 입증한다.

## Allowed Scope

- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`의 `dry_run_reserve` 및 projection-ready evidence 보강
- append-only preview / dry-run report 작성
- live runtime의 before snapshot 추출 및 비교 근거 작성
- thin projection 예상 결과를 bucket별(`related_vocab`, `cross_links`)로 정리

## Forbidden Scope

- `09_app/public/data/live/` overwrite 금지
- `run_rev47_xwd_mining.py --publish-only` 실행 금지
- `rebuild_rev23_detail_chunks.py` 실행 금지
- 실제 chunk / tree / search index 결과물 덮어쓰기 금지
- 새 개념 / 새 relation type / 새 runtime contract 제안 금지

## Work Package Expectation

- 이 revision은 checklist 수행이 아니라 아래를 한 번에 닫는 big step이다:
  - before snapshot evidence
  - projection preview / dry-run mapping
  - holdout 4 exclusion proof
  - runtime bucket expectation 정리
  - publish gate로 넘어가기 전 남은 조건 제안

## Required Outcome

- package-level projection gate memo
- before snapshot evidence for target anchors
- `dry_run_reserve.projection_preview` 보강 여부와 결과
- each REV83-added edge의 expected runtime bucket 정리
- holdout 4 exclusion proof at projection stage
- publish / rebuild 미실행 증거
- next recommendation:
  - publish gate를 열어도 되는지
  - 열면 어떤 최소 guard set이 필요한지
