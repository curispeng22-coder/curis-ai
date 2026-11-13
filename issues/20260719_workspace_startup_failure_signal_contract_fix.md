# Workspace 启动失败信号契约修复

- 状态：`CANCELLED_BY_TOTAL_CONTROLLED_REVERT`
- 优先级：`P0`
- 当前责任席：系统交付席
- 隔离基线：`fec65c1aa58010639d10eeca9cdfd099d54f805b`
- 父 Gate：`issues/20260719_workspace_startup_failure_deterministic_evidence_gate.md`（`CLOSED`，仅契约）
- 父 E2E：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（保持冻结）

## 已取消

总控最终裁决为受控撤销 `fec65c1a`。本 Issue 不得实施、不得补授权或逐 hunk 保留；撤销完成后仅保留本文件作为裁决变更审计。

## 唯一目标

只修复隔离改动，使 Workspace 启动失败的结构化信号严格符合已闭合契约，然后交质量席 focused 验收。

## 必须满足

1. `unknown` 只允许 `failure_code=unknown`；不得包含 stage、signal、原文或其他明细。
2. 整个 Workspace 启动 / uvicorn 路径的未知异常统一收敛为无原文 `unknown`，不得逃逸。
3. 仅 `database_initialize + schema_condition` 可映射为 `schema_incompatible`；其他 `DatabaseError` 一律 `unknown`。
4. 补齐总控最小实施授权索引与 focused 测试，覆盖未知、异常、精确 schema 及四种唯一映射。

## 禁止范围

- 不运行 sentinel、Docker、服务、D1 POST、pytest、模型或外网；不注 Key，不读写 D1 目标；
- 不新增诊断类别、自由字段、原始异常、日志、路径、环境值或客户端响应；
- 不回滚或扩大 `fec65c1a` 之外的范围，不修改数据库、Compose 以外的运行边界或父 D1 契约。

## 验收

- 系统交付只跑 focused 测试并交质量；
- 质量独立确认契约逐项成立，且零 sentinel / D1 / 模型副作用；
- 通过后仍须单独建立运行诊断 Gate，父 D1 才可继续。
