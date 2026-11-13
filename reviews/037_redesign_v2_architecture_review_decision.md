# Review 037 — redesign-v2 架构文档评审结论（决策级）

- Review date: 2026-07-07
- Reviewer seat: 系统交付席 / Software Architect
- Subject: `docs/architecture/redesign-v2-architecture-and-roadmap.md` + 第三方反馈评审
- Related: ADR-0016 (Proposed), ADR-0017 (Proposed), knowledge/002_Product_Vision.md, knowledge/003_Architecture.md

## Product Progress（一句话）

Curis Workspace 现可确认：v1.8 受控自演进执行内核仍是唯一事实源（SoT），v2 架构重设计降级为「未来蓝图」而非当前执行计划，避免 L 编号冲突污染所有角色文档。

## Decision（结论收敛）

### 1. v2 方向保留，执行不可直接批准
- v2 更接近终局「商业化多租户 AI 公司系统」，方向合理，应**归档为未来蓝图**。
- **不替换** knowledge/002 + 003 的 canonical L0–L6 分层（当前唯一事实源）。

### 2. 最大阻塞 = L 编号推翻 SoT + 内部自相矛盾（必须修）
- v2 把 `L1 执行层→统计层`、`L6 经济层→执行内核层`，推翻 002 line13 / 003 line15 的已定编号约定。
- v2 文档**内部不一致**：line 40 散文称「在原 L0–L6 之上新增 L1」，但 line 42–52 图实为整条栈重排。
- 修复方式：**保留 canonical L0–L6**，新内容用「横切 D 数据底座（不占 L 编号）」+「未来 gate 下的新层」表达，而非重排编号。

### 3. 阶段 0 必须拆开看（三项独立 gate 动作）
| 子项 | 性质 | 处置 |
|------|------|------|
| 0.3 role_context 串进 prompt / step 路由 | **明确行为变更**，撞已批准 Sprint 3 Role Context Runtime Reference Boundary（003 line112–121，runtime prompt 接入仍 blocked） | 必须**单独解禁 gate**，不可算「当前 gate 内零风险」 |
| 0.1 append-only event log | 加性 schema（新增 `evolution_events` 表） | 仍需**独立 slice gate**（ADR-0016 Slice C） |
| 0.2 tenant_id 预留 | 风险相对低，有 ADR-0017 D1「现在就做聚合根预留 tenant_id」支撑 | 可低风险落，但**严禁与多租户落地混为一谈**（仅加列+中间件注入点，不启用隔离） |

### 4. 下一执行动作（不是另写新计划）
- 下一动作 = **把 ADR-0016 提交总控决策席做 gate 批准**（ADR-0016 自身 line91 即路由 总控决策席）。
- 批准后按既定顺序开三个小 gate：**Role wiring → Event log → Sandbox**（与 ADR-0016 line65–71 一致）。
- 多租户 / 部门目录 / ROI / BI / 人事部 / 外部平台 → 继续留在 ADR-0017 的未来 gate，不提前。

## Changed files
- `docs/architecture/redesign-v2-architecture-and-roadmap.md` — 维持 Proposed；待修分层表达（行动项，未执行）
- `docs/decisions/ADR-0016-execution-substance-initiative.md` — 维持 Proposed；作为下一 gate 批准对象
- `docs/decisions/ADR-0017-multitenant-department-catalog.md` — 维持 Proposed；未来 gate

## Verification（本评审依据）
- 逐行核对 v2 文档 line 1–212、002 line13、003 line15/112–121、ADR-0016 全文、ADR-0017 全文。
- 确认：ADR-0016/0017 均为 Proposed；Sprint 3 Role Context 边界明确 blocked runtime prompt 接入；v2 line40 与 line42–52 自相矛盾。
- 本次为文档/决策评审，**无代码变更、无回归运行**。

## Known gaps
- v2 文档分层表达尚未实际修订（仅定结论，待执行）。
- ADR-0016 gate 批准尚未提交总控决策席（待路由）。
- 阶段 0.3 的解禁 gate 边界文件（Sprint 3 Role Context Runtime Reference Boundary 的扩展）尚未起草。

## Scope risks
- 若有人照 v2 排期直接开干，阶段 0.3 会绕过已批准边界 → 必须在 gate 批准前钉死「0.3 单独解禁」。
- L 编号若不在 v2 修订时统一，后续所有角色文档将持续读混。

## Next Curis seat
总控决策席（gate 决策 + 范围冲突）

## Handoff status
HANDOFF_REQUIRED → 总控决策席
- Payload: 「批准 ADR-0016 进入 gate（Role wiring / Event log / Sandbox 三切片）；确认 v2 仅作未来蓝图、不替换 SoT；确认 v2 必须先修 L 编号冲突与内部自相矛盾后方可归档。」
