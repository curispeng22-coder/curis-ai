# Admin / Workspace 统一协作纪律

> 生效日期：2026-07-17
> 状态：长期有效，替代此前所有临时口头约定
> 文档性质：Shared 治理文档（由产品负责人裁决，自 2026-07-17 起对 Admin 与 Workspace 双方生效）

---

## 一、分支

- Admin 只使用 `Admin` 分支。
- Workspace 只使用 `Workspace` 分支。
- 禁止直接修改对方分支。
- 禁止强推（`--force`）、改写远程历史、覆盖他人提交。

## 二、目录归属

**Admin**
- `frontend/app/platform/**`
- Admin 专属测试、文档和交付文件

**Workspace**
- `frontend-workspace/**`
- `frontend/app/page.js`
- `frontend/app/ceo-office/**`
- `frontend/app/employees/**`

**Shared**
- `backend/**`
- `deploy/curis/**`
- `.github/**`
- 共享架构、部署、契约和治理文档

## 三、跨团队规则

任何跨边界修改必须先建立 Issue，并写明：

- 修改文件
- 所属团队
- 目标部署端
- 验收负责人
- 是否涉及共享后端
- 回滚方式

## 四、提交格式

```
[Admin][类型] 内容
[Workspace][类型] 内容
[Shared][类型] 内容
```

## 五、提交前检查

```bash
git diff --check
git status --short
```

禁止提交：

- `.env`
- `.sqlite`
- `.next/`
- `node_modules/`
- 缓存、日志、临时文件
- 未确认归属的文件

## 六、自动推送

首次在本地执行：

```bash
git config core.hooksPath .githooks
```

之后正常提交即可自动检查并推送。自动推送失败时，**不要重复创建提交**，先处理失败原因。

> 注：本仓库 `.githooks/post-commit` 已启用，行为为「无上游则跳过 → 校验本次提交的 `git diff --check` → 推当前分支到其上游 → 推送失败保留本地提交」。Admin 仅推送 `Admin` 分支，Workspace 仅推送 `Workspace` 分支。

## 七、Shared 修改

以下内容必须由 Admin 与 Workspace 双方确认后才能合入：

- 后端代码
- 数据库结构和迁移
- API 契约
- 部署配置
- 环境变量
- CI/CD 流程
- 共享组件和全局样式

## 八、交接格式

每次交接必须返回：

```
Issue：
本次完成：
修改范围：
验证结果：
未完成：
下一负责人：
```

## 九、阶段结束检查

每个 Issue 或里程碑结束时，确认：

- 两个分支都能构建；
- 两个环境能独立启动；
- 没有未归属文件；
- 没有未提交改动；
- 没有跨团队越界修改；
- 本地与 GitHub 分支同步。

---

## Admin 侧执行备注（齐活林组）

- 当前分支 `Admin`，上游 `origin/Admin`，自动推送已启用。
- 已冻结归档提交：`7f582676`、`f6bcb92b`、`c7b1bc2e`、`b117f5a9`、`d1cab174`、`0e967172`、`d751f8af`（不得修改或重做）。
- 既有隔离 Issue 已就位：`issues/088`（前端拆分）、`issues/089`（后端进程与 DB 隔离）、`issues/090`（构建/发布/回滚）。
- 后续 Admin 提交严格限 `frontend/app/platform/**`、Admin 平台文档、Admin 专属测试、已明确归属 Admin 的交付文件；跨边界改动一律先建 Issue。
