# CURIS VISUAL EXPLORATION BRIEF

Status: Review
Authority Class: RESEARCH
Disposition: READY FOR FIGMA MAKE / CEO REVIEW AFTER EXPLORATION
Owner: Product / Design
Updated: 2026-08-23
Baseline: main @ c797db840bad285d7e9f1962d06eac61aa28508b

> 给下一轮 Figma Make 的 brief。只做视觉探索，不修改当前 Figma Structural Candidate、Product Authority、Frozen Design System 或代码。

## 1. Goal

验证 `Calm Surface / Strong Focus / Rich Work` 是否能在两个 benchmark screen 上成立：

1. `Research`
2. `Employee Conversation`

这不是重新设计产品结构。结构、内容、交互模型、Employee 三入口和 Context/Main/Utility 职责保持一致；只有视觉系统开放。

## 2. Shared content and structure

所有方向使用完全相同的：

- 页面结构和 pane 职责。
- 中文文案、Employee、Work、Result、Evidence、引用和 Composer 内容。
- 交互入口：Direct Conversation、Current Work、Employee Profile。
- 视口：1440×900、1280×800、1024×800；可附 390 宽度，但不把移动版当本轮主验收。

## 3. Three directions

### Direction A — Quiet / Neutral baseline

中性表面、低对比边界、Typography 与 whitespace 为主、极少 accent。验证“安静但不空”。

### Direction B — Curis Strong Focus

在 A 的中性表面上强化 L1：更清楚的标题/对象层级、明显但受控的 Deep Green focus、单一 Primary CTA、Raised surface 稀缺。验证“普通用户是否第一眼抓住重点”。

### Direction C — Curis Focus + restrained Professional Accent

在 B 上加入受限的 domain annotation，仅用于 Research 内容类型、引用/可视化或专业对象；不能改变 Curis shell、Composer、Employee identity 或基础 semantic roles。验证“专业感是否增强而不变成 domain skin”。

## 4. Required visual system

- L1/L2/L3/L4 明确可见，但不显示技术术语。
- 每个视口 1 L1、≤2 accent areas、≤1 Primary CTA。
- Content width 使用 Reading/Work mode，不铺满。
- Conversation 是阅读流，不是 bubble wall。
- Composer 以输入与发送为主，低频控制渐进披露。
- Employee 统一身份，三入口语义不同。
- Work/Result/Evidence/Decision 不使用三种大彩色 Card 区分。
- Card 遵循 typography → spacing → divider → subtle surface → card 的顺序。
- Deep Green 作为候选品牌/焦点，不作大面积背景。
- 不使用 gradient SaaS、彩色导航、AI sparkle、Agent online wall。

## 5. Figma Make output

每个方向至少输出：Research desktop、Employee Conversation desktop、1280/1024 responsive states、light mode；Dark mode 只做方向性映射，不要求完整设计。标注每个主要对象的 L1–L4、surface/elevation、content width、Primary CTA 和 domain accent 使用点。

## 6. CEO comparison rubric

每个方向 1–5 分，附一句证据：

| Dimension | Question |
|---|---|
| First focus | 2 秒内能否说出当前重点？ |
| Calmness | 长时间阅读是否低噪音？ |
| Rich Work | 真实业务信息是否保留且可扫描？ |
| Brand | 不看 Logo 是否仍有 Curis 记忆点？ |
| Employee | 是否是责任主体，而非监控对象？ |
| Conversation | 长回答、引用、Composer 是否舒服？ |
| Card discipline | 是否避免 Card/Dashboard Wall？ |
| Cross-domain | 规则能否迁移到 XHS/RD/CEO Desk/Business/Commerce？ |
| Accessibility | focus、status、contrast 是否不依赖单一颜色？ |

## 7. Stop gate

探索结束后只返回：三方向截图/链接、评分、保留规则、否决规则、未解决问题。停止等待 CEO 选择；不得自动更新 Shared Visual Design System、Frozen 文档或 Frontend。

