# EvoFlow vs Curis 竞品对比分析报告

> 研究日期：2026-08-04（初版）；2026-08-04（独立复核）
> 研究对象：EvovexAI/EvoFlow（GitHub: https://github.com/EvovexAI/EvoFlow；官网：https://www.evovexai.com）
> 方法：主理人齐活林侦察 EvoFlow 事实（README + 官网 + 搜索交叉验证），产品经理许清楚（研究模式）产出对比分析
> 复核：2026-08-04 对照 GitHub README 独立复核（`docs/plan/evoflow-reuse-repo-mapping.md` §竞品复核），核心事实全部确认，3 处遗漏 + 1 处小偏差已在本版修正
> 许可证红线：EvoFlow 源码未公开，受 Evovex AI Non-Commercial License 1.0 约束，商业使用需书面授权 → 本报告仅借鉴架构思想，不含任何代码复制

---

## 1. 执行摘要（TL;DR）
- EvoFlow 是面向「长期自主软件工作」的**原生 Agent 运行时 + 桌面控制平面**（规划/分解/执行/恢复/可观测一体化）；Curis 是面向一人公司的 **AI 公司操作系统**，核心是全自动任务流（目标→规划→任务图→队列→调度→执行→验收→返工→完成）与可替换能力层。
- 两者在「规划先行 + 任务图 + 多 Agent + 可恢复编排」理念高度重合，但 Curis 的「员工=动态调用能力的岗位」比 EvoFlow「固定角色子 Agent」在抽象上更先进，复用建议中**不得回退**此原则。
- EvoFlow 在工程实现（中间件链、检查点、可观测、桌面壳）更成熟，是 Curis 当前「前端仅 UI 壳 + 后端 7 能力」阶段值得借鉴的成熟范式。
- 结论：以「思想/架构层借鉴」为主，严禁代码或专有术语字面复制（许可证 + 商标红线）。

## 2. 产品定位对比

| 维度 | EvoFlow | Curis |
|---|---|---|
| 定位 | 长期自主软件工作的原生 Agent 运行时 + 控制平面 | 一人公司自动任务与工作流系统（AI Company OS） |
| 目标用户 | 需要长任务/多 Agent 协作的开发者、团队 | 创始人/CEO（第一位 AI 员工 = 目标助理） |
| 核心隐喻 | Agent Teams + Supervisor 总控 | 公司→部门→项目→员工（组织运行层） |
| 交付物 | artifacts + Markdown 摘要 + 可选 IM 推送 | 任务流自动闭环（accept/rework/complete） |
| 许可证 | Evovex AI Non-Commercial 1.0（源码未公开，商用需授权） | 自有项目，ADR-0017 冻结商业化相关 |

## 3. 架构与技术栈对比

| 维度 | EvoFlow | Curis |
|---|---|---|
| 运行时 | LangGraph（图编排）+ LangChain | 自研后端（7 项能力 + 能力路由降级），无图编排 |
| 前端/控制平面 | EvoPanel（Tauri v2 + React）桌面壳 | 极简 6 步入口；CEO Office UI V2（47 页 Next.js 壳，未接后端） |
| 网关 | FastAPI Gateway（:8001，模型/记忆/技能/MCP/渠道） | 未独立网关，能力路由内聚于后端 |
| 协议 | MCP（已用）+ ACP（实验） | MCP 属能力层可替换组件之一 |
| 沙箱 | 本地 / Docker / k3s，每线程隔离 /mnt/user-data | 未显式实现沙箱隔离 |
| 状态持久化 | 线程状态 + 子任务进度检查点，可恢复 | data/curis.sqlite；业务生命周期状态机 |

## 4. 核心机制逐项对比

