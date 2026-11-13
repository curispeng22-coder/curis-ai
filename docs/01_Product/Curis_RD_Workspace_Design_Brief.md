# Curis RD Workspace Design Brief

Status: Review

Review state: READY FOR DESIGN REVIEW

Document type: Design-AI input derived from reference research

Research date: 2026-08-14, Phase 2 direct walkthrough update

This brief is not a Blueprint and does not authorize UI implementation. It defines what a future design exploration must preserve from the reference synthesis.

## FINAL SCOPE SUMMARY

### DESIGN NOW

- Workspace foundation;
- multiple vertical Employee Workstations;
- Employee Identity, Role, Provider/Agent, Status, Current Work, Collapse/Expand;
- provider-native Agent Conversation;
- compact Composer: natural-language input, `+`, Mode, Model, Send/Stop;
- automatic Handoff and Needs CEO;
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

- Employee top tabs;
- Employees in the Context Sidebar;
- DAG as the ordinary user representation;
- permanent tool walls;
- every capability expanded at once;
- Session Manager as the first-screen interaction;
- buttons added for professional appearance;
- a full Codex / Cursor / VS Code clone.

## 1. Page goal

Help a CEO supervise real software development carried by multiple AI Employees while keeping each responsibility, session, technical evidence, handoff, and decision recoverable.

The page must make three things immediately clear:

1. what development responsibility is active;
2. which Employee owns the next action;
3. whether the CEO needs to decide, inspect, or simply let work continue.

The page is a professional R&D Workspace with an employee-facing workstation layer. It is not a chatbot home, generic task board, workflow-DAG editor, or technical control panel.

## 2. Information hierarchy

1. Workspace identity and current development responsibility.
2. Employee Workstations and their status / ownership.
3. Active Conversation for the expanded employee.
4. Current execution state and CEO attention.
5. Minimal Context Sidebar: current Workspace, responsibility, related files/directories, recent object.
6. Developer Utility Surface: Code/Source, Diff/Changes, Preview/Result; Test Result only when needed to understand the result.
7. Durable Result / Evidence / Review / Learning.

Technical objects must be visible when useful, but never displace ownership, current work, or the next action.

## 3. Spatial structure

Use three independently understandable surfaces:

- Main Workspace: Employee Workstations and the active employee Conversation.
- Context Sidebar: current Workspace, responsibility, related files/directories, and recent object. It is collapsible. It is not a Session Manager, employee directory, permission center, or tool catalog.
- Utility Surface: a focus-switched professional area for source, Diff, Terminal, Test, Preview, Git, PR, or Review. It can open beside or over the main conversation and must preserve the owning Workstation.

Do not make the Utility Surface a permanently open right rail. Do not make Employee Workstations a navigation sidebar or top-level tabs.

## 4. Employee Workstation behavior

Each Workstation shows:

- Employee identity
- Role
- Responsibility
- Current work summary
- Status
- Handoff source/receiver when relevant
- Last result or blocker
- Collapse / expand control

State behavior:

| State | Default behavior |
|---|---|
| Working | Expanded when it is the active owner; compact summary when another employee is active. |
| Needs CEO | Expanded and surfaced as an attention item with the exact decision needed. |
| Waiting | Collapsed with reason, waiting-on, and resume condition. |
| Completed | Collapsed with result, evidence, and next handoff. |
| Failed | Expanded or prominently surfaced with failure stage, owner, recovery action, and retry boundary. |
| Idle | Collapsed; retains a resumable summary. |

Expanding a Workstation opens its actual Agent Conversation. It must not create a new thread unless the user explicitly starts a new responsibility.

## 5. Composer

The composer belongs to the active Workstation Conversation. It needs:

- natural-language input;
- current Workspace and responsibility shown as inherited context;
- add source/file/folder/image context;
- plan versus run;
- model/reasoning control when it changes the run contract;
- skill/tool availability only when it affects this run;
- permission mode at the point of consequence;
- send, stop, and safe follow-up.

