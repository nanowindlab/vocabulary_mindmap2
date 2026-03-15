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
> 📎 **dispatch package**: [Relative Year Batch Dispatch Package](../08_expansion/pm_reports/20260315_PM_RELATIVE_YEAR_BATCH_DISPATCH_PACKAGE_V1.md)
> 
> 📎 **execution report**: [Relative Year Batch Execution Report](../08_expansion/pm_reports/20260315_PM_RELATIVE_YEAR_BATCH_EXECUTION_REPORT_V1.md)
> 
> 📎 **second execution report**: [Temporal Reference Batch Execution Report](../08_expansion/pm_reports/20260315_PM_TEMPORAL_REFERENCE_BATCH_EXECUTION_REPORT_V1.md)
> 
> 📎 **third execution report**: [Past Day Reference Batch Execution Report](../08_expansion/pm_reports/20260315_PM_PAST_DAY_REFERENCE_BATCH_EXECUTION_REPORT_V1.md)
> 
> 📎 **bulk time-point report**: [Time Point Bulk Batch-65 Execution Report](../08_expansion/pm_reports/20260315_PM_TIME_POINT_BULK_BATCH65_EXECUTION_REPORT_V1.md)
> 
> 📎 **bulk time-root report**: [Time Root Bulk Remaining Batch-132 Execution Report](../08_expansion/pm_reports/20260315_PM_TIME_ROOT_BULK_REMAINING_BATCH132_EXECUTION_REPORT_V1.md)
> 
> 📎 **full mirror report**: [Full Runtime Mirror Execution Report](../08_expansion/pm_reports/20260315_PM_FULL_RUNTIME_MIRROR_EXECUTION_REPORT_V1.md)
> 
> 📎 **full node coverage report**: [Full Live Node Coverage Execution Report](../08_expansion/pm_reports/20260315_PM_FULL_LIVE_NODE_COVERAGE_EXECUTION_REPORT_V1.md)
> 
> 📎 **zero relation generation report**: [Zero Relation Generation Execution Report](../08_expansion/pm_reports/20260315_PM_ZERO_RELATION_GENERATION_EXECUTION_REPORT_V1.md)
> 
> 📎 **medical enrichment report**: [Medical Learner Journey Execution Report](../08_expansion/pm_reports/20260315_PM_MEDICAL_LEARNER_JOURNEY_EXECUTION_REPORT_V1.md)
> 
> 📎 **rollout status**: [Post-Restart Rollout Status](../08_expansion/pm_reports/20260315_PM_POST_RESTART_ROLLOUT_STATUS_V1.md)

> **기본 프로토콜**: 사용자는 이 대시보드 한 문서만 기준으로 모니터링하고 지시한다. 세부 근거와 milestone 산출물은 `08_expansion/pm_reports/`를 기준으로 읽는다.
>
> **현재 운영 재정렬**: `REV-74`는 버리는 기획이 아니라 현재 restart gate의 planning baseline이다. `Calendar Continuity Batch-14`는 완료되었고, `Calendar Label Batch-11`은 `Yellow / Runtime Reclassification`으로 재분류되었다. Yellow closure와 runtime projection hardening은 완료되었으며, 승인 이후 current live parity와 non-control generation까지 닫혔고 `병원 -> 아프다` 축의 richer enrichment도 검증됐다. 다음 meaningful gate는 이 richer enrichment 패턴을 다른 domain으로 확장할지에 대한 사용자 승인이다. sequencing은 Codex/Main PM이 직접 주도한다.

