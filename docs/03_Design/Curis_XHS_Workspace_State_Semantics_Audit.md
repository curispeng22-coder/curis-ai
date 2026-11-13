# Curis XHS Workspace — State Semantics Audit（状态语义审计）

> **范围**：仅审计 XHS A–E 五个状态的业务时间线一致性（AI Employee 责任 / 状态 / Handoff / Automation / Needs CEO），不涉及 Pane Shell 结构、Search、视觉改版、Blueprint 或正式代码。
> **依据**：`Curis_XHS_Workspace_Design_Brief.md`（§8 Review Gate 与 Handoff、§9 Employee Workstation 出现时机、§10 Needs CEO、§11 Analytics / Content Reuse Loop）、`Curis_XHS_Workspace_Interaction_Exploration_v2.md`、`Curis_XHS_Workspace_Visual_v4.html`（A–E 实物）。
> **状态**：XHS INSTANCE APPROVED CANDIDATE（最终收口 · 待 Shell / Shared Pattern Delta Review）

---

## 1. 角色模型（不发明新岗位）

所有角色均来自 Brief / Research，审计中**禁止自创岗位**：

| 角色 | 姓名 | 职责 | 来源 |
|------|------|------|------|
| 策划 | 李翔 | 选题 / 信号 → 交接内容创作 | Brief §8 / v4 |
| 内容创作 | 陈真 | 制作 Note（封面/标题/正文/标签）→ 完成后交接审核 | Brief §8 / v4 |
| 内容审核 | 王芳 | 违禁词 / 人设一致性 / 品牌表达检查；通过→交接发布员工；阻塞→升级 CEO | Brief §8 / v4 |
| 发布员工 | （未具名，角色标签） | 执行发布（"通过 → Handoff 到发布员工"） | **Brief §8 明示** |
| 数据复盘 | — | **不是独立员工岗位**；是自动 Analytics / Content Reuse Loop（系统事件，指标阈值可配置） | Brief §11 |
| CEO | — | **仅 Decision Gate**；处理真正的决策，不是工作流"下一步按钮" | Brief §10 |

**Handoff 链（单一事实源）**：
`策划·李翔 → 内容创作·陈真 → 内容审核·王芳 → 发布员工 →（已发布）→ 数据复盘`

> 注意：发布员工是 Brief §8 中**最后一个被点名的 Handoff 接收方**。"数据复盘"是发布后的自动分析阶段（Brief §11 的 Content Reuse Loop），**不是一次新的员工 Handoff**，因此不得杜撰"数据分析/运营复盘"独立岗位。

---

## 2. 三层责任语义拆分（核心修正）

本轮新增的关键语义拆分。**三者必须严格区分**，混用会直接催生 A–E 状态文案冲突（如 E 把已完成发布员工当当前 Presence）。

| 维度 | 定义 | 是否随 Handoff 改变 | 在 Employee Presence 中表达 |
|------|------|:---:|:---:|
| **Object Owner（对象归属）** | 业务对象的稳定归属：所属 Business / Workspace / 长期责任岗位（如「小红书运营办公室」） | ❌ **不改变**（一次 Handoff 不改变对象归属） | **不表达**。Presence 不是 Object Owner，也不是"最后一个处理过该对象的人" |
| **Current Responsibility（当前责任）** | 当前工作阶段由谁负责；**Handoff 改变的就是它** | ✅ 随 Handoff 转移 | ✅ 表达 |
| **Current Executor（当前执行者）** | 此刻真正执行工作的 Employee | ✅ 随工作完成 / 系统接管而置空 | ✅ 表达；**允许为空（none）** |

**Employee Presence 的硬边界**：
- Presence **只**表达 **Current Responsibility / Current Executor**。
- Presence **不是** Object Owner。
- Presence **不是**"最后一个处理过该对象的人"（历史 Handoff 用历史 Event 呈现，不占 Presence）。
- **Current Executor 允许为空**：当员工工作已完成、系统进入自动 Analytics 时，Presence 显示系统自动活动（明确标注"非员工"），且 **Current Executor = none**。

**原则（Shared Pattern Delta Candidate，见 §7）**：
> **Object Owner ≠ Current Responsibility ≠ Current Executor**

---

## 3. 统一状态模型（审计判据 · 基于 §2 三层拆分）

