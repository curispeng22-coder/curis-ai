# CURIS Content Growth 平台 / 账号「诚实本地链」产品合同

> Status: **Frozen**
> Authority Class: **CURRENT / PRODUCT CONTRACT（V1 平台链·CG 专业业务任务适用）**
> Owner: Curis V1 Delivery Owner
> Confirmed: **2026-10-07 CEO「合同确认 + D1–D5 按建议」**（来源对话裁定；草案与裁定 provenance 见 [任务区草案](../../artifacts/tasks/CURIS-V1-PLATFORM-LOCAL-CHAIN-CONTRACT-20261007/CURIS_PLATFORM_ACCOUNT_LOCAL_CHAIN_CONTRACT_DRAFT.md)）
> 输入来源: [CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md](CURIS_CONTENT_GROWTH_BUSINESS_LOGIC_V2.md)（CEO ACCEPT WITH 4 CORRECTIONS）· [CURIS_V1_EXECUTION_BACKLOG.md](../reviews/CURIS_V1_EXECUTION_BACKLOG.md) V1-P3-001~005 · CURIS-V1-APP-COMPLETION-INVENTORY-20261006 §3/§6 · CONTENT_GROWTH_FINAL_PRE_IA_RED_TEAM_VERIFICATION.md · CONTENT_GROWTH_INDEPENDENT_RED_TEAM_SECOND_PASS.md · 同构范式: Music 人工事实链（BOUNDED ACCEPTED）/ Writing 经营面「合同先行」Owner 决策

---

## 0. 目的与范围

本合同把 Content Growth Logic V2 的 **Business → Platform → Account** 层级中「账号持续经营（V2 §1.4）」翻译为 V1 可实现的产品合同，约束条件是 **零外部凭证**：所有外部平台能力（OAuth / API 发布 / 数据采集）在 V1-P3-005（EXTERNAL-BLOCKED）解除前不存在。

**v1 管辖**：Platform 目录、ChannelAccount 本地模型、账号注册与经营信息、不发出的发布核验清单与本地导出、人工回执回填、人工表现观察、账号异常本地记录。
**v1 不管辖**（明确排除，见 §5）：任何连接器、真实发布、真实数据、验证平台事实。

## 1. 真值规则（红线，先于一切功能）

1. **连接真值**：所有平台 / 账号的 `connection_status` 在 v1 恒为 `NOT_CONNECTED`。产品任何界面不得出现「已连接」「已自动发布」「实时数据」断言；每处外部事实位固定显示「未连接」。
2. **人工回填三强制**（服务端强制，客户端不可覆盖，同 Music/Writing 范式）：
   - `verification = UNVERIFIED`
   - `source = CEO_MANUAL`
   - 时点不可变记录：每次保存新实体（revision=1、identity_ref=自身、无编辑链），同 request_id 同指纹重放幂等、异指纹 409。
3. **人工回填永不升级为平台事实**（Execution Backlog V1-P3-004）：手工填写的发布 URL / 数据仅作为「人工回填 · 未验证」证据展示，产品逻辑不得将其用于任何「已验证成功」推导。
4. **零外发**：v1 全链无任何对外网络请求；QA 必须含 forbidden 网关零外发证据。
5. **不造数据**：无数据即诚实空态；不预填任何平台能力为可用（红队结论：五平台无 audited VERIFIED capability）。

## 2. 对象模型

### 2.1 Platform（平台目录）

- **固定目录**（系统级常量，不开放用户新建；D1 已裁定 6 平台全量）：`xhs（小红书）/ douyin（抖音）/ wechat_oa（公众号）/ tiktok / youtube / bilibili`。
- 仅三主平台（小红书/抖音/公众号）提供生产链检查模板（V2 §3.2 现实链）；其余三平台仅给通用合规检查项。
- Platform 不是可登录对象；它只承载：生产链检查模板（§4.2）、规则提示文本、账号归属。

### 2.2 ChannelAccount（渠道账号 = 长期经营单元）

对齐 V2 §1.4 / §3.3，字段（全部本地人工维护）：

| 字段 | 说明 |
|---|---|
| platform_ref | 归属平台（目录枚举） |
| name | 账号名（用户填写） |
| positioning / audience | 定位 / 受众画像（V2 §4.3） |
| content_mix / cadence / voice | 内容结构配比 + 发布节奏 + 语感（账号策略） |
| growth_stage | `cold_start / growing / mature / declining_transforming`（V2 §4.4） |
| responsibility | 经营责任归属：可 Leader 直担 / 一员工多项 / 多员工分摊；**不强制单负责人**（V2 §1.4 修正④） |
| status | `active / dormant / banned`（V2 §4.5 异常本地记录；出入组合/封禁属 CEO 关切事项，产品只记录不外发） |
| connection_status | 恒 `NOT_CONNECTED`（常量，不可编辑） |

- **归属 scope（D2 已裁定）**：**business 级**（Company 内 CG 业务可见、跨工作区复用），依据 V2「账号是业务中的长期经营单元」。
- 同平台矩阵号定位必须可区隔（V2 §4.3），表单提示不做硬校验。

