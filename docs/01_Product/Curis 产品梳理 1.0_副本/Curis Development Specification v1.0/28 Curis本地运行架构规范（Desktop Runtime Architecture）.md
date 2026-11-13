# Curis Development Specification

# 28 Curis本地运行架构规范（Desktop Runtime Architecture）

版本：v1.0-draft

---

# 1. 系统定位

Curis Desktop 是第一阶段产品运行形态。

目标：

让用户在自己的电脑上拥有完整 AI 工作环境。

支持：

- 本地资料；
- 本地AI应用；
- 本地工具；
- 本地项目；
- 本地执行能力。

---

# 2. 核心理念

Curis Desktop 不是简单客户端。

它是：

> 用户本机上的 AI 工作操作系统。

---

架构：

```
Curis Desktop

↓

Local Runtime

↓

Local Bridge

↓

用户本地环境

↓

AI能力执行
```

---

# 3. 总体架构

```
Curis Desktop

├── UI Layer

├── Workspace Layer

├── AI Orchestration Layer

├── Context Engine

├── Memory System

├── Capability System

├── Local Bridge

└── Storage Layer
```

---

# 4. UI Layer

负责：

用户交互。

包括：

- 首页；
- 项目；
- 工作区；
- AI秘书；
- 能力切换；
- 数据展示。

---

特点：

不直接处理执行逻辑。

---

# 5. Workspace Layer

负责：

业务体验。

包括：

- 公司；
- 部门；
- 员工；
- 项目；
- 任务；
- 成果。

---

Workspace不关心：

底层调用哪个模型。

---

# 6. AI Orchestration Layer

负责：

智能调度。

连接：

```
Task

↓

Capability Router

↓

Agent Runtime

↓

Model / Agent / Tool
```

---

# 7. Context Engine

负责：

生成任务上下文。

---

处理：

- 项目背景；
- Memory；
- Knowledge；
- 当前任务；
- 历史经验。

---

目标：

减少Token消耗。

避免加载全部历史。

---

# 8. Memory System

负责：

长期经验。

包括：

- 用户Memory；
- 项目Memory；
- 员工Memory；
- 部门Memory。

---

让AI员工：

持续成长。

---

# 9. Capability System

负责：

管理：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow；
- Connector。

---

提供：

能力池。

---

# 10. Local Bridge

## 定位

连接本地环境。

---

负责：

## 文件

访问本地文件。

---

## Git

操作代码仓库。

---

## 本地应用

发现：

- Codex；
- Claude Code；
- Trae；
- WorkBuddy；
- Cursor。

---

## 本地工具

调用：

Terminal。

IDE。

脚本。

---

# 11. Local Agent发现机制

Curis启动时：

扫描：

本机可用能力。

---

例如：

发现：

```
Claude Code

路径：

/Applications/Claude Code

状态：

可用
```

---

注册：

Local Capability。

---

# 12. 本地Agent调用流程

例如：

调用Codex：

```
Curis

↓

Agent Router

↓

Local Bridge

↓

Codex

↓

执行任务

↓

返回结果
```

---

# 13. 本地权限

Local Bridge必须：

用户授权。

---

权限：

## 文件权限

读取。

写入。

执行。

---

## 应用权限

允许调用哪些应用。

---

## 项目绑定

哪个项目可以访问。

---

# 14. 本地数据存储

当前阶段：

本地优先。

---

保存：

## 项目数据

公司。

员工。

任务。

成果。

---

## 知识数据

索引。

Memory。

缓存。

---

## 配置数据

能力。

连接。

权限。

---

# 15. 数据同步设计

第一阶段：

本地运行。

---

未来：

支持：

云端同步。

---

架构预留：

```
Local Storage

↓

Sync Layer

↓

Cloud Platform
```

---

# 16. 离线能力

支持：

部分功能离线运行。

---

例如：

查看：

项目。

资料。

Memory。

---

需要联网：

- 云模型；
- 外部Agent；
- 外部平台。

---

# 17. 本地安全

原则：

最小权限。

---

保护：

- API Key；
- 本地文件；
- 项目代码；
- 私人资料。

---

# 18. Runtime监控

记录：

执行状态。

---

包括：

- Agent调用；
- Tool调用；
- 文件操作；
- 错误。

---

用于：

数据洞察。

---

# 19. 更新机制

支持：

应用更新。

Local Bridge更新。

能力更新。

---

保持：

数据兼容。

---

# 20. 与未来Cloud架构关系

当前：

```
Desktop

+

Local Runtime
```

---

未来：

```
Cloud Platform

+

Desktop Client

+

Local Agent
```

---

Desktop继续作为：

个人工作入口。

---

# 21. AI秘书与Runtime

AI秘书不直接操作本地资源。

---

流程：

```
AI秘书

↓

任务

↓

调度中心

↓

Local Bridge

↓

执行
```

---

# 22. 验收标准

Desktop Runtime完成后：

用户可以：

打开Curis。

连接本机资源。

调用本地AI应用。

管理项目。

执行任务。

保存知识。

---

检查：

## 能力

是否能连接真实环境。

---

## 安全

权限是否透明。

---

## 扩展

未来是否支持云端化。

---

# 本章冻结内容

本章定义Curis Desktop运行架构。

核心：

Curis Desktop不是聊天窗口。

而是连接：

用户。

AI员工。

本地工具。

外部能力。

知识系统。

的个人AI操作系统。

---

下一章：

# 29 数据同步与云端演进规范（Sync & Cloud Evolution）