| 일시 | Agent | 지시 버전 | 지시완료 (Mgr) | 사용자 승인 | 지시접수 (Agent) | 작업 완료 (Agent) | 진행 상태 (Status) | 비고 (Verdict) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 03-15, 21:00:00 | Codex/PM | PM-MEDICAL-LEARNER-JOURNEY-V1 | ✅ (Manager) | `요청 전` | ✅ | ✅ | **REPORTED** | [RICHER-ENRICHMENT] `병원 -> 아프다`, `아프다 -> 병원/진료/약국` 등 medical learner journey jump runtime 반영 확인 |
| 03-15, 21:26:46 | Codex/PM | PM-ZERO-RELATION-GENERATION-V1 | ✅ (Manager) | `요청 전` | ✅ (21:15) | ✅ (21:26) | **REPORTED** | [GENERATION-CLOSURE] non-control zero-relation rows `0` 달성. holdout `4`개만 intentional zero 상태 유지 |
| 03-15, 21:14:01 | Codex/PM | PM-FULL-LIVE-NODE-COVERAGE-V1 | ✅ (Manager) | `요청 전` | ✅ (21:08) | ✅ (21:14) | **REPORTED** | [FULL-NODE-COVERAGE] current live node coverage `8094/8094` 달성. integrity 유지, 다음 승인 게이트는 zero-relation `422`개 생성 단계 |
| 03-15, 21:07:45 | Codex/PM | PM-FULL-LIVE-RUNTIME-MIRROR-V1 | ✅ (Manager) | `요청 전` | ✅ (21:02) | ✅ (21:07) | **REPORTED** | [FULL-RUNTIME-MIRROR] full runtime relation mirror는 integrity를 유지했지만 duplicate-term dedupe로 `related_total -30` 정규화가 발생. 다음 승인 게이트 필요 |
| 03-15, 21:01:53 | Codex/PM | PM-TIME-ROOT-BULK-REMAINING-132 | ✅ (Manager) | `요청 전` | ✅ (21:00) | ✅ (21:01) | **REPORTED** | [SAFE-COVERAGE-CLOSURE] `시간과 흐름` root의 remaining safe noun coverage bulk mirror 완료. global integrity `0 mismatch`, control drift `0` |
| 03-15, 21:00:16 | Codex/PM | PM-TIME-POINT-BULK-65 | ✅ (Manager) | `요청 전` | ✅ (21:00) | ✅ (21:00) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Time Point Bulk Batch-65` publish/rebuild/consistency check 통과. duplicate ids `0`, control drift `0` |
| 03-15, 20:51:42 | Codex/PM | PM-PAST-DAY-REFERENCE-BATCH6 | ✅ (Manager) | `요청 전` | ✅ (20:49) | ✅ (20:51) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Past Day Reference Batch-6` publish/rebuild/consistency check 통과. holdout/reserve/sentinel drift `0`, duplicate ids `0` |
| 03-15, 20:38:52 | Codex/PM | PM-TEMPORAL-REFERENCE-BATCH8 | ✅ (Manager) | `요청 전` | ✅ (20:36) | ✅ (20:38) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Temporal Reference Nouns Batch-8` publish/rebuild/consistency check 통과. holdout/reserve/sentinel drift `0`, duplicate ids `0` |
| 03-15, 20:21:50 | Codex/PM | PM-RELATIVE-YEAR-BATCH6 | ✅ (Manager) | `요청 전` | ✅ (20:19) | ✅ (20:21) | **REPORTED** | [RESTART-GREEN-EXECUTION] `Relative Year Markers Batch-6` publish/rebuild/consistency check 통과. holdout/reserve/sentinel drift `0`, duplicate ids `0` |
| 03-15, 16:59:30 | 그린배치-2 | V1-REV-102 | ✅ (Manager) | `승인됨` | ✅ (17:42) | ✅ (17:42) | **REPORTED** | [GREEN-AUTOPILOT-COMPARISON] `Calendar Label Batch-11` comparison trial은 `AUTOPILOT_ABORTED_TO_YELLOW`. 후속 Yellow closure 완료 후 batch는 `Runtime Reclassification`으로 재분류되었고, 현재 상태는 `restart-ready` |
| 03-15, 15:19:11 | 그린배치-1 | V1-REV-101 | ✅ (Manager) | `승인됨` | ✅ (15:20) | ✅ (15:40) | **REPORTED** | [GREEN-AUTOPILOT-TRIAL] `Calendar Label Batch-11` 완료. 31 ids(SIT 23, EXP 1, BAS 7) projection 및 chunk 021 sync 성공. 정합성(8,123건) 일치 확인 |
| 03-15, 14:28:49 | 기획 | V1-REV-100 | ✅ (Manager) | `승인됨` | ✅ (14:32) | ✅ (14:32) | **REPORTED** | [GREEN-BATCH-AUTOPILOT] autopilot model proposal 제출 완료. step chain, yellow 승격 조건, PM 개입 규칙, first rollout 권고 포함 |
| 03-15, 14:06:24 | 데이터 | V1-REV-98 | ✅ (Manager) | `승인됨` | ✅ (14:10) | ✅ (14:10) | **REPORTED** | [LABEL-BATCH11-PROJECTION-GATE] projection gate package 보고 제출. 신규 20 edge preview 100% 커버, before snapshot 및 holdout/reserve/sentinel baseline 확보 |
| 03-15, 14:12:39 | 데이터 | V1-REV-99 | ✅ (Manager) | `승인됨` | - | - | **WITHDRAWN** | [LABEL-BATCH11-RUNTIME-PROJECTION] 회수. Green Batch Autopilot 운영 검토를 먼저 수행하고, runtime projection은 그 설계 후 재개 |
| 03-15, 14:02:08 | 리뷰 | V1-REV-97 | ✅ (Manager) | `승인됨` | ✅ (14:05) | ✅ (14:05) | **REPORTED** | [LABEL-BATCH11-INTERNAL-ACCEPTANCE] internal build review 보고 제출. Verdict `ACCEPT`, residual risk는 preview 미갱신 20건이며 다음 단계는 projection gate package |
| 03-15, 13:47:18 | 데이터 | V1-REV-96 | ✅ (Manager) | `승인됨` | ✅ (13:59) | ✅ (13:59) | **REPORTED** | [CALENDAR-LABEL-BATCH11] next green batch internal build 보고 제출 확인. nodes `30->41`, edges `44->64`, holdout/reserve invariant 유지, 다음 단계는 internal acceptance review |
| 03-15, 13:41:59 | 기획 | V1-REV-95 | ✅ (Manager) | `승인됨` | ✅ (13:45) | ✅ (13:45) | **REPORTED** | [NEXT-GREEN-BATCH] next green batch proposal 제출 완료. `Calendar Label Batch-11` 추천, month/date-point는 yellow 유지 |
| 03-15, 13:27:50 | 기획 | V1-REV-94 | ✅ (Manager) | `승인됨` | ✅ (13:32) | ✅ (13:32) | **REPORTED** | [BATCH-AGENT-OPERATING-MODEL] operating model proposal 제출 완료. `Type A/B/C`, `Green/Yellow/Red`, one-batch-one-rev 조건 포함 |
| 03-15, 13:19:12 | 데이터 | V1-REV-93 | ✅ (Manager) | `승인됨` | ✅ (13:20) | ✅ (13:20) | **REPORTED** | [BATCH14-CHUNK-REBUILD] Batch-14 chunk rebuild gate 완료. Batch-14 14 ids search/tree/chunk 정합성 확인, holdout/reserve/sentinel drift `0` |
| 03-15, 13:11:56 | 데이터 | V1-REV-92 | ✅ (Manager) | `승인됨` | ✅ (13:18) | ✅ (13:18) | **REPORTED** | [BATCH14-RUNTIME-PROJECTION] runtime projection gate 보고 제출. Batch-14 actual bucket vs expected `14/14` 일치, holdout/reserve/sentinel drift `0`, 다음 단계는 chunk rebuild gate |
| 03-15, 13:01:55 | 데이터 | V1-REV-91 | ✅ (Manager) | `승인됨` | ✅ (13:08) | ✅ (13:08) | **REPORTED** | [BATCH14-PROJECTION-GATE] projection gate package 보고 제출. 신규 28 edge preview 100% 커버, before snapshot 및 holdout/reserve/sentinel baseline 확보 |
| 03-15, 12:34:21 | 리뷰 | V1-REV-90 | ✅ (Manager) | `승인됨` | ✅ (12:58) | ✅ (12:58) | **REPORTED** | [BATCH14-INTERNAL-ACCEPTANCE] internal build review 보고 제출. Verdict `ACCEPT`, residual risk는 preview 미갱신 28건이며 다음 단계는 projection gate package |
| 03-15, 12:34:21 | 데이터 | V1-REV-89 | ✅ (Manager) | `승인됨` | ✅ (12:43) | ✅ (12:43) | **REPORTED** | [CALENDAR-CONTINUITY-BATCH14] first coverage expansion build 보고 제출 확인. nodes `16->30`, edges `16->44`, holdout/reserve invariant 유지, 다음 단계는 internal acceptance review |
| 03-15, 01:31:51 | 기획 | V1-REV-88 | ✅ (Manager) | `승인됨` | ✅ (11:54) | ✅ (11:54) | **REPORTED** | [COVERAGE-EXPANSION-BUILD] planning package 제출 완료. `Calendar Continuity Batch-14` 추천, reserve/holdout/gate evidence plan 포함 |
| 03-15, 01:05:34 | 데이터 | V1-REV-87 | ✅ (Manager) | `승인됨` | ✅ (01:13) | ✅ (01:13) | **REPORTED** | [CHUNK-REBUILD-GATE] pilot chunk rebuild gate 완료. pilot 16 ids search/tree/chunk 정합성 확인, holdout 4 chunk exclusion 유지, 다음 단계는 coverage expansion build |
| 03-15, 01:05:34 | 데이터 | V1-REV-86 | ✅ (Manager) | `승인됨` | ✅ (01:13 note) | ✅ (01:13 note) | **REPORTED** | [PILOT-RUNTIME-PROJECTION] pilot runtime projection 완료. publish-only 성공, holdout exclusion/anchor bucket 검증 완료, 후속 chunk rebuild gate로 연결 |
| 03-15, 00:43:33 | 데이터 | V1-REV-85 | ✅ (Manager) | `승인됨` | ✅ (00:47) | ✅ (00:47) | **REPORTED** | [PROJECTION-GATE-PACKAGE] projection-ready package 보고 제출 확인. dry_run_reserve 16 edge 전부 커버, holdout 4 exclusion proof 확보, publish/rebuild/live overwrite 미실행 |
| 03-15, 00:24:29 | 리뷰 | V1-REV-84 | ✅ (Manager) | `승인됨` | ✅ (00:36) | ✅ (00:36) | **REPORTED** | [CORE12-EDGE-ACCEPTANCE] package-level acceptance review 보고 제출. Verdict `ACCEPT`, 다음은 publish 직행이 아니라 projection gate package 권고 |
| 03-15, 00:07:07 | 데이터 | V1-REV-83 | ✅ (Manager) | `승인됨` | ✅ (00:18) | ✅ (00:18) | **REPORTED** | [CORE12-EDGE-EXECUTION] internal-only edge package 보고 제출 확인. core 12 edge 16건, holdout 4 edge 0 유지, dedup/reciprocal/target_id 검증 보고 완료 |
| 03-14, 23:52:42 | 기획 | V1-PRE-REV-83-PLAN | ✅ (Manager) | `승인됨` | ✅ (00:04) | ✅ (00:04) | **REPORTED** | [PRE-REV83-SURVEY] bounded survey memo 제출 완료. method/order/validation blind spot만 보고, 새 정의/회귀 없음 |
| 03-14, 23:52:42 | 리뷰 | V1-PRE-REV-83-REVIEW | ✅ (Manager) | `승인됨` | ✅ (00:01) | ✅ (00:01) | **REPORTED** | [PRE-REV83-SURVEY] bounded survey report 제출 완료. acceptance/failure mode/validation blind spot 보고, 새 정의/재심 없음 |
| 03-14, 23:52:42 | 개발 | V1-PRE-REV-83-DEV | ✅ (Manager) | `승인됨` | ✅ (00:00 note) | ✅ (00:00 note) | **REPORTED** | [PRE-REV83-SURVEY] 개발 관점 memo 수용. report path는 review archive에 기록됐지만 runtime/projection handoff risk 입력으로 반영 완료 |
| 03-14, 23:24:31 | 데이터 | V1-REV-82 | ✅ (Manager) | `요청 전` | ✅ (23:19 report) | ✅ (23:19 report) | **REPORTED** | [HOLDOUT-DISAMBIGUATION] holdout ambiguity rule 보고 제출 확인. 내용상 `node seeded / edge held` 유지 권고. 전임 PM 프로토콜 불일치는 로그 기준으로 복구 |
| 03-14, 23:01:01 | 데이터 | V1-REV-81 | ✅ (Manager) | `승인됨` | ✅ (23:12) | ✅ (23:12) | **DONE** | [PILOT-POPULATION] pilot batch population 승인 완료. 다음 단계는 holdout disambiguation rule 정리 |
| 03-14, 22:55:45 | 데이터 | V1-REV-80 | ✅ (Manager) | `승인됨` | ✅ (23:04) | ✅ (23:04) | **DONE** | [SKELETON-CREATION] RELATION_GRAPH_CANONICAL_V1 empty skeleton 생성 완료. 승인 및 pilot population 단계 개시 |
| 03-14, 22:45:06 | 데이터 | V1-REV-79 | ✅ (Manager) | `승인됨` | ✅ (22:58) | ✅ (22:58) | **DONE** | [PILOT-PREPARATION] skeleton/pilot/dry-run proposal 승인 완료. 다음 단계는 skeleton 생성 revision 결정 |
| 03-14, 22:16:22 | 리뷰 | V1-REV-78 | ✅ (Manager) | `요청 전` | ✅ (22:16) | ✅ (22:34) | **REPORTED** | [CANONICAL-APPLY-REVIEW] canonical apply conformity review 완료. Verdict `ACCEPT`, Main PM 검토/사용자 승인 대기 |
| 03-14, 21:44:07 | 기획 | V1-REV-77 | ✅ (Manager) | `승인됨` | ✅ (21:51) | ✅ (21:51) | **DONE** | [IMPLEMENTATION-PLANNING] implementation architecture proposal 승인 및 canonical 문서 반영 완료 |
| 03-14, 17:23:58 | 리뷰 | V1-REV-76 | ✅ (Manager) | `승인됨` | ✅ (18:02) | ✅ (21:33) | **DONE** | [REV74-REVIEW] 3인 전문가 관점 비판 검토 완료, planning 반영 입력으로 수용 |
| 03-14, 17:23:57 | 데이터 | V1-REV-75 | ✅ (Manager) | `승인됨` | ✅ (18:02) | ✅ (18:18) | **DONE** | [REV74-STRUCTURE-REVIEW] 구조/구현 영향 검토 완료, planning 반영 입력으로 수용 |
| 03-14, 17:23:56 | 기획 | V1-REV-74 | ✅ (Manager) | `승인됨` | ✅ (20:46) | ✅ (20:46) | **DONE** | [BASELINE-REPLAN] proposal-only planning 보고 완료, 후속 planning/patch drafting의 기준 입력으로 수용 |
| 03-12, 00:00:00 | 리뷰 | V1-REV-73 | ✅ (Manager) | `승인됨` | ✅ | ✅ | **DONE** | **COMPLETE** (`V1-REV-72` 정책 초안에 대한 1차 검수 완료, 후속 재검토 입력으로 사용) |
| 03-12, 00:00:00 | 기획 | V1-REV-72 | ✅ (Manager) | `승인됨` | ✅ | ✅ | **DONE** | [POLICY-REARCH] 1차 정책 재설계 완료, 후속 재검토/재빌드 입력으로 고정 |
| 03-12, 00:00:00 | 개발 | V1-REV-70 | ✅ (Manager) | `승인됨` | ✅ | ✅ (08:58) | **DONE** | [RELEASE-HARDENING] 1차 구현 결과 완료, 후속 재검토/재빌드 입력으로 고정 |
| 03-12, 00:00:00 | 리뷰 | V1-REV-69 | ✅ (Manager) | `-` | ✅ | ✅ (GM Check) | **DONE** | **ULTIMATE_ACCEPT** (8.1K XWD 데이터 무결성 100% 검증 완료) |
| 03-12, 00:00:00 | 데이터 | V1-REV-68 | ✅ (Manager) | `-` | - | - | **WITHDRAWN** | [XWD-FINALIZE] 미션 철회: V47 작업 과정에서 트리 재생성 및 주입 완료됨 확인 |
| 03-11, 00:00:00 | 데이터 | V1-REV-47 | ✅ (Manager) | `-` | ✅ | ✅ (08:13) | **DONE** | **ACCEPT** (8.1K 단어 XWD 마이닝 및 양방향 주입, 트리 재생성 완료) |
| 03-11, 00:00:00 | 데이터 | V1-REV-65 | ✅ (Manager) | `-` | ✅ | ✅ (08:13) | **DONE** | **ACCEPT** (scripts/ 격리 및 경로 보정 완료, 새 환경 빌드 무결성 확인) |
| 03-11, 00:00:00 | 개발 | V1-REV-66 | ✅ (Manager) | `-` | ✅ | ✅ (00:37) | **DONE** | **ACCEPT** (다중 품사 필터 드롭다운 UI 개편 및 필터 연산 최적화 완결) |
| 03-11, 00:00:00 | 리뷰 | V1-REV-64 | ✅ (Manager) | `-` | ✅ | ✅ | **DONE** | **ACCEPT** (마스터 권한 기반 로드맵/태스크리스트 링크 수동 교정 및 구버전 아카이빙 완료) |
| 03-11, 00:00:00 | 리뷰 | V1-REV-63 | ✅ (Manager) | `-` | ✅ | ✅ | **DONE** | **ULTIMATE_ACCEPT** (3인 전문가 검증 통과: 링크 교정 및 무결성 회복 설계 완료) |
... (중략: 이전 데이터와 동일) ...
