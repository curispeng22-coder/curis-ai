# DeepSeek 真实接入 · 验证报告

**日期**：2026-08-07
**结论**：✅ 通过。双击 `Curis.app` 即可用 DeepSeek 真实执行任务，无需手工设置任何环境变量，密钥零明文落库。

---

## 1. 密钥处置方式

| 项 | 落点 | 是否明文 |
|---|---|---|
| 密钥本体 | `deploy/new-api/.env` 的 `DEEPSEEK_API_KEY`（被 `deploy/.gitignore:2` 忽略） | 文件内为明文，但**不入库、不入 git** |
| 数据库记录 | `tenant_private_capabilities.metadata_json` | ❌ 无明文，仅 `"credential_ref": "env:DEEPSEEK_API_KEY"` |
| 接口返回 | `GET /api/workspace/capabilities/private` | ❌ 无 `sk-` 明文，仅引用 |

数据库实存内容：

```json
{
  "name": "deepseek-chat",
  "provider_type": "deepseek",
  "base_url": "https://api.deepseek.com",
  "model_name": "deepseek-chat",
  "credential_ref": "env:DEEPSEEK_API_KEY"
}
```

`main.py` 的 `_validate_reference` 显式拒绝 `plaintext://` 与 `raw_api_key`；前端 `PrivateModelDrawer` 只接受 `env:VAR` 引用。

## 2. 代码改动

**`backend/app/main.py`** 顶部新增 `_load_local_dotenv()`：进程启动时读取 `deploy/new-api/.env` 注入 `os.environ`，不覆盖已有变量、异常静默、零第三方依赖。

作用：解决此前「local-dev 密钥只在进程内存、重启即丢」的边界。密钥改为从文件加载，**跨重启可用且仍不入库**，原计划的 Fernet 加密密钥文件方案不再必要。

## 3. 端到端验证

### 第一轮（注入环境变量，:8000）

| 步骤 | 接口 | 结果 |
|---|---|---|
| 建公司/员工 | `POST /api/workspace/quickstart` | 200 |
| 注册模型 | `POST /api/workspace/private-models` | 201 |
| 绑定员工 | `PUT /api/workspace/employees/{id}/capabilities` | 200 |
| 建任务 + 执行 | `POST /api/task` → `POST /api/task/{id}/run` | 200，`status=COMPLETED` |

DeepSeek 真实返回：**「Curis 是一个 AI 全自动任务与工作流系统。」**

### 第二轮 · 无外挂复验（:8010，决定性）

第一轮在启动命令里显式注入了 `DEEPSEEK_API_KEY`，不能证明真实使用场景。故另起后端复验：

- 环境严格照抄桌面壳：`cd backend` + `CURIS_ENV=local` + `CURIS_IDENTITY_MODE=selfuse`
- **显式 `unset DEEPSEEK_API_KEY`**，仅靠 `_load_local_dotenv()` 取密钥

结果：

```
含 deepseek-chat: True
含 env: 引用     : True
含明文 sk-      : False
ai_readiness    : {'has_private_model': True, 'has_bound_employee': True}
task status     : COMPLETED
output          : 收到
```

→ **`.env` 加载器成立，用户双击 app 即可用。**

## 4. 数据与清理

- 复验任务 `5d7e5b1d` 已从 `tasks` / `executions` / `runtime_trace_event` 删除（`ai_usage_records` 设计为 immutable，保留属预期）。
- 仅保留有意义的 `cea5c278`（COMPLETED，含 DeepSeek 真实输出）。
- 临时后端 :8010 已关闭；`git status` 中无任何密钥文件。

## 5. 后台任务 failed 说明

三条后台任务的 failed 状态已逐一核查：

| task_id | 真实情况 |
|---|---|
| `3CYls1` | 路径写错（`backend/backend/.venv`），本就该失败 |
| `Tm7Kyj` | 同上 |
| `B0iYUh` | **实际成功**：运行 8m15s，所有验证请求 200/201，任务执行完成；长驻服务进程被 harness 回收才标 failed |

## 6. 使用方式

直接打开已有的 `Curis.app`（无需重建 —— `lib.rs` 运行时从仓库拉起 uvicorn/next，`main.py` 改动已生效）：

- 首屏不再出现「去绑模型」门禁；
- CEO 工作台 / 研发 / 小红书 / 抖音 任一空间点「启动任务」，走 `deepseek-chat` 真实执行；
- 能力中心可见已注册的 `deepseek-chat`。
