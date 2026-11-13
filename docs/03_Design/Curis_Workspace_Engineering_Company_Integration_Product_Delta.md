# Curis · Workspace Engineering — Company Integration Product Delta（公司集成产品 Delta）

**Status**: WORKSPACE ENGINEERING COMPANY INTEGRATION PRODUCT DELTA（Delta 评审 · 仅做 Delta，不重做 Product Translation）
**阶段**: PRODUCT / WORKSPACE DESIGN — Company Integration Product Delta（承接《Product Translation · APPROVED CANDIDATE》+《Technical Reality Delta Review · GO FOR VISUAL》）
**日期**: 2026-08-16
**新增真实验收层**: Workspace Engineering **P0.5 = ACCEPTED**，最高真实验收层 = **Operating**（Installed / Operational / Company Integrated / Operating 全部 ACCEPTED；**Evolvable = NOT IMPLEMENTED**）

**上位依据（只引用，不重定义）**:
- `docs/03_Design/Curis_Workspace_Engineering_Product_Translation.md`（APPROVED CANDIDATE）
- `docs/03_Design/Curis_Workspace_Engineering_Technical_Reality_Delta_Review.md`（GO FOR VISUAL · BOUNDED）
- `CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md`（§12.2 裁定；Office⊥Org 等）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen · P1–P7）

---

## 0. 本 Delta 范围与纪律（硬约束）

**只做一次很小的 Company Integration Product Delta**——在《Product Translation》+《Technical Reality Delta》之上，仅因 P0.5「Operating 层真实验收」而必须调整的产品语义，**不重做 Translation、不重做 Technical Reality Delta、不进高保真**（高保真由本 Delta 收口后直接进入）。

**能力边界铁律（与 Technical Reality Delta 一致，不扩大）**：
- 保持：Installed / Operational / Company Integrated / Operating = **ACCEPTED**。
- 保持：**Evolvable = NOT IMPLEMENTED**。
- **不设计** Package update / migration / Marketplace / arbitrary extension / XHS·RD migration。

---

## 1. P0.5 新增真实技术事实（仅列本 Delta 处理的项）

> 来源：P0.5 ACCEPTED，最高真实层 Operating。以下事实已由真实 Runtime 证明，且对象与 Core 使用**真实 identity / reference contract**（不得用字符串伪造关系）。

动态 Workspace 已证明可走通完整 Operating 链：

```text
Package Workspace
  → real Company / Workspace identity
  → real Responsibility
  → real Employee
  → existing Capability
  → real Task / Execution
  → Artifact / Evidence / Result
  → business object state update
  → Desktop restart recovery
```

关键含义（对产品语义的影响）：
- 办公室创建后，**真实进入 Curis Company OS**——它有真实公司/空间身份、真实责任、真实员工、真实任务与执行、真实结果与证据，且这些实体之间用真实引用关联（非字符串伪造）。
- 因此 CEO 在 Business Home 看到的「员工 / 责任 / 正在执行的工作 / 结果 / 证据」是**真实运营真相**，不是抽象占位。

---

## 2. 对《Product Translation》+《Technical Reality Delta》的 Delta 打标

