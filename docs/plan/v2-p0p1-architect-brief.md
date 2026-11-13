# V2 P0/P1 架构师输入包（Architect Brief）

> 主理人齐活林预组装。用途：Agent 框架恢复后，直接将本文件作为上下文喂给架构师高见远，产出 `docs/plan/v2-p0p1-impl-design.md`（实现设计 + 任务分解）。
> 本文件**不是架构设计本身**，仅是协调前置的上下文包，不替代成员专业产出。

## 一、任务背景与已批准范围

- 运营协定 v2 下 AI 资产工厂自主运行。
- 总控裁定：**P0 + P1 允许自主推进**（ADR-0017 预授权方向内，无需逐项审批）。
- **下列四项必须暂停、等待后续 L2 Gate，本次绝不可触碰**：
  1. 新商业包（内容/商业公司产品线补全）
  2. Marketplace
  3. 收费体系（`cmcf_*` 解冻/计费/配额）
  4. 外部 Agent 生态
- 红线（铁律，全程禁止）：不碰 payment/invoice/真实计费、Employee CRUD 端点、外部凭证接入、真实 instantiation（建真实公司实例）、多 Agent、向量库、复杂 UI。
- 本次纯属「已批准方向内的官方资产内容填充 + 资产体系机制完善」，**不引入新资产类型**（形象仅作 `pt_*` 字段扩展，规避 L2 #7）。

## 二、必读上下文文档（已在磁盘，请实地读取，不要凭空设计）

- V2 复盘报告：`docs/plan/ai-company-asset-factory-v2-roadmap-review.md`（含 P0/P1/P2 划分、§6 资产完成度七准则——直接采纳为验收闸门）
- 真实内容来源（P0-1/2/3 要 seed 的数据全在这些文档里，零编造）：
  - `docs/research/domain/official-skill-catalog-v1.md` + `docs/contracts/official-skill-catalog-contract.md`：105 个 Skill 全量目录，含 ai_rd 包（Pack A，约 52 个 `skl_ai_rd_*`）的真实 id / 分类 / 定义。
  - `docs/plan/tool-catalog-official-plan.md`：46 个官方 Tool，含 ai_rd 包（Pack A，约 30 个 `tl_ai_rd_*`）真实 id / 域 / 定义。
  - `docs/plan/workflow-official-content-plan.md`：36 个官方 Workflow（`wl_*`），含 ai_rd 包（16 个）及其指向的 `wt_*` 容器定义。
  - `docs/plan/employee-persona-system-plan.md`：Persona 五元模型，形象/性格/沟通/汇报字段设计（P1-1 依据）。
  - `docs/plan/dashboard-official-content-plan.md`：8 个看板 `dtpl_*`，widget 数据占位（P1-4 依据）。
- 现役代码与契约（实现落点）：`backend/app/database.py`（seed 函数、`skill_templates`/`tool_templates`/`workflow_templates`/`persona_templates`/`employee_templates`/`dashboard_template` 表与字段）、`docs/contracts/` 下各资产契约。

## 三、已核验空壳事实（主理人 Grep 确认，勿再重复质疑）

- `skill_templates` 仅 3 个 `official.skill.*` 通用行、`skl_ai_rd_*` 零行。
- `tool_templates` 整表未 seed，但 `et_*`/`ccp_*` 大量引用 `tl_ai_rd_*` → 空壳。
- `workflow_templates` 仅 `official.workflow.software_rnd_sop`，36 条 `wl_*` 指向的 `wt_*` 容器缺失 → 悬空。

## 四、设计任务要求（产出落盘 `docs/plan/v2-p0p1-impl-design.md`）

请一次性输出设计文档，包含：

1. **实现方案 + 框架选型**：确认沿用现役 FastAPI + SQLite + Pydantic 技术栈，无新框架、无 UI。
2. **P0-4 资产完成度标准（验收闸门）**：把 V2 review §6 的七准则正式化为「每个资产填充任务完成的定义 + 一条可执行的校验清单」（可落为测试断言方向）。
3. **文件列表及相对路径**：本次改动涉及的所有文件，标注新增/修改。
4. **数据结构和接口（字段变更）**：
   - P1-1：`persona_templates` 加「形象」字段（头像/昵称/身份描述）+ `employee_templates` 加 `persona_overrides`（JSON，覆盖性格/沟通/汇报）；明确不立新表、不立新资产类。
   - P1-2：Skill 体系四件套——`skill_templates` 的生命周期状态机（draft→review→active→deprecated）、版本策略、分类字段（对齐 35 类目）、默认绑定规则（仅做出厂装配清单，不自动改权限）。
   - 其余 P0/P1 主要是 seed 数据，不新增结构（除非必须）。
5. **程序调用流程（时序图）**：seed 执行顺序、引用闭环校验顺序。
6. **任务列表**（有序、含依赖、用 T 编号）：
   - T1 = P0-4 资产完成度标准落地（设计文档 + 验收清单，作为后续闸门）
   - T2 = P0-1 补 `skl_ai_rd_*`（ai_rd 包全部，约 52 个）真实内容到 `skill_templates`
   - T3 = P0-2 补 `tl_ai_rd_*`（ai_rd 包全部，约 30 个）真实内容到 `tool_templates`
   - T4 = P0-3 补 `wt_*` 工作流容器 + P1-3 把 36 条 `wl_*` 的 `workflow_template_ref` 对齐到真实 `wt_*`
   - T5 = P1-1 `persona_templates` 形象字段 + `employee_templates` `persona_overrides`
   - T6 = P1-2 Skill 四件套（生命周期/版本/分类/默认绑定）
   - T7 = P1-4 Dashboard widget 数据真实化（仅 ai_rd 看板，不碰内容/商业线——那属暂停项）
   - T8 = 验收：基于 P0-4 标准写/补校验（可并入测试）
   - 说明各 T 依赖（如 T2/T3/T4 依赖既有契约字段已存在；T5/T6 是 schema 变更须先于对应 seed；T8 依赖全部）。
7. **依赖包列表**：应为空或极少（不引入新依赖）。
8. **共享知识（跨文件约定）**：seed 幂等策略（`INSERT OR IGNORE` 还是 `UPSERT`？现有库已存在行如何更新？给出明确策略，避免破坏既有数据）、id 命名统一、引用闭环规则。
9. **待明确事项 / 风险**：列出需主理人/总控拍板的点（如：P1-2 默认绑定若未来涉及「员工自动获得能力」是否需重新评估 L2 #5/#6；ai_rd 包 Skill 是否全量 52 个还是先 ≥6 个最小可用——给推荐）。

## 五、约束

- 设计必须能直接交给工程师（寇豆码）批量落地，依赖清晰、文件明确。
- 严禁任何涉及暂停四项（新商业包/Marketplace/收费/外部Agent）或红线的设计。
- 设计文档本身是内部技术交付，允许必要的结构化（表格/Mermaid/JSON schema）。
- 落盘设计文档后，在回复中给出 TL;DR + 任务列表摘要。
