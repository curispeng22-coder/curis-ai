# DESKTOP-SINGLE-INSTANCE-001 Review

Status: Completed (local behavior; external release gates open)  
Decision: `PASS_DESKTOP_SINGLE_INSTANCE_WITH_EXTERNAL_RELEASE_BLOCKER`  
Date: 2026-08-09

## 1. 结论

第二实例命中应用锁时不再触发 Tauri panic 或 macOS “Curis 意外退出”。setup 将
重复启动视为可处理状态，记录诊断信息，调用 macOS Bundle ID 唤回既有实例，并以
退出码 `0` 结束。首实例的 sidecar、Gateway、Runtime 和 Frontend 启动路径未改变。

## 2. 实际改动

- `desktop/src/lib.rs`
  - 增加固定 Bundle ID 的 macOS 唤回调用；
  - 将 setup 错误从 Tauri `expect` panic 改为受控退出；
  - 重复实例退出码为 `0`，其它启动错误为 `1`，并保留 stderr 诊断。
- `issues/20260809_desktop_single_instance_001.md`
- 本 Review、`CURRENT_STATE.md`、`CHANGE_LOG.md`

未修改 Backend、Frontend、Runtime 状态机、数据库模型或外部平台 API。

## 3. 证据

### 编译与静态检查

- `cargo check --manifest-path desktop/Cargo.toml`：通过
- `cargo build --manifest-path desktop/Cargo.toml --release`：通过
- `git diff --check`：通过
- `cargo fmt --check`：未执行成功，当前机器未安装 `cargo-fmt`；不是代码编译失败。

### 重复启动回归

使用本次 release binary 启动首实例，再启动第二实例：

- 首实例实际拉起 Guardian / Workspace / Gateway sidecar；
- 第二实例输出：`Curis 启动失败: Curis 已经在运行；请切换到现有窗口。`；
- 第二实例退出码：`0`；
- 回归前后最新 `curis-desktop` Diagnostic Report 未变化，没有新增崩溃报告；
- 第二实例未启动第二套 Workspace / Gateway 端口。

### 制品

- `.app`：`desktop/target/release/bundle/macos/Curis.app`
- 手工 DMG：`desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg`
- DMG SHA-256：`81d96dccde3176c569a8993a7dab0f376a821359cb99c927b9e93515ee0a7768`
- 当前活动库只读复核 SHA-256：`data/curis.sqlite` = `b5c3609e9f0c6dd7a03dbeb20cc8d25643a2bf087f3c7157f3d6ac3795960043`

活动库 SHA 与前一轮记录的 `c663222…` 不同，且本轮测试前文件时间已为
22:08；没有证据把该漂移归因于本 Issue，因此未猜测性回退或覆盖。

## 4. 未关闭事项

- macOS Developer ID、Hardened Runtime、公证、staple、Gatekeeper 和
  `/Applications` 安装仍未验证；
- 本机 `cargo-fmt` 缺失；
- 在锁屏环境下无法用可视窗口证明“唤回”前台状态；本轮只证明 Bundle ID 唤回调用、
  第二实例安全退出和无新增崩溃。

## 5. 下一步

继续进入真实 AI 执行、Evidence、CEO 验收与外部反馈闭环；Desktop 发布签名与公证
另行作为外部分发门，不把本地 DMG 当作最终交付。
