# 各平台开发者资质申请追踪表（内容发布执行层 · design-only）

> 承接 `aiearn-content-marketing-final-decision.md` §11 与 `federated-agent-os.md` §8 的渐进替换路线。
> 用途：并行推进各平台开发者资质申请时，统一盯进度；资质获批后将该平台执行端从「分支 B（social-auto-upload 浏览器自动化，MIT 自托管）」drop-in 替换为「分支 A（Curis 自有 OAuth App，原生 API）」。
> 性质：轻量追踪文档（零代码 / 零提交 / 不 patch 契约）。状态列初始均为「待申请」，执行落地时由对应负责人滚动更新。

## 状态图例
- 待申请 → 申请中 → 已获批 / 已驳回
- 执行端路径：获批前 = 分支 B（social-auto-upload，MIT 自托管）；获批后 = 分支 A（Curis 自有 OAuth App，原生 API）

## 追踪表

| # | 平台 | 开放发布 API? | 所需资质 / 账号类型 | 申请入口 | 状态 | 预计批复周期 | 执行端路径（获批前 → 获批后） | 备注 |
|---|------|--------------|---------------------|----------|------|--------------|-------------------------------|------|
| 1 | 抖音 | ✅ 有（开放平台 / 企业号） | 抖音开放平台企业开发者 / 企业号 | open.douyin.com | 待申请 | 1–4 周 | B → A | 企业资质审核，需营业执照 |
| 2 | 哔哩哔哩 | ✅ 有（OAuth，含投稿/数据 scope） | B站开放平台开发者 | openhome.bilibili.com | 待申请 | 1–3 周 | B → A | OAuth scope 已确认含投稿管理 |
| 3 | 微信公众号 | ✅ 有（公众号 OAuth） | 微信公众平台服务号 | mp.weixin.qq.com | 待申请 | 1–2 周 | B → A | 服务号需认证（300 元/年） |
| 4 | YouTube | ✅ 有（官方 Data API） | Google Cloud 项目 + OAuth 同意屏 | console.cloud.google.com | 待申请 | 即时–数日 | B → A | 注意配额；本就走官方 API |
| 5 | X (Twitter) | ✅ 有（API v2） | X Developer 账号 | developer.x.com | 待申请 | 数日–数周 | B → A | 免费层有限额 |
| 6 | TikTok | ✅ 有（Content Posting API） | TikTok 开发者账号 | developer.tiktok.com | 待申请 | 1–4 周 | B → A | 需应用审核 |
| 7 | Facebook / Instagram | ✅ 有（Graph API） | Meta 开发者应用 | developers.facebook.com | 待申请 | 数日–数周 | B → A | 需应用审查 + 业务验证 |
| 8 | 快手 | ⚠️ 部分（开放平台） | 快手开放平台开发者 | open.kuaishou.com | 待申请 | 1–4 周 | B → A | 发布能力需确认 scope |
| 9 | 百家号 | ⚠️ 部分（开放平台） | 百度智能云 / 百家号开放平台 | baijiahao.baidu.com | 待申请 | 1–4 周 | B → A | 内容发布 API 需确认 |
| 10 | 小红书 | ❌ 无开放发布 API | 专业号 / 机构号（仅登录态，无发布 API） | 小红书专业号后台 | 待申请（资质） | 2–6 周 | B（长期，无 A 可换） | **无官方发布 API** → 分支 B 为长期手段，非过渡；持续关注开放平台 |
| 11 | 微信视频号 | ❌ 无开放发布 API | 视频号（依附微信生态，无独立发布 API） | 微信视频号助手 | 待申请（资质） | 不确定 | B（长期，无 A 可换） | **无官方发布 API** → 分支 B 为长期手段；关注视频号开放能力 |
| 12 | Threads / Pinterest / LinkedIn | ✅ 有（各官方 API） | 各平台开发者应用 | 各自开发者中心 | 待申请 | 数日–数周 | B → A | 国际平台，按需优先级 |

## 关键说明
- **无 API 平台（小红书 / 视频号）**：social-auto-upload 不是「过渡」而是**长期执行手段**——因为没有官方发布 API 可换。这两项的「逐步替换」不成立，应持续投入反爬 / 封号对抗与监控，而非等 API。
- **L2 #5 触发点**：实际注册 Curis 自有 OAuth App、把 `client_secret` 等凭据存入 Credential Vault 时，触发安全边界席裁定（已是合法自有资产，非 Relay 灰区）。
- **资质驳回处理**：若某平台驳回，该平台留在分支 B；必要时评估 OEM / 第三方授权（走对应 L2 Gate）。
- **滚动更新规则**：状态变更由执行负责人即时更新本表；已获批项在 `federated-agent-os.md` §8 对应平台路径标注「已切 A」。

---

*—— 轻量追踪文档（零代码、零提交、不 patch 契约）。DevOps Automator · 2026-07-12。*
