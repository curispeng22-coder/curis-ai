# CURIS V1 — CLOUD AI CONTINUITY ACCEPTANCE

Status: Frozen

Authority Class: FROZEN / IMPLEMENTATION ACCEPTANCE RECORD

Disposition: V1-P0-003 IMPLEMENTED / ACCEPTED

Date: 2026-08-30

Evidence: `docs/reviews/CURIS_V1_P0_003_KEYCHAIN_IMPLEMENTATION_REVIEW.md`; `docs/reviews/CURIS_V1_CLOUD_MODEL_CONTINUITY_IMPLEMENTATION_REVIEW.md`

## Accepted implementation truth

- Native macOS Keychain save, read, overwrite, delete and fail-closed recovery pass.
- DeepSeek real Health and dynamic model discovery pass; discovered tenant-private models may be eligible default-model and conversation-selection candidates when tenant, Provider, Health and eligibility rules pass.
- A discovered `deepseek-v4-pro` became the tenant default and completed a real cloud call before restart.
- The same packaged `Curis.app`, with the same isolated app-data root and no credential re-entry, recovered Keychain credentials, Health, discovery, default selection and completed a second real cloud call after full restart.
- Credential deletion and post-delete restart correctly return unconnected truth.
- Secret scan: `0` hits. Repository active SQLite files remained byte-identical and healthy.

## Scope boundary

This closes the current Provider architecture + Credential Vault + native Keychain + discovery + preference + Runtime execution path as proven by DeepSeek. It does not claim every Provider is verified, nor that external Provider quality/cost or whole-app live AI acceptance is complete.

## Superseded current wording

The earlier `IMPLEMENTED / PARTIAL`, `M3 BLOCKED`, “Keychain restart unverified”, and “cloud restart continuity unverified” statements are superseded for this bounded P0 by the 2026-08-30 accepted evidence above. Historical Reviews retain their original evidence and provenance.

## Historical next gates at registration time

Whole-app Live AI Acceptance was later closed by `CURIS_V1_WHOLE_APP_LIVE_AI_ACCEPTANCE_REGISTRATION.md`. The current distribution and recovery route is owned by `CURRENT_STATE.md`; the dated items below preserve this acceptance record's original next-gate context.

- Whole-app Live AI Acceptance.
- Release-grade signing, notarization, installation, upgrade and backup/restore recovery.
- Build Reliability Debt remains tracked separately for transient Google Fonts network failures; it is not a Cloud Continuity or Keychain failure.

CLOUD AI CONTINUITY ACCEPTANCE REGISTERED
