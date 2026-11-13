# CURIS DESIGN DOCUMENT CONSOLIDATION / AUTHORITY AUDIT

> **性质**：READ-ONLY 审计。本报告为唯一新增文件；**未修改任何 Authority / Closure / Pointer / Blueprint / 高保真 / 代码**。
> **日期**：2026-08-17
> **触发**：设计文档过多、Authority 分散，导致新 Workspace Design Agent 难以定位「最少必读集合」。
> **目标**：回答「新 Agent 接手时最少应读哪些文件才能获得完整、最新、不冲突的 Shared 设计规则」，并给出 MERGE / KEEP / HISTORICAL / DEPRECATE / POINTER UPDATE 建议清单。
> **纪律（本轮）**：不创建新的 Design Specification；不修改任何现有文件；冲突只记录不解决。

---

## 0. 核心结论速览（TL;DR）

1. **真正的 Workspace Shared Design Authority 是 `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen）**。它是 Workspace 共享契约层（Layer 0–3：四独立 Pane + Adaptive Surface + 7 Shared Pattern + Employee Workstation/Detail/Presence + Main 组合 + Employee Work Area/Composer）的唯一 Frozen 真源。
2. **最近三轮 Closure（Main Composition ΔX9 / Work Area+Composer ΔX10 / Workstation Pattern ΔS1-3）已完整回写 Shell Contract**（Pointer #45/#48 确认）。
3. **唯一明显「Closure 有规则未被 Authority 吸收」的是 `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`**：其「七状态矩阵 / 长期 History·Asset·Config IA / 高保真整改清单」未进入任何 Frozen Authority。
4. **可退出新 Agent 必读集合**：`WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md`（已取代）、`Curis_Workspace_Shell.md`（草案·高风险误导）、`CURIS_SHARED_EMPLOYEE_WORKSTATION_PATTERN_CLOSURE.md`（已回写→历史参考）、`Curis_Company_OS_Shared_Authority_Consolidation_Review.md`（评审记录）、`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md`（视觉收口·过程参考）。
5. **存在同一规则多真源**：Employee Workstation=Conversation-first、Context Isolation、Main=业务展示区+工作区 均有多处表述，但层级一致（Blueprint→Shell Contract→Closure），无实质冲突。
6. **旧规则仍会误导新 Agent**：`Curis_Workspace_Shell.md`（草案·「5 槽位」模型）高风险；`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` §0 仍写「每 Employee 固定轻量卡」，与 Delta-X11 后「普通列表行、无 Card」已脱节（中风险）。
7. **Pointer 能路由到核心 Frozen Authority + 两份 Approved Closure，但不完整**：缺 Final IA、Design System 视觉基线未显式列入权威链、#45/#48 重复。
8. **最小阅读集目标可达**：1 入口（Pointer）+ 1 Shared Design Authority（Shell Contract，辅以 Shared Authority 语义 + Design System 视觉基线）+ 当前 Domain 必要输入。

---

## 1. 文档清单与分类标记

> 标签说明（按用户指定）：`CURRENT AUTHORITY` / `DOMAIN AUTHORITY` / `METHOD·INPUT` / `REVIEW·CLOSURE EVIDENCE` / `SUPERSEDED` / `DUPLICATE` / `UNKNOWN`。
> 「必读(新 Agent)」= 设计通用 Workspace Shared 规则时是否必须读。

### A 组 — Frozen 权威（Shared / 跨业务 / 视觉 / 路由）

| 文件 | 分类标签 | Status | 角色 | 必读 |
|---|---|---|---|---|
| `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | **CURRENT AUTHORITY**（Workspace Shared） | Frozen（S1–S7 + P1–P7 + ΔS1/2/3 + ΔX9 + ΔX10） | **Workspace Shared Design Authority**：四 Pane、Adaptive Surface、7 共享 Pattern、Employee Workstation/Detail/Presence、Main 组合、Employee Work Area/Composer | ✅ 核心 |
| `Curis_Company_OS_Shared_Authority.md` | **CURRENT AUTHORITY**（跨业务语义） | Frozen（2026-08-16 FINAL REVIEW） | Company OS 跨业务语义：Context Isolation Truth、Shared Employee Service Relation、Business=Team+Office 等；**不定义 UI Status / Runtime State Schema**（让位 Shell Contract） | ✅（被 Shell Contract 消费） |
| `Curis_Design_System.md` | **CURRENT AUTHORITY**（视觉令牌） | Frozen | 设计系统基线：Desktop First、Company OS+Workspace 关系、`--ui-*` 令牌纪律 | ✅ 视觉基线 |
| `Curis_UI_Frozen_Spec_2026-08-04.md` | **CURRENT AUTHORITY**（UI 视觉基线） | Frozen | 冻结 UI 交付规格：`_system/tokens.css`、18 页高保真、Dev Mode、组件/页面规格、a11y | ✅ 视觉基线 |
| `PRODUCT_DOCUMENT_POINTER.md` | **CURRENT AUTHORITY**（路由入口） | Frozen | 唯一导航页；权威链 #32/#45/#46/#47/#48 覆盖 Shared Authority / Shell Contract / 两份 Approved Closure | ✅ 入口 |

