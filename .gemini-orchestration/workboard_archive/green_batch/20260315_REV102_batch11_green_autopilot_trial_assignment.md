# Green Batch Agent Assignment Log

> Agent: `Green Batch Agent`
> Revision: `V1-REV-102`
> Logged: `2026-03-15 16:59:30`
> Status: `DISPATCHED / NOT STARTED`

## Assignment Summary

- comparison trial:
  - `Calendar Label Batch-11`
- purpose:
  - 상위 LLM 모델에서 동일한 green autopilot chain을 다시 실행해
    stop rule 민감도, 정합성 검증 품질, consolidated report 품질을 비교한다.

## Execution Chain

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
- comparison note:
  - `REV-101` 결과와 다른 점이 있다면 명시

---

## Execution Update

> Logged: `2026-03-15 17:14:14 KST`
> Agent: `그린배치-2`
> Final Status: `AUTOPILOT_ABORTED_TO_YELLOW`
> Consolidated Report: `.gemini-orchestration/workboard_archive/green_batch/20260315_REV102_batch11_green_autopilot_trial_report.md`

- stop trigger:
  - `search/tree/chunk mismatch`
- immediate evidence:
  - `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json` 파싱 실패
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`가 동일 파일 JSONDecodeError로 즉시 실패
  - `CHUNK_MANIFEST_V1.json`의 `chunk_021.item_count=92`인데, `APP_READY_SEARCH_INDEX.json` / `APP_READY_CHUNK_RICH_chunk_021.json` / `APP_READY_CHUNK_EXAMPLES_chunk_021.json`는 모두 `123`
- chain result:
  - projection gate final check: partial pass
  - `publish-only`: failed before write completion
  - actual bucket verification: not executed
  - chunk rebuild: not executed
  - search/tree/chunk consistency check: failed on pre-existing runtime mismatch

---

## Execution Update

> Logged: `2026-03-15 17:42:25 KST`
> Agent: `그린배치-2`
> Run: `rerun-01 after baseline recovery`
> Final Status: `AUTOPILOT_ABORTED_TO_YELLOW`
> Consolidated Report: `.gemini-orchestration/workboard_archive/green_batch/20260315_REV102_batch11_green_autopilot_trial_report_rerun01.md`

- baseline recovery check:
  - `APP_READY_SITUATIONS_TREE.json` parse restored
  - `chunk_021` manifest/search/rich/examples count restored to `123`
- projection gate final check:
  - pass
- `publish-only`:
  - executed successfully in `internal_canonical_overlay` mode
  - actual bucket matched expected `31` core ids (`상황과 장소 23 / 마음과 표현 1 / 구조와 기초 7`)
- stop triggers found:
  - `holdout/reserve/sentinel drift`
  - `search/tree/chunk mismatch`
- key evidence:
  - sentinel `요일_일반명사-1` expected `4|0` but actual `1|0`
  - rebuild 후 `APP_READY_SEARCH_INDEX.json` length `8123`, unique ids `8094`, duplicate ids `29`
  - chunk union unique ids `8094`, duplicate ids `28`
- chain result:
  - projection gate final check: pass
  - `publish-only`: success
  - actual bucket verification: pass
  - `chunk rebuild`: executed
  - search/tree/chunk consistency check: failed
