# Workspace R4 第8项｜8b.2 来源完整性与篡改防护 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`eacfeb708f1c916a4eae1b930bff8d110581c5a0`
- 质量契约结论：`PASS`
- 总体结论：`BLOCKED`

## 结论

父契约与 focused 已正确区分缺失 `404`、已存在错配/关系不可证 `403`，质量证据成立；但现有安全 Review 仍把“不可证明”归为 `404`，未对修正后的 `403` 口径完成安全重确认。由于本 Gate 要求质量与安全均 PASS，当前不得推进 `8b.3`。

## 已通过质量核对

- StepResult 仅经 tenant + `workflow_steps` 真实路径关联 Run。
- package/content 只核验本源字段，不推断跨状态机关系。
- 对象/中间行缺失、不可见或状态不可安全承接 → `404`。
- 对象存在但 tenant/归属/值错配，或 schema 无法证明请求所需关系 → `403`。
- `CONFLICT/STALE_CONTEXT` 仅为内部 fail_code，并映射全局 `404` 固定体。
- 预定义非敏感模板验证失败时省略或整体拒绝；禁止篡改、历史替代、fallback、拼接、默认值、最近一次和裸文本。
- 完整性拒绝在 Adapter/模型调用/出网前完成，不继续查询关联对象。
- 独立 focused：`11 passed in 0.07s`。

## 唯一阻塞

安全 Review `reviews/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_security_review.md` 仍写“必经对象或中间行缺失、不可见或不可证明 → 404”，未区分：

- 对象/中间行缺失、不可见 → `404`；
- 对象存在但 schema 无法证明请求关系 → `403`。

这与固定 SHA `eacfeb70` 的父契约及 focused 不一致，因此不能把旧安全 PASS 当作新口径的安全 PASS。

最小下一步：安全边界席只重审并更新该 Review，明确接受上述 `403/404` 分界；质量测试无需重复。收到一致的安全 PASS 后，本父项即可收口。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 未代签安全结论。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
