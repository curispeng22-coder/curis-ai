# ADR-0045：普通用户优先的 Desktop 产品重定基线

Status: Frozen

Date: 2026-08-14

## Decision

Curis 的产品定义从“让 CEO 配置并运行 Company OS”重定基线为：

> Curis 是一款把成熟 AI 工作能力组装成一家公司，并让普通用户能够统一使用、
> 管理、扩张和进化这家公司的 Desktop App。

Company OS 仍是固定经营语义，但不再要求普通用户先理解内部 Runtime、组织装配或能力门禁。
Workspace 是可以内嵌成熟 AI 产品的独立数字办公室，每个业务可以拥有不同的工作对象、布局、
员工、能力、节奏、结果和用户介入点。

## Product shape

Curis 保留六个主工作区域：

1. 首页 / CEO 工作台
2. 业务空间
3. 组织中心
4. 人才市场
5. 资料库
6. 会议

个人、公司、资源、连接、权限、主题、成本、帮助和数据维护进入左下角用户头像菜单。
CEO Assistant、搜索、最近工作、通知和上下文返回是跨层能力，不新增一级导航。

## User contract

用户主线固定为：

```text
用户表达意图
→ Assistant 形成最小方案
→ 用户确认关键边界
→ 首个可感知结果
→ CEO 工作台
→ 业务空间 / 独立 Workspace
→ AI 员工持续工作
→ 结果、证据、反馈和异常
→ CEO 决策
→ 公司进入下一轮调整
```

用户不应被迫先填写组织、岗位、Provider、Skill、Tool、Knowledge 或 Runtime 状态。
复杂能力必须存在，但通过渐进式披露、上下文缺口和人才市场 / 设置按需进入。

## Capability and Talent Market boundary

- 人才市场负责发现和扩展专家、Agent、Skill、Tool、Connector、工作方法和职业模板。
- 设置负责连接、授权、维护、撤销、成本和权限。
- 组织中心负责公司已经拥有谁、谁负责什么、怎样招聘和组队。
- Workspace 负责员工实际工作的业务现场。
- 目录可见不等于连接、验证、授权或可运行；运行前仍必须真实检查。

## Runtime boundary

Runtime、Simulation、Evidence、Acceptance、Decision 和 Rollback 继续作为真实性与可恢复性支撑，
但不能成为普通用户的默认产品语言。前台优先显示目标、责任、当前发生的事、结果、原因、负责人、
下一步和恢复动作。

## Consequences

- 现有唯一 Blueprint 必须在同一文件内回写本决策，不创建 Blueprint v2 平行真相。
- 旧总装配包、旧页面交互包和旧开发队列只能作为迁移参考。
- 新开发必须先完成壳层、First Value、CEO Desk、业务空间和一条独立 Workspace 结果链。
- 研发、小红书、抖音是可装配的首批 Workspace 模板；不预置“完善 Curis”任务，也不把三者伪装成固定实例。
- 页面、路由、Draft、目录可见、接口或 focused test 不能单独构成产品完成。

## Evidence

- `docs/01_Product/Curis_Product_Master_Map.md`
- `docs/01_Product/Curis_Product_Page_Map_v1.0.md`
- `docs/01_Product/Curis_Product_Rethink_Reasoning_2026-08-13.md`
- `docs/01_Product/Curis_Talent_Market_Product_Map.md`
- `docs/01_Product/Curis_Talent_Market_Integration_Contract.md`
- `docs/01_Product/Curis_Talent_Market_Resource_Audit.md`
- `docs/reviews/20260813_current_state_product_drift_audit/Curis_Current_State_and_Product_Drift_Audit.md`
