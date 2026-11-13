# D1 工具链解冻 — QA 脱敏专项验收（T5）

- **验收人**：严过关（QA 工程师）
- **日期**：2026-07-19
- **关联实现 Issue**：`issues/20260719_d1_toolchain_unfreeze_implement.md`
- **关联提案**：`issues/20260719_d1_toolchain_unfreeze_proposal.md`（§二 技术实现方案，总控 gate 批准 A+B）
- **范围**：T5 QA 脱敏专项（仅验收与文档，未修改任何源码）
- **结论**：**PASS_WITH_NOTES**

---

## 一、验收范围（T5 五项）

| # | 验收项 | 判定 |
|---|---|---|
| 1 | 脱敏红线：warning / 异常 / 启动信号 / 路由 detail 无绝对路径、无堆栈、无 Key、无参数值；统一用 `D1_UNAVAILABLE_MESSAGE` 或固定脱敏文案；`LocalRDToolError` 一律 `from None` | ✅ PASS |
| 2 | frozen 回退：`CURIS_D1_FROZEN=true` → `build_d1_toolchain` 返回 None、路由 503（kill-switch 整体回退） | ✅ PASS |
| 3 | E2E 1/1：基于单测 (a)(b)(c) + 容器实证，确认 D1 端到端从 0/1 → 1/1（非冻结配置下真实可用） | ✅ PASS（含说明见备注） |
| 4 | 范围护栏：未引入 L2 Gate 七项任何新范围；无新增依赖 | ✅ PASS |
| 5 | 回归：`/health` 仍 200；既有 `test_workspace_startup_stage_signal.py` 7/7 未破坏 | ✅ PASS |

---

## 二、复现步骤与结果

### 2.1 单元测试复跑（聚焦套件）

在仓库根执行主理人指定命令（独立复跑确认）：

```bash
backend/.venv/bin/python -m pytest \
  backend/tests/test_workspace_startup_stage_signal.py \
  backend/tests/test_d1_unfreeze.py \
  backend/tests/test_local_rd_toolset.py -q
```

**结果：16 passed in ~0.8s**（主理人测得同样 16 passed，独立复跑一致）。

| 测试文件 | 用例数 | 结果 |
|---|---|---|
| `backend/tests/test_workspace_startup_stage_signal.py` | 7 | ✅ 全部通过（回归未破坏） |
| `backend/tests/test_d1_unfreeze.py` | 3 | ✅ 全部通过（T4 新增） |
| `backend/tests/test_local_rd_toolset.py` | 6 | ✅ 全部通过（既有工具集回归） |

`test_d1_unfreeze.py` 三项逐一核对（与 T4 约定一致）：
- **(a) `test_build_non_frozen_returns_instance`**：非冻结 + 推导根存在 → `build_d1_toolchain` 返回非 `None` 实例，且未污染模块级 `_WORKSPACE_ROOT_OVERRIDE`。✅
- **(b) `test_build_frozen_returns_none`**：`frozen=True` → kill-switch 返回 `None`。✅
- **(c) `test_override_missing_root_raises_desensitized`**：覆盖位指向不存在路径 → 构造抛 `LocalRDToolError`（`failure_code="workspace_root_unavailable"`），且异常文案不含 `"/nonexistent"`；`build_d1_toolchain` 同样抛 `LocalRDToolError`。脱敏红线在用例内被断言。✅

### 2.2 脱敏 grep 核验（全仓 + 四文件）

| 检查项 | 命令/范围 | 结果 |
|---|---|---|
| 宿主机绝对路径残留 | `grep -rn "/Users/\|Documents/Curis" backend/` | **No matches**（整个 `backend/` 无残留；macOS 硬编码路径仅存于被删除行，见 §2.3） |
| 堆栈打印 | 4 文件 grep `logger.exception\|traceback\|format_exc\|print_exc\|exc_info` | **No matches**（无堆栈打印） |
| Key / 凭据 / 令牌 | 4 文件 grep `api_key\|secret\|token\|password\|Bearer` 命中均为既有正则常量或模型配置校验逻辑（`self.model.api_key` 为内存对象判空，非明文/日志输出） | 无泄漏点 |
| 新增第三方依赖 | 4 文件 import 清单 + `requirements.txt` | 仅标准库 + 既有内部模块；`requirements.txt` 仍为 5 项既有依赖（fastapi/uvicorn/pytest/httpx/pyyaml），未变 |

