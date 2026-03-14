---
name: multi-agent-orchestration
description: Use when coordinating a working agent and a review agent across complex multi-step work in any project. Creates and maintains a project-local orchestration folder with a hub, per-agent workboards, and a handoff template so instructions, status, and review stay in one place and do not drift across threads or projects.
---

# Multi-Agent Orchestration

Use this skill when:

- one agent is producing artifacts and another is reviewing them
- work will continue across multiple threads
- the user wants document-driven coordination instead of repeated chat handoffs
- different projects must not share coordination files or stale instructions

This skill is especially appropriate when:

- the user wants one-time handoff to multiple agents
- the user is tired of acting as the relay between agents
- build, review, and product-direction work must stay synchronized

## Core Rule

Create all coordination files inside the **current project root**, not in a global folder.

Recommended folder:

```text
<project-root>/.codex-orchestration/
```

If the repository already has an established coordination folder, use that instead of creating a second one.

## Why This Location Is Recommended

Prefer a **project-local hidden folder** over a shared cross-project folder.

Reasons:

1. prevents cross-project instruction drift
2. keeps agent state tied to the repository that owns the work
3. makes archived context reproducible when another thread opens the same project
4. avoids accidental reuse of stale workboards from another project
5. allows file names to stay consistent across projects

### Do Not Prefer This by Default

Avoid using one shared global folder such as:

```text
<main-folder>/orchestration/
```

unless the user explicitly wants a portfolio-level control room.

That pattern is more likely to cause:

- mixed project state
- stale handoff reuse
- naming collisions
- the wrong agent reading the wrong board

If a central overview is needed, keep the **working boards** in the project root and create only a small external index that points to them.

## Required Files

Create these files inside the project-local orchestration folder:

1. `WORK_ORCHESTRATION_HUB_V1.md`
2. `<WORKING_AGENT_NAME>_WORKBOARD_V1.md` for each working agent
3. `<REVIEW_AGENT_NAME>_WORKBOARD_V1.md` for each review-only agent
4. `HANDOFF_REPORT_TEMPLATE_V1.md`

Recommended naming:

- `DATA_VALIDATION_AGENT_WORKBOARD_V1.md`
- `DEVELOPMENT_AGENT_WORKBOARD_V1.md`
- `REVIEW_AGENT_WORKBOARD_V1.md`

Use stable names. Prefer changing the `Revision` field inside the file over renaming files frequently.

Optional but recommended:

5. `README.md` inside the orchestration folder only if the user explicitly asks for a human onboarding note

Otherwise, avoid adding extra docs.

## Roles

### Codex

- final owner of direction
- validates actual outputs, not just reports
- decides sequencing between agents

### Working Agent

- creates or updates artifacts
- must report in its workboard
- must not mark work complete without outputs and validation

### Review Agent

- review only
- no direct implementation unless explicitly re-assigned
- must end with `ACCEPT`, `PARTIAL_ACCEPT`, or `REJECT`

### User

- approves direction changes
- does not need to relay full context every turn
- may only need to send an initial handoff once if the orchestration files are maintained well

## Operating Sequence

Default order:

1. working agent
2. Codex validation
3. review agent
4. Codex decision
5. next workboard update

Do not let implementation and review silently redefine the same contract in parallel.

## Review Handoff Pattern

Default handoff pattern should be:

1. Codex updates the working agent workboard first
2. the user relays that workboard to the working agent
3. the working agent writes its result back into the same workboard
4. the user relays that same workboard to the review agent
5. the review agent appends its review into that same workboard
6. the user tells Codex the workboard is ready
7. Codex verifies the same workboard plus the underlying artifacts

Use this by default for both:

- `개발 에이전트`
- `데이터 검증 에이전트`

This means the working agent workboard should be the main thread-of-record for:

- current task
- latest work report
- latest review
- final Codex verification context

User-facing reporting rule:

- Codex and every agent should still leave a short, exact chat summary for the user
- prefer 1-3 short lines
- include only:
  - current state
  - main finding or blocker
  - next handoff target

The review agent may keep its own queue/status board, but the review verdict itself should be added to the target working workboard.

Exception:

- Codex may work directly with the review agent alone when the task is review-only
- in that case, the review agent board itself may be the primary document for that cycle

Apply these operating rules throughout the workflow:

- `tool_persistence_rules`: once a phase starts, keep moving until there is a verified handoff, a concrete blocker, or the next agent step is set
- `completeness_contract`: a phase is not complete unless workboard, artifacts, verification evidence, and next-step instruction are all aligned
- `verification_loop`: Codex must verify the actual artifacts before moving the next agent or accepting a report

## Prompting Principle

All agent instructions should explicitly use:

- `Self-Refine prompt`
- `Iterative Prompting`
- `Reflection Pattern`

This means:

1. do not ask an agent for a single-pass answer when the task is materially important
2. instruct the agent to produce an initial pass, critique its own weak points, revise, and only then leave the final report
3. require a brief reflection note in the final report stating:
   - what was re-checked
   - what changed after self-review
   - what remains uncertain

Minimum cycle:

1. draft
2. self-review
3. revision
4. reflection
5. final report

Use this principle for working agents and review agents alike.

## Initialization Procedure

When first applying this skill in a project:

1. identify the true project root
2. create `<project-root>/.codex-orchestration/`
3. create the hub
4. create one workboard per active agent
5. create the handoff template
6. write the current project phase, guardrails, and active tracks into the hub
7. write exactly one current task into each active workboard

Do not create extra status files, automation logs, or helper READMEs unless the user explicitly asks.

## Project Root Detection

Before creating `.codex-orchestration/`, identify the real project root.

Good signals:

