# Curis Development Specification

# 20 Agent运行与调度系统（Agent Runtime & Orchestration）

版本：v1.0-draft

---

# 1. 系统定位

Agent Runtime 是 Curis 多Agent体系的执行核心。

负责：

- 管理Agent生命周期；
- 调度不同Agent执行任务；
- 管理Agent会话；
- 协调多Agent协作；
- 控制执行资源；
- 记录执行过程。

---

# 2. 核心目标

让Curis可以：

- 同时管理多个AI员工；
- 调用不同AI应用；
- 根据任务自动选择Agent；
- 支持Agent协作；
- 支持Agent替换；
- 支持长期运行任务。

---

# 3. 核心关系

```
用户目标

↓

AI秘书

↓

项目负责人

↓

Task

↓

Agent Router

↓

Agent Runtime

↓

外部Agent

↓

成果
```

---

# 4. Agent Runtime职责

Agent Runtime负责：

## 会话管理

维护：

- Agent Session；
- 当前任务；
- 当前Context；
- 执行状态。

---

## 生命周期管理

管理：

创建。

启动。

暂停。

恢复。

结束。

异常处理。

---

## 资源控制

控制：

- Token；
- 时间；
- 并发；
- 成本。

---

## 输出管理

收集：

- Agent输出；
- 文件；
- 代码；
- 数据；
- 日志。

---

# 5. Agent Session

## 定位

一次Agent执行过程。

---

包含：

```
Agent Session

├── Agent

├── Task

├── Context

├── Input

├── Execution

├── Output

└── Status
```

---

# 6. Agent状态

支持：

```
Created

↓

Ready

↓

Running

↓

Waiting

↓

Completed

↓

Failed

↓

Stopped
```

---

# 7. Agent启动流程

流程：

```
Task创建

↓

选择Agent

↓

生成Context Package

↓

初始化Session

↓

调用Agent

↓

执行任务

↓

返回结果
```

---

# 8. Agent Router

## 定位

Agent选择系统。

---

负责判断：

哪个Agent最适合当前任务。

---

输入：

- Task类型；
- 项目；
- 员工角色；
- 能力；
- 历史成功率。

---

输出：

最佳Agent。

---

# 9. Agent选择策略

考虑：

## 能力匹配

例如：

代码任务。

优先：

编程Agent。

---

## 历史表现

例如：

某Agent完成类似任务成功率更高。

---

## 成本

例如：

简单任务无需高级模型。

---

## 可用状态

例如：

额度不足。

自动切换。

---

# 10. Agent优先级

用户可以配置：

首选Agent。

备用Agent。

---

例如：

研发员工：

```
第一：

Codex

第二：

Claude Code

第三：

其他开发Agent
```

---

# 11. 多Agent协作

支持：

多个Agent共同完成任务。

---

例如：

软件研发：

```
产品Agent

↓

架构Agent

↓

开发Agent

↓

测试Agent

↓

审查Agent
```

---

# 12. Agent协作模式

## 顺序协作

一个完成后进入下一个。

---

例如：

设计完成。

↓

开发。

↓

测试。

---

## 并行协作

多个Agent同时执行。

---

例如：

多个模型同时分析方案。

---

## 竞争模式

多个Agent提供方案。

然后比较。

---

例如：

技术方案评审。

---

# 13. Agent通信

Agent之间通过：

结构化消息。

---

消息包含：

```
Source Agent

↓

Target Agent

↓

Context

↓

Request

↓

Output
```

---

避免：

大量自然语言传递。

---

# 14. 外部AI应用接入

支持：

## API Agent

例如：

模型API。

---

## 本地Agent

例如：

安装的软件：

- Codex；
- Claude Code；
- Trae；
- WorkBuddy。

---

## MCP Agent

通过MCP连接。

---

# 15. 本地Agent调用

通过：

Local Bridge。

---

流程：

```
Curis

↓

Local Bridge

↓

检测本机Agent

↓

创建Session

↓

执行任务
```

---

例如：

用户电脑安装：

Claude Code。

Curis发现：

可用。

注册：

Claude Code Agent。

---

# 16. Agent权限

每个Agent需要：

权限范围。

---

例如：

开发Agent：

允许：

代码目录。

Git。

测试。

---

不允许：

私人文件。

---

# 17. Agent执行日志

记录：

```
Agent

↓

Task

↓

Context

↓

Tool调用

↓

Output

↓

Cost
```

---

用于：

分析。

优化。

审计。

---

# 18. Agent失败处理

失败类型：

## 能力失败

例如：

模型不可用。

---

处理：

切换Agent。

---

## 上下文不足

处理：

重新生成Context。

---

## 任务错误

处理：

返回负责人分析。

---

## 权限问题

处理：

请求授权。

---

# 19. Agent成本控制

支持：

预算。

---

限制：

单次任务。

项目。

员工。

公司。

---

例如：

研发项目：

限制：

每日Token。

---

超过：

暂停。

通知。

---

# 20. Agent学习

Agent执行完成后：

生成：

经验。

---

进入：

Memory系统。

---

例如：

开发Agent：

记录：

某类Bug解决方式。

---

# 21. AI秘书与Agent Runtime

用户不需要直接管理：

几十个Agent。

---

AI秘书负责：

理解需求。

选择执行路径。

---

例如：

用户：

“优化这个页面。”

流程：

```
AI秘书

↓

项目负责人

↓

设计Agent

↓

开发Agent

↓

测试Agent
```

---

# 22. API设计

## 注册Agent

```
POST /agents/register
```

---

## 获取Agent列表

```
GET /agents
```

---

## 创建Session

```
POST /agents/{id}/session
```

---

## 执行任务

```
POST /agents/{id}/execute
```

---

## 获取状态

```
GET /agents/{id}/status
```

---

# 23. 验收标准

Agent Runtime完成后：

用户可以：

接入多个AI应用。

统一管理。

自动调用。

切换Agent。

查看执行。

控制成本。

---

# 24. 核心指标

评估：

## Agent利用率

是否真正使用多个能力。

---

## 成功率

任务完成情况。

---

## 成本效率

单位成果成本。

---

## 切换能力

Agent失败后恢复能力。

---

# 本章冻结内容

本章定义Agent运行与调度系统。

核心：

Curis不是聊天聚合器。

而是：

管理多个AI员工和执行能力的智能操作系统。

---

下一章：

# 21 多Agent团队协作规范（Multi-Agent Team Collaboration）