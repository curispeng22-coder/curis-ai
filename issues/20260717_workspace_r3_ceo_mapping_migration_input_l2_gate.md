# Workspace R3 CEO 映射迁移输入 L2 Gate

- 日期：2026-07-17
- 状态：CLOSED — PASS
- Parent：`issues/20260717_workspace_r3_real_model_execution_gate.md`
- Owner：产品规划席
- Next Seat：产品规划席（Parent R3）
- 类型：身份事实源与一次性数据迁移审批

## 先说结论

新建唯一 Run 与一次真实调用虽已获批准，但执行前核对发现当前 `quality.sqlite` 尚无 `tenant_memberships.ceo_id` 列，`membership-quality` 与 `company-a` 也没有可直接使用的可信非空 `ceo_id`。在没有事实源或单独审批迁移输入前，R3 必须继续 `BLOCKED_L2`。

本 Issue 只确定 `company-a` 与 `membership-quality` 应使用的同一个可信、非空 `ceo_id` 迁移输入及其来源；不实施迁移，不启动服务，不创建 Run，不注入 Key，不调用模型。

## 当前证据

- 可信 CEO UsageContext 实现与无出网质量验证已通过：`issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md`。
- 固定实现修订：`718af2c463e39820ac6928681b16818a9fbccc25`。
- 执行前核对：`quality.sqlite` 缺 `tenant_memberships.ceo_id` 列；`membership-quality` 与 `company-a` 均无已确认的可信非空 CEO 映射值。
- 系统交付席未启动、未创建 Run、未注入 Key、未调用模型。
- 总负责人明确不批准猜测、默认值或临时写入；CEO 映射迁移必须单独审定。

## 架构边界席唯一任务

1. 只读核对仓库和批准测试数据中是否已有可追溯的 CEO 身份事实源，优先顺序为：已验证身份主体映射、批准 seed / fixture、已审定 Company 所有者记录、已有正式 Issue / Review 明确值。
2. 明确 `company-a` 与 `membership-quality` 是否能确定同一个非空 `ceo_id`；给出值的来源文件、字段、创建链与可信理由。
3. 如没有既有可信值，只能形成一个明确的单值迁移提案和人工确认点，不得自行生成、猜测、沿用客户端 `X-Ceo-Id`、使用 Admin token、默认 CEO 或仅根据 tenant 推导。
4. 迁移必须 additive、可重复、仅作用于批准测试 company/membership；不得覆盖其他租户、其他 membership 或历史失败 Run。
5. 明确迁移前置检查、唯一性/一致性条件、回滚和 fail-closed：列缺失可迁移；值缺失、冲突、跨租户或 Company 不一致时必须停止。

## 允许范围

- 只读查看与 `company-a`、`membership-quality`、批准 R3 测试主体直接相关的数据定义、seed、fixture、Issue 和 Review。
- 形成 Architecture Review 与唯一迁移输入提案。
- 安全边界席对事实源、范围、回滚和 fail-closed 给出 `PASS` 或 `BLOCKED_L2`。

## 禁止范围

- 不修改代码、数据库、seed、fixture 或部署文件。
- 不启动服务、不创建 Run、不注入或读取 Key、不调用模型。
- 不改 Provider、Model、Gateway、受控出口、Token/成本规则、前端或 Admin。
- 不使用客户端 Header、默认 CEO、固定字符串、随机值、临时值或未审定的推断值。
- 不删除、覆盖或修补历史失败 Run、StepResult、UsageEvent 或审计。

## Gate 输出

架构 Review 必须只给一个结果：

- `PASS`：给出唯一 `ceo_id`、完整可信来源、只作用于 `company-a + membership-quality` 的迁移边界、前置检查、回滚与验证；随后交安全边界席。
- `BLOCKED_L2`：明确没有现有可信事实源，并列出需要总负责人人工确认的唯一单值输入；不得给多套候选。

安全复核后，由产品规划席提交总负责人单独审批。未获批准前，Parent R3 不得继续。

## 架构与安全复核结论

- Architecture Review：`reviews/20260717_workspace_r3_ceo_mapping_migration_input_architecture_review.md`。
- 架构结论：`BLOCKED_L2`；仓内没有能证明 `company-a` 与 `membership-quality` 共用同一可信非空 `ceo_id` 的现有事实源。
- 安全边界席复核：`BLOCKED_L2`；测试 fixture、历史客户端 Header 来源、默认值和临时值均不得作为迁移事实。
- 唯一可解除方式：总负责人显式批准一个新建、不透明、非空的 `ceo_id`，把该批准记录本身作为测试主体唯一事实源。

## 产品规划席提交的唯一单值提案

- 提议 `ceo_id`：`ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`。
- 该值为新建不透明标识，不沿用 `ceo-a`、客户端 Header、Admin token、默认值或任何历史占位值。
- 仅绑定现有目标活动 membership：当前受信 issuer + `subject_id=membership-quality` + `tenant_id=tenant-a` + `company_id=company-a`。
- 同一值仅允许 additive/idempotent 写入目标 membership 与 active `company-a`；任何 issuer、状态、有效期、tenant、company、Company CEO 冲突或重复活动映射不一致都必须停止。
- 本提案不是实施授权。只有总负责人明确批准该精确值与精确绑定后，系统交付席才可迁移；迁移完成后先做无出网核对，再创建已获批的唯一 Run。

## 批准、迁移与收口

- 总负责人已批准唯一值：`ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`。
- 实际目标：membership `membership-quality`，受信 issuer `https://quality.issuer.local`，subject `quality-member-sub`，`tenant-a + company-a`，角色 owner，状态 active。
- `quality.sqlite` 已 additive 增加 nullable `tenant_memberships.ceo_id`，并仅对上述 membership 与 active `company-a` 写入同一批准值。
- 核对：active mapping=1、membership/company 冲突=0、幂等复核待变更=0。
- 固定修订仍为 `718af2c463e39820ac6928681b16818a9fbccc25`；未改代码、未启动服务、未注入 Key、未创建 Run、未调用模型。
- 总负责人确认映射 `PASS`；本数据前置 Gate 关闭，Parent R3 可进入此前批准的唯一 Run 创建阶段。
