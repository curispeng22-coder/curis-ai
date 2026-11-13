# Curis V1 Shared Employee Interaction — Candidate

Status: Review
Authority Class: RESEARCH / DECISION EVIDENCE
Disposition: ACCEPTED / RECONCILED — NOT A SECOND AUTHORITY / NOT RUNTIME ACCEPTANCE
Owner: Main Development research; decision owner CEO / Product
Source: CEO 2026-09-23 bounded reconciliation request; Current Required Input and three current HTML explorations below
Target Authority: consumed by Current Blueprint / Master Map / UI Blueprint / Shared Shell §3.1A on 2026-09-23
Next Action: stop exploration; Business owners consume Current Authority for bounded reconciliation
Next Gate: Business reconciliation evidence → CEO V1 Product Freeze readiness review

## Accepted disposition — 2026-09-23

CEO Final Review接受总体Grammar与Writing三态。唯一后续实施依据是[Blueprint](../../01_Product/Curis_Product_Blueprint.html#shared-employee-interaction-20260923) → Master Map / UI Blueprint → [Shell §3.1A](../../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md)。下文保留研究/验证provenance，旧“待CEO接受/NOT FROZEN”指研究文件或此前checkpoint，不表示已吸收的共享合同仍未接受。HTML不继续修改，能力/Runtime open questions仍须真实验证；本文不独立规定Current产品。

## 1. Finding and scope

Shared is **who owns this work, what this message refers to, what happened, what returned, and what my choice changes**. Shared is not an identical right-hand chat box, a fixed execution sequence, or a new status machine.

Read-only inputs:

- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`, Current Required Input → `Curis_Product_Blueprint.html`, `Curis_Product_Master_Map.md`, `Curis_Product_UI_Blueprint.html`: current Company/Employee/Conversation/scope and Main/Utility boundaries.
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §0.1, §3.1, §3.4–3.5, §3.8–3.12: Frozen shared semantics. Current accepted three-state Employee projection is retained.
- `CONTENT_GROWTH_CODEX_HTML_EXPLORATION/{index.html,app.js,data.js,styles.css}`: current Codex re-expression, RESEARCH / Review; W-202 / w2, 高戈, 徐白, Script v3. Existing chat drawer records advice separately from the revision button; this is the specific interaction gap, not a reason to reopen the business.
- `WRITING_BUSINESS_HTML_EXPLORATION/{index.html,views-book.js,app.js,data.js,styles.css}` and `CURIS_WRITING_HTML_EXPLORATION_CLOSURE.md`: CEO-accepted exploration, still Candidate. 《夜行灯》 / Chapter 43; 沈知远 and independent reviewer 许清禾. Existing selection/discuss and draft/formal/published snapshots are useful; contradictory old candidate hint saying “合入” directly creates formal must not become shared grammar.
- `MUSIC_BUSINESS_CODEX_HTML_EXPLORATION/{index.html,app.js,team.js,model.js,styles.css}` and `CURIS_MUSIC_HTML_EXPLORATION_CLOSURE.md`: CEO-accepted exploration, still Candidate. 《夜行线》, 林音, Candidate B; existing Song conversation is already Main-local and separate from details. Local audio is synthetic instrumental illustration, not generated vocals or quality proof.
- Runtime read only: `backend/app/conversation_service.py` owner/context/references/prepare; `runtime/responsibility_routing.py` begin/finish/review/consult; `frontend/components/v1/SharedConversation.js` and `EmployeeConversation.js`. Existing stable conversations, scoped references, executor clearing and failure language are reusable. **Cross-domain character/time/shot Selection anchoring is not proved by these implementations.** No import, DB connection, provider call or test run against Runtime in this research.

Current accepted HTML direction is the visual input, not production truth. Original business files remain unchanged. V1 scope here is Content Growth / Writing / Music; no RD or E-commerce work. No Current/Frozen document is patched by this Candidate.

## 2. Shared Interaction Grammar

`Current object + version → responsible Assignment/Employee → bounded message + explicit references → discussion / proposed action → authorized execution (if any) → result reference + domain candidate → domain review / human choice → explicit scoped state change → continue in the same context`.

Not every message executes, not every result needs a choice, and not every choice creates new Work. “解释这里” can end in a reply/finding. “改这里” requires a bounded affected object and preserved base version. Existing authorization, capability, cost and external-action gates apply; Send is not consent to publish, spend beyond scope or transfer responsibility. No routine creative choice is automatically P7.

Shared invariants:

1. Object Owner ≠ Responsibility Holder ≠ Current Executor. Holder remains during waiting/review; no active execution means no “正在工作” animation.
2. Employee identity is canonical and Company-owned; current Assignment supplies responsibility/scope. Changing tabs/chapters does not clone Employee or rewrite old message context.
3. Same Conversation can continue across lawful contexts; each new send validates current Assignment and selected refs. It does not inherit unlimited historical access. Recipient change is explicit; cannot have Assistant secretly reply as Employee.
4. Result/candidate is a reference to its real producer, source Work and version. Chat never becomes the only copy of the artifact.
5. Accept/Reject/Revise names the exact version and effect. No automatic overwrite, no silent “latest” rebinding, no completion from view exposure.

## 3. Presence: lightweight Employee Bar — CEO targeted revision

Immediately below the professional object title/status, keep a lightweight **Employee Bar: avatar + name + current responsibility + one meaningful status if needed + 一起讨论**. It remains present when discussion is closed; never a large profile card. Conversation is **entirely hidden by default**, consuming no space. 一起讨论 expands an optional Main.WorkArea directly below the bar and above the professional surface; 收起讨论 hides the entire WorkArea without losing Employee presence, messages, pending input or selected context. No permanent right drawer or floating Employee chat. No important activity → responsibility alone is sufficient; do not continuously display 空闲 · 无进行中执行.

Do not show employee inventory, online dots, provider sessions, agent graph or every collaborator. Supporting/review contributions appear by the result they authored. No current Holder → “尚未安排负责人” with a legal assignment route, not a fictional named employee. If System Activity alone runs, use its own label, not an Employee avatar.

## 4. Shared Composer / Context / Selection

|Slot|Shared behavior|Boundary|
|---|---|---|
|Text|Plain request; preserve on failure; recipient visible before Send|Not a prompt/configuration form|
|Current Context|Readable object + version, e.g. 夜行灯 / 第43章 / 草稿r3|Scope enforced, not a removable permission grant; changing object is explicit|
|Selection|Visible chip: object/version + paragraph/shot/time + short quote; locate, remove, replace|Removing selection means whole current object, not whole Workspace; removing a chip does not delete source|
|Reference / Add|Choose legal Work/Result/Evidence/Artifact/Knowledge reference, provenance stays attached|No automatic all-history hydration; unsupported sources remain disabled|
|Attachment|Only if real ingest/type/size/scope/capability available; upload failure keeps text|This prototype disables it; a filename is not usable content or authorization|
|Target Employee|Current responsible Employee default; explicit Reviewer/support target when relevant|Changing target does not transfer Holder or create a new identity|
|Access / Mode / Execution|Keep existing explicit semantic slots, distinguish Model from Agent and requested/configured/effective|No fake enabled model, mode, tool or Full Access; exploration labels execution disconnected|
|Send|One message/action attempt; show acknowledged/working only from real evidence; retry bounded and idempotent|HTML uses explicitly labeled demonstration controls, never claims a real Employee ran|

Selection payload is **a candidate interaction contract**, not an authorized new schema: existing object ref, immutable base version, typed locator, short excerpt, return anchor, scope/permission. Writing uses paragraph + char range + excerpt; CG script paragraph/shot; Music candidate identity + seconds range. Audio time cannot be assumed to align across candidates, nor text offsets across revisions. If base changes before send/apply: preserve input, show stale reference, require re-selection/recomparison. Already sent references remain historical. No silent fuzzy remap.

Clicking a passage/shot or “引用选段” brings its visible chip into Composer without retyping Book/Song/account context. A later click replaces only the pending selection, never a sent message. Whole-object context remains visible when selection removed. Details/evidence can be inspected and returned from without changing draft or target.

## 5. Conversation vs Main vs Utility

- Conversation = clarification, reasoning, questions, bounded progress, result references. It is an optional Main.WorkArea immediately below the Employee Bar, **default collapsed, expand on demand**. Selecting a passage and choosing 讨论这段 / 要求修改 opens it with object, version, selection and excerpt/locator. Result return does not require it to stay open; user can collapse and compare/review/choose in Main. No permanent chat-only Utility.
- Professional Main = editable/inspectable script, manuscript/diff, candidate audio/lyrics; candidate appears here with its own identity and human actions. It remains useful with Conversation closed.
- P6 Result reference still opens an auxiliary Utility inspection of the same result; “回到工作面比较/处理” restores the exact object/version/anchor in Main. This reconciles result-return with Frozen P6, rather than changing every reference click to a new route.
- Employee detail / evidence / provenance = Utility. Comparison/editor can expand in Main; full creative operation is not hidden in a side inspector.
- Global CEO Assistant coordinates Company intent and escalation, not the responsible professional Employee or its conversation. Keep its lightweight floating entry independent; reduce its visual prominence during Employee discussion, never present two competing full composers. The standalone Writing page represents this boundary with a collapsed Company-coordinator entry and explicit exploration-only explanation, not a functional second chat.

## 6. State mapping — retain existing three-state Employee projection

|Fact / source|Employee line|Work/result line and next action|
|---|---|---|
|Verified active execution + actual executor|工作中 · actual activity|处理中; owner can differ from executing reviewer|
|No current execution, Holder exists|Responsibility only, or 当前章节可继续修改; omit Idle label|Current Work remains visible; not “completed Employee”|
|Explicit missing user fact / material|缺少 / 等你补充 the precise fact|Exact missing fact / reason / recovery; keep Holder, executor none|
|Failed attempt / capability missing|阻塞 · confirmed cause, not fabricated enum|本次未完成; retained input, result/evidence if any; repair then bounded retry|
|Result exists, executor ended|有结果可查看 / 等你确认, explicitly this Work's fact|候选可查看 / 等你选择 attached to this Work/version; no claim of ongoing execution|
|Restart or lost connection with no liveness proof|Do not claim 工作中|上次进展尚未确认; query/reconcile, no automatic duplicate attempt|
|No responsibility holder|No invented Employee presence|尚未安排负责人; assignment gap|

Thus proposed Idle/Working/Waiting-for-you/Blocked/Result-ready **is not a new five-state Employee enum**. Waiting and Result-ready belong to Work/Need/Result. Product state is a read projection of actual facts, not a new execution truth. Current code clears currentExecutorRef when finishing an attempt; WAITING alone cannot prove “waiting for CEO”.

## 7. Result / Candidate / Finding / Recommendation / Decision

Result is delivered output with provenance, not automatically accepted/effective. Candidate is a domain proposal/alternative requiring evaluation before promotion. Finding is a scoped observation with evidence/limitations. Recommendation suggests action, not approval. Decision Request is only for an actual authorization/operating decision under existing P7.

|Action|Shared effect|Must not imply|
|---|---|---|
|Preview / Compare / Audition|Read exact versions; can set UI focus|Result Acceptance, Master, published, task completed|
|Accept|Apply explicitly named domain transition with basis/version check|One universal “ACCEPTED” state across all business objects|
|Reject|Retain candidate/history and reason; base unchanged|Delete Work/history or dismiss all future attention|
|Revise|Keep prior candidate, prepare bounded next request with refs|Overwrite formal artifact or silently re-run external action|
|Continue|Continue the lawful existing work/context, revalidate after changes|Automatic next Cycle / unlimited execution|

Viewed ≠ Accepted. A real explicit successful Result open may use the existing Viewed Receipt; this static exploration does not write that receipt. Creative choice ≠ Handoff ≠ P7; publishing/license/payment changes use their actual gates.

## 8. Multi-Employee

One visible accountable Holder for the current responsibility; show a supporting Employee/reviewer when their contribution matters. Requesting review retains the writer/producer Holder. The reviewer returns Finding + reviewed version/basis; a later edit invalidates that review's applicability, not its history. Only real responsibility transfer uses Handoff/ACK. No user-facing Agent Manager, forced DAG or fabricated “team is busy” row. In the demonstration, choosing the reviewer only changes the addressed participant; it never changes the Holder.

## 9. Three-business translation / counterexamples

|Grammar|Content Growth production|Writing Chapter|Music Song|
|---|---|---|---|
|Object/context|w2 / target account / Script v3 / paragraph|夜行灯 ch43 / draft r3 / paragraph; formal v2 and online v2 independent|夜行线 / Direction v1 / Candidate B / time range|
|Responsibility|高戈 owns production; 徐白 contributes script review|沈知远 owns revision; 许清禾 independently reviews|林音 owns production; relevant research/rights support only when needed|
|Request|缩短开头，保留任务清单|冲突太突然，保留人物未知信息|这里再克制一点，保留呼吸感|
|Return|Script revision v4 with preserved v3|Revision candidate → adopted draft r4 → review of r4|Independent Candidate C with source B; no sample-accurate edit promise|
|Human choice|Compare/review → adopt Script v4; rendered video still needs its own verification|Select changes → merge draft → independent review → author confirms formal v3|Audition/compare → select candidate → explicitly confirm Master|
|Never implied|Script approved ≠ footage/rights/audio/video verified ≠ published|Merged draft ≠ formal manuscript ≠ online chapter|Selection ≠ Master ≠ Published; instrumental sample ≠ sung lyrics|

Counterexamples change the shared rule, not the business: (1) Writing acceptance is staged, not direct formal overwrite. (2) Music time range describes intent, not provider support for precise in-place editing. (3) CG script acceptance cannot clear appearance/voice rights or accept a rendered video. (4) Review returns information without Handoff. (5) Author writes directly without AI: same version/review rules, no compulsory Employee execution.

## 10. Open questions / exact future gaps

1. CEO to accept the shared **interaction grammar**, not freeze three layouts or a new state schema.
2. Implementation owners must map paragraph/shot/time anchors into existing reference vocabulary, with stale/version authorization checks. Current generic reference support alone does not prove selection transport or provider understanding.
3. Exact domain acceptance policy (which findings block, partial adoption, rights prerequisite, version conflict) stays with each accepted Business contract. Do not implement universal gating logic here.
4. Model/Agent ability to inspect shots/audio, revise locally, preserve timestamps or understand selected text: UNKNOWN until capability evidence; all demonstrated employee responses/candidates are labeled fixtures.
5. Participant/context switching draft behavior: proposed preserve text and require visible context reconfirmation. No cross-Company data grants. Validate real persistence/concurrency separately after product acceptance.

## 11. Exploration evidence / Product Findings

### CEO targeted revision — current Writing proof

Overall grammar accepted; this revision remains Review / NOT FROZEN. Only `writing.html` was adapted; shared JS/CSS, Content Growth and Music pages/screenshots were not regenerated or modified. Their older expanded-conversation captures below are historical first-pass evidence, not the revised default-layout contract.

Writing now has a persistent lightweight Employee Bar, default-hidden discussion immediately below it, contextual expansion, and full collapse retaining input/messages/selection/results. Reviewer appears in the actual review result, not the default Employee Bar. Meaningful work wording replaces permanent Idle text. The independent CEO Assistant launcher is visually subdued while discussing; this standalone page only demonstrates its separate Company-coordinator identity, not real Assistant execution.

**21 targeted browser checks PASS; console/page errors = 0.** Evidence: `CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/writing-revision-checks.json`. Includes default invisibility, contextual opening, object/version/selection, collapse/reopen retaining input, returned candidate in Main, same Holder, review/author confirmation and independent Assistant boundary.

- [State A — Default](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/writing-revision-A-default.png)
- [State B — Contextual Discussion](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/writing-revision-B-discussion.png)
- [State C — Result Returned / Discussion Collapsed](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/writing-revision-C-result-collapsed.png)

### Prior three-domain proof (before targeted layout revision)

Entry: `CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/index.html`; three representative pages only. Status: Review; Disposition: READY FOR CEO REVIEW, not Frozen. Owner: shared interaction research; next gate: CEO accepts/revises grammar before domain owners change original explorations. No Current Authority / Pointer update: this remains an independent research candidate.

Browser verification: Chrome through Playwright, 1440×1100 viewport, **73 checks PASS; console/page errors = 0; external requests = 0**. Runnable check: `CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/check.cjs`; machine evidence: `evidence/checks.json`. Covers selection/removal, references, bounded request, duplicate send guard during simulated working, result return, reference inspection/return, reviewer retaining holder, human choice, missing facts, failed input preservation, retry, stale candidate/selection rejection, reload reset and horizontal overflow. Music additionally plays the existing local C audio sample; this proves local playback only. JavaScript syntax check passed. These are HTML interaction checks, **not Runtime, persistence or provider acceptance**.

Screenshots (under the exploration directory, full-page PNG):

|Workspace|Selected context / Composer|Result / human choice|
|---|---|---|
|Content Growth|[Selection](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/content-01-selection.png)|[Script candidate / review](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/content-02-result-choice.png)|
|Writing|[Selection](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/writing-01-selection.png)|[Draft / review / author choice](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/writing-02-result-choice.png)|
|Music|[Time range](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/music-01-selection.png)|[Audition / candidate choice](../../../CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION/evidence/music-02-result-choice.png)|

Product Findings:

1. Shared grammar works across three professional surfaces; a fixed right-hand chat layout is unnecessary. Interface audit preserves manuscript reading, script comparison and song audition rather than flattening them into one layout.
2. Employee presence and work readiness are separate axes. Returned result clears current execution, not responsibility. Waiting for user input does not invent a new canonical Employee state.
3. “Accept” is not a universal transition: script version adoption, draft merge / author confirmation, and Master selection remain domain decisions. Writing source contains an older merge hint implying formal version creation; this candidate follows draft → review → author confirmation and leaves the original untouched for its owner to reconcile.
4. P6 inspection and Main editing coexist: a result reference opens bounded source/version details, then returns to the professional Main for comparison/choice. Conversation contains explanation and reference, not the entire deliverable.
5. Review does not transfer responsibility. Supporting/reviewing employee selection is not an Agent graph, Handoff or P7 gate.
6. Text and time anchors require version-aware implementation evidence later. A selected audio range is an instruction boundary, not proof that the provider supports precise audio editing. Unsupported attachments and execution selectors are disabled, not fake capabilities.

Original-source protection: SHA-256 over sorted top-level `.html/.js/.css` filenames + NUL + file bytes, before = after:

|Original directory|Files|Aggregate SHA-256|
|---|---:|---|
|CONTENT_GROWTH_CODEX_HTML_EXPLORATION|4|`7aa5719b126eb1cb086c4260f8bfd7c238301ebe8a5bc3883c11817b1a119390`|
|WRITING_BUSINESS_HTML_EXPLORATION|27|`f50ea3784565b8be641eda326da5a1bbcce1d783450a08597dc2022bc7a8816a`|
|MUSIC_BUSINESS_CODEX_HTML_EXPLORATION|9|`b7dde5062373acb01f1ddb05cbb3b7741b3dfb9cfc79e3fedf5b0cdad79ee284`|

No production frontend/runtime/DB modifications; no commit/push. Prototype state is memory-only; reload resets. No persistence, model, platform or audio-quality acceptance is claimed. No original Business HTML reconciliation is authorized by this delivery.
