# Planning Detailed Report Log

> Agent: `기획 에이전트`
> Revision: `V1-REV-74`
> Logged: `2026-03-14`
> Status: `PROPOSAL ONLY / NOT APPROVED`
> Rule: canonical policy, 분류 규칙, roadmap, tasklist는 **Codex 검토 + 사용자 승인 전 확정 반영 금지**
> Reporting Rule: `append-only only`

## Scope

- `related_vocab` / `refs.cross_links`의 현재 internal 정의 확인
- 학습자 관점 relation model 재정의
- 내용 sufficiency / 구조 sufficiency 분리 평가
- learner scenario / 서비스 시나리오 정리
- 다음 cycle용 planning package, owner docs map, execution order, handoff gate 제안
- 외부 딥 리서치 용역용 상세 프롬프트 초안 작성

## Sources Used

### Internal canonical / implementation

- `README.md`
- `PROJECT_DOCUMENT_MAP.md`
- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/PLANNING_AGENT_WORKBOARD_V1.md`
- `08_expansion/README.md`
- `08_expansion/MASTER_ROADMAP_V1.md`
- `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- `08_expansion/RELATION_DATA_POLICY_V1.md`
- `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
- `08_expansion/PROJECT_DECISION_LOG_V1.md`
- `.gemini-orchestration/workboard_archive/planning/20260314_REV72_policy_rework_snapshot.md`
- `.gemini-orchestration/workboard_archive/review/20260314_REV73_policy_review_snapshot.md`
- `.gemini-orchestration/workboard_archive/development/20260314_REV70_release_hardening_snapshot.md`
- `scripts/mining/run_rev47_xwd_mining.py`
- `09_app/src/App.jsx`
- `09_app/src/components/TermDetail.jsx`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`

### Web research

