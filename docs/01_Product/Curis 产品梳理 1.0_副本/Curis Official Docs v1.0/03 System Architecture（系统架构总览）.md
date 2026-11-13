# Curis Official Docs v1.0

# 03 System Architecture（系统架构总览）

版本：v1.0

---

# 1. 架构定位

Curis采用：

> AI工作组织操作系统架构（AI Work Organization OS）

---

系统目标：

将：

```
用户目标

↓

AI组织

↓

AI员工

↓

AI能力

↓

业务执行

↓

成果沉淀
```

形成完整闭环。

---

# 2. 顶层架构

Curis整体分层：

```
Curis Platform

├── Experience Layer（体验层）

├── Workspace Layer（工作空间层）

├── Organization Layer（组织层）

├── AI Employee Layer（AI员工层）

├── Capability Layer（能力层）

├── Execution Layer（执行层）

├── Intelligence Layer（智能层）

├── Knowledge Layer（知识层）

└── Infrastructure Layer（基础设施层）
```

---

# 3. Experience Layer（体验层）

## 定义

用户与Curis交互的入口。

---

包含：

- Desktop App；
- Workspace UI；
- AI秘书；
- 项目界面；
- 员工界面。

---

核心原则：

用户操作：

业务目标。

---

而不是：

直接操作模型和工具。

---

# 4. Workspace Layer（工作空间层）

## 定义

用户日常工作的主要空间。

---

负责：

- 公司空间；
- 项目；
- 任务；
- 成果。

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

## 定义

管理AI组织结构。

---

负责：

```
Company

↓

Department

↓

Employee
```

---

作用：

让AI能力以组织形式存在。

---

# 6. AI Employee Layer（AI员工层）

## 定义

Curis执行工作的核心。

---

AI员工包含：

```
Identity

↓

Role

↓

Responsibility

↓

Capability Profile

↓

Memory

↓

Project
```

---

员工负责：

理解职责。

管理任务。

调用能力。

产生结果。

---

# 7. Capability Layer（能力层）

## 定义

统一管理所有AI能力。

---

结构：

```
Capability

├── Model

├── Agent

├── Skill

├── Tool

├── Workflow

└── Connector
```

---

核心原则：

Curis不绑定单一AI工具。

---

例如：

研发能力：

```
Software Development Capability

=

Coding Agent

+

Claude/Codex

+

Git

+

Testing Workflow
```

---

# 8. Model Gateway（模型网关）

属于Capability层。

---

作用：

统一接入模型。

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

支持：

- OpenAI；
- Anthropic；
- Google；
- New API；
- 本地模型。

---

MVP：

人工选择模型。

---

未来：

智能选择模型。

---

# 9. Execution Layer（执行层）

## 定义

负责真正执行任务。

---

流程：

```
Task

↓

Execution Runtime

↓

Agent

↓

Capability

↓

Result
```

---

负责：

- Agent调用；
- Tool调用；
- Workflow执行；
- 状态管理。

---

# 10. Execution Runtime（执行运行时）

核心职责：

管理一次AI执行生命周期。

---

包括：

```
Execution

├── Task

├── Context

├── Agent

├── Capability

├── Events

└── Result
```

---

# 11. Intelligence Layer（智能层）

## 定义

Curis未来智能化核心。

---

包括：

## Orchestration

智能调度。

---

## Context Engine

上下文生成。

---

## Decision System

决策辅助。

---

MVP阶段：

基础存在。

智能程度降低。

---

# 12. Context Engine（上下文引擎）

## 定义

解决：

长期工作上下文问题。

---

输入：

```
Task

+

Project State

+

Memory

+

Knowledge
```

---

输出：

```
Context Package
```

---

目标：

减少Token消耗。

避免加载全部历史。

---

# 13. Knowledge Layer（知识层）

## 定义

管理组织知识资产。

---

结构：

```
Source

↓

Document

↓

Knowledge

↓

Knowledge Graph
```

---

来源：

- 文件；
- Obsidian；
- Git；
- Connector。

---

# 14. Memory Layer（记忆系统）

## 定义

保存AI长期经验。

---

层级：

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

作用：

让AI持续工作。

---

# 15. Infrastructure Layer（基础设施层）

包括：

## Backend Services

提供：

业务服务。

---

## Database

保存：

业务数据。

---

## Vector Storage

支持：

知识检索。

---

## Local Runtime

连接：

用户本地环境。

---

# 16. Local Runtime Architecture（本地运行架构）

结构：

```
Curis Desktop

↓

Local Bridge

↓

Local Capability

↓

External Application
```

---

支持：

- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor；
- Git。

---

# 17. Backend服务架构

采用：

模块化架构。

---

核心服务：

```
Workspace Service

Organization Service

Project Service

Task Service

Employee Service

Capability Service

Execution Service

Knowledge Service

Memory Service

Context Service

Analytics Service
```

---

# 18. 数据流架构

完整流程：

```
用户输入

↓

Workspace

↓

Task

↓

Context Engine

↓

Execution Runtime

↓

AI Employee

↓

Capability

↓

Result

↓

Memory
```

---

# 19. MVP架构范围

MVP实现：

```
Workspace

+

Organization

+

Employee

+

Project

+

Task

+

Capability

+

Execution

+

Artifact

+

Basic Memory
```

---

暂不实现：

- 智能调度；
- 自动Agent组队；
- Marketplace；
- 企业Admin。

---

# 20. 架构扩展原则

未来扩展：

不改变核心模型。

---

增加：

```
Admin

Marketplace

Enterprise

Developer Platform
```

---

通过：

Capability。

Template。

Connector。

扩展。

---

# 21. 架构核心原则

## 原则1

业务不直接绑定模型。

---

## 原则2

AI工具属于Capability。

---

## 原则3

员工是执行主体。

---

## 原则4

项目是业务容器。

---

## 原则5

Memory和Knowledge支撑长期智能。

---

# 本文档状态

状态：

Active

---

用途：

定义Curis整体技术架构。

所有新功能必须判断：

是否符合该架构。

---

下一篇：

# 04 AI Organization Model（AI组织模型）