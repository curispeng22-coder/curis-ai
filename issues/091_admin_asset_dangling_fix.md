# Admin 官方资产悬空引用与空壳数据修复

状态：OPEN
类型：[Admin][Fix]
发起团队：Admin（产品规划席 齐活林）
归属模块：官方资产事实源（Company Package / Capability Package / Employee Template）
是否阻塞：否
是否触发 L2：部分（能力包连接器引用触 V2 冻结，见下）

## 结论
修复资产复盘（docs/review/2026-07-17_admin-asset-real-status-review.md）发现的悬空引用与空壳数据，使官方资产达到「已真实可用」标准（有内容 + 稳定 ID/版本 + 引用真实 + 只读接口 + 可实例化/绑定 + 自动测试证据）。

## 真实证据（来自复盘三席位核查）
- 公司包 `ccp_ai_software_company.workflow_refs_json` 引用 6 个 `wl_ai_rd_*`，真实 ID 为 `wt_*`/`official.workflow.*` → 全部悬空，实例化时工作流恒为 0 实例。
- 公司包 `sub_package_refs_json` 含 `tp_code_executor` / `sp_backend_coding`，全库无归属 → 悬空。
- 能力包 `cp_content_ops.connector_ids = ["xiaohongshu","douyin","shopify"]` → 全悬空（触 V2 冻结"外部生态"）。
- `employee_templates` 中 `official.employee.*` 10 条 `status=draft` 且绑定全空 → 占位壳。

## 修改内容（计划）
1. 修正公司包 `workflow_refs`：`wl_ai_rd_*` → 对应 `wt_*`/`official.workflow.*` 真实 ID（数据修正 + 种子更新）。
2. 清理 `sub_package_refs`：移除无归属的 `tp_code_executor` / `sp_backend_coding`；`cp_content_ops` 的外部连接器引用改为 design-only 占位或移除（若保留需标 L2 升级）。
3. `official.employee.*` 10 条：补全绑定或明确标记为 design-only reservation（与 `et_*` 对齐语义）。

## 验收方式
- QA 跑实例化：`CompanyInstantiationService.instantiate` 后 `workflow_instances > 0`。
- 悬空引用计数 = 0（SQL 校验所有 JSON ref 目标存在）。

## 禁止越界
不改 Workspace Runtime / 前端；不启用外部平台/OAuth；不碰 `cmcf_*`；连接器悬空项不补真实外部连接器。

## 任务分解（待架构师细化）
- T1 数据修正脚本（wl→wt、清理 sub_package）
- T2 能力包连接器引用处置（冻结占位）
- T3 official.employee.* 绑定补全或标记
- T4 QA 实例化验证
