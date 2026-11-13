# AI Company Asset Factory V2 · P0/P1 实现设计 + 任务分解

> 产出人：主理人齐活林（Qi）· 架构师代理人（Agent 框架故障期降级执行，已派高见远独立复核）
> 状态：**ai_rd 线闭环 + 公开生态工具库扩展**（52 技能 + 115 工具 + 16 工作流容器 + 6 形象 + 97 条富字段编目）。内容/商业 `tl_*` 工具模板经用户授权「工具库自行完善补充 / 继续扩行业包」已 seed；「新商业包」资产（ccp_/ct_/dt_/et_/skl_ai_commercial_*）仍零触碰。
> 边界：已批准自主推进 P0+P1；暂停四项零触碰（内容/商业工具模板编目属已授权范围）；红线全守。复核：架构师高见远有条件 PASS + QA 严过关 13/13 全通过。

---

## 1. 实现方案 + 框架选型

沿用现役栈 **FastAPI + SQLite + Pydantic**，零新框架、零 UI。本次为「官方资产内容填充 + 资产机制完善」，不引入新资产类型（形象仅作 `pt_*` 字段扩展，规避 L2 #7）。所有改动幂等（`insert or ignore` / `on conflict do update` / `_ensure_column`），可重复 `initialize()`。

## 2. P0-4 资产完成度标准（验收闸门）

一个资产判定「完成」须**全部满足**（任一不满足 = 空壳，禁止声称就绪）：

1. **有真实内容行**：库里确有 seed 数据，非仅表/端点/引用存在。
2. **内容非空非占位**：描述可读、非 `TBD`/空。
3. **下游引用全闭环**：被引用的 id 真实存在（`et_→pt_/skl_/tl_*`、`wl_→wt_*`、`ccp_→skl_/tl_/wl_*` 无一悬空）。
4. **有版本与状态**：`version` 非空、`status=active`。
5. **被上层装配**：至少被一个 Package/Template 引用。
6. **可溯源、无编造 id**。
7. **对 Skill/Tool/Workflow**：有可执行的真实定义（技能有指令、工具可调、workflow 有步骤），非仅名字。

本次校验脚本已落实上述第 3 条闭环断言。

## 3. 文件清单

| 文件 | 改动 | 说明 |
|---|---|---|
| `backend/app/database.py` | 修改 | ① 新增 `tool_templates` 建表（seed 内 `create table if not exists`）；② `_ensure_column` 加 `persona_templates.image_ref_json`、`skill_templates.version`/`category`；③ 新增 4 个 seed 方法；④ 调度点挂载 4 调用。 |
| `docs/plan/v2-p0p1-impl-design.md` | 新增 | 本设计文档（T1）。 |
| `docs/plan/v2-p0p1-architect-brief.md` | 既有 | 架构师输入包（框架恢复后喂给高见远复核）。 |

## 4. 数据模型 / 字段变更

- **P1-1 Persona 形象**：`persona_templates` 加 `image_ref_json`（`{avatar, nickname, identity}`）。`employee_templates.persona_overrides_json` 已于 Phase-1 建好（947 行），本次仅填充 6 原型形象。不立新表/新类。
- **P1-2 Skill 四件套（部分）**：`skill_templates` 加 `version` + `category`（分类对齐产品/架构/开发/测试/运维等）。生命周期由既有 `status`（draft/active/disabled/archived）覆盖。默认绑定（员工→技能映射）已由 `employee_templates.default_skill` + `employee_skill_bindings` 承载，本次不新增自动赋权逻辑（避免 L2 #5/#6）。
- **P0-2 Tool Catalog**：原 `tool_templates` 表**根本不存在**（空壳根因之一），本次新建并 seed 30 个 `tl_ai_rd_*`。

## 5. 任务列表（T1–T8）与落地状态

