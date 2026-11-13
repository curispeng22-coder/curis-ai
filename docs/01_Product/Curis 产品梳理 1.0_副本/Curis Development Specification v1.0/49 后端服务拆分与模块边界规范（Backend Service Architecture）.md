# Curis Development Specification

# 49 后端服务拆分与模块边界规范（Backend Service Architecture）

版本：v1.0-draft

---

# 1. 系统定位

后端架构规范用于定义：

Curis后台系统如何组织服务。

目标：

- 保持模块独立；
- 支撑Workspace发展；
- 支撑未来Admin拆分；
- 支撑AI能力扩展；
- 降低业务耦合。

---

# 2. 核心理念

Curis不是传统业务系统。

后端需要同时支持：

```
业务对象

+

AI执行系统

+

知识系统

+

能力系统

+

数据系统
```

---

# 3. 服务架构总览

```
Curis Backend

├── API Gateway

├── Identity Service

├── Workspace Service

├── Organization Service

├── Project Service

├── Task Service

├── Agent Service

├── Capability Service

├── Workflow Service

├── Knowledge Service

├── Memory Service

├── Context Service

├── Analytics Service

└── Execution Runtime
```

---

# 4. API Gateway

## 定位

统一入口。

---

负责：

- 请求路由；
- 身份验证；
- 权限检查；
- API版本管理。

---

结构：

```
Client

↓

API Gateway

↓

Backend Services
```

---

# 5. Identity Service

## 定位

身份管理。

---

负责：

- 用户；
- 登录；
- 会话；
- Token；
- 权限身份。

---

未来支持：

- 企业账号；
- 多用户。

---

# 6. Workspace Service

## 定位

工作空间核心服务。

---

管理：

- 公司；
- 项目空间；
- 用户工作环境。

---

提供：

Workspace上下文。

---

# 7. Organization Service

## 定位

组织管理。

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

管理：

- 组织关系；
- 员工归属；
- 角色。

---

# 8. Project Service

## 定位

业务项目管理。

---

负责：

- 项目创建；
- 项目状态；
- 项目模板；
- 项目配置。

---

不负责：

任务执行。

---

# 9. Task Service

## 定位

执行任务管理。

---

负责：

- 创建任务；
- 任务状态；
- 任务生命周期。

---

关系：

```
Project

↓

Task

↓

Execution
```

---

# 10. Agent Service

## 定位

AI员工和Agent管理。

---

负责：

- Agent注册；
- Agent状态；
- Agent配置；
- Agent会话。

---

不负责：

具体模型调用。

---

# 11. Capability Service

## 定位

能力管理中心。

---

负责：

```
Model

Agent

Skill

Tool

Workflow

Connector
```

---

管理：

- 注册；
- 配置；
- 权限；
- 状态。

---

# 12. Model Gateway Service

## 定位

模型统一调用。

---

负责：

- Provider管理；
- 模型调用；
- Token统计；
- 成本统计。

---

关系：

```
Capability

↓

Model Gateway

↓

Provider
```

---

# 13. Workflow Service

## 定位

流程定义和管理。

---

负责：

- Workflow模板；
- 节点；
- 条件；
- 版本。

---

执行：

交给：

Execution Runtime。

---

# 14. Execution Runtime

## 定位

AI任务执行引擎。

---

负责：

- 调度执行；
- Agent调用；
- Tool调用；
- 状态管理。

---

流程：

```
Task

↓

Runtime

↓

Agent

↓

Capability

↓

Result
```

---

# 15. Knowledge Service

## 定位

知识管理。

---

负责：

- 资料来源；
- 索引；
- 搜索；
- 知识关系。

---

连接：

- Obsidian；
- Git；
- 文件；
- Connector。

---

# 16. Memory Service

## 定位

长期经验管理。

---

负责：

- Memory存储；
- 检索；
- 更新；
- 权限。

---

包括：

- 用户Memory；
- 员工Memory；
- 项目Memory。

---

# 17. Context Service

## 定位

上下文生成。

---

负责：

根据任务生成：

```
Task Context

+

Memory

+

Knowledge

+

Project State
```

---

输出：

Context Package。

---

# 18. Analytics Service

## 定位

数据分析。

---

负责：

- 指标；
- 成本；
- 使用情况；
- 经营数据。

---

不负责：

AI推理。

---

# 19. Notification Service

## 定位

消息通知。

---

负责：

- 任务完成；
- 异常；
- 审批；
- 提醒。

---

支持：

未来：

移动端通知。

---

# 20. Audit Service

## 定位

审计记录。

---

记录：

- 用户操作；
- AI执行；
- 权限变化；
- 外部调用。

---

# 21. 服务之间关系

核心链路：

```
Workspace

↓

Project

↓

Task

↓

Context Service

↓

Execution Runtime

↓

Agent Service

↓

Capability Service

↓

Result

↓

Memory
```

---

# 22. 数据边界原则

服务之间：

通过API通信。

---

避免：

直接访问其他服务数据库。

---

例如：

Task Service：

不直接修改：

Agent数据库。

---

# 23. 当前Desktop实现

第一阶段：

可以采用：

模块化单体。

---

结构：

```
Curis Backend

├── Module A

├── Module B

├── Module C
```

---

未来：

拆分微服务。

---

# 24. 为什么不立即微服务

原因：

早期：

业务变化快。

---

过早拆分：

增加：

- 部署复杂度；
- 调试成本；
- 运维成本。

---

优先：

模块边界清晰。

---

# 25. AI开发要求

AI开发Agent实现后端时：

必须遵守：

模块边界。

---

禁止：

为了快速实现：

跨模块修改核心逻辑。

---

# 26. API设计原则

统一：

REST API。

---

复杂执行：

采用：

Async Job。

---

例如：

```
POST /tasks/run

返回：

job_id
```

---

查询：

```
GET /jobs/{id}
```

---

# 27. 验收标准

后端架构完成后：

支持：

业务扩展。

AI能力扩展。

未来Admin拆分。

---

检查：

## 模块独立

职责清晰。

---

## 扩展性

新增能力无需修改核心。

---

## 稳定性

任务执行可追踪。

---

# 本章冻结内容

本章定义Curis后端服务架构。

核心：

Curis采用模块化架构。

当前保证开发效率。

未来支持平台化演进。

---

下一章：

# 50 数据库设计与数据治理规范（Database & Data Governance）