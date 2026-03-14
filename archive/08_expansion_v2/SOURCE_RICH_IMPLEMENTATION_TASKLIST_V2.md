# Source-Rich Implementation Tasklist V2

> Version: `V2`
> Date: `2026-03-09`
> Owner: `Codex`
> Status: `active`
> Role: `authoritative tasklist + todo`

## 1. 목적

이 문서는 현재 `schema pass + UI shell` 상태를 넘어,
실제 source 자료가 가진 정보를 제품 경험에 모두 연결하기 위한 구현 tasklist다.

운영 원칙:

- 이 문서가 현재 마일스톤의 `단일 authoritative tasklist/todo`다.
- 별도의 임시 todo를 다른 문서에 중복 관리하지 않는다.
- 새로운 요구가 생기면 이 문서에 직접 task를 추가한다.

## 2. 필수 범위

이번 마일스톤에서 반드시 반영해야 하는 요소는 아래다.

1. 사용자가 지적한 현재 정보 누락을 최소 기준으로 모두 해소
2. 사전 source와 corpus source의 정보를 가능한 한 전부 projection에 반영
3. source 정보를 실제 사용자 시나리오에 맞게 배치
4. `expression core`를 별도 core로 승격
5. `scene core`와 `expression core` 모두 실제 mindmap으로 구현
6. 플립카드 학습 흐름 구현
7. `PRODUCT_USER_SCENARIOS_V1.md`와 결합해 제품 개선안 반영
8. 이번 범위에서는 `visual_material`은 제외하고 나머지 source 정보 연결을 우선
9. corpus 9개 table은 실제 추출본을 `05_source` 하위 적절한 snapshot 폴더에 보관하고 projection 입력으로 사용
10. 단어 뜻(`def_ko` / `definition_ko`)은 core / meta / expression 어디서든 실제로 연결돼 보여야 한다
11. 단어별 `related_vocab`가 있으면 비어 보이지 않게 실제로 활용돼야 한다
12. `romanization`이 없는 단어는 source에서 보충하거나 missing policy를 가져야 한다
13. `romanization` 표기 규칙과 표기법 검증이 필요하다
14. 출현 예문의 출처 표시는 정책화하되, `세종한국어` 표기는 사용하지 않는다
15. 빈도 / 출처 / 등장 회차는 나중에 숨길 수 있도록 설계하고, 대신 `frequency band 1~5`를 설계한다
16. `https://nuri.iksi.or.kr/` 계열 링크는 제품에서 제거한다
17. learner examples(합쇼체 / 해요체 / 해라체 등 6개 예문)를 가능한 한 적극 활용한다
18. 모든 단어는 장기적으로 필요한 필드를 모두 가진 schema-complete 상태를 목표로 한다
19. `문화와 명절` 등 일부 그룹의 분류 누락 문제를 해결해야 한다
20. scene core / expression core / meta learning 모두 리스트가 아니라 실제 탐색 구조를 가져야 한다
21. 플립카드는 별도 검토 항목이 아니라 구현 task로 관리한다
22. Codex가 `mindmap UI/spec draft`를 먼저 만들고, `Review Gemini` 검토, `Antigravity` 피드백, Codex 최종 정리 순서로 잠근다
23. `Gemini CLI`는 payload 보강 트랙의 선행 담당임을 task sequence에 명시한다
24. scene core의 잘못된 분류 / 중복 분기 / meta leakage는 `broad tree UI 구현 전`에 교정되어야 한다
25. **영어 정의(`def_en`)는 상시 노출하는 것으로 정책 확정 (사용자 피드백 반영)**

... (중간 생략) ...

### Track D. Implementation

