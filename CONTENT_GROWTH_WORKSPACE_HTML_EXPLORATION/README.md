# Content Growth Professional Workspace — 高保真交互探索（HIGH FIDELITY PRODUCT EXPLORATION）


## 当前整合版 · 2026-09-20

Authority Class: EVIDENCE / PROTOTYPE
Status: Review
Disposition: COMPLETE — READY FOR CEO REVIEW；仅原型整合，非正式Runtime验收。

当前完整工作台：[index.html](index.html)；同源单文件：[Content Growth Workspace.html](Content%20Growth%20Workspace.html)。本地预览：http://127.0.0.1:8777/index.html 。独立W202探索保留为历史评审输入，当前完整工作台统一使用production-work.js的方法驱动详情。

七区、六账号保留；V2制作/改版/QA接入发布→观测→复盘→Learning→Leader确认→策略→下一选题。主链与图文/文章/混剪实际浏览器验证；57项状态检查通过，所查两标签Console Error为0。真实模型、发布、平台数据与持续调度未接入，Mock刷新重置。

- [整合审计与结果](CONTENT_GROWTH_FULL_WORKSPACE_RECONCILIATION.md)
- [运行问题与范围](CONTENT_GROWTH_FULL_WORKSPACE_RUNTIME_FINDINGS.md)
- [35张截图索引](CONTENT_GROWTH_FULL_WORKSPACE_CEO_REVIEW/CEO_REVIEW_SCREENSHOT_INDEX.md)
- 重建：`node _build.js`；最小检查：`node _check-reconciliation.cjs`。

以下保留各历史轮次记录；旧轮次Current或完成表述仅指当时范围，不覆盖本节。


Status: Exploration / For CEO Review — **不是** UI Authority，不修改任何 Frozen / Blueprint / Master Map / UI Blueprint / Shared Authority / Domain Authority / Shell / Visual Standard / 正式 Authority。
Latest: 第 5 轮「定向修订」（见 §二）已完成并实际打开两版 HTTP 页面逐项验收（分文件版 PASS 135 / FAIL 0；单文件版 PASS 130 / FAIL 0）。
唯一主要输入：`docs/research/newmedia-workspace-reference-2026-09-16/` 下的候选合同与评审文档（见 §二）
Date: 2026-09-16 · Mock 数据 · 无后端 · 无真实 API 调用
本轮输入：`CURIS_CONTENT_GROWTH_HTML_REVISION_INSTRUCTION.md` + 4 份候选合同 / 评审文档

> **Authority 声明**：候选合同（Candidate）是本轮原型的**输入**，不是 Current Authority；本目录内全部产物是 `PROTOTYPE MOCK`，不代表任何 Runtime 能力已交付。

---

## 一、如何打开

**方式 A（推荐，最简单）：双击单文件版本**
```
Content Growth Workspace.html
```
全部 CSS / JS / Mock 数据已内联，双击即用，不需要服务器、不需要联网、可离线、可随意拷贝给别人。

**方式 B（开发/改动用）：分文件版本**
```
index.html   ← 双击这个
styles.css
data.js      （Mock 基础数据：账号 / 员工 / Work / 参考 / 素材 / 数字人…）
data-wf.js   （生产事实层：方法步骤 / 产线 / 步骤执行事实 / Target Deliverables）
data-r5.js   （第 5 轮数据层：交付组合身份 / 真实依赖图 / 可发布同源 / 观测与指标 / 流程调整 / 徽标口径）
visuals.js   （内联 SVG 视觉生成：封面 / 缩略图 / 数字人）
app.js       （状态 / 路由 / 会话（四种 Scope）/ 员工与团队 / 弹窗 / 高频直达入口）
pages.js     （经营 + 研究与选题）
pages2.js    （内容制作 / 发布 / 账号 / 素材 + 流程调整与高频入口的交互）
analytics-r5.js（第 5 轮 §3 复盘重组：概览 → 趋势 → 对比 → 判断 → 下一步 + 图表与手录）
```
用浏览器打开 `index.html` 即可（同目录相对路径引用）。修改源文件后重建单文件版：
```
/Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _build.js
```

**方式 C（第 5 轮 §6 十项验收 · 当前基准，需要 Chrome）**
```
cd CONTENT_GROWTH_WORKSPACE_HTML_EXPLORATION
./_serve.sh 8777                    # 先起本地 http（后台）
NODE_PATH=/Users/yy/.workbuddy/binaries/node/workspace/node_modules \
/Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _verify-r5.js
# 再跑另一版（两版必须各跑一次，不照抄对方的 PASS）：
TARGET=single NODE_PATH=... /Users/yy/.workbuddy/binaries/node/versions/22.22.2-3/bin/node _verify-r5.js
```
实际打开 HTTP 页面并操作 DOM，逐项 PASS/FAIL 写入 `_verify-r5.log` / `_verify-r5-single.log`，截图写入 `_shots-r5/`（两版各 29 张）。
**方式 C2（第 4 轮遗留完整链路脚本）**：`_test-full.js` → `_test-full.log` / `_shots3/`。

**方式 D（其他 Agent / 自动化工具用）：走 http:// 供出来**

其他 Agent 的浏览器工具出于安全策略**只允许 http(s) 协议，不会操作 `file://` 页面**——这不是本 HTML 的问题（本原型零外部依赖：`fetch` / `XMLHttpRequest` / `type="module"` / `Worker` 全为 0，走 http 与 file:// 表现完全一致，实测见 `_check-http.log`）。给工具一个 http 地址即可：

```
./_serve.sh            # 默认 8777 端口
# 分文件版（改动用） : http://127.0.0.1:8777/index.html
# 单文件版（交付用） : http://127.0.0.1:8777/Content%20Growth%20Workspace.html
```

> 本机探测要加 `--noproxy 127.0.0.1`（本环境设有 `HTTP_PROXY`）；用 Chrome/Playwright 时加 `--no-proxy-server`。
> 验证脚本：`_check-http.js`（只用 http、不带任何 file:// 特权参数，PASS 14 / FAIL 0）。

> 为什么没用「资料库」在线部署：本轮明确要求「不依赖真实 API / 使用 Mock / 不需要 Backend」；且这是 Curis 内部产品探索，不适合发布成公网可访问链接。所以采用本地单文件方案。

---

## 二、第 5 轮定向修订（CURRENT · 本次交付）

### 2.0 输入、范围与纪律

输入（5 份，均在 `docs/research/newmedia-workspace-reference-2026-09-16/`）

1. `CURIS_CONTENT_GROWTH_HTML_REVISION_INSTRUCTION.md`（本轮指令 · Status: Review · Disposition: READY TO HAND OFF / PROTOTYPE ONLY）
2. `CURIS_CONTENT_GROWTH_TEAM_WORKSPACE_PRODUCT_STRUCTURE_CANDIDATE.md`（§5.3.1 Workflow 调整合同 / §5.6–5.6.2 / §6 协作 Scope）
3. `CURIS_CONTENT_GROWTH_OPERATIONAL_PRODUCT_EXPRESSION_CANDIDATE.md`（§3 手录 / 窄幅同步）
4. `CURIS_CONTENT_GROWTH_HTML_FLOW_SIMPLIFICATION_AND_CONTRACT_REVIEW.md`
5. `CURIS_CONTENT_GROWTH_HTML_TARGETED_REVISION_REVIEW.md`

纪律：只在 `CONTENT_GROWTH_WORKSPACE_HTML_EXPLORATION/` 内改动；不接真实平台账号 / Token / API Key；不真实发布 / 购买；不引入框架或远程脚本；不进入完整 Curis App 或 Figma；不 commit / push。候选合同是**输入**不是 Current Authority —— 遇到旧 Review 与本轮候选冲突时按候选执行并在下方如实记录，不自行造第三种产品关系。

