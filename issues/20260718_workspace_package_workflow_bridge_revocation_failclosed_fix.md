# Workspace：版本化桥接撤销后 Run 创建必须拒绝

- 状态：`VERIFIED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 质量复核：质量运行席
- 父 Issue：`issues/20260718_workspace_package_workflow_versioned_bridge_implementation.md`

## 目标

在 Task / Run 任何写入发生前，复用唯一的精确桥接校验，确保已撤销、非 active、无 tenant 可见性或版本不一致的桥接不能创建 Run。

## 最小修复

1. 不另造第二套判断；复用实例化路径的精确 bridge 校验。
2. 在 Task / Run 写入前校验 bridge ID、版本、`active`、`revoked_at`、tenant 可见性、结构化可执行状态及 capability。
3. 任一失败必须 fail-closed：拒绝请求，Task / Run / Step / Usage 均零写入。
4. 增加 focused 回归：先合法创建 Workflow Instance，再撤销 bridge 后创建 Run；断言拒绝且所有运行实体计数不变。

## 禁止范围

- 不改 bridge 数据、历史 Company / Run / Usage、模型、网关、成本、前端或公开 API。
- 不启动模型、不注入凭据、不调用外部服务。

## 验收

- 质量运行席独立复跑撤销后零写入用例和既有正向用例。
- 仅在父 Issue 的全部 fail-closed 条件重获 PASS 后，才恢复父 Issue 验收；真实模型调用仍需另立 Gate。

## 验证结果

质量运行席在 `bc9b55ec` 独立复核：撤销 bridge 后创建 Run 返回 422，Task / Run / Step / Usage 计数均不变；focused 16 passed，compileall PASS。见 `reviews/20260718_workspace_package_workflow_bridge_revocation_failclosed_fix_review.md`。
