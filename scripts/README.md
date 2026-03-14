# Scripts Layout

- `scripts/core`: build, parse, rebuild, audit, extraction utilities that operate on project data or documentation.
- `scripts/mining`: relation/link discovery and other mining-style pipelines.
- `scripts/triage`: LLM triage and augmentation pipelines that produce classification outputs.
- `scripts/legacy`: legacy or superseded scripts retained for reference or one-off recovery work.

All scripts should resolve project-relative paths from the repository root, not from the script file directory.
