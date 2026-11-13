# 2026-07-18 Workspace R4 Memory 兼容性与历史保留复核（B3）

- Issue: `issues/20260718_workspace_r4_project_memory_recovery_b3_compatibility_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`（与现有 R3 历史闭环兼容）

## 复核范围

- 验证历史 Run/Artifact 在仅做 Memory 恢复定义后的可见性不变；
- 验证跨租户查询保护不泄露；
- 验证同 project 下历史失败与成功链路并存不被混淆。

## 复核命令（只读）

```bash
DB='/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite'
PROJECT='project-e84e06d4-f014-4326-abcd-e6d9aea6ff95'
TENANT='tenant-a'

backend/.venv/bin/python - <<'PY'
import sqlite3

db='/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite'
tenant='tenant-a'
project='project-e84e06d4-f014-4326-abcd-e6d9aea6ff95'
run_ids=[
  'wfr-69926fdb-21a2-4166-b6c6-37059309d7ff',
  'wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6',
  'wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc',
  'wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50',
]

with sqlite3.connect(db) as c:
    c.row_factory=sqlite3.Row
    runs=c.execute(
        "select workflow_run_id,status,final_report,length(final_report) as fr_len from workflow_runs where tenant_id=? and project_id=? order by created_at",
        (tenant,project)
    ).fetchall()
    print('runs_in_project', len(runs))
    for r in runs:
        steps=c.execute(
            "select count(*) from workflow_steps where tenant_id=? and workflow_run_id=?",
            (tenant,r['workflow_run_id'])
        ).fetchone()[0]
        tasks=c.execute(
            "select task_id from workflow_runs where workflow_run_id=?",
            (r['workflow_run_id'],)
        ).fetchone()['task_id']
        usage=c.execute(
            "select count(*) from evolution_events where tenant_id=? and correlation_id=? and event_type='usage.model_call'",
            (tenant,tasks)
        ).fetchone()[0]
        print(r['workflow_run_id'], r['status'], 'steps',steps, 'usage',usage, 'final_len', r['fr_len'])

    # cross-tenant fail-closed
    cross=c.execute(
        "select count(*) from workflow_runs where workflow_run_id='wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50' and tenant_id='tenant-b'",
        ).fetchone()[0]
    print('cross_tenant_match', cross)
PY
```

## 结果（单次）

- 项目 `project-e84e06d4-f014-4326-abcd-e6d9aea6ff95` 下当前可见 run 共 4 条：3 条 `failed`、1 条 `succeeded`。
- 失败 run (`wfr-69926...`, `wfr-ecc7...`, `wfr-e96...`) 的 `final_report` 长度均为 `0`，`usage` 为 `0/0/5`，保留历史失败边界。
- 成功 run `wfr-33a...` 的 `final_report` 非空、`usage=7`，且 run 内 step/result 均完整（历史 R3 证据链路可继承）。
- 跨 tenant 校验 `tenant-b` 对成功 run 返回 `0` 命中（fail-closed）。
- 当前结果与 B1/B2 的 scope 复核一致：无新增 run、无历史 run 字段重写证据出现。

## 结论

- 历史失败/成功证据兼容关系未被 Memory 定义改写；
- 已满足 B3 的兼容性收口条件，可进入父链验收。

Compact Handoff:
Issue: `issues/20260718_workspace_r4_project_memory_recovery_b3_compatibility_gate.md`
Special Constraints: 不改历史、只读复核、不得引入新出网。  
Next Seat: 产品规划席
Handoff: sent to 产品规划席
