---
title: Phase-4.5 Admin Demo Polish · 执行步骤（Execution Steps）
priority: P0
phase: phase-4.5
owner: 主理人(Qi) 编排 / 工程师(Kou) 执行 / 产品经理(Xu) 验收
status: execution-plan
related_issue: issues/phase45_admin_demo_polish.md
constraint: 零核心能力变更、零治理边界改动、不新增复杂 Admin 页面
---

# Phase-4.5 Admin Demo Polish · 执行步骤

> 本文件是 `phase45_admin_demo_polish.md` 的**执行拆解**，由主理人齐活林编排。
> 所有步骤严守：不新增 API、不改 schema、不碰 tenant_private 写路径、不进入真实密钥托管（G2 范畴）、不新增复杂 Admin 页面。

## 执行原则

- **两层轻量改造**：① 可选演示数据种子（可重复加载）② 前端/文案呈现（复用既有只读接口）。
- **零回归风险**：每步完成后必须跑 `test_d5_*.py + test_d4_platform.py` 回归（基线 157 例），不退化方可合入。
- **可一键重现**：最终演示不依赖临场手动造数。

---

## Step 1 · 演示数据种子脚本（可选、隔离）

- **目标**：提供可重复加载的演示租户 / 员工 / usage_event 数据，覆盖 10 条链路所需。
- **改动文件**（新建，独立脚本，不进核心模块）：
  - `backend/scripts/seed_admin_demo.py`（经现有 `/api/platform/*` 写入，或直写 sqlite 演示库）
- **命令**：
  ```bash
  cd backend && ./.venv/bin/python scripts/seed_admin_demo.py --reset --tenant demo-tenant
  ```
- **验收**：脚本可幂等重跑；加载后演示租户含 ≥1 个员工、usage_event 含 official + tenant_private 两态样本。
- **不碰边界**：不建表、不改 schema、不改 `/api/platform/*` 实现；`credential_ref`/`config_ref` 维持 `env:DEMO_REF` 类占位，不写真实密钥。

## Step 2 · Admin 用量页演示呈现（复用只读接口）

- **目标**：默认载入演示租户，official / tenant_private 用量对比卡片 + usage_event 员工归因时间线。
- **改动文件**（前端，最小呈现；不新增路由/页面）：
  - `frontend/app/platform/UsageProjectionPanel.js`（既有文件，扩展演示默认租户与对比卡片）
- **复用接口**：`/api/platform/usage`（7 维）、`/api/catalog/*`、`/api/platform/audit`，无新增/修改。
- **命令**（本地起前端联调）：
  ```bash
  cd frontend && npm run dev   # 人工核对 10 条链路观感
  ```
- **验收**：演示租户用量页一键呈现 official/tenant_private 对比与员工归因；无新 API 调用。
- **不碰边界**：仅读接口编排，不改后端；不新增复杂 Admin 页面。

## Step 3 · 三处易误解点统一澄清文案

- **目标**：消除评审误读——marketplace 占位、estimated_cost 为演示估算、credential_ref 为演示托管。
- **改动文件**（前端文案 / 可选 markdown）：
  - `frontend/app/platform/UsageProjectionPanel.js`（字段旁注）
  - 可选 `docs/demo/admin-governance-boundary.md`（对外治理边界说明）
- **澄清内容**：
  - `estimated_cost` → 标注「演示估算，非权威计费」
  - `marketplace` 维度 → 标注「治理源预留，未上线」
  - `credential_ref` → 标注「演示托管（不透明指针），真实密钥托管见 G2 Gate」
- **验收**：三处均有统一澄清文案，演示中无需口头解释。
- **不碰边界**：纯文案，不改任何逻辑/数据。

## Step 4 · 对外治理边界说明（演示辅助）

- **目标**：一份简洁的 Admin 治理边界说明，供评审/对外展示引用。
- **改动文件**（新建文档，非代码）：
  - `docs/demo/admin-governance-boundary.md`
- **内容**：10 条链路状态表（稳定/需解释）、三态治理边界、Admin 只读观测 private 的说明、G2/Billing/Marketplace 路线占位。
- **验收**：文档与 `phase45_admin_demo_polish.md` 验收标准第 4 条一致。

## Step 5 · 演示脚本与叙事（一键重现）

- **目标**：一键加载种子并重现全部 10 条链路 + 演示叙事文案。
- **改动文件**：
  - `docs/demo/admin-demo-runbook.md`（叙事 + 步骤 + 截图指引）
  - 可选：演示启动 shell 封装（调用 Step1 种子 + 启动前后端）
- **验收**：依 runbook 可在一台干净环境重现 10 条链路演示，无需临场手动造数。

---

## 测试与回归（每步必跑）

```bash
cd backend
./.venv/bin/python -m pytest tests/test_d5_*.py tests/test_d4_platform.py -q
# 期望：157 passed（不退化）
# 新增：1–2 个演示数据加载冒烟测试（种子可加载、10 条链路可重现）
```

## 合入门槛（主理人 gate）

- [ ] 157 例 Admin 相关测试零退化
- [ ] 演示数据加载冒烟测试通过
- [ ] 演示脚本可一键重现 10 条链路
- [ ] marketplace / estimated_cost / credential_ref 三处统一澄清文案就位
- [ ] 未触碰任何禁止区（核心能力 / 治理边界 / tenant_private 写 / 真实密钥托管）

## 关联

- Issue 主体：`issues/phase45_admin_demo_polish.md`（P0，Admin 专属）
- 通用 Demo Polish：`issues/phase45_demo_polish.md`（P2，并行安全）
- 真实密钥托管路线：`issues/phase5_g2_credential_vault_gate.md` + `issues/phase5_g2_security_review_kickoff.md`

---

*主理人齐活林 编排；工程师寇豆码执行、产品经理许清楚验收。*
