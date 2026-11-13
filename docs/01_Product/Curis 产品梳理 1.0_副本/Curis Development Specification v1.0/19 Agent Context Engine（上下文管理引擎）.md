# Curis Development Specification

# 19 Agent Context Engine（上下文管理引擎）

版本：v1.0-draft

---

# 1. 系统定位

Agent Context Engine 是 Curis 多Agent体系中的核心上下文调度系统。

负责解决：

- 长期项目上下文膨胀；
- Agent遗忘历史；
- 大量资料导致Token浪费；
- 多Agent之间上下文不一致。

---

# 2. 核心目标

让Agent在执行任务时：

获得：

> 足够的信息。

而不是：

> 所有信息。

---

目标：

```
最少Token

+

最高相关性

+

完整任务理解
```

---

# 3. 传统AI问题

传统方式：

```
用户

↓

发送完整历史聊天

↓

发送全部资料

↓

模型处理

↓

执行
```

问题：

---

## 上下文无限增长

长期项目：

几个月甚至几年。

历史内容越来越多。

---

## Token成本增加

每次调用：

重复发送。

---

## 速度下降

Context越大：

模型处理越慢。

---

## 信息干扰

无关历史降低判断质量。

---

# 4. Curis上下文架构

Curis采用：

分层Context。

---

结构：

```
L0 当前输入

↓

L1 当前任务Context

↓

L2 项目Context

↓

L3 员工Memory

↓

L4 部门/公司Memory

↓

L5 Knowledge检索

↓

Agent执行
```

---

# 5. Context Package

每次Agent执行前：

生成：

Context Package。

---

不是直接读取：

全部资料。

---

而是生成：

任务专属上下文包。

---

结构：

```
Context Package

├── Task Goal

├── Current Status

├── Relevant Memory

├── Relevant Knowledge

├── Required Tools

├── Constraints

└── Output Requirement
```

---

# 6. Context生成流程

流程：

```
Task创建

↓

分析任务类型

↓

识别执行Agent

↓

检索Memory

↓

检索Knowledge

↓

压缩摘要

↓

生成Context Package

↓

发送Agent
```

---

# 7. Context来源优先级

不同来源优先级：

---

## 第一优先

当前任务。

例如：

用户刚提出的需求。

---

## 第二优先

项目Memory。

例如：

当前项目目标。

历史决策。

---

## 第三优先

员工Memory。

例如：

研发经验。

工作习惯。

---

## 第四优先

Knowledge。

例如：

文档。

代码。

资料。

---

## 第五优先

历史日志。

只有需要时读取。

---

# 8. Context检索机制

采用：

相关性检索。

---

根据：

任务。

角色。

项目。

时间。

标签。

关系。

选择内容。

---

例如：

研发任务：

查询：

```
研发项目Memory

+

技术文档

+

相关代码

+

历史Bug
```

---

不会加载：

内容运营资料。

---

# 9. Context压缩

长期项目：

自动压缩。

---

例如：

100次会议记录。

转换：

```
项目长期摘要

+

关键决策

+

历史问题

+

经验
```

---

保留：

价值。

删除：

噪音。

---

# 10. Context摘要层

系统维护：

多级摘要。

---

## 项目摘要

例如：

```
Curis研发项目：

目标：

完成AI工作台。

当前阶段：

前端开发。

主要风险：

Agent调度。
```

---

## 任务摘要

例如：

```
首页开发任务：

已完成：

布局。

剩余：

AI秘书交互。
```

---

## 会话摘要

保存：

最近讨论重点。

---

# 11. Context缓存

避免重复生成。

---

缓存：

项目Context。

任务Context。

AgentContext。

---

当：

项目没有变化。

直接复用。

---

# 12. Context更新机制

触发：

## 新任务

重新生成。

---

## 项目重大变化

更新。

---

## 新成果产生

补充。

---

## 会议决策

更新。

---

# 13. 多Agent Context共享

多个Agent协作：

共享：

项目Context。

---

例如：

研发：

产品Agent。

开发Agent。

测试Agent。

---

共享：

目标。

约束。

成果。

---

但：

保留：

各自专业Memory。

---

# 14. Agent隔离机制

不同Agent不应该读取：

全部其他Agent记忆。

---

例如：

开发Agent：

不需要：

市场营销Memory。

---

避免：

无关信息污染。

---

# 15. Context Token优化

优化策略：

---

## 摘要替代

长文本。

↓

摘要。

---

## 检索替代

全部资料。

↓

相关资料。

---

## 分层加载

先摘要。

需要时深入。

---

## 缓存复用

避免重复生成。

---

# 16. Context质量评价

指标：

---

## 相关性

Agent是否获得正确信息。

---

## 完整性

是否缺少关键背景。

---

## Token效率

完成任务消耗多少Token。

---

## 成功率

是否提高任务完成率。

---

# 17. Context失败处理

如果：

信息不足。

系统：

提示：

缺少资料。

---

例如：

开发任务：

缺少技术方案。

提示：

是否补充资料。

---

如果：

信息冲突。

提示：

发现多个版本。

需要确认。

---

# 18. AI秘书与Context Engine

AI秘书负责：

理解用户意图。

---

Context Engine负责：

准备执行环境。

---

流程：

```
用户

↓

AI秘书

↓

任务理解

↓

Context Engine

↓

Agent

↓

成果
```

---

# 19. API设计

## 创建Context

```
POST /context/build
```

---

输入：

task_id。

agent_id。

project_id。

---

输出：

Context Package。

---

## 查询Context

```
GET /context/{id}
```

---

## 更新Context

```
PATCH /context/{id}
```

---

# 20. 验收标准

Context Engine完成后：

Agent可以：

长期参与项目。

快速恢复状态。

减少重复输入。

降低Token消耗。

保持多Agent协作一致。

---

# 21. 核心指标

评估：

## Token减少比例

例如：

原：

20000 Token。

优化后：

4000 Token。

---

## 响应速度

Context减少后的提升。

---

## 任务成功率

是否因为上下文优化提升。

---

# 本章冻结内容

本章定义 Agent Context Engine。

核心：

Curis不是简单保存聊天历史。

而是通过：

Memory。

Knowledge。

Context。

Agent。

形成长期工作的智能执行系统。

---

下一章：

# 20 Agent运行与调度系统（Agent Runtime & Orchestration）