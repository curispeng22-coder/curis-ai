# Curis Product Bible

# 38 API产品架构规范（API Product Architecture Specification）

版本：v1.0-draft

---

# 1. 规范定位

API 是 Curis 各模块之间通信的统一接口。

目标：

- 支撑前后端分离；
- 支撑 Workspace / Admin 未来拆分；
- 支撑外部 Agent 接入；
- 支撑能力扩展；
- 保持业务对象统一。

---

# 2. API设计原则

## 2.1 围绕业务对象

API 不直接暴露数据库结构。

围绕：

- Company；
- Department；
- Employee；
- Project；
- Task；
- Artifact；
- Capability；
- Knowledge。

设计。

---

## 2.2 面向业务行为

优先：

表达用户动作。

例如：

推荐：

```
POST /projects/{id}/pause
```

而不是：

```
UPDATE projects SET status='paused'
```

---

## 2.3 保持扩展能力

新增业务时：

优先增加：

- Template；
- Configuration；
- Workflow；
- Capability。

减少修改核心 API。

---

# 3. API分层

推荐结构：

```
API Gateway

↓

Business API

↓

Capability API

↓

Execution API

↓

Data Service
```

---

# 4. 用户接口 API

负责：

Workspace 功能。

---

包含：

## 用户

例如：

```
/users
```

支持：

- 获取用户信息；
- 修改设置；
- 管理偏好。

---

## 公司

```
/companies
```

支持：

创建公司。

查看公司。

修改公司。

---

## 部门

```
/departments
```

支持：

创建部门。

查询部门。

修改部门。

解散部门。

---

## 员工

```
/employees
```

支持：

创建员工。

修改员工。

绑定能力。

查看状态。

---

# 5. 项目 API

路径：

```
/projects
```

---

支持：

## 创建项目

```
POST /projects
```

输入：

- 项目名称；
- 业务模板；
- 目标；
- 团队配置。

---

## 获取项目

```
GET /projects/{id}
```

返回：

- 项目状态；
- 工作区；
- 任务；
- 成果。

---

## 更新项目

```
PATCH /projects/{id}
```

支持：

修改：

- 目标；
- 负责人；
- 状态。

---

## 项目生命周期

```
POST /projects/{id}/pause

POST /projects/{id}/resume

POST /projects/{id}/archive

DELETE /projects/{id}
```

---

# 6. 工作区 API

负责：

业务工作区生成。

---

路径：

```
/workspaces
```

---

支持：

## 获取工作区定义

```
GET /projects/{id}/workspace
```

返回：

- 模块；
- 字段；
- 布局；
- 状态。

---

## 更新工作区配置

```
PATCH /workspaces/{id}
```

---

# 7. 任务 API

路径：

```
/tasks
```

---

支持：

创建任务。

查看任务。

修改任务。

执行任务。

---

## 创建任务

输入：

- 项目；
- 目标；
- 负责人；
- Workflow。

---

## 执行任务

```
POST /tasks/{id}/run
```

---

## 任务状态

返回：

- waiting；
- running；
- paused；
- failed；
- completed。

---

# 8. Workflow API

路径：

```
/workflows
```

---

支持：

创建。

测试。

运行。

暂停。

版本管理。

---

## Workflow运行

```
POST /workflows/{id}/execute
```

---

返回：

- Run ID；
- 当前节点；
- 状态；
- 输出。

---

# 9. 能力 API

路径：

```
/capabilities
```

---

支持：

添加能力。

测试能力。

绑定能力。

管理能力。

---

## 查询能力

返回：

- 类型；
- 状态；
- Provider；
- 成本。

---

## 测试能力

```
POST /capabilities/{id}/test
```

---

# 10. Agent 接入 API

用于：

外部 Agent 接入 Curis。

---

支持：

注册 Agent。

更新 Agent。

调用 Agent。

获取状态。

---

例如：

```
POST /agents/register
```

---

注册信息：

- 名称；
- 类型；
- 能力；
- 权限；
- 接口方式。

---

# 11. Knowledge API

路径：

```
/knowledge
```

---

支持：

资料来源管理。

知识查询。

索引。

关联项目。

---

## 添加来源

```
POST /knowledge/sources
```

---

例如：

添加：

Obsidian Vault。

---

## 搜索知识

```
GET /knowledge/search
```

---

返回：

- 内容；
- 来源；
- 关联对象。

---

# 12. Memory API

路径：

```
/memory
```

---

支持：

创建。

查询。

更新。

删除。

---

例如：

员工 Memory：

```
GET /employees/{id}/memory
```

---

# 13. 成果 API

路径：

```
/artifacts
```

---

支持：

创建。

查看。

版本管理。

验收。

发布。

---

## 验收

```
POST /artifacts/{id}/review
```

---

结果：

通过。

修改。

拒绝。

---

# 14. 会议 API

路径：

```
/meetings
```

---

支持：

创建会议。

邀请参与者。

开始会议。

生成结论。

创建任务。

---

## 创建会议

输入：

- 主题；
- 项目；
- 参与者；
- 类型。

---

# 15. 数据分析 API

路径：

```
/analytics
```

---

支持：

查询：

- 成本；
- Token；
- 项目数据；
- 经营指标。

---

# 16. Business Template API

路径：

```
/templates
```

---

支持：

创建模板。

测试模板。

发布模板。

版本管理。

---

返回：

Business Definition。

---

# 17. 事件系统

Curis支持事件驱动。

例如：

事件：

```
task.completed
```

触发：

- 通知；
- 数据更新；
- Memory提取。

---

常见事件：

```
project.created

task.started

task.completed

artifact.created

workflow.failed

capability.error
```

---

# 18. 错误规范

统一错误结构：

```json
{
  "code": "CAPABILITY_UNAVAILABLE",
  "message": "当前能力不可用",
  "detail": {},
  "suggestion": "切换备用能力"
}
```

---

错误包含：

- 错误类型；
- 用户说明；
- 技术详情；
- 建议操作。

---

# 19. 权限控制

API需要支持：

对象权限。

包括：

- Company；
- Department；
- Project；
- Knowledge；
- Capability。

---

# 20. API版本管理

采用：

版本号。

例如：

```
/api/v1/projects
```

---

重大变化：

创建新版本。

避免：

破坏已有调用。

---

# 21. 外部生态接入

未来支持：

第三方：

- Agent；
- Skill；
- Tool；
- Connector。

---

通过：

统一 API。

进入 Curis 能力体系。

---

# 22. 本章冻结内容

本章定义 Curis API设计原则。

核心：

API服务产品对象。

支持扩展。

支持多Agent、多能力、多端接入。

下一章：

# 39 安全与权限规范（Security & Permission）