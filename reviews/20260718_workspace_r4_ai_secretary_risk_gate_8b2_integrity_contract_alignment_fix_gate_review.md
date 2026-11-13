# Workspace R4 第8项｜8b.2 完整性契约对齐修复 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_integrity_contract_alignment_fix_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`eacfeb708f1c916a4eae1b930bff8d110581c5a0`
- 质量结论：`PASS`
- 安全结论：`PASS`

## 结论

父契约与 focused 已同步 8a 响应口径：必经对象/中间行缺失或不可见为 `404`；对象存在但 tenant/归属/值错配，或 schema 无法证明请求关系为 `403`。原跨 Gate 冲突已关闭。

唯一缺口：无。本修复 Gate 通过；需重派父项 8b.2 复核，完成前 `8b.3` 继续冻结。

## 独立核对

- StepResult 仅经 tenant + `workflow_steps` 真实路径关联 Run。
- package/content 只核验本源字段，不推断跨状态机关系。
- 对象/必经中间行缺失、不可见或状态不可安全承接 → `404 secretary_source_unavailable`。
- 对象存在但 tenant/归属/关联值错配，或请求关系不在 schema 可证范围 → `403 secretary_source_forbidden`。
- `CONFLICT/STALE_CONTEXT` 仍仅为内部 fail_code，并对外映射 `404`；不使用 `409/423`。
- 篡改、历史替代、fallback、同名 ID、拼接、默认值、最近一次和裸文本均禁止。
- 模板验证失败时先省略；整体不满足契约则按对应失败类别拒绝。

## 新鲜证据

提交仅修改父 8b.2 契约与 focused 两文件，未修改实现、API 或 schema。

```text
.venv/bin/python -m pytest -q \
  backend/tests/test_ai_secretary_integrity_contract.py \
  backend/tests/test_ai_secretary_refusal_response_contract.py
```

结果：`11 passed in 0.07s`。其中完整性 focused `7 passed`，新增断言锁定缺失 `404`、已存在错配/不可证 `403` 和全局固定体。

`git diff --check eacfeb70^ eacfeb70`：通过。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 本 Review 不替代父项 8b.2 的重新复核。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
