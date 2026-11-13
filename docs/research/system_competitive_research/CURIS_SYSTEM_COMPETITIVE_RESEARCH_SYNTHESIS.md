# CURIS SYSTEM COMPETITIVE RESEARCH — FINAL SYNTHESIS

> Authority Class: RESEARCH / EVIDENCE（研究综合；不构成 Product Authority，不修改任何 Frozen 文档）
> Status: **SYSTEM COMPETITIVE RESEARCH COMPLETE**（2026-09-12）
> 研究范围：9 产品功能盘点 + 字段级页面拆解 + 交互/状态研究 + 视觉审计 + Curis UI 找茬 + 产品缺口发现。
> 方法纠偏：主路线 = 真实产品 → 功能 → 对象 → 字段 → 流程 → 交互 → 状态 → 视觉 → 像素 → Curis 对照 → 缺口 → 建议；本地代码/资源仅作 L2 验证。

---

## 1. 交付物总目录（全部位于 `docs/research/system_competitive_research/`）

| # | 交付物 | 文件 | 状态 |
|---|---|---|---|
| 1 | 研究主计划 | `CURIS_SYSTEM_COMPETITIVE_RESEARCH_MASTER_PLAN.md` | COMPLETE |
| 2 | Curis 本地 UI/实现证据盘点 | `CURIS_UI_EVIDENCE_CATALOG.md` | COMPLETE |
| 3 | 功能清单 ×9 | `CURIS_RESEARCH_{WORKBUDDY,ZCODE,COZE,CLAUDE,CURSOR,CHATGPT,MANUS,DEVIN}_FUNCTION_INVENTORY.md` + `CURIS_RESEARCH_WORKBUDDY_LOCAL_EVIDENCE.md` | COMPLETE（字段级，含来源 URL，UNKNOWN 显式标注） |
| 4 | Curis 当前 UI 找茬审计（A/B/C/D 四代） | `CURIS_CURRENT_UI_AUDIT.md` | COMPLETE |
| 5 | Product Capability Gap Matrix（八档状态） | `CURIS_PRODUCT_CAPABILITY_GAP_MATRIX.md` | COMPLETE |
| 6 | Settings Matrix（字段级） | `CURIS_COMPETITIVE_SETTINGS_MATRIX.md` | COMPLETE（九产品列齐） |
| 7 | 横向九矩阵（Composer/Conversation/Progress/Multi-Agent/Talent/Result/Desktop/Settings→独立文件/Visual） | `CURIS_COMPETITIVE_CROSS_PRODUCT_MATRICES.md` | COMPLETE（九产品列齐） |
| 8 | UI Problem Register（P0/P1/P2） | `CURIS_UI_PROBLEM_REGISTER.md` | COMPLETE |
| 9 | Missing Capability Register（M-01~M-20 + 保护清单 + 不做清单） | `CURIS_MISSING_CAPABILITY_REGISTER.md` | COMPLETE |
| 10 | Competitive Pattern Library + Translation Matrix（⭐升级制） | `CURIS_COMPETITIVE_PATTERN_LIBRARY.md` | COMPLETE（v3，40+ 模式，⭐21） |
| 11 | **CURIS DESKTOP PRODUCT & DESIGN DIRECTION**（重启 Final UI Master 的正式研究输入） | `CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md` | COMPLETE |
| 12 | **像素级复刻参照矩阵**（Surface×Reference 主矩阵 + L0–L4 分级 + E1–E9 本机实拍证据 + DO NOT REINVENT / CURIS ORIGINAL 双登记） | `CURIS_PIXEL_LEVEL_COMPETITIVE_REFERENCE_MATRIX.md` + `evidence/pixel-reference/`（9 张竞品窗口实拍：WorkBuddy×3 / Claude / ChatGPT / Cursor / 扣子×2 / Linear） | COMPLETE — STOP FOR CEO REVIEW |
| 13 | **页面拼装蓝图**（P1–P14 逐页：语义 L0 + 骨架 Ref + 组件 Ref + 统一化规则） | `CURIS_PAGE_REFERENCE_BLUEPRINT.md` | COMPLETE — STOP FOR CEO REVIEW |

历史竞品研究（Dify/CrewAI/MetaGPT/AutoAgents/ChatDev/GPTs/Make/Zapier/Taskade 等，`docs/research/competitors/`）保留为 L2 背景证据，本轮未重做。

## 2. 五个核心问题的直接回答

### Q1 Curis 还缺什么功能？

缺的不是"宏大能力"，是 **2026 年 AI 桌面产品的标配层**：
- 全局搜索/⌘K、通知中心、成熟 Composer、Work 进度可视化、Result 消费面（预览/版本/下载）、完整 Settings、Usage/成本面、权限政策面、Automation、Memory 面、桌面壳能力（全局快捷键/菜单栏）、Dark/1024。
- 全部带竞品坐标登记于 `CURIS_MISSING_CAPABILITY_REGISTER.md`（M-01~M-20），并附"保护清单"（9 项独有资产不可丢失）与"不做清单"（多租户/Marketplace 生态等裁决性缺席）。

### Q2 已有功能哪里没做完整？

模式高度一致：**Runtime 强、Surface 弱**（Gap Matrix：COMPLETE=0，IMPLEMENTED BUT WEAK UX=8，RUNTIME ONLY=4）。
- 七个一级区全部已实现但 UX 弱化：CEO 工作台（注意力无优先级）、业务空间（后台目录）、组织中心（Search/Filter 未接）、人才与能力（无市场语言/无用户语言）、经营洞察（数据接入缺）、资料库（检索/引用 UX 缺）、会议（multi-cycle 证据 pending）。
- 四条 Runtime 链没有脸：Usage Ledger、Scope/授权、Handoff、Meeting advancement cycle。

