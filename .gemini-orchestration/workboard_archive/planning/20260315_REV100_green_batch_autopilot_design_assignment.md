# Planning Assignment Log

> Agent: `기획 에이전트`
> Revision: `V1-REV-100`
> Logged: `2026-03-15 14:28:49`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- `REV-94`의 batch-agent operating model과 `REV-95`의 next green batch selection을 바탕으로,
  이번 revision은 **Green Batch Autopilot** 설계를 실제 운영 문서 수준으로 닫는다.
- 목적은 PM 관할 아래에서, green batch가
  - internal build
  - internal self-check
  - projection gate
  - runtime projection
  - chunk sync
  를 한 번의 자동 실행 흐름으로 어디까지 처리할 수 있는지 정하는 것이다.

## Required Outcome

- Green Batch Autopilot memo
- autopilot step chain
- stop / promote-to-yellow rule
- PM intervention rule
- evidence pack auto-generation spec
- first rollout recommendation
