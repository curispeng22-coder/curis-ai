---
title: Phase-4.5 Admin Demo Polish（Admin 专属演示打磨）
priority: P0
phase: phase-4.5
owner: 产品经理(Xu) / 主理人(Qi)
status: draft
---

# Phase-4.5 Admin Demo Polish（Admin 专属演示打磨）

## 背景
Phase-4 Demo Freeze 已完成，Admin Platform 核心治理链路（official 能力目录、`/api/catalog/*` Workspace 只读、`/api/platform/*` Admin-only 写、usage_event 7 维查询、tenant_private 隔离、AuditEvent 白名单）均真实可用——**157 例 Admin 相关测试全绿**（test_d5_*.py + test_d4_platform.py）。但当前 Admin 侧演示仍依赖临场造数，且以下三处易引发评审误读：

1. `marketplace` 治理源查询恒为空（仅 schema 占位、0 业务引用）；
2. `estimated_cost` 为 env 单价估算、非权威计费；
3. `credential_ref` 仅为演示托管（不透明指针，无真实 KMS）。

本 issue 在**不改动任何后端核心能力与治理边界**前提下，提升 Admin 侧演示观感与可重复性。

## 目标
通过"可选 Admin 演示数据种子 + Admin 前端/文案呈现"两层轻量改造，使 Admin 10 条演示链路观感一致、可一键重现、可对外展示；对外叙事统一（澄清 marketplace 占位、estimated_cost 为演示估算、credential_ref 为演示托管）。

## 不做范围
- 不新增 API、不修改 schema、不实现新功能
- 不碰 tenant_private 写路径、不改 usage_event 写入
- 不进入真实密钥托管（G2 Gate 范畴）
- 不新增复杂 Admin 页面（仅最小文案/筛选呈现）

## 数据模型影响
无 schema 变更；可选 Admin 演示种子（seed）数据，仅用于演示租户 / 员工 / usage_event 填充（经现有 `/api/platform/*` 写入或本地脚本）。

## API 影响
复用 `/api/platform/usage`（7 维）、`/api/catalog/*`、`/api/platform/audit`；仅在前端 / 演示脚本层编排，无新增或修改接口。

## UI 影响
- Admin 用量页：默认载入演示租户，official / tenant_private 用量对比卡片、usage_event 员工归因时间线
- 文案澄清：estimated_cost 标注"演示估算，非权威计费"；marketplace 维度标注"治理源预留，未上线"
- 可选：Admin 演示脚本一键加载种子并重现 10 条链路

## 安全边界
不变（仍 `_require_platform_admin` 401 + fail-closed）；演示种子不引入任何权限降级；`credential_ref` / `config_ref` 维持 `env:DEMO_REF` 类占位，不写入真实密钥。

## 测试要求
- 回归 157 例 Admin 相关测试基线（test_d5_*.py + test_d4_platform.py）不退化
- 新增 1–2 个演示数据加载冒烟测试（种子可加载、10 条链路可重现）

## 验收标准
1. 157 例 Admin 相关测试零退化
2. 演示数据加载冒烟测试通过
3. Admin 演示脚本可一键加载种子并重现全部 10 条链路
4. 对外演示无需临场手动造数；marketplace / estimated_cost / credential_ref 三处均有统一澄清文案

## 关联
- 通用 Demo Polish 见 `issues/phase45_demo_polish.md`（标 P2，并行安全）
- 本 Admin 专属草案将优先级在 Admin 演示视角**提升为 P0**：直接支撑 Phase-4.5 评审通过率，零技术风险
