# Curis Development Specification

# 23 Curis智能调度中心（Intelligent Capability Orchestration Center）

版本：v1.0-draft

---

# 1. 系统定位

智能调度中心是 Curis 的核心执行大脑。

负责：

根据用户目标、任务需求和当前环境。

自动选择：

- 哪个Agent；
- 哪个模型；
- 哪个Skill；
- 哪个Tool；
- 哪个Workflow；
- 哪个MCP；
- 哪个外部应用。

完成任务。

---

# 2. 核心理念

Curis不管理：

“用户选择哪个AI工具”。

而管理：

“完成目标需要什么能力”。

---

关系：

```
用户目标

↓

任务理解

↓

能力规划

↓

能力组合

↓

执行

↓

成果
```

---

# 3. 能力统一抽象

所有执行资源统一抽象为：

Capability。

---

包括：

```
Capability

├── Agent

├── Model

├── Skill

├── Tool

├── Workflow

├── MCP

├── Connector

└── Local Application
```

---

# 4. 为什么需要统一调度

现实环境：

用户可能同时拥有：

- ChatGPT；
- Codex；
- Claude Code；
- WorkBuddy；
- Trae；
- Cursor；
- Gemini；
- 本地模型。

---

不同工具：

优势不同。

限制不同。

成本不同。

---

Curis负责：

组合最佳能力。

---

# 5. Capability Registry

能力注册中心。

负责记录：

所有可用能力。

---

数据：

```
Capability

├── Name

├── Type

├── Provider

├── Function

├── Input

├── Output

├── Cost

├── Performance

├── Permission

└── Status
```

---

# 6. 能力描述协议

每个能力需要声明：

---

## 能力名称

例如：

Claude Code。

---

## 类型

Agent。

Model。

Tool。

---

## 能完成什么

例如：

代码开发。

---

## 输入要求

例如：

代码目录。

需求文档。

---

## 输出形式

例如：

代码Diff。

报告。

文件。

---

## 限制

例如：

需要API Key。

需要本地安装。

---

# 7. 任务理解层

组件：

Task Understanding Engine。

---

负责分析：

用户真正需要什么。

---

例如：

用户：

“帮我优化首页。”

---

理解：

不是：

调用聊天。

---

而是：

需要：

- UI分析；
- 产品分析；
- 前端修改；
- 测试验证。

---

输出：

能力需求。

---

# 8. 能力规划层

组件：

Capability Planner。

---

根据任务：

生成执行方案。

---

例如：

开发任务：

```
需求分析

↓

产品Agent

↓

设计Agent

↓

Codex

↓

测试Tool

↓

审查Agent
```

---

# 9. 能力选择策略

选择依据：

---

## 任务匹配度

是否适合。

---

## 历史成功率

过去表现。

---

## 成本

Token。

费用。

---

## 速度

响应时间。

---

## 当前状态

是否可用。

---

## 用户偏好

用户指定优先级。

---

# 10. 动态切换机制

执行过程中：

支持切换。

---

例如：

开发任务：

开始：

Codex。

---

发现：

额度不足。

---

自动：

切换：

Claude Code。

---

保持：

同一个Task。

同一个Context。

继续执行。

---

# 11. 模型切换

Model作为Capability。

---

支持：

GPT。

Claude。

Gemini。

DeepSeek。

本地模型。

---

选择依据：

任务复杂度。

成本。

速度。

---

例如：

简单总结：

小模型。

---

架构设计：

高级模型。

---

# 12. Agent切换

支持：

不同Agent执行同一任务。

---

例如：

代码开发：

首选：

Codex。

---

备用：

Claude Code。

---

特殊任务：

Cursor Agent。

---

# 13. Skill组合

Skill不是独立聊天。

而是能力模块。

---

例如：

内容任务：

组合：

```
热点分析Skill

+

标题优化Skill

+

图片生成Skill

+

数据分析Skill
```

---

# 14. Tool调用

Tool负责：

实际操作。

---

例如：

研发：

```
开发Agent

↓

Git Tool

↓

文件Tool

↓

测试Tool
```

---

内容：

```
内容Agent

↓

搜索Tool

↓

图片Tool

↓

发布Tool
```

---

# 15. Workflow调度

Workflow负责：

流程组织。

---

例如：

自动发布：

```
内容生成Workflow

↓

调用：

文案Skill

图片Skill

审核Tool

发布Connector
```

---

# 16. MCP调度

MCP作为外部能力接口。

---

例如：

连接：

GitHub。

Notion。

数据库。

第三方平台。

---

由调度中心统一管理。

---

# 17. 本地应用调度

支持：

调用用户电脑已有AI应用。

---

例如：

检测：

本机安装：

Codex。

Claude Code。

Trae。

---

注册为：

Local Capability。

---

通过：

Local Bridge。

执行。

---

# 18. 能力组合优化

系统根据历史结果：

优化组合。

---

例如：

发现：

研发任务：

Codex + 测试Tool

成功率最高。

---

以后优先推荐。

---

# 19. 能力降级

能力失败：

自动降级。

---

例如：

高级模型不可用。

↓

普通模型。

---

Agent不可用。

↓

备用Agent。

---

Tool失败。

↓

人工处理。

---

# 20. 执行成本优化

调度中心实时考虑：

成本。

---

例如：

任务：

生成日报。

---

选择：

低成本模型。

---

任务：

架构设计。

---

选择：

高能力模型。

---

# 21. 用户控制

用户可以：

设置：

默认能力。

优先级。

预算。

禁止使用。

---

例如：

研发项目：

优先：

Codex。

---

禁止：

某模型。

---

# 22. 调度记录

记录：

```
Task

↓

选择能力

↓

原因

↓

执行结果

↓

成本

↓

优化建议
```

---

用于：

数据洞察。

自进化。

---

# 23. AI秘书关系

AI秘书：

理解用户。

---

调度中心：

安排能力。

---

关系：

```
用户

↓

AI秘书

↓

智能调度中心

↓

Capability

↓

执行
```

---

# 24. API设计

## 获取能力

```
GET /capabilities
```

---

## 能力匹配

```
POST /orchestration/match
```

---

## 创建执行计划

```
POST /orchestration/plan
```

---

## 执行计划

```
POST /orchestration/run
```

---

## 获取调度记录

```
GET /orchestration/history
```

---

# 25. 验收标准

智能调度中心完成后：

用户可以：

接入不同AI工具。

不用关注具体调用。

系统自动组合能力。

自动切换。

自动优化。

---

# 核心指标

## 成功率

任务完成质量。

---

## 成本效率

单位成果成本。

---

## 切换能力

失败恢复速度。

---

## Token效率

上下文利用率。

---

# 本章冻结内容

本章定义Curis智能调度中心。

核心：

Curis不是Agent管理工具。

也不是模型聚合工具。

而是：

统一管理所有AI能力，并根据目标自动组合执行的智能工作操作系统。

---

下一章：

# 24 Capability Marketplace与生态接入规范（Capability Ecosystem）