### 2.1 §2 断路与状态事实（本轮先修）

| 指令条目 | 修前实况 | 本轮落点 | 证据 |
|---|---|---|---|
| 选题 →「完善为提案」出现「未找到」 | 选题与提案的映射靠标题 / 顺序，可能落到无关提案 | 选题 → 提案收敛改为**按对象身份解析**（`INS-5 → PROP-7`、`INS-2 → PROP-1`），池内入口与解析结果必须同源 | `_verify-r5.log` §6-1：解析结果＝池中可点入口＝PROP-7；开工后 Work 归属 PROP-7（W-208/209/210），交付身份＝`PROP-7.TD-1/2/3`，重复开工 0 |
| 账号列表「进入经营」跳到长期档案 | 按钮与父级行点击的优先级冲突 | 行内动作优先于行导航，直达 `operate / account / {accountId}` 且 Account Scope 同步 | §6-2：进入经营后 `{"area":"operate","view":"account","accountId":"xhs-brand"}`、`scope={"type":"account",...}`；返回回账号列表保来源 |
| W-206「可发布 100%」与「QA 执行中」并存 | 两个状态各算各的 | 「可发布」只由**该版本合法把关**推导（`CG.releasable` 返回 `{ok,why,by}`），Work 状态与可发布口径同源 | §6-7：`releasable.ok=false`（QA 待 Review）、`status=working`、QA 步骤如实显示「待 Review」 |
| W-202 制作与发布同标题状态不同 | 会被读成同源矛盾 | 明确标注**发布用版本 ≠ 在制版本**（`PUB-304`：平台执行 Script v2 / 在制 Script v3），并说明 v3 未过人工 Review 故不进入本次发布 | §6-7：版本分离两项 PASS |
| 导航徽标口径不明、账号同名歧义 | 徽标只有数字；账号只显示单个名字 | 每区徽标带 `title` 说明「在数什么」（待办 / 异常 / 总量口径），同源 `CG.badgeCounts()`；账号命名统一「平台｜账号」 | §6 补充段：7 区徽标口径元数据齐备；6 个账号命名带平台前缀 |
| 手录空值标完成 / 保存后固定结论 | 保存后固定显示公众号「重新分析」，冒充模型推理 | 空值一律 Unknown（不标完成）；保存只更新**对应对象与缺口**的状态；原型分析明确标「示例 / 模拟」，不冒充模型推理 | §6-4、§6-5 |

### 2.2 §3 复盘按候选合同重组（`analytics-r5.js`）

固定顺序 **本期概览 → 可视化趋势 → 对比表现 → 分析判断 → 下一步**：简介讲当前范围 / 周期 / 关键变化 / 数据完整性，不是功能教程；缺数据就地提示，不把「集中待补」当默认首屏；不建图表墙，默认少量与目标相关指标。

- **图表纪律**：单位 / 图例 / 时间轴 / 数值查看 / 可阅读明细齐备，不靠颜色单独承载；窄桌面面板与宽桌面均可用；缺数不画 0，空白＝Unknown；只有两个观测点不制造「每日曲线」；所有数值标「示例 / 模拟」，来源样例不伪装实时同步。
- **两级时间序列**：账号级（粉丝净增 / 互动 / 发布节奏）与 Publication 级（曲线 + 内容明细表），提供自然日期与「发布后相同时长」两种口径，累计与增量分开。
- **两种比较**：同账号不同内容（可选两篇，改对象 / 指标 / 窗口会改变图表与明细，未到窗口显示未成熟）；同内容跨平台（按同 Intent / Proposal 的 Variant 与 Publication，不按标题匹配；同口径可比、不同口径并排解释，不强排名）。
- **异常点可下钻**：点图上异常点 / 区间进入相关 Publication 与观测来源，返回保留比较集合、日期、指标与选择。
- **平台手录**：复用既有 Publication / Account 入口，待补只是索引；按「平台 × 内容形式 × 对象层级」决定适用字段，单次只要求当前必要项；观测带定义 / 单位 / 对象 / 区间或累计截至 / 时区 / 采集时间 / 来源与验证状态；计数 / 百分比 / 日期做校验，0 合法、空白 Unknown、部分录入保缺口；订正留旧值与原因；本地示例的重开方式与限制写明，不伪称服务器持久化。
- **「解释这段变化」**携当前范围与证据进入既有员工协作入口，分析产出的选题 / 实验 / Work 保来源与回程；不重新设计 Conversation 外观。

### 2.3 §4 Workflow 合并 / 拆分只做最小产品表达

| 合同要求 | 原型表达 | 证据 |
|---|---|---|
| 「折叠为后期制作」只是呈现分组 | `fold` 只改呈现：折叠前后步骤节点数不变、依赖 / 状态 / 责任 / 审核不变 | §6-6：折叠 7 → 7 节点、分组 0 → 1，事实一致 |
| 提供「调整制作步骤」，对话进同一意图 | Workbench「调整制作步骤」→ 面板含 原计划（保留引用）/ 调整后计划 / 依赖影响 / 责任影响 / 输入产物版本 / 时间预算 / 审核影响 / 如何回退 | §6-6：8 项全部 PASS |
| 无证据估计显示 Unknown | 时间 / 预算无证据时显示 **Unknown** 并注明不编造 | §6-6 PASS |
| 未开始步骤合并 | 合并真实改计划（步骤 7 → 6）、被合并步骤留「含合并步骤」标记 | §6-6 PASS |
| 一个步骤拆分 | 拆分真实改计划（6 → 7），`edit` → `edit-1` / `edit-2` 各自独立可查 | §6-6 PASS |
| 运行中等待安全边界 | 受影响步骤正在执行 → 拒绝应用并给出「先确认可停止或等待到安全边界」；面板同时写明该状态且**不提供「应用调整」按钮** | §6-6：样本 W-201 · `visual=working` → `ok=false / wait=true`，理由含「安全边界」 |
| 已完成保持历史 / 强制 Review 不可删除 | 已完成步骤与旧版本不被重写；`qa` 永不出现在合并 / 拆分候选里 | §6-6 PASS |
| 取消不改原计划、留记录 | 「取消调整（回到原计划）」→ `plan=null`，取消记入调整历史（追加，不覆盖） | §6-6：log 3 → 4 |
| 不开发 DAG 编辑器 / 新 Runtime / 第二 Task 系统 | 全部在本地原型内改既有计划数据，无新表 / 新服务；调整改的是真步骤而不是只弹 Toast | 见 `data-r5.js` `CG.applyAdjust` |

### 2.4 §5 做减法

- 七区保留；**团队责任长说明、员工 0..N、同源事实等建模语言移出日常主界面**，保留负责人、团队入口、交流与必要阻塞 / 权限提示。
- 制作总览：紧凑产线选择 + 队列，删重复标题与说明；Work 可直接打开，不强制经过产线页；规格按需展开。
- Work 详情：交付摘要 / 当前产物 / 步骤 / 下一动作优先；完整规格、历史、版本、责任可展开但可发现；中文业务动作优先，内部英文 ID 按需查看。
- 素材：默认**紧凑列表**（同屏可扫描全部非品牌素材），可切大图网格；授权 / 版本 / 被哪些内容使用清楚；数字人仍在素材管理、在制作使用，**不是 Employee**。
- 高频直达入口固定 4 个：记灵感 / 贴参考 / 素材 / 继续制作，与 Conversation 同一对象系统，不强迫所有直接动作都聊天。
- 修当前面板横向截断与浅色小字；保内容密度但不再「每项字段一张卡」；不重新定义 Curis 视觉规范。

### 2.5 本轮修掉的真实缺陷（不只是"按要求加功能"）

