# DESKTOP-PACKAGING-001：Curis 自包含桌面交付链

Status: Completed (local implementation; external release gates open)  
Decision: `PASS_LOCAL_DESKTOP_WITH_EXTERNAL_RELEASE_BLOCKER`  
Input: Desktop Packaging Gap 只读审查  
Owner: Curis 产品 / Runtime / Desktop 评审  
Date: 2026-08-09

Authorization record (2026-08-09): The product owner continued the active goal to
deliver a real, complete and usable Desktop target. The prerequisite Reviews are
closed: Runtime Workspace Foundation is `PASS_RUNTIME_WORKSPACE_WITH_EXTERNAL_ACTIVITY_DB_BASELINE`
and `THREE-BUSINESS-WORKSPACE-UI-001` is `PASS_THREE_BUSINESS_WORKSPACE_RUNTIME_UI`.
The product owner confirmed `data/curis.sqlite` as the unique active database;
its implementation-start SHA is `c663222af90129012e41b542780c9dffcd302b540e27074a13fbd62cce65321e`.
The non-active `backend/data/curis.sqlite` drift is recorded as external baseline
evidence and is not to be restored, merged or cleaned by this Issue.

Closed implementation lane:

- `desktop/src/main.rs`
- `desktop/src/lib.rs`
- `desktop/Cargo.toml` / `desktop/Cargo.lock`
- `desktop/tauri.conf.json`
- `desktop/package.json` / `desktop/package-lock.json`
- `frontend/next.config.js` (production standalone output only; no UI or route changes)
- new files under `desktop/scripts/`, `desktop/runtime/` and `desktop/resources/`
- `docs/reviews/20260809_desktop_packaging_001_review.md`

No other Backend, Frontend, prototype, active database or legacy execution files
are in scope. Signing and notarization may only be claimed when local credentials
and Apple verification evidence actually exist; otherwise the Review must record
the exact external release blocker.

## 1. 背景

当前 `Curis.app` 只是在开发机上从仓库启动 Python 与 Next.js 的 Tauri 壳。它依赖仓库、
本机运行时、`.venv`、`node_modules` 和 `.next`，未形成可从批准基线复现、可安装、可签名、
可公证的 Desktop Runtime。现有产物不能作为目标 Curis Desktop 已完成的证据。

本 Issue 已获授权并完成本地 Desktop Packaging 实现；外部分发签名、公证、DMG 与
`/Applications` 安装仍由独立发布门控制，不得以本地 `.app` 证据替代。

## 2. 前置条件

以下条件必须全部满足，才能把本 Issue 改为 Authorized：

1. `RUNTIME-WORKSPACE-FOUNDATION-001` 的独立 Review 必须为 `PASS`，不得仍处于
   `BLOCKED_PENDING_ACTIVITY_DB_PROVENANCE` 或其它阻塞状态；
2. `data/curis.sqlite` 与 `backend/data/curis.sqlite` 的双库 provenance 必须完成调查、形成
   明确裁定并关闭；所有无法解释的活动库写入必须停止；
3. 当前唯一活动数据库必须重新确认为 `data/curis.sqlite`，并取得实施前 SHA、路径、权限和
   进程占用快照；
4. 产品负责人必须另行给出 Desktop 实施授权、封闭文件清单和独立质量 Review 责任人。

任一条件未满足时，只允许只读审查，不得构建、启动、迁移或写入活动库。

## 3. 目标

交付一个可从批准代码基线复现的 macOS `Curis.app` 与最终 DMG：

```text
Curis.app
→ 单实例锁
→ 自包含 Frontend / Trusted Gateway / Workspace sidecars
→ Gateway :8080 健康通过
→ 唯一 data/curis.sqlite
→ First Arrival 或已存在 Company Runtime
```

应用安装后不得依赖源码仓库、WorkBuddy 私有目录、系统 Node/Python、开发 `.venv`、
`node_modules`、Docker 或 `next dev`。

## 4. 实施要求

### 4.1 自包含 Sidecar

- Frontend、Trusted Gateway 和 Workspace Runtime 的运行制品必须随 `.app` 打包并受同一发布
  版本管理；
- Tauri 只能启动包内已知 sidecar，不通过 `/bin/bash -lc` 拼接仓库路径或加载用户 shell profile；
- 不读取 `/Users/...` 等开发机绝对路径，不依赖 `CURIS_REPO_ROOT` 定位源码；
- Sidecar 参数、环境和可执行文件路径必须固定、最小化且不携带明文密钥；
- 不新增第二套 Workspace、Company、身份、Gateway 或数据库体系。

### 4.2 唯一数据库

- Desktop Runtime 只允许解析到一个规范数据库：`data/curis.sqlite`；
- 启动时必须显式传入并核验数据库绝对路径，禁止依赖工作目录解析相对路径；
- 禁止创建、读取或回退到 `backend/data/curis.sqlite`、包内种子业务库或其它隐式数据库；
- `.app`、DMG 和 Git 制品不得包含现有活动数据库或用户业务数据；
- 首次启动、升级、重启和失败恢复必须保持同一数据库及现有迁移机制，失败时 fail-closed；
- 本 Issue 不授权数据回填、双库合并或修改数据库业务模型。

