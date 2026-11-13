# Curis Development Specification

# 51 API工程实现规范（API Engineering Specification）

版本：v1.0-draft

---

# 1. 规范定位

API工程实现规范用于定义：

Curis后端API如何被统一设计、开发、维护。

本规范服务：

- 前端开发；
- 后端开发；
- AI开发Agent；
- 外部能力接入。

---

# 2. 与Product Bible关系

```
Product Bible

第38章：

API产品架构规范

定义：

系统需要哪些API能力。


↓

Development Specification

第51章：

API工程实现规范

定义：

这些API如何实现。


↓

代码实现
```

---

# 3. API设计原则

## 3.1 资源导向

API围绕业务对象设计。

---

例如：

项目：

```
/projects
```

任务：

```
/tasks
```

员工：

```
/employees
```

---

避免：

按照页面设计接口。

错误：

```
/home/getProjectList
```

---

正确：

```
/projects
```

---

# 4. API分层

Curis API分为：

```
Business API

↓

AI Runtime API

↓

Capability API

↓

Knowledge API

↓

Analytics API

↓

Admin API
```

---

# 5. Business API规范

负责：

业务对象管理。

---

对象：

```
Company

Department

Employee

Project

Task

Artifact
```

---

示例：

获取项目：

```
GET /api/v1/projects/{id}
```

---

创建项目：

```
POST /api/v1/projects
```

---

# 6. AI Runtime API规范

负责：

AI执行过程。

---

包括：

- Task执行；
- Agent运行；
- Workflow执行；
- Tool调用。

---

例如：

启动任务：

```
POST /api/v1/tasks/{id}/execute
```

---

返回：

```json
{
  "job_id":"xxx",
  "status":"running"
}
```

---

# 7. Capability API规范

负责：

能力管理。

---

包括：

```
Model

Agent

Skill

Tool

Workflow

Connector
```

---

例如：

获取能力：

```
GET /api/v1/capabilities
```

---

测试能力：

```
POST /api/v1/capabilities/{id}/test
```

---

# 8. Knowledge API规范

负责：

知识系统。

---

包括：

- 文件来源；
- 知识索引；
- 知识查询；
- 知识关系。

---

例如：

搜索知识：

```
GET /api/v1/knowledge/search
```

---

同步资料：

```
POST /api/v1/knowledge/sources/{id}/sync
```

---

# 9. Memory API规范

负责：

长期记忆。

---

包括：

- 创建Memory；
- 检索Memory；
- 更新Memory。

---

例如：

检索：

```
POST /api/v1/memory/retrieve
```

---

输入：

```json
{
 "context":"开发登录模块"
}
```

---

返回：

相关经验。

---

# 10. Context API规范

负责：

生成Agent执行上下文。

---

例如：

```
POST /api/v1/context/build
```

---

输入：

```json
{
 "task_id":"xxx",
 "agent_id":"xxx"
}
```

---

输出：

```json
{
 "summary":"...",
 "memory":[ ],
 "knowledge":[ ]
}
```

---

# 11. API响应规范

统一格式：

## 成功

```json
{
 "success":true,
 "data":{},
 "message":"success"
}
```

---

## 失败

```json
{
 "success":false,
 "code":"TASK_FAILED",
 "message":"任务执行失败",
 "details":{}
}
```

---

# 12. HTTP状态规范

使用标准状态：

---

## 200

成功。

---

## 201

创建成功。

---

## 400

参数错误。

---

## 401

身份验证失败。

---

## 403

权限不足。

---

## 404

资源不存在。

---

## 409

状态冲突。

---

## 500

系统错误。

---

# 13. 分页规范

列表接口统一：

请求：

```
?page=1

&size=20
```

---

返回：

```json
{
"items":[],
"pagination":{
 "page":1,
 "size":20,
 "total":100
}
}
```

---

# 14. 搜索规范

支持：

关键词搜索。

---

例如：

```
GET /projects/search?q=AI
```

---

AI增强搜索：

单独接口。

---

例如：

```
POST /knowledge/semantic-search
```

---

# 15. 异步任务规范

AI任务通常耗时较长。

禁止：

同步等待。

---

统一：

```
提交任务

↓

返回job_id

↓

后台执行

↓

查询状态

↓

获取结果
```

---

例如：

```
POST /executions
```

返回：

```json
{
"job_id":"123"
}
```

---

查询：

```
GET /jobs/123
```

---

# 16. Streaming接口规范

AI交互需要支持流式输出。

---

应用：

- AI秘书；
- Agent执行；
- 会议讨论。

---

形式：

```
Client

↓

Stream Connection

↓

AI Events
```

---

事件类型：

```
message.delta

agent.status

tool.call

workflow.update

task.completed
```

---

# 17. WebSocket/Event规范

实时事件：

统一事件模型。

---

例如：

任务开始：

```
task.started
```

---

任务完成：

```
task.completed
```

---

Agent切换：

```
agent.switched
```

---

能力异常：

```
capability.error
```

---

# 18. 文件接口规范

涉及：

- 资料；
- 成果；
- 项目文件。

---

支持：

上传。

下载。

预览。

版本。

---

例如：

```
POST /files/upload
```

---

文件必须关联：

```
Workspace

Project

User
```

---

# 19. 权限验证规范

所有API：

必须经过：

```
Authentication

↓

Authorization

↓

Resource Check
```

---

例如：

读取项目：

检查：

用户是否属于项目。

---

# 20. 高风险API

需要额外确认。

包括：

- 删除；
- 发布；
- 外部发送；
- 修改权限；
- 大规模执行。

---

流程：

```
请求

↓

风险判断

↓

确认

↓

执行
```

---

# 21. API版本管理

统一：

```
/api/v1/
```

---

未来：

```
/api/v2/
```

---

禁止：

直接修改已有接口行为。

---

# 22. API文档规范

所有API必须包含：

- 描述；
- 请求参数；
- 返回格式；
- 错误码；
- 示例。

---

同步：

OpenAPI文档。

---

# 23. AI开发Agent要求

AI开发Agent新增API时：

必须同步：

```
API

↓

数据模型

↓

权限

↓

测试

↓

文档
```

---

禁止：

只修改代码。

---

# 24. API测试规范

包括：

## 单接口测试

验证：

输入输出。

---

## 权限测试

验证：

访问控制。

---

## 异常测试

验证：

失败处理。

---

## AI任务测试

验证：

异步执行。

流式输出。

---

# 25. 验收标准

API工程规范完成后：

开发团队可以：

统一开发接口。

快速接入模块。

支持AI系统扩展。

---

检查：

## 一致性

所有API风格统一。

---

## 扩展性

支持未来Admin和生态。

---

## 稳定性

支持长期运行。

---

# 本章冻结内容

本章定义Curis API工程实现规范。

核心：

Product Bible定义API能力边界。

Development Specification定义API工程实现方式。

API作为：

Workspace、AI员工、Capability、Knowledge和外部生态之间的连接层。

下一章：

# 52 AI系统配置规范（Prompt & Agent Configuration）