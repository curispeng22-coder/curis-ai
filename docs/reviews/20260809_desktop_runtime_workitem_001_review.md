# DESKTOP-RUNTIME-WORKITEM-001 Review

Status: Review  
Decision: `PASS_DESKTOP_FIRST_WORKITEM_WITH_SIMULATION_GATE`  
Date: 2026-08-09

## 1. 结论

三类 Workspace 已从“只有办公室”推进到可以承接真实业务对象：CEO 在研发办公室建立了首个
Cycle“完善 Curis”，在小红书与抖音办公室分别建立了第一条 ContentItem。对象从 Runtime
读取并在刷新后可恢复；没有创建 Project / Task，也没有生成平台成功、发布回执或互动数据。

本 Review 不宣称 AI 执行、Simulation 通过、CEO 验收或真实平台发布已经完成；这些门仍然保持
显式可见。

## 2. 实际变更

- `frontend/lib/runtimeApi.js`：增加 Runtime Cycle 与 ContentItem 创建请求。
- `frontend/components/runtime/WorkspaceRuntimeView.js`：三个办公室加入真实创建表单；RD 写入
  `PLANNED` Cycle，XHS / TTK 写入 `IDEA` ContentItem 和 `READY / UNVERIFIED` 版本；明确提示
  不自动通过 Simulation、不生成外部结果。
- `frontend/tests/runtimeApi.test.mjs`、`frontend/tests/runtimeWorkspaceUi.test.mjs`：增加契约和
  UI 门禁测试。

Backend、数据库 schema、旧 Project / Task、平台 API、导航和 Desktop 壳未修改。

## 3. 证据

| 检查 | 结果 |
| --- | --- |
| Runtime 前端测试 | `13 passed` |
| Next production build | `44/44` 路由生成通过 |
| scoped ESLint | 通过 |
| fresh Desktop Company 链 | 空公司 → FoundingRun → Company `Curis AI` 通过 |
| RD 真实窗口 | 创建 `研发工作台`，再创建“完善 Curis” Cycle；页面显示 `PLANNED`、8 阶段、CEO Assistant、0 证据 |
| XHS 真实窗口 | 创建“小红书运营工作台”，再创建 ContentItem；页面显示 `XHS IDEA`、图文版本、`UNVERIFIED`、无回执 / 互动 |
| TTK 真实窗口 | 创建“抖音运营工作台”，再创建 ContentItem；页面显示 `TTK IDEA`、60 秒竖屏视频版本、`UNVERIFIED`、无回执 / 互动 |
| 隔离库复核 | 1 Company、3 Workspace、1 Cycle、2 ContentItem、2 ContentVersion；`CYCLE=PLANNED`、`CONTENT_ITEM=IDEA`、全部 `UNVERIFIED`；SQLite `integrity_check=ok` |
| 源库保护 | 活动 `data/curis.sqlite` SHA-256 仍为 `c663222af90129012e41b542780c9dffcd302b540e27074a13fbd62cce65321e` |
| 退出清理 | `8002`、`8080`、`3010` 均已关闭 |

## 4. 未关闭门

- Cycle 仍需 Simulation、真实研发执行、构建 / 测试证据和 CEO 验收。
- XHS / TTK 仍需 AI 创作、CEO 审核、平台授权或 CEO 手动反馈；手动反馈只能保持未验证，不能冒充平台成功。
- Workspace Studio 仍是最小创建入口，尚未实现 Blueprint Canvas、能力绑定、AI 岗位装配、模拟台和审批交付。
- Desktop 外部分发仍缺 Developer ID、Hardened Runtime、公证、staple、Gatekeeper 和 `/Applications` 安装证据。
