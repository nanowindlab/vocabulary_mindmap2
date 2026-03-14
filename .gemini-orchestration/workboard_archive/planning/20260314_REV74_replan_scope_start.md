# Planning Detailed Report Log

> Agent: `기획 에이전트`
> Revision: `V1-REV-74`
> Logged: `2026-03-14 17:37:12`
> Status: `IN_PROGRESS`
> Trigger: `사용자 착수 승인`

## Work Title

- baseline replan scope definition for next rebuild cycle

## Initial Pass

- 기준선 산출물 `V1-REV-70`, `V1-REV-72`, `V1-REV-73`와 현재 canonical 문서의 정렬 상태를 우선 확인함
- 현재 canonical 기준은 `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`, `RELATION_DATA_POLICY_V1.md`, `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`, `PROJECT_DECISION_LOG_V1.md`로 묶음 확인함
- `V1-REV-70`은 release hardening 완료 상태이며, 다음 사이클의 직접 선행 조건은 runtime 재빌드보다도 정책/분류 기준 재정렬 쪽에 있음

## Findings

1. `V1-REV-73`의 조건부 승인 사항 3건이 현재 canonical 문서에 완결형으로 반영되지 않음
   - `내용성 시간` 정의 명문화 부재
   - `제거 테스트`, `IS-A 테스트`의 프로토콜 본문 반영 부재
   - `Basics`로 이관된 시간/계절 어휘의 `Situations` hard-link 또는 anchoring 운영 규칙 상세 부재
2. `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`는 위 보완이 필요한 상태를 전제로 `T2.16`, `T2.17`을 아직 pending으로 유지하고 있어, 실행 순서는 대체로 일관됨
3. `RELATION_DATA_POLICY_V1.md`는 `related_vocab`와 `refs.cross_links` 분리 기준은 고정했지만, 시간 anchor 전용 연결 쿼터나 필수 cross-link 기준은 아직 다루지 않음
4. `PROJECT_DECISION_LOG_V1.md`에는 REV72/73로 확정된 V5 정책 보강점이 아직 결정 로그 항목으로 명시되지 않음

## Planning Delta Draft

- Step 1: `SDCP`에 좌표성 시간 대 내용성 시간 경계, `제거 테스트`, `IS-A 테스트`를 canonical rule로 명문화
- Step 2: `RELATION_DATA_POLICY_V1.md` 또는 동급 canonical 문서에 시간/계절 anchor의 cross-link 의무 기준을 명시
- Step 3: `PROJECT_DECISION_LOG_V1.md`에 위 정책 변경을 결정 로그로 남김
- Step 4: 그다음 `T2.16`, `T2.17` 재실행 범위와 검증 기준을 data/review용으로 재배정
- Step 5: data rebuild 결과가 나오면 `T3.16` 범위만 제한적으로 개발 재투입

## Self-Review

- `REV72` snapshot에 적힌 required outputs와 `REV73` findings를 현재 SSOT와 대조해 누락 여부를 다시 확인함
- tasklist가 planning보다 data execution을 먼저 암시하는지 검토했으나, pending 항목 구성이 오히려 선행 planning 보강 필요성을 뒷받침함

## Reflection

- 재검토한 문서: `20260314_REV70_release_hardening_snapshot.md`, `20260314_REV72_policy_rework_snapshot.md`, `20260314_REV73_policy_review_snapshot.md`, `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`, `RELATION_DATA_POLICY_V1.md`, `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`, `PROJECT_DECISION_LOG_V1.md`
- self-review 후 바뀐 점: 단순 재독해 과제에서 끝내지 않고, 실제 다음 사이클 선행 조건을 `정책 canon closure -> data rebuild -> review -> limited dev` 순서로 명시함
- 남은 불확실성: 시간 anchor 의무 기준을 `RELATION_DATA_POLICY_V1.md`에 넣을지, `SDCP` 부속 규칙으로 합칠지는 아직 결정 전

## User Approval

- requested: yes
- state: `승인됨`
- evidence: 사용자가 `대시보드 업무 시작`으로 착수 승인
