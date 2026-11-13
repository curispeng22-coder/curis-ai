# Curis Development Specification

# 47 前端设计系统实现规范（Frontend Design System Implementation）

版本：v1.0-draft

---

# 1. 系统定位

前端设计系统实现规范用于定义：

Curis如何将产品设计转化为：

- 可复用前端组件；
- 统一交互模式；
- 稳定页面结构；
- 可扩展业务工作区。

---

# 2. 与Product Bible关系

Curis文档体系：

```
Product Bible

定义：

产品目标

用户体验

页面设计


↓

Development Specification

定义：

技术实现


↓

Frontend Design System

定义：

组件如何实现


↓

页面代码
```

---

# 3. 核心目标

设计系统解决：

- 页面风格统一；
- 组件重复开发；
- 业务页面快速生成；
- AI工作场景特殊交互。

---

# 4. 设计系统结构

```
Frontend Design System

├── Design Token

├── Base Components

├── Layout Components

├── Business Components

├── AI Components

├── Data Components

└── Workspace Renderer Components
```

---

# 5. Design Token实现规范

Design Token负责：

将视觉规范转换为代码变量。

---

包括：

## Color Token

例如：

```ts
color.primary

color.background

color.success

color.warning

color.error
```

---

## Typography Token

包括：

```ts
font.title

font.body

font.caption

font.number
```

---

## Spacing Token

统一：

```ts
spacing.sm

spacing.md

spacing.lg
```

---

## Radius Token

例如：

```ts
radius.card

radius.button

radius.modal
```

---

## Shadow Token

用于：

- 卡片；
- 浮层；
- AI秘书。

---

# 6. Base Components基础组件

基础组件提供：

页面构建基础能力。

---

# Button

用途：

执行操作。

---

Props：

```
type

size

loading

disabled

onClick
```

---

状态：

- Default；
- Hover；
- Loading；
- Disabled。

---

# Input

用途：

输入。

---

支持：

- 文本；
- 搜索；
- Prompt输入。

---

# Select

用途：

选择配置。

---

例如：

- 模板；
- 员工；
- 能力。

---

# Card

用途：

信息展示。

---

用于：

- 项目；
- 员工；
- 成果；
- 能力。

---

# Modal

用途：

配置。

确认。

编辑。

---

# Table

用途：

结构化数据展示。

---

# Tag

用途：

状态标识。

---

例如：

```
运行中

完成

异常
```

---

# 7. Layout Components布局组件

---

# App Shell

Curis统一应用框架。

包含：

- Sidebar；
- TopBar；
- Main Content；
- AI Layer。

---

# Page Header

统一页面头部。

结构：

```
标题

描述

主要操作
```

---

# Split Panel

用于复杂工作页面。

---

例如：

左：

任务。

右：

AI执行。

---

# Drawer

用于快速查看详情。

---

例如：

点击员工。

展开员工详情。

---

# 8. Business Components业务组件

业务组件对应：

Curis核心对象。

---

# ProjectCard

展示项目。

字段：

```
name

status

stage

owner

progress
```

---

# EmployeeCard

展示AI员工。

字段：

```
name

role

status

capabilityProfile
```

---

# CapabilityCard

展示能力。

字段：

```
name

type

provider

status
```

---

# ArtifactCard

展示成果。

字段：

```
name

type

project

status
```

---

# WorkflowCard

展示流程。

字段：

```
name

nodes

status
```

---

# 9. AI Components人工智能交互组件

AI组件是Curis区别于普通软件的重要部分。

---

# AI Assistant Bubble

AI秘书组件。

---

支持：

- 悬浮；
- 拖动；
- 展开；
- 收起。

---

状态：

```
Idle

Thinking

Planning

Executing

Waiting

Completed

Error
```

---

# Capability Switcher

能力切换组件。

---

定位：

工作现场快速调整能力。

---

不是：

后台能力管理。

---

展示：

```
当前工作模式

软件开发模式


执行能力

Codex

Git Tool

测试Workflow
```

---

支持：

- Auto模式；
- 手动切换；
- 查看调度原因。

---

# Agent Status Card

展示：

AI员工当前状态。

---

例如：

```
研发负责人

当前任务：

首页开发


状态：

执行中
```

---

# AI Timeline

展示：

AI执行过程。

---

例如：

```
分析需求

↓

调用Agent

↓

执行任务

↓

生成成果
```

---

# Context Preview

展示：

AI当前使用上下文。

---

包括：

- Task Context；
- Memory；
- Knowledge。

---

# 10. Data Components数据组件

用于：

数据洞察。

经营分析。

---

# Metric Card

展示关键指标。

---

例如：

```
Token消耗

50000

变化趋势
```

---

# Chart

支持：

- 趋势；
- 对比；
- 分布。

---

# Timeline

展示：

历史过程。

---

# Status Indicator

展示：

运行状态。

---

# 11. Workspace Renderer组件

这是Curis业务扩展核心。

---

目标：

不同业务不重新开发页面。

---

结构：

```
Business Definition

↓

Workspace Schema

↓

Component Renderer

↓

Business Workspace
```

---

例如：

研发项目：

组合：

```
TaskBoard

+

CodeView

+

Artifact

+

Metric
```

---

内容项目：

组合：

```
ContentCard

+

Schedule

+

DataChart
```

---

# 12. 组件状态规范

所有组件统一支持：

---

## Loading

加载状态。

---

## Empty

空状态。

---

## Error

异常状态。

---

## Disabled

不可操作。

---

## Permission

权限限制。

---

# 13. 组件开发规范

新增组件必须定义：

---

## 用途

解决什么问题。

---

## Props

输入数据。

---

## Events

用户操作。

---

## State

状态变化。

---

## Example

使用示例。

---

# 14. 组件复用原则

优先：

组合已有组件。

---

避免：

页面内创建私有组件。

---

例如：

不要：

项目页面重新开发Card。

---

应该：

使用：

ProjectCard。

---

# 15. AI开发Agent使用规范

AI开发Agent读取：

- Product Bible；
- 页面规格；
- Design System。

---

开发时：

优先使用：

已有组件。

---

新增组件：

需要说明原因。

---

# 16. 与前端状态管理关系

Design System负责：

组件表现。

---

State Management负责：

数据和状态。

---

关系：

```
State

↓

Component Props

↓

UI Render
```

---

# 17. 验收标准

前端设计系统完成后：

开发团队可以：

快速创建页面。

保持统一体验。

支持动态工作区。

---

检查：

## 一致性

所有页面风格统一。

---

## 复用性

组件可以跨业务使用。

---

## 扩展性

支持未来模板系统。

---

# 本章冻结内容

本章定义Curis前端设计系统实现规范。

核心：

Product Bible定义产品体验。

Frontend Design System负责将体验转化为可维护、可扩展的前端组件体系。

---

下一章：

# 48 前端状态管理与数据流规范（Frontend State & Data Flow）