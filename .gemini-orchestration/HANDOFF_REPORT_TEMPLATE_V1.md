# Handoff Report Template V1

> Version: `V1`
> Use this template for working-agent and review-agent reports

## 1. Work Title

- short task name

## 2. Agent

- `기획 에이전트` / `데이터 에이전트` / `개발 에이전트` / `리뷰 에이전트`

## 3. What Was Read

- input documents
- input data
- input code or scripts

## 4. What Was Produced

- created files
- updated files
- no-file result if applicable

## 5. Validation Performed

- schema check
- build or run result
- payload verification
- review method

## 6. Problems Found

- issue 1
- issue 2

## 7. Solution Proposed

- solution 1
- solution 2

독자 결정이 어려우면:

- option A / pros / risks / recommended?
- option B / pros / risks / recommended?
- option C / pros / risks / recommended?

## 8. Fixes Applied

- fix 1
- fix 2

## 9. Acceptance or Status

- `ACCEPT` / `PARTIAL_ACCEPT` / `REJECT` for review
- `COMPLETE` / `BLOCKED` / `IN_PROGRESS` for working agent

## 10. Remaining Risks

- risk 1
- risk 2

## 11. Next Suggested Action

- one next unit only

## 12. Detailed Report Path

- `.gemini-orchestration/workboard_archive/<agent>/...`

에이전트는 이 상세 보고 문서만 작성한다.
dashboard와 workboard snapshot의 제어 필드는 직접 수정하지 않는다.

## 13. User Approval Gate

- approval requested: yes / no
- state: `요청 전` / `승인 대기` / `승인됨` / `보류` / `반려`
- evidence:

## 14. Review Attachment

- for working-agent workboards: paste the review verdict here after review
- for review-agent workboards: state which target workboard was updated

## 15. Self-Refine Note

- what was re-checked
- what changed after self-review

## 16. Reflection Note

- weakest assumption
- remaining uncertainty

## 17. Canonical Guard

- confirmed `06_normalized_lexicon/01_canonical/NORMALIZED_LEXICON_CONFIRMED_283_V1.json` untouched: yes / no
