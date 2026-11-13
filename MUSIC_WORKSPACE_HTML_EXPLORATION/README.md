# Music Professional Workspace — 视觉 / 交互 HTML 探索 · Review 材料

> **Status**: `EXPLORATION` / `CANDIDATE`（视觉探索产物，**非 Authority**、非设计终稿、非正式前端）
> **Round**: CURIS — RD + MUSIC VISUAL EXPLORATION（本目录为 **Music 线**，与 RD 线**分开设计 / 分开 HTML / 分开验证**，未套同一模板）
> **Date**: 2026-09-19
> **结构输入（唯一）**: `Curis Business Research/product-translation/shared/RECONCILIATION_INDEX.md` + `music/` 五份文档
> **视觉基线**: `curis-ui-prototype/_system/tokens.css`（Frozen 令牌，暗色为默认）
> **边界**: 未修改 Authority / Blueprint / Runtime / Backend / Database / 正式 Frontend；未 Figma；未 commit / push；**未研究 Browser / Computer Use 技术实现**（仅以状态表达）。

---

## 1. 页面结构说明

### 1.1 四 Pane 外壳

```
┌─ window bar（窗口点 / 面包屑 / MOCK 标记 / 待处理徽标 / 主题切换）─────────┐
├──────────────┬────────────────────────────────┬──────────────────────────┤
│ 全局导航（七区）│ Main（当前 Work Area 内容）      │ 该 Work Area 的局部专业导航 │
│ + 音乐工作区  │                                │ （**按实需命名，非「上下文」**）│
│   局部导航    │                                │                          │
│   （5 区）    │                                │                          │
└──────────────┴────────────────────────────────┴──────────────────────────┘
```

左栏 = Curis 七区（CEO 工作台 / 业务空间 / 组织中心 / 人才与能力 / 经营洞察 / 资料库 / 会议，原样）+ 音乐工作区 5 个长期 Work Area 及其计数。七区中只有「业务空间」可进入本工作区，其余为占位。

### 1.2 五个长期 Work Area 与**各自的局部专业导航**

| # | Work Area | 主面要点 | 局部专业导航（右栏） |
|---|---|---|---|
| ① | **经营** | 经营目标 / 选题策略 / 红线 / Song 管线（研究中·制作中·待发布·已发布）/ Leader 判断 / Needs CEO / Next Cycle | **持续经营看板**：经营健康度 · 九问速览 · 下一步 |
| ② | **研究与方向** | Reference 信息流（58 张封面缩略图）+ 趋势榜单 + 歌曲方向；点参考看 Pattern 拆解 | **研究 · 专业导航**：Reference / 趋势 / 歌曲方向（sub-nav）+ Pattern 画像 · 红线 |
| ③ | **歌曲制作** | Song 头（封面 / 风格 / BPM / 平台）+ 模拟播放器 + 版本工作室（A/B/C）+ A/B 比较 + 制作 Employee 工作台 | **制作 · 专业导航**：Song 队列 · 当前 Song · Versions · 不做什么 |
| ④ | **发布** | Release Package 字段表（Song Name / Audio 母带 / Cover / Lyrics / Artist / Credits·AI 声明 / ISRC / 著作权声明）+ 五态状态机 + Computer Use 发布动作 | **发布 · 专业导航**：Release Package · Release 状态机 · Auth Stop Gate 规则 · Provider 实例 |
| ⑤ | **数据与复盘** | 已发布 Song 表现对比（Plays / 完播 / Saves / Shares / Likes）+ 分析链路 + 形成下一首方向 | **数据 · 专业导航**：已发布 Song · 四模式 Result Intake · 最小指标集 · 分析 Employee |

> **13 页已降级为内部页面/对象**，不再并列一级导航（对齐 `MUSIC_PRODUCT_TRANSLATION §9` 的 13 行逐条去向）。
> **右栏不叫「上下文」**：每个 Work Area 按真实需要命名自己的辅助区（brief §20）。

### 1.3 目录内容

