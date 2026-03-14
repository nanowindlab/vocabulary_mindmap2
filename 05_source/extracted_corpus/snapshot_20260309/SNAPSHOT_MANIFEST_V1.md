# Corpus Snapshot Manifest V1 (2026-03-09)

> Version: `V1`
> Date: `2026-03-09`
> Purpose: `Authoritative source for Source-Rich Projection Builder`

이 폴더는 코퍼스 DB(`corpus.db`)에서 추출된 9개 핵심 객체의 최신 스냅샷을 보관합니다. `PROJECTION_BUILDER`는 이 경로를 고정 입력 소스로 사용합니다.

## 1. Snapshot Items

| Object Name | Source Type | Filename | Row Count (Est.) |
| :--- | :--- | :--- | :--- |
| **Lemma_Examples** | Table | `Lemma_Examples.jsonl` | 48,654 |
| **Lemma_Meanings** | Table | `Lemma_Meanings.jsonl` | 8,139 |
| **Processing_Errors**| Table | `Processing_Errors.jsonl`| 0 |
| **Sentences_Staging**| Table | `Sentences_Staging.jsonl`| 23,203 |
| **Sources** | Table | `Sources.jsonl` | 84 |
| **Word_Occurrences** | Table | `Word_Occurrences.jsonl` | 310,617 |
| **Example_Sentences**| View | `Example_Sentences.jsonl`| 310,617 |
| **MY_Lemma_Stats** | View | `MY_Lemma_Stats.jsonl` | 7,866 |
| **Z_ALL_Lemma_Stats**| View | `Z_ALL_Lemma_Stats.jsonl`| 9,044 |

## 2. Usage Policy

1.  **Read-Only**: 이 폴더의 파일은 수동으로 수정하지 않습니다.
2.  **Stable Key**: 조인 시 `lemma_id` 또는 `meaning_id`를 기본 키로 사용합니다.
3.  **Authoritative Fields**:
    - 통계 및 빈도: `MY_Lemma_Stats` 우선
    - 발음 및 발음 로마자: `Lemma_Meanings` 우선
    - 실제 기출 예문: `Example_Sentences` 우선

## 3. Storage Plan

- **Path**: `05_source/extracted_corpus/snapshot_20260309/`
- **Retention**: 마일스톤 완료 시까지 유지하며, DB 업데이트 시 폴더를 새로 생성하여 버저닝함.
