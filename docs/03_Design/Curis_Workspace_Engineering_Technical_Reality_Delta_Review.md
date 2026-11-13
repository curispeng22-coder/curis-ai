# Curis · Workspace Engineering Technical Reality Delta Review（空间工程 · 技术现实 Delta 评审）

**Status**: WORKSPACE ENGINEERING TECHNICAL REALITY DELTA REVIEW（Delta 评审完成 · 仅做 Delta，不重做 Product Translation）
**阶段**: PRODUCT / WORKSPACE DESIGN — Technical Reality Delta（承接《Workspace Engineering Product Translation · APPROVED CANDIDATE》+《WORKSPACE-ENGINEERING-P0-001_review》）
**日期**: 2026-08-16
**上位依据（只引用，不重定义）**:
- `docs/03_Design/Curis_Workspace_Engineering_Product_Translation.md`（APPROVED CANDIDATE · 本轮不重做）
- `docs/03_Design/Curis_Workspace_Engineering_Product_Translation_Review.md`（APPROVED CANDIDATE · 上文为 P0 前 Closure）
- `reviews/WORKSPACE-ENGINEERING-P0-001_review.md`（Decision: `IMPLEMENTED / ACCEPTED`）
- `docs/reviews/workspace-engineering-p0-2026-08-16/`（Desktop Evidence：7 张截图 + 构建先于 Package 哈希链 + 打包 Runtime API 安装证据）
- `CURIS_WORKSPACE_ENGINEERING_PRODUCT_HANDOFF.md`（§11 / §12.2 裁定，只引用）

---

## 0. 本评审范围与纪律（硬约束）

**只做 Delta，不重做 Product Translation。** 本评审不改写《Product Translation》任何章节、不新增界面像素、不进 Figma、不写前端、不重定义 Handoff 已裁定语义、不暴露内部原语。

**本评审唯一目的**：
1. 取 P0 真实验收通过后的技术事实，重新核对《Product Translation》§11「现在可确定 / 等 P0」矩阵；
2. 对矩阵每一项打标：`CONFIRMED BY P0` / `STILL POST-P3` / `PRODUCT DESIGN DECISION`；
3. 应用此前 Review 已批准的 Capability 激活三分类语义（Required for Activation / Required for Specific Action / Optional·Enhancement），用户侧仍只用自然语言、不暴露 Capability Primitive；
4. **不扩大 P0 能力**——不假设 update / migration / Marketplace / arbitrary extension / XHS·RD migration 已实现；
5. 判断 Workspace Engineering 是否已具备进入 Visual / High-Fidelity Design 的真实技术输入。

> **能力边界铁律（来自 P0 剩余边界 + Package 不能携带任意代码）**：P0 仅证明「可动态安装此前未知的 declarative Workspace Package」+「声明式渲染 + 通用领域对象投影 + 持久化 + 重启恢复 + 卸载保留」。**Package 仍不能携带任意代码**：因此「任意扩展 / 新 Surface 类型 / 升级迁移回滚 / 签名市场第三方信任」均未被 P0 覆盖，须等新 bounded Issue。

---

## 1. P0 真实验收通过的技术事实（仅列本评审处理的项）

来源：`WORKSPACE-ENGINEERING-P0-001_review.md` + Desktop Evidence（7 张截图：`desktop-dynamic-navigation` / `desktop-main-surface` / `desktop-context-main-utility` / `desktop-utility-surface` / `desktop-customer-feedback-created` / `desktop-restart-recovery` / `desktop-uninstall-navigation-removed`）。