> 说明：`local_rd_toolset.py` 中出现的 `/usr/bin/git`、`/usr/bin/sandbox-exec`、`/usr/bin:/bin` 为固定系统二进制路径（预存在、非用户/工作区路径），不泄露工作区/宿主布局，不属脱敏红线范畴。

### 2.3 git diff 核验（四源文件 + 两测试）

工作树 diff 确认 D1 解冻仅触及 5 个文件，且与实现 Issue 约定一致：

- **`backend/app/d1_config.py`（新增）**：`D1ToolchainConfig(frozen, workspace_root_override, env_profile)` + `load_d1_config()` 读 `CURIS_D1_FROZEN`(默认 false)/`CURIS_D1_WORKSPACE_ROOT`(默认 None)/`CURIS_ENV`(默认 "prod")；多环境 profile 表；非法 profile → 回退 "prod" + 脱敏 warning；常量 `D1_UNAVAILABLE_MESSAGE`；仅标准库、不 import `local_rd_toolset`。
- **`backend/app/local_rd_toolset.py`**：删除行 `-WORKSPACE_ROOT = Path("/Users/yy/Documents/Curis AI Workspace")`（macOS 硬编码仅此一处、仅存删除行）；新增 `_DERIVED_ROOT = Path(__file__).resolve().parents[2]`、`_WORKSPACE_ROOT_OVERRIDE`、`_resolve_workspace_root(override)`；`__init__`(L108) 与 `_assert_root`(L430) 改用受控解析；保留 `WORKSPACE_ROOT = _DERIVED_ROOT` 别名。
- **`backend/app/d1_single_model_toolchain.py`**：`build_d1_toolchain(model, event_log, config=None)` 增 `config`；`config.frozen` → 返回 `None`；否则注入 `config.workspace_root_override` 到 `_WORKSPACE_ROOT_OVERRIDE`。
- **`backend/app/main.py`**：`create_app` 内 `d1_config = load_d1_config()` 后 `build_d1_toolchain(default_executor, event_log, d1_config)`；D1 路由 503 守卫收敛为 `if d1_toolchain is None or d1_config.frozen:`（L2051），`try:` 在函数体内（8/12 空格，未掉出）；detail 为固定脱敏文案 `"D1 toolchain unavailable"`。
- **`backend/tests/test_d1_unfreeze.py`（新增）**：(a)/(b)/(c) 三项（见 §2.1）。

### 2.4 容器级实证（主理人提供，引用为证据）

以下为总控 gate 后主理人重建 `gateway-workspace:latest` 的实测，作为 E2E 实证支撑（本 QA 环境未复跑容器，原样引用）：

- sentinel `CURIS_GATEWAY_SENTINEL=1` → `HTTP 200 health_ok`，三服务 running/exit 0（证据 `gateway-startup-20260719T143253Z-19175`，`http_code=200 failure_class=health_ok`）。
- detached workspace 容器内：① `/health`=200（2s）；② `build_d1_toolchain(None,None,load_d1_config())` → 返回 `D1SingleModelToolchain`（非 None）；③ `build_d1_toolchain(None,None,D1ToolchainConfig(frozen=True))` → `None`（kill-switch 生效）；④ `POST /api/workspace/internal/d1-tenant-reservation/run`（空 body）→ **HTTP 401 `untrusted_gateway_source`，不是 503** → 503 守卫未触发，证明 `d1_toolchain` 非 None 且未冻结（容器内真解冻）；401 为独立网关身份校验，与解冻无关。

---

## 三、测试通过率

- **聚焦套件**：16/16（100%）—— 7（启动信号回归）+ 3（D1 解冻）+ 6（工具集回归）。
- **D1 解冻专项（test_d1_unfreeze.py）**：3/3（100%）。
- **回归（test_workspace_startup_stage_signal.py）**：7/7（100%，未破坏）。

---

## 四、脱敏核验证据点（文件:行号）

