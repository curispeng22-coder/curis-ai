# Curis UI 原型设计评审报告

Status: Deprecated

> 本文是 2026-08-03 的历史 UI 评审快照。它保留问题证据，不覆盖当前 Product Blueprint 4.12、Business Runtime v1.0、冻结 Design System 或最新 UI Evidence Review。

- **评审对象**：`curis-ui-prototype/`（18 个 HTML + `curis-prototype.js`）
- **历史评审基准**：产品蓝图 `docs/01_Product/Curis_Product_Blueprint.html`（当时 v4.3）、UI 蓝图 `docs/03_Design/Curis_Design_System.md`（Frozen）+ `Curis_Visual_Design_System_v1.0.html`、产品推导日志 `docs/01_Product/Curis_Product_Derivation_Journal.md`
- **评审日期**：2026-08-03
- **评审人**：UI Designer

---

## 一、总体结论

**界面结构覆盖度几乎完整（14/14 预期界面 + 4 个 Workspace 运行现场全部落地），但实现层系统性偏离冻结设计系统。**

三处阻断性（P0）问题：

1. **颜色系统完全脱轨**——18 个页面**零采用**注册的 `--ui-*` 令牌，存在两套私有调色板，8 个页面使用被禁止的渐变，并引入未注册的第二 accent 蓝色。
2. **Shell 导航碎片化**——每个页面各自实现侧边栏，冻结规范要求的固定分组（公司 / 经营工具 / 办公室 / 公司资源 / 设置）**没有任何一页完整正确实现**；顶栏高度分裂为 52px 与 62px 两派。
3. **术语污染**——ROI / KPI / Blueprint / Agent / Outcome / Evidence / 下注·赌注 / 回报 等用户可见违禁词大量存在，未按规范本地化为「投入产出 / 工作指标 / 搭建方案 / AI 员工 / 目标结果 / 依据 / 反馈 / 业务方向」。

视觉打磨度高，但对照 Frozen 设计系统属于"另一套设计语言"，尚未成为可交付的产品 UI。

---

## 二、完成了哪些（覆盖度）

| 预期界面（来自推导日志 §28–34） | 对应文件 | 完成度 | 备注 |
|---|---|---|---|
| Founding Flow（欢迎→简报→公司→业务→AI团队→启动检查） | `founding-flow.html` | ~85% | 6 步结构完整，有进入 CEO Desk 出口 |
| CEO Desk / Operating Day | `ceo-desk.html` | ~85% | 含 Brief Header / Assistant Brief / Matters / Timeline / Company Pulse / Handoffs 六段骨架 |
| 经营（公司健康与干预） | `operating.html` | ~80% | matters / 异常 / 机会 / 脉搏齐备 |
| 业务（价值与投资） | `business.html` | ~75% | 业务卡 / 阶段 / 结果时间线 / 投资建议 |
| 公司 / AI 组织 | `ai-organization.html` | ~75% | 员工目录 / 能力矩阵 / 抽屉详情 |
| 工作空间门户 | `workspace-portal.html` | ~70% | 装修/运行/暂停 Workspace 卡，空状态覆盖较好 |
| Workspace Studio | `workspace-studio.html` | ~70% | 画布 / 节点 / 配置检查 / 审批模拟 |
| Workspace 运行现场 ×4 | `workspace-runtime-shortvideo / software / department / xhs.html` | 50–75% | 业务指标差异化（短视频、小红书较好；software/department 偏模板） |
| 决策室（上下文模式） | `decision-room.html` | ~70% | 事实/观点/选项/模拟/结果，状态设计较好 |
| 会议（上下文模式） | `meeting.html` | ~60% | 仅容器，内容由 JS 渲染 |
| 成果库 | `assets.html` | ~30% | style 为空，依赖 JS 注入 |
| 知识库 | `knowledge.html` | ~25% | 近乎占位 |
| 财务 | `finance.html` | ~25% | 近乎占位 |
| 日历 | `calendar.html` | ~25% | 近乎占位 |

**结构覆盖 = 完成。** 蓝图要求的首屏流、五个经营视角、上下文模式、Workspace Studio 与多业务运行现场，在原型中均有对应页面。

---

## 三、未完成 / 系统性偏离（合规缺口）

### P0 — 阻断性