- the folder containing the main source tree
- the folder containing the primary package manifest / build config / repo root
- the folder the user explicitly identifies as the project path

If the user gives both a data repo and an app repo, keep orchestration in the repo where the current thread's decisions are owned. Link to the sibling repo from the hub instead of splitting one orchestration state across both by default.

## What Codex Must Do

Every cycle:

1. read the hub
2. read the relevant workboard
3. inspect real files, code, JSON, build output, or validation logs
4. summarize for the user
5. update the next workboard only if direction is clear

Do not accept:

- chat-only status with no workboard update
- review with no verdict
- implementation report with no actual artifact verification

Codex should also:

- keep the hub short and current
- move detailed instructions into workboards
- update the sequence when the critical path changes
- prevent one agent from racing ahead of an unapproved structural decision
- prefer small, verified handoffs over optimistic status jumps

## Workboard Rules

Each workboard must contain:

- mission
- read first
- current task
- expected outputs
- self-validation rule
- reporting rule
- blocking / decision needed
- latest report

For working-agent workboards, also include:

- latest work report
- latest review
- review status

For review-agent workboards, keep:

- current review target
- review queue / blocking state
- latest review delivery note

Keep the `Latest Report` brief but concrete.
If there is a detailed report, link it from the workboard.

Only one active task should be primary in each workboard.
If a new task replaces the old one, update the existing workboard instead of spawning a second competing board.

If an agent is blocked waiting for another agent, say so explicitly in `Blocking / Decision Needed`.
Do not leave a stale task active without that note.

When using the review handoff pattern:

- do not leave the review verdict only in the review agent board
- append the actual review verdict and findings into the target working workboard
- let Codex validate that combined workboard after the user reports it back

## Reporting Discipline

If an agent reports in chat but not in its workboard, treat the work as **not fully reported**.
If a review agent reports only in chat and does not leave a review memo file plus a workboard update, treat the review as **not delivered**.

When Codex reviews an agent report:

- prioritize missing pieces, weak assumptions, regressions, and improvement opportunities over strengths
- summarize strengths briefly only after the gaps are clear
- turn the identified gaps directly into the next agent instruction whenever the next step is naturally determined
- do not rely on the report text alone; verify the underlying files, data, code, or build output directly before accepting the report
- if verification is incomplete, say so explicitly and do not treat the step as fully complete

If an agent says work is complete, Codex should still verify:

- files exist
- outputs match the stated contract
- build or validation really passed
- the result is aligned with the current hub direction

For review agents, require all of the following before treating the review as complete:

- updated `Latest Report` in the review workboard
- updated `Latest Review` in the target working workboard
- one concrete review memo file in the project
- a final verdict in `ACCEPT`, `PARTIAL_ACCEPT`, or `REJECT`
- enough file references that Codex can verify the findings directly

If the workboard and the actual files disagree, trust the files and update the workboard after verification.

## User-Facing Guidance

When the user asks how to run this system:

- tell them to send each agent one initial message only
- after that, all detailed coordination should happen through the project-local orchestration files
- when you give a task to an agent, also send the user a brief status update in chat
- when addressing a specific agent, name that agent explicitly so the instruction target is unambiguous
- that brief user update should also include a short summary of the instruction you just gave
- do not call out agents that are simply waiting unless the user asks for a full status sweep
- when the user asks what to do next, name only the agent that should act now unless multiple agents truly need to move in parallel
- prefer giving the agent call order explicitly so there is no ambiguity about sequencing
- do not generate a full handoff message every time if the agent already has a valid workboard
- after the first initialization message, prefer short instructions such as `GEMINI_WORKBOARD 확인` or `REVIEW_GEMINI_WORKBOARD 확인`
- only give a full explicit instruction block to an agent on its first use, after a reset/restart, or when the workboard alone would be ambiguous
- before telling the user `현재 바로 작업할 에이전트` and linking a workboard, first update that workboard and any directly related orchestration docs so the link reflects the latest instruction state
- do not give the user an agent link first and then update the workboard afterward; update first, then share the agent name and link
- if the next step is naturally determined and does not require user judgment, proceed to the next agent step immediately
- in that case, review the current agent report, update the next agent workboard if needed, and give the user only a brief progress report
- when a working agent finishes, tell the user to pass that same workboard to the review agent
- when a review agent finishes, expect the user to return with that same workboard as the review-bearing source

Suggested one-time handoff pattern:

```text
Use the orchestration files in <project-root>/.codex-orchestration/ as the source of truth.
Check your workboard for new tasks.
Write progress and blockers back to your workboard.
```

## File Placement Advice

Use this folder layout:

```text
<project-root>/
  .codex-orchestration/
    WORK_ORCHESTRATION_HUB_V1.md
    WORKING_AGENT_WORKBOARD_V1.md
    REVIEW_AGENT_WORKBOARD_V1.md
    HANDOFF_REPORT_TEMPLATE_V1.md
```

This avoids confusion between projects and prevents old coordination state from leaking into a new repository.

Optional only if needed:

```text
<main-folder>/
  orchestration-index.md
```

This file may link to multiple project-local orchestration folders, but it should not replace them.

## Templates

Use the templates in:

- [document-layout.md](references/document-layout.md)
- [instruction-patterns.md](references/instruction-patterns.md)
- [placement-rationale.md](references/placement-rationale.md)

## Important

This skill is about coordination, not project policy.

Do not invent taxonomy, product rules, or technical contracts inside the orchestration files.
Those belong in the project's own documents.

If the project already has product, taxonomy, or payload contracts, the hub should only link to them.
Do not duplicate those rules into the orchestration files unless a short summary is necessary for execution safety.

Read [expert-review-notes.md](references/expert-review-notes.md) before large changes to the coordination structure.
