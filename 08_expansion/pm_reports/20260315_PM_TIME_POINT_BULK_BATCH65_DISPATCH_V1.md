# PM Time Point Bulk Batch-65 Dispatch V1

> Date: `2026-03-15 21:00:16 +0900`
> Owner: `Codex / Main PM`
> Status: `READY FOR EXECUTION`
> Purpose: current live에서 이미 안정적인 `시간과 흐름 > 시점` 명사 65개를 internal canonical로 bulk 흡수한다.

## 1. Batch Identity

- batch name: `Time Point Bulk Batch-65`
- batch type: `Green / Relation Overlay Mirror`
- runtime owner: `current live hierarchy and current live related_vocab`

## 2. Selection Rule

아래 조건을 모두 만족하는 live row만 선택했다.

- `system = 구조와 기초`
- `root = 시간과 흐름`
- `category = 시점`
- `pos = 일반명사`
- current graph node에 아직 없음
- control set 아님
- current live `cross_links = 0`
- current live `related_vocab > 0`

## 3. Why This Batch Is Safe

- 이번 batch는 새 relation semantics를 발명하지 않는다.
- current live에서 이미 노출 중인 `related_vocab`를 internal canonical로 그대로 미러링한다.
- 즉 rollout 속도를 높이면서도 runtime output을 재해석하지 않는 batch다.

## 4. Scope Size

- selected ids: `65`

대표 예시:

- `공휴일_일반명사-1`
- `기한_일반명사-1`
- `나중_일반명사-1`
- `날_일반명사-1`
- `다음_일반명사-1`
- `시점_일반명사-1`
- `이번_일반명사-1`
- `이전_일반명사-1`
- `직전_일반명사-1`
- `직후_일반명사-1`

## 5. PM Note

이 batch는 개별 의미망 설계보다 coverage absorption에 가깝다.
이 단계까지는 승인된 rollout model 안에서 계속 진행 가능하다고 판단한다.
