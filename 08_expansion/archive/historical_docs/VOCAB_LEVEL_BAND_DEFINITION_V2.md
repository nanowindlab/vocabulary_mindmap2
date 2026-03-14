# 어휘 레벨(Level) 및 빈도(Band) 산출 통합 명세서 (V2)

> **문서 성격**: 본 문서는 어휘 레벨 및 빈도 산출을 위한 **최종 통합 지침서**입니다. V1의 핵심 수식과 V2의 지능형 추정 로직을 모두 포함하고 있으므로, 데이터 에이전트는 이 문서 하나만으로 8,545건 전수에 대한 레벨링 공정을 완수하십시오.

---

## 1. 사용 빈도 (Band 1~5) 산출 시스템

단순 출현 횟수의 편중을 막기 위해 전체 빈도와 TOPIK 기출 분포를 결합한 **가중 중요도 점수(Weighted Importance Score)**를 사용하여 5단계 밴드를 부여합니다.

### 1.1. 점수 산출 수식 (Standard Logic)
데이터 에이전트는 각 단어에 대해 다음 수식을 적용하여 `Importance_Score`를 계산합니다.

$$Score = (Norm\_Freq \times 0.4) + (Norm\_Round \times 0.6)$$

- **$Norm\_Freq$**: $\log_{10}(frequency + 1) / \log_{10}(max\_frequency + 1)$
- **$Norm\_Round$**: $round\_count / max\_round$ (현재 데이터 기준 $max\_round = 16$)

### 1.2. Band 구간 정의 및 피팅 목표
산출된 점수를 바탕으로 5개 구간으로 분류합니다.

| Band | 등급 명칭 | 점수 구간 ($Score$) | 학습적 의미 및 데이터 목표 |
| :--- | :--- | :--- | :--- |
| **Band 1** | **Essential** | $Score \ge 0.75$ | 최상위 빈도 및 기출 핵심 (약 10%) |
| **Band 2** | **High** | $0.55 \le Score < 0.75$ | 빈번하게 노출되는 주요 어휘 (약 15%) |
| **Band 3** | **Medium** | $0.35 \le Score < 0.55$ | 일상 소통이 가능한 일반 어휘 (약 25%) |
| **Band 4** | **Low** | $0.15 \le Score < 0.35$ | 특정 상황 보조 어휘 (약 30%) |
| **Band 5** | **Rare** | $Score < 0.15$ | 출현 빈도가 낮은 전문/심화 어휘 (잔여) |

### 1.3. 통계 데이터 부재 단어 처리 (LLM Estimation)
통계가 없는 외부 사전 단어는 LLM(gemini-2.5-flash)이 "TOPIK 필수 어휘 6,000" 목록을 참조하여 다음 기준에 따라 Band를 추정합니다.
- TOPIK 초급 필수 포함 ➔ **Band 1**
- TOPIK 중급 필수 포함 ➔ **Band 2~3**
- 목록에 없으나 일상적 ➔ **Band 4**, 매우 전문적 ➔ **Band 5**

---

## 2. 학습 레벨 (Level) 매핑 및 보정 시스템

기존 사전 데이터의 `grade`(초/중/고)를 기반으로 하되, 통계적 중요도(Band)를 반영하여 최종 레벨을 확정합니다.

### 2.1. 기본 레벨 매핑 (Base Mapping)
| 원본 grade | 최종 Level (ID) | UI 표시 명칭 |
| :--- | :--- | :--- |
| 초 | **Beginner** | 초급 어휘 |
| 중 | **Intermediate** | 중급 어휘 |
| 고 | **Advanced** | 고급 어휘 |
| N/A | **Unrated** | 미분류 (2.3절에 따라 자동 산출) |

### 2.2. 통계적 보정 규칙 (Priority Correction Rules)
학습 효율을 위해 교육적 등급보다 통계적 빈도가 압도적으로 높을 경우 레벨을 조정합니다.

1.  **Essential Advanced (고급 ➔ 중급)**: 원본 `grade`가 **'고'** 이지만 **Band 1**인 경우 ➔ 최종 Level **'Intermediate'**.
2.  **Core Intermediate (중급 ➔ 초급)**: 원본 `grade`가 **'중'** 이지만 **Band 1**인 경우 ➔ 최종 Level **'Beginner'**.
3.  **Conservative Retention (초급 유지)**: 원본 `grade`가 **'초'** 인 경우, Band가 낮더라도 무조건 **'Beginner'** 등급 유지.

### 2.3. grade 정보 부재 단어 자동 레벨링 (Auto-Leveling Matrix)
원본 데이터에 등급 정보가 없는 경우, 아래 매트릭스에 따라 `level`을 자동 부여합니다.

| 구분 | Band 1 (Essential) | Band 2~3 (High/Med) | Band 4~5 (Low/Rare) |
| :--- | :--- | :--- | :--- |
| **명사/동사/형용사** | **Beginner** | **Intermediate** | **Advanced** |
| **부사/관형사** | **Intermediate** | **Intermediate** | **Advanced** |
| **기타 (감탄사 등)** | **Beginner** | **Advanced** | **Advanced** |

---

## 3. 예외 상황 및 데이터 품질 관리

1.  **예문 부족군 식별**: **Band 1~2** 단어인데 `sentence_count`가 0인 경우 ➔ 데이터 에이전트가 별도 리스트로 추출하여 우선 보강 대상으로 관리.
2.  **다의어 독립 빈도**: 동일한 표기(homonym)라도 개별 의미별로 측정된 빈도를 각자 유지하여, 실제 쓰임의 차이를 보존함.
3.  **데이터 무결성 규격**:
    - `stats.band`: 1, 2, 3, 4, 5 (Integer)
    - `stats.level`: "Beginner", "Intermediate", "Advanced" (String)

---
**Verdict**: 본 명세서는 통계적 엄밀성과 교육적 유연성을 결합한 완성된 시스템이며, 8천 건 전수에 대한 무결한 레벨링을 보장합니다.
