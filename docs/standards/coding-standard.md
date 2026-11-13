# Coding Standard

This standard defines the quality bar for the current Tool System v1.5 implementation and future approved implementation.

## General Rules

- Prefer simple, readable code over clever abstractions.
- Follow existing project patterns once implementation begins.
- Keep modules small and bounded by responsibility.
- Avoid global state unless explicitly justified.
- Make integration boundaries explicit.
- Handle errors deliberately.
- Never hide verification gaps.

## Testing Rules

- Add tests for business logic, shared utilities, integrations, and regressions.
- Run the relevant test command before claiming completion.
- Include manual verification when UI or local automation is involved.
- Record unavailable verification as a known gap.

## Review Rules

Code review must check:

- Scope compliance
- Correctness
- Test coverage
- Security and privacy impact
- Maintainability
- Documentation updates

## Prohibited Until Sprint 1

- ROI system
- Employee CRUD or employee expansion
- Multi-agent system
- Business modules
- UI complexity
- Mock data or simulation mode
- External service integrations beyond the approved Codex/OpenAI executor boundary
