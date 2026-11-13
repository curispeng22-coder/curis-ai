# Curis · Multi-Channel Architecture Review

> **状态**：CONTENT × CHANNEL ARCHITECTURE REVIEW REQUIRED
> **类型**：Reference Only · 架构复盘（非权威）
> **配套**：`Curis_Content_Production_Channel_Operations_Model.md`、`Curis_Canonical_Content_Channel_Variant_Model.md`、`Curis_AiToEarn_Architecture_Review.md`

---

## G. 平台差异模型（同一 Canonical Video 进入不同平台后的变化）

> 原则：**不要为了统一而抹平平台差异**。差异是 Channel Variant 模型存在的根本理由。

| 维度 | Douyin（中国抖音） | XHS（小红书） | TikTok（国际） | Bilibili（B站） | YouTube |
|---|---|---|---|---|---|
| **首选 ratio** | 9:16 | 9:16（3:4 / 16:9 兼容） | 9:16 | 16:9（支持竖屏） | 16:9（Shorts=9:16） |
| **时长上限** | 15 min | ~15 min | 3 min（国际） | 5 小时 | 120 min（长） / 60s（Shorts） |
| **分辨率上限** | 720p+ | 1080p+ | 1080p+ | 4096×2160 (4K) | 4K/8K |
| **edit 差异** | 竖屏原生、原声强 | 竖屏、封面 3:4 独立 | 竖屏、海外音乐库 | 横屏、可遮幅、弹幕位 | 横屏、可章节/字幕轨 |
| **title/caption 上限** | ≤55 字 | ≤20 字 | ≤150 字 | ≤80 字 | ≤100 字 |
| **cover** | 可选 | 必填 3:4 (1242×1660) | 可选 | **必填**（上传封面接口） | 可选 ≥1280×720 <2MB |
| **hashtag** | ≤5 | ≤5 | ≤5 | 逗号分隔 ≤200 | ≤15 |
| **music** | 原声强依赖 | 弱 | 海外曲库 | 可选 | 可选 |
| **copyright** | 无显式字段 | 无 | 无 | **必填**（原创/转载） | 无（但音乐版权分离） |
| **AI disclosure** | 网信办 6 类标签 + 生活服务 AIGC 规范 | 社区 AIGC 规范 | 平台合成媒体政策 | AIGC 内容标注要求 | "altered or synthetic" 标注 |
| **moderation** | 平台审核（发布后先仅自己可见） | 社区公约 + 原创性 | 机器+人工 | 投稿审核 | 机器+人工+年龄限制 |
| **scheduling（定时发布）** | ❌ 官方 API 无 schedule 参数 | ❌ 官方未确认 | ⚠️ 第三方工具支持 | ❓ API 未确认（Studio 有） | ✅ `publishAt`（须 private） |
| **engagement 原语** | 评论/赞/收藏/分享 | 评论/赞/**收藏**/分享 | 评论/赞/分享 | 评论/**弹幕**/**投币**/收藏/分享 | 评论/赞/订阅/分享 |
| **analytics 深度** | OpenAPI 仅计数；完播率仅**经营号授权层** | 创作中心（含完播） | 创作者后台 | 投稿效果管理 | **Analytics API 丰富** |

**关键不可抹平点**：
1. **scheduling 能力不平等**：YouTube 原生支持 `publishAt`，Douyin 官方 API **缺失**定时发布，XHS/B站未确认 —— 跨平台「统一排期」必须由 Curis 侧或各 Connector 分别实现，不能假设平台都支持。
2. **copyright 字段**：Bilibili 强制要求，其他平台无 —— 必须在 Variant 层表达。
3. **AI disclosure 字典不同**：各平台标签类型/触发条件不同，由政策层维护。
4. **analytics 深度差异**：完播率等深度指标的可得性随平台/账号类型（经营号/企业号）剧烈变化。
5. **engagement 原语差异**：B站弹幕/投币、XHS 收藏是平台特有互动，Channel Variant/Engagement 模型必须可扩展。

**结论**：Channel Variant 模型是**强制**而非可选。统一的「一个 Video 发全网」必须经由 N 个 Variant 各自适配。

---

## B/E 深化指引（详见 Model 文档 §3 / §6）

- 两类 Workspace（Production 平台无关 / Channel Ops 每平台）符合 Curis「Professional Workspace + Employee Responsibility + Capability Provider」。
- Target Channels 前置生成 Production Requirements，是两者的契约点。
- Video Production 默认面 = Production Pipeline；Channel Operations 默认面推荐 Mixed Operations Surface（Publishing Queue + Engagement Inbox + Performance）。

---

## 7. 七个必答问题（最终结论）

**Q1. Video Production 是否独立于平台？**
> **YES。** Video（及 Note）是跨平台 Company/Business 级 Canonical Content，由 Video Production Workspace 以平台无关方式生产，不属于任何单一渠道 Workspace。

