# CURIS AUTONOMOUS OPERATING V1
## IMPLEMENTATION READINESS REVIEW

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** READY AFTER CANONICAL BUSINESS SPINE ACCEPTANCE — IMPLEMENTATION NOT AUTHORIZED  
**Date:** 2026-08-20  
**Related Issue:** `issues/20260820_autonomous_operating_v1_implementation_001.md`  
**Source:** CEO accepted Operating Lifecycle Contract + CEO accepted Product Surface Mapping  

## 0. Readiness verdict

```text
READY — NOT AUTHORIZED
```

本 Review 只准备实施边界。它不证明 Autonomous Operating V1 已实现，也不证明 Business Spine 已通过。唯一硬 Start Gate 是：

```text
Canonical Business Spine = IMPLEMENTED / ACCEPTED
```

在该 Gate 之前，不得创建 Cycle、写入 autonomous control data、修改 Runtime / Schema / DB / Frontend，或用进行中的 Business Spine 状态推断可用性。

## 1. Existing reusable runtime

以下是实现前必须优先核对并复用的既有能力，不代表每一项已满足本专项的完整证据门槛：

| Reusable capability | 复用目的 | Phase 0 需要确认 |
|---|---|---|
| Work | 将 bounded Plan 释放为真实工作 | canonical Workspace scope、责任和结果回收 |
| Responsibility Assignment | Leader / Employee / Scope ownership | Assignment 是否能唯一承接 Cycle responsibility |
| Responsibility Router | Result / Handoff / Return / Escalation | 是否支持同一责任链的幂等 continuation |
| Team Operating Engine | Default Flow、Consult、Review、Return、Handoff | 是否能接受 pinned Operating Definition |
| Employee Execution | 真实员工执行路径 | Provider Task / Session、callback、cancel、restart |
| Provider Task / Session | 实际模型/Agent调用封装 | 外部质量/成本仍须真实验证，不可推测 |
| Result / Evidence | 结果与证据事实源 | 是否能关联 Evaluation Contract 与 Scope |
| Decision / Handoff | CEO Gate、Leader升级、责任交接 | actor、理由、边界、回退入口 |
| immutable Operating Definition | 防止运行中被覆盖 | version pin 与下一 Cycle 生效边界 |
| existing restart / recovery | 重启后恢复与失败回退 | 同一 SQLite / 同一对象 / 同一 responsibility |
| Context isolation | 责任、Workspace、租户隔离 | 不携带无关会话与跨 Scope 数据 |

不得因为缺少某个控制职责而复制上述对象；先登记 `EXTEND EXISTING` 或 `PRODUCT → IMPLEMENTATION GAP`。

## 2. Required minimal control plane

只允许补足以下薄控制职责：

1. Trigger intake / claim；
2. Workspace operating scope 的单 active Cycle 约束；
3. Situation Snapshot 派生；
4. Goal / Strategy / Plan pin；
5. bounded Plan release；
6. Review / Evaluation gate；
7. accepted Learning；
8. Next-cycle Decision；
9. exactly-one atomic successor；
10. durable WAIT / PAUSE / STOP；
11. restart-safe continuation。

这些职责必须作为 Company OS thin control plane，不能升级成 Generic Autonomous Agent Runtime、Operating Console 或第二套执行系统。

## 3. Product concept classification

Phase 0 必须对每项实际落点做最终确认：

| Classification | 允许的含义 |
|---|---|
| EXISTING OBJECT | 直接使用既有对象与来源，不重建 |
| EXTEND EXISTING | 在既有对象/接口上增加必要 bounded 语义 |
| VERSIONED SCOPE TRUTH | 需要版本、Scope、actor、证据和恢复引用的长期事实 |
| DERIVED | 可由既有事实重建的投影，不成为第二事实源 |
| TEMP AI REASONING | 仅提案/解释，未被 Review 接受前不可改变策略 |
| NOT V1 | 明确不进入本专项 |

任何“需要新增表/对象”的结论必须先证明既有对象无法承载，并触发 Stop Gate；本 Readiness 不预设具体 Schema。

## 4. Schema / data gap

### 4.1 目前可确认的产品缺口

- 需要让 Workspace-scoped Operating Cycle、pinned Strategy / Plan、Review / Learning 与 Next-cycle Decision 具有可持久、可回放的关系；
- 需要表达 durable WAIT / PAUSE / STOP 与 restart continuation；
- 需要把 Trigger claim、duplicate trigger、late Result、callback 幂等连接到同一 canonical Workspace scope；
- 需要明确 Evaluation Contract 与 Evidence / Result 的来源关系。

### 4.2 尚不能预设的内容

- 不预设新表名、列名、enum、migration 顺序；
- 不预设 OperatingDay / Cycle / Strategy 必须成为独立页面或 Primitive；
- 不把 Business 作为执行 Scope；
- 不复制现有 Result、Task、Employee、Workflow 或 Company Truth。

### 4.3 Phase 0 输出