| # | P0 已确认技术事实 | 证据 |
|---|---|---|
| F1 | 已 Build 的 Curis 可动态安装**此前未知**的 declarative Workspace Package（构建时该 Package 不存在，构建后才创建并安装，未改源码/未重建/未重装 App） | Build-before-Package PASS：App 可执行 mtime/hash 先于 Package；打包 App 扫描 Package ID、`CustomerFeedback`、客户反馈办公室 = **0 匹配**；post-build Package 经打包 Runtime API 安装 |
| F2 | Registry-driven navigation 已成立（安装后导航出现，卸载后消失） | Dynamic navigation PASS；`desktop-dynamic-navigation.jpg` + `desktop-uninstall-navigation-removed.jpg` |
| F3 | declarative Main / Context / Utility 已成立（同一通用宿主渲染声明的三 Pane 组件） | Declarative surfaces PASS；`desktop-main-surface` / `desktop-context-main-utility` / `desktop-utility-surface.jpg` |
| F4 | generic Package domain object + safe Core action 已成立（一个通用 Package 领域对象/活动投影；有限 P0 Core action allowlist 仅含 `core.domain-object.create`） | Business persistence PASS：声明的 `CustomerFeedback` 经 UI 创建并持久化（`desktop-customer-feedback-created.jpg`）；actual architecture 记录「one generic Package domain-object/activity projection」 |
| F5 | SQLite persistence + Desktop restart 已成立（同一 App 二进制完整停止/启动后恢复 Registry/Workspace/对象/活动） | Desktop restart PASS；`desktop-restart-recovery.jpg`；isolated SQLite 路径 + instance/Workspace 恢复 |
| F6 | uninstall + read-only retention 已成立（活动文件移除、Package 卸载、instance/Workspace 归档、对象/活动/来源保留只读） | Uninstall/retention PASS；`desktop-uninstall-navigation-removed.jpg` |
| F7 | **Package 仍不能携带任意代码**（strict JSON Package validator + 本地不可变 Package Store；No second Employee/Responsibility/Capability/Decision/Evidence/Computer Access system 被引入；权限需求仍是 declaration 而非 grant） | actual architecture + Shared Core impact + Remaining boundary 明确「arbitrary extensions … remain unimplemented」 |

> **P0 剩余边界（直接约束本评审，不可越过）**：Package update / migration / rollback、signing / Marketplace trust、arbitrary extensions、Workspace migrations、以及 Workspace Engineering 的 product/UX 本身，**均未实现**，须新 bounded Issue。

---

## 2. 重新核对《Product Translation》§11 矩阵（Delta 打标）

### 2.1 §11.1「现在就可以确定」—— 全部为 `PRODUCT DESIGN DECISION`

这些项在 P0 前已基于 Frozen Shell + 允许 Surface 注册表 + Package Domain Schema 概念确定，P0 不改变其决策，也不为其提供「新」信息（少数被 P0 运行时佐证，但决策基础本来就不依赖 P0）。