前 6 条是原型的真实缺陷，本轮在验收过程中被实操暴露并修复；后 4 条是**验收脚本自身**的缺陷（若不修，会把工具问题记成产品问题，或让断言空过）：

| # | 缺陷 | 现象 | 修法 |
|---|---|---|---|
| 1 | **路由里的 tab 意图被整体丢弃** | 「更换数字人」「返回选题池」等入口带了 `tab`，但 `assets` / `research` / `analytics` 只读 `S.tabs.*` → 点了却落在默认页签（`production` 已用 `tabToStep` 处理，其余没有） → **断路** | `app.js` `CG.go` 统一把 `r.tab` 写进 `S.tabs[area]`，一处修好一类返回链 |
| 2 | **下钻时来源 `from` 不随列表传递** | 从 Work 点「更换」到数字人列表后，`from` 在列表这一步丢掉 → 详情页不知道要换给哪个 Work，只能看不能换 | `pages2.js` 新增 `withFrom()`，素材 / 数字人列表、卡片、表格行、返回按钮全部带上 `from` |
| 3 | **「更换数字人」没有完成动作** | 弹「请在列表中选定」但列表与详情都没有选定按钮 —— 入口许诺了一个做不到的动作 | 详情页新增「改用此数字人（W-xxx）」：写入 `b.dh.current` 与引用版本、清掉旧合成态、如实带出授权覆盖结论；**授权不覆盖该账号时明确不能用于该 Work** |
| 4 | **弹窗动作按钮点了没反应** | `modal-act` 只认 4 个 action，`wf-adj-apply` / `adj-close` / `qk-idea-save` / `qk-ref-save` 全部无处理器 | `app.js` `modal-act` 增加 `CG.H[a]` 兜底回退；相关 action 的参数统一放进 `p`（渲染层只序列化 `a` / `p`） |
| 5 | **应用合并后 Work 再也打不开（严重）** | `afterGroups` 从「只含 names 的展示分组」派生，缺 `steps` → 渲染抛 `Cannot read properties of undefined (reading 'map')` | `data-r5.js` 一律从带 `steps` 的真实步骤分组派生；`planOf` 加 fail-safe（结构不合法就回退）；`adjOf` 把折叠状态归一化为布尔 |
| 6 | **手录保存无效 / 概览关键指标行漏接** | ① `an-save` 的参数挂在 action 对象上（渲染层丢弃）→ 永远提示「未保存任何观测」；② `const KPI` 构建好但从未拼进 body → 概览 `.kpi` 数 = 0 | ①参数压进 `p:JSON.stringify({...})` 并在处理器解析；②把 KPI 行接回 body 首位 |
| 7 | 折叠状态恒为 true | `adjOf` 初始值写错（对象当布尔用） | 归一化 `if(typeof a.folded!=='boolean') a.folded=false;` |
| 8 | 验收脚本：后台标签页点击挂死 | 新建第二个 page 后原 page 变后台，`page.click` 15s 超时（心跳 `evaluate` 正常）→ 误判成原型死循环 | `page2.close()` + `bringToFront()`；弹窗点击改 `$eval(e=>e.click())`；加 `protocolTimeout: 30000` |
| 9 | 验收脚本：favicon 404 噪声被当成运行时错误 | 消息文本不含 "favicon"，URL 在 `m.location().url` | 新增 `isFaviconNoise()` 按 URL 判断 |
| 10 | 验收脚本：3 处期望值过期 / 会让断言空过 | ①按 `data-action="back"` 找返回入口（原型里不存在，页内返回是 `data-go` + 全局返回）→ 假失败；②换数字人样本选在详情页上找列表卡片 → 假失败；③受阻样本用「合并正在执行的步骤」（实现上候选只对未开始步骤开放）→ `skip:true` **空过**，等于没测 | 全部按实际产品表达与可复现样本重写；受阻改为「拆分一个正在执行的步骤」，实测压到安全边界 |

### 2.6 本轮新增 / 改动的文件

| 文件 | 说明 |
|---|---|
| `data-r5.js`（新） | 交付身份（Proposal + Deliverable 组合 ID）、真实依赖与显示分组、可发布同源、观测与指标定义、流程调整（原计划 / 建议计划 / 影响 / 生命周期）、徽标口径 |
| `analytics-r5.js`（新） | §3 复盘重组（概览 → 趋势 → 对比 → 判断 → 下一步）+ 内联 SVG 图表 + 平台手录 + 订正历史 |
| `app.js` | `CG.go` 落实 tab 意图；`modal-act` 兜底回退与 `work-conv`；会话 / 员工与团队；高频直达入口 |
| `pages.js` | 选题 → 提案按对象身份解析；开工 Target Deliverables；团队条减负 |
| `pages2.js` | 素材紧凑列表 / 大图网格、数字人下钻与「改用此数字人」、`withFrom` 来源传递、制作总览与 Workflow 调整面板 |
| `styles.css` | 追加本轮组件样式（紧凑列表、调整面板、概览 KPI 行等），不改既有视觉体系 |
| `_verify-r5.js`（新） | §6 十项实操验收脚本（两版各跑一次），产出 `_verify-r5.log` / `_verify-r5-single.log` 与 `_shots-r5/` |
| `Content Growth Workspace.html` | 由 `_build.js` 重新内联生成（411.8KB，与分文件版同步） |

---

## 二·A、第 4 轮定向修订（历史记录 · TARGETED REVISION）

输入（4 份）
1. `CURIS_CONTENT_GROWTH_TEAM_WORKSPACE_PRODUCT_STRUCTURE_CANDIDATE.md`
2. `CURIS_CONTENT_GROWTH_OPERATIONAL_PRODUCT_EXPRESSION_CANDIDATE.md`
3. `CURIS_CONTENT_GROWTH_EMPLOYEE_COLLABORATION_AND_PRODUCTION_RECONCILIATION.md`
4. `CURIS_CONTENT_GROWTH_HTML_PRODUCT_EXPRESSION_REVIEW.md`（A1–A10 缺陷清单）

本轮**不是重做 HTML**，是在既有高保真原型上做定向修订：落实四种协作 Scope、重建开工与 Production 表达、修掉 A1–A10 逻辑缺陷，并新引入一层"生产事实"数据（`data-wf.js`）。

### 2A.1 Employee Collaboration —— 四种 Scope（同一 Conversation System ≠ 同一默认收件人）

| Scope | 从哪进 | 携带什么 | 谁接收 |
|---|---|---|---|
| **Team Intent** | 每区唯一的「向整个区域交代新事情」输入框 | Area + Account Scope + Selected Object + Work | 本区 Responsibility → Assignment 路由；**不是指定某个人**，路由结果显式写出「按责任交给谁」 |
| **Specific Employee** | Team Presence 条上的员工 chip / 员工详情「找我交流」 | 被点的那名员工 + Account Scope | 严格保持指定人。若请求落在别人的责任域，**显式插入一条系统说明**说"转交给谁、为什么"，回复不会被改写成被点员工的结论 |
| **Specific Work** | 队列行 / 卡片 / 「讨论这个 Work」 | workId + 实际 Work Owner + Account + 当前 Artifact/Version + 状态 | 该 Work 的**实际 Owner**；无有效 Assignment 时显示责任缺口，不由本区责任承担者冒充 |
| **Workflow Step** | 步骤详情「就这一步交流」 | Work + Step + Responsibility + 当前 Employee + Input 版本 + Artifact 版本 + Dependency | **该步骤的当前承担人**；结果只回到这个 Work 的这个 Step 与那个 Artifact 版本 |

