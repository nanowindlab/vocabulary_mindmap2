# Placement Rationale

## Default Recommendation

Place orchestration files in:

```text
<project-root>/.codex-orchestration/
```

## Why

- keeps execution state attached to the repository
- prevents cross-project leakage
- allows standard file names
- makes reopen / continuation easier
- minimizes confusion for working and review agents

## When a Central Folder Is Acceptable

Only use a central cross-project folder if the user explicitly wants portfolio-level management.

Even then, prefer:

1. project-local working files
2. one central index that points to them

Do not put the real active workboards for multiple projects in one shared folder by default.

## Naming Rule

Prefer:

```text
.codex-orchestration/
  WORK_ORCHESTRATION_HUB_V1.md
  GEMINI_WORKBOARD_V1.md
  REVIEW_GEMINI_WORKBOARD_V1.md
```

over custom per-project file names.

Project identity should come from the folder location, not from renaming every file.