| §11.1 设计项 | 打标 | 说明（Delta 备注） |
|---|---|---|
| IA 布局（经营总览 / 业务空间首页 / 创建·启用流 在四 Pane 内位置与角色） | **PRODUCT DESIGN DECISION** | Frozen Shell 四 Pane 约束；P0 的 F2/F3 佐证「Registry 驱动导航 + 声明式 Surface 渲染」真实成立，但不改变 IA 决策。 |
| Surface 类型（仅用注册表 9 种，不新增） | **PRODUCT DESIGN DECISION** | Frozen Shell 硬约束；P0 的 F3/F7 进一步确认「Package 只能声明复用既有 Surface，不能借代码新增 Surface 类型」。 |
| 内部概念隐藏（Handoff §9 全部原语不进用户视野） | **PRODUCT DESIGN DECISION** | Handoff §12.2 + §9 裁定；P0 内部架构（Package/Gate/Router/Schema 不暴露）与此一致。 |
| CEO 决策点（4 个经营决策点语义） | **PRODUCT DESIGN DECISION** | Handoff §3.2；不依赖 Runtime。 |
| Workspace Proposal（6 答结构） | **PRODUCT DESIGN DECISION** | 用户面文档结构；不依赖 Runtime。 |
| 三态表达（默认/单独设置/例外 pill） | **PRODUCT DESIGN DECISION** | 复用 Content Growth Operating Rules 三态。 |
| Employee 可见（Shared Employee Detail 内「工作方式」扩展） | **PRODUCT DESIGN DECISION** | T5 裁定；P0 未引入新 Employee 系统（F7），一致。 |
| Capability 缺口语言（「需连接 X」+ capability-gap 卡；不静默降级） | **PRODUCT DESIGN DECISION** | 语义层决策；P0 的 F7（权限是 declaration 非 grant，fail-closed）佐证「不静默降级」成立。三分类见 §3。 |
| 进化通知（Business Home 轻量浮现 + 结构性变更走 P7 决策包） | **PRODUCT DESIGN DECISION** | 复用 Content Growth 进化机制；运营学习驱动的 method 进化，非 Package 升级（见 §4 边界）。 |
| 同一份方法（Conversation + Direct Edit 改同一底层） | **PRODUCT DESIGN DECISION** | Content Growth 裁定。 |
| 失败/空/缺口（empty-failure-gap card 三态） | **PRODUCT DESIGN DECISION** | Frozen Shell 注册表 Surface。 |
| Package First 思维（用 Surface 组合/领域对象/允许 Action/能力需求 思考，不写页面） | **PRODUCT DESIGN DECISION** | 设计方法论；P0 的 F1/F4 证明此思维与真实 Runtime 模型一致。 |

### 2.2 §11.2「必须等 P0 Runtime 验证」—— 逐项重新打标

| §11.2 原待验证项 | 打标 | P0 事实依据 | Delta 结论 |
|---|---|---|---|
| ① 动态安装未知 Workspace | **CONFIRMED BY P0** | F1（构建先于 Package、0 匹配、post-build 经 Runtime API 安装）+ F2（Registry 驱动导航） | 「能否不改源码/不重建就上新业务」已由真实 Desktop 证据回答：**能**。原 §11.2 该项不确定性消除。 |
| ② 任意新 Surface 类型 | **CONFIRMED BY P0（有界约束）** | F3（声明式 Main/Context/Utility 由通用宿主渲染）+ F7（Package 不能携带任意代码） | 明确为**有界确认**：声明式渲染既有注册表 Surface 已成立；但 Package **不能新增 Surface 类型**（无代码载体）。原「假设能用任意新 Surface」之不确定性消除 → 结论为「仅限既有 9 种 + 声明式组合」。 |
| ③ 自定义领域对象自动运行 | **CONFIRMED BY P0（有界约束）** | F4（generic Package domain-object/activity 投影 + `core.domain-object.create` allowlist）+ F5（持久化 + 重启恢复）+ F7（无任意代码） | 明确为**有界确认**：declarative 自定义领域对象经声明即可投影、持久化、重启恢复、UI 创建（`CustomerFeedback` 实例即证据）。但限「声明式 + 通用投影」，不含任意代码驱动的对象。原不确定性消除。 |
| ④ Capability 检查自动通过 | **CONFIRMED BY P0（约束匹配）+ 语义为 PRODUCT DESIGN DECISION** | F7（权限是 declaration 非 grant；Failure truth PASS：无效路径/未知 action fail-closed，Registry 无残留） | 技术现实**已确认**与 Translation 假设一致：权限是 request、缺失即诚实呈现、fail-closed、不静默降级。**不自动通过**。其「是否阻塞激活」的产品三分类（§8.1）为 PRODUCT DESIGN DECISION，P0 不改动。 |
| ⑤ 签名 / 市场 / 第三方信任 | **STILL POST-P3** | P0 Remaining boundary 明确「signing / Marketplace trust … remain unimplemented」 | 未覆盖。不假设已实现。须新 bounded Issue。 |
| ⑥ 升级 / 迁移 / 回滚 | **STILL POST-P3** | P0 Remaining boundary 明确「Package update / migration / rollback … remain unimplemented」 | 未覆盖。不假设已实现。须新 bounded Issue。 |

