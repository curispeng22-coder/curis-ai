# Rejected Research Patterns

Status: Phase-3.5 Research -> Decision -> Contract record

## Rejected Decision Table

| Rejection ID | Source | Rejected Design | Why Not Adopt | Risk If Adopted Now | Long-Term Reference |
| --- | --- | --- | --- | --- | --- |
| RJ-PAPERCLIP-HEARTBEAT | Paperclip | 24/7 autonomous company heartbeats | Requires stronger safety, scheduling, budget, and rollback controls | runaway execution and hidden spend | yes, post-runtime governance |
| RJ-PAPERCLIP-BUDGET | Paperclip | Workspace-side budget enforcement | Belongs to L6 economy/Admin billing gates | mixes execution and billing authority | yes |
| RJ-PAPERCLIP-IMPORT | Paperclip Companies | direct company import/export mutation | Needs Admin review and tenant isolation | official catalog pollution | yes |
| RJ-METAGPT-AUTOGEN | MetaGPT | one-line requirement to full repo generation | Too broad for Phase-4 employee template MVP | uncontrolled code changes | yes |
| RJ-METAGPT-ROLEPLAY | MetaGPT | role social simulation | Not needed for CEO operating system | token waste and roleplay drift | limited |
| RJ-CHATDEV-DAG | ChatDev | full ChatChain/DAG runtime | Too heavy before workflow contracts are proven | breaks Task Execution boundary | yes |
| RJ-CHATDEV-CODE-NODES | ChatDev | arbitrary code/Python workflow nodes | Unsafe without sandbox and review | code execution/security risk | no for Phase-4 |
| RJ-CHATDEV-VOTING | ChatDev | majority voting | Adds cost and complexity | token/cost explosion | maybe later |
| RJ-CREWAI-RAW-YAML | CrewAI | raw YAML/JSONC editing as primary UI | Too developer-centric for CEO users | poor product usability | internal only |
| RJ-CREWAI-HIERARCHY | CrewAI | hierarchical manager execution | Needs routing, memory, and escalation gates | hidden multi-agent behavior | yes |
| RJ-CREWAI-BACKSTORY | CrewAI | public `backstory` field | Roleplay wording is not CEO-facing | confusing template UX | map to hidden instructions |
| RJ-AUTOAGENTS-HIRING | AutoAgents | automatic employee creation | Explicitly outside Phase-4 | unapproved staff/runtime expansion | yes, as suggestion only |
| RJ-AUTOAGENTS-LOOPS | AutoAgents | open-ended reflection loops | Needs iteration and review guardrails | infinite loops/token waste | bounded QA later |
| RJ-OPENCLAW-RAW-SOUL | OpenClaw | raw SOUL.md import | Not a safe CEO-facing template format | unsafe/unreviewed prompts | curate after Admin review |
| RJ-GPTS-CHATBOT | GPTs | chatbot-first product surface | Curis is company/task/evidence-first | loses company structure | no |
| RJ-GPTS-STORE | GPTs | GPT Store as marketplace equivalent | Curis needs tenant isolation and Admin review | marketplace governance bypass | concept only |
| RJ-COZE-BUILDER | Coze | full visual workflow builder | Too much UI/runtime scope | complex UI and workflow engine creep | later |
| RJ-DIFY-MARKETPLACE | Dify | plugin execution directly from marketplace | Needs Admin/security review | external-service risk | later G3 |
| RJ-GATEWAY-SDK | New API / One API / LiteLLM | direct provider SDK calls from Workspace | Curis requires ModelGatewayAdapter path | usage_event drift and secret exposure | no |
| RJ-TASKADE-MEMORY | Taskade | persistent workspace memory in employees | Phase-4 excludes employee memory | privacy and scope creep | later memory gate |

## Non-Negotiable Rejections For Phase-4

- direct employee system runtime
- direct department execution runtime
- full workflow engine
- capability marketplace implementation
- real credential custody
- current Task Execution main-flow mutation
- `/api/platform/*` calls from Workspace runtime
- direct provider calls outside ModelGatewayAdapter
