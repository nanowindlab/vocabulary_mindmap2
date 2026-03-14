# Payload 136 Audit Report V1

> Date: `2026-03-10`
> Scope: `09_app/public/data/APP_READY_CORE_PAYLOAD_V1.json`에 이미 들어가 있던 `136`개 항목 전수 재감사
> Method: `gemini-2.5-flash` + 로컬 검증 파이프라인(`gemini_batch_refiner.py`)

## 1. Audit Summary

- 감사 대상 `136`건은 `SYSTEM_CANDIDATES_V1.json`, `CATEGORY_CANDIDATES_V1.json`, `EXCLUDED_WORDS_V1.json`에는 없지만, 모두 `APP_READY_CORE_PAYLOAD_V1.json`에는 이미 들어가 있던 집합이다.
- 따라서 이번 감사의 목적은 `누락 복구`가 아니라 `기존 core payload의 SDCP V1 / IA V4 재판정`이다.
- 배치 구성:
  - `BATCH_001`: `100`건
  - `BATCH_002`: `36`건
- 누적 결과:
  - `core 117`
  - `candidate 19`
  - `exclusion 0`
- 검증 상태:
  - `BATCH_001_report.json`: `validation_issues []`
  - `BATCH_002_report.json`: `validation_issues []`

## 2. Key Verdict

- 기존 `APP_READY_CORE_PAYLOAD_V1.json`의 `136`건 중 `117`건은 core 유지 가능하다.
- 다만 그중 `11`건은 기존 root가 부정확해 root 이동이 필요하다.
- 기존 core였던 `19`건은 100% 확신이 부족하므로 즉시 core 유지하지 말고 `candidate`로 낮춰 검토하는 편이 안전하다.
- 이번 감사 집합에서는 `exclusion`이 `0`건이었다.
  - 해석: 이 집합이 원래 기존 core payload에서 추출된 집합이기 때문에, SDCP Filter 대상이 거의 섞여 있지 않았다는 뜻이다.
  - 의미: 전체 프로젝트 차원에서 exclusion이 없다는 뜻은 아니다.

## 3. Distribution

- 기존 root 분포:
  - `식생활 121`
  - `보건과 의료 9`
  - `사람과 관계 6`
- 재감사 후 core root 분포:
  - `식생활 93`
  - `보건과 의료 17`
  - `사람과 관계 4`
  - `주거와 일상 2`
  - `문화와 사회 1`
- candidate 제안 root 분포:
  - `식생활 13`
  - `감각과 묘사 2`
  - `내면과 감정 1`
  - `공공 서비스 1`
  - `보건과 의료 1`
  - `주거와 일상 1`

## 4. Confirmed Root Shifts

아래 `11`건은 core로 유지 가능하지만 기존 payload root를 바꾸는 편이 타당하다.

| meaning_id | 기존 root | 재감사 root | 근거 |
| :--- | :--- | :--- | :--- |
| `배탈_일반명사-1` | `식생활` | `보건과 의료` | 음식 관련이지만 본질은 소화기 증상 |
| `소화_일반명사-1` | `식생활` | `보건과 의료` | 음식 섭취 맥락보다 신체 기능이 중심 |
| `소화액_일반명사-1` | `식생활` | `보건과 의료` | 신체 구성 요소 |
| `제사상_일반명사-1` | `식생활` | `문화와 사회` | 음식 자체보다 의례 문맥이 중심 |
| `집안일_일반명사-1` | `식생활` | `주거와 일상` | 음식 준비를 포함하지만 가사 활동이 상위 개념 |
| `체증_일반명사-1` | `식생활` | `보건과 의료` | 소화기 증상 |
| `체하다_동사-1` | `식생활` | `보건과 의료` | 소화 불량 상태 |
| `치아_일반명사-1` | `식생활` | `보건과 의료` | 신체 부위 |
| `침_일반명사-1` | `식생활` | `보건과 의료` | 신체 구성 요소 |
| `거실_일반명사-1` | `사람과 관계` | `주거와 일상` | 사람 관계보다 생활 공간이 중심 |
| `배_일반명사-1` | `식생활` | `보건과 의료` | 소화 기관 의미가 채택됨 |

