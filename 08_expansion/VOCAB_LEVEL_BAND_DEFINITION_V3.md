# 어휘 레벨(Level) 및 빈도(Band) 산출 최종 명세서 (V3 Final)

> **매니저 특별 지시 사항 (Absolute Rule)**: 빈도수(Band)는 오직 실제 수집된 TOPIK 통계 데이터에 기반해야 합니다. 데이터가 없는 단어에 대해 LLM 등을 활용하여 인위적으로 빈도를 추정해 내는 행위는 엄격히 금지됩니다.

---

## 1. 실측 기반 사용 빈도 (Band 1~5) 산출 시스템

단순 출현 횟수의 편중을 막기 위해 전체 빈도와 TOPIK 기출 분포를 결합한 **가중 중요도 점수(Weighted Importance Score)**를 사용하여 5단계 밴드를 부여합니다.

### 1.1. 점수 산출 수식 (대상: 통계 보유 단어 한정)
데이터 에이전트는 `frequency` 및 `round_count` 데이터가 존재하는 단어에 한해 다음 수식을 적용합니다.

$$Score = (Norm\_Freq \times 0.4) + (Norm\_Round \times 0.6)$$

- **$Norm\_Freq$**: $\log_{10}(frequency + 1) / \log_{10}(max\_frequency + 1)$
- **$Norm\_Round$**: $round\_count / max\_round$ (현재 데이터 기준 $max\_round = 16$)

### 1.2. Band 구간 정의
산출된 점수를 바탕으로 5개 구간으로 분류합니다.

| Band | 등급 명칭 | 점수 구간 ($Score$) | 학습적 의미 |
| :--- | :--- | :--- | :--- |
| **Band 1** | **Essential** | $Score \ge 0.75$ | 최상위 빈도 및 기출 핵심 (약 상위 10%) |
| **Band 2** | **High** | $0.55 \le Score < 0.75$ | 빈번하게 노출되는 주요 어휘 |
| **Band 3** | **Medium** | $0.35 \le Score < 0.55$ | 일상 소통이 가능한 일반 어휘 |
| **Band 4** | **Low** | $0.15 \le Score < 0.35$ | 특정 상황 보조 어휘 |
| **Band 5** | **Rare** | $Score < 0.15$ | 출현 빈도가 낮은 전문/심화 어휘 |

### 1.3. 통계 데이터 부재 단어 (No Data Fallback)
TOPIK 통계(`total_frequency`, `round_count`)가 없는 단어의 경우:
- **어떠한 추정도 하지 않으며**, 최종 데이터셋(JSON)의 `stats` 객체 내에서 **`freq: null`, `rank: null`, `band: null`** 로 처리합니다. (또는 해당 필드를 생략)
- 프론트엔드는 `band`가 존재하지 않을 경우 해당 배지를 렌더링하지 않습니다.

---

## 2. 밴드 비의존적 학습 레벨 (Level) 산정 시스템

기존 사전 데이터의 `grade`(초/중/고)를 기반으로 하되, 등급 정보가 없거나 밴드 데이터와 충돌하는 경우를 위한 독립적 산정 로직입니다.

### 2.1. 기본 레벨 매핑 (Base Mapping)
원본 데이터에 `grade`가 존재하는 경우, 아래와 같이 매핑합니다.

| 원본 grade | 최종 Level (ID) | UI 표시 명칭 |
| :--- | :--- | :--- |
| 초 | **Beginner** | 초급 어휘 |
| 중 | **Intermediate** | 중급 어휘 |
| 고 | **Advanced** | 고급 어휘 |

### 2.2. 통계적 보정 규칙 (Priority Correction) - Band 존재 시
Band 데이터가 존재하는 단어에 한하여, 학습 효율을 위해 아래 보정 규칙을 우선 적용합니다.

1.  **Essential Advanced (고급 ➔ 중급)**: 원본 `grade`가 **'고'** 이지만 **Band 1**인 경우 ➔ 최종 Level **'Intermediate'**.
2.  **Core Intermediate (중급 ➔ 초급)**: 원본 `grade`가 **'중'** 이지만 **Band 1**인 경우 ➔ 최종 Level **'Beginner'**.
3.  **Conservative Retention (초급 유지)**: 원본 `grade`가 **'초'** 인 경우, Band가 낮더라도 무조건 **'Beginner'** 등급 유지.

### 2.3. grade 정보 부재 단어 독립 레벨링 (Fallback Leveling)
원본 데이터에 `grade` 정보가 없는 단어들(주로 외부 사전 편입 단어)에 대한 처리 지침입니다.

- **방식**: 빈도(Band) 추정이 금지되었으므로, 해당 단어의 **형태론적/의미적 난이도 자체**만을 기준으로 LLM(gemini-2.5-flash) 평가를 수행합니다.
- **LLM 평가 가이드라인 (복합 기준 적용)**:
  - **Beginner (초급)**: 
    - (원어민 기준) 어린아이도 직관적으로 이해하는 기초 단어.
    - (학습자 기준) **TOPIK 1~2급 수준**. 인사, 음식 주문, 가족 등 **생존 한국어(Survival Korean)** 필수 어휘.
  - **Intermediate (중급)**: 
    - (원어민 기준) 일반 성인이 일상 대화나 뉴스에서 무리 없이 사용하는 단어 및 파생어.
    - (학습자 기준) **TOPIK 3~4급 수준**. 공공 시설 이용, 감정 표현, 일상적 사회 이슈 등 **실용 한국어(Practical Korean)** 어휘.
  - **Advanced (고급)**: 
    - (원어민 기준) 학술적, 전문적, 혹은 한자어 비중이 높아 문어체에서 주로 쓰이는 단어.
    - (학습자 기준) **TOPIK 5~6급 수준**. 전문 분야(정치, 경제, 과학 등)의 토론이나 논문 작성에 필요한 **학술 한국어(Academic Korean)** 어휘.
- **Fallback**: LLM 평가마저 모호하거나 실패할 경우 최종적으로 **`Unrated` (미분류)** 로 남겨두어 데이터의 무결성을 훼손하지 않습니다.

---

## 3. 데이터 및 개발 에이전트 실행 규격

- **데이터 에이전트 (Payload Builder)**
  - 산출물: `stats` 객체 내에 `band` (1~5 정수 또는 `null`), `level` (Beginner/Intermediate/Advanced/Unrated 문자열) 필드 확정.
  - 다의어(`homonym_group_id`): 각 뜻마다 고유의 통계를 가지고 있다면 그 값을 유지하고, 합산하지 말 것.
- **개발 에이전트 (UI/UX)**
  - `stats.band`가 `null`이거나 `undefined`인 경우 UI에서 Band 칩(배지)을 숨김 처리(Conditional Rendering)하여 레이아웃이 깨지지 않도록 방어 로직 구현.
