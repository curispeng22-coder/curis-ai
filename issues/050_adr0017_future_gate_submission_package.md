# ADR-0017 Future Gate Submission Package — 总控决策席 决策请求

- Date: 2026-07-07
- Submitted by: 系统交付席
- Source gate: `issues/049_adr0017_future_gate.md` (Proposed, pending)
- Source ADR: `docs/decisions/ADR-0017-multitenant-department-catalog.md` (Proposed)
- Target approval: 总控决策席
- Status: Proposed — pending 总控决策席 approval.

---

## 1. 背景与定位

- 本包是 `issues/049` 的正式决策请求，附 `docs/decisions/ADR-0017`。
- 上游已定：`reviews/037_redesign_v2_architecture_review_decision.md` 结论 = v2 架构文档归档为未来蓝图、不替换 SoT；ADR-0016（执行实质化）已全量关闭（D1→D3→D2，63 测试通过，d24dd5de 提交），为 ADR-0017 提供了 D1（runtime role 接入）与 D3（追加写事件日志）的地基。
- `docs/decisions/ADR-0017` 已起草为 Proposed，统一了此前散列的「L5/L6 多部门方向 / 部门插件缝 / 多租户部门拓扑」三设想，但当前 gate（v1.8 / MVP v0.1）明确禁止其全部子决策。本包请求 总控决策席 裁决：是否开放 ADR-0017 未来阶段 gate。

## 2. 决策请求（一句话）

请求总控决策席：**批准开放 ADR-0017 未来阶段 gate**（多租户 CEO + 部门目录），授权分阶段边界定义，从最低风险的 D1（tenant_id 预留）起步；不批准任何实现。

## 3. ADR-0017 四子决策摘要

| 子决策 | 内容 | 性质 | 风险 |
|--------|------|------|------|
| **D1 多租户 CEO 模型** | 聚合根预留 `tenant_id` 作用域；company = manifest；现在只设计预留，不实现隔离 | 设计预留（加性 schema 预留） | 低（仅预留，无隔离/凭证/worker 透传） |
| **D2 部门目录通用化** | 部门 = Manifest 配置单元；业务型（对外平台）+ 职能型（人事/行政/BI）共用缝 | 设计/配置模型 | 中（引入元递归复杂度） |
| **D3 元循环与自可观测** | 职能型部门消费运行数据产出 ROI/配置/可视化；把 ADR-0016 D3 升级为硬依赖 | 设计 + 复用 D3 | 中（自可观测成地基） |
| **D4 两级治理** | 类型级扩展走 gate+ADR；实例级扩展仅配置+审计 | 治理策略 | 低（缓解治理复利） |

## 4. ⚠️ 关键决策点

**DP-1 多租户终结「纯本地零依赖」简洁性**
- 多租户隔离（数据/凭证/计算按租户）是硬需求，与 MVP「纯本地零依赖」核心卖点冲突。
- 缓解：D1 仅做 `tenant_id` 列预留（设计层面），不实现隔离；真实隔离留待企业版阶段（独立库/schema）。先预留、后实现、分阶段。

**DP-2 自可观测从补丁升级为地基**
- 行政部/BI 部要算 token 产出比、做可视化，系统必须把自身运行数据建为可查询/可归因数据源。
- 影响：ADR-0016 D3（追加写事件日志 + correlation id）优先级显著提前，从「审计 nice-to-have」变为职能型部门的硬依赖。D3 已在 ADR-0016 落地，可直接复用。

**DP-3 安全边界席触发**
- D1 多租户隔离、业务部外部平台凭证与合规、发布安全状态机 —— 任一进入实现，必触发 **安全边界席** 评审（外部服务 / 密钥 / 数据合规）。

## 5. 选项

