# CEO 经营日聚合与经营指标事实源（Phase-9）设计

> 状态：Draft（随 Issue `phase9_ceo_operating_day` 评审）
> 日期：2026-08-04
> 范围：后端（指标事实源 + 聚合端点）；供原型 `ceo-desk` / `operating` 两页接真实数据。

## 1. 背景与目标

后端接入评估（2026-08-04）：`ceo-desk`（Brief / Matters / Timeline / Pulse / Handoffs）
与 `operating`（脉搏 / 异常 / 机会）是产品主轴「CEO 决策」入口，但后端只有实体明细，
无经营聚合端点、无指标事实源。本设计补齐该缺口，v1 最小闭环。

目标：

1. **指标事实源** `business_metrics`：租户内可计算、可持久化、带周期的经营指标，
   从现有实体聚合，供任何页面/端点复用。
2. **CEO 经营日聚合** `GET /api/workspace/ceo/operating-day`：一次返回五段结构，
   前端 `ceo-desk` 六段 / `operating` 三块可直接渲染。
3. 不调 AI（brief 模板拼装）、不碰商业化、不新建实体 CRUD。

## 2. 数据模型：business_metrics

```sql
create table if not exists business_metrics (
  metric_id    text primary key,
  tenant_id    text not null,
  company_id   text not null,
  period       text not null,   -- 'day:YYYY-MM-DD' | 'week:...' | 'month:...'
  metric_key   text not null,
  value        real not null,
  unit         text not null default '',
  source       text not null default 'aggregated',  -- aggregated | manual（预留）
  computed_at  text not null default current_timestamp,
  updated_at   text not null default current_timestamp
);
create unique index if not exists uq_business_metrics
  on business_metrics(tenant_id, company_id, period, metric_key);
```

- 周期粒度：day（默认）/ week / month，`compute` 一次只算一个周期。
- upsert 幂等：同 (tenant, company, period, metric_key) 覆盖更新。

## 3. 指标集（v1，全部聚合自现有实体）

| metric_key | 来源 | 单位 |
|---|---|---|
| active_projects | projects status='active' | 个 |
| tasks_total | tasks（公司项目内） | 个 |
| tasks_completed | tasks status='COMPLETED' | 个 |
| blocked_tasks | tasks status IN ('FAILED','BLOCKED') | 个 |
| task_completion_rate | completed / total | % |
| artifacts_count | artifacts（公司项目内） | 项 |
| employees_active | employee_instances enabled=1 | 人 |
| workflow_runs | workflow_runs | 次 |
| estimated_cost | ai_usage_records.cost 合计（未计费，仅估算） | USD |

聚合统一按 `company_id` 过滤（tenant 内）；任务/成果按 project.company_id 关联。

## 4. 聚合端点

`GET /api/workspace/ceo/operating-day?company_id=...&period=day:YYYY-MM-DD`

（company_id 缺省用租户默认公司；period 缺省取今天。）

```json
{
  "company_id": "...",
  "date": "2026-08-04",
  "brief": {
    "summary": "3 个项目活跃；任务完成率 62%；累计成果 5 项；员工 2 人；2 个任务受阻。",
    "generated_at": "..."
  },
  "matters": [
    { "level": "risk", "severity": "high", "metric_key": "blocked_tasks",
      "message": "2 个任务受阻，需要处理" }
  ],
  "timeline": [
    { "at": "...", "type": "task", "title": "...", "ref": "task-xxx" }
  ],
  "pulse": [
    { "metric_key": "task_completion_rate", "value": 0.62, "unit": "%",
      "trend": "up" }
  ],
  "handoffs": []
}
```

### matters 推导规则（v1 确定性规则，不调模型）

| 条件 | level | severity | message |
|---|---|---|---|
| blocked_tasks > 0 | risk | high | N 个任务受阻，需要处理 |
| tasks_total > 0 且 completion_rate < 0.3 | attention | medium | 任务完成率偏低（N%） |
| estimated_cost > 0 | attention | low | 本周期模型成本估算 $X |
| 均无异常 | info | low | 经营正常（active_projects 个项目活跃） |

### pulse 趋势（v1 简单）

与上一周期（period-1 天）对比：up / down / flat；无历史 → flat。

### brief（v1 模板拼装）

模板：「{active_projects} 个项目活跃；任务完成率 {rate}%；累计成果 {artifacts} 项；
员工 {employees} 人；{N} 个任务受阻。」无数据时输出「暂无经营数据，先创建你的第一个业务」。

## 5. 组件与文件

| 组件 | 文件 |
|---|---|
| 表迁移 `_migrate_business_metrics` | `backend/app/database.py` |
| `BusinessMetricService`（compute / read_period / latest_period） | `backend/app/business_metrics.py` |
| `CeoOperatingDayService`（build） | `backend/app/business_metrics.py` |
| 端点 + 依赖注入 | `backend/app/main.py` |
| 测试 | `backend/tests/test_ceo_operating_day.py` |

## 6. 安全与纪律

- 全部租户作用域（TenantContext），company 归属校验。
- `estimated_cost` 仅估算聚合，不做计费、不触碰 payment（与 CURRENT_STATE 红线一致）。
- 事件：`business.metrics_computed`（compute 后记录，脱敏）。
- 不调 AI、不新增 CRUD、不改既有表结构（仅新表）。

## 7. 测试策略

- 空公司：五段结构完整、brief 显示空态文案、matters 为 info。
- 有数据：造 project/task/artifact/usage → compute → 断言各指标值。
- 周期 upsert 幂等：同周期 compute 两次，行数不变、值更新。
- 端点：默认公司解析、period 参数、matters 推导、timeline 排序。

## 8. 待办

实现状态：**已实现并全量回归通过（1197 passed / 2 skipped / 0 failed，2026-08-04）**。

1. [x] `_migrate_business_metrics` 迁移
2. [x] `BusinessMetricService`（聚合 + upsert + 读）
3. [x] `CeoOperatingDayService`（matters / timeline / pulse / brief / handoffs）
4. [x] 端点 + 注入
5. [x] 测试 + 全量回归（`tests/test_ceo_operating_day.py` 5 用例）
6. [x] 文档同步（CURRENT_STATE / CHANGE_LOG）

实现要点（与 Draft 差异）：
- `ai_usage_records` 成本列是 `cost_amount`（非 `cost`）。
- 默认公司解析复用 `company_project_runtime.list_companies()`（惰性创建）。
- 测试注意：不设 `CURIS_D1_WORKSPACE_ROOT` env，避免 create_app 把
  `local_rd_toolset._WORKSPACE_ROOT_OVERRIDE` 残留成已删除临时目录，污染后续
  `test_local_rd_toolset` 系列（workspace_root_unavailable）。