## 3. 与现有链的关系（不重设计既有对象）

- **内容生产不变**：contents / materials / 既有 learnings 链零改动。
- **发布候选 gate 不变**：`INTERNAL_CANDIDATE_NO_PUBLICATION` 语义保留——「发布核验清单 + 导出」不是发布，不改变该 gate。
- **回执 / 表现观察**为新增时点记录，不写入既有 content 状态机。
- **账号级 Learning（D3 已裁定）**：v1 **复用既有 CG learnings 端点不加 scope**（账号经验以自由文本记录，账号引用写正文）；v1.1 再评估账号 scope_ref 扩展。

## 4. 本地动作链（无凭证，全部本地）

### 4.1 账号注册 / 编辑
创建与维护 §2.2 全部字段；含账号异常状态变更（限流/违规/封禁仅作状态+备注记录）。

### 4.2 发布核验清单（per-account，不发出）
- 输入：一篇既有 content（用户显式选择）+ 目标账号。
- 生成：按平台生产链检查模板（小红书=封面/标题关键词/标签话题/图文格式；抖音=封面标题/时长字幕；公众号=排版/标题摘要封面；其余平台通用合规项）逐项人工勾核。
- 产出：核验记录（时点不可变）+ **本地导出（D4 已裁定）**：**新最小导出**（标题/正文/平台/账号/检查结果），不复用 legacy `content_publish_package.py`（其绑定 legacy AiToEarn/social-auto-upload 语境，避免误读为发布能力）。
- 明确：**无「发送」按钮、无排队、无定时**。

### 4.3 人工回执回填
对某账号某次核验记录，人工回填：`published_at / platform_post_url / note`（全部可选）。三强制真值（§1.2）；URL 展示固定标注「人工回填 · 未验证」。

### 4.4 人工表现观察
仿 Music Observation：`title / body / scope_ref（须命中本业务 ChannelAccount，否则 404） / period`；时点不可变、强制 UNVERIFIED、外部数据位恒「未连接」。分析/比较仅基于人工观察，样本不足不下结论（V2 §1.5 纪律在 UI 提示，不强制）。

## 5. 明确排除（v1 红线清单）

1. 任何 OAuth / cookie / 连接器 / 爬虫代码（legacy `connectors/` 与 `content_workflow_runtime.py` 维持 CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007 冻结，不接新包）。
2. 定时发布、发布队列、自动重试。
3. analytics 采集、平台 API 客户端、webhook。
4. 任何 VERIFIED 平台事实、自动「已发布」状态。
5. 账号数据删除同步到平台（产品无平台侧操作能力）。
6. 本合同不修改 Product Freeze / 既有 Frozen Authority；不触碰 RD/XHS/TTK legacy 链。

## 6. 实现分片（每切片独立 Issue → 实施 → 独立真实 QA → 接受登记）

| 切片 | 内容 | 规模 | 前置 |
|---|---|---|---|
| S1 | Platform 目录 + ChannelAccount 本地 CRUD + 诚实未连接投影（CG 工作台新视图） | M | **Architecture Review**（新增 primitive：ChannelAccount 存储） |
| S2 | 发布核验清单 + 本地导出 | M | S1 |
| S3 | 人工回执 + 人工表现观察 | M | S1；范式=Music Observation |
| S4（v1.1，D5 已裁定挂起） | 平台角色记录（V2 §1.1 组合策略）+ 账号 Learning scope 扩展 | S | 不阻塞 S1–S3 |

- UI 落点：CG PACKAGE 安装工作台新视图（账号 / 账号详情 / 发布核验），仅 `--ui-*` token；Execution Backlog V1-P3-001「UI-HOLD」的解除以本合同确认为前置（已满足）。
- QA 必含：三强制真值、伪造 verification 422、越权 scope 404、零 5xx、forbidden 网关零外发、PREHASH=POSTHASH、诚实空态。

## 7. Owner 决策记录（2026-10-07，D1–D5 全部按建议采纳）

| # | 决策 | 裁定 |
|---|---|---|
| D1 | 平台目录范围 | 6 平台全量；仅三主平台带生产链检查模板 |
| D2 | ChannelAccount 归属 scope | business 级 |
| D3 | 账号级 Learning | v1 复用既有 learnings 不加 scope |
| D4 | 核验导出格式 | 新最小导出，不复用 legacy ContentPublishPackage |
| D5 | S4（平台角色记录+Learning scope） | 挂 v1.1，不阻塞 S1–S3 |

## 8. Provenance 与变更纪律

- 本合同由任务区草案经 CEO 2026-10-07「合同确认 + D1–D5 按建议」晋升；草案原文保留于任务区作 provenance。
- 修改本 Frozen 合同需 Owner 明确决定 + 同步本节 provenance + CHANGE_LOG 登记。
- 实现 sliced by §6；任何需要新 schema 的切片先过 Architecture Review。
