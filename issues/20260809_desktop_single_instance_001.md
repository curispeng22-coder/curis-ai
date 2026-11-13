# DESKTOP-SINGLE-INSTANCE-001

Status: Completed (local behavior; external release gates open)  
Date: 2026-08-09  
Owner: Curis Desktop Runtime

## 1. 问题

第二次启动 Curis 时，应用级锁能够正确阻止第二套 sidecar，但 Tauri setup
错误被 `expect` 升级为不可恢复 panic，macOS 显示“Curis 意外退出”。这违反
Desktop Packaging 既定契约：第二实例应唤回现有窗口并正常退出。

## 2. 目标

- 保留单实例锁和 sidecar 隔离；
- 第二次启动不再 panic 或生成崩溃报告；
- 尝试通过系统 Bundle ID 唤回已运行的 Curis；
- 启动失败仍写入可诊断的 stderr，不隐藏真实原因。

## 3. 允许文件

- `desktop/src/lib.rs`
- 本 Issue Review、`CURRENT_STATE.md`、`CHANGE_LOG.md`

## 4. 不在范围

- 不改数据库、Workspace Runtime、Frontend 或业务状态机；
- 不引入新的多实例数据模型；
- 不处理外部签名、公证和发布授权。

## 5. 验收

1. 第一实例正常启动并通过 Gateway、Runtime、Frontend readiness；
2. 第二实例退出码为 0，不产生 panic / macOS crash report，并执行已有实例唤回；
3. 第一实例仍可正常退出，sidecar 无孤儿进程；
4. Rust 编译、`git diff --check` 和隔离运行证据通过。

## 6. 结果

已完成：setup 错误不再通过 Tauri `expect` 触发 panic；重复启动记录可诊断错误、尝试
唤回既有 Bundle，并以退出码 0 结束；正常启动路径和 sidecar 逻辑保持不变。

Review：`docs/reviews/20260809_desktop_single_instance_001_review.md`