| 情形 | 表现规则 |
|------|---------|
| **当前员工 working** | Presence 显示 Current Executor + Activity + 上一步 Handoff Origin（如有）+ 下一步责任可显示为"**下一步：内容审核 · 王芳**"；**不得写"已交接"** |
| **当前员工 completed** | 才产生 Handoff Event（历史）；Responsibility 转移给下一员工 |
| **下一员工 working** | Presence 切换为下一员工；上一跳 Handoff 成为历史 Event |
| **系统自动阶段（如 Analytics / Monitoring / Automation）** | **Current Executor = none** → **使用独立的 System Activity 组件**，不再复用 Employee Presence 组件；不显员工头像、不显"工作过程"入口；**不创造"数据分析员工"**，绝不把系统活动伪装成员工 |
| **Needs CEO** | 当前员工（仍是 Current Responsibility / Executor）已完成判断 → 自动升级 Decision Gate；**CEO 是 Decision Authority，不接管 Current Responsibility**，也不产生 Handoff；Presence 仍显当前员工，不显 CEO 为责任方 |
| **Utility 打开** | **仅视图变化，不改变业务状态**；继承来源状态（D == B 业务时间线） |

**基本原则**：
- Automation by default；Human action only at Decision Gates。
- 不要让 CEO 充当工作流"下一步"按钮。
- **System Activity ≠ Employee Presence（硬拆分）**：当 Current Executor = none、系统接管运行时，必须改用**独立轻量 System Activity 组件**（如 `⚙ 自动数据观察中` + 历史 Handoff + 非员工 Runtime 说明），**不得继续使用 Employee Presence 组件**、**不得显员工头像**、**不得显"工作过程"入口**。二者语义不同，混用会误导责任归属。
- 八维审计口径：**① Object Owner ② 当前责任员工（Current Responsibility / Executor）③ 员工状态 ④ 当前 Activity ⑤ 上一步 Handoff ⑥ 下一步责任 ⑦ 是否已发生 Handoff ⑧ 下一步触发方（AI自动 / CEO Decision / 系统事件）**。

---

## 4. A–E 逐状态审计

### A · Default Calendar（默认日历，日历主导）
| 维度 | 审计结论 |
|------|---------|
| ① Object Owner | 小红书运营办公室（稳定归属） |
| ② 当前责任员工 | （无 — 未选 Note，日历主导视图，**不强制员工卡**，符合 Brief §9） |
| ③ 员工状态 | N/A（默认浏览态） |
| ④ 当前 Activity | N/A |
| ⑤ 上一步 Handoff | N/A |
| ⑥ 下一步责任 | N/A（点选 Note → 进入 B） |
| ⑦ 已发生 Handoff | 否（尚未进入工作流） |
| ⑧ 需要 CEO | 否 |
| ⑨ 下一步触发 | 用户事件（点选 Note）→ B；AI 自动（若当天有 in-progress Note，Presence 浮现） |

**判定**：✅ 一致。无员工 Presence 是设计意图（日历主导），不冲突。

---

### B · Note Selected → Split Working（专业创作工作面）
| 维度 | 审计结论 |
|------|---------|
| ① Object Owner | 小红书运营办公室（稳定归属，不变） |
| ② 当前责任员工 | Current Responsibility = 陈真 · 内容创作；Current Executor = 陈真（制作中） |
| ③ 员工状态 | working（制作中） |
| ④ 当前 Activity | 正在制作：封面生成中 |
| ⑤ 上一步 Handoff | 策划·李翔 → 内容创作·陈真（自动）✅ 正确 |
| ⑥ 下一步责任 | 内容审核 · 王芳（显示为"下一步：内容审核 · 王芳"） |
| ⑦ 已发生 Handoff（陈真→王芳） | **否**（陈真仍在 working，未完成） |
| ⑧ 需要 CEO | 否 |
| ⑨ 下一步触发 | AI 自动：陈真创作完成后自动 Handoff 王芳 |

**判定**：✅ 一致（前序轮次已修正）。Presence 正确表达 Current Executor = 陈真，未误写"已交接王芳"，未把 Object Owner 当当前员工。本轮新模型下仍正确，**无需改动**。

---

