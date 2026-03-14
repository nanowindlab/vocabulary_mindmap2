# Raw Dictionary Missing Scan Report V1

> Date: `2026-03-11`
> Scope: `05_source/raw_dictionary/한국어 어휘사전(영어판)_사전.json` 대비 `Lemma_Meanings.jsonl` 누락 항목 식별
> Output:
> - `08_expansion/augmentation/RAW_DICTIONARY_MISSING_CANDIDATES_V1.jsonl`
> - `08_expansion/augmentation/RAW_DICTIONARY_MISSING_SKIPPED_V1.json`
> - `08_expansion/augmentation/RAW_DICTIONARY_MISSING_SCAN_SUMMARY_V1.json`

## 1. Scan Result

- 원본 raw dictionary:
  - `entries 5,041`
  - `senses 5,041`
- 기존 처리 대상:
  - `Lemma_Meanings 8,139`
- 기존 처리와 직접 매칭된 raw sense:
  - `3,747`
- 추가 편입 후보:
  - `1,291`
- 자동 추출에서 제외된 항목:
  - `3`

## 2. Candidate Distribution

- `일반명사 810`
- `동사 161`
- `형용사 133`
- `일반부사 89`
- `수사 31`
- `의존명사 21`
- `관형사 17`
- `감탄사 16`
- `대명사 12`
- `접속부사 1`

## 3. Excluded From Auto-Augmentation

아래 3건은 뜻풀이 또는 품사 정보가 비어 있어 자동 triage 대상에서 제외했다.

- `교실`
  - visual-only row, `definition_ko` 없음
- `동물원`
  - visual-only row, `definition_ko` 없음
- `애기`
  - `example_ko`와 영어 equivalent는 있으나 `definition_ko` 없음

이 3건은 후속 수동 보강 또는 다른 source 결합이 필요하다.

## 4. Candidate Examples

- `가늘다_형용사-1`
- `가능성_일반명사-1`
- `가득하다_형용사-1`
- `가득히_일반부사-1`
- `가만_일반부사-1`

## 5. Operational Note

- 이번 추출은 기존 처리 집합에 없는 raw dictionary origin sense를 augmentation 전용 입력으로 분리한 것이다.
- 다음 단계는 `RAW_DICTIONARY_MISSING_CANDIDATES_V1.jsonl`을 별도 triage 파이프라인으로 분류하고, 성공 시 기존 `CORE / SYSTEM_CAND / CAT_CAND / EXCLUDED` 결과에 병합하는 것이다.
