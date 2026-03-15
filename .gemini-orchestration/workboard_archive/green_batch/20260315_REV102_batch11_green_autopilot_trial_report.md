# Green Batch Autopilot Trial Report: Batch-11 (REV-102)

## 1. Overview
- batch:
  - `Calendar Label Batch-11`
- agent:
  - `그린배치-2`
- executed_at:
  - `2026-03-15 17:14:14 KST`
- final_status:
  - `AUTOPILOT_ABORTED_TO_YELLOW`
- stop_rule_hit:
  - `search/tree/chunk mismatch`

## 2. Authoritative Inputs Read
- `08_expansion/batch_runs/BATCH_011M_validated.json`
- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/CHUNK_MANIFEST_V1.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_021.json`
- `09_app/public/data/live/APP_READY_CHUNK_EXAMPLES_chunk_021.json`
- `scripts/mining/run_rev47_xwd_mining.py`
- `scripts/core/rebuild_rev23_detail_chunks.py`
- `.gemini-orchestration/workboard_archive/green_batch/20260315_REV101_batch11_green_autopilot_trial_report.md`

## 3. Execution Chain Result

### 3.1 Projection Gate Final Check
- `BATCH_011M_validated.json` decision count:
  - `40`
- expected bucket split from validated decisions:
  - `core=31`
  - `candidate=9`
- internal canonical scope evidence:
  - `calendar_label_batch11` edges=`20`
  - total graph edges=`64`
- result:
  - partial pass

### 3.2 Publish-only
- command:
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
- observed result:
  - failed before publish summary emission
- direct failure:
  - `APP_READY_SITUATIONS_TREE.json` JSONDecodeError
  - error point: line `73741`, column `24`
- local corruption evidence near failure point:
  - duplicate orphan fragment: `"is_center_profile": false` followed by `},` before next object open
- stop decision:
  - chain terminated here

### 3.3 Actual Bucket Verification
- not executed
- reason:
  - `publish-only` failed and runtime tree was already invalid

### 3.4 Chunk Rebuild
- not executed
- reason:
  - stop rule already triggered upstream

### 3.5 Search/Tree/Chunk Consistency Check
- current runtime mismatch confirmed before rebuild:
  - `APP_READY_SITUATIONS_TREE.json`: invalid JSON, unreadable by runtime tooling
  - `CHUNK_MANIFEST_V1.json` `chunk_021.item_count=92`
  - `APP_READY_SEARCH_INDEX.json` rows with `chunk_id=chunk_021`: `123`
  - `APP_READY_CHUNK_RICH_chunk_021.json` entries: `123`
  - `APP_READY_CHUNK_EXAMPLES_chunk_021.json` entries: `123`
- classification:
  - `search/tree/chunk mismatch`

## 4. Stop Rule Evaluation
- expected vs actual bucket mismatch:
  - not evaluated after publish failure
- holdout/reserve/sentinel drift:
  - no new drift observed before abort, but full post-publish verification not reached
- search/tree/chunk mismatch:
  - triggered
- unexpected script mode change:
  - not observed
- target_id ambiguity:
  - not observed before abort

## 5. Difference From REV-101
- `REV-101` reported `AUTOPILOT_SUCCESS` with publish and chunk rebuild completed.
- `REV-101` reported `APP_READY_SITUATIONS_TREE.json` 정상 반영 및 total `4,564`.
- `REV-102` current runtime evidence shows `APP_READY_SITUATIONS_TREE.json` is malformed and blocks `publish-only`.
- `REV-101` reported `chunk_021` sync success for Batch-11 additions.
- `REV-102` current runtime evidence shows `CHUNK_MANIFEST_V1.json` claims `chunk_021=92` while search/rich/examples all show `123`, so manifest is no longer aligned with runtime artifacts.

## 6. Verdict
- final verdict:
  - `AUTOPILOT_ABORTED_TO_YELLOW`
- reason:
  - current live runtime is not in a publishable baseline state for the Batch-11 comparison autopilot trial
- next action:
  - repair `APP_READY_SITUATIONS_TREE.json`
  - reconcile `CHUNK_MANIFEST_V1.json` with live search/chunk artifacts
  - rerun the chain from `publish-only` only after baseline runtime integrity is restored