| 文件 | 大小 | 作用 |
|---|---|---|
| `index.html` | 2.2 KB | 开发版骨架 |
| `styles.css` | 23.6 KB | 全部样式（Frozen `--ui-*` 令牌） |
| `tokens.css` | 11.5 KB | Frozen 令牌副本（内联进单文件） |
| `data.js` | 48.9 KB | 全部 Mock 数据（12 Song / 58 Reference / 12 Trend / 8 Learning / 5 Employee / 2 open CEO Decision） |
| `app.js` | 12.7 KB | 外壳、路由、主题、局部导航、轻量提示 |
| `pages.js` | 58.2 KB | 五个 Work Area 的页面渲染与交互 |
| `_build.js` | 2.3 KB | 零依赖打包为单文件 |
| **`Music Workspace.html`** | **156.9 KB** | **单文件版**（由 `_build.js` 生成，**禁止手改**），零外链，双击即用 |
| `_check.js` | 12.6 KB | 真实浏览器点击自测脚本 |
| `_check.log` | 4.2 KB | 自测输出（29 条断言 + Console 记录） |
| `_evidence/*.png` | 16 张 | 逐步截图证据 |
| `README.md` | 本文件 | Review 材料 |

---

## 2. 关键交互说明

| # | 交互 | 行为 |
|---|---|---|
| 1 | **五区路由** | 左栏局部导航切换 5 个 Work Area，Main 与右栏局部专业导航**同时**切换 —— 这是与 RD 线最本质的结构差别（RD 无专业导航）。 |
| 2 | **CEO 决策** | 经营区决策卡 → 批准并执行 / 拒绝 / 提供指示。批准后 `ceoDecisions.status = resolved` 并重渲染；指示走轻量提示回执。 |
| 3 | **Reference** | 点击任一 Reference → 详情（Pattern 拆解：情绪 / Hook / 结构 / BPM）→「形成歌曲方向」→ 在「歌曲方向」sub-nav 生成 Direction 卡。 |
| 4 | **Direction 批准** | Direction 卡 →「批准」→ 转为 Song Proposal 并进入制作区。 |
| 5 | **版本工作室** | Song 卡展开 Version A/B/C：每版标注 Provider（Mureka / ElevenLabs Music）与模型、五维评分条（能量 / 结构 / 响度 / 情绪 / 商业潜力）、逐版动作（试听 / 对比 / 定稿此版 / 驳回）。 |
| 6 | **试听** | 点击「试听」→ **内置 Mock 播放器**：该版本卡内出现进度条与计时（0:00 / 0:30 · 播放中），按钮变「⏸ 暂停」；**再点暂停**；播放 30 秒后自动归位。单实例语义 —— 切到别的版本自动停掉上一个。 |
| 7 | **A/B 比较** | 逐个点「对比」选择两个版本 → A/B 比较面板并排显示五维评分并高亮领先方。 |
| 8 | **驳回 / 定稿** | 驳回 → 该版 `status = rejected` 并写入返工说明；定稿 → `song.approvedMaster = 该版本`、Song `status = ready`，进入发布区。 |
| 9 | **发布状态机** | `Ready → Publishing → Waiting for User → Pending Review → Published` 五态可视化；按钮随状态变化（经 Computer Use 发布 / 继续填写上传 / 前往处理 → 恢复后 Resume / 平台已审核，标记已上线）。 |
| 10 | **Auth Stop Gate** | 遇验证/登录过期 → 页面出现琥珀色条 **「Authentication Stop Gate = WAITING_FOR_USER」**并写明原因；「前往处理」后状态推进（**不绕过验证**，等用户完成后 Resume）。 |
| 11 | **数据下钻** | 数据区点任一已发布 Song → Observation / Evidence / Analysis / Learning / Recommendation。 |
| 12 | **形成下一首方向** | 点「形成下一首方向 →」→ 真的 `directions.unshift(...)` 并跳到研究区的「歌曲方向」——**业务在循环**可见。 |
| 13 | **主题切换** | 暗 / 亮切换，暗色为默认。 |

---

## 3. 与 Product Translation 的对应关系

