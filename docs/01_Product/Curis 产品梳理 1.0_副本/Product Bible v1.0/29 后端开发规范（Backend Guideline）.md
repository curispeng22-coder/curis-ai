# Curis Product Bible

# 29 后端开发规范（Backend Guideline）

版本：v1.0-draft

---

# 1. 规范定位

后端负责支撑 Curis 的产品模型和业务运行。

目标：

- 支撑公司、部门、员工、项目等核心对象；
- 支撑 AI 能力调度；
- 支撑业务模板生成；
- 支撑任务和 Workflow 执行；
- 支撑数据沉淀和分析。

---

# 2. 后端核心原则

## 2.1 围绕产品对象设计

后端模型优先围绕：

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

设计。

---

避免：

围绕单个功能创建孤立系统。

例如：

不要因为增加一个 Agent 而重新设计业务模型。

---

# 3. 服务边界

推荐拆分：

```
产品层

↓

业务服务层

↓

能力服务层

↓

执行层

↓

数据层
```

---

# 4. 核心业务服务

## 4.1 Organization Service

负责：

- 公司；
- 部门；
- 员工；
- 角色关系。

---

## 4.2 Project Service

负责：

- 项目创建；
- 项目状态；
- 项目生命周期；
- 项目上下文。

---

## 4.3 Task Service

负责：

- 任务创建；
- 任务状态；
- 任务关系；
- 任务执行记录。

---

## 4.4 Artifact Service

负责：

- 成果生成；
- 成果版本；
- 成果状态；
- 成果关联。

---

## 4.5 Knowledge Service

负责：

- 资料来源；
- 索引；
- 知识关联；
- 检索。

---

## 4.6 Analytics Service

负责：

- 数据统计；
- 指标计算；
- 经营分析数据。

---

# 5. 能力系统后端

能力相关服务：

```
Capability Registry

↓

Capability Router

↓

Executor
```

---

# 5.1 Capability Registry

保存：

能力信息。

包括：

- 类型；
- 来源；
- 版本；
- 配置；
- 状态。

---

# 5.2 Capability Router

负责：

根据任务选择能力。

参考：

- 员工职责；
- 任务类型；
- 成本；
- 状态；
- 成功率；
- 用户配置。

---

# 5.3 Executor

负责：

实际调用。

例如：

调用：

Model。

Agent。

Tool。

Workflow。

---

# 6. Business Definition系统

业务模板不能写死。

需要结构化保存。

---

包括：

业务信息：

- 名称；
- 描述；
- 目标。

---

流程：

- 阶段；
- 状态；
- 依赖。

---

工作区：

- 模块；
- 字段；
- 页面配置。

---

执行：

- Workflow；
- Skill；
- Tool。

---

输出：

- 成果类型；
- 验收条件。

---

# 7. Workspace生成

后端负责提供：

Workspace Definition。

前端根据定义渲染。

---

流程：

```
Business Definition

↓

Project Instance

↓

Workspace Definition

↓

Frontend Render
```

---

避免：

后端直接控制页面。

---

# 8. Task执行系统

任务执行需要记录：

## 输入

- 用户目标；
- 项目上下文；
- 资料。

---

## 执行

- 员工；
- 能力；
- Workflow。

---

## 输出

- 成果；
- 状态；
- 日志。

---

# 9. Workflow Runtime

负责：

Workflow执行。

---

记录：

- 节点；
- 状态；
- 输入；
- 输出；
- 错误；
- 重试。

---

支持：

暂停。

恢复。

取消。

---

# 10. Memory系统后端

Memory不直接保存所有聊天。

需要：

提取层。

---

流程：

```
原始信息

↓

Memory提取

↓

审核

↓

存储

↓

调用
```

---

Memory记录：

- 来源；
- 创建时间；
- 使用范围；
- 可信度。

---

# 11. Knowledge系统后端

资料来源：

统一抽象。

例如：

```
Local File

Obsidian

Git

Web

Connector
```

---

统一进入：

Knowledge Pipeline。

---

流程：

```
Source

↓

Parser

↓

Index

↓

Knowledge

↓

Retrieval
```

---

# 12. 数据系统

记录：

## 运行数据

- Task；
- Workflow；
- Agent调用；
- 成本；
- Token。

---

## 业务数据

- 项目指标；
- 外部数据；
- 人工录入。

---

提供：

数据洞察。

经营分析。

---

# 13. Local Bridge 后端协同

Local Bridge负责本地连接。

后端负责：

- 注册；
- 授权；
- 状态管理；
- 操作记录。

---

不直接保存：

用户本地敏感数据。

---

# 14. 权限设计

当前个人版本：

简单权限。

---

未来商业版本：

支持：

用户。

团队。

角色。

组织权限。

---

权限对象：

- 公司；
- 部门；
- 项目；
- 资料；
- 能力。

---

# 15. 数据隔离

未来 Workspace / Admin 分离：

需要支持：

平台数据。

用户数据。

项目数据。

---

当前版本：

统一管理。

预留边界。

---

# 16. API设计

API围绕业务对象。

例如：

```
/companies

/departments

/employees

/projects

/tasks

/artifacts

/capabilities
```

---

避免：

围绕数据库表暴露接口。

---

# 17. 错误处理

统一返回：

错误类型。

错误原因。

解决建议。

---

例如：

能力不可用：

返回：

- 哪个能力失败；
- 原因；
- 是否有备用能力。

---

# 18. 日志与审计

记录：

重要操作：

- 创建；
- 修改；
- 删除；
- 执行；
- 权限变化。

---

用于：

问题排查。

安全分析。

经营复盘。

---

# 19. 扩展原则

新增业务：

优先增加：

Business Definition。

Workflow。

Skill。

Tool。

---

减少：

修改核心代码。

---

# 20. 后端验收标准

检查：

## 产品支持

是否支撑页面需求。

---

## 扩展能力

新增业务是否需要大量开发。

---

## 稳定性

任务失败是否可恢复。

---

## 可观测性

是否知道：

发生什么。

为什么。

如何处理。

---

# 本章冻结内容

本章定义 Curis 后端开发规范。

核心：

后端围绕产品模型建设。

业务通过模板扩展。

能力通过统一系统接入。

下一章：

# 30 Codex 开发规范（Codex Guideline）