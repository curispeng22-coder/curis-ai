# CONTENT GROWTH — CURRENT UI RECONCILIATION
### 现有 XHS 页面作为旧 Structural Candidate 的 KEEP / REPURPOSE / MERGE / DEMOTE / REMOVE / MISSING 判定

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，未修改任何页面）
Companion: `CONTENT_GROWTH_PRODUCT_MAPPING_MODEL.md` · `CONTENT_GROWTH_PRODUCT_EXPERIENCE_MODEL.md` · `CONTENT_GROWTH_USER_JOURNEY_MODEL.md`
前置：现有 XHS 页面清单来自 `Curis_XHS_Workspace_Instance_Spec_v1.md` 与 `ai-tech-workspace/pages/`（14 页）+ `curis-ui-prototype/workspace-runtime-xhs.html`（上一代）+ `docs/03_Design/Curis_XHS_Workspace_Visual_v3/v4.html`（视觉探索）。

---

## 0. 判定口径

- 本模型下：**Content Growth = Professional Workspace**；**XHS = Channel**（4 Module + Connector），不再是一个 6-Surface 的独立 Workspace。
- 因此现有 XHS 页面的「XHS 专属 6 Surface」框架是**旧 Structural Candidate**，须重判。
- 判定只回答「在新 Content Growth 模型下它们还有无意义 / 怎么重组」，**不修改页面、不画 UI**（STOP GATE）。
- 标记：`KEEP`(保留原义) / `REPURPOSE`(改归属/去 XHS 化后复用) / `MERGE`(并入他者) / `DEMOTE`(降为 Channel/子视图) / `REMOVE`(淘汰) / `MISSING`(新模型需要但现有缺失)。

---

## 1. 六个原始 XHS Surface 重组（直接回答本轮 §23）

| 原 XHS Surface | 新模型归属 | 判定 | 理由 |
|---|---|---|---|
| 经营概览 | → Content Growth **默认 Main（经营驾驶舱）** | **REPURPOSE** | 原 overview 是 XHS-scoped；应去 XHS 化、升为 Content Growth 共享驾驶舱（OUTPUT 2 §1） |
| 研究与洞察 | → Content Growth **「研究与洞察」Surface**（SHARED） | **REPURPOSE** | 研究是 SHARED，不绑 XHS；去渠道化 |
| 内容运营 | → Content Growth **「内容」Surface**（SHARED 创作 + CHANNEL 适配） | **REPURPOSE** | 创作 SHARED，适配 CHANNEL；不再叫「XHS 内容运营」 |
| 增长与评估 | → Content Growth **「增长与评估」Surface**（SHARED 真相） | **REPURPOSE** | 归因跨渠道可比，SHARED |
| 用户反馈 | → Content Growth **「反馈」Surface**（归一化后 SHARED 呈现） | **REPURPOSE** | 采集在 Channel，归一后 Signal 属 SHARED |
| 商业化 | → **XHS Channel Module**（蒲公英/聚光/千帆/星图/千川） | **DEMOTE** | 商业化是 CHANNEL 专属（各平台矩阵不可共用），降为 Channel Module，非 Workspace 默认 Surface |

> 即：原 6 Surface 中 5 个上浮为 Content Growth 共享 Surface/Main，1 个（商业化）降为 Channel Module。XHS 从「6 Surface 独立 Workspace」变为「Content Growth 下的一个 Channel」。

---

## 2. ai-tech-workspace/pages/ 逐页面判定（14 页）

| # | 文件 | 原 Surface | 判定 | 新归属 / 动作 |
|---|---|---|---|---|
| 1 | overview.html（经营总览） | 经营概览 | **REPURPOSE** | → Content Growth 默认 Main（去 XHS 化） |
| 2 | research.html（研究与洞察） | 研究与洞察 | **REPURPOSE** | → 「研究与洞察」Surface（SHARED） |
| 3 | content.html（内容运营） | 内容运营 | **REPURPOSE** | → 「内容」Surface |
| 4 | growth.html（增长与评估） | 增长与评估 | **REPURPOSE** | → 「增长与评估」Surface |
| 5 | feedback.html（反馈） | 用户反馈 | **REPURPOSE** | → 「反馈」Surface（归一化呈现） |
| 6 | commercial.html（商业化） | 商业化 | **DEMOTE** | → XHS Channel Module（商用化矩阵） |
| 7 | calendar.html（内容日历视图） | 内容运营子视图 | **KEEP** | 作为「内容」Surface 内视图；尊重 OPEN QUESTION Z1/Z7（默认非入口） |
| 8 | team.html（团队与责任） | other | **KEEP** | Employee/Responsibility 投影（SHARED，非 XHS） |
| 9 | handoff.html（员工工作与交接） | other | **KEEP** | Handoff 对象视图（复用 Company OS Handoff） |
| 10 | utility.html（工具区详情） | other | **KEEP** | Utility 右栏（OUTPUT 2 §5） |
| 11 | assistant.html（CEO 助理） | other | **KEEP** | CEO Assistant（三入口之对话） |
| 12 | collapsed.html（上下文收起） | other | **KEEP** | Context 收起态（OUTPUT 2 §8） |
| 13 | 1280.html（1280 视图） | other | **KEEP** | 响应式验收态 |
| 14 | rdcheck.html（XHS↔RD 结构对照） | other | **REMOVE** | RD 实例对照，与 Content Growth 业务无关 |

