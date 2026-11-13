# 内容发布包 Schema（Content Publish Package · 阶段1 方向③ 基石）

> 承接 `federated-agent-os.md` §3（执行抽象层 / 发布包 schema 契约）与 `aiearn-content-marketing-final-decision.md` §9（阶段1 把 `ai_content` 资产落成「可导出内容工件」）。
> 用途：定义 `ai_content` 12 个 `wl_*` 工作流产出的**统一结构化导出格式**，使 tenant 能直接拷贝到各平台手动发布（方向③），并为未来分支 A/B 执行端 drop-in 提供归一化输入。
> 性质：**design-only 契约规范（零代码 / 零提交 / 不 patch 既有契约）**。真实内容落库与执行端接入归后续 Gate（分支 A/B 落地触发 L2 #5）。

---

## 0. 为什么先定义这个

阶段1 方向③ 的核心是「**工作流产出，用户自发改发**」。但当前 `wl_ai_content_*` 的 `output_standard` 只写了"产出 PRD 式的文字描述"（如 `output_standard: 发布内容 + SEO 元数据 + 多平台分发记录 + 周度量报告`），没有机器可读的结构。结果是：

- tenant 拿到的是一段散文，要自己拆标题/正文/标签/分镜；
- 同一篇内容发抖音和小红书，得手动改两遍格式（字数/标签/比例）；
- 未来接执行端（分支 A/B）时，每个工作流要单独适配，无法复用统一契约。

**发布包 schema 就是解**：所有 `ai_content` 工作流产出统一收敛到 `ContentPublishPackage`，tenant 拿去手动发，执行端拿去自动发——同一份结构，两种消费方式。

---

## 1. 资产模型定位

```
ai_content 工作流（wl_*）
   │ 产出
   ▼
ContentPublishPackage（本 schema 定义的结构化工件）
   ├── artifacts[]  ← 5 类内容工件（文案/脚本/分镜/排期/多平台草稿）
   │
   ├──▶ tenant 手动消费：导出为 Markdown / 逐平台 Clipboard（方向③ 阶段1）
   │
   └──▶ 执行端自动消费：归一化输入 → 分支 A（原生 API）/ 分支 B（social-auto-upload）（未来）
```

- 与 `federated-agent-os.md` §3 的"发布包 schema"是**同一个契约**——本文件是其具体字段定义。
- 与 `workflow-official-content-plan.md` 的 `wl_*` 正交：工作流定义"怎么做"，本 schema 定义"产出长什么样"，互不侵入。

---

