# Curis RD Workspace Reference Synthesis

Status: Review

Document type: Product reference research / design input

Research date: 2026-08-14, Phase 2 direct walkthrough

Owner: Curis Principal Product Reference Researcher

Boundary: This is not the Product Blueprint, UI Blueprint, prototype, runtime contract, or implementation specification. It records externally evidenced interaction patterns and Curis reuse decisions only.

## 1. Research method and evidence boundary

This research is organized by real development tasks, not by product introductions. Every claim is classified as:

- `CONFIRMED`: directly supported by a current official document or an observable local application state.
- `INFERRED`: a product implication derived from confirmed behavior; not a claim that the product explicitly uses this design language.
- `UNVERIFIED`: not confirmed in this pass, unavailable in the local UI, or only described by a secondary source.

Local observations:

| Product | Observation | Evidence status |
|---|---|---|
| VS Code | Running local app exposes Explorer, Search, Source Control, Run and Debug, Extensions, Agent entry, integrated panel, and open-folder commands. | CONFIRMED local UI |
| Linear | Local app was at `linear.app/auth/desktop` with `Loading…`; no authenticated workspace surface was available. | UNVERIFIED local product behavior |
| Codex Desktop | The local bundle identifier `com.openai.codex` returned no readable accessibility tree in this pass. | UNVERIFIED local UI |
| EvoFlow | The local bundle identifier `com.evovex.evoflow` returned no readable accessibility tree in this pass. | UNVERIFIED local UI |
| Chrome research tabs | Existing tabs included Codex/Claude-related references, Relevance AI, EvoFlow, and Curis prototype pages. | CONFIRMED local browser state; not product capability evidence |

The official evidence set is listed in §13. No feature was promoted to confirmed merely because it appears in the requested research checklist.

## 2. Cross-product task matrix

### Task A — Start a development work

| Product | Entry and object | During work | Return / continuation | Evidence |
|---|---|---|---|---|
| Codex Desktop | Project organizes separate agent threads; each thread is an independently addressable work item. | Multiple agents can run in parallel; worktrees isolate edits. | Switch threads without losing context; inspect or check out changes later. | CONFIRMED official Codex app page |
| Claude Code | Start in a project directory; session is local to the directory. | A session can continue, resume by ID, or run in a worktree. | `--continue`, `--resume`, and `/resume` restore work; worktrees enable parallel sessions. | CONFIRMED official Claude docs |
| Cursor | Open a codebase in the editor; Agent, Ask, Manual, and Custom modes select the operating contract. | Agent explores, edits, runs terminal commands, and fixes errors; Ask is read-only. | Chat history and background agents provide continuation; web/background work can return to desktop. | CONFIRMED official Cursor docs |
| VS Code + GitHub | Open a folder/repository; Source Control becomes the repository work surface. | Edit, inspect changes, stage, commit, sync; PR extension adds PR flow. | Branch/worktree can open in another window; PR review stays linked to source control. | CONFIRMED official VS Code docs |
| Linear | Project overview is an orientation and planning object with resources, milestones, status, and details sidebar. | Work items carry status, assignee, project and progress context. | Search/recent/command access restores the last working object. | CONFIRMED official Linear docs |

**Reference decision:** Curis should start from `研发任务 / Workspace / 工作线程` as distinct but linked objects. The CEO returns to a thread or active employee workstation, not to a generic chat home. Project-like context is orientation; the actual work object is the active responsibility and its evidence.

### Task B — Give an agent a task

| Product | Composer / input behavior | Context controls | Execution contract |
|---|---|---|---|
| Codex Desktop | Official evidence confirms a thread prompt, project organization, skills, and permission boundary. Exact current desktop composer placement and all visible controls are `UNVERIFIED`. | Project/thread context, local branch or worktree, skills, and permissions are explicit concepts. | Agent can edit within its working folder/branch and requests permission for elevated actions by default. |
| Claude Code | CLI prompt is the primary confirmed input; prompts can reference files/directories with `@`. | Plan mode, permission mode, model, session continuation, MCP, skills, and subagents are explicit control surfaces. | Plan reads and proposes without disk edits until approval; permissions are session/tool boundaries. |
| Cursor | Agent composer supports mode selection and codebase context; `@file`, `@folder`, and other context references are confirmed. | Automatic relevant-context gathering plus surgical context; tools can be enabled/disabled per mode. | Agent may search, edit, run terminal, use MCP, auto-apply, auto-run, and guardrails according to mode/settings. |

