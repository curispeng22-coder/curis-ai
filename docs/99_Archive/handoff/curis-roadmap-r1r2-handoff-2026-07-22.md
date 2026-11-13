# Curis Roadmap R1R2 交接文档

Status: Deprecated

> **文档类型**：开发交接（Handoff）
> **编制**：软件开发团队（主理人 齐活林 / 交付总监）
> **日期**：2026-07-22
> **交接对象**：接手后续 roadmap（R3/R4+）的原开发团队 / 后续维护者
> **对应分支**：`feat/roadmap-r1r2`（已推 `origin/feat/roadmap-r1r2`）
> **范围**：Roadmap R1R2 的 P0（自动任务流核心闭环 + 极简前端）+ P1（适配器抽象 / 员工=能力组合 / 外部 Agent 接入）+ 验证①②③④

---

## 一、背景与产品基准（不可动摇）

Curis = 一人公司的自动任务与工作流系统。三层架构 + 四条原则：

- **组织层**：公司 → 部门 → 项目 → 员工（研发部为首个验证部门）
- **运行层（核心）**：目标澄清 → 规划 → 动态任务图 → 队列 → 调度 → 执行 → 验收 → 返工 → 完成（支持固定/自主/混合/重规划/定时事件条件触发）
- **能力层**：Agent / 模型 / Skill / Tool / MCP / CLI / API / Workflow，经 CLI/HTTP/MCP/Webhook/Local 适配器接入
- **四条原则**：① 全自动任务流是核心，组织只是管理方式；② 能力可替换不写死具体产品；③ 员工非固定 Agent，是动态调用能力的岗位（职责+目标+权限+项目上下文+记忆+可用能力）；④ 任何开发须让「目标→执行→验收→返工→完成」更自动

**当前阶段 ONLY 做**：后端 7 项能力（目标澄清规划 / 动态任务图 / 队列调度 / 统一能力注册与路由降级 / Agent 等替换降级 / 验收重试返工 / 项目状态与经验沉淀）+ 能力路由降级；前端仅极简 6 步入口。CEO Office / 员工形象 / 复杂看板 / 组织树美化一律后置。

---

## 二、本次交接范围

| 项 | 内容 | 提交 | 状态 |
|----|------|------|------|
| P0 | 自动任务流核心闭环 + 极简前端 6 步入口 | `3ab5257d` | 已提交已推 |
| ③ | 增强 NLParser 规划器（自然语言拆有意义 DAG） | `aa9c5bc5` | 已提交已推 |
| P1 | 适配器抽象 + 员工=能力组合 + 外部 Agent 统一接入（T08/T09/T10） | `2f7480c7` | 已提交已推 |
| ④ | 降级实测端到端 + 节点 trace 可观测 | `d47cac5b` | 已提交已推 |
| ① | 联调验证 P0 后端 + 极简前端（已实跑通过） | — | 验证完成，未单独提交（属 P0 验证） |
| ② | 提交 P0 代码 | `3ab5257d` | 已提交已推 |

**验证闭环**：①②③④ 全部闭合。①②联调验证通过（`/health` ok、`/api/tasks` 200、前端 3000 渲染+身份头正确）；③ 已提交；④ 降级实测端到端 3 测试通过。

---

## 三、已完成交付清单（按能力模块）

### 3.1 P0 — 自动任务流核心闭环
- `CapabilityResolver`：能力静默降级（按 `backup_chain` 逐候选尝试，全部失败→升级 CEO）
- `task_graph`：DAG 任务图（节点/边/状态机）
- `scheduler`：常驻调度器（轮询执行就绪节点）
- `pipeline_runtime`：验收返工闭环（`ResultReviewer` 验收→失败重试→升级）
- `project_state` + `lesson_memory`：项目状态与经验沉淀（`capability_lessons` 表）
- `capability_catalog`：统一注册表（落 `official_models` 表，`runtime_meta_json` 列）
- 极简前端 6 步入口：`frontend/app/page.js`（输入目标→看计划→启动→看进度→处理决策→看成果）

### 3.2 ③ — NLParser 规划器增强
- 自然语言目标 → 有意义 DAG（非机械拆分）
- 提交 `aa9c5bc5`

