# ADR-0044: First Arrival And Company Space

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-08-01

Module: Product Experience

## Decision

Curis 的首次进入体验采用 **First Arrival / Company Space Seed**：CEO 进入一间尚未建立完成、
但已有 Assistant 和下一步的 CEO 办公室，而不是进入空 Dashboard、注册表单或产品功能导览。

首次体验沿着真实经营对象逐步生长：

```text
经营意图
→ Company 牌匾
→ CEO 办公室
→ Business 版图
→ Department Office / Workspace
→ AI Team
→ 第一个可运行业务周期
```

公司空间使用二维办公室、房间和存在状态表达组织关系；不要求 3D，不以游戏化装饰替代经营语义。

## Reason

- Curis 的第一印象决定 CEO 是否相信这里是一家可以一起经营的 AI 公司。
- 传统 onboarding 只能解释功能，不能让 CEO 感受到公司正在从一句意图中形成。
- StaffDeck 的首屏验证了欢迎语、角色身份、能力概览、建议问题和自然输入可以形成有温度的 AI 产品入口；Curis 需要将这套气质转化为真实的公司创建流程。[StaffDeck](https://staffdeck.openbmb.cn/)
- “空白但不空旷”能同时保留真实性、方向感和探索兴趣，避免假数据与冷清空状态。

## Consequences

- Welcome、Founding Brief 和 CEO Office Seed 必须先设计，再设计后续经营页面。
- 空状态、首次引导、Assistant 介绍和公司空间地图成为全局设计规范的一部分。
- 业务、公司和 Workspace 页面必须使用办公室、版图、团队、存在状态和交接动线表达，而不是只使用列表与后台面板。
- 首次体验必须通过“10 秒知道是什么、30 秒知道 Assistant 是谁、2 分钟表达意图”的验收。