**Reference decision:** Curis should adopt a compact composer with three layers:

1. intent input: the CEO/employee request;
2. attached context: current Workspace, responsibility, files, branch/worktree, and evidence;
3. execution controls: plan or run, model/reasoning, skill/tool availability, and permission.

Do not expose every tool as a button. Show only controls that change the current run contract.

### Task C — Agent is developing

| Need | Codex | Claude Code | Cursor | Curis reference |
|---|---|---|---|---|
| Current activity | Thread progress and reviewable changes are confirmed; exact event taxonomy is `UNVERIFIED`. | Turn-by-turn output is available with verbose mode; tool/session behavior is visible in the terminal session. | Agent reads terminal output and continues; terminal history is preserved. | Keep Conversation as the explanation and decision stream; expose a compact activity strip for current step, tool, file, command, test, and wait state. |
| Permission | Sandbox and elevated-command permission are explicit. | Permission modes and prompts are explicit. | Auto-run/guardrails are explicit settings. | Permission request must appear at the action boundary with reason, scope, and allow-once/allow-for-session choices. |
| Long-running work | Separate threads, parallel agents, worktrees, and automations are confirmed. | Scheduled tasks, resume, worktrees, background/parallel sessions are confirmed. | Background agents run remotely and can be followed up or taken over. | Employee Workstation remains openable and resumable; status must say working, waiting, needs CEO, failed, or completed—not “AI running” only. |
| Human intervention | Review/comment on diff and continue thread are confirmed. | Plan approval, permission approval, resume, and follow-up are confirmed. | Take over, review diffs, and send follow-ups are confirmed for background work. | CEO intervention attaches to the same responsibility/session and preserves the previous state. |

### Task D — Inspect output

| Object | User need | Mature entry pattern | Curis contract |
|---|---|---|---|
| File / source | Understand exact source and context. | Explorer, file references, codebase search, or `@file` context. | Open from current thread, file tree, or evidence; return preserves thread position. |
| Diff / changes | Decide what changed and whether it matches intent. | Codex review in thread; VS Code Source Control/diff editor; Cursor edits/review. | Utility surface opens beside or above the thread; conversation remains resumable. Actions: inspect, comment, request change, accept/reject at the applicable product boundary. |
| Terminal / command | See actual runtime behavior and reproduce failures. | VS Code integrated terminal; Claude/Cursor agent terminal; Codex terminal evidence. | Terminal is a utility view with command, output, exit status, and rerun/stop; do not bury it in prose. |
| Test / problems | Validate behavior, not just text changes. | VS Code Run/Debug and Problems; agents run tests and read outputs. | Test result is a durable evidence object linked to the change and responsible employee. |
| Browser / preview | Verify the user-facing result. | Product-specific preview/browser surfaces are not uniformly confirmed across all references. | Treat browser/preview as `UNVERIFIED` until provider evidence or local proof exists; when available, it is a utility surface linked to the thread and result. |
| Review / PR | Make an informed integration decision. | VS Code GitHub extension creates and reviews PRs; Codex and Claude can assist PR workflows. | Review is a result stage, not a decorative button; it must show scope, checks, comments, owner, and next action. |

### Task E — Complete Git work

VS Code provides the clearest source-control contract: open repository → inspect Changes → stage → commit → sync/pull/push; branches and worktrees support parallel work; GitHub integration adds PR creation and review. The official docs also make a boundary visible: virtual GitHub repositories have limited support for tasks, debugging, and integrated terminals.