### 3.3 P1 — 适配器抽象 / 员工=能力组合 / 外部 Agent 接入
- **T08 统一 `CapabilityAdapter` 协议** + 四大适配器（Cli / Http / Webhook / Mcp）+ `UnconfiguredAdapter` + `CapabilityAdapterFactory`
- **T09 员工=能力组合**：`employee_capabilities` 表 + `EmployeeCapabilityModel` + resolver 按 `employee_id` 过滤/首选
- **T10 外部 Agent 统一接入**：`CapabilityCatalog.register_external_agent`（仅能力层登记，零代码改动，严守 L2 红线）
- 设计契约：`docs/architecture/curis-p1-adapters-arch.md`（权威）、`docs/design/p1-adapters/{class-diagram,sequence-diagram,system_design}.md`

### 3.4 ④ — 降级实测端到端 + 可观测
- `TaskNode` 新增 `capability_path` / `trace` 字段
- `PipelineRuntime.run_node` 每次尝试写入节点 trace（含降级事件）
- 新增 `GET /api/pipeline/{graph_id}/trace` 端点
- 测试 `backend/tests/test_roadmap_degrade_e2e.py`：耗尽→升级、节点 trace 记录降级链、经验沉淀成功/失败路径

---

## 四、关键架构与设计决策（接手必读）

1. **`UnconfiguredAdapter` 取代 P0 的 `NullDevAgent`（恒 success）**
   非 model 类型无真实适配器时**明确失败** → 触发 resolver 静默降级（而非假装成功）。这是「降级链/升级真正生效」的前提，符合第四条原则。

2. **密钥零明文**
   仅 `credentials_ref: "env:XXX"` 形态，运行时从 `os.environ` 取（`capability_adapters._resolve_credentials_env`）。绝不落明文。

3. **外部 Agent 接入零代码改动（L2 红线）**
   `register_external_agent` 仅登记能力层 `ext.{name}`，**绝不**转成 Package/Department/Employee/Skill/Workflow 资产。`kind` 不能是 `model`/`agent`（走既有模型网关，会被拒 422）。

4. **员工=能力组合穿透选路**
   `employee_id` 从 `TaskNode` → `pipeline_runtime.run_node` → `resolver.resolve(employee_id=)` → `EmployeeCapabilityModel` 取组合 keys 集与 preferred；候选可见性过滤 + 首选偏好，保留静默降级到 `backup_chain`。

5. **降级链可观测**
   `TaskNode.capability_path`（tried 链）+ `trace`（每次尝试事件：tool/status/error/output）。前端「工具追踪与降级」区消费 `trace`，但当前前端查的是 `main.py` 的 task 体系（见 §八设计债）。

---

## 五、关键文件清单

### 新增文件
- `backend/app/capability_adapters.py` — 统一适配器协议 + Cli/Http/Webhook/Mcp/Unconfigured + Factory
- `backend/app/employee_capability_model.py` — 员工能力组合读写
- `backend/tests/test_p1_adapters.py` — P1 联调测试（19 用例，即本地联调载体）
- `backend/tests/test_roadmap_degrade_e2e.py` — ④ 降级实测端到端（3 用例）
- `docs/architecture/curis-p1-adapters-arch.md` — P1 权威设计契约
- `docs/design/p1-adapters/{class-diagram,sequence-diagram,system_design}.md` — 类图/时序图/补充设计

### 修改文件（本次 roadmap scope）
- `backend/app/database.py` — +`employee_capabilities` 表 + `replace/list/get_preferred` 三方法（幂等）
- `backend/app/capability_catalog.py` — 恢复 `get` + 新增 `register_external_agent`
- `backend/app/capability_resolver.py` — `resolve(employee_id=)` 过滤/首选 + 引用 `CapabilityAdapterFactory`
- `backend/app/dev_agent.py` — `DevAgentFactory` 迁移至此供 adapters 复用
- `backend/app/main.py` — `POST /api/platform/capabilities/external-agent` 端点 + `ExternalAgentRegisterIn` 模型
- `backend/app/pipeline_runtime.py` — `employee_id` 透传 + 节点 trace 写入
- `backend/app/task_graph.py` — `employee_id` / `capability_path` / `trace` 字段透传
- `backend/app/issue_pipeline_api.py` — `GET /api/pipeline/{graph_id}/trace` 端点
- `frontend/app/page.js` — 极简 6 步入口（含「工具追踪与降级」区，数据来自 `/api/task/{id}/trace`）

