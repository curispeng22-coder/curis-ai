# Curis Writing Domain Authority（Draft — 五经营面合同）

Status: **Draft**
Authority Class: DRAFT DOMAIN PRODUCT CONTRACT（非 Frozen Authority；产品实现验收前不升级）
Disposition: OWNER CONFIRMED DRAFT / READY TO EXECUTE P1-a（Owner 2026-10-06 确认决策 D1–D4）
Updated: 2026-10-06
Scope: Writing 业务域五个缺失经营面（DIRECTION / LEARNING / MARKET / PERFORMANCE / OP）的本地人工事实链语义
依据：Owner 2026-10-06 完工盘点决策 1（artifacts/tasks/CURIS-V1-APP-COMPLETION-INVENTORY-20261006/V1_APP_COMPLETION_INVENTORY.md §6）
来源草案：artifacts/tasks/CURIS-V1-WRITING-OPERATING-SURFACES-CONTRACT-DRAFT-20261006/WRITING_OPERATING_SURFACES_CONTRACT_DRAFT.md（PROMOTE 2026-10-06）

---

## 0. 本文件的性质与边界

- 本文件只为 **Writing 五个缺失经营面** 补书面产品合同，消除「仅原型注册表条目、语义 UNCLEAR」的 Authority 缺口。
- 五面：**WR-DIRECTION（创作方向）、WR-LEARNING（经验学习）、WR-MARKET（市场）、WR-PERFORMANCE（表现）、WR-OP（经营投影）**。
- 已接受资产不在本文件重定义：作品库/章节/作者人工确认正式稿/本地发布包下载（approvedScope = LOCAL_BOOK_CHAPTER / AUTHOR_MANUAL_FORMAL / LOCAL_DOWNLOAD）；WR-NEWBOOK-01 内联创建与 WR-SERIAL-01 本地发布包为既有 ADAPT* 面，其封存/解封另行登记。
- **不在本合同**：平台连载、读者数据、收益、任何平台凭证链（P3，凭证到位后逐链独立立项）；新 schema 表/列（存储复用 runtime_entities PACKAGE_DOMAIN_OBJECT 范式，发现必须加表即 STOP 上报）；UI 新风格（沿用已接受视觉基线与 `--ui-*` token）。
- 全程诚实状态：本合同所有面均为**本地人工事实链**，无平台自动采集、无「平台验证/效果提升」表述。

## 1. 定义（Definitions）

### 1.1 WritingDirection（创作方向）

「这部作品/这个工作区往哪写」的明确记录：题材定位、读者承诺、风格基调、结构选择。

- 字段：`title`（≤2000 字非空）、`body`（≤20000 字非空）、`scope_ref`（适用范围引用，见 §3.1）、`reference_refs`（≤8，引用本工作区合法素材/章节）、`learning_ref`（可空，来源经验）、`confirmed`（明确 bool；确认时服务端写 `confirmed_by`/`confirmed_at`）。
- 方向**必须明确确认**才可被章节创作引用；未确认方向只是草稿记录。
- 方向版本化：修改产生新版本（revision+1、previous_ref、identity_ref 不变）；引用旧版本需显式 `historical: true`。

### 1.2 WritingLearning（人工经验）

作者沉淀的写作经验，**强制 `validation=UNVERIFIED`**。

- 字段（严格 exact）：`title`、`body`、`basis_refs`（≤8，本工作区内对象，保存时快照 basis hash）、`applicability`（适用范围）、`counterexample`（反例与限制）、`accepted`（明确 bool；接受时服务端写 `accepted_by`）。
- 未被明确接受的经验不可被引用应用；旧版本经验需显式 `historical: true`。
- 禁存：AI 推理过程 / Prompt / 中间草稿 / 工具调用日志。

### 1.3 WritingMarketSnapshot（人工市场快照）

人工录入的选题/平台/读者信号快照（仿 Music MarketSnapshot）。

- 字段：`title`、`body`、`period`（观察周期）、`source_note`（人工来源说明，必填——写明"人工观察/编辑沟通/公开榜单阅读"等）。
- 强制 `verification=UNVERIFIED`；**无平台自动采集**（外部凭证 P3）。

### 1.4 WritingObservation（人工表现观察）

对作品/章节表现的人工记录（仿 Music Observation）。

- 字段：`title`、`body`、`scope_ref`（作品或章节引用）、`period`。
- 强制 `verification=UNVERIFIED`；真实平台读者/阅读数据属外部链（P3），缺失时如实显示「未连接」。

### 1.5 WritingOperatingView（经营投影）

只读投影面，**不是数据源**：聚合本工作区作品、章节、方向、经验、快照、观察的当前状态，回答「方向是什么/正在写什么/积累了什么经验/下一步是什么」。

- 只读取现有对象，不产生新对象、不新建统计系统；无数据时如实显示空态。

## 2. 关系与不变量（Relationships / Invariants）

```
WritingWorkspace
 ├─ WritingBook → WritingChapter（已接受，不重定义）
 ├─ WritingDirection ──scope_ref──▶ Book 或 Workspace（D1：两级允许）
 │        └─learning_ref──▶ WritingLearning（可空）
 ├─ WritingLearning ──basis_refs(≤8+hash 快照)──▶ 本工作区对象
 │        └─应用──▶ 新章节（新 WritingChapter + 首版草稿，不替换任何现有章节 latest）
 ├─ WritingMarketSnapshot（独立人工记录）
 ├─ WritingObservation ──scope_ref──▶ Book 或 Chapter
 └─ WritingOperatingView = 以上全部的只读投影
```

