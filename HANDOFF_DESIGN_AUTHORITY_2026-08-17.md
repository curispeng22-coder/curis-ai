# Curis Workspace Engineering — 设计权威收敛交接文档

> **用途**：本文件用于把「设计权威收敛（Design Authority Consolidation）」这一轮工作从当前对话转移到新对话。新对话读完本文件 + 文末「必读最小集」即可完整理解已完成的任务、当前进度、纪律红线与可选下一步。
> **读完即可删**：本文件是临时交接产物，非产品权威文档；接手后可作为 VISUAL QUALITY REFERENCE 之外的普通笔记，任务稳定后请删除，避免再次制造文档冗余。

---

## 0. 一句话背景

Curis = 一人公司自动任务与工作流系统（产品主轴见工作记忆 §2）。本轮工作的范围**只限「Workspace Engineering 的设计权威（Design Authority）收敛」**——即把散落多份设计文档中的 Shared 规则统一到唯一真源、清理陈旧表述、收敛文档路由。**全程未写产品代码、未动 Runtime State Schema、未改任何产品真相（Blueprint/Authority）。**

---

## 1. 当前进度（STOP 状态）

| 阶段 | 产出 | 状态 |
|---|---|---|
| Shared Main Composition Closure | `CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md` + 回写 Frozen ΔX9 | APPROVED，回写完成 |
| Shared Work Area + Composer Closure | `CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md` + 回写 Frozen ΔX10 | APPROVED，回写完成 |
| 高保真最后一轮简化 ΔX11 | `Curis_Workspace_Engineering_High_Fidelity_Remake.html` | 完成，STOP FOR REVIEW |
| Design Document Consolidation Audit（只读） | `CURIS_DESIGN_DOCUMENT_CONSOLIDATION_AUDIT.md` | 仅审计，未改文件 |
| Design Authority RECONCILIATION | 收敛 6 份文档 + Pointer + UI Blueprint 同步 | 完成，STOP FOR REVIEW |
| **STALE-RULE CLEANUP（最后一轮）** | 清 4 份文件陈旧表述 | **完成，STOP FOR REVIEW** |

**结论**：所有轮次均已「完成后停止 Review」。当前**没有任何进行中任务**。用户连续多轮明确指令「完成后停止 Review」，新对话**不应自动继续任何任务**，除非用户在新对话中发出新指令。

---

## 2. 权威地图（谁说了算）

### 2.1 唯一 Shared 真源（Frozen）
- **`docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`**（POINTER #45，Status: Frozen）
  - 这是 Workspace Shared 规则的唯一真源。Layer 0–3：四独立 Pane + Adaptive Surface + 7 Shared Pattern + Employee Workstation/Detail/UI Status 投影/Presence。
  - 已回写 Delta：S1–S3（2026-08-16）+ **X9（Shared Main Composition）+ X10（Shared Employee Work Area + Composer）+ X12（Shared Conversation Content Block）**（均为 2026-08-17）。
  - 关键边界已写入（STALE-RULE 新增）：
    - **三层概念边界**：`Runtime State Schema ≠ Employee UI Status Projection ≠ Conversation 展开状态`，相互独立不混用。
    - **Shared Work Area 是 Main 统一组成部分，非 Domain 可选项**。
    - **编目 ≠ 可省略**：采用矩阵是 Shared Pattern 编目，不授予 Business Workspace 省略 Shared Work Area 的自由。

### 2.2 配套权威（Frozen / Review）
- **跨业务语义（Frozen）**：`docs/03_Design/Curis_Company_OS_Shared_Authority.md`（§9 已 Frozen；§0 仅消费 Provider Permission 真值，不定义 UI Status/Runtime State Schema）
- **视觉基线（Frozen）**：`docs/03_Design/Curis_Design_System.md` + `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md`
- **UI 结构消费方（Review）**：`docs/01_Product/Curis_Product_UI_Blueprint.html`（唯一 Current UI Blueprint，POINTER #49；只消费 #45，不新增规则，已新增「Workspace 结构权威」节 #ws-auth）
- **产品真相（Review）**：`docs/01_Product/Curis_Product_Blueprint.html`（v5.1）

