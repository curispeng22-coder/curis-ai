# CURIS SYSTEM COMPETITIVE RESEARCH — MASTER PLAN

> Authority Class: RESEARCH（研究执行计划，不是 Product Authority）
> Status: **COMPLETE — SYSTEM COMPETITIVE RESEARCH COMPLETE（2026-09-12）**；终局综合见 `CURIS_SYSTEM_COMPETITIVE_RESEARCH_SYNTHESIS.md`
> Created: 2026-09-12
> Inputs: `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` (Frozen router)、`docs/01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md` (Frozen structure baseline)、`docs/00_Context/CURRENT_STATE.md`、`docs/03_Design/CURIS_VISUAL_STANDARD_V1.md`、已有竞品研究 (`docs/research/competitors/` 等)
> Output directory: `docs/research/system_competitive_research/`
> Boundary: 只研究、审计、报告。不改代码 / Figma / Runtime / Product Authority，不 commit / push。

## 1. Goal

系统级产品功能对标 + 字段级页面拆解 + 交互研究 + 视觉研究 + Curis UI 找茬 + 产品缺口发现。
最终输出能直接指导 Final UI Master 重启的 `CURIS DESKTOP PRODUCT & DESIGN DIRECTION`。

## 2. Method (纠偏后的主路线)

```
REAL PRODUCT → FUNCTION → OBJECT → FIELD → USER FLOW → INTERACTION
→ STATE → VISUAL → PIXEL → CURIS COMPARISON → GAP → RECOMMENDATION
```

- 主路线基于真实产品/真实截图/真实文档；代码与本地资源只用于验证 UI 看不出的事实、获取精确 token/metric、验证状态机制。
- Implementation Detail 不得直接决定 Curis Product Architecture。
- Current / Frozen Authority 优先；Candidate / Review / Research 不覆盖 Frozen；实现不反推产品。
- OBSERVATION → PATTERN → CURIS GAP 三步后才允许升级为 RECOMMENDATION CANDIDATE；少而精。

## 3. Competitors

新增深研：Workbuddy、Zcode（自研产品自我盘点）、Coze / 扣子。
继续覆盖已有产品：Claude (Desktop/Cowork)、Cursor、ChatGPT Desktop、Manus、Devin；
历史研究档案（Dify、CrewAI、MetaGPT、AutoAgents、ChatDev、GPTs、Make、Zapier、Taskade 等）作为 L2 背景证据保留，不重做。

## 4. Workstreams & Deliverables

