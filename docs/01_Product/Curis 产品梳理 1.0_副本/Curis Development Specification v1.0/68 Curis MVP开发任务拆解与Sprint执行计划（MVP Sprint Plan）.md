# Curis Development Specification

# 68 Curis MVP开发任务拆解与Sprint执行计划（MVP Sprint Plan）

版本：v1.0-draft

---

# 1. 规范定位

本文档用于将：

```
MVP产品范围

↓

具体开发任务

↓

Sprint执行计划
```

转换为开发团队可直接执行的开发路线。

---

# 2. MVP开发原则

MVP开发不是：

按页面开发。

---

不是：

按技术模块孤立开发。

---

采用：

```
用户价值闭环

↓

产品模块

↓

开发任务

↓

验收标准
```

---

# 3. MVP总体阶段划分

MVP分为：

```
Phase 1

基础Workspace


↓

Phase 2

AI组织体系


↓

Phase 3

业务执行能力


↓

Phase 4

Capability体系


↓

Phase 5

真实业务场景验证


↓

Phase 6

体验优化与稳定化
```

---

# Phase 1：Workspace基础建设

目标：

建立Curis运行基础。

---

## Sprint 1：应用基础框架

### Task 001

## Desktop Application Shell

实现：

- 应用框架；
- 页面路由；
- 全局布局；
- 基础导航。

---

验收：

用户可以进入Curis主要工作区域。

---

### Task 002

## Frontend Design System基础

实现：

- Layout组件；
- Card组件；
- Button组件；
- Modal组件；
- 状态组件。

---

依据：

第47章。

---

验收：

后续页面统一使用组件体系。

---

# Sprint 2：Workspace基础模型

目标：

建立AI公司的基础空间。

---

## Task 003

## Company系统

实现：

用户创建：

```
Company
```

包含：

- 名称；
- 描述；
- 基础配置。

---

## Task 004

## Department系统

实现：

部门管理。

---

例如：

```
研发部

内容部

研究部
```

---

## Task 005

## Workspace首页

展示：

- 公司状态；
- 项目；
- AI员工；
- 最近成果。

---

验收：

用户拥有自己的AI工作空间。

---

# Phase 2：AI组织体系建设

目标：

让Curis从工具变成AI组织。

---

# Sprint 3：AI Employee系统

---

## Task 006

## AI员工创建

实现：

创建：

```
Employee
```

配置：

- 名称；
- 角色；
- 职责。

---

## Task 007

## 员工能力绑定

实现：

员工绑定：

```
Capability Profile
```

---

例如：

```
研发负责人

↓

软件开发模式
```

---

## Task 008

## 员工状态展示

展示：

- 空闲；
- 工作；
- 完成；
- 异常。

---

验收：

用户可以管理AI员工。

---

# Phase 3：项目与业务执行

目标：

支持真实业务。

---

# Sprint 4：Project系统

---

## Task 009

## 项目创建

实现：

创建：

```
Project
```

包含：

- 目标；
- 团队；
- 状态。

---

## Task 010

## 项目工作台

展示：

```
目标

↓

团队

↓

任务

↓

成果
```

---

验收：

项目成为业务执行中心。

---

# Sprint 5：Task系统

---

## Task 011

## 任务管理

实现：

- 创建任务；
- 分配员工；
- 更新状态。

---

状态：

```
Pending

Running

Completed

Failed
```

---

## Task 012

## 任务执行记录

记录：

```
任务

↓

员工

↓

能力

↓

结果
```

---

验收：

用户可以推动业务执行。

---

# Phase 4：Capability体系

目标：

统一AI能力。

---

# Sprint 6：Capability Registry

---

## Task 013

## 能力注册中心

支持：

```
Model

Agent

Skill

Tool

Workflow

Connector
```

---

## Task 014

## Skill迁移

迁移已有：

Admin团队Skill。

---

例如：

- 热点分析；
- 文案；
- SEO；
- 图片生成；
- 数据分析。

---

转换：

```
旧Skill

↓

Capability

↓

员工能力
```

---

验收：

已有能力进入统一体系。

---

# Sprint 7：Model Gateway

---

## Task 015

## Provider管理

支持：

- OpenAI；
- Claude；
- Gemini；
- New API。

---

## Task 016

## 模型调用

实现：

```
Capability

↓

Model Gateway

↓

Provider
```

---

MVP：

手动选择。

---

验收：

系统可调用多模型。

---

# Phase 5：真实业务场景

目标：

验证Curis价值。

---

# Sprint 8：研发业务模板

实现：

软件研发流程。

---

包含：

```
研发负责人

↓

开发任务

↓

代码能力

↓

测试

↓

成果
```

---

验证：

Codex/Claude Code接入。

---

# Sprint 9：内容创作业务模板

实现：

内容增长流程。

---

包含：

```
内容负责人

↓

选题

↓

文案

↓

图片

↓

复盘
```

---

支持：

- 小红书；
- 抖音；
- 头条。

---

# Sprint 10：知识管理业务

实现：

知识工作流程。

---

包含：

- 文件连接；
- Obsidian连接；
- 知识调用。

---

# Phase 6：Memory与体验完善

目标：

形成长期使用能力。

---

# Sprint 11：基础Memory

实现：

## 用户Memory

保存：

偏好。

---

## 项目Memory

保存：

项目背景。

---

## 员工Memory

保存：

工作经验。

---

# Sprint 12：MVP体验优化

优化：

- UI；
- 性能；
- 稳定性；
- 错误处理。

---

# 4. MVP开发优先级

优先级：

```
P0

产品闭环


P1

AI员工


P2

Capability


P3

业务模板


P4

Memory


P5

体验优化
```

---

# 5. 每个Sprint输出

必须包含：

```
代码

+

测试

+

文档更新

+

演示版本

+

问题记录
```

---

# 6. AI开发工具协作

开发工具：

不是团队。

---

使用：

- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor。

---

统一：

```
Git

+

文档

+

Task

+

交接记录
```

---

# 7. Sprint验收

每个Sprint结束检查：

---

## 产品

是否符合MVP目标。

---

## 技术

是否符合架构。

---

## AI

是否正确调用能力。

---

## 用户体验

是否形成闭环。

---

# 8. MVP完成最终验收

必须达到：

用户可以：

```
创建AI公司

↓

创建部门

↓

创建员工

↓

创建项目

↓

配置能力

↓

执行业务

↓

获得成果

↓

沉淀经验
```

---

# 本章冻结内容

本章定义Curis MVP开发执行计划。

核心：

MVP按照完整产品骨架推进。

开发重点不是制作单点功能。

而是建立：

AI组织运行闭环。

---

下一章：

# 69 Curis开发任务管理与AI Agent执行规范（Task Execution Protocol）