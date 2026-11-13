# Curis Workspace — AI Task Executor MVP 图集总览

## 这是什么
Curis Workspace 的终极目标是面向个人创业者的 **AI 公司系统**（用户扮演 CEO）。当前上线范围是它的第一块基石 **AI Task Executor MVP**：一个 **受控自演进的 AI 操作系统内核**（Controlled Self-Evolving AI OS Kernel，Tool System v1.8）。用户提交任务 → 自动生成工作流 → AI 员工协调工具执行 → 记录 trace/学习 → 元开发自检 → 演进治理（稳定性优先，可决定「不演进」）。技术栈：FastAPI + SQLite + Next.js。

## 目前进度
- 已走到 **v0.1 本地/Demo 发布**（2026-07-06 关闭）。
- Sprint 0–4 全部交付并验收：执行内核、统一操作台、多入口 UI、中文控制台、Tool System v1.6 元开发、v1.8 受控自演进内核。
- 后端 41 个回归测试全绿；质量运行席用真实本地 FastAPI smoke 验证 health / 创建 / 历史接口（无 Mock / simulation）。

## 开发重点 / 难点
- **重点**：在 gate 约束下把「执行闭环 + 学习闭环 + 受控演进闭环」三层都跑通，并预留 L0–L6 框架避免返工。
- **难点**：① 严格 gate / 禁止范围（无 ROI、无 Employee CRUD、无多 Agent、无复杂 UI、无 Mock）下的增量交付；② 低 Token 五席位角色协作工作流；③ 演进治理的稳定性优先与 Architecture Lock；④ 当前为纯本地/Demo，无外部服务。

## 图集（8 张）
见 `curis-architecture-diagrams.html`：
1. 产品功能结构图（L0–L6 分层 + MVP 能力域）
2. 信息/数据结构图（Task 聚合根 + SQLite 19 类表 ER）
3. 产品架构图（分层 + 容器 + 执行闭环）
4. 业务流程泳道图（用户/前端/Orchestrator/AI员工/工具/学习演进/存储）
5. 页面流程图（操作台：输入→历史→详情多 tab）
6. 状态机图（Task：INIT→CREATED→RUNNING→EXECUTING→COMPLETED/FAILED→ADAPTING）
7. 原型图（统一任务操作台 wireframe）
8. 交互说明图（前端 ↔ 后端 API 时序）

## 来源
AGENTS.md / README.md / PROJECT_STATUS.md / TASKS.md / knowledge/（003_Architecture、004_Workflow、CURRENT_CONTEXT、ROLE_PROFILES）/ docs/product/prd.md / docs/sprints/ / backend/app/* / frontend/app/page.js