### 4.3 Production Frontend Bundle

- Frontend 必须以可复现的 production bundle 进入应用，不得在运行期使用 `next dev`；
- 动态路由所需的生产服务及其运行时必须自包含，不依赖仓库 `.next` 或 `node_modules`；
- Tauri 窗口只能加载本次发布包对应的本机 Frontend，不能随工作树变化漂移；
- 构建必须冻结 API Base、版本号和制品清单，并证明安装后的 First Arrival、CEO Desk、
  Workspace Portal 与 Global Assistant 使用同一 Runtime 版本。

### 4.4 Trusted Gateway 8080

- Frontend 的业务请求必须统一经过 `127.0.0.1:8080` Trusted Gateway；
- Gateway 再访问 Workspace Runtime，禁止 Desktop 默认直连 Workspace Backend `:8000`；
- 仅绑定回环地址，不向局域网或公网暴露；
- Local Owner Session、Tenant、Company 和 CEO 身份继续沿用现有 fail-closed 边界；
- Gateway 启动失败、身份失败或上游不可用时必须返回真实错误，不允许绕过 Gateway 或伪装成功。

### 4.5 单实例、健康、重启与退出

- 获取应用级单实例锁后才能启动 sidecar；第二实例只聚焦现有窗口，不再启动另一套服务；
- 禁止按端口对未知进程执行无归属校验的 `kill -9`；端口冲突必须安全失败并给出可操作错误；
- 就绪检查必须覆盖 Frontend、Gateway `/health`、Workspace 健康、数据库版本和身份链，而非只检查
  TCP 端口；
- Sidecar 异常退出必须可见并进入受控恢复或明确失败状态，不得留下白屏或静默假运行；
- 正常退出先优雅停止全部所属 sidecar，超时后才强制回收；强杀、系统重启和再次启动后不得遗留
  或误认孤儿进程；
- 日志写入 Owner 私有应用日志目录并限制权限，不写共享 `/tmp`，不得记录密钥或敏感业务正文。

### 4.6 签名、公证与 DMG

- `.app` 使用 Developer ID Application 签名并启用 Hardened Runtime；
- `codesign --verify --deep --strict` 和 `spctl --assess` 必须通过；
- 完成 Apple notarization，公证票据必须 staple 到 `.app` / 最终交付制品并可离线验证；
- 生成最终只读、压缩 DMG，不接受 `rw.*.dmg` 等构建中间文件作为交付证据；
- DMG 必须包含本次签名后的同一 `.app`，提供 SHA-256、版本、架构、Git SHA 和构建时间清单；
- 从 DMG 安装到 `/Applications` 后，在没有源码仓库和开发依赖的环境中完成首次启动与重启验证。

## 5. 必须证明

1. clean checkout 可重复构建，`desktop/` 源码和锁文件已进入批准 Git 基线；
2. `.app` 内容清单证明 Frontend、Gateway、Workspace sidecar 自包含，且无 `.env`、密钥、活动库或
   用户数据；
3. 断开源码仓库路径并移入 `/Applications` 后仍能启动；
4. fresh 临时数据目录只创建唯一 `data/curis.sqlite`，不存在 `backend/data/curis.sqlite`；
5. First Arrival、Company 物化、CEO Desk、三业务 Workspace Runtime 在 Gateway `:8080` 链路下通过；
6. 单实例、端口冲突、Sidecar 启动失败、运行中崩溃、应用重启、正常退出、强杀和孤儿清理通过；
7. 数据库升级、重启、完整性和 Tenant / Company / CEO 隔离通过，且测试只使用临时 SQLite；
8. `.app` 签名、Hardened Runtime、Gatekeeper、公证、staple、最终 DMG 和 SHA-256 全部有可核验证据；
9. 独立质量席在真实安装路径完成浏览器/WebView、进程、端口、数据库和退出 Review；
10. 活动 `data/curis.sqlite` 在整个构建与测试过程中保持只读且 SHA 不变。

## 6. 禁止范围

- 不修改 Runtime Workspace 产品模型、状态机或三业务语义；
- 不新增 Workspace、Company、Tenant、Admin、认证或数据库体系；
- 不迁移、合并、复制、恢复或清理活动数据库；
- 不顺带重做 Frontend UI、Global Assistant、业务页面或真实平台 API；
- 不把开发模式、仓库内启动、临时 DMG、ad-hoc 签名或历史截图作为发布验收；
- 未获得 Authorized 状态与封闭文件清单前，不得实施本 Issue。

## 7. 关闭条件

实施授权后必须生成独立 Desktop Packaging Review，记录：实际改动文件、pre-existing diff 分离、
构建命令、制品清单、Sidecar 与数据库路径、Gateway 8080、单实例 / 健康 / 重启 / 退出、临时数据库
验证、签名 / 公证 / DMG / checksum、真实 `/Applications` 安装启动和已知限制。

Review：`docs/reviews/20260809_desktop_packaging_001_review.md`。本地实现已通过 Review；
在 Developer ID、notarization、staple、最终 DMG 和 `/Applications` 安装证据补齐前，
只能描述为“本地可用 Desktop 实现”，不能描述为最终外部分发完成。