## 5. Candidate Demotions

아래 `19`건은 기존 core payload에 있었지만, 재감사 기준으로는 boundary 충돌이 남아 `candidate`로 내리는 편이 안전하다.

### 5.1. Taste / Sense Boundary

- `밥맛_일반명사-1`
- `싱겁다_형용사-1`
- `고프다_형용사-1`
- `맛_일반명사-1`
- `맛없다_형용사-1`
- `맛있다_형용사-1`
- `부르다_동사-3`
- `식감_일반명사-1`
- `입맛_일반명사-1`
- `풍미_일반명사-1`

해석:
- 이 집단은 대부분 기존 payload에서 `식생활`로 바로 들어가 있었지만, IA V4 기준으로는 `감각과 묘사`, `내면과 감정`, `보건과 의료`와 경계가 겹친다.
- `맛/감각/신체 경계가 겹치면 candidate 우선`이라는 이번 감사 규칙이 핵심적으로 적용된 영역이다.

### 5.2. Social / Ceremony Boundary

- `대접_일반명사-1`
- `연회_일반명사-1`
- `제사_일반명사-1`
- `파티_일반명사-1`

해석:
- 음식이 등장하지만 본질은 `사람과 관계`, `문화와 사회`, `여가와 취미`와 충돌한다.
- 기존처럼 무조건 `식생활`에 고정하는 것은 과감한 단순화였고, 지금은 candidate로 보류하는 쪽이 더 안전하다.

### 5.3. Institution / Space Boundary

- `가족부_일반명사-1`
- `차림_일반명사-1`
- `카페_일반명사-1`
- `위_일반명사-1`
- `식욕_일반명사-1`

해석:
- `가족부`: `사람과 관계`보다 `공공 서비스` 또는 `직장과 업무`에 가깝다.
- `차림`: 옷차림과 음식 차림이 공존한다.
- `카페`: `식생활`과 `쇼핑/상업 공간` 경계가 있다.
- `위`: 공간 지시어 의미와 소화 기관 의미가 충돌한다.
- `식욕`: 식생활이 아니라 내면 상태로도 읽힌다.

## 6. Structural Insights

- 기존 payload는 `식생활` 흡인력이 지나치게 강했다.
- 특히 다음 세 부류가 `식생활`로 과도하게 빨려 들어가 있었다.
  - 소화기 증상 / 신체 기관
  - 감각·맛·포만감 표현
  - 의례·사교·상업 공간
- 데이터 관점에서 필요한 보강은 다음과 같다.
  - `식생활` 내부에서 `음식 종류 / 식기 / 조리 도구 / 조리 행위 / 식당`은 그대로 유지
  - `맛·풍미·식감·밥맛·입맛` 계열은 `감각과 묘사` 브리지 검토
  - `배탈·체증·체하다·소화·소화액·치아·침·배` 계열은 `보건과 의료`로 이동 잠금 검토
  - `제사상`은 `문화와 사회` 쪽으로 잠그는 것이 더 일관적

## 7. Recommended Next Action

1. `APP_READY_CORE_PAYLOAD_V1.json`의 `117 core` 유지 / `19 candidate` 분리 반영 여부를 manager decision으로 잠근다.
2. `11`개 root shift는 review agent 샘플 검수 없이도 우선순위 높게 확인할 가치가 있다.
3. `candidate 19`는 단어군 단위로 review handoff를 구성한다.
4. 이후 broad tree 확장 전에 `식생활`의 경계 규칙을 이번 감사 결과 기준으로 명문화한다.

## 8. Source Files

- `08_expansion/batch_runs/BATCH_001_buckets.json`
- `08_expansion/batch_runs/BATCH_001_report.json`
- `08_expansion/batch_runs/BATCH_002_buckets.json`
- `08_expansion/batch_runs/BATCH_002_report.json`
- `09_app/public/data/APP_READY_CORE_PAYLOAD_V1.json`
