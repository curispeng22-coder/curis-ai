# PR #2 合入后范围治理 Review

- 日期：2026-07-17
- 审计状态：CLOSED — KEEP MERGE
- 产品状态：部分可用
- 固定修订：`72186d5843106554c759f647b7998f1adf31406a`
- 约束：只做证据追溯，不改代码、不跑测试、不恢复 stash、不执行 R3 E2E

## 结论

PR #2 实际包含 12 commits / 45 unique files，横跨 Admin Catalog、Workspace 身份 L2、R1、R2、R3 Model Gate 与受控出口，范围显著超出原 R1/R2 标题。

总负责人已批准 `APPROVE_KEEP_MERGE_AND_CLOSE_AUDIT`：保留当前修订，不回滚。安全边界席确认 R3 新增边界 PASS，但该 PASS 只表示安全契约成立，不表示真实模型 E2E 已验收。

## 提交追溯

| 范围 | 提交 | 追溯结果 |
| --- | --- | --- |
| Admin Catalog / token / 能力态 / 测试 | `f6e020e8`、`d7c0b21b`、`019217d6`、`d9157c9e` | 093、095 item 5 与后续 R2 证据覆盖；其中 C/D 为后补追溯，不伪造提交前独立审批 |
| stash 交接文档 | `ab4419bf` | 总负责人决定保留 stash 且永不 apply/pop，交接待办关闭 |
| Workspace 身份 L2 | `0671a35b` | IdentityMembership、TenantContext、scope、可信 Gateway 已有安全与质量 PASS |
| R1 | `306b9a11` | 统一运行基线 Review PASS |
| R2 | `b85f30fb`、`43521be5`、`758da525` | 资产实例化、兼容修复、Workspace 独立库 seed Review PASS |
| R3 Model Gate / egress | `8f426be9`、`72186d58` | 架构与安全契约 PASS；真实质量 Gate 仍 `BLOCKED_L2` |

## 五类治理缺口处置

1. 093：以现有测试文件、Shared focused 结果及 R2 Catalog 运行证据完成 post-merge 追溯，状态转 `VERIFIED/CLOSED`。
2. 095：仅 item 5 以 R1 无/错令牌 401、严格模式缺令牌拒绝启动证据关闭；其余四项继续 `BLOCKED_L2`。
3. `019217d6`、`d9157c9e`：明确为后续 R2 追溯覆盖，不补写虚假前置审批。
4. stash：`348b68800cfdfa23129ff2a0c139aee2ae669338` 保留作历史核对，禁止恢复；交接 Issue 按取消恢复待办关闭。
5. R1 Issue 与 `knowledge/NOW.md` 夹入 `0671a35b`：记录提交边界不纯，不拆分、不重写历史。

## 复用证据

- `reviews/20260717_workspace_r1_unified_runtime_baseline_review.md`：Admin 无/错令牌 401、严格模式缺令牌拒绝启动、R1 PASS。
- `reviews/20260717_workspace_r2_asset_instantiation_closure_review.md`：聚焦 66 passed、全量 603 passed / 19 failed、Catalog 200、无令牌 401、跨租户 403、R2 PASS。
- `reviews/20260717_workspace_shared_main_manual_merge_preparation_review.md`：Admin token 与 Workspace 身份边界可共存，禁止恢复默认弱口令，Shared 合并准备 PASS。
- `backend/tests/test_issue093_readonly_catalog_routes.py`：四条只读 GET 的 200、真实种子行及无/错令牌 401 覆盖。
- 安全边界席 post-merge 回传：`8f426be9` 与 `72186d58` 未发现 Provider、Model、Gateway、scope、限额、重试、Fallback、日志或受控出口绕过。

本 Review 不新增测试结果，只复用已存在证据。

## 当前状态

- PR #2：保留，审计关闭。
- Identity L2：已真实可用。
- R1：已真实可用。
- R2：已真实可用。
- R3：部分可用；实现与安全边界已存在，但真实模型 E2E 未通过，保持 `BLOCKED_L2` 并继续冻结。

