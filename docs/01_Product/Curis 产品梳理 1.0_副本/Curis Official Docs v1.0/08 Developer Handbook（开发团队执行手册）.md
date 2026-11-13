# Curis Official Docs v1.0

# 08 Developer Handbook（开发团队执行手册）

版本：v1.0

---

# 1. 手册定位

本文档是 Curis MVP 开发团队的主要执行入口。

目标：

让不同开发人员、不同AI开发工具：

- 理解同一个目标；
- 遵循同一架构；
- 使用同一代码主线；
- 按统一流程开发。

---

# 2. 开发团队模型

Curis采用：

```
一个开发团队

+

多个AI开发工具
```

---

不是：

```
Codex团队

↓

Workspace


WorkBuddy团队

↓

Admin
```

---

未来：

Codex、Claude Code、WorkBuddy、Trae、Cursor 等都是：

开发能力（Development Capability）。

---

# 3. 开发最高原则

---

# 原则1：产品优先

所有开发必须符合：

```
Curis Product Bible

↓

MVP Specification

↓

当前Task
```

---

禁止：

因为已有代码改变产品方向。

---

# 原则2：架构优先

开发必须遵循：

```
Product Model

↓

System Architecture

↓

Engineering Specification
```

---

禁止：

为了快速实现：

- 绕过架构；
- 创建孤立模块；
- 绑定单一AI工具。

---

# 原则3：能力抽象

Curis不直接绑定：

- GPT；
- Claude；
- Codex；
- 某个Skill。

---

统一：

```
Business

↓

Employee

↓

Capability

↓

Execution
```

---

# 原则4：单一代码主线

所有开发：

使用：

- 同一个Git仓库；
- 同一个开发分支体系；
- 同一套文档。

---

禁止：

不同AI工具维护不同版本。

---

# 4. 开发工作流程

标准流程：

```
需求

↓

Task

↓

读取上下文

↓

方案设计

↓

代码开发

↓

测试

↓

Review

↓

Merge
```

---

# 5. Task开发规范

任何开发不能直接开始编码。

必须先有：

Development Task。

---

Task包含：

```
Task ID

任务名称

目标

产品依据

技术依据

影响范围

实现方案

验收标准

测试要求
```

---

# 6. AI开发Agent使用规范

AI开发工具执行前：

必须读取：

---

## 产品上下文

包括：

- Product Bible；
- MVP规范。

---

## 技术上下文

包括：

- 架构文档；
- API规范；
- 数据规范。

---

## 当前任务上下文

包括：

- Task；
- 代码状态；
- 历史交接。

---

禁止：

依赖聊天记录作为唯一依据。

---

# 7. AI开发执行流程

AI Agent执行：

```
理解任务

↓

分析现有代码

↓

提出方案

↓

修改代码

↓

运行测试

↓

提交结果
```

---

复杂任务：

必须先输出：

Implementation Plan。

---

# 8. AI代码修改规范

每次修改必须记录：

```
修改文件

↓

修改内容

↓

修改原因

↓

影响范围

↓

测试结果
```

---

---

# 9. 前端开发规范

前端必须遵循：

## Design System

统一使用：

- Layout；
- Card；
- Button；
- AI组件。

---

禁止：

重复创建相似组件。

---

## 页面设计

页面必须符合：

```
Product Model

↓

Workspace

↓

业务流程
```

---

禁止：

开发旧版UI。

---

# 10. 后端开发规范

后端必须遵循：

模块边界。

---

核心模块：

```
Workspace

Organization

Employee

Project

Task

Capability

Execution

Knowledge

Memory
```

---

禁止：

业务直接调用模型。

---

正确：

```
Business

↓

Capability

↓

Model Gateway

↓

Provider
```

---

# 11. AI系统开发规范

AI相关开发必须考虑：

```
Agent

+

Prompt

+

Capability

+

Memory

+

Context
```

---

禁止：

只修改Prompt解决所有问题。

---

# 12. 数据开发规范

数据设计必须符合：

核心对象模型：

```
Company

Department

Employee

Project

Task

Artifact
```

---

新增数据：

必须考虑：

- 权限；
- 生命周期；
- 迁移。

---

# 13. API开发规范

所有API遵循：

统一接口规范。

---

要求：

- REST规范；
- 统一响应；
- 错误处理；
- 权限验证。

---

AI任务：

支持异步执行。

---

# 14. Git协作规范

分支：

```
main

正式版本


develop

开发主线


feature/*

功能开发


fix/*

问题修复
```

---

提交：

必须说明：

```
功能

修改范围

测试结果
```

---

# 15. AI工具切换规范

当：

- 模型额度耗尽；
- 更换AI工具；
- 开发人员交接；

必须生成：

Handoff Report。

---

内容：

```
当前任务

已完成内容

未完成内容

修改文件

技术决策

问题风险

下一步
```

---

# 16. 开发上下文管理

禁止：

加载全部历史聊天。

---

采用：

```
Project Context

+

Task Context

+

Code Context

+

Relevant Docs
```

---

目标：

减少Token消耗。

提高开发效率。

---

# 17. 代码Review规范

代码完成后检查：

---

## 产品符合

是否满足用户需求。

---

## 架构符合

是否符合Curis设计。

---

## 代码质量

是否：

- 清晰；
- 可维护；
- 可扩展。

---

## 安全

是否：

- 权限正确；
- 数据安全。

---

# 18. 测试规范

所有功能必须测试：

---

## 软件测试

- 单元测试；
- API测试；
- UI测试。

---

## AI测试

- Agent行为；
- Prompt效果；
- Capability调用。

---

## 数据测试

- 一致性；
- 权限。

---

# 19. 开发完成标准

任务完成必须满足：

```
功能完成

+

测试通过

+

代码Review

+

文档更新
```

---

不是：

代码能运行即可。

---

# 20. MVP开发重点

当前优先：

```
Workspace

↓

AI Employee

↓

Project

↓

Task

↓

Capability

↓

Artifact

↓

Memory
```

---

# 21. 当前禁止开发

MVP阶段禁止：

- Marketplace；
- 企业Admin；
- 自动智能调度；
- 自主Agent团队；
- 复杂生态系统。

---

# 22. 新需求处理

新增需求必须判断：

---

是否增强：

```
AI组织工作闭环
```

---

如果：

不是核心闭环。

进入：

Future Roadmap。

---

# 23. 开发团队每日执行入口

每天只关注：

```
当前Sprint

↓

当前Task

↓

相关规范

↓

代码实现
```

---

不要：

重新讨论产品方向。

---

# 本文档状态

状态：

Active

---

用途：

作为Curis MVP开发团队日常执行手册。

所有开发人员和AI开发工具必须遵循本手册。

---

下一篇：

# 09 Engineering Specification（工程实现规范）