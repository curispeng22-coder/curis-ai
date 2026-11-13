# CONTENT GROWTH — SHARED vs CHANNEL MATRIX
### 哪些能力跨渠道共享，哪些只属渠道；XHS / Douyin 压力测试与层级裁定

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen）
Companion: `CONTENT_GROWTH_DOMAIN_OPERATING_MODEL.md` · `CONTENT_GROWTH_OPERATING_MATRIX.md` · `CONTENT_GROWTH_CEO_EXPERIENCE_MODEL.md` · `CONTENT_GROWTH_UNIT_ECONOMICS_AND_DEPTH_MODEL.md`

---

## 0. 层级定义（用于裁定）

```
Workspace（内容增长 OS）
  └─ Surface（跨渠道内容工件 / Brief / 资产 / 评估）
       └─ Channel（渠道：XHS / Douyin / 公众号 / 视频号 / B站）
            ├─ Module（格式适配 / 发布 / 渠道分析 / 渠道反馈）
            └─ Connector（平台开放平台 / 授权 IM / 商单平台 集成边界）
                 └─ Capability（原子功能，可替换，不拥有）
```

**裁定问题（CEO 原话）**：小红书/抖音到底更适合 **Workspace / Surface / Channel / Module / Capability / Connector** 中的哪一种？
→ **结论：Channel（可拆为 4 Module + N Connector）**，不是 Workspace。`[CAND][COMP][INF]`

---

## 1. 能力分类总表

| 能力 | 归类 | 理由 | 证据 |
|---|---|---|---|
| 信息搜集（源配置/监控） | **SHARED** | 来源与监控逻辑跨渠道，建一次 | `[COMP]` |
| Signal / 信号池 | **SHARED** | 信号与渠道无关 | `[CAND]` |
| Opportunity / 机会 | **SHARED** | 什么值得做，不绑平台 | `[CURIS-AUTH]` |
| Topic Pool / 选题池 | **SHARED** | 选题与账号定位/受众相关，非平台 | `[COMP]` |
| 调研 / Deep Research | **SHARED** | 研究问题/证据跨渠道 | `[REAL]` |
| 内容策略 / Brief / Intent | **SHARED** | WHY/WHAT/GOAL，共享上游 | `[CURIS-AUTH]` |
| Knowledge / 资产（核心观点） | **SHARED** | 1 长文→多形态复用 | `[COMP]` |
| Evaluation / 效果评估 | **SHARED** | 归因与判断跨渠道可比 | `[COMP]` |
| Learning / Strategy Adj. | **SHARED** | 学习方法复利 | `[INF]` |
| **平台发现 / 搜索算法** | **CHANNEL** | 流量池/搜索权重两平台本质不同 | `[COMP]` |
| **内容格式适配** | **CHANNEL** | 时长/封面/竖横屏/钩子各异 | `[COMP]` |
| **发布 / 定时 / API** | **CHANNEL** | 开放平台/权限/定时上限/RPA合规不同 | `[REAL][COMP]` |
| **平台数据分析** | **CHANNEL** | 原生指标+三方工具各自独立 | `[COMP]` |
| **渠道反馈 / 私信合规** | **CHANNEL** | 留资卡/权限回收/三方IM名单不同 | `[REAL]` |
| **商单 / 变现矩阵** | **CHANNEL** | 蒲公英/聚光 vs 星图/千川不可共用 | `[REAL]` |
| 内容质量信号（Hook/留存） | **HYBRID** | 原理共享；阈值/形态 CHANNEL | `[INF]` |
| AI 标识强制令 | **HYBRID** | 法规共享（全国《标识办法》）；声明路径 CHANNEL | `[REAL]` |
| 线索意图识别 / qualification | **HYBRID** | 识别/SOP/知识库共享；合规话术包装 CHANNEL | `[INF]` |

**量化结论**：约 **60–70%** 内容增长实质价值是 SHARED（建一次）；仅 **30–40%** 为 CHANNEL-SPECIFIC `[COMP][INF]`。

---

## 2. XHS（小红书）渠道解剖

| 维度 | 事实（VERIFIED/CONDITIONAL/UNKNOWN） | 归类 |
|---|---|
| 发现/算法 | CES+流量池，收藏权重>点赞；搜索已成独立场 `VERIFIED`；具体公式 `UNKNOWN` | CHANNEL |
| 格式规范 | 图文 3:4 竖图、正文≤1000字、视频≤15min；AI 须 `#AI生成` `VERIFIED` | CHANNEL |
| 发布机制 | 原生定时 ≤7天(APP)/≤30天(网页, CONDITIONAL)；企业开放平台+聚光 `VERIFIED`；个人号 RPA 灰产 | CHANNEL |
| 数据分析 | 创作者中心/专业号数据中心；三方 千瓜/灰豚/新红 `VERIFIED/COMP` | CHANNEL |
| 反馈/私信 | 私信通(官方)+授权三方IM(来鼓/美洽)；蒲公英(商单)；2026-05 私信三大红线 `VERIFIED` | CHANNEL |
| 商业化 | 专业号→聚光→蒲公英→薯条→乘风→千帆→灵犀 `VERIFIED` | CHANNEL |

