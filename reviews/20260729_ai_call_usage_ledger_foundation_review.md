# AI Call Usage Ledger Foundation Review

Issue: `issues/20260729_ai_call_usage_ledger_foundation.md`

Final HEAD: `e6371ae957da77a8a40f31cc34547850d5b10f3f`

Status: `PASS（Issue Scope）`

## 结论

AI Call Usage Ledger Foundation 的 Issue 范围质量验收通过。

首轮 Backend 全量回归在提交 `3aefe836331c4d679d28de53c62bd60c8bb0873a` 上得到
`16 failed, 1146 passed, 2 skipped`。按质量指令不重复全量；最终 HEAD
`e6371ae9` 仅复验其中 10 个 AI Usage 相关失败节点，并追加
`backend/tests/test_ai_usage_ledger.py` 与 `backend/tests/test_local_rd_toolset.py`，
最终 `21 passed, 0 failed`。

其余 6 个失败节点属于 Issue 外、当前 workspace 尚未提交的 Department
Delete / employee affiliation 变更，不属于 AI Usage Ledger 修复范围；主线程已对这
6 个节点完成聚焦验证并回传 PASS。本 Review 不把它们归因于本 Issue，也未扩展修复。

安全边界席已对最终提交 `e6371ae9` 回传 `PASS`。本次未连接外部服务、未发起真实模型
调用、未读取或写入凭据。

## 证据

### 提交与范围

- 初始实现提交：`3aefe836331c4d679d28de53c62bd60c8bb0873a`
- 归因修复：`5f802750`（`fix(usage): close ledger attribution gaps`）
- 最终修复：`e6371ae9`（`fix(usage): remove local tool pseudo-metering`）
- 最终 HEAD：`e6371ae957da77a8a40f31cc34547850d5b10f3f`
- `git diff --check`：PASS。
- 当前 workspace 仍有 Issue 外未提交变更：
  - `backend/app/company_project_runtime.py`
  - `backend/app/database.py`
  - `backend/app/main.py`
  - `backend/app/employee_affiliations.py`
- 静态 diff 复核表明上述增量属于 ADR-0017 employee affiliation / Project
  delete 路径，不是 AI Usage Ledger 契约扩展。

### 首轮 Backend 全量

隔离 detached worktree 固定在 `3aefe836`：

```text
.venv/bin/python -m pytest backend/tests
```

结果：

```text
16 failed, 1146 passed, 2 skipped
```

首个失败表现为旧测试仍期待
`usage.model_call, usage.tool_call, usage.task_execution` 三条审计事件，实际只得到
`usage.tool_call, usage.task_execution`。这暴露了旧 `usage.model_call` 契约与新
权威账本的归因/审计引用尚未同步。

16 个失败分为：

- 10 个 AI Usage 相关节点：旧 usage event、模型选择、Credential、S8/S9/S12、
  RealRD 与本地 Tool 伪计量契约。
- 6 个 Issue 外 Department Delete 节点：
  - `backend/tests/test_employee_directory_qa.py` 下 5 个节点；
  - `backend/tests/test_mvp_phase1_s2_workspace.py::MVPPhase1S2WorkspaceTests::test_department_can_be_updated_and_active_employee_blocks_delete`。

### 最终聚焦复验

最终 HEAD `e6371ae9` 执行：

```text
.venv/bin/python -m pytest \
  backend/tests/test_ai_usage_ledger.py \
  backend/tests/test_local_rd_toolset.py \
  <首轮 10 个 AI Usage 相关失败节点>
```

结果：

```text
21 passed, 0 failed
```

构成：

- `backend/tests/test_ai_usage_ledger.py`：`5 passed`
- `backend/tests/test_local_rd_toolset.py`：`6 passed`
- 首轮 10 个 AI Usage 相关失败节点：`10 passed`

已闭合的 10 个节点：

1. `test_task_execution_can_select_tenant_private_tool_and_usage_records_private_source`
2. `test_task_execution_emits_tenant_and_ceo_scoped_usage_event`
3. `test_usage_events_are_idempotent_for_same_execution`
4. `test_real_development_task_writes_tests_and_records_git_diff`
5. `test_real_content_task_persists_copy_svg_and_retrospective`
6. `test_local_selfuse_execution_has_trusted_ceo_usage_context`
7. `test_private_capabilities_bind_credential_ref_and_usage_event_is_redacted`
8. `test_a4_real_executor_modifies_target_a`
9. `test_target_a_test_fails`
10. `test_runtime_uses_valid_preference_through_model_gateway_adapter_and_falls_back_when_invalid`

按指令未执行第二次 Backend 全量回归。

### Frontend 回归

虽然本 Issue 无前端代码变更，仍完成既有 Frontend 回归：

- Frontend tests：`49 passed, 0 failed`
- Frontend lint：PASS
- Frontend build：PASS
- Next.js 静态页面：`28`

隔离 worktree 首次 build 因 `node_modules` 跨 worktree 符号链接被 Turbopack
拒绝；使用同一 lockfile 的离线本地依赖目录后 build PASS。该失败属于隔离验证环境，
不是产品代码失败。

### 官方启动链

- 官方命令：
  `CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh`
- 启动结果：PASS。
  - Frontend：`3001`
  - Workspace：容器内部 `8002`
  - Gateway：`8080`
- 当前只读健康复核：
  - `GET http://127.0.0.1:8080/health`：`200`
  - `GET http://127.0.0.1:3001/gateway/api/auth/local/status`：`200`
- 启动链相关文件在 `5f802750..e6371ae9` 未变化，因此复用既有启动证据，未重复重启。

### 契约覆盖

`backend/tests/test_ai_usage_ledger.py` 最终 5 项覆盖：

- 追加式 usage record 与禁止普通更新/物理删除；
- Token/成本未知保持 `NULL`，成本使用固定精度；
- tenant、Business Department、Project、Task、Employee、Capability 归属校验；
- idempotency、聚合、跨租户隔离；
- Retry/Fallback 每次真实出站尝试独立记录；
- 审计事件只引用 `usage_record_id`；
- Prompt、回答、API Key、Credential、原始供应商响应不进入账本或接口。

安全边界席对最终提交 `e6371ae9` 的敏感字段、追加性、伪计量移除和无外部服务扩张
结论为 `PASS`。

## 阻塞项

本 Issue 范围无阻塞。

Workspace 的 Issue 外未提交 Department Delete / employee affiliation 变更必须继续由
其所属 Issue 管理。本 Review 仅记录主线程回传的 6 节点聚焦 PASS，不替代其正式
Review，也不把它们纳入 AI Usage Ledger 的修改范围。

## 建议

1. 产品规划席接受 AI Call Usage Ledger Foundation，并关闭本 Issue。
2. Token 与 AI 成本后续只从 `ai_usage_records` 读取；不得恢复旧伪计量或重复汇总。
3. UI、数据洞察、预算、账单、历史回填与外部插件继续另立 Issue。
4. 相关代码未变化时，不重复 Backend 全量、Frontend 或启动链验证。

Handoff: sent to 产品规划席；建议接受并关闭本 Issue。
