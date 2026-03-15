# Source-Rich Implementation Tasklist V11 (ULTIMATE)

> Version: `V11-ULTIMATE`
> Date: `2026-03-14`
> Owner: `Gemini Orchestrator (Manager)`
> Status: `ACTIVE - Data Execution Phase`
> Role: `Single Authoritative Tasklist / Todo`

---

## 1. 3대 핵심 체계 (3 Pillars) - [LOCKED]
- **[상황과 장소]**: 물리적 공간 및 실생활 Scene 중심.
- **[마음과 표현]**: 내면 감정, 오감 묘사, 주관적 평가 중심.
- **[구조와 기초]**: 문장 골격, 숫자, 시간, 논리, 지시어 중심. (SDCP V5 좌표성 시간 포함)

---

## 2. 상세 태스크 및 체크리스트 (Tracks)

### Track 1. Integrated Planning (Planning Agent)

- [ ] **T1.30: [CURRENT-CRITICAL] 학습자 관점 relation model 재정의 및 재빌드 기준 closure**
    - [ ] `related_vocab`와 `refs.cross_links`를 데이터 필드가 아니라 학습자 탐색 장치로 다시 정의할 것.
    - [ ] 외국인 한국어 학습자 기준으로 두 관계가 각각 어떤 탐색 경험을 제공해야 하는지, 서비스 기획 시나리오와 learner journey 기준으로 명시할 것.
    - [ ] 현재 자료의 **내용 sufficiency**와 **구조 sufficiency**를 분리해 평가하고, 무엇이 부족한지 적시할 것.
    - [ ] 한국어 교육, 학습자용 단어 사전(한국어/영어), 연관 탐색 활용 실태를 웹 리서치로 보강하고 내부 정의와 비교할 것.
    - [ ] 결과는 `SDCP`, `Relation Policy`, `Decision Log` 중 어느 문서가 owner인지까지 포함하여 정리할 것.
- [ ] **T1.31: [CURRENT] 다음 재빌드 사이클 planning package 및 handoff gate 설계**
    - [ ] planning → data → review → dev 순서의 handoff gate를 명시할 것.
    - [ ] data 에이전트가 바로 집행 가능한 재분류/앵커링 기준과 review 에이전트의 acceptance 기준을 함께 정리할 것.
    - [ ] 외부 딥리서치가 필요하면 기대 산출물, 범위, 제외 범위, 참고 서비스, 반환 포맷까지 포함한 상세 의뢰문을 작성할 것.
    - [ ] 위 결과를 roadmap/tasklist 단위에서 의미 중심 work package로 다시 묶고, 파편적 TODO가 생기지 않도록 정리할 것.
- [ ] **T1.33: [CURRENT] planning proposal에 대한 data/review cross-check loop**
    - [ ] 데이터 에이전트는 기획 proposal이 의미하는 데이터 구조, runtime 영향, 재빌드 구현 요건을 건설적으로 비판할 것.
    - [ ] 리뷰 에이전트는 3인의 전문가 시각으로 proposal을 검토하고, 기획이 놓친 중요한 누락 포인트를 찾을 것.
    - [ ] 두 에이전트 모두 진단에서 끝나지 말고, planning 문서에 추가되어야 할 해결안/포함 항목을 제시할 것.
- [ ] **T1.34: [CURRENT] cross-check 반영 후 implementation architecture planning**
    - [ ] planning은 data/review cross-check 결과와 Codex 조언을 받아 implementation 구조를 재설계할 것.
    - [ ] `무엇을 어떻게 구현할지`, `어떤 구조로 반영할지`, `어떤 순서로 적용할지`를 문서 owner 기준으로 정리할 것.
    - [ ] canonical 문서 직접 반영 전 proposal delta와 apply order를 닫을 것.
    - [ ] `rich internal canonical`, `thin runtime projection`, `rebuild trigger matrix`, `pilot-first 전략`을 implementation architecture acceptance에 포함할 것.
- [ ] **T1.32: [RELEASE-READY] 학습자 안내 경험 패키지 정리**
    - [ ] 기존 `T1.14`, `T1.15`, `T1.16`을 하나의 release work package로 묶어 관리한다.
    - [ ] 선행 조건: `T2.16`, `T2.17` 완료 후 착수.
    - [ ] 범위: 온보딩 시나리오, 도움말 UI, 핵심 UI 텍스트 및 브랜딩 일관성.
- [ ] **T1.17: README.md 상시 현행화 및 프로젝트 개요 관리 [RULE]**
    - [ ] README에 연결된 핵심 문서(가이드, 로드맵 등) 작업 시, README의 링크와 요약 정보도 반드시 동시 업데이트할 것.
