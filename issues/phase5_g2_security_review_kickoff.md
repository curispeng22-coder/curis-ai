---
title: Phase-5 G2 Credential Vault Gate · 安全评审启动清单（Kickoff）
priority: P0
phase: phase-5 (pre-gate)
owner_seat: 安全边界席 (主导) / 总控决策席 (gate 决策)
status: kickoff-draft
related_issue: issues/phase5_g2_credential_vault_gate.md
note: 架构师 agent 通道本次不可用，由主理人齐活林依 Phase-4.5 已锁定结论与 gate issue 展开起草；待 Agent 恢复后由高见远复核补签。
---

# Phase-5 G2 Credential Vault Gate · 安全评审启动清单

> 本清单是 `phase5_g2_credential_vault_gate.md` 的**评审启动展开**，非实现文档。
> 目标：在 Phase-5 实现之前，先完成威胁建模 + 安全边界定义，作为总控决策席 gate 批准的前置。

## 0. 文档元信息

| 项 | 值 |
|----|----|
| 关联 issue | `issues/phase5_g2_credential_vault_gate.md` |
| 性质 | 安全评审启动清单（kickoff），**非实现** |
| 主导席位 | 安全边界席 |
| 决策席位 | 总控决策席 |
| 状态 | P0 / 待启动 |
| 实现归属 | 系统交付席（仅 gate 批准后可开实现 issue） |

## 1. 为什么现在启动安全评审（而非实现）

- **评审周期长，须早于实现**：威胁建模、存储后端选型、边界契约签署均需在写代码前完成；若与开发迭代混跑，会被排期挤压导致安全边界草率。
- **风险性质（Phase-4.5 结论）**：真实密钥托管 = **生产高风险 / 演示无风险**。当前 `credential_ref` / `config_ref` 为 `scheme:reference` 不透明指针（演示态，runtime 走 env，无 Vault/KMS），演示链路口径安全；但一旦面向真实租户私有集成，缺失 KMS/轮转/脱敏即构成生产级泄露面。
- **gate 前置要求**：`phase5_g2_credential_vault_gate.md` 明确本 issue 只产出 gate 决策与边界定义，实现须批准后再单独开 issue。安全评审正是该 gate 的决策输入。

## 2. 评审目标（验收式）

输出以下 4 类 gate 决策输入物：
1. **威胁模型文档** —— 资产、威胁主体、STRIDE 逐类缓解方向。
2. **安全设计文档** —— `CredentialReference` 契约 + 存储后端选型 + 密钥解析层契约。
3. **安全鸿沟分析（gap analysis）** —— 当前 `scheme:reference` 占位 → 目标 KMS 句柄的差距与迁移路径。
4. **Gate 通过标准文档** —— 总控可批准的前置条件清单。

## 3. 评审范围（In-Scope）

- 真实 `credential_ref` / `config_ref` 密钥托管架构（model / tool / connector 接入凭证）。
- 存储后端选型对比与决策标准：**Vault** vs **云 KMS（KMS + 加密表）** vs **自研加密表**，给出选型维度（隔离性 / 轮转 / 审计 / 运维成本 / 合规）。
- 密钥解析层契约：`ModelGatewayAdapter` / tool execution 运行时如何**经解析层**取密，不直连存储。
- Admin 密钥策略面：规划 `/api/platform/secrets/policy`（Admin 仅配策略，不触明文）。
- 七类安全边界决策（见 §6）。

## 4. 评审范围外（Out-of-Scope）

与 gate issue 严格对齐，**明确不做什么**：
- 不实现 vault 存储、不存明文密钥。
- 不改 Task Execution 语义、不接 provider SDK / 直接 provider 调用。
- 不做 billing / ROI / marketplace。
- 不改 New API 源码、不依赖 New API 内部库。
- 不建表、不持久化、不迁移、不运行时读密钥（本期仅规划）。

## 5. 威胁建模草案（Threat Model）

**资产**：租户私有密钥（model / tool / connector 接入凭证），泄露即等于接管租户外部集成。

**威胁主体与 STRIDE 映射**：

| 威胁主体 | STRIDE 类 | 威胁场景 | 既有缓解（引用） | 待补缓解 |
|---------|----------|---------|----------------|---------|
| 外部攻击者 | I（信息泄露） | 直接读后端密钥表 | 当前无真实密钥（仅占位） | KMS 加密、静态加密 at-rest |
| 租户越权 | E（越权） | A 租户读 B 租户密钥 | `tenant_id` fail-closed 必填 | 密钥行级租户隔离 + 解析层强制 tenant scoping |
| Admin 越权 | E | Admin 读租户明文密钥 | Admin 仅配策略面（规划中） | Admin **零明文**：策略与密钥存储分离 |
| 内部运维 | I | 运维误拷日志/备份含密钥 | 密钥不进日志/trace/usage_event/audit（gate 约束） | 静态扫描 + 脱敏中间件 |
| 日志/链路泄露 | I | trace/audit 误带密钥 | AuditEvent 白名单（capability.*/governance.*） | 评估是否新增 `secret.*` 白名单 + 脱敏规则 |
| 密钥吊销失效 | D（拒绝服务） | 吊销后任务仍用旧密钥 | 无（待定义） | 解析层校验 `status=active` + 失败模式 |

## 6. 安全边界决策清单（须安全边界席签署）

逐项给出：待评审问题 / 建议选项 / 决策 owner。

