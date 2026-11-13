# Curis Development Specification

# 48 前端状态管理与数据流规范（Frontend State & Data Flow）

版本：v1.0-draft

---

# 1. 系统定位

前端状态管理规范用于定义 Curis Desktop 前端如何：

- 管理用户状态；
- 管理业务对象状态；
- 管理AI执行状态；
- 管理实时数据；
- 保持页面之间的数据一致。

---

# 2. 核心理念

Curis不是传统后台系统。

前端需要同时管理：

```
用户交互状态

+

业务数据状态

+

AI执行状态

+

实时反馈状态
```

---

# 3. 状态分类

Curis前端状态分为：

```
Global State

↓

Workspace State

↓

Page State

↓

Component State
```

---

# 4. Global State（全局状态）

定位：

整个应用共享的数据。

---

包括：

## 用户状态

例如：

```
User

├── id

├── name

├── preferences

└── permissions
```

---

## 公司状态

例如：

```
Company

├── id

├── name

├── departments
```

---

## 当前上下文

包括：

- 当前公司；
- 当前部门；
- 当前项目；
- 当前员工。

---

## AI秘书状态

包括：

- 显示状态；
- 当前会话；
- 执行状态。

---

# 5. Workspace State

定位：

业务空间状态。

---

例如：

当前项目：

```
Project Workspace

├── Project

├── Tasks

├── Employees

├── Artifacts

├── Knowledge

└── Metrics
```

---

作用：

保证项目内部页面一致。

---

例如：

任务完成。

项目概览自动更新。

成果中心同步变化。

---

# 6. Page State

定位：

单页面状态。

---

例如：

项目列表页：

```
Project Page State

├── Filter

├── Sort

├── Pagination

└── Loading
```

---

例如：

能力中心：

```
Capability Page State

├── Category

├── Search

├── Selected Capability
```

---

# 7. Component State

定位：

组件内部状态。

---

例如：

弹窗：

打开。

关闭。

---

输入框：

内容。

验证。

---

不应该进入全局。

---

# 8. 数据流原则

采用：

单向数据流。

---

结构：

```
Data Source

↓

Service Layer

↓

State Store

↓

Component

↓

User Action

↓

Update State
```

---

# 9. Service Layer

前端不直接调用接口。

---

结构：

```
Component

↓

Service

↓

API

↓

Backend
```

---

例如：

项目：

```
ProjectService

↓

GET /projects
```

---

# 10. API数据缓存

支持：

缓存。

---

例如：

项目列表。

能力列表。

知识列表。

---

避免：

重复请求。

---

# 11. AI执行状态管理

这是Curis特殊部分。

---

需要管理：

```
AI Execution State

├── Task

├── Agent

├── Capability

├── Progress

├── Output

└── Error
```

---

# 12. 实时状态更新

支持：

AI任务运行时：

实时展示。

---

例如：

```
研发Agent

正在分析需求

↓

正在修改代码

↓

正在测试
```

---

方式：

支持：

- WebSocket；
- Event Stream；
- Polling。

---

# 13. Event驱动状态更新

推荐：

事件驱动。

---

例如：

后端发送：

```
task.completed
```

---

前端：

更新：

任务状态。

成果列表。

通知。

---

# 14. AI秘书状态

特殊处理。

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

UI根据状态变化。

---

# 15. Capability Switcher状态

管理：

当前工作模式。

---

例如：

```
Current Profile:

Software Development


Capabilities:

Codex

Git

Testing Workflow
```

---

切换后：

更新：

当前Task上下文。

---

# 16. Context Preview状态

用于展示：

AI当前使用什么信息。

---

包括：

Memory。

Knowledge。

Task Context。

---

状态：

加载。

完成。

更新。

---

# 17. 错误状态管理

统一：

Error Boundary。

---

错误类型：

## 网络错误

接口失败。

---

## 权限错误

无法访问。

---

## AI错误

Agent失败。

---

## 数据错误

数据异常。

---

# 18. 页面刷新恢复

支持：

状态恢复。

---

例如：

用户关闭应用。

重新打开：

恢复：

- 当前项目；
- 当前任务；
- AI秘书状态。

---

# 19. 本地缓存

支持：

本地保存：

- 用户设置；
- 最近项目；
- 页面状态；
- 离线数据。

---

敏感数据：

加密保存。

---

# 20. 与Backend关系

前端负责：

展示。

交互。

状态。

---

Backend负责：

业务逻辑。

数据。

执行。

---

避免：

前端实现复杂业务规则。

---

# 21. 与AI系统关系

前端展示：

AI状态。

---

不负责：

选择Agent。

选择模型。

---

流程：

```
用户操作

↓

Backend

↓

Orchestrator

↓

Agent

↓

Frontend展示
```

---

# 22. 验收标准

前端状态体系完成后：

用户可以：

流畅使用页面。

实时看到AI执行。

保持数据一致。

---

检查：

## 一致性

不同页面数据同步。

---

## 稳定性

异常状态可恢复。

---

## 扩展性

新增业务页面容易接入。

---

# 本章冻结内容

本章定义Curis前端状态和数据流规范。

核心：

前端负责体验和状态展示。

业务决策、AI调度、数据处理由后端和AI系统负责。

---

下一章：

# 49 后端服务拆分与模块边界规范（Backend Service Architecture）