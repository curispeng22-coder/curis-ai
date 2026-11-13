# Curis Development Specification

# 54 部署与运行环境规范（Deployment Specification）

版本：v1.0-draft

---

# 1. 系统定位

部署与运行环境规范用于定义：

Curis 如何从开发环境运行到正式使用环境。

目标：

保证：

- Desktop稳定运行；
- Backend可部署；
- Local Runtime可靠；
- 数据安全；
- 环境可复制。

---

# 2. 核心理念

Curis采用：

本地优先 + 云端可扩展架构。

---

当前阶段：

```
Curis Desktop

+

Local Runtime

+

Backend Service
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

# 3. 部署架构总览

```
User Device

↓

Curis Desktop

↓

Local Bridge

↓

Backend API

↓

AI Services

↓

External Providers
```

---

# 4. 运行环境分类

Curis包含：

```
Development Environment

↓

Testing Environment

↓

Production Environment
```

---

# 5. Development开发环境

用途：

开发和调试。

---

包含：

## 前端

Desktop App。

---

## 后端

API服务。

---

## 数据库

开发数据库。

---

## AI能力

测试模型。

测试Agent。

---

# 6. Testing测试环境

用途：

验证版本。

---

特点：

接近生产环境。

---

包含：

- 测试数据库；
- 测试Workspace；
- 测试模型配置；
- 测试Connector。

---

禁止：

连接真实生产数据。

---

# 7. Production生产环境

用途：

真实用户使用。

---

要求：

- 稳定；
- 安全；
- 可监控；
- 可恢复。

---

# 8. Desktop部署

## 定位

用户主要入口。

---

支持：

- macOS；
- Windows；
- Linux（未来）。

---

# 9. Desktop打包

支持：

## macOS

例如：

```
.dmg
.app
```

---

## Windows

例如：

```
.exe
.msi
```

---

## Linux

例如：

```
.AppImage
```

---

# 10. Desktop更新机制

支持：

自动更新。

---

包括：

- 应用版本；
- Local Bridge版本；
- 配置迁移。

---

升级流程：

```
检查版本

↓

下载更新

↓

备份数据

↓

升级

↓

启动验证
```

---

# 11. Local Runtime部署

## 定位

本地执行环境。

---

负责：

- 文件访问；
- 本地Agent；
- 本地Tool；
- 本地Connector。

---

# 12. Local Bridge部署

组件：

Local Bridge。

---

运行：

用户设备。

---

能力：

发现：

- Codex；
- Claude Code；
- Trae；
- WorkBuddy；
- Git；
- IDE。

---

# 13. Backend部署

当前支持：

模块化服务。

---

结构：

```
Backend

├── API Gateway

├── Business Modules

├── AI Runtime

├── Knowledge

├── Memory

└── Analytics
```

---

# 14. 数据库部署

支持：

关系数据库。

---

保存：

- 用户；
- 项目；
- 任务；
- 配置。

---

知识相关：

支持：

向量数据库。

---

用于：

- Knowledge；
- Memory；
- Context检索。

---

# 15. AI服务部署

支持：

## 云模型

例如：

OpenAI。

Anthropic。

Google。

---

## Gateway

例如：

New API。

---

## 本地模型

例如：

Ollama。

---

统一：

Model Gateway管理。

---

# 16. 环境变量管理

敏感配置：

不写入代码。

---

包括：

- API Key；
- 数据库密码；
- Token；
- Secret。

---

使用：

环境变量。

安全配置中心。

---

# 17. 配置管理

配置分类：

```
Application Config

↓

Environment Config

↓

User Config

↓

Workspace Config
```

---

避免：

不同环境混乱。

---

# 18. 数据迁移

版本升级：

需要：

数据库迁移。

---

流程：

```
备份

↓

Migration

↓

验证

↓

启动
```

---

# 19. 日志管理

部署环境需要：

统一日志。

---

包括：

- 应用日志；
- API日志；
- AI执行日志；
- 错误日志。

---

注意：

日志不自动发送给AI。

---

# 20. 监控部署

结合：

第42章可观测系统。

---

监控：

- 服务状态；
- API状态；
- Agent状态；
- 成本。

---

# 21. 备份策略

备份：

## 业务数据

例如：

项目。

任务。

成果。

---

## 配置数据

例如：

能力配置。

Workflow。

---

## Memory

长期经验。

---

# 22. 恢复策略

支持：

恢复：

- 数据库；
- Workspace；
- 配置。

---

目标：

避免数据丢失。

---

# 23. 安全部署要求

包括：

## 网络安全

接口访问控制。

---

## 数据安全

加密存储。

---

## 权限安全

最小权限。

---

# 24. CI/CD流程

自动化：

```
代码提交

↓

测试

↓

构建

↓

部署

↓

验证
```

---

# 25. AI开发部署流程

AI生成代码：

必须经过：

```
开发环境

↓

测试环境

↓

人工验收

↓

生产环境
```

---

禁止：

AI直接修改生产环境。

---

# 26. 版本管理

版本：

```
Major.Minor.Patch
```

---

例如：

```
1.0.0

1.1.0

1.1.1
```

---

记录：

- 新功能；
- 修改；
- 修复。

---

# 27. 企业部署扩展

未来支持：

## SaaS

云端部署。

---

## 私有部署

企业服务器。

---

## 混合部署

云端管理。

本地执行。

---

# 28. 验收标准

部署体系完成后：

Curis可以：

稳定运行。

快速更新。

安全部署。

支持未来扩展。

---

检查：

## 可复制

新环境可以快速搭建。

---

## 可维护

问题可以定位。

---

## 可恢复

故障可以恢复。

---

# 本章冻结内容

本章定义Curis部署与运行环境规范。

核心：

Curis采用本地优先架构，同时预留云端平台演进能力。

部署体系需要支持：

个人使用。

团队协作。

未来企业化运行。

---

下一章：

# 55 开发验收与版本发布规范（Release & Acceptance Specification）