# Curis · Canonical Content × Channel Variant 数据模型

> **状态**：CONTENT × CHANNEL ARCHITECTURE REVIEW REQUIRED
> **类型**：Reference Only · 数据模型草案（非权威、非最终）
> **配套**：`Curis_Content_Production_Channel_Operations_Model.md` §2 / §3

本文定义 **A 节统一内容模型** 的候选对象结构与字段，并回答 A1–A4。**不预设该结构最终正确** —— 末尾列出待设计期裁决的开放问题。

---

## 1. 对象总览（纵向链）

```
Canonical Content (平台无关, Video Production WS 拥有)
  ├─ Script            (Video 子对象)
  ├─ Assets[]          (素材)
  ├─ Production Result (平台无关母版/成品)
  └─ Channel Variant ×N  (每平台一份, Channel Operations WS 拥有)
        └─ Publication ×M  (每次发布一份, Channel Operations WS 拥有)
              ├─ Engagement ×K   (挂在 Publication)
              └─ Analytics ×T    (挂在 Publication)
```

**关键所有权分界**：
- `Canonical Content / Script / Assets / Production Result` → **Video Production Workspace**（平台无关）
- `Channel Variant / Publication / Engagement / Analytics` → **Channel Operations Workspace**（per-platform）

---

## 2. Canonical Content（平台无关，可泛化）

| 字段 | 说明 |
|---|---|
| `id` | 全局唯一 |
| `type` | `VIDEO` \| `NOTE` \| `IMAGE_SET`（泛化，不止 Video） |
| `title_working` | 工作标题（非发布标题） |
| `brief` | 内容简报 / 选题依据 |
| `business_id` | 所属 Company/Business |
| `workspace_id` | 生产 Workspace |
| `status` | DRAFT / IN_PRODUCTION / REVIEW / APPROVED / ARCHIVED |
| `created_by` | 创建员工 |

**子类型**：
- `Canonical Video`：`script_ref`、`assets[]`、`production_result_ref`、`ratio_spec`、`duration_spec`
- `Canonical Note`：`body_ref`、`images[]`、`title_spec`

> 与用户候选树的差异：用户树以 `Canonical Video` 为根；本文泛化为 `Canonical Content`（Video/Note 为子类型），以容纳 XHS 的 Note 与 Video 双形态（见 Model 文档 §4）。

---

## 3. Script（Video 子对象）

| 字段 | 说明 |
|---|---|
| `id` | |
| `canonical_content_id` | 归属 |
| `draft` | 当前草稿文本 |
| `versions[]` | 版本历史 |
| `status` | DRAFT / EDITING / APPROVED |

---

## 4. Assets

| 字段 | 说明 |
|---|---|
| `id` | |
| `type` | `video_clip` \| `image` \| `audio` \| `music` \| `srt` |
| `storage_ref` | 存储引用 |
| `license` | 授权状态（原创/授权/CC） |
| `source` | 生成工具或来源（即梦/Kling/自制…） |

---

## 5. Production Result（平台无关母版）

| 字段 | 说明 |
|---|---|
| `id` | |
| `canonical_content_id` | |
| `master_file_ref` | 最高质量平台无关母版（如 4K 横竖双母版或单一高码率母版） |
| `specs` | `resolution` / `codec` / `master_ratio` |
| `status` | APPROVED / REJECTED |

> **注意**：Production Result 是**平台无关的成品**；Channel Variant 由其派生平台特化版本（裁剪/转码/遮幅/字幕）。这是「一次生产、多平台适配」的物理基础。

---

## 6. Channel Variant（每平台一份 —— 核心对象，回答 A2）

**归属**：Channel Operations Workspace
**回答 A2：YES —— Variant 应拥有以下全部属性**

| 字段 | 说明 | 平台差异举例（见 Doc 3 §G） |
|---|---|---|
| `platform` | `DOUYIN`\|`XHS`\|`TIKTOK`\|`BILIBILI`\|`YOUTUBE`\|… | 枚举 |
| `ratio` | 画幅 | 9:16（抖/XHS/TK）/ 16:9（YT/B站）/ 3:4（XHS 封面向） |
| `duration` | 平台特化时长 | YT 120min / B站 5h / XHS 15min / 抖 15min / TK 3min |
| `resolution` | 平台特化分辨率 | B站 4096×2160 / YT 4K / 抖 720p+ |
| `edit_variant` | 剪辑版本/裁剪/遮幅/字幕版 | 横版加遮幅变竖版、加字幕版 |
| `caption` / `title` | 平台特化文案 | XHS ≤20 字 / 抖 ≤55 / B站 ≤80 / YT ≤100 / TK ≤150 |
| `cover` | 平台特化封面 | XHS 3:4 (1242×1660) / YT ≥1280×720 / B站必填 |
| `hashtag[]` | 平台特化话题 | XHS ≤5 / 抖 ≤5 / B站 逗号分隔≤200 / YT ≤15 / TK ≤5 |
| `music` | 平台特化 BGM/原声 | 抖原声强依赖 / XHS 弱 / YT 可选 |
| `disclosure` | AI 生成标识状态 | `required / applied / label_type`（各平台标签不同） |
| `platform_policy_result` | 平台政策预检结果 | `PASS / RISK / NEEDS_HUMAN` |
| `publish_configuration` | 发布配置 | 可见性 / 分区(tid) / 版权类型(原创·转载) / 定时(若支持) / POI / 小程序 / 合集 |
| `derived_from` | 来源 | `production_result_ref` 或 `master` |
| `status` | `ADAPTED`\|`REVIEW_REQUIRED`\|`APPROVED`\|`PUBLISHED` | |

