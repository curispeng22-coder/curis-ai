# Curis Official Docs v1.0

# 04 AI Organization Model（AI组织模型）

版本：v1.0

---

# 1. 模型定位

AI Organization Model 是 Curis 的核心产品模型。

定义：

> 如何让AI从单个工具，变成可以承担职责、协作完成业务的数字组织。

---

# 2. 核心理念

传统AI使用方式：

```
用户

↓

选择工具

↓

输入问题

↓

获得回答
```

---

Curis模式：

```
用户目标

↓

AI组织

↓

AI员工

↓

能力调用

↓

业务成果
```

---

# 3. AI组织基本结构

Curis模拟真实组织：

```
用户（Owner）

↓

AI秘书（AI Secretary）

↓

AI管理角色（AI Manager）

↓

专业AI员工（AI Employee）

↓

执行Agent

↓

Capability
```

---

# 4. 用户（Owner）

## 定义

用户是AI组织的最终负责人。

---

负责：

- 提出目标；
- 制定方向；
- 审批关键决策；
- 验收成果。

---

用户不需要：

管理每一次模型调用。

---

# 5. AI秘书（AI Secretary）

## 定义

AI秘书是用户与AI组织之间的入口。

---

职责：

- 理解用户目标；
- 创建项目；
- 协调员工；
- 汇总结果；
- 提醒风险。

---

例如：

用户：

“我要运营一个小红书账号。”

---

AI秘书：

理解：

```
目标：

账号增长


需要：

内容团队

数据分析

创作流程
```

---

# 6. AI员工（AI Employee）

## 定义

AI员工是Curis真正承担工作的主体。

---

AI员工不是：

- 模型；
- Prompt；
- Agent。

---

AI员工是：

具有职责的数字角色。

---

# 7. AI员工组成

```
AI Employee

├── Identity

├── Role

├── Responsibility

├── Capability Profile

├── Memory

├── Project Assignment

└── Work History
```

---

# 8. Identity（身份）

定义：

员工是谁。

---

包括：

- 名称；
- 描述；
- 所属部门；
- 状态。

---

示例：

```
姓名：

研发负责人


部门：

研发部
```

---

# 9. Role（角色）

定义：

员工承担什么职位。

---

示例：

```
研发负责人

内容负责人

数据分析师

产品经理
```

---

角色决定：

工作范围。

---

# 10. Responsibility（职责）

定义：

员工负责什么。

---

例如：

研发负责人：

```
负责：

技术方案

开发管理

代码质量
```

---

内容负责人：

```
负责：

内容策略

生产流程

数据复盘
```

---

# 11. Capability Profile（能力配置）

## 定义

员工能够使用的能力组合。

---

结构：

```
Employee

↓

Capability Profile

↓

Capability
```

---

示例：

研发负责人：

```
软件开发模式

=

Coding Agent

+

Codex

+

Git

+

Testing Workflow
```

---

# 12. Project Assignment（项目关系）

AI员工不是全局孤立存在。

---

员工属于：

部门。

---

参与：

项目。

---

关系：

```
Department

↓

Employee

↓

Project
```

---

# 13. AI员工生命周期

状态：

```
Created

↓

Configured

↓

Working

↓

Learning

↓

Paused

↓

Archived
```

---

# 14. AI员工工作流程

标准流程：

```
项目目标

↓

负责人理解

↓

任务拆解

↓

员工执行

↓

成果输出

↓

经验沉淀
```

---

# 15. AI员工协作模型

MVP阶段：

人工组织。

---

例如：

用户创建：

```
内容团队

↓

内容负责人

↓

文案员工

↓

数据员工
```

---

未来：

自动组建团队。

---

# 16. AI员工与Agent关系

必须区分：

---

## AI Employee

负责：

业务职责。

---

## Agent

负责：

具体执行。

---

关系：

```
AI Employee

↓

调用

↓

Agent
```

---

例如：

研发负责人：

调用：

- Coding Agent；
- Testing Agent。

---

# 17. AI员工与Model关系

员工不直接绑定模型。

---

关系：

```
Employee

↓

Capability Profile

↓

Capability

↓

Model
```

---

这样：

未来可以替换模型。

---

# 18. AI员工与Memory关系

员工拥有长期经验。

---

例如：

研发负责人Memory：

保存：

- 技术决策；
- 历史项目经验；
- 最佳实践。

---

# 19. AI员工与Knowledge关系

员工可以访问：

相关知识。

---

例如：

内容员工：

读取：

- 内容资料；
- 用户画像；
- 历史数据。

---

研发员工：

读取：

- 代码；
- 技术文档；
- Bug记录。

---

# 20. AI团队模型

多个员工组成：

AI Team。

---

例如：

软件研发团队：

```
研发负责人

↓

产品分析员工

↓

开发员工

↓

测试员工

↓

部署员工
```

---

# 21. MVP实现范围

MVP实现：

```
用户

↓

部门

↓

AI员工

↓

能力配置

↓

项目执行
```

---

支持：

人工创建员工。

人工配置能力。

---

# 22. MVP暂不实现

暂不实现：

## 自动招聘AI员工

未来：

根据目标自动生成团队。

---

## 自动组织协作

未来：

AI员工自主会议。

---

## 自动绩效优化

未来：

根据数据调整组织。

---

# 23. AI组织未来演进

阶段：

```
MVP

人工管理AI员工


↓

智能阶段

AI辅助管理员工


↓

高级阶段

AI自主组织协作
```

---

# 24. 核心价值

AI组织模型解决：

传统AI：

“一个AI回答一次问题”。

---

Curis：

“一个AI组织持续完成业务”。

---

# 本文档状态

状态：

Active

---

用途：

定义Curis AI员工和组织模型。

所有员工系统、项目系统、Capability系统必须遵循该模型。

---

下一篇：

# 05 Capability Platform（能力平台）