| 证据点 | 内容 | 脱敏判定 |
|---|---|---|
| `d1_config.py:26` | `D1_UNAVAILABLE_MESSAGE = "D1 toolchain unavailable; service continues without it"`（统一脱敏常量定义） | ✅ 固定常量，无路径/堆栈/Key |
| `d1_config.py:31-35` | 多环境 profile 表 `dev/test/prod`（仅含 `allow_override`/`strict_root` 策略，无路径/Key） | ✅ |
| `d1_config.py:59-65` | `_resolve_env_profile`：非法 profile → 回退 `"prod"` + `logger.warning(D1_UNAVAILABLE_MESSAGE)` | ✅ 用统一常量 |
| `d1_config.py:68-91` | `load_d1_config`：读 `CURIS_D1_FROZEN`(默认 false)/`CURIS_D1_WORKSPACE_ROOT`(默认 None)/`CURIS_ENV`(默认 "prod") | ✅ 仅读 env，无路径/Key 硬编码 |
| `local_rd_toolset.py:24-28` | `_DERIVED_ROOT` / `WORKSPACE_ROOT` 别名 / `_WORKSPACE_ROOT_OVERRIDE`（无 macOS 硬编码） | ✅ |
| `local_rd_toolset.py:68-83` | `_resolve_workspace_root`：解析失败/符号链接 → `LocalRDToolError("workspace_root_unavailable", D1_UNAVAILABLE_MESSAGE)`，`from None`（L80） | ✅ 脱敏文案 + `from None` |
| `local_rd_toolset.py:108` | `__init__` 改用 `_resolve_workspace_root(_WORKSPACE_ROOT_OVERRIDE)` | ✅ 受控解析 |
| `local_rd_toolset.py:430` | `_assert_root` 改用 `_resolve_workspace_root(_WORKSPACE_ROOT_OVERRIDE)` | ✅ 受控解析 |
| `d1_single_model_toolchain.py:328-338` | `build_d1_toolchain` 增 `config`；`config.frozen`→`None`；注入 `workspace_root_override` | ✅ 无路径/Key 输出 |
| `main.py:907-912` | `load_d1_config()` + `try/except` 弹性降级 + 脱敏 warning | ✅ 见备注 R1 |
| `main.py:2051-2052` | 503 守卫：`if d1_toolchain is None or d1_config.frozen:` → `raise HTTPException(503, detail="D1 toolchain unavailable")` | ✅ 固定脱敏文案 |
| 4 文件 grep | 无 `logger.exception`/`traceback`/`format_exc`/`print_exc`/`exc_info` | ✅ 无堆栈打印 |
| 全仓 grep | 无 `/Users/`、`Documents/Curis` 残留（macOS 路径仅存于 `local_rd_toolset.py` 删除行） | ✅ |

---

## 五、五项验收逐项判定

1. **脱敏红线（PASS）**：全部 warning / 异常 / 启动信号 / 路由 detail 经 grep + 代码审阅，确认无绝对工作区路径、无堆栈打印、无 Key/凭据明文、无参数值泄露；新受控解析路径统一使用 `D1_UNAVAILABLE_MESSAGE` 并以 `from None` 斩断 `__cause__` 链；既有常量与正则（敏感值/路径拒绝）保持不变。
2. **frozen 回退（PASS）**：单测 (b) 与容器实证 ③ 双重确认 `CURIS_D1_FROZEN=true` → `build_d1_toolchain` 返回 `None`；`main.py:2051` 守卫在 `d1_config.frozen` 时直接 503。kill-switch 整体回退有效。
3. **E2E 1/1（PASS，含说明）**：单测 (a) 证明非冻结+推导根存在 → 返回真实 `D1SingleModelToolchain`；容器实证 ④ 证明非冻结配置下 D1 路由到达 `execute()`（返回 401 而非 503），即「容器内真解冻」。D1 端到端由 0/1（仅弹性降级）推进到 1/1（工具链真实可用）。完整 `.execute()` → `status=succeeded` 的真实执行路径依赖外部 R3 模型网关（凭据/网络），未在聚焦单测与无凭据容器内执行（属既有 E2E 脚本 `tools/verify_d1_tenant_reservation.py` + `backend/tests/test_d1_verify_script.py` 的边界，非本次解冻范围）。见备注 R2。
4. **范围护栏（PASS）**：diff 仅触及 `local_rd_toolset` 解析 + `d1_config` + `main.py` 接线 + `d1_single_model_toolchain` 签名；无外部平台/凭证接入、无自动改生产码、无多 Agent / Employee CRUD / 真实隔离 / 复杂 UI / 向量库；无新增第三方依赖（`requirements.txt` 未变）。不触 L2 Gate 七项。
5. **回归（PASS）**：容器 sentinel 实测 `/health`=200；聚焦套件中 `test_workspace_startup_stage_signal.py` 7/7 全过，启动信号回归未破坏。

