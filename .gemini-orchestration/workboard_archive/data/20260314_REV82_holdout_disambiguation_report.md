# Data Holdout Disambiguation Report

> Agent: `데이터 에이전트`
> Revision: `V1-REV-82`
> Logged: `2026-03-14 23:19:00`
> Scope: `holdout ambiguity sense boundary / handling rule / node-edge hold criteria`
> Reporting Rule: `append-only only`

## Skills Used

- `data-validation`
- `korean-lexical-data-curation`
- `multi-agent-orchestration`

## Authoritative Inputs Read

- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `.gemini-orchestration/workboard_archive/data/20260314_REV81_pilot_population_report.md`

## Evidence Surfaces Checked

- `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`

## Executive Rule

- 추천안:
  - holdout ambiguity는 모두 `node seeded / edge held` 상태를 유지한다.
  - 해제 조건은 `surface ambiguity가 target_id 수준으로 닫히고`, `learner-facing jump purpose가 명시되고`, `현재 runtime-safe word_to_word contract 안에서 투영 가능할 때`로 둔다.

## Sense Boundary 1: `오늘/어제` 명사 vs 부사

### Boundary

- `오늘_일반명사-1`, `어제_일반명사-1`
  - lexical role: 날짜/시점 자체를 가리키는 **time-point noun**
  - learner task: “어느 날인가”를 명사 단위로 파악
- `오늘_일반부사-1`, `어제_일반부사-1`
  - lexical role: 사건의 발생 시점을 꾸미는 **temporal adverb**
  - learner task: “언제 일어났는가”를 문장 부사로 처리

### Evidence

- `오늘_일반명사-1`: `지금 지나가고 있는 이날`
- `오늘_일반부사-1`: `바로 지금 지나가고 있는 날`
- `어제_일반명사-1`: `오늘의 하루 전날`
- `어제_일반부사-1`: `오늘의 바로 전날`

### Handling Rule

- node rule:
  - noun sense와 adverb sense는 **동일 표면형이라도 별도 node 유지**
  - noun sense만 현재 pilot core anchor contract의 direct candidate로 취급
  - adverb sense는 `holdout` 유지
- edge rule:
  - noun <-> adverb 직접 edge는 현재 revision에서 만들지 않음
  - 이유:
    - 같은 표면형 반복은 learner navigation value보다 sense collapse 위험이 큼
    - 현재 runtime thin projection의 `related_vocab`는 `string[]`이므로 `어제`/`오늘`를 target_id 단위로 구분해 투영할 수 없음

## Sense Boundary 2: `점심/저녁` 시간 vs 식사

### Boundary

- `저녁_일반명사-1`
  - lexical role: 해가 진 뒤 잠들기 전까지의 **day-part / time anchor**
  - learner task: 시간대 개념, 일과 흐름, 장면 전환 anchor
- `점심_일반명사-1`, `저녁_일반명사-2`
  - lexical role: 특정 시간대에 먹는 **meal / scene noun**
  - learner task: 식사 장면, 메뉴, 생활 루틴

### Evidence

- `저녁_일반명사-1`: `해가 지고 난 뒤부터 잠자리에 들 때까지의 시간`
- `점심_일반명사-1`: `낮에 먹는 식사`
- `저녁_일반명사-2`: `하루 중 저녁때 먹는 밥`

### Handling Rule

- node rule:
  - `저녁_일반명사-1`은 `day_part` core anchor 유지
  - `점심_일반명사-1`, `저녁_일반명사-2`는 `ambiguity_meal_time` holdout 유지
- edge rule:
  - `점심 -> 저녁` 또는 `저녁(식사) -> 점심` edge는 현재 revision에서 만들지 않음
  - `저녁(시간) -> 저녁(식사)` edge도 만들지 않음
  - 이유:
    - meal senses는 시간 anchor가 아니라 scene noun이며, pilot 목표인 coordinate-time anchor graph를 흐림
    - 현재 `related_vocab`가 문자열 `"저녁"`만 제공해 `저녁_일반명사-1`과 `저녁_일반명사-2`를 분리 투영할 수 없음

## Node Hold Criteria

- 아래 중 하나라도 맞으면 holdout node로 유지:
  - 동일 표면형이 둘 이상 존재하고 현재 live projection이 `target_id`가 아닌 문자열 기준이라 sense-safe하지 않음
  - 같은 한국어 표면형이지만 learner task가 `time anchor`와 `scene noun`처럼 다름
  - 현재 pilot 범위가 `coordinate_time_anchors_only`인데 해당 sense가 meal/scene 쪽으로 흐름
  - current live data에서 explicit cross-link evidence가 없고, relation 생성이 해석 의존적임

## Edge Hold Criteria

- 아래 중 하나라도 맞으면 edge 보류:
  - `related_vocab` string만으로 target sense를 유일하게 확정할 수 없음
  - `display_intent`가 `related_vocab`인지 `cross_links`인지 결정돼도 learner jump purpose가 불명확함
  - edge가 생성되면 동일 표면형 sense collapse를 일으킬 가능성이 큼
  - edge가 사실상 `word_to_scene` 또는 sense-switch contract를 요구하는데 current runtime-safe relation type은 `word_to_word`만 허용함

## Connection To REV81 Pilot Population

- maintain as-is:
  - core 12 node inventory는 유지
  - existing minimal 4 edges는 유지
- keep held:
  - `오늘_일반부사-1`
  - `어제_일반부사-1`
  - `점심_일반명사-1`
  - `저녁_일반명사-2`
- specific hold effects:
  - holdout 4는 `nodes`에는 남되 `edges`에는 추가하지 않음
  - `오늘/어제` noun-adverb pair는 relation candidate가 아니라 `sense boundary candidate`로만 관리
  - `점심/저녁(식사)` pair는 relation candidate가 아니라 `scene-side reserve candidate`로 관리

## Recommended Next Rule For Future Revisions

- noun-adverb pair 해제 조건:
  - internal canonical에 `sense_switch` 또는 동급의 non-runtime projection contract가 도입될 때만 재검토
- meal-time pair 해제 조건:
  - `time anchor`와 `meal scene`을 잇는 별도 contract가 승인될 때만 재검토
  - 예: internal-only `word_to_scene` reserve를 실제 operational type으로 승격하는 경우

## Non-Execution Guard

- `projection preview` not executed
- `publish` not executed
- `chunk rebuild` not executed
- `live overwrite` not executed

## Conclusion

- `오늘/어제`는 **품사-기능 경계 ambiguity**
- `점심/저녁`은 **시간 anchor vs 식사 scene 경계 ambiguity**
- 두 축 모두 현재 pilot 단계에서는 **node seeded / edge held**가 가장 안전한 처리 rule이다
