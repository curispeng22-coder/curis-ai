# Admin L2 Gate 待升级事项跟踪

状态：BLOCKED_L2
类型：[Admin][Gate]
发起团队：Admin（安全边界席 + 产品规划席）
归属模块：安全边界席 / 总控决策席

## 结论
以下事项触发 L2 Gate，Admin 不自主推进，须升级总控决策席 + 安全边界席，等决策后解锁。

## 清单（均来自资产复盘 + 协作规则红线）
1. 外部连接器生态：能力包 `cp_content_ops.connector_ids = xiaohongshu/douyin/shopify` 全部悬空且触 V2 冻结"外部 Agent 生态导入" → L2 #3/#4/#5/#6。
2. 真实计费 / 配额商业化：接 `quota_rules`/`pricing_rules`/`plans` 启用真实计费（含 `cmcf_*`）→ L2 #1/#2。
3. content 公司产品线：`ccp_ai_content_company` 入库、商业域 Dashboard 渲染 → L2 #1/#2/#3（自用例外须总控明确）。
4. 真实多租户隔离实现：ADR-0017 D1–D4 当前 design-only，真实隔离超出现有 gate → L2 #5/#6。
5. 平台管理员缺省令牌硬编码：`backend/app/main.py:1676-1678` 默认 `"platform-admin-dev"`，生产未注入即等同默认口令 → **安全红线**。**状态：VERIFIED/CLOSED（仅 item 5）**——提交 `d7c0b21` 已随 PR #2 合入 `72186d58`；未配置令牌时 Admin 请求返回 401，`ADMIN_STRICT=true` 且缺令牌时拒绝启动。该项移出 L2 待决策，不影响其余四项继续阻塞。

## 动作
- 由安全边界席起草飞书升级通知（群「Curis 开发通知」`oc_1b559ad633e40345229275d15f7e8d42`）；
- 每项解锁后转对应内部 Issue 跟进；
- 未解锁前 Admin 不实现、不补数据、不渲染。

## 注意
- 第 5 项（弱令牌）经基线 R1.8 授权已由 PR #2（commit `d7c0b21`）实现并完成双 lead 合入，转 `VERIFIED/CLOSED`，移出 L2 待决策；本文件头状态仍 BLOCKED_L2，因其余 4 项（外部连接器 / 真实计费 / content 公司 / 多租户）仍待总控。
- 其余 4 项未解锁前 Admin 不实现、不补数据、不渲染。

## 升级记录
- 2026-07-17 04:47 已飞书升级（群「Curis 开发通知」`oc_1b559ad633e40345229275d15f7e8d42`，bot 身份，message_id `om_x100b6aa0796b74a0b340013b1377298`），待总控 + 安全边界席决策。决策前 Admin 不实现、不渲染。
- 2026-07-17（收尾）第 5 项（弱令牌）依基线 R1.8「未配置拒绝」授权，已由 R1/R2 波次实现（PR #2，commit `d7c0b21`），状态改为「已实现（待 Shared 双确认合入）」；其余 4 项仍 BLOCKED_L2 待总控。
- 2026-07-17（post-merge）PR #2 已合入 `72186d58`。`reviews/20260717_workspace_r1_unified_runtime_baseline_review.md` 记录无/错令牌 401、严格模式缺令牌拒绝启动；`reviews/20260717_pr2_post_merge_scope_governance_review.md` 完成追溯收口。仅 item 5 关闭，文件整体仍 `BLOCKED_L2`。
