# 探索稿缺口 + 简洁方向审计（2026-08-04 · UI Designer）

Status: Deprecated

> 本文是早期探索稿审计，不是当前 UI 设计依据。当前设计以冻结 `Curis_Design_System.md`、Business Runtime v1.0 和最新 UI Evidence Alignment 为准。

> 目标（历史）：把"还缺什么"和"美观与操作的简单方向"两件事实地查清楚，对齐当时蓝图 §14（CEO UI Blueprint，v4.4）。
> 范围：仅 `curis-ui-prototype/` 探索稿，不碰冻结前端 `frontend/`。

## 0. 路程确认（你问的"这个路程没错吧"）
**没错，与既有裁决一致：**
1. 持续完善 `curis-ui-prototype/` 探索稿（设计系统 + 界面探索）
2. 完全 OK 后 → 产出 **Frozen 可交付 UI**
3. 前端接入（`frontend/` 按此实现）
4. 生成桌面应用（v1 本地自用）

依据：2026-08-03 评审已定性"探索稿是视觉探索稿，非 Frozen 可交付"，且产品主轴要求遵循 `Blueprint → Design → Code` 顺序。本审计就是第 1 步的"还缺什么 + 简洁方向"核查。

---

## 1. 还缺什么（蓝图 §14 逐面对齐）

| 蓝图 §14 要求 | 探索稿现状 | 缺口等级 |
|---|---|---|
| **AI Team & Capability**（§14.2/§14.8：调整角色、权限、**能力绑定**） | `ai-organization.html` 存在，但只有"能力绑定"**死链 `#`**；**无「+ 添加能力」入口**，无模型/Agent/Skill/Tool/MCP 添加表单 | **P0 缺** |
| **Employee Detail Drawer 能力绑定**（§14.8） | 抽屉结构多为占位，能力绑定无真实交互 | P1 缺 |
| **设置页**（侧栏底部"设置·帮助"） | 页脚"设置/帮助"改为打开 Assistant 抽屉，**无真实设置页**；而 v1 自用需在此配置外部模型 API key | P1 缺 |
| **Evidence Review 模式**（§14.10） | 无独立证据复核界面 | P1 缺 |
| **引导分步**（Welcome / Founding Brief / Company Design / First Business / Launch Check，§14.2–§14.7） | `founding-flow.html` 单页合并，分步屏幕级交互未逐屏落地 | P1 待核 |
| **Change Mode**（§14.10） | 无 | P2 可选 |
| CEO Desk / 经营 / 业务 / 工作空间 / Decision Room / Meeting | 均已有对应页，主区结构顺序与蓝图基本一致 ✓ | 已覆盖 |

**核心缺口一句话**：能力"添加 / 绑定 / 切换"这条闭环在探索稿里**完全缺失**（只有死链占位），这正是你质问的"员工空如何干活"。

---

## 2. 美观与操作的简单方向（实地核查，非印象）

蓝图 §14 视觉总判断：**Calm Executive Workspace**——中性纯色、单一主强调色、低对比边界、事实/观点/决议**不做成彩色容器**、仅系统/浅/深三主题、深色用深灰非纯黑、中文为主。

### 2.1 已达标（好消息）
- **主区叙事顺序**：`ceo-desk`（脉搏→事项→自动运行→时间线→AI 承担→日终）、`operating`（脉搏→关注/风险/阻塞→决策/异常/机会→约束）与蓝图 §14.5/§14.6 对得上，遵循"先状态、后证据、再动作"。
- **令牌系统**：全站已统一 `--ui-*`，无私有调色板；单一强调色（terra 绿）；暗色为深灰 `#1a1c1f` 非纯黑 ✓。
- **图标**：已统一 SVG 线性图标，无 Unicode 乱码 ✓。
- **渐变**：已从 8 页降至 **1 页残留**。

### 2.2 仍违反"简洁/一致"的硬伤（需收口）
| 违规 | 现状 | 影响 |
|---|---|---|
| **未本地化英文术语** | `ceo-day-demo.html` / `business.html` / `finance.html` 仍含 `ROI / KPI / Blueprint / Outcome / Evidence / Agent` | 破坏"中文为主、英文仅作内部对象名"红线 |
| **顶栏高度两派** | runtime×4 + meeting + shell-reference 用 `min-height:62px`；`workspace-studio.html:1266` 用 `height:52px` | 跨页视觉跳动，一致性崩坏 |
| **渐变残留** | `workspace-studio.html` 仍有 2 处渐变 | 与"不做彩色容器/花哨背景"冲突 |

> 这三类正好是 2026-08-03 评审的 P0-2/P0-3 项，当时**发现但未收口**——对应你说的"两点一直没完成"。本次把它们重新列成可勾清单。

---

## 3. 能力添加放哪里（简洁答案，不新建一级中心）

蓝图 §14 明令：**"不把 Agent / Task / Knowledge / Meeting 单独升为一级中心"**。所以**不要**做一个沉重的"能力中心"独立页。

正确落点（3 处内嵌，保持简洁）：
1. **公司（AI Team）页内嵌 "+ 添加能力"**：轻量内联操作，按蓝图 §14.2"调整角色、权限、能力绑定"。
2. **Employee Detail Drawer 的能力绑定区**：绑定已添加的能力到具体 AI 员工（§14.8）。
3. **Studio 装修台「能力与工具」面板**：按 Workspace 切换模型/Skill/Tool/MCP 组合。

添加表单（v1 自用 · 本地配置 · 不碰真实商业化）：
- 类型：`模型 / Agent / Skill / Tool / MCP`（10 类资产核心）
- 字段极简：名称 + 类型 + `effect_class`（只读/检索/写入/执行）+ 关联资源（连接器占位）
- 保存 → 进入资产库 → 绑定员工 → 运行现场可切换

红线保留项仍生效：**不建 Marketplace、不开放、不计费、不碰多租户**——v1 自用连接你**自己**的外部模型 key 在范围内（已按蓝图 §16 校正 §4）。

---

## 4. 建议的下一批精修（先收口一致性，再补核心闭环）
**A. 一致性收口（快赢，1 批）**
- 移除 `workspace-studio.html` 2 处渐变
- 本地化 `ceo-day-demo / business / finance` 的英文术语（ROI→投入产出、KPI→关键指标、Blueprint→搭建方案、Outcome→结果、Evidence→证据、Agent→AI 员工）
- 统一顶栏高度（全部归一到同一值，建议 56px）

**B. 核心闭环（P0，1 批）**
- 在 `ai-organization.html`（公司/AI Team）落地「+ 添加能力」轻量界面 + 资产库 + 绑定到员工 + 运行现场切换

**C. 待你拍板后再做**
- 真实设置页（外部模型 key 配置入口）
- Evidence Review 模式、引导分步逐屏化

---
**UI Designer**: 探索稿缺口与简洁方向审计已对齐蓝图 §14，待你确认 A/B 顺序后动手。
