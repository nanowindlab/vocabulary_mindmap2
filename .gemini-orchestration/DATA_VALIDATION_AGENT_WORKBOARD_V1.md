# 데이터 에이전트 작업보드 [ROUND 10 / REVISION 65]

> Agent: `신임 데이터 에이전트` (Data Strategist Gemini)
> Version: `V1-RESTART-REVISION-65`
> Date: `2026-03-11`
> Status: `DONE` (Data Agent Completed)
> Runtime redeploy SOP: `08_expansion/APP_DATA_REDEPLOY_SOP_V1.md`를 단어 업데이트/재배포 작업 전에 반드시 먼저 읽을 것

## 💬 매니저 전달용 채팅 지시문 (Manager's Command)
"데이터 에이전트님, 프로젝트 환경 최적화를 위한 **[X-CLEAN Phase 2: 스크립트 격리 및 경로 보정]** 미션을 하달합니다. 
1. **[물리적 격리]**: 루트 디렉토리에 산재된 모든 `*.py` 스크립트를 `scripts/core/`, `scripts/mining/`, `scripts/triage/` 등 성격에 맞게 분류하여 이동시키십시오.
2. **[경로 무결성 회복]**: 스크립트 위치가 바뀌었으므로 내부의 상대 경로(`../` 등)가 모두 깨질 것입니다. `08_expansion/STRUCTURAL_CHANGELOG_V1.md`를 참고하여 소스 코드 내의 파일 참조 경로를 전수 보정하십시오.
3. **[검증]**: 이동 후 스크립트(`build_master_pool_v1.py` 등)를 `--help`나 기본 모드로 실행하여 `FileNotFoundError`가 발생하지 않는지 확인 후 보고하십시오."

---

## 1. Current Task: [V1-REV-65] 루트 스크립트 격리 및 파일 경로 정규화 실행

### Goal: 프로젝트 루트를 슬림화하고, 변경된 디렉토리 구조(scripts/ 도입)에 맞춰 모든 Python 로직이 정상 작동하도록 경로를 하드닝함.

1.  **[Isolation] 스크립트 도메인 분리**:
    *   루트의 파이썬 스크립트들을 `scripts/` 하위 구조로 재배치.
2.  **[Path Refactoring] 코드 레벨 상대 경로 교정**:
    *   파이썬 코드 내의 파일 참조 경로들을 전수 보정.
3.  **[Dry Run Check]**:
    *   주요 스크립트 구동 테스트를 통한 에러 선제 방어.

---

## 2. Latest Report (Previous)
- **2026-03-12 09:50:11 KST**: `V1-REV-47` 후속 정규화 완료.
  - 정책 반영:
    - 같은 `system/root/category`만 `related_vocab` 유지
    - 다른 분류로 넘어가는 연결은 `refs.cross_links`로 이동
  - live runtime count:
    - `APP_READY_SITUATIONS_TREE.json`: `related_vocab 4289 / cross_links 559`
    - `APP_READY_EXPRESSIONS_TREE.json`: `related_vocab 1724 / cross_links 100`
    - `APP_READY_BASICS_TREE.json`: `related_vocab 1618 / cross_links 146`
    - `APP_READY_SEARCH_INDEX.json`: `related_vocab 7631 / cross_links 805`
  - 전수 검증:
    - `related_vocab` 타깃 누락 `0`
    - `related_vocab` 타분류 오염 `0`
    - `cross_links` 동일분류 오염 `0`
    - `cross_links` 타깃 누락 `0`
    - `chunk_id` 존재 `8092 / 8092`
  - detail chunk도 동일 기준으로 재생성 완료.
- **2026-03-11**: [V1-REV-47] 8.1K 단어 풀 대상 XWD 마이닝 및 양방향 주입 진행 중 (백그라운드).
- **2026-03-11**: [V1-REV-44] 연관 데이터 196건 주입 실재 확인 및 배포 완료 (최종 승인).

- **2026-03-12 08:13:13 KST**: `V1-REV-47` 완료.
  - linked_terms `7675`, link_edges `28308`
  - split `related_vocab`: 상황 `4319`, 표현 `1732`, 기초 `1624`
  - split `cross_links`: 상황 `69`, 표현 `33`, 기초 `53`
  - 최종 산출물:
    - `09_app/public/data/APP_READY_SITUATIONS_TREE.json`
    - `09_app/public/data/APP_READY_EXPRESSIONS_TREE.json`
    - `09_app/public/data/APP_READY_BASICS_TREE.json`
    - `09_app/public/data/APP_READY_SEARCH_INDEX.json`
    - `08_expansion/rev47/REV47_RELATED_LINKS_V1.json`
    - `08_expansion/rev47/REV47_PUBLISH_SUMMARY_V1.json`
  - 무결성 검증:
    - `self_link_count 0`
    - `asymmetry_sample_count 0`
  - 개발 handoff: `08_expansion/rev47/REV47_DEV_HANDOFF_V1.md`
- **2026-03-12 08:13:13 KST**: `V1-REV-65` 완료.
  - scripts/ 격리 및 경로 보정 후 새 경로 기준 REV-47 완료 검증 통과.
  - 추가 정리:
    - `09_app/public/data/live/`: 앱 runtime canonical
    - `09_app/public/data/internal/`: rebuild support files
    - `09_app/public/data/legacy/`: 구세대 산출물
    - `09_app/public/data/archive/`: obsolete backup/chunks
  - 경로 보정 대상:
    - `09_app/src/data/loaderAdapter.js`
    - `scripts/core/*`
    - `scripts/triage/*`
    - `scripts/mining/*`
  - 검증 통과 스크립트 예시:
    - `scripts/core/build_master_pool_v1.py`
    - `scripts/core/parse_xwd_framework.py`
    - `scripts/triage/run_rev23_3depth_triage.py --publish-only`
    - `scripts/mining/run_rev47_xwd_mining.py`
- **리뷰 에이전트 안내**:
  - current runtime canonical과 폴더 역할 혼동 방지를 위해 `08_expansion/REVIEW_HANDOFF_CANONICAL_GUIDE_V1.md`를 먼저 읽을 것.
