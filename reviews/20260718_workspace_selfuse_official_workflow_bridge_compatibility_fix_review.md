# Workspace selfuse 官方 Workflow 版本桥兼容修复质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_selfuse_official_workflow_bridge_compatibility_fix.md`
- 分支：`feat/roadmap-r1r2`
- 固定修订：`f01b3df4d1dbb81f277bcbfac9aae0a1aad53700`
- 验证席：质量运行席

## 结论

**PASS。**

原父 Gate 的 15 项 Wave1/2 影响集已全部恢复，版本桥的精确版本及 missing / duplicate / version mismatch / revoked / design-only / cross-tenant / client override 拒绝仍成立。全量不再出现原 8 failed + 7 errors，本修复未新增失败。

父 Gate 第 1/3 步的唯一已登记阻塞已解除；可交产品规划席确认后进入 R4 代码审计，不代表授权 Tool、前端或 provenance Step1。

## 独立证据

### 1. 修订与范围

- 当前 HEAD 与指定 SHA 一致：`f01b3df4d1dbb81f277bcbfac9aae0a1aad53700`。
- 修订仅涉及 `backend/app/company_instantiation.py`、`backend/app/database.py`、`backend/tests/test_package_workflow_versioned_bridge.py`。
- `git diff --check 0947b9e6..f01b3df4`：PASS。
- 未修改资产、历史 Run、Tool、前端、模型、网关或成本；未启动服务、未注 Key、未出网、未调用模型。

### 2. 原影响集与桥负向

命令：

```text
cd backend
.venv/bin/python -m pytest -q \
  tests/test_package_workflow_versioned_bridge.py \
  tests/test_v1_wave1_ceo_overview.py \
  tests/test_v1_wave1_publish_package.py \
  tests/test_v1_wave1_rd_runtime.py \
  tests/test_v1_wave1_seed.py \
  tests/test_v1_wave2_rd_engine.py \
  tests/test_v1_wave2_tool_exists.py
```

结果：**28 passed / 0 failed / 0 skipped**，6.33s。

覆盖原 15 项失败/错误、selfuse official 正向解析，以及 missing、duplicate、version mismatch、revoked、design-only、cross-tenant、禁止 default/latest/name 推断和客户端来源覆盖。

### 3. Wave1/2 扩展集

命令：

```text
.venv/bin/python -m pytest -q \
  tests/test_package_workflow_versioned_bridge.py \
  tests/test_v1_wave1_*.py tests/test_v1_wave2_*.py -rs --tb=short
```

结果：**45 passed / 2 skipped / 0 failed**，77.54s。

两项跳过均为本机环境限制：esbuild 无法联网下载；Docker daemon 不可用。交付席报告的“46 passed + 1 个 docker compose 环境失败”在本机表现为两项显式 skip，不影响后端版本桥结论。

### 4. 一次全量回归

命令：`cd backend && .venv/bin/python -m pytest -q`

结果：**671 passed / 20 failed / 2 skipped / 0 errors**，132.23s。

与修复前 **655 passed / 28 failed / 2 skipped / 7 errors** 比较：

- 原 8 failed + 7 errors 全部消失；
- 新增的 selfuse 正向用例通过，因此通过数增加 16；
- 剩余 20 项与修复前非 Wave 失败集合逐项一致，仍是 ADR-0028 旧可信 CEO/Admin 断言、`default/selfuse` 旧断言与校验、Department/Platform 旧断言、vector 扫描和前端标签检查；不是本修复新增。

### 5. 公共修复点与 fail-closed

- Source Workflow 统一经既有 `get_workflow_content(id, tenant)` 读取；官方来源保持全局可见，从而兼容其 `tenant_id` 被迁移为 `selfuse` 的既有事实。
- Resolver 随后仍精确核对 source、version、active、enabled；不接受 marketplace、缺失版本或不可执行状态。
- Target Workflow 统一经 `get_official_workflow_template_version(id, version)` 精确读取，只接受 active、enabled、official；没有 default/latest/same-name 回退。
- Company 实例化只对批准的 `ccp_ai_software_company@1.0.0` 强制版本桥；其他既有包不被错误要求具备该桥。
- 负向测试证明拒绝发生在实例/Task/Run 写入前，跨租户与撤销边界未放宽。

## Gate 判断

- selfuse official Workflow 精确版本桥兼容：**通过**。
- 原 15 项 Wave1/2 回归：**已清零**。
- 本修复新增回归：**无**。
- 父 Gate 是否可进入下一步：**可提交产品规划席确认；确认后可进入 R4 代码审计**。
- provenance Step1：继续 `PAUSED_BY_NEW_PRIORITY`。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
