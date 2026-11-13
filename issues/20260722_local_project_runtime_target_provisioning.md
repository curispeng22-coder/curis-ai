# Local Project Runtime Target Provisioning

## Status

`CLOSED — PASS` — 质量独立复核通过，证据见 `reviews/20260722_local_project_runtime_target_provisioning_review.md`；Google 回调前仍无 active owner membership。

## Fixed Local IDs

- tenant: `local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4`
- company: `local-company-076a4926-4b95-404c-a019-acf36c26108b`
- ceo: `local-ceo-660378a5-a637-45ff-b6bd-431cd36c7046`
- project: `local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8`
- preauthorization: `local-owner-preauth-589a0ce3-97cf-401b-a54b-fb745b6fe579`

## Parent

`issues/20260722_macos_keychain_google_oidc_project_runtime.md`

## Objective

仅为同一 Google OIDC → Project Runtime 本机纵向切片，在 `quality.sqlite` 受控创建一条全新、隔离、可绑定的本机项目目标链。

## Scope

- 仅 `CURIS_ENV=local/development` 且仅 `127.0.0.1`；仅 `deploy/curis/gateway/.generated/data/quality.sqlite`。
- 单一受控 bootstrap 事务生成不可预测的 tenant、company、ceo、project 及项目运行所需最小关联；任一冲突或不完整整体回滚。
- 实际返回的 tenant/company/ceo/project ID 必须写回父 Issue，成为唯一后续输入；禁止默认、客户端选择、同名或历史推断。
- 首次 Google 回调成功前，只允许一次性不透明预授权；不得创建或伪造 active owner membership。

## Non-goals

- 不修改历史 tenant/company/project/Run/Usage；不启模型、Key、外网或 Project Runtime 执行。
- 不新增生产路径、多租户治理、第二身份源或客户端写入入口。

## Acceptance

1. 端口关闭条件下，唯一 local `quality.sqlite` 中出现一条完整隔离链；
2. 所有实际 ID 可从同库只读回查，且不与历史链混用；
3. 无 active owner membership，只有一次性预授权材料；
4. 失败时零残留；质量独立复核后，实际 ID 固定回父 Issue。

## Route

系统交付席单主线程实施与 focused 验证 → 质量运行席独立同库复核 → 产品规划席将实际 ID 固定回父 Issue。
