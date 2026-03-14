# Workboard Archive Guide

> Purpose: workboard overwrite로 인한 보고 유실을 막기 위한 append-only 로그 보관 규칙

## Rule

- 현재 workboard는 snapshot만 유지한다.
- 상세 보고는 먼저 이 폴더 하위 agent별 경로에 append-only 문서로 남긴다.
- 그 뒤 workboard에는 `Latest Detailed Report Path`와 최신 상태만 남긴다.

## Recommended Layout

- `workboard_archive/planning/`
- `workboard_archive/data/`
- `workboard_archive/development/`
- `workboard_archive/review/`

## Naming

- `<YYYYMMDD>_<REVISION>_<SHORT_TITLE>.md`
- 예: `20260314_REV72_policy_rework.md`

## Approval

- 사용자 승인 요청/결과도 가능하면 상세 로그 문서에 함께 남긴다.
