# System Feedback Loop

## Purpose

The System Feedback Loop turns review findings, verification gaps, and runtime observations into controlled updates to the operating system.

## Feedback Sources

- User review
- 总控决策席 gate decision
- QA verification gap
- Documentation source-of-truth issue
- Architecture boundary issue
- Security or privacy blocker
- Runtime state observer finding
- Repeated agent execution failure

## Feedback States

```text
Captured
  -> Classified
  -> Routed
  -> Applied
  -> Verified
  -> Closed
```

Rejected feedback moves to `Rejected` with rationale.

## Classification

Feedback must be classified as one of:

- Correction: fixes an error or contradiction.
- Clarification: makes existing rules easier to execute.
- Expansion: adds a missing system or rule.
- Gate change: changes allowed work.
- Risk: identifies a blocker or unsafe path.

## Routing

| Feedback Type | Owner | Target |
| --- | --- | --- |
| Correction | 产品规划席 | Source-of-truth document |
| Clarification | 产品规划席 | Relevant governance doc |
| Expansion | 系统交付席 | Operating system doc |
| Gate change | 总控决策席 | Sprint gate or review file |
| Risk | Relevant blocker role | Risk, gate, or ADR |

## Application Rules

- Apply feedback to the smallest affected document.
- Update indexes when a new source-of-truth file is added.
- Update plugin skill context when governance source-of-truth changes.
- Update Sprint review checklist when review scope changes.
- Preserve closed gates unless the 总控决策席 explicitly opens them.

## Verification Rules

Feedback is closed only after:

- The target document has been updated.
- Related indexes or references are current.
- Validation has passed when plugin or skill files changed.
- Gate status is restated.
