# Shared Employee Interaction Map

Status: Review
Authority Class: RESEARCH / DECISION EVIDENCE
Disposition: ACCEPTED / RECONCILED — NOT A SECOND AUTHORITY
Owner: CEO / Product review; Main Development exploration
Source: `CURIS_V1_SHARED_EMPLOYEE_INTERACTION_CANDIDATE.md`
Target Authority: Current Blueprint / Master Map / UI Blueprint / Shell §3.1A (consumed 2026-09-23)
Next Gate: Business owner bounded reconciliation evidence

CEO Final Review已接受本关系；Current正式定义见[Shell §3.1A](../../03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md)。本图仅保留Decision Evidence，不成为第二Authority；末尾“不修改Frozen”属于探索阶段记录，此次正式文档吸收已独立获CEO授权。

```text
Professional Object + version + optional selection
                 │  scoped, visible, removable selection
                 ▼
Responsibility → Lightweight Employee Bar (always present)
                 │                    │
        Optional Main.WorkArea Conversation (default hidden)
        expand: 一起讨论 / 讨论这段; collapse: 收起讨论
                 │  messages/input/selection preserved on collapse
        Shared Composer
        text · target · context / selection · refs · real capabilities
                 │
       ┌─────────┴──────────────┐
       │ discussion / question │ authorized bounded execution
       │ no automatic edit     │ Holder ≠ current executor
       └─────────┬──────────────┘
                 ▼
       Result / Candidate + provenance
          │                     │
          │ lightweight ref     │ professional artifact
          ▼                     ▼
  Utility inspection  ←→  Main preview / compare / audition
                                │
                   domain review + explicit human choice
                   reviewer appears with actual contribution
                   (responsibility does not automatically transfer)
                                │
              version-checked domain transition / revise / reject
                                │
                     same Work/context continuation
```

|Domain|Selection|Human choice changes|Does not change|
|---|---|---|---|
|Content Growth|Script paragraph / Shot|accepted script/selected artifact version|rendered video, rights, publication without separate verification|
|Writing|chapter / draft version / text range|draft → reviewed draft → author-confirmed formal snapshot|old formal/online snapshots or story Canon implicitly|
|Music|candidate / exact time range|selected candidate → explicitly confirmed Master|old audio, publication or sung-lyric verification|

Default layout: Professional Object → Employee Bar → Professional Main. Expanded layout inserts the optional Conversation / Shared Composer immediately below the bar. Results return to Main; discussion can close while the responsible Employee stays visible. No permanent right chat or floating Employee panel.

Global CEO Assistant is a separate lightweight floating Company coordinator, visually subdued during Employee discussion, not this Employee. Conversation belongs to Main; full artifact is not a chat bubble. Context/Utility visibility is UI-only. Waiting/Result-ready are Work facts, not additional Employee states. These arrows describe relations and optional transitions, not a Workflow Engine/DAG.
