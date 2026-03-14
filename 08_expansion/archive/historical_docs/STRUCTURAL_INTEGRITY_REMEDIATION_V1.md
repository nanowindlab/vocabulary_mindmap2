# [V1-REV-63] 프로젝트 무결성 리스크 해결 및 검증 보고서 (Validated Remediation Plan)

> 작성일: 2026-03-11
> 작성자: 리뷰 에이전트 (Review Agent)
> 검증 완료: 3인 전문가(DevOps/Data/Gov) 교차 검증 및 리뷰어 2차 검증 통과
> 상태: **FINAL_REMEDIATION_READY**

## 1. 개요 (Executive Summary)
본 보고서는 3인 전문가 및 리뷰어의 2단계 검증을 거쳐 확정된 프로젝트 무결성 회복 설계도임. 기존 기획 리스크에 대한 해결책 외에, 시스템 리스크(스크립트 경로)와 데이터 정합성(로그 링크)을 대폭 보강함.

---

## 2. [Remediation 1] 버전/링크 교정 및 SSOT 회복 (Fix-up List)

| 대상 문서 | 현재 상태 (As-Is) | 교정 안 (To-Be) | 조치 유형 |
| :--- | :--- | :--- | :--- |
| `MASTER_ROADMAP_V1.md` | `...TASKLIST_V5.md` | `...TASKLIST_V9.md` | **Version Fix** |
| `MASTER_ROADMAP_V1.md` | `...SCENARIO_SPEC_V6.md` | `...SCENARIO_SPEC_V8.md` | **Version Fix** |
| `TASKLIST_V9.md` | `Tasklist V5 HD` | `Tasklist V9 HD (historical target, current canonical은 [Tasklist V11](../../SOURCE_RICH_IMPLEMENTATION_TASKLIST_V11.md))` | **Link Conversion** |
| `TASKLIST_V9.md` | `IA V4` | `[IA V4 Spec](../../IA_AND_UX_SCENARIO_SPEC_V8.md)` | **Link Conversion** |

---

## 3. [Remediation 2] 다차원 경로 보정 및 무결성 검증 (Path Fix)

### 3.1. 전방위 경로 치환 (Target: MD & Python)
- **MD 보정**: `find . -name "*.md" -exec sed -i '' 's|(\.\./|(\.\./\.\./|g' {} +`
- **PY 보정**: 스크립트 내 하드코딩된 경로(`open('../08_expansion/...')`)를 `os.path` 기반 절대 경로 또는 보정된 상대 경로로 일괄 전환. (데이터 에이전트 전담)

### 3.2. 실행 안전 장치 (Safety Net)
- **Pre-check**: `git status`를 통해 'Clean' 상태 확인 필수.
- **Verification**: `find . -name "*.md" | xargs grep -l "(\.\./\.\./"` 명령어로 치환 여부 전수 확인.

---

## 4. [Remediation 3] Asset Ownership Matrix (Governance)

| 분류 | 관리 자산 | 주 오너 | 관리 가이드라인 |
| :--- | :--- | :--- | :--- |
| **정책/명세** | `Spec/Dictionary/Framework` | **기획** | 헤더 메타데이터 수정 금지. 본문 내용 변경 시 리뷰어 승인. |
| **빌드/데이터** | `scripts/core/`, `raw_data/*.json` | **데이터** | 스크립트 내부 경로 무결성 책임. 리팩토링 시 개발팀과 동기화. |
| **검증/감사** | `scripts/triage/`, `QC_Reports` | **리뷰** | **최종 아카이빙 권한 보유.** 타 에이전트의 오너십 침해 여부 감시. |
| **배포/구현** | `09_app/`, `dist/` | **개발** | 런타임 데이터 로드 경로 및 빌드 안정성 책임. |

---

## 5. [Remediation 4] 결정 로그(Decision Log) 정밀 업데이트 (V29~V63)

`PROJECT_DECISION_LOG_V1.md` 섹션 5에 다음의 '증거 기반 로그'를 주입함.

- **[V31-V34] 알고리즘**: 실측 기반 레벨/밴드 알고리즘 확정 (참조: `IA_AND_UX_SPEC_V8`)
- **[V42-V44] 데이터 복구**: 8K 예문 및 연관어 재주입 완료 (참조: `DATA_REFINEMENT_REPORT_V1`)
- **[V48] XWD 프레임워크**: 20종 컨텍스트 훅 설계 승인 (참조: `XWD_DISCOVERY_FRAMEWORK_V1.md`)
- **[V60-V63] 구조 최적화**: Project X-CLEAN 및 무결성 보정 안 확정 (참조: `STRUCTURAL_INTEGRITY_REMEDIATION_V1.md`)

---

## 6. 향후 실행 계획 (Next Actions)
1.  **[Phase 1]**: 위 리스트에 기반한 `MASTER_ROADMAP` 및 `TASKLIST` 링크 수동 교정 (즉시).
2.  **[Phase 2]**: `DECISION_LOG`에 증거 링크를 포함한 로그 주입 (즉시).
3.  **[Phase 3]**: 물리적 파일 이동 후, 검증된 `sed` 명령어로 경로 파손 일괄 보정 및 링크 체크 수행.
