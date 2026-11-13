# Curis Development Specification

# 50 数据库设计与数据治理规范（Database & Data Governance）

版本：v1.0-draft

---

# 1. 系统定位

数据库设计规范用于定义：

Curis 如何组织、存储和管理：

- 业务数据；
- AI执行数据；
- 知识数据；
- Memory数据；
- 配置数据；
- 分析数据。

---

# 2. 核心理念

Curis的数据不是简单业务数据。

需要同时支持：

```
业务运行

+

AI执行

+

知识积累

+

经验成长

+

未来商业化
```

---

# 3. 数据分类

Curis数据分为：

```
Business Data

↓

Execution Data

↓

Knowledge Data

↓

Memory Data

↓

Configuration Data

↓

Analytics Data
```

---

# 4. Business Data业务数据

负责：

用户看到的业务对象。

---

包括：

## Company

公司。

---

## Department

部门。

---

## Employee

AI员工。

---

## Project

项目。

---

## Task

任务。

---

## Artifact

成果。

---

# 5. 核心对象关系

```
Company

↓

Department

↓

Employee


Company

↓

Project

↓

Task

↓

Artifact
```

---

# 6. Company数据模型

```
Company

id

name

description

owner_id

status

created_at

updated_at
```

---

# 7. Department数据模型

```
Department

id

company_id

name

description

owner_id

status

created_at
```

---

# 8. Employee数据模型

```
Employee

id

department_id

name

role

description

capability_profile_id

memory_id

status

created_at
```

---

# 9. Project数据模型

```
Project

id

company_id

department_id

template_id

name

objective

owner_id

status

stage

created_at
```

---

# 10. Task数据模型

```
Task

id

project_id

name

description

executor_id

workflow_id

status

priority

created_at
```

---

# 11. Artifact数据模型

```
Artifact

id

project_id

task_id

type

name

location

version

status

created_at
```

---

# 12. Execution Data执行数据

负责记录：

AI如何工作。

---

包括：

## Agent Execution

记录：

哪个Agent执行。

---

## Workflow Run

记录：

流程运行。

---

## Tool Call

记录：

工具调用。

---

## Model Usage

记录：

模型消耗。

---

# 13. Execution数据设计

```
Execution

id

task_id

agent_id

capability_id

status

started_at

finished_at

result
```

---

# 14. Knowledge Data知识数据

负责：

资料和知识关系。

---

包括：

## Source

资料来源。

---

## Document

文档。

---

## Knowledge Node

知识节点。

---

## Relation

知识关系。

---

# 15. Memory Data设计

Memory不是普通文本。

需要结构化。

---

```
Memory

id

type

content

source

owner

confidence

created_at

updated_at
```

---

# 16. Memory类型

包括：

```
User Memory

Employee Memory

Project Memory

Department Memory

Company Memory
```

---

# 17. Memory数据治理

Memory需要：

## 来源

来自哪里。

---

## 可信度

是否验证。

---

## 更新时间

是否过期。

---

## 使用记录

是否有效。

---

# 18. Configuration Data配置数据

负责：

系统配置。

---

包括：

## Capability配置

模型。

Agent。

Tool。

---

## Workflow配置

流程定义。

---

## Permission配置

权限规则。

---

# 19. Analytics Data分析数据

用于：

数据洞察。

经营分析。

---

包括：

- Token；
- 成本；
- 使用次数；
- 成功率；
- 项目指标。

---

# 20. 数据隔离

未来企业模式：

采用：

Tenant隔离。

---

结构：

```
Tenant

↓

Workspace

↓

Business Data
```

---

# 21. 权限字段设计

核心数据需要包含：

```
owner_id

workspace_id

department_id

permission_scope
```

---

用于：

数据访问控制。

---

# 22. 数据版本管理

重要对象支持版本。

---

包括：

- Workflow；
- Template；
- Artifact；
- Knowledge。

---

例如：

Workflow：

```
v1

↓

v2

↓

v3
```

---

# 23. 数据删除策略

采用：

软删除。

---

字段：

```
deleted_at
```

---

避免：

历史关系丢失。

---

# 24. 数据生命周期

对象生命周期：

```
Created

↓

Active

↓

Updated

↓

Archived

↓

Deleted
```

---

# 25. 数据同步设计

未来：

本地。

云端。

同步。

---

需要区分：

## 可同步数据

例如：

项目。

任务。

Memory。

---

## 本地数据

例如：

文件路径。

API Key。

私人文件。

---

# 26. 数据索引策略

高频查询：

建立索引。

---

例如：

Project：

company_id。

status。

owner_id。

---

Task：

project_id。

status。

executor_id。

---

# 27. AI检索数据设计

Context Engine需要：

快速获取：

相关数据。

---

支持：

- 向量索引；
- 关系索引；
- 标签索引。

---

# 28. 数据治理原则

## 数据最小化

只保存必要数据。

---

## 数据可追踪

知道来源。

---

## 数据可恢复

支持恢复。

---

## 数据可迁移

支持未来云端。

---

# 29. AI开发要求

AI开发Agent修改数据库：

必须同步更新：

- 数据模型；
- API；
- 文档；
- 迁移脚本。

---

禁止：

直接修改生产数据结构。

---

# 30. 验收标准

数据库体系完成后：

支持：

业务运行。

AI执行。

知识沉淀。

未来商业化。

---

检查：

## 一致性

对象关系正确。

---

## 扩展性

新增业务不破坏结构。

---

## 安全性

数据权限明确。

---

# 本章冻结内容

本章定义Curis数据库设计与数据治理规范。

核心：

数据库不仅保存业务数据。

还支撑：

AI员工长期工作、知识积累和智能优化。

---

下一章：

# 51 API工程实现规范（API Engineering Specification）