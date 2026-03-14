# 통합 IA 및 차세대 시각화 UX 시나리오 명세서 (V7)

> **기획 의도**: 8,092건의 대규모 어휘 데이터를 학습자가 스트레스 없이 탐색할 수 있도록, 물리 엔진 기반의 마인드맵 배치 알고리즘과 실시간 지능형 필터링 시스템을 설계합니다.

---

## 1. 스마트 Radial 배치 알고리즘 (Smart Radial Engine)

기존의 고정형 방사형 배치를 폐기하고, 데이터의 밀도와 노드 간의 거리를 동적으로 계산하는 엔진으로 업그레이드합니다.

### 1.1. 충돌 방지 및 거리 자동 산출 (Collision Avoidance)
- **가변 반지름 (Dynamic Radius)**: 특정 카테고리의 단어(Term) 수가 많을 경우, 해당 브랜치의 반지름을 자동으로 확장하여 노드 간의 겹침을 방지함.
  - 공식 예시: $R_{new} = R_{base} + (Count_{terms} \times Node\_Padding)$
- **척력 기반 배치 (Force-Directed Radial)**: 각 노드 사이에 가상의 척력(Repulsion)을 부여하여, 밀집 지역에서 노드들이 스스로 최적의 각도를 찾아 퍼지도록 설계함.

### 1.2. 점진적 렌더링 (Progressive Rendering)
- **Viewport-Aware Loading**: 현재 사용자의 화면(Viewport)에 보이는 영역의 노드만 우선 렌더링하고, 줌인/줌아웃 및 패닝 동작에 따라 배후 데이터를 실시간으로 보정함.
- **Level of Detail (LOD)**: 줌아웃 상태에서는 '단어(Term)' 노드를 숨기고 '카테고리' 노드만 노출하며, 일정 비율 이상 줌인했을 때만 단어 노드와 상세 정보(영어 뜻 등)를 노출함.

---

## 2. 지능형 필터링 시스템 (Intelligent Filtering)

학습자의 개인화된 학습을 위해 Level(단계)과 Band(빈도)를 활용한 실시간 필터링을 제공합니다.

### 2.1. 퀵 필터 인터랙션 (Quick Filter UI)
- **학습 단계 필터 (Level Switcher)**: [Beginner / Intermediate / Advanced] 버튼을 통해 마인드맵 전체에서 해당 레벨 단어만 하이라이트하거나 나머지를 반투명(Dim) 처리함.
- **중요도 슬라이더 (Band Slider)**: Band 1~5를 조절하여 사용자가 원하는 빈도수의 단어만 선별적으로 노출함. (예: "오늘의 핵심 단어(Band 1~2)만 보기")

### 2.2. 상태 동기화 및 탭 전환 로직
- **Global Filter State**: 사용자가 설정한 필터 값은 3대 축([상황], [마음], [구조]) 전환 시에도 유지되어 일관된 학습 경험을 제공함.
- **Empty State 대응**: 필터링 결과 현재 카테고리에 단어가 하나도 없을 경우, "필터를 조정해 보세요"라는 안내와 함께 상위 카테고리로 자동 안내하는 UI 제공.

---

## 3. 개발 에이전트 구현 가이드 (Technical Blueprint)

### 3.1. 기술 스택 추천 및 연동
- **D3.js (Force Layout)**: 노드 간의 물리적 관계 계산 및 애니메이션 처리에 최적.
- **Canvas API**: 8K 이상의 노드를 SVG보다 훨씬 빠른 성능으로 렌더링 가능 (현재 MindmapCanvas의 아키텍처 유지 및 강화).

### 3.2. 상태 관리 (Zustand/Redux)
- `filterCriteria: { levels: string[], bands: number[] }` 객체를 전역 상태로 관리.
- 마인드맵 컴포넌트 내부에서 `memo`화 된 필터링 로직을 통해 렌더링 오버헤드 최소화.

---

## 4. 용어 및 브랜딩 정제 (Final Branding)

- **[시각화 모드] ➔ 탐색 지도 (Explorer Map)**
- **[지능형 필터링] ➔ 맞춤 레벨 필터 (Smart Level Filter)**

---
**Verdict**: 본 명세서는 대규모 데이터의 가시성 문제를 물리 엔진과 지능형 필터링으로 해결하는 UI/UX 완성판입니다.
