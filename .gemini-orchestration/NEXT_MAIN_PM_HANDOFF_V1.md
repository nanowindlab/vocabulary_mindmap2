# Next Main PM Handoff V1

> Purpose: 다음 Main PM이 현재 프로젝트 상태를 빠르게 이어받기 위한 handoff
> Scope: `V1-REV-87` chunk rebuild gate 보고 제출까지 반영된 상태
> Date: `2026-03-15`

## 1. 먼저 읽을 문서

1. `README.md`
2. `PROJECT_DOCUMENT_MAP.md`
3. `.gemini-orchestration/MAIN_PM_ROLE_DEFINITION_V1.md`
4. `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
5. `.gemini-orchestration/WORK_ORCHESTRATION_HUB_V1.md`

## 2. 현재 authoritative 상태

- 대시보드가 유일한 control plane
- workboard는 snapshot
- append-only 로그가 실제 receipt/report evidence
- 최종 승인(`ACCEPT`, `DONE`, 배포)은 사용자 승인 필요

## 3. 현재까지 완료된 핵심 흐름

- `V1-REV-74`: relation model 재정의 proposal 완료
- `V1-REV-75`: data 구조/구현 영향 검토 완료
- `V1-REV-76`: review 비판 검토 완료
- `V1-REV-77`: implementation architecture proposal 완료
- `V1-REV-78`: canonical apply conformity review 완료
- `V1-REV-79`: pilot preparation proposal 완료
- `V1-REV-80`: `RELATION_GRAPH_CANONICAL_V1.json` empty skeleton 생성 완료
- `V1-REV-81`: pilot core 12 + holdout 4 population proposal 완료
- `V1-REV-82`: holdout ambiguity disambiguation rule 보고 제출, Main PM 내용 검토 완료
- `PRE-REV-83`: planning/review/development bounded survey dispatch 완료 (`REV-83`은 아직 unopened)
- `V1-REV-83`: survey 피드백을 guardrail로 흡수한 core 12 internal-only edge package 보고 제출 완료
- `V1-REV-84`: `REV-83` package-level acceptance review 보고 제출 완료, verdict `ACCEPT`
- `V1-REV-85`: projection gate package 보고 제출 완료
- `V1-REV-86`: pilot runtime projection 보고 제출 완료
- `V1-REV-87`: chunk rebuild gate 보고 제출 완료

## 4. 현재 활성 revision

- `V1-REV-87`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - pilot chunk rebuild gate를 닫고 search/tree/chunk 정합성을 확인
  - Result:
    - pilot ids `16/16` search/tree/chunk relation counts 일치
    - holdout 4 exclusion이 chunk layer까지 유지
    - pilot build cycle이 runtime chunk layer까지 완결
  - Guard:
    - 새 coverage expansion build 시작 금지
    - 새 개념 / 새 runtime contract 금지

- `V1-REV-86`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - `core12 + holdout4` pilot을 실제 runtime에 내려 검증
    - before/after snapshot, anchor bucket 대조, holdout exclusion 역추적을 한 번에 닫기
  - Result:
    - pilot runtime projection 성공
    - holdout 4 exclusion이 live runtime에서 유지
    - 남은 open issue가 chunk rebuild gate로 국한됨
  - Guard:
    - `publish-only`는 허용
    - `chunk rebuild`는 후속 gate로 분리
    - 새 개념 / 새 runtime contract 금지

- `V1-REV-85`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - `REV-83` accepted edge package를 projection-ready 상태로 끌고 가는 big-step data package
    - before snapshot / dry-run mapping / holdout exclusion proof를 한 번에 닫기
  - Result:
    - `dry_run_reserve.projection_preview`가 16 edge 전체를 커버
    - core12 + holdout4 before snapshot evidence 기록
    - holdout 4 projection-stage exclusion proof 확보
    - publish / rebuild / live overwrite 미실행 유지
  - Guard:
    - preview / dry-run evidence는 허용
    - `publish` 금지
    - `chunk rebuild` 금지
    - `live overwrite` 금지
    - 새 개념 / 새 runtime contract 금지

- `V1-REV-84`
  - Agent: 리뷰
  - Status: `REPORTED`
  - Purpose:
    - `REV-83` internal edge package에 대한 package-level acceptance review
    - 다음 projection gate 가능 여부와 guard set 판단
  - Result:
    - verdict `ACCEPT`
    - 다만 publish 직행이 아니라 projection gate package를 먼저 여는 것이 적절
  - Guard:
    - 새 개념 / 새 relation type / 새 runtime contract 금지
    - checklist-only review 금지
    - publish / rebuild / live overwrite 실행 금지

- `V1-REV-83`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - `core 12 anchor`만 대상으로 2차 edge 확장
    - holdout 4는 `node exists / edge 0` 유지
    - survey 피드백을 method / order / validation gate에 반영
  - Result:
    - edge count `4 -> 16`
    - holdout 4 incoming/outgoing edge `0`
    - duplicate pair 없음
    - reciprocal pair 누락 없음
    - required edge field 누락 없음
  - Guard:
    - write target은 `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`과 append-only 로그로 제한
    - `projection preview` 금지
    - `publish` 금지
    - `chunk rebuild` 금지
    - `live overwrite` 금지
    - dedup / reciprocal pair / `target_id` 검증 필수

- `V1-PRE-REV-83-PLAN`
  - Agent: 기획
  - Status: `REPORTED`
  - Purpose:
    - `REV-83` 직전 execution-method survey
    - scope / owner / gate blind spot만 점검
  - Guard:
    - 새 정의 / 새 개념 금지
    - 과거 planning 논의 회귀 금지

- `V1-PRE-REV-83-REVIEW`
  - Agent: 리뷰
  - Status: `REPORTED`
  - Purpose:
    - `REV-83` 직전 acceptance / failure mode / validation blind spot survey
  - Guard:
    - 새 acceptance contract 금지
    - `REV-82` 재심 금지

- `V1-PRE-REV-83-DEV`
  - Agent: 개발
  - Status: `REPORTED`
  - Purpose:
    - `REV-83` 직전 runtime / projection handoff risk survey
  - Guard:
    - 새 runtime contract 금지
    - 구현 / 배포 시작 금지

- `V1-REV-82`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - `오늘/어제` 명사-부사
    - `점심/저녁` 시간-식사
    의 holdout ambiguity 처리 기준 정리
  - Result:
    - holdout 4는 현재 `node seeded / edge held` 유지
    - `오늘/어제`는 noun-adverb sense boundary candidate
    - `점심/저녁(식사)`는 scene-side reserve candidate
  - Guard:
    - `projection preview` 금지
    - `publish-only` 금지
    - `chunk rebuild` 금지
    - `live overwrite` 금지

## 5. canonical에 이미 반영된 문서

- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `09_app/public/data/README.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `08_expansion/MASTER_ROADMAP_V1.md`

