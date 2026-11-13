# Curis Development Specification

# 69 Curis开发任务管理与AI Agent执行规范（Task Execution Protocol）

版本：v1.0-draft

---

# 1. 规范定位

本文档定义：

Curis开发过程中，如何将产品需求转换为：

- 可执行开发任务；
- AI开发Agent任务；
- 代码提交；
- 测试验证；
- 交接记录。

---

# 2. 核心理念

开发任务不是：

“告诉AI写什么代码”。

---

而是：

```
产品目标

↓

开发任务

↓

上下文准备

↓

AI Agent执行

↓

代码结果

↓

验证验收
```

---

# 3. 任务层级模型

Curis开发任务采用：

```
Epic

↓

Feature

↓

Task

↓

Sub Task
```

---

# 4. Epic（开发主题）

定位：

较大的产品目标。

---

例如：

```
Epic:

AI员工体系建设
```

---

包含：

- Employee模型；
- 员工页面；
- 能力绑定；
- 状态管理。

---

# 5. Feature（功能）

定位：

具体产品能力。

---

例如：

```
Feature:

AI员工创建
```

---

包含：

- 创建页面；
- API；
- 数据模型；
- 测试。

---

# 6. Task（开发任务）

定位：

AI开发Agent可以执行的工作单元。

---

例如：

```
Task:

实现Employee创建API
```

---

包含：

- 输入；
- 输出；
- 文件范围；
- 验收标准。

---

# 7. Sub Task（子任务）

用于拆分复杂任务。

---

例如：

Employee API：

拆分：

```
数据库模型

↓

接口实现

↓

权限验证

↓

测试
```

---

# 8. 开发任务标准格式

每个Task必须包含：

```
Task ID

任务名称

目标

产品依据

技术依据

输入

输出

影响范围

验收标准

测试要求

状态
```

---

# 9. Task示例

```
Task ID:

EMP-001


名称:

实现AI员工创建


目标:

支持用户创建AI员工


产品依据:

AI Employee规范


技术依据:

Employee Service


输入:

员工名称

角色

部门


输出:

Employee对象


验收:

用户可以创建员工
```

---

# 10. AI Agent执行前准备

AI开发Agent执行任务前：

必须读取：

---

## 产品上下文

包括：

- Product Bible；
- 页面规范。

---

## 技术上下文

包括：

- 架构规范；
- API规范；
- 数据规范。

---

## 当前代码上下文

包括：

- 目录；
- 文件；
- 已有实现。

---

# 11. AI Agent执行流程

标准流程：

```
读取任务

↓

分析现状

↓

生成方案

↓

修改代码

↓

运行测试

↓

提交结果
```

---

# 12. 方案阶段要求

复杂任务不能直接编码。

必须先输出：

Implementation Plan。

---

内容：

```
当前问题

↓

实现方案

↓

修改文件

↓

技术影响

↓

风险
```

---

# 13. AI代码修改范围控制

AI Agent必须：

限制修改范围。

---

例如：

任务：

开发员工页面。

---

允许：

Employee相关文件。

---

禁止：

随意修改：

- 导航；
- 数据库；
- 核心架构。

---

除非：

说明原因。

---

# 14. AI任务上下文管理

禁止：

依赖历史聊天。

---

必须使用：

```
Task Context

+

Architecture Context

+

Code Context

+

Previous Handoff
```

---

# 15. AI开发结果格式

完成任务后：

必须输出：

```
完成内容

↓

修改文件

↓

实现方式

↓

测试结果

↓

遗留问题

↓

下一步建议
```

---

# 16. Git提交规范

每个Task完成：

必须：

```
检查状态

↓

Commit

↓

Push

↓

更新Task状态
```

---

Commit格式：

```
type(scope): description
```

---

例如：

```
feat(employee):

add employee creation api
```

---

# 17. Task状态管理

统一：

```
Backlog

↓

Ready

↓

Developing

↓

Testing

↓

Review

↓

Completed

↓

Archived
```

---

# 18. AI开发交接规范

当：

- 模型额度结束；
- 工具切换；
- 开发人员更换；

必须生成：

Handoff Report。

---

内容：

```
当前任务

完成内容

未完成内容

代码状态

技术决策

问题风险

下一步
```

---

# 19. 多AI工具执行

AI工具：

属于Capability。

---

例如：

```
Task:

重构代码


执行:

Claude Code
```

---

如果额度不足：

切换：

```
Claude Code

↓

Codex

↓

WorkBuddy
```

---

保持：

任务连续。

---

# 20. Task与Capability关系

任务提出：

需要什么能力。

---

例如：

代码任务：

需要：

```
Code Agent

+

Git Tool

+

Testing Workflow
```

---

MVP阶段：

人工配置。

---

未来：

智能调度。

---

# 21. Task与Memory关系

任务完成后：

判断是否产生长期经验。

---

如果：

有价值。

进入：

研发Memory。

---

例如：

保存：

“新增Capability必须同步更新Registry。”

---

不保存：

一次性错误日志。

---

# 22. Task与测试关系

每个任务必须定义：

测试方式。

---

包括：

- 单元测试；
- API测试；
- UI测试；
- AI行为测试。

---

# 23. Task验收原则

完成条件：

不是：

代码运行。

---

必须满足：

```
功能正确

+

架构正确

+

测试通过

+

文档更新
```

---

# 24. AI开发质量控制

AI生成代码必须检查：

---

## 产品符合

是否解决目标。

---

## 架构符合

是否破坏边界。

---

## 代码质量

是否可维护。

---

## 安全

是否存在风险。

---

# 25. MVP任务管理应用

MVP开发期间：

所有开发必须进入Task系统。

---

禁止：

直接修改代码。

---

流程：

```
需求

↓

Task

↓

AI执行

↓

Review

↓

Merge
```

---

# 本章冻结内容

本章定义Curis开发任务管理与AI Agent执行规范。

核心：

AI开发工具不是自由编码助手。

而是在统一任务、上下文、架构约束下执行开发工作的AI研发能力。

通过：

Task。

Context。

Git。

Review。

形成可持续AI研发流程。

---

下一章：

# 70 Curis MVP验收测试场景规范（MVP Acceptance Scenario）