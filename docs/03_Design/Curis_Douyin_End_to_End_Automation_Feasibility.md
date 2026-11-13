# Curis 中国抖音端到端自动经营闭环 — 可行性研究（DOUYIN END-TO-END AUTOMATION FEASIBILITY）

**阶段**：DOUYIN END-TO-END AUTOMATION FEASIBILITY（第二阶段专项 · 仅研究中国抖音）  
**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**不修改**：Product Blueprint / Frozen Shell / Frozen Shared Patterns P1–P7 / XHS Instance / RD Instance / Runtime / 正式代码 / Connector 实现  
**只研究**：中国抖音（open.douyin.com 开放平台）。**TikTok 国际版不混入**。  
**铁律**：官方能力优先验证；**不得因第三方 SaaS（蝉妈妈/飞瓜/易媒等）能做到，就推断抖音官方 API 一定允许 Curis 做到**。  
**输入**：首轮 TTK 三份文档、`CURRENT_STATE.md`、Frozen P1–P7、外部官方源（open.douyin.com 文档 / 抖音生活服务 AIGC 规范 / 网信办 AI 标识办法）+ 生产工具官方文档（CapCut API / 即梦火山视觉 API / 可灵 / HeyGen MCP / Runway MCP）。  
**专家角色**：UiDesigner（可行性研究，非高保真 / 非 Prototype / 非开发）

> 标注约定：`OFFICIAL`=抖音开放平台官方事实；`POLICY`=平台政策/法规；`TOOL`=生产工具官方能力；`INF`=基于官方的推断；`GAP`=当前缺口。

---

## 0. 自动化等级定义（7 类，全文档统一）

| 代码 | 等级 | 含义 |
|------|------|------|
| **A0** | FULLY_AUTOMATABLE | 配置完成后稳态无人介入，端到端自动跑 |
| **A1** | AUTOMATABLE_WITH_REVIEW | AI 执行；进入下一步前需一个**人工审核/批准门禁**（Artifact Review） |
| **A2** | HUMAN_IN_THE_LOOP | AI 提议/辅助；**人做决定/动作** |
| **A3** | CEO_DECISION_REQUIRED | 需触发 Frozen P7 CEO Decision Package（经营/风险判断） |
| **A4** | TOOL_ASSISTED_MANUAL | 人做主工作；Tool Capability 仅辅助 |
| **A5** | NOT_AUTOMATABLE_BY_API | 官方 API/平台当前**不提供**该能力 |
| **A6** | BLOCKED_BY_POLICY | 平台政策**禁止**自动化此行为 |

---

## J. 最终必须回答（前置结论，供 Review 直接裁定）

### J1. Curis 能否实现中国抖音端到端自动经营闭环？

**结论：CONDITIONAL（条件性）。**

- **MVP AUTOMATION LOOP（人工审核门禁下的半自动闭环）= 可行（YES）**：在拿到官方授权 + 接好生产工具 + 保留「发布前人工审核门禁」的前提下，Curis 可以把「选题→脚本→AI 生成/剪辑→审核→发布→数据观察→复盘反哺」跑成 AI 主执行、人只在定义好的审核/决策门禁点介入的自动闭环。
- **FULL AUTOMATION LOOP（无人值守全自动闭环）= 不可行（NO）**：① 抖音**严打「AI 托管类账号」**，全自动托管 = 封禁，仅「AI 辅助 + 人工审核发布」安全（POLICY GAP）；② 官方发布 API **无定时发布参数**（A5 GAP）；③ 完播率等深度指标仅经营号授权层可得（ACCOUNT GAP）。因此「完全无人值守」既违规也缺能力。

> 一句话：Curis 能建「AI 执行 + 人在关键门禁点确认」的端到端**可自动化**闭环，但不能建「无人值守全自动」闭环。

### J2. 如果可以，需要哪些条件？

1. **开发者账号 + 应用审核**：企业开发者优先（配额/高级权限更高）；应用审核 2–3 工作日；回调域名需 https 且非 IP/localhost。
2. **OAuth2.0 用户授权**：access_token（用户级，2h）/ client_token（应用级）；scopes：`video.create.bind`（发布）、`video.comment`（评论）、`video.data`（基础数据）、`im.direct_message`（私信，企业号）、`video.data.bind`（经营号深度数据）。
3. **企业号认证 + 经营抖音号授权**：评论置顶、私信 receive_msg、完播率深度数据均依赖企业号/经营号授权。
4. **Webhook 回调**：配置 https 回调地址并订阅 `create_video` / `authorize` / `unauthorize` / `receive_msg`(enterprise.im) / `enter_im` 等事件。
5. **生产工具连接**：CapCutAPI（桌面草稿）、即梦（火山视觉 API AK/SK）、可灵（AK/SK 或 kling.ai Key）、HeyGen（MCP/OAuth）、Runway（Enterprise MCP）。
6. **AIGC 披露合规**：生成内容须按《人工智能生成合成内容标识办法》(2025-09-01) + 抖音《AIGC 创作规范》(2026-04-22) 做 AI 标识。
7. **发布前人工审核门禁（非可选）**：为满足「AI 辅助 + 人工审核发布 = 安全」，发布动作前必须有人类审核批准（A1 门禁）。

