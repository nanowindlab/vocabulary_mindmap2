# 프로젝트 오케스트레이션 대시보드 (RESTART-V1)

> ⚠️ **에이전트 필독**: [OPERATING_GUIDE_V1.md (운영 가이드)](./OPERATING_GUIDE_V1.md) | [MASTER_ROADMAP_V1.md (마스터 로드맵)](../08_expansion/MASTER_ROADMAP_V1.md)
> 
> 🗺️ **프로젝트 안내**: [PROJECT_DOCUMENT_MAP.md (문서 지도)](../PROJECT_DOCUMENT_MAP.md) | [PROJECT_INFRASTRUCTURE_GUIDE_V1.md (인프라 가이드)](../08_expansion/PROJECT_INFRASTRUCTURE_GUIDE_V1.md)
> 
> 📋 **실행 지침서**: [SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md (태스크리스트)](../08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md)
> 
> 📎 **현재 evidence owner**: [PM State Management Protocol](../08_expansion/PM_STATE_MANAGEMENT_PROTOCOL_V1.md) | [Current Milestone Report](../08_expansion/pm_reports/20260315_PM_RUNTIME_RECOVERY_AND_RESTART_PLAN_V1.md)
> 
> 📎 **다음 green 추천안**: [Next Green Batch Selection](../08_expansion/pm_reports/20260315_PM_NEXT_GREEN_BATCH_SELECTION_V1.md)
> 
> 📎 **medical enrichment report**: [Medical Learner Journey Execution Report](../08_expansion/pm_reports/20260315_PM_MEDICAL_LEARNER_JOURNEY_EXECUTION_REPORT_V1.md)
> 
> 📎 **food dining enrichment report**: [Food & Dining Learner Journey Execution Report](../08_expansion/pm_reports/20260315_PM_WP1_FOOD_DINING_JOURNEY_EXECUTION_REPORT_V1.md)
> 
> 📎 **rollout status**: [Post-Restart Rollout Status](../08_expansion/pm_reports/20260315_PM_POST_RESTART_ROLLOUT_STATUS_V1.md)

> **기본 프로토콜**: 사용자는 이 대시보드 한 문서만 기준으로 모니터링하고 지시한다. 세부 근거와 milestone 산출물은 `08_expansion/pm_reports/`를 기준으로 읽는다.
>
> **현재 운영 재정렬**: `REV-74`는 버리는 기획이 아니라 현재 restart gate의 planning baseline이다. `Calendar Label Batch-11`은 `Yellow / Runtime Reclassification`으로 재분류되었다. Yellow closure와 runtime projection hardening은 완료되었으며, 승인 이후 current live parity와 non-control generation까지 닫혔고, `병원 -> 아프다` (Medical) 및 `식당 -> 배고프다` (Food) 축의 richer enrichment도 검증/반영됐다. 다음 의미 있는 게이트는 추가 도메인(쇼핑, 교통, 학교)으로의 확장 승인이다.

| 일시 | Agent | 지시 버전 | 지시완료 (Mgr) | 사용자 승인 | 지시접수 (Agent) | 작업 완료 (Agent) | 진행 상태 (Status) | 비고 (Verdict) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 03-15, 21:50:00 | Codex/PM | PM-WP1-FOOD-DINING-JOURNEY-V1 | ✅ (Manager) | `요청 전` | ✅ | ✅ | **REPORTED** | [RICHER-ENRICHMENT] `식당 -> 배고프다`, `음식 -> 맛` 등 Food & Dining learner journey jump (28건) runtime 반영 확인 및 정합성 유지 |
| 03-15, 21:00:00 | Codex/PM | PM-MEDICAL-LEARNER-JOURNEY-V1 | ✅ (Manager) | `승인됨` | ✅ | ✅ | **REPORTED** | [RICHER-ENRICHMENT] `병원 -> 아프다`, `아프다 -> 병원/진료/약국` 등 medical learner journey jump runtime 반영 확인 |
| 03-15, 21:26:46 | Codex/PM | PM-ZERO-RELATION-GENERATION-V1 | ✅ (Manager) | `승인됨` | ✅ (21:15) | ✅ (21:26) | **REPORTED** | [GENERATION-CLOSURE] non-control zero-relation rows `0` 달성. holdout `4`개만 intentional zero 상태 유지 |
| 03-15, 21:14:01 | Codex/PM | PM-FULL-LIVE-NODE-COVERAGE-V1 | ✅ (Manager) | `승인됨` | ✅ (21:08) | ✅ (21:14) | **REPORTED** | [FULL-NODE-COVERAGE] current live node coverage `8094/8094` 달성. integrity 유지 |
| 03-15, 21:07:45 | Codex/PM | PM-FULL-LIVE-RUNTIME-MIRROR-V1 | ✅ (Manager) | `승인됨` | ✅ (21:02) | ✅ (21:07) | **REPORTED** | [FULL-RUNTIME-MIRROR] full runtime relation mirror는 integrity를 유지했지만 duplicate-term dedupe로 `related_total -30` 정규화가 발생 |
| 03-15, 21:01:53 | Codex/PM | PM-TIME-ROOT-BULK-REMAINING-132 | ✅ (Manager) | `승인됨` | ✅ (21:00) | ✅ (21:01) | **REPORTED** | [SAFE-COVERAGE-CLOSURE] `시간과 흐름` root의 remaining safe 정합성 유지 확인 bulk mirror 완료 |
| 03-15, 21:00:16 | Codex/PM | PM-TIME-POINT-BULK-65 | ✅ (Manager) | `승인됨` | ✅ (21:00) | ✅ (21:00) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Time Point Bulk Batch-65` publish/rebuild/consistency check 통과 |
| 03-15, 20:51:42 | Codex/PM | PM-PAST-DAY-REFERENCE-BATCH6 | ✅ (Manager) | `승인됨` | ✅ (20:49) | ✅ (20:51) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Past Day Reference Batch-6` publish/rebuild/consistency check 통과 |
| 03-15, 20:38:52 | Codex/PM | PM-TEMPORAL-REFERENCE-BATCH8 | ✅ (Manager) | `승인됨` | ✅ (20:36) | ✅ (20:38) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Temporal Reference Nouns Batch-8` publish/rebuild/consistency check 통과 |
| 03-15, 20:21:50 | Codex/PM | PM-RELATIVE-YEAR-BATCH6 | ✅ (Manager) | `승인됨` | ✅ (20:19) | ✅ (20:21) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Relative Year Markers Batch-6` publish/rebuild/consistency check 통과 |