**Curis reuse:** show Git only when a real repository/worktree is attached. The minimum meaningful path is:

`worktree / branch → changes → checks → commit → push or PR → review result`.

If a provider cannot perform an operation, show the exact blocked stage and recovery path. Do not show an unconnected “Git” button.

### Task F — Multiple agents collaborate

| Product | Confirmed mechanism | What it teaches Curis |
|---|---|---|
| Codex | Separate project threads, parallel agents, isolated worktrees, review/comment/check-out. | Parallel work is manageable when each run has an addressable thread, isolation, and return path. |
| Claude Code | Subagents have their own context/tool access/permissions and return summaries; worktrees and background/parallel sessions are documented. | Side work should return a concise result, not flood the main conversation. |
| Cursor | Background agents run asynchronously in isolated remote environments; user can follow up, take over, review/merge, and open in Cursor. | Long-running work needs status, takeover, review, and handoff across surfaces. |
| Relevance AI | Workforce connects specialists; AI connection, forced next step, approval required, max auto-runs, Task View, escalation, and continuation/new-task options are documented. | Status must describe who is acting, what is waiting, and whether the handoff is automatic or human-gated. |
| EvoFlow | Current local UI was not readable; the requested DAG/super-agent concepts are not accepted as product evidence. | `UNVERIFIED`; Curis must not copy a DAG view based on a product name or remembered concept. |

**Curis reuse:** Employee + Role + Responsibility is the visible unit. Handoff is a responsibility transition with a source employee, receiving employee, context package, acceptance state, and return/result. Parallel employees are sibling Workstations around one goal, not top navigation tabs and not an exposed DAG.

## 3. Interaction contracts

### 3.1 Composer

| Field | Reference contract |
|---|---|
| User need | State or refine a concrete development responsibility while keeping the active Workspace and employee context. |
| Entry | Expand the active Employee Workstation or select “继续当前工作”; a new thread is available only when there is a new responsibility. |
| Spatial location | Within the active Workstation’s Conversation area; execution controls are attached to the composer, not a permanent global tool rail. |
| Required context shown | Workspace, current responsibility, employee identity, current branch/worktree, files/evidence attached, and unresolved needs. |
| Input | Natural-language task, clarification, correction, or approval. |
| Context actions | Add file/folder/image/source; select current worktree; attach goal or plan; reference skill/tool only when it changes execution. Exact Codex desktop affordances are `UNVERIFIED`; the behavior is a synthesis from confirmed provider patterns. |
| Run controls | Plan / run; model/reasoning; permission mode; send/stop. “Voice” is `UNVERIFIED` and should not be added without a user need. |
| During work | Composer remains available for safe follow-up; destructive or scope-expanding actions pause for approval. |
| Result | Conversation summary plus linked file changes, commands, tests, review, and next handoff. |
| Return | Close utility surface or collapse workstation; reopening restores the same session and active result. |
| Do not copy | A kitchen-sink menu with every plugin/tool/setting visible on every task. |

### 3.2 Diff

| Field | Interaction contract |
|---|---|
| User need | Verify that a proposed change is the smallest correct change for the stated responsibility. |
| Entry | From agent result, Changes/Source Control, file, Review, or PR. |
| Spatial location | Developer Utility Surface; can occupy the main work area while the Workstation remains the owning session. |
| Open behavior | Opens the selected file/change set with scope, originating responsibility, and related test output. |
| During work | Conversation remains available as a companion; user can comment, request revision, navigate files, and inspect adjacent evidence. |
| Actions | Inspect, comment, request revision, open externally, stage/commit only when the repository contract permits. Accept/reject must mean something in the connected provider; otherwise use review decision language. |
| Exit / return | Close or switch utility view returns to the same Conversation message and Workstation state. |
| Curis addition | Employee identity, responsibility, handoff source, evidence status, and CEO decision boundary. |

### 3.3 Permission / needs CEO

