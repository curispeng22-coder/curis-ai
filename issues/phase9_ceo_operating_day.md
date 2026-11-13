# Phase-9 CEO Operating Day

Status: Review

Owner Seat: 产品规划席（slice 验收）/ 系统交付席（实现）

Source contracts:

- `docs/00_Context/CURRENT_STATE.md`（Completed Capabilities 基线）
- `docs/02_Architecture/Curis_System_Architecture.md`
- `docs/plan/ceo-operating-day-design.md`（本 Issue 的设计）

## Background

原型评审（2026-08-04）确认后端接入缺口的第二档：`ceo-desk`（Brief / Matters /
Timeline / Company Pulse / Handoffs 六段）与 `operating`（脉搏 / 异常 / 机会）
两页在后端只有 Company / Project / Task 等实体明细，**没有「CEO 经营日」聚合端点，
也没有经营指标事实源**。这是产品主轴「CEO 决策」入口，v1 可立项，不触碰商业化红线。

## Goal

- 提供租户内可计算、可持久化的**经营指标事实源**（`business_metrics`），
  从现有实体（projects / tasks / artifacts / ai_usage_records / workflow_runs /
  employee_instances）聚合，指标带周期（day/week/month）。
- 提供 **CEO 经营日聚合端点** `GET /api/workspace/ceo/operating-day`，
  返回 Brief / Matters / Timeline / Pulse / Handoffs 五段结构，
  供 `ceo-desk` / `operating` 原型页面接真实数据。

## Scope

- 新增 `business_metrics` 表（幂等迁移）+ 唯一索引（tenant, company, period, metric_key）。
- `BusinessMetricService.compute(company_id, period)`：从现有实体聚合指标并 upsert。
- `CeoOperatingDayService.build(company_id)`：matters 推导（受阻任务→风险、
  完成率低→关注）、timeline（近期 tasks/workflow_runs/artifacts）、
  pulse（指标 + 简单趋势）、brief（模板拼装摘要，v1 不调模型）。
- 端点 `GET /api/workspace/ceo/operating-day`（tenant 作用域）。
- 测试：指标聚合正确性、matters 推导、周期 upsert 幂等、端点结构。

## Non-goals

- 不做决策室 / 会议 / 财务 / 日历（蓝图级未立项）。
- 不做经营指标的人工录入 / 编辑（仅聚合计算；manual source 字段预留）。
- 不调 AI 生成 brief（v1 模板拼装，模型接入留后）。
- 不触碰 payment / billing / Marketplace。

## Acceptance

- 全量回归通过（基线 1192 passed 不回退）。
- `operating-day` 在空公司 / 有数据公司两种情况下均返回完整五段结构。
- `business_metrics` 周期 upsert 幂等，重复 compute 不产生重复行。
