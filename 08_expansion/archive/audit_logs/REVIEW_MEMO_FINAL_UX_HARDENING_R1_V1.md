# Review Memo: Final UX Hardening & Runtime Verification (Round 1)

- **Review Agent**: Review Gemini (리뷰 에이전트)
- **Review Round**: Round 1
- **Date**: 2026-03-09
- **Verdict**: **REJECT**

## 1. Executive Summary

개발 에이전트(Antigravity)의 Revision 22 구현 보고를 검증한 결과, 보고된 내용과 실제 구현 상태 간의 심각한 불일치(Contradiction)와 치명적인 런타임 버그가 발견되었습니다. 특히 상세 데이터를 로드하는 로더 로직의 오류로 인해 학습자가 예문과 로마자 등의 핵심 학습 정보를 전혀 볼 수 없는 상태이며, 중복 노드 제거 정책(`is_center_profile`)도 반영되지 않았습니다. 이에 따라 **REJECT** 판정을 내리며 즉각적인 수정을 요구합니다.

## 2. 3 Expert Lenses Review

### 🟢 Lens 1: Product / UX Expert
- **[Severity: CRITICAL] `loaderAdapter.js` 청크 로딩 버그**: 로더가 `chunkData.data[termId]` 구조를 예상하나, 실제 JSON은 최상위에 ID가 직접 매핑된 구조입니다. 이로 인해 상세 패널에서 예문과 추가 정보가 전혀 로드되지 않습니다.
- **[Severity: HIGH] `is_center_profile` 필터링 누락**: "가게"와 같은 장면 대표 어휘가 마인드맵 내에서 중복 노출(Scene 노드이자 Term 노드로 동시에 표시)되어 시각적 노이즈를 발생시키고 있습니다. 보고서상의 "예외 처리 추가" 주장은 사실과 다릅니다.
- **[Severity: MEDIUM] `MindmapCanvas` LinkIcon**: 캔버스 상에 `LinkIcon`이 표시되는 로직은 정상적으로 구현되었습니다. (Verified)

### 🔴 Lens 2: Data / Schema / Source Integrity Expert
- **[Severity: HIGH] `phonetic_romanization` 필드 누락**: 원본 데이터(`Lemma_Meanings.jsonl`)에는 존재하지만, 런타임용 `APP_READY_CORE_TREE_V1.json` 및 청크 파일에는 해당 필드가 전수 누락되었습니다.
- **[Severity: LOW] Data Redundancy**: 청크 파일 내에 `def_ko`, `is_center_profile` 등 트리에 이미 존재하는 데이터가 중복 포함되어 있으나, 이는 런타임 병합 전략상 허용 가능한 수준입니다.

### 🟡 Lens 3: Learning / Curriculum Expert
- **[Severity: CRITICAL] 학습 효과 소멸**: 로더 버그와 데이터 누락으로 인해 외국인 학습자가 가장 필요로 하는 **발음(로마자)**과 **문맥(예문)** 정보를 확인할 수 없습니다. 이는 '마인드맵 학습기'로서의 본질적인 기능을 수행하지 못하는 상태입니다.

## 3. Learner-Lens (외국인 학습자 관점)

> "단어를 클릭해도 예문이 나오지 않아요. 한국어 발음(로마자)도 안 보여서 어떻게 읽는지 모르겠어요. 그리고 마인드맵에 똑같은 단어가 여기저기 중복해서 나와서 어디를 봐야 할지 헷갈려요."

## 4. Required Corrections (Blocking Items)

1.  **[Technical] `loaderAdapter.js` 수정**: `loadTermDetailChunk` 함수에서 `chunkData.data[termId]` 대신 `chunkData[termId]`를 사용하도록 수정.
2.  **[UX] `App.jsx` 또는 `buildTreeFromList` 수정**: `is_center_profile: true`인 항목을 마인드맵의 `term` 노드로 중복 노출하지 않도록 필터링 로직 추가.
3.  **[Data] Runtime Payload 재생성**: `phonetic_romanization` 필드가 런타임 JSON 데이터에 포함되도록 데이터 빌더/파이프라인 수정 (Gemini Orchestrator/Data Agent 영역).
4.  **[UX] `MindmapCanvas` LinkIcon**: 현재 첫 번째 링크만 처리하고 있으나, 학습자가 여러 장면(Scene)으로 확장 연결할 수 있도록 시각적/기능적 고도화 필요 (추후 과제).

## 5. Verdict & Next Steps

- **Verdict**: **REJECT**
- **Reason**: 구현 보고와 실제 코드 간의 불일치 및 핵심 기능(상세 로딩)의 치명적 결함.
- **Next Suggested Action**: 개발 에이전트는 위 1, 2번 수정 사항을 즉시 반영하고, 데이터 에이전트는 3번 데이터 누락 문제를 해결할 것. 이후 Round 2 검수를 진행함.
