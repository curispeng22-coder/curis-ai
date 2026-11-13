# Curis Development Specification

# 26 能力配置档案系统（Capability Profile System）

版本：v1.0-draft

---

# 1. 系统定位

Capability Profile 是 Curis 对复杂AI能力组合的抽象。

解决：

用户不需要理解：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow。

而是选择：

适合当前任务的工作模式。

---

# 2. 核心理念

单个能力：

解决一个动作。

能力组合：

解决一个工作场景。

---

例如：

不是：

选择Claude。

而是：

选择：

“高级代码开发模式”。

---

内部组合：

```
高级代码开发模式

├── 开发Agent

├── Claude Code

├── Git Tool

├── 测试Workflow

├── 代码审查Skill

└── 项目Memory
```

---

# 3. Capability Profile组成

结构：

```
Capability Profile

├── 名称

├── 适用场景

├── 默认Agent

├── 默认Model

├── Skills

├── Tools

├── Workflow

├── Memory策略

└── 成本策略
```

---

# 4. 默认工作模式

Curis预置：

---

## 通用助手模式

用途：

日常问答。

资料整理。

简单任务。

---

能力：

- 通用Model；
- 搜索Tool；
- 知识检索。

---

## 深度研究模式

用途：

分析。

调研。

方案设计。

---

能力：

- 高级Model；
- Research Agent；
- 搜索Tool；
- 数据分析Skill。

---

## 软件开发模式

用途：

研发任务。

---

能力：

```
研发负责人

↓

开发Agent

↓

Codex / Claude Code

↓

Git Tool

↓

测试Workflow
```

---

## 内容创作模式

用途：

内容增长。

---

能力：

```
内容负责人

↓

热点分析Agent

↓

文案Skill

↓

图片Tool

↓

数据分析Skill
```

---

## 数据分析模式

用途：

经营分析。

---

能力：

- 数据Agent；
- Python Tool；
- 分析Skill。

---

# 5. 员工默认Profile

每个AI员工可以绑定：

默认工作模式。

---

例如：

研发负责人：

默认：

软件开发模式。

---

内容负责人：

默认：

内容创作模式。

---

# 6. 任务临时切换

用户可以：

临时修改。

---

例如：

研发任务：

当前：

软件开发模式。

---

用户：

“先让它做技术调研。”

切换：

深度研究模式。

---

任务完成：

恢复默认。

---

# 7. UI设计

## 工作区域入口

位置：

AI输入框附近。

---

展示：

当前模式。

---

例如：

```
🛠 软件开发模式  ▼
```

---

点击：

打开选择器。

---

# 8. 能力选择器结构

```
当前模式

软件开发模式


推荐模式

高级代码开发


其他模式

深度研究

快速修改

代码审查


自定义
```

---

# 9. 高级展开

高级用户：

可以查看：

实际能力。

---

例如：

```
软件开发模式


Agent:

Claude Code


Model:

Claude


Tool:

Git


Workflow:

测试流程
```

---

普通用户：

隐藏。

---

# 10. 自动模式

默认：

Auto。

---

智能调度中心：

根据任务自动选择。

---

例如：

用户：

“修复这个Bug。”

系统：

自动：

进入：

软件开发模式。

---

# 11. 手动模式

高级用户：

固定。

---

例如：

当前项目：

强制使用：

Codex。

---

原因：

用户熟悉。

---

# 12. 模式切换记录

记录：

```
任务

↓

原模式

↓

新模式

↓

原因

↓

结果
```

---

用于：

优化调度。

---

# 13. 与智能调度中心关系

关系：

```
Capability Profile

↓

Orchestrator

↓

具体Capability

↓

执行
```

---

Profile：

告诉系统：

应该怎么工作。

---

Orchestrator：

决定：

具体调用谁。

---

# 14. 与Memory关系

不同Profile：

使用不同Memory策略。

---

例如：

研发模式：

优先加载：

技术Memory。

---

内容模式：

优先加载：

用户画像。

---

# 15. 与项目关系

项目可以设置：

默认Profile。

---

例如：

研发项目：

默认：

软件开发模式。

---

内容项目：

默认：

内容创作模式。

---

# 16. API设计

## 获取Profile

```
GET /capability-profiles
```

---

## 创建Profile

```
POST /capability-profiles
```

---

## 应用Profile

```
POST /tasks/{id}/profile
```

---

# 17. 验收标准

完成后：

用户可以：

像切换模型一样。

快速切换工作模式。

---

同时：

系统内部自动管理：

Agent。

Model。

Skill。

Tool。

Workflow。

---

# 本章冻结内容

Curis用户侧不直接管理复杂能力。

通过：

Capability Profile

降低使用复杂度。

后台保持：

能力可组合。

前台保持：

简单快速。

---

下一章：

# 27 Connector与外部系统连接规范（Connector Integration）