# Workspace 同源 Package 来源隔离链准备质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_company_package_provenance_isolated_setup.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`0947b9e6425dc586e77303e559098df2394fa6ad`
- 数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 质量结论：`PASS`

## 结论

停机只读核验通过。新的 tenant→membership/CEO→Company→Package/version→Bridge→Workflow/version→Workflow Instance→Project→Task→pending Run 全链均由同一 `quality.sqlite` 的服务端字段和真实关联证明；六角色新 Employee/Binding 唯一，运行与出网计数均为零。本结论只允许申请后续单次真实执行 Gate，不授权模型调用。

## 同库与身份链

- SQLite `main` 实际路径唯一为 `/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite`，未附加或查询第二数据库。
- operation：`op-9f341260-0a91-4e39-8b83-e8fd9c62cd56`；provisioning：`prov-7da2ad98-d821-4c6b-9f3d-cec35dfaf959`。
- tenant：`tenant-3160d289-7dfa-4684-8e53-f25d1fa3fd8a`，唯一且 `active`。
- membership：`membership-fcfabb3d-cf4a-4f1b-b97a-1df419d035a9`，唯一、`active`、未撤销、未过期；issuer/subject 仅做布尔匹配，均与批准值一致，未输出原值。
- CEO：`ceo-55642f4c-9e00-4ef0-be11-8f4568d64430`，membership 与 Company 映射一致。
- provisioning 与 setup 审计各 1 条，subject 仅保留非空 digest；审计 payload 禁止字段计数为 0。

## 来源与运行链

- Company：`company-f108f133-597b-4d12-9682-53c821af5b32`，`active`，来源为 `ccp_ai_software_company@1.0.0`。
- Bridge：`bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0`，`active`、未撤销，目标 `official.workflow.software_rnd_sop@1.0.0`，capability=`structured_executable`。
- Department：`dept-c0fb4115-6919-44b8-b4dc-d7f62b2ae17f`，同 tenant/Company，`active`、enabled。
- Package Workflow Instance 共 6，精确 bridge 的 executable Instance 唯一：`wfi-f0eb0523-0e36-4ed3-8c65-1b03fd5f2200`；其 Package/bridge/Workflow 版本来源字段与 Company、Run 完全一致。
- Project：`project-bc562b8d-37b3-4f03-bbff-658dcef851aa`；Task：`087e4a8b-4aa4-4a35-a6fb-bff0b60e81a3`。
- Run：`wfr-06489c59-fd30-47f1-8bbf-0d19c5d15415`，`pending`，7 个 Step 全部 `pending`；Run 的 tenant/Company/Department/Project/Task/WFI 和来源快照逐项一致。

## 六角色新 Binding

- Tech Lead：`emp-1c1f3c1b-db51-451c-b33d-02e7d229b719` → `bind-1504ce7e-75fe-4db6-b3cb-094a80a2ffdf`
- Product Manager：`emp-a8d95229-fcb5-4786-b18b-fa8fc8fe8de7` → `bind-1c42b740-8548-4af1-9060-91466659c86b`
- Architect：`emp-d150ca5f-a671-40a2-83a6-f5a39d0171d2` → `bind-40bdb391-4ad1-4af1-bf55-c13e0ffedf3b`
- Frontend Engineer：`emp-12bf8b42-4cf8-4de2-a3c0-75e3b8924f12` → `bind-5b69658a-2074-4c04-9803-d92f0b498eee`
- Backend Engineer：`emp-5a1ce6bf-1a71-4d36-bab8-703313c35af2` → `bind-1b324332-4071-479c-aab3-308b345eae30`
- QA Engineer：`emp-c88882bb-393d-4e64-9d1b-db142c0c622e` → `bind-5aa4a90f-b541-45a1-a2ac-6d6cacb26095`
- 六个 Employee 均属于新 tenant/Company/Department，enabled 且 `idle`；六个 Binding ID 唯一、enabled，均指向 `official/model/official.openai.gpt-5.4-mini-2026-03-17`。

## 零执行与停机

- StepResult=0、Execution=0、Usage/outbound/model event=0，Run 无 started/completed/failed 时间；Artifact 持久表不存在。
- 当前 tenant 审计事件仅有 provisioning、company instantiated、workflow run created 和 setup completed，无模型或出网事件。
- 端口 `3000/3100/8001/8002/8080` 全部 `CLOSED`。
- 撤销桥接后 Run 写入前拒绝与跨租户 fail-closed 已由当前 SHA 包含的既有质量 Review/16 项 focused 证据覆盖，本次停机核验未改库重演。

## 范围声明

- 全程使用 `sqlite3 -readonly` 和本地端口探测；未修改数据库或历史记录。
- 未启动服务、未读取或注入 Key、未出网、未调用模型。
- 新隔离链所有实体均指向新 tenant/Company；未引用 `tenant-a` 或 `company-a` 的 Employee/Binding/Run。

## 唯一缺口

无。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