---

## 3. 上一代 / 视觉探索页面判定

| 文件 | 判定 | 理由 |
|---|---|---|
| `curis-ui-prototype/workspace-runtime-xhs.html`（小红书运营办公室） | **DEMOTE → REMOVE（框架）** | 上一代单页，把 XHS 建成「办公室」Workspace。新模型下 XHS=Channel，应重表达为 Channel runtime 视图；「办公室」隐喻已 deprecated `[CURIS-AUTH §3.2]`。建议：降级为 Channel 视图原型，移除 Office 框架 |
| `curis-ui-prototype.bak/workspace-runtime-xhs.html` | **REMOVE** | 备份副本 |
| `curis-ui-prototype/coverage-exploration-2026-08-17/09-xhs-workspace.html`（含副本） | **REMOVE** | coverage 探索产物，非交付 |
| `docs/03_Design/Curis_XHS_Workspace_Visual_v3.html` | **KEEP（研究用）** | 视觉探索，STOP GATE 不碰 Figma/视觉；仅标注为历史视觉参考 |
| `docs/03_Design/Curis_XHS_Workspace_Visual_v4.html` | **KEEP（研究用）** | 同上 |

---

## 4. 平台级导航 reconciliation（canonical-nav.js）

- 现状：`curis-ui-prototype/_system/canonical-nav.js` 将「小红书运营办公室」列为 **办公室（Office）** 分组下的 Workspace runtime 入口。
- 问题：①「Office」隐喻已 deprecated（Shared Authority §3.2，`ORG_AND_SERVICE_ORTHOGONAL`）；②新模型 XHS 是 Channel 而非 Workspace。
- 建议（**GAP / 待 CEO 裁决，不修改**）：将平台 nav 的「小红书运营办公室」改为 **Content Growth Workspace 下的 Channel 入口**（如 Workspace 内 Channel switch / Channel Detail），不再作为与「研发办公室」并列的 Office。
- 这是导航语义修正，非 UI 实施；纳入 OPEN QUESTION（Mapping §6-Q5）。

---

## 5. MISSING — 新模型需要但现有 XHS UI 缺失的

| 缺失项 | 说明 | 对应新模型 |
|---|---|---|
| **经营驾驶舱（默认 Main）** | 现有 overview 是 XHS-scoped 概览，非 Content Growth 共享驾驶舱（8 类型结果投影） | OUTPUT 2 §1 |
| **信息与机会 Surface** | 现有无独立 Signal/Opportunity 池视图（研究页混含） | Surface 1 |
| **Channel switch / 多渠道 awareness** | 现有无 XHS/Douyin 切换与 per-Account 真相视图 | OUTPUT 2 §6 |
| **Quick Path 对话入口** | 现有无「直接说一句话→自动选路径」的明确入口语义 | OUTPUT 2 §7 / Journey C |
| **CEO Projection 信息合同** | 现有卡片未结构化 11 字段（结论/价值/风险/未知/下一步/员工/Gate/证据） | OUTPUT 2 §3 |
| **Unit-Economics Auto-Selector** | 无 Quick/Structured/Deep 自动选型与升级提示 | OUTPUT 2 §7 |
| **内容域 Work/Result 子类型** | 无 Content Research/Brief/Publish/Evaluation Work 与 Result 枚举（Mapping G3） | Mapping §2.2 |
| **Signal Schema 结构约定** | 无 Signal/Opportunity 结构定义（Mapping G1） | Mapping §2.2 |

> MISSING 项均**不发明新 Runtime primitive**：以现有 Work/Result/Artifact/Surface/Channel/Connector + 结构约定（Extension/Contract 层）承载。

---

## 6. 重组后信息架构（建议，非实施）

```
Content Growth Workspace（Professional）
├ 默认 Main：经营驾驶舱（8 类型结果投影）
├ Surface：信息与机会 / 选题 / 研究与洞察 / 内容 / 增长与评估 / 反馈 / 渠道
├ 共享：Asset/Knowledge / Team&Responsibility / Handoff / Utility / CEO Assistant
└ Channel（XHS / Douyin / …）：Module(格式/发布/分析/反馈) + Connector
   （商业化矩阵 = XHS Channel Module 之一）
```

现有 XHS 14 页中 6 页 REPURPOSE 上浮、1 页 DEMOTE、1 页 KEEP 子视图、6 页 KEEP 基础设施、1 页 REMOVE；上一代 office 页 DEMOTE/REMOVE；视觉探索 KEEP 研究用。

---

*CONTENT GROWTH CURRENT UI RECONCILIATION — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
