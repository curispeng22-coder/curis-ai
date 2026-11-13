# CURIS DESKTOP PRODUCT & DESIGN DIRECTION

> Authority Class: RESEARCH → RECOMMENDATION（重启 Final UI Master 之前的正式研究输入；非 Product Authority，不修改 Blueprint / Shell Contract / Visual Standard）
> Status: **COMPLETE**（基于 UI AUDIT A/B/C/D 四代证据 + GAP MATRIX + 全部 9 份竞品清单回填后的 Pattern Library；Synthesis 见 `CURIS_SYSTEM_COMPETITIVE_RESEARCH_SYNTHESIS.md`）
> Date: 2026-09-12
> 输入：`CURIS_CURRENT_UI_AUDIT.md`、`CURIS_PRODUCT_CAPABILITY_GAP_MATRIX.md`、`CURIS_UI_PROBLEM_REGISTER.md`、`CURIS_MISSING_CAPABILITY_REGISTER.md`、`CURIS_UI_EVIDENCE_CATALOG.md`、`CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md`（Frozen）、`CURIS_VISUAL_STANDARD_V1.md`（Frozen）、各 `CURIS_RESEARCH_*_FUNCTION_INVENTORY.md`
> 边界：不推翻 Frozen Product Structure（七区、Company OS、Four-Pane、原装组织）；产品模型变化必须走 Blueprint 优先的三文档流程。

---

## 0. 一句话方向

**Curis 的差异化在组织与经营语义层（没有竞品有对等物），落后在通用 AI 桌面产品层（竞品已全部标配）。下一轮 Final UI Master 的任务不是重新发明组织模型，而是给已有 Runtime 穿上 2026 年标准的产品外衣：对象化的员工、可视化的工作、可消费的结果、成熟的 Composer、完整的 Settings、安静的桌面级视觉。**

## 1. 产品层方向（Product）

### 1.1 应补（按优先级；每项 = Frozen 已要求 或 多产品共同验证 或 直接解决已登记缺陷）

| 优先 | 能力 | 依据 | 备注 |
|---|---|---|---|
| 1 | **Employee Detail / 完整员工工作站**（身份/组织关系/责任/能力/当前工作/进度/成果/对话/设置一体） | Structure Baseline §4 + Current P1 + D 代骨架已存在（D3） | 这是全产品最缺口的一张"脸" |
| 2 | **Work 进度可视化**（计划→步骤→当前动作→完成，参考 todo/plan 模式） | Z1/Z2/Z3；Manus task list、Devin plan pane 共同验证 | Runtime 的 Work/Task 已存在，缺投影 |
| 3 | **Result 消费面**（预览/版本/下载/引用/Evidence 溯源） | Current P1 + Claude Artifacts / Manus deliverables 验证 | Result→Evidence 是独有强项，必须可看 |
| 4 | **结构化 Composer**（输入/附件/模型或员工选择/访问权限/工作模式/执行者语义槽位） | X10 合同已 Frozen；D 代 08 页已实现语义槽位 | 合同在先，落实现 |
| 5 | **全局对象搜索 / ⌘K** | Current P1；全员竞品标配 | 与 D 代 `10-global-search.html` 衔接 |
| 6 | **完整 Settings IA**（个人偏好/公司设置/AI 与能力（模型/Provider/Skill/Tool/MCP/Connector）/权限与数据/运行与成本/通知/外观/快捷键/关于） | D 代 07-settings 骨架 + SETTINGS_MATRIX 竞品字段 | 字段级清单见 §3.7 |
| 7 | **Usage/成本面**（每员工/每 Work/每模型用量，读唯一 Usage Ledger） | RUNTIME ONLY→补产品面；Coze credits / Devin ACU / Cursor usage 验证 | 无新 Runtime，只加投影 |
| 8 | **权限政策面**（"这个员工能做什么"用户语言清单 + 授权/升级历史） | Z4 + Workbuddy 席位升级模式 | 与 Responsibility 模型天然契合 |
| 9 | **人才与能力市场语言**（浏览/分类/详情/安装/已安装，专家·技能·连接器三目录） | M-06；Workbuddy 140+ 专家/7 万+技能/连接器市场参照 | Curis 原装组织是差异点，发现侧需同等目录语言 |
| 10 | **通知中心**（结果就绪/需要决定/员工阻塞/会议开始） | 全员标配；CEO Desk attention 是数据源 | |
| 11 | **桌面壳能力**（全局快捷键、菜单栏入口、原生窗口质感、离线/连接态） | M-15；ChatGPT/Claude/Zcode desktop 参照 | Tauri 壳已有 sidecar 基础 |
| 12 | **Dark / 1024 / 无障碍** | M-16；多处 P2 债务 | Final UI Master 必须双主题出图 |