### J3. 哪些环节永远/当前必须有人参与？

| 环节 | 是否必须有人 | 原因 |
|------|--------------|------|
| 发布前审核/批准 | **永远必须（政策强制）** | 全自动托管封禁；人工审核发布才安全 |
| CEO 高风险决策 | **必须（触发 P7）** | 投放预算 / 版权风险 / 合规风险 / 对外承诺 |
| 选题方向最终拍板 | 建议人确认（A2） | 战略/人设判断，AI 可提议 |
| 真实拍摄（非全 AI 生成） | 必须（A4） | 实拍无法 API 化 |
| 成片最终审美判断 | 建议人确认（A2） | 品牌声音/成片质量 |

### J4. 当前 Curis 距离完整闭环还缺什么？

- 无抖音 Publishing / Engagement / Analytics Connector（未建）。
- 无官方 API 集成（OAuth / scope / 应用 / 企业号授权全缺）。
- 无生产工具连接器接入运行时（CapCut / 即梦 / 可灵 / HeyGen / Runway 均未接）。
- 无完播率数据通路（需经营号授权 + 小程序层）。
- 无定时发布变通方案（官方缺能力）。
- 无 AIGC 披露 UI / 运行时。
- **TTK Instance Spec 尚未批准**（仍 REVIEW REQUIRED）→ 无 Video / Script / Analytics 运行时对象模型。

### J5. 最小可行真实自动闭环：MVP AUTOMATION LOOP = ?

```
选题(AI提议 → 人确认 A2)
 → 脚本(AI起草 → 人编辑 A2 / 品牌预检 A1)
 → AI生成素材 + CapCut 剪辑草稿(A1 需版权/披露复核)
 → 审核(Artifact Review A1 · 人批准发布门禁)
 → 发布(官方 create_video · 批准后触发 A1，非无人值守)
 → 数据观察(自动拉取计数 A0 · 完播率需经营号 A0+AccountGap)
 → 复盘(自动反哺选题库 A0 + 可选深度解读 A2)
互动：评论/私信 自动分类 → AUTO_REPLY(FAQ) / EMPLOYEE_REVIEW(敏感) / CEO_DECISION(升级)
```
人在：确认选题、编辑脚本、批准发布门禁、CEO 高风险；其余 AI 自动。

### J6. 满足什么条件后，可以从 MVP 升级到 FULL AUTOMATION LOOP？

1. 官方提供定时发布能力，或可接受「到点即时发布」批处理变通（解除 A5）。
2. 完播率深度数据通路上线（经营号授权完成，解除 Account Gap）。
3. 互动 scope 全接线（评论仅自己视频、私信仅企业号均已配置）。
4. AIGC 披露自动化且合规。
5. **平台政策放宽对无人值守的判定**，或 Curis 保留轻量人工确认（当前 FULL 因「托管封禁」不可达）。
6. 所有 Connector 建成、测试、fail-closed。

### J7. 第一轮 Product Model 是否需要因此修改？

**核心 KEEP；4 处需 MODIFY（非 REJECT）。** 详见 §K。

---

## A. 完整闭环逐节点自动化等级

闭环（沿用首轮 Proposal §A 工作链）：

