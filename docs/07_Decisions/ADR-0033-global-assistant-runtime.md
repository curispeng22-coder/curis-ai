# ADR-0033: Global Assistant Runtime

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-07-30

Module: Assistant

## Decision

Curis 当前 Assistant 采用 Global Assistant Runtime。

旧方案：

```text
CEO Office 固定秘书栏
```

当前方案：

```text
根布局级 Global Assistant Provider / Host
→ 用户自定义 Identity
→ Snapshot / Notifications
→ Project 与 Business Department Query
→ Command 创建并启动现有 Task
→ Task / Execution / Artifact / AI Usage
```

## Reason

- Assistant 需要跨页面保持状态
- Assistant 必须读取真实业务事实
- 执行必须复用现有 Task 和权限边界
- 固定秘书栏把 Assistant 错误限制在 CEO Office 单一页面

## Consequences

- CEO Office 不再拥有独立固定秘书架构
- Assistant UI 可以随页面改变展示形态，但 Runtime 保持全局一致
- Assistant 不得绕过业务服务直接修改业务对象
- 真实外部模型能力与本地 Runtime 回归必须分别声明

## Supersedes

- CEO Office 固定秘书栏方向
- 仅页面级 Assistant 状态
