# 2026-07-22 Local Project Runtime Target Provisioning Review

## 结论

`PASS`。`quality.sqlite` 中唯一 local 目标链完整、隔离且可回查；Google 回调前无 active Owner membership。固定 UUID 可作为父 Issue 的唯一后续输入。

## 独立证据

- 数据库唯一为 `deploy/curis/gateway/.generated/data/quality.sqlite`；只读快照 SHA-256：`04b46a2ccd5de236e409326fd267617bf31fc6d4706ec28c7886db0fbb2e9c46`，`integrity_check=ok`，`foreign_key_check=0`。
- 固定链各精确 1 行：
  - tenant `local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4`
  - company `local-company-076a4926-4b95-404c-a019-acf36c26108b`
  - ceo `local-ceo-660378a5-a637-45ff-b6bd-431cd36c7046`
  - project `local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8`
  - preauthorization `local-owner-preauth-589a0ce3-97cf-401b-a54b-fb745b6fe579`
- Company 的 tenant/ceo/default_project 与 Project 的 tenant/company 全部精确关联；同库 `local-*` tenant/company/project 及固定 operation key 均只有 1 行，未混用历史链。
- 预授权为 `pending`，`material_digest IS NULL`、`consumed_at IS NULL`；目标 tenant/company/ceo 下 active `owner|ceo` membership 为 0。
- 原子与历史边界：实现以 `BEGIN IMMEDIATE` 包围建链，冲突或异常统一 rollback；仅 INSERT 新 UUID，并只 UPDATE 同事务新建 Company。回滚测试确认失败后 tenants/companies/projects 均为 0；幂等测试确认第二次不新增。交付前后计数证据为 tenants/companies/projects/preauth 各 `+1`、memberships `+0`，未发现历史实体更新路径。
- 端口先决条件覆盖 `3000/3100/8001/8002/8080`，任一开放即写入前拒绝；目标链已创建与该拒绝条件共同证明 provisioning 时端口释放。复核时 `3000=LISTEN`、`8080=LISTEN`，`gateway-egress-1`、`gateway-gateway-1`、`gateway-workspace-1`、`curis-new-api` 均已恢复运行；其余三个目标端口关闭。
- Focused：`PYTHONDONTWRITEBYTECODE=1 backend/.venv/bin/python -m unittest -v backend.tests.test_local_project_runtime_target` → `3 tests OK`；目标文件 `git diff --check` PASS。
- 本次质量复核仅执行只读 DB/容器/端口检查与临时库 focused 测试；未启模型、未读取或注入 Key、未访问外网、未修改实现或业务数据。

## 后续

父 Issue 仅可使用上述固定 UUID；直到真实 Google OIDC 回调原子消费预授权前，不得创建 active Owner membership。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
