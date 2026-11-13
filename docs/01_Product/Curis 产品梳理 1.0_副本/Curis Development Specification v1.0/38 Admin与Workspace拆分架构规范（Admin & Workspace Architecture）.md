# Curis Development Specification

# 38 Admin与Workspace拆分架构规范（Admin & Workspace Architecture）

版本：v1.0-draft

---

# 1. 系统定位

Admin与Workspace拆分用于支持 Curis 从：

个人AI工作台。

发展为：

企业级AI组织平台。

---

# 2. 核心理念

当前阶段：

Curis Desktop。

一个应用。

一个用户。

同时承担：

使用者。

管理员。

配置者。

---

未来：

拆分：

```
Curis Platform

├── Admin

└── Workspace
```

---

# 3. 拆分原则

不是：

重新开发两个产品。

---

而是：

按照职责重新组织。

---

关系：

```
Admin

负责：

提供能力。


Workspace

负责：

使用能力。
```

---

# 4. Workspace定位

Workspace是用户日常工作的空间。

---

负责：

- 项目；
- 任务；
- AI员工；
- 成果；
- 资料；
- 数据分析。

---

面向：

员工。

项目负责人。

业务用户。

---

# 5. Workspace核心模块

包括：

## 首页

查看：

AI公司状态。

---

## 项目

管理：

业务项目。

---

## 会议室

进行：

分析和决策。

---

## 组织中心

查看：

公司组织。

---

## 能力中心

使用：

可用能力。

---

## 资料中心

管理：

知识。

---

## 成果中心

查看：

产出。

---

## 数据洞察

查看：

运行数据。

---

## 经营分析

查看：

业务分析。

---

# 6. Admin定位

Admin是：

AI组织管理后台。

---

负责：

创建。

配置。

治理。

发布。

---

面向：

平台管理员。

企业管理员。

---

# 7. Admin核心模块

---

# 7.1 组织管理

负责：

企业结构。

---

包括：

- 企业；
- 部门；
- 用户；
- 角色；
- 权限。

---

# 7.2 能力管理

负责：

平台能力。

---

包括：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow；
- MCP；
- Connector。

---

# 7.3 模板管理

负责：

Business Template。

---

包括：

- 行业模板；
- 项目模板；
- 工作区定义；
- Workflow模板。

---

# 7.4 Agent管理

负责：

AI员工模板。

---

例如：

研发团队模板：

```
研发负责人

开发员工

测试员工
```

---

# 7.5 治理管理

负责：

规则。

---

包括：

- 权限；
- 成本；
- 审批；
- 安全。

---

# 7.6 数据管理

负责：

平台级数据。

---

包括：

- 使用情况；
- 成本；
- 能力表现。

---

# 8. Admin向Workspace提供内容

关系：

```
Admin

↓

发布

↓

Workspace

↓

使用
```

---

例如：

Admin发布：

“小红书增长模板”。

---

Workspace：

创建：

小红书项目。

---

# 9. 能力提供关系

Admin：

管理：

能力池。

---

Workspace：

选择：

员工可使用能力。

---

例如：

Admin：

提供：

Claude。

Codex。

测试Workflow。

---

Workspace：

绑定：

研发员工。

---

# 10. 模板提供关系

Admin：

创建：

业务模板。

---

Workspace：

创建：

项目实例。

---

例如：

Admin：

发布：

研发项目模板。

---

Workspace：

创建：

Curis研发项目。

---

# 11. 数据边界

## Admin数据

包括：

- 平台模板；
- 公共能力；
- 治理规则。

---

## Workspace数据

包括：

- 项目；
- 任务；
- 成果；
- 用户资料。

---

# 12. Local能力关系

本地能力：

仍属于Workspace。

---

例如：

用户电脑安装：

Codex。

---

Workspace：

注册：

Local Capability。

---

Admin：

不直接访问。

---

# 13. 当前Desktop兼容方案

当前：

不拆分应用。

---

采用：

逻辑隔离。

---

结构：

```
Curis Desktop

├── Workspace

└── Advanced Management
```

---

未来：

迁移：

Advanced Management

↓

Admin。

---

# 14. 技术架构

未来：

```
Admin Frontend

↓

Admin API


Workspace Frontend

↓

Workspace API


        ↓

Common Services

        ↓

Capability

Knowledge

Execution
```

---

# 15. 用户迁移

个人用户：

升级后：

自动拥有：

个人Workspace。

---

企业用户：

创建：

企业Workspace。

---

# 16. UI差异

Workspace：

强调：

业务执行。

---

Admin：

强调：

配置治理。

---

避免：

Workspace出现大量后台配置。

---

# 17. 权限关系

Admin权限：

管理。

---

Workspace权限：

使用。

---

例如：

管理员：

添加模型。

---

员工：

使用模型。

---

# 18. API边界

Admin API：

```
/admin/templates

/admin/capabilities

/admin/users

/admin/policies
```

---

Workspace API：

```
/projects

/tasks

/employees

/artifacts

/knowledge
```

---

# 19. 验收标准

拆分完成后：

企业可以：

管理员配置平台。

员工使用Workspace。

能力统一管理。

业务独立运行。

---

检查：

## 边界

Admin和Workspace职责清晰。

---

## 扩展

未来商业化无需重构。

---

## 数据

权限隔离正确。

---

# 本章冻结内容

本章定义Admin与Workspace未来拆分架构。

核心：

Admin负责创造和治理能力。

Workspace负责利用能力完成业务。

当前阶段：

保持单体Desktop。

未来：

平滑演进为企业平台。

---

下一章：

# 39 商业化产品架构规范（Commercial Product Architecture）