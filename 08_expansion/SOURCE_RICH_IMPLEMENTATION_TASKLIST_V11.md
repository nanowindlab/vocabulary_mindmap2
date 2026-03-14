# Source-Rich Implementation Tasklist V11 (ULTIMATE)

> Version: `V11-ULTIMATE`
> Date: `2026-03-12`
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

- [ ] **T1.17: README.md 상시 현행화 및 프로젝트 개요 관리 [RULE]**
    - [ ] **상시 업데이트**: README에 연결된 핵심 문서(가이드, 로드맵 등) 작업 시, README의 링크와 요약 정보도 반드시 동시 업데이트할 것.
- [ ] **T1.14: 신규 사용자를 위한 가이드 및 튜토리얼 설계 [RELEASE-READY]**
    - [ ] **온보딩 시나리오**: 앱 최초 진입 시 '3대 축'의 의미와 '마인드맵 단계별 확장' 방법을 안내하는 툴팁/오버레이 설계.
- [ ] **T1.15: UI 텍스트 및 브랜딩 전수 검수 (SDCP V5 기준) [RELEASE-READY]**
    - [ ] **선행 조건**: T2.16(전수 재분류) 및 T2.17(앵커링) 완료 후 착수.
    - [ ] **Label Audit**: 'Band 1' ➔ '최상위 필수' 등 모든 텍스트가 최신 브랜딩 정책(V8)과 SDCP V5 철학을 따르는지 점검.
- [ ] **T1.16: 인앱 인터랙티브 튜토리얼 및 도움말 UI 시스템 설계 [NEXT]**

---

### Track 2. Data Engineering (Data Agent)

- [ ] **T2.16: [SDCP V5] 8.5K 데이터셋 전수 재분류 실행 [CRITICAL]**
    - [ ] **좌표성 시간 이관**: 계절, 시간 어휘를 `Basics` 축으로 대대적 이동.
    - [ ] **이중 검증 적용**: LLM 프롬프트에 '제거 테스트'와 'IS-A 테스트'를 주입하여 오분류 0% 달성.
- [ ] **T2.17: [XWD Anchoring] 좌표성 시간 어휘 횡단 링크 강제 주입 [CRITICAL]**
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
