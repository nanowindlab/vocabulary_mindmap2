---
name: doc-state-manager
description: Use when a project has multiple operational documents such as roadmap, tasklist, handoff notes, and agent workboards, and you need to keep them synchronized without repeating the same content in every file. Use it to choose one authoritative document, reduce duplication, update only deltas, and keep next-thread handoffs aligned with the current source of truth.
---

# Doc State Manager

## Overview

This skill keeps project documentation lean and synchronized.
It is for situations where `roadmap`, `tasklist`, `handoff`, and `workboard` files start drifting or repeating the same content.

## Core Rule

- Pick one authoritative document for each function and state it explicitly.
- Do not maintain the same todo list in multiple files.
- Update derivative docs with links and short deltas, not full rewrites, unless a reset is needed.

Apply these operating rules:

- `tool_persistence_rules`: keep going until the authoritative doc and all necessary dependent docs are updated, or a real blocker is recorded
- `completeness_contract`: treat the update as incomplete if the authoritative doc changed but roadmap/handoff/workboard references are left stale
- `verification_loop`: re-open the edited docs and confirm the intended source-of-truth relationship is actually reflected

Recommended split:

- `tasklist`: single authoritative todo source
- `roadmap`: status, priorities, milestone framing
- `handoff`: what changed, what to read next, what remains blocked
- `workboard`: one current task per agent

## Workflow

1. Identify which document is authoritative for the request.
2. Verify whether the requested change belongs in the tasklist, roadmap, handoff, or workboard.
3. Apply the change to the authoritative document first.
4. Update dependent docs only enough to stay accurate.
5. If the user asked for a review or status check, verify the real files before summarizing.
6. When preparing a next-thread handoff, prefer:
   - current milestone
   - key achievements
   - verified gaps
   - authoritative tasklist path
   - which agent should act next and why

## Update Rules

- If a requirement appears in chat and must not be forgotten, add it to the authoritative tasklist.
- If a status summary becomes outdated, update the roadmap instead of copying the tasklist into it.
- If an agent needs to continue later, update the handoff with the latest verified state.
- If an agent is currently working, update its workboard, not the handoff.
- If multiple docs mention the same thing, collapse them so one file owns the detail and the others point to it.

## Verification

- Treat report text as insufficient by itself.
- Check the referenced files, data, code, or build output directly.
- In summaries, lead with missing pieces and next actions, not compliments.
- After editing, confirm that the next thread could reopen the project by reading only the authoritative tasklist, roadmap, and handoff.

## Example Triggers

- "tasklist와 handoff가 중복돼서 정리해줘"
- "현재 내용 기준으로 다음 스레드 handoff 다시 써줘"
- "roadmap, tasklist, workboard를 동기화해줘"
- "이 요구사항 잊지 않도록 todo에 넣어줘"

## Default Assumption

When in doubt, reduce duplication and strengthen one source of truth rather than adding another summary file.
