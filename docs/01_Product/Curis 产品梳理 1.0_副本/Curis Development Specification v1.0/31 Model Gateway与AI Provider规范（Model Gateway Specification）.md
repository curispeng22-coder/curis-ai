# Curis Development Specification

# 31 Model Gateway与AI Provider规范（Model Gateway Specification）

版本：v1.0-draft

---

# 1. 系统定位

Model Gateway 是 Curis 统一管理模型能力的基础服务。

负责：

- 接入不同模型服务；
- 统一调用接口；
- 管理模型配置；
- 统计模型使用；
- 支持模型切换；
- 支持智能调度。

---

# 2. 核心理念

模型不是产品。

模型属于：

Capability（能力）。

---

Curis 不绑定：

- OpenAI；
- Anthropic；
- Google；
- DeepSeek；
- New API；
- OpenRouter；
- 本地模型。

---

统一抽象：

```
Model Provider

↓

Model Gateway

↓

Capability System

↓

Workspace
```

---

# 3. Model Gateway职责

## 3.1 模型统一接入

不同模型服务统一转换。

例如：

```
GPT

Claude

Gemini

本地模型

第三方Gateway
```

统一进入：

Model Gateway。

---

## 3.2 模型代理

负责：

- 请求转发；
- 参数转换；
- 错误处理；
- 重试机制。

---

## 3.3 模型管理

管理：

- 模型名称；
- Provider；
- API地址；
- Key；
- 参数；
- 状态。

---

## 3.4 使用统计

记录：

- 调用次数；
- Token消耗；
- 成本；
- 响应时间；
- 成功率。

---

# 4. Provider模型

Provider表示：

模型来源。

---

例如：

```
Provider

├── OpenAI

├── Anthropic

├── Google

├── New API

├── OpenRouter

├── Ollama

└── Custom
```

---

# 5. Model数据结构

```
Model

├── id

├── name

├── provider_id

├── model_id

├── endpoint

├── capability_tags

├── context_length

├── cost_rule

├── status

└── created_at
```

---

# 6. 模型能力标签

每个模型需要描述：

---

## 推理能力

例如：

复杂分析。

方案设计。

---

## 编程能力

例如：

代码生成。

代码修改。

---

## 长上下文能力

例如：

大型文档分析。

---

## 速度

例如：

实时响应。

---

## 成本

例如：

低成本任务。

---

这些标签用于：

智能调度。

---

# 7. 模型接入方式

支持：

---

## API接入

例如：

OpenAI API。

Anthropic API。

---

## Gateway接入

例如：

New API。

OpenRouter。

---

## 本地模型

例如：

Ollama。

LM Studio。

---

## 自定义Provider

支持：

用户自己的接口。

---

# 8. New API适配

New API作为：

Provider Adapter。

---

不是：

Curis核心系统。

---

结构：

```
Curis

↓

Model Gateway

↓

New API Adapter

↓

模型服务
```

---

用户无需登录New API。

---

Curis管理：

- 模型；
- Key；
- 调用；
- 统计。

---

# 9. 模型配置页面

入口：

能力中心。

---

展示：

```
模型能力

├── 已连接

├── 未配置

├── 异常

└── 推荐
```

---

展示：

模型名称。

Provider。

用途。

成本。

状态。

---

# 10. 模型测试

支持：

## 连接测试

检查：

是否可调用。

---

## 性能测试

检查：

响应时间。

---

## 基础质量测试

检查：

输出是否正常。

---

# 11. 模型调用策略

支持：

## 固定模型

用户指定。

---

例如：

研发项目固定：

Claude。

---

## 自动选择

智能调度中心选择。

---

例如：

简单任务：

低成本模型。

---

复杂任务：

高级模型。

---

# 12. 模型Fallback机制

模型异常：

自动切换。

---

例如：

```
Claude失败

↓

GPT

↓

本地模型
```

---

保持：

- 当前任务；
- Context；
- Memory。

---

# 13. 模型成本控制

统计：

```
公司

↓

部门

↓

项目

↓

员工

↓

任务

↓

模型
```

---

支持：

预算限制。

---

例如：

研发项目：

每日Token限制。

---

# 14. 与Capability Profile关系

用户不直接选择模型。

---

选择：

工作模式。

---

例如：

软件开发模式：

内部：

```
开发Agent

+

Claude Code

+

Claude模型

+

Git Tool
```

---

# 15. 与智能调度中心关系

智能调度中心根据：

- 任务类型；
- 模型能力；
- 成本；
- 历史效果；

选择模型。

---

例如：

任务：

架构设计。

选择：

高推理模型。

---

任务：

代码格式调整。

选择：

快速模型。

---

# 16. 与Agent关系

Agent可以绑定多个模型。

---

例如：

研发Agent：

```
主要模型：

Claude


备用模型：

GPT
```

---

Agent执行时：

由调度中心决定。

---

# 17. 用户侧快速切换

用户可以：

在当前工作环境快速切换。

---

例如：

```
研发负责人

当前模式：

软件开发模式

↓

切换

高级代码模式

研究模式

快速修改模式
```

---

底层自动调整：

- Agent；
- Model；
- Skill；
- Tool。

---

# 18. API设计

## 获取Provider

```
GET /providers
```

---

## 添加Provider

```
POST /providers
```

---

## 获取模型

```
GET /models
```

---

## 添加模型

```
POST /models
```

---

## 测试模型

```
POST /models/{id}/test
```

---

## 调用模型

```
POST /models/{id}/completion
```

---

## 查询使用情况

```
GET /models/{id}/usage
```

---

# 19. 验收标准

Model Gateway完成后：

用户可以：

接入多个模型。

统一管理。

统一调用。

统计成本。

快速切换。

---

检查：

## 扩展性

新增模型无需修改业务系统。

---

## 兼容性

支持未来Provider。

---

## 调度能力

可以被智能调度中心调用。

---

# 本章冻结内容

Model Gateway定义：

Curis如何管理模型来源。

核心：

模型只是能力资源。

Curis负责：

统一接入。

统一管理。

智能调用。

---

下一章：

# 32 AI员工管理系统详细规范（AI Employee System）