### 2.3 矩阵打标汇总

- **CONFIRMED BY P0（含 2 项有界约束）**：§11.2 ① 动态安装未知 Workspace；② 任意新 Surface 类型（有界：声明式复用既有）；③ 自定义领域对象自动运行（有界：声明式 + 通用投影）；④ Capability 检查（约束匹配：request 非 grant、fail-closed）。
- **STILL POST-P3**：§11.2 ⑤ 签名/市场/第三方信任；⑥ 升级/迁移/回滚。
- **PRODUCT DESIGN DECISION**：§11.1 全部 12 项 + ④ 的语义三分类。

---

## 3. 应用此前 Review 批准的 Capability 激活三分类语义

此前 Product Translation Review 已批准的一处修正，本次 Delta **原样沿用、不重做**：

| 分类 | 用户面自然语言 | 对激活 / 功能的影响 |
|---|---|---|
| **Required for Activation（启用必需）** | 「启用前需先连接 X 平台/工具」 | 阻塞激活，直到连接；连接后可启用 |
| **Required for Specific Action（某项功能需要）** | 「连接 X 后，[某功能] 才能用」 | **不阻塞激活**；该特定功能连接前不可用（置灰/提示），其余正常 |
| **Optional / Enhancement（可增强）** | 「可稍后连接 X，获得增强」 | 不阻塞；启用后随时连接，纯增强 |

**与 P0 技术现实的一致性（Delta 确认）**：
- P0 的 F7 确认「权限需求仍是 declaration 而非 grant」、Failure truth PASS 确认「无效/未知 fail-closed、Registry 无残留」→ 与 Translation「不静默降级、缺失即诚实呈现」完全一致。
- P0 **未改变**能力检查的 request 模型，因此三分类的「是否阻塞激活」纯属产品语义层判定（PRODUCT DESIGN DECISION），不暴露 Capability Primitive。
- 用户侧仍只用自然语言；不写「缺一个 Connector Primitive / Capability Gap 判定失败」。

---

## 4. 进化旅程（§2.C）的边界澄清（防止误读 P0）

《Product Translation》§2.C「已有 Workspace 进化」描述的是**运营学习驱动的经营方法进化**（Content Growth 已落地机制：轻量微调留痕、结构性变更走 P7 决策包），**不是 Package 升级/重装**。

- P0 的 F6（uninstall + read-only retention）证明的是 **Package 生命周期真实成立**（安装/卸载/保留），**不是**「进化 = 重新打包升级」。
- 「进化」在 CEO 面 = 经营方法调整（可设计）；「Package 升级/迁移/回滚」= §11.2 ⑥ **STILL POST-P3**，不在本批 Visual Design 范围。

> 因此 §2.C 的 CEO 体验**可基于已确认技术现实设计**；但任何把「进化」画成「换 Package 版本 / 迁移数据」的暗示都越界，须剔除。

---

## 5. Visual / High-Fidelity Design 真实技术输入判断

### 5.1 判定

```text
VERDICT: GO — Workspace Engineering 已具备进入 Visual / High-Fidelity Design 的真实技术输入
          （CEO 面三条旅程 + Proposal + 决策点 + 能力三分类 + 失败/缺口卡 均可进入高保真）
BOUNDS:  声明式能力边界（无任意代码）· POST-P3 排除项（见 §5.2）
```

### 5.2 判定依据

