# ADR-0037: Domain Frozen Entry Documents

Status: Frozen

Baseline:
main @ c0e1855f

Updated:
2026-07-30

Module: Documentation Governance

## Decision

Curis uses one Frozen entry document for each current domain:

- Product: `docs/01_Product/Curis_Product_Context.md`
- Architecture: `docs/02_Architecture/Curis_System_Architecture.md`
- Design: `docs/03_Design/Curis_Design_System.md`
- Development: `docs/04_Development/Curis_Development_Guide.md`

The entry documents summarize current rules. Existing documents remain in
place as evidence, reference, Review or Deprecated history.

## Reason

- Agents need a bounded current context path.
- Historical files must remain searchable without competing with current facts.
- Phase 2 must not perform a bulk migration or delete evidence.

## Consequences

- `CURRENT_STATE.md` remains the first authority and points to the four entries.
- Each domain entry owns the current summary for that domain.
- Lower-authority sources cannot override a Frozen entry.
- File migration remains deferred to a separately confirmed Phase 3.