### B 组 — Approved Closure（已回写 Shell Contract，作审批证据保留）

| 文件 | 分类标签 | Status | 角色 | 必读 |
|---|---|---|---|---|
| `CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md` | **REVIEW·CLOSURE EVIDENCE** | APPROVED（已回写 ΔX9） | Main = 业务展示区 + 工作区 Shared 规则；是 Workstation Pattern Closure 的超集扩展 | ⚠️ 可选（已入 Shell Contract） |
| `CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` | **REVIEW·CLOSURE EVIDENCE** | APPROVED（修正 3 点 · 已回写 ΔX10） | 工作区 + Composer Shared Shell 固定；Employee Row / UI Status 投影 / Conversation Surface / Provider Adaptation | ⚠️ 可选（已入 Shell Contract） |

### C 组 — Closure 证据 / 部分未吸收

| 文件 | 分类标签 | Status | 角色 | 必读 |
|---|---|---|---|---|
| `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md` | **REVIEW·CLOSURE EVIDENCE** | FINAL IA CLOSURE（收口版） | 四 Pane 职责 + 最终 IA + **七状态矩阵** + **长期 History·Asset·Config 归属** + 高保真整改清单。自声明替代 Pane Responsibility Closure | ⚠️ 需读，但注意其「七状态矩阵 / 长期 History·Asset·Config」**未入 Frozen Authority** |
| `WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` | **REVIEW·CLOSURE EVIDENCE** | VISUAL CLOSURE（高保真重制完成·停止 Review） | 高保真重制视觉收口；§0 仍含「每 Employee 固定轻量卡」旧术语（与 Delta-X11 脱节） | ❌ 过程参考 |

### D 组 — 已取代 / 草案 / 应弃用

| 文件 | 分类标签 | Status | 角色 | 必读 |
|---|---|---|---|---|
| `WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md` | **SUPERSEDED** | REVIEW INPUT（已被 Final IA 收口替代） | 四栏职责急救版；核心论断被 Final IA 吸收 | ❌ 已取代 |
| `Curis_Workspace_Shell.md` | **UNKNOWN / 草案**（高风险误导） | 草案·「待 Frozen 验收」 | 早期「域无关工作台骨架 / 5 槽位」模型；被 Frozen Shell Contract 取代，但仍在被引用为「运营视角补充」 | ❌ **高风险** |
| `CURIS_SHARED_EMPLOYEE_WORKSTATION_PATTERN_CLOSURE.md` | **REVIEW·CLOSURE EVIDENCE**（已回写→历史） | APPROVED + ΔS1/2/3 已回写 | 早期 Employee Workstation Pattern Closure；内容已入 Shell Contract | ❌ 历史参考 |
| `Curis_Company_OS_Shared_Authority_Consolidation_Review.md` | **REVIEW·CLOSURE EVIDENCE**（评审记录） | AUTHORITY CONSOLIDATION REVIEW（未 Frozen） | Shared Authority 升格评审；结论已落定 Frozen Shared Authority | ❌ 评审记录 |

### E 组 — Domain（非 Shared，仅在设计该具体域时必读）

| 文件 | 分类标签 | Status | 角色 |
|---|---|---|---|
| `Curis_Content_Growth_Domain_Authority.md` | **DOMAIN AUTHORITY** | Frozen | Content Growth 域权威；设计该域时必读 |
| `Curis_Workspace_Engineering_Product_Translation.md` | **DOMAIN AUTHORITY / METHOD** | APPROVED CANDIDATE | Workspace Engineering 域产品翻译（当前 Domain 必要输入） |
| `Curis_Workspace_Engineering_Product_Translation_Review.md` | **REVIEW·CLOSURE EVIDENCE** | APPROVED CANDIDATE | 上述翻译的 Review/Closure |
| `Curis_Workspace_Engineering_Technical_Reality_Delta_Review.md` | **METHOD·INPUT** | Delta Review | 技术现实 Delta（P0 后） |
| `Curis_Workspace_Engineering_Company_Integration_Product_Delta.md` | **METHOD·INPUT** | Delta Review | 公司集成产品 Delta（P0.5 后） |
| `Curis_Design_System_Delta_RD_Workspace.md` | **METHOD·INPUT** | Review（RD 专属，未回写 Design System） | RD Workspace 视觉基线 v1 Delta |
| XHS / RD / Douyin / TTK / Channel / Content Growth 探索类文档（约 40+ 份） | **METHOD·INPUT / DOMAIN** | Review / Exploration | 各域探索、实例 Spec、竞品研究；非 Shared，非通用必读 |

