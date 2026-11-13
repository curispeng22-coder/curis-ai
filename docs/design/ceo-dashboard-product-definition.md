# CEO AI Company Dashboard 产品定义

状态：Phase-1B.5 CEO Dashboard Design Gate

日期：2026-07-10

归属：Workspace 产品规划席

## 产品定位

CEO Dashboard 是 CEO 经营 AI 公司的驾驶舱，不是任务列表，也不是平台后台。

它回答 CEO 的八个经营问题：

1. 公司是否健康运转？
2. 哪个研发部门正在工作，是否存在阻塞？
3. 哪些项目在推进、完成或存在风险？
4. 哪些 AI 员工可用、繁忙或停用？
5. 当前研发 SOP 运行到哪一步？
6. AI 消耗了多少 Token、调用了哪些模型、产生了多少估算成本？
7. 已记录哪些 AI 价值事件和预估影响？
8. 项目与公司知识是否在沉淀增长？

## 信息架构

```text
CEO Dashboard
  -> 公司总览
  -> 项目与 Workflow
  -> 员工与能力
  -> 消耗与成本
  -> 价值与知识
```

Dashboard 是 Company 上下文中的默认经营概览；Project 详情仍是启动 Workflow 和查看研发交付物的工作入口。

## 默认驾驶舱布局

| 区域 | 默认 Widget | CEO 关注点 |
| --- | --- | --- |
| 公司总览 | Company Health、Department Overview | 公司与研发部门是否可用、是否有阻塞 |
| 项目与 Workflow | Project Progress、Project Risk | 哪些项目在执行、哪个项目需要干预 |
| 员工与能力 | Employee Status、Employee Load、Employee Growth | 员工是否可分配、能力是否覆盖、是否有积累 |
| 消耗与成本 | Token Usage、Model Usage、AI Cost | 用量结构与估算消耗，不是账单 |
| 价值与知识 | Value Event、Estimated Impact、Knowledge Growth | 已确认/待确认的价值记录与知识沉淀 |
| 能力使用 | Skill Usage、Tool Usage | 哪些能力被使用、是否值得保留或补充 |

## CEO 操作边界

Dashboard 允许 CEO：

- 切换当前 Company、Project 范围和时间范围。
- 增加、删除、排序、折叠已批准的 Widget。
- 从 Widget 跳转到 Company、Project、Employee 或 Workflow 的详情页。
- 查看脱敏用量、估算成本、Value Event 记录和知识摘要。

Dashboard 不允许 CEO：

- 通过 Widget 修改官方 Template、官方能力目录或 Admin 配置。
- 在 Dashboard 中执行 Billing、支付、配额、Invoice、ROI 结算或 Marketplace 操作。
- 查看 tenant_private 明文密钥、凭据引用内容或 Provider 原始响应。
- 用 Widget 改写 Workflow Engine、Tool Router、Model Gateway 或 Credential Vault。

## 指标表达原则

- `AI Cost` 只展示 Usage Event 的 `estimated_cost` 聚合，明确标记为“估算消耗”，不是权威账单。
- `Value Event` 与 `Estimated Impact` 只展示已记录的估算价值及来源，不自动宣称 ROI，也不用于收费。
- `Company Health`、`Project Risk`、`Employee Growth` 在第一版优先展示可解释的事实状态和趋势；不引入黑箱评分模型。
- `Knowledge Growth` 仅统计已批准的 Project Memory / Knowledge 记录数量、更新时间和来源摘要，不解释知识质量。

## Phase-1B UI 范围建议

第一版采用单公司、可切换 Project 范围的紧凑经营页：顶部是 Company 状态与范围筛选，中部是项目/工作流/员工事实状态，下部是用量、价值和知识摘要。页面结构、文案、视觉优先级、空状态和关键交互必须先经产品规划席批准。

不做复杂大屏、可视化组织图、拖拽 BI、实时协同、预测模型或多公司比较。
