# Curis Development Specification

# 64 Curis最终架构总览（Final Architecture Overview）

版本：v1.0-draft

---

# 1. 架构定位

本文档用于总结：

Curis经过产品、架构、开发规范整理后的最终系统架构。

目标：

建立：

```
个人AI工作系统

↓

AI员工组织平台

↓

企业AI操作系统
```

的长期演进基础。

---

# 2. 核心理念

Curis不是：

- AI聊天工具；
- 模型聚合工具；
- Agent集合；
- 自动化脚本平台。

---

Curis是：

> 管理AI员工、调度AI能力、组织知识、执行业务流程的AI工作操作系统。

---

# 3. 顶层架构

整体：

```
Curis Platform

├── Workspace Layer

├── Organization Layer

├── AI Employee Layer

├── Capability Layer

├── Execution Layer

├── Knowledge Layer

├── Intelligence Layer

└── Infrastructure Layer
```

---

# 4. Workspace Layer（工作空间层）

定位：

用户日常工作的入口。

---

负责：

- 公司空间；
- 项目；
- 任务；
- 成果；
- 业务工作区。

---

结构：

```
Workspace

↓

Project

↓

Task

↓

Artifact
```

---

# 5. Organization Layer（组织层）

定位：

定义AI公司的组织结构。

---

负责：

- 公司；
- 部门；
- 员工。

---

结构：

```
Company

↓

Department

↓

AI Employee
```

---

# 6. AI Employee Layer（AI员工层）

定位：

Curis核心业务执行主体。

---

AI员工拥有：

```
Employee

├── Role

├── Responsibility

├── Memory

├── Capability Profile

├── Project Relation

└── History
```

---

# 7. Capability Layer（能力层）

定位：

管理所有AI执行能力。

---

统一抽象：

```
Capability

├── Model

├── Agent

├── Skill

├── Tool

├── Workflow

├── Connector

└── Local Application
```

---

# 8. Capability Profile（能力模式）

定位：

用户侧简单交互。

---

将复杂能力组合为：

工作模式。

---

例如：

```
软件开发模式

=

开发Agent

+

Codex

+

Git Tool

+

测试Workflow
```

---

用户切换：

模式。

---

系统调整：

能力组合。

---

# 9. Execution Layer（执行层）

定位：

负责真正执行任务。

---

包含：

```
Task

↓

Workflow Runtime

↓

Agent Runtime

↓

Capability Execution
```

---

负责：

- Agent调用；
- Tool调用；
- Workflow执行；
- 状态管理。

---

# 10. Intelligent Orchestration Layer（智能调度层）

定位：

Curis执行大脑。

---

负责：

根据任务选择：

- Agent；
- Model；
- Skill；
- Tool；
- Workflow。

---

流程：

```
目标

↓

任务理解

↓

能力规划

↓

能力选择

↓

执行
```

---

# 11. Context Engine（上下文引擎）

定位：

解决长期工作上下文问题。

---

负责：

生成：

Task Context Package。

---

来源：

```
任务

+

项目状态

+

Memory

+

Knowledge
```

---

目标：

最少Token完成工作。

---

# 12. Memory Layer（记忆层）

定位：

让AI员工长期成长。

---

分层：

```
User Memory

↓

Employee Memory

↓

Project Memory

↓

Department Memory

↓

Company Memory
```

---

保存：

经验。

决策。

偏好。

最佳实践。

---

# 13. Knowledge Layer（知识层）

定位：

管理知识资产。

---

包括：

```
资料

↓

Knowledge

↓

Knowledge Graph

↓

Context调用
```

---

来源：

- Obsidian；
- Git；
- 文件；
- Connector。

---

# 14. Knowledge Graph（知识关系层）

定位：

连接：

知识之间的关系。

---

例如：

```
技术方案

↓

项目

↓

代码

↓

Bug

↓

解决方案
```

---

# 15. Model Gateway Layer（模型网关层）

定位：

统一管理模型来源。

---

支持：

- OpenAI；
- Claude；
- Gemini；
- New API；
- OpenRouter；
- 本地模型。

---

结构：

```
Model Gateway

↓

Provider

↓

Model
```

---

# 16. Local Runtime Layer（本地运行层）

定位：

连接用户电脑环境。

---

负责：

- 文件；
- Git；
- 本地Agent；
- 本地应用。

---

例如：

```
Curis

↓

Local Bridge

↓

Codex

Claude Code

Trae

WorkBuddy
```

---

# 17. API Layer（接口层）

定位：

连接所有系统。

---

包括：

```
Business API

AI Runtime API

Capability API

Knowledge API

Analytics API

Admin API
```

---

# 18. Data Layer（数据层）

管理：

```
Business Data

Execution Data

Knowledge Data

Memory Data

Analytics Data
```

---

要求：

- 可追踪；
- 可迁移；
- 可扩展。

---

# 19. Security Layer（安全层）

贯穿所有模块。

---

负责：

- 身份；
- 权限；
- 数据保护；
- 审计。

---

原则：

```
授权

↓

执行

↓

记录

↓

可撤销
```

---

# 20. Frontend Architecture（前端架构）

结构：

```
Application Shell

↓

Workspace UI

↓

Business Components

↓

AI Components

↓

Design System
```

---

核心组件：

- AI秘书；
- Capability Switcher；
- Agent状态；
- Task执行面板。

---

# 21. Backend Architecture（后端架构）

采用：

模块化架构。

---

核心模块：

```
Workspace Service

Organization Service

Project Service

Task Service

Agent Service

Capability Service

Knowledge Service

Memory Service

Context Service

Analytics Service
```

---

# 22. Admin与Workspace关系

当前：

单体Desktop。

---

未来：

```
Admin

↓

治理能力


Workspace

↓

业务执行
```

---

# 23. 开发模式

采用：

统一开发团队。

---

AI工具：

作为开发能力。

---

支持：

- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor。

---

统一：

```
代码仓库

+

文档体系

+

任务体系
```

---

# 24. 数据与AI闭环

完整闭环：

```
用户目标

↓

AI秘书

↓

项目

↓

AI员工

↓

能力调度

↓

任务执行

↓

成果

↓

分析

↓

Memory

↓

能力优化
```

---

# 25. Curis核心竞争力

不是：

模型。

---

不是：

单个Agent。

---

核心：

## AI员工组织模型

让AI像团队一样工作。

---

## Capability Orchestration

统一调度所有AI能力。

---

## Memory + Context

让AI长期工作。

---

## Knowledge System

让AI理解组织资产。

---

# 26. 当前开发原则

未来所有开发：

必须满足：

```
符合产品架构

↓

符合模块边界

↓

支持能力扩展

↓

支持长期演进
```

---

# 27. 最终目标

Curis最终成为：

```
个人AI工作系统

↓

AI团队管理平台

↓

企业AI操作系统
```

---

# 本章冻结内容

本章定义Curis最终架构总览。

核心：

Curis通过：

Workspace管理业务。

AI Employee承担职责。

Capability提供能力。

Orchestration负责调度。

Memory和Knowledge提供长期智能。

最终形成：

一个能够持续工作的AI组织系统。

---

下一章：

# 65 Curis MVP第一阶段实施规范（MVP Implementation Specification）