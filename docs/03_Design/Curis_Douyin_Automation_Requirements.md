# Curis 中国抖音自动化打通条件与反馈环（DOUYIN AUTOMATION REQUIREMENTS）

**阶段**：DOUYIN END-TO-END AUTOMATION FEASIBILITY  
**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**范围**：中国抖音（open.douyin.com）。TikTok 国际版不混入。  
**配套**：可行性文档（结论/等级）、能力矩阵（D/E/G）、缺口地图（I）。  
**专家角色**：UiDesigner（研究，非开发）

---

## C. 打通条件（八项）

### C1. 开发者账号
- 个人开发者 vs **企业开发者**（推荐企业：50 应用 / 高配额 / 高级权限）。
- 应用审核 2–3 工作日；回调域名需 **https 且非 IP/localhost**。

### C2. OAuth2.0 授权
- `access_token`（用户级，2h 有效期）/ `client_token`（应用级）。
- 用户授权流程必须走官方 OAuth，密钥不落库（沿用 Curis `env:VAR` 引用 + 进程内存模式，见 working memory §13）。

### C3. Scope（权限范围）
| Scope | 用途 | 备注 |
|-------|------|------|
| `video.create.bind` | 发布视频 | 需申请权限 + 用户授权 |
| `video.comment` | 评论管理 | 需「互动管理」权限；仅自己视频 |
| `video.data` | 基础数据（计数） | OpenAPI 层 |
| `video.data.bind` | 经营号深度数据（完播率等） | 需经营抖音号授权 |
| `im.direct_message` | 私信 | `receive_msg` 需企业号 |

### C4. 企业资质
- **企业号认证** → 获「企业号开放能力」（评论置顶、私信 receive_msg、经营号数据）。
- 个人号能力受限，MVP 亦建议企业号以便互动/深度数据。

### C5. 白名单 / 权限申请
- 部分 Scope（如 `video.create.bind`、互动管理）需**单独申请**并通过审核，非默认开通。
- 内容发布接入方案默认对审核通过应用开通「视频发布及管理」权限。

### C6. 配额
- 企业账号配额显著高于个人；具体限流以官方文档为准，Connector 需做限流/退避。

### C7. Webhook 回调
- 配置 https 回调地址 + 订阅事件：`create_video` / `authorize` / `unauthorize` / `receive_msg`(enterprise.im) / `enter_im` / `dial_phone` / `website_contact` / `personal_tab_contact`。
- IM webhook 需额外订阅配置。

### C8. AI 披露（合规强制）
- 《人工智能生成合成内容标识办法》2025-09-01 施行；中央网信办 6 类必选标签含「含有 AI 生成内容」。
- 抖音生活服务《AIGC 创作规范》2026-04-22（重点行业禁 AI 生成）。
- **Curis 必须在生成/发布链路内置 AIGC 标识**，并在 CEO Decision 中暴露版权/合规/披露风险（P7 Provenance 标 POLICY）。

---

## F. Analytics 反馈环要求

### F1. 铁律：禁止无真实数据生成 AI 复盘
- AI 复盘 / 反哺选题库**必须**基于真实拉取的平台回执（A0 数据通路），**不得**用 mock / 估算 / 训练先验生成「复盘结论」。
- 在无真实回执前，Analytics 显示「—」/ 空态（继承 working memory §11 设计边界：v1 无真实指标时显示「—」/空管道，禁止编造）。

### F2. 数据路径
- **基础计数**：OpenAPI `/video/data/`（Scope `video.data`）→ `play_count` / `digg_count` / `download_count` / `share_count` / `forward_count` / `comment_count`。等级 A0。
- **深度指标（完播率等）**：小程序「短视频详细数据」（Scope `video.data.bind` / 经营抖音号授权）→ `item_completion_rate` / `item_last_frame_watch_cnt` / `item_vv` / `item_uv`。等级 A0 + **Account Gap**（需经营号授权）。
- **未确认字段**：2 秒跳出 / 平均观看时长——官方 API 未确认提供，列为 UNK，待连接验证。

### F3. 时效与边界
- 用户首次授权后**次日**才产生全部数据。
- 视频数据查询限 **30 天内**创建视频。
- 巨量引擎 = 营销/投放数据，非内容经营数据（独立体系，不混入反馈环）。

### F4. 反馈环结构
```
发布(A1) → Webhook create_video 回执(A0) → 定时拉取 /video/data/(A0) →
System Activity 聚合 → 自动反哺选题库(A0) → 可选深度解读(A2 员工)
异常指标(如合规风险/重大掉量) → CEO_DECISION(A3, 仅升级事件)
```

---

## H. Handoff 重新验证（Frozen Handoff A vs Artifact Review B）

> 本阶段研究对首轮 Proposal 的审核/交接设计做二次验证。

| 情形 | 归类 | 是否责任转移 | 模式 |
|------|------|--------------|------|
| 策划完成 → 脚本接手 | **A：真 Frozen Handoff (P5)** | 是 | Handoff Event |
| 制作送审核 | **B：Artifact Review Request** | **否**（制作仍持责任） | Instance Candidate（与 RD 一致，不升格 P5） |
| 审核通过 → 发布运营接手 | A：Handoff（审核责任闭合后） | 是 | Handoff Event |
| 发布前人工审核门禁 | **B（A1 审核点）** | 否 | 政策强制批准点，非 Handoff |
| 高风险发布（投放/版权/合规/对外） | **A3 CEO Decision (P7)** | — | 独立于 Handoff/Artifact Review |

**裁定**：首轮 Proposal「审核 = Artifact Review（B 类）」**正确且须保持**；发布门禁是 A1 审核点而非 Handoff；CEO Decision 永远独立于 Handoff（P7 ≠ P5）。本阶段**未推翻**任何 Frozen Pattern 应用。

---

**状态**：DOUYIN END-TO-END AUTOMATION REVIEW REQUIRED  
**UI Designer** · 2026-08-15 · RESEARCH ONLY
