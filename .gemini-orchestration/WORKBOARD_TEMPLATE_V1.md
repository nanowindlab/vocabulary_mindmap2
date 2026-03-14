# Workboard Template V1

> Use: planning / data validation / development / review workboards
> Rule: 이 문서는 현재 상태 snapshot이다. 세부 보고는 append-only 로그 파일로 먼저 남긴다.
> Control Fields: 헤더, `Current Task`, `User Approval`은 Codex/사용자 전용이다. 에이전트는 append-only 로그에만 보고한다.

## Header

- Agent:
- Required Skills:
- Version:
- Date:
- Status:
- Read First:
- Latest Detailed Report Path:
- User Approval Gate:

## Current Task

- task title
- objective
- scope in / out

## Expected Outputs

- required files
- required document updates
- required validation evidence

## Validation Rule

- artifact checks
- runtime checks
- review checks

## Solution Expectation

- 진단만 하지 말고 기본적으로 해결안을 제시
- 가능한 경우 직접 수정 또는 후속 실행안 제시
- 독자 결정이 어려우면 최대 3개 이내의 선택지 제시
- 각 선택지에 추천안 / 장점 / 리스크 포함

## Blocking / Decision Needed

- blocker 1
- question for user or Codex

## Latest Snapshot

- current state
- key result
- main risk
- next suggested handoff target

## Latest Review

- review verdict
- major findings
- follow-up required

## User Approval

- requested: yes / no
- state: `요청 전` / `승인 대기` / `승인됨` / `보류` / `반려`
- evidence:

## Append-Only Report Log

- detailed report path 1
- detailed report path 2
