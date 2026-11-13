# 孤儿实例清理（employee_instances / department_instances）

状态：OPEN
类型：[Admin][Fix]
发起团队：Admin（产品规划席 齐活林）
归属模块：运行时实例（employee_instances / department_instances）
是否阻塞：否
是否触发 L2：否

## 结论
清理资产复盘发现的孤儿实例：`employee_instances`(18) 与 `department_instances`(2) 的 `template_id` 指向不存在的模板（`et_ai_rd_*` / `dt_ai_rd`），经 API 不可重新解析/校验，会误导"真实可用"判断。

## 真实证据
- `employee_instances` 18 行 `template_id` 全不在 `employee_templates`（仅 6 `et_*` + 10 `official.employee.*`）。
- `department_instances` 2 行 `template_id = dt_ai_rd / dt_ai_content`，不在 `department_templates`（仅 `dt_engineering` / `official.department.software_rnd` / `official.department.content_growth`）。
- `create_employee_instance` 要求模板存在，故用这些 ID 走 API 今日直接报错 → 早期绕过校验 seed 进库。

## 修改内容
- 方案 A：回填正确 `template_id`（映射 `et_ai_rd_*` → `et_*`/`official.employee.*`，`dt_ai_rd` → `dt_engineering` 等）。
- 方案 B：标记为历史残留/已停用（加 deprecated 标记，不删除），避免误判"真实可用"。
- 经架构师确认选 A 或 B，工程师实现，QA 校验。

## 验收方式
- 所有 instances 的 `template_id` 可解析（SQL 校验 `NOT IN` 模板表 = 0）。
- 实例化 API 可重新解析这些实例。

## 禁止越界
不改 Workspace Runtime；不删除业务数据（仅回填或标记）。

## 任务分解
- T1 映射规则（架构师）
- T2 修正/标记脚本（工程师）
- T3 QA 校验（严过关）