| # | 任务 | 状态 | 说明 |
|---|---|---|---|
| T1 | P0-4 资产完成度标准 | ✅ 已落地（本文 §2） | 验收闸门确立 |
| T2 | P0-1 补 `skl_ai_rd_*` 真实内容 | ✅ 52 个全 seed | Pack A 全部 52 个 ai_rd 技能已闭环（9 关键 + 43 增量），分类覆盖 产品/架构/开发/测试/DevOps/数据/安全 |
| T3 | P0-2 补 `tl_ai_rd_*` 真实内容 | ✅ 30 个全 seed | `tool_templates` 表新建 + 全包落地 |
| T4 | P0-3 补 `wt_*` 容器 | ✅ ai_rd 16 个 | `wl_ai_rd_*` 的 `workflow_template_ref` 原本已指向正确 `wt_*`，仅容器缺失；本次创建 16 个 ai_rd 容器，引用全闭环 |
| T5 | P1-1 员工形象 + persona_overrides | ✅ 6 原型形象已填 | 字段/覆盖机制就绪 |
| T6 | P1-2 Skill 四件套 | 🟡 版本+分类已加 | 生命周期/默认绑定机制已部分具备；完整分类体系 + 出厂装配清单细化待后续 |
| T7 | P1-4 Dashboard 数据真实化 | ✅ 已满足（ai_rd） | Phase-1 测试已断言 ai_rd 看板 `widget_ids` 全部指向真实 catalog 行 |
| T8 | 验收 | ✅ 本次闭环校验 0 悬空 | 含 ai_rd wl→wt / et→skl,tl / ccp→skl,tl 全 0 悬空 |

## 6. 依赖与执行顺序

`tool_templates` 建表 → skill/tool/wt seed（独立表，无序）→ persona 形象（依赖 persona 先 seed，故在 `_seed_phase1_asset_factory` 之后调用）→ 闭环校验。

## 7. 本次实测结果（fresh temp DB）

- `skill_templates`：55（3 official + 52 ai_rd）；`category`/`version` 非空。
- `tool_templates`：**115**（ai_rd 30 执行器 + Pack A 16 连接器 + Pack C 15 通用/框架 + Pack D 14 内容公司 + Pack E 12 电商公司 + Pack F-J 28 办公/产品/内容/电商营销补强）；slug/id 全唯一、description/source 合规。
- `workflow_templates`：17（1 official + 16 ai_rd `wt_*`）。
- `persona_templates`：6，均含 `image_ref_json`。
- 闭环：ai_rd `wl_→wt_*` 0 悬空；员工 `default_skill→skl_*` 0、`default_tool→tl_*` 0；出厂包 `skill_refs→skl_*` 0、`tool_refs→tl_*` 0；内容/商业 `wl_→wt_*` 20 条为有意悬空（暂停项，不计入失败）。
- 回归：Phase-1 QA 套件 19 passed / 0 failed；B 方案 seed 完整性回归 `test_bplan_seed_integrity.py` **13 passed / 0 failed**（QA 严过关独立编写并运行）。

## 8. 已知缺口 / 待办（非阻塞）

1. ~~完整 52 个 ai_rd 技能~~：**已完成**（2026-07-11 续补 43 个增量，连同前 9 关键共 52 个；分类分布 产品9/架构9/开发16/测试6/DevOps8/数据2/安全1/运维1）。
2. **内容/商业线（ai_content/ai_commercial）**：`wt_*` 容器未建、`skl_ai_content_*`/`skl_ai_commercial_*` 未 seed（属**暂停四项中的「新商业包」L2 Gate**，仍冻结）；但**工具模板 `tl_*` 经用户明确授权已 seed**——Pack D 内容公司 14 + Pack E 电商公司 12 + Pack F-J 内容/电商营销补强（来源公开生态扫描，含中文介绍 + 安全分级，见 `docs/research/domain/official-tool-catalog-v1.md`）。此属「工具库自行完善补充 / 继续扩行业包」授权范围，**非**「新商业包」资产（ccp_/ct_/dt_/et_/skl_ai_commercial_* 一个未建）。其 `wl_*` 引用 20 条为有意悬空，记入暂停范围。
3. **P1-2 默认绑定细化**：出厂装配清单（员工/部门/出厂包默认挂哪些 skill）的显式规则待后续定义（仅做出厂装配清单，不自动改权限）。

## 9. 降级执行声明与复核结论（重要）

本设计 + 落地由主理人在 **Agent 框架持续故障**期直落（用户 B 方案授权）。框架恢复后已执行独立复核：
- **架构师高见远复核**：结论 **有条件 PASS**（报告 `docs/plan/v2-p0p1-architect-review.md`）。无硬红线突破、幂等稳健、ai_rd 闭环、CEO 标准正确、agency-agents 仅编目。唯一条件为文档陈旧（本 §7/§8.2 已本次修订至 115 工具口径）。
- **QA 严过关独立测试**：`backend/tests/test_bplan_seed_integrity.py` **13 passed / 0 failed**，种子完整性全验证。
- 两项复核均已闭环，原「未经复核」声明作废。
