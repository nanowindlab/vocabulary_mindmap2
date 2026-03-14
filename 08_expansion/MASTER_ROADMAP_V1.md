# 프로젝트 마스터 로드맵 V1 (RESTART-V1)

> **프로젝트 거버넌스**: 본 프로젝트는 [오케스트레이션 운영 가이드](../.gemini-orchestration/OPERATING_GUIDE_V1.md)를 준수합니다. 모든 에이전트는 작업 전 운영 가이드를 숙지하십시오.

> Version: `V1-MASTER`
> Date: `2026-03-11`
> Owner: `Gemini Orchestrator (Manager)`
> Status: `ACTIVE - Phase 3 In-Progress`
> Base: `IA V4` / [Tasklist V10 HD](./SOURCE_RICH_IMPLEMENTATION_TASKLIST_V10.md)

## 1. 프로젝트 정의 및 비전
본 프로젝트는 8,545건의 방대한 한국어 어휘 데이터를 **3대 핵심 체계(상황/마음/구조)**로 구조화하고, 이를 **3 Depth 마인드맵** 및 **플래시카드** 환경으로 시각화하여 학습자에게 직관적인 어휘 확장 경험을 제공하는 것을 목표로 한다.

---

## 2. 핵심 마일스톤 (Phases)

### Phase 1. IA V4 Architecture Design [COMPLETED]
- 3대 핵심 축 및 22개 루트 정의 확립.
- 100여 개 세부 카테고리(3 Depth) 사전 구축 및 최종 승인.
- 실측 통계 기반 등급(Band/Level) 산출 알고리즘 수립.

### Phase 2. Data Master Pool Consolidation [COMPLETED]
- 파편화된 중간 산출물 및 누락 단어(8,545건) 통합.
- 스키마 명칭 표준화 (`total_frequency` ➔ `frequency` 등).

### Phase 3. Smart Triage & Enrichment [IN-PROGRESS]
- **3 Depth 전수 재분류**: [System > Root > Category] 계층을 강제 적용하여 사이드바와 마인드맵의 렌더링 부하를 줄이고 데이터 구조를 체계화한다.
- **데이터 내실화**: 6종 문체별 예문 매핑 및 연관 단어(Cross-link) 구축을 통해 단순 단어 나열이 아닌 유기적 학습 콘텐츠를 완성한다.
- **물리적 분할**: 3대 축별 독립 JSON 파일로 분리하여 탭 전환 시 필요한 데이터만 로드하는 지연 로딩(Lazy Load)의 기반을 마련한다.

### Phase 4. Unified UI/UX Implementation [NEXT]
- **탭 라우팅**: 축별 파일 동적 전환 시스템을 구축하여 사용자가 탭을 바꿀 때마다 해당 테마의 마인드맵이 실시간으로 교체되도록 구현한다.
- **엔진 고도화**: 대량의 노드(8.5K) 노출 시에도 쾌적한 조작감을 위해 충돌 방지 및 단계별 노출 로직이 적용된 고성능 마인드맵 엔진을 탑재한다.
- **UI 리팩토링**: 한국어 단어와 영어 대응어를 병렬로 배치하여 시독성을 높이고, 플래시카드 중심의 브랜딩을 강화한다.

### Phase 5. Quality Audit & Performance Tuning
- 8.5K 데이터 대상 렌더링 성능 최적화 (노드 150개 제한 등).
- 데이터 무결성 전수 검수 및 Null-Safety 방어 로직 검증.

### Phase 6. Integrated Release & Feedback
- 프로덕션 빌드 및 배포.
- 실제 학습자 피드백 수집 및 2차 고도화 계획 수립.

---

## 3. 미래 확장 과제 (Future Scope) - [Manager Approved]
본 마일스톤 완료 후 진행될 고도화 핵심 과제입니다.

1.  **다국어 확장 데이터 레이어 (Multi-lang)**: `translations: { en, fr, jp... }` 스키마 전환.
2.  **모바일 최적화 탐색 (Mobile UX)**: 모바일 전용 리스트 및 카드 인터랙션 설계.
3.  **학습 상태 유지 (Learning Persistence)**: 로컬 스토리지 기반 즐겨찾기 및 진척도 저장.

---

## 4. 참조 문서 (SSOT)
- **최종 태스크리스트**: [`08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V10.md`](./SOURCE_RICH_IMPLEMENTATION_TASKLIST_V10.md)
- **결정 로그**: `08_expansion/PROJECT_DECISION_LOG_V1.md`
- **UX 명세서**: `08_expansion/IA_AND_UX_SCENARIO_SPEC_V8.md`
