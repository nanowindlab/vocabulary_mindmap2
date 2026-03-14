# Data Pilot Population Report

> Agent: `데이터 에이전트`
> Revision: `V1-REV-81`
> Logged: `2026-03-14 23:12:00`
> Scope: `pilot core 12 + holdout 4 population into RELATION_GRAPH_CANONICAL_V1`
> Reporting Rule: `append-only only`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260314_REV81_pilot_population_assignment.md`

## Action Taken

- updated:
  - `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- populated:
  - core 12 pilot ids
  - holdout 4 ids
  - node inventory for all 16 ids
  - minimal edge draft 4건

## Node Inventory Summary

- core 12 families:
  - `relative_day`: `오늘_일반명사-1`, `내일_일반명사-1`, `어제_일반명사-1`
  - `day_part`: `아침_일반명사-1`, `저녁_일반명사-1`, `밤_일반명사-1`
  - `week_anchor`: `월요일_일반명사-1`, `금요일_일반명사-1`, `주말_일반명사-1`
  - `season_anchor`: `봄_일반명사-1`, `여름_일반명사-1`, `겨울_일반명사-1`
- holdout 4 families:
  - `ambiguity_temporal_adverb`: `오늘_일반부사-1`, `어제_일반부사-1`
  - `ambiguity_meal_time`: `점심_일반명사-1`, `저녁_일반명사-2`

## Minimal Edge Draft Scope

- populated edges:
  - `저녁_일반명사-1 -> 밤_일반명사-1`
  - `밤_일반명사-1 -> 저녁_일반명사-1`
  - `금요일_일반명사-1 -> 주말_일반명사-1`
  - `주말_일반명사-1 -> 금요일_일반명사-1`
- holdout policy:
  - `오늘/어제` noun-adverb ambiguity pair와 `점심/저녁(식생활)` meal pair는 node만 시드하고 edge는 보류함

## Evidence Basis

- node inventory basis:
  - `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- edge basis:
  - current live `cross_links` intersection
  - current live `related_vocab` intersection
- edge draft constraint:
  - live-supported 교집합만 채웠고, 추정성 높은 jump는 의도적으로 제외함

## Non-Execution Guard

- `publish-only` not executed
- `chunk rebuild` not executed
- `live/` overwrite not executed

## Next Recommendation

- next revision에서
  - holdout disambiguation 기준을 먼저 닫고
  - pilot edge를 2차 확장할지 결정한 뒤
  - projection preview memo를 정교화하는 순서를 권장