对话头（只读上下文卡）必须回答三件事：**和谁交流 / 讨论什么 / 为何由其负责**——四种 Scope 都能看到 `交流范围 / 讨论对象 / 步骤 / 本步目的 / Input·Artifact 版本 / Dependency / Account Scope / Selected Object / 实际接收人 / 为何由其接收 / 责任缺口`。

### 2A.2 Work Area Team Presence（不做 Employee Card Wall）

每个 Work Area 顶部是一条紧凑的 **Team Presence**：Responsibility（本区唯一责任域）· 当前责任承担者 · 实际承担（各 Work Owner 计数）· 相关 Work 数 · 员工 0..N 的可点 chip · 「责任与团队」入口。员工 chip = 找这个人交流；输入框 = 向整个区域交代新事情。**专业 Surface 仍是页面主角**，团队条只占一行。

### 2A.3 开工：Target Deliverables（不再跳旧 Production Work）

`Proposal → 开工` 先形成明确的 **Target Deliverable 集合**：Target Account / 经营目的 / 成功判据 / Format / Production Method / 必要 Output Specification / Human Review 要求 / 依据。系统按 Account Goal · Strategy · Proposal 预填，**只让 CEO 确认真正存在分歧的项**（每项分歧都可一键采用备选）。确认后按 Target Deliverable 逐个创建关联 Work（方法不同 → 步骤集不同 → 责任人不同 → Retry 边界不同），不做笛卡尔积，也不"一账号一 Work"。

样例（`PROP-7`）：同一个选题在三个账号上拆成 3 个 Target Deliverable —— 小红书品牌号图文 3:4/8 页 · 抖音创始人 IP 数字人口播 9:16/60s · 公众号创始人号长文 2,000–2,500 字，可多选开工。

### 2A.4 Production Overview：Production Lines 与 Cross-line Work Queue 共存

- **Production Lines**：按 Format + Method 分组的四条线（图文排版 / 口播视频 / 视频 / 长文章），一行一条显示典型规格、Work 数、阻塞数。**同一 Work 只归属一条线，不重复计数**（各线之和 = 全部 Work 数）。
- **Cross-line Work Queue**：唯一 Work 事实的跨线队列；每行体现**内容本身**（缩略图 / 形态·方法 / 目标账号 / 交付规格 / 当前步骤·承担人 / Owner·协作 / 状态）。
- 产线**不是新导航**：不强制三级跳，可以直接从队列进 Work。
- 口播与非口播共用「视频」Format，靠 Method 互斥归属。

### 2A.5 Specific Production Work：Method-specific Workflow（删掉固定 12 Tabs）

每个 Work 只显示**本方法真正需要的步骤**：
- 图文排版：Brief → 文案 / 排版 → 视觉 / 排版 → QA
- 数字人口播：Brief → Script → 数字人 / 资产 → Synthesis → Editing → Subtitle / Packaging → QA
- 长文章：Brief → Research → Outline → Draft → Editing → Illustration → QA
- 混剪 / 录屏等：各自步骤集

每步显示 Purpose / Status / Dependency / Responsibility / Current Employee / Collaborator / Input 版本 / Artifact 版本 / Blocker / Review Result / Conversation Entry。**图文不会出现数字人、视频、字幕**；长文章不会出现比例、页码。步骤尚未连接真实编排时，诚实标注「节点执行视图尚未连接」，不假装跑过。

### 2A.6 改某一版 Script = 出新 Version + 标下游受影响

从 Script 步骤「就这一步交流」说明修改要求（如"开头太慢，重写前 3 秒"）→ 该步骤产出**新 Version**，旧版本保留可查；**所有下游步骤标注"上游已更新"**，其中已经产出过的进一步标「输入已失效 · 需重检」。未受影响的上游步骤保持不变。页面上的「让徐白再给 3 个开头」是**直接动作**，走同一条改版路径，不产生第二套结果。

### 2A.7 第 4 轮修复的 A1–A10 逻辑缺陷

| ID | 缺陷 | 修法 |
|---|---|---|
| A1 | conv-open 没有完整处理；Workbench 用固定 12 Tabs 抹掉 Format/Method 差异 | 唯一 `discuss` action + Method-specific Workflow |
| A2 | Specific Employee 被静默换人/改口 | 转交时插入系统说明，消息保留真实 sender，标「执行转交」 |
| A3 | Specific Employee 丢 Account / Selected Object | 上下文全部来自入口元素属性，不再依赖"当前路由恰好是哪个区" |
| A4 | Work 讨论丢 workId | 会话 key 与上下文都带 workId |
| A5 | Work 讨论找错 Owner（找区域责任承担者） | `routeConv` 按实际 Work Owner 解析 |
| A6 | 开工固定跳旧 W-204 | Target Deliverables → 按选项创建关联 Work |
| A7 | Proposal 开工链路与 Production 脱节 | 开工即写入 Work + 步骤事实（`CG.WF`） |
| A8 | Account Scope 丢失 | 入口自带 + 沿用当前经营范围，对话头显式标注 |
| A9 | Research 结果硬编码 `dy-brand` | 结果与落地全部按当前 `Account Scope` 生成 |
| A10 | 异步回复在切换 Conversation / Work 后串台 | 会话 key 隔离 + 异步绑定 `sid` + 归位判断（回到原会话并计数未读） |

### 2A.8 第 4 轮新增/改动的文件

| 文件 | 说明 |
|---|---|
| `data-wf.js`（新） | 生产事实层：方法步骤定义（`CG.METHODS`）、产线（`CG.LINES` / `lineOf`）、步骤执行事实（`CG.WF` / `wfOf` / `stepOf`）、Target Deliverables（`CG.DELIVERABLES` / `delivOf` / `delivById`）、方法必要团队（`methodTeam`）、区域责任（`CG.AREA_RESP`）、数字人选取（`dhFor`） |
| `app.js` | 重写会话系统（四种 Scope / 会话隔离 / 上下文头 / 改版路径）、员工与团队弹窗、`discuss` action |
| `pages.js` | Team Presence 版 collabBar、开工链路（`openDeliverables` / `deliv-confirm`）、Proposal 多 Target Deliverable 表达 |
| `pages2.js` | Production Overview（Lines + Cross-line Queue）、Method-specific Workbench、Artifact 与版本表达 |
| `styles.css` | 追加本轮新组件样式（Team Presence / ctx-box / line-row / wf-rail / deliv 卡片），不改既有视觉体系 |
| `_build.js`（新） | 由分文件版生成单文件版（全内联） |
| `_test-full.js`（新） | 完整链路 + 多员工 + 并行 + 窄屏 + 单文件版自测（`_test-full.log` / `_shots3/`） |

---

## 三、第 4 轮验证的 10 个问题，在这些地方看（页面位置仍然有效）

| # | 要验证的问题 | 在哪里看 |
|---|---|---|
| 1 | 整体排版 | 任意页面。深灰导航 + 浅色工作区；上=判断/焦点，中=专业工作面，右=团队与相关工作 |
| 2 | Professional Workspace Navigation | 左侧固定 7 项：经营 / 研究与选题 / 内容制作 / 发布 / 账号 / 复盘 / 素材（带待处理计数）。**没有固定 Context 栏** |
| 3 | Portfolio / Platform / Account 切换 | 经营页右上「经营范围」下拉（Portfolio → 平台 → 账号）+ 下方 6 个账号横向 Account Strip，两种方式都能切换 |
| 4 | 7 个 Work Area 是否清楚 | 每区都有：一句话 Purpose、负责团队条、专业工作面、相关工作 |
| 5 | Professional Surface + Shared Work Area 共存 | 专业页面永远是主角（占主列），Shared Work Area 收在右侧窄栏「相关工作」 |
| 6 | AI Employee / Team 如何自然驻守 | 每区顶部团队条只占一行（负责人 + 当前重点 + 相关 Work 数 + 交流按钮），点负责人打开员工详情（多 Work） |
| 7 | Conversation 如何进入 | 每区「与团队交流」，打开右侧抽屉；抽屉里带本范围只读上下文、按责任路由提示、并行 Work 提示 |
| 8 | 多 Work 并行如何表达 | 制作队列一次列出 7 个 Work、5 种状态；员工详情列出该员工多个 Work；抽屉顶部提示「另外 N 个 Work 继续推进」 |
| 9 | 页面之间如何跳转和返回 | 见下方「跳转链路」；面包屑 + ← 返回保持原 Scope |
| 10 | 像不像专业新媒体运营工作台 | 全流程走一遍：经营判断 → 研究 → 参考拆解 → 提案 → 开工 → 口播制作 → 把关 → 排期 → 回执 → 复盘补数据 → 新实验 |