### 2.3 路由入口
- **`docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`**（Status: Frozen，2026-08-17 更新）—— 新会话进入 Curis 产品工作的唯一导航页。其末尾「设计文档路由（Design Agent）」段已给出最小必读集、勿读清单、External Design Agent Handoff Set。

### 2.4 历史文档（勿读 / 非必读 / NOT AUTHORITY）
- DEPRECATED：`Curis_Workspace_Shell.md`（草案 5 槽位）
- SUPERSEDED：`WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md`
- SUPERSEDED-for-Shared-UI：`WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`（其 Shared UI 规则已被 ΔX9/X10/X12 取代；仅保留 Workspace Engineering 自身 History/Asset/Config/Retention Domain IA 证据）
- HISTORICAL：`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md`、`CURIS_SHARED_BUSINESS_WORKSPACE_MAIN_COMPOSITION_CLOSURE.md`（#46）、`CURIS_SHARED_EMPLOYEE_WORK_AREA_AND_COMPOSER_CONTRACT_CLOSURE.md`（#47）—— 均为历史审批证据，规则已回写 #45
- **NOT AUTHORITY**：任何旧原型 HTML（如 `Curis_Workspace_Engineering_High_Fidelity_Remake.html`、`Curis_UI_Blueprint_Prototype.html`）仅作 VISUAL QUALITY REFERENCE — NOT AUTHORITY

---

## 3. 已完成的任务链（按时间，供理解因果）

1. **高保真重制 + ΔX9 回写**：Main = Domain Business Surface + 工作区；Employee Workstation ∈ Main.WorkArea。高保真 `Curis_Workspace_Engineering_High_Fidelity_Remake.html` 重制（真实四独立 Pane，无全局 Topbar）。
2. **有界 UX 收敛（第二轮）**：Context 改名「资料台」、工作区去 Card 化、Workstation 回归普通 AI Conversation。
3. **Shared Work Area + Composer Closure（ΔX10）**：Employee Row 两行结构、Shared Employee UI Status = Runtime Truth 投影（空闲 / 工作中·<desc> / 阻塞·<cause>，不新增 Primitive、不改 Runtime State Schema）、Shared Composer Shell 语义槽位。
4. **高保真最终简化 ΔX11**：彻底去 Card（单行列表行）、Conversation 删 wsStatusLine 整套、Result/Artifact 改 artRef 轻量引用、Composer 统一圆角 Surface、去大外框、清 HTML 顶部旧规则。
5. **Consolidation Audit（只读）**：确认真正 Authority = Shell Contract；三轮 Closure 已回写；指出 Final IA 七状态矩阵未吸收；给出最小阅读集与 MERGE/KEEP/DEPRECATE/POINTER UPDATE 建议。
6. **RECONCILIATION**：补 ΔX12（长内容块 bounded embedded）+ 标记 3 份历史文档（DEPRECATED/SUPERSEDED/HISTORICAL）+ 同步 UI Blueprint 消费 Frozen + 更新 Pointer（合并重复入口、建 Handoff Set）。
7. **STALE-RULE CLEANUP（最后一轮）**：清除 UI Blueprint 第 08 节 / Frozen Shell §3.1·§4 / Final IA Closure / Pointer 中已被取代的旧表述；全文 stale-term 复扫确认目标陈旧术语已清。

---

## 4. 纪律红线（新对话 MUST 遵守，若继续设计工作）

任何「继续设计 / 收敛 / 清理」类任务都必须守住：

