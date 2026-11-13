# Curis · Organization & Routing 架构

> **状态**：CONTENT GROWTH ARCHITECTURE DELTAS APPLIED（DELTA 1/2/3 已应用）
> **类型**：Reference Only · 组织/路由架构草案（非权威）
> **配套**：`Curis_Content_Growth_Operating_Model.md`（H/I/J/K/L 节）、`Curis_Channel_Account_Matrix_Model.md`、`Curis_Content_Growth_Company_Evolution_Model.md`

本文定义 **Process / Responsibility Requirement / Organization Routing / Employee / Team / Capacity / Queue** 的关系与运行模型。普通用户不可见路由细节（K 节硬约束）。

---

## 1. 核心原则：Process 不绑固定 Employee

```
Business Process
  → Responsibility Requirement      （WHAT：需要什么责任能力）
    → Organization Routing          （WHO：谁承担，动态求解）
      → Responsibility Holder       （当前责任持有人）
        → Current Executor         （当前执行人，可为 none / 等待）
          → Employee / Team        （具体岗位）
            → Execution Binding    （绑定到具体任务实例）
              → Agent / Skill / Tool / Connector （HOW：能力）
```

**三句判诀**：
- **Process asks WHAT**（声明责任需求）
- **Organization decides WHO**（动态路由求解）
- **Capability determines HOW**（能力决定如何执行）

**禁止固定 DAG**：不写死「字幕永远由员工 X 做」。路由是运行期按上下文求解，随 Employee/Team/Capacity 演化而变化。

**DELTA 1 补充**：上述链中的 `Employee / Team` 属于 Company 的 **Organization** 轴（Company → Organization → Department/Team/Role/Employee），与 `Office` 正交。Employee 经 **Responsibility Assignment** 服务 Office，**不隶属于 Office**。Office 是经营单元（Company → Business/Operating Context → Office），不是组织节点。

---

## 2. Responsibility Requirement（流程只声明这个）

Process 中的每个节点声明**责任需求**，而非具体执行人。候选责任族：

```
Topic Research      （选题研究）
Script Writing      （脚本）
Video Production    （视频生产）
Subtitle Production （字幕）
Content Review      （内容审核）
Channel Adaptation  （渠道适配）
Engagement Handling （互动处理）
Analytics Synthesis （数据复盘）
...
```

每个 Responsibility Requirement 可带**约束**（非执行人）：

- `required_capability`（需要什么能力，如「字幕生成」）
- `required_specialty`（专业，如「中文视频字幕」）
- `required_content_type`（如 VIDEO / NOTE）
- `required_platform_experience`（如 DOUYIN / XHS）
- `required_language`（如 zh-CN）
- `account_context`（该责任发生在哪个 Channel Account 的上下文）

---

## 3. Organization Routing（动态求解 WHO · DELTA 2：确定性机械调度）

**输入**：Responsibility Requirement + Account Context + 候选 Employee/Team 属性 + Capacity/Availability。

**匹配维度**（候选）：
`capability` / `specialty` / `platform_experience` / `content_type` / `language` / `style` / `capacity` / `availability`

**输出**：Responsibility Holder → Current Executor。

**路由结果形态**：
- 单人空闲且匹配 → 直接指派 Employee
- 多人均匹配 → 按 capacity/availability/load 选最优（**确定性规则，不调用 LLM Team Lead**）
- 已有同 specialty Team → Router **确定性分派**给空闲成员（常规 Assignment 属 Router，非 Team Lead）
- 单 Employee 持续超载 → 触发 Bottleneck Candidate（见 §6），建议建 Team

> **DELTA 2 — Router 与 Team Lead 职责分离**：正常任务路由是 **确定性、低成本** 的机械调度（eligibility / capability / availability / queue / capacity / auto-assignment）。**每任务不得调用 Team Lead 决策**。Team Lead 仅在**异常 / 管理判断**时介入（见 §5）。目标：避免每个任务都经过额外 LLM Team Lead，降低 Token / latency / complexity。

**硬约束**：路由由系统在后台求解，**不要求普通用户配置任何 Routing Rule**。

---

## 4. Employee（可跨 Office / Account 共享）

**示例**：Subtitle Employee 职责 =「为公司所有视频生产字幕」，可同时服务 Douyin Office / XHS Office / Bilibili Office，**不必复制**为「Douyin字幕员工 / XHS字幕员工 / B站字幕员工」。

| 属性 | 说明 |
|---|---|
| `capability` | 拥有的能力（如字幕生成） |
| `specialty` | 专业（中文视频字幕 / 英文 / 特效字幕） |
| `platform_experience` | 平台经验（DOUYIN / XHS / BILIBILI…） |
| `content_type` | 内容类型（VIDEO / NOTE / IMAGE_SET） |
| `language` | 语言 |
| `style` | 风格（可与 Channel Account 的 tone_style 匹配） |
| `capacity` | 容量（可并行/单位时间处理量） |
| `availability` | 可用性（在线/负载） |

> Employee 是**动态调用能力的岗位**（Curis 四原则之一），非固定 Agent。其 `platform_experience` / `style` 可与 Channel Account 的 `tone_style` / `language` 自动匹配，实现「同一员工服务多账号」而无需复制。

---

## 5. Team 自然演化（J 节）

```
早期：  Subtitle Employee A → 服务所有视频
增长：  Subtitle Employee A / B / C
再增长：Subtitle Team
        ├ Team Lead
        ├ Employee A
        ├ Employee B
        └ Employee C
```

