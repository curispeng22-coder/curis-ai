# Workspace 启动阶段信号最小实现

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 授权：总控 `APPROVE_NEW_MINIMAL_STARTUP_STAGE_SIGNAL_IMPLEMENTATION_ISSUE`
- 复用契约：`issues/20260719_workspace_startup_failure_deterministic_evidence_gate.md`（`CLOSED`）
- 父 E2E：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（保持冻结）
- 固定质量路由：`019f6cb7-3e8d-7313-91d9-95b226c9ed2e`

## 唯一目标

在既有 Workspace 启动边界中，增加固定、互斥、无原文的阶段信号，使未来的本地 sentinel 能按照已闭合契约分类失败。

## 精确范围

- 只允许修改 `backend/app/main.py`；
- 只允许新增或修改一份 focused 测试：`backend/tests/test_workspace_startup_stage_signal.py`；
- 复用既有 Docker CMD 与既有启动链；不新增模块、通用诊断框架、配置项、日志存储、环境变量或客户端接口。

## 固定信号契约

仅允许四组完整映射：

- `module_import + import_exception → import_failed`
- `database_initialize + schema_condition → schema_incompatible`
- `identity_config|admin_config|model_config + validator_rejection → config_rejected`
- `create_app + factory_exception → create_app_failed`

所有其他情况（字段缺失、冲突、多类别、普通数据库异常、未知异常、敏感命中或脱敏失败）严格仅为 `failure_code=unknown`，不得携带 stage、signal、异常文本、路径、堆栈或任何自由字段。

## 禁止范围

- 不运行 Docker / 服务 / sentinel，不注 Key，不调用模型、D1、pytest 或外网；
- 不修改 Dockerfile、Compose、数据库、启动脚本、D1、工具链或父 E2E；
- 不保存、回传或暴露原始 stderr / 日志 / Key / Header / Cookie / JWT / subject / 环境原文 / Prompt / Payload / DB 内容；
- 不新增通用异常处理、诊断框架、日志框架或可配置分类。

## 验收

1. focused 测试覆盖四种唯一映射、严格 single-field `unknown`、普通 `DatabaseError=unknown` 与启动路径未知异常不逃逸；
2. 系统交付只跑 focused 检查并交质量；
3. 质量独立确认无出网、无运行副作用且契约逐项成立；
4. 仅在质量 PASS 后，产品规划席才可建立一次无秘密 sentinel 诊断 Issue；D1 在此之前继续冻结。

## 收口

质量 Review `reviews/20260719_workspace_startup_stage_signal_minimal_implementation_review.md` 在 `09c26a8e` 给出 `PASS`。下一步仅为一次无秘密 sentinel 诊断。