---

## 四、固定测试账号（3 平台 × 2 账号 = 6 个，字段全部不同）

| 平台 | 账号 | 阶段 | 健康 | 值得一看的点 |
|---|---|---|---|---|
| 小红书 | 品牌号 | 稳定更新期 | 健康 | 封面实验见效、库存 6 天、Goal 净增 8k |
| 小红书 | 创始人IP | 起步期 | **断档风险** | 库存 2 天、语气 A/B、工作被授权照片阻塞（W-205） |
| 抖音 | 品牌号 | 快速测试期 | 健康 | 前 3 秒实验、完播 22%→28% 但咨询 0（反例） |
| 抖音 | 创始人IP | 起步期 | **阻塞** | 口播 Workbench 主角、数字人语速实验 |
| 公众号 | 品牌官方号 | 沉淀期 | 健康 | 无 API 授权 → 必须人工发布 + 人工补数据 |
| 公众号 | 创始人号 | 休眠后重启 | **需关注** | **空态**：当前无进行中 Work，团队在准备下一轮 |

---

## 五、7 个专业工作区与页面清单

### 01 经营（Leader Operating Surface）
- Portfolio：Leader 判断条（结论先行）→ 账号组合表（按平台分组、点行展开经营摘要）→ 本轮重点与资源安排 / 供应与节奏健康（Pipeline Health）→ 结果、实验与经营判断 / 下一轮与待决定事项 → 当前经营边界（Operating Envelope，7 项）
- Account Scope：身份阶段目标 / 策略内容方向节奏 / 当前推进与供应 / 实验结果学习 / Leader 判断与下一步（默认开 3 个、收起 2 个，做信息优先级 + 渐进披露）
- 空态：公众号｜创始人号 → 「当前无进行中 Work」+ 让团队准备下一轮

### 02 研究与选题
- 快速输入（记灵感 / 分析参考 / 按账号找选题）
- 5 个局部视图：选题池与灵感（左列表 + 右详情）/ 参考与拆解 / 内容提案 / 持续关注 / 研究工作
- 适用性过滤：全部 / 未分配 / 账号专属 / 多账号适用
- Reference 详情：Source / Theme / Hook / Opening / Structure / Rhythm / Visual / CTA / Why it works / 来源片段（00:03-00:08 等）/ 关联 Knowledge 与 Proposal / **适用性表**（同一 Reference 不复制：Theme 适合小红书品牌号、Hook 适合抖音创始人IP、Structure 两边都可，含依据 / 可信度 / 限制）
- Proposal 详情：[开工] → 直接进制作 Work

### 03 内容制作
- **Production Overview**：Production Lines（按 Format + Method 四条线，一行一条，不重复计数）+ Cross-line Work Queue（每行体现内容本身：缩略图 / 形态·方法 / 目标账号 / 交付规格 / 当前步骤·承担人 / Owner·协作 / 状态）+ 产线 / 状态 / 方法 / 账号筛选；10 个 Work 并行，含 Waiting / Working / Review / Blocked / Ready 与 1 个「待分配负责人」责任缺口
- **Specific Production Work**：按本 Work 的 Production Method 只显示真正需要的步骤（图文 4 步 / 数字人口播 7 步 / 长文章 7 步 / 混剪 5 步），每步含 Purpose / Status / Dependency / Responsibility / Current Employee / Collaborator / Input·Artifact 版本 / Blocker / Review Result /「就这一步交流」；[生成口播] 走 Working → 产出 Artifact（版本写入步骤事实）
- Artifact 与版本：按步骤列出产物（点任意一项跳回该步骤）+ 版本历史（新版本不覆盖旧版本）+ 引用资产 + 账号 Variant

### 04 发布
- 发布队列 / 日历 / 记录与回执 / 人工接续
- 日历：行 = 6 个账号、列 = 7 天（09-14→09-20，今天高亮），支持按平台 / 账号 / 状态过滤，共 11 条排期
- 三种关键状态都能看到下一步：自动发布成功（回执正常）/ 需人工发布（发布包 + 报告已完成）/ 外部效果 Unknown（先核验，禁止用重试制造重复发布）

### 05 账号
- 账号组合：按平台分组、搜索、平台筛选、6 个账号全展示
- 账号详情：身份 / 绑定与准备状态 / 长期定位与阶段历史 / 作品与发布历史 / 数据新鲜度 + [进入经营] 跳到经营 Account Scope（不重复第二个经营页）

### 06 复盘
- 数据质量与待补（3 项待补，含手动录入）/ 判断与反例 / 表现与实验 / 学习与下一步
- 每一条判断都是「事实 → 推断 → 反例 / 混杂 → 适用限制 → 下一步」，不止图表
- 手动录入：点 [去录入] → 只填本次判断必要指标 → 保存 → 页面更新 + 「苏澈 刚刚重新形成判断」

### 07 素材
- 素材与参考 / 品牌表达 / 数字人 / 待准备与请求（含搜索、过滤、详情、被哪些 Content 引用）
- 数字人 3 个（言舟 v2 可用 / 苏黎 v3 可用 / 陈屿 v1 授权待续期受限），每个含人设 / 外观 / 声音 / 适用账号 / 授权 / 版本 / 可用性 / 历史使用
- 标注清楚：**数字人是资产，不是员工**；版本更新不静默替换在途引用

---

## 六、可交互清单（都能点）

- **导航**：7 个 Work Area 切换；面包屑；← 返回（保留原 Scope 与原筛选）
- **经营范围**：Scope Switcher（Portfolio / 平台 / 账号，唯一入口）、账号表展开行、Account ↔ Portfolio 往返
- **Team Collaboration（每区唯一入口）**：Team Presence 条（Responsibility / 责任承担者 / 实际承担 / 员工 chips / 责任与团队）→ 员工 chip = 找这个人交流（Specific Employee）；输入框 = 向整个区域交代新事情（Team Intent）；「责任与团队」弹窗含本区 Work（每条可「讨论此 Work」= Specific Work）
- **会话（右侧抽屉）**：只读上下文卡（和谁 / 讨论什么 / 为何由其负责 / Input·Artifact 版本 / Dependency / Account Scope / Selected Object）→ 输入 → 路由说明（转交必须显式）→ Working → Structured Result 卡片 → 结果动作回到专业页面；离开后结果自动归位到原会话并提示
- **员工详情弹窗**：责任 / 当前重点 / 该员工负责或参与的 Work（讨论 = 具体 Work）/ 当前承担步骤（讨论 = Workflow Step）
- **开工（Proposal → Target Deliverables）**：[开工] → 多选 Target Deliverable（含需确认的分歧项，可一键采用备选）→ 确认后按方法创建关联 Work 并进入对应 Workflow
- **Production**：产线筛选 / 状态筛选 / 方法筛选 / 账号筛选；行点击进 Work；Workflow 轨道点步骤切换；[生成口播]（Working → Artifact + 版本）；[让徐白再给 3 个开头]（出新版本 + 标下游受影响）；[提交把关结论]（写回步骤事实）；[启用派生 Variant]
- **发布**：日历 / 队列 / 记录 / 人工接续切换；[核验] 会把 Unknown 变成已发布；[报告已完成] 会写入人工自报；[下载发布包] / [打开平台]
- **复盘**：[去录入] 弹窗 → 保存 → 页面与判断同步更新；[建立实验 Work] 新增实验；学习状态过滤（全部 / 已接受 / 候选 / 不适用）
- **复盘（第 5 轮）**：概览 → 趋势 → 对比 → 判断 → 下一步；两种比较（同账号两篇 / 同内容跨平台）可换对象·指标·窗口；点图上异常点下钻到 Publication 与观测来源并可返回；手录按平台 × 形式 × 层级给字段、留订正历史
- **素材（第 5 轮）**：紧凑列表 ↔ 大图网格；点条目看大图与授权 / 版本 / 被谁引用；[用于制作] 选定具体版本后可回原 Work
- **Workflow 调整（第 5 轮）**：[调整制作步骤] → 选合并 / 拆分对象 → 看变更前后 / 依赖 / 责任 / 版本 / 时间预算 / 审核影响 → [应用调整]（真实改计划）；[取消调整] 回到原计划并留历史；受影响步骤正在执行时不给「应用调整」，改为写明等待安全边界
- **经营**：顶部「经营边界」弹窗（7 项边界 + 2 项等待 CEO 的决定）
- **持续经营表现**：进行中 Work 的进度条会自己往前走（2.6 秒一次），页面不刷新不丢状态

