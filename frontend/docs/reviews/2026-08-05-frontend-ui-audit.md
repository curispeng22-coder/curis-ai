# Curis 前端 UI 审计报告（Frozen 令牌红线）

- 目标：http://localhost:3000
- 主题：dark
- 时间：2026-08-05T09:21:35.645Z
- 结论：**error 0 · warn 47**（error 为红线违规，必须清零）

## 违规分布

| 规则 | 命中次数 |
| --- | ---: |
| R6-后端接口 | 47 |

## 分页明细

| 路由 | 页面 | 采样节点 | error | warn |
| --- | --- | ---: | ---: | ---: |
| `/ceo-office` | 总裁办公室 | 256 | 0 | 3 |
| `/ceo-office/organization` | 组织中心 | 210 | 0 | 3 |
| `/ceo-office/organization/employees` | 员工列表 | 212 | 0 | 3 |
| `/ceo-office/projects` | 项目中心 | 204 | 0 | 3 |
| `/ceo-office/execution` | 执行工作台 | 210 | 0 | 3 |
| `/ceo-office/capabilities` | 能力中心 | 226 | 0 | 5 |
| `/ceo-office/knowledge` | 知识中心 | 214 | 0 | 3 |
| `/ceo-office/decisions` | 待决策 | 293 | 0 | 2 |
| `/ceo-office/reports` | 报告中心 | 321 | 0 | 2 |
| `/ceo-office/analytics` | 数据分析 | 251 | 0 | 5 |
| `/ceo-office/company-runtime` | 公司运行视图 | 273 | 0 | 3 |
| `/ceo-office/runtime-trace` | 运行轨迹 | 216 | 0 | 3 |
| `/ceo-office/strategy-room` | 战略室 | 281 | 0 | 2 |
| `/ceo-office/brainstorm` | 头脑风暴 | 251 | 0 | 2 |
| `/ceo-office/settings` | 设置 | 254 | 0 | 2 |
| `/guide` | 引导 | 198 | 0 | 1 |
| `/onboarding` | 初始化 | 25 | 0 | 1 |
| `/control/secret-vault` | 凭据保管 | 21 | 0 | 1 |

### 总裁办公室 `/ceo-office`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/home/summary | `-` |  |

### 组织中心 `/ceo-office/organization`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/companies | `-` |  |

### 员工列表 `/ceo-office/organization/employees`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/employees | `-` |  |

### 项目中心 `/ceo-office/projects`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/companies | `-` |  |

### 执行工作台 `/ceo-office/execution`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/tasks | `-` |  |

### 能力中心 `/ceo-office/capabilities`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/capabilities/registry?include_inactive=true | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/private-models | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/capabilities/private?capability_type=agent | `-` |  |

### 知识中心 `/ceo-office/knowledge`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/knowledge/entries | `-` |  |

### 待决策 `/ceo-office/decisions`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |

### 报告中心 `/ceo-office/reports`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |

### 数据分析 `/ceo-office/analytics`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/departments | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/employees | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/projects | `-` |  |

### 公司运行视图 `/ceo-office/company-runtime`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/capabilities/registry?include_inactive=false | `-` |  |

### 运行轨迹 `/ceo-office/runtime-trace`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/runtime-trace?limit=100 | `-` |  |

### 战略室 `/ceo-office/strategy-room`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |

### 头脑风暴 `/ceo-office/brainstorm`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |

### 设置 `/ceo-office/settings`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/snapshot | `-` |  |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/assistant/notifications?after_event_id=0 | `-` |  |

### 引导 `/guide`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/guides | `-` |  |

### 初始化 `/onboarding`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/workspace/companies | `-` |  |

### 凭据保管 `/control/secret-vault`

| 级别 | 规则 | 详情 | 元素 | 文本 |
| --- | --- | --- | --- | --- |
| warn | R6-后端接口 | Failed to load resource: the server responded with a status of 500 (Internal Server Error) · /gateway/api/credential | `-` |  |
