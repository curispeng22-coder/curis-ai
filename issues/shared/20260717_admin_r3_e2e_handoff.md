# R3「AI 研发部」真实纵向执行链路 E2E 交接验证

状态：VERIFIED（由 Admin 侧同步）
路径：issues/shared/20260717_admin_r3_e2e_handoff.md
发起团队：Admin
目标团队：Codex（Workspace）
归属模块：R3 真实纵向执行链路（基线 §六）
是否阻塞：否
是否触发 L2：否

## 结论

请 Codex 主导跑通基线 §六「AI 研发部」统一验证场景，证明 Curis 现有骨架（官方公司包 + 部门/员工/技能/工具/工作流）能组合成一条真实、可重复、可验证的运行链路。Admin 侧资产与目录已就绪，执行中如发现官方资产 / 目录缺口，Admin 即时配合补齐（落 091/093/094 波次或新内部 Issue），不接管 Workspace Runtime。

## 统一验证场景（AI 研发部）

```text
实例化软件公司
→ 创建真实研发项目
→ 指定负责人和员工
→ 分配真实开发目标
→ 绑定 Skill / Tool
→ 运行 Workflow / Task
→ 调用模型或工具
→ 产生代码、文档或 Demo 成果
→ 记录 Token、模型和预估成本
→ 输出项目状态和下一步建议
```

## Admin 侧已就绪资产（R1/R2 波次，PR #2）

- 公司包 `ccp_ai_software_company` 可实例化：实例化产出 `departments` / `employees`(6) / `workflow_instances`(**6**)，`unresolved_refs` 全空。
- `wl_*`→`wt_*` 引用已解析（库内 `workflow_contents` 种子），实例化工作流 > 0。
- **6 条只读 Catalog 路由已就位**：Company Template / Company Package / Persona / Dashboard / Skill Templates / Employee 绑定类只读 GET，可供 Workspace 真实消费。
- **Tool / Workflow 能力态已标注**：115 Tool 标记（目录可见 / 已配置 / 可真实执行 / Mock-Stub），18 Workflow 标记（结构化可执行 / 只有设计 / 禁止实例化）。
- 资产完成度标准（094）已落地：`docs/plan/admin-asset-completion-standard.md`，验收以六条件为准。

## 需要 Codex 完成

- 主导跑通上述「AI 研发部」场景，形成真实 E2E 证据，至少包含（基线 §六完成标准）：
  项目目标 / 项目负责人 / 员工与能力绑定 / Workflow 与 Task 执行记录 / 真实结果 / 成果位置 / Token·模型和成本 / 失败原因或成功状态 / 下一步建议。
- 反馈执行中发现的官方资产 / 目录缺口（ID、版本、字段缺失），便于 Admin 配合补齐。
- 不能只提供 Task ID、数据库行或历史测试截图。

## Admin 配合方式

- 收到缺口即时修（落 091/093/094 波次或新内部 Issue），不发散、不越界；
- 不修改 Workspace Runtime / Task / Workflow Runtime / Employee Session / CEO Office 前端。

## Admin 验收方式

- Codex 提供真实 E2E 证据即视为 R3 通过；Admin 侧资产缺口补齐以对应 Issue 关闭为证。

## 禁止越界

Admin 不修改 Workspace Runtime、Task、Workflow Runtime、Employee Session 或 CEO Office 前端；不替 Codex 完成执行链。

## Workspace 侧进展同步（由 Admin 侧核验回填）

2026-07-17，Codex（Workspace）侧的 R3「AI 研发部」真实纵向执行链路 E2E 已收口，结论为 **PASS / `AI_RD_VERTICAL_E2E_CLOSED`**，并有独立质量运行席 Review 佐证。据此，本 Admin 侧交接 Issue 同步为 `VERIFIED（由 Admin 侧同步）`——依据本 Issue「Admin 验收方式」：Codex 提供真实 E2E 证据即视为 R3 通过。

**Workspace R3 E2E 关键证据（取自 `issues/20260717_workspace_r3_ai_rd_vertical_e2e.md` 与 `reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md`）：**

- Review 结论：`PASS`；Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`，Run 与 7 个 Step 全部 `succeeded`。
- 真实模型调用 7 次，总计 **9,622 tokens**，成本 **USD 0.01326900**（低于 USD 0.10）。
- 模型：`gpt-5.4-mini-2026-03-17`；`final_report` 非空，大小 **6,018B**。
- `final_report` SHA-256：`2d14cf90ca1fa850f7e8425763b922cda4c6c9c2132a2f55eac07791a07ba96c`。
- 固定分支：`feat/roadmap-r1r2`；凭据未读取/输出/落盘，停机后端口与容器全部关闭。

**SHA 引用对齐说明（消除上次复盘发现的 SHA 未对齐缺口）：**

本 Issue 历史引用的「前置提交 `758da525`」与 Workspace Review 引用的「固定 SHA `b0f791f7`」在复查中存在表述不一致。经核对，两者均为本仓库内**可达的祖先提交**：

- Issue 侧写法：`758da525b15adff17c16a063261d8a0d487e7f3e`（Workpace R3 E2E Issue 的「前置提交」）。
- Review 侧写法：`b0f791f74e449be1d6c907480cc183cf92a78209`（质量运行席 Review 的「固定 SHA」）。

时间线可解释为：Workspace 在编写 R3 E2E Issue 时以当时的前置提交 `758da525` 为基准；后续质量运行席在独立重跑并出 Review 时，环境已推进到其固定 SHA `b0f791f7`（两者皆为可达祖先，无冲突、无篡改）。**统一以 Review 文档的 `b0f791f7` 为权威固定 SHA 准**；如需追溯更早基准点，`758da525` 仍可作为并列参照（二者皆仓库内合法祖先，不构成状态分歧）。

> 备注：本轮仅做文档状态同步，未改动任何代码、未新建文件、未触碰其他 Issue；下一轮 handoff Issue 留待 Phase B 实现后再建。