## 2. 发布包 Schema（JSON Schema draft-07）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ContentPublishPackage",
  "type": "object",
  "additionalProperties": false,
  "required": ["package_id", "version", "source_workflow", "language", "artifacts"],
  "properties": {
    "package_id": {
      "type": "string", "pattern": "^pkg_[a-z0-9_]+$",
      "description": "发布包稳定 ID"
    },
    "version": {
      "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$", "default": "1.0.0"
    },
    "created_at": { "type": "string", "format": "date-time" },
    "source_workflow": {
      "type": "string", "pattern": "^wl_ai_content_[a-z0-9_]+$",
      "description": "产出该包的工作流（对齐 workflow_id）"
    },
    "brand_voice_ref": {
      "type": ["string", "null"], "pattern": "^pt_|^persona_",
      "description": "可选：引用的品牌声量/人格模板"
    },
    "language": { "type": "string", "default": "zh-CN" },
    "platforms_targeted": {
      "type": "array", "items": { "type": "string" }, "default": [],
      "description": "目标平台（douyin/xhs/wechat_channels/youtube/bilibili/tiktok/...）"
    },
    "artifacts": {
      "type": "array", "minItems": 1,
      "items": { "$ref": "#/definitions/artifact" }
    }
  },
  "definitions": {
    "artifact": {
      "type": "object",
      "additionalProperties": false,
      "required": ["artifact_id", "type", "title", "body"],
      "properties": {
        "artifact_id": { "type": "string" },
        "type": {
          "type": "string",
          "enum": ["copywriting", "script", "storyboard", "editorial_calendar", "multichannel_draft", "media_asset"]
        },
        "platform": {
          "type": "string",
          "description": "universal 或具体平台 key；multichannel_draft 恒为 universal"
        },
        "title": { "type": "string" },
        "body": { "type": "object", "description": "按 type 结构化的内容体（见 §3）" },
        "metadata": { "type": "object", "default": {} }
      }
    }
  },
  "examples": [{
    "package_id": "pkg_spring_skincare_001",
    "version": "1.0.0",
    "created_at": "2026-07-12T10:00:00+08:00",
    "source_workflow": "wl_ai_content_content_production_sop",
    "brand_voice_ref": "pt_ai_content_brand_voice_demo",
    "language": "zh-CN",
    "platforms_targeted": ["douyin", "xhs", "wechat_channels"],
    "artifacts": [
      {
        "artifact_id": "art_copy_001",
        "type": "copywriting",
        "platform": "universal",
        "title": "春季护肤主文案",
        "body": {
          "hook": "换季烂脸？三步稳住皮肤屏障",
          "body_text": "气温一变脸就闹情绪？先停掉猛药，做好三件事……",
          "cta": "评论区扣1领护肤清单",
          "hashtags": ["#春季护肤", "#敏感肌", "#烂脸自救"]
        }
      },
      {
        "artifact_id": "art_mcd_001",
        "type": "multichannel_draft",
        "platform": "universal",
        "title": "多平台发布草稿",
        "body": {
          "base_caption": "换季烂脸？三步稳住皮肤屏障，评论区扣1领清单",
          "variants": {
            "douyin": { "caption": "换季烂脸？三步稳住皮肤屏障🔥评论区扣1领护肤清单", "hashtags": ["#春季护肤", "#敏感肌"], "media_spec": "竖屏 9:16", "aspect_ratio": "9:16", "char_count": 28, "notes": "前3秒抛痛点" },
            "xhs": { "caption": "换季烂脸自救指南📝三步稳住皮肤屏障\n\n气温一变脸就闹情绪？先停掉猛药……", "hashtags": ["#春季护肤", "#敏感肌", "#烂脸自救", "#护肤清单"], "media_spec": "竖屏 3:4", "aspect_ratio": "3:4", "char_count": 22, "notes": "首图加标题文案" },
            "wechat_channels": { "caption": "换季烂脸？三步稳住皮肤屏障", "hashtags": [], "media_spec": "竖屏 9:16", "aspect_ratio": "9:16", "char_count": 15, "notes": "无标签，靠封面" }
          }
        }
      }
    ]
  }]
}
```

---

## 3. 五类内容工件（`artifact.body` 结构）

| type | 对应产出 | body 关键字段 | 主要来源工作流 |
|------|---------|--------------|---------------|
| `copywriting` | 文案 | `hook` / `body_text` / `cta` / `hashtags[]` | content_production_sop / copywriting skill |
| `script` | 脚本 | `duration_sec` / `scenes[]`（shot/narration/visual/caption） | script_writing_sop |
| `storyboard` | 视频分镜 | `shots[]`（index/description/duration/camera/audio） | video_production_sop |
| `editorial_calendar` | 排期表 | `entries[]`（date/platform/topic/status/owner） | editorial_calendar_sop |
| `multichannel_draft` | 多平台发布草稿 | `base_caption` / `variants{platform}`（caption/hashtags/media_spec/aspect_ratio/char_count/notes） | multichannel_distribution_sop |
| `media_asset` | 媒体素材说明 | `asset_type` / `spec` / `source_ref` | video_production / image_generator |

- `multichannel_draft.variants` 是方向③的**核心价值点**：一份 `base_caption` 自动适配成各平台合规草稿（字数/标签/比例），tenant 复制即用。
- `media_asset` 仅描述素材**规格与来源**（如"竖屏 9:16 口播视频，15s"），不承载二进制；阶段1 媒体由 tenant 自备或既有生成工具产出。

---

## 4. 各平台适配规则（per-platform profile）

> 这是 `multichannel_draft.variants` 的生成依据，也是未来执行端（分支 A/B）的平台配置。阶段1 仅用于给 tenant 出合规草稿。

| platform key | 文案上限 | 标签惯例 | 视频比例 | 备注 |
|--------------|---------|---------|---------|------|
| `douyin` | 短（标题 20–30 字） | 2–5 个，# 前缀 | 9:16 竖屏 | 前3秒抛钩子；允许表情 |
| `xhs` | 正文可达 1000 字 | 8–10 个，# 前缀 | 3:4 竖图 / 9:16 视频 | 首图必须含标题；禁用导流外链 |
| `wechat_channels` | 短（无标签机制） | 无 | 9:16 竖屏 | 靠封面与口播；无 hashtag |
| `bilibili` | 简介 2000 字 | 无强制 | 16:9 | 标题决定点击；分区选对 |
| `youtube` | 描述不限 | 无强制 | 16:9 | 依赖 thumbnail + SEO 标题 |
| `tiktok` | 短（2200 字符上限但短为佳） | 3–5 个 | 9:16 | 英区标签 # 前缀；节奏快 |
| `kuaishou` | 短 | 2–5 个 | 9:16 | 类抖音 |
| `baijiahao` | 中 | 少量 | 16:9 / 1:1 | 偏图文 |

> **无 API 平台（xhs / wechat_channels）** 在阶段1 仅产出"合规草稿 + 封面文案建议"，真实发布由 tenant 手动操作——与 `federated-agent-os.md` §8 / 追踪表一致。

---

## 5. 与 12 个 `wl_ai_content_*` 的映射

| workflow_id | 主要产出 artifact.type | 说明 |
|---|---|---|
| `wl_ai_content_content_production_sop` | copywriting / multichannel_draft | 内容营销 7 步主流程，末端出可发草稿 |
| `wl_ai_content_topic_research_sop` | （前置，输入 research 笔记） | 不直接出发布包，供 content_production 消费 |
| `wl_ai_content_script_writing_sop` | script | 口播/短视频脚本 |
| `wl_ai_content_video_production_sop` | storyboard / media_asset | 分镜 + 素材规格 |
| `wl_ai_content_seo_optimization_sop` | copywriting（含 SEO 字段） | 在 body 增 `seo_keywords[]` / `meta_description` |
| `wl_ai_content_editorial_calendar_sop` | editorial_calendar | 排期表 |
| `wl_ai_content_multichannel_distribution_sop` | multichannel_draft | 多平台草稿生成器（核心适配逻辑） |
| `wl_ai_content_content_audit_sop` | （审核，不改结构） | 校验发布包合规性，打 `metadata.audit` |
| `wl_ai_content_livestream_sop` | script（直播大纲） | 直播话术/节奏 |
| `wl_ai_content_ugc_campaign_sop` | copywriting（征集文案） | UGC 活动文案 |
| `wl_ai_content_viral_analysis_sop` | （分析，输入度量） | 不直接出发布包 |
| `wl_ai_content_brand_voice_sop` | （声量，供 brand_voice_ref） | 产出可引用的品牌声量模板 |

---

## 6. 阶段1 导出格式（tenant 手动消费）

方向③ 不需要执行端，tenant 拿发布包后导出为：

1. **Markdown 汇总**：每个 artifact 一段，multichannel_draft 按平台分节，附复制按钮。
2. **逐平台 Clipboard**：点「复制小红书版」即复制该 variant 的 caption + hashtags（已按 §4 规则裁剪）。
3. **排期表 CSV**：editorial_calendar 直接导出为日历/表格导入。

> 导出层是纯前端/只读渲染，**不写运行时、不碰 Credential Vault、不触任何 Gate**——完全落在方向③ 红线内。

---

## 7. 边界与后续 Gate

- **design-only**：本文件仅定义契约，未落库、未写代码、未 patch `workflow-template-contract.md` 等既有契约。
- **未来执行端接入**：当分支 A（原生 API）或分支 B（social-auto-upload）落地时，发布包即其归一化输入；届时注册 OAuth App / 自托管执行端触发 **L2 #5（安全边界席）**。
- **schema 演进**：`version` 遵循 SemVer；新增 artifact.type 或 platform key 走 minor，破坏性变更走 major， tenant 实例快照隔离。

---

*—— 内容发布包 Schema 规范（design-only，零代码 / 零提交 / 不 patch 契约）。DevOps Automator · 2026-07-12。*
