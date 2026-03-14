---
name: ia-structure-designer
description: Designs and validates Information Architecture (IA) and data taxonomies. Use when restructuring vocabulary categories, defining hierarchy (Root-Category-Term), or organizing complex data structures. Do not use for database schema SQL or frontend code generation.
---

# IA Structure Designer

This skill provides expert guidance for designing and restructuring Information Architecture (IA) and taxonomies, specifically tailored for educational applications and mindmaps. 

## Core Principles

1.  **Scene-Centric Roots:** Top-level categories (대분류) must represent practical life scenes or clear conceptual buckets, not abstract linguistic terms.
2.  **Progressive Disclosure:** Keep depth to a strict 3-tier maximum: Root (대분류) ➔ Category (중분류) ➔ Term (단어). Avoid deep nesting.
3.  **Labeling Standards:**
    *   Use clear, intuitive Korean nouns.
    *   No numerical prefixes (e.g., use '쇼핑', not '4.쇼핑').
    *   No generic filler categories (e.g., remove '일반', '일반명사'). Categories must represent meaningful subdivisions.
    *   No special symbols in terms (e.g., use '사과', not '#사과').

## Workflow: IA Design & Validation

When asked to design or review a taxonomy, follow this sequential workflow:

### Step 1: Audit Current Structure
Identify violations of the core principles (e.g., numbers in roots, meaningless categories like "일반", symbolic characters).

### Step 2: Propose Restructure (Draft)
Use the following template structure to propose the new taxonomy:
```markdown
### [Root Name] (e.g., 쇼핑)
- **Rationale:** [1-sentence explanation of why this root exists]
- **Categories:**
  - [Category 1] (e.g., 가게 종류): [Term], [Term]...
  - [Category 2] (e.g., 결제): [Term], [Term]...
```

### Step 3: Quality Checklist (Self-Refinement)
Before submitting, verify:
- [ ] Are all numerical prefixes removed from Root names?
- [ ] Are all '일반' or part-of-speech (품사) categories replaced with semantic divisions?
- [ ] Are all terms clean of symbols like `#`?
- [ ] Is the maximum depth exactly 3 levels?

## Troubleshooting
*   **If a term fits multiple roots:** Assign it to the primary situational context and use `cross-links` for the secondary context. Do not duplicate nodes.
*   **If a category is too small (<3 terms):** Consider merging it with a broader category to reduce cognitive load.