**已具备真实技术输入（P0 已用真实 Desktop 证据闭环）**：
- 核心机制真实成立：Build Curis 可动态安装此前未知的 declarative Workspace Package（F1）→ Registry 驱动导航（F2）→ 声明式 Main/Context/Utility 渲染（F3）→ 通用领域对象投影 + 安全 Core action（F4）→ SQLite 持久化 + 桌面重启恢复（F5）→ 卸载 + 只读保留（F6）。
- CEO 面体验所依赖的全部上层约定，要么 Frozen/APPROVED（Frozen Shell 四 Pane、9 种 Surface、P1–P7、Content Growth 已落地用户面），要么 P0-CONFIRMED（动态声明式安装/渲染/持久化），要么 PRODUCT DESIGN DECISION（4 决策点、Proposal 6 答、能力三分类、失败/缺口卡）。
- 因此「表达意图 → 看 Proposal → 决策 → 激活 → 运营/进化通知」这条 CEO 主链，已从「设计假设」升级为「有真实 Runtime 背书的可用体验」，可以进入像素级高保真。

**进入 Visual Design 时的硬性边界（不扩大 P0 能力）**：
1. **声明式能力边界**：设计必须假定 Package 只能声明复用既有 Surface + 通用领域对象投影 + 有限安全 Core action；**不得**预设「Package 携带代码实现任意新交互/新 Surface 类型」。
2. **POST-P3 排除项（本批 Visual Design 不含其流程）**：
   - ⑤ 签名 / Marketplace / 第三方信任的 UX（如「从市场安装」「签名校验失败」）→ STILL POST-P3；
   - ⑥ Package 升级 / 迁移 / 回滚的 UX（如「升级此 Workspace」「迁移旧数据」）→ STILL POST-P3；
   - arbitrary extension / XHS·RD migration 的 UX → 未被 P0 覆盖，不设计。
3. **进化 ≠ 升级**：§2.C 只设计「经营方法进化」用户面，不设计「Package 版本变更」用户面（见 §4）。

**结论**：可以启动 Visual / High-Fidelity Design，产出三条旅程的 CEO 面高保真（结构稿 → 视觉）。但高保真文档须显式标注上述边界，且不得出现 POST-P3 排除项的入口或流程。

---

## 6. 仍待 POST-P3 的项（须新 bounded Issue，不在本批）

| 项 | 状态 | 后续 |
|---|---|---|
| ⑤ 签名 / Marketplace / 第三方信任 | **STILL POST-P3** | 需新 bounded Issue：签名校验 UX、市场安装流、第三方信任呈现 |
| ⑥ 升级 / 迁移 / 回滚 | **STILL POST-P3** | 需新 bounded Issue：Package 升级/迁移/回滚 UX |
| arbitrary extension（任意扩展） | **未覆盖** | P0 明确 remain unimplemented；禁用，待 Issue |
| XHS·RD·TTK migration | **未覆盖** | P0 仅 two bounded integration seams；既有业务逻辑未迁移，待 Issue |

---

## 7. 停止状态

```text
WORKSPACE ENGINEERING TECHNICAL REALITY DELTA REVIEW — COMPLETE
→ GO FOR VISUAL / HIGH-FIDELITY DESIGN (BOUNDED)
```

（本评审为独立 Delta 层，不重做《Product Translation》（仍 APPROVED CANDIDATE）。仅重新核对并打标其 §11 矩阵：① 动态安装未知 Workspace / ② 任意新 Surface 类型（有界）/ ③ 自定义领域对象自动运行（有界）/ ④ Capability 检查（约束匹配）均 **CONFIRMED BY P0**；⑤ 签名·市场·第三方信任 / ⑥ 升级·迁移·回滚仍 **STILL POST-P3**；§11.1 全部 12 项 + ④ 语义为 **PRODUCT DESIGN DECISION**。沿用此前批准的 Capability 激活三分类（Required for Activation / Required for Specific Action / Optional·Enhancement），用户侧仅自然语言。判定：已具备进入 Visual / High-Fidelity Design 的真实技术输入（GO，带声明式能力边界 + POST-P3 排除项）。本评审输出后停止，待进入 Visual Design 阶段。）

---

*Curis Workspace Engineering Technical Reality Delta Review · 2026-08-16（Delta-only · 非重写 Translation · 非高保真 · 非 Runtime）*
