# DESKTOP-PACKAGING-001 Review

Status: Review  
Decision: `PASS_LOCAL_DESKTOP_WITH_EXTERNAL_RELEASE_BLOCKER`  
Date: 2026-08-09

## 1. 评审结论

Desktop Packaging 的实现门已关闭：本地 `Curis.app` 已可在隔离 HOME 中自包含启动，
但最终外部分发仍受签名、公证、DMG 和 `/Applications` 安装证据约束。以下记录实现前
缺口、实现后证据和未关闭的外部发布门。

## 2. 已关闭前置条件

| 条件 | 证据 | 结论 |
| --- | --- | --- |
| Workspace Runtime Review | `PASS_RUNTIME_WORKSPACE_WITH_EXTERNAL_ACTIVITY_DB_BASELINE` | 通过 |
| 三业务 Workspace UI | `PASS_THREE_BUSINESS_WORKSPACE_RUNTIME_UI` | 通过 |
| 唯一活动数据库 | `data/curis.sqlite`，SHA-256 `c663222af90129012e41b542780c9dffcd302b540e27074a13fbd62cce65321e` | 通过 |
| 遗留数据库边界 | `backend/data/curis.sqlite` 的漂移已记录为外部活动基线 | 不恢复、不合并、不清理 |
| Desktop 产品授权 | 产品负责人继续“真实、完整、可用 Desktop”目标，并授权本 Issue 封闭实施 | 通过 |

## 3. 现状证据

- `desktop/src/lib.rs` 通过 `CURIS_REPO_ROOT`、`/bin/bash -lc`、系统 Node / Python
  启动 sidecar，并在 `:3000` / `:8000` 上运行；这不是自包含交付。
- `desktop/tauri.conf.json` 的 `frontendDist` 只有旧静态占位页，窗口允许访问开发端口和
  `:8000`；没有 production bundle、Gateway `:8080` 或资源清单。
- `frontend/next.config.js` 默认 `NEXT_PUBLIC_API_BASE` 为 `http://127.0.0.1:8000`；
  Desktop 构建必须显式冻结为本机 Trusted Gateway `:8080`。
- 当前仓库存在 `frontend/.next`、`frontend/node_modules` 和 `backend/.venv`，但它们
  不能直接作为安装后运行依赖。

## 4. 实施顺序

```text
生产 Frontend standalone bundle
  → 可重定位 Python Workspace sidecar
  → 本机 Trusted Gateway :8080
  → 单实例 / 健康 / 优雅退出 / 失败恢复
  → Tauri .app / DMG
  → 安装路径与隔离 SQLite 验证
  → 签名 / 公证 / staple（有真实凭据时）
```

实现必须先让 `Curis.app` 在移出源码仓库后，通过同一 Gateway `:8080` 完成
First Arrival、Company 物化、CEO Desk 和三业务 Workspace，再进行打包和发布验证。

## 5. 外部发布门

当前机器存在一个名为 `ClaudeCN Signing` 的 codesign identity，但它尚未证明为
Developer ID Application，也没有 notarization / staple 证据。因此本 Review 只允许
实现本地可用的签名检测与清单；不能把 ad-hoc 或未验证 identity 写成公证完成。

## 6. 实现后必须回传

- 实际修改文件和 pre-existing diff 分离；
- clean checkout 可重复构建命令与版本；
- `.app` 内容清单（无活动库、密钥、`.env`、开发绝对路径）；
- sidecar 路径、Gateway `:8080`、唯一数据库路径；
- First Arrival、已有 Company、三业务 Workspace、失败和越权验证；
- 单实例、端口冲突、sidecar 崩溃、重启、退出和孤儿进程证据；
- `/Applications` 安装启动证据；
- 签名 / Gatekeeper / notarization / staple 的真实结果和限制。

在这些证据完整前，Desktop 只能标记为本地可用实现，不能标记为最终外部分发完成。

## 7. 实现复核（2026-08-09）

实现已在授权文件边界内完成。关键修正包括：

- Tauri 仅启动 `.app/Contents/Resources/runtime` 内的 Node、Workspace、Gateway 和
  guardian，不再读取仓库或系统 Node/Python；
