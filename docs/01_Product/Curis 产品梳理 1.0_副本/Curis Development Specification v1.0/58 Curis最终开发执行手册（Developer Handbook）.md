# Curis Development Specification

# 58 Curis最终开发执行手册（Developer Handbook）

版本：v1.0-draft

---

# 1. 手册定位

本手册用于指导：

- 产品团队；
- 前端团队；
- 后端团队；
- AI开发Agent；
- 测试团队；

如何按照 Curis 统一架构进行开发。

---

# 2. 核心目标

所有开发活动必须围绕：

```
用户目标

↓

AI组织

↓

任务执行

↓

成果产生

↓

经验沉淀
```

展开。

---

# 3. 开发最高原则

## 原则1：产品优先

所有代码必须服务：

产品目标。

---

开发前必须确认：

- 对应Product Bible章节；
- 对应Development章节；
- 验收标准。

---

# 原则2：架构优先

禁止：

为了快速实现破坏整体架构。

---

例如：

错误：

```
项目页面

↓

直接调用Claude API
```

---

正确：

```
项目任务

↓

Capability

↓

Model Gateway

↓

Provider
```

---

# 原则3：能力解耦

Curis不绑定：

- ChatGPT；
- Codex；
- Claude Code；
- Gemini；
- New API。

---

统一：

```
Capability

↓

Orchestration

↓

Execution
```

---

# 原则4：配置优先

避免硬编码。

---

例如：

错误：

```javascript
if(model=="claude")
```

---

正确：

```
Capability Configuration

↓

Router

↓

Model
```

---

# 原则5：长期演进

所有设计需要考虑：

- Memory；
- Context；
- Workspace；
- Admin；
- Cloud。

---

# 4. 开发流程规范

标准流程：

```
需求确认

↓

方案设计

↓

任务拆解

↓

开发实现

↓

测试验证

↓

Review

↓

发布
```

---

# 5. 开发任务规范

每个任务必须包含：

```
任务名称

目标

产品依据

技术依据

影响范围

实现方案

测试方案

验收标准
```

---

# 6. AI开发Agent使用规范

AI开发Agent是：

开发执行者。

不是：

架构决策者。

---

执行前必须读取：

```
Product Bible

+

Development Specification

+

当前任务Context
```

---

# 7. AI开发输出规范

每次开发完成：

必须输出：

```
修改内容

↓

修改原因

↓

影响范围

↓

测试结果

↓

风险
```

---

# 8. 前端开发规范

前端必须遵守：

## 使用Design System

禁止：

重复创建组件。

---

## 使用统一状态管理

禁止：

页面私自维护业务状态。

---

## AI交互统一

必须使用：

- AI Assistant；
- Capability Switcher；
- Agent Status。

---

# 9. 后端开发规范

后端必须遵守：

## 模块边界

例如：

Task Service。

不能直接修改：

Agent内部逻辑。

---

## API规范

必须符合：

第51章。

---

## 数据规范

必须符合：

第50章。

---

# 10. AI系统开发规范

AI相关开发必须考虑：

```
Agent

+

Prompt

+

Memory

+

Context

+

Capability
```

---

禁止：

只优化Prompt。

忽略：

数据。

上下文。

能力。

---

# 11. Memory开发规范

Memory不是日志。

---

保存：

长期有效经验。

---

不保存：

临时执行过程。

---

判断标准：

是否未来仍有价值。

---

# 12. Context开发规范

Context目标：

最少信息完成任务。

---

禁止：

每次加载全部历史。

---

优先：

```
任务

↓

项目摘要

↓

相关Memory

↓

相关Knowledge
```

---

# 13. Capability开发规范

新增能力必须定义：

```
名称

类型

输入

输出

权限

成本

状态
```

---

支持：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow；
- Connector。

---

# 14. UI设计规范

用户看到：

业务。

---

不要看到：

复杂技术。

---

例如：

展示：

```
软件开发模式
```

而不是：

```
Claude + MCP + Git Tool + Workflow
```

---

高级用户：

可以展开查看。

---

# 15. 数据安全规范

任何AI执行：

必须经过：

```
身份验证

↓

权限检查

↓

能力授权

↓

执行记录
```

---

# 16. 测试规范

发布前必须验证：

## 软件

功能。

接口。

性能。

---

## AI

Agent。

Prompt。

Memory。

Context。

---

## 数据

权限。

一致性。

---

# 17. 代码提交规范

提交必须包含：

```
功能说明

修改范围

测试结果

关联任务
```

---

示例：

```
feat:

add capability switcher

Task:

T010
```

---

# 18. Git规范

分支：

```
main

develop

feature/*
bugfix/*
```

---

流程：

```
开发

↓

Commit

↓

Review

↓

Merge
```

---

# 19. 发布规范

发布必须经过：

```
测试环境

↓

验收

↓

Release Candidate

↓

正式版本
```

---

# 20. 禁止事项

禁止：

## 绑定单一AI工具

例如：

只支持Codex。

---

## 页面硬编码业务

例如：

写死研发页面。

---

## 大量复制代码

优先组件化。

---

## 无记录修改

所有变化必须可追踪。

---

# 21. 当前开发重点

团队优先关注：

```
Workspace闭环

↓

AI员工

↓

Capability

↓

Task执行

↓

Memory

↓

Context

↓

智能调度
```

---

# 22. 后续扩展

未来：

```
Admin

↓

企业

↓

Marketplace

↓

Developer Ecosystem
```

---

# 23. 最终验收标准

Curis开发完成后：

用户能够：

打开Curis。

创建AI公司。

创建项目。

管理AI员工。

调用不同AI能力。

完成真实任务。

沉淀经验。

持续优化。

---

# 本章冻结内容

本章定义Curis开发执行手册。

核心：

所有团队和AI开发Agent必须围绕统一产品架构开发。

Curis不是多个AI工具拼接。

而是：

一个能够组织AI员工、调度AI能力、沉淀知识并持续成长的AI工作系统。

---

# Curis Development Specification v1.0 完成