# Curis Official Docs v1.0

# 02 Product Model（产品模型与核心对象）

版本：v1.0

---

# 1. 产品模型定位

Curis采用：

> AI组织模型（AI Organization Model）

作为核心产品模型。

---

传统软件：

```
用户

↓

工具

↓

操作
```

---

Curis：

```
用户

↓

AI组织

↓

AI员工

↓

能力

↓

业务执行

↓

成果
```

---

# 2. 核心对象关系

Curis核心对象：

```
Company

↓

Department

↓

Employee

↓

Project

↓

Task

↓

Artifact
```

同时：

```
Employee

↓

Capability Profile

↓

Capability

↓

Execution
```

---

# 3. Company（AI公司）

## 定义

Company代表用户创建的AI工作组织。

---

用途：

管理：

- 部门；
- AI员工；
- 项目；
- 知识；
- 能力。

---

示例：

```
Curis Studio
```

---

## 属性

```
Company

├── Name

├── Description

├── Members

├── Departments

├── Projects

└── Knowledge
```

---

# 4. Department（AI部门）

## 定义

Department代表业务领域。

---

作用：

组织AI员工。

---

示例：

```
Curis Studio

├── 研发部

├── 内容部

├── 研究部

└── 运营部
```

---

## 部门职责

负责：

- 员工管理；
- 项目归属；
- 专业知识沉淀。

---

# 5. AI Employee（AI员工）

## 定义

AI Employee是Curis执行工作的核心单位。

---

不是：

模型。

不是：

Agent。

不是：

聊天窗口。

---

AI员工代表：

一个具有职责的数字员工。

---

## 员工结构

```
Employee

├── Identity

├── Role

├── Responsibility

├── Capability Profile

├── Memory

├── Projects

└── History
```

---

# 6. Employee Role（员工角色）

定义：

员工负责什么。

---

示例：

## 研发负责人

职责：

- 技术规划；
- 开发管理；
- 质量控制。

---

## 内容负责人

职责：

- 内容策略；
- 选题规划；
- 数据分析。

---

# 7. Capability Profile（能力配置）

## 定义

Capability Profile是员工工作的能力组合。

---

解决：

用户不需要直接管理大量模型和工具。

---

例如：

```
软件开发模式

=

开发Agent

+

Codex

+

Git

+

测试Workflow
```

---

## 关系

```
Employee

↓

Capability Profile

↓

Capability
```

---

# 8. Project（项目）

## 定义

Project是业务目标执行空间。

---

项目不是简单任务集合。

---

项目包含：

```
目标

团队

任务

资料

成果

状态

经验
```

---

## 示例

### 软件研发项目

目标：

开发AI工作台。

---

### 内容增长项目

目标：

提升账号影响力。

---

### 知识项目

目标：

建立行业知识库。

---

# 9. Task（任务）

## 定义

Task是项目中的具体执行单元。

---

任务来源：

- 用户创建；
- 项目拆解；
- 员工规划。

---

示例：

研发：

```
设计数据库

开发首页

修复Bug
```

---

内容：

```
分析热点

生成选题

制作内容
```

---

# 10. Artifact（成果）

## 定义

Artifact代表AI执行产生的价值输出。

---

包括：

- 文档；
- 代码；
- 图片；
- 视频；
- 数据报告；
- 文件。

---

## 成果关系

```
Task

↓

Execution

↓

Artifact
```

---

# 11. Capability（能力）

## 定义

Capability是Curis统一管理AI能力的抽象。

---

包括：

```
Model

Agent

Skill

Tool

Workflow

Connector
```

---

# 12. Model（模型）

负责：

提供基础AI推理能力。

---

例如：

- GPT；
- Claude；
- Gemini；
- 本地模型。

---

# 13. Agent（执行代理）

负责：

执行特定任务。

---

例如：

- 编码Agent；
- 分析Agent；
- 内容Agent。

---

# 14. Skill（技能）

负责：

专业能力增强。

---

例如：

- SEO分析；
- 热点分析；
- 文案生成；
- 数据分析。

---

# 15. Tool（工具）

负责：

操作外部资源。

---

例如：

- Git；
- 文件系统；
- 浏览器；
- 数据库。

---

# 16. Workflow（工作流程）

负责：

定义执行步骤。

---

例如：

内容生产流程：

```
热点分析

↓

选题

↓

文案

↓

审核
```

---

研发流程：

```
需求分析

↓

开发

↓

测试
```

---

# 17. Connector（连接器）

负责：

连接外部系统。

---

例如：

- GitHub；
- Obsidian；
- 云存储；
- 内容平台。

---

# 18. Knowledge（知识）

## 定义

组织可使用的信息资产。

---

来源：

- 文件；
- 文档；
- 项目资料；
- 外部系统。

---

# 19. Memory（记忆）

## 定义

AI长期工作经验。

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

# 20. Execution（执行）

## 定义

记录一次完整AI工作过程。

---

结构：

```
Task

↓

Context

↓

Agent

↓

Capability

↓

Result
```

---

# 21. 对象之间完整关系

最终模型：

```
Company

↓

Department

↓

Employee

↓

Project

↓

Task

↓

Execution

↓

Artifact


Employee

↓

Capability Profile

↓

Capability


Execution

↓

Memory

↓

Knowledge
```

---

# 22. MVP实现对象

MVP必须实现：

```
Company

Department

Employee

Project

Task

Capability

Artifact

Basic Memory
```

---

# 23. 未来扩展对象

未来增加：

```
Admin

Organization User

Marketplace

Template

Developer Ecosystem
```

---

# 本文档状态

状态：

Active

---

用途：

定义Curis产品核心对象。

所有功能设计、数据库设计、API设计必须围绕这些核心对象展开。

---

下一篇：

# 03 System Architecture（系统架构总览）