# Curis Development Specification

# 52 AI系统配置规范（Prompt & Agent Configuration）

版本：v1.0-draft

---

# 1. 系统定位

AI系统配置规范用于定义：

Curis中的AI员工、Agent、Workflow、Capability如何配置和管理。

目标：

避免：

- Prompt散落在代码中；
- Agent行为不可控；
- 不同项目重复配置；
- 无法版本管理。

---

# 2. 核心理念

Prompt不是代码。

Prompt属于：

AI能力配置。

---

关系：

```
AI Employee

↓

Agent Configuration

↓

Prompt

↓

Capability

↓

Execution
```

---

# 3. AI配置分层

Curis采用分层配置：

```
System Layer

↓

Role Layer

↓

Employee Layer

↓

Project Layer

↓

Task Layer

↓

Runtime Layer
```

---

# 4. System Layer（系统层）

定位：

所有AI共享的基础规则。

---

包括：

## 基础行为规范

例如：

- 输出格式；
- 安全规则；
- 权限规则。

---

## 通用能力约束

例如：

不能绕过权限。

不能执行未授权操作。

---

特点：

稳定。

低频修改。

---

# 5. Role Layer（角色层）

定位：

定义岗位职责。

---

例如：

研发负责人：

```
角色：

技术项目负责人


职责：

制定技术方案

协调开发任务

保证交付质量
```

---

内容：

- 角色目标；
- 工作范围；
- 决策权限；
- 输出要求。

---

# 6. Employee Layer（员工层）

定位：

定义具体AI员工个性。

---

例如：

研发负责人A：

配置：

```
角色：

研发负责人


经验：

长期参与Curis开发


偏好：

优先考虑可维护性
```

---

包含：

- 人格；
- 工作习惯；
- Memory；
- Capability Profile。

---

# 7. Project Layer（项目层）

定位：

项目特殊要求。

---

例如：

Curis研发项目：

增加：

```
技术规范：

React

TypeScript

模块化架构
```

---

项目配置覆盖：

员工默认配置。

---

# 8. Task Layer（任务层）

定位：

当前任务临时要求。

---

例如：

任务：

优化首页。

---

临时增加：

```
重点：

降低加载时间

保持UI一致
```

---

任务结束：

不进入长期配置。

---

# 9. Runtime Layer（运行层）

定位：

执行时动态参数。

---

包括：

- 当前Context；
- 当前Memory；
- 当前Knowledge；
- 当前工具状态。

---

由：

Context Engine生成。

---

# 10. Agent Configuration模型

```
AgentConfig

├── identity

├── role

├── objective

├── system_prompt

├── capabilities

├── memory_policy

├── context_policy

├── output_format

└── version
```

---

# 11. Prompt管理规范

Prompt必须：

版本化。

---

例如：

```
研发负责人Prompt

v1.0

基础项目管理


v1.1

增加代码审查要求
```

---

支持：

- 创建版本；
- 比较版本；
- 回滚版本。

---

# 12. Prompt与代码分离

禁止：

直接写入代码：

```python
system_prompt = "..."
```

---

推荐：

配置化：

```
Prompt Registry

↓

Agent Runtime

↓

加载Prompt
```

---

# 13. Prompt Registry

组件：

Prompt Registry。

---

负责：

管理：

- System Prompt；
- Role Prompt；
- Task Prompt。

---

字段：

```
Prompt

id

name

type

content

version

status

created_at
```

---

# 14. 输出格式配置

Agent需要定义：

输出规范。

---

例如：

研发Agent：

输出：

```
修改内容

↓

影响文件

↓

测试结果

↓

风险
```

---

内容Agent：

输出：

```
标题

↓

正文

↓

素材需求

↓

发布建议
```

---

# 15. Memory调用策略配置

不同Agent：

Memory策略不同。

---

例如：

研发Agent：

优先：

- 技术Memory；
- 项目Memory。

---

内容Agent：

优先：

- 用户画像；
- 内容经验。

---

# 16. Knowledge调用策略

定义：

Agent读取什么知识。

---

例如：

研发Agent：

读取：

代码库。

技术文档。

历史Bug。

---

不读取：

无关运营资料。

---

# 17. Capability配置

Agent需要声明：

可使用能力。

---

例如：

研发Agent：

```
Model:

Claude


Agent:

Claude Code


Tool:

Git


Workflow:

Testing
```

---

# 18. Agent配置版本管理

配置变化：

需要版本。

---

例如：

```
研发Agent

v1

基础开发


v2

增加自动测试


v3

增加代码审查
```

---

支持：

升级。

回滚。

比较。

---

# 19. 配置环境

支持：

不同环境。

---

例如：

```
Development

Testing

Production
```

---

避免：

测试配置影响正式运行。

---

# 20. AI安全约束配置

Agent需要配置：

权限边界。

---

例如：

开发Agent：

允许：

修改代码。

---

禁止：

访问私人目录。

---

# 21. AI配置与调度中心

调度中心读取：

Agent配置。

---

决定：

是否适合当前任务。

---

例如：

任务：

代码开发。

---

匹配：

研发Agent。

---

# 22. UI管理

配置入口：

高级管理。

---

展示：

Agent配置。

Prompt版本。

能力绑定。

---

普通用户：

不直接修改底层Prompt。

---

# 23. AI秘书配置

AI秘书自身也是Agent。

---

配置：

- 全局职责；
- 用户偏好；
- 操作权限；
- 主动程度。

---

# 24. API设计

## 获取Agent配置

```
GET /agents/{id}/config
```

---

## 更新配置

```
PATCH /agents/{id}/config
```

---

## 获取Prompt版本

```
GET /prompts/{id}/versions
```

---

## 发布Prompt版本

```
POST /prompts/{id}/publish
```

---

# 25. 验收标准

AI配置系统完成后：

可以：

管理Agent行为。

版本化Prompt。

控制能力。

调整员工工作方式。

---

检查：

## 可维护

Prompt不散落代码。

---

## 可控制

AI行为可调整。

---

## 可演进

员工能力持续升级。

---

# 本章冻结内容

本章定义Curis AI系统配置规范。

核心：

AI员工不是简单调用模型。

而是由：

角色。

Prompt。

Memory。

Context。

Capability。

共同构成的可管理数字员工。

---

下一章：

# 53 测试体系规范（Testing Specification）