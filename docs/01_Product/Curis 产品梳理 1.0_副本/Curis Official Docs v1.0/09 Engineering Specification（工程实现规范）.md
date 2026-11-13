# Curis Official Docs v1.0

# 09 Engineering Specification（工程实现规范）

版本：v1.0

---

# 1. 规范定位

本文档定义 Curis MVP 开发过程中的工程实现标准。

目标：

保证：

- 前端实现统一；
- 后端结构清晰；
- 数据模型稳定；
- API规范一致；
- AI能力可扩展。

---

# 2. 工程架构原则

Curis采用：

```
模块化架构

+

能力抽象

+

配置驱动

+

可扩展设计
```

---

# 3. 总体技术架构

```
Frontend

↓

API Layer

↓

Backend Services

↓

Execution Runtime

↓

Capability Layer

↓

External Provider
```

---

# 4. 前端工程规范

## 4.1 前端定位

前端负责：

- 用户体验；
- 页面展示；
- 状态管理；
- 用户交互。

---

前端不负责：

- AI决策；
- 模型选择；
- 业务核心逻辑。

---

# 4.2 前端结构

推荐：

```
Frontend

├── App Shell

├── Pages

├── Business Components

├── AI Components

├── Design System

├── State Management

└── Services
```

---

# 5. Design System规范

所有页面必须使用：

统一组件体系。

---

基础组件：

```
Button

Input

Card

Modal

Table

Tag
```

---

业务组件：

```
ProjectCard

EmployeeCard

CapabilityCard

ArtifactCard

WorkflowCard
```

---

AI组件：

```
AI Assistant

Capability Switcher

Agent Status

Task Execution Panel
```

---

# 6. 前端状态管理

采用：

统一状态管理。

---

状态分层：

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

禁止：

多个页面维护重复业务状态。

---

# 7. 前端数据流

统一：

```
Component

↓

Service

↓

API

↓

Backend

↓

Database
```

---

组件禁止：

直接访问数据库或业务服务。

---

# 8. AI交互规范

AI相关页面必须展示：

结构化状态。

---

例如：

任务执行：

```
任务目标

↓

执行员工

↓

当前能力

↓

执行状态

↓

成果
```

---

避免：

只有聊天记录。

---

# 9. 后端工程规范

## 9.1 后端定位

后端负责：

- 业务逻辑；
- 数据管理；
- 权限；
- AI执行协调。

---

# 9.2 模块划分

核心模块：

```
Workspace Service

Organization Service

Employee Service

Project Service

Task Service

Capability Service

Execution Service

Knowledge Service

Memory Service

Context Service

Analytics Service
```

---

# 10. 模块边界原则

模块之间：

通过API通信。

---

禁止：

直接访问其他模块内部数据。

---

例如：

错误：

```
Project Service

直接修改

Employee数据库
```

---

正确：

```
Project Service

↓

Employee API
```

---

# 11. 数据库工程规范

核心对象：

```
Company

Department

Employee

Project

Task

Artifact
```

---

所有数据需要考虑：

- 生命周期；
- 权限；
- 版本；
- 迁移。

---

# 12. 数据设计原则

## 数据来源明确

知道：

数据从哪里产生。

---

## 数据关系明确

知道：

对象如何关联。

---

## 数据可恢复

支持：

备份和迁移。

---

# 13. API工程规范

所有API遵循：

统一标准。

---

包括：

## REST规范

例如：

```
GET /projects

POST /projects
```

---

## 统一响应

成功：

```json
{
 "success":true,
 "data":{}
}
```

---

失败：

```json
{
 "success":false,
 "code":"ERROR",
 "message":"..."
}
```

---

# 14. 异步任务规范

AI任务通常耗时。

---

禁止：

同步等待。

---

采用：

```
创建任务

↓

返回job_id

↓

后台执行

↓

查询状态
```

---

例如：

```
POST /tasks/run
```

返回：

```
job_id
```

---

# 15. Capability工程规范

所有AI能力必须注册。

---

结构：

```
Capability

├── Name

├── Type

├── Provider

├── Input

├── Output

├── Permission

├── Cost

└── Status
```

---

# 16. Model Gateway规范

模型调用：

禁止：

业务直接调用模型API。

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

优势：

- 可替换模型；
- 可统计成本；
- 可统一管理。

---

# 17. Agent工程规范

Agent必须定义：

```
Identity

Role

Capability

Prompt

Memory Policy

Context Policy
```

---

Agent不是简单Prompt。

---

# 18. Workflow工程规范

Workflow定义：

业务执行流程。

---

结构：

```
Workflow

↓

Node

↓

Action

↓

Result
```

---

节点需要支持：

- 成功；
- 失败；
- 重试；
- 中断。

---

# 19. Memory工程规范

Memory不是日志。

---

保存：

长期有效经验。

---

包括：

```
User Memory

Employee Memory

Project Memory
```

---

不保存：

临时执行记录。

---

# 20. Context工程规范

Context目标：

最少信息完成任务。

---

生成：

```
Task Context

+

Relevant Knowledge

+

Relevant Memory
```

---

禁止：

每次加载全部历史。

---

# 21. 安全工程规范

所有执行：

必须经过：

```
Authentication

↓

Authorization

↓

Execution

↓

Audit
```

---

敏感信息：

必须加密。

---

# 22. 日志与监控

记录：

- API调用；
- AI执行；
- 错误；
- 成本。

---

注意：

日志默认不进入Memory。

---

# 23. 测试工程要求

必须覆盖：

## 软件测试

- 单元测试；
- API测试；
- UI测试。

---

## AI测试

- Agent行为；
- Prompt；
- Capability调用。

---

## 数据测试

- 一致性；
- 权限。

---

# 24. 部署规范

支持：

```
Development

↓

Testing

↓

Production
```

---

发布流程：

```
代码提交

↓

测试

↓

Review

↓

部署
```

---

# 25. MVP工程优先级

第一优先：

```
Workspace

↓

Employee

↓

Project

↓

Task

↓

Capability

↓

Artifact
```

---

第二：

```
Memory

Knowledge
```

---

第三：

```
智能调度

自动优化
```

---

# 26. 工程禁止事项

禁止：

- 业务绑定模型；
- 页面硬编码业务；
- 重复创建组件；
- 直接修改生产数据；
- 绕过Capability体系。

---

# 本文档状态

状态：

Active

---

用途：

定义Curis MVP工程实现标准。

所有前端、后端、AI开发必须遵循本规范。

---

下一篇：

# 10 Development Workflow（开发流程规范）