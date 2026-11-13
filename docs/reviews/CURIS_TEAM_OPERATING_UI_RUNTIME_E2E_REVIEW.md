# CURIS TEAM OPERATING UI / RUNTIME E2E REVIEW

Authority Class: REVIEW · IMPLEMENTATION EVIDENCE
Status: Review
Date: 2026-08-19
Issue: `CURIS-TEAM-OPERATING-UI-RUNTIME-E2E-001`
Accepted Runtime Baseline: `abb60e040`
Disposition: IMPLEMENTED · CEO REVIEW REQUIRED

## Verdict

UI/API Adapter、immutable Operating Definition、Business/Workspace scope、版本 pin、Content Growth 与 RD 动态协作已真实接通 accepted `ResponsibilityRoutingRuntime`。未创建新 Schema、Task、Provider Session、Workflow Engine 或第五套 Runtime。

唯一未冒充通过的交互 closure：Browser 与桌面 Chrome 自动化均未触发 HTML5 native pointer drag event。相同 Team Operating Editor 的可访问“上移/下移”操作已真实改变顺序、发布 v2、写入隔离 SQLite 并在后端重启后恢复。严格 pointer-drag 仍需 CEO 复核或后续浏览器驱动 closure。

## 14 Questions

1. **能读取真实 Operating Definition：是。** `GET /team-operating/definition` 返回当前 published version、Assignment snapshot、可用 Employee 与 running Work pinned version；前端不读取 `runtime_entities`。
2. **修改会发布 immutable version：是。** Browser 从 v1 发布 v2；SQLite 同时保留 v1/v2，未静默迁移旧 Work。
3. **Reorder 是否改变 Default Flow：部分验收。** Browser 可访问排序真实把 `topic → research → copy → visual → publish` 改为 `topic → research → visual → copy → publish` 并发布 v2；严格 pointer-drag 自动化未触发 native drag event，不能写成已通过。
4. **Employee Binding 是否改变 Assignment：是。** E2E 将 visual 责任绑定到 replacement Employee，新 v2 snapshot 与 New Work均读取新 Employee；v1 Work保留旧 snapshot。
5. **Responsibility / Input / Output 是否被 Runtime 消费：是。** v2 visual snapshot持久化修改后的 responsibility、required refs 与 result contract，New Work pin v2 后按该 snapshot 运行。
6. **Running Work是否继续 pin旧版本：是。** old Work=`v1`，New Work=`v2`；API 同时投影两者。
7. **Content Growth是否跑通：是。** Default route、holder-preserving Leader Consult、Return to copy、修订后继续、final Result recovery均通过；Consult不创建 Handoff。
8. **RD是否证明 Default Flow不锁死协作：是。** Business scope完成 Product/Architect Consult、Developer→QA、QA Return Developer、fix→QA、final complete。
9. **Business scope无需 Workspace：是。** RD E2E 的 Business scope运行时 Workspace row count=`0`。
10. **Provider execution：未接通且未伪造。** 当前 Adapter只负责 Definition/Assignment/Router；安全接入真实 Provider需已授权 Domain execution bridge。本 E2E明确保持 provider Task=`0`、provider Session=`0`。
11. **Context/Token成本：** Content consult=`18 chars / 54 bytes / 16 refs / 0 hydrated bodies / 0 copied Conversation history`；Consult count=`1`，Handoff count=`4`（均来自真实责任转移），new Task/Session=`0/0`。RD Consult count=`2`，Handoff count=`5`。Resume latency当前路径不适用，未编造数值。
12. **Active DB：未修改。** Repository active `data/curis.sqlite` 前后均为 size=`1232896`、mtime_ns=`1786873339.955841838`、SHA-256=`2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`、integrity=`ok`。`backend/data/curis.sqlite` 同样保持 size=`1277952`、mtime_ns=`1786783659.967572836`、SHA-256=`a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`、integrity=`ok`。
13. **第五套 Runtime：没有。** Adapter复用 `ROLE_SLOT`、`RESPONSIBILITY_ASSIGNMENT`、`RESPONSIBILITY_WORKFLOW`、`CYCLE`、`HANDOFF` 与 accepted Runtime。
14. **剩余 Product → Implementation Gap：** 严格 pointer-drag 操作证据；真实 Provider execution；已接受 RD/XHS Domain Runtime 的完整迁移（本 Issue明确排除）。

## Browser / Restart Evidence

- Fresh ports: Backend `127.0.0.1:18751`; Frontend `localhost:18752`.
- Isolated DB: `/tmp/curis-team-operating-browser.sqlite`.
- Workspace: `workspace-0a1f990b-99ed-4918-9517-1b22ab82f5e7`.
- Browser UI读取 v1，进入“团队运转 / 默认流程”，真实调整顺序并保存。
- 页面显示 v2 与 `选题 → 调研 → 视觉 → 文案 → 发布`。
- SQLite：v1/v2 两条 `RESPONSIBILITY_WORKFLOW` 均为 `PUBLISHED`，defaultFlow分别保留旧/新顺序；integrity=`ok`。
- Backend stop/start使用同一 DB；页面 reload后仍显示 v2与新顺序。
- Browser console error/warn=`0`。

## Tests

- Backend focused: `2 passed`.
- Backend combined no-regression: `22 passed`（Team Operating、Routing、Foundation Persistence、Employee Identity、RD 2B、XHS Calendar、Workflow MVP、DB Safety）。
- Frontend: `14 passed`。
- Next production build: `45/45` routes generated。
- Python compile: PASS。
- Existing warnings仅为 FastAPI/asyncio deprecation；无新增 test failure。

## Commit Discipline

- Accepted Runtime baseline已提交：`abb60e040`。
- 本 Phase 2 UI/API Adapter未提交、未 push，等待 CEO Review。
