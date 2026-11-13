# Curis 完整产品 UI 覆盖探索 · 质量评审报告（Critique Review）

**评审对象**：`coverage-exploration-2026-08-17/` 下 12 个高保真 HTML 原型
（index / 01–11）+ 支撑文档（00-PAGE-STATE-INVENTORY / 01-DESIGN-TOKENS / 03-DELIVERY）
**评审性质**：Coverage First / Visual Exploration（非最终 Production Visual，非 Frozen Authority）
**权威基准**：
- `_system/tokens.css`（Frozen `--ui-*` 令牌，已通读 273 行）
- `_system/shell.css`（Frozen Shell 组件）
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（Frozen Shell Contract + P1–P7 + Delta-X9/X10/X12）
- `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md`（Frozen 视觉令牌）
- `docs/01_Product/Curis_Product_UI_Blueprint_v1.0.html`（UI Blueprint 六区）
**评审方式**：逐文件通读 HTML，对照权威文档核验（A–J + 设计令牌 + 结构 + 布局 + Anti-Slop），全部结论附 `file:line` 证据。**未修改任何 HTML 文件。**

---

## 1. 总评结论（Summary Verdict）

本次覆盖探索整体 **PASS**，可进入后续 Figma 最终视觉重建的输入池。12 个页面全部采用 Frozen `tokens.css` + `shell.css`，并以自定义类名（`.ws` / `.pane` / `.pane-header` / `.nav-item` / `.nav-zones` / `.emp-row`）镜像 Frozen Shell 的四独立 Pane、六区导航、Pane-local Header 与 T1/T2/T3 行为语义；所有颜色/间距/圆角/字号引用 `--ui-*`，未发现 `#387bff`、`terra-*` 等历史违规私有色，也未出现 `rgb()` 或内联 `style` 私有 hex 泄漏。结构完整度、权威合规（A–J）与 Anti-Slop（安静、信息密集、克制卡片/胶囊）均达标。需修复的多为 **P1 级轻微问题**（角色色头像私有 hex、2 个页面用「（示例）」而非 Frozen `.mock-badge`、Employee UI Status 投影超出 Frozen 三态等），均不阻断交付。特别注意：清单自审声称的「nav-zone 2x/文件」是**误报**——真实类名为 `nav-zones`（容器，CSS+标记各 1 次）+ 每区一个 `.nav-item`，通读导航 HTML 确认 12 文件**均正确渲染六区**。

---

## 2. 五维评分卡（Five-dimension Scorecard）

| 维度 | 评分 | 说明 |
|------|:----:|------|
| 1. 设计令牌合规（Design-token compliance） | **4/5** | 颜色/间距/圆角/字号几乎全部 `var(--ui-*)`；余量问题为角色色头像私有 hex（`.av-1..6`）、`#0c0c0d` 字面量（应 `var(--ui-action-primary-fg)`）、08 代码高亮私有 hex（待 `--ui-syntax-*` 令牌，B 阶段）。无 `#387bff`/`terra-*`/`#181a1d` 泄漏。 |
| 2. 结构完整度（Structure completeness） | **4/5** | 12 文件均含四 Pane + Pane Header + 六区导航 + `.mock-badge`（多数）。扣分项：04-talent-market / 07-settings 用内联「（示例）」而非 Frozen `.mock-badge`；05-library / 06-meeting 无 demo 数据（可接受，无需徽标）。 |
| 3. 权威合规 A–J（Authority compliance） | **4/5** | A–E、G–J 结构性检查全部 PASS；唯一 Authority 瑕疵是 Employee UI Status 投影出现 Frozen 三态之外的 `等待`/`等待用户`（见 §3-E 与 §6）。其余完全贴合 Shell Contract 与 Delta-X9/X10/X12。 |
| 4. 布局合理性（Layout reasonableness） | **4/5** | 一致的 `.ws` 网格（Nav 固定列 + Main 弹性满宽，Context/Utility 默认收起）、合理信息密度、暗色可读性良好。轻微：头像 36px（Frozen 写 32px）；少量内联 `style` 用于局部微调。 |
| 5. Anti-Slop | **5/5** | 安静、信息密集、低表面复杂度，克制 Card/Pill，无 AI 套话/占位废话，贴合「旧 Figma RD 原型」视觉方向。 |

**综合**：无 P0；P1 轻微、可后续统一收敛。建议作为 Figma 最终视觉重建的可信输入。

---

## 3. 权威合规 A–J 检查（Authority Compliance）

> 注：任务清单列 A–E、G–J（无 F）。以下逐条核验，证据为 `file:line`。

