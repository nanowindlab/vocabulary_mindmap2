# Review Handoff Canonical Guide V1

> Date: `2026-03-12`
> Purpose: 리뷰 에이전트가 최근 데이터 작업 결과를 검토할 때 canonical 파일, 폴더 역할, 검토 범위를 혼동하지 않도록 하기 위한 안내문

## 1. Current Canonical Runtime Data

리뷰 에이전트는 아래 경로를 현재 앱의 실제 runtime canonical로 간주해야 한다.

- `09_app/public/data/live/APP_READY_SITUATIONS_TREE.json`
- `09_app/public/data/live/APP_READY_EXPRESSIONS_TREE.json`
- `09_app/public/data/live/APP_READY_BASICS_TREE.json`
- `09_app/public/data/live/APP_READY_SEARCH_INDEX.json`
- `09_app/public/data/live/CHUNK_MANIFEST_V1.json`
- `09_app/public/data/live/APP_READY_CHUNK_RICH_chunk_*.json`
- `09_app/public/data/live/APP_READY_CHUNK_EXAMPLES_chunk_*.json`

## 2. Folder Role Clarification

- `09_app/public/data/live/`
  - 앱이 실제 fetch하는 현재 canonical
- `09_app/public/data/internal/`
  - rebuild 및 검증 보조용 내부 파일
  - 예: `APP_READY_CORE_PAYLOAD_V1.json`, `APP_READY_SCHEMA_COMPLETE_V1.json`
- `09_app/public/data/legacy/`
  - 비교/복구용 구세대 산출물
  - 현재 앱 runtime 검증 기준으로는 primary source가 아님
- `09_app/public/data/archive/`
  - 보관용

리뷰 에이전트는 `legacy/`나 `archive/`에 있는 예전 파일을 current runtime evidence로 오인하지 말 것.

## 3. Recent Data Work Scope

### V1-REV-44

- 목적: 기존 source/expansion/archive 자료를 다시 읽어 `related_vocab`와 `cross_links`를 복구하고, 이를 배포 4개 파일 본문에 주입
- current runtime 기준 결과:
  - situations `related_vocab` non-empty `156`
  - expressions `related_vocab` non-empty `23`
  - basics `related_vocab` non-empty `17`
  - unified search `related_vocab` non-empty `196`

### V1-REV-47

- 목적: 기존 연관어휘를 유지하는 것이 아니라, XWD 프레임워크 기반으로 8,092 core 풀의 연관 관계를 재마이닝하고 양방향 정합화 후 재배포
- current runtime 기준 결과:
  - `linked_terms 7675`
  - `link_edges 28308`
  - `self_link_count 0`
  - `asymmetry_sample_count 0`

### V1-REV-65

- 목적: 루트 Python 스크립트 격리와 경로 무결성 보정
- 결과:
  - `scripts/core`, `scripts/mining`, `scripts/triage`, `scripts/legacy` 구조 신설
  - `09_app/public/data`도 `live/internal/legacy/archive`로 역할 분리

## 4. Recommended Review Procedure

1. `live/` 기준 파일 count와 주요 필드 존재를 확인
2. `APP_READY_SEARCH_INDEX.json`와 3 split tree 사이의 `id`, `related_vocab`, `refs.cross_links` 정합성을 검토
3. detail chunk는 `live/APP_READY_CHUNK_RICH_*`, `live/APP_READY_CHUNK_EXAMPLES_*`만 본다
4. 문제가 보이면 먼저 `live/` 기준인지, `legacy/`를 잘못 본 것인지 확인한다

## 5. Key References

- `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`
- `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`
- `08_expansion/rev47/REV47_PUBLISH_SUMMARY_V1.json`
- `08_expansion/rev47/REV47_DEV_HANDOFF_V1.md`
- `08_expansion/STRUCTURAL_CHANGELOG_V1.md`
- `.gemini-orchestration/ORCHESTRATION_DASHBOARD.md`
- `.gemini-orchestration/DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