- **(a) 批准开放 ADR-0017 未来阶段 gate**：授权分阶段边界定义，从 D1（tenant_id 预留，设计-only、加性 schema 预留）起步；D2/D3/D4 各自走独立小 gate。**建议 (a)**。
- **(b) 仅批准 D1 tenant_id 预留** 作为未来 gate 内的首个窄切片，D2/D3/D4 暂不开。
- **(c) 暂缓 / 否决**：维持 v1.8 / MVP，ADR-0017 继续作为 Proposed 蓝图，不开放 gate。

## 6. 推荐执行顺序与每片验证

**顺序**：D1（tenant_id 预留）→ D2（部门目录通用设计）→ D3（自可观测加固，复用 ADR-0016 D3）→ D4（两级治理），每片独立小 gate。

**D1 验证（未来小 gate）**：断言聚合根新增 `tenant_id` 列预留（DEFAULT NULL / 单用户兼容）；断言无凭证隔离 / worker 透传 / 多租户查询逻辑；断言现有单用户行为不变。

## 7. Trade-off（命名放弃项）

- **放弃**：v0.1「纯本地单用户零依赖」纯度，换取产品从「一个 AI 公司」走向「可拼装的商业能力目录（每个 CEO 组装自己的公司）」的轨迹。
- **保留**：Stability > Optimization > Evolution 策略、生产变更人工批准、不解除自动改码禁令、ADR-0016 全部成果、中文操作台、Task API `{ content }`、Project Memory 事实源归属。

## 8. Forbidden Scope（沿用 049 + 当前 gate）

实际多租户隔离 / 凭证按租户作用域 / worker 透传 tenant_id；Employee CRUD/扩展；外部平台集成或凭证；L6 经济回流/ROI 计算；部门实现或公司组织；新执行行为（规划外）；自动演进行为变更 / 自动改码；业务模块；当前 gate 禁止项全集。

## 9. Required Preservation（沿用 049）

AI Task Executor MVP v0.1；Tool System v1.8 loop；Stability > Optimization > Evolution；中文操作台；Task API `{ content }`；现有 API 语义；现有执行行为；Evolution Governor 决策策略；人工批准 gate；Project Memory 事实源归属；Role Profiles / Role Context；ADR-0016 成果（D1/D2/D3）。

## 10. 关联与依赖

- `reviews/037_redesign_v2_architecture_review_decision.md` — v2 评审结论（蓝图不替 SoT）
- `docs/decisions/ADR-0016-execution-substance-initiative.md` — 执行实质化（已 Accepted、全关闭，为 D1/D3 提供地基）
- `docs/decisions/ADR-0017-multitenant-department-catalog.md` — 源决策（Proposed）
- `issues/049_adr0017_future_gate.md` — 本 gate issue（Proposed, pending）
- `issues/048_adr0016_gate_submission_package.md` — 上一 gate 包（已 Approved，参考格式）

## 11. Compact Handoff Payload（给总控决策席）

- **Issue**: `issues/050_adr0017_future_gate_submission_package.md`（+ `049` + `ADR-0017`）
- **Objective**: 批准开放 ADR-0017 未来阶段 gate；授权分阶段边界定义（D1 起步）；不批实现
- **关键决策**: D1 tenant_id 预留（建议 a，设计-only）/ 仅 D1（b）/ 暂缓（c）
- **Preserve**: 见 §9 ｜ **Allow**: 未来阶段边界定义 + 事实源更新 + 分阶段子决策规划 ｜ **Forbid**: 见 §8
- **Next Seat**: 批准后 → 系统交付席 定义 D1 边界 → 质量运行席 验证 → 产品规划席 接受 → 开 D1 first-slice issue

## Handoff

**Handoff: HANDOFF_REQUIRED to 总控决策席.**

总控决策席 需裁决：是否开放 ADR-0017 未来阶段 gate（选项 a/b/c）。本包与 `issues/049` 一并提交：049 定义 gate 边界与禁止/保留范围，本包补充关键决策点（DP-1/2/3）与裁决请求，二者不可拆分审批。