| 检查 | 结果 | 证据 |
|------|:----:|------|
| **(A) 无全局 Topbar（Global Topbar 横跨）** | ✅ PASS | 全 12 文件 `*.html` 均**不含 `topbar` 字符串**；每 Pane 独立 `.pane-header`（如 01-ceo-desk.html:129/162/186；11-states.html:108/139/—/—）。符合 §1.5.1「四 Pane 各自 Pane Header，不采用 Global Topbar」。 |
| **(B) 四 Pane 顶部齐平、独立列** | ✅ PASS | `.ws` 为 `grid-template-columns: var(--ui-sidebar-w) minmax(0,1fr)`（01-ceo-desk.html:20），Nav/Context/Main/Utility 各为 `.pane` 独立列、各自 `.pane-header` 居列顶；四 Pane 在每个文件均出现 4 次（grep `class="pane pane-*"`：12 文件各计 4）。 |
| **(C) 六区导航固定且一致** | ✅ PASS | 12 文件导航均为：①首页/CEO工作台 ②业务空间（含子项 研发办公室、小红书运营办公室）③组织中心 ④人才市场 ⑤资料库 ⑥会议 + 底部 设置/帮助与反馈（01-ceo-desk.html:139–155；11-states.html:118–135）。顺序、图标、active 态跨文件一致。业务空间以 `nav-children` 承载 Workspace 子项（§1.3 合规：子项非第七一级区）。 |
| **(D) Main = Domain Business Surface + Shared Work Area** | ✅ PASS | 各页面 Main 含「业务展示区」+「工作区」：01=A1–A6 简报/运行/复盘 + emp-row 工作区；08=H1 Domain Business Surface + H2 多 Employee Workstation；09=I1 总览/日历/内容/数据/自动化 + I2 Presence 工作区；02=B1 业务总览 + B2 详情。符合 Delta-X9「Main = Domain Business Surface + 工作区」。 |
| **(E) Employee Row 两行结构** | ✅ PASS（轻微注记） | 真实类名为 `.emp-row` / `.emp-row-head`（grep `employee-row`=0 是因为类名不同，非缺失）。结构：`.emp-row-head` 为 `grid-template-columns: 36px 1fr auto auto; grid-template-rows: auto auto`（08-rd-workspace.html:78）；头像 `grid-row:1/3`（跨两行）、行1 姓名+岗位（`.emp-id`）、行2 当前职责（`.emp-duty`）、状态（`.emp-status` col3 跨两行）、展开箭头（`.emp-chevron` col4 跨两行）——与 §3.1 两行结构一致。轻微：头像 36px（Frozen 写 32px）。另见 §6 投影三态注记。 |
| **(G) Shared Composer Shell 语义槽位** | ✅ PASS | 08-rd-workspace.html:268–272 完整呈现：Input（`textarea.composer-input`）+ `+ 添加`（Add）+ `访问权限 ▾` + `工作模式 ▾` + `执行 · Codex ▾`（Execution Selector，正确区分 **Agent=Codex**，未降级为模型）+ `发送`。符合 §3.5 语义槽位冻结。 |
| **(H) Result Reference 轻量 → Utility** | ✅ PASS | `.result-ref` 用 `var(--ui-accent)`、带 `▸`、点击 `data-open-utility` 开右侧 Utility（08-rd-workspace.html:257/266；09-xhs-workspace.html:273）。对话内仅引用行、不铺完整 Diff/数据，符合 §3.4。 |
| **(I) Runtime State ≠ UI 展开** | ✅ PASS | `.emp-row.is-open` 由点击 `emp-row-head` 切换（08-rd-workspace.html:354–358），与 `emp-status`（工作中/空闲/等待）**解耦**；收起不改 Runtime。符合 Delta-X10「展开收起只改 UI 不改 Runtime」。 |
| **(J) 未新造 Runtime Primitive** | ✅ PASS | 全文件未发现 `blocked`/`offline`/`unavailable` 作为 Employee Runtime 状态。Employee 状态仅用 `working/waiting/idle` 投影（空闲/工作中·/等待）。11-states.html 的「离线 Offline」是**连接性 UI 状态**（标题「离线 / 未知 Offline」，11-states.html:299），非 Employee Runtime Primitive；但建议确认其命名不与 Δ-X10 禁止清单混淆（见 §6）。 |

**小结**：A–J 结构性全部 PASS。唯一 Authority 级瑕疵为 Employee UI Status 投影集超出 Frozen 三态（§6 详述），属 P1。

---

## 4. 逐页发现（Per-page Findings）

