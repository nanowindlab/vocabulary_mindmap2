# Source-Rich Implementation Tasklist V3 (RESTART)

> Version: `V3-RESTART-UPDATED-V5`
> Date: `2026-03-10`
> Owner: `Gemini Orchestrator (Manager)`
> Status: `ACTIVE - Data Mapping Phase`
> Role: `Single Authoritative Tasklist / Todo`

## 1. 3대 핵심 어휘 체계 정의 (Core Pillars) - [LOCKED]
*   **[상황과 장소] (Situations & Places)**: 물리적 공간과 일상 장면 중심.
*   **[마음과 표현] (Heart & Expression)**: 내면의 감정, 상태 서술, 주관적 평가 중심.
*   **[구조와 기초] (Structure & Basics)**: 언어의 추상적 골격(숫자, 시간, 문법 등) 중심.

## 2. 핵심 마일스톤
- **IA Restructuring (기획 1):** 🏆 완료 (V4 Final 승인됨).
- **Data Re-allocation & Schema Connection (데이터):** [진행 중] V4 시스템에 따른 전수 분류 및 모든 스키마(뜻, 예문, 빈도 등) 완벽 통합.
- **Implementation (개발):** 탭 명칭 교체 및 레이아웃 통합.

## 3. 상세 태스크 (Track별)

### Track 1. Structural Planning (Planning Agent)
- [✅] T1.1: 3대 어휘 체계 공식 명칭 및 정의 확립
- [✅] T1.2: 8,139개 단어 수용 가능한 대규모 3단계 분류 체계(22개 루트) 확립
- [✅] T1.3: 계층 이동 및 Cross-link 횡단 탐색 시나리오 기획
- [✅] T1.4: 뷰 모드(마인드맵/리스트/단어카드) 전환 시나리오 확정

### Track 2. Data Connection & Expansion (Data Agent)
- [ ] T2.1: **[전수 분류 및 매핑]** IA V4 결정 알고리즘에 따른 8,139개 단어 전수 분류 (Self-Refinement 루프 적용).
- [ ] T2.2: **[분류 불능 단어 처리]** 모호한 단어를 별도 큐로 추출하고 반복적 보정을 통해 분류 성공률 95% 이상 달성.
- [ ] T2.3: **[스키마 전면 통합]** 모든 단어에 뜻, 다양한 예문(6종), 연관 단어, 로마자 등 100% 스키마 주입 및 JSON 생성.
- [ ] T2.4: **[Cross-link 고도화]** 단어 간 상호 참조 데이터 및 탭 전환 라우팅 데이터 최종 검증.
- [ ] T2.5: **[마스터 풀 3 Depth 재분류]** 파편화된 모든 중간 산출물(누락 단어 포함 8,500여 건)을 단일 풀로 병합 후, IA V4 3단계(Category)를 포함하는 고도화된 프롬프트로 100% 전수 재분류(Triage) 실행.
- [ ] T2.6: **[3대 축 파일 분리 생성]** 전수 분류된 결과를 단일 트리가 아닌 `상황과 장소`, `마음과 표현`, `구조와 기초` 3개의 개별 JSON 트리 파일로 분할하여 출력 및 저장.

### Track 3. UI/UX Refactoring (Development Agent)
- [ ] T3.1: **[3대 축 탭 라우팅 분리]** 단일 거대 JSON 대신 탭별로 매칭된 3개의 전용 JSON 파일을 동적/지연 로드(Lazy Load)하도록 프론트엔드 아키텍처 개편.
- [ ] T3.2: **[3 Depth 트리 렌더링 복원]** 데이터에서 새롭게 도출된 3단계 Category 속성을 트리의 중간 폴더로 사용하여 사이드바 UI의 렌더링 과부하 해소 및 가독성 확보.