**P0-1 颜色系统脱轨**
- 0/18 页面引用 `--ui-*` 注册令牌（已 grep 确认）。
- 两套私有调色板：
  - **Palette-A**（9 文件：`ceo-desk / operating / business / ai-organization / workspace-portal / workspace-studio / shortvideo / decision-room / founding-flow`）：以 `--bg-base-default:#191a1d`、accent `#32f08c` + 未注册蓝 `#387bff` 为核心。
  - **Palette-B**（7 文件：`meeting / calendar / finance / knowledge / xhs / software / department`）：以 `:root{--bg:#191a1d;--panel:#202226}` 为核心，灰阶数值与 A 不同。
- 8/18 页面使用渐变（**禁止项**）：`ai-organization / business / ceo-desk / decision-room / founding-flow / operating / workspace-portal / workspace-studio`。
- 引入未注册第二 accent 蓝 `#387bff`（Palette-A 全系），违反「一页 = 中性 + 最多一个 accent」。
- 语义色被用作整卡 / 徽章背景（`.pulse-ontrack`、`.stage-opportunity`、`.lifecycle-badge` 等）。
- 共享 JS 注入的 `darkTokens/lightTokens` 也与 Frozen 不符（`#191a1d`≠`#1a1c1f`、`#f7f7f8`≠`#ffffff`、未注册 `--status-primary:#aab6ff` 等）。

**P0-2 Shell 导航碎片化**
- 每个页面独立实现侧边栏，无共享 Shell 组件。
- 冻结要求的固定分组（公司 / 经营工具 / 办公室 / 公司资源 / 设置）**无任何一页完整正确实现**；分组命名混乱（出现「运行」而非「经营工具」、把「员工目录/能力中心」塞进运行组等）。
- 顶栏高度分裂：Palette-A = 52px，Palette-B = 62px（已确认）。
- 边栏宽度 220px 在多数页存在，但 `assets / knowledge / finance / calendar / meeting` 等 Palette-B 页的导航项、分组、active 状态各自为政。

**P0-3 术语污染**（用户可见违禁词，已 grep 确认分布）
| 违禁词 | 出现页面数 | 应改为 |
|---|---|---|
| ROI | 8 页 | 投入产出 |
| Blueprint | 5 页 | 搭建方案 |
| Outcome | 5 页 | 目标结果 |
| 回报 | 5 页 | 反馈 |
| Agent | 4 页 | AI 员工 |
| Evidence | 4 页 | 依据 / 记录 |
| 下注 / 赌注 | 2 页 | 业务方向 / 经营选择 |
| KPI | 1 页 | 工作指标 |

同一概念全站未统一中文叫法，违反「英文只作内部对象名，用户操作词必须中文」。

### P1 — 高优先

**P1-1 主按钮纪律**：违反「每视口最多 1 个主按钮」。计数（primary-ish）：`ai-organization=10`、`workspace-portal=9`、`operating=8`、`decision-room=7`、`ceo-desk=6`、`founding-flow=6`、`workspace-studio=6`、`business=5`、`shortvideo=5`……批量/低频操作未降级到上下文菜单或抽屉。

**P1-2 助手模式不统一**：非 root-level Global Assistant。
- `ceo-desk / operating` 有 390px drawer + 浮动入口（相对最规范）；
- `business / ai-organization / shortvideo` 的 drawer 用于业务/员工/视频详情，**不是 Assistant**；
- `workspace-portal` 把「Assistant 在线」静态塞进边栏——形成**固定 rail**（明确违规）；
- Palette-B 页面全无 Assistant。
- 无真实 loading / failure / blocked 状态（仅静态文案）。

**P1-3 状态与 mock 数据**：
- 空 / 加载 / 错误 / 阻塞 / 未知 / 过期 / 冲突状态几乎缺失（仅 `business` 有过滤空态、`workspace-portal` 有 Workspace 空态）。
- 大量硬编码数字（`¥12,000`、`47 条反馈`、`2 条爆款`…）直接渲染为真实产品状态，**无「模拟数据」标识**。
- 缺失事实未用「未记录 / 未分配」占位。

### P2 — 中优先

**P2-1 排版**：未使用 Inter（实际 SF Pro / PingFang 混合）；页面标题 25–28px（规范 24px/1.15/650），字重/行高偏差；辅助文字偶见 10px。