- [ ] **T1.35: [RULE] 배치용 에이전트 운영 모델 정립**
    - [ ] 반복 가능한 data/review work를 `batch type` 단위로 정의할 것.
    - [ ] 각 batch에 필요한 스킬, write target, evidence pack, acceptance check를 표준화할 것.
    - [ ] ambiguity/holdout가 큰 batch와 one-batch-one-rev 자동화가 가능한 batch를 구분하는 기준을 만들 것.
    - [ ] batch agent가 능동적으로 big step을 수행하고, PM은 batch 정의와 verdict에 집중할 수 있게 운영 모델을 정리할 것.

---

### Track 2. Data Engineering (Data Agent)

- 운영 메모: `T2.18~T2.22`는 pilot relation cycle로 해석한다. skeleton 준비 → pilot population/holdout disambiguation → pilot runtime projection → chunk rebuild gate까지 같은 pilot work package의 내부 단계다.
- [x] **T2.18: relation graph canonical pilot preparation**
    - [x] `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`의 empty skeleton과 field contract를 준비할 것.
    - [x] pilot 대상 anchor batch 범위를 정의할 것.
    - [x] 실제 publish/rebuild 전 필요한 dry-run 준비 항목과 검증 checklist를 정리할 것.
- [x] **T2.19: empty skeleton actual creation**
    - [x] `09_app/public/data/internal/RELATION_GRAPH_CANONICAL_V1.json`를 실제 파일로 생성할 것.
    - [x] field contract와 top-level structure가 current policy / SOP / data README와 일치하는지 확인할 것.
    - [x] pilot build 단계에서는 `publish-only`, `chunk rebuild`, `live overwrite`를 실행하지 말 것.
- [x] **T2.20: pilot batch population and holdout disambiguation**
    - [x] core 12 anchors + ambiguity holdout 4를 pilot batch로 채울 것.
    - [x] node inventory와 최소 edge 초안을 internal canonical skeleton에 반영할 것.
    - [x] `오늘/어제`, `점심/저녁`의 sense boundary와 holdout 처리 rule을 정리할 것.
    - [x] pilot build 단계에서는 `publish-only`, `chunk rebuild`, `live overwrite`를 실행하지 말 것.
- [x] **T2.21: pilot runtime projection**
    - [x] core 12 + holdout 4 pilot relation을 실제 runtime으로 투영할 것.
    - [x] target anchor 12개 projected bucket과 holdout exclusion을 live runtime에서 검증할 것.
- [x] **T2.22: chunk rebuild gate**
    - [x] detail chunk를 재생성하여 pilot ids의 search/tree/chunk 정합성을 닫을 것.
    - [x] holdout 4 exclusion이 chunk rich files에서도 유지되는지 검증할 것.
- [ ] **T2.23: [CURRENT] coverage expansion build package**
    - [ ] 다음 relation 확장 배치를 pilot 수준 품질로 어떻게 확장할지 package를 설계할 것.
    - [ ] ambiguity holdout, family-level reason consistency, runtime-safe projection 가능성을 함께 유지할 범위를 정의할 것.
    - [ ] expansion build와 이후 projection/rebuild gate를 어떤 배치 단위로 끊을지 정할 것.
- [ ] **T2.16: [SDCP V5] 8.5K 데이터셋 전수 재분류 실행 [CRITICAL]**
    - [ ] 선행 조건: `T1.34` implementation architecture proposal 승인 후 착수.
    - [ ] **좌표성 시간 이관**: 계절, 시간 어휘를 `Basics` 축으로 대대적 이동.
    - [ ] **이중 검증 적용**: LLM 프롬프트에 '제거 테스트'와 'IS-A 테스트'를 주입하여 오분류 0% 달성.
- [ ] **T2.17: [XWD Anchoring] 좌표성 시간 어휘 횡단 링크 강제 주입 [CRITICAL]**
    - [ ] 선행 조건: `T1.34` implementation architecture proposal 승인 후 착수.
    - [ ] **연결 쿼터제**: `Basics`로 이동한 모든 Anchor 단어에 대해 최소 3개 이상의 `Situations` 횡단 링크 주입.
    - [ ] **무결성**: 주입 후 `related_vocab` 필드와 검색 인덱스 간의 참조 무결성 전수 확인.

---

### Track 3. UI/UX Implementation (Development Agent)

- [ ] **T3.13: 프로덕션 빌드 최적화 및 배포 환경 안정화 [RELEASE-READY]**
- [ ] **T3.16: [V5 통합] 재분류 데이터 기반 UI 최종 최적화 [UI-DEV]**
    - [ ] **횡단 점프 최적화**: Anchor 단어 클릭 시 `Basics`에서 `Situations`로의 탭 전환 및 포커싱 로직의 부드러움 확보.
    - [ ] **60fps 보장**: 2.8만 개 연결망이 로드된 상태에서 마인드맵 인터랙션 성능 유지.

---