- `frontend` 采用 standalone production bundle，业务 API 固定走 `127.0.0.1:8080`；
- Workspace 使用应用数据目录下的唯一 `data/curis.sqlite`，不会写入活动仓库库；
- guardian 兼容 PyInstaller one-file 的 bootloader 子进程链，并在父进程失联时回收子进程；
- 就绪检查覆盖 Gateway `/health` 与真实 `/ceo-office` 路由；单实例锁使用应用数据目录文件锁。

## 8. Fresh App 证据

验证命令（源码仓库保持不参与运行；Runtime Flow 修复后重新打包）：

```text
CURIS_BUILD_PYTHON="$PWD/backend/.venv/bin/python" ./desktop/scripts/build-runtime.sh
cd desktop && CURIS_SKIP_RUNTIME_BUILD=1 pnpm exec tauri build --bundles app
pnpm build:dmg
```

产物：`desktop/target/release/bundle/macos/Curis.app`，arm64；主可执行文件 SHA-256
`20a40bf06ade55d177a39113d937eebfc10849fb9a290099a16920f0bf573c7f`。Runtime Flow 修复后的
手工 DMG SHA-256 为 `b5ff9495749f10d86df1624f5d924f074c4e0d57b3ea2229fcca2a8da1b01d4e`。
包内实际存在：

```text
Contents/Resources/runtime/frontend/server.js
Contents/Resources/runtime/node
Contents/Resources/runtime/workspace/curis-workspace
Contents/Resources/runtime/gateway/curis-gateway
Contents/Resources/runtime/guardian/curis-guardian
```

隔离 HOME `/tmp/curis-desktop-finalisolated.WcNz` 验证结果：

| 检查 | 结果 |
| --- | --- |
| Workspace `:8002/health` | `{"status":"ok"}` |
| Trusted Gateway `:8080/health` | `{"status":"ok"}` |
| Frontend `/ceo-office` | HTTP 200 |
| Runtime API 经 Gateway | `{"tenant_id":"selfuse","companies":[]}` |
| 数据库 | 仅创建 `~/Library/Application Support/com.curis.desktop/data/curis.sqlite` |
| 源库保护 | 活动 `data/curis.sqlite` SHA-256 仍为 `c663222af90129012e41b542780c9dffcd302b540e27074a13fbd62cce65321e` |
| 单实例 | 第二实例 fail-closed，提示“Curis 已经在运行” |
| 退出清理 | 退出后 `:8002`、`:8080`、`:3010` 均不可连接，无 Curis sidecar/guardian 孤儿 |

## 9. 当前阻塞与边界

- 截图中的“意外退出”来自上一版 guardian 直接比较父 PID：PyInstaller one-file 会插入
  bootloader 子进程，导致启动等待超时。现版已改为检查父进程祖先链，并把前端就绪检查改为
  真实 `/ceo-office` 路由；fresh app 验证已通过。
- 已生成本地验证 DMG：`desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg`，
  当前 SHA-256 `ab0f5745e361bf1c719fa016a499e03e0ef68b004a8116450c32f9ae9c80c9e9`。Tauri 的
  Finder 美化 DMG 脚本在当前环境缺少 create-dmg support 目录而失败；该手工 DMG 不能替代最终发布制品。
- 当前可运行 `.app` 保持 Tauri 默认 ad-hoc 签名；`codesign --verify --deep --strict`、
  Developer ID、公证、staple 与 `spctl --assess` 均未作为本地完成条件伪称通过。任何
  Hardened Runtime / Developer ID 签名必须在具备正确 entitlements 与 Apple 证据后重做，
  不能直接对当前 PyInstaller sidecar 做深度签名。
- 尚未在 `/Applications` 做无源码路径安装验收；因此本 Review 不宣称外部分发完成。

## 10. Runtime Flow 补充复核（2026-08-09）

`DESKTOP-RUNTIME-FLOW-001` 修复了 Gateway OPTIONS 预检与重复 CORS 响应头，并将 Workspace
Studio 改为调用 Runtime Workspace 创建契约。隔离 HOME 的真实窗口完成：空公司 → Founding Guide
→ Company 物化 → Workspace Portal → Studio 创建研发 / 小红书 / 抖音三间 Workspace → 分别进入
Runtime 运行现场；最终 Portal 显示 3 个真实 Workspace，空态不生成示例数据，退出后端口和 Curis
sidecar 均清理。该补充证据不改变本 Review 的外部发布阻塞结论。