- [ ] D1. source-rich core projection 생성
- [ ] D2. source-rich expression projection 생성
- [ ] D3. source-rich meta projection 생성
- [ ] D4. Antigravity가 core/expression mindmap 구현
- [ ] D5. Antigravity가 meta detail / expression detail / flipcard 구현
- [ ] D6. bridge navigation / provenance / grade 표시 구현
- [ ] D7. Antigravity가 TOPIK 빈도 탐색 전용 리스트 / 구간 UI 구현
- [ ] D8. Antigravity가 예문 문체 비교 탭 / 필터 UI 구현
- [ ] D9. Antigravity가 플립카드 학습 상태 저장 / 복원 로직 구현
- [ ] D10. Antigravity가 deck context 생성/전환 UI 구현
- [ ] D11. Antigravity가 corpus 예문 난이도 필터와 source 우선순위 UI 구현
- [ ] D12. Antigravity가 learner-facing 영어 보조 라벨 / 설명 UI 구현
- [ ] D13. Antigravity가 전역 검색 바 / 결과 패널 / 결과 진입 UX 구현
- [ ] D14. Antigravity가 동음이의어 구분 UI와 검색 결과 disambiguation 구현
- [ ] D15. Antigravity가 related vocab 기반 추천 탐색 UI 구현
- [ ] D16. Antigravity가 corpus source example / learner example 병렬 노출 UI 구현
- [ ] D17. builder가 실제 chunk sharding과 provenance `top_sources`를 생성하도록 구현
- [ ] D18. core / meta / expression 공통 detail panel에 한국어 뜻 연결
- [ ] D19. `romanization` 누락 단어 보충 데이터 반영
- [ ] D20. `frequency band 1~5` UI 구현
- [ ] D21. 출처 표시 토글 및 `세종한국어` 문구 제거 구현 (2026-03-09)
- [ ] D22. `nuri.iksi.or.kr` 링크 제거 구현 (2026-03-09)
- [ ] D23. `문화와 명절` 등 분류 누락 그룹 보정 구현
- [ ] D24. scene core 실제 mindmap 렌더링 구현
- [ ] D25. expression core 실제 mindmap 렌더링 구현
- [ ] D26. meta learning map 구현
- [ ] D27. 플립카드 UI 구현
- [ ] D28. scene core 재분류 교정 결과를 runtime payload / sidebar tree / mindmap 입력에 반영
- [ ] D29. learner examples 6개 세트 누락 단어 보충 및 runtime payload 반영
- [ ] **D30. 영어 정의(`def_en`)를 detail/search/meta/expression UI에 상시 노출로 확정 및 토글 제거 (2026-03-09)**
- [ ] D31. flipcard hydration용 runtime manifest 보강: `chunk_id` 또는 대표 예문을 core/meta/expression manifest에 주입
- [ ] D32. 현재 단계 플립카드 조작을 `이전/다음` 중심으로 전환하고, `알아요/몰라요`는 다음 프로젝트 단계로 분리 (2026-03-09)
- [ ] D33. 현재 단계 플립카드 덱에서 scene core / expression core의 정제된 complete-data 단어만 사용하도록 구현 (2026-03-09)
- [ ] D34. scene core / expression core 화면에 `리스트 보기 / 플립카드 보기` mode 선택 UI 구현
- [ ] D35. detail panel의 중복 same-sense chip 제거 및 current surface/context 명확화 구현 (2026-03-09)
- [ ] D36. `related_vocab` target normalization: 클릭 가능한 연관 어휘는 runtime record/search entry로 해석 가능해야 하며, 불가 시 fallback policy를 명시
- [ ] D37. `related_vocab` reciprocity / center-profile display policy: 연관어휘 상호성 규칙과 center-profile 단어의 중복 노출 금지 규칙을 runtime에 반영
- [ ] D38. `cross_links` source-rich population: core / expression / meta runtime payload에 실제 탐색 가능한 link set을 주입 (2026-03-09)
- [ ] D39. detail-field runtime integrity hardening: 예문 / romanization / provenance가 실제 detail panel에서 안정적으로 유지되는지 검증하고 보정 (2026-03-09)
- [ ] **D41. 상단 레이아웃 가려짐 수정: Top-nav 높이 70px 상향 및 z-index 적용으로 가시성 확보 (2026-03-09)**
- [ ] D40. (TBD: Remaining high-priority implementation items)

... (이하 생략) ...