### C · Review Gate / Needs CEO（审核闸 + 决策横幅）
| 维度 | 审计结论 |
|------|---------|
| ① Object Owner | 小红书运营办公室（稳定归属） |
| ② 当前责任员工 | Current Responsibility = 王芳 · 内容审核（她发起闸，责任仍归属其审核节点）；Current Executor = 王芳（已完成判断，等待） |
| ③ 员工状态 | needs_ceo（已升级 CEO，等待决策） |
| ④ 当前 Activity | 已完成审核判断 → 命中绝对化用语 → 自动升级 CEO 决策 |
| ⑤ 上一步 Handoff | 内容创作·陈真 → 内容审核·王芳（自动）✅ 正确（此时陈真已 completed，Handoff 成立） |
| ⑥ 下一步责任 | **CEO 决策**（Decision Gate，**不是**工作流下一员工，**不是** Handoff） |
| ⑦ 已发生 Handoff | 是（陈真→王芳）；CEO 升级是 Decision Gate 事件，**非** Handoff |
| ⑧ 需要 CEO | **是** |
| ⑨ 下一步触发 | CEO Decision（人类决策闸）→ 决策后工作流自动恢复（自动发布或退回修改） |

**判定**：✅ 一致。**CEO 是 Decision Authority，不接管 Current Responsibility**；Presence 仍显王芳（未把 CEO 当责任接管方 / 员工）；"自动升级 CEO 决策"与 Handoff 并列呈现、不混淆。本轮新模型下仍正确，**无需改动**。

---

### D · Utility Preview（图文预览，右 · Resizable）
| 维度 | 审计结论 |
|------|---------|
| ① Object Owner | 小红书运营办公室（继承 B） |
| ② 当前责任员工 | Current Responsibility = 陈真 · 内容创作；Current Executor = 陈真（继承 B） |
| ③ 员工状态 | working（制作中）（继承 B） |
| ④ 当前 Activity | 正在制作：封面生成中（继承 B） |
| ⑤ 上一步 Handoff | 策划·李翔 → 内容创作·陈真（自动）（继承 B） |
| ⑥ 下一步责任 | 内容审核 · 王芳（继承 B） |
| ⑦ 已发生 Handoff（陈真→王芳） | **否**（继承 B） |
| ⑧ 需要 CEO | 否（继承 B） |
| ⑨ 下一步触发 | Utility 打开是**视图变化，业务状态不变**；业务时间线必须与 B 完全一致 |

**判定**：✅ 一致（前序轮次已修正）。业务语义完全继承 B，仅打开 Utility 视图，未改任何业务状态文案。本轮新模型下仍正确，**无需改动**。

---

### E · Published / Analytics（已发布 + 数据）
| 维度 | 审计结论 |
|------|---------|
| ① Object Owner | **小红书运营办公室（稳定归属，不变）** |
| ② 当前责任员工 | Current Responsibility：发布员工已完成发布 → 当前责任阶段结束；进入**系统自动 Analytics 阶段**（系统事件，非员工责任）。Current Executor：**none**（发布员工 completed；系统自动活动不是员工） |
| ③ 员工状态 | completed（已发布）+ 系统自动 Analytics 进行中 |
| ④ 当前 Activity | 系统正在进行自动 Analytics / Content Reuse Loop（**非员工活动**） |
| ⑤ 上一步 Handoff | 内容创作·陈真 → 内容审核·王芳 → 发布员工（自动）；全链达成，作为**历史 Handoff / Result** 呈现 |
| ⑥ 下一步责任 | 系统自动 Analytics / Content Reuse Loop（**非员工 handoff**，不创造"数据分析员工"） |
| ⑦ 已发生 Handoff | 是（陈真→王芳→发布员工 三跳完成）；发布后无新员工 Handoff |
| ⑧ 需要 CEO | 否（CEO 决策已在 C 完成并自动发布） |
| ⑨ 下一步触发 | 系统事件（自动数据观察 / 复盘反哺选题库，Content Reuse Loop） |

**判定**：✅ **一致（最终修正）**。发布员工 completed 后**不再作为当前 Employee Presence**（Current Executor = none）。改用**独立 System Activity 组件**表达系统自动 Analytics——`⚙ 自动数据观察中` + `发布员工已完成发布（历史 Handoff / Result）` + `Object Owner：小红书运营办公室` + `当前无执行员工 · 正在进行 Analytics / Content Reuse Loop（非员工 Runtime）`。**不显员工头像、不显"工作过程"入口、不创造"数据分析员工"**。历史 Handoff（陈真→王芳→发布员工）作为 Result 保留；Object Owner 稳定归属小红书运营办公室。本轮最终收口（见 §6 映射）。

---

## 5. 发现汇总

