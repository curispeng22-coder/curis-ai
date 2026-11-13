# Curis Development Specification

# 18 多Agent管理与外部Agent接入规范（Multi-Agent Orchestration Specification）

版本：v1.0-draft

---

# 1. 系统定位

多Agent系统负责管理：

外部AI应用。

内部AI员工。

专业Agent。

开发Agent。

业务Agent。

---

目标：

让不同AI能力成为Curis员工体系中的可调用执行者。

---

# 2. 核心理念

Curis不绑定：

- ChatGPT；
- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor；
- Gemini；
- 其他AI工具。

---

这些工具在Curis中属于：

Agent Provider。

---

关系：

```
用户目标

↓

AI秘书

↓

项目负责人

↓

Agent调度中心

↓

外部Agent

↓

成果
```

---

# 3. Agent与Employee关系

需要区分：

## Employee

业务责任主体。

负责：

- 理解目标；
- 管理任务；
- 汇报结果。

---

## Agent

执行能力。

负责：

- 编码；
- 分析；
- 生成；
- 操作工具。

---

例如：

研发负责人：

Employee。

拥有：

- Codex Agent；
- Claude Code Agent；
- 测试Agent。

---

# 4. Agent类型

支持：

---

# 4.1 通用对话Agent

例如：

ChatGPT。

用途：

分析。

规划。

总结。

---

# 4.2 编程Agent

例如：

- Codex；
- Claude Code；
- Cursor Agent；
- Trae。

用途：

代码开发。

调试。

测试。

---

# 4.3 业务Agent

例如：

内容运营Agent。

数据分析Agent。

SEO Agent。

---

# 4.4 工具型Agent

负责：

调用外部工具。

例如：

浏览器Agent。

自动化Agent。

---

# 5. Agent接入方式

支持多种方式：

---

## 5.1 API接入

例如：

模型API。

Agent API。

---

配置：

- Endpoint；
- Key；
- Model；
- 权限。

---

## 5.2 本地应用接入

用于：

已经安装的软件。

例如：

本机：

Codex。

Claude Code。

Trae。

WorkBuddy。

---

通过：

Local Bridge。

发现：

应用。

目录。

接口。

执行能力。

---

## 5.3 MCP接入

通过MCP：

连接外部Agent和工具。

---

## 5.4 Plugin接入

未来：

第三方扩展。

---

# 6. Agent注册中心

组件：

Agent Registry。

---

保存：

```
Agent

├── 名称

├── 类型

├── Provider

├── 连接方式

├── 能力

├── Memory

├── 状态

└── 权限
```

---

# 7. Agent能力描述

每个Agent需要声明：

---

## 能做什么

例如：

Codex：

代码开发。

---

## 不擅长什么

例如：

不负责内容运营。

---

## 输入

例如：

代码仓库。

需求文档。

---

## 输出

例如：

代码修改。

Diff。

测试报告。

---

# 8. Agent路由系统

这是核心。

---

任务进入：

```
Task

↓

分析需求

↓

匹配Agent

↓

选择最佳Agent

↓

执行
```

---

选择依据：

- 任务类型；
- Agent能力；
- 成功率；
- 成本；
- 可用状态；
- 用户偏好。

---

# 9. 多Agent协作

支持：

多个Agent共同完成任务。

---

例如：

开发项目：

```
项目负责人Agent

↓

产品分析Agent

↓

Codex

↓

Claude Code

↓

测试Agent

↓

审查Agent
```

---

每个Agent：

共享：

项目上下文。

Memory。

成果。

---

# 10. Agent上下文管理

重点：

避免每次重新发送大量内容。

---

Agent调用前：

不是发送：

整个项目历史。

---

而是：

生成：

Agent Context Package。

---

包含：

## 项目摘要

目标。

状态。

阶段。

---

## 当前任务

需要完成什么。

---

## 相关Memory

历史经验。

---

## 必要资料

相关文档。

---

## 验收标准

最终要求。

---

# 11. Agent Memory绑定

不同Agent拥有：

不同经验。

---

例如：

Codex Agent Memory：

保存：

代码规范。

项目架构。

历史Bug。

---

内容Agent Memory：

保存：

内容策略。

用户偏好。

---

# 12. Agent成本控制

每个Agent记录：

- Token；
- 时间；
- 成本；
- 成功率。

---

系统可以：

自动选择：

性价比更高Agent。

---

例如：

简单任务：

小模型。

复杂任务：

高级模型。

---

# 13. Agent失败处理

Agent失败：

不等于任务失败。

---

处理：

## 重试

重新执行。

---

## 切换Agent

例如：

Codex失败。

切换Claude Code。

---

## 召开会议

复杂问题进入讨论。

---

# 14. Agent状态管理

状态：

在线。

离线。

执行中。

额度不足。

授权失败。

异常。

---

用户可以查看：

当前Agent状态。

---

# 15. Agent使用记录

记录：

```
任务

↓

Agent

↓

输入Context

↓

执行时间

↓

输出

↓

成本
```

---

用于：

数据分析。

优化调度。

---

# 16. AI秘书与Agent

用户不直接选择Agent。

---

例如：

用户：

“帮我开发这个功能。”

---

AI秘书：

判断：

需要研发负责人。

调用：

Codex。

测试Agent。

---

用户看到：

结果。

---

不是：

模型切换。

---

# 17. Agent市场（未来）

未来支持：

第三方Agent。

---

包括：

安装。

更新。

评价。

授权。

---

形成：

Agent生态。

---

# 18. 验收标准

多Agent系统完成后：

用户可以：

接入多个AI工具。

统一管理。

统一调用。

统一记录。

统一记忆。

---

验证：

## 是否减少工具切换。

---

## 是否保持长期上下文。

---

## 是否降低Token消耗。

---

## 是否能自动选择最佳Agent。

---

# 本章冻结内容

本章定义Curis多Agent管理体系。

核心：

Curis不是AI工具集合。

而是：

管理AI员工和执行能力的操作系统。

---

下一章：

# 19 Agent Context Engine（上下文管理引擎）