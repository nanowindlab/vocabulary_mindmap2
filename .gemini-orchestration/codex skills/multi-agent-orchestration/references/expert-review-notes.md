# Expert Review Notes

This skill was tightened using three perspectives.

## 1. Product Operations Perspective

Key conclusion:

- orchestration state must live with the project that owns the decision-making
- project-local placement reduces drift and makes reopen behavior predictable

Applied changes:

- recommended `.codex-orchestration/` under the project root
- added project-root detection guidance
- discouraged shared global active workboards

## 2. Agent Workflow Perspective

Key conclusion:

- agents need one current task, one reporting location, and one blocking section
- stale parallel boards create confusion faster than stale chat

Applied changes:

- enforced one active task per workboard
- clarified blocking behavior
- clarified that chat-only progress is insufficient

## 3. Governance / Verification Perspective

Key conclusion:

- Codex must verify outputs directly
- files outrank summaries
- orchestration docs should not become shadow product specs

Applied changes:

- explicit verification rule
- explicit “trust files over reports” rule
- stronger boundary between orchestration docs and project policy docs