| 本探索的体现 | 结构来源 |
|---|---|
| **5 个长期 Work Area**（经营 / 研究与方向 / 歌曲制作 / 发布 / 数据与复盘），13 页降级为内部页面 | `RECONCILIATION_INDEX §2.2`；`MUSIC_PRODUCT_TRANSLATION §9 · §13`；`RECONCILIATION_RULINGS §4 **M1**` |
| 三级分层纪律：一级 Work Area / 二级内部页面 / 三级对象·状态不进导航 | `MUSIC_PROFESSIONAL_WORKSPACE_STRUCTURE_CANDIDATE §2` |
| 经营区不是普通 Dashboard：回答「最近怎么样 / 往哪走 / 谁在做 / 什么要你定」 | 同文件 §1（① 经营）；`MUSIC_PRODUCT_TRANSLATION §14 Q2` |
| 研究区有音乐内容感（封面 / 歌手 / 平台 / 热度 / 风格 / 情绪 / Hook / 结构 / BPM），支持趋势 · 热歌 · 榜单 · Reference · Pattern 拆解 | `§14 Q3`；`RECONCILIATION_RULINGS §2` |
| 制作区为专业工作区但**不是 DAW**；核心链 Direction → Brief → Provider → Version A/B/C → 试听·比较·评审 → Approved Master | `§14 Q4–Q7`；`RECONCILIATION_RULINGS §1 不自建清单` |
| Song 不是表格行：封面 / 名称 / 方向 / 风格 / 状态 / 当前版本 / 目标平台 / Employee / Provider + 版本关系 | brief §15 |
| 发布 = Release Package + 汽水音乐第一平台 + 五态（`Ready` / `Publishing` / `Waiting for User` / `Pending Review` / `Published`） | `§14 Q8`；`MUSIC_QISHUI_PUBLISH_AND_RESULT_INTAKE_MODEL` |
| **Auth Stop Gate = 既有 `WAITING_FOR_USER`**，不新造状态名；不绕过 CAPTCHA/MFA/风控 | `RECONCILIATION_RULINGS §3`；G1 §3 |
| 四模式 Result Intake（`API_SYNC` / `COMPUTER_USE` / `IMPORT` / `MANUAL_ENTRY`） | `RECONCILIATION_RULINGS §2` |
| 数据区不止数字：Observation → Evidence → Analysis → Learning → Recommendation，并回到研究循环 | `§14 Q12`；brief §18–§19 |
| Provider（Mureka / ElevenLabs Music / 汽水音乐）显式标注且**不等于员工** | `RECONCILIATION_INDEX §0`；`MUSIC_EMPLOYEE_AND_PROVIDER_EXECUTION_MODEL` |
| B2B Distributor API 在 Provider 实例里标注为「未来 · M2 关闭主路径」 | `RECONCILIATION_RULINGS §4 **M2**` |
| 右栏为**局部专业导航**，不叫「上下文」 | brief §20 |

**明确未做（符合禁令）**：无 Mixer / 音轨编辑器 / EQ / Compressor / Reverb / 波形剪辑 / 时间线 / 音频引擎；未把 Track / Stem / Take / Comp 提升为一级对象；未复制任何真实歌词或旋律。

---

## 4. 本轮主动做出的视觉判断

1. **没有把两线做成同一种 Dashboard（brief §2 的硬要求）**：RD 线是「无专业导航 + Conversation 为主面」，Music 线是「**5 区专业导航 + 每区局部专业导航**」。两者的导航数量、页面骨架、对象模型完全独立，只共享 Curis 外壳语言与 `--ui-*` 令牌。
2. **五区各自命名自己的辅助区**：明确拒绝「上下文」这个泛称 —— 经营叫「持续经营看板」，研究/制作/发布/数据分别叫「… · 专业导航」，且每区内容不同（研究是 Pattern 画像与红线，制作是 Song 队列与 Versions，发布是状态机与 Auth Stop Gate 规则，数据是四模式与最小指标集）。
3. **封面是这一轮的视觉主角**：58 个 Reference + 12 首 Song 全部使用 CSS 渐变 / inline SVG 生成确定性封面（同一 seed 恒等），这是让「音乐产品看起来像音乐产品」的关键手段，也是与 RD 线最直观的差异。
4. **版本评分用条形而非雷达图**：五维评分并排条形便于快速比较与扫描；A/B 面板用表格并高亮领先方，避免图形化过度。
5. **发布状态机做成横向五态进度条**（而非下拉或文字），让「现在卡在哪一步」一眼可见；Auth Stop Gate 用琥珀色内联条，与正常推进区分。
6. **试听做成原型内的 Mock 播放器**（进度 + 计时 + 暂停），**不用浏览器原生对话框** —— 原生 `alert` 既阻塞页面又不符合成熟度要求（详见 §5-1）。
7. **暗色为默认**，亮色可切换；字阶严格取 Frozen 的 7 档，下限 12px。

