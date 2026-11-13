# ADR-001: Employee Before Model

Status: Deprecated

## Status

Accepted

## Context

Most AI workspace products require users to select a model first, then configure an agent. This reflects AI industry language but not how solo entrepreneurs think about work.

## Decision

Curis Workspace will make Employee the primary user-facing object. Model selection is part of the employee's resource strategy, not the first step of creation.

## Consequences

- Users think in terms of hiring employees.
- Model configuration becomes an advanced setting.
- The system can optimize model selection based on task type, quality, speed, and budget.
