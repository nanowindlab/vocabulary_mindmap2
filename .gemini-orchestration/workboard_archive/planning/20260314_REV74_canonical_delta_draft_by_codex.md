# Canonical Delta Draft By Codex

> Source Basis:
> - `.gemini-orchestration/workboard_archive/planning/20260314_REV74_relation_model_execution_closure_proposal.md`
> - `08_expansion/references/relation_model_research/20260314_relation_model_deep_research_report_v1.md`
>
> Status: `DRAFT / NOT APPLIED`
> Purpose: planning proposal을 canonical owner 문서별 실제 반영 단위로 압축한 Codex 검토 초안

## 1. RELATION_DATA_POLICY_V1.md Delta

### Add: relation의 learner-facing 재정의

- `related_vocab`를 “같은 분류권 안의 가까운 단어”가 아니라
  - 같은 화면에서 같이 보여 줄 이유가 있는 learner-neighborhood
  - 비교, 대체, 대조, 국소 확장용 relation
  로 재정의

- `refs.cross_links`를 “다른 분류로 넘어가는 연결”이 아니라
  - 다음 학습 단계로 이동시키는 next-step jump
  - scene-jump / grammar-anchor / usage-route / sense-disambiguation
  용 relation
  로 재정의

### Add: learner scenario section

- 서비스 기획 시나리오:
  - 단어 선택 비교
  - 장면 확장
  - 시간/요일/계절 anchor jump
  - bilingual learner lookup

### Add: sufficiency judgment section

- 내용 sufficiency와 구조 sufficiency를 분리해서 판단하는 기준
- 현재 구조의 강점/약점
- 현재 내용의 강점/약점

### Add: minimum internal relation schema guidance

- 최소 필드:
  - `target_id`
  - `target_term`
  - `relation_role`
  - `jump_purpose`
  - `reason`
  - `hook_id`
  - `target_system`
  - `target_root`
  - `target_category`

### Add: time-anchor obligation rule

- `Basics`로 이관된 시간/계절/요일 anchor는
  - learner scene로 이어지는 `Situations` jump를 최소 1개 이상 가져야 함
  - 단, 단순 분류 차이만으로 cross-link를 만들지 말고 jump purpose가 명시돼야 함

## 2. STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md Delta

### Add: 좌표성 시간 vs 내용성 시간

- `좌표성 시간`
  - 달력, 시각, 주기, 요일, 계절처럼 시간 좌표를 지정하는 어휘
  - 기본 축: `구조와 기초`

- `내용성 시간`
  - 사건, 관습, 활동 장면과 결합해 학습 장면을 여는 시간 표현
  - 필요 시 `상황과 장소` 쪽 relation 또는 jump로 연결

### Add: explicit test rules

- `제거 테스트`
  - 시간 표현을 제거해도 장면의 본질이 유지되면 anchor일 가능성이 높음
- `IS-A 테스트`
  - 해당 어휘가 장면 자체인지, 장면을 좌표화하는 도구인지 판정

### Add: placement + relation split rule

- `Basics` 배치 여부와 `Situations` 연결 여부를 분리
- 분류는 `Basics`, 학습 전이는 `Situations` jump로 해결 가능하다는 원칙 명시

## 3. PROJECT_DECISION_LOG_V1.md Delta

### Add: decision entries only

- `related_vocab`를 learner-neighborhood로 재정의
- `cross_links`를 next-step jump로 재정의
- 시간 anchor는 분류와 학습 전이를 분리해 다룸
- `내용성 시간`, `제거 테스트`, `IS-A 테스트`를 canonical rule로 채택

원칙:

- 상세 규칙 본문은 넣지 않음
- “무엇을 결정했고 왜 바뀌었는지”만 기록

## 4. MASTER_ROADMAP_V1.md Delta

### Adjust Phase 3 wording

- Phase 3의 첫 선행 조건을
  - policy closure
  - relation model redefinition
  - learner dictionary usage pattern reflection
  로 더 명확히 씀

### Add gate wording

- data rebuild는 policy closure 이후
- review acceptance는 data rebuild 이후
- limited dev reopen은 review acceptance 이후

## 5. SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md Delta

### Keep current Track 1 grouping, sharpen acceptance

- `T1.30`
  - relation 재정의 deliverable을 더 명시
  - learner scenario, sufficiency split, web research synthesis, owner docs map 포함

- `T1.31`
  - handoff gate를 더 명시
  - data input / review input / dev reopen condition을 acceptance로 추가

### Add acceptance bullets

- `T1.30` acceptance:
  - 정의 재정의
  - learner scenario
  - 내용/구조 sufficiency split
  - 개선안
  - owner docs map

- `T1.31` acceptance:
  - execution order
  - data handoff input
  - review acceptance input
  - dev reopen condition
  - deep research external prompt

## 6. Recommended Apply Order

1. `RELATION_DATA_POLICY_V1.md`
2. `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`
3. `PROJECT_DECISION_LOG_V1.md`
4. `MASTER_ROADMAP_V1.md`
5. `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`

## 7. Why This Order

- relation meaning을 먼저 잠가야
- 분류 규칙과 jump rule이 서로 안 엇갈리고
- 결정 로그는 그 뒤 요약만 남기며
- roadmap/tasklist는 실행 연결만 반영할 수 있음
