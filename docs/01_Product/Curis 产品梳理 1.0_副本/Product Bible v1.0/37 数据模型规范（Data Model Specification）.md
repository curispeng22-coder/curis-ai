# Curis Product Bible

# 37 数据模型规范（Data Model Specification）

版本：v1.0-draft

---

# 1. 规范定位

数据模型用于定义 Curis 核心业务对象的数据结构。

目标：

- 支撑产品对象；
- 支撑业务扩展；
- 支撑 Workspace 与 Admin 演进；
- 保证不同模块使用统一数据。

---

# 2. 数据模型原则

## 2.1 产品对象优先

数据模型围绕：

- 公司；
- 部门；
- 员工；
- 项目；
- 任务；
- 成果；
- 能力；
- 资料。

建立。

---

## 2.2 业务扩展配置化

新增业务：

优先增加：

- Business Definition；
- Template；
- Field；
- Workflow。

而不是修改核心数据结构。

---

## 2.3 数据关联优先

对象之间通过关系连接。

例如：

员工参与项目。

项目产生成果。

任务调用能力。

资料服务项目。

---

# 3. 核心对象模型

---

# 3.1 Company

## 定义

AI公司的根对象。

---

## 基础字段

包括：

- id
- name
- description
- avatar
- status
- created_at
- updated_at

---

## 关联对象

拥有：

- Departments
- Projects
- Employees
- Knowledge
- Capabilities

---

# 3.2 Department

## 定义

业务组织单元。

---

## 基础字段

包括：

- id
- company_id
- name
- description
- owner_id
- status

---

## 关联对象

拥有：

- Employees
- Projects
- Department Knowledge
- Metrics

---

# 3.3 Employee

## 定义

AI员工对象。

---

## 基础字段

包括：

- id
- name
- role
- department_id
- personality
- status

---

## 能力关系

关联：

- Capabilities
- Skills
- Tools

---

## 记忆关系

关联：

- Employee Memory

---

# 3.4 Project

## 定义

业务执行中心。

---

## 基础字段

包括：

- id
- department_id
- template_id
- name
- description
- objective
- owner_id
- status

---

## 关联对象

拥有：

- Tasks
- Meetings
- Artifacts
- Knowledge
- Metrics
- Workspaces

---

# 3.5 Workspace Definition

## 定义

描述项目工作区如何生成。

---

字段：

- id
- business_definition_id
- modules
- fields
- layout
- workflows

---

作用：

告诉前端如何渲染业务页面。

---

# 3.6 Task

## 定义

执行单元。

---

字段：

- id
- project_id
- name
- description
- owner_id
- status
- priority
- workflow_id

---

## 关联：

- Inputs
- Outputs
- Runs
- Capabilities

---

# 3.7 Workflow

## 定义

任务执行流程。

---

字段：

- id
- name
- version
- nodes
- triggers
- conditions

---

关联：

- Tasks
- Capabilities

---

# 3.8 Artifact

## 定义

最终成果对象。

---

字段：

- id
- project_id
- task_id
- type
- title
- version
- status

---

关联：

- Files
- Reviews
- Releases

---

# 3.9 Capability

## 定义

AI执行能力。

---

字段：

- id
- type
- provider
- name
- version
- status
- config

---

类型：

- Model
- Agent
- Skill
- Tool
- Workflow
- MCP
- Connector

---

# 3.10 Knowledge Source

## 定义

知识来源。

---

字段：

- id
- type
- location
- status
- sync_time

---

类型：

- Local Folder
- Obsidian
- Git
- Web
- Connector

---

# 3.11 Knowledge

## 定义

经过处理后的知识。

---

字段：

- id
- source_id
- title
- content
- tags
- embedding
- permissions

---

# 3.12 Memory

## 定义

长期经验。

---

字段：

- id
- owner_type
- owner_id
- content
- source
- confidence
- created_at

---

类型：

- User Memory
- Company Memory
- Department Memory
- Project Memory
- Employee Memory

---

# 4. 业务模板模型

---

# Business Definition

定义业务。

字段：

- id
- name
- description
- stages
- roles
- modules
- workflows
- metrics

---

# Project Template

定义项目创建方式。

字段：

- id
- business_definition_id
- default_team
- default_capabilities
- default_workspace

---

# 5. 执行模型

一次任务执行：

```
Task

↓

Task Run

↓

Workflow Run

↓

Capability Call

↓

Artifact
```

---

# Task Run

记录：

- 开始时间；
- 结束时间；
- 状态；
- 输入；
- 输出。

---

# Capability Call

记录：

- 调用了什么能力；
- 使用哪个模型；
- 消耗多少资源；
- 执行结果。

---

# 6. 数据权限模型

当前个人版本：

简单权限。

---

未来商业版本：

支持：

- 用户；
- 团队；
- 企业；
- 角色。

---

权限范围：

- Company；
- Department；
- Project；
- Knowledge；
- Capability。

---

# 7. 数据生命周期

对象通用生命周期：

```
Create

↓

Active

↓

Update

↓

Archive

↓

Delete

↓

Restore
```

---

# 8. 删除策略

优先：

软删除。

保留：

历史关系。

---

删除前：

检查：

关联对象。

影响范围。

恢复方式。

---

# 9. 数据版本

需要版本管理：

- Workflow；
- Template；
- Workspace Definition；
- Artifact。

---

记录：

版本。

修改时间。

修改人。

变化内容。

---

# 10. 数据分析来源

经营分析数据来源：

业务数据。

执行数据。

成果数据。

人工录入数据。

---

形成：

```
业务执行

↓

数据沉淀

↓

数据洞察

↓

经营分析

↓

优化建议
```

---

# 11. 本章冻结内容

本章定义 Curis 数据模型方向。

核心：

统一对象模型。

配置化扩展业务。

数据服务产品，而不是限制产品。

下一章：

# 38 API设计规范（API Specification）