The default composer should be calm and small. Its visible controls are natural-language input, `+`, one compact Mode selector, Model, Send, and Stop. The `+` menu aggregates files, folders, images, materials/context, and low-frequency capabilities. Permission appears only when an action requires it; it is not a permanent composer button. Context should be automatic where safe and surgical where precision matters.

## 6. Context Sidebar

The sidebar should answer “what Workspace context must remain visible while this responsibility continues?” It may contain only:

- current project / Workspace;
- current work / responsibility;
- relevant files and directories;
- recent work / recent object.

It must not become a second employee directory, Session Manager, Git dashboard, permission center, handoff queue, result-detail panel, or permanent tool catalog.

## 7. Developer Utility Surface

The future Utility Surface can support:

- Source / file tree and Code;
- Diff / Changes;
- Preview / Result;
- Test Result when it is necessary to understand the result.

Terminal, Problems, full Test tooling, Git, Branch, Worktree, Commit, Push, PR, Review, Debug, and External Editor remain Reserved/Later surfaces.

Every utility must show its owning responsibility and provide a return action to the Conversation anchor. Opening a utility must not erase the Conversation, reset the employee, or silently change the worktree.

Git surfaces appear only for a real repository/worktree. Commit, push, and PR require connected provider state, permission, and evidence. If unavailable, show the blocked stage and recovery path rather than a disabled-looking decorative button.

## 8. Automatic handoff

Handoff is a visible business event with:

- sending Employee;
- receiving Employee;
- responsibility being transferred;
- context package;
- acceptance state;
- pending questions;
- expected result;
- return / escalation path.

The sender may collapse after a handoff is accepted. The receiver expands. If the receiver rejects or lacks context, the handoff returns to the sender or surfaces as Needs CEO. The page must show the chain without exposing a DAG.

## 9. Parallel employees

Parallel work is represented as multiple responsibility Workstations under one R&D goal. Each has its own status, owner, current continuous session, source scope, and result. The user can switch focus without exposing Session Management or losing the other responsibilities.

Do not represent parallel employees as top tabs, an undifferentiated group chat, or a node graph. The CEO needs ownership and progress, not orchestration topology.

## 10. Needs CEO

Needs CEO is a first-class state, not a toast. It must show:

- the decision or input needed;
- why the Employee cannot continue safely;
- the affected responsibility and external impact;
- supporting evidence;
- approve / reject / answer / take over / return choices;
- what resumes after the decision.

After the CEO acts, the same Workstation and session continue whenever safe. Create a new conversation only when the responsibility genuinely changes.

## 11. Failure and recovery

Failure states must identify:

- failed stage;
- Employee and tool responsible;
- reproducible evidence;
- whether the failure is retryable;
- safe retry scope;
- recovery owner;
- CEO decision requirement;
- return stage.

Recovery should be a continuation of the same responsibility, not an empty-state reset. Preserve prior commands, tests, diffs, and handoff context.

## 12. Git, Review, Test, and Result

The minimum credible delivery sequence is:

`worktree / branch → change → test → review → commit → push or PR → CEO result review`.

Design must show the relationship among these objects. A “Git” button without a repository, branch, or next action is prohibited. Review must be able to return an actionable comment to the responsible Employee. Test output must be evidence linked to the change, not just a green badge.

The final result is business-readable first, with technical evidence available beneath it:

- what was changed;
- why it satisfies the responsibility;
- tests and runtime checks;
- unresolved risk;
- branch/commit/PR state;
- next owner or CEO decision;
- reusable learning.

## 13. Reference product mapping