1. **唯一 Shared 真源 = Frozen Shell Contract（#45）**。新规则必须先回写这里，再同步 Closure/Pointer/Blueprint。
2. **不建新 Primitive**：禁止新增如 `offline`/`unavailable`/`blocked` 等 Runtime/UI Primitive。
3. **不改 Runtime State Schema**：`working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle` 语义不动、不删、不迁移。
4. **不写产品代码**：本轮工作纯设计文档/原型层面，未动任何产品源码。
5. **不新建 Design Specification**：`CURIS_WORKSPACE_SHARED_DESIGN_SPECIFICATION.md` 已被用户暂停创建。
6. **不画 UI / 不重做高保真**：除非用户明确授权；旧原型仅 VISUAL QUALITY REFERENCE。
7. **视觉以 Frozen UI Spec 为准**，非 `terra-*`/`Terra*` 旧令牌（已作废）。
8. **文档路由以 POINTER 为准**，勿读 Deprecated/Superseded/Historical；不要因为「代码里有这个页面」就认为是需求依据。
9. **汇报强制三段式**：结论 → 原因 → 建议；中文白话、先结论（见工作记忆 §1）。

---

## 5. 可选下一步（均非进行中，需用户明确授权）

以下功能在审计/RECONCILIATION 中识别为「可选」，当前**未执行、未授权**：

- **MERGE Final IA 七状态矩阵 → Shell Contract 新 Delta**：审计建议，但用户此前裁定该矩阵属 Workspace Engineering Domain，按纪律未并入 Shared Shell。若用户改主意可执行。
- **POINTER C3 修复**：Blueprint 引用 v4.4 vs v5.1 不一致（产品真相已是 v5.1，引用以 Pointer #4 为准即可，低风险）。
- **POINTER C4 修复**：个别 Closure 旧引用路径（实际在 `docs/05_Workspace_Engineering/`）；已由 Handoff Set 用正确路径间接缓解，影响小。
- **正式创建 `CURIS_WORKSPACE_SHARED_DESIGN_SPECIFICATION.md`**：曾被暂停；若用户认为 Authority 已足够稳定可重启（但需注意纪律第 5 条，需用户明确放行）。

---

## 6. 文件改动日志（本轮最后两轮实际修改）

**RECONCILIATION 修改**：Shell Contract（ΔX12）、`Curis_Product_UI_Blueprint.html`（#ws-auth）、Pointer（#45/#48 合并、#49、路由段）、`Curis_Workspace_Shell.md`（DEPRECATED）、`WORKSPACE_ENGINEERING_PANE_RESPONSIBILITY_CLOSURE.md`（SUPERSEDED）、`WORKSPACE_ENGINEERING_VISUAL_DESIGN_REMAKE_CLOSURE.md`（HISTORICAL）。

**STALE-RULE CLEANUP 修改（4 份）**：
1. `Curis_Product_UI_Blueprint.html` 第 08 节：员工状态行→Shared UI Projection；Composer→语义槽位；删「自动展开规则」卡→用户控制、不绑定 Runtime。
2. `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §3.1/§4：三层概念边界 blockquote；工作区本质加注「非 Domain 可选项」；§4 加注「编目 ≠ 可省略」。
3. `WORKSPACE_ENGINEERING_FINAL_IA_CLOSURE.md`：顶部 SUPERSEDED-for-Shared-UI 声明。
4. `PRODUCT_DOCUMENT_POINTER.md`：路由段补充 Final IA Closure 的 SUPERSEDED-for-Shared-UI 边界。

---

## 7. 新对话接手清单（必做）

1. 先读 `PRODUCT_DOCUMENT_POINTER.md`（本文件 §2.3）。
2. 再读 Frozen `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（#45）—— 这是所有 Workspace Shared 规则的真源。
3. 若做具体业务设计，额外读对应 Domain Product Translation / Domain Authority。
4. **不要**读 Deprecated/Superseded/Historical 文档；**不要**把旧原型当权威。
5. 任何设计改动先想「是否破坏 §4 纪律红线」；宁可只改文档、回写 Frozen、更新 Pointer，不擅自写代码或画 UI。
6. 用户未发新指令前，**不要自动继续任何任务**——本轮以「STOP FOR REVIEW」收尾。

---

*本交接文档生成于 2026-08-17 凌晨，对应 STALE-RULE CLEANUP 完成后的稳定态。接手后若任务稳定，请删除本文件。*