---

## 5. 暴露出的产品问题（诚实列出）

1. **【本轮修复】原型中残留原生 `alert()` → 会阻塞页面**：初版「试听」与「CEO 提供指示」使用 `alert()`。在真实浏览器里它会中断交互，在自动化验证中直接**永久挂起页面**。已在 `pages.js` 中替换为**(a)** 版本卡内置的 Mock 播放器、**(b)** 全局 `MU.toast()` 轻量提示。**这属于本轮发现并修复的缺陷**，不是设计取舍。
2. **组织模型在 UI 上仍是「一区一员工」，与 §16 的开放组织要求有差距**：数据层 `employees.e1..e5` 各自只带一个 `area` 字段。§16 明确要求不能把「5 Work Area = 5 固定 Employee」做成产品规则，且需支持「制作区有多个 Employee（Lyrics / Production / Cover / QA）」与「一个 Employee 承担多个 Responsibility」。**当前 UI 未表达这两种情况**，属真实缺口。
3. **发布区在途 Release 数量少时信息量偏低**：本轮只有 1 条 `Ready` + 1 条 `Waiting for User`。当没有在途 Release 时，该区的独立存在价值需要重新验证（是否应并入制作区，或在无在途对象时呈现「历史发布」视图）。
4. **发布中途遇 Auth Stop 后的失败路径未建模**：只做了「处理 → Resume → 继续推进」。未表达「再次过期」「用户放弃」「平台最终拒绝（Rejected）」的分支（五态里 `Rejected` 未造样本）。
5. **指标口径未定义**：Plays / 完播率 / Saves / Shares / Likes 有具体数值，但**时间窗、去重规则、平台差异、四模式来源混合时的口径一致性**都没有定义。真实接入前必须先定口径，否则数字不可比。
6. **58 个 Reference 一次性全渲染**：无分页 / 无虚拟滚动 / 无筛选。真实参考库规模（数百以上）会有渲染与检索问题。
7. **「重新生成」缺少 Provider 成本与配额反馈**：`genVersion` 会新增版本并切换 Provider（Mureka ↔ ElevenLabs），但界面没有展示调用次数、成本或配额 —— 而 `MUSIC_PRODUCT_TRANSLATION` 把 Provider 计量列为 Curis 自有 Surface 之一。
8. **一个 Employee 对多个 Work Area 的呈现未验证**：Leader（林岸）只在经营区出现；若 Leader 需要跨区出现（例如在制作区做取舍决策），当前结构不支持。
9. **试听不是真音频**：符合「Curis 不造音频引擎」的边界，但产品上需要明确「标准播放器由 Curis 提供还是由 Provider 提供」这一归属问题。

---

## 6. 哪些只是 Mock

| 项 | 性质 |
|---|---|
| 12 首 Song / 58 个 Reference / 12 条 Trend / 8 条 Learning | 全部虚构；曲名、歌手、平台热度、数据表现均非真实 |
| 全部封面 | CSS 渐变 + inline SVG（按 seed 确定性生成），非真实图片 |
| 试听播放 | **纯前端定时器模拟**，无音频文件、无音频引擎 |
| Provider 生成（Mureka / ElevenLabs / 版本生成） | 本地同步函数模拟，**未调用任何真实 Provider 接口** |
| 发布流程 / Computer Use 发布 | **只表达状态，不做任何浏览器自动化**；`Ready→…→Published` 由本地状态机推进 |
| Auth Stop Gate | 状态与文案 Mock；未连接任何真实平台登录态 |
| 数据区指标（Plays / 完播 / Saves …） | 静态 Mock 数值，非真实平台数据 |
| Analytics 的 Observation/Evidence/Analysis/Learning | 预置文本，非模型推理 |
| 七区中的其余六区 | 占位页（提示「本轮只探索 AI 音乐经营工作区」） |
| 无后端、无网络 | 零请求、零持久化；刷新即回初始状态 |

