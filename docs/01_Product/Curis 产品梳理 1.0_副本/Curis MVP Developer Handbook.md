# Curis MVP Developer Handbook

版本：v1.0

---

# 1. 项目目标

Curis MVP目标：

建立一个完整可运行的AI工作组织系统。

不是：

- AI聊天工具；
- 模型调用工具；
- 任务管理软件。

---

最终用户体验：

```
创建AI公司

↓

建立部门

↓

创建AI员工

↓

创建业务项目

↓

配置能力

↓

执行任务

↓

获得成果

↓

沉淀经验
```

---

# 2. MVP开发原则

## 原则1：产品模型完整

MVP必须具备：

```
Company

Department

Employee

Project

Task

Capability

Artifact
```

---

## 原则2：智能程度逐步增加

MVP：

人工配置。

未来：

自动智能。

---

例如：

MVP：

```
研发员工

绑定：

Codex

Git

测试Workflow
```

---

未来：

```
任务

↓

自动选择最佳能力
```

---

## 原则3：能力必须抽象

禁止：

业务直接绑定AI工具。

---

错误：

```
项目页面

↓

调用Claude API
```

---

正确：

```
Project

↓

Task

↓

Capability

↓

Model/Agent/Tool
```

---

# 3. MVP范围

## 必须完成

---

## Workspace

包括：

- 公司；
- 部门；
- 项目；
- 任务。

---

## AI员工

包括：

- 创建；
- 角色；
- 职责；
- 能力绑定。

---

## Capability

包括：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow。

---

## 成果

包括：

- 文档；
- 文件；
- 代码；
- 内容。

---

## 基础Memory

包括：

- 用户偏好；
- 项目背景；
- 员工经验。

---

# 4. MVP业务场景

## 场景1：研发团队

流程：

```
研发部

↓

研发负责人

↓

开发项目

↓

代码任务

↓

Codex/Claude Code

↓

代码成果
```

---

## 场景2：内容团队

流程：

```
内容部

↓

内容负责人

↓

账号增长项目

↓

选题任务

↓

文案任务

↓

图片任务

↓

内容成果
```

---

支持：

- 小红书；
- 抖音；
- 头条；
- 公众号。

---

## 场景3：知识团队

流程：

```
知识库

↓

研究项目

↓

资料分析

↓

报告成果
```

---

# 5. 当前不开发

明确延期：

---

## 智能调度中心

暂不自动选择：

- 模型；
- Agent；
- Skill。

---

## 多Agent自治团队

暂不实现复杂自主协作。

---

## Marketplace

暂不开放第三方生态。

---

## 企业Admin

暂不做企业权限。

---

# 6. 开发架构约束

所有开发遵循：

```
Frontend

↓

API

↓

Backend Service

↓

Capability Layer

↓

Provider
```

---

禁止：

跨层调用。

---

# 7. 前端开发规则

必须：

使用：

Frontend Design System。

---

禁止：

单独创建页面风格。

---

AI相关组件统一：

- AI秘书；
- Capability Switcher；
- Agent状态；
- Task执行面板。

---

# 8. 后端开发规则

必须：

模块化。

---

核心模块：

```
Workspace

Project

Task

Employee

Capability

Memory

Knowledge
```

---

禁止：

业务逻辑写死在接口。

---

# 9. AI开发规则

AI开发工具：

不是团队。

---

统一使用：

```
Git

+

Task

+

Documentation
```

---

支持：

- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor。

---

# 10. 开发任务流程

所有开发：

必须经过：

```
Task创建

↓

读取上下文

↓

方案设计

↓

代码实现

↓

测试

↓

Review

↓

Merge
```

---

# 11. AI工具交接

额度耗尽或切换工具：

必须生成：

Handoff Report。

---

包含：

```
完成内容

未完成内容

修改文件

技术决策

下一步
```

---

# 12. Git规则

统一：

```
main

develop

feature/*
```

---

提交必须说明：

```
功能

范围

测试
```

---

# 13. 验收标准

功能完成必须满足：

---

## 产品

符合需求。

---

## 架构

符合规范。

---

## 测试

通过验证。

---

## 文档

同步更新。

---

# 14. 开发优先级

排序：

```
P0

用户闭环


P1

AI员工


P2

Capability


P3

业务场景


P4

Memory


P5

体验优化
```

---

# 15. 开发团队每日入口

开发人员每日只关注：

```
当前Sprint

↓

当前Task

↓

相关规范

↓

代码实现
```

---

不要：

阅读全部历史文档。

---

# 本手册冻结内容

Curis MVP开发团队唯一执行目标：

构建一个完整AI组织工作系统。

通过：

Workspace。

AI员工。

Capability。

项目。

任务。

成果。

形成真实业务闭环。

---

所有未来智能化能力：

在此基础上增强。