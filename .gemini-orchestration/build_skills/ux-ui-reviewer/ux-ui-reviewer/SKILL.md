---
name: ux-ui-reviewer
description: Evaluates UI copy, layout consistency, and overall user experience from a learner's perspective. Use when verifying screen layouts, terminology, and data presentation. Do not use for code debugging or performance profiling.
---

# UX/UI Reviewer

This skill empowers you to conduct heuristic evaluations of user interfaces, focusing specifically on educational apps and non-native speaker usability (Learner-lens).

## Core Principles: Iterative Refinement

UI reviews should not just point out flaws; they must propose concrete, iterative refinements that align with the established design system.

1.  **Consistency First:** Similar functions must look and behave identically across different contexts (e.g., all 3 main tabs must share the same structural layout).
2.  **Learner-Lens (Cognitive Load):** Terminology must be simple. If a feature represents flashcards, call it something universally understood, avoiding overly technical jargon.
3.  **Data Hierarchy:** Primary information (Target Word) must be visually dominant. Secondary information (English translation, Frequency) must be supportive but clearly separated.

## Workflow: UI/UX Critique

Structure your review using the following analytical framework:

### 1. Layout & Structural Consistency
- **Check:** Do the Scene, Expression, and Meta tabs utilize the exact same foundational layout (Sidebar + Canvas + Detail Panel)?
- **Refinement:** If discrepancies exist, dictate the exact components that need normalization.

### 2. Microcopy & Terminology (Learner-Lens)
- **Check:** Are the labels intuitive? (e.g., Is '카드 학습' better than '플립카드' for the target demographic?)
- **Refinement:** Provide a mapping table of `[Current Term] -> [Proposed Term] -> [Rationale]`.

### 3. Data Presentation & Proximity
- **Check:** Is related information grouped correctly? (e.g., The English translation should be adjacent to the Korean headword, not buried under the definition).
- **Check:** Is frequency (Band 1-5) presented as an objective metric rather than a mandatory 'level' gate?
- **Refinement:** Specify the exact spatial relationship required (e.g., "Move `def_en` to render `inline-flex` next to the `h1` headword").

## Output Verdict
End every review with a clear verdict:
*   **ACCEPT:** All UX criteria met.
*   **PARTIAL_ACCEPT:** Good foundation, but specific microcopy or proximity tweaks required (list them).
*   **REJECT:** Fundamental layout inconsistency or severe cognitive load issues.