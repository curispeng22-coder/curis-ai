# Curis Complete Product UI Coverage — 明早统一交付（10 项）

> 生成：2026-08-17 · 主理人统筹汇总
> 性质：**Coverage First / Visual Exploration** —— 非最终 Production Visual，非 Frozen Authority
> 交付包：`curis-ui-prototype/coverage-exploration-2026-08-17/`（12 HTML + 4 文档 + zip）

---

## 1. Complete Product Page/State Inventory（页面/状态清单）
文件：`00-PAGE-STATE-INVENTORY.md`
- 11 个一级区（A–K）+ 每区多状态（Normal/Empty/Loading/Error/Needs CEO…）。
- A 首页/CEO工作台、B 业务空间、C 组织中心、D 人才市场、E 资料库、F 会议、G 设置、H RD Workspace、I Content Growth/XHS、J 全局搜索、K 重要状态集。
- 覆盖原则：不新建 Blueprint 外系统；Shared Pattern 直接复用；Domain Business Surface 是探索重点；状态必须存在；视觉安静信息密集。

## 2. 完整可浏览高保真原型
- 12 个 HTML：`index.html`（统一入口/目录）+ `01-ceo-desk` … `11-states`。
- 全部引用 `../_system/tokens.css` + `shell.css`，四 Pane 结构，内联六区导航，带 `.mock-badge`。
- 配套：`03-DELIVERY.md`（交付说明）、`coverage-exploration-2026-08-17.zip`（开箱即看）。

## 3. 页面覆盖率
- **Blueprint 六一级区（首页/CEO工作台、业务空间、组织中心、人才市场、资料库、会议）= 100% 覆盖**。
- 额外覆盖：设置（用户菜单）、RD Workspace、Content Growth/XHS Workspace、全局对象搜索、跨页状态集。
- **未新建 Blueprint 外系统**；抖音/TikTok Workspace 仅作占位标记（见 #8 GAP）。

## 4. 每个一级产品区的关键页面
| 一级区 | 关键页面 | 覆盖要点 |
|--------|---------|---------|
| A 首页/CEO工作台 | `01-ceo-desk.html` | 简报/待决定(Decision Banner)/运行/复盘/首次创建/空态 |
| B 业务空间 | `02-business-space.html` | 总览/详情/搭建预览/Workspace Engineering/新建 |
| C 组织中心 | `03-org-center.html` | 三视图/部门/员工列表(Employee Row)/能力/招聘 |
| D 人才市场 | `04-talent-market.html` | 专家·技能·连接器/详情/招募/已安装 |
| E 资料库 | `05-library.html` | 首页/阅读/搜索/外部连接/空态 |
| F 会议 | `06-meeting.html` | 首页/创建/中央 Conversation/Proposal·Decision |
| G 设置 | `07-settings.html` | 个人/公司/AI能力/权限数据/运行成本（用户菜单） |
| H RD Workspace | `08-rd-workspace.html` | 标杆页：Domain Surface/多 Workstation/Code·Diff·Preview/Needs CEO |
| I Content Growth/XHS | `09-xhs-workspace.html` | 总览/日历·内容·数据·自动化/Presence/System Activity |
| J 全局能力 | `10-global-search.html` | 空查询=Recent/按对象类型分组/点击直达 |
| K 状态集 | `11-states.html` | Empty/Loading/Failure/Needs CEO/Permission/First-use/Offline/Success |

## 5. Shared Pattern 复用情况
（详见 `00` 矩阵 + `02` §3 A–J）
- 四 Pane Shell + Pane Header：**12/12 文件**
- 六区导航（一致顺序/active）：**12/12**
- Employee Row（`.emp-row` 两行结构）：CEO/RD/XHS/组织中心（多文件）
- Decision Banner（`.decision-banner` + 三按钮）：**5 文件**
- Shared Composer Shell（语义槽位）：**7 文件**
- Result Reference（→ Utility）：**10–11 文件**
- Context/Utility Surface、Conversation（不 Card 化/有界块）、Employee Detail、Employee Presence、System Activity 均按 Frozen Shell Contract 复用，未重新解释。

