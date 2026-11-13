# Curis 前端 UI 审计报告（Frozen 令牌红线）

- 目标：http://localhost:3000
- 主题：dark
- 时间：2026-08-05T17:05:18.814Z
- 结论：**error 0 · warn 1**（error 为红线违规，必须清零）

## 违规分布

| 规则 | 命中次数 |
| --- | ---: |
| R6-后端接口 | 1 |

## 分页明细

| 路由 | 页面 | 采样节点 | error | warn |
| --- | --- | ---: | ---: | ---: |
| `/` | 首页入口 | 402 | 0 | 0 |
| `/ceo-office` | 总裁办公室 | 402 | 0 | 0 |
| `/ceo-office/organization` | 组织中心 | 462 | 0 | 0 |
| `/ceo-office/organization/employees` | 员工列表 | 570 | 0 | 0 |
| `/ceo-office/projects` | 项目中心 | 312 | 0 | 0 |
| `/ceo-office/execution` | 执行工作台 | 177 | 0 | 0 |
| `/ceo-office/capabilities` | 能力中心 | 272 | 0 | 0 |
| `/ceo-office/knowledge` | 知识中心 | 217 | 0 | 0 |
| `/ceo-office/knowledge/memory` | 记忆库 | 181 | 0 | 0 |
| `/ceo-office/decisions` | 待决策 | 223 | 0 | 0 |
| `/ceo-office/reports` | 报告中心 | 245 | 0 | 0 |
| `/ceo-office/analytics` | 数据分析 | 246 | 0 | 0 |
| `/ceo-office/company-runtime` | 公司运行视图 | 187 | 0 | 0 |
| `/ceo-office/runtime-trace` | 运行轨迹 | 145 | 0 | 0 |
| `/ceo-office/strategy-room` | 战略室 | 205 | 0 | 0 |
| `/ceo-office/brainstorm` | 头脑风暴 | 199 | 0 | 0 |
| `/ceo-office/settings` | 设置 | 172 | 0 | 0 |
| `/guide` | 引导 | 122 | 0 | 0 |
| `/login` | 登录 | 7 | 0 | 1 |
| `/onboarding` | 初始化 | 26 | 0 | 0 |
| `/control/secret-vault` | 凭据保管 | 20 | 0 | 0 |

### 登录 `/login`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 404 (Not Found) · http://127.0.0.1:8000/api/auth/local/status | `-` |  |
