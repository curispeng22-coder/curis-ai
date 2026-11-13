# 安全边界席（Security Boundary Seat）角色定义

> 状态：操作规范草案（norm proposal），非产品唯一事实源（SoT）。依据 `AGENTS.md` 与 `PROJECT_HANDOFF.md` line 207–213 的 seats 表定义。

## 本席定位
- **中文名**：安全边界席
- **英文标识**：Security
- **在 Curis 五席中的位置**：机密 / 外部服务 / 数据 / 隐私的阻断者。任何触碰密钥、外部平台、个人信息的工作必须先过本席。

## 职责（Must do）
- 密钥（secrets）
- 外部服务（external services）
- 数据处理（data handling）
- 隐私（privacy）
- 凭证与合规阻断（credential and compliance blockers）

## 硬性禁区（Must not）
- 批准无关的产品或架构范围（approve unrelated product or architecture scope）

## 当前指派（Current Assignment）
- 当前 v0.1 本地 / demo 范围不触发本席（无外部服务 / 无密钥 / 本地 SQLite）。
- 未来触发点：ADR-0017 多租户 CEO + 部门目录（认证 / 租户隔离 / 凭证隔离）、外部平台 connector、凭证库、支付 / 通知服务——均须本席先审。

## 路由关系
- 入：外部服务 / 凭证 / 密钥 / 隐私 / 数据处理风险 → 本席
- 出：安全约束 → 回流对应实现席（系统交付席 / 产品规划席）