### 1.2 不应补（本阶段）

- 多租户/计费/Marketplace 开放生态/独立 Admin（v1 self-use 红线 + L2 Gate）。
- Voice、多真实员工 seat（未设计、非当前用户价值）。
- Computer Access 产品面（ADR-0046 已冻结路径：先 Runtime Delta Plan，不跳级）。
- 第二套组织模型、Workflow graph/DAG 编辑器、Operating Console（多次裁决禁止）。

### 1.3 Runtime 需要补 Product Surface 的清单（Runtime 存在、面缺失）

| Runtime 事实 | 缺的 Surface |
|---|---|
| 唯一 Usage Ledger（四层 scope 贯通） | 成本/用量页（§1.1-7） |
| Scope/授权/溯源 | 权限政策页（§1.1-8） |
| Responsibility routing / Handoff | 交接收件箱 / Handoff 流（B 代 Quick Panel 已有"当前交接"字段雏形） |
| Meeting advancement cycle | 会议生命周期可视化（进行中/待 CEO 决定/休会中） |
| 共识归档 / 公司记忆 | Memory 查看与编辑面（M-12，观察级） |
| parallel multi-Work（未实现） | 并行工作视图（依赖 Runtime 先行，观察级） |

### 1.4 空壳/薄壳 UI（存在但无内容深度，需做实）

- Utility 面板（B 代只有标题+预览+3 按钮，无元数据）。
- Employee Quick Panel 的"打开完整员工工作站"目标页。
- D 代 Settings / 全局搜索（IA 骨架，字段未填充）。
- 成果库 nav（无 Result 视图证据）。

### 1.5 Model / Skill / Tool / MCP / Provider 的组织方式（建议结构，非裁决）

- **用户语言三层**：能力（员工会做什么，自然语言）→ 模块（Skill/Tool/Connector，可安装对象）→ 连接（Provider/MCP/凭据，系统层）。用户默认只见第一层，第二层在员工详情与人才市场出现，第三层收进 Settings。
- 员工详情显示"能力卡"（Curis 用户语言 P1），点开才暴露 Skill/Model 绑定；Settings 承担 Provider/Key/MCP 配置。
- 对照：Coze 的"技能=插件+工作流+知识库三类挂载"（O2）证明绑定关系必须是显式对象；Curis 已有 Employee Capability Binding，需给用户语言。

### 1.6 Multi-Agent 如何进入真实工作流

- 不引入画布编排（Coze O1 是工具思路，与 Curis 组织思路相悖——Curis 的"编排"是组织结构+责任，不是节点图）。
- 可迁移的竞品模式（仅记录为候选）：场景路由的用户解释（让 CEO 看懂"为什么这件事派给了 TA"）、节点级身份的故障域隔离（员工级调试/重跑）、规则安全阀（O10：硬规则优先于自动路由——对应 Curis only-on-exception 的用户语言化）、单点旁路对话（P7：对单个员工直接开小会，B 代 Quick Panel"直接对话"已是此模式）。
- 落点：Leader 分工画面（谁/做什么/为什么/状态）、Handoff 契约卡、会议决议→Work 的可视链。

## 2. 页面层方向（Page）

> 每页给出：结构 / 关键字段 / 动作 / 状态。七区结构不动；以下为 Final UI Master 的每页设计要求。统一状态规范：每页必须设计 Normal / Empty（首次）/ Empty（用尽）/ Loading / Error / Needs-CEO 六态（D 代 11-states.html 已立骨架）。

### 2.1 全局壳（Desktop Shell）

- 结构：左侧导航轨（七区，D 代六区+设置即事实标准）+ 每区四 Pane（Context 可收起/Main/Utility 按需/对话与 Composer 内嵌于工作面）。
- 新增全局件：⌘K 搜索（对象+动作）、通知中心（右上）、助理浮层（保留 Phase B 可拖动浮层，但内部重构为对话式，见 §3.5）、设置入口（左下头像菜单）。
- 桌面化：去掉网页后台痕迹（浏览器式顶栏、面包屑堆叠）；Pane header 承担层级（D 代已合规：无全局 Topbar）。

### 2.2 CEO 工作台

- 结构：今日简报（3-5 条有优先级的"今天要注意什么"）→ 需要你的决定（Decision 卡队列）→ 正在运行（员工工作行）→ 最新结果（Result 引用行）→ 公司脉搏（收进侧栏或次级 tab，不再六卡平铺）。
- 字段：简报项=事实+影响+来源员工+时间+动作；决定卡=P7 包（背景/选项/建议/Evidence 引用）。
- 空态：单一主行动（创建公司/第一条业务）+ 一句叙事；禁止 0 值统计卡与六遍"等待启动"。
- 动作：处理/稍后/转交某员工/看证据。