**Q2. Douyin Operations 的核心对象是什么？**
> **Channel Variant + Publication。** Douyin Operations Workspace 拥有该平台的 Variant（平台特化适配）、Publication（真实发布记录）、以及挂在 Publication 上的 Engagement 与 Analytics。Canonical Video 只是它的输入（Intake），不是它拥有的对象。

**Q3. XHS 未来是否支持 Note + Video？**
> **YES。** XHS 已支持视频笔记（9:16/3:4/16:9，≤15min）。未来 XHS Channel Operations 应同时接受 `Canonical Note → XHS Note Variant` 与 `Canonical Video → XHS Video Variant`。当前 Approved XHS Instance（Note 首版）不改，但概念上 XHS = Channel Operations Workspace，Content Type 是其参数。

**Q4. Canonical Content 与 Channel Variant 如何关联？**
> **1 Canonical Content → N Channel Variants（每目标平台一份）。** Variant = 平台特化适配（ratio/duration/edit/caption/cover/hashtag/music/disclosure/policy_result/publish_config），由 Production Result 派生。关系见数据模型文档 §10。

**Q5. Publication / Engagement / Analytics 归属哪里？**
> **Publication 独立于 Canonical Content（1 内容 → N Publications）；Engagement 与 Analytics 挂在具体 Channel Publication 上**（per-platform 真相源）。Canonical Content 仅持有跨平台 rollup 视图。

**Q6. AiToEarn 在 Curis 中最合适的定位？**
> **主：Reference Implementation（参考实现）；次：Multi-platform Distribution Provider 设计灵感。**
> 非「直接接入的 Channel Operations Capability Provider」—— 因其 content+channel 混淆、浏览器插件互动自动化触碰封禁风险、Relay 凭据代理不合 Curis 安全模型。详见 Doc 4。

**Q7. 下一步应先设计哪个？**
> **先建立 Contract，再分别设计。**
> 不应先设计 Video Production WS **或** Douyin Channel Ops WS 其中之一，因为二者通过「Target Channels 前置 → Production Requirements」与「Channel Variant 契约」耦合。正确顺序：**先定义共享对象（Canonical Content / Channel Variant / Publication 模式 + 跨 WS 交接协议）= Contract**，然后两个 Workspace 基于同一 Contract **并行分别设计**。

---

## 对既有研究的处置：KEEP / MODIFY / REINTERPRET / REJECT

### (1) TTK Product Model（首轮 3 份之一）
> **判定：REINTERPRET（重新解释）**

- **保留**：Video 核心对象、Script 子对象、Production Pipeline 责任链、6 责任角色、Artifact Review 审核机制、CEO Decision 真实场景、DO NOT COPY 清单 —— 这些对象与机制**可复用**，但需**重新语境化**。
- **重新解释（核心修正）**：首轮「TTK Workspace = Video Production（默认面=Pipeline，抖音为隐含渠道）」的前提被**拒绝**。正确语境是：Video = Canonical Content（跨平台）；原 TTK Product Model 应拆为「Video Production Workspace 模型」+「Channel Operations Workspace 模型」两块。
- **不 REJECT**：对象层价值高，仅 reposition。

### (2) Douyin End-to-End Automation Research（本轮前一份）
> **判定：REINTERPRET（事实保留，归类重定，政策降级）**

- **KEEP（事实层）**：官方能力研究（发布/互动/数据/OAuth/Scope/Webhook/账号要求）**完全保留** —— 用户明示「官方能力研究部分保留」。
- **REINTERPRET（归类层）**：上述能力从「Video Production 能力」重归类为 **Douyin Channel Capabilities**（归属 Douyin Operations WS / Douyin Connector）；生产工具重归类为 VIDEO PRODUCTION CAPABILITY PROVIDERS。
- **DOWNGRADE（政策层）**：原「全自动托管=封禁」「发布前人工审核永远必须」降级为 `POLICY VERIFICATION REQUIRED`，不进入 Frozen Product Rule（见 Model 文档 §7）。
- **不 REJECT**：事实资产有效，仅重新归属与降级政策结论。

### (3) XHS 未来扩展（研究假设）
> **判定：MODIFY（增补 Video 内容类型）**

- **保留**：当前 XHS Instance（Note Publishing/Ops 首版）**不改**；Note 作为首个 Content Type 成立。
- **MODIFY（未来扩展）**：XHS 未来 Channel Operations 应增补 **Canonical Video → XHS Video Variant → Publication** 路径（因 XHS 已支持视频笔记）。即由「XHS=Note」修正为「XHS=Note+Video 双 Content Type 的 Channel Operations」。

---

## 纪律核对

- ❌ 未画 UI
- ❌ 未改 Frozen Shell / P1–P7
- ❌ 未改 XHS / RD Instance
- ❌ 未开发 Connector
- ❌ 未改 Runtime
- ✅ 仅产出 4 份 Reference Only 文档 + 同步 CURRENT_STATE（状态登记，非权威改写）

---
*CONTENT × CHANNEL ARCHITECTURE REVIEW REQUIRED —— 待 Review 批准后，方可进入 Contract 设计与 Workspace 实例化。*
