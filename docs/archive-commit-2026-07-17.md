# 2026-07-17 项目空间归档与提交记录

## 已完成提交

| 提交 | 归属 | 内容 |
|---|---|---|
| `7f582676` | Admin / QA | Wave-1、Wave-2 与员工目录测试证据 |
| `f6bcb92b` | Admin / 文档 | PRD、研究、计划、产品文档与架构图 |
| `c7b1bc2e` | Admin / UI | `.agents/skills/` 设计技能库 |
| `b117f5a9` | Admin / 交付 | 记忆、空间确认文档、Issue 088/089/090 |
| `d1cab174` | Admin / 前端 | `frontend-admin/` 源码与配置 |
| `0e967172` | Shared / 隔离 | 双进程后端、部署脚本、CI 配置 |
| `d751f8af` | Admin / 交付 | 本阶段提交记录补记 |

## 尚未归档

- `frontend-workspace/`：Workspace 接收，禁止 Admin 修改。
- `frontend/app/employees/page.js`：Workspace 接收，当前仍有未提交改动。
- `Curis AI Workspace Worktrees/`：Codex / 总控确认后处理。
- `data/admin.sqlite.pre-split`、`data/workspace.sqlite.pre-split`：隔离前备份，确认发布稳定后再清理。
- `knowledge/NOW.md`、`data/sample_publish_package.md`、`skills-lock.json`：待归属确认。

## 规则

- 新前端构建产物、依赖目录和发布包不进入 Git。
- Admin 与 Workspace 不互改对方页面。
- `backend/` 和 `deploy/curis/` 的跨团队修改必须先建 Issue。
- 当前文档只记录归档事实，不授权继续开发。
