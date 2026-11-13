# Curis Official Docs v1.0

# 06 Knowledge & Memory System（知识与记忆系统）

版本：v1.0

---

# 1. 系统定位

Knowledge & Memory System 是 Curis 实现长期工作的核心基础。

负责解决：

- AI不知道历史背景；
- 每次任务需要重新解释；
- 上下文越来越长；
- Token消耗越来越高；
- 知识无法沉淀。

---

# 2. 核心理念

Curis不通过：

```
不断增加聊天上下文
```

解决长期工作。

---

而通过：

```
Knowledge

+

Memory

+

Context Engine

```

构建长期智能。

---

# 3. Knowledge与Memory区别

必须明确：

二者不是同一个系统。

---

# Knowledge（知识）

回答：

> 外部信息是什么。

---

来源：

- 文档；
- 文件；
- 网页；
- Git代码；
- 数据库；
- Obsidian。

---

例如：

```
React官方文档

↓

技术知识
```

---

# Memory（记忆）

回答：

> Curis过去工作中积累了什么经验。

---

来源：

- 用户习惯；
- 项目经验；
- 员工经验；
- 决策记录。

---

例如：

```
这个项目之前采用模块化架构效果最好。

↓

研发Memory
```

---

# 4. Knowledge系统架构

结构：

```
Source

↓

Document

↓

Knowledge Node

↓

Knowledge Graph

↓

Context调用
```

---

# 5. Knowledge Source（知识来源）

支持：

## 本地资料

例如：

- 文件夹；
- PDF；
- 文档。

---

## 项目资料

例如：

- 需求文档；
- 技术方案；
- 项目记录。

---

## 外部连接

例如：

- Obsidian；
- GitHub；
- 云存储。

---

# 6. Knowledge Node（知识节点）

知识被解析后：

形成结构化节点。

---

例如：

文档：

```
数据库设计方案
```

转换：

```
Knowledge Node

类型：

Technical Document


关联：

研发项目

数据库模块

相关代码
```

---

# 7. Knowledge Graph（知识关系）

## 定义

连接知识之间关系。

---

示例：

```
技术方案

↓

项目

↓

代码

↓

Bug

↓

解决方案
```

---

价值：

AI不仅知道内容。

还能理解关系。

---

# 8. Memory系统架构

Memory分层：

```
User Memory

↓

Employee Memory

↓

Project Memory

↓

Department Memory

↓

Company Memory
```

---

# 9. User Memory（用户记忆）

保存：

用户长期偏好。

---

例如：

```
用户喜欢：

简洁方案

优先考虑长期架构

需要明确执行路径
```

---

# 10. Employee Memory（员工记忆）

保存：

AI员工工作经验。

---

例如：

研发负责人：

```
历史项目：

采用模块化架构

减少后期维护成本
```

---

# 11. Project Memory（项目记忆）

保存：

项目长期背景。

---

例如：

```
项目目标

技术决策

重要讨论

历史问题
```

---

作用：

项目重新打开时：

无需重新介绍。

---

# 12. Department Memory（部门记忆）

保存：

部门经验。

---

例如：

研发部：

```
代码规范

最佳实践

常见问题
```

---

# 13. Company Memory（公司记忆）

保存：

组织级经验。

---

例如：

```
业务流程

管理规则

长期战略
```

---

# 14. Memory生成原则

Memory不是日志。

---

不能保存：

```
10:30调用一次API失败
```

---

应该保存：

```
以后开发接口时必须先定义数据模型。
```

---

判断标准：

是否未来仍然有价值。

---

# 15. Memory生命周期

流程：

```
执行过程

↓

分析

↓

判断价值

↓

生成Memory

↓

未来调用
```

---

不是：

所有执行记录自动进入Memory。

---

# 16. Context Engine关系

Knowledge和Memory不会直接全部发送给AI。

---

流程：

```
Task

↓

Context Engine

↓

检索Knowledge

↓

检索Memory

↓

生成Context Package

↓

Agent执行
```

---

# 17. Context优化目标

目标：

最少信息完成任务。

---

错误方式：

```
加载整个项目历史
```

---

正确方式：

```
当前任务

+

相关知识

+

相关经验
```

---

# 18. Token优化原则

减少：

无效上下文。

---

例如：

开发登录功能：

不需要读取：

整个公司历史。

---

只需要：

```
登录相关代码

+

历史设计

+

相关Bug经验
```

---

# 19. MVP实现范围

MVP实现：

---

## Knowledge

支持：

- 文件；
- 项目资料；
- 基础搜索。

---

## Memory

支持：

- 用户Memory；
- 项目Memory；
- 员工基础Memory。

---

## Context

支持：

基础检索和调用。

---

# 20. MVP不实现

暂不实现：

---

## 自动Memory进化

未来：

AI自动总结经验。

---

## 完整Knowledge Graph推理

未来：

复杂关系分析。

---

## 自动知识治理

未来：

自动清理、更新。

---

# 21. 与AI员工关系

AI员工通过：

Memory + Knowledge

获得长期能力。

---

关系：

```
AI Employee

↓

Memory

↓

Knowledge

↓

Context

↓

Execution
```

---

# 22. 与Capability关系

Capability提供：

执行能力。

---

Knowledge提供：

信息。

---

Memory提供：

经验。

---

三者共同组成：

AI员工能力。

---

# 23. 安全原则

知识和Memory必须：

权限隔离。

---

例如：

个人Memory：

不能被其他员工访问。

---

研发知识：

不能默认开放给内容部门。

---

# 24. 未来演进

阶段：

```
MVP

基础保存和检索


↓

智能阶段

自动总结经验


↓

高级阶段

AI组织持续学习
```

---

# 25. 核心价值

Knowledge解决：

“AI知道什么”。

---

Memory解决：

“AI经历过什么”。

---

Context解决：

“AI现在应该用什么”。

---

三者共同解决：

AI长期工作能力。

---

# 本文档状态

状态：

Active

---

用途：

定义Curis知识和记忆体系。

所有长期智能、上下文优化、AI员工成长能力必须遵循该模型。

---

下一篇：

# 07 MVP Specification（MVP产品实施规范）