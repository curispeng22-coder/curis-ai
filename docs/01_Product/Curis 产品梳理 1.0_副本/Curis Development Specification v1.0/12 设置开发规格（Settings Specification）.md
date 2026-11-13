# Curis Development Specification

# 12 设置开发规格（Settings Specification）

版本：v1.0-draft

---

# 1. 页面定位

设置负责管理 Curis Desktop 的系统配置。

设置不是业务工作区。

业务相关内容进入：

- 项目；
- 组织中心；
- 能力中心；
- 资料中心。

设置负责：

- 用户偏好；
- 系统配置；
- 本地连接；
- 高级管理。

---

# 2. 页面结构

```
Settings

├── 基础设置

├── 账户设置

├── 通知设置

├── 预算设置

├── 数据设置

├── Local Bridge

└── 高级管理
```

---

# 3. 基础设置

组件：

GeneralSettings

---

## 目标

管理 Curis 基础运行体验。

---

## 配置项

包括：

语言。

时区。

主题。

启动页面。

界面偏好。

---

## 操作

保存。

恢复默认。

---

# 4. 账户设置

组件：

AccountSettings

---

## 当前阶段

个人版本。

---

## 展示：

用户名。

头像。

个人信息。

登录信息。

---

## 未来扩展

商业版本：

- 团队账号；
- 企业账号；
- 登录管理。

---

# 5. 通知设置

组件：

NotificationSettings

---

## 目标

管理 Curis 如何提醒用户。

---

## 通知类型

支持：

任务完成。

任务失败。

待决策。

会议提醒。

经营报告。

能力异常。

资料同步。

---

## 通知方式

支持：

应用内。

桌面通知。

未来：

移动端通知。

第三方消息。

---

# 6. 预算设置

组件：

BudgetSettings

---

## 目标

控制 AI 使用成本。

---

## 配置范围

支持：

公司预算。

项目预算。

任务预算。

---

## 限制类型

Token限制。

成本限制。

执行时间限制。

失败次数限制。

---

# 7. 自动停止规则

组件：

ExecutionLimitSettings

---

## 示例

研发项目：

设置：

24小时Token超过阈值。

---

执行：

```
达到限制

↓

暂停任务

↓

通知负责人

↓

等待处理
```

---

用户可以：

调整限制。

恢复执行。

修改预算。

---

# 8. 数据设置

组件：

DataSettings

---

## 管理：

数据存储。

备份。

恢复。

导出。

删除。

---

## 支持：

项目数据导出。

成果导出。

知识导出。

---

# 9. Local Bridge

组件：

LocalBridgeSettings

---

## 页面定位

管理 Curis 与本机环境连接。

---

连接：

- 文件目录；
- Git；
- Obsidian；
- 本地工具。

---

# 10. Local Bridge状态

展示：

连接状态。

版本。

授权目录。

最近操作。

---

状态：

已连接。

未连接。

异常。

权限不足。

---

# 11. 授权管理

组件：

PermissionManager

---

管理：

目录权限。

操作权限。

项目绑定。

---

例如：

授权：

```
/Projects/Curis
```

允许：

读取。

写入。

执行。

---

# 12. 操作记录

组件：

LocalActivityLog

---

记录：

时间。

项目。

员工。

操作。

结果。

---

例如：

```
研发员工

读取：

src/main.ts

结果：

成功
```

---

# 13. 高级管理

组件：

AdminConsole

---

## 当前阶段定位

Curis Desktop 内部管理区域。

---

未来商业化：

迁移到：

Admin 产品。

---

# 14. 业务模板管理

组件：

TemplateManager

---

负责：

Business Definition。

---

功能：

创建模板。

编辑模板。

测试模板。

发布模板。

版本管理。

---

管理：

- 阶段；
- 角色；
- 工作区；
- Workflow；
- 能力；
- 指标。

---

# 15. 业务Agent管理

组件：

BusinessAgentManager

---

负责：

管理业务拆解Agent。

---

功能：

创建。

配置。

测试。

发布。

停用。

---

输出：

Business Definition。

不是：

前端代码。

---

# 16. 能力管理

组件：

AdminCapabilityManager

---

负责：

平台能力。

---

包括：

Model。

Agent。

Skill。

Tool。

Workflow。

MCP。

Connector。

---

功能：

添加。

测试。

发布。

下架。

版本管理。

---

# 17. 治理规则

组件：

GovernanceManager

---

管理：

审批规则。

预算规则。

风险规则。

权限规则。

指标规则。

---

# 18. AI秘书协助

AI秘书可以：

帮助配置系统。

---

示例：

用户：

“连接我的Obsidian。”

AI秘书：

引导：

选择目录。

授权。

测试。

完成。

---

用户：

“设置研发项目每天最多消耗5万Token。”

AI秘书：

生成配置。

等待确认。

---

# 19. API需求

## 基础设置

```
GET /settings

PATCH /settings
```

---

## 通知设置

```
GET /notifications/settings

PATCH /notifications/settings
```

---

## Local Bridge

```
GET /local-bridge/status

POST /local-bridge/connect
```

---

## 模板管理

```
GET /templates

POST /templates

PATCH /templates/{id}
```

---

## 治理规则

```
GET /governance/rules

PATCH /governance/rules
```

---

# 20. 页面状态

支持：

首次配置。

保存中。

保存成功。

连接测试中。

连接成功。

连接失败。

权限不足。

---

# 21. 验收标准

设置完成后：

用户可以：

配置个人环境。

连接本地资源。

管理能力。

管理模板。

设置预算。

控制系统行为。

---

检查：

## 产品

普通用户不会被复杂管理干扰。

---

## 架构

未来可拆分Admin。

---

## 安全

敏感配置受保护。

---

# 本章冻结内容

本章定义设置开发规格。

核心：

设置管理系统环境。

高级管理支撑未来Admin演进。

---

下一章：

# 13 AI秘书开发规格（AI Assistant Specification）