> `copyright` 字段在 Bilibili 为**必填**（原创/转载），是平台差异的硬证据 —— 必须在 Variant 层表达，不能上提到 Canonical。

---

## 7. Publication（每次发布一份 —— 回答 A3）

**回答 A3：YES —— Publication 应独立于 Video，同一 Video 可产生多个平台 Publication**

| 字段 | 说明 |
|---|---|
| `id` | |
| `channel_variant_id` | 来源 Variant |
| `platform` | |
| `platform_post_id` | 平台侧作品 ID |
| `status` | `DRAFT`\|`SCHEDULED`\|`PUBLISHED`\|`FAILED`\|`REMOVED` |
| `publish_time` | 实际/计划发布时间 |
| `receipt` | 平台回执 / URL |
| `error` | 失败原因 |

> 同一 Canonical Video → 5 个 Channel Variant → 每个可发布 1+ 次 Publication。Publication 是「真实发生的一次发布」的事实记录。

---

## 8. Engagement（挂在 Publication —— 回答 A4 归属）

**回答 A4：Engagement/Analytics 归属于具体 Channel Publication，不是 Canonical Content**

| 字段 | 说明 |
|---|---|
| `id` | |
| `publication_id` | 归属 Publication（进而归属平台） |
| `platform` | |
| `type` | `COMMENT`\|`DM`\|`LIKE`\|`COLLECT`(收藏)\|`COIN`(投币)\|`DANMAKU`(弹幕)\|`SHARE` |
| `content` | 原文 |
| `author` | 平台用户 |
| `classified_as` | `AUTO_REPLY`\|`EMPLOYEE_REVIEW`\|`CEO_DECISION`（沿用 Douyin Research E 节三档路由） |
| `handled_by` | 处理员工/系统 |
| `status` | 待处理/已回/已升级 |

> 你不会在 YouTube 上收到抖音的评论。互动的**真相源**是 Publication，Canonical Content 只持有跨平台 rollup 视图。

---

## 9. Analytics（挂在 Publication —— 回答 A4 归属）

| 字段 | 说明 |
|---|---|
| `id` | |
| `publication_id` | 归属 Publication |
| `platform` | |
| `metrics` | 平台原生指标（play/vv、like、comment、share、completion_rate*…） |
| `fetched_at` | 拉取时间 |
| `source` | `OpenAPI`\|`经营号授权层`\|`YouTube Analytics API`\|`B站投稿效果` |

> `*completion_rate`(完播率) 等深度指标**并非所有平台 API 平等提供**：Douyin 仅经营号授权层可得；YouTube Analytics API 丰富；B站有投稿效果管理。这再次证明 Analytics 必须 per-Publication、per-platform，不能统一上提。

---

## 10. 关系图（文字）

```
Canonical Content (Video / Note)          ← Video Production WS
  ├─ Script, Assets, Production Result     （平台无关母版）
  └─ Channel Variant ×N  (platform)        ← Channel Operations WS
        └─ Publication ×M                  ← Channel Operations WS
              ├─ Engagement ×K
              └─ Analytics ×T
Canonical Content 仅持有【跨平台 rollup 视图】，不持有平台原生互动/数据。
```

---

## 11. 用户对候选树的结构评估

| 候选树要素 | 处置 |
|---|---|
| `Canonical Video` 含 `Script/Assets/Production Result/Channel Variants` | ✅ 采用（泛化为 Canonical Content） |
| `Channel Variants` 下列 5 个平台 | ⚠️ 改为 `platform × content_type` 枚举，避免写死 |
| 缺 `Publication` 独立层 | ⚠️ 补入（A3 要求） |
| `Engagement/Analytics` 位置 | ⚠️ 必须挂在 `Publication`，非 Variant/Content |

---

## 12. 开放问题（不预设最终正确，留设计期）

1. `Assets` 是否独立实体，还是直接挂在 Production Result？
2. `Production Result` 与 `Canonical Video` 是否应合并为单一「成品」对象？
3. `Canonical Note` 的 `body` 结构如何定义（富文本/块/图片集）？
4. 跨内容复用：一个 Video 能否作为多个 Note 的素材（内容关系网）？
5. `Channel Variant` 的 `edit_variant` 是否应引用独立的「剪辑工程」对象（与 CapCut 草稿对应）？
6. `Publication` 失败重试、跨平台去重（超时导致重复发布）如何处置？
7. `disclosure` 标签在各平台的精确取值字典由谁维护（政策层）？

---
*数据模型草案，未固化。字段集将在 Video Production WS 与 Channel Operations WS 的 Contract 设计中最终裁定。*