---

## 六、已知问题 / 备注

- **R1（备注，非红线违规）**：`main.py:911` 启动降级 warning 文案为 `"D1 toolchain unavailable at startup; continuing without it (D1 frozen)"`，未复用 `D1_UNAVAILABLE_MESSAGE` 常量，但属「固定脱敏文案」（无路径/堆栈/Key/参数），符合跨文件约定中「`D1_UNAVAILABLE_MESSAGE` 或固定脱敏文案」的允许项。建议后续统一引用常量以消除文案漂移。
- **R2（说明，非缺陷）**：完整 `D1SingleModelToolchain.execute()` 返回 `status=succeeded` 的真实闭环依赖外部 R3 模型网关（凭据/网络），本次解冻验收以「工具链真实构建 + 路由非 503 触达 execute」为证据边界（单测 (a) + 容器实证 ④）。模型调用层 E2E 由原 D1 专用 E2E 脚本覆盖，不在 T5 解冻验收单测范围内。
- **R3（观察，建议主理人跟进）**：工作树中存在大量与本 Issue 无关的未提交改动（`docs/`、`issues/`、`data/`、`.workbuddy/` 等）。本 QA 仅核验 D1 解冻相关的 5 个文件，diff 与实现 Issue 约定完全一致；提醒按「提交纪律」仅提交 T1–T5 相关改动，勿将无关工作树修改混入本 Issue 提交。
- **R4（观察，非本次引入）**：`local_rd_toolset.py` 的 `_execute` 审计失败路径（`L285/L292/L302/L305`）的 `LocalRDToolError` 仍使用 `from audit_error`/`from error` 链式，其消息均为脱敏固定文案（"tool audit is unavailable"/"local tool failed" 等），无路径/Key 泄露；该路径属预存在代码、不在本次解冻 diff 内。本次新增的 workspace 根解析路径已严格 `from None`。如后续收紧全局 `from None` 纪律可一并处理，但不影响本次红线判定。

---

## 七、三段式结论

**结论：PASS_WITH_NOTES**

**原因**：
1. 脱敏红线专项核验全部通过——四文件经 grep 与代码审阅，无绝对工作区路径残留（macOS 硬编码仅存于删除行）、无堆栈打印、无 Key/凭据/参数值泄露；新增受控解析路径统一使用 `D1_UNAVAILABLE_MESSAGE` 并以 `from None` 斩断异常链；`main.py:2051` 路由 503 守卫与 detail 均为固定脱敏文案。
2. frozen 回退 kill-switch 经单测 (b) 与容器实证双重确认有效（`build_d1_toolchain`→None、路由→503）。
3. E2E 由 0/1 推进到 1/1 得到单测 (a)（真实构建）与容器实证 ④（非冻结路由触达 `execute`、非 503）支撑；D1 工具链在容器内确已真实解冻。
4. 范围护栏与依赖面经 diff + import 清单核验：未触 L2 Gate 七项、无新增第三方依赖。
5. 聚焦套件 16/16 通过，`/health` 200 与启动信号 7/7 回归均未破坏。
唯一需说明项：完整 `execute()`→`status=succeeded` 闭环依赖外部 R3 模型网关，本次以「构建真实实例 + 路由非 503」为证据边界；以及 `main.py:911` warning 未复用统一常量（仍属固定脱敏文案，不违规）。

**建议**：
1. 可推进本 Issue 提交与合入；提交时仅包含 T1–T5 相关的 5 个文件，勿混入工作树中无关改动（见 R3）。
2. 后续可小步重构：将 `main.py:911` 的 warning 改为引用 `D1_UNAVAILABLE_MESSAGE` 常量，消除文案漂移（R1）。
3. 模型调用层完整 E2E（`status=succeeded`）建议在具备 R3 凭据的受控环境中由既有 D1 专用脚本另行回归，作为解冻后的独立跟踪项（R2）。
4. 若后续决定全局收紧 `LocalRDToolError` 的 `from None` 纪律，可将 `_execute` 审计失败路径一并处理，但不阻塞本次验收（R4）。