### 2.3 业务空间

- 结构：业务卡/行（名称/状态/本周一句话/Workspace 数）→ 进入 Workspace = 四 Pane 工作面（B 代已对）。
- 修：门户页去掉统计卡联排与双重空态；"装修中"并入统一状态机。

### 2.4 组织中心

- 保持公司版图/员工目录两 Tab（已验收）。
- 员工行 = D 代 emp-row 两行结构（头像/姓名+岗位/当前职责/状态）；点击进 Employee Detail（§2.5）。
- 补：Search/Filter、空岗显示、Leader 标识。

### 2.5 Employee Detail / 工作站（新核心页）

- 结构（单页双列或 Tab）：
  1. Header：头像/姓名/岗位/部门/状态（工作中·<desc>/空闲/阻塞·<cause>）/入口动作（对话/派工作/更多）。
  2. 责任区：长期责任/当前责任/在什么 Scope。
  3. 能力区：能力卡（用户语言）→ 展开 Skill/Model 绑定（第二层）。
  4. 当前工作区：Work 卡（计划步骤+当前动作+进度+所属 Workspace+预算）。
  5. 最近结果区：Result 引用行（标题/状态/Evidence 数/查看→Utility）。
  6. 对话区：与该员工的 Conversation（复用共享 Composer）。
  7. 设置区：模型偏好/权限/通知。
- 状态：缺模型/缺 Holder 必须 truthful 显示（Phase A.1 决定）。

### 2.6 工作中的员工（Work 进度）——跨页组件

- Work 卡三段：计划（步骤 checklist）/ 当前动作（工具级细节可折叠，参考 Z2）/ 结果引用。
- 阻塞/需 CEO：卡片变 Decision Banner（--ui-warning 指示线，不大面积铺色）。
- 完成：Result 行 + 通知。

### 2.7 Settings（字段级最低清单）

| 节 | 字段 |
|---|---|
| 个人偏好 | 姓名/头像/语言/主题（Light/Dark/Auto）/启动项 |
| 公司设置 | 公司名/品牌/行业/档案（已有本地草稿，接真数据） |
| AI 与能力·模型 | Provider 列表（名称/Endpoint/凭据状态(已连接·需授权·未连接)/默认模型/健康）；模型列表（Name/Model ID/Vision/Reasoning/Context/启用/默认/成本）；每员工默认模型 |
| AI 与能力·技能 | 已装 Skill（名称/类型/版本/来源/绑定员工/启用）；Skill 详情（触发方式/参数/权限）；连接器（状态/授权/数据范围） |
| AI 与能力·MCP | server 列表（URL/命令/凭据/启用/工具清单/健康） |
| 权限与数据 | 员工执行授权默认值/工具白名单/升级规则/数据保留/隐私 |
| 运行与成本 | 用量总览（按员工/模型/业务）/预算上限/账单历史 |
| 通知 | 结果就绪/需要决定/阻塞/会议；渠道（系统/邮件/飞书升级） |
| 快捷键 | ⌘K/全局唤起/常用动作 |
| 关于 | 版本/更新渠道/许可 |

### 2.8 会议 / 资料库 / 经营洞察

- 三区均已有 **已验收 Figma 基线**（214/187/172 系列）——Final UI Master 直接消费这三套基线做视觉统一翻新，不重新发明 IA。审计中 A 代对应页全部废弃。

## 3. 视觉层方向（Visual）

### 3.1 Token 裁决（前提）

- **Accent：以 Frozen `CURIS_VISUAL_STANDARD_V1`（Direction D / `#806BE5`）为准**；`#32f08c` 条款已被 V1 取代（Pointer #4 明确）。实现与 D 代的绿色是未迁移债务，不是第二选择。若 CEO 想重选 accent，走 V1 修订，不在页面层各自为政。
- 建立唯一 token 表（V1 已给出 Light/Dark 中性阶全表）：Final UI Master 出图只允许引用 token，禁止页面私有值（D 代已实践此纪律，延续）。

### 3.2 视觉方向

- 延续 D 代已验证的方向：**安静、信息密集、低表面复杂度**（Linear/Notion 学派），层级靠排版/字重/灰度/分隔，不靠色块；语义三色只做小面积信号（文字/图标/指示线）。
- 修正 D 代的不足：信息密度不能退化为"标签堆叠"——对象要有**视觉身份**（头像/图标/状态点/元数据行的固定节奏），参考 B 代对象卡与 Quick Panel 的密度感。

