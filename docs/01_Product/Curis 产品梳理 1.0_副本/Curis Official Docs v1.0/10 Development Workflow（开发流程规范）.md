# Curis Official Docs v1.0

# 10 Development Workflow（开发流程规范）

版本：v1.0

---

# 1. 流程定位

本文档定义 Curis MVP 开发过程中：

- 需求如何进入开发；
- AI开发工具如何协作；
- 代码如何提交；
- 如何测试；
- 如何发布。

---

# 2. 核心理念

Curis采用：

```
产品目标

↓

开发任务

↓

AI执行

↓

代码成果

↓

验证发布
```

---

开发不是：

直接让AI写代码。

---

而是：

在明确目标、上下文和约束下，让AI成为研发能力。

---

# 3. 开发流程总览

完整流程：

```
需求提出

↓

Task创建

↓

上下文准备

↓

方案设计

↓

开发实现

↓

测试验证

↓

Code Review

↓

合并发布

↓

经验沉淀
```

---

# 4. Step 1：需求进入

所有开发来源：

必须明确：

- 用户目标；
- 产品价值；
- 所属模块。

---

需求来源：

## 产品需求

例如：

新增AI员工能力配置。

---

## Bug修复

例如：

任务状态异常。

---

## 技术优化

例如：

优化Context加载。

---

# 5. Step 2：创建开发Task

所有开发必须进入Task系统。

---

Task包含：

```
Task ID

名称

目标

产品依据

技术依据

实现范围

验收标准

测试要求
```

---

示例：

```
Task:

EMP-001


目标:

支持创建AI员工


依据:

AI Employee Model


验收:

用户可以创建员工并绑定能力
```

---

# 6. Step 3：上下文准备

AI开发Agent执行前：

必须加载：

---

## 产品Context

包括：

- Product Vision；
- Product Model；
- MVP规范。

---

## 技术Context

包括：

- Architecture；
- Engineering Specification。

---

## 任务Context

包括：

- 当前Task；
- 相关代码；
- 历史记录。

---

# 7. Context加载原则

禁止：

一次加载全部文档。

---

采用：

任务相关加载。

---

例如：

开发员工页面：

加载：

```
AI Employee Model

+

Frontend Specification

+

Employee API
```

---

不加载：

商业规划。

---

# 8. Step 4：方案设计

复杂任务：

必须先输出：

Implementation Plan。

---

格式：

```
问题分析

↓

实现方案

↓

修改范围

↓

影响模块

↓

风险
```

---

确认后：

开始开发。

---

# 9. Step 5：AI开发执行

AI开发Agent负责：

- 编写代码；
- 修改代码；
- 创建测试；
- 更新文档。

---

执行流程：

```
读取Task

↓

分析代码

↓

修改

↓

测试

↓

提交结果
```

---

# 10. 多AI工具协作流程

Curis采用：

```
一个开发团队

+

多个AI工具
```

---

支持：

- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor。

---

工具切换：

不改变：

- 产品目标；
- 架构；
- Task。

---

# 11. AI交接流程

当：

- Token额度结束；
- 切换模型；
- 更换工具；

必须：

生成Handoff Report。

---

包含：

```
当前任务

已完成内容

未完成内容

修改文件

技术决策

问题风险

下一步
```

---

# 12. Git流程

统一：

```
main

↓

develop

↓

feature/*
```

---

开发流程：

```
创建分支

↓

开发

↓

提交

↓

测试

↓

Review

↓

Merge
```

---

# 13. Commit规范

提交格式：

```
type(scope): description
```

---

例如：

```
feat(employee):

add employee creation flow
```

---

提交说明：

必须包含：

- 修改内容；
- 关联Task；
- 测试结果。

---

# 14. Code Review流程

Review检查：

---

## 产品一致性

是否满足需求。

---

## 架构一致性

是否符合Curis设计。

---

## 代码质量

是否：

- 清晰；
- 可维护；
- 可扩展。

---

## 安全

是否：

- 权限正确；
- 数据安全。

---

# 15. 测试流程

代码完成后：

进入测试。

---

包括：

## 功能测试

验证：

用户流程。

---

## 工程测试

验证：

代码和接口。

---

## AI测试

验证：

- Agent行为；
- Prompt；
- Capability。

---

# 16. 发布流程

标准：

```
Development

↓

Testing

↓

Release Candidate

↓

Production
```

---

发布前：

必须确认：

- 测试通过；
- 文档更新；
- 风险确认。

---

# 17. Bug处理流程

Bug：

进入Task系统。

---

记录：

```
问题

↓

原因

↓

修复

↓

验证
```

---

禁止：

临时修改不记录。

---

# 18. Memory沉淀流程

开发结束后：

判断：

是否产生长期经验。

---

如果：

有价值。

进入：

Development Memory。

---

例如：

```
新增Capability必须同步更新Registry。
```

---

不保存：

普通调试过程。

---

# 19. MVP开发优先级

所有任务优先：

```
P0

核心用户闭环


P1

AI员工能力


P2

Capability体系


P3

业务场景


P4

Memory增强


P5

体验优化
```

---

# 20. 新需求控制

新增需求必须判断：

---

是否增强：

```
AI组织工作闭环
```

---

如果：

不是。

进入：

Future Roadmap。

---

# 21. 开发完成标准

一个Task完成：

必须满足：

```
代码完成

+

测试通过

+

Review完成

+

文档更新
```

---

# 22. 开发团队最终工作模式

每天执行：

```
查看Sprint

↓

领取Task

↓

读取相关文档

↓

AI辅助开发

↓

提交结果

↓

更新状态
```

---

# 本文档状态

状态：

Active

---

用途：

定义Curis MVP开发工作流。

所有开发人员和AI开发工具必须遵循该流程。

---

# Curis Official Docs v1.0 第一版整理完成

核心文档：

```
01 Product Vision

02 Product Model

03 System Architecture

04 AI Organization Model

05 Capability Platform

06 Knowledge & Memory System

07 MVP Specification

08 Developer Handbook

09 Engineering Specification

10 Development Workflow
```

---

