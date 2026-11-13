# Curis · Content Growth 公司演化模型

> **状态**：CONTENT GROWTH ARCHITECTURE DELTAS APPLIED（DELTA 1/2/3 已应用）
> **类型**：Reference Only · 演化路径草案（非权威）
> **配套**：`Curis_Content_Growth_Operating_Model.md`（G/J/K/L/M 节）、`Curis_Channel_Account_Matrix_Model.md`、`Curis_Organization_Routing_Architecture.md`

本文描述 **Company 从单人起步到多团队** 的自然演化路径，以及 Content Growth 如何在各阶段保持「普通用户简单、底层组织复杂」。含 Unified Growth Feedback 闭环。

---

## 1. 演化的两个正交轴

Content Growth 的复杂度沿**两个轴**自然增长，Curis 须同时支持、互不绑架：（注意 **DELTA 1**：`Organization` 轴与 `Office` 经营轴**正交**——Employee/Team 属 Organization，经 Responsibility Assignment 服务 Office，非组织隶属。）

| 轴 | 早期 | 增长后 |
|---|---|---|
| **账号/平台轴**（Channel Account 数） | 1–2 账号 | 多 Office × 多平台多账号 |
| **组织轴**（Employee/Team） | 单人全能 | 多 Employee → Team |

两轴独立：一家公司可「账号多但人少」（靠共享 Employee + 高复用），也可「人多在少数账号精耕」。

---

## 2. 阶段模型

> **DELTA 1 提示**：以下各 Stage 中的 Employee/Team 均属 Company 的 **Organization** 轴（与 Office 正交），经 Responsibility Assignment 服务 Office，不隶属于 Office。

### Stage 0 — 单人 / 单 Office / 单账号
```
Company
└ Office A（个人IP）
   └ Douyin·个人IP号
Employee：全能 AI 员工（兼选题/脚本/生产/字幕/发布/互动）
用户理解：Office + 1 个 AI Employee + Connected Account + Current Work
```
- Org Routing 几乎透明（单人即唯一 Holder）。
- 无 Capacity/Queue 信号需求。

### Stage 1 — 单 Office / 多账号（跨平台同定位）
```
Office B（AI工具内容）
├ Douyin·AI工具号
├ XHS·AI工具号
├ Bilibili·AI教程号
└ TikTok·AI Tools
Employee：仍可能单人，但按 Account Context 动态分流生产
```
- 出现 **Account-aware Production** 分流（HIGH REUSE + 部分 DIVERGENCE）。
- Target Account 子集选择开始有意义（Content #101 发 3 个、#102 发 2 个）。

### Stage 2 — 多 Office（不同定位）
```
Office A（个人IP）  Office B（AI工具）  Office C（生活方式）
```
- 上游 **Content Opportunity / Intent 在 Office 间或全局共享**，下游按 Office 定位分流。
- 开始出现 **Shared Employee**（字幕员工跨 A/B/C 服务）。

### Stage 3 — Employee 倍增 / 专业分工
```
Subtitle Employee A / B / C
Script Employee A / B
Video Employee A / B
```
- Org Router 按 specialty/capacity/availability 动态分配。
- **Capacity 信号**开始有价值（某责任等待升高）。

### Stage 4 — Team 化
```
Subtitle Team（Lead + A/B/C）
Video Team（Lead + A/B）
```
- Team Lead **仅介入异常/管理判断**（Priority Conflict / Blocker / Quality·Acceptance / Exception / Standards·Coaching / Abnormal Workload）；**常规 Queue/Assignment/Load balancing 由 Organization Router 确定性完成**（DELTA 2）。
- 分组维度自由（职能或平台）。
- 用户**仍只看到 Office + AI Employee + Current Work**；Team 是后台组织形态。

---

## 3. 普通用户始终简单的机制（K 节落地）

无论 Stage 几，**首版用户界面只暴露**：
`Office` · `AI Employee` · `Connected Accounts` · `Current Work` · `Needs CEO`

复杂度由后台吸收：

| 后台机制 | 用户感知 |
|---|---|
| Org Routing 动态求解 Holder/Executor | 无（任务自动到人） |
| Capacity / Bottleneck 检测 | 无（除非触发建议） |
| Team 形成 / Lead 分派 | 无（仍是「AI Employee 完成」） |
| 瓶颈建议 | CEO Assistant 白话 + 二选一按钮 |