- **index.html**：统一入口/页面目录，导航六区 + 各页面卡片索引。四 Pane、`.mock-badge`（2 处）、角色色头像 hex 同全站一致。结构稳定，可作为目录基准。**结论：稳定。**
- **01-ceo-desk.html（A 首页/CEO工作台）**：覆盖 A1 简报/A2 待决定(Decision Banner)/A3 当前运行/A4 结果复盘/A5 首次创建/A6 空态，含 emp-row 工作区。Decision Banner 用 `--ui-warning` 边框 + 三按钮，符合 P7。角色色 `.av-*` 私有 hex（:94）。**结论：稳定。**
- **02-business-space.html（B 业务空间）**：B1 总览/B2 详情/B3 搭建预览/B4 空间工程部/B5 新建业务。`.mock-badge` 1 处。**DESIGN GAP**：业务空间 ↔ 组织中心 ↔ Workspace 搭建的边界（B3/B5）产品定义仍模糊，建议优先评审（见 §5b）。**结论：基本稳定，需定义澄清。**
- **03-org-center.html（C 组织中心）**：C1 总览/C2 部门/C3 员工列表(Employee Row→Utility)/C4 能力/C5 招聘。emp-row 两行结构正确（:235/258/268）。角色色 hex。**结论：稳定。**
- **04-talent-market.html（D 人才市场）**：D1 首页/D2 专家详情/D3 招募/D4 Skill·Connector/D5 已安装。**问题**：用内联「（示例）」而非 Frozen `.mock-badge`（:230/233）；市场/专家/技能/连接器模型与「组织中心员工」关系存在产品定义歧义。**结论：建议优先评审（§5b）。**
- **05-library.html（E 资料库）**：E1 首页(Context 默认展开)/E2 阅读/E3 搜索/E4 外部连接/E5 空态。无 demo 数据故无 `.mock-badge`（可接受）。Connector 状态用 `status` 正确。**结论：稳定。**
- **06-meeting.html（F 会议）**：F1 首页/F2 创建/F3 中央 Conversation 工作面/F4 Proposal/Decision。四 Pane 完整、六区导航一致。会议工作面对齐「讨论/证据/Decision」方向无明显冲突；建议复查 Proposal→Decision 与 P7 八要素语义贴合度。**结论：稳定，建议复查 Decision 表达。**
- **07-settings.html（G 设置）**：G1–G6 六大子区，从用户菜单进入（非一级导航，符合 §1.3）。**问题**：内联「（示例）」替代 `.mock-badge`（:181/193/239）；G1–G6 面过宽、产品定义最不确定，建议优先评审（§5b）。**结论：建议优先评审。**
- **08-rd-workspace.html（H RD 办公室）**：完成度最高——H1 Domain Surface + H2 多 Workstation（Conversation + Composer 槽位齐全）+ H3 文件树 + H4 Code/Diff/Preview + H5 Needs CEO Banner。`.result-ref`（:257/266）、Composer 槽位（:268–272）均 Frozen 合规。唯一瑕疵：代码高亮私有 hex（`.syn-kw/str/fn`，:111，待 `--ui-syntax-*` 令牌，B 阶段 DESIGN GAP）。**结论：稳定（标杆页）。**
- **09-xhs-workspace.html（I 小红书运营办公室）**：I1 总览/I2 Presence 工作区/I3 Context 选题库/I4 Utility 图文·数据·审核/I5 发布后 Analytics(System Activity)。Employee Presence（P2）与 System Activity（P3）区分清晰（:201/206/211），`.av-*` 角色色 + `#0c0c0d` 字面量（:100）。**结论：稳定。**
- **10-global-search.html（J 全局对象搜索）**：J1 入口（空查询=Recent）/J2 结果（按对象类型分组，点击直达）。作为 Search Surface 实现，符合 §1.5.4（Object-first, Task-capable，非 Task 历史）。`.mock-badge` 2 处。**结论：稳定。**
- **11-states.html（K 重要状态集）**：覆盖 Empty/Loading/Failure/Needs CEO/Permission/First-use/Offline/Success 八状态，复用 Shared Pattern（empty/error/skeleton/decision/composer/conversation）。`.mock-badge` 6 处（最完整）。「Offline」为连接性 UI 状态（:299），非 Employee Runtime Primitive。**结论：稳定（状态参考基准）。**

---

## 5. 稳定性判断（Stability Judgment）

### 5a. 稳定、可进入后续 Figma 最终视觉重建的页面
（结构清晰、权威合规、定义确定度高）

1. **index.html** — 目录基准，零歧义。
2. **01-ceo-desk.html** — 覆盖 A1–A6 完整，Decision/空态/运行均 Frozen 对齐。
3. **02-business-space.html** — 业务总览/详情结构稳（仅 B3/B5 定义待澄清，不影响视觉重建）。
4. **03-org-center.html** — 组织/部门/员工列表 Employee Row 两行结构正确。
5. **05-library.html** — 资料库各态稳定，无 demo 数据依赖。
6. **06-meeting.html** — 会议工作面方向明确（仅 Decision 表达待复查）。
7. **08-rd-workspace.html** — **标杆页**，Composer/Result Ref/Employee Workstation 全部 Frozen 对齐。
8. **09-xhs-workspace.html** — Presence/System Activity 区分清晰，可作为第二个 Adaptive Surface 实例范本。
9. **10-global-search.html** — Search Surface 语义正确。
10. **11-states.html** — 八状态参考集，复用 Shared Pattern，徽标最完整。