### 跳转链路（都已实测）
```
经营 Portfolio → 账号展开 → Account 经营 → 相关 Work → 返回
经营 Portfolio → 账号档案 → [进入经营] → 经营 Account Scope
研究与选题 → 向团队交代新研究（显示谁接收）→ 找具体员工交流 → Reference 详情 → 围绕 Reference 讨论
→ Proposal → 开工 → 多选 Target Deliverable → Production（Lines / Cross-line Queue）
→ 数字人口播 Work → Workflow → Script 步骤 → 就这一步交流 → 出新版本 + 下游受影响
→ Artifact → 发布 → 复盘 → 账号经营
Production Workbench → [管理此数字人] → 素材 · 数字人详情 → [返回原 Work]
Production Workbench（数字人步骤）→ [更换] → 素材 · 数字人列表（页签已落到「数字人」）→ 选定某个数字人
  → 授权覆盖该账号 → [改用此数字人（W-xxx）] → 回到原 Work 的数字人步骤（引用版本更新、旧合成态清空）
  → 授权不覆盖该账号 → 明确「不能用于 W-xxx · 授权不含该账号」，不提供选定按钮
Production Ready Work → [进入发布排期] → 发布 → 发布记录详情 → [去复盘补数据] → 复盘
复盘 → Insight / 学习候选 → [建实验 Work] / [去研究]
```
所有跨区下钻都带来源，返回路径保持原 Scope。

---

## 七、状态覆盖（不新增 Domain 状态枚举，只做 UI 表达）

Empty（创始人号无 Work）· Working（4 个 Work 进行中）· Waiting（数字人队列）· Review（待把关）· Blocked（缺授权 / 封面规格）· Unknown（平台回执超时）· Needs Human（人工发布）· Completed（已发布 / 已接受学习）· 责任未配置（W-207 待分配负责人）

---

## 八、验收结果

### 8.1 第 5 轮（CURRENT）· §6 十项 · 实际打开两版 HTTP 页面

```
=== 分文件版（index.html）        PASS 138 / FAIL 0 · 运行时错误 0 ===
=== 单文件版（Content Growth Workspace.html） PASS 133 / FAIL 0 · 运行时错误 0 ===
```
记录：`_verify-r5.log` / `_verify-r5-single.log`；截图：`_shots-r5/`（两版各 29 张，含复盘概览 / 趋势、两种比较、手录、Workflow 折叠·合并·拆分·**运行中受阻**、制作队列、素材）。

| # | 指令要求的验收项 | 结果 | 关键证据 |
|---|---|---|---|
| 1 | 选题→正确提案→确认目标交付→正确 Work→返回来源；无未找到 / 串对象 / 重复开工 | PASS | 解析＝入口＝PROP-7；Work＝W-208/209/210，交付身份 `PROP-7.TD-1/2/3`，重复 0 |
| 2 | 账号列表经营直达、返回保范围；产线筛选→Work→返回保筛选 | PASS | `operate/account/xhs-brand` + Account Scope；产线筛选状态往返保持 |
| 3 | 同账号两篇对比；同内容两平台对比；累计与同龄窗；不同口径 / 样本未成熟说明 | PASS | 两种比较截图；未到窗口显示「未成熟」；不同口径并排解释不强排名 |
| 4 | 图表→明细 / 证据→回原范围；无数据、两点手录、空白 / 0 / 错误百分比、订正历史 | PASS | 异常点下钻与返回保比较集合；0 合法 / 空白 Unknown / 越界拦截；订正留旧值 |
| 5 | 复盘分析→下一步选题 / 实验，保持原证据；模拟结果明确 | PASS | 「解释这段变化」携范围与证据进协作入口；模拟标注可见 |
| 6 | Workflow 合并 / 拆分 / 取消 / 运行中受阻 / 已完成历史 / 不可移除 Review；应用后步骤·依赖·责任与产物引用一致 | PASS | 折叠 7→7、合并 7→6、拆分 6→7、取消 `plan=null`＋历史追加；受阻样本 W-201 拒绝并指向安全边界 |
| 7 | 制作与发布准确关联版本；可发布只来自该版本合法把关；未知外部效果先核验而非重发 | PASS | W-206 `releasable.ok=false`；PUB-304 标注发布 v2 / 在制 v3；核验不新增发布记录（13→13） |
| 8 | 素材多项目可扫描、数字人可找到、选资产后回原 Work；无真实上传或外部副作用 | PASS | 紧凑列表 4/4 行可扫描；授权不覆盖时如实「不能用于」；选定回原 Work；本地空操作 |
| 9 | 窄桌面面板与宽桌面视口查看首屏 / 表格 / 图表 / 步骤条；关键按钮可键盘到达并可理解 | PASS | 1600px 与 1180px 均无横向溢出；图表随容器缩放；入口可 Tab 聚焦且带可理解名称 |
| 10 | 分文件版 / 单文件版均加载并走关键路径、无运行时错误 | PASS | 两版各跑整套 §6（并交叉确认另一版可加载），运行时错误 0 |

### 8.2 第 4 轮（历史）· 自测 90/90

```
=== 自测汇总：PASS 90 / FAIL 0 ===
--- 运行时错误（开发版） ---
none
```

完整记录：`_test-full.log`；截图：`_shots3/`（21 张）。覆盖：