---

## 六、如何运行与联调

### 6.1 后端（uvicorn，端口 8000）
```bash
cd "/Users/yy/Documents/Curis AI Workspace/backend"
CURIS_IDENTITY_MODE=selfuse CURIS_PLATFORM_ADMIN_TOKEN=devtoken \
  /Users/yy/.workbuddy/binaries/python/envs/default/bin/python -m uvicorn app.main:app \
  --host 127.0.0.1 --port 8000
```
> 托管 Python venv（`/Users/yy/.workbuddy/binaries/python/envs/default`）已含 uvicorn 0.51.0。

### 6.2 前端（Next dev，端口 3000）
```bash
cd "/Users/yy/Documents/Curis AI Workspace/frontend"
PATH="/Users/yy/.workbuddy/binaries/node/versions/22.22.2/bin:$PATH" \
  node node_modules/.bin/next dev -p 3000
```
> 前端 `frontend/app/page.js` 直连后端 `http://127.0.0.1:8000`（默认 `NEXT_PUBLIC_API_BASE` 未设时），`apiHeaders()` 已带 `X-Tenant-Id: selfuse` + `X-Ceo-Id`。

### 6.3 身份前提（坑点）
- 环境变量 **`CURIS_IDENTITY_MODE=selfuse`**（必须在 import app 之前设）
- 每个请求带 header **`X-Tenant-Id: selfuse`**，否则一律 `401 trusted_identity_missing`
- 平台管理员端点额外需 `CURIS_PLATFORM_ADMIN_TOKEN` + `Authorization: Bearer <token>`（或 `X-Platform-Admin-Token`）

### 6.4 本地联调脚本（已实跑验证）
- `backend/tests/test_p1_adapters.py`：真实 subprocess CLI、本地 http.server 回环、Mcp stdio JSON-RPC、员工选路、降级 backup —— **19 passed**
- `backend/tests/test_roadmap_degrade_e2e.py`：耗尽→升级、trace 记录、经验沉淀 —— **3 passed**
- `/tmp/curis_e2e_p1.py`（临时，未入库）：FastAPI `TestClient` 驱动 `/health`→`/submit`→`/graph`→`/auto-run`→轮询→`/lessons` 全链路，等价于真机 HTTP

### 6.5 登记外部 Agent（T10 真·配置化接入）
```bash
curl -X POST http://127.0.0.1:8000/api/platform/capabilities/external-agent \
  -H "X-Tenant-Id: selfuse" -H "Authorization: Bearer $CURIS_PLATFORM_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-cli-agent","kind":"cli","config":{"command":"python","args":["-c","print(\"diff ok\")"]},"backup_chain":[],"credentials_ref":"env:MY_TOKEN"}'
```

---

## 七、测试状态

| 套件 | 用例数 | 结果 | 说明 |
|------|--------|------|------|
| `test_p1_adapters.py` | 19 | ✅ passed | P1 联调（含真实 CLI/HTTP/Mcp/员工选路/降级） |
| `test_roadmap_degrade_e2e.py` | 3 | ✅ passed | ④ 降级实测端到端（耗尽升级/trace/经验沉淀） |
| 后端 `app.main` 加载 | 160 routes | ✅ OK | 无导入错误 |

**回归**：④ 提交后重跑 P1 套件，19 passed 无回归。

---

## 八、已知问题 / 设计债（非阻断，接手须知）

1. **任务体系双轨未打通（前端降级可视化暂空）**
   前端「工具追踪与降级」查 `main.py` 的 `/api/task/{id}/trace`（依赖 `tool_traces` 表，带 `references tasks` 外键）；而 pipeline 是 `graph_id` 体系，两套未打通。硬接会撞 FK 且前端查不到。
   **现状**：后端闭环已完整可观测（走 `GET /api/pipeline/{graph_id}/trace`）；前端降级可视化暂空。
   **建议**：pipeline/task 体系打通时统一做，不急。

2. **selfuse 环境无真实模型 key**
   无真实 key 时节点走到「降级耗尽 → 升级 CEO」——这是设计意图（验证降级机制），非 bug。真实执行需配 `CURIS_PLATFORM_ADMIN_TOKEN` + 模型 key。

