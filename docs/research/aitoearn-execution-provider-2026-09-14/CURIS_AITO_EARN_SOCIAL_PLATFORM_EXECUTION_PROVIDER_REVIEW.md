# CURIS — AITO EARN SOCIAL PLATFORM EXECUTION PROVIDER REVIEW

Authority Class: REVIEW  
Status: Review  
Disposition: C — PARTIAL PLATFORM PROVIDER CANDIDATE；D — NOT ACCEPTED AS PRIMARY DEPENDENCY  
Owner: CEO / Product Review  
Date: 2026-09-14，Asia/Shanghai  
Target Authority: 无直接写入；以下均为研究判断与候选合同  
Next Gate: CEO REVIEW；获准后另立最小执行验证范围  
Scope: Final Asset → Publish → Result → Analytics Return；不研究机会市场价值  
Boundary: NO CURIS CODE / RUNTIME / SCHEMA / UI / AUTHORITY CHANGE；NO NEW ACCOUNT / PUBLISH / PAYMENT

## 1. Executive Conclusion

**AiToEarn 能减少部分平台的执行工作，但本轮证据不足以让它成为 Curis 第一版唯一或主要的全平台执行依赖。当前选择 C；作为主要依赖仍受 D 阻断。** 不能选“只会发、完全没有数据”的 B：B站、TikTok、YouTube 确有 Analytics Provider。也不能选 A：抖音、小红书这两个优先平台的发布路径和数据回收都有缺口。

五项决定性发现：

