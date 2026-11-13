# Curis Product Bible

# 36 技术架构规范（Technical Architecture）

版本：v1.0-draft

---

# 1. 架构定位

技术架构用于支撑 Curis 产品模型。

核心目标：

- 支撑个人桌面应用；
- 支撑 AI 员工体系；
- 支撑业务模板扩展；
- 支撑未来 Workspace / Admin 拆分；
- 支撑多模型、多 Agent、多工具接入。

---

# 2. 总体架构

Curis 采用分层架构：

```
用户层

↓

Workspace 产品层

↓

业务服务层

↓

AI能力层

↓

执行层

↓

数据与知识层
```

---

# 3. 用户层

负责：

用户交互。

包括：

- 桌面应用；
- UI；
- AI秘书；
- 页面交互。

---

用户不直接接触：

- Model；
- Runtime；
- Tool调用；
- Workflow节点。

---

# 4. Workspace 产品层

负责：

业务体验。

包含：

- 首页；
- 项目；
- 会议室；
- 组织中心；
- 能力中心；
- 资料中心；
- 成果中心；
- 数据洞察；
- 经营分析。

---

Workspace负责：

将底层能力包装成用户可理解的业务流程。

---

# 5. 业务服务层

围绕核心对象。

包括：

## Organization Service

管理：

- 公司；
- 部门；
- 员工。

---

## Project Service

管理：

- 项目；
- 工作区；
- 项目状态。

---

## Task Service

管理：

- 任务；
- 执行状态；
- 生命周期。

---

## Artifact Service

管理：

- 成果；
- 版本；
- 验收。

---

## Meeting Service

管理：

- 会议；
- 讨论；
- 决策。

---

## Template Service

管理：

- Business Definition；
- 项目模板；
- 工作区定义。

---

# 6. AI能力层

负责统一接入：

## Model

例如：

- GPT；
- Claude；
- Gemini；
- 本地模型。

---

## Agent

例如：

- 编程Agent；
- 内容Agent；
- 数据Agent。

---

## Skill

例如：

- 分析；
- 生成；
- 优化。

---

## Tool

例如：

- 浏览器；
- 文件；
- Git。

---

## MCP

连接外部能力。

---

# 7. 能力路由层

Capability Router。

负责：

根据任务选择能力。

考虑：

- 员工角色；
- 任务类型；
- 成本；
- 性能；
- 可用状态；
- 用户配置。

---

例如：

研发任务：

选择：

代码Agent。

内容任务：

选择：

内容Agent。

---

# 8. 执行层

负责：

真正运行任务。

包括：

## Task Runtime

执行任务。

---

## Workflow Runtime

运行流程。

---

## Agent Runtime

管理Agent会话。

---

## Tool Executor

执行工具调用。

---

# 9. 工作流架构

Workflow：

不是业务。

是执行方式。

结构：

```
Workflow

↓

Node

↓

Capability

↓

Output
```

---

节点类型：

- Agent节点；
- Tool节点；
- 条件节点；
- 审批节点；
- 数据节点。

---

# 10. 知识层

知识系统：

负责：

资料。

知识。

Memory。

---

结构：

```
Source

↓

Parser

↓

Index

↓

Knowledge

↓

Memory

↓

Context
```

---

# 11. 数据层

保存：

## 业务数据

包括：

- 公司；
- 部门；
- 员工；
- 项目；
- 任务；
- 成果。

---

## 运行数据

包括：

- Workflow记录；
- Agent调用；
- Token；
- 成本。

---

## 知识数据

包括：

- 文件索引；
- 向量数据；
- Memory。

---

# 12. 本地执行架构

Desktop版本：

包含：

```
Curis Desktop

+

Local Bridge

+

本地资源
```

---

Local Bridge负责：

- 文件访问；
- Git；
- 本地命令；
- 项目目录。

---

# 13. 多模型架构

Curis 不绑定单一模型。

支持：

多个模型同时存在。

---

例如：

员工：

研发负责人。

能力：

首选：

Claude。

备用：

GPT。

---

系统根据：

任务。

成本。

状态。

自动选择。

---

# 14. 多Agent架构

支持：

多个Agent协作。

例如：

研发项目：

```
项目负责人Agent

↓

开发Agent

↓

测试Agent

↓

审查Agent
```

---

Agent之间：

通过：

任务。

成果。

上下文。

协作。

---

# 15. 数据流

典型流程：

```
用户目标

↓

AI秘书理解

↓

项目负责人规划

↓

任务生成

↓

Workflow执行

↓

调用能力

↓

生成成果

↓

经营分析

↓

经验沉淀
```

---

# 16. 扩展原则

新增能力：

优先：

增加：

- Capability；
- Skill；
- Tool；
- Workflow；
- Business Definition。

---

减少：

修改核心系统。

---

# 17. Workspace / Admin兼容

当前：

单体桌面应用。

---

架构预留：

未来拆分：

```
Admin

↓

模板

能力

治理


Workspace

↓

项目

员工

成果
```

---

# 18. 安全设计

关注：

- 凭证管理；
- 权限控制；
- 本地授权；
- 数据隔离；
- 操作审计。

---

# 19. 可观测性

系统需要记录：

- 执行状态；
- 错误；
- 成本；
- 调用链；
- 用户操作。

用于：

数据洞察。

问题排查。

优化。

---

# 20. 本章冻结内容

本章定义 Curis 技术架构方向。

核心：

产品对象驱动架构。

能力可插拔。

业务可扩展。

开发工具可替换。

下一章：

# 37 数据模型规范（Data Model Specification）