**4.1 规划与确认**：EvoFlow 由 Supervisor 在副作用前澄清意图、`plan()` 产出可审阅计划（绑定 `boundTaskId`）；Curis 运行层含「规划→任务图」但无显式确认门 + ID 溯源。
**4.2 多智能体协作**：EvoFlow 内置 general/bash 子 Agent + 自定义 Agent（SOUL/身份、模型、工具白名单）+ 预设团队（project team: architect/plan/implement/review/QA）；**每轮 ≤3 并发、15min 超时**（已确认）；Curis「员工=动态能力岗位」，按岗位临时组装能力，更灵活但缺并发上限治理。⚠️复核修正：EvoFlow 的预设团队是「recommended pattern，非硬编码」，自定义 agent 可配 SOUL——并非完全「固定角色」；Curis 抽象仍更先进，但对比表述需准确。
**4.3 工具与技能暴露**：EvoFlow 冷启动只挂核心+检索，按需挂载技能/MCP（50+ SKILL.md 白名单），PlanGuardMiddleware 在规划期过滤副作用工具（中间件链第 9 段）；Curis 已有「能力路由降级」，精神相似但无 PlanGuard 式阶段过滤。
**4.4 记忆与检查点**：EvoFlow LLM 驱动记忆提取（debounced atomic 写入）+ 线程状态/子任务进度持久化检查点可恢复；Curis 暂无显式记忆抽取机制。
**4.5 长任务恢复**：EvoFlow 支持暂停/恢复/取消/失败重试/部分重规划；另有 **Goal mode**（独立线程运行 + 完成推 Markdown 摘要到 IM）；Curis 有「返工」业务态但缺技术层检查点支撑。
**4.6 可观测性**：EvoFlow Agent Trace 视图（token 明细含缓存命中/写入）+ 子任务 DAG 可视化；Curis CEO Office 暂无 runtime trace。
**4.7 IM 与交付**：EvoFlow 微信/飞书已可用（Slack/Telegram planned），完成推摘要；Curis 聚焦内部闭环交付，IM 非当前阶段重点。
**4.8 智能员工（复核补充）**：EvoFlow 有 **Smart Employees** 概念（值勤台 duty desk、审批 approvals、名册 roster）+ Agents 页「角色配置与 hire 入口」——与 Curis「员工」概念存在概念重叠，值得对比（EvoFlow 员工偏预设角色 + 审批，Curis 员工=动态能力岗位）；原报告遗漏此节，复核后补入。

## 4A. 复核确认清单（2026-08-04 对照 GitHub README）

| 竞品分析声明 | README 依据 | 复核结论 |
|---|---|---|
| 原生 Agent Runtime + 桌面控制平面 | "A native Agent Runtime and Control Plane for long-running autonomous software work" | ✅ 准确 |
| LangGraph + LangChain | "LangGraph-based lead agent" / "built on LangGraph"（LangChain 在 Acknowledgements） | ✅ 准确 |
| EvoPanel = Tauri v2 + React | "EvoPanel (Tauri v2 + React)"，端口 1420 | ✅ 准确 |
| FastAPI Gateway :8001 | "Gateway (FastAPI · port 8001)" | ✅ 准确 |
| MCP 已用 + ACP 实验 | MCP 广泛使用；ACP "experimental / not yet verified"（Claude Code / Codex / Trae / CodeBuddy 适配器均为 planned，未验证端到端） | ✅ 准确（可补：适配器清单） |
| Supervisor + plan() + boundTaskId | "Supervisor clarifies intent, calls plan()…bound to a boundTaskId for traceability" | ✅ 准确 |
| PlanGuard 规划期过滤副作用工具 | 中间件链第 9 段 "PlanGuardMiddleware - filter side-effectful tool calls during planning phases" | ✅ 准确 |
| 中间件链 ~10 段 | 10 段：ThreadData→Uploads→Sandbox→Summarization→TodoList→Title→Memory→ViewImage→PlanGuard→Clarification | ✅ 准确（可补全名） |
| 检查点 + 暂停/恢复/取消/重试/部分重规划 | "thread state and subtask progress are persisted so runs can resume"；"pause / resume / cancel, retry on failure, and partial re-planning" | ✅ 准确 |
| Agent Trace token 明细含缓存命中/写入 | "per-request token usage (including cache hit/write breakdown)" | ✅ 准确 |
| ≤3 并发 / 15min 超时 | "Up to 3 subagents run concurrently per turn with a 15-minute timeout" | ✅ 准确 |
| 50+ SKILL.md 白名单 | "SKILL.md skill packages (50+ public skills) loaded by whitelist" | ✅ 准确 |
| 微信/飞书 IM 可用 | "IM Channel (WeChat · Feishu available; Slack · Telegram planned)" | ✅ 准确 |
| 沙箱 local/Docker/k3s + /mnt/user-data | "virtual path translation (/mnt/user-data/...)" + "local filesystem, Docker/container, and a k3s Provisioner" | ✅ 准确 |
| 源码未公开 + Non-Commercial 1.0 | "source code is not yet publicly released"；"Evovex AI Non-Commercial License 1.0…commercial use requires written authorization" | ✅ 准确 |
| 工程基线 | README Acknowledgements 提到 DeerFlow（MIT）为 early engineering baseline | ➕ 补充（原报告未提） |
| 端口拓扑 | Nginx 2026 / LangGraph Server 2024 / Gateway 8001 / EvoPanel 1420 / Provisioner 8002 | ➕ 补充 |

## 5. 关键差异总结（总表）

| 维度 | 谁更强 / 互补 | 说明 |
|---|---|---|
| 规划 + 溯源 | EvoFlow | boundTaskId + 确认门，Curis 可借鉴 |
| 多 Agent 模型 | Curis（概念更先进） | 动态岗位 > 固定角色，不得回退 |
| 工具渐进暴露 | EvoFlow（更成型） | Curis 已有降级，缺 PlanGuard |
| 检查点/恢复 | EvoFlow | 技术层成熟，Curis 仅业务态 |
| 可观测 | EvoFlow | Trace + DAG，Curis 待补 |
| 桌面壳 | EvoFlow | Tauri；Curis Desktop First 可参考 |
| 能力可替换 | 互补 | 双方皆支持，Curis 原则更坚定 |

