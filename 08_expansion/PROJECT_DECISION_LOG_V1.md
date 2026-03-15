# 프로젝트 결정 로그 및 컨텍스트 가이드 (Project Decision Log)

> 이 문서는 프로젝트의 핵심 아키텍처 변경, 용어 체계, 기획적 결정을 기록하는 **단일 진실의 원천(SSOT)**입니다. 모든 에이전트는 작업 착수 전 이 로그를 필독하여 현재의 프로젝트 맥락을 동기화해야 합니다.

---

## 1. 핵심 용어 체계 변경 (Terminology)
*결정 일자: 2026-03-11*
사용자의 인지적 직관성을 높이기 위해 최상위 3대 축의 명칭을 다음과 같이 변경함.

| 구 용어 (Legacy) | 신 용어 (New Standard) | 정의 및 범위 |
| :--- | :--- | :--- |
| **장면 코어** | **상황과 장소 (Situations & Places)** | 특정 장소와 생활 장면에 종속된 물리적 어휘 |
| **표현 코어** | **마음과 표현 (Heart & Expression)** | 감정, 성격, 감각 및 주관적 평가 어휘 |
| **메타 학습** | **구조와 기초 (Structure & Basics)** | 숫자, 시간, 논리, 접속사 등 문법적 뼈대 어휘 |

---

## 2. 아키텍처 리팩토링 (Architecture)
*결정 일자: 2026-03-11*
데이터 규모 확장(8,500건+)에 따른 성능 저하와 렌더링 부하를 해결하기 위한 결정 사항.

- **3 Depth 구조화 강제**: [System > Root] 2단계 구조에서 [System > Root > Category] 3단계 구조로 세분화. (사이드바 트리 가독성 확보)
- **물리적 파일 분할**: 단일 거대 JSON(`CORE_TREE`)을 폐기하고, 3대 축별로 독립된 3개의 파일로 분리 관리함.
- **지연 로딩(Lazy Loading)**: 프론트엔드는 탭 전환 시에만 해당 축의 파일을 로드하여 초기 구동 속도 최적화.

---

## 3. 데이터 필드 표준화 (Data Schema Standardization)
*결정 일자: 2026-03-11*
소스 데이터에 따라 다르게 표현된 동일 정보를 아래 표준 명칭으로 통일함.

| 정보 유형 | 구 명칭 (Legacy) | 표준 명칭 (Standard) | 비고 |
| :--- | :--- | :--- | :--- |
| **전체 빈도** | `total_frequency` | **`frequency`** | 수식 연산 및 UI 바인딩 키 |
| **회차 수** | `round_count` | **`round_count`** | 유지 |
| **문장 수** | `sentence_count` | **`sentence_count`** | 유지 |

---

## 4. 실무 참조 가이드 (Implementation Reference)
에이전트가 현황 분석을 위해 반드시 확인해야 할 위치.

- **프론트엔드 로직**: `09_app/src/App.jsx` (데이터 파싱 및 탭 분배)
- **데이터 저장소**: `09_app/public/data/live/` (실제 앱 runtime canonical JSON)
- **분류 기준 사전**: `08_expansion/IA_V4_3DEPTH_CATEGORY_DICTIONARY_V1.md`
- **전체 작업 현황**: `08_expansion/SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`

---

## 5. 주요 결정 이력 (Change Log)
- **V1-REV-21**: 원본 사전 누락 단어 추가 발굴 및 8,545건 마스터 풀 확보.
- **V1-REV-24**: 3 Depth(100여 개 세부 카테고리) 설계 및 사전 구축.
- **V1-REV-28**: 통합 내비게이션 및 콘텐츠 시나리오 고도화 착수.
- **V1-REV-61**: 구조 정리 리스크 감사 및 오너십 매핑 완료.

---

## 6. PM-Centric State Management
*결정 일자: 2026-03-15*

- active state surface는 `ORCHESTRATION_DASHBOARD.md`, `NEXT_MAIN_PM_HANDOFF_V1.md`, `PROJECT_DECISION_LOG_V1.md`, `SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md`, `08_expansion/pm_reports/*.md`로 고정한다.
- workboard/workboard_archive는 history-only다.
- intermediate evidence와 milestone closure는 `08_expansion/pm_reports/`가 소유한다.

## 7. Thin Runtime Projection Hardening
*결정 일자: 2026-03-15*

- `scripts/mining/run_rev47_xwd_mining.py --publish-only`는 relation overlay only다.
- `publish-only`는 new runtime id admission에 사용할 수 없다.
- `publish-only`는 live `system/root/category` reclassification에 사용할 수 없다.
- split/search duplicate 또는 split/search mismatch 위에서는 publish를 시작하지 않는다.

## 8. Batch-11 Reclassification
*결정 일자: 2026-03-15*

- `Calendar Label Batch-11`은 더 이상 `Type A + Green`으로 취급하지 않는다.
- 현재 분류는 `Yellow / Runtime Reclassification`이다.
- `요일_일반명사-1`는 change surface에 포함되므로 no-drift sentinel에서 제외한다.

## 9. Coverage Restart Gate
*결정 일자: 2026-03-15*

- coverage expansion은 `green autopilot 확대`가 아니라 `green relation-overlay batch만 제한적으로 재개`로 다시 연다.
- green 자격은 duplicate-free runtime, count-consistent surfaces, clean control set, existing live id-only overlay를 동시에 만족해야 한다.

## 10. Restart Model Accepted
*결정 일자: 2026-03-15*

- 사용자는 restart model을 승인했다.
- 승인 이후 `Relative Year Markers Batch-6`, `Temporal Reference Nouns Batch-8`가 연속으로 runtime-safe하게 집행되었다.
- 다음 승인 게이트는 개별 batch 승인보다 rollout scale decision이다.