| Field | Interaction contract |
|---|---|
| User need | Make a consequential action safe and understandable without forcing the CEO to monitor every low-risk tool call. |
| Entry | Agent reaches a restricted command, external write, missing context, failed recovery, or decision boundary. |
| Spatial location | Status card in the Workstation and a surfaced CEO attention item; not a hidden settings page. |
| Open behavior | Shows requested action, target, reason, impact, evidence, and available choices. |
| Actions | Approve once, approve within stated scope, reject, provide instruction, take over, or return to sender. |
| Result | The same session resumes or transitions to a recorded blocked/recovery state. |

## 4. Composer reference by provider

| Provider | Confirmed reusable behavior | Exact visible controls still needing direct product capture |
|---|---|---|
| Codex | Project/thread organization; parallel agents; worktrees; diff review/comment; editor handoff; skills; sandbox/elevated permission; automations/review queue. | Current desktop composer geometry; exact file/folder/image/goal/plan/model/reasoning controls; current browser/preview/terminal tabs. `UNVERIFIED`. |
| Claude Code | Prompt in project directory; `@` file/directory references; plan mode before edits; permission modes; session continue/resume; worktrees; subagents; skills/MCP; scheduled tasks; PR workflow. | Desktop composer layout and exact attachment affordances. CLI-first behavior is confirmed; GUI parity is not assumed. |
| Cursor | Mode picker; automatic and surgical context; file/folder references; agent tools; terminal; auto-apply/auto-run/guardrails; background agent follow-up and takeover. | Current composer menu labels and exact placement may vary by version. Treat visual details as `UNVERIFIED`. |

## 5. Developer Utility Surface reference

The utility surface is a flexible work area, not a permanent right sidebar. Its object rules are:

| Utility | Open when | Must preserve | Close / return |
|---|---|---|---|
| Source / file tree | Need to locate or attach source | Current employee/session and selected file | Return to thread with selected source reference |
| Code / editor | Need to inspect or manually edit source | Worktree, unsaved state, origin responsibility | Return to thread; external editor handoff must be explicit |
| Diff / Changes | Need to verify or comment on modifications | Change scope, evidence, conversation anchor | Return to originating result or review |
| Terminal | Need actual command/runtime evidence | Command history, process status, exit code | Return to the step that requested it |
| Test / Problems | Need validation or failure diagnosis | Test command, output, timestamp, affected change | Return to result/revision loop |
| Browser / preview | Need user-facing verification | URL/preview target, captured state, environment | Return to result or CEO review |
| Git / PR / Review | Need integration or acceptance decision | Branch/worktree, checks, comments, owner | Return to Workspace result and next handoff |

Default behavior: one utility can take focus; multiple utilities may be opened only when their relation helps the current decision. Utilities must not permanently consume the Workspace or replace the owning Conversation.

## 6. Context classification

| Context object | Curis primary navigation | Workspace context | Employee Workstation | Flexible utility |
|---|---:|---:|---:|---:|
| Company / Business / Workspace | ✓ |  |  |  |
| Current responsibility / goal |  | ✓ | ✓ |  |
| Employee identity / role / status |  | ✓ | ✓ |  |
| Work threads / sessions |  | ✓ | ✓ |  |
| Files / source / recent files |  | ✓ | ✓ | ✓ |
| Worktree / branch |  | ✓ |  | ✓ |
| Diff / changes / review |  | ✓ | linked result | ✓ |
| Terminal / test / problems |  |  | linked activity | ✓ |
| PR / commit / push |  | ✓ | linked result | ✓ |
| Skills / tools / plugins |  |  | execution control | ✓ when configured |
| Scheduled/background work |  | ✓ status | ✓ status |  |
| History / recent |  | ✓ | ✓ |  |

Reasoning: primary navigation answers “where in the company am I?”; Workspace context answers “which development responsibility and resources are active?”; Workstation answers “who is currently responsible and what is the live conversation?”; utility answers “which professional inspection or execution surface is needed for this decision?”

## 7. End-to-end development journey

