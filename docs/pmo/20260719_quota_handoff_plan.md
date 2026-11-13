# 2026-07-19 额度切换交接计划

## 当前唯一目标

处理已确认的 Workspace `create_app_failed`，恢复可用 `/health`；随后才继续 D1 真实研发工具闭环。

## 已实现并验证

- `09c26a8e`：`main.py` 固定启动信号，Review：`reviews/20260719_workspace_startup_stage_signal_minimal_implementation_review.md`。
- `76b6d2ba`：Workspace 路径抑制 Admin 专属警告，Admin 行为不变。
- `ed8376f1`：Workspace 专用启动入口与 Docker CMD，质量 focused 5 OK；Admin 未改。
- `4d04cffa`：两条镜像 digest、四域名、唯一在线 build 与构建后 sentinel 均经质量核验；分类为 `create_app_failed`。

已实现能力：Workspace 启动链可输出四类固定分类或单字段 `unknown`；真实新镜像已返回可采信 `create_app_failed`。

## 当前进行中

- 已完成 Issue：`issues/20260719_workspace_pinned_online_build_postbuild_sentinel.md`。
- 状态：`PAUSED_FOR_QUOTA_HANDOFF`，无活动实施 Issue。
- 最新待办：仅处理已确认的 `create_app_failed`；额度恢复前不实施。

## 外部授权与禁止项

- 允许域名仅：`auth.docker.io`、`registry-1.docker.io`、`pypi.org`、`files.pythonhosted.org`。
- 固定镜像：
  - `python:3.14-slim@sha256:cea0e6040540fb2b965b6e7fb5ffa00871e632eef63719f0ea54bca189ce14a6`
  - `envoyproxy/envoy:v1.31-latest@sha256:caa5b411be1633b90023592a34a7e010c933d6e60206c758f631485e53006865`
- 禁止：Key、模型、D1、pytest、业务请求、其他镜像、其他包源、其他域名和重试。

## D1 授权与阻塞

- D1 真实模型 / 工具 E2E 授权仍为 `0/1`，尚未消耗；保持冻结。
- 真实阻塞：`create_app_failed` 的具体最小修复尚未处理；此前三次旧 sentinel 均不得重试。
- 当前暂停原因：额度切换交接；不是新的代码结论。

## 单主执行模式

系统交付席在既定目标和本地范围内连续诊断、最小修复、focused 验证、重跑；不为普通小故障新建 Gate。质量席只做里程碑独立验收和最终 E2E。安全席只在密钥、外部出网、跨租户 / 隐私、不可逆数据或新范围时介入。产品席只维护一个目标、停点汇报和最终验收。

## 正式席位与路由

- 总控决策席：`019f6c51-6fc8-7642-927b-bd4f15828669`
- 系统交付席：`019f6c48-8999-7ac1-aade-119ac71b483d`
- 质量运行席：`019f6cb7-3e8d-7313-91d9-95b226c9ed2e`
- 安全边界席：`019f6c48-bca4-7be3-8ff0-dccaf3ea5b93`
- 路由：总控 / 产品 → 系统交付单主执行 → 质量里程碑 / 最终验收 → 产品收口 → 总控。

## 新团队首个动作与完成判定

1. 额度恢复后，系统交付席在同一主目标内定位并最小修复 `create_app_failed`；不重放历史 sentinel。
2. focused 验证后，质量席只做里程碑验收；外部出网或新范围才交安全席。
3. 只有恢复可采信健康状态后，才由总控决定 D1 真实 E2E 是否解除冻结；否则停点汇报，不猜测、不重试。