### 5b. 建议明日优先评审的页面（产品定义歧义 / DESIGN GAP 依赖 / 结构信心最弱）

1. **04-talent-market.html** — **产品定义歧义**：专家/技能/连接器市场模型，与「组织中心员工」「AI Employee」的关系未定；且 `.mock-badge` 约定未遵循（内联「（示例）」）。优先澄清市场语义再定稿视觉。
2. **07-settings.html** — **产品定义歧义最重**：G1–G6 六大子区、作为用户菜单入口的大面，多处定义未收敛；`.mock-badge` 约定未遵循。建议先收敛设置信息架构。
3. **02-business-space.html** — **DESIGN GAP**：业务空间 ↔ 组织中心 ↔ Workspace 搭建（B3/B5）边界与「空间工程部」职责需权威裁定，否则视觉重建会固化错误层级。
4. **06-meeting.html** — **结构信心次弱**：Proposal→Decision 流程与 P7「八要素 + 分层证据 + Provenance」的贴合度需复查，避免把 Decision 表达成普通表单。
5. **（跨页）Employee UI Status 投影一致性** — **权威对齐**：`等待`/`等待用户`（09-xhs:248、08-rd:283、03-org:268）超出 Frozen 三态（空闲/工作中·/阻塞·），需与 Δ-X10 三态投影规则统一，否则各页状态语言不一致。

---

## 6. 关键问题（Critical Issues）

**无 P0。** 下列为 P1（轻微、不阻断本次 Coverage 探索交付，建议交付后统一收敛）：

1. **角色色头像私有 hex（6 文件）**：`.av-1..6`（`#4a6fa5/#5b8c6e/#9a7b4e/#7a5b8c/#a05b6b/#4e8c8c`）为页面私有色板，未进入 Frozen。Shell Contract §3.1 允许角色色作区分但要求配非颜色指示（头像内已有姓名首字，满足），故非 accent 违规；建议后续将角色色收敛为 Frozen `--ui-role-*` 令牌。影响：01:94、02:88、03:87、08:88、09:87、index:136。
2. **`#0c0c0d` 字面量**（应 `var(--ui-action-primary-fg)`）：01:86、03:79、08:80、09:79/100、index:126。值恰等于令牌，属字面量冗余，非视觉偏差。
3. **`.mock-badge` 约定未遵循**（04-talent-market、07-settings）：用内联「（示例）」文本替代 Frozen `.mock-badge` 徽标（04:230/233；07:181/193/239）。05-library、06-meeting 无 demo 数据，无需徽标（可接受）。建议 04/07 改用 `.mock-badge` 以统一「示例数据」信号。
4. **Employee UI Status 投影超 Frozen 三态**：出现 `等待`/`等待用户`，超出 Δ-X10 固定的 `空闲`/`工作中·<描述>`/`阻塞·<原因>` 三态。属投影纪律轻微偏离，需与权威对齐（见 §5b-5）。
5. **代码高亮私有 hex（08-rd-workspace.html:111）**：`.syn-kw #c98a5e`/`.syn-str #7fae6b`/`.syn-fn #6f9fd8` 为私有色。Shell Contract §2.3 已注明 `--ui-syntax-*` 子令牌「B 阶段定」，故为已知 **DESIGN GAP**，待 syntax 令牌 Frozen 后替换。
6. **「Offline」状态命名（11-states.html:299）**：属连接性 UI 状态，非 Employee Runtime Primitive；建议确认其命名不与 Δ-X10 禁止新增 `offline` Runtime Primitive 清单混淆（当前为 UI 状态，合规，仅命名提醒）。

> 说明（回应任务特别提示）：`--ui-utility-bg` 在 `tokens.css` 中**未定义**（已通读 273 行确认）；但全部 `*.html` 经 grep **零次引用** `--ui-utility-bg`，故「`var(--ui-utility-bg,#181a1d)` 兜底泄漏私有 hex」的风险**未在本次评审的 HTML 中实际发生**。Utility Pane 实际用 `var(--ui-surface-2)`（shell.css `.pane-utility`），暗色更深背景 `#181a1d` 仅作为 Shell Contract §2.3 文档中的「专注模式」说明值，未硬编码进 HTML。

---

**评审人**：critique-reviewer（general-purpose-1）
**评审日期**：2026-08-17
**范围**：只读评审，未修改任何 HTML / CSS 文件。