### F 组 — 研究 / 方法论（非 Authority）

| 文件 | 分类标签 | Status | 角色 |
|---|---|---|---|
| `WORKBUDDY_PROJECT_TO_CURIS_WORKSPACE_LONG_TERM_IA_REVIEW.md` | **METHOD·INPUT**（研究） | RESEARCH + GAP REVIEW | 长期 IA 参考研究；含 Context Isolation 约束 |
| `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Methodology.md` 等 Methodology Set | **METHOD·INPUT** | Review / APPROVED CANDIDATE | Workspace Engineering 方法论（Pointer #34） |

---

## 2. 八问逐条回答

### Q1. 当前真正的 Workspace Shared Design Authority 是哪一份？
**`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen）是唯一 Workspace Shared Design Authority**（契约层 + 模式层，Layer 0–3）。
其 Companion（非替代）为：
- `Curis_Company_OS_Shared_Authority.md`（Frozen）— 跨业务语义（Context Isolation、Employee Service Relation、Business=Team+Office），被 Shell Contract 消费；
- `Curis_Design_System.md` + `Curis_UI_Frozen_Spec_2026-08-04.md`（Frozen）— 视觉令牌与 UI 基线。
三者共同构成「Shared Design 基线」，但**契约/Shell 层真源只有 Shell Contract 一份**。

### Q2. 最近 Main Composition / Work Area / Composer 规则是否已完整回写 Authority？
**是，已全部回写 Shell Contract。**
- Main Composition → ΔX9（Pointer #45/#46 确认）；
- Employee Work Area + Composer → ΔX10（Pointer #47/#48 确认；Shell Contract §3.1/§3.5/§3.14 + Shared Authority 跨文档引用）；
- Employee Workstation Pattern → ΔS1/S2/S3（Pointer #91 区域 + Pattern Closure 自述）。
三份 Closure 现均为「审批证据」，规则真值在 Shell Contract。

### Q3. 哪些 Closure 还有 Authority 未吸收的规则？
**`WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`** 含未被任何 Frozen Authority 吸收的内容：
- **七状态矩阵**（状态 1–7 显示/为什么/禁止）— Shell Contract 无此矩阵；
- **长期 History·Asset·Config 归属 / 活动流 IA** — Shell Contract 仅一处「Company-wide Object Search」提及，未定义长期信息表面 IA；
- **高保真整改清单 / 重制条件判定** — 属过程证据，非产品 Authority 内容。
`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` 的通用视觉规则（四 Pane、无全局 Topbar）已被 Shell Contract / Design System 覆盖；其原型特有规则（评审控件不伪装 Topbar）非 Authority 内容。**结论：Final IA 是主要缺口。**

### Q4. 哪些文档可以退出新 Agent 必读集合？
| 文档 | 退出理由 |
|---|---|
| `WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md` | 已取代（Final IA 收口） |
| `Curis_Workspace_Shell.md` | 草案，被 Frozen Shell Contract 取代，且「5 槽位」模型会误导 |
| `CURIS_SHARED_EMPLOYEE_WORKSTATION_PATTERN_CLOSURE.md` | 已回写 Shell Contract，仅作历史参考 |
| `Curis_Company_OS_Shared_Authority_Consolidation_Review.md` | 评审记录，结论已落定 Frozen |
| `WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` | 视觉收口·过程参考（高保真保留为参考） |
| E/F 组 Domain·Methodology·Research 文档 | 非 Shared；仅设计具体域时按需读 |

### Q5. 是否存在同一规则多个真源？
| 规则 | 多处表述 | 判定 |
|---|---|---|
| Employee Workstation = Conversation-first | Product Blueprint + Shell Contract §3.1 + 多份 Closure | 层级一致（Blueprint→Shell→Closure），无实质冲突 |
| Context Isolation | Shared Authority + WorkBuddy IA Review + Final IA | 一致，Shared Authority 为真源 |
| Main = 业务展示区 + 工作区 | Main Composition Closure（APPROVED）→ Shell Contract ΔX9 | 现已单真源（Shell Contract） |
| Employee Detail = Utility | Shell Contract §3.14 + Shared Authority + Closures | 一致 |
**结论：多真源但层级清晰、无冲突。** 唯一例外见 §3 冲突记录（草案 `Curis_Workspace_Shell.md` 的「5 槽位」模型与 Frozen 四 Pane 实质不同）。

### Q6. 是否存在旧规则仍会误导新 Agent？
- **高风险**：`Curis_Workspace_Shell.md`（草案·「5 槽位 / 域无关工作台骨架」）与 Frozen Shell Contract「四独立 Pane + Adaptive Surface（Context/Utility 默认收起）」模型不同，且仍被 Shell Contract 注释引用为「运营视角补充」。新 Agent 若先读此草案会误解 Shell 结构。
- **中风险**：`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` §0 仍写「每 Employee 固定轻量卡（头像+姓名+岗位+当前职责+当前状态+展开/收起）」，与 Delta-X11 后「普通列表行、无 Card、状态轻量文本靠右」已脱节。
- **低风险**：早期 Closure（Pane Responsibility / Workstation Pattern）已自标注「已取代 / 已回写」，单独读不致严重误导。

### Q7. PRODUCT_DOCUMENT_POINTER.md 当前是否已能明确路由 Design Agent？
**能路由到核心，但不完整。**
- ✅ 已覆盖：`#32` Shared Authority、`#45`/`#48` Shell Contract、`#46` Main Composition Closure、`#47` Employee Work Area+Composer Closure。
- ❌ 缺口 1：未列入 `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md` → 新 Agent 会错过七状态矩阵 / 长期 History·Asset·Config IA。
- ❌ 缺口 2：`Curis_Design_System.md` / `Curis_UI_Frozen_Spec_2026-08-04.md` 未显式列入权威链（视觉基线隐含但未指明）。
- ⚠️ 冗余：`#45` 与 `#48` 均为 Shell Contract（一个记 ΔX9、一个记 ΔX10），可合并。
- ⚠️ 未标注弃用：`Curis_Workspace_Shell.md`、`Pane Responsibility Closure` 未标记为「新 Agent 勿读」。

