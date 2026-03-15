# Next Main PM Handoff V1

> Purpose: 다음 Main PM이 현재 프로젝트 상태를 빠르게 이어받기 위한 handoff
> Scope: `V1-REV-102` comparison autopilot abort와 post-abort baseline/runtime consistency repair까지 반영된 상태
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
- 현재 investigation phase의 sequencing과 runtime consistency 복구는 Codex/Main PM이 직접 주도하고, multi-agent workboard는 증거/기록 용도로 유지

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
- `V1-REV-88`: coverage expansion build planning 보고 제출 완료
- `V1-REV-89`: `Calendar Continuity Batch-14` data build 보고 제출 완료
- `V1-REV-90`: `Calendar Continuity Batch-14` internal acceptance review 보고 제출 완료, verdict `ACCEPT`
- `V1-REV-91`: Batch-14 projection gate package 보고 제출 완료
- `V1-REV-92`: Batch-14 runtime projection gate 보고 제출 완료
- `V1-REV-93`: Batch-14 chunk rebuild gate 보고 제출 완료
- `V1-REV-94`: batch-agent operating model planning 보고 제출 완료
- `V1-REV-95`: next green batch selection planning 보고 제출 완료
- `V1-REV-96`: `Calendar Label Batch-11` data build 보고 제출 완료
- `V1-REV-97`: `Calendar Label Batch-11` internal acceptance review 보고 제출 완료, verdict `ACCEPT`
- `V1-REV-98`: Calendar Label Batch-11 projection gate package dispatch 완료
- `V1-REV-100`: Green Batch Autopilot design 보고 제출 완료
- `V1-REV-101`: Green Batch Agent first trial dispatch 완료
- `V1-REV-102`: `Calendar Label Batch-11` comparison autopilot rerun 결과 `AUTOPILOT_ABORTED_TO_YELLOW`; duplicate-id / sentinel drift 이슈 노출
- post-`REV-102`: live split/search duplicate-id `29`건이 runtime projection/replace 단계에서 유입된 것으로 확인했고, local baseline/runtime consistency를 `8094` unique ids 기준으로 복구함
- post-`REV-102`: `scripts/core/rebuild_rev23_detail_chunks.py`는 duplicate live input을 조기 실패시키도록 hard-fail guard를 추가함

## 4. 현재 활성 초점

- `Yellow runtime consistency investigation`
  - Owner: Codex / Main PM
  - Status: `IN_PROGRESS`
  - Purpose:
    - `Calendar Label Batch-11` comparison abort 이후 duplicate-id 생성 경로와 sentinel control 해석 문제를 정리
    - green autopilot 확대 전에 baseline/runtime 정합성을 다시 고정
  - Verified so far:
    - live split/search current unique ids는 `8094`
    - true new ids는 `자료_일반명사-1`, `먼저_일반부사-1` 2건뿐임
    - overlapping `29` ids는 기존 live node와 재분류본이 중복 append된 상태였음
    - `rebuild_rev23_detail_chunks.py`는 duplicate input을 생성하지 않았지만, duplicated live tree를 읽어 chunk dict key overwrite로 manifest/search mismatch를 유발할 수 있었음
  - Next:
    - runtime projection/replace 단계에서 왜 batch core `31`개를 전부 live append했는지 경로를 특정
    - sentinel `요일_일반명사-1`를 no-drift control set에 둔 판단이 맞는지 재분류

- `V1-REV-98`
  - Agent: 데이터
  - Status: `DISPATCHED`
  - Purpose:
    - Calendar Label Batch-11 projection gate package를 닫고 runtime projection 직전 evidence를 완성
    - 신규 20 edge preview coverage, before snapshot, holdout/reserve/sentinel baseline을 한 번에 정리
  - Guard:
    - `publish` 금지
    - `chunk rebuild` 금지
    - holdout / reserve unchanged
    - 새 relation semantics 금지

- `V1-REV-97`
  - Agent: 리뷰
  - Status: `REPORTED`
  - Purpose:
    - `Calendar Label Batch-11` internal build package-level acceptance review
    - verified / residual risk / next projection gate condition 판단
  - Result:
    - verdict `ACCEPT`
    - residual risk는 신규 20 edge preview 미갱신
    - next step은 runtime projection 직행이 아니라 projection gate package
  - Guard:
    - 새 relation semantics 금지
    - batch 재기획 금지
    - checklist-only review 금지

- `V1-REV-96`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - `Calendar Label Batch-11`를 next green batch로 internal canonical에 구축
    - validated contract를 재사용하는 one-batch-one-rev 후보로 집행
  - Result:
    - nodes `30 -> 41`, edges `44 -> 64`
    - holdout / reserve invariant 유지
    - family template mismatch `0`, duplicate / reciprocal / required field 문제 `0`
  - Guard:
    - `publish` 금지
    - `chunk rebuild` 금지
    - reserve / yellow candidate touch 금지
    - 새 relation semantics 금지

- `V1-REV-95`
  - Agent: 기획
  - Status: `REPORTED`
  - Purpose:
    - 운영 모델을 실제 다음 batch 선정에 적용
    - Type/Gate 기준으로 next green batch를 고르고 바로 dispatch outline까지 정리
  - Result:
    - `Calendar Label Batch-11`
    - `Type A + Green`
    - month/date-point는 yellow 유지
  - Guard:
    - 새 relation semantics 금지
    - validated contract 재개방 금지
    - 후보 나열로 끝내지 말 것