- [Korean-English Learners' Dictionary - Search by Category](https://krdict.korean.go.kr/eng)  
  - category/theme based entry access, learner-facing Korean-English dictionary position
- [Korean-English Learners' Dictionary - Translation Guidelines](https://krdict.korean.go.kr/eng/dicSearch/translationGuide?nation=eng)  
  - learner-facing translation policy, natural beginner/intermediate wording emphasis
- [Cambridge Dictionary Help - SMART Vocabulary](https://dictionary.cambridge.org/help/smart-vocabulary)  
  - topic clusters, related words, phrase/synonym navigation
- [Longman Dictionary of Contemporary English Online](https://www.ldoceonline.com/)  
  - collocations, thesaurus, examples, word sets for learner navigation
- [Oxford Research: Hyperlinks in electronic dictionaries](https://doi.org/10.1093/ijl/ecad015)  
  - dictionary hyperlink utility depends on clear function and low clutter
- [Oxford Research: Accessing collocations in a learner's dictionary](https://doi.org/10.1093/ijl/ecac015)  
  - learners struggle when related information is present but retrieval path is unclear

### Attached deep research artifact

- `08_expansion/references/relation_model_research/20260314_relation_model_deep_research_report_v1.md`
  - external-style deep research synthesis copied into workspace for stable reference
  - relation model 비교 연구, learner dictionary usage pattern, time-anchor jump pattern, minimum schema 제안 포함

## 문제 진단

### 1. 현재 internal 정의

- current policy definition:
  - `related_vocab` = source/target의 `system`, `root`, `category`가 모두 같을 때 유지되는 가까운 단어 목록
  - `refs.cross_links` = 위 셋 중 하나라도 다르면 보내는 횡단 링크
- current implementation definition:
  - `scripts/mining/run_rev47_xwd_mining.py` publish 단계에서 같은 분류권이면 `related_vocab`, 아니면 `refs.cross_links`로 분기
  - `related_vocab`는 runtime에서 `string[]`만 저장
  - `refs.cross_links`는 `target_id`, `target_term`, `target_system`, `target_root`, `target_category`, `hook_id`만 저장
- current UI interpretation:
  - `related_vocab`는 “연관 어휘” 칩
  - `cross_links`는 “교차 연결 장면” 칩
  - `App.jsx`는 `cross_links` 클릭 시 `target_id` 우선, 없으면 `target_term` fallback으로 탐색

### 2. 현재 데이터 상태 요약

- search index 기준 `8092`개 항목
- `related_vocab` non-empty: `7631`
- `cross_links` non-empty: `805`
- `related_vocab` 평균 길이: `3.57`, 최대 `5`
- `cross_links` 평균 길이: `1.31`, 최대 `5`
- `related_vocab`는 전부 문자열(`27256` relation slots)
- `cross_links` shape는 사실상 1종으로 고정
- `cross_links` 총 edge `1052` 중 same-system edge가 `868`개
  - 즉 현재 `cross_links`는 “다른 탭으로 점프”보다 “분류권을 넘는 이동”에 더 가깝다

### 3. 학습자 관점에서의 정의 부족

- 현재 정의는 **분류 경계**에는 강하지만, **학습 목적**에는 약하다.
- 같은 category라고 모두 learner에게 “같이 봐야 할 단어”는 아니다.
- 다른 category라고 모두 learner에게 “지금 점프해야 할 단어”도 아니다.
- 현재 구조만으로는 아래 질문에 답하기 어렵다.
  - 이 단어와 무엇을 비교하면 좋은가
  - 어떤 단어로 바꿔 말할 수 있는가
  - 어떤 장면/문법 포인트로 넘어가면 학습 효율이 커지는가
  - 왜 이 jump가 추천되는가

### 4. learner scenario 관점의 문제

- `related_vocab`는 현재 “가까움”만 있고, `비교/대체/대조/확장` 중 어떤 가까움인지 없다.
- `cross_links`는 현재 target path는 있지만, `왜 지금 이동해야 하는지`가 없다.
- 시간/계절/요일 같은 anchor 어휘는 learner journey에서 장면 전환의 핵심인데, 현재는 mandatory jump coverage가 빈약하다.
- 실제 샘플에서 시간 anchor 다수는 cross-link가 `0`이거나, 있어도 jump purpose가 불명확하다.

### 5. 웹 리서치 비교 진단

- Korean-English Learners' Dictionary는 category/theme entry 접근을 지원한다.  
  - 의미: learner 탐색은 알파벳/표제어 검색만이 아니라 주제 진입이 중요하다.
- Cambridge SMART Vocabulary는 related words를 topic cluster로 묶고, phrase/synonym으로 추가 탐색을 연다.  
  - 의미: relation은 단순 링크보다 “묶음의 이름”과 “학습 의도”가 중요하다.
- Longman은 collocations, thesaurus, examples를 함께 묶는다.  
  - 의미: learner relation은 단어 주변망뿐 아니라 실제 사용 선택을 돕는 비교 장치여야 한다.
- Oxford 연구는 hyperlink가 많아도 기능이 불분명하면 잘 쓰이지 않는다고 본다.  
  - 의미: 현재 `cross_links`는 존재 자체보다 jump purpose labeling이 더 중요하다.

## 해결안

### 1. relation model 재정의안

#### `related_vocab`

- 재정의:
  - 현재 보고 있는 단어를 **같은 시야 안에서 비교, 대체, 대조, 국소 확장**하는 데 필요한 learner-neighborhood
- learner question:
  - “이 장면/기능 안에서 같이 비교해서 익혀야 할 단어는 무엇인가?”
- 허용 역할:
  - `compare`: 비슷하지만 차이를 봐야 하는 단어
  - `substitute`: 문맥상 바꿔 써 볼 수 있는 단어
  - `contrast-lite`: 헷갈리기 쉬워 같이 보여 줘야 하는 단어
  - `scope-expand`: 같은 장면 안에서 바로 옆으로 확장되는 단어
- 배제 기준:
  - 같은 category라는 이유만으로 자동 포함 금지
  - learner에게 즉시 비교 가치가 없으면 제외

#### `refs.cross_links`

- 재정의:
  - 현재 단어를 이해한 뒤 **다른 장면, 다른 기능, 다른 학습 축으로 넘어가게 하는 next-step jump**
- learner question:
  - “이 단어를 알았으면 다음에 어디로 점프해야 실제 사용이 쉬워지는가?”
- 허용 역할:
  - `scene-jump`: 다른 장면/상황으로 이동
  - `grammar-anchor`: 시간/수량/방향 등 구조 어휘를 실제 장면과 연결
  - `usage-route`: 표현/감정/평가 쪽으로 이동
  - `sense-disambiguation`: 다른 의미권으로 이동
- 배제 기준:
  - 분류권이 다르다는 사실만으로 자동 포함 금지
  - learner action이 열리지 않으면 제외

### 2. learner scenario / 서비스 시나리오

#### Scenario A. 단어 선택 비교

- learner는 `가게`를 보고 `매장`, `매점`, `시장`의 차이를 빠르게 비교하고 싶다.
- 이때 필요한 것은 분류 일치 여부보다 “같은 상황에서 혼동/대체될 수 있는지”다.
- owner: `RELATION_DATA_POLICY`

#### Scenario B. 장면 확장

- learner는 `병원`을 배운 뒤 `예약`, `접수`, `진료`, `처방` 쪽으로 장면을 넓히고 싶다.
- 이 경우 `related_vocab`는 장면 내 국소 확장, `cross_links`는 다른 root나 기능권으로 넘어가는 안내가 된다.
- owner: `RELATION_DATA_POLICY`

#### Scenario C. 시간 anchor jump

- learner는 `아침`, `봄`, `금요일` 같은 구조 어휘를 장면 없는 추상 정보로만 익히면 활용이 약하다.
- 이 단어들은 `등교`, `출근`, `아침 식사`, `소풍`, `주말 약속` 같은 장면으로 연결되어야 한다.
- owner split:
  - 분류 위치 판정: `SDCP`
  - jump obligation: `RELATION_DATA_POLICY`

#### Scenario D. bilingual learner lookup

- 영어권 learner는 번역만으로는 usage choice를 못 닫는다.
- `related_vocab`는 near-equivalent cluster, `cross_links`는 usage scene jump를 담당해야 한다.
- owner: `RELATION_DATA_POLICY` + UI later

### 3. sufficiency 평가

#### 내용 sufficiency

- 강점:
  - relation 자체는 이미 광범위하게 주입되어 있다.
  - 대부분 항목에 `related_vocab`가 있어 주변 탐색의 시작점은 존재한다.
  - `cross_links`는 최소한 target path와 hook trace를 보존한다.
- 부족:
  - relation purpose가 없다.
  - 시간 anchor, 학습 빈도 높은 일상 scene bridge, compare/contrast pair coverage 기준이 없다.
  - `cross_links`는 coverage보다 “왜 이 점프가 learner에게 유의미한가” 설명이 빠져 있다.
  - same-system cross-link가 많아 “교차 연결 장면”이라는 UI 해석과 실제 데이터 의미가 어긋난다.

#### 구조 sufficiency

- 강점:
  - thin runtime 구조라 배포와 렌더링은 단순하다.
  - `cross_links`는 최소한 `target_id`와 path metadata가 있어 점프는 가능하다.
- 부족:
  - `related_vocab`가 `string[]`라 target identity, relation role, reason, ranking을 잃는다.
  - `cross_links`에도 `jump_purpose`, `reason`, `source-side learner prompt`가 없다.
  - UI가 `target_term` fallback을 유지하고 있어 구조적으로 취약하다.
  - search/split/detail 간 의미 일치는 맞지만, pedagogic contract는 비어 있다.

### 4. 개선안

#### 내용 부족 시 개선안

- `related_vocab`를 “같은 분류권” 기준에서 “같이 비교/대체/대조할 가치” 기준으로 재선별
- 시간/계절/요일/시점 anchor에 대해 scene-jump 의무 기준 도입
- 상위 learner value bucket 우선순위 도입
  - A급: 일상 장면 이동에 직결되는 anchor
  - B급: 혼동/대조 학습 가치가 큰 near-equivalent
  - C급: 범주 확장용 주변 어휘
- `cross_links`는 source별 최소 1개가 아니라, “jump purpose가 명확한 1개 이상” 기준으로 재설계

#### 구조 부족 시 개선안

- internal canonical relation layer는 아래 필드를 유지하도록 증설 제안
  - `target_id`
  - `target_term`
  - `relation_role`
  - `jump_purpose`
  - `reason`
  - `hook_id`
  - `target_system/root/category`
- runtime live는 당장 thin projection을 유지할 수 있음
  - 단, internal canonical / review artifact에서는 richer record를 유지해야 함
- UI 표시는 향후 단계에서 다음처럼 정렬
  - `related_vocab` = 비교/대체/확장 라벨
  - `cross_links` = 왜 이동해야 하는지 한 줄 목적 라벨

### 5. planning options

#### Option 1. Policy Closure First

- 추천안
- 요지:
  - relation 정의, 분류 경계, owner map, rebuild gate를 문서별 delta 초안으로 먼저 닫고 그 뒤 data cycle을 연다.
- 장점:
  - 다음 cycle의 기준이 가장 명확하다.
  - data/review 재작업 가능성이 가장 낮다.
  - dashboard/workboard의 current control 구조와 충돌이 적다.
- 리스크:
  - 초반 체감 속도는 가장 느리다.

#### Option 2. Policy + Sample Probe

- 요지:
  - policy proposal과 함께 시간 anchor 샘플군만 별도 probe 설계
- 장점:
  - anchor 부족 지점을 빠르게 확인할 수 있다.
- 리스크:
  - 승인 전 실데이터 probe 요구로 오해될 수 있다.
  - 이번 요청의 “planning closure 우선”과 긴장된다.

#### Option 3. External Deep Research First

- 요지:
  - 외부 딥 리서치 결과를 먼저 받아 relation model을 더 풍부하게 닫는다.
- 장점:
  - 한국어 교육/사전 서비스 비교가 더 탄탄해질 수 있다.
- 리스크:
  - 현재 cycle 개시가 늦어진다.
  - 외부 결과 품질 편차가 크면 다시 정리 비용이 생긴다.

### 6. 문서별 delta 초안

> 아래는 **proposal draft only**다. canonical 반영 확정 아님.

#### `08_expansion/RELATION_DATA_POLICY_V1.md`

- 추가할 내용:
  - current internal operating definition와 learner-facing canonical definition 분리
  - `related_vocab`를 compare/substitute/contrast-lite/scope-expand 장치로 재정의
  - `cross_links`를 scene-jump/grammar-anchor/usage-route 장치로 재정의
  - time anchor jump obligation 명시
  - thin runtime vs richer internal canonical relation layer 분리 명시
- owner reason:
  - relation semantics와 relation data contract의 primary owner이기 때문

#### `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`

- 추가할 내용:
  - 좌표성 시간 vs 내용성 시간 판정 게이트
  - `제거 테스트`, `IS-A 테스트`를 분류 판정 루틴으로 명문화
  - relation owner boundary 명시
    - 분류 위치는 SDCP owner
    - jump obligation은 Relation Policy owner
- owner reason:
  - 분류 경계와 axis placement의 primary owner이기 때문

#### `08_expansion/PROJECT_DECISION_LOG_V1.md`

- 추가할 내용:
  - relation model redefinition 결정 기록
  - owner docs map 기록
  - next cycle gate sequence 기록
- owner reason:
  - 구조 변경의 승인 이력을 남기는 SSOT이기 때문

#### `08_expansion/MASTER_ROADMAP_V1.md`

- 추가할 내용:
  - Phase 3를 work package 중심으로 재묶기
    - WP-A Policy Closure
    - WP-B Reclassification + Anchored Relation Rebuild
    - WP-C Review Acceptance + Limited Runtime Handoff
- owner reason:
  - phase framing과 package intent의 primary owner이기 때문

#### `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`

- 추가할 내용:
  - T1.30/T1.31/T2.16/T2.17/T4.6/T3.16/T1.32를 work package와 handoff gate 기준으로 묶는 운영 메모
  - planning -> data -> review -> dev 순 gate와 completion evidence 정의
  - external deep research 결과가 들어올 경우 merge 위치 명시
- owner reason:
  - 실제 집행 순서, gate, done criteria의 single authoritative todo이기 때문

## owner 문서

### Owner Docs Map

- relation semantic definition owner:
  - `08_expansion/RELATION_DATA_POLICY_V1.md`
- classification boundary owner:
  - `08_expansion/STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
- decision trace owner:
  - `08_expansion/PROJECT_DECISION_LOG_V1.md`
- phase/package framing owner:
  - `08_expansion/MASTER_ROADMAP_V1.md`
- execution order / gate / done criteria owner:
  - `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`
- append-only proposal / review memo owner:
  - `.gemini-orchestration/workboard_archive/planning/`

## 다음 순서

### Recommended Execution Order

1. planning proposal 검토
2. Codex가 proposal을 canonical delta candidate로 정리
3. 사용자 승인 후에만 canonical 문서 반영
4. 승인 후 data agent에 execution handoff
5. data 결과를 review agent가 acceptance 검수
6. review 통과 후에만 dev handoff
7. dev는 limited runtime/UI adjustment만 수행

### Handoff Gate

#### Gate 1. Planning -> Data

- 필요 산출물:
  - 승인된 relation model delta
  - 승인된 시간 anchor 기준
  - owner docs map
  - sample acceptance checklist
- gate question:
  - “data agent가 추가 해석 없이 재분류/주입을 바로 집행할 수 있는가?”

#### Gate 2. Data -> Review

- 필요 산출물:
  - rebuild output stats
  - anchor coverage report
  - relation integrity report
  - changed term sample set
- gate question:
  - “policy delta가 실제 8.5K 산출물에 반영되었는가?”

#### Gate 3. Review -> Dev

- 필요 산출물:
  - acceptance verdict
  - runtime-safe field contract
  - UI-visible behavior checklist
- gate question:
  - “UI가 바뀐 relation semantics를 오해 없이 렌더링할 수 있는가?”

## 완료 기준

### Planning completion criteria

- `related_vocab` / `cross_links`가 learner-facing terms로 구분 정의됨
- 내용 sufficiency / 구조 sufficiency가 분리 평가됨
- learner scenario / 서비스 시나리오가 최소 3종 이상 닫힘
- owner docs map이 명시됨
- execution order와 handoff gate가 명시됨
- 외부 딥 리서치 의뢰문이 준비됨
- canonical 반영 전 승인 필요 상태가 명확히 기록됨

### Next cycle open criteria

- 사용자 승인 포함한 canonical delta 확정
- data agent용 execution brief 생성 완료
- review acceptance checklist 사전 합의

## 외부 딥 리서치 지시문

### Recommended Outsourcing Prompt

아래 프롬프트를 그대로 외부 딥 리서치 용역에 전달하는 것을 권장합니다.

```text
프로젝트 배경:
우리는 외국인 한국어 학습자를 위한 한국어 어휘 탐색 서비스의 relation model을 재설계하려고 합니다. 현재 서비스는 단어별로 related_vocab와 cross_links를 제공하지만, 현재 정의는 분류 기준 중심이고 학습자 관점의 탐색 목적이 충분히 닫혀 있지 않습니다.

당신의 과업:
한국어 교육, 한국어 학습자용 사전(특히 한국어-영어), 영어 learner's dictionary, 그리고 학습자용 어휘 탐색 UX 사례를 조사해 다음 질문에 답하십시오.

핵심 질문:
1. learner-facing dictionary/service에서 “related words”는 어떤 학습 목적(비교, 대체, 대조, collocation, topic expansion 등)으로 운영되는가?
2. learner-facing dictionary/service에서 “cross-link / jump / see also / topic move”는 어떤 목적(장면 전환, 문법 anchor, sense disambiguation, function move 등)으로 운영되는가?
3. 한국어 학습자에게 시간/요일/계절/시점 같은 구조 어휘를 실제 장면과 연결할 때 어떤 탐색 패턴이 가장 유효한가?
4. bilingual learner가 번역만으로 해결되지 않는 경우, 어떤 relation information이 추가로 필요해지는가?
5. relation 데이터를 서비스에 넣을 때 최소 필드와 권장 필드는 무엇인가?

반드시 포함할 것:
- 공식 사전/공식 서비스/공신력 있는 연구 중심으로 조사
- 한국어 학습자용 사전 최소 2종
- 영어 learner's dictionary 최소 2종
- 학습자용 relation 탐색 UX 패턴 최소 5종
- 시간 anchor 또는 grammar anchor 관련 학습 사례 최소 5종

반드시 제외할 것:
- 일반 SEO 블로그 요약
- 출처 없는 마케팅 글
- 생성형 AI가 다시 요약한 2차 콘텐츠

원하는 산출물 형식:
1. Executive summary (10문장 이내)
2. Source table
   - source name
   - url
   - type (official dictionary / official help / research / paper)
   - relevant feature
   - direct implication for our service
3. Related words model synthesis
   - role taxonomy
   - good examples
   - design cautions
4. Cross-link model synthesis
   - jump taxonomy
   - good examples
   - design cautions
5. Time anchor / grammar anchor section
   - what learners need
   - recommended jump patterns
   - anti-patterns
6. Proposed minimum schema
   - must-have fields
   - nice-to-have fields
7. Decision memo for PM
   - recommend
   - why
   - risks

추가 요구:
- 각 주장마다 source citation을 붙이십시오.
- 단순 feature 나열이 아니라 learner task 중심으로 정리하십시오.
- “현재 단어를 본 뒤 다음에 어디로 이동해야 학습 효율이 커지는가”라는 관점으로 cross-link를 해석하십시오.
- “같은 장면 안에서 왜 이 단어들을 같이 보여 줘야 하는가”라는 관점으로 related words를 해석하십시오.
```

## next action 제안

- immediate next action:
  - 본 proposal을 Codex 검토 대상으로 올리고, canonical 반영 후보 delta만 정리
- if user wants external research now:
  - 위 프롬프트로 용역 발주 후 결과 회수
  - 회수 결과를 planning appendix로 병합
- if user wants internal-only next:
  - user 승인 전까지는 canonical 미수정 유지
  - 승인 후 문서별 patch set을 한 번에 적용

## Conclusion

- 이번 cycle에서 planning agent가 지금 확정할 수 있는 것은 **proposal draft**까지다.
- canonical policy / SDCP / roadmap / tasklist 동시 변경은 사용자 승인 전 확정 불가다.
- 따라서 현재 가장 적절한 산출물은:
  - relation model 재정의안
  - sufficiency 평가
  - owner docs map
  - execution order / handoff gate
  - document-wise delta draft
  - external deep research prompt
- 위 산출물은 본 append-only 로그에 제출 완료한다.