## 6. 新发现、可固定为 Shared Pattern 的候选
1. **导航子项渲染规范**：Workspace 实例（如「小红书运营办公室」）在 Primary Nav 的呈现（缩进/图标/active/owner 头像）—— 本轮用 `nav-children` 建立示例，Shell §6 Open Q#7 尚未冻结，建议定型。
2. **Utility 语法高亮令牌 `--ui-syntax-*`**：RD 代码/Diff 高亮需求明确，当前用临时私有 hex，建议 B 阶段 Frozen 子令牌。
3. **角色色头像令牌 `--ui-role-*`**：6 个角色色（`.av-1..6`）当前为页面私有 hex，建议收敛为 Frozen 角色色令牌（须配非颜色指示，已满足）。
4. **Mobile Adaptive Surface（<640px Overlay）交互规范**：产品未实例化，建议定型。
5. **Workspace Studio 视觉（当前运行版本 vs 待修改版本）**：Blueprint 有语义无像素，建议定型。
6. **Employee UI Status 投影三态纪律**：Frozen `空闲 / 工作中·<描述> / 阻塞·<原因>`，需与 Δ-X10 对齐，禁止 `等待/等待用户` 等变体（见 #9）。

## 7. DESIGN GAP（发现后记录，未自行改 Frozen）
1. Navigation 子项渲染（Shell §6 Open Q#7）。
2. Utility Syntax Tokens 未冻结（代码高亮临时色）。
3. Mobile Adaptive Surface 未实例化。
4. Workspace Studio 视觉（版本对比）无像素规范。

## 8. PRODUCT DEFINITION GAP（标记但不脑补）
1. **抖音/TikTok Workspace**：Blueprint 有结构无专项 Design Brief，本轮仅轻量占位。
2. **财务/日历/成果库**：旧 Spec 有页面，Blueprint 5.1 未明确为一级入口，按「设置/资料库子能力」处理。
3. **具体 Provider 适配**（Codex/Claude Code/Coze 等原生交互）：Composer 用通用占位。
4. **Agent Computer Access 运行时 UI**：ADR-0046 冻结权限语义，但设置/请求界面未单独定义。

## 9. 建议明天重点 Review 的页面
（来自 `02-QUALITY-REVIEW.md` §5b，产品定义歧义 / DESIGN GAP 依赖 / 结构信心最弱）
1. **`04-talent-market.html`** —— 市场模型与「组织中心员工/AI Employee」关系未定；`.mock-badge` 未遵循。
2. **`07-settings.html`** —— G1–G6 定义最不确定；`.mock-badge` 未遵循。
3. **`02-business-space.html`** —— 业务空间 ↔ 组织中心 ↔ Workspace 搭建边界 + 「空间工程部」职责需权威裁定。
4. **`06-meeting.html`** —— Proposal→Decision 与 P7 八要素/Provenance 贴合度需复查。
5. **（跨页）Employee UI Status 投影一致性** —— `等待/等待用户` 超出 Frozen 三态，需统一。

## 10. 已稳定、可直接进入未来 Figma 最终视觉重制的页面
（来自 `02` §5a；整体评审 PASS，无 P0）
1. `index.html` 2. `01-ceo-desk.html` 3. `02-business-space.html` 4. `03-org-center.html` 5. `05-library.html` 6. `06-meeting.html` 7. `08-rd-workspace.html`（标杆页） 8. `09-xhs-workspace.html` 9. `10-global-search.html` 10. `11-states.html`
> `04`/`07` 因定义歧义留待 #9 优先评审后再进 Figma。

---

## 质量结论（来自 `02-QUALITY-REVIEW.md`）
- 五维评分：令牌合规 4/5、结构 4/5、权威 A–J 4/5、布局 4/5、Anti-Slop 5/5。
- **无 P0**；6 条 P1 轻微项（角色色私有 hex、`#0c0c0d` 字面量、04/07 缺 `.mock-badge`、Employee 状态超三态、代码高亮私有 hex、Offline 命名提醒），均不阻断交付。
- **本轮额外修复**：Utility Pane 原 `var(--ui-utility-bg, #181a1d)` 兜底私有 hex 已全部替换为 `var(--ui-surface-2)`（12 文件），消除私有色泄漏，符合 `01-DESIGN-TOKENS.md` HARD PROHIBITION #2。

## 约束声明
- 未改任何产品代码、未改 Frozen Authority（tokens.css / Shell Contract / UI Blueprint / Frozen Spec 全程只读）。
- 标注为 Coverage Exploration，非 Production Visual / 非 Frozen Authority。

*主理人汇总 · 2026-08-17*