- **XHS = Channel**：其承载的是渠道规则+连接器+4 Module（格式/发布/分析/反馈）。其上「研究/选题/策略/Brief/资产/评估」全为 SHARED，必须上浮 Workspace。
- **若把 XHS 建成独立 Workspace**：等于为每个平台重复造共享大脑 → 架构浪费 `[CAND][INF]`。
- **Connector**：小红书商业开放平台、聚光、私信通、来鼓/美洽等授权 IM、蒲公英。
- **承前序研究**：Calendar = Content Operating 内部主视图非默认入口（OPEN QUESTION Z1/Z7 待 CEO）；西方工具（Hootsuite/Buffer/Later/Sprout）**均不支持 XHS 发布**——印证 XHS 须自建 Channel Connector `[COMP]`。

---

## 3. Douyin（抖音）渠道解剖

| 维度 | 事实 | 归类 |
|---|---|---|
| 发现/算法 | 分层流量池+赛马；2025–26 升级动态评分+分级赛马，推流 7–15天慢热；前3秒留存权重~40% `VERIFIED/COMP` | CHANNEL |
| 格式规范 | 9:16，15–40s，前3秒强钩子；口播硬广/水印/二维码降权 `COMP` | CHANNEL |
| 发布机制 | 企业号后台定时(`CONDITIONAL`)；巨量引擎开放平台；**2025-04-14 关停新开发者私信/群聊 scope** `VERIFIED` | CHANNEL |
| 数据分析 | 创作者服务中心/电商罗盘；三方 巨量算数/蝉妈妈/飞瓜 `VERIFIED/COMP` | CHANNEL |
| 反馈/私信 | 企业号蓝V 自动回复卡片（留资/预约/名片，经风控）；星图商单；三方IM受权限回收冲击 `VERIFIED` | CHANNEL |
| 商业化 | 巨量引擎→星图→抖店→千川(乘方) `VERIFIED` | CHANNEL |

- **Douyin = Channel**（电商闭环更深，但仍是 Channel）。其 SHARED 大脑与 XHS 共用。
- **Connector**：巨量引擎开放平台、星图、蓝V卡片、存量三方IM。
- **关键差异提示**：抖音 2025 私信权限回收使「第三方 IM 自动回复」可靠性 `CONDITIONAL`——反馈 Module 须以官方蓝V卡片为主、三方为辅 `[REAL]`。

---

## 4. HYBRID 在层中的落点

| HYBRID 能力 | SHARED 部分（Workspace） | CHANNEL 部分（Module） |
|---|---|---|
| 内容质量信号 | Hook/留存/价值 原理与评估方法 | 阈值与形态（XHS 重封面点击+收藏；抖音重前3秒完播） |
| AI 标识 | 法规知识库（全国《标识办法》） | 声明动作进发布 Module（路径/元数据格式） |
| 线索意图识别 | 意图识别/SOP/知识库 | 合规留资卡包装进反馈 Module |

→ HYBRID 的处理原则：**逻辑/知识在 SHARED，执行包装在 CHANNEL** `[CAND]`。

---

## 5. 层级裁定（直接回答 CEO Q4）

| 对象 | 裁定 | 理由 |
|---|---|---|
| **Content Growth** | **Workspace（Professional）** | 域边界；承载 SHARED 大脑 + 多 Channel |
| **XHS** | **Channel**（4 Module + N Connector） | 仅渠道规则/连接器/模块；非 Workspace |
| **Douyin** | **Channel**（4 Module + N Connector） | 同上 |
| 未来 公众号/视频号/B站 | **Channel** | 同构扩展 |
| Calendar | **Surface（Content Operating 内部）** | 非默认入口（OPEN QUESTION） |

**最终架构主张**：构建 **Content Growth Workspace**，下设统一 Surface（Brief/资产/评估），下挂 **XHS Channel** 与 **Douyin Channel**（未来可加微信/视频号/B站）。SHARED 一次构建多端复用，CHANNEL 差异封装在 Connector 与 Module 内。**「XHS = 完整 Workspace」不成立**——它只是内容增长 OS 中的一个渠道节点。`[CAND]`

---

## 6. 对现有 XHS 六大 Surface 的重组建议（回答 CEO Q15）

| 原 XHS Surface | 新归属 | 动作 |
|---|---|---|
| Topic Pool / 选题 | 上浮 → Workspace SHARED Surface | 不再属 XHS |
| Research / 调研 | 上浮 → Workspace SHARED Surface | 不再属 XHS |
| Assets / Knowledge / 资产 | 上浮 → Workspace SHARED Surface | 跨渠道复用 |
| CEO Overview / 经营重点 | 上浮 → Workspace 默认 Main（OUTPUT 4） | CEO 默认可见 |
| Evaluation / Learning | 上浮 → Workspace SHARED Surface | 不再属 XHS |
| Calendar | 降为 Content Operating 内部 Surface（非默认） | OPEN QUESTION Z1/Z7 |
| 发布 / Format / Channel Analytics / Feedback | 降为 **XHS Channel Module**（4 子模块） | 渠道封装 |

→ 即 XHS 从「6 Surface 的独立 Workspace」重组为 **Content Growth Workspace 下的一个 Channel**。`[CAND]`

---

*CONTENT GROWTH SHARED vs CHANNEL MATRIX — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*