### Track 4. Quality Audit (Review Agent)

- [ ] **T4.7: [CURRENT] canonical apply conformity review after REV77**
    - [ ] `RELATION_DATA_POLICY`, `APP_DATA_REDEPLOY_SOP`, `09_app/public/data/README`, `Tasklist`, `Roadmap` 반영값이 `REV77` 의도와 맞는지 검토할 것.
    - [ ] 누락 반영, 과잉 반영, phase/gate 위반, runtime-safe 계약 위반 여부를 찾을 것.
    - [ ] 진단에서 끝나지 말고 즉시 수정해야 할 항목과 보류 가능한 항목을 분리 제시할 것.
- [ ] **T4.6: [Final QC] 재분류 데이터 전수 검수 및 릴리즈 승인 [GO-NO-GO]**
    - [ ] **실측 검증**: SDCP V5 규칙이 실제 8.5K 데이터에 100% 투영되었는지 샘플링 및 통계 검수.
    - [ ] **최종 판정**: 전수 재분류 데이터의 무결성 확인 후 배포용 `live/` 데이터 최종 승인.

---

## 3. 운영 원칙 (Mandatory)
1. **[SDCP V5 엄수]**: 모든 데이터 분류 및 연결은 `STRICT_DATA_CLASSIFICATION_PROTOCOL_V2.md`를 절대적 기준으로 삼는다.
2. **[실측주의]**: 모든 데이터 작업 후에는 반드시 통계 수치(Link Count, Distribution)를 포함하여 보고한다.
3. **[무결성]**: 모든 변경 사항은 [`PROJECT_DECISION_LOG`](./PROJECT_DECISION_LOG_V1.md)에 기록 후 전수 적용한다.

---

## 4. 🗄️ 완료된 태스크 보관소 (Completed Tasks)
<details>
<summary><b>과거 완료 내역 전체 펼쳐보기 (Click to expand)</b></summary>

### Track 1. Integrated Planning (Completed)
- [x] **T1.22**: **[SDCP V5]** 좌표/내용 이원화 및 이중 검증 기반 분류 정책 전면 재설계 (V1-REV-72)
- [x] **T1.1**: 3대 어휘 체계 공식 명칭 및 정의 확립 (V1-REV-1, 5)
- [x] **T1.2**: 8,139개 단어 수용 대규모 3단계 분류 체계(22개 루트) 확립 (V1-REV-2, 6, 7, 8)
- [x] **T1.3**: IA V4 3 Depth 카테고리 사전 구축 및 피드백 반영 (V1-REV-24, 26)
- [x] **T1.4**: 분류 프로토콜(SDCP V1/V2) 설계 및 철학 내재화 (V1-REV-11, 12, 17)
- [x] **T1.5**: 3대 축 차별화 기획 및 사용자 페르소나 시나리오 수립 (V1-REV-56)
- [x] **T1.18**: 참조 무결성을 고려한 에이전트 합의 기반 구조화 설계 (V1-REV-61)
- [x] **T1.20**: **[XWD 프레임워크 V1]** 20종 맥락적 훅 기반 연관 단어 발굴 전략 수립 (V1-REV-48)

### Track 2. Data Engineering (Completed)
- [x] **T2.15**: **[X-CLEAN Phase 2]** 루트 스크립트 격리 및 경로 무결성 보정 (V1-REV-65)
- [x] **T2.5**: **[마스터 풀 3 Depth 재분류]** 8,545건 단어 전수 대상 계층 강제화 (V1-REV-23)
- [x] **T2.9**: 예문 8,087건 및 연관어 196건 복구 및 최종 주입 완료 (V1-REV-44)
- [x] **T2.10**: **[XWD Mining]** 8.1K 단어 대상 전수 마이닝 및 2.8만 개 엣지 생성 (V1-REV-47)

### Track 3. UI/UX Implementation (Completed)
- [x] **T3.15**: **[글로벌 필터 확장]** 품사(POS) 기반 다중 선택 필터 UI 및 로직 최적화 (V1-REV-66)
- [x] **T3.13**: **[Release Hardening]** 8.1K 실전 연동 및 연관망 통합 빌드 완결 (V1-REV-70)
- [x] **T3.10**: **[글로벌 필터 및 횡단]** Level/Band 복합 필터링 및 횡단 점프 완결 (V1-REV-46)

### Track 4. Quality Audit (Completed)
- [x] **T4.5**: **[V5-ULTIMATE]** 분류 정책 전면 재기획 및 비판적 감사 완료 (V1-REV-73)
- [x] **T4.4**: **[마스터 오너십 실행]** 로드맵/태스크리스트 링크 교정 및 아카이빙 (V1-REV-64)
- [x] **T4.2**: 1,290개 샘플 확대 무결성 검증 및 최종 데이터 승인 (V1-REV-38)

</details>