Phase 0 必须形成一张“对象 / 来源 / 关系 / 可扩展点 / 不可承载原因”的 evidence table，并在发现 active DB migration、destructive rewrite、legacy mapping 不清时停止。

## 5. Frontend adapter gap

实现目标只是在既有表面消费摘要：

| Surface | Adapter projection |
|---|---|
| CEO Desk | Needs You、Important Result、Company Operating |
| Business | Operating Summary、Workspace Directory |
| Workspace | 经营状态、本轮重点、最新判断、下一步、conditional Need/Risk |
| Leader Conversation | Why、Evidence、Boundary、Next |

不新增 Operating Console、Strategy Center、Review Center、Learning Center、Cycle UI 或一级导航；不把 Runtime enum 直接显示给普通用户。

UI 适配必须保持：

- Domain Primary Surface 最大视觉区域；
- Current Operating 轻量；
- 进展由 Domain Primary Surface 优先表达；
- Need / Risk / CEO Gate 条件显示；
- 来源、freshness、unknown、manual、stale 真实投影；
- 处理后返回原 Company / Business / Workspace / Conversation 上下文。

## 6. Domain evidence gap

### 6.1 Primary Autonomous E2E

至少一个真实 Domain 必须完成连续两轮：

```text
Goal → Strategy → Plan → Team Operating → real Employee execution
→ Result / Evidence → Review → accepted Learning
→ CONTINUE / ADJUST → Cycle 2 → second Result
```

并提供 restart、duplicate trigger、late Result、WAIT、ESCALATE、CEO Gate 证据。controlled/replay 不能冒充真实 Primary E2E。

### 6.2 Cross-domain Contract Proof

第二 Domain 证明相同 Lifecycle 可承载不同 Strategy、Team Operating、Result Contract、Signal、Evaluation 与 Risk。允许 controlled/replay，但必须在 Review 中标明来源、限制和未验证外部边界。

### 6.3 首批候选

XHS 与 RD 是候选，不预设 Primary 排名，也不提前假定各自外部 Connector、Provider quality、Cost 或发布结果已可用。

## 7. Business Spine dependency

本专项依赖 Canonical Business Spine 的最终 Accepted Review，至少需要：

1. canonical Business identity；
2. Business 必归 Department；
3. Workspace 必归真实 Business；
4. `Workspace → Business → Department → Company` resolver；
5. Business + First Workspace atomic creation；
6. legacy unresolved → quarantined fail-closed；
7. clean frontend baseline / shared route seam；
8. Single / Multi / Generic E2E。

### Dependency disposition

```text
Business Spine 正在进行中的实现 = 不可消费为 PASS
Business Spine PARTIAL / BLOCKED = 本 Issue 保持 READY / NOT AUTHORIZED
Business Spine IMPLEMENTED / ACCEPTED = 才可进入 Phase 0
```

## 8. Exact start gate

主开发只有在以下材料齐全后才可启动本 Issue：

- Canonical Business Spine Accepted Review，明确 `IMPLEMENTED / ACCEPTED`；
- Accepted Evidence 覆盖 canonical identity、resolver、atomic create、legacy quarantine、clean frontend baseline、Single/Multi/Generic E2E；
- Product Architecture 确认该 Review 未产生与 Autonomous Operating Contract 冲突的 Delta；
- 新的执行子 Issue 逐项列出 Allowed Files、隔离 DB、Browser/Desktop、restart/recovery、failure、secret 与 cross-tenant 门禁；
- 主开发确认不会从旧 worktree、候选构建、活动数据库或进行中的分支拼接证明。

在以上材料缺任何一项时：`STOP / REPORT BLOCKED`，不修改代码。

## 9. Readiness conclusion

| 问题 | 结论 |
|---|---|
| Existing reusable runtime | 有，优先复用 Work / Assignment / Router / Team Operating / Employee / Result / Evidence / Decision / Recovery |
| Required minimal new control plane | 仅 Trigger、single active Cycle、pin、Review/Learning、Decision、WAIT/PAUSE/STOP、restart continuation |
| Schema/data gap | 需要 Phase 0 只读审计后确定；本 Review 不预设 Schema |
| Frontend adapter gap | 四个既有表面需要轻量投影，不新增 Console 或一级页面 |
| Domain evidence gap | 尚需 Primary 2-cycle E2E 与第二 Domain Cross-domain proof |
| Business Spine dependency | 硬依赖，未 Accepted 不可开工 |
| Exact start gate | `CANONICAL BUSINESS SPINE = IMPLEMENTED / ACCEPTED` + Accepted evidence 全套 |

## 10. Final state

```text
CURIS AUTONOMOUS OPERATING V1
— IMPLEMENTATION READINESS PREPARED
— CONTRACT BOUNDARY LOCKED
— EXISTING RUNTIME REUSE LOCKED
— PRIMARY / CROSS-DOMAIN PROOF LOCKED
— WAITING FOR CANONICAL BUSINESS SPINE ACCEPTANCE
— IMPLEMENTATION NOT AUTHORIZED
— STOP
```