**Team Lead 责任（DELTA 2：仅管理判断 / 异常，非机械调度）**：

Team Lead 是 **Employee / Role**（运行层管理角色），**不是新的系统 primitive**。正常机械调度（Queue / Assignment / Load balancing / auto-assignment）由 **Organization Router** 确定性完成（§3），Team Lead **不介入**每个任务。

Team Lead 只在**异常 / 管理判断**时介入：
- `Priority Conflict`（优先级冲突裁决）
- `Blocker`（阻塞处理 / 升级）
- `Quality / Acceptance`（验收与质量把关）
- `Exception Handling`（异常处置）
- `Standards / Coaching`（标准制定与辅导）
- `Abnormal Workload Intervention`（异常负载干预，如突发积压）

**分组维度不强制**：允许按职能（字幕 Team / 脚本 Team）或按平台（Douyin Team / Bilibili Team / Overseas Team）。Curis 不规定。

---

## 6. Capacity / Queue / Bottleneck（DELTA 3：首版降复杂度，暂不 Frozen）

**候选成为 Company OS Shared Runtime Candidate**：✅ 方向是。

**DELTA 3 — 首版降复杂度**：方向保留，但首版**不建设**完整 throughput 预测 / 复杂 capacity score / 智能负载算法 / 企业级 scheduler。

**首版最小 Runtime Facts（仅观测）**：
1. `queue_depth`（某 Responsibility 当前排队深度）
2. `waiting_since` / `oldest_wait`（最旧任务等待时长）
3. `active_count`（在制数量）
4. `employee_availability`（相关 Employee 可用性）

→ 由上述事实直接产生 **Bottleneck Candidate**（如某 Responsibility `oldest_wait` 持续超阈值）。

**一键「增加员工」建议**：Bottleneck Candidate 触发 → CEO Assistant 白话汇报（「最近视频经常卡在字幕环节，建议增加一名字幕员工。」）→ 用户 `[按建议增加]` / `[先不增加]` → 后台完成 Employee 创建 + 加入 Routing Pool + Capacity 更新 + Responsibility 指派。

**演化路径**：Runtime Facts + Bottleneck Candidate（首版）→ Team Lead 异常干预 / 负载均衡（规模增长后）→ throughput 度量 / 自适应 capacity / Team scheduling（确有需要才出现，不预设）。

---

## 7. 普通用户简化（K 节硬约束）

**首版用户可见概念**：`Office` · `AI Employee` · `Connected Accounts` · `Current Work` · `Needs CEO`。

**后台不可见**：Organization Router / Capacity / Queue / Load balancing / Team topology。

**瓶颈自管示例**：
```
系统检测到：字幕责任 oldest_wait（最旧任务等待）持续升高，上游产出 > 字幕处理能力
  → CEO Assistant 汇报：「最近视频经常卡在字幕环节。建议增加一名字幕员工。」
  → 用户：[按建议增加] / [先不增加]
  → 后台：Employee 创建 → Routing Pool → Capacity 更新 → Responsibility 指派
```

用户**永远只做二选一**，不接触组织设计。

---

## 8. 与运行层（全自动任务流）的衔接

本架构直接服务 Curis 产品主轴「四原则不可动摇」：
- **全自动任务流是核心**：Process→Routing→Executor→Capability 全自动串联。
- **能力可替换不写死**：Capability Provider（Agent/Skill/Tool/Connector）可替换。
- **员工=动态调用能力的岗位**：Employee 是岗位，由 Org Router 动态绑定到责任。
- **让「目标→执行→验收→返工→完成」更自动**：Bottleneck 自检 + 一键增员闭环正是「更自动」的体现。

---

## 9. 开放问题

1. Responsibility Requirement 的约束能否引用 Channel Account 的 `tone_style` 做风格匹配？
2. **（DELTA 2 已定）Team Lead 是否介入每个任务路由？** 否。正常 Assignment 由 Router 确定性完成；Team Lead 仅介入异常/管理判断（priority conflict/blocker/quality/exception/standards/abnormal workload）。Lead 本身作为 Employee/Role 仍可由 Router 在异常时路由。
3. Capacity 信号的首版阈值如何设定（静态规则 / 自适应基线）？
4. 用户拒绝「增加员工」建议后，系统是否降级（暂停部分 Production / 排队）？
5. 多 Company 共享同一 Employee 池是否允许（本模型限定单 Company 内）？

---

## DELTA 2/3 应用记录（本轮批准）

- **DELTA 2 — Router / Team Lead 分离**：Router 确定性机械调度（eligibility/capability/availability/queue/capacity/auto-assignment），不逐任务调 Team Lead；Team Lead 仅异常/管理判断（priority conflict/blocker/quality/acceptance/exception/standards/coaching/abnormal workload），仍是 Employee/Role（见 §3、§5）。
- **DELTA 3 — 首版 Capacity 降复杂度**：首版只采集 Runtime Facts（queue_depth/waiting_since/oldest_wait/active_count/employee_availability）→ Bottleneck Candidate，不建 throughput 预测/capacity score/智能负载/企业级 scheduler（见 §6）。
- DELTA 1（Office/Org 正交）见 §1、Doc 1 §G、Doc 2。

---

*组织/路由架构草案，未固化。将在 Org Routing Contract 设计中与 Office / Intent Contract 一并裁定。*
