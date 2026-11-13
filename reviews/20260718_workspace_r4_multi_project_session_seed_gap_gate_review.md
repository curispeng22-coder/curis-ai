# Workspace R4 第2项子Issue C0｜跨项目样本前置复核结果

- 日期：2026-07-18
- 状态：PASS（C0 解除）
- Issue：`issues/20260718_workspace_r4_multi_project_session_seed_gap_gate.md`
- 分支：`feat/roadmap-r1r2`
- 证据数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 执行方式：只读 + 可复核 API/SQL 采样（最小预置）

## 证据与核验

### 1）补齐跨项目样本

- 新建项目：
  - `project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`
  - 同租户：`tenant-a`
  - 同公司：`company-a`
- 新建工作流 run：
  - `wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`
  - 归属项目：`project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`
  - `tenant-a`、`official.workflow.software_rnd_sop`

### 2）`C0` 核验 SQL

按 `issues/20260718_workspace_r4_multi_project_session_seed_gap_gate.md` 内核验脚本聚合：

- `multi-project candidates: 2`

返回示例：

```text
{'tenant_id': 'tenant-a', 'employee_id': 'emp-7417237e-2f30-4268-807f-88eaaf951bf8', 'c': 2}
{'tenant_id': 'tenant-a', 'employee_id': 'emp-75f8934f-cfb9-4c9f-a759-bdfe942f15db', 'c': 2}
```

### 3）新增样本有效性

- 同人同租户跨项目条目存在：
  - `emp-7417237e-2f30-4268-807f-88eaaf951bf8`：
    - `project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`
    - `project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`
  - `emp-75f8934f-cfb9-4c9f-a759-bdfe942f15db`：
    - `project-e84e06d4-f014-4326-abcd-e6d9aea6ff95`
    - `project-65258742-8ba3-42a8-b36f-dbe78d1ab9cd`
- 运行态最小检查：新 run 已触发真实 API 聚合前两步，`step_assignments` 已出现，满足 C1/C2 样本先决条件。

## 结论

- C0 前置样本阻塞解除，可继续进入 C1（scope/key 规范）与 C2（跨项目切换隔离）核验。
- 未改运行契约与前端；未发起外网调用；未提交代码。

## 递交

- Next Seat：`系统交付席`（进入 C1/C2）

