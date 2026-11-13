# ADR-0042: Calm Executive Visual Language

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-08-01

Module: Design

## Decision

Curis 的全局视觉语言采用 **Calm Executive Workspace（安静的 CEO 工作空间）**。

```text
内容与经营语义优先
→ 中性纯色表面
→ 单一主强调色
→ 低对比边界
→ 对话流与上下文抽屉
→ 结构化结果在需要时出现
```

Curis 不采用多彩 Dashboard、控制台式卡片堆叠或渐变霓虹视觉。会议、CEO Assistant、
Workspace 和经营页面都遵守同一视觉语法；Workspace 可以改变布局，但不能绕过中性表面、
克制颜色、内容优先和可访问性规则。

## Reason

- Curis 服务的是需要阅读、判断和决策的 CEO，而不是需要操作大量控件的后台管理员。
- 当前页面把事实、观点、决议、承诺和状态分别做成彩色容器，导致视觉噪音和操作台感。
- Linear、Codex、ChatGPT 和 Apple 的共同优点是减少装饰，让层级、留白、文本和上下文承担主要表达。
- 会议和 Assistant 需要有对话温度，但不能牺牲证据、决议和执行关联的经营结构。

## Consequences

- 设计规范新增全局视觉立场、目标色彩、排版和组件禁用项。
- 会议工作台改为带语义标签的讨论流；结构化结果进入会议产出区和上下文抽屉。
- 新页面评审必须回答：主叙事是什么、唯一主要行动是什么、哪些颜色是 CEO 必须关注的。
- 主题只提供系统、浅色、深色三种模式；深色使用深灰而非纯黑，主题切换不改变页面结构与经营语义。

## Supersedes

- 以多色卡片、强边框和多面板并列为默认表达的页面视觉方向。
- 将运营页面默认设计成 Dashboard / 控制台的视觉倾向。