1. **抖音公开发布 Provider 的实际动作是生成手机交接，而非服务器无人工直接发帖。** 返回 shareId、短链接和一小时到期时间；必须继续查询最终 videoId。[S11](#s11)
2. **小红书、视频号公开 PublishProvider 主要登记已经完成的发布。** 小红书要求现成 workLink，视频号要求 workId 或 workLink；真正发送素材另由浏览器插件承担。把这两个 Provider 的成功当成“服务器上传并发帖成功”会产生假闭环。[S13](#s13)–[S15](#s15)、D2
3. **数据零值不能一概信任。** 在线页明确显示“已更新0/0”“暂无采集数据”，同时总览为0。TikTok 源码在未获得目标视频时，也可能生成含0指标的非空快照。缺失被折叠后，仅凭 metrics 无法还原真0。E04、[S23](#s23)
4. **当前公开源码登记35个 MCP 工具，但缺账号列表/授权健康、二进制上传、失败重试、完整人工交接获取等工具。** 当前账号的远端 tools/list 没有获得；不把源码清单冒充线上 Discovery。[S08](#s08)–[S10](#s10)、[S31](#s31)–[S32](#s32)
5. **恢复不是普通重试问题。** TikTok 已有“远端接受、ID未落库、重试重复发布”的 Issue；公开代码存在相应危险窗口。数据库唯一键只能限制本地记录，不能保证远端 exactly-once。[S04](#s04)–[S05](#s05)、[S17](#s17)、G586

**完成度：本轮只读可行性审查完成；实际发布、到账数据、故障恢复和 Curis 接入验收均未完成，也未执行。** 所有自动化收益为候选，不改写 Current Implementation Truth。

### 证据版本与口径

| 来源 | 本轮依据 | 限制 |
|---|---|---|
| 公开源码 L2 | yikart/AiToEarn@9413d73918271bd716b9ea59f61c9f59e485619b，HEAD于本轮复核 | 静态实现，未运行后端；不代表商业线上构建 |
| OpenClaw 源码 L2 | yikart/aitoearn-openclaw-plugin@c5c5e722b150167249aafa448ebaee80cb4d3840 | 较主仓库旧；不能据旧工具名定义当前 MCP |
| 已登录产品 L1 | macOS / Chrome，aitoearn.cn；已有会话，频道/发布/统计/互动只读 | Web build、账户tier、国际站账户能力 UNKNOWN |
| 官方文档 L3 | docs.aitoearn.ai，发布Flow、插件、上传、REST | 与公开源码部分不一致，按表面分别判断 |
| Issues L5 | 报告者描述，状态实时读取并存档 | 未复现；closed不等于修复且部署 |
| 建议 L6 | 本报告候选架构/映射/恢复规则 | 非 Curis Authority、非实施验收 |

本文 L2 指源码；输入《抖音深拆》自己的 L2 指官方产品，两套编号不能直接混用。这里引用该文件只作已有研究输入，不把其编号继承成源码证据。

## 2. Curis 当前 Content Growth 执行断点

当前能够用真实云模型承担研究、写作、分析，并在已验证范围内执行员工/Work 协作和 Usage 归因；这不等于所有 Strategy、视频制作、Learning、自主经营都已产品验收。Boundary 已明确：Content Growth 无头链止于 Research→Content→Evaluation，Publishing/Analytics = NOT_CONNECTED / UNAVAILABLE，评估 WAITING。全日独立审查也要求把产品目标、局部实现、真实闭环分开。A1–A3、A5

| 断点 | 当前 Curis 状态 | AiToEarn 候选补位 | 仍不能声称 |
|---|---|---|---|
| Account Connection | 未接通真实外部 Connector | 账号授权与引用接口 | 用户无须首次登录或重连 |
| Content Upload | Final Asset 不是平台可读文件 | 签名上传或公共URL | 本地文件路径可直接给云服务 |
| Publish | AI准备≠真实发布 | API发布/插件/手机handoff | 七平台同样自动化 |
| Multi-platform | 多Variant仍需执行关联 | Flow+多个发布记录 | 原子提交、全成功 |
| Publish Status/Result | 缺实际外部执行回执 | 记录ID、平台ID、URL、失败状态 | 202或code0即发帖成功 |
| Analytics | 当前未连接 | 部分平台API快照 | 所有0都是真实数据 |
| Comment | 未形成自动回收执行链 | 部分平台评论API；国内另有插件 | 统一七平台收件箱已打通 |
| Recovery | 需真实外部未知结果处理 | 查询、finalize、有限retry | 网络异常可无条件重发 |

本轮假定已有合法 Final Asset；不验证 Curis 是否能生成满足各平台规范的成片。不将“Provider能上传”倒推“Curis视频生产已完成”。

## 3. AiToEarn 真实 Execution 能力

源码中存在完整的 Channels 层：Accounts/Auth、Platforms Registry、Publish Flow/Task/Record、Works、Analytics、Engagement、Relay。调用链可追到真实平台服务；不是仅README。统一模型在业务侧压缩了接口数量，但平台实现并不齐平。[S01](#s01)–[S10](#s10)

读取注册模块后，15个平台中 Google Business Profile 仅有授权，没有本轮可接受的发布 Provider；其余包含不同形式的 PublishProvider，其中小红书/视频号为已完成结果登记。9个平台注册了 Analytics Provider。**Provider文件存在、模块注册、配置可用、账号有权、实际调用成功是五个不同条件。** LinkedIn 有 engagement 文件但模块未注册，不能算当前已暴露能力。

L1 本账号只有一个已存在但离线的抖音频道，插件显示未安装；发布编辑器要求选择账号，素材分组为空。没有据此测试发布，也没有新绑定。国际平台在中国站频道面板标为“仅国际站”。

## 4. PLATFORM EXECUTION CAPABILITY MATRIX

“有”均指本轮 L2 实现或明确L3合同；不是当前账号生产验收。“无注册”指公开 Channels 路径，不能排除商业产品其他接口。所有状态均需读第12节，审核不具有统一完成合同。

| 平台 | Account Connection | Publish / 内容 | 同Flow限制 | Status / Result | Analytics | Engage | 人工/可靠性 |
|---|---|---|---|---|---|---|---|
| 抖音 | OAuth或小程序扫码；也有插件路径 | 服务端生成handoff；普通视频/图文素材；插件另可执行 | 同环境、账号有效；handoff独立完成 | WaitingForUserAction；shareId→videoId/URL；过期交接 | 无注册Analytics；粉丝有另一路读取，不证明内容全指标 | 无注册Engagement；插件评论/点赞/收藏 | 手机确认或插件会话；当前账号离线；#549 |
| 小红书 | 浏览器插件同步已有登录 | 插件图文1–9图或视频+封面；服务端只登记workLink | 插件步骤在Flow前；不能直接与API批量上传等同 | 插件success/workId/shareLink；服务端登记成功 | 无注册Analytics；Crawler元数据不是已验证回流 | Channels无注册；插件互动、商业UI另一路 | 会话/域名识别、验证码；#569/#583 |
| B站 | OAuth，平台应用权限 | API上传视频→投稿；category tid必填 | 可以参与兼容环境的Flow | 先resourceId，轮询得到作品结果；失败独立 | 账号粉丝/关注/作品；作品播放赞评分享收藏等 | 无注册 | 初次OAuth/到期重连；媒体可达、分区等校验 |
| 视频号 | 浏览器插件会话同步 | 插件视频+封面；服务端登记workId/link | 插件单独执行，链接可稍后补全 | 成功与linkStatus分开，可能有ID无链接 | 无注册Analytics | 无注册 | 浏览器在线、扫码/验证码、#584频繁离线报告 |
| 微信公众号 | 存在OAuth实现；任意公众号管理授权未证明 | 文章HTML→素材/草稿→freepublish；部署配置身份限制 | 代码模型可表达，不代表任意账号可用 | 异步提交ID→查询文章ID/URL | 无注册Analytics | 无注册 | 必须核验实际发布公众号身份；暂不纳入首批 |
| TikTok | OAuth及应用/账号许可 | Direct Post视频/图文，隐私等creator约束 | 国际站；不能假定与中国站同Flow | publish_id→最终postID；SelfOnly可无最终ID/链接 | 账号粉丝关注赞作品；作品播放赞评分享 | 无注册 | 首次授权、平台审核权限；#586重复风险 |
| YouTube | OAuth频道授权 | 视频上传；封面可单独失败；Shorts分类非简单统一开关 | 国际站、账号许可、配额 | 返回视频ID；公开可见/处理与审核另判 | 频道订阅/视频/浏览；作品浏览赞评 | 读评论、发评论、回复、删除有实现 | 首次授权/配额/平台处理；封面警告不阻止视频成功 |

关键实现：[S11](#s11)–[S26](#s26)；官方插件：D2；模块证据见附录平台索引。

### 其他已注册平台——不授予“稳定支持”标签

| 平台 | 连接/发布模式 | Analytics实现 | Engagement注册 | 当前站点/判断 |
|---|---|---|---|---|
| 快手 | OAuth，视频发布/轮询 | 粉丝关注；作品播放赞评 | 无 | 中国站入口；尚未实发 |
| Facebook | OAuth，发布，Sync路径 | followers；作品曝光/互动用户/点击 | 有，具体动作需动态能力 | 中国站标仅国际站；未验稳定性 |
| Instagram | OAuth，创建容器/轮询 | reach/profile views/website clicks；作品赞评分享收藏等 | 有 | 仅国际站；账号类型与权限未验 |
| Pinterest | OAuth，发布，board必填 | followers/monthly views；曝光收藏点击播放 | 无 | 仅国际站；点击字段归一化有口径风险 |
| Threads | OAuth，轮询 | 浏览/赞/回复/转发/引用等 | 注册但无createComment实现 | 仅国际站；不能由有Engagement推出可回复 |
| X/Twitter | OAuth，Sync发布 | 粉丝关注；赞评转发收藏曝光等 | 有 | 仅国际站；费用/权限另约束 |
| LinkedIn | OAuth，Sync发布 | 无注册 | 文件存在但未注册 | 仅国际站；只列已装配能力 |
| Google Business Profile | Auth only | 无注册 | 无 | 不算已解决Publishing |

没有一个平台在本轮获得“当前账户稳定端到端通过”。媒体类型和动态权限必须消费部署的metadata/option schema，不能固化本表为未来平台事实。

## 5. Account Connection

建议 **Option B为常规路径，Option C为明确缺口的后备；不选同时自建七套授权的A。** 用户在AiToEarn管理平台连接，Curis只引用被授权账号和健康状态，不接收平台Cookie/OAuth Token。AiToEarn连接成功也不等于任何 Curis Employee 都获准在该账号发布。[L6]

| 层 | 所有权/责任 |
|---|---|
| 用户平台账号 | 用户；登录、扫码、MFA、资格仍由用户完成 |
| 平台连接凭据 | 由AiToEarn及其受控浏览器插件/Relay持有，具体托管需验收；不复制进Curis对话 |
| AiToEarn服务访问凭据 | 若未来接入，由安全配置持有，按部署/账号限定；不交给模型展示 |
| Curis授权 | 哪个Employee可对哪个账号做哪种动作、使用哪版内容，由Curis现有责任/授权控制 |
| 映射 | Provider环境+账号ID+平台UID；不能只用昵称或头像匹配 |

REST有 `GET /api/v2/channels/accounts`、`/{accountId}`、`/{accountId}/auth-status`；源MCP无对应账号清单工具。[S27](#s27)、D4–D5 auth-status与平台实际可执行权限不是同一件事：需验证有效期、scope、account type、发布权限、插件在线。账号删除重连后可能产生新ID；#569报告过前端新号而实际发旧号，应把目标身份复核列为验收门，不能据closed断言现已安全。

Relay账号另有 `relayAccountRef`。必须保留本地与远端ID的对应关系及环境；中国站/国际站不可假设共用账号ID或访问配置。重连由AiToEarn正常流程完成，Curis只投影“需重连”。本轮没有执行这些连接动作。

## 6. Production → Publish Input

机器接口已经存在：REST `POST /api/v2/channels/publish/flows`，MCP `createChannelPublishFlow`共享新版内容结构。`flowId`可外部提供；`context.taskId`是外部业务关联；`content`公共，`items[]`包含 `platform/accountId/option/overrides`。hashtags在新版发布内容中通过body解析；不要误用旧Draft接口的独立topics字段。[S03](#s03)、[S09](#s09)、[S33](#s33)–[S34](#s34)

### 6.1 文件桥

本地 `final.mp4` → 公共可达HTTPS URL，或官方三步上传：

1. `POST /api/assets/uploadSign`，给文件名、字节数、type=publishMedia。
2. 向返回uploadUrl PUT二进制；不要额外把AiToEarn凭据带到对象存储。
3. `POST /api/assets/{id}/confirm`，取得data.url；发布使用该最终URL。

本地路径、未授权私有链接、过期URL、只给assetId都不等于合法PublishMedia。URL需要覆盖排程和平台拉取窗口。OpenClaw的 `uploadAssetFromPath` 是本地封装，不能当作远端MCP服务器自带工具。D3

### 6.2 视频示例：Curis Result → B站发布Flow

以下为据源码整理的合同示例，**未调用，ID虚构，.invalid地址不可执行**。实际分区需动态查询，不能直接使用示例tid。Final Asset的hash/版本留在Curis证据，非API新增字段。

```json
{
  "flowId": "curis-demo-work-01-asset-v3-attempt-1",
  "context": { "taskId": "curis-demo-work-01" },
  "publishAt": "2026-09-15T04:00:00Z",
  "content": {
    "title": "一条已审核的短视频",
    "body": "完整说明 #示例话题",
    "media": [{ "url": "https://assets.example.invalid/final-v3.mp4" }],
    "cover": { "url": "https://assets.example.invalid/cover-v3.jpg" }
  },
  "items": [{
    "platform": "bilibili",
    "accountId": "EXAMPLE_ACCOUNT_ID",
    "option": { "tid": 1, "copyright": 1 }
  }]
}
```

MCP context.source由服务端固定为MCP，不允许调用者伪造来源。视频生产结果包含tags数组时，应按目标平台转换成body中的话题语义，不能只是原样塞进不存在字段。

### 6.3 小红书图文：先插件执行，再登记结果

**不能伪造一个“给小红书图片URL即可服务器发布”的Flow例子。** 官方浏览器接口接受以下形状；只展示参数，不提供自动执行语句。D2

```json
{
  "platform": "xhs",
  "type": "image",
  "title": "已审核图文标题",
  "desc": "已审核正文",
  "images": ["https://assets.example.invalid/1.jpg", "https://assets.example.invalid/2.jpg"],
  "topics": ["示例话题"]
}
```

由已安装插件、受信任页面和正确平台会话执行 `AIToEarnPlugin.publish(params,onProgress)`。收到真实success/workId/shareLink后，才可把该完成结果交给含 `platform: xhs`、`accountId`、`option.workLink` 的服务端Flow登记。**workLink必须是真实已发布链接，不是待上传素材链接。** 仅调用createChannelPublishFlow不能覆盖前半段。[S13](#s13)–[S14](#s14)

文章输入则以title、HTML正文、图片/封面进入公众号Provider；图片上传、thumb_media_id、draft/media_id、publish_id属于平台执行内部。任意用户公众号管理授权问题未解决前，不把这个例子扩展成可用承诺。[S19](#s19)–[S20](#s20)、[S35](#s35)

## 7. MCP 能力

**远端 Tool Discovery: NOT OBSERVED。** 本会话没有已配置的AiToEarn MCP工具；当前限制禁止新绑定、取凭据或产生副作用。已完成的是公开服务器源码Tool装饰器与输入Schema核查，共35项（Channels22+Content10+Generation3），完整清单在附录B和JSON。不能说“线上账户当前全部工具已发现”。

| 类别 | 真实工具/接口情况 | Employee能否仅靠它完成 |
|---|---|---|
| 平台能力 | listChannelPlatforms/getChannelPlatform，分类查询 | 可作为动态能力输入；仍需账号许可 |
| 账号 | MCP没有list accounts/auth-status；REST有 | MCP-alone缺口 |
| 发布 | createChannelPublishFlow、即时发布、取消、改排程/更新 | 有副作用，需Curis授权；取消仍受平台限制 |
| 查询 | listChannelPublishRecords、ByRecordId/TaskId/FlowId | 建议按Flow列出全部记录；单条ByFlowId只返回首条 |
| 失败重试 | REST有retry，MCP无对应工具 | 不能猜名字调用 |
| 人工交接 | REST record user-action；MCP未专门暴露 | 抖音handoff链不能只靠公开MCP闭合 |
| 数据 | getChannelAccountAnalytics/getChannelWorkAnalytics | 平台覆盖有限；调用可能触发抓取/落快照，不当纯静态读取 |
| 评论 | list/submit/call function | 按平台注册方法，不是全平台通用 |
| 媒体 | createMedia只登记URL；生成、Draft不是上传 | 本地文件另经Upload API/OpenClaw本地桥 |

两个命名陷阱：[S04](#s04)、[S07](#s07)、[S10](#s10)

- `getChannelPublishRecordByFlowId` 返回 `records[0]`，不是整个多平台Flow。
- createFlow返回的 `tasks[n].id` 是发布记录id；DB的 `taskId`来自 `context.taskId`外部关联。不要拿返回id盲调ByTaskId；优先ByRecordId，或listRecords按flowId获取全体。

**未来可以把MCP作为受控传输方式，但不建议让Employee直接自由使用整个工具集。** 最薄的AiToEarn适配要补REST账号/交接/恢复、结果标准化、权限及幂等约束，先隐藏内容生成、删除和无关工具。OpenClaw现有两个本地辅助 `getAiToEarnEnvironment` / `uploadAssetFromPath` 不计入35个远端工具；旧Playbook里的publishPostToDouyin也不作为新版能力凭据。

## 8. Multi-platform Publish Model

模型是 **Common + Platform-specific settings + Content overrides**，值得复用思想，不复制第二套内容库。

`一份Final Asset版本 → 一个Curis发布意图 → 多个环境/执行分组 → 每组Flow → 每个平台账号独立Record → 平台ID/结果/数据`。

| 差异 | AiToEarn表达 | Curis应保留 |
|---|---|---|
| 标题/正文 | content公共值+items.overrides | 已审核的逐平台Variant版本，不静默AI改写 |
| 多媒体/封面 | overrides.media/cover，cover=null清空 | 转换后文件hash、来源与内容关系 |
| 标签 | body话题解析；插件topics另形状 | 统一意图、按真实接口转换 |
| privacy/category | 每个平台option，动态取值 | 用户发布意图与合法选项 |
| schedule | 顶层publishAt；部分平台option另有原生排程 | 目标时间、时区、平台接受时间分开 |
| 成功/失败 | 每个item独立Record | 部分成功；不能整Flow重发 |

五平台短视频场景：B站API、中国站抖音handoff、小红书插件登记、国际站TikTok与YouTube，**没有证据能在当前账号用一次调用全部成功**。源码还明确拒绝混合Relay和非Relay账号的单一Flow。应按环境和执行方式拆组，Curis仍只有一个工作意图与各外部引用。[S04](#s04)、E01

验证所有账号和输入在服务端创建记录前进行，但这不是跨平台事务：某平台之后成功、另一个失败，无自动rollback；插件发帖可能早于服务端登记。重新登记与重新发帖必须是两个动作。metadata全部scheduleByPlatform=false的表述与YouTube option.publishAt不应混成“无排程”：一个是AiToEarn调度，一个是平台原生设置，需分别验证。

## 9. Douyin 深拆

公开 `DouyinPublishProvider.publish` 检查platformUid后直接进入 `createHandoffPublishResult`。它解析媒体与话题，取shareId，生成分享schema/shortLink，返回202+userAction，expiresAt为一小时后。Task层投影WaitingForUserAction。[S11](#s11)

正常链路为：素材可达 → 创建记录 → 取得交接链接 → 用户手机打开并在正确账号确认 → getSharePublishResult/share webhook → 获得videoId → Published与作品URL。**shareId是操作引用，不是已公开作品ID。** `verify`/`finalize`只有见最终videoId才返回已发布；无ID继续等待。当前cancel实现返回false，不能向CEO承诺“停止后手机旧链接失效”。

| 问题 | 本轮答案 |
|---|---|
| 如何连接 | OAuth或小程序扫码；mini-app回调验证用户与scope；中国站本账号现在离线 |
| 能否从AiToEarn发普通视频 | 存在协助发布链，但公开服务端路径需要手机交接；插件另有自动化路径 |
| 手机确认是否必须 | 对所读server handoff路径是；不能拿插件文档取消这个条件 |
| 发布结果 | 查询最终videoId/link；短链接生成/打开不等于发帖 |
| views/likes/comments/shares | Channels无注册Analytics Provider；不能承诺自动获取这四项 |
| followers | mini-app授权/频道资料有粉丝读取；页面提示有刷新条件；不是完整内容分析 |
| 更新频率 | 没有验证内容数据实时或T+1 SLA。L1粉丝刷新提示每平台一小时限制、离线跳过、部分条件次日；不外推到作品指标 |
| 评论读取/回复 | 公开Channels无注册；插件文档有评论/点赞/收藏，未证明完整评论回收+定向回复 |
| 商品/团购/任务/星图 | 当前Publish option未找到相应挂载/交付参数；不能作为已支持 |

#549为旧MCP工具的短链接15100报告，证明此类handoff值得验收，不证明新版相同故障必然存在。把源码getSharePublishResult的调用存在当成当前商业服务可用同样不成立。**Normal Content Loop仅部分可补；Monetization Content Loop未因此打通。**

## 10. Xiaohongshu 深拆

连接在已登录浏览器插件里完成，不是server AuthProvider OAuth。官方文档要求正确浏览器profile、插件和受信任来源；登录辅助可能涉及Cookie，Curis模型不应读取它，本轮也未调用。D2

| 项 | 真实合同 / 限制 |
|---|---|
| 图文 | plugin type=image，images 1–9，title/desc/topics |
| 视频 | plugin type=video，video和cover必填 |
| 标签 | plugin topics是不带#的名称；和server body解析区分 |
| 标题/正文 | 公开metadata标题20/正文1000；这是该版本应用约束，不认证平台永久限制 |
| 计划发布 | 文档不推荐XHS scheduledTime；不能把公用字段等同平台可靠排程 |
| 结果 | plugin success/workId/shareLink/publishTime；服务端workLink登记并解析 |
| 账号选择 | 发布前确认platform UID与当前插件会话，昵称不足 |
| Analytics | metadata有Crawler类型但没有注册AnalyticsProvider；商业采集页不是已验MCP回流 |
| Comment | 插件有互动动作；线上有付费评论搜索入口；无本轮自动评论闭环 |

重要可靠性证据：#583仍open，国际rednote.com登录识别失败；#569已closed，报告更换账号后发布到旧号；不能据这些报告量化失败率，也不能忽略账号串用的验收需求。没有真实登录新小红书或发布测试，因此当前用户是否可用UNKNOWN。

## 11. 其他平台

**B站：最适合中国站首个API执行候选之一。** 有上传/投稿/轮询、分区取值和Analytics。option.tid必填；转载需source，copyright语义不可忽略。投稿取得resourceId不等于最终公开作品。封面可达性、分区、版权与授权仍需验证；不能用成功HTTP替代最终链接。评论回收未注册。[S16](#s16)、[S24](#s24)

**YouTube：接口链较完整。** publish上传后读取videoDetails核验频道；设置缩略图失败可能仅记录warning，仍返回视频成功。因此“视频已发”和“封面完全符合Final Asset”要分验。Analytics是基础计数，未证明完播、watch time、流量来源或收益；评论读/回有真实实现。[S18](#s18)、[S25](#s25)–[S26](#s26)

**TikTok：API能力有价值，恢复风险阻断自动依赖。** init→上传→返回publish_id，finalize查询最终ID。SelfOnly成功分支可能保留publish_id和pending链接；Published也不保证有可公开URL。隐私、禁duet/stitch/comment、AIGC/商业内容标签等须依据creator允许值，不能默认PUBLIC。#586与代码显示远端提交前后需要严谨checkpoint。[S17](#s17)、G586

**视频号：插件执行，云端登记。** 可拿workId但链接稍后解析；文档还有wxSphStartLinkPolling以recordId/mediaMd5sum等继续处理。#584报告一天多次重登；当前closed并不是本账号复验。该路径应作为有浏览器条件的辅助执行候选。[S15](#s15)、D2

**微信公众号：暂不进入首批。** publish确实调用上传图片、addDraft、freePublish；但WeChatService使用部署配置appId/appSecret取得服务令牌；AuthProvider走用户网页OAuth。源码没有证明“连接任意用户公众号后，用该公众号独立authorizer credential发布”的完整能力。这个身份边界必须由官方/部署端说明并实测，不将其解释为已经确认的安全漏洞，也不宣传任意公众号支持。[S19](#s19)–[S20](#s20)、[S35](#s35)

## 12. Publish Result

有可用的外部记录框架，但需保留原始语义。[S05](#s05)–[S07](#s07)

| 原始PublishStatus | 值 | Curis候选展示 |
|---|---:|---|
| Failed | -1 | 执行失败；仍判远端结果是否确定 |
| WaitingForPublish | 0 | 等待计划执行 |
| Published | 1 | Provider确认完成；另验最终ID/公开性/素材一致性 |
| Publishing | 2 | 已运行，不能另发 |
| WaitingForUpdate | 3 | 等待更新既有作品 |
| Updating | 4 | 更新中 |
| UpdatedFailed | 5 | 更新失败，原作品可能仍存在 |
| Queued | 6 | 排队中 |
| PlatformScheduled | 7 | 平台已接受排程，不是已公开 |
| WaitingForUserAction | 8 | 需人工交接 |
| Canceled | 9 | 取消记录；需确认是否还能由已发出handoff产生结果 |

还要独立保存 `linkStatus=pending/ready/failed`。record的platformWorkId可能先是shareId/publish_id/resourceId，最终才是作品ID；TikTok私密完成甚至保留操作ID。`publishTime`在计划阶段与完成阶段可能语义不同，不能无条件命名为actualPublishedAt。

接口 `code:0` 是请求业务成功；Provider200/202是内部处理结果，不等同HTTP状态或平台公开可见。没有发现跨平台统一的platform_reviewing枚举，因此审核中/受限可见/仅本人可见需原始平台字段或另行查询，不填造的已审通过。

## 13. Analytics Return

### 13.1 当前实现覆盖

| 平台 | Account Analytics | Work Analytics | 来源与不足 |
|---|---|---|---|
| B站 | fans/following/work | views/likes/favorites/shares/comments；coin/danmaku额外值 | API；不是收入/成交/完整观看质量 |
| TikTok | followers/following/likes/video count | views/likes/comments/shares | API；missing video可折叠为0 |
| YouTube | subscribers/videos/views | views/likes/comments | API；无watchtime/CTR/收入验收 |
| 快手 | followers/following | views/likes/comments | API；覆盖有限 |
| Facebook | followers | impressions/engaged users/clicks | API；不同口径不可直接同义汇总 |
| Instagram | reach/profile views/website clicks等 | reach/likes/comments/shares/saved/total interactions | API；权限、媒体类型影响返回 |
| Pinterest | followers/following/monthly views/pins | impressions/save/click/video views | 不同click来源映射同字段，可能覆盖 |
| Threads | views/likes/replies/reposts/quotes/followers | views/likes/replies/reposts/shares/quotes | repost/share归同字段，口径需查 |
| X/Twitter | followers/following/work/likes | likes/replies/retweets/bookmarks/impressions；quote extra | 缺失字段也有默认0 |
| 抖音/小红书/视频号/公众号/LinkedIn | 本轮未见注册Analytics | 本轮未见注册Analytics | 不能将单个service函数/爬虫标签当完整AnalyticsAPI |

### 13.2 时间、无数据与真实性

源码AnalyticsService有fetchedAt、snapshots和归一化metrics；不支持时返回空snapshots及message。官方work analytics文档说未采集时code0、空snapshots且不带metrics。**不同层并不完全一致**：公开服务按账号Provider取数据，hosted文档可能是采集结果查询；不能推断线上使用完全同一源码。[S21](#s21)–[S25](#s25)、D6

L1本次复看统计页：日期2026-09-07—13，显示“已更新0/0”“暂无采集数据”，六项0及“该时间范围内暂无发布作品”。没有点击“查询数据”或“刷新”。**这些0应读为界面空态，不能读为账号经营实测0。**E04

L2更强风险：TikTok `video=response.videos?.[0]` 后，仍以输入id作fallback，并把缺失计数 `Number(...??0)` 写入非空snapshot。故“有snapshot+metrics=0”仍不足以证明真实0。B站/YouTube等也对缺失计数默认0。

多个Provider的snapshotAt采用作品publishedAt，而非本次指标观测时刻。fetchedAt最多证明拉取时间，不能证明上游实时程度。必须拆开作品发布时间、采样时间、获取时间和统计区间；不能把发布日期画成每次更新的时间。

### DATA QUALITY CANDIDATE

| 情况 | 可接受证据 | Curis分析规则 |
|---|---|---|
| 真0 | 上游明确返回该指标、身份/作品匹配、采样范围明确 | 作为0参与分析 |
| 未采集 | 空snapshots/明确未采集message | NULL/UNKNOWN，不计失败表现 |
| 不支持 | capabilities和具体响应一致指明不支持 | UNSUPPORTED，不循环重试 |
| 连接失败 | auth error/账号健康失败 | CONNECTION_FAILED，不填0 |
| 过期 | 合同已定义freshness阈值且超过 | STALE，保留旧值/旧时间 |
| 被默认值覆盖 | 只剩normalized0，raw存在性无法判断 | UNVERIFIED_ZERO，不能入经营Truth |

这些是L6消费原则，不新建Schema。应优先让Provider返回原始字段存在性与采集状态；拿不到则降低可信度。没有证据支持“接入即每日自动可靠回收全部平台数据”。还需合法的周期触发、额度、增量口径和重叠样本去重；不把累计数当周期增量。

## 14. Engage

Channels MCP确有读评论、提交评论和function调用；submit schema有parentCommentId。但平台没有注册对应方法时，公用工具不会让能力凭空出现。[S08](#s08)–[S10](#s10)

YouTube可分页读顶层评论，parent分支调用replyComment，返回platformActionId；它列的是评论线程的顶层信息，不证明已经完整遍历全部楼中楼。[S26](#s26) Facebook/Instagram/Twitter注册了Engagement，具体动作按动态方法判断。Threads注册不意味着createComment；LinkedIn文件未装配不计入。

抖音/小红书：官方插件提供评论、点赞、收藏等动作，需浏览器会话；这与服务端 `listChannelEngagementComments` 是不同接口。线上“AI互动”页面可见评论搜索结果，按钮明确搜索消耗10积分。本轮只查看现有结果，未搜索/回复/互动；不能把搜索能力当成免费、持续、自有作品评论同步接口。E05、D2

候选接法：评论作为外部Evidence输入→Employee拟答→按现有授权执行→保留comment/action id与对应原文。无读取或无reply定位的目标平台仍人工；禁止用“有comment字段”承诺完整客服闭环。

## 15. Human Handoff

| Trigger | 人做什么 | 系统能继续做什么 |
|---|---|---|
| 初次平台授权/过期 | 正常登录、扫码、MFA | 重新读健康与目标身份 |
| 抖音server发布 | 打开本次有效链接并确认 | 按同一shareId查询最终作品，收回执 |
| 插件未安装/会话失效 | 未来经授权安装/恢复会话 | 继续已有意图，不创建新发布副本 |
| CAPTCHA/风控 | 人处理平台要求 | 保持waiting；plugin needHumanAssist不自动循环重试 |
| 审核/资格不足 | 按平台要求补材料/决策 | 记录等待/拒绝，不伪造成功 |
| 未知结果 | 核对作品历史与实际账号 | 先对账；确认未发布后才允许新尝试 |

Handoff应包含目标账号、待完成动作、关联记录、有效期、完成判据。CEO点击“完成”是报告，不是平台事实；最终仍查询可核验结果。发布手机动作不应要求用户重复输入本可由AI备齐的标题/素材，但是否确实预填完整未实测。

## 16. Failure / Retry / Unknown Outcome

源码优势：flowId可由外部提供；账号/平台输入前验；数据库有用户+flow+account+type唯一约束；失败任务有查询/finalize/retry路径。局限：重复flowId报已存在，不是直接返回原始结果；必须查询。记录唯一不保证平台副作用唯一。[S04](#s04)–[S05](#s05)

`retryTask`只有Failed可进入；若已有platformWorkId优先finalize，不另发布；无ID会走retryUnsubmittedTask。TikTok发布初始化之后、ID持久化之前出现网络/上传错误，仍可能无ID而远端已接受。#586明确报告此情形；#587修复PR已closed但未merged，不能把其“测试69项通过”写成当前主干修复。G586–G587

### EXTERNAL EXECUTION RECOVERY CONTRACT — CANDIDATE ONLY

| 已知状态 | 允许动作 | 禁止动作 |
|---|---|---|
| 本地输入验证失败、尚未发请求 | 修正后按新内容版本提交 | 把失败算平台拒绝 |
| 请求是否到达不明 | 查询原flow/record、平台历史；标UNKNOWN_OUTCOME | 新flowId直接重发 |
| 已有远端operation ID | 对原ID查询/finalize，必要时人工核对 | 再调用publish init |
| WaitingForUserAction | 读取本条user-action，核对有效期 | 创建多份交接导致多个可执行链接 |
| 某些平台成功 | 只处理确定失败的item | 重发整个多平台Flow |
| 平台确认未接受且内容未变 | 在已批准政策内单条重试，记录attempt | 无限重试/改变账号绕过失败 |
| Published但缺URL | 链接解析/对账，保留成功事实及缺口 | 再发一条以获得URL |
| 数据采集失败 | 重新获取指标，不动发布记录 | 因数据缺失重发作品 |

最小候选记录：稳定外部意图键、asset版本hash、目标环境/账号、provider recordId、operation id与final content id分开、提交时间、每次尝试、结果确定性。未知状态不得自动进入Learning的成功/失败样本。无需先造通用分布式执行框架；先在一个AiToEarn适配中落实这些约束。

## 17. Result Mapping 到 Curis

映射原则：**Curis保留Work/Result/Evidence和原scope；AiToEarn提供外部执行事实，不成为第二个Work系统。** Company/Department/Business/Workspace的既有范围不得被新Provider强迫改成“所有Result属于Business”。A3

| Curis语义候选 | AiToEarn来源 | 注意 |
|---|---|---|
| Work关联 | context.taskId | 外部关联而非provider record主键 |
| external_execution_ref | 环境+flowId+record.id | 每账号item独立；不只存flow |
| platform/account | record账号+platform UID映射 | 保留重连/Relay映射版本 |
| content version | Curis已有Result/asset证据 | 上游修改不能覆盖发布时版本 |
| status | 原始PublishStatus+确定性 | 更新失败与首次发布失败分开 |
| remote operation ref | shareId/publish_id/resourceId | 不混成final content id |
| platform_content_id/url | 已核实的最终ID/workLink/linkStatus | private/审核可能无公共URL |
| published_at | 平台实际时间，或标Provider确认时间 | 不把计划时间改名实际时间 |
| handoff/failure | user-action endpoint/errorMessage | 过期链接与未知结果可区分 |
| analytics refs | snapshot来源、指标存在性、采样/拉取时间 | normalized0不足以作Truth |

这是映射建议，不宣称Curis已有这些字段或需要新增表。先对账现有Execution/Result/Evidence合同，再决定最小扩展。只导入去敏的证据，不把credential/raw authorization抄回Conversation。

## 18. Browser Plugin / Relay

| 机制 | 真正解决什么 | 不解决什么 |
|---|---|---|
| Browser Plugin | 在本地正确平台session下执行小红书/视频号/抖音发布与部分互动；提供progress和结果 | 不等于云MCP可直接操纵用户浏览器；不保证会话永久有效 |
| Relay | 把受限本地平台请求转发到远端AiToEarn；映射account ID、处理授权callback；可转存本地素材URL | 不自动消除手机交接、插件依赖、账号权限、服务可用性 |
| Curis薄适配 | 把现有Work意图映射为Provider请求和回执 | 不重建AiToEarn团队/Agent/素材库/市场 |

源码RelayExceptionFilter捕获Relay账号/授权异常，转发原请求，替换本地账号引用；授权加callback，媒体URL必要时上传到Relay。Analytics/Works/Engagement也可能走Relay分支。因此Relay不仅是“登录桥”。HTTP filter能转发不意味着所有MCP内部服务异常同样转发成功；该transport差异尚未运行验证。[S21](#s21)、[S28](#s28)–[S30](#s30)

**直接调用托管服务，通常可免于自建Relay，但不能保证完全免于本地插件桥或Provider Adapter。** 尤其XHS/视频号源码云端只是登记结果；要减少人工，必须证明合法的现有插件调用方式能从Curis受控动作触发，并把回执带回来。尚无证据Curis native WebView获得插件注入；不要先实现再声称已支持。

## 19. Provider Architecture 建议

CURRENT：只读研究结果，可把AiToEarn列为外部执行候选；不进入Curis Core依赖。  
NEXT：CEO批准后，验证一个API平台和一个国内插件/handoff平台，连同数据质量与恢复。  
FUTURE：实测通过的平台进入可替换Provider选择，缺口保留官方API或人工handoff。

候选流程：

`Curis现有Work/授权/Final Asset → AiToEarn薄适配（账号能力校验、输入映射） → API / Plugin Handoff → 查询原执行记录 → Curis Result/Evidence → 有质量标记的数据 → Analysis → 下一轮决策`。

Employee可发起受控请求；Connector配置负责秘密，执行边界负责权限，AiToEarn负责平台操作，Curis负责业务判断。未获得数据时应继续等待/请求补证据，而不是让AI根据0制造“运营下降”结论。无需先建第二个调度器、媒体系统、平台账号主数据或新的Work实体。

## 20. BEFORE / AFTER AI-USER Boundary

此表为A1逐项重评的候选差异；**After不是已实施**。

| A1原边界 | AiToEarn之后可能变化 | 不能消除 |
|---|---|---|
| Account首次接管USER REQUIRED | 在AiToEarn做一次授权，Curis引用 | 扫码/MFA/到期重连 |
| 普通发布AI ASSISTED/API FUTURE | B站/YT/TT API封装；抖音转手机handoff；XHS转插件 | 平台许可、确认/会话、内容审批 |
| 多平台人工切换 | 公共资产+各自Variant统一提交/跟踪 | 中国/国际/Relay/插件分组、部分失败 |
| 数据手工文件回填 | 已注册且质量合格的平台可候选自动回收 | 抖音/XHS等未证能力、缺失/真0歧义 |
| 评论拟稿后用户发送 | YT等可走受控reply；国内插件可候选互动 | 国内完整评论回收、风控与发送授权 |
| COMPUTER USE候选 | 某些插件已封装，无需重写全部UI自动化 | 插件集成/可信来源/会话仍需验证 |
| Failure人工核对 | 自动先查record和operation id | 远端未知且无可对账ID时仍人查 |
| Analysis/Learning | 增加真实外部证据后更有价值 | 接口存在不会自动完成Curis分析链验收 |
| 变现绑定/送审 | 无充分新执行证据，保持原边界 | 商品/团购/任务/星图/实名/结算 |

A1的“发布并非永远USER REQUIRED”得到进一步具体化，但没有证据把“抖音全面自动、数据自动”升级为Current。

## 21. 变现内容执行边界

| 类型 | 普通素材发布 | 商业绑定/提交 | 数据回收 |
|---|---|---|---|
| 商品带货 | 可准备并经相应普通发布路径 | 未见抖音商品挂载参数，不能支持承诺 | 无订单/佣金/退款闭环证明 |
| 团购 | 可准备视频/位置相关内容 | plugin location不等于团购商品/套餐挂载 | 无核销/佣金证明 |
| 变现任务 | 可发布符合题材的普通内容 | B站mission_id是投稿活动选项，不能泛化成全平台赚钱任务绑定 | 无统一任务结算Proof |
| 商单/星图 | 可准备/分发普通素材 | 无星图接单、送审、交付API证据 | 无品牌验收/结算闭环证明 |

TikTok商业内容声明是披露/合规参数，不等于商品链接；标签也不等于任务正式绑定。本轮不评估任务市场机会、不接单、不讨论收益可达性。

## 22. 已解决的问题

这里“已解决”限定为AiToEarn已有实现，非Curis接入验收：

- 共享内容+逐平台参数+每账号独立记录的发布表达。[S03](#s03)–[S04](#s04)
- B站/YouTube/TikTok等真实上传/发布服务包装。[S16](#s16)–[S18](#s18)
- 记录状态、排队、延时、人工交接、最终结果查询的基本骨架。[S05](#s05)–[S07](#s07)、[S11](#s11)
- 多个平台基础Analytics与部分评论API归一化。[S21](#s21)–[S26](#s26)
- 独立公共素材上传、浏览器插件发布合同和Relay连接机制。D2–D3、[S28](#s28)–[S30](#s30)

这些足以证明“不必默认从零开发每个平台全部接口”。

## 23. 仍未解决的问题

1. 当前账号抖音离线，插件未安装；没有可执行验收基础。
2. 远端MCP实际tools/list与部署version未验证；源码与hosted接口有差异。
3. 抖音服务端要求手机handoff；XHS/视频号执行在插件，云端receipt不可代替发布。
4. 国内优先平台Analytics与完整评论回流不够；missing→0存在实际源码分支。
5. 远端接受/本地超时的去重与未知结果安全恢复未通过。
6. 中国站/国际站、Relay/非Relay混合Flow未打通。
7. 平台审核、私密可见性、最终作品ID、封面一致性与时间口径未统一验收。
8. 公众号任意账号管理授权和发布身份未证明。
9. 凭据所有权、账号身份、quota/收费、服务SLA需部署级确认。
10. Curis适配与业务反馈链尚未集成；不能把报告变成已交付能力。

## 24. 是否停止 Curis 自研各平台 Adapter

**停止“七个平台全部默认平行自研”的规划惯性；不要删除已有实现，也不要宣布不再需要平台适配。** 优先验证AiToEarn能稳定覆盖的具体能力，复用API封装，Curis仅保留薄适配与既有授权/证据机制。[L6]

| 平台 | 建议 |
|---|---|
| B站 / YouTube | 优先验证AiToEarn，暂不重复造完整发布SDK |
| TikTok | 先通过未知结果/重复发布验收，再放开自动执行 |
| 抖音 | AiToEarn可作handoff候选；官方API路线仍有必要保留，不等于立即自研 |
| 小红书 / 视频号 | 先证明现成插件桥可用；不先写自有爬虫/插件，也不假设无需桥 |
| 公众号 | 核清目标身份和授权前暂停接入设计 |
| Analytics缺口 | 保留可信导出或另Provider；不要用假0补齐表格 |

未来替换先通过现有Connector/Capability边界，只有出现第二个真实Provider需要时再抽取共同实现；不预建大型Social Platform框架。

## 25. 最终架构结论

| 选项 | 判定 | 原因 |
|---|---|---|
| A 主要Social Execution Provider | NOT ACCEPTED | 国内核心平台闭环、稳定性、远端接口与数据质量未达标 |
| B 仅Publishing，Analytics全另找 | 不准确 | 部分平台已有真实Analytics，不能全盘否定 |
| C 部分平台Adapter补充 | **CURRENT RECOMMENDATION** | API平台有具体复用价值，国内插件/handoff可补部分步骤 |
| D 当前不适合依赖 | **适用于唯一/主要生产依赖** | 未获得实际执行、恢复和数据真实性验收，不是断言所有功能不可用 |

值得作为V1的**第一优先验证对象**；不值得在今天作为V1已确定主要执行底座。若未来B站/YT与国内一平台通过完整验收，可扩大Publishing职责；Analytics仍逐平台逐指标授权进入Truth。

## 26. 下一步最小验证

仅提出方案，**本轮未执行**。不需要再研究完整机会市场，也不需要先实现Curis集成。

| Gate | 最小动作（需另批准对应外部动作） | 通过标准 |
|---|---|---|
| 1 只读接口 | 用户安全配置现有服务访问；获取远端tools/list、version、platforms、accounts/auth-status | 实际Schema归档；可执行账号与环境映射一致；不导出凭据 |
| 2 单一API平台 | 已授权研究内容，在一个合法测试目标上一次发布；默认私密/草稿仅当真实支持 | 最终ID、实际目标账号、素材/封面一致、链接/可见性分别验证 |
| 3 国内链路 | 在抖音handoff或XHS插件选择一个，明确用户参与与回执桥 | 仅一次发布；交接到期/会话条件清楚；返回同一Work外部引用 |
| 4 数据 | 对一条已知作品核对正数、真实0、无数据/无权限 | 逐指标原始存在性、时间口径匹配；缺失不会伪装0 |
| 5 恢复 | 优先隔离测试环境注入超时；不在真实账号随意制造重复发布 | 远端已接受后只查原operation；不再init；部分成功不整组重发 |
| 6 范围扩展 | 以上通过后才批准Curis薄适配Issue | Allowed Files/授权/证据/失败边界明确；不另造Work系统 |

人工减少暂不报百分比。未来记录每平台每条内容：上传/填字段/确认/贴回执/导数据/故障核对的人工次数与耗时；按同等内容和平台数对照。当前只有“哪些步骤可能减少”的证据，没有“减少85%”的计量。

### 最后用白话回答14个CEO问题

1. **做完视频今天能直接发抖音吗？** 有AiToEarn协助发布路径，但当前账号离线；公开server路径还需手机确认，Curis也未接入。不能承诺今天自动直发。
2. **能同时发多平台吗？** 模型支持多账号Flow；五平台跨中国/国际和插件路径不能假定一个调用全完成。
3. **各平台自动到哪？** B站/YT/TT有API上传发布；抖音server到手机交接；XHS/视频号依赖插件执行；公众号管理身份仍待证明。
4. **哪些还需要人？** 首次授权/重连全平台；抖音handoff；插件会话/验证码；平台审核和资格动作。
5. **发布结果能可靠回Curis吗？** 有记录查询结构，但未集成验收；必须区分操作ID、作品ID、链接与公开性，并防未知结果重复发。
6. **数据能自动回来吗？** 部分平台有接口，国内核心平台未证明完整回流；还需触发、权限、额度和质量规则。
7. **能区分0/未采集/不支持吗？** 空响应可区分一部分，但某些Provider已把缺失压成0；normalized metrics单独不够可信。
8. **评论互动能回来吗？** YT等有真实读/回复实现；抖音/XHS公开Channels未补齐，插件/商业搜索是另一条链。
9. **MCP够Employee直接用吗？** 不够覆盖全链；账号健康、文件上传、handoff、retry等要补接口，且远端Discovery尚未验证。
10. **还要自研各平台Adapter吗？** 不应全量平行重做；先薄适配AiToEarn，缺口按实证保留官方API/人工方案。
11. **人工能少多少？** 暂不能量化。成熟API路径可能减少上传、重复填字段、贴链接、导基础数据；国内链减少幅度取决于handoff和插件。
12. **消除不了什么？** 身份/授权、验证码、某些手机确认、商品/任务绑定、平台审核、未知结果人工对账。
13. **放哪层？** Curis既有外部能力/执行Provider层，提供外部事实；不替换Business/Employee/Work/Result。
14. **作为V1主要Provider值得吗？** 值得优先验证，不足以现在定为主要或唯一依赖；当前C，主依赖受D gate约束。

**VERDICT：READ-ONLY PROVIDER REVIEW COMPLETE；LIVE EXECUTION / CURIS INTEGRATION NOT VALIDATED。**  
**CURIS AUTHORITY / CODE / RUNTIME / SCHEMA / UI：UNCHANGED BY THIS REVIEW。**  
**STOP FOR CEO REVIEW。**

---

## 附录A. Evidence Index

### Curis输入与研究约束

- **A1** [Content Growth AI/User Boundary](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_CONTENT_GROWTH_AI_USER_OPERATING_BOUNDARY.md>) — RESEARCH / BOUNDARY REVIEW，Draft；B2、B3、B4、B5。
- **A2** [Douyin Real Platform Deep Dive](</Users/yy/Documents/Curis AI Workspace/docs/01_Product/CURIS_DOUYIN_REAL_PLATFORM_OPERATING_DEEP_DIVE.md>) — RESEARCH，Draft；先前平台观察，不升级成Current。
- **A3** [全日独立产品推导审查](</Users/yy/Documents/Curis AI Workspace/docs/research/full-product-rethink-2026-09-14/CURIS_2026_09_14_FULL_PRODUCT_RETHINK_REVIEW.md>) — REVIEW，Review；已固定24小时窗口、Current/Implementation分界、历史AiToEarn研究H1–H5。历史85%复用估计没有作为本报告事实。
- **A4** [本轮原始请求](</Users/yy/.codex/attachments/a09641cf-1482-4cce-862e-026f9b0f186f/pasted-text.txt>) — 本轮限制以这份用户请求为准。

- **A5** [CURRENT_STATE: Content Growth execution proof](</Users/yy/Documents/Curis AI Workspace/docs/00_Context/CURRENT_STATE.md:288>) — Implementation Truth；本轮读取该段，Publishing/Analytics未连接、Evaluation等待。

### L1只读操作

- **E01** [频道与平台状态](evidence/01-account-platform-state.txt)，[截图](evidence/01-account-platform-state.png) — 已有抖音离线，插件未安装，国际平台标仅国际站。
- **E02** [发布历史](evidence/02-publish-history.txt) — 当前日历可见范围，无本轮新发布。
- **E03** [空发布编辑器](evidence/03-publish-editor.txt) — 未选账号、未填内容、未上传。关闭出现保存提示，选择取消，再导航到统计页；未确认保存。
- **E04** [统计页](evidence/04-analytics-state.txt)，[截图](evidence/04-analytics-state.png) — 本轮重新观察0/0+暂无采集+总览0；没有点击查询/刷新。
- **E05** [互动入口](evidence/05-engagement-entry.txt) — 现有页面显示搜索消耗10积分；未执行搜索/回复，现有结果正文未纳入报告。

Web build/账户tier UNKNOWN。旧研究创建的CURIS-RESEARCH-TEST-2026-09-14仍保留；本轮未新建对象、未清理它。未读取凭据、Cookie或Authorization Header。

### L3官方文档

- **D1** [发布工作流](https://docs.aitoearn.ai/zh/use/publish-flow/index) — 本地快照zh_use_publish-flow_index.md。
- **D2** [浏览器插件发布接口](https://docs.aitoearn.ai/zh/use/plugin-publish/index) — 本地快照zh_use_plugin-publish_index.md。
- **D3** [素材上传](https://docs.aitoearn.ai/zh/use/asset-upload/index) — 本地快照zh_use_asset-upload_index.md。
- **D4** [账号列表](https://docs.aitoearn.ai/api-reference/get-api-v2-channels-accounts) — 对应本地快照。
- **D5** [账号授权状态](https://docs.aitoearn.ai/api-reference/get-api-v2-channels-accounts-account-id-auth-status) — 对应本地快照。
- **D6** [作品Analytics](https://docs.aitoearn.ai/api-reference/get-api-v2-channels-works-platform-platform-work-id-analytics) — 无数据语义与响应结构。
- **D7** [创建Flow](https://docs.aitoearn.ai/api-reference/post-api-v2-channels-publish-flows)、[重试](https://docs.aitoearn.ai/api-reference/post-api-v2-channels-publish-tasks-task-id-retry)、[人工动作](https://docs.aitoearn.ai/api-reference/get-api-v2-channels-publish-records-record-id-user-action) — 本地快照与docs-manifest.json可追溯。

### Issue / PR报告者证据，不是本轮复现

- **G549** [#549](https://github.com/yikart/AiToEarn/issues/549) — open，旧工具抖音短链接失败报告。
- **G569** [#569](https://github.com/yikart/AiToEarn/issues/569) — closed，小红书账号映射异常报告。
- **G583** [#583](https://github.com/yikart/AiToEarn/issues/583) — open，rednote.com登录识别报告。
- **G584** [#584](https://github.com/yikart/AiToEarn/issues/584) — closed，视频号频繁离线报告。
- **G586** [#586](https://github.com/yikart/AiToEarn/issues/586) — open，TikTok未知结果重试重复发帖报告。
- **G587** [PR#587](https://github.com/yikart/AiToEarn/pull/587) — closed/unmerged；不作为主干已修复证据。状态与正文存selected-issue-evidence.json，合并字段另存pr-587-status.json。

### L2关键源码（统一repo / commit / path / symbol）

以下全部来自 `yikart/AiToEarn@9413d73918271bd716b9ea59f61c9f59e485619b`；符号按声明核对，未运行代码。

<a id="s01"></a>**S01** [PlatformIntegrationRegistry](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/platforms.registry.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/platforms.registry.ts`；注册能力与实际 Provider 的区别。

<a id="s02"></a>**S02** [PlatformRegistryModule](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/platforms.registry.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/platforms.registry.module.ts`；平台模块装配。

<a id="s03"></a>**S03** [CreatePublishFlowSchema / PublishFlowContextSchema](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/flows/publish-flow.dto.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/flows/publish-flow.dto.ts`；发布输入与外部关联。

<a id="s04"></a>**S04** [PublishFlowService.createFlow](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/flows/publish-flow.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/flows/publish-flow.service.ts`；验证、幂等键、账号分组和记录创建。

<a id="s05"></a>**S05** [PublishTaskService.processPublishJob / retryTask](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/tasks/publish-task.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/tasks/publish-task.service.ts`；执行、恢复、取消。

<a id="s06"></a>**S06** [PublishRecordVo](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/records/publish-record.vo.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/records/publish-record.vo.ts`；对外结果字段。

<a id="s07"></a>**S07** [PublishRecordReadService](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/records/publish-record-read.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/records/publish-record-read.service.ts`；记录查询、Relay 合并与 user action。

<a id="s08"></a>**S08** [ChannelsMcpController](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts`；22 个 Channels 工具。

<a id="s09"></a>**S09** [CreateChannelPublishFlowSchema 等](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels-mcp.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels-mcp.schema.ts`；MCP 输入合同。

<a id="s10"></a>**S10** [ChannelsMcpService](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.service.ts`；工具实际调用及单记录返回。

<a id="s11"></a>**S11** [DouyinPublishProvider.publish / createHandoffPublishResult / finalize / verify](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin-publish.provider.ts`；抖音交接和最终 ID。

<a id="s12"></a>**S12** [DouyinAuthProvider.generateAuthUrl / exchangeCode](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin-auth.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin-auth.provider.ts`；OAuth / 小程序扫码连接。

<a id="s13"></a>**S13** [RedNotePublishProvider.publish / validate](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote-publish.provider.ts`；小红书已发布链接登记。

<a id="s14"></a>**S14** [RedNoteOptionSchema](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.schema.ts`；必填 workLink。

<a id="s15"></a>**S15** [WeChatChannelsPublishProvider](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels-publish.provider.ts`；视频号已完成作品登记。

<a id="s16"></a>**S16** [BilibiliPublishProvider](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili-publish.provider.ts`；上传、提交与结果确认。

<a id="s17"></a>**S17** [TikTokPublishProvider.publishVideo / finalize](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok-publish.provider.ts`；远端 publish_id、上传与状态查询。

<a id="s18"></a>**S18** [YoutubePublishProvider.publish](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-publish.provider.ts`；视频上传与封面处理。

<a id="s19"></a>**S19** [WeChatOfficialPublishProvider.publish](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official-publish.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official-publish.provider.ts`；公众号草稿与发布提交。

<a id="s20"></a>**S20** [WeChatService.getOfficialAccessToken / addDraft / freePublish](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat.service.ts`；服务配置令牌与发布身份边界。

<a id="s21"></a>**S21** [AnalyticsService.fetchAccountAnalytics / fetchWorkAnalytics](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/analytics/analytics.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/analytics/analytics.service.ts`；不支持、Relay、数据归档。

<a id="s22"></a>**S22** [ChannelAccountAnalyticsVo / ChannelWorkAnalyticsVo](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/analytics/analytics.vo.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/analytics/analytics.vo.ts`；对外数据结构。

<a id="s23"></a>**S23** [TikTokAnalyticsProvider.fetchWorkAnalytics](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok-analytics.provider.ts`；缺失视频仍可形成零值快照。

<a id="s24"></a>**S24** [BilibiliAnalyticsProvider](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili-analytics.provider.ts`；播放、互动与快照时间。

<a id="s25"></a>**S25** [YoutubeAnalyticsProvider](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-analytics.provider.ts`；频道与视频基础统计。

<a id="s26"></a>**S26** [YoutubeEngagementProvider.listComments / createComment](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-engagement.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-engagement.provider.ts`；评论分页与回复。

<a id="s27"></a>**S27** [AccountsController.list / authStatus](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/accounts/accounts.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/accounts/accounts.controller.ts`；账号列表与健康状态 REST。

<a id="s28"></a>**S28** [RelayExceptionFilter.handleRelay / replaceLocalUrls](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-exception.filter.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-exception.filter.ts`；转发、账号 ID 替换、素材转存。

<a id="s29"></a>**S29** [RelayCallbackController](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-callback.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-callback.controller.ts`；账号回调。

<a id="s30"></a>**S30** [RelayClientService](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-client.service.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/relay/relay-client.service.ts`；服务端 Relay 请求。

<a id="s31"></a>**S31** [ContentMcpController](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts`；10 个内容库工具。

<a id="s32"></a>**S32** [DraftGenerationMcpController](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/draft-generation.mcp.controller.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/draft-generation.mcp.controller.ts`；3 个 AI 生成工具。

<a id="s33"></a>**S33** [PublishContentInputSchema / PublishContentOverrideSchema](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/schemas/publish-content.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/publish/schemas/publish-content.schema.ts`；公共内容与覆盖项。

<a id="s34"></a>**S34** [createPlatformPublishOptionItemSchema](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/publish.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/publish.schema.ts`；平台判别联合与 option。

<a id="s35"></a>**S35** [WeChatOfficialAuthProvider](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official-auth.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official-auth.provider.ts`；OAuth 用户身份不能等同任意公众号管理授权。

- **S37** [OpenClaw runtime register](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/index.ts) — 同OpenClaw repo/commit；`packages/runtime/index.ts` 的工具注册入口；getAiToEarnEnvironment与本地上传辅助，不代表当前远端Discovery。

### 平台模块、参数与指标源码索引

各条均是同一repo/commit；module的register实际装配，constants为应用metadata，schema为发布option，analytics provider的fetch方法为数据来源。
- [bilibili-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili-analytics.provider.ts`
- [bilibili.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili.constants.ts`
- [bilibili.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili.module.ts`
- [bilibili.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/bilibili/bilibili.schema.ts`
- [douyin.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin.constants.ts`
- [douyin.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin.module.ts`
- [douyin.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/douyin/douyin.schema.ts`
- [facebook-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook-analytics.provider.ts`
- [facebook.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook.constants.ts`
- [facebook.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook.module.ts`
- [facebook.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/facebook/facebook.schema.ts`
- [google-business.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/google-business/google-business.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/google-business/google-business.constants.ts`
- [google-business.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/google-business/google-business.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/google-business/google-business.module.ts`
- [instagram-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram-analytics.provider.ts`
- [instagram.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram.constants.ts`
- [instagram.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram.module.ts`
- [instagram.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/instagram/instagram.schema.ts`
- [kwai-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai-analytics.provider.ts`
- [kwai.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai.constants.ts`
- [kwai.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai.module.ts`
- [kwai.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/kwai/kwai.schema.ts`
- [linkedin.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/linkedin/linkedin.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/linkedin/linkedin.constants.ts`
- [linkedin.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/linkedin/linkedin.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/linkedin/linkedin.module.ts`
- [linkedin.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/linkedin/linkedin.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/linkedin/linkedin.schema.ts`
- [pinterest-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest-analytics.provider.ts`
- [pinterest.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest.constants.ts`
- [pinterest.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest.module.ts`
- [pinterest.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/pinterest/pinterest.schema.ts`
- [rednote.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.constants.ts`
- [rednote.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.module.ts`
- [rednote.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/rednote/rednote.schema.ts`
- [threads-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads-analytics.provider.ts`
- [threads.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads.constants.ts`
- [threads.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads.module.ts`
- [threads.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/threads/threads.schema.ts`
- [tiktok-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok-analytics.provider.ts`
- [tiktok.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok.constants.ts`
- [tiktok.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok.module.ts`
- [tiktok.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/tiktok/tiktok.schema.ts`
- [twitter-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter-analytics.provider.ts`
- [twitter.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter.constants.ts`
- [twitter.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter.module.ts`
- [twitter.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/twitter/twitter.schema.ts`
- [wechat-channels.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels.constants.ts`
- [wechat-channels.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels.module.ts`
- [wechat-channels.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-channels/wechat-channels.schema.ts`
- [wechat-official.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official.constants.ts`
- [wechat-official.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official.module.ts`
- [wechat-official.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat-official/wechat-official.schema.ts`
- [wechat.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/wechat/wechat.module.ts`
- [youtube-analytics.provider.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-analytics.provider.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube-analytics.provider.ts`
- [youtube.constants.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube.constants.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube.constants.ts`
- [youtube.module.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube.module.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube.module.ts`
- [youtube.schema.ts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube.schema.ts) — `project/aitoearn-backend/apps/aitoearn-server/src/core/channels/platforms/youtube/youtube.schema.ts`
- [PublishStatus](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/libs/mongodb/src/enums/publish.enum.ts) — `project/aitoearn-backend/libs/mongodb/src/enums/publish.enum.ts`；状态枚举/持久化唯一键。
- [PublishRecord](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/libs/mongodb/src/schemas/publish-record.schema.ts) — `project/aitoearn-backend/libs/mongodb/src/schemas/publish-record.schema.ts`；状态枚举/持久化唯一键。


- **S36** [uploadAssetFromPath](https://github.com/yikart/aitoearn-openclaw-plugin/blob/c5c5e722b150167249aafa448ebaee80cb4d3840/packages/runtime/src/asset-upload.ts) — repo `yikart/aitoearn-openclaw-plugin`；commit `c5c5e722b150167249aafa448ebaee80cb4d3840`；path `packages/runtime/src/asset-upload.ts`；本地文件上传封装，不是远端工具。

## 附录B. 全部公开源码 MCP Tool 清单

L2 SOURCE REGISTRATION ONLY；不是远端tools/list。输入完整细节按链接Schema；生成工具不在执行Provider最小范围。副作用工具本轮均未调用。

| # | Tool | 参数Schema / 核心输入 | 分类 |
|---:|---|---|---|
| 1 | [createVideoDraft](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/draft-generation.mcp.controller.ts) | `CreateDraftGenerationV2DtoSchema` | Generation |
| 2 | [createImageTextDraft](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/draft-generation.mcp.controller.ts) | `CreateImageTextDraftDtoSchema` | Generation |
| 3 | [getDraftTaskStatus](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/unified-mcp/draft-generation.mcp.controller.ts) | `z.object({ taskId: z.string().describe('Draft generation task ID') })` | Generation |
| 4 | [getMediaGroupInfoByName](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `GetGroupInfoByNameSchema` | Content |
| 5 | [createMedia](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `CreateMediaSchema` | Content |
| 6 | [getDraftGroupInfoByName](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `GetGroupInfoByNameSchema` | Content |
| 7 | [createDraft](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `CreateMaterialSchema` | Content |
| 8 | [listDrafts](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `ListDraftsSchema` | Content |
| 9 | [getDraftDetail](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `GetDraftDetailSchema` | Content |
| 10 | [deleteDraft](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `DeleteDraftSchema` | Content |
| 11 | [listMedia](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `ListMediaSchema` | Content |
| 12 | [listDraftGroups](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `ListGroupsSchema` | Content |
| 13 | [listMediaGroups](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/content/content.mcp.controller.ts) | `ListGroupsSchema` | Content |
| 14 | [createChannelPublishFlow](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `CreateChannelPublishFlowSchema` | Channels |
| 15 | [listChannelPublishRecords](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ListChannelPublishRecordsSchema` | Channels |
| 16 | [getChannelPublishRecordByRecordId](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `GetChannelPublishRecordByRecordIdSchema` | Channels |
| 17 | [getChannelPublishRecordByTaskId](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `GetChannelPublishRecordByTaskIdSchema` | Channels |
| 18 | [getChannelPublishRecordByFlowId](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `GetChannelPublishRecordByFlowIdSchema` | Channels |
| 19 | [publishChannelTaskNow](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ChannelPublishTaskSchema` | Channels |
| 20 | [cancelChannelPublishTask](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ChannelPublishTaskSchema` | Channels |
| 21 | [updateChannelPublishAt](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `UpdateChannelPublishAtSchema` | Channels |
| 22 | [requestChannelPublishUpdate](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `RequestChannelPublishUpdateSchema` | Channels |
| 23 | [listChannelPlatforms](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `undefined` | Channels |
| 24 | [getChannelPlatform](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ChannelPlatformSchema` | Channels |
| 25 | [listBilibiliChannelPlatformCategories](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ListBilibiliChannelPlatformCategoriesSchema` | Channels |
| 26 | [listYoutubeChannelPlatformCategories](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ListYoutubeChannelPlatformCategoriesSchema` | Channels |
| 27 | [getChannelWorkLinkInfo](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `GetChannelWorkLinkInfoSchema` | Channels |
| 28 | [listChannelWorks](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ListChannelWorksSchema` | Channels |
| 29 | [getChannelWorkDetail](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ChannelWorkSchema` | Channels |
| 30 | [verifyChannelWorkOwnership](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `VerifyChannelWorkOwnershipSchema` | Channels |
| 31 | [getChannelAccountAnalytics](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `GetChannelAccountAnalyticsSchema` | Channels |
| 32 | [getChannelWorkAnalytics](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ChannelWorkSchema` | Channels |
| 33 | [listChannelEngagementComments](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `ListChannelEngagementCommentsSchema` | Channels |
| 34 | [submitChannelEngagementComment](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `SubmitChannelEngagementCommentSchema` | Channels |
| 35 | [callChannelEngagementFunction](https://github.com/yikart/AiToEarn/blob/9413d73918271bd716b9ea59f61c9f59e485619b/project/aitoearn-backend/apps/aitoearn-server/src/core/channels/mcp/channels.mcp.controller.ts) | `CallChannelEngagementFunctionSchema` | Channels |

Channels输入细化：[S09]：记录查询recordId/taskId/flowId；作品查询platform、platformWorkId与可选accountId；listWorks账号必填并支持分页；Analytics账号可带since/until；评论列表带分页、提交带content/可选parentCommentId；function带name/data。schema允许accountId可选不保证服务实现无需账号，需按具体功能验证。

Content输入：[S31]：Group查询title，列表pageNo/pageSize；createMedia为groupId/type/url及可选描述；createDraft为groupId/title/mediaList/type等；get/deleteDraft用draftId。它们会创建或删除AiToEarn自己的内容对象，不是完成发布所必需。

Generation输入：[S32]：视频/图文生成Dto；getDraftTaskStatus用taskId。Final Asset已由Curis完成时无需再次生成；不用其生成状态代替平台发布状态。

## 附录C. Research Journal / 未执行边界

- 复用独立研究clone，读取平台注册、发布输入、平台Provider、记录/重试、Analytics、MCP、Relay与官方文档；公开GitHub HEAD对照归档。
- 通过已有合法会话只读检查频道、空发布编辑器、统计页及互动入口；不绑定、不填入内容、不上传、不发布、不搜索付费数据、不重连账号。
- 编制全部35个公开源码工具及Schema索引；remote authenticated discovery未进行。
- 读取指定Curis Boundary、抖音研究和已完成全日审查；未晋升或覆盖这些文档。
- 未本地构建运行AiToEarn；未模拟真实平台失败；源码分支、报告者Issue和L1观察分别标注。
- 输出文件和本地证据目录仅为REVIEW/EVIDENCE；未更新Product Pointer/CURRENT_STATE/Change Log，因为没有Current Truth变更。
- 未解决下一步：CEO决定是否批准26节的有限真实执行验证。全日Zcode审查另见A3，本报告不替代它，也不宣称最初全部竞品研究完成。