## 6. 중요한 산출물 위치

- planning proposal:
  - `.gemini-orchestration/workboard_archive/planning/20260314_REV74_relation_model_execution_closure_proposal.md`
- planning implementation architecture:
  - `.gemini-orchestration/workboard_archive/planning/20260314_REV77_implementation_architecture_proposal.md`
- review on apply:
  - `.gemini-orchestration/workboard_archive/review/20260314_REV78_canonical_apply_review_report.md`
- pilot preparation:
  - `.gemini-orchestration/workboard_archive/data/20260314_REV79_pilot_preparation_proposal.md`
- skeleton creation:
  - `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
  - `.gemini-orchestration/workboard_archive/data/20260314_REV80_skeleton_creation_report.md`
- pilot population:
  - `.gemini-orchestration/workboard_archive/data/20260314_REV81_pilot_population_report.md`
- holdout disambiguation:
  - `.gemini-orchestration/workboard_archive/data/20260314_REV82_holdout_disambiguation_report.md`
- REV-83 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV83_core12_edge_execution_assignment.md`
- REV-83 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV83_core12_edge_execution_report.md`
- REV-84 assignment:
  - `.gemini-orchestration/workboard_archive/review/20260315_REV84_core12_edge_package_acceptance_assignment.md`
- REV-84 report:
  - `.gemini-orchestration/workboard_archive/review/20260315_REV84_core12_edge_package_acceptance_report.md`
- REV-85 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV85_projection_gate_package_assignment.md`
- REV-85 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV85_projection_gate_package_report.md`
- REV-86 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV86_pilot_runtime_projection_assignment.md`
- REV-86 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV86_pilot_runtime_projection_report.md`
- REV-87 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV87_chunk_rebuild_gate_assignment.md`
- REV-87 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV87_chunk_rebuild_gate_report.md`
- pre-REV-83 survey assignments:
  - `.gemini-orchestration/workboard_archive/planning/20260314_PRE_REV83_execution_method_survey_assignment.md`
  - `.gemini-orchestration/workboard_archive/review/20260314_PRE_REV83_execution_method_survey_assignment.md`
  - `.gemini-orchestration/workboard_archive/development/20260314_PRE_REV83_execution_method_survey_assignment.md`

## 7. 현재 Main PM 판단 메모

- 문서/프로토콜 구조는 이미 충분히 정리됨
- `REV-82` 내용 검토 결과, holdout 4는 현재 단계에서 `node seeded / edge held` 유지가 타당함
- 전임 Main PM의 protocol mismatch는 control plane 동기화 범위에서만 복구했고, 내용 판단에는 반영하지 않음
- 사용자 요청에 따라 `REV-83` 직전의 bounded cross-agent survey를 먼저 수행함
- survey 목적은 새 개념 정의가 아니라 execution-method blind spot 점검임
- survey에서 나온 오류 가능성은 모두 무시하지 않고 `REV-83` guardrail로 흡수함
- `REV-83` 보고는 현재까지 artifact와 부합하며 internal-only package 범위를 지킴
- `REV-84` verdict는 수용하되, next action은 publish 직행이 아니라 projection gate package로 한 단계 분리하는 것이 맞다고 판단함
- `REV-85` 보고는 artifact와 부합하며 projection-ready claim을 뒷받침함
- `REV-86` pilot runtime projection은 성공했고, `REV-87`에서 chunk sync까지 닫힘
- pilot chain이 build -> acceptance -> projection -> chunk sync까지 한 사이클 완결됨
- 현재 단계의 용어는 `publish gate`보다 `pilot runtime projection`이 더 정확하다고 판단함
- 과도하게 micro revision을 쪼개는 문제를 인식하고 있음
  - 이후는 가능한 `work package` 단위로 더 크게 묶는 편이 좋음

## 8. 바로 다음 액션

- 다음 단계는 `coverage expansion build` work package 설계 및 개시 판단
- 판단 메모:
  - pilot chain은 충분히 검증되었으므로, 다음 큰 난제는 더 많은 단어에 같은 relation structure를 확장하는 package다
