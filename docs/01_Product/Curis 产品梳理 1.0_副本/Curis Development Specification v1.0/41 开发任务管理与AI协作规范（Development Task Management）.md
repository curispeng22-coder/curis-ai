# Curis Development Specification

# 41 开发任务管理与AI协作规范（Development Task Management）

版本：v1.0-draft

---

# 1. 系统定位

开发任务管理系统用于管理：

Curis自身研发过程。

以及未来：

AI辅助软件开发流程。

---

# 2. 核心理念

开发不是：

直接让AI写代码。

---

而是：

```
产品目标

↓

开发任务

↓

AI开发Agent

↓

代码实现

↓

测试验证

↓

产品验收
```

---

# 3. 开发任务对象

Development Task：

```
Development Task

├── 目标

├── 背景

├── 产品依据

├── 技术要求

├── 输入资料

├── 执行Agent

├── 输出结果

├── 测试

└── 验收
```

---

# 4. 开发任务来源

支持：

## 产品需求

例如：

新增项目工作区。

---

## Bug修复

例如：

修复任务状态异常。

---

## 技术优化

例如：

优化Context Engine。

---

## 架构调整

例如：

调整Capability结构。

---

# 5. 开发任务创建

流程：

```
创建任务

↓

关联产品文档

↓

指定模块

↓

设置目标

↓

分配开发Agent

↓

执行
```

---

# 6. 任务输入规范

AI开发Agent执行任务前：

必须提供：

---

## 产品输入

包括：

- Product Bible章节；
- Development Specification章节；
- 页面规格。

---

## 技术输入

包括：

- 架构；
- 数据模型；
- API。

---

## 验收输入

包括：

- 完成标准；
- 测试要求。

---

# 7. AI开发Agent角色

支持：

不同开发能力。

---

例如：

## 前端Agent

负责：

- 页面；
- 组件；
- 交互。

---

## 后端Agent

负责：

- API；
- 数据；
- 服务。

---

## 测试Agent

负责：

- 测试；
- 验证；
- 问题发现。

---

## 架构Agent

负责：

- 技术方案；
- 代码审查。

---

# 8. 多开发Agent协作

支持：

```
产品Agent

↓

架构Agent

↓

前端Agent

↓

后端Agent

↓

测试Agent

↓

Review Agent
```

---

# 9. AI开发上下文

开发Agent不读取全部项目。

---

通过：

Context Engine。

生成：

Development Context。

---

包含：

- 任务目标；
- 相关代码；
- 技术规范；
- 历史决策；
- 验收标准。

---

# 10. 开发执行流程

```
任务创建

↓

Context生成

↓

Agent选择

↓

代码修改

↓

测试

↓

Review

↓

合并

↓

验收
```

---

# 11. 代码修改规范

AI开发Agent修改代码：

需要：

说明：

修改什么。

为什么修改。

影响什么。

---

输出：

```
修改文件

↓

修改内容

↓

测试结果

↓

风险
```

---

# 12. Git协作

支持：

关联：

Git仓库。

---

记录：

- Branch；
- Commit；
- Diff；
- Pull Request。

---

# 13. 开发状态

统一：

```
Draft

↓

Ready

↓

Developing

↓

Testing

↓

Reviewing

↓

Accepted

↓

Released
```

---

# 14. 开发结果验收

检查：

## 产品

是否符合需求。

---

## 技术

代码是否稳定。

---

## 测试

是否通过。

---

## 扩展

是否破坏架构。

---

# 15. AI代码审查

Review Agent负责：

检查：

---

## 代码质量

结构。

规范。

维护性。

---

## 安全

权限。

漏洞。

---

## 架构

是否符合Curis设计。

---

# 16. 开发Memory沉淀

开发完成后：

提取：

技术经验。

---

例如：

```
问题：

Context加载过大。


解决：

增加摘要层。
```

---

进入：

研发部门Memory。

---

# 17. 开发成本分析

记录：

- 使用Agent；
- 使用模型；
- Token；
- 时间；
- 成功率。

---

用于：

AI研发效率分析。

---

# 18. AI开发工具切换

开发工具不是固定。

---

支持：

- Codex；
- Claude Code；
- Cursor；
- Trae；
- WorkBuddy。

---

切换保持：

- 项目Context；
- 任务状态；
- Git状态。

---

# 19. 开发任务与智能调度

任务提出：

需要什么能力。

---

调度中心选择：

开发Agent。

模型。

工具。

---

例如：

代码重构：

选择：

Claude Code。

---

新功能开发：

选择：

Codex。

---

# 20. UI设计要求

开发中心展示：

不是聊天。

---

展示：

```
开发任务

↓

负责人

↓

执行Agent

↓

代码状态

↓

测试状态

↓

成果
```

---

# 21. API设计

## 创建开发任务

```
POST /development/tasks
```

---

## 分配Agent

```
POST /development/tasks/{id}/agent
```

---

## 获取状态

```
GET /development/tasks/{id}
```

---

## 提交结果

```
POST /development/tasks/{id}/result
```

---

# 22. 验收标准

开发任务系统完成后：

用户可以：

管理AI开发流程。

切换开发Agent。

追踪代码变化。

查看执行结果。

---

检查：

## 可控

知道AI改了什么。

---

## 可追踪

知道为什么修改。

---

## 可复用

经验可以沉淀。

---

# 本章冻结内容

本章定义Curis开发任务管理体系。

核心：

AI开发工具只是执行者。

Curis负责管理：

目标。

任务。

上下文。

能力。

结果。

---

下一章：

# 42 系统监控与可观测性规范（Observability System）