| # | 节点 | 等级 | 官方/事实依据 |
|---|------|------|---------------|
| 1 | 选题/热点 | **A2**（AI 提议 + 人确认）；趋势监控 = A0 System Activity | 官方 OpenAPI 无「热词」端点；巨量算数属独立体系（非 open.douyin.com scope）。选题方向 = 策划员工责任 |
| 2 | 脚本 | **A2**（AI 起草 + 人编辑）；品牌预检可 A1 | 编剧责任；脚本结构/钩子/品牌声音 AI 去不掉 |
| 3 | 素材准备 | **A4**（实采）+ **A1**（即梦 AI 生成需版权/披露复核） | Asset 管理 + Tool Capability |
| 4 | 拍摄/AI 生成 | **A4**（实拍）/ **A1**（AI 生成需版权/披露复核） | 即梦/可灵/HeyGen/Runway（TOOL） |
| 5 | 剪辑 | **A1**（CapCut 草稿自动 + 制作人成片判断）/ **A2** 终剪 | 剪映/CapCut = Tool Capability（非渲染） |
| 6 | 审核 | **A1** AUTOMATABLE_WITH_REVIEW（Artifact Review Request） | 合规/品牌/版权判断留人；AI 预检 |
| 7 | 排期 | **A1**（计划自动）**但定时实际发布 = A5** | 官方 `create_video` **无 schedule_time**；定时发布仅 TikTok 国际版第三方工具有 |
| 8 | 发布 | **A1**（审核后触发自动发布）/**A6** 若无人值守 | 官方 `upload_video`+`create_video`（Scope `video.create.bind`）支持；但**全自动托管封禁** → 必须有人工审核门禁 |
| 9 | 数据观察 | **A0**（计数 `/video/data/`）/ 完播率 **A0+AccountGap**（需经营号 `video.data.bind`） | OpenAPI 层仅计数；完播率仅小程序经营号授权层；2 秒跳出/平均观看时长官方 API 未确认 |
| 10 | 复盘 | **A0**（自动反哺选题库）+ **A2** 可选深度解读 | System Activity |
| 11 | 二次利用 | **A1**（推荐）+ **A2**（多平台分发运营） | 矩阵/一条多平台 |

**结论读数**：11 节点中 A0×4、A1×5、A2×多（混合）、A5×1（定时发布）、A6×1（无人值守发布）。即「AI 主执行 + 人审核门禁」的 MVP 闭环可达；「无人值守 FULL」因 A5 + A6 不可达。

---

## B. 官方能力优先验证（4 类：内容 / 互动 / 数据 / 输入）

> 仅列 open.douyin.com 官方事实；第三方 SaaS 能力**不**作为官方 API 可达性证据。

### B1. 内容发布（Content）
- `POST /api/douyin/v1/video/upload_video/`（Scope `video.create.bind`，需申请权限 + 用户授权）✅ OFFICIAL
- `POST /api/douyin/v1/video/create_video/`（同 Scope）✅ OFFICIAL
- 支持话题 / @用户 / 小程序 / POI 锚点；视频限制 16:9、720p+、mp4/webm、≤4G、≤15min ✅ OFFICIAL
- 创建后平台审核（期间仅自己可见）✅ OFFICIAL
- **定时发布（schedule_time）：官方 `create_video` 无此参数** ❌ A5（仅 TikTok 国际版第三方 blog 提及，不混入中国抖音结论）
- 删除视频 / 查看审核状态 / 发布回执：官方有 ✅ OFFICIAL

### B2. 互动（Interaction）
- 评论：Scope `video.comment`（需「互动管理」权限）；`videoCommentListGet` / `videoCommentReplyListGet` / `videoCommentReplyPost` / `videoCommentTopPost`（置顶仅企业号）✅ OFFICIAL
- **限制：只能回复授权用户自己发布的视频** ⚠️ OFFICIAL
- 私信/群聊：Scope `im.direct_message` 等（需用户授权）；`receive_msg` 事件**要求当前抖音用户是企业号** ⚠️ OFFICIAL
- Webhook 事件：`create_video` / `authorize` / `unauthorize` / `receive_msg`(enterprise.im) / `enter_im` / `dial_phone` / `website_contact` / `personal_tab_contact` ✅ OFFICIAL（IM webhook 需配置回调 + 订阅）

### B3. 数据（Analytics）— 两层
- OpenAPI `/video/data/`（Scope `video.data`）：返回 `play_count` / `digg_count` / `download_count` / `share_count` / `forward_count` / `comment_count` ✅ OFFICIAL **不含完播率/2 秒跳出/平均观看时长**
- 小程序「短视频详细数据」（Scope `video.data.bind` / 经营抖音号授权）：返回 `item_completion_rate`（完播率）/ `item_last_frame_watch_cnt` / `item_vv` / `item_uv` 等 ✅ OFFICIAL（需经营号授权）
- 数据时效：用户首次授权后**次日**才产生全部数据；视频数据查询限 30 天内创建 ✅ OFFICIAL
- 巨量引擎（Ocean Engine）= 营销/投放数据，非内容经营数据（独立体系）

### B4. 输入（Input）
- OAuth2.0：access_token（用户级）/ client_token（应用级），2h 有效期 ✅ OFFICIAL
- Webhook 回调：需 https、非 IP/localhost、订阅事件 ✅ OFFICIAL
- 开发者资质：个人 vs 企业（企业 50 应用/高配额/高级权限）；企业号认证获「企业号开放能力」✅ OFFICIAL

---

## C. 打通条件（摘要，详见 Doc 3 `Curis_Douyin_Automation_Requirements.md`）

开发者账号 / OAuth / Scope / 企业资质 / 白名单 / 配额 / Webhook / AI 披露 八项，Doc 3 逐条展开。

---

## D / E / G. Connector 与生产能力矩阵

详见 Doc 2 `Curis_Douyin_Capability_Matrix.md`（Publishing Connector / Engagement Connector / Production Automation 三张矩阵）。

---

## F. Analytics 反馈环（要求，详见 Doc 3）

**禁止无真实数据生成 AI 复盘**：AI 复盘/反哺必须基于真实拉取的平台回执（A0 数据通路），不得用 mock/估算生成「复盘结论」。数据路径、时效、字段依赖见 Doc 3 §F。

---

## H. 重新验证 Handoff（情况 A 真 Frozen Handoff vs 情况 B Artifact Review）

| 场景 | 归类 | 判定 |
|------|------|------|
| 策划完成 → 脚本接手（责任真正转移） | **情况 A：真 Frozen Handoff (P5)** | 责任 Owner 从策划转移到编剧，用 Handoff Event |
| 制作把成片送审核 | **情况 B：Artifact Review Request** | 制作员工**仍持** Video 制作责任；审核员工只做合规/品牌/版权检查，**不转移责任**，保持 Instance Candidate（与 RD 一致） |
| 审核通过 → 发布 | 审核责任完成 + 发布责任启动（可 Handoff） | 审核责任闭合后，发布运营接手 = 情况 A |
| 发布前人工审核门禁 | **情况 B（A1 审核门禁）**，非 Frozen Handoff | 政策强制的发布批准点，是 A1 门禁，不是责任转移 |
| 高风险发布（投放/版权/合规） | **A3 CEO Decision (P7)** | 高风险触发 CEO，独立于 Handoff/Artifact Review |

**结论**：本阶段研究**确认首轮 Proposal 的「审核 = Artifact Review（B 类，不升格 Frozen P5）」正确**，且与 RD 保持一致；发布门禁是 A1 审核点而非 Handoff。CEO Decision 始终独立于 Handoff（P7 ≠ P5）。

---

## I. 缺口地图（摘要，详见 Doc 4 `Curis_Douyin_Automation_Gap_Map.md`）

七类缺口（Product / Connector / Runtime / Account / Platform / Policy / Tool），Doc 4 逐条列严重度与 MVP/FULL 阻断关系。最关键三项：
- **Platform Gap**：官方无定时发布（A5）。
- **Account Gap**：完播率仅经营号授权层（MVP 可先用计数，FULL 需经营号）。
- **Policy Gap**：全自动托管封禁（FULL 不可达的根因）。

---

## K. 第一轮 3 份文档处理建议（KEEP / MODIFY / REJECT）

| 文档 | 建议 | 理由 / 需改点 |
|------|------|----------------|
| `Curis_TTK_Workspace_Reference_Research.md` | **KEEP** | 外部证据底表（S1–S20）扎实、来源类型标注规范。仅建议**增补**官方 open.douyin.com 源登记（S21+：发布/评论/数据/Webhook/OAuth 官方文档），为本次可行性提供官事实锚点（属 additive，不改原结论） |
| `Curis_TTK_Workspace_Product_Model_Proposal.md` | **MODIFY** | 核心模型（Video 对象 / Pipeline 默认面 / 6 责任角色 / Artifact Review / P7 / System Activity Analytics）**全部 KEEP**；需补 4 处（非推翻）：① 发布门禁为**政策强制**非可选（§F/§A 审核 + 发布 gate）；② 「排期可自动」需限定为「计划自动、定时实际发布=A5 官方缺能力」（§A/§C）；③ 完播率字段依赖**经营号授权**（Account Gap，§B/§I）；④ 互动需补 Engagement Connector 范围（评论仅自己视频、私信仅企业号，本阶段新增 E 节） |
| `Curis_TTK_vs_XHS_Reuse_Matrix.md` | **KEEP** | 12 维复用边界仍成立；其「排期视图 RESERVED」已预判排期非默认，与本次 A5 发现一致。仅建议对齐 Proposal 上述 4 处 MODIFY（矩阵 #3/#7/#11 行加注官方缺口） |

> **无 REJECT**：首轮方向（Video 核心 / Pipeline 默认 / 不抄 XHS）经本轮官方能力验证后**基本通过**，仅需局部 MODIFY 以纳入官方 API 事实边界。

---

**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**下一步**：待 Review 批准后，方可进入「TTK Instance Spec 固化 / Connector 设计 / 高保真」阶段（不在此轮）。

**UI Designer** · 2026-08-15 · RESEARCH ONLY（未修改任何权威文档）
