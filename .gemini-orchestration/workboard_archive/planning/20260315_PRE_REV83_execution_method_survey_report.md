# Planning Survey Memo

> Agent: `기획 에이전트`
> Revision: `V1-PRE-REV-83-PLAN`
> Logged: `2026-03-15`
> Status: `REPORTED`
> Scope: `REV-82` 결론 고정 하의 bounded pre-REV-83 blind spot survey

1. 우려사항: `REV-83` 시작 전에 write target이 흐리면, core 12 population과 holdout 4 hold rule이 같은 pass에서 섞여 derived artifact까지 오염될 수 있음.
대안: `internal canonical only write`와 `preview/publish 계열`을 분리한다.
추천안: `REV-83`의 쓰기 대상은 `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`과 append-only 보고로만 고정하고, `live/*`, `publish-only`, `chunk rebuild`, `live overwrite`는 revision 범위에서 명시적으로 금지한다.

2. 우려사항: 작업 순서가 `core 12 확정 -> holdout 4 masking -> edge 입력`으로 고정되지 않으면, holdout 4가 한번이라도 edge 계산에 끼어 preview 후보를 오염시킬 수 있음.
대안: holdout masking을 edge 작업보다 앞에 둔다.
추천안: `skeleton 확인 -> core 12 node inventory 확정 -> holdout 4 mask 적용 -> holdout 4 outgoing/incoming edge 0 확인 -> core 12 edge 입력` 순서로만 진행한다.

3. 우려사항: validation이 count 확인만으로 끝나면, surface collision이나 holdout leak를 놓친 채 `REV-83`을 닫을 수 있음.
대안: count, boundary, no-execution을 같이 본다.
추천안: `core 12만 edge-bearing 대상인지`, `holdout 4는 node 존재 / edge 0 / preview projection 0인지`, `projection preview / publish / chunk rebuild / live overwrite가 모두 미실행인지`를 필수 검증점으로 고정한다.
