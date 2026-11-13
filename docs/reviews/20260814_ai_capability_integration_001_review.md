# AI-CAPABILITY-INTEGRATION-001 Review

Status: Review  
Decision: `CAPABILITY ECOSYSTEM REVIEW REQUIRED`  
Runtime Evidence: PARTIAL  
Date: 2026-08-14

## Accepted evidence

- Existing New API/OpenAI-compatible Gateway, Catalog, Capability, Employee Binding, Usage and Artifact paths were reused.
- Ollama completed real discovery and Employee → Model → Runtime → Artifact in an isolated database.
- Codex completed real local discovery, authorization probe, JSONL execution, session resume and Employee → Agent → Runtime → Artifact in a temporary read-only workspace.
- Skill/Expert reuses the existing 55 active SkillTemplate chain, Curis expert templates and read-only external production line; external scan remains 27 resources and 0 newly Curis-ready.
- MCP/Connector reuses the existing manifest parser, stdio minimum adapter and two connector registrations; no real MCP vertical is claimed.
- Local Agent discovery is Registry-driven and returns only actually detected entries; tests cover hiding uninstalled products and rejecting GUI-only programmatic import.
- Focused Registry/Agent/protocol tests pass: `11 passed in 0.15s`.

## Not accepted as complete

- No cloud Provider Key was available; official BYOK authorization/discovery/execution remains unverified.
- Local credential secrets are process-memory only and do not survive Desktop restart.
- No external Skill Candidate has newly passed Curis task/recovery validation; five missing-license Skills remain BLOCKED.
- Streamable HTTP/OAuth MCP and a real MCP Employee/Workspace vertical are absent.
- Claude Code, TRAE, Cursor, OpenClaw, Gemini CLI, Copilot CLI and Coze have research/contract evidence only, not current Curis execution evidence.
- Codex cancel is not implemented; adapter reports `cancel_supported=false`.

## Product contract

- Four Review registries are canonical for this专项: Model Provider, Skill/Expert, MCP/Connector and Agent Adapter Compatibility.
- The ordinary-user Agent list is discovery output, not the internal compatibility catalog; uninstalled brands do not appear.
- Official BYOK, advanced gateway, local model and future PLATFORM supply remain one Model Capability path.
- `LIVE / READY / DISCOVERABLE / RESEARCHED / BLOCKED / UNKNOWN` never overrides actual product states or execution gates.
- `AI_Capability_UI_Contract.md` provides data and action contracts only; no Product Blueprint, UI Blueprint, Prototype, navigation or second Runtime change is accepted here.

## Decision

The ecosystem shape is ready for Product/Frontend review. Runtime remains PARTIAL until secure credentials, one real cloud BYOK path and one real MCP vertical pass. Further Agent work starts only from an actually installed/authorized target and a concrete use case.

`CAPABILITY ECOSYSTEM REVIEW REQUIRED`
