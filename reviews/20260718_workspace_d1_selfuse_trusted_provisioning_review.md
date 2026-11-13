# Workspace D1 selfuse 可信 Owner / CEO Provisioning 质量 Review

- Issue：`issues/20260718_workspace_d1_selfuse_trusted_provisioning.md`
- 复核分支 / 修订：`feat/roadmap-r1r2` / `d57da0da16ea39c16d65b4da500de6e5674257e0`
- 结论：`PASS`
- 范围：停机、只读 SQLite 与端口 / 容器核验；未启动、未注 Key、未出网、未读写 D1 目标、未运行 pytest

## 独立证据

1. 数据源固定为 `deploy/curis/gateway/.generated/data/quality.sqlite`；本次只读快照 SHA-256 为 `8511a45b445463a33b118e9ec4a8241003ac80bdba22b07e746385a40288eb6b`。
2. `selfuse` 当前仅有 1 条 membership、1 条 active owner membership、1 个 Company、1 个 active Company。固定链唯一成立：
   - operation：`operation-9b36c8d5-384f-465c-a778-a5cd0462e609`
   - membership：`membership-23c57ccb-429c-4bb1-bcfc-d8af0ba62e21`
   - company：`company-ffef9eeb-ad15-4ee2-b3ad-39c6a1ef0c36`
   - ceo：`ceo-a40b6651-5184-40aa-b038-05f167932ce3`
   - membership 为 `owner/active`、未撤销、未过期；Company 为 `active`，两侧 `tenant/company/ceo_id` 精确一致。
3. 批准的 issuer + subject 在 `selfuse` 内无第二条 membership。库内另有 tenant-scoped 历史 membership，但均不属于 `selfuse`，未被本次映射复用；selfuse 查询结果保持唯一。
4. operation 审计仅 1 条，event type 为 `identity.selfuse_owner_provisioned`，outcome 为 `succeeded`；同一 correlation/idempotency 均唯一。payload 键精确为 `ceo_id/company_id/membership_id/operation_id/outcome/reason/role/subject_digest/tenant_id`，`subject_digest` 为 64 位摘要，无 subject 原文或凭据字段。
5. 只读终态核对显示：幂等重放未产生第二组 Company、membership 或 audit；错误映射未在 `selfuse` 留下冲突行。因本席禁止写入，本次不重新执行重放或冲突注入，结论取数据库提交后唯一性与零残留结果。
6. D1 固定 correlation 下 claim/model/tool 事件均为 0；Execution、Tool trace、Task、Result、Usage 均无新增记录。
7. `3000/3100/8001/8002/8080` 全部 `CLOSED`；Docker 中未发现 Gateway、Workspace、egress 或 JWKS 相关运行 / 停止容器。

## 结论与边界

Provisioning 的唯一 active owner → active Company → 同值非空 CEO 链、幂等终态、冲突零残留、脱敏审计及 D1 零副作用均满足 Issue 验收，结论为 `PASS`。

本 PASS 仅允许重新执行 D1 静态预检与质量 Gate；不授权启动、Key 注入、模型调用或工具链执行。

Next Seat：产品规划席

Handoff: sent to 产品规划席
