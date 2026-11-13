# WorkBuddy / Admin 团队跨线协作与当前开发规则

日期：2026-07-17  
状态：立即生效  
适用：WorkBuddy 产品规划席、系统交付席、质量运行席、安全边界席、总控决策席

## 一、当前目标

Admin 暂停扩展新行业、新商业包、Marketplace、真实计费和前端页面。

当前只把已有官方资产修到“真实可查、可引用、可实例化、可被 Workspace 消费”。

当前重点：

- 修复官方资产悬空引用和空壳数据；
- 确认 Company Package 能真实生成部门、员工和 Workflow；
- 补必要的只读 Catalog 接口；
- 建立资产完成度标准；
- 处理孤儿实例和 Admin 安全问题；
- 收到 Workspace 跨线请求后，按共享 Issue 自主响应。

## 二、Admin 团队负责什么

Admin 负责：

- Company、Department、Employee、Persona、Skill、Tool、Workflow、Dashboard 模板；
- Company Package、Capability Package 和官方目录；
- 官方资产版本、状态、生命周期和事实源；
- Admin 治理、目录接口和平台安全。

Admin 不负责：

- 修改 Workspace 运行实例；
- 直接改 Task、Workflow Runtime 或 Employee Session；
- 替 Workspace 完成执行链；
- 修改 CEO Office 或其他 Workspace 前端；
- 未经 L2 Gate 启用外部平台、真实计费或 Marketplace。

## 三、什么时候需要 Codex / Workspace 配合

遇到以下情况，必须创建跨团队请求，不再让用户人工传话：

- 需要确认模板如何映射为 Workspace 实例；
- 需要真实实例化或运行证据；
- 需要确认 Workspace 所需字段、ID和版本快照；
- 资产已修复，但必须由 Workspace 证明能消费；
- 目录接口变更可能影响运行时；
- 需要确认 official 资产与 tenant_private 实例边界。

## 四、跨团队协作方式

以仓库中的共享 Issue 作为唯一事实源：

```text
issues/shared/YYYYMMDD_admin_<主题>.md
```

状态统一使用：

```text
OPEN
→ ACKNOWLEDGED
→ IN_PROGRESS
→ READY_FOR_VERIFY
→ VERIFIED
→ CLOSED
```

触发 L2 Gate 时改为：

```text
BLOCKED_L2
```

工作规则：

1. 每轮工作开始和结束时检查 `issues/shared/`。
2. 收到 Workspace 的 `OPEN` 请求后，产品规划席先改为 `ACKNOWLEDGED`。
3. 在已批准边界内，自主创建内部 Issue、实现、测试并提交。
4. 涉及新商业模式、外部平台、权限边界或跨产品架构时，标记 `BLOCKED_L2`。
5. 完成后写清 API、资产 ID、版本、commit 和测试证据，将状态改为 `READY_FOR_VERIFY`。
6. 不直接修改 Workspace Runtime 或前端。
7. Workspace 验证通过后才算真正关闭。

## 五、Shared Issue 必填内容

```markdown
# 标题

状态：OPEN
发起团队：Admin
目标团队：Workspace
归属模块：
是否阻塞：是 / 否
是否触发 L2：是 / 否

## 结论
需要 Workspace 确认或完成什么。

## 真实证据
数据库、接口、种子、实例化代码或测试结果。

## 需要 Workspace 完成
只写清楚消费、映射或验证要求。

## Admin 验收方式
怎样证明资产已被真实使用。

## 禁止越界
不能修改哪些边界。
```

## 六、向 Workspace 回传必须包含

```markdown
## Admin 交付结果

结论：
已完成 / 未完成。

修改内容：
资产、接口、ID映射或数据修正。

事实源：
权威表、API和版本。

交付证据：
commit、测试命令、查询结果。

Workspace 应执行：
具体消费或验证动作。

风险：
无则写“无”。
```

## 七、资产完成标准

任何官方资产只有同时满足以下条件才可标记“已真实可用”：

```text
有真实内容
+ 有稳定 ID 和版本
+ 引用目标真实存在
+ 有只读消费接口
+ 可被 Workspace 实例化或绑定
+ 有自动测试和真实验证证据
```

只有文档、表结构、占位行、字符串步骤或 mock，不得称为“已完成”。

## 八、汇报规范

所有汇报使用中文白话：

- 结论：发生了什么；
- 原因：为什么；
- 建议：下一步怎么做。

不得用大量术语掩盖空壳、悬空引用或未实现执行能力。
