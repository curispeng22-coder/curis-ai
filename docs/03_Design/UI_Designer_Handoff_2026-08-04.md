# UI 设计师交接指令 · 第一版 Desktop 前端接入（2026-08-04）

> 交接方：系统交付席（后端 + 前端壳已接真实数据）
> 接收方：UI 设计师（当前在做 UI 重审）
> 目标：两边对齐后，前端按此清单接入第一版 Desktop；本指令列出「前端已实现但需要你重审/定稿」的视觉点 + 对应 API 契约。
> 关联：UI 重审材料 `docs/03_Design/Curis_UI_Review_2026-08-04.md`、`docs/03_Design/Curis_Workspace_Shell.md`、`docs/reviews/2026-08-04-curis-ui-audit-report.md`

---

## 1. 背景

后端能力层已闭环（Step5 多网关 / 私有模型 Agent 桥 / 业务工作台引导 / 经营日聚合 / 岗位级授权 / 运行轨迹），前端已接真实数据的页面：CEO Office（home/summary + operating-day）、能力中心（selector 含 effect_class）、运行轨迹（runtime-trace 只读）、业务引导向导（/guide）、员工能力绑定（岗位授权校验）。

**目标**：第一版 Desktop = 以上页面按 Frozen 设计系统（`docs/03_Design/Curis_Design_System.md`）定稿，UI 重审通过后前端完成最终视觉接入。

## 2. 需要 UI 设计师定稿/重审的视觉点（按优先级）

### P0（本次新增，需视觉规范）

| # | 视觉点 | 现状（前端实现） | 请 UI 定稿 |
|---|---|---|---|
| 1 | **effect_class 副作用标签** | 能力中心卡片显示「副作用面：read/retrieve/write/exec」纯文本；向导蓝图确认处岗位旁显示授权小胶囊 | 标签的语义色/图标（如 read=绿只读、write=琥珀写、exec=红执行）、展示位置、中英文对照 |
| 2 | **经营日卡片（CEO Office）** | 「今日经营概览」卡片：brief 摘要 + matters 彩色 Tag（risk=红/attention=琥珀/info=绿）+ pulse 5 项指标小格（含 ↑↓ 趋势） | 卡片层级（是否置顶）、指标格视觉（环形/条形/数字）、matters 分级样式 |
| 3 | **运行轨迹只读视图** | `/ceo-office/runtime-trace`：事件行（类型 Tag + 能力名 + 时间 + token/缓存/延迟 meta） | 事件行密度、时间线形态（是否分组/分页）、token/缓存字段的呈现 |
| 4 | **业务引导向导页（/guide）** | 四阶段：选模板 → 对话（textarea + 追问）→ 蓝图确认（表单 + 岗位授权胶囊）→ 成功 | 向导进度指示（步骤条？）、对话 vs 表单切换的视觉一致性、manual_fallback 兜底态 |
| 5 | **onboarding 双选择** | 保存公司后「进入总裁办公室 / 创建业务工作台（引导）→」两个按钮 | 主次按钮层级、引导入口的引导性（是否更突出「创建业务」） |

### P1（既有页面，重审同步）

| # | 视觉点 | 现状 | 请 UI 定稿 |
|---|---|---|---|
| 6 | 能力中心卡片 | 已含 effect_class 文本（见 #1） | 与重审报告的分组/密度对齐 |
| 7 | 员工能力绑定错误 | 岗位授权拒绝时中文友好提示 | 错误态视觉（是否用 TerraBoundary 规范） |

## 3. API 契约（供 UI 理解数据形态，前端已按此渲染）

### 3.1 CEO 经营日 `GET /api/workspace/ceo/operating-day`

```json
{
  "company_id": "...", "date": "2026-08-04", "period": "day:2026-08-04",
  "brief": { "summary": "1 个项目活跃；任务完成率 66.7%；…", "generated_at": "..." },
  "matters": [ { "level": "risk|attention|info", "severity": "high|medium|low",
                 "metric_key": "blocked_tasks", "message": "1 个任务受阻，需要处理" } ],
  "timeline": [ { "at": "...", "type": "task|workflow|artifact", "title": "...", "ref": "..." } ],
  "pulse": [ { "metric_key": "task_completion_rate", "value": 66.7, "unit": "%", "trend": "up|down|flat" } ],
  "handoffs": []
}
```

### 3.2 运行轨迹 `GET /api/workspace/runtime-trace?limit=100&run_id=...`

```json
{ "events": [ { "id": "tr-...", "run_id": "...", "task_id": "...", "task_ref": "...",
  "event_type": "model_call|tool_call|workflow|task", "capability": "...",
  "tokens_in": 10, "tokens_out": 20, "cache_hit": true, "latency_ms": 123,
  "payload": {}, "created_at": "..." } ] }
```

### 3.3 能力 selector（含 effect_class）`GET /api/workspace/capabilities/selector`

```json
{ "capabilities": [ { "capability_id": "...", "capability_type": "model|agent|tool|...",
  "label": "...", "source": "official|tenant_private", "enabled": true,
  "effect_class": "read|retrieve|write|exec" } ] }
```

### 3.4 业务引导 `GET/POST /api/workspace/guides*`

- `POST /sessions` → step（free_form/confirm）
- `POST {id}/answer` → `{mode: follow_up|blueprint|manual_fallback, ...}`
- `POST {id}/confirm` → `{workbench: {project_id, project_name, department_ids, employee_ids, owner_employee_id}}`

## 4. 与 UI 重审的衔接

- 重审报告（`2026-08-04-curis-ui-audit-report.md`）聚焦原型（curis-ui-prototype/）P0 三项（令牌/Shell/术语）；本指令的 5 个 P0 视觉点**是前端接入后的新增表面**，不在原型里——请并入重审范围一起定稿。
- 设计令牌：前端已用 `terra-*` 类（Frozen Design System 语义）；本指令新增表面（标签/卡片/轨迹行）请用同一令牌体系，不引入新私有调色板。
- 术语：新增表面沿用「投入产出/工作指标」等已冻结中文映射（effect_class 显示建议中文：只读/检索/写入/执行）。

## 5. 验收口径

UI 重审通过 + 前端按定稿接入后，第一版 Desktop 的验收 = 用户能在浏览器完成：创建公司 → 引导创建业务（生成项目/部门/员工）→ CEO Office 看到真实经营概览 → 能力中心查看能力与岗位授权 → 运行轨迹回看执行过程。
