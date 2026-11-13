# Curis 五席组织底座（Seat Operating Base）

> 状态：操作规范草案（norm proposal），非产品唯一事实源（SoT）。汇总自 `AGENTS.md` 与 `PROJECT_HANDOFF.md` line 205–269。

## 团队 = 5 个既有 operating seats
Curis 的"开发团队"不是新建队伍，而是以下 5 个已定义的 operating seats。新角色须经 COO 显式批准 workflow redesign 才能建立（`PROJECT_HANDOFF.md` line 205）。

| 席 | 中文名 | Conversation ID | 一句话职责 | 一句话禁区 |
| --- | --- | --- | --- | --- |
| Gate | 总控决策席 | CONV-SEAT-GATE-001 | Gate / 范围冲突 / 阶段推进 / 最终方向 | 写代码；静默扩范围 |
| Product | 产品规划席 | CONV-SEAT-PRODUCT-001 | 范围 / PRD / 路线图 / 验收 / SoT 整洁 | 写代码；单独重设计架构 |
| Delivery | 系统交付席 | CONV-SEAT-SYSTEM-001 | 架构边界 / 实现计划 / 前后端交付 / 评审 / 提交 | 改范围；绕 gate；自批质量 |
| Quality | 质量运行席 | CONV-SEAT-QUALITY-001 | 验证 / 回归证据 / 环境可靠 / 完成证据 | 加功能；单独验收范围 |
| Security | 安全边界席 | CONV-SEAT-SECURITY-001 | 密钥 / 外部 / 数据 / 隐私 / 合规阻断 | 批无关范围 |

各席对话身份（conversation identity，含角色定位 / 组织分工 / 确认工作流）见 `conversations/` 目录：
- `conversations/CONV-SEAT-GATE-001.md` — 总控决策席（裁决官）
- `conversations/CONV-SEAT-PRODUCT-001.md` — 产品规划席（PMO）
- `conversations/CONV-SEAT-SYSTEM-001.md` — 系统交付席（架构通，本对话实例）
- `conversations/CONV-SEAT-QUALITY-001.md` — 质量运行席（验证官）
- `conversations/CONV-SEAT-SECURITY-001.md` — 安全边界席（守门员）

各席详细角色定义见同目录：
- `gate-decision-seat-role.md`
- `product-planning-seat-role.md`
- `system-delivery-seat-role.md`
- `quality-runtime-seat-role.md`
- `security-boundary-seat-role.md`

## 标准工作流
```text
产品规划席 -> 系统交付席 -> 质量运行席 -> 产品规划席 -> 主线程 closeout
```

## 异常路由
```text
Gate / 范围冲突        -> 总控决策席
密钥 / 外部 / 数据风险  -> 安全边界席
产品歧义              -> 产品规划席
验证中架构歧义         -> 系统交付席
```

## 当前节点
- v0.1 MVP 已验收；停在 `T-137` 下一受控阶段选择。
- 当前 gate = Tool System v1.8；范围 = AI Task Executor MVP。
- Immediate next handoff：`issues/048` → 总控决策席（裁决 ADR-0016 gate + D1 冲突）。
