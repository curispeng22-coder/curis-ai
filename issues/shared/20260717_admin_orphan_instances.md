# 请 Workspace 确认孤儿实例处置（Admin 侧修复前协调）

状态：VERIFIED/CLOSED（ACKNOWLEDGED → IN_PROGRESS → VERIFIED/CLOSED）
路径：issues/shared/20260717_admin_orphan_instances.md
发起团队：Admin
目标团队：Workspace
归属模块：employee_instances / department_instances
是否阻塞：否（阻塞 Admin 侧 Issue 092 执行）
是否触发 L2：否

## 背景
Admin 资产复盘发现孤儿实例（Issue 092）：`employee_instances`(18) 与 `department_instances`(2) 的 `template_id` 指向不存在的模板（`et_ai_rd_*` / `dt_ai_rd`），经 API 不可重新解析/校验，会误导"真实可用"判断。Admin 计划在不改 Workspace Runtime 前提下，于 Admin 侧回填正确 `template_id` 或标记 deprecated。

## 真实证据（Admin 侧）
- `employee_instances` 18 行 `template_id` 全不在 `employee_templates`（仅 6 `et_*` + 10 `official.employee.*`）。
- `department_instances` 2 行 `template_id = dt_ai_rd / dt_ai_content`，不在 `department_templates`（仅 `dt_engineering` / `official.department.software_rnd` / `official.department.content_growth`）。
- `create_employee_instance` 要求模板存在，故用这些 ID 走 API 今日直接报错 → 早期绕过校验 seed 进库。

## 需要 Workspace 确认
1. 这些实例是否已被 Workspace 运行态消费（部门激活 / 员工会话 / Workflow 运行）？
2. 若 Admin 回填 `template_id`（映射 `et_ai_rd_*` → `et_*` / `official.employee.*`，`dt_ai_rd` → `dt_engineering`）或标记 deprecated，是否会破坏你的消费层？
3. 你方倾向方案 A（回填正确 `template_id`）还是方案 B（标记 deprecated 不删除）？

## Admin 承诺（禁止越界）
- 不改 Workspace Runtime / Task / Workflow Runtime / Employee Session / CEO Office 前端；
- 不删除业务数据，仅回填或标记；
- 修复前已备份 `data/admin.sqlite.20260717.pre-split`。

## 流程
- Workspace ACKNOWLEDGED 并确认方案后，Admin 执行 092（T2 修正脚本 + T3 QA 校验）；
- 验收：所有 instances 的 `template_id` 可解析（SQL `NOT IN` 模板表 = 0），实例化 API 可重新解析这些实例。

## Workspace 处置结果（2026-07-17）

- 已先查询 13 类员工运行引用与 3 类部门运行引用；18 个员工、2 个部门均无真实运行引用。
- 5 个员工按唯一 active role 映射到真实 `et_*`；其余 13 个映射不唯一或不存在，保留原 ID/来源并标记 `deprecated`、`enabled=0`。
- 2 个部门分别回填 `dt_engineering`、`official.department.content_growth`；未删除任何实例，未解释孤儿数为 0。
- 回滚备份：`data/curis.sqlite.20260717.pre-r2-orphan`（本地忽略文件，不入库）。
