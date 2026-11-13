# Curis Development Specification

# 16 Workflow系统开发规格（Workflow Specification）

版本：v1.0-draft

---

# 1. 页面定位

Workflow系统负责定义和执行：

> 任务如何完成。

Workflow不是业务本身。

业务由：

Business Definition

↓

Project

↓

Task

定义。

Workflow负责：

执行过程。

---

# 2. 核心关系

```
业务目标

↓

项目

↓

任务

↓

Workflow

↓

节点

↓

能力

↓

成果
```

---

# 3. Workflow组成

一个Workflow包含：

```
Workflow

├── Trigger

├── Nodes

├── Conditions

├── Inputs

├── Outputs

├── Approval

└── Runtime Record
```

---

# 4. Trigger触发器

负责：

决定Workflow什么时候启动。

---

支持：

## 手动触发

用户点击执行。

例如：

运行一次内容分析。

---

## 定时触发

按照时间执行。

例如：

每天10点收集热点。

---

## 条件触发

满足条件执行。

例如：

Token超过限制。

---

## 事件触发

系统事件发生。

例如：

任务完成。

成果生成。

---

# 5. Workflow节点

节点是执行步骤。

---

支持：

## Agent节点

调用：

AI员工。

---

例如：

内容分析Agent。

代码Agent。

---

## Model节点

调用：

模型能力。

---

例如：

生成文本。

分析数据。

---

## Tool节点

调用：

工具。

---

例如：

Git。

浏览器。

文件。

---

## Data节点

处理：

数据。

---

## Approval节点

等待：

人工确认。

---

## Condition节点

判断：

下一步流程。

---

# 6. Workflow编辑

组件：

WorkflowEditor

---

支持：

创建节点。

连接节点。

配置参数。

设置条件。

测试运行。

---

展示：

流程图。

节点详情。

运行状态。

---

# 7. Workflow创建方式

支持：

## 模板创建

选择已有Workflow。

---

例如：

自动测试。

日报生成。

热点分析。

---

## AI生成

用户描述：

“每天帮我分析竞争对手。”

---

AI生成：

Workflow草案。

---

## 手动编辑

高级用户：

调整节点。

条件。

参数。

---

# 8. Workflow输入输出

## 输入

来源：

用户。

项目。

任务。

资料。

数据。

---

例如：

内容分析Workflow：

输入：

账号信息。

历史内容。

热点数据。

---

## 输出

包括：

成果。

数据。

状态。

建议。

---

# 9. Workflow运行

组件：

WorkflowRuntime

---

执行过程：

```
Trigger

↓

Node1

↓

Node2

↓

Node3

↓

Output
```

---

记录：

开始时间。

结束时间。

节点状态。

调用能力。

错误。

成本。

---

# 10. Workflow状态

支持：

```
Draft

↓

Testing

↓

Running

↓

Paused

↓

Failed

↓

Completed

↓

Archived
```

---

# 11. Workflow失败处理

失败时记录：

失败节点。

错误原因。

调用能力。

输入数据。

---

处理方式：

## 重试

重新执行。

---

## 跳过

继续后续节点。

---

## 切换能力

使用备用能力。

---

## 转人工

等待负责人处理。

---

# 12. Workflow版本管理

Workflow支持版本。

---

例如：

内容分析Workflow：

v1：

基础热点分析。

---

v2：

增加用户画像分析。

---

项目可以选择：

使用版本。

升级版本。

---

# 13. Workflow权限

控制：

谁可以：

查看。

编辑。

执行。

发布。

---

例如：

个人Workflow。

部门Workflow。

平台Workflow。

---

# 14. Workflow与业务模板关系

Business Definition：

定义：

需要什么流程。

---

Workflow：

提供：

执行方式。

---

例如：

内容增长模板：

需要：

热点分析。

---

绑定：

热点分析Workflow。

---

# 15. Workflow与能力系统关系

Workflow不固定绑定：

某个模型。

---

执行时：

通过：

Capability Router。

选择能力。

---

例如：

内容生成Workflow：

可以使用：

GPT。

Claude。

其他模型。

---

# 16. 自动化任务关系

自动化任务：

引用Workflow。

---

关系：

```
Automation Task

↓

Workflow

↓

Capability

↓

Result
```

---

例如：

每天10点：

执行热点分析Workflow。

---

# 17. 预算控制

Workflow支持：

设置：

Token限制。

成本限制。

时间限制。

失败次数。

---

达到限制：

暂停。

通知。

等待确认。

---

# 18. Workflow运行记录

组件：

WorkflowRunHistory

---

记录：

运行时间。

输入。

节点过程。

输出。

错误。

成本。

---

支持：

查看详情。

重新运行。

复制配置。

---

# 19. AI秘书协助

AI秘书可以：

创建Workflow。

---

例如：

用户：

“每天帮我整理AI新闻。”

---

生成：

新闻整理Workflow。

---

AI秘书可以：

解释Workflow。

---

例如：

“这个自动任务怎么运行？”

---

# 20. API需求

## 获取Workflow列表

```
GET /workflows
```

---

## 创建Workflow

```
POST /workflows
```

---

## 测试Workflow

```
POST /workflows/{id}/test
```

---

## 执行Workflow

```
POST /workflows/{id}/run
```

---

## 获取运行记录

```
GET /workflows/{id}/runs
```

---

# 21. 页面状态

支持：

无Workflow。

创建中。

测试中。

运行中。

等待审批。

失败。

完成。

---

# 22. 验收标准

Workflow系统完成后：

用户可以：

创建流程。

绑定任务。

调用能力。

查看执行。

处理异常。

优化流程。

---

检查：

## 产品

业务和执行分离。

---

## 扩展

新增业务通过Workflow组合完成。

---

## AI

支持多Agent、多模型协作。

---

# 本章冻结内容

本章定义Workflow系统开发规格。

核心：

Workflow负责执行过程。

Business Definition负责业务逻辑。

Task负责具体工作。

三者保持独立。

---

下一章：

# 17 Memory系统开发规格（Memory Specification）