不变量：

1. **UNVERIFIED 强制**：Learning/Observation/MarketSnapshot 服务端强制写入，客户端不可指定。
2. **不替换 latest**：应用经验生成**新章节**（新对象 + 首版草稿），原有章节与草稿指针不变（D2 确认）。
3. **basis 固定**：保存学习时快照 basis 内容 hash；应用时固定原 basis 与范围。
4. **幂等**：所有写动作 `request_id` + 指纹 fail-closed（重放同指纹返回原结果，异指纹 409）。
5. **scope 三层隔离**：tenant/company/workspace 校验；跨公司不可见不可引用（404）。
6. **诚实空态**：无数据如实显示，不造 Mock。

## 3. 逐面合同

### 3.1 WR-DIRECTION-01（P1-a，仿 Music Direction）

- 动作：`save-direction`（保存+明确 confirmed）、`apply-direction`（章节创作引用方向，写 runtime_links 显式引用关系）。
- 视图：方向列表/详情（标题、确认状态、适用范围、来源经验、版本历史入口）。
- **D1（Owner 确认 2026-10-06）**：scope_ref 允许两级——①单部作品（book ref）②整个写作工作区（空串）；作品级优先展示。

### 3.2 WR-LEARNING-01（P1-a，仿 CG-LEARNING-01 已接受链）

- 动作：`save-learning` / `use-learning`。
- **D2（Owner 确认 2026-10-06）**：`use-learning` 创建**新章节**——在选定作品下新建 WritingChapter（DRAFT）并写入首版草稿（含经验正文/适用范围/反例与 learning_ref），不触碰任何现有章节及其草稿；旧版本经验须 `historical:true` 显式确认。
- 视图：经验列表/查看（含「未验证」标识）、保存表单、应用入口（选定作品 → 新标题）。

### 3.3 WR-MARKET-01（P1-b，人工版）

- 动作：`save-snapshot`（人工录入）。
- 视图：快照列表/详情；如实标注「人工录入 · 未验证」。

### 3.4 WR-PERFORMANCE-01（P1-b，人工版）

- 动作：`save-observation`（人工录入，绑定作品/章节）。
- 视图：观察列表/详情；外部平台数据位如实显示「未连接」（P3 前置）。

### 3.5 WR-OP-01（P1-c，投影收尾）

- 无写动作；只读聚合投影：当前方向 → 在写章节 → 最新经验 → 最新快照/观察。
- 数据不齐时逐块显示空态；OP 不是数据源，不新建聚合表。

## 4. 诚实状态与禁止项

- 禁：「平台验证」「效果提升」「自动采集」「智能推荐市场机会」等表述；禁 Mock 数据；禁隐藏 UNVERIFIED 标识。
- 禁：新 schema 表/列（复用 runtime_entities 范式）；新 Surface/Dashboard；改动已接受章节链语义。
- 生产 router `allow_execution=False` 边界不变；五面不引入任何执行授权。

## 5. 与现有资产的关系

| 资产 | 关系 |
|---|---|
| 作品库/章节/作者确认/本地发布包 | CONSUMES（消费，不修改） |
| Music 七视图经营链 | 同构参照（Direction/Learning/Observation/MarketSnapshot/Report 模式） |
| CG-LEARNING-01 已接受链 | 同构参照（save/use-learning、basis hash、UNVERIFIED、不替换 latest） |
| WR-NEWBOOK-01 / WR-SERIAL-01（ADAPT*） | 不在本合同；封存/解封另行登记 |
| 原型注册表 WR-OP/MARKET/DIRECTION/PERFORMANCE/LEARNING 条目 | 本合同取代其 UNCLEAR 语义；原型仅作视觉参照 |

## 6. 批次与决策记录

| 批次 | 面 | 工作量 | 状态 |
|---|---|---|---|
| P1-a | DIRECTION + LEARNING | M+M | READY_TO_EXECUTE（Issue CURIS-V1-WRITING-DIRECTION-LEARNING-20261006） |
| P1-b | MARKET + PERFORMANCE（人工版） | M+M | 待 P1-a 接受后立项 |
| P1-c | OP（投影收尾） | S（诚实壳） | 待前两批接受后立项 |
| P3 | 平台连载/读者数据/收益 | L | 外部凭证到位后独立立项 |

- **D1（2026-10-06 Owner 确认）**：方向 scope_ref 两级（作品 + 工作区）。
- **D2（2026-10-06 Owner 确认）**：经验应用 = 新章节，不替换现有章节 latest。
- **D3（2026-10-06 Owner 确认）**：按 P1-a → P1-b → P1-c 顺序。
- **D4（2026-10-06 Owner 确认）**：合同草案 PROMOTE 至本文件（Draft 状态）；首个切片接受并经复核后才可申请 Frozen。

每项沿用治理：正式 Issue（Scope/Allowed Files/验收证据）→ 实施 → 独立真实浏览器 QA → 接受登记；受保护 DB 指纹、零 Git 写、诚实状态表达不变。
