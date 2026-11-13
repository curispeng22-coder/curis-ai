# Curis · Workspace Engineering Expert Handoff Protocol（专家交接协议）

**Status**: `Review`
**Methodology State**: `WORKSPACE ENGINEERING METHODOLOGY APPROVED CANDIDATE`
**类型**: 方法论 · 交接协议
**日期**: 2026-08-16
**上位**: `Curis_Workspace_Engineering_Methodology.md` · Lifecycle 步骤 4
**配套**: Gates（Doc 3）· Case Study（Doc 5）· RD Gap（Doc 6）

---

## 0. 阅读指引

本文件定义 **Domain Expert（领域专家）→ Product Expert（产品专家）** 的 Handoff 协议。

**核心问题它要解决**：领域专家做完几十份研究后，如果把全部 Research 直接甩给产品设计师，设计师会：
- 淹没在细节里，无法判断优先级；
- 自行重新解释业务，偏离真实经营方法；
- 把研究中的内部架构机械画给用户。

**协议的核心规则**：领域专家必须先**收敛成一份**下游可直接消费的 Handoff，再交接。Append-only 参考索引保留全部研究，但**主入口只有一份**。

---

## 1. 为什么需要 Handoff 协议（而不是「研究文档直接进设计」）

| 错误做法 | 后果 |
|---|---|
| 把 9 份 Research + Review 全丢给设计师 | 设计师重新解释业务，偏离权威；优先级丢失 |
| 设计师自行读全部原始研究 | 信息过载；无法区分 VERIFIED/UNKNOWN；易把研究数字当产品规则 |
| 无收敛 Handoff，设计直接进 UI | 违反 PRODUCT TRANSLATION GATE（Gate 2） |
| 研究文档与 Handoff 内容冲突 | 下游不知以谁为准 |

**正确链路**（Lifecycle 步骤 2→4）：
```
Domain Expert 研究（多份 Research）
   ↓ 收敛
Product Handoff（单份，唯一入口）
   ↓ 经本协议中转
Product Expert 翻译 → 用户语言产品
```

---

## 2. Handoff 的角色与责任

| 角色 | 责任 | 禁止 |
|---|---|---|
| **Domain Expert（作者）** | 写 Handoff；对经营方法的真实性与证据分类负责；保留研究索引 | 把未收敛的原始 Research 当 Handoff；在 Handoff 里设计 UI |
| **Product Expert（消费者）** | 消费 Handoff 翻译产品；对翻译保真度负责；发现歧义回到 Handoff 而非自行重研 | 自行重新解释业务；跳过 Handoff 直接读全部原始研究做设计 |
| **Methodology Expert** | 审计 Handoff 是否达标（见 §5 清单）；在 Gate 2 签署 | 代替任何一方写内容 |

---

## 3. Handoff 文档结构（单份收敛模板）

一份合格的 Product Handoff 必须包含以下 9 节（参考 Content Growth 的《Operating Strategy Product Handoff》）：

```markdown
---
title: <业务> Operating Strategy — Product Design Handoff
status: RESEARCH / EXPERT RECOMMENDATION
author: <Domain Expert 身份>
date: <YYYY-MM-DD>
purpose: 把 N 份领域研究收敛为「一份」可直接供产品专家消费的 Handoff
source_docs: Doc1…DocN（参考索引，非正文）
handoff_to: Curis 产品专家
---

# 0. 阅读指引
- 本文件是唯一入口；产品专家无需重读并自行解释全部研究
- 只定义「业务需要什么能力 / 什么边界」，不定义页面/字段/前端
- 所有平台具体数值一律 REFERENCE / NEEDS VERIFICATION

# 1. 核心经营模型
（八步飞轮 / 等效模型；每步标注 用户感知 / 员工执行 / 仅内部逻辑）

# 2. 策略归属矩阵
（五层 / 等效：经营方向 / Account / Employee Method / Platform Facts / Operating Rules；
 每层：归属谁 / 包含什么 / 用户如何感知）

# 3. 用户交互方式要求
（对话驱动 vs 直接编辑 修改同一份底层方法；禁止两套存储）

# 4. Semantic Model
（业务对象 / 关系 / 状态 / 责任 / 关键业务真相；标注哪些仅属 Package 局部语义）

# 5. Business Home 必须看见什么
（只提炼经营层必需信息，不堆 Dashboard）

# 6. Employee 需要展示什么
（用户能查看某员工「怎么工作」；Employee Method ≠ 复杂后台）

# 7. 平台事实四态
（VERIFIED / CONDITIONAL / UNKNOWN / UNAVAILABLE；禁止写死研究数字）

# 8. 边界与 Non-goals
（明确不做什么；不 Frozen；不进 UI；不改 Authority）

# 9. 证据分类与开放问题
（每条结论标 VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE；列出待核问题）
```

