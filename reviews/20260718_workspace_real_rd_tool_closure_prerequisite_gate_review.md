# Workspace 真实研发工具闭环前置 Gate（第 1/3 步）质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_real_rd_tool_closure_prerequisite_gate.md`
- 分支：`feat/roadmap-r1r2`
- 固定修订：`0947b9e6425dc586e77303e559098df2394fa6ad`
- 验证范围：既有项目全量回归、失败归因、是否可进入 R4 代码审计
- 验证席：质量运行席

## 结论

**BLOCKED（第 1/3 步已执行，但验收未通过；不得进入 R4 代码审计）。**

固定修订全量结果为 **655 passed / 28 failed / 2 skipped / 7 errors**，共 692 项，耗时 137.99s。相对最近已记录的固定全量基线 **609 passed / 19 failed / 0 skipped**，当前出现直接命中研发闭环的新增失败：Wave-1/2 的 Company Package 实例化在写入前被版本化 Workflow bridge 拒绝，导致 8 failed + 7 errors。该失败覆盖研发 Runtime、Seed、CEO Overview、Publish Package、RD Engine 和 Tool Exists，直接阻断“最小真实研发工具集”后续实施资格。

## 独立证据

### 1. 固定修订与边界

- `git rev-parse HEAD`：`0947b9e6425dc586e77303e559098df2394fa6ad`。
- 当前分支：`feat/roadmap-r1r2`。
- `backend/app` 与 `backend/tests` 无相对该修订的本地改动；工作区既有文档/状态文件改动未参与本次验证。
- 未修改代码、数据、配置或运行环境；未实现 Tool、未做前端。
- provenance Step1 保持 `PAUSED_BY_NEW_PRIORITY`；未注 Key、未启动服务、未发 HTTP、未调用模型。

### 2. 全量回归

命令：

```text
cd backend
.venv/bin/python -m pytest -q
```

结果：

- 通过：**655**
- 失败：**28**
- 跳过：**2**
- 错误：**7**
- 总计：**692**
- 警告：57,379
- 耗时：137.99s

### 3. 跳过项

聚焦复核跳过原因：

- `tests/test_v1_wave1_frontend.py`：网络受限，esbuild 无法下载，跳过前端语法检查。
- `tests/test_v1_wave2_docker_compliance.py`：Docker daemon 不可用，跳过 compose config 校验。

本 Issue 禁止前端和运行环境变更，因此两项仅记录为环境跳过，不在本席启动或修复。

### 4. 新增且直接阻断研发工具闭环的失败

共 **15 个失败结果（8 failed + 7 errors）**，均在 `CompanyInstantiationService.instantiate("ccp_ai_software_company", "selfuse")` 阶段触发同一异常：

```text
ValueError: workflow bridge source version is not available
```

涉及：

- `test_v1_wave1_rd_runtime.py`：2 failed
- `test_v1_wave1_seed.py`：2 failed
- `test_v1_wave2_rd_engine.py`：3 failed
- `test_v1_wave2_tool_exists.py`：1 failed
- `test_v1_wave1_ceo_overview.py`：2 errors
- `test_v1_wave1_publish_package.py`：5 errors

静态归因：`wave1_seed._migrate_selfuse_tenant()` 会把 `workflow_contents` 的 `tenant_id` 从 `platform` 归一到 `selfuse`，但该行仍为 `source='official'`；版本化 bridge resolver 对租户行只接受 `tenant_private` 或 `Curis internal`，因此精确的 `wl_ai_rd_software_dev_sop@1.0.0` 在 `selfuse` 下不可见。失败发生在 Company/Task/Run 写入前，fail-closed 本身成立，但既有 Wave-1/2 研发消费链被切断。

### 5. 其余失败归因

其余 **20 failed** 聚焦复跑为 **91 passed / 20 failed**，均落在历史已知失败族：

- ADR-0028 旧可信 CEO/Admin 读取与 UsageEvent 断言：4
- `default/selfuse` 旧断言与 D1 校验脚本：5
- Department/Platform 旧上下文、跨连接和列表断言：9
- vector 禁止区旧扫描：1
- 前端 `tenant_private` 标签旧检查：1

但最近固定基线记录的是 19 项失败，未保存逐测试清单；当前同族为 20 项，**不能仅凭类别把多出的 1 项认定为既有失败**。因此除上述 15 项明确新增阻断外，失败集合还存在 1 项数量漂移，需随最小修复后的全量重跑一并核销。

## Gate 判断

- 第 1/3 步执行状态：**已完成回归，结果失败**。
- 是否存在阻断最小真实研发工具集的新增回归：**是**。
- 是否可进入 R4 代码审计：**否**。
- 是否授权 Tool、前端或 provenance Step1：**否**。

## 唯一下一步

由系统交付席建立最小修复 Issue：只对齐 Wave-1 `selfuse` 迁移后的 Workflow source/version 可见性与版本化 bridge 精确解析，保持 missing/duplicate/version/cross-tenant/revoked/design-only 全部 fail-closed；修复后由质量运行席在同一规则下重跑一次全量。全量失败集合回到可解释基线且 Wave-1/2 研发链恢复前，产品规划席不得批准进入 R4 代码审计。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
