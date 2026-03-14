# Instruction Patterns

## Working Agent Pattern

Include:

- single goal
- why this is the next step
- read-first files
- required outputs
- self-validation
- final report format

## Review Agent Pattern

Include:

- scope to review
- review-only restriction
- acceptance verdict requirement
- findings ordered by severity
- next suggested action

## Codex Decision Pattern

After reading a report:

1. summarize only the important change
2. verify artifacts directly
3. state accept / partial accept / reject
4. update the next workboard only if warranted

## Escalation Pattern

If there is ambiguity:

- do not silently choose for both agents
- record the blocker in the relevant workboard
- ask the user only when the decision is materially risky
