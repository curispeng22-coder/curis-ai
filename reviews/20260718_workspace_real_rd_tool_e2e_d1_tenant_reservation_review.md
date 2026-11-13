# Workspace 真实研发工具 E2E｜D1 Tenant Reservation 质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`
- 分支 / 修订：`feat/roadmap-r1r2` / `d57da0da16ea39c16d65b4da500de6e5674257e0`
- 质量结论：`PASS（仅无出网静态预检）`
- E2E 状态：`WAIT_FOR_OWNER_INJECTION`

## 独立证据

1. 固定身份链：实际库 `deploy/curis/gateway/.generated/data/quality.sqlite` 中，批准 issuer + subject 精确命中唯一 `selfuse` active owner membership；membership 未撤销、未过期、`ceo_id` 非空，且唯一 active Company 的 `ceo_id` 同值。selfuse membership / Company 计数均为 1。
2. 两文件保持固定且未改：
   - `tools/verify_d1_tenant_reservation.py`：10,580 bytes，SHA-256 `8187c6bc27b2e27fb2c654ee5b6be46311916d2d0300fb70072c3fb6418040e1`
   - `backend/tests/test_d1_verify_script.py`：3,335 bytes，SHA-256 `d9c6a13ae077a7f4f6e86131f4c9f2636c980c4db0d249fcaf640d9de234fae5`
   - API key / secret / password / Cookie / Authorization / Bearer / JWT / credential / private-key 模式扫描均为 0；目标未暂存、未提交的 diff 均为空。
3. 不可泛化入口仍固定：`selfuse / curis-ai-workspace / d1-tenant-reservation / 20260718-workspace-d1-tenant-reservation-single-model-e2e`；只允许上述两读路径、唯一写路径、4 KiB diff。
4. 唯一 `command_id` 为 `rd_e2e_verify_d1_tenant_reservation`，唯一 argv 精确为 `backend/.venv/bin/python -m pytest -q backend/tests/test_d1_verify_script.py`；Reader 与 Git Tool command registry 为空，Writer registry 仅此一项。
5. 入口在 claim 前强制 tenant 与可信 identity 均为 `selfuse`、membership 为 `active`、role 仅 `owner/ceo`、`ceo_id` 与 `request_id` 非空；同时校验固定模型配置、Tool scope、路径、命令与审计可用性。请求体和查询参数必须为空。
6. 零副作用：固定 D1 Run 对应 `workflow_runs/tasks/executions/tool_traces` 均为 0；同 correlation 的 claim/model/tool/usage 及其他 evolution event 总数为 0。授权未消费。
7. 环境：`3000/3100/8001/8002/8080` 全部 `CLOSED`；未启动、未注 Key、未调用模型、未读取或写入 D1 业务目标内容、未运行 pytest；仅对批准的两份代码文件执行只读哈希与敏感模式扫描。

## 状态判断

无出网静态预检全部通过。宿主仅检查 `CURIS_MODEL_GATEWAY_API_KEY` 存在性，结果为 `MISSING`，因此父 E2E 回到 `WAIT_FOR_OWNER_INJECTION`。

本 PASS 不授权启动、注 Key、模型调用、diff、测试命令或 E2E；仅待 Owner 隐藏注入完成并正式回传后，按既定单次契约继续。

Next Seat：产品规划席

Handoff: sent to 产品规划席