---

## 4. Handoff 质量契约（作者必须遵守）

1. **单一入口**：产品专家只需要读这一份就能工作；原始研究仅作参考索引。
2. **不重新解释**：Handoff 已收敛，设计师不重新解释业务。
3. **不设计 UI**：Handoff 只定义能力与边界，不定义页面、字段、前端实现。
4. **证据分类**：每条结论带 VERIFIED / CONDITIONAL / UNKNOWN / UNAVAILABLE；禁止把研究中的第三方数字（权重/频率/最佳时间/算法数值）变成产品规则。
5. **隐藏内部原语**：Office / Routing / Queue / Token 等不在 Handoff 用户面出现（翻译阶段再处理，但 Handoff 应标注哪些需隐藏）。
6. **边界明确**：Non-goals 显式列出；不 Frozen、不进 UI、不改 Authority 的纪律在文件头声明。
7. **可追溯**：source_docs 列出全部研究，便于设计师按需深读。
8. **局部语义优先**：普通 Workspace 的 Semantic Model 默认进入 Package Domain Schema；只有跨多个 Instance 复用、成为官方标准、影响 Company OS 或需要长期兼容保证时，才提出 Domain Authority / Frozen 升级建议。

---

## 5. Handoff 质量检查清单（Methodology Expert 在 Gate 2 前审）

| # | 检查 | 通过 |
|---|---|---|
| 1 | 是否**单份收敛**（非多份原始研究直投） | ✅/❌ |
| 2 | 是否定义「能力/边界」而非「页面/字段」 | ✅/❌ |
| 3 | 核心经营模型是否覆盖「长期运行并变更好」 | ✅/❌ |
| 4 | 策略归属是否分层、标注归属方 | ✅/❌ |
| 5 | 是否明确对象 / 关系 / 状态 / 责任 / 关键业务真相 | ✅/❌ |
| 6 | 是否区分 Package 局部语义与需要升格的 Domain Authority | ✅/❌ |
| 7 | 是否禁止两套交互存储（对话 vs 编辑） | ✅/❌ |
| 8 | 平台事实是否四态、无写死数字 | ✅/❌ |
| 9 | Non-goals 是否显式 | ✅/❌ |
| 10 | 证据是否逐条分类 + 开放问题列出 | ✅/❌ |
| 11 | 内部原语是否标注需隐藏 | ✅/❌ |
| 12 | source_docs 索引是否完整 | ✅/❌ |

> 任一 ❌ → Handoff 不达标 → 退回 Domain Expert 收敛 → 不得进入 PRODUCT TRANSLATION GATE。

---

## 6. 反向：Product Expert → Workspace Runtime / Core 的交接

Handoff 协议只覆盖「领域→产品」。产品之后必须先走 Package First：

```text
TARGET（NOT IMPLEMENTED）
Semantic Model + Workspace Design
→ Package Composition
→ Core Expressibility Check
→ EXPRESSIBLE：Validate / Install / Run
→ GAP：bounded Core / Capability Issue → 扩展 Core → 回到 Package

CURRENT
Instance Design → Gap Audit → bounded Issue → 修改源码 → Rebuild
```

- Package 必须包含局部语义、Surface、允许 Action、版本与来源，但不包含实例数据、凭据或预授权；
- Core 能表达时不得为了单一 Workspace 修改源码；
- Core 不能表达时，研发能力只执行 bounded Core / Capability Issue，不自行定义业务或产品形态；
- 当前源码交付路径必须明确标注，不能冒充 Target Package Runtime。

> 任何「设计稿直接进代码」「研究文档直接进设计」都违反本协议与 Gate 链。

---

## 7. 状态

```text
WORKSPACE ENGINEERING EXPERT HANDOFF PROTOCOL APPROVED CANDIDATE
```

*Curis Workspace Engineering Expert Handoff Protocol · APPROVED CANDIDATE / Review（非 Frozen）*
