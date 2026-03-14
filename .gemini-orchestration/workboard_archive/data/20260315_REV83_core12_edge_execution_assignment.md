# Data Assignment Log

> Agent: `데이터 에이전트`
> Revision: `V1-REV-83`
> Logged: `2026-03-15 00:07:07`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-82`의 holdout ambiguity 결론과 `PRE-REV-83` survey 피드백을 모두 고정 입력으로 받아,
  `core 12 anchor`만 대상으로 하는 **internal-only 2차 edge execution package**를 수행한다.
- 이번 revision의 목적은 `RELATION_GRAPH_CANONICAL_V1.json` 내부에서만 edge 확장을 닫고,
  holdout 4를 계속 `node seeded / edge held`로 유지한 채 다음 projection gate로 넘길 수 있는
  검증 가능한 내부 산출물을 만드는 것이다.

## Required Inputs

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260314_REV81_pilot_population_report.md`
- `.gemini-orchestration/workboard_archive/data/20260314_REV82_holdout_disambiguation_report.md`
- `.gemini-orchestration/workboard_archive/planning/20260315_PRE_REV83_execution_method_survey_report.md`
- `.gemini-orchestration/workboard_archive/review/20260314_PRE_REV83_execution_method_survey_report.md`
- `.gemini-orchestration/workboard_archive/review/20260315_PRE_REV83_execution_method_survey_report.md`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`

## Fixed Goal

- `core 12 anchor`만 edge-bearing 대상으로 취급한다.
- holdout 4(`오늘_일반부사-1`, `어제_일반부사-1`, `점심_일반명사-1`, `저녁_일반명사-2`)는
  이번 revision 내내 `node exists / edge 0` 상태를 유지한다.
- `projection preview`, `publish`, `chunk rebuild`, `live overwrite`는 이번 revision 범위에 포함되지 않는다.

## Mandatory Execution Order

1. 현재 skeleton / nodes / edges 기준선 재확인
2. core 12 node inventory 고정 재확인
3. holdout 4 mask 적용 상태 재확인
4. holdout 4 outgoing / incoming edge count가 모두 `0`인지 먼저 검증
5. core 12 대상 2차 edge candidate 생성
6. 기존 internal edge와 live string-derived overlap 기준으로 dedup 수행
7. `required_edge_fields` 완전성 및 reciprocal pair 충족 여부 검증
8. `target_id`가 의도한 명사형 sense에 정확히 매핑되는지 수동 점검 근거 작성
9. append-only 보고 제출

## Required Outcome

- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json` 업데이트
- core 12 edge delta 요약
- holdout 4 edge count `0` 증거
- dedup 근거
- `required_edge_fields` / reciprocal pair / `target_id` 정확성 검증 근거
- no-execution evidence:
  - `projection preview` 미실행
  - `publish` 미실행
  - `chunk rebuild` 미실행
  - `live overwrite` 미실행

## Forbidden Scope

- `09_app/public/data/live/` 직접 수정 금지
- `run_rev47_xwd_mining.py --publish-only` 실행 금지
- `rebuild_rev23_detail_chunks.py` 실행 금지
- `projection preview` 산출물 생성 금지
- holdout 4에 edge 추가 금지
- 새 정의 / 새 개념 / 새 relation type 제안 금지

## Additional Guard

- survey에서 제기된 오류 가능성은 모두 무시하지 말고 method / order / validation gate에 반영할 것
- 특히 아래 항목은 보고서 본문에 명시적으로 포함할 것:
  - internal-only write target 고정
  - holdout 4 mask 선적용
  - dedup 처리 방식
  - reciprocal pair 충족 여부
  - `target_id` 수동 검증 결과
  - 다음 단계의 projection gate로 넘길 때 필요한 snapshot requirement는 future gate로 분리
