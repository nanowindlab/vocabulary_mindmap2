---
name: report-verifier
description: Use when an agent claims work is done and you need to verify that claim against the real files, data, code, build output, or logs. Use it for progress checks, code reviews, payload validation, document updates, and any handoff where chat summaries might drift from the actual artifacts.
---

# Report Verifier

## Overview

This skill turns an agent report into a verification workflow.
It is for cases where you must check the artifacts directly before accepting the report or deciding the next step.

## Core Rule

- Do not trust report text by itself.
- Verify the referenced artifacts directly.
- Lead with gaps, mismatches, and residual risks before strengths.

Apply these operating rules:

- `tool_persistence_rules`: keep verifying until the main claims are either confirmed, disproved, or explicitly marked unverified
- `completeness_contract`: treat the report as incomplete if claims, artifacts, validation evidence, and next action do not line up
- `verification_loop`: read the report, inspect the artifacts, compare them, and only then set the next instruction

## Verification Workflow

1. Read the report or workboard update.
2. Extract the concrete claims:
   - files changed
   - counts or metrics
   - build/test status
   - UX behavior
   - next suggested action
3. Check the real artifacts:
   - files exist
   - code actually changed
   - data values match the report
   - build or test output confirms the claim
4. Separate findings into:
   - verified
   - unverified
   - contradicted
5. Summarize:
   - what is confirmed
   - what is still missing
   - what should happen next

Minimum acceptance contract:

- claimed artifacts exist
- claimed behavior is supported by code or data
- claimed validation actually ran
- residual gaps are named
- the next step follows from the verified gaps

## What To Check First

- Runtime/build claims
- Data counts and payload shape
- Whether the claimed UI behavior is actually supported by the code
- Whether “done” really means done or just partially implemented
- Whether the next step proposed by the agent is blocked by unresolved gaps

## Output Style

- Keep strengths brief.
- Put missing pieces, mismatches, and improvement opportunities first.
- If the report is incomplete, say that explicitly.
- If the next step is clear, convert the gaps directly into the next agent instruction.
- If verification is partial, say exactly what was not checked.

## Example Triggers

- "제미나이 보고서 확인"
- "안티그래비티 보고 확인"
- "이 보고 내용이 실제로 반영됐는지 검증해줘"
- "주장 말고 실제 파일 기준으로 검토해줘"

## Default Assumption

If verification and the report disagree, trust the artifacts and update the next instruction accordingly.
