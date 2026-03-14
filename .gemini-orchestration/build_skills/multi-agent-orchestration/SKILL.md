---
name: multi-agent-orchestration
description: Use when coordinating a working agent and a review agent across complex multi-step work. Creates and maintains a project-local orchestration folder with a hub, per-agent workboards, and a handoff template so instructions, status, and review stay in one place.
---

# Multi-Agent Orchestration

## Overview

Use this skill to coordinate multiple agents (Working Agent, Review Agent) through document-driven coordination in `.gemini-orchestration/`.

## Core Rule

- Create all coordination files inside the project root's `.gemini-orchestration/` folder.
- Use the Working Agent Workboard as the main thread-of-record.
- Do not mark work complete without artifact verification.

## Roles

- **Gemini Orchestrator (Manager)**: Final owner, validates outputs, decides sequencing.
- **Working Agent**: Creates/updates artifacts, reports in its workboard.
- **Review Agent**: Review only, provides findings and verdict (ACCEPT/REJECT).

## Operation Sequence

1. Manager updates the working agent workboard.
2. Working agent performs task and reports in the same workboard.
3. Review agent appends review findings and verdict into the same workboard.
4. Manager verifies both the report and the actual artifacts.

## Required Documents

1. `WORK_ORCHESTRATION_HUB_V1.md`: Project phase, guardrails, tracks.
2. `*_WORKBOARD_V1.md`: One per agent (Working/Review).
3. `HANDOFF_REPORT_TEMPLATE_V1.md`: Template for detailed reports.

## Prompting Principle

Always use:
- `Self-Refine prompt`: Draft -> Self-Review -> Revision.
- `Reflection Pattern`: Brief note on what was re-checked and what remains uncertain.