**唯一例外**：当系统检测到瓶颈，CEO Assistant 用白话汇报并给 `[按建议增加]` / `[先不增加]` —— 用户只做二选一，不设计组织。

---

## 4. Unified Growth Feedback（M 节闭环）

`Publication / Engagement / Analytics` 保持 **per-Account、per-Platform 真相源**（上一轮结论）。

但必须**回流 Growth Intelligence**，形成闭环：

```
同一主题跨账号表现：
  Douyin AI号     → 完播表现好        → 该账号偏好快节奏口播
  Bilibili 教程号 → 用户更关注成本     → 该账号偏好深度教程
  XHS 效率号      → 收藏表现高        → 该账号偏好干货清单
        ↓
  Cross-account Growth Knowledge（跨账号增长知识）
        ↓
  驱动下一轮：
    Content Opportunity（什么值得做）
      → Target Accounts（哪些账号更适合此主题）
        → Account-aware Production（据此调整分流策略）
```

**闭环意义**：Content Growth 不是单向管道，而是 G 节八阶段的**自驱循环**。Growth Knowledge 积累越多，Target Account 推荐与 Production 分流越准。

---

## 5. 首版最小可行范围（建议）

为不超前建设，首版建议只落地：

1. **Office + Account Pool + Target Account 子集**（A/B/C/D 节）—— 经营层骨架。
2. **Content Intent / Opportunity 作为共享对象**（E 节）—— 上游推理共享。
3. **Content Production WS + Channel Ops WS**（上一轮两层）—— 执行层。
4. **Shared Employee + Org Routing 基础版**（H/I 节）—— 动态指派，不暴露规则。
5. **轻量 Runtime Facts + Bottleneck Candidate + 一键增员建议**（DELTA 3 / L/K 节）—— 采集 queue_depth / waiting_since / oldest_wait / active_count / employee_availability，产生 Bottleneck Candidate，触发 CEO Assistant 白话建议。不建 throughput 预测 / capacity score。
6. **per-Account Publication/Engagement/Analytics + 回流**（M 节）—— 闭环起点。

**首版不做**：完整 Team 调度、负载均衡算法、大型调度系统、throughput 预测、复杂 capacity score、智能负载、企业级 scheduler（Stage 4+ 按需演化，DELTA 3）。

---

## 6. 与既有 Curis 三层架构对齐

- **组织层（DELTA 1 正交）**：Company 下两轴并列——`Business/Operating Context → Office`（经营单元：目标/定位/受众/策略/Knowledge/Account Pool/Growth Context）；`Organization → (Department/Team/Role/Employee)`（组织结构）。Office ≠ Department/Team；Employee 经 Responsibility Assignment 服务 Office，非组织隶属。本模型的 Office 即经营轴的新增单元。
- **运行层**：Content Growth 八阶段闭环 = 跨 Office + 跨 Professional Workspace 的业务流程编排（目标→规划→任务图→队列→调度→执行→验收→返工→完成）。
- **能力层**：Capability Provider（生产工具 / 渠道 Connector / Agent/Skill/Tool）可替换，Office/Employee 不拥有能力，只声明责任需求。

**不新建顶层 primitive**：Content Growth 是上述三层的**编排与增长上下文**，不是新的一级产品概念（满足用户硬约束）。

---

## 7. 开放问题

1. Office 能否在 Stage 间动态增删（公司业务线调整）？删 Office 时其 Account/历史如何处置？
2. Cross-account Growth Knowledge 的存储与隐私边界（是否跨 Office 共享）？
3. 首版 Capacity 信号是否足以驱动「增员建议」，还是需更丰富瓶颈识别？
4. Team 化后，用户是否需要在某处「看到团队」（如 CEO 工作台概览），还是完全后台？

---

## DELTA 1/2/3 应用记录（本轮批准）

- **DELTA 1 — Office/Org 正交**：取消 `Company → Office → Employee/Team`；Employee/Team 属 Organization 轴，与 Office 正交，经 Responsibility Assignment 服务 Office（见 §1、§2、§6）。
- **DELTA 2 — Router/Team Lead 分离**：Stage 4 Team Lead 仅异常/管理判断，常规调度归 Router（见 §2）。
- **DELTA 3 — 首版 Capacity 降复杂度**：首版只采集 Runtime Facts → Bottleneck Candidate，不建 throughput/capacity score/智能负载/企业级 scheduler（见 §5）。

---

*公司演化模型草案，未固化。与 Office / Intent / Org Routing Contract 一并设计。*