| Design concern | Primary reference | Secondary reference | Boundary |
|---|---|---|---|
| Conversation/session | Codex | Claude Code | Preserve thread continuity and return. |
| Composer/context | Cursor | Claude Code | Adopt automatic plus surgical context; verify exact visual controls before design. |
| Source/editor/utility surfaces | VS Code | Cursor | Keep professional tools out of message bodies. |
| Diff/review | Codex | VS Code/GitHub | Anchor to responsibility and evidence. |
| Git/worktree/PR | VS Code/GitHub | Codex | Only show connected real operations. |
| Search/recent/status | Linear | Codex | Low-noise context switching only; do not copy its issue model. |
| Multi-agent state/handoff | Relevance AI | Claude Code | Use statuses, approvals, escalation, and summaries; do not copy the builder/DAG. |
| Long-running/background | Codex | Cursor | Show progress, follow-up, takeover, and return. |
| Employee identity/responsibility | Curis | — | Curis-specific organizational layer. |

## 14. Prohibited design errors

- Chat UI with fake developer labels and no source, diff, test, or Git object.
- Employee top tabs or employees placed in Context Sidebar.
- Code, Diff, Preview, Terminal, or Test embedded as long Conversation prose.
- Permanent Utility Surface that makes every tool visible at once.
- Generic “running” status without current step, owner, wait reason, or next action.
- DAG canvas as the CEO’s normal view of multi-agent work.
- Git actions without repository/worktree/provider truth.
- A completed badge without result, evidence, review, or return path.
- Provider-specific UI copied from memory or a stale screenshot.
- Adding Goal, Plan, Skill, Plugin, Browser, Voice, or model controls solely to look professional.

## 15. Design gate

Before any UI design or implementation, confirm:

1. the provider interaction to reuse is directly captured or officially documented;
2. the active responsibility and employee ownership are visible;
3. every utility surface has an entry, return, and persistence contract;
4. handoff, Needs CEO, failure, and recovery are represented;
5. Git/test/review claims are connected to real objects;
6. the design does not turn Curis into a generic AI chat shell or workflow builder.

Final status: `READY FOR DESIGN REVIEW`.

## 16. Phase 2 design constraints from direct walkthrough

The following constraints come from direct VS Code observation and narrow the first design exploration. They are reference constraints, not a final Curis UI.

### Keep

- A persistent Workspace / repository surface beside the Agent conversation.
- One context disclosure that can contain files, folders, screenshots, commands, source-control state, problems, symbols, sessions, and tools.
- Separate mode choices for editing, read-only investigation, and plan-before-edit.
- Compact model, target, tool, and permission controls directly attached to the composer.
- Continue the current responsibility-owned session automatically; Session list management is Reserved/Later.
- Professional utilities as sibling surfaces: Code/Source, Diff/Changes, Preview/Result; Test Result only when needed.
- A visible degraded-state message when repository scale or missing access limits functionality.

### Reduce

- First reference design should not expose every future Skill, Plugin, Browser, Preview, PR, Worktree, Schedule, or Voice action.
- Do not create a permanent utility wall; open utilities from a concrete result or need and preserve the Conversation anchor.
- Do not combine model, permission, target, and mode into one ambiguous “settings” menu; they change different execution contracts.
- Do not treat `Autopilot` as a default pattern. It is a preview autonomy mode in the observed VS Code surface and requires a future Curis safety contract.

### Directly verified versus pending

| Area | Phase 2 result |
|---|---|
| VS Code source / explorer / chat coexistence | CONFIRMED by local screenshot and accessibility tree |
| VS Code context disclosure | CONFIRMED: files/folders, MCP, screenshot, command, Source Control, Problems, symbols, sessions, tools |
| VS Code Agent / Ask / Plan | CONFIRMED by local mode picker |
| VS Code model / target / permission controls | CONFIRMED by local composer |
| Codex Desktop Composer and Utility Surface | UNVERIFIED; no readable local surface |
| Cursor Composer and IDE utility behavior | NOT FOUND locally; no direct capture |
| Final Curis layout | Not designed in this phase |

### First-design reference boundary

The minimum future design surface is: one Employee Workstation, one Conversation, one minimal context disclosure, one mode picker, compact model control, on-demand permission, and result-triggered Code/Diff/Preview utilities. The responsibility-owned session remains continuous but is not exposed as a Session Manager. Everything else remains an extensibility slot or a later evidence gate.