| 段 | 覆盖 | 结果 |
|---|---|---|
| A | 经营 → 小红书（平台）→ 小红书品牌号（Account Scope）；唯一 Scope Switcher / 唯一 Team 入口 | ✓ |
| B | 研究 → 向团队交代新研究 → 对话头显示接收人 + 为何由其接收 + Account Scope | ✓ |
| C | 找具体 Employee（沈述）→ 保持指定人；hook 请求显式转交徐白，不偷换身份 | ✓ |
| D | 打开 Reference → 围绕 Reference 讨论（Selected Object + Account Scope 都在） | ✓ |
| E | Proposal → 开工 → 3 个 Target Deliverable 多选 → 创建 3 个关联 Work（方法/步骤集各不相同，不笛卡尔积） | ✓ |
| F | Production Lines（5 行）+ Cross-line Queue 共存；各产线之和 = 全部 Work 数（10=10，不重复计数）；口播产线筛选 | ✓ |
| G | 数字人口播 Work → 7 步 Method-specific Workflow → Script 步骤交流 → 新 Version + 下游 5/5 步标受影响 + 页面同步显示 | ✓ |
| H | Artifact 与版本历史 → 合成产出 → 发布 → 复盘 → 账号经营 | ✓ |
| I | 四种 Scope（team / employee / work / step）生成 4 个不同会话 key，收件人各不相同且符合规则 | ✓ |
| J | 徐白同时参与 8 个 Work；发送后立即切换页面，异步结果回到原会话、另一会话不被塞入（不串台） | ✓ |
| K | UI 简化自检：1 个 Team 入口 / 0 个固定 Tabs / 0 个员工卡片墙 / Work 只渲染本方法步骤 / 交流入口 ≤2 / 确定动作仅 5 个 | ✓ |
| L | 窄屏 1100px：生产总览与 Workflow 正常 | ✓ |
| M | 单文件版可运行、数据层一致、零运行时错误 | ✓ |

## 九、已知问题 / 剩余限制（第 5 轮更新）

**A. 本轮明确未做的（在指令 scope 之外，不是缺陷）**

1. **不接真实平台 / Token / API Key**：全部数据是本地 Mock；页面所有数值标「示例 / 模拟」，来源样例不伪装成实时同步。
2. **无服务端持久化**：手录与调整只改内存状态，刷新回到 Mock 初值；页面上明确写明这一限制，不伪称服务器存储。
3. **平台字段未做官方映射核验**：手录按「平台 × 内容形式 × 对象层级」给适用字段，但**不宣称全面平台适配**（指令明确本轮不扩大竞品研究）。
4. **不做 DAG 编辑器 / 新 Workflow Runtime / 第二 Task 系统**：合并 / 拆分 / 取消只在既有计划数据上做最小表达。
5. **移动端仍未适配**：本轮是 Desktop first，只保证窄桌面面板（≤1180px）与宽桌面视口可用。

**B. 原型内部的模拟口径（避免被当成能力）**

6. **会话是脚本化模拟**：按关键词路由到预设回复 + 结果卡，不是真模型调用。
7. **步骤执行事实是 Mock 投影**：没有显式事实的 Work 生成步骤骨架并标注「节点执行视图尚未连接」，不假装跑过真实编排。
8. **进度条自动前进是视觉模拟**，不代表真实调度 / 并发能力。
9. **`W-207`（待分配负责人）是刻意保留的缺口样本**，用于验证「责任未落实必须如实显示」。

**C. 值得记录的边界与残留**

10. **「运行中受阻」只在「拆分正在执行的步骤」这条路径上被实测覆盖**：合并候选在实现上只对**未开始**的步骤开放，因此「合并一个正在执行的步骤」会先被「没有可合并的未开始相邻步骤」挡下，走不到安全边界检查（`_verify-r5.js` 已把这一点写明，并改用可复现样本，不再让断言空过）。
11. **受阻安全边界闸是原型级判断**（受影响步骤状态 + 外部效果未知），不是正式 Runtime 的安全边界实现。
12. **`_smoke.js` / `_check-video.js` 是更早轮次的脚本**，其中 `.wb-tabs` 选择器已随固定 12 Tabs 的删除失效；当前基准是 `_verify-r5.js`（§6 十项）与 `_test-full.js`（第 4 轮完整链路）。

## 十、完成后状态

第 5 轮只修改 `CONTENT_GROWTH_WORKSPACE_HTML_EXPLORATION/` 内的原型、打包 / 验证脚本与 README 本文件，未修改 Blueprint / Master Map / UI Blueprint / Shell / Visual Standard / Pointer / 任何 Frozen 或 Candidate Authority，未触碰 `backend/`、`frontend/`、数据库或配置，未接入任何真实平台凭据，未 commit / push。

**TARGETED HTML REVISION COMPLETE（第 5 轮）**
**两版实操验收：分文件版 PASS 138 / FAIL 0；单文件版 PASS 133 / FAIL 0。**
**STOP FOR CEO / INDEPENDENT BROWSER REVIEW。**

## 第 6 轮：统一 BI 趋势比较（2026-09-16）

仅修改本目录原型。复盘保留概览 → 趋势与对比 → 分析判断 → 下一步。
- 同一视图切换账号 / 同账号不同内容 / 同内容跨平台；对象、指标、自然日期或发布后时长、7/14/30 天与自定义日期共同控制图表。
- 支持播放、阅读、粉丝净增/总量、完播率、收藏、互动；只有现有示例观测才绘点。不制造内容涨粉归因。不同平台互动构成分面说明，不混算排名。
- 修正未来观测参与比较、120h 冒充7d、手录指标错位、观测时间/来源缺失、W-201交付记录缺失、调整面板显示其他Work发布风险、日期和计数轴表达问题。
- 手录追加并保留旧值，同指标同时间订正要求原因；本次会话有效，刷新仍恢复Mock。

验证：`node _verify-bi.js` 通过选择保留、7天过滤、Unknown、内容入口、未来点排除、跨平台、数值校验、W-201组合身份检查。语法检查与 `_build.js` 成功。
实际浏览器：分文件版验证内容阅读→收藏切换保留选择、跨平台互动分面、账号互动缺口录入1000后缺口减少且图表出现1000；单文件版验证账号粉丝总量→近7天为每账号7点，所查浏览器错误日志为空；检查最终图表截图。未重跑上一轮全套133/138项，不沿用其通过数。
边界：平台字段尚未官方逐项核验；示例观测稀疏、无服务端持久化、无平台连接；不代表真实经营能力验收。未修改Authority、Curis运行代码或数据库，未commit/push。


## 第七轮：功能补齐与页面减法（2026-09-16）

范围仅为此 HTML 原型目录；未改 Curis Authority、业务代码或数据库，未 commit / push。

- 经营改为平台图标下拉选择账号；制作、发布按平台分组多选。经营保留目标与节奏，账号页聚焦身份、连接与权限。
- 移除顶部重复快捷入口、标题副说明与制作重复统计；制作列表精简，步骤详情显示用途、负责人和问题，交付要求与技术详情按需展开。员工交流结构及导航保持原样。
- 复盘增加按标题、账号、发布时间筛选的内容表现表；点击内容进入观测和手录，选择同账号内容或同一内容的跨平台版本进入现有趋势比较。缺失数据保持未知，累计值与区间新增不混用。
- 素材支持本地多文件选择及拖入、分类、预览、去重、保存失败提示与重试。数字人外部文件可记录人设、外观、声音、授权、版本，并引用到制作工作；导入不代表授权或驱动能力已经就绪。

### 验证

`node _verify-r7.js`：分组账号、内容身份/搜索/日期/账号筛选、未知值、自定义日期、七区渲染与步骤面板通过。`node _verify-bi.js`：原趋势选择、时间窗口、未知值和跨平台检查通过。

实际浏览器验证：经营账号切换、制作多账号筛选；本地文本与测试声音文件选择导入、刷新保留、数字人文件引用到 W-202；两版 HTTP 页面均可读取同源导入文件；单文件内容表选中两平台版本后进入跨平台趋势图。未复跑旧版 138/133 全套验收，不沿用旧计数。

### 数据和能力边界

导入文件以 Blob 存于当前浏览器 IndexedDB；单文件上限 200 MB，受浏览器可用空间限制，不上传云端。相同浏览器、相同协议/主机/端口的两版共享这些文件；切换端口、浏览器或清除站点数据不会自动迁移/保留。经营数据仍为 Mock，手录和工作计划刷新恢复示例。没有连接真实平台或数字人生成服务；平台字段未完成官方全面核验。拖放路径已实现，本轮实际导入证据使用文件选择器。