3. **子代理分发通道故障（已文档化 fallback）**
   本会话 engineer/QA 子代理分发曾收空 prompt（平台故障，同 2026-07-11 记录）。P1/④ 由主理人持设计契约直接实现 + 自验，功能等价于标准 SOP。框架恢复后后续 slice 可换回指定成员。详见 §十一。

4. **工作树大量未提交改动不属于本范围**
   当前 303 个未提交改动（R3/R4 issues、dept_catalog、前端构建产物、memory 等）**均非本次 roadmap 交付**，按 Git 基线纪律未混入 roadmap 提交，由各自 issue/团队处理。

---

## 九、L2 红线与未决 Gate（越界须升总控 + 安全边界席）

- ❌ 新商业包（ccp_/ct_/dt_/et_/skl_ai_commercial_* 补全）→ L2 #1/#2/#3
- ❌ Marketplace（外部能力对外提供）→ L2 #4
- ❌ 收费体系（cmcf_* 解冻、定价/计费/配额）→ L2 #1/#2
- ❌ 外部 Agent **批量导入**成 Package/Department/Employee/Skill/Workflow 资产 → L2 #3/#4/#5/#6（T10 仅做能力层配置化登记，不导入）
- ❌ 真实计费 / payment / invoice / 多租户商业化
- ⚠️ `tenant_id` 预留已实现（D1 committed）；D2 部门目录通用化实现中（Kou T01–T05）；D3 自可观测、D4 两级治理待各自边界后走自主管线
- 飞书仅升级事件推送（群 `oc_1b559ad633e40345229275d15f7e8d42`），常规阶段汇报不再打扰

---

## 十、后续建议（接手团队参考）

1. **R3/R4 协作保障态**：R1/R2 已合入，进入 R3 协作保障（不做新功能，值守 shared issues）。新功能开发需新开 gate。
2. **前端接员工选路展示**：极简前端可展示员工能力组合驱动的选路结果（需先打通 §八.1 任务体系）。
3. **pipeline/task 体系打通**：统一 trace 存储，让前端降级可视化生效。
4. **外部 Agent 多源接入 gate**：CrewAI / skill 仓库 / Coze-Dify / MCP Registry 扩展仍待后续 gate（非本次范围）。
5. **真实降级实测**：配真实凭证后跑 `ext.*` 首选失败→降级 backup 真实 CLI/model，验证生产级闭环。

---

## 十一、子代理分发故障与 Fallback 说明（供接手团队知晓）

- **现象**：TeamCreate 后派发的 engineer/QA 子代理收到空 prompt（`undefined`），报 `500 internal server error`。同 2026-07-11 记录的 Agent 框架故障模式。
- **处置**：按已文档化 fallback，P1/④ 由主理人持 `docs/architecture/curis-p1-adapters-arch.md` 设计契约直接实现 + 自验（等价于标准 SOP 的 T08-1→T10-1 全实现）。团队清理（`TeamDelete`）已执行。
- **恢复**：框架恢复后，后续 slice 应换回指定成员（`software-engineer` / `software-qa-engineer` 等），走正常 SOP 中转。

---

## 附录 A：提交清单（已推 origin/feat/roadmap-r1r2）

| Hash | 标题 |
|------|------|
| `3ab5257d` | feat(roadmap): 自动任务流核心闭环 + 极简前端 6 步入口 |
| `aa9c5bc5` | feat(roadmap): 增强 NLParser 规划器，自然语言拆成有意义 DAG |
| `2f7480c7` | feat(roadmap): P1 适配器抽象 + 员工=能力组合 (T08/T09/T10) |
| `d47cac5b` | feat(roadmap): ④ 降级实测端到端 + 节点 trace 可观测 |

## 附录 B：关键设计文档索引

- `docs/architecture/curis-p1-adapters-arch.md` — P1 权威设计契约（T08/T09/T10、runtime_meta 扩展、任务分解、红线）
- `docs/design/p1-adapters/{class-diagram,sequence-diagram,system_design}.md` — 类图/时序图/补充设计
- `docs/team/*` — 席位分工（总控/产品规划/系统交付/质量运行/安全边界）
- 运营协定 v2（2026-07-11 起）：席位链、L2 Gate、汇报规范、前端分工边界

---

*编制：齐活林（交付总监）/ 软件开发团队 — 2026-07-22*
*本交接文档覆盖 roadmap R1R2 全部已交付与验证内容，未提交工作树改动不属本范围。*