| WS | 内容 | Deliverable | Owner | Status |
|----|------|-------------|-------|--------|
| WS0 | 本计划 | `CURIS_SYSTEM_COMPETITIVE_RESEARCH_MASTER_PLAN.md` | Main | DONE |
| WS1 | Curis 本地 UI / 实现证据盘点（当前页面清单、截图资产、Visual Standard token、结构基线摘要） | `CURIS_UI_EVIDENCE_CATALOG.md` | Explore agent | IN PROGRESS |
| WS2 | Workbuddy 全功能盘点（Expert / Expert Marketplace / Skill Marketplace / Model·Tool·MCP·Skill 组合） | `CURIS_RESEARCH_WORKBUDDY_FUNCTION_INVENTORY.md` | Research agent | IN PROGRESS |
| WS3 | Zcode 自我盘点（Project/Session/Agent/Mode/Skill/MCP/Permission/Settings/Desktop shell 全量） | `CURIS_RESEARCH_ZCODE_FUNCTION_INVENTORY.md` | Main | PENDING |
| WS4 | Coze / 扣子 Multi-Agent 深研 | `CURIS_RESEARCH_COZE_FUNCTION_INVENTORY.md` | Research agent | IN PROGRESS |
| WS5 | Claude Desktop / Cowork 盘点 | `CURIS_RESEARCH_CLAUDE_FUNCTION_INVENTORY.md` | Research agent | IN PROGRESS |
| WS6 | Cursor 盘点 | `CURIS_RESEARCH_CURSOR_FUNCTION_INVENTORY.md` | Research agent | IN PROGRESS |
| WS7 | ChatGPT Desktop / Manus / Devin 盘点 | `CURIS_RESEARCH_CHATGPT_FUNCTION_INVENTORY.md`、`CURIS_RESEARCH_MANUS_FUNCTION_INVENTORY.md`、`CURIS_RESEARCH_DEVIN_FUNCTION_INVENTORY.md` | Research agent | IN PROGRESS |
| WS8 | Curis 当前 UI 像素级找茬（P0 Directional / P1 Structural / P2 Polish） | `CURIS_CURRENT_UI_AUDIT.md` | Main（视觉模型直接看图） | PENDING |
| WS9 | 横向九矩阵：Composer / Conversation / Agent Progress / Multi-Agent / Talent & Capability / Result·Artifact / Desktop Shell / Settings / Visual System | `CURIS_COMPETITIVE_SETTINGS_MATRIX.md`、`CURIS_COMPETITIVE_CROSS_PRODUCT_MATRICES.md`（九矩阵分章） | Main | PENDING |
| WS10 | Capability Gap Matrix（COMPLETE / IMPLEMENTED BUT WEAK UX / PARTIAL / RUNTIME ONLY / UI ONLY / NOT IMPLEMENTED / NOT DESIGNED / UNKNOWN） | `CURIS_PRODUCT_CAPABILITY_GAP_MATRIX.md` | Main | PENDING |
| WS11 | UI Problem Register + Missing Capability Register + Pattern Library + Pattern Translation | `CURIS_UI_PROBLEM_REGISTER.md`、`CURIS_MISSING_CAPABILITY_REGISTER.md`、`CURIS_COMPETITIVE_PATTERN_LIBRARY.md` | Main | PENDING |
| WS12 | 最终方向：CURIS DESKTOP PRODUCT & DESIGN DIRECTION + System Synthesis | `CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md`、`CURIS_SYSTEM_COMPETITIVE_RESEARCH_SYNTHESIS.md` | Main | PENDING |

## 5. Execution Order

1. 并行：WS1 + WS2 + WS4–WS7（研究代理）。
2. Main 同时完成 WS3（Zcode 自盘点）与 WS8（基于 `curis-ui-prototype/p1-preview/*.png`、`docs/reviews/multi-surface-workspace-screenshots/*.png`、`docs/reviews/2026-08-08-product-audit/*.png` 及 Visual Standard / 结构基线做视觉审计）。
3. 代理返回后：WS9 → WS10 → WS11 → WS12。
4. 全部核心交付形成后，本文件与 SYNTHESIS 标记 `SYSTEM COMPETITIVE RESEARCH COMPLETE`。

## 6. Execution Status（2026-09-12 收口）

- ALL COMPLETE: WS0–WS12 + 追加交付（CEO 2026-09-12 指令）：`CURIS_PIXEL_LEVEL_COMPETITIVE_REFERENCE_MATRIX.md`（含本机实拍证据 E1–E9）与 `CURIS_PAGE_REFERENCE_BLUEPRINT.md`——两者为 STOP FOR CEO / CHATGPT REVIEW 状态，不自行开始 Final UI Master。
- 研究代理实际执行为串行（用户并发限制）；ChatGPT/Manus/Devin 由同一代理一次产出三份清单。
- 未尽事项（如实记录）：ChatGPT 国际版部分 Settings 分区、Workbuddy 企业版文档、各清单内标 UNKNOWN 项——均已在清单文末 UNKNOWN 汇总登记，不影响结论。

## 7. Stop / Guard

- 只批评 UI / Interaction，不推翻 Frozen Product Structure（七区、Company OS、Four-Pane、原装组织等）。
- Runtime 存在 ≠ Product 完成；Gap Matrix 必须按八档状态分级。
- 不将 Mock、静态页面、局部测试当作完整产品能力。
- 遇 Authority 冲突 → 记录冲突并以最新合法 Current/Frozen 为准，不自行重设计。