平台图标来自 Simple Icons（xiaohongshu/tiktok/wechat），保存于 assets/platforms 并内联，不依赖外部图片请求。


## 第八轮：补齐示例页面交互（2026-09-17）

本轮按 CEO 澄清，仅补完整页面操作和演示对象流转，不要求接通真实扫描、发布或下载，也不做 Curis 装配方案。

- 账号：添加、编辑、连接方式选择、暂停/恢复、移出/恢复；已有未结束工作/排期时阻止移出，历史仍保留。暂停或移出的账号不能新开工。
- 持续关注：添加/编辑来源、类型、频率、获取方式，暂停/恢复、移除、立即检查演示、查看发现、手动发现进入选题池。真实浏览器/API/MCP连接留待集成。
- 选题：移除重复提案卡，未分配选题可编辑并选择账号；形成提案后才确认交付开工；可放弃并保留灵感记录。
- 决定：批准/拒绝/要求调整及说明；不付款、不自动授予外部权限。
- 制作/素材：长文章编辑不再复用视频剪辑说明；普通素材可选择目标工作并记录具体版本引用。
- 复盘：建立实验研究工作，可见负责人/来源/观察窗口，重复提交不重复创建。
- 发布：下载明确是演示；人工登记先填写链接/记录编号与时间，保持待核验；核验结果可手动演示。阻塞处理先看具体原因再回相关制作。

验证：浏览器实测新增账号→移出→已移出列表→恢复；新增关键词关注和每6小时频率→手动发现→选题池；经营决定要求调整；复盘建立实验后研究工作数量增加。`node _verify-r7.js`覆盖七区渲染及新增生命周期/重复防护/待核验状态，`node _verify-bi.js`覆盖既有趋势逻辑。

边界：新增管理数据仍只在当前示例内存中，刷新回到初始演示；本地导入文件保持上一轮IndexedDB存储。没有真实后台扫描/平台授权/发布。未修改任何正式产品Authority、Curis业务代码或数据库，未commit/push。

## 第9轮：来源 → 讨论 → 确认 → 选题 → 提案 → 制作

Authority Class: EVIDENCE
Status: Review

本轮只更新示例原型，不修改 Curis 正式合同。不能将以下局部验收理解为完整 Curis 产品验收。

- 策略：账号经营页“调整策略”，编辑、差异确认、放弃、确认生效、历史版本；账号范围内向负责人提出调整请求进入同一流程。既有制作、权限、预算不自动变更。
- 灵感 / 选题：主题、内容形式、核心内容可编辑；讨论保留在当前对象会话，成果经整理和差异确认后才更新同一对象。旧版本保留，确认后可留在灵感、进入选题池或进入提案准备。没有账号先确认账号，不能直接开工。
- 参考：外部内容不改写，讨论决议存为备注。用于新选题时保留确切参考 ID 与备注；重复点击回到同一来源选题，不跳任意旧提案。
- 选题池：已转提案的选题继续保留，并能查看去向；提案反向返回来源选题。修改源灵感不覆盖已形成提案。
- 关注发现：交给研究员工会生成可查看的研究工作；填写演示研究结论后，结果回到来源选题。预置扫描信息明确为示例，不表示真实联网采集。
- 修复长图文被误判成9页图文、旧“未指定账号”备注、素材选择未落引用、研究工作点击原地跳列表、会话结果按钮未传入渲染器等问题。

### 本轮实际浏览器证据

| 操作链 | 实测结果 |
|---|---|
| 分文件：讨论 INS-1 → 整理 → 修改主题/长文章/核心内容 → 预览 → 确认 | 当前对象更新，确认前显示原内容与新内容 |
| 分文件：设置公众号品牌账号 → 形成 PROP-P1 → 确认交付 → 开工 | 创建 W-208，长文章7步骤、2,000–2,500字；未套9页图文 |
| 分文件：账号策略修改 → 差异确认 → 生效 | 发布节奏更新，显示修订1；截图 `_audit-20260917/r9-strategy.png` |
| 单文件：参考备注保存 → 用于新选题 | 原参考标题保留，准确来源 REF-1、讨论备注进入新选题 |
| 单文件：关注发现 → 研究工作 → 保存结论 → 选题池 | 可见已完成研究及对应选题结论 |
| 单文件：添加账号 → 管理 → 移出业务 | 新账号存在；移出后有“已移出”入口，不删除历史 |

可复跑：`node _verify-r7.js`、`node _verify-bi.js`。前者包括七区渲染、账号/关注/研究/来源/策略/灵感历史与取消/重复操作；后者检查BI筛选、时间、Unknown和跨平台。它们是本地状态检查，不代替浏览器。单文件由 `_build.js` 生成，禁止手动另改。

### 边界

AI讨论是明确的演示交互，不接模型、不生成真实研究结论；用户可编辑整理的成果再确认。除本地导入资产外，普通演示对象刷新回初始数据。真实扫描、下载发布包、发布与授权仍按先前范围保留演示，不当成功能开发失败。完整 Curis 宿主接入、真实执行与持久化另行验收；本轮未进行。

### 参考讨论补查
参考画廊、列表、详情统一使用「讨论这条」进入同一对象会话。讨论意见不会自动写入备注；用户通过「整理为参考备注」编辑决议并确认保存，原始参考不改写。提案的「参考与讨论备注」可查看关联参考的确认结论。
实际浏览器验证：两轮讨论 → 编辑决议 → 确认保存 → 参考详情显示 → 用于新选题 → 形成内容提案 → 提案显示结论 → 返回参考继续讨论（历史保留）。分文件版完成上述实测，单文件版同步重新构建。仍为演示会话，无模型调用；当前研究数据刷新后重置。

## Product UI Simplification — 本轮页面减法

范围仅限本目录原型；七区不变，不修改 Curis 产品 Authority、Runtime 或全局对话规范。

- 经营：单账号首层收拢目标、当前表现、负责人判断、下一步与检查时间；策略/节奏复用已有预览确认；资源讨论进入林岚会话；下一轮准备确认后进入既有 Work 列表，同范围同检查时间不重复建立。不会开启后台自动经营、发布或扩大权限。
- 整体经营：待决定与最近团队动态前置。动态明确为预置演示记录；供应、资源、工作与决定历史收在第二层。相关工作统计按当前账号范围，修正进行中状态被错误排到末尾的问题。
- 研究：日常主视图为选题池、参考与灵感、持续研究。提案在选题池的次级状态视图；关注来源和研究记录在持续研究内。原路由仍可进入参考、选题、提案详情，选题池改紧凑行列表。
- 制作：首层展示当前步骤、承担人、下一步、已有产物和当前步骤操作；依赖、输入版本、执行记录、交付规格与历史按需展开。流程调整仍在流程设置，原合并/拆分/QA/运行中阻塞规则未改。待生成或无版本产物不列作已有产物。
- 素材：内容组件直接引用原 KNOWLEDGE，显示已接受/候选与适用限制。引用组件可进入选题再到提案，不复制一份知识或自动晋升验证状态。

验证：`_verify-r7.js` 与 `_verify-bi.js` 通过；新增三主视图/六子路由、全部现有制作方法、单一高级调整入口、下一轮幂等/暂停阻止、知识引用检查。实际浏览器操作了账号切换、策略入口、下一轮确认与负责人会话、参考讨论、添加关注表单、制作步骤讨论、高级流程调整、内容组件→选题→提案。单文件版另外验证三个主视图、长文章制作与高级入口默认隐藏；所检查页面无控制台错误。两版同步构建。

边界：这些是示例产品交互验证；未接真实模型/平台/定时扫描，非后台持续经营验收。除本地导入素材外，演示操作数据刷新后重置。