| Stage | CEO sees | Employee state | Context | Utility surface | Transition |
|---|---|---|---|---|---|
| CEO states a development goal | R&D Workspace and a new responsibility draft | Product/Planning employee working | Workspace, goal, source constraints | None or source picker | Goal becomes a scoped responsibility |
| Product manager clarifies | One expanded Workstation with questions and proposed acceptance | Working / needs CEO | Goal, assumptions, acceptance, linked source | Optional source | CEO answers or approves plan |
| Handoff to architect | Previous workstation collapses with handoff summary; architect expands | Product completed; architect working | Handoff package and responsibility ownership | None | Architect accepts responsibility |
| Architect proposes solution | Plan and affected areas visible | Working / needs CEO if scope changes | Files, constraints, plan | File/source or plan utility | CEO approves or revises |
| Handoff to developer | Architect collapses; developer expands | Developer working | Approved plan, worktree, relevant files | Optional source | Developer executes in same Workspace chain |
| Code / diff / test | Conversation remains the explanation; utility shows source, diff, test | Working or needs CEO | Branch/worktree, changes, commands | Diff, terminal, test | Evidence accumulates against responsibility |
| CEO intervenes | Attention item shows exact question and impact | Developer needs CEO | Same session, pending action | Relevant utility opens only if needed | CEO answers, approves, rejects, or takes over |
| QA finds issue | QA workstation expands with failed evidence | QA working; developer waiting or reactivated | Failure, reproduction, affected change | Test/problems/diff | Explicit handoff returns issue to developer |
| Review | Review result with scope, checks, unresolved comments | Developer/QA collapsed unless action needed | PR/branch/commit, evidence | Review/PR | CEO accepts, requests change, or blocks |
| Commit / push / PR | Real repository status and next action | Release/developer responsible | Worktree, branch, remote, permissions | Git/PR | Connected provider records result |
| Result / CEO review | Business-readable result, technical evidence, residual risk | All relevant employees collapsed; owner remains visible | Result, evidence, decision, learning | Optional diff/preview | CEO closes, continues, or opens next responsibility |

## 8. Curis RD Workspace synthesis matrix

| Curis capability | First reference | Second reference | Why | Curis absorption |
|---|---|---|---|---|
| Agent Conversation / Session | Codex | Claude Code | Thread/session is the durable unit of continuing work. | Employee Workstation owns one resumable responsibility conversation. |
| Composer | Cursor | Claude Code | Context can be both automatic and surgical; plan/permission changes execution. | Compact composer with attached context and run contract. |
| Project / Workspace context | Codex | Linear | Codex binds agents to projects; Linear supplies low-noise orientation, status, search and recent access. | Workspace context sidebar links responsibility, threads, files, worktree, result. |
| Source / editor | VS Code | Cursor | Professional source navigation and editing remain distinct from chat. | Utility surface; external editor handoff is a first-class return path. |
| Diff / changes | Codex | VS Code | Reviewable changes connect agent result with repository truth. | Diff anchored to responsibility, evidence, and reviewer decision. |
| Terminal / test / problems | VS Code | Cursor | Runtime output is evidence; agent reads it to iterate. | Utility surfaces with durable command/test evidence. |
| Git / branch / worktree | VS Code | Codex | Isolation, source control, and parallel work prevent collision and create integration stages. | Show only for connected repo/worktree; no fake Git affordance. |
| PR / review | VS Code + GitHub | Claude Code | PR is a reviewable integration object with comments and checks. | Result stage with owner, checks, comments, and CEO boundary. |
| Long-running work | Codex | Cursor | Threads/background agents need progress, follow-up, takeover, and review. | Workstation state plus resumable session and result queue. |
| Plan / permission | Claude Code | Codex | Plan-before-edit and sandbox permission create trust boundaries. | Plan and permission are visible run contracts, not hidden settings. |
| Multi-agent handoff | Relevance AI | Claude Code | Explicit responsibility routing plus isolated subagent context. | Employee, role, responsibility, handoff package, acceptance, return. |
| Status / search / recent | Linear | Codex | Low-noise context switching reduces loss of working memory. | Recent work and attention items support return without making a task manager. |
| Recovery / human intervention | Relevance AI | Codex/Cursor | Approval, escalation, take-over, and continuation are explicit. | Needs CEO / failed / retry / recovery states with owner and next action. |

