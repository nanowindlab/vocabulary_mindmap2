# Planning Detailed Report Log

> Agent: `기획 에이전트`
> Revision: `V1-REV-74`
> Logged: `2026-03-14 17:51:12`
> Mode: `PASS_1`
> Reporting Rule: `append-only only`

## Scope

- 기존 완료 산출물 `V1-REV-70`, `V1-REV-72`, `V1-REV-73` 재독해
- 현재 canonical 문서와의 정렬 상태 재확인
- 다음 재빌드 사이클 planning delta 초안 도출

## Sources Rechecked

- `README.md`
- `PROJECT_DOCUMENT_MAP.md`
- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `08_expansion/README.md`
- `.gemini-orchestration/workboard_archive/development/20260314_REV70_release_hardening_snapshot.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV72_policy_rework_snapshot.md`
- `.gemini-orchestration/workboard_archive/review/20260314_REV73_policy_review_snapshot.md`
- `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `08_expansion/PROJECT_DECISION_LOG_V1.md`

## Required Skills Applied

- `doc-state-manager`
  - control source는 dashboard로 제한
  - workboard snapshot은 읽기용으로만 사용
  - planning 결과는 append-only delta 보고로 남김
- `korean-lexical-data-curation`
  - learner-facing taxonomy와 relation quality 관점에서 정책 보강 포인트를 읽음
  - 한국어 시간/계절 어휘의 분류 경계와 횡단 연결 기준을 우선 검토함

## Findings

1. `V1-REV-73`의 조건부 승인 포인트 3건이 current canonical에 아직 완결 반영되지 않음
   - `내용성 시간` 정의 명문화 부재
   - `제거 테스트`, `IS-A 테스트`의 프로토콜 본문 주입 부재
   - `Basics` 이관 시간/계절 어휘의 `Situations` anchor 또는 hard-link 운영 규칙 상세 부재
2. `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`는 위 보강을 전제로 `T2.16`, `T2.17`을 pending으로 유지하고 있어, planning 선행 보완 후 data rebuild로 이어지는 흐름과 충돌하지 않음
3. `RELATION_DATA_POLICY_V1.md`는 `related_vocab`와 `refs.cross_links`의 분리 규칙은 확정했지만, 시간 anchor 전용 cross-link 의무 기준은 아직 비어 있음
4. `PROJECT_DECISION_LOG_V1.md`에는 REV72/73에서 요구된 V5 보강점이 결정 로그 항목으로 명시되지 않음
5. `V1-REV-70` 개발 산출물은 release hardening 완료 기준선으로 읽히며, 다음 planning 사이클의 직접 선행 조건은 UI 수정이 아니라 정책 canon closure 쪽에 가까움

## Planning Delta Draft

- Step 1: `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`에 좌표성 시간 대 내용성 시간 경계, `제거 테스트`, `IS-A 테스트`를 canonical rule로 반영
- Step 2: 시간/계절 anchor의 `Situations` 횡단 연결 의무 기준을 `RELATION_DATA_POLICY_V1.md` 또는 동급 canonical 정책 문서에 반영
- Step 3: 위 정책 변화를 `PROJECT_DECISION_LOG_V1.md`에 결정 로그로 남김
- Step 4: 그 다음 `T2.16`, `T2.17` 재실행 범위와 검증 기준을 data/review 트랙 입력으로 재정리
- Step 5: data rebuild 결과가 나온 뒤 `T3.16` 범위만 제한적으로 개발 재투입

## Self-Review

- workboard snapshot을 control source로 사용하지 않고, dashboard row와 baseline archive를 기준으로 revision scope를 다시 맞춤
- 정책/태스크리스트/결정 로그 사이 중복 요약을 늘리지 않고, 다음 변경 후보를 canonical owner 기준으로만 정리함

## Reflection

- 재검토 후 유지한 판단: 이번 cycle의 선행 과제는 `정책 canon closure -> data rebuild -> review -> limited dev`
- 재검토 후 보수적으로 남긴 부분: 시간 anchor 의무 기준의 최종 소유 문서는 아직 결정하지 않음
- control field 미수정 원칙에 따라 본 보고서는 append-only 로그로만 남김
