# Product Blueprint 4.4 · 评审就绪评估（S0 前置）

Status: Deprecated

> 本文评估的是已被 Blueprint 5.0 取代的历史版本。当前 Review 与实现门禁以唯一 Blueprint 5.0、Business Runtime v1.0 和 ADR-0041 为准。

> 日期：2026-08-04
> 目的：EvoFlow 复用四项（阶段门 / 验收标准 / 检查点 / trace）的 S0 强制前置 = Business Runtime Blueprint 变更评审。
> 本文件评估 Blueprint 4.4（`docs/01_Product/Curis_Product_Blueprint.html`，Status Review）的评审就绪度，输出差距与检查清单。

---

## 1. 当前状态（CURRENT_STATE §7/§11a 事实）

- Product Blueprint v4.4：`Status: Review`；Freeze 条件 = 核心生命周期、研发工作台首个任务“Curis 的自研发” Runtime、失败与外部证据路径、跨对象闭环和 Runtime Simulation 全部完成并通过 Review。
- Gap Report（`docs/01_Product/Business_Runtime_Gap_Report_2026-07-31.md`）：Status Review；结论「Product Definition 足够进入 Runtime 设计；**Business Runtime Blueprint 已定义但独立 Review 与 Simulation 未完成**」。
- 权威基线：`main @ c0e1855f`；产品/架构/设计/开发四条 Frozen 入口在 `CURRENT_STATE §11`。

**结论：Blueprint 4.4 处于「已定义、待评审、Simulation 未完成」——S0 前置尚未达成。**

## 2. 评审就绪度评估

| 维度 | 状态 | 差距 |
|---|---|---|
| 产品定义（One-person AI Company / Company OS / Workspace） | Frozen（ADR-0040） | 无 |
| 完成标准 | Frozen（ADR-0041） | 无 |
| Blueprint 内容（v4.4：生命周期/First Arrival/CEO Operating Day/Assistant Runtime/AI 组织/Workspace Studio/UI 路径/经营循环/Simulation） | 已定义（Review） | 内容齐备性未知，需独立评审核对 |
| 独立 Review | **未完成** | 需评审记录（对照 ADR-0041 完成标准逐项） |
| Runtime Simulation（研发工作台首个任务：Curis 的自研发） | **未完成** | 需 Simulation 计划 + 执行证据 |
| 与本仓库已交付事实的一致性 | **有偏差风险** | CURRENT_STATE 已完成能力（Step5 网关/桥/引导/经营日聚合）晚于 Blueprint 4.4 冻结基线（c0e1855f），评审时需以 CURRENT_STATE 为权威事实、Blueprint 为目标态，勿混用 |

## 3. 评审检查清单（评审通过需逐项有证据）

### 3.1 生命周期与核心对象
- [ ] 一人 AI 公司完整生命周期（First Arrival → 公司空间 → CEO Operating Day → 经营 → 关闭）有明确状态机与阶段契约（ADR-0041 要求）
- [ ] 核心对象（Company/Project/Department/Employee/Capability/Task/Artifact/Workspace）生命周期与交叉闭环在 Blueprint 中可追溯
- [ ] 与 CURRENT_STATE「已交付事实」逐条对账：Blueprint 目标 ≠ 已交付，评审不把目标当事实（AGENTS.md 纪律）

### 3.2 CEO Operating Day 与 Assistant Runtime
- [ ] CEO Operating Day（今天后端已交付 `operating-day` 聚合端点）在 Blueprint 中的定义与实现一致
- [ ] 独立 CEO Assistant Runtime 边界（Identity/Snapshot/Notifications/Query/Command）与 CURRENT_STATE 一致
- [ ] 经营循环（价值/公司经营循环、Truth/Decision/Change）有 Simulation 场景

### 3.3 Workspace Studio 与 AI 组织
- [ ] Workspace Studio 装修与交付、Workspace Runtime 状态机定义完整
- [ ] AI 组织关系（员工=动态能力岗位）不因复用建议回退（评审红线）

### 3.4 失败与外部证据路径
- [ ] 失败/异常/外部证据路径（accept/rework/recovery）在 Blueprint 有定义——**这直接决定 EvoFlow 复用 2.2/2.3 的语义落点**：验收标准、检查点恢复都必须先有业务层定义，才能进技术设计

### 3.5 Runtime Simulation
- [ ] Simulation 计划（研发工作台首个任务：Curis 的自研发，如「用 Curis 开发 Curis」）已评审
- [ ] Simulation 执行证据（真实运行轨迹，非 mock）已产出并附入评审

## 4. 就绪度结论

**未就绪**：差「独立 Review 记录 + Runtime Simulation 计划与执行证据」两项硬条件（ADR-0041 + CURRENT_STATE §7 Freeze condition）。

## 5. 建议路径（推动 S0 达成）

1. **Step A（评审闭环）**：以 ADR-0041 完成标准为清单，对照 Blueprint 4.4 逐项独立评审，产出评审记录（可参照 `reviews/` 既有格式，标注 Status: Review → 通过后 Frozen）。
2. **Step B（Simulation 计划）**：定义研发工作台首个任务“Curis 的自研发”的 Simulation 场景（建议与「业务工作台引导 + 经营日聚合」真实能力联动——引导生成研发项目 → 执行 → 经营日展示结果，形成真实闭环证据）。
3. **Step C（Simulation 执行）**：跑通真实运行轨迹（复用已交付的 rd-workflow / 引导 / operating-day），产出证据。
4. **Step D（S0 达成）**：Review + Simulation 证据齐 → Blueprint 4.4 转 Frozen → EvoFlow 复用四项方可按 `docs/plan/evoflow-reuse-repo-mapping.md` 立项进 Code。

## 6. 附：与 EvoFlow 复用立项的衔接

- S0 是四项的**硬前置**（架构评审 §5 依赖图 S0→S2→S4；S1/S3 可并行）。
- 建议把「验收标准 / 检查点恢复」的**业务语义**（评审问题 1/3：验收最低可判定、重规划分叉语义）在 Blueprint 评审时一并拍板，避免技术设计反推业务定义。
- 本评估不授权任何 Blueprint 变更或业务代码实现（Scope: 只读评估）。
