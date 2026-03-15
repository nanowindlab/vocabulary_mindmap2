# Green Batch Agent Assignment Log

> Agent: `Green Batch Agent`
> Revision: `V1-REV-101`
> Logged: `2026-03-15 15:19:11`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- first autopilot trial:
  - `Calendar Label Batch-11`
- execution chain:
  1. projection gate final check
  2. `publish-only`
  3. actual bucket verification
  4. `chunk rebuild`
  5. search/tree/chunk consistency check
  6. consolidated report

## Stop Rule

- 아래 중 하나면 즉시 중단하고 yellow로 승격:
  - expected vs actual bucket mismatch
  - holdout/reserve/sentinel drift
  - search/tree/chunk mismatch
  - unexpected script mode change
  - target_id ambiguity

## Required Outcome

- one consolidated autopilot trial report
- final status:
  - `AUTOPILOT_SUCCESS`
  - `AUTOPILOT_ABORTED_TO_YELLOW`