## 9. Directly reusable patterns

- A thread/session is a durable work object, not a disposable chat message.
- Separate worktree or isolated execution is the safety boundary for parallel agent work.
- Plan, permission, and review are run contracts visible at the point of consequence.
- File, diff, terminal, test, PR, and preview are professional utility objects, not paragraphs inside Conversation.
- Automatic context gathering and explicit file/folder references should coexist.
- Long-running work needs status, follow-up, takeover, and a return path.
- Search, recent, status, and breadcrumb-like orientation lower context-switching cost.
- Agent-to-agent handoff must identify the sender, receiver, responsibility, context package, and acceptance state.

## 10. Curis-specific additions

- Employee identity, role, responsibility, and reporting context remain visible around provider-native work interaction.
- Employee Workstations expand for `working` and `needs_ceo`; `idle`, `waiting`, and `completed` collapse while retaining a resumable summary.
- CEO intervention returns to the same session and responsibility, not a new generic conversation.
- Handoff is a business responsibility transition, not merely a tool call or workflow edge.
- Technical result must return as Result / Evidence / Review / Learning to the Workspace and CEO Operating Day.
- Recovery includes owner, blocked stage, reason, safe next action, and return stage.

## 11. Do not copy

- Do not copy a provider’s visual chrome before confirming the actual current interaction.
- Do not put Code, Diff, Preview, Terminal, or Test inside Conversation message bodies.
- Do not make each employee a top-level tab or put employees in the Context Sidebar.
- Do not expose a DAG as the ordinary CEO representation of multi-agent work.
- Do not add Git, PR, Browser, Voice, Goal, or Plugin buttons without a connected object and user need.
- Do not call a local prototype, documentation page, or candidate build a completed Curis capability.
- Do not treat Relevance AI’s Workforce Builder as the Curis end-user Workspace; it is evidence for status, handoff, approval, and monitoring only.

## 12. Review questions before design

1. Which provider-native interaction will be embedded first for the developer employee?
2. What is the minimum connected repository/worktree contract for Git surfaces?
3. Which utility surfaces need simultaneous view, and which must remain focus-switched?
4. What exact evidence makes a handoff accepted rather than merely sent?
5. Which CEO decisions interrupt execution, and which are safe for the employee to continue?
6. Which current Codex Desktop and Cursor/Claude GUI details require a fresh direct capture before UI design?

## 13. Sources

Official sources used:

- OpenAI, Introducing the Codex app: https://openai.com/index/introducing-the-codex-app/
- OpenAI, Introducing Codex: https://openai.com/index/introducing-codex/
- Anthropic, Claude Code common workflows: https://code.claude.com/docs/en/common-workflows
- Anthropic, Claude Code CLI reference: https://docs.anthropic.com/en/docs/claude-code/cli-usage
- Anthropic, Create custom subagents: https://code.claude.com/docs/en/sub-agents
- Cursor, Agent modes: https://docs.cursor.com/agent
- Cursor, Working with context: https://docs.cursor.com/en/guides/working-with-context
- Cursor, Agent tools: https://docs.cursor.com/en/agent/tools
- Cursor, Background agents: https://docs.cursor.com/background-agent
- Cursor, Web and mobile handoff: https://docs.cursor.com/en/background-agent/web-and-mobile
- VS Code, Source Control quickstart: https://code.visualstudio.com/docs/sourcecontrol/quickstart
- VS Code, GitHub integration and pull requests: https://code.visualstudio.com/docs/sourcecontrol/github
- VS Code, Branches and worktrees: https://code.visualstudio.com/docs/sourcecontrol/branches-worktrees
- Linear, Search: https://linear.app/docs/search
- Linear, Project overview: https://linear.app/docs/project-overview
- Linear, Project status: https://linear.app/docs/project-status
- Linear, Assign and delegate issues: https://linear.app/docs/assigning-issues
- Relevance AI, Workforces: https://relevanceai.com/docs/get-started/core-concepts/workforces
- Relevance AI, Agent-to-agent configuration: https://relevanceai.com/docs/build/workforces/workforce-features/agent-to-agent-configuration
- Relevance AI, Approvals and escalations: https://relevanceai.com/docs/build/workforces/workforce-features/approvals-and-escalations
- Relevance AI, Workforce Task View: https://relevanceai.com/docs/build/workforces/workforce-features/workforce-task-view