**P2-2 Workspace 运行现场差异化不足**：`software` 与 `department` 几乎是「标题替换」的同一模板，违反「Workspace 不能只是换标题的 Dashboard」。

**P2-3 主题**：仅暗色实现，无 System / 浅色切换 UI；审计截图显示存在光亮态——与「三种主题模式」要求不一致。

**P2-4 布局违规**：`workspace-studio` 双 `aside`（palette + config）形成四列；`shortvideo` 有 340px 第三列——均违反标准 Shell。

**P2-5 越界文件**：`ceo-day-demo.html` 是独立 API 演示页，第三套私有调色板（`#0f1115`），不属于正式原型，应移出 `curis-ui-prototype/`。

---

## 四、改进建议（执行顺序）

1. **建立单一共享 Shell + 设计令牌**（P0）：抽出 `shell.css` 与 `tokens.css`，强制使用 `--ui-*`；删除所有页面私有 `:root` 调色板与全部渐变；统一顶栏 52px、边栏 220px。
2. **统一导航**（P0）：实现冻结分组与顺序（公司 / 经营工具 / 办公室 / 公司资源 / 设置），全站复用同一 Shell 组件，消除 Palette-A/B 两派。
3. **全局术语审计**（P0）：脚本化替换 ROI→投入产出、KPI→工作指标、Blueprint→搭建方案、Agent→AI 员工、Outcome→目标结果、Evidence→依据/记录、下注/赌注→业务方向、回报→反馈；同一概念全站唯一中文名。
4. **统一 Global Assistant**（P1）：浮动 fab + 390px drawer，root-level，所有页面共享同一入口与状态；移除边栏静态 rail 与冒充 Assistant 的实体详情 drawer；补 loading/failure/blocked 状态。
5. **主按钮收敛**（P1）：每视口 ≤1 个主按钮，其余降频操作进上下文菜单 / 抽屉。
6. **状态与真实性**（P1）：为每个真实表面补 empty/loading/error/blocked/unknown/stale/conflict（含原因+owner+最小解法+next checkpoint）；缺失事实用「未记录/未分配」；所有硬编码数字标为「模拟数据」或接真实 API。
7. **排版统一**（P2）：字体族 Inter / system sans；页面标题统一 24px/1.15/650。
8. **Workspace 差异化**（P2）：software/department 按各自业务重构信息结构与指标，而非标题替换。
9. **主题支持**（P2）：实现 System / 浅色 / 深色三模式 + 切换 UI，对齐审计截图中的光亮态。
10. **清理**（P2）：拆除 studio 双 aside、shortvideo 第三列；移出 `ceo-day-demo.html`。

---

## 五、验证证据摘要

| 检查项 | 结果 |
|---|---|
| 引用 `--ui-*` 令牌的页面 | **0 / 18** |
| 含 gradient 的页面 | **8 / 18**（ceo-desk, operating, business, ai-organization, workspace-portal, workspace-studio, shortvideo, founding-flow） |
| 顶栏高度 | 52px（7 页 Palette-A）/ 62px（7 页 Palette-B） |
| 私有调色板 | Palette-A（9 文件）+ Palette-B（7 文件） |
| 未注册第二 accent | `#387bff` 存在于 Palette-A 全系 |
| 主按钮超标页 | ai-organization(10) / workspace-portal(9) / operating(8) / decision-room(7) / ceo-desk(6) / founding-flow(6) / workspace-studio(6) |
| 术语违禁分布 | ROI×8, Blueprint×5, Outcome×5, 回报×5, Agent×4, Evidence×4, 下注/赌注×2, KPI×1 |

---

## 六、评审判定

- **覆盖度：完成**（预期界面 100% 有对应原型）。
- **设计系统符合度：不符合**（P0 三项阻断，需系统性返工而非局部修补）。
- **可交付状态：未达 Frozen 标准**，当前视为高保真视觉探索稿，不能直接作为产品 UI 验收依据。

**下一步建议**：先完成 P0-1/2/3（令牌 + Shell + 术语）三件事，可一次性消除 80% 的系统性偏离；再按 P1/P2 逐项收敛。返工应以「共享组件 + 强制令牌」为前提，避免继续在各页面私有调色板上打补丁。
