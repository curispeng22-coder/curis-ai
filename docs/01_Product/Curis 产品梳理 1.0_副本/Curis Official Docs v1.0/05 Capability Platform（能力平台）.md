# Curis Official Docs v1.0

# 05 Capability Platform（能力平台）

版本：v1.0

---

# 1. 平台定位

Capability Platform 是 Curis 的AI能力基础设施。

负责：

统一管理：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow；
- Connector。

---

核心目标：

> 不让用户管理零散AI工具，而是将所有AI能力组织成可被AI员工调用的能力体系。

---

# 2. 核心理念

Curis不生产所有AI能力。

Curis负责：

```
发现能力

↓

管理能力

↓

组合能力

↓

调用能力

↓

优化能力
```

---

模型、Agent、Skill、Tool都是：

Capability。

---

# 3. Capability整体结构

```
Capability Platform

├── Model

├── Agent

├── Skill

├── Tool

├── Workflow

└── Connector
```

---

# 4. Capability与AI员工关系

关系：

```
AI Employee

↓

Capability Profile

↓

Capability

↓

Execution
```

---

例如：

研发负责人：

```
Capability Profile:

Software Development


包含：

Coding Agent

Claude Code

Git Tool

Testing Workflow
```

---

# 5. Model（模型能力）

## 定义

Model提供基础AI推理能力。

---

例如：

- GPT；
- Claude；
- Gemini；
- DeepSeek；
- 本地模型。

---

# 6. Model Gateway

## 定义

Model Gateway负责统一管理模型调用。

---

结构：

```
Capability

↓

Model Gateway

↓

Provider

↓

Model
```

---

负责：

- 模型接入；
- API管理；
- 调用转发；
- Token统计；
- 成本统计。

---

# 7. Provider（模型来源）

Provider代表：

模型服务来源。

---

例如：

```
OpenAI

Anthropic

Google

New API

OpenRouter

Local Model
```

---

Curis不绑定单一Provider。

---

# 8. Agent（执行能力）

## 定义

Agent负责执行具体任务。

---

例如：

- Coding Agent；
- Research Agent；
- Writing Agent；
- Analysis Agent。

---

关系：

```
Employee

↓

Agent

↓

Execution
```

---

# 9. Skill（专业技能）

## 定义

Skill用于增强AI员工专业能力。

---

例如：

内容领域：

```
热点分析Skill

标题优化Skill

SEO Skill

文案Skill
```

---

研发领域：

```
代码分析Skill

测试Skill

架构分析Skill
```

---

# 10. Tool（工具能力）

## 定义

Tool负责操作外部资源。

---

例如：

```
Git

文件系统

浏览器

数据库

终端
```

---

Tool解决：

“AI可以做什么操作”。

---

# 11. Workflow（流程能力）

## 定义

Workflow定义业务执行流程。

---

例如：

内容生产：

```
热点分析

↓

选题生成

↓

文案生成

↓

审核
```

---

研发流程：

```
需求分析

↓

代码开发

↓

测试

↓

发布
```

---

# 12. Connector（连接能力）

## 定义

Connector负责连接外部系统。

---

例如：

```
GitHub

Obsidian

云存储

内容平台

企业系统
```

---

# 13. Capability Registry（能力注册中心）

## 定义

所有能力统一登记管理。

---

保存：

```
Capability

├── Name

├── Type

├── Provider

├── Input

├── Output

├── Permission

├── Cost

└── Status
```

---

# 14. Capability Profile（能力组合）

## 定义

将多个Capability组合成工作模式。

---

例如：

## 软件开发模式

```
Coding Agent

+

Claude Code

+

Git

+

Testing Workflow
```

---

## 内容创作模式

```
GPT

+

热点分析Skill

+

文案Skill

+

图片生成
```

---

# 15. Capability Switcher（能力切换）

用户不直接操作所有Capability。

---

用户看到：

```
工作模式

↓

研发模式

内容模式

研究模式
```

---

系统内部：

切换：

- Agent；
- Model；
- Skill；
- Tool；
- Workflow。

---

# 16. MVP阶段能力体系

MVP实现：

```
Capability Registry

+

Capability Profile

+

Manual Configuration
```

---

用户：

人工配置员工能力。

---

例如：

创建：

内容负责人。

绑定：

```
GPT

+

热点分析Skill

+

文案Skill
```

---

# 17. MVP不实现

暂不实现：

---

## 智能能力推荐

未来：

系统根据任务自动推荐。

---

## 自动模型选择

未来：

根据成本和效果选择模型。

---

## Capability Marketplace

未来：

第三方能力生态。

---

# 18. 已有Skill迁移规则

之前Admin团队创建的Skill：

保留。

---

迁移：

```
Existing Skill

↓

Capability Registry

↓

Employee Capability Profile
```

---

不作为：

独立产品。

---

# 19. Capability安全

所有能力必须定义：

```
Permission

↓

Authorization

↓

Execution

↓

Audit
```

---

例如：

Git能力：

允许：

代码读取。

---

禁止：

未经确认删除仓库。

---

# 20. Capability成本管理

记录：

```
Workspace

↓

Project

↓

Employee

↓

Capability

↓

Model
```

---

用于：

未来智能优化。

---

# 21. Capability未来演进

阶段：

```
MVP

人工配置能力


↓

智能阶段

自动匹配能力


↓

生态阶段

第三方能力市场
```

---

# 22. 核心价值

Capability Platform解决：

传统AI：

```
用户寻找工具
```

---

Curis：

```
AI员工调用能力完成工作
```

---

# 本文档状态

状态：

Active

---

用途：

定义Curis能力体系。

所有模型、Agent、Skill、Tool、Workflow接入必须遵循本规范。

---

下一篇：

# 06 Knowledge & Memory System（知识与记忆系统）