Curis authority inputs read:

- `/Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md`
- `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Context.md`
- `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Master_Map.md`
- `/Users/yy/Documents/Curis AI Workspace/docs/01_Product/Curis_Product_Page_Map_v1.0.md`

## 15. Final synthesis scope

### DESIGN NOW

- Workspace foundation;
- multiple vertical Employee Workstations;
- Employee identity, Role, Provider/Agent, Status, Current Work, Collapse/Expand;
- default expanded/collapsed behavior;
- provider-native Agent Conversation;
- compact Composer with natural-language input, `+`, Mode, Model, Send/Stop;
- automatic Handoff and Needs CEO state;
- minimal Context Sidebar;
- on-demand Utility Surface;
- Code/Source, Diff/Changes, Preview/Result.

### RESERVED

- Test;
- Terminal;
- Git, Branch, Worktree;
- Review;
- External Editor;
- Session History;
- detailed Permission surfaces;
- Background Work.

### LATER

- Commit / Push / PR flow;
- Debug and Problems;
- Scheduled Work;
- Autopilot;
- Voice;
- multiple utilities shown simultaneously;
- advanced IDE capabilities.

### DO NOT COPY

- Employee top tabs, contact lists, or employee placement in Context Sidebar;
- DAG as the ordinary user representation;
- permanent tool wall;
- all capabilities expanded at once;
- Session Manager as the first-screen interaction;
- buttons added for professional appearance;
- a full Codex, Cursor, or VS Code clone.

Final research status: `READY FOR DESIGN REVIEW`.

## 14. Phase 2 direct walkthrough evidence

This section extends the previous research. It does not replace the official-source matrix above and does not claim that an unavailable product was inspected.

### 14.1 Local product availability

| Product | Direct walkthrough result | Classification |
|---|---|---|
| Codex Desktop | `com.openai.codex` produced no readable accessibility tree or usable product surface in the current desktop session. | UNVERIFIED; no Composer or Utility Surface claims promoted |
| Cursor | No Cursor application bundle was found under `/Applications`; no direct local walkthrough was possible. | NOT FOUND locally |
| VS Code | Running `/Applications/Visual Studio Code.app`; Curis AI Workspace opened; visual screenshot and accessibility tree captured. | CONFIRMED local UI |
| Claude Code | No direct CLI/desktop walkthrough in this phase, per scope; prior official documentation remains the reference. | NOT RUN in Phase 2 |
| Linear / Relevance AI / EvoFlow | No repeat walkthrough; prior conclusions retained. | OUT OF SCOPE for this phase |

### 14.2 VS Code direct capture: real objects and spatial behavior

The local VS Code surface is not a single chat panel. It exposes a source workspace and a separate Agent chat surface at the same time.

