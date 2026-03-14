# Payload 136 Review Handoff V1

> Purpose: `APP_READY_CORE_PAYLOAD_V1.json` 감사 결과 중 manager/review 판단이 필요한 포인트만 압축 전달

## 1. Immediate Decision Set

이번 감사에서 기존 core payload `136`건은 다음과 같이 재판정되었다.

- `117`건: core 유지 가능
- `11`건: core 유지 가능하지만 root 이동 필요
- `19`건: core 확정 금지, candidate로 강등 권고

즉시 판단이 필요한 범주는 아래 두 묶음이다.

## 2. Root Shift Set (`11`)

이 묶음은 candidate가 아니라 `core 유지` 쪽이지만, 기존 root가 잘못 잡혀 있었다.

- `식생활 -> 보건과 의료`
  - `배탈_일반명사-1`
  - `소화_일반명사-1`
  - `소화액_일반명사-1`
  - `체증_일반명사-1`
  - `체하다_동사-1`
  - `치아_일반명사-1`
  - `침_일반명사-1`
  - `배_일반명사-1`
- `식생활 -> 문화와 사회`
  - `제사상_일반명사-1`
- `식생활 -> 주거와 일상`
  - `집안일_일반명사-1`
- `사람과 관계 -> 주거와 일상`
  - `거실_일반명사-1`

우선 검토 포인트:
- `식생활`이 신체 기관/증상까지 흡수하던 기존 경향을 계속 허용할지
- `제사상`을 음식 맥락보다 의례 맥락으로 잠글지
- `거실`을 사람 관계가 아니라 생활 공간으로 재고정할지

## 3. Candidate Demotion Set (`19`)

### 3.1. Taste / Sense Boundary

- `밥맛_일반명사-1`
- `식욕_일반명사-1`
- `싱겁다_형용사-1`
- `고프다_형용사-1`
- `맛_일반명사-1`
- `맛없다_형용사-1`
- `맛있다_형용사-1`
- `부르다_동사-3`
- `식감_일반명사-1`
- `위_일반명사-1`
- `입맛_일반명사-1`
- `풍미_일반명사-1`

핵심 질문:
- 이 묶음을 `식생활`에 그대로 둘 것인지
- 일부를 `감각과 묘사`, `내면과 감정`, `보건과 의료` 브리지로 돌릴 것인지

### 3.2. Social / Ceremony Boundary

- `대접_일반명사-1`
- `연회_일반명사-1`
- `제사_일반명사-1`
- `파티_일반명사-1`

핵심 질문:
- 음식이 등장하더라도 본질이 `사람과 관계`, `문화와 사회`, `여가와 취미`에 더 가까운지

### 3.3. Institution / Space Boundary

- `가족부_일반명사-1`
- `차림_일반명사-1`
- `카페_일반명사-1`

핵심 질문:
- `가족부`를 `사람과 관계`가 아닌 `공공 서비스`로 보내야 하는지
- `차림`의 다의성을 payload에서 어떻게 처리할지
- `카페`를 `식생활`로 잠글지, 상업 공간 경계를 열어 둘지

## 4. Recommended Review Order

1. `Root Shift Set 11`을 먼저 잠근다.
2. `Taste / Sense Boundary 12`를 두 번째로 본다.
3. `Social / Ceremony Boundary 4`와 `Institution / Space Boundary 3`을 마지막에 본다.

## 5. Source

- `08_expansion/PAYLOAD_136_AUDIT_REPORT_V1.md`
- `08_expansion/PAYLOAD_136_AUDIT_ACTIONS_V1.json`
- `08_expansion/batch_runs/BATCH_001_buckets.json`
- `08_expansion/batch_runs/BATCH_002_buckets.json`
