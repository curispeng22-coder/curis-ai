# 真实研发闭环 · 本地复跑与 sandbox 开关说明

本文档说明「真实研发闭环 hardening」（步骤③ sandbox 硬依赖降级 + 步骤① 非沙箱开关封装）
的设计意图、开关用法与安全边界。

## 1. 背景

`LocalRDToolset.run_test` 原先**硬检查** `/usr/bin/sandbox-exec` 是否存在，缺失即
抛 `sandbox_unavailable`。在 WorkBuddy 外层沙箱等环境下该路径不可见，导致真实闭环只能在
`/tmp/real_rd_prove.py` 的 `ProofLocalRDToolset` 覆写里跑，无法在代码库内一键复跑。

本次 hardening 将硬依赖降级为**可配置策略**（见 `backend/app/local_rd_toolset.py`
的 `SandboxMode` 与 `LocalRDToolset.__init__(sandbox_mode=...)`），并透传到
`RealRDExecutor`（`sandbox_mode=...`）。

## 2. SandboxMode 三态

| 模式 | 行为 | 适用场景 |
| --- | --- | --- |
| `AUTO`（默认） | sandbox-exec 存在则走隔离；缺失则**降级为直跑**，审计标记 `sandbox_degraded=True` | 本地开发 / 受信 CI |
| `OFF` | 关闭隔离，直接执行注册命令 | 仅本地开发 / 受信 CI |
| `ENFORCE` | 强制隔离；sandbox-exec 缺失时**直接拒绝**（`sandbox_unavailable`，fail-closed） | 生产多租户（必须确保 sandbox-exec 存在，或显式 ENFORCE） |

> ⚠️ **安全红线**：`OFF` 与 `AUTO` 缺失下**失去网络隔离**能力。仅限本地开发 /
> 受信 CI 使用。**生产多租户环境必须 `ENFORCE`，或确保 `/usr/bin/sandbox-exec`
> 真实存在**；切勿在生产用 `OFF`/`AUTO` 跑不可信输入。

## 3. 配置方式

1. **环境变量**（作用于 `LocalRDToolset` 默认解析）：
   ```bash
   export CURIS_RD_SANDBOX=auto      # auto | off | enforce
   ```
2. **代码透传**：`RealRDExecutor(model, event_log, sandbox_mode=SandboxMode.OFF)`
   会原样透传给其构造的三个 `LocalRDToolset` 实例。

## 4. 本地一键复跑

脚本：`backend/scripts/run_real_rd.py`

```bash
# 加载 deploy/new-api/.env 注入模型网关环境（不写死密钥）
python backend/scripts/run_real_rd.py --issue spec.json
python backend/scripts/run_real_rd.py --issue spec.json --no-sandbox   # OFF
echo '{"issue_id":"rd-001","target_file":"tools/real_rd_fixture/target_a.py",\
       "issue":"Change BETA = 2 to BETA = 3",\
       "expected_test":"backend/tests/test_real_rd_fixture_a.py"}' \
  | python backend/scripts/run_real_rd.py --issue -
```

脚本行为：
- 加载 `deploy/new-api/.env` 注入 `CURIS_MODEL_GATEWAY_*` 环境（密钥不写死）。
- 构造 `ModelGatewayAdapter`（本地 New API `http://127.0.0.1:3000`，模型 `deepseek-v4-pro`）
  + 真实 `LocalRDToolset(sandbox_mode=auto，或 --no-sandbox → OFF)` + `RealRDExecutor`。
- 调用 `RealRDExecutor.run(issue_spec)`，打印 `status / rounds / test_exit_code / diff_text`。

`issue` 规格 JSON 字段见脚本内 docstring。

## 5. 审计一致性

无论走 / 不走 sandbox，`run_test` 都经由既有 `_execute` / `_audit` 与
`_safe_process_output`：路径白名单、脱敏、审计字段完全一致。仅 `AUTO` + sandbox 缺失时，
审计 `payload` 额外携带 `sandbox_degraded=True` 以可追溯降级。

## 6. 相关测试

- `backend/tests/test_local_rd_toolset_sandbox.py`：覆盖 run_test 三分支
  （AUTO+存在 / OFF / ENFORCE+缺失 / AUTO+缺失降级）。
- `backend/tests/test_real_rd_executor.py`：新增用例验证 `sandbox_mode` 透传至三个
  `LocalRDToolset` 实例。
- `backend/tests/fakes_rd.py`：`FakeLocalToolset` 测试替身（捕获 argv）。