| # | 决策 | 待评审问题 | 建议选项 | 决策 owner |
|---|------|-----------|---------|-----------|
| 1 | 密钥归属与存储后端 | 密钥 truth 放哪？ | Vault / 云 KMS / 加密表（推荐 KMS+加密表，Admin 不持明文） | 安全边界席 |
| 2 | 租户隔离规则 | 跨租户如何隔离？ | 行级 `tenant_id` + 解析层强制 scoping（沿用 fail-closed） | 安全边界席 |
| 3 | 运行时访问规则 | 谁能在运行时取密？ | 仅解析层（ModelGatewayAdapter / tool exec），经 token 换取，不直接暴露 | 安全边界席 + 系统交付席 |
| 4 | 密钥脱敏规则 | 各层如何脱敏？ | UI 仅显 reference id + status；日志/trace/audit 全脱敏；新增 `secret.*` 白名单评估 | 安全边界席 |
| 5 | 轮转/吊销规则 | 如何轮转与吊销？ | 支持 `rotated_at` / `status=revoked`；解析层拒绝非 active | 安全边界席 |
| 6 | 审计事件白名单 | 是否新增 `secret.*`？ | 评估新增 `secret.policy_changed` / `secret.rotated`，不记录值 | 安全边界席 |
| 7 | 缺失/吊销失败模式 | 密钥缺失或吊销时？ | **fail-closed**：任务拒绝 + 审计记录，不降级重试 | 安全边界席 + 总控决策席 |

## 7. 评审交付物清单（Deliverables）

| 交付物 | 产出方 | 时机 |
|--------|-------|------|
| 威胁模型文档 | 安全边界席 + 架构师 | M1 |
| 安全设计文档（CredentialReference 契约 + 存储后端 + 解析层） | 架构师 | M2 |
| 安全鸿沟分析（gap: scheme:reference → KMS 句柄） | 架构师 | M2 |
| Gate 通过标准文档 | 安全边界席 | M3 |

## 8. 评审流程与里程碑

```mermaid
flowchart LR
    M0[启动会 席位确认] --> M1[威胁建模完成]
    M1 --> M2[安全设计 + gap 分析]
    M2 --> M3[边界条件签署 安全边界席]
    M3 --> M4[总控决策席 gate 批准/驳回]
```

| 里程碑 | 内容 | 建议工期（相对周） | 退出标准 |
|--------|------|------------------|---------|
| M0 | 启动会，席位就位，范围对齐 | 第 1 周初 | gate issue 已读、范围签字 |
| M1 | 威胁建模完成 | +1 周 | 威胁模型文档评审通过 |
| M2 | 安全设计 + gap 分析 | +1.5 周 | 设计文档 + gap 定稿 |
| M3 | 边界条件签署 | +0.5 周 | 安全边界席签署 7 类决策 |
| M4 | 总控 gate 决策 | +0.5 周 | 批准/驳回结论 + 实现 issue 可开 |

## 9. Gate 通过标准（Pass Criteria，供 M4 决策）

总控决策席**仅在满足全部以下条件时**批准：
- [ ] 威胁模型覆盖全部 5 类威胁主体，缓解方向可执行。
- [ ] 存储后端选型决策明确，且 Admin **零明文**。
- [ ] `CredentialReference` 契约与解析层契约定稿（无实现）。
- [ ] 7 类安全边界决策均经安全边界席签署。
- [ ] 审计白名单策略（含是否新增 `secret.*`）定稿。
- [ ] 失败模式定义为 fail-closed。
- [ ] 可据此开 Phase-5 实现 issue，含 allowed files / tests 约束。

## 10. 依赖与升级路径

- **依赖**：现有 `_require_platform_admin` 401 + fail-closed、`AuditEvent` 白名单（capability.*/governance.*）、`catalog_constants` 枚举。
- **升级**：超出 ADR-0017 范围或触发安全边界冲突时，升级 **总控决策席**。
- **Handoff 契约（评审通过 → 实现 issue）**：实现 issue 须显式声明 allowed files（如 `model_gateways`、`secret_metadata` 新表、解析层模块）、禁止文件（Workspace 写路径、usage_event/audit payload）、必含测试（ref 解析 / 拒绝明文 / 轮转 / KMS mock / Admin 无法读明文负向 / 401·403 守卫）。

## 11. 启动前检查表（Kickoff Checklist）

- [ ] 席位就位（安全边界席主导、总控决策席待命、系统交付席旁听）
- [ ] `phase5_g2_credential_vault_gate.md` 已读且范围对齐
- [ ] 现有代码事实已盘点（credential_ref 占位、无 vault 模块、fail-closed 守卫）
- [ ] 评审范围 In/Out 已对齐（不含实现）
- [ ] 威胁建模模板选定（STRIDE）
- [ ] 交付物 owner 已指派（§7）
- [ ] 时间表已排（§8 里程碑）

## 12. 给主理人的建议

- **现在即可启动**：安全评审本身**不依赖 gate**（评审是 gate 的输入），建议立即开 M0，不阻塞 demo。
- **实现留 Phase-5**：本清单与 gate issue 均明确「不实现」，避免评审期误进代码。
- **独立专项**：建议将 G2 安全评审作为**独立安全专项**推进，不混在功能开发迭代里，确保席位专注与审计可追溯。
- **待 Agent 恢复**：架构师高见远应复核本清单并补签（尤其 §5 威胁建模与 §6 决策建议选项）。

---

*主理人齐活林 依 Phase-4.5 架构评审结论与 gate issue 起草；架构师复核补签待 Agent 通道恢复。*
