# Token Governance Layer

## Purpose

The Token Governance Layer defines runtime rules for controlling context size, preventing repeated context loading, and preserving enough evidence for reliable AI execution.

## Token Budget Levels

| Level | Use | Context Rule |
| --- | --- | --- |
| L0 Minimal | Simple status or gate checks | Load only `AGENTS.md` and current Sprint status |
| L1 Focused | Single governance artifact | Load target doc plus governing index |
| L2 Cross-system | Multiple operating-system docs | Load affected source-of-truth docs only |
| L3 Audit | Contradiction or unknown ownership | Use targeted search across docs |
| L4 Recovery | Repeated failure or unclear repo state | Broader file review with explicit reason |

Agents must start at the lowest viable level and escalate only when blocked.

## Context Cache Rules

- Treat documents read in the current task as active context.
- Do not re-read unchanged files unless verification needs exact text.
- Prefer line-targeted reads after a file is known.
- Use indexes to avoid loading unrelated documents.
- Summarize stable decisions by linking to source docs.

## Output Compression Rules

Final updates should include:

- Files changed
- Verification evidence
- Current state
- Gate status

Avoid:

- Repeating full role definitions
- Repeating full checklists
- Explaining unchanged background
- Mixing future options into completion reports

## Escalation Rules

Escalate token level when:

- The target source-of-truth file is unknown.
- Two documents appear contradictory.
- A verifier reports an unexpected failure.
- A role or gate cannot be determined from loaded context.

Record the reason for L3 or L4 escalation in the final report when it materially affected the work.

## Runtime Metrics

Track qualitatively:

- Context tier used
- Files read
- Files changed
- Verification commands
- Avoided broad scans

These metrics support future optimization without adding heavy process overhead.
