# ADR-0034: Main Baseline Restoration

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-07-30

Module: Source Control

## Decision

Curis 当前唯一有效产品代码基线为：

```text
main @ c0e1855f446a55aa3a384006cfcfed9877130338
```

旧状态：

```text
main 停留在旧提交，最新产品能力分散在功能和集成分支
```

当前状态：

```text
integration/curis-v1 经 Review 后 fast-forward 提升为本地 main
```

## Reason

- 候选包含当前完整产品、Assistant Runtime 和 Schema Governance
- `main` 与候选没有分叉提交
- Backend、Assistant、Integration、Frontend、启动链和数据库验证通过

## Consequences

- 所有文档、Issue 和后续开发必须使用完整 SHA 标识当前基线
- 旧分支只能作为历史和差异来源，不能声明为当前产品事实
- 远程发布需要单独 push 授权；远程滞后不构成第二产品基线
- 禁止通过 reset 或历史重写制造新的隐含基线