### Q8. 最终建议的 Minimum Design Agent Reading Set
**目标：1 入口 + 1 Shared Design Authority + 当前 Domain 必要输入。**

```
① 入口（必读）
   PRODUCT_DOCUMENT_POINTER.md
        ↓ 路由到
② Shared Design Authority（核心必读，3 份 Frozen 互补）
   - Curis_Workspace_Shell_Contract_And_Shared_Patterns.md   ← Workspace Shared 契约/模式真源
   - Curis_Company_OS_Shared_Authority.md                    ← 跨业务语义（Context Isolation 等）
   - Curis_Design_System.md + Curis_UI_Frozen_Spec_2026-08-04.md  ← 视觉令牌/UI 基线
        ↓ 若需理解「为何这样定」
   ③ 可选证据（已回写，可不读）
   - CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md
   - CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md
        ↓ 设计具体域时追加
④ 当前 Domain 必要输入（按域选一）
   - Workspace Engineering 域 → Curis_Workspace_Engineering_Product_Translation.md (APPROVED CANDIDATE)
   - Content Growth 域     → Curis_Content_Growth_Domain_Authority.md (Frozen)
   - 其他域                → 该域 Domain Authority / Instance Spec
```

**说明**：严格意义上「1 个 Shared Design Authority」在物理上是 Shell Contract 单份（契约层真源）；Shared Authority 与 Design System 是其语义/视觉 Companion，稳定且数量极少，不显著增加新 Agent 负担。两份 Approved Closure 已回写，可省。

---

## 3. 冲突记录（仅记录 · 不解决）

> 以下冲突**只记录，本轮不解决、不修改任何文件**。