| 设计点 | 原状态（Translation / Technical Delta） | P0.5 Delta 调整 | 打标 |
|---|---|---|---|
| 办公室创建成功的归属 | Translation §2.A/§6：激活 =「可运营的空间」 | **强化**：新办公室是**真正进入 Curis Company OS**（出现在导航「办公室」分组、有真实公司身份），**不是独立 App / 插件** | **CONFIRMED + 语义强化**（不重做，补一条归属铁律） |
| Workspace Proposal 结构（§4 六答） | 经营方向 / 成功 / 启用哪些空间 / 默认运行 / 你能做什么 / 需连接什么 | **新增一栏自然语言**：「这个办公室**由谁负责 / 怎么工作 / 需要什么能力**」——用真实 Employee 角色 + 工作方式 + 能力三分类呈现，**不暴露 Responsibility/Employee/Capability Primitive** | **PRODUCT DESIGN DECISION（扩展）** |
| Business Home 呈现（§1.1 / §9 Q1） | 复用 Content Growth 八问模型（抽象经营层） | **强化为真实运营真相**：可自然呈现**真实 Employee（P2 Employee Presence）/ 责任（Current Responsibility）/ 正在执行的工作（P3 System Activity + real Task/Execution）/ 结果·证据（P6 Result Reference + Evidence list）** | **CONFIRMED + 呈现强化**（P0.5 证明实体真实，故可呈现真实而非占位） |
| Capability 缺口语言 | §8.1 三分类（Required for Activation / Required for Specific Action / Optional·Enhancement） | **沿用**，无变化 | **PRODUCT DESIGN DECISION（沿用）** |
| Handoff / P7 出现条件 | §2.C / §5：仅结构性进化走 P7 决策包 | **显式裁定**：Handoff / P7 **仅在真实业务需要时出现**，不作为每个办公室的固定步骤 / 固定 onboarding 环节 | **PRODUCT DESIGN DECISION（显式化）** |
| 激活确认文案 | §6：「已启用 · 现在可以运营」 | **钉死文案语义**：用户面表达「**已经可以经营**」，**绝不写「Package 安装成功 / 包已部署」**等内部状态 | **PRODUCT DESIGN DECISION（文案铁律）** |
| 内部概念隐藏（§9 Q3 / §12） | 隐藏 Handoff §9 全部原语 | **维持 + 强化**：P0.5 引入 real Responsibility/Employee/Task/Execution，但用户面一律转为自然语言（由谁负责 / 正在执行 / 结果已生成），原语不进 UI | **PRODUCT DESIGN DECISION（维持）** |

**§11 矩阵（Technical Reality Delta 结论）不受影响**：P0.5 属 Operating 层，进一步佐证 ① 动态安装 / ③ 自定义领域对象运行 / ④ 能力检查约束 等已 CONFIRMED 项；⑤ 签名·市场·第三方信任 / ⑥ 升级·迁移·回滚 仍为 **STILL POST-P3**；Evolvable 仍为 **NOT IMPLEMENTED**。本 Delta 不重打标。

---

## 3. 本 Delta 锁定的 6 条产品语义铁律（供后续高保真直接消费）

1. **进入公司，非独立 App**：新办公室创建成功 = 真正进入 Curis Company OS（导航「办公室」分组动态出现、真实公司身份），不是插件/独立应用。
2. **Proposal 三问自然语言**：「由谁负责 / 怎么工作 / 需要什么能力」用真实角色 + 工作方式 + 能力三分类表达，不暴露 Primitive。
3. **Business Home = 真实运营真相**：呈现真实 Employee / 责任 / 正在执行的工作 / 结果 / 证据（P2/P3/P6 落地），非抽象占位。
4. **能力缺口三分类沿用**：Required for Activation / Required for Specific Action / Optional·Enhancement；用户侧仅自然语言。
5. **Handoff / P7 仅真实需要时出现**：不是每个办公室的固定步骤。
6. **激活文案 =「已经可以经营」**：绝不出现「Package 安装成功 / 已部署」等内部状态词。

---

## 4. 停止状态

```text
WORKSPACE ENGINEERING COMPANY INTEGRATION PRODUCT DELTA — COMPLETE
→ 直接进入 Workspace Engineering Final High-Fidelity Design
```

（本 Delta 为独立小评审，不重做《Product Translation》（仍 APPROVED CANDIDATE）与《Technical Reality Delta Review》（仍 GO FOR VISUAL）。仅因 P0.5 Operating 层真实验收，补充 6 条产品语义铁律（进入公司 / Proposal 三问 / Business Home 真实化 / 能力三分类沿用 / Handoff·P7 仅真实需要 / 激活文案"已经可以经营"）。保持 Installed/Operational/Company Integrated/Operating = ACCEPTED；Evolvable = NOT IMPLEMENTED；不设计 update/migration/Marketplace/arbitrary extension。）

---

*Curis Workspace Engineering Company Integration Product Delta · 2026-08-16（Delta-only · 非重写 Translation · 非高保真 · 非 Runtime）*