- `V1-REV-94`
  - Agent: 기획
  - Status: `REPORTED`
  - Purpose:
    - batch type + exception-based gate 모델을 운영 규칙 수준으로 설계
    - one-batch-one-rev 가능 조건과 skill map을 정리
  - Result:
    - `Type A/B/C`
    - `Green/Yellow/Red`
    - one-batch-one-rev 조건
    - PM sequencing simplification
  - Guard:
    - 새 relation semantics 금지
    - validated contract 재개방 금지
    - 아이디어 나열로 끝내지 말 것

- `V1-REV-93`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - Batch-14 chunk rebuild gate를 닫고 search/tree/chunk 정합성을 확인
  - Result:
    - Batch-14 ids `14/14` search/tree/chunk relation counts 일치
    - holdout / reserve / sentinel drift `0`
    - Batch-14가 build -> acceptance -> projection -> chunk sync까지 한 배치로 완결
  - Guard:
    - 다음 step은 의미 있는 batch-level 운영 모델 또는 next expansion batch 설계

- `V1-REV-92`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - Batch-14 runtime projection을 실제로 실행하고 live runtime 결과를 검증
    - actual bucket vs expected bucket, holdout/reserve/sentinel drift를 한 번에 판단
  - Result:
    - actual bucket vs expected bucket `14/14` match
    - holdout / reserve / sentinel drift `0`
    - next step은 chunk rebuild gate
  - Guard:
    - `publish-only`는 허용
    - `chunk rebuild`는 후속 gate로 분리
    - holdout / reserve unchanged
    - 새 relation semantics 금지

- `V1-REV-91`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - Batch-14 projection gate package를 닫고 runtime projection 직전 evidence를 완성
    - 신규 28 edge preview coverage, before snapshot, sentinel baseline을 한 번에 정리
  - Result:
    - 신규 28 edge preview coverage `100%`
    - before snapshot과 holdout/reserve/sentinel baseline 확보
    - next step은 runtime projection gate
  - Guard:
    - `publish` 금지
    - `chunk rebuild` 금지
    - holdout / reserve unchanged
    - 새 relation semantics 금지

- `V1-REV-90`
  - Agent: 리뷰
  - Status: `REPORTED`
  - Purpose:
    - `Calendar Continuity Batch-14` internal build package-level acceptance review
    - verified / residual risk / next projection gate condition 판단
  - Result:
    - verdict `ACCEPT`
    - residual risk는 신규 28 edge preview 미갱신
    - next step은 runtime projection 직행이 아니라 projection gate package
  - Guard:
    - 새 relation semantics 금지
    - batch 재기획 금지
    - checklist-only review 금지

- `V1-REV-89`
  - Agent: 데이터
  - Status: `REPORTED`
  - Purpose:
    - `Calendar Continuity Batch-14`를 first coverage expansion build로 internal canonical에 구축
    - holdout/reserve 유지와 family-consistent edge package 구축을 한 번에 닫기
  - Result:
    - graph totals `nodes 16 -> 30`, `edges 16 -> 44`
    - holdout / reserve invariant 유지
    - family template mismatch `0`
    - duplicate / reciprocal / required field 문제 `0`
  - Guard:
    - `publish` 금지
    - `chunk rebuild` 금지
    - reserve queue 해제 금지
    - 새 relation semantics 금지

- `V1-REV-88`
  - Agent: 기획
  - Status: `REPORTED`
  - Purpose:
    - coverage expansion build를 실행 가능한 big-step package로 설계
    - first batch, ambiguity control, build/projection/rebuild gate sequence를 함께 닫기
  - Result:
    - 추천안 `Calendar Continuity Batch-14`
    - reserve / holdout / exception queue plan 포함
    - build -> projection -> chunk rebuild gate sequence 제안
  - Guard:
    - 새 relation semantics 금지
    - pilot contract 재개방 금지
    - micro-step TODO 나열 금지

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
- REV-88 report:
  - `.gemini-orchestration/workboard_archive/planning/20260315_REV88_coverage_expansion_build_package_report.md`
- REV-89 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV89_calendar_continuity_batch14_assignment.md`
- REV-89 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV89_calendar_continuity_batch14_report.md`
- REV-90 assignment:
  - `.gemini-orchestration/workboard_archive/review/20260315_REV90_calendar_continuity_batch14_acceptance_assignment.md`
- REV-90 report:
  - `.gemini-orchestration/workboard_archive/review/20260315_REV90_calendar_continuity_batch14_acceptance_report.md`
- REV-91 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV91_batch14_projection_gate_package_assignment.md`
- REV-91 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV91_batch14_projection_gate_package_report.md`
- REV-92 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV92_batch14_runtime_projection_assignment.md`
- REV-92 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV92_batch14_runtime_projection_report.md`
- REV-93 assignment:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV93_batch14_chunk_rebuild_gate_assignment.md`
- REV-93 report:
  - `.gemini-orchestration/workboard_archive/data/20260315_REV93_batch14_chunk_rebuild_gate_report.md`
- REV-94 report:
  - `.gemini-orchestration/workboard_archive/planning/20260315_REV94_batch_agent_operating_model_report.md`
- REV-95 assignment:
  - `.gemini-orchestration/workboard_archive/planning/20260315_REV95_next_green_batch_selection_assignment.md`
- REV-94 assignment:
  - `.gemini-orchestration/workboard_archive/planning/20260315_REV94_batch_agent_operating_model_assignment.md`
- REV-88 assignment:
  - `.gemini-orchestration/workboard_archive/planning/20260315_REV88_coverage_expansion_build_package_assignment.md`
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

- 다음 단계는 `REV-98` projection gate package 보고 확인
- 판단 메모:
  - `REV-97` verdict는 수용
  - 신규 20 edge preview coverage를 먼저 닫은 뒤 runtime projection으로 가는 것이 맞다
