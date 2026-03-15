# 프로젝트 오케스트레이션 운영 가이드 (Operating Guide)

> **핵심 원칙**: 모든 에이전트의 작업 시작은 **`ORCHESTRATION_DASHBOARD.md`**에서 출발한다.
>
> **적용 범위**: 개발 에이전트의 실행 환경과 무관하게 동일한 workboard, 사용자 승인, append-only 로그 규칙을 적용한다.
>
> **사용자 프로토콜**: 사용자는 기본적으로 `ORCHESTRATION_DASHBOARD.md` 한 문서만 보고 모니터링하고 지시한다. workboard는 에이전트 상세 지시용으로 사용한다.

---

## 1. 에이전트 작업 프로세스 위계 (The Hierarchy)

모든 에이전트는 미션 수행 시 아래의 문서를 순차적으로 확인해야 합니다.

1.  **[1차 문서] 대시보드 (Dashboard)**: 
    - 자신의 행에 `DISPATCHED` 또는 `READY` 미션이 있는지 확인.
    - 프로젝트의 전체적인 맥락과 다른 에이전트의 완료 상태 파악.
    - 사용자는 이 문서만 보고 현재 누구를 움직일지 판단한다.
2.  **[2차 문서] 워크보드 (Workboard)**: 
    - 대시보드의 미션을 확인했다면, 즉시 자신의 워크보드로 이동.
    - 매니저의 상세 지시문(Manager's Command)과 검증 체크리스트 숙지.
3.  **[3차 실행] 작업 및 보고 (Execution & Report)**: 
    - 실제 코드/문서 작업 수행.
    - 작업 완료 후 워크보드에 `Latest Report`를 작성하고, 마지막으로 대시보드 상태를 `REPORTED`로 변경.

### 1.1. 접수 / 착수 반영 절차

- 에이전트가 첫 append-only 로그를 남기면, 그 로그를 **지시접수 / 착수 증거**로 간주합니다.
- 에이전트는 대시보드 상태를 직접 수정하지 않습니다.
- Codex는 해당 로그를 확인한 뒤 대시보드의 아래 필드를 갱신합니다.
  - `지시접수 (Agent)`
  - `진행 상태 (Status)`
- 따라서 에이전트의 책임은 `로그를 남기는 것`, Codex의 책임은 `대시보드에 반영하는 것`입니다.

---

## 2. 대시보드 운영 표준 (REV-71 개정)

- **상태 동기화**: 대시보드는 프로젝트의 '실시간 상태'를 나타내는 유일한 SSOT입니다.
- **비고란 활용**: 단순 상태 외에 핵심 결과물(Accept/Reject)의 이유를 간결하게 기록합니다.
- **제어 필드 소유권**: 대시보드의 상태, 사용자 승인, 행 추가/수정은 Codex 또는 사용자만 변경합니다. 에이전트는 대시보드를 직접 수정하지 않습니다.

---

## 3. 사용자 승인 게이트 (User Approval Gate)

- 최종 승인(`ACCEPT`, `DONE`, 다음 단계 승격, 배포 진행)은 반드시 **사용자 승인**을 거쳐야 합니다.
- Codex가 검증을 완료해도, 사용자 승인 기록이 없으면 최종 완료로 처리하지 않습니다.
- 사용자 승인 상태는 최소 아래 두 곳 중 하나에 남겨야 합니다.
  - `ORCHESTRATION_DASHBOARD.md`
  - 해당 agent workboard
- 권장 상태값:
  - `요청 전`
  - `승인 대기`
  - `승인됨`
  - `보류`
  - `반려`

### 3.1. Main PM 자율 진행 원칙

- 아래 항목은 사용자 승인 없이 Codex가 바로 다음 단계로 진행할 수 있다.
  - 다음 revision 개시
  - 에이전트 handoff sequencing
  - package-level review 개시
  - planning/data/review/dev 간 내부 work package 전환
- 단, 아래는 계속 사용자 승인 대상이다.
  - `ACCEPT`
  - `DONE`
  - 배포 진행
  - 다음 단계 승격 중 사용자 비용/리스크가 큰 결정
- 원칙:
  - 승인 게이트가 아닌데도 매번 사용자에게 재확인하지 말고, Codex가 근거를 갖고 바로 진행한다.

---

## 4. 워크보드 관리 표준

- **snapshot 원칙**: 현재 workboard는 최신 상태 요약판으로 유지하고, 세부 보고는 append-only 로그 파일로 남깁니다.
- **append-only 원칙**: workboard를 덮어쓰기 전에 상세 보고를 `.gemini-orchestration/workboard_archive/<agent>/` 아래 별도 문서로 먼저 보관합니다.
- **write_file 원칙**: 현재 snapshot 갱신이 필요할 때만 전체 갱신(`write_file`)을 사용합니다.
- **제어 필드 소유권**: workboard의 헤더(`Version`, `Status`, `User Approval Gate`, `Latest Detailed Report Path`)와 `Current Task`는 Codex 또는 사용자만 변경합니다. 에이전트는 append-only 로그에만 보고합니다.
- **Self-Validation**: 지시문에 포함된 검증 루프(예: 3인 전문가 검증)를 보고서에 반드시 포함합니다.
- **유실 방지 최소 항목**:
  - `Current Task`
  - `Expected Outputs`
  - `Latest Snapshot`
  - `Latest Detailed Report Path`
  - `User Approval Gate`

## 5. 솔루션 우선 프로토콜 (Solution-First Protocol)

- 모든 에이전트는 **진단에서 멈추지 않고 기본적으로 솔루션을 제시**해야 합니다.
- 문제를 발견하면 최소 아래 순서로 움직입니다.
  1. 문제 진단
  2. 1차 해결안 제시
  3. 가능하면 직접 수정 또는 후속 작업 계획 제시
  4. 수정 후 재검증 또는 재검증 계획 제시
- `문제만 적고 끝내는 보고`는 불완전한 보고로 간주합니다.

### 5.1. 독자 결정 가능 시

- 문서 정리, 증거 수집, 검증 보강, 경미한 구조 정렬, 명백한 누락 보완은 에이전트가 스스로 해결안을 제시하고 진행할 수 있습니다.

### 5.2. 독자 결정이 어려울 시

- 방향을 독자적으로 결정할 수 없으면 `질문만 남기지 말고`, **최대 3개 이내의 방안**을 제시해야 합니다.
- 각 방안에는 아래를 포함합니다.
  - 어떤 선택인지
  - 장점/리스크
  - 추천안 여부

### 5.3. 역할별 기대치

- **기획 에이전트**: 문제 진단 후 정책/문서 수정안 제시
- **데이터 에이전트**: 문제 진단 후 검증/재빌드/데이터 수정안 제시
- **리뷰 에이전트**: 문제 진단 후 acceptance 기준 또는 수정 권고안 제시
- **개발 에이전트**: 문제 진단 후 구현 수정안, 테스트안, 리스크 완화안 제시

## 6. 역할별 필수 스킬 기준

- **메인 PM / Codex**: `multi-agent-orchestration`, `doc-state-manager`, `data-validation`
- **기획 에이전트**: `doc-state-manager`, `korean-lexical-data-curation`
- **데이터 에이전트**: `data-validation`
- **리뷰 에이전트**: `report-verifier`, `data-validation`
- **개발 에이전트**: 고정 필수 없음, 필요 시 `design-principles`

조건부 사용:

- 문서 authoritative 판단: `doc-state-manager`
- 보고서 검토 entry: `report-verifier`
- 승인 전 실제 산출물 검증: `data-validation`