| # | 状态 | 问题 | 严重度 | 修正 |
|---|------|------|:------:|------|
| F1 | B / D | "已交接内容审核·王芳" 与"陈真仍在制作中"语义冲突（working 态不得写"已交接"） | 高 | 前序已修正 → "下一步：内容审核·王芳"；本轮新模型下确认仍一致 |
| F2 | E | 原"发布员工 · 发布"作为当前 Employee Presence，违反 Current Executor = none 规则（发布员工已 completed） | 高 | 本轮修正：Presence 改显系统自动 Analytics（非员工）；Current Executor = none；发布员工完成转历史 Handoff / Result；Object Owner 仍显小红书运营办公室 |
| F3 | C | — | — | 一致，无需修改（CEO 不接管责任、非 Handoff 已正确） |
| F4 | A | — | — | 一致，无需修改 |

---

## 6. 对应 v4 HTML 修正映射

| 位置（v4） | 原（冲突） | 最终修正 |
|-----------|------|--------|
| E `presence`（原） | `发`（发布员工头像）+ `发布员工 · 发布` + `▸ 工作过程` 按钮 | **删除 Employee Presence 组件**，改 `.sys-activity` 独立系统组件 |
| E `.sys-ico` | — | `⚙`（系统图标，**非员工头像**） |
| E `.sys-title` | — | `自动数据观察中` |
| E `.sys-meta` | — | `发布员工已完成发布（历史 Handoff / Result）　·　Object Owner：小红书运营办公室` |
| E `.sys-sub` | — | `当前无执行员工　·　正在进行 Analytics / Content Reuse Loop（非员工 Runtime）` |
| E `handoff-light` | `✅ …进入数据复盘（自动）` | `✅ Handoff：陈真 → 王芳 → 发布员工 已完成发布（历史 Result）` |
| E 说明文字（caption） | "Employee Presence 转为「已发布」" | 改为：发布员工 completed 后**不再作为当前 Employee Presence**（Current Executor = none）；改用 **System Activity 组件**（非员工）；Object Owner 仍归属小红书运营办公室 |

> **关键边界**：System Activity 组件**无员工头像、无"工作过程"入口、不伪装成 Employee Presence**；发布员工仅作为历史 Handoff / Result 出现。**B / D / C 经审计已一致，本轮无改动**。

---

## 7. Shared Pattern Delta Candidate

> **Object Owner ≠ Current Responsibility ≠ Current Executor**

作为跨 Workspace 强制语义基线候选（Shared Pattern Delta Candidate），建议随 Shell Contract / Design System 一同 Frozen：

- **Object Owner**：业务对象的稳定归属（Business / Workspace / 长期责任岗位）。不因任何单次 Handoff 改变。用于对象卡片、详情页、权限判断的来源，**不进入 Employee Presence**。
- **Current Responsibility**：当前工作阶段的责任方；Handoff 转移它。
- **Current Executor**：此刻真正执行工作的 Employee；员工完成 / 系统接管时允许为 **none**。
- **Employee Presence 硬边界**：只表达 Current Responsibility / Current Executor；不是 Object Owner，不是"最后处理过的人"；系统自动活动以"**非员工**"显式标注，**绝不伪装成员工**，**绝不创造"数据分析员工"等伪岗位**。

**适用**：XHS / RD / 未来所有 Workspace 的对象详情、工作流 Presence、Handoff 历史、Analytics 阶段呈现。

---

> **Shared Pattern Delta Candidate #2：Employee Presence ≠ System Activity**

作为跨 Workspace 强制语义基线候选（Shared Pattern Delta Candidate），与 #1（Object Owner ≠ Current Responsibility ≠ Current Executor）并列建议随 Shell Contract / Design System 一同 Frozen：

- **Employee Presence** = 表达 **Employee 的 Current Responsibility / Current Executor**（有真实员工在场）。
- **System Activity** = 表达 **非员工的 Runtime / Automation 状态**（Analytics / Monitoring / 定时任务 / Content Reuse Loop 等），**Current Executor = none** 时启用。
- **二者不得混用**：系统自动运行阶段**严禁复用 Employee Presence 组件**（不显员工头像、不显"工作过程"入口），必须改用独立 System Activity 组件；**绝不把系统活动伪装成员工**、**绝不创造"数据分析员工"等伪岗位**。

**适用**：XHS / RD / 未来所有 Workspace 的已发布 / 已完成 / 自动化阶段呈现、Analytics 看板、监控态、自动化流水线状态。

---

## 8. 范围外（本轮不做）

- Pane Shell / Toggle / Search 结构（已在前序轮次 Frozen）。
- Calendar / Note 编辑 / Employee Presence 浮现时机 / Utility 浏览器 / Decision 等已确认结构的改动。
- 新功能、新岗位、新状态枚举。
- Blueprint 修改、正式前端代码。
