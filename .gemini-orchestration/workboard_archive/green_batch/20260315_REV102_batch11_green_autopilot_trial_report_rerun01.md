# Green Batch Autopilot Trial Report: Batch-11 (REV-102 Rerun-01)

## 1. Overview
- batch:
  - `Calendar Label Batch-11`
- agent:
  - `그린배치-2`
- executed_at:
  - `2026-03-15 17:42:25 KST`
- final_status:
  - `AUTOPILOT_ABORTED_TO_YELLOW`

## 2. Authoritative Inputs Read
- `.gemini-orchestration/GREEN_BATCH_AGENT_2_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/green_batch/20260315_REV102_batch11_green_autopilot_trial_assignment.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV96_calendar_label_batch11_report.md`
- `.gemini-orchestration/workboard_archive/data/20260315_REV98_batch11_projection_gate_package_report.md`
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

## 3. Pre-Run Baseline Recovery Check
- live runtime parse:
  - `APP_READY_SITUATIONS_TREE.json=4564`
  - `APP_READY_EXPRESSIONS_TREE.json=1830`
  - `APP_READY_BASICS_TREE.json=1729`
  - `APP_READY_SEARCH_INDEX.json=8123`
- `chunk_021` repair proof:
  - manifest `123`
  - search `123`
  - rich `123`
  - examples `123`
  - search/rich/examples set diff `0`
- conclusion:
  - baseline runtime recovery confirmed before rerun

## 4. Execution Chain Result

### 4.1 Projection Gate Final Check
- validated decision count:
  - `40`
- expected batch split:
  - `core=31`
  - `candidate=9`
- internal canonical scope:
  - `calendar_label_batch11` edges=`20`
  - graph edges total=`64`
- result:
  - pass

### 4.2 Publish-only
- command:
  - `python3 scripts/mining/run_rev47_xwd_mining.py --publish-only`
- output:
  - `mode=internal_canonical_overlay`
  - `graph_status=calendar_label_batch11_draft`
  - `graph_edge_count=64`
  - `overlay_terms=41`
  - `related_terms=30`
  - `cross_system_terms=16`
- unexpected script mode change:
  - none

### 4.3 Actual Bucket Verification
- expected runtime core ids:
  - `31`
- actual runtime system counts after publish:
  - `상황과 장소=23`
  - `마음과 표현=1`
  - `구조와 기초=7`
- missing core ids in search:
  - `0`
- Batch-11 11-node expected relation counts all matched:

```text
날짜_일반명사-1|0|1
달력_일반명사-1|2|1
요일_일반명사-1|1|0
월_일반명사-1|2|0
연도_일반명사-1|0|2
금년_일반명사-1|2|1
내년_일반명사-1|1|1
이달_일반명사-1|1|2
내달_일반명사-1|0|1
연말_일반명사-1|1|0
월말_일반명사-1|0|1
```

### 4.4 Holdout / Reserve / Sentinel Check
- holdout:
  - `오늘_일반부사-1=0|0`
  - `어제_일반부사-1=0|0`
  - `점심_일반명사-1=0|0`
  - `저녁_일반명사-2=0|0`
- reserve:
  - `가을_일반명사-1=3|2`
  - `계절_일반명사-1=5|0`
  - `사계절_일반명사-1=5|0`
- sentinel:
  - `모레_일반명사-1=5|0`
  - `정오_일반명사-1=4|0`
  - `요일_일반명사-1=1|0`
- drift result:
  - stop rule hit
  - sentinel `요일_일반명사-1` expected baseline `4|0` vs actual `1|0`

### 4.5 Chunk Rebuild
- command:
  - `python3 scripts/core/rebuild_rev23_detail_chunks.py`
- output:
  - `tree_total=8123`
  - `chunk_count=21`
  - `related_non_empty=7621`
  - `examples_non_empty=8118`

### 4.6 Search / Tree / Chunk Consistency Check
- Batch-11 core `31` ids:
  - search/tree/rich/examples consistency issues `0`
- global count integrity:
  - split total=`8123`
  - search total=`8123`
  - manifest sum=`8122`
- duplicate-id integrity:
  - search length `8123`, unique ids `8094`, duplicate ids `29`
  - situations length `4564`, unique ids `4543`, duplicate ids `21`
  - basics length `1729`, unique ids `1724`, duplicate ids `5`
  - chunk union unique ids `8094`, duplicate ids `28`
- classification:
  - stop rule hit
  - `search/tree/chunk mismatch`

## 5. Stop Rule Evaluation
- expected vs actual bucket mismatch:
  - not triggered
- holdout/reserve/sentinel drift:
  - triggered
- search/tree/chunk mismatch:
  - triggered
- unexpected script mode change:
  - not triggered
- target_id ambiguity:
  - not triggered

## 6. Difference From REV-101
- `REV-101` reported `AUTOPILOT_SUCCESS`.
- this rerun started from a repaired baseline and `publish-only` itself succeeded, unlike the first `REV-102` attempt.
- despite that, this rerun still failed the stop rule because sentinel `요일_일반명사-1` drifted from baseline `4|0` to `1|0`.
- after `chunk rebuild`, global runtime artifacts also diverged: search length stayed `8123` but unique ids dropped to `8094`, with duplicate ids appearing in split/search/chunk outputs.
- therefore the repaired baseline was not sufficient to reproduce the `REV-101` success path under the current runtime state.

## 7. Verdict
- final verdict:
  - `AUTOPILOT_ABORTED_TO_YELLOW`
- reason:
  - `publish-only` passed, but control baseline drift and post-rebuild duplicate-id mismatch violated the stop rule
- next action:
  - investigate why sentinel `요일_일반명사-1` was included in the no-drift control set while also being part of the Batch-11 expected change surface
  - trace duplicate-id generation path in `rebuild_rev23_detail_chunks.py` / current live tree inputs before any further autopilot rerun
