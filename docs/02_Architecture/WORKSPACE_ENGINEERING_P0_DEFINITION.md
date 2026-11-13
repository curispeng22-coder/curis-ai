# Workspace Engineering P0 Definition

**Status:** Review
**Definition State:** `WORKSPACE ENGINEERING P0 DEFINED`
**Date:** 2026-08-16
**Implementation State:** `NOT STARTED / REVIEW REQUIRED`

## P0 目标

证明一个**已经安装好的 Curis**，在不修改源码、不重新 Build、不重新安装 Curis 的情况下，可以安装此前不存在的声明式“客户反馈办公室” Workspace Package，并完成动态导航、Main / Context / Utility 渲染、真实 `CustomerFeedback` 创建与持久化、Desktop 重启恢复、卸载后导航消失，以及业务数据按明确规则归档保留。

通过前不得宣称 Dynamic Workspace Package Runtime 已实现。Codex 可以修改 Curis 源码不属于该证明。

## Scope

- 受控本地声明式 Package：`com.curis.sample.customer-feedback-office@0.1.0`。
- 最小 Manifest、Surface 声明与 `CustomerFeedback` Package Domain Schema。
- 安装、校验、原子存储、Registry 注册、Template → Instance materialization、启用、禁用与卸载。
- Registry 驱动的 Workspace 二级导航；Package 不新增一级导航。
- 使用有限 Core 组件真实渲染 Main / Context / Utility。
- 使用一个受限 Core Action 创建真实 `CustomerFeedback`；Core 提供安全读取投影。
- 记录 package/version/digest/import source/install state/instance pin provenance。
- 使用现有 SQLite 完成 Package、Instance、Domain Object 与 Activity 的重启恢复。
- 卸载默认规则：移除导航、禁用 Package、移除未引用的 active package files；保留业务对象与 archived manifest/schema/provenance snapshot 为只读归档。物理删除不进入 P0。

## Non-goals

- 任意 JavaScript、Python、Shell、SQL、Rust / Tauri 动态插件或其他任意代码执行。
- Marketplace、模板售卖、导出发布、通用 Publisher PKI、密钥轮换或第三方信任平台。
- Package update、schema migration、rollback engine；P0 只记录版本并拒绝不兼容更新。
- 万能低代码 UI Builder、Workflow Engine、DAG 或自由 Automation Builder。
- 新 Employee、Decision、Task、Evidence、Result、Capability、Permission 或 Computer Access 系统。
- Full Computer Access、自动授权 Connector、凭据写入 Package 或明文凭据持久化。
- XHS / RD / TTK / Content Growth 迁移到 Package。
- Workspace Engineering 自身最终 UI。

## Reuse

- 现有 Tenant / Company / Workspace identity 与 fail-closed scope。
- 当前活动 SQLite 持久化与现有迁移治理；验收只使用隔离数据库，不写活动库。
- Frozen Workspace Shell / Shared Patterns，尤其 Main / Context / Utility、P1–P7、Result Reference 与 System Activity 边界。
- Employee、Responsibility、Handoff、Decision P7、Artifact / Evidence / Result Reference；Package 只引用，不重建。
- Capability Registry、Connection / Health / Binding truth、Agent Adapter。
- ADR-0046 Computer Access Truth：Requested != Configured != Effective；安装 Package 不授予访问。
- XHS 已验收 Runtime / Desktop 路径与 RD 已验收 Phase 0/1 真实执行路径作为 no-regression 基线；RD 后续仍处于 Review 的部分不冒充 accepted baseline。

## Minimal Core Additions

- Workspace Package 最小 Manifest 与严格 Validator。
- 本地原子 Package Store。
- Installed Package Registry 与 package/version provenance。
- Registry 驱动的动态 Workspace 导航。
- 有限内置组件的声明式 Surface Renderer。
- 一个 Tenant / Company / Workspace scoped Generic Domain Object。
- 一个有限 Safe Action Registry；P0 只开放 domain object create，读取走安全投影。
- Template → Instance materialization 与 package version pin。
- Restart recovery。
- Disable / Uninstall 与默认只读归档规则。

## Acceptance

1. 验收用 Curis build 的源码、路由、业务类型常量与打包资源中不存在 sample `packageId`、`workspaceType` 或“客户反馈办公室”标签。
2. 启动已安装 Curis 后，通过 Core 本地 install command/API 导入 Package；全程不改 React / Python / Rust 源码，不重新 Build，不更新或重装 App。
3. Validator 拒绝未知字段 / action、路径穿越、未声明文件、不兼容 Core、非法 schema 与重复冲突安装；失败不留下半安装 Registry / files。
4. 成功安装后 Registry、Package Store、digest/provenance 与 instance version pin 真实存在，业务空间导航动态出现。
5. 打开办公室后，Main / Context / Utility 都由声明式 Renderer 真实渲染；未使用 package HTML/JS 或编译期专用 Route。
6. 通过受限 Action 创建一条真实 `CustomerFeedback`，并生成真实 object ID、scope、status、timestamps 与 activity；无 fixture / Mock。
7. 关闭并重启完整 Curis Desktop；Package 注册、导航、Instance、对象与 Activity 恢复为同一记录，SQLite integrity / foreign keys 通过。
8. 卸载前不存在 active run；卸载后导航消失、Package 禁用、active files 移除，业务对象及 archived manifest/schema/provenance snapshot 保留且不被静默删除。
9. XHS accepted focused Runtime/Desktop checks、RD accepted Phase 0/1 focused checks、Shared Runtime scope/persistence checks与 Computer Access truth checks无新增回归。
10. 只有以上证据全部通过，结论才可升级为“第一个真实 Runtime substrate”；P0 不证明 Marketplace、第三方包安全、Package update 或专业扩展能力。

## 主开发冲突风险

- 当前工作树存在大量预先修改 / 未跟踪文件；P0 不得在未冻结输入快照和 Allowed Files 前开始。
- 动态导航可能与主开发正在修改的 `TerraNavData` / Shell / route mapping 冲突；必须采用 Registry 增量投影，不重写现有六区导航或 XHS / RD 路由。
- Generic Domain Object、Registry 与 install API 可能触及 `runtime/workspace.py`、Runtime Foundation、API router、database migration 等主开发热点；未来 Issue 必须锁定最小文件并协调窗口。
- Surface Renderer 可能影响 `WorkspacePaneShell`、`runtimeApi` 与现有业务组件；必须 opt-in，只对 installed package route 生效，现有 RD / XHS / TTK 保持编译路径。
- Desktop app-data 路径、sidecar lifecycle 与 packaged resources 属打包主线热点；验收 Package 必须在 build 完成后外部导入，不能偷偷随 App 打包。
- P0 需要 schema / registry persistence，但活动 `data/curis.sqlite` 禁止作为开发写目标；所有迁移、重启、卸载证据使用隔离 HOME / SQLite。
- ADR-0046、XHS Accepted Record 与 RD 正在 Review 的 long-running closure 状态不同；no-regression 必须按各自正式接受边界表达，不能把未 Review 部分写成基线。