- **冲突 C1（高风险误导）**：`Curis_Workspace_Shell.md`（草案·「5 槽位 / 域无关工作台骨架」）vs `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen·四独立 Pane + Adaptive Surface）。二者 Shell 模型不一致。裁定权：Frozen Shell Contract 胜（草案未 Frozen，且 Shell Contract 注释仅将其作「运营视角补充」引用）。
- **冲突 C2（术语脱节）**：`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md` §0 写「每 Employee 固定轻量卡」vs Delta-X11 后高保真「普通列表行、无 Card」。文档术语与最新实现脱节。
- **冲突 C3（版本引用不一致）**：多处引用 Product Blueprint 为「v4.4 Single Current」（Employee Workstation Pattern Closure），而 Pointer #4 记当前 Blueprint 为 **v5.1（Status: Review）**。Blueprint 版本引用不统一。
- **冲突 C4（引用路径错误 / 路由风险，非规则冲突）**：
  - `Curis_Workspace_Engineering_Technical_Reality_Delta_Review.md` 引用 `docs/03_Design/CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md`，实际文件在 `docs/05_Workspace_Engineering/`；
  - `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md` 引用 `Curis_Workspace_Engineering_lifecycle.md`，全仓未找到（实际为 `docs/05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md`）。
  上述错误路径会导致新 Agent 找不到文件。

---

## 4. 后续建议清单（MERGE / KEEP / HISTORICAL / DEPRECATE / POINTER UPDATE）

> 以下为**建议**，本轮 READ-ONLY 不执行。

### MERGE（未来合并，非本轮）
- **M1**：将 `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md` 的「七状态矩阵 / 长期 History·Asset·Config IA」作为新 Delta 回写 `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（或新建 Frozen IA Authority），消除「Closure 有而 Authority 无」的缺口。
- **M2**：若未来恢复 `CURIS_WORKSPACE_SHARED_DESIGN_SPECIFICATION.md` 的创建，应将其定位为 **Shell Contract + Shared Authority + Design System 视觉基线的纯消费型整合文档**（Authority Consolidation，不新增规则），而不是新的真源。

### KEEP（保持为当前权威 / 必读）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen）— 核心。
- `Curis_Company_OS_Shared_Authority.md`（Frozen）。
- `Curis_Design_System.md`（Frozen）+ `Curis_UI_Frozen_Spec_2026-08-04.md`（Frozen）。
- `PRODUCT_DOCUMENT_POINTER.md`（Frozen）— 入口。
- `CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md` + `CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` — 保留为 APPROVED 审批证据（已回写）。

### HISTORICAL（降级为参考，退出必读，保留记录）
- `CURIS_SHARED_EMPLOYEE_WORKSTATION_PATTERN_CLOSURE.md`（已回写→历史）。
- `Curis_Company_OS_Shared_Authority_Consolidation_Review.md`（评审记录）。
- `WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md`（视觉收口·过程参考；高保真保留）。
- `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md` — 暂 KEEP，待 M1 合并后可转 HISTORICAL。

### DEPRECATE（移出活跃流转，避免误导）
- `Curis_Workspace_Shell.md` — 草案·「5 槽位」模型，与 Frozen 四 Pane 冲突，**高风险**，建议明确标记 DEPRECATED 并从 Shell Contract 注释的「运营视角补充」引用中摘除。
- `WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md` — 已自声明 SUPERSEDED，确认弃用。

### POINTER UPDATE（建议更新 Pointer）
- **P1**：新增 `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md` 条目，并注明「其七状态矩阵 / 长期 History·Asset·Config IA 尚未进入 Frozen Authority（见审计 M1）」。
- **P2**：合并 Pointer #45 / #48（同为 Shell Contract，分别记 ΔX9 / ΔX10 可合并为一行）。
- **P3**：在权威链中显式列入 `Curis_Design_System.md` + `Curis_UI_Frozen_Spec_2026-08-04.md` 作为视觉基线入口。
- **P4**：在 Pointer 标注 DEPRECATED 文档（`Curis_Workspace_Shell.md`、`Pane Responsibility Closure`）为「新 Agent 勿读」。
- **P5**：修正 C4 错误引用路径（PRODUCT_HANDOFF、lifecycle.md 实际位于 `docs/05_Workspace_Engineering/`）。
- **P6**：若未来创建 Shared Design Specification，于 Pointer 增加该整合入口（消费型，非真源）。

---

## 5. 本轮交付与纪律确认

- ✅ 仅生成本报告 `CURIS_DESIGN_DOCUMENT_CONSOLIDATION_AUDIT.md`；
- ✅ 未修改任何 Authority / Closure / Pointer / Blueprint / 高保真 / 代码；
- ✅ 未创建新的 Design Specification（原 `CURIS_WORKSPACE_SHARED_DESIGN_SPECIFICATION.md` 仍暂停）；
- ✅ 冲突仅记录不解决；
- ✅ 未新增设计规则、未自行优化、未重新解释产品（纯 Authority Consolidation 审计）。

**完成后停止 Review。**
