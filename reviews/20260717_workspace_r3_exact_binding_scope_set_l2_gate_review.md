# R3 精确 Binding Scope 集合 L2 Gate 质量 Review

- Issue：`issues/20260717_workspace_r3_exact_binding_scope_set_l2_gate.md`
- 固定分支/修订：`feat/roadmap-r1r2` @ `250fc6833e5b40ca5876d63bea654c6b407a1cef`
- 基线实现：`9a790746782240aaa5e6e45f39272073e4521553`
- 结论：`PASS`

## 结论

六角色 role→binding 的服务端选择、fail-closed、历史 Tech Lead UsageEvent 兼容与无出网聚焦测试通过。此前 `workspace.env.example` 经 Bash `source` 后 JSON 失真的唯一阻塞已由完整单引号修复；独立按现有启动脚本语义加载后，JSON 可解析且精确等于批准的六角色集合。本 Gate 质量复核 `PASS`。

## 已通过证据

- HEAD 与修复 SHA 一致；修复提交仅改 `deploy/curis/workspace.env.example`，`main.py` 授权逻辑未变。
- 独立聚焦命令：

```bash
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q \
  backend/tests/test_model_gateway_adapter.py -k 'r3_'
```

- 修复后独立结果：`13 passed, 6 deselected, 4408 warnings in 4.98s`。Warnings 为 FastAPI/Python 3.14 既有弃用提示，无测试失败。
- `backend/.venv/bin/python -m compileall -q backend/app backend/tests/test_model_gateway_adapter.py`：PASS。
- `git diff --check HEAD^ HEAD`：PASS。
- 静态与测试确认：
  - 配置仅接受六个固定 role，拒绝缺失、空、未知、重复 role、重复或非法 binding UUID；新集合错误时不回退旧单值。
  - 当前 Step 的服务端 `employee_role` 是唯一 binding 选择键，请求没有 role/binding 覆盖入口。
  - binding 继续校验 tenant/company/department/project/run/workflow/step/employee/role/capability；唯一可执行 Employee、唯一 enabled binding、active Department/Project 均为前置条件。
  - 历史 UsageEvent 按其 Step role 映射到对应 binding，Tech Lead 首步不再与后续角色 binding 冲突。
  - 六角色七步正向、重复调用、跳步、预算不足及 role/binding/config/资源错配均由 RecordingHttpPost 证明在网络前处理。
- `3000/3100/8001/8002/8080` 均为 CLOSED；未启动、未注 Key、未出网、未跑全量、未改数据。

## 阻塞解除证据

`deploy/curis/run-workspace-backend.sh` 使用：

```bash
source "${CURIS_WORKSPACE_ENV:-deploy/curis/workspace.env.example}"
```

修复提交把完整 JSON 用单引号整体引用。独立严格复用 `set -a + source + set +a` 后执行断言：

- `json.loads`：PASS；
- 与批准六角色 role→binding 字典精确相等：PASS；
- roles：`6`；
- raw bytes：`360`；
- `git diff --check HEAD^ HEAD`：PASS。

原 `INVALID_JSON_AFTER_SOURCE` 阻塞已独立复现为解除，无剩余质量阻塞。

## 状态

- 服务端集合与聚焦测试：`VERIFIED — PASS`
- 仓库启动配置装载：`VERIFIED — PASS`
- 最终：`PASS`
- 剩余阻塞：无（仅限本 Binding Scope Gate；不代表剩余六步已真实执行）。
- Next Seat：产品规划席
- Handoff：sent to 产品规划席
