# 어휘 레벨(Level) 및 빈도(Band) 산출 알고리즘 명세서 (V1)

> **기획 의도**: 8,545건의 어휘에 대해 단순 통계치를 넘어선 학습적 가치를 부여합니다. 사용 빈도(Band)는 실제 코퍼스 분석 데이터를 기반으로 하고, 학습 레벨(Level)은 교육적 등급과 통계적 중요도를 결합하여 산출합니다.

---

## 1. 사용 빈도 (Band 1~5) 산출 시스템

단순 출현 횟수의 편중을 막기 위해 전체 빈도와 TOPIK 기출 분포를 결합한 **가중 중요도 점수(Weighted Importance Score)**를 사용합니다.

### 1.1. 점수 산출 수식
데이터 에이전트는 각 단어에 대해 다음 수식을 적용하여 `Importance_Score`를 계산합니다.

$$Score = (Norm\_Freq \times 0.4) + (Norm\_Round \times 0.6)$$

- **$Norm\_Freq$**: $\log_{10}(frequency + 1) / \log_{10}(max\_frequency + 1)$
- **$Norm\_Round$**: $round\_count / max\_round$ (현재 데이터 기준 $max\_round = 16$)

### 1.2. Band 구간 정의
산출된 점수를 바탕으로 5개 구간으로 분류합니다.

| Band | 등급 명칭 | 점수 구간 ($Score$) | 학습적 의미 |
| :--- | :--- | :--- | :--- |
| **Band 1** | **Essential** | $Score \ge 0.8$ | 한국어 생활 및 시험에서 가장 핵심적인 어휘 |
| **Band 2** | **High** | $0.6 \le Score < 0.8$ | 매우 자주 사용되는 주요 어휘 |
| **Band 3** | **Medium** | $0.4 \le Score < 0.6$ | 일상적인 의사소통에 필요한 일반 어휘 |
| **Band 4** | **Low** | $0.2 \le Score < 0.4$ | 특정 문맥에서 주로 사용되는 보조 어휘 |
| **Band 5** | **Rare** | $Score < 0.2$ | 출현 빈도가 낮거나 전문적인 어휘 |

---

## 2. 학습 레벨 (Level) 매핑 및 보정 시스템

기존 사전 데이터의 `grade`(초/중/고)를 기반으로 하되, 통계적 중요도(Band)를 반영하여 최종 레벨을 확정합니다.

### 2.1. 기본 레벨 매핑
| 원본 grade | 최종 Level (ID) | UI 표시 명칭 |
| :--- | :--- | :--- |
| 초 | **Beginner** | 초급 어휘 |
| 중 | **Intermediate** | 중급 어휘 |
| 고 | **Advanced** | 고급 어휘 |
| N/A | **Unrated** | 미분류 어휘 |

### 2.2. 통계적 보정 규칙 (Priority Rules)
학습자의 학습 효율을 위해 교육적 등급보다 통계적 빈도가 압도적으로 높을 경우 레벨을 조정합니다.

1.  **Essential Advanced (고급 ➔ 중급 조정)**:
    - 조건: 원본 `grade`가 **'고'** 이지만, 산출된 **Band가 1**인 경우.
    - 결과: 최종 Level을 **'Intermediate'**로 하향 조정. (난이도는 높으나 사용 빈도가 매우 높으므로 중급 단계에서 미리 학습 권장)
2.  **Core Intermediate (중급 ➔ 초급 조정)**:
    - 조건: 원본 `grade`가 **'중'** 이지만, 산출된 **Band가 1**인 경우.
    - 결과: 최종 Level을 **'Beginner'**로 하향 조정. (필수 기본 어휘로 간주)
3.  **Conservative Retention (초급 유지)**:
    - 조건: 원본 `grade`가 **'초'** 인 경우, Band가 아무리 낮더라도(Band 5) **'Beginner'** 등급을 유지함. (기초 어휘의 교육적 상징성 보존)

---

## 3. 데이터 에이전트 실행 가이드 (Implementation)

1.  **데이터 결합**: `Lemma_Meanings.jsonl`과 `MY_Lemma_Stats.jsonl`을 `meaning_id` 기준으로 Join 하여 `frequency`와 `round_count`를 확보할 것.
2.  **수식 적용**: 위 1.1의 수식을 적용하여 모든 단어의 `Importance_Score`를 계산할 것.
3.  **필드 생성**: 최종 결과물에 `stats.band` (1~5 정수)와 `stats.level` (Beginner/Intermediate/Advanced) 필드를 추가할 것.
4.  **예외 처리**: `round_count`가 없는 단어는 0으로 처리하되, `frequency`만으로 $Norm\_Freq$를 계산하여 점수를 산출할 것.

---
**Verdict**: 본 알고리즘은 언어학적 통계와 교육적 목적을 결합한 최적의 레벨링 시스템입니다.