### 3.3 具体规范基线（Final UI Master 出图起点，全部引用 token）

| 项 | 规范 |
|---|---|
| 页面标题 | 20px/600（B 代尺度，弃 A 代 28-32 营销尺度） |
| 正文 | 13px；辅助 12px（下限 12px，Frozen D4） |
| 密度 | 列表行高 40-44px；卡片 padding 16px；Pane gap 1px 分隔线（不做卡片套卡片） |
| 卡片 | 仅用于真聚合容器；radius 8-12px；边框 1px `--ui-line`；阴影仅浮层（Popover/Drawer/Modal 用 shadow，页面内平面） |
| 状态色 | success/warning/danger 小面积信号 + 左指示线；状态词典统一（进行中/制作中合并；禁"装修中"） |
| 主按钮 | Light=深实心、Dark=accent（Frozen 既定）；每屏至多一个主按钮 |
| Material | 不用玻璃拟态/大模糊；深色 `#1a1c1f` 底 + `#222529` 面（V1 表） |
| Motion | 150-250ms ease-out；Pane 展开/收起、Drawer 滑入、Result→Utility 转场三处足矣；工作动画集中在状态点（呼吸/进度条），不做装饰动画 |
| Activity 表达 | 员工状态点（空闲/工作中·desc/阻塞）+ Work 卡进度 + 简报时间线——三层即可，不要流水账 |

### 3.4 Conversation / Composer 规范

- Composer 语义槽位（Frozen X10）：输入 / +添加（附件、引用）/ 访问权限 / 工作模式 / 执行者（Agent 语义，不是模型名）/ 发送。
- 回复结构化：文本 + 可选卡（Result 引用行、Decision Banner、Evidence chip）；工具/执行细节默认折叠为"做了什么"摘要行，点开看过程（Z2 降密度模式）。
- 禁止：面板内嵌统计卡组（C3）、常驻免责声明、内部术语。

### 3.5 空态/错误态规范

- 空态 = 主题插画或结构示意 + 一句"这里会发生什么" + 单一主行动；全产品空态文案长度 ≤ 2 行。
- 错误态 = 中文解释 + 已尝试什么 + 重试/返回/求助三路径；禁止裸英文（C8）。

### 3.6 桌面感清单

原生窗口控件对齐、菜单栏（macOS）接入、全局快捷键唤起助理、Dock 徽标（待办/通知）、离线态、Keychain 凭据态显示。

## 4. 优先级路线（给 Final UI Master 的执行顺序建议）

1. **R1 基础**：Token 统一（V1 迁移完成）+ 全局壳（七区导航 + 四 Pane + ⌘K + 通知中心 + 设置入口）+ 状态机词典。
2. **R2 脸面**：Employee Detail + Work 进度组件 + Result 消费面 + 结构化 Composer（四件套是同一个生态）。
3. **R3 面貌**：CEO 工作台重做 + 业务空间门户去后台化 + 会议/资料库/经营洞察按已验收 Figma 基线视觉翻新。
4. **R4 深度**：Settings 全量 + Usage 面 + 权限政策面 + 人才市场语言。
5. **R5 桌面**：桌面壳能力 + Dark/1024/无障碍收口。

每轮 R 必须双主题（Light/Dark）+ 1440/1280/1024 三宽出图。

## 5. 风险与开放问题（需 CEO/Product Gate）

1. Accent 是否维持 V1 `#806BE5`（Frozen 现行）——建议维持并完成迁移，除非 CEO 重启视觉方向评审。
2. 人才市场是否引入外部目录规模（Workbuddy 式 7 万技能）——涉及 Marketplace L2 Gate，本方向只建议"产品语言"，不建议开放生态。
3. Automation（M-11）与 Memory 面（M-12）是否进入下一 Initiative——研究建议 OBSERVATION 级，等 R1-R3 落地后验证用途。
4. 四套 IA 资产的退役标记需 Pointer 登记动作（G-02/G-03）。

## 6. 与既有 Authority 的关系声明

- 本方向消费且不修改：Structure Baseline（七区/组织模型）、Shell Contract（四 Pane/Shared Pattern/Composer 槽位）、Visual Standard V1（token）。
- 本方向建议新增的产品对象（Employee Detail 页、Work 进度组件、通知中心、Settings 节、Usage 面）均为 **Surface 层**，不新增 Runtime Primitive；凡需新 primitive/schema 的（如通知模型、自动化对象）必须先 Architecture Review + 正式 Issue。