---

## 7. 哪些需要 CEO Review

| # | 待裁事项 | 为什么需要 CEO |
|---|---|---|
| C1 | **5 区长期形态是否就此确认**（尤其「发布」区在无在途 Release 时是否仍独立） | M1 已裁定 5 区门槛成立，但本轮 HTML 补充了「发布区依赖在途对象」这一观察 |
| C2 | **组织开放度（§16）的落地方式**：制作区多员工（Lyrics / Production / Cover / QA）与一员工多责任，何时进入 UI | 涉及组织模型与 Employee 页面形态，不能由设计层自行决定 |
| C3 | **指标口径与数据可信度**：时间窗、去重、平台差异、四模式混用时的可比性 | 进入实现即为产品承诺 |
| C4 | **Provider 计量 / 成本 / 配额是否需要在工作区内可见** | 与 RD 线同源的跨业务问题，建议一次性裁定 |
| C5 | **试听播放器的归属**（Curis 提供标准播放器 vs 跳转 Provider） | 影响「Curis 不造音频引擎」边界的解释 |
| C6 | **发布失败分支**（再次过期 / 用户放弃 / 平台 Rejected）是否需要完整状态与话术 | 影响发布闭环的完整性 |
| C7 | **B2B Distributor（M2 已关闭主路径）** 在 UI 中保留「未来」提示是否合适 | 避免给用户造成「即将可用」的预期 |

---

## 8. 自测路径与结果

**执行方式**：`puppeteer-core` + 系统 Google Chrome（`--headless=new --no-sandbox --no-proxy-server`），以 `file://` 加载**单文件版**，**全部通过真实点击与键盘输入**驱动，逐步截图存证；并挂 `dialog` 监听器作为「禁止原生对话框」的硬性检查。

**执行命令**
```bash
cd "MUSIC_WORKSPACE_HTML_EXPLORATION"
NODE_PATH=/Users/yy/.workbuddy/binaries/node/workspace/node_modules \
/Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _check.js
```

**执行链路**（对应 brief §19 完整闭环）
经营（目标/策略/管线/Needs CEO）→ 研究与方向（Reference 信息流）→ 点 Reference 看 Pattern → 形成 Song Direction → 歌曲制作（Song + 版本）→ 选多版本 Song → 试听（Mock 播放器）→ A/B 对比 → 驳回 → 定稿 → Approved Master = `v-4b` → 发布（Release Package）→ Auth Stop Gate「前往处理」→ 状态机推进至 `Published` → 数据与复盘（多首已发布 Song 表现）→ 下钻单首看 Learning → **形成下一首方向**（`directions` 增加，跳回研究区）。

**结果**

| 指标 | 值 |
|---|---|
| 断言通过 | **29 / 29** |
| **Console Error** | **0**（含 `pageerror` / `requestfailed` / 原生 dialog 检测） |
| 截图证据 | 16 张（`_evidence/`） |
| 关键观测 | A/B 对比 `{a: v-4a, b: v-4b}`；定稿 `approvedMaster = v-4b`；Auth Stop 处理后 `song-08 release.state: auth_stop → publishing`；发布状态机产出 `published`；「形成下一首方向」→ `songs 12 → 12 · directions = 5`（新方向生成并跳转研究区） |

**已知验证边界**：本轮验证的是**单文件离线版**；开发分文件版（`index.html`）未单独跑自测；未做多分辨率（仅 1680×1050）与键盘遍历测试。

---

> 本目录为**视觉探索产物**，不是 Current Product Truth，也不是第二套 Blueprint / Master Map / UI Blueprint。
> 任何被接受的结论须由正式流程（Blueprint → Design → Code）吸收后方为有效。
