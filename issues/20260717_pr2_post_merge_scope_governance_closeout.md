# PR #2 合入后范围治理文档收口

- 日期：2026-07-17
- 状态：CLOSED — DOC_ONLY PASS
- 类型：产品治理 / 合入证据收口
- Owner：产品规划席
- 执行约束：只改 Issue、Review 与当前状态文档；不改代码、不恢复 stash、不运行 R3 E2E
- 前置决策：总负责人 `APPROVE_KEEP_MERGE_AND_CLOSE_AUDIT`

## 结论

保留 PR #2 合入结果 `72186d5843106554c759f647b7998f1adf31406a`，不回滚、不恢复 stash。

PR 实际包含 12 commits / 45 files，范围横跨 Admin Catalog、Workspace 身份 L2、R1、R2、R3 Model Gate 与受控出口，明显超出原 PR 的 R1/R2 标题。现有实现大多可追溯到已批准 Issue 与 Review，因此不以标题失真为由回滚；缺失部分只做文档治理收口。

R3 真实模型 E2E 继续冻结，质量状态保持 `BLOCKED_L2`。新 Run `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6` 仍为 `pending`，不得写成已完成。

## 待收口的五类证据缺口

1. `issues/093_admin_readonly_catalog_routes.md` 仍为 OPEN，缺独立 Review；只允许引用现有 R2 Catalog HTTP 与聚焦测试证据收口。
2. `issues/095_admin_l2_gate_tracking.md` item 5 缺独立 Review；只允许引用现有 Admin token、R1 与安全证据收口，其他四项 L2 不得误关。
3. `019217d6`、`d9157c9e` 的部分 Admin C/D 内容仅被后续 R2 Issue/Review 追溯覆盖；需明确写成“后补追溯”，不得伪造提交前独立审批。
4. `issues/shared/20260717_admin_workspace_stash_handoff.md` 无独立 Review；stash 继续保留，禁止 apply/pop，以当前“不恢复”决策更新边界，不宣称内容已恢复。
5. R1 Issue 与 `knowledge/NOW.md` 被夹入 L2 提交 `0671a35b`；只记录打包边界不纯，不重写历史、不拆提交。

## 验收标准

- 五类缺口均有明确事实、引用证据和最终状态，不新增测试或实现。
- 不改变已通过的 Identity L2、R1、R2 验收结论。
- 不把 R3 架构/安全 PASS 写成真实 E2E PASS。
- 不读取、保存或回显模型凭据。
- 不恢复 stash，不创建补偿性代码提交。
- 完成后由产品规划席回传总负责人，并通知项目调度席更新状态链。

## 当前 Gate

- PR #2 post-merge scope audit：CLOSED — KEEP MERGE。
- Identity L2：PASS。
- R1：PASS。
- R2：PASS。
- R3 Model Gate：`BLOCKED_L2`，E2E 冻结。

## 产品验收

- Review：`reviews/20260717_pr2_post_merge_scope_governance_review.md`。
- 093 已以既有测试与 R2 运行证据完成 post-merge 追溯并关闭。
- 095 仅 item 5 关闭；其余四项保持 `BLOCKED_L2`。
- Admin C/D 早期提交明确标记为“后续 R2 追溯覆盖”，未伪造提交前审批。
- stash 交接按总负责人决策关闭为 `RETAINED / DO_NOT_APPLY_OR_POP`。
- R1 Issue / `knowledge/NOW.md` 夹入 L2 提交的边界不纯已记录，不重写历史。
- 未修改代码、未运行测试、未启动服务、未读取凭据。

结论：本治理 Issue 文档收口完成；R3 Gate 状态不变。