### Q3 每个页面应该显示什么、用户怎么操作？

- 逐页结构/字段/动作/状态要求已在 `CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md` §2（全局壳/CEO 工作台/业务空间/组织中心/**Employee Detail 新核心页**/Work 进度组件/Settings 字段级清单/会议·资料库·洞察消费已验收 Figma 基线）。
- 字段级竞品参照在各 FUNCTION_INVENTORY（如 Expert 卡、Agent 配置页、Playbook 五段、Knowledge Trigger Description）。
- 每页六态规范：Normal / Empty（首次）/ Empty（用尽）/ Loading / Error / Needs-CEO。

### Q4 视觉为什么不好？

三层原因（审计 §0/§10/§14）：
1. **身份碎片**：`#32f08c`（前端 frozen token）/`#806BE5`（V1 Frozen 未消费）/黑绿（A 代）并存——产品没有可识别的脸。
2. **语汇错误**：网页后台语汇（0 值统计卡/tab 计数/表单卡/面包屑）代替桌面对象语汇；空态是"空报表"不是"公司等你启动"。
3. **纪律缺失**：状态词典漂移、卡片泛滥（A 代）、标签堆叠无对象感（D 代）、开发者注释与内部术语（SimulationRun/--ui-*/aware）直接暴露。

### Q5 应该如何重新建立 Final UI Master？

不是重画，是**收口**（Direction §4 路线）：
- 基础已存在：七区结构（Structure Baseline Frozen）+ 四 Pane 壳（D 代合规实现）+ 三套已验收 Figma 基线（会议 214/资料库 187/洞察 172）+ V1 token 表 + D 代"安静高密度"纪律。
- R1 Token 统一（V1 迁移收口，accent 单一化）→ R2 员工脸面四件套（Employee Detail/Work 进度/Result 消费/结构化 Composer）→ R3 CEO 工作台与门户重做 + 三基线视觉翻新 → R4 Settings 全量/Usage/权限/人才市场语言 → R5 桌面壳 + Dark/1024/无障碍。
- 每轮 Light/Dark × 1440/1280/1024 出图；全部消费 token，禁止页面私有值。

## 3. 关键竞品事实（影响判断的 8 条）

1. **扣子已正面转向**："AI 团队协作平台/扣子空间"叙事与 Curis Company OS 直接重叠——窗口期存在，但 Curis 组织语义（Leader/Assignment/会议制度/Result→Evidence）仍无对等物。
2. **ChatGPT 弃 Agent mode 转 Work**（Chat/Work/Codex 三区）+ 个人停建 GPT：行业从"开放市场"收敛到"组织化工作台"，验证 Curis 方向。
3. **Workbuddy（腾讯 CodeBuddy 团队）是人才与能力的最直接对标**：Skill→专家→专家团三层能力模型、召唤制、成果反查导购、授权边界（票据双轨）、四级审批梯度。
4. **权限已进入四层体系时代**（档位 × 自然语言白名单 × sandbox × 硬红线）：Claude/Cursor/Workbuddy 三家共同验证；Curis 只有 Runtime scope。
5. **自动化全部标配且带身份**：ChatGPT 事件触发任务、Devin Automations 8×4 + Scheduled Sessions Run-as、Manus Scheduled Tasks；自动化归属身份（Run-as）与 Curis Usage Ledger 天然同构。
6. **记忆全部透明可编辑**，且新增安全设计（Cursor 注入警示、ChatGPT sources 可解释、Claude 敏感 opt-in）。
7. **Manus 首次触及会议**（Meeting Minutes 纪要+说话人识别）——但仍是工具纪要，非 Curis 制度化会议；保护项不受威胁。
8. **Devin Knowledge Trigger Description / Playbook 五段结构**是"组织内部能力资产化"的最佳字段设计，比公开市场更同构于 Curis 员工模型。

## 4. Authority 冲突与处置记录（研究期间发现，均未自行裁决）

| 冲突 | 现状 | 处置建议（待 CEO/Product Gate） |
|---|---|---|
| Accent：V1 `#806BE5`（Frozen/CEO Selected D）vs 前端+D 代 `#32f08c`（旧 Spec，Pointer 已注明被取代） | Pointer 明确 `#32f08c` accent 条款已被 V1 取代；实现未迁移属债务 | 按 V1 迁移收口；若 CEO 想重选 accent，走 V1 修订，不在页面层各自为政 |
| A 代原型（办公室词汇）与 08-24 Office 退出裁决冲突 | A 代资产仍无 HISTORY 标记 | 在 Pointer/DOCUMENT_INVENTORY 标记 A 代资产为 HISTORY / VISUAL REFERENCE ONLY |
| 四套 IA 并存（A/B/C/D 代） | D 代 + Structure Baseline 为收敛基础 | Final UI Master 以 Structure Baseline 七区 + D 代壳为唯一起点；其余资产降级 |
| C 代真实前端（4 项+更多侧栏）与七区不符 | 08-13 截图早于 Phase B 集成 | Phase B 后重新取证；取证前不得把 C 代截图当作当前 IA 证据 |

## 5. 状态宣告

**SYSTEM COMPETITIVE RESEARCH COMPLETE**（2026-09-12）。
下一 Gate（非本轮任务）：CEO 消费 `CURIS_DESKTOP_PRODUCT_AND_DESIGN_DIRECTION.md` 与本 Synthesis → 决定 Final UI Master 重启范围（建议按 R1→R5）→ 正式 Design Research / Issue 流程。
本轮边界遵守声明：未修改任何代码/Figma/Runtime/Product Authority；未 commit/push；所有新文件均为 RESEARCH/EVIDENCE 类。