| Observed object | Direct evidence | Interaction implication |
|---|---|---|
| Project / workspace | Explorer shows `CURIS AI WORKSPACE`, a full folder tree, and a Git status entry in the bottom bar. | The codebase is a persistent spatial anchor; the agent does not replace the workspace. |
| Agent conversation | Auxiliary sidebar contains `会话`, refresh, search, filter, show-session-sidebar, new chat, and a chat composer. | Sessions are browseable objects; the active conversation is not the entire navigation model. |
| Composer | Placeholder is `描述要构建的内容`; send is disabled until input; controls sit immediately below the input. | Keep input dominant and make execution controls adjacent, not scattered across the page. |
| Add context | Menu shows files/folders, MCP resources, screenshot window, command, Source Control, Problems, symbols, sessions, and tools. | Many context types can stay hidden behind one disclosure without reducing capability. |
| Agent mode | Picker shows Agent, Ask, Plan, and Configure custom agents. Agent edits, Ask answers without changes, Plan researches/outlines. | Mode is a run contract, not a decorative filter. Read-only and planning are explicit safe states. |
| Model | Composer exposes `Models, Auto`. | Model selection can be compact and adjacent to the composer; exact model list is not required in the default state. |
| Tool configuration | Composer has `配置工具...`. | Tool selection is a secondary execution configuration, not a primary navigation item. |
| Session target | Composer exposes `本地`. | Execution target is visible but compact; target is distinct from model and permission. |
| Permission | Picker shows `默认审批`, `绕过审批`, `Autopilot (预览版)`; default also exposes terminal sandbox checkbox. | Permission deserves its own control and should explain autonomy and sandbox consequences. |
| Source Control | Activity bar has Source Control with `10K` pending changes; bottom status shows `main*` and `发布分支`. | Git state is always nearby in an IDE, but large dirty state can degrade the surface; Curis must not turn a dirty repository into a generic status badge. |
| Tests / Problems | Activity bar exposes Tests; Problems status shows zero issues. | Test and problem surfaces are sibling professional utilities, not chat message types. |
| Layout | Explorer is the primary left surface; Agent chat is the auxiliary right surface; editor remains central. | The chat and code workspace coexist. Curis should preserve this separation conceptually even if its final layout differs. |

### 14.3 What the capture changes

The prior synthesis already said “compact composer with attached context and run contract.” The direct capture makes that contract more specific:

- One `+ / 添加上下文` disclosure is sufficient for a large context vocabulary.
- Plan and Ask should be first-class safe modes; they should not be hidden as vague status labels.
- Model, tools, target, and permission are separate controls because they change different execution dimensions.
- Session search/filter and new chat belong near the session list, not in the global primary navigation.
- Source Control, Tests, Problems, and Explorer remain professional surfaces adjacent to the agent, not content inside the conversation.
- A large repository warning is part of product truth: the UI must be able to say that a surface is degraded or partially enabled.

### 14.4 Scope reduction for Curis first frontend reference

For the first design exploration, retain only the smallest set that has a clear user need and direct reference support:

1. Employee Workstation Conversation.
2. One collapsed/expandable context disclosure for Workspace, responsibility, related source, and recent object.
3. One compact mode selector for direct execution, planning, and questions.
4. Compact model control; permission appears only when needed.
5. Continue the current responsibility-owned session automatically; do not expose Session Management in P0.
6. Utility entry points for Code/Source, Diff/Changes, and Preview/Result; Test Result only when needed to understand the result.
7. Status states: working, waiting, needs CEO, failed, completed.

Defer until direct provider evidence or a real Curis Runtime contract exists:

- Terminal, Problems, and full Test tooling;
- Browser / Preview beyond the minimal Preview/Result surface;
- Commit / Push / PR orchestration;
- Worktree management UI;
- Scheduled/background work UI;
- Plugin marketplace or broad skill browser;
- Autopilot-like autonomous mode;
- Voice controls;
- multi-pane simultaneous utility composition.

This is scope reduction, not a rejection of future capability. The key extensibility rule is to keep the context disclosure, mode picker, permission control, session model, and utility-surface return anchor extensible without making every future capability visible now.

### 14.5 Visual capture record

- VS Code welcome/workspace screenshot captured through Computer Use after opening `Curis AI Workspace`.
- VS Code Agent composer screenshot/state captured with the Add Context menu open.
- VS Code Agent mode picker screenshot/state captured with Agent / Ask / Plan visible.
- VS Code permission picker screenshot/state captured with Default Approval / Bypass Approval / Autopilot and terminal sandbox visible.
- Codex Desktop and Cursor visual captures: NOT AVAILABLE because Codex had no readable surface and Cursor was not installed locally.