## 6. 对 Curis 的可复用点（按落地价值排序）

1. **工具渐进暴露 / PlanGuard**（P0，不触红线）：EvoFlow 冷启动挂核心、规划期过滤副作用工具。→ Curis 已有能力路由降级。建议：在路由层增设「阶段门」——规划态仅暴露只读/检索能力，执行态再放开写/命令能力，降低误操作与上下文膨胀。落点在 backend 能力路由，不新增端点。
2. **Supervisor 规划 + boundTaskId 溯源**（P0，不触红线）：EvoFlow 子任务带输入/输出/验收标准并绑定 ID。→ Curis 任务图无显式验收标准 + ID 溯源。建议：任务图节点增加「验收标准字段」与全局 taskId 绑定，使 accept/rework 有技术依据。纯 schema 层增强。
3. **长任务检查点 / Recovery**（P1，不触红线）：EvoFlow 检查点 + 暂停/恢复/部分重规划。→ Curis 仅有业务态返工。建议：在运行层为任务图执行增加持久化检查点，使「取消/续跑/局部重规划」可技术支撑，复用 sqlite 状态表即可。
4. **可观测 / Agent Trace**（P1，不触红线）：EvoFlow token 明细 + DAG 可视化。→ CEO Office 仅 UI 壳。建议：在已交付的 CEO Office UI 中预留 runtime trace 视图位（仅先定义数据结构，不接后端），匹配 Desktop First。
5. **中间件链执行管道**（P2，不触红线）：EvoFlow 10 段中间件（Sandbox/Summarization/Clarification…）。→ Curis 运行层尚无显式管道。建议：将现有能力路由/降级抽象为可插拔中间件链，未来扩展成本低；当前不必全抄。
6. **Agent Teams 并发模型**（P2，不触红线）：≤3 并发 + 超时。→ Curis 项目内并行调度待治理。建议：为任务队列增设并发上限与超时，避免资源抢占；与「员工=动态岗位」不冲突。
7. **桌面控制平面 EvoPanel (Tauri)**（P2，需评估）：→ Curis Desktop First 已定。建议：当前 CEO Office 用 Web 壳即可，Tauri 桌面壳可作为后续增强，非当前阶段必需，避免范围膨胀。
8. **技能/MCP 白名单市场**（P2，部分触红线）：50+ SKILL.md 白名单。→ Curis 能力层可替换。注意：ADR-0017 冻结「外部 Agent 生态/Marketplace」，故**仅借鉴白名单加载思想**，不建收费市场。

## 7. 风险与注意事项
- **许可证/IP**：EvoFlow 源码未公开、非 OSI 开源，受 Non-Commercial 1.0 约束；**仅借鉴思想，严禁复制代码或架构文件**；避免字面借鉴 EvoFlow/EvoPanel/Supervisor 等专有术语（商标 + 混淆风险），报告中已使用中性表述。
- **命名空间碰撞**：本次对象仅为 EvovexAI/EvoFlow；学术 "EvoFlow: Evolving Agentic Workflows"(arXiv 2502.07373) 与 "Micdiane/EvoFlow" 为同名异物，已澄清以免误导。
- **Curis 红线**：所有复用建议不得违反 ADR-0017（不引入 Employee CRUD、不接真实计费/实例化、不建收费 Marketplace、不引入向量库）；「员工=动态能力岗位」优于 EvoFlow 固定子 Agent，**任何建议不得使其回退**。
- **范围守卫**：Curis 当前后端仅 7 能力、前端仅 UI 壳（CEO Office 未接后端）。复用建议须匹配阶段，优先 P0 两项（阶段门 + 验收标准/ID 溯源），不超前膨胀到桌面壳/完整中间件链。

## 8. 对 Curis 的下一步建议（按优先级）
1. **P0 - 能力路由增设「阶段门」**：规划态仅暴露只读/检索，执行态放开写能力（借鉴 PlanGuard），落地 backend 路由层，零新增端点。
2. **P0 - 任务图补「验收标准 + boundTaskId」**：为任务节点增加验收字段与全局 ID 绑定，支撑 accept/rework 技术判定。
3. **P1 - 运行层加持久化检查点**：基于 sqlite 为任务图执行增检查点，支持暂停/恢复/局部重规划。
4. **P1 - CEO Office 预留 runtime trace 视图位**：先定义 trace 数据结构与占位，不接后端，匹配 Desktop First。
5. **P2 - 白名单能力加载思想**：在不建收费市场前提下，将能力加载抽象为白名单模式，为能力层可替换加分。

（报告完。全部结论基于主理人已核实材料，未做额外网络抓取。）
