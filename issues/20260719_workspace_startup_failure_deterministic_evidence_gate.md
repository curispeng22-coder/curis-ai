# Workspace 启动失败可判定证据 Gate

- 状态：`CLOSED`
- 优先级：`P0`
- 发起：产品规划席
- 架构意见：系统交付席
- 安全复核：安全边界席
- 父 Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`

## 目标

先固定一次 Workspace 启动失败诊断可回传的结构化、脱敏字段与分类规则；只有契约双 PASS 后，才可另行申请一次本地 sentinel 诊断。

## 唯一要解决的问题

现有证据只得到 `Workspace exited/1` 和 Gateway `503`，分类为 `unknown`。新契约必须能区分至少下列启动期类别：`import_failed`、`config_rejected`、`schema_incompatible`、`create_app_failed`、`unknown`。

## 允许范围

- 只读核对 Workspace 启动链、现有异常边界和现有脱敏/诊断机制；
- 形成固定 allowlist 字段、每个字段的来源、允许值、分类优先级和脱敏规则；
- 明确一次未来 sentinel 的最小回传格式与清理条件。

## 禁止范围

- 不启动容器或服务，不注 Key，不调用模型，不执行 D1 POST / pytest，不读写 D1 目标，不出网；
- 不保存或回显原始日志、stderr、Key、Header、Cookie、JWT、subject、环境变量原文、Prompt、Payload 或数据库行内容；
- 不修改运行时代码、Compose、数据库或现有诊断文件；
- 不将任意未允许字段、自由文本、堆栈、路径或原始异常作为回传内容。

## 验收标准

1. 架构与安全给出同一份字段 allowlist；字段不足或分类异常统一 `unknown`；
2. 每个允许分类都有确定的、无原文依赖的判定条件，且分类不重叠；
3. 诊断回传只能由 allowlist 组成，敏感命中、未知字段、多分类或脱敏失败时零明细、仅 `unknown`；
4. 明确诊断后立即 cleanup；D1、模型、外网、文件写入与测试均保持零副作用；
5. 双 PASS 后才建立一次性运行诊断 Issue；父 D1 在此之前保持冻结。

## 已对齐的唯一回传契约

- 固定公共字段：`event=startup_failure`、`component=workspace`、`container_exit_code=1`、`health_code∈{000,200,401,503}`、`log_lines_seen∈[0,200]`、`redaction_status=passed`、`cleanup_status=completed`、`timestamp=RFC3339`。
- 仅在完整、无冲突映射成立时，额外回传 `failed_stage`、`failure_signal` 与 `failure_code`：
  - `module_import + import_exception → import_failed`
  - `database_initialize + schema_condition → schema_incompatible`
  - `identity_config|admin_config|model_config + validator_rejection → config_rejected`
  - `create_app + factory_exception → create_app_failed`
- `unknown + unknown`、字段缺失、交叉组合、重复/多类别、敏感命中、脱敏失败或未知异常：只回传 `{failure_code:unknown}`，不回传阶段、信号或任何明细。
- 禁止 `reason`、`message`、`error`、`stack`、`path`、`details`、`source`、异常文本、原始日志、stderr、Key、Header、Cookie、JWT、subject、环境原文、Prompt、Payload 或数据库内容。

## 收口

架构、安全、质量对同一结构化映射契约均已 `PASS`。本 Gate 仅固定证据格式，不包含阶段标记实现或 sentinel 运行；父 D1 继续冻结。下一步必须由总控单独批准最小实现 Issue，再申请一次无秘密 sentinel 诊断。
