# CURIS — BUSINESS WORKING SPACE BASELINE（候选）

**Authority Class**: `RESEARCH` — Candidate / Reconciliation（**非 Authority；不得作为 Current Product / Implementation Truth 引用**）
**Status**: `Review`
**Round**: BUSINESS WORKING SPACE BASELINE RECONCILIATION
**Date**: 2026-09-20
**上游**：`docs/research/rd-multi-agent-development/CURIS_RD_MULTI_AGENT_ORCHESTRATION_CONCLUSIONS.md`（RD Project Working Space = 本模型下的 **Development 特化**）
**本轮边界**：只允许 **RECONCILE / MODEL / DOCUMENT**。
**未做（逐条）**：未重新研究 Multi-Agent；未做 GitHub 泛搜；未改 RD HTML；未创建任何真实目录；未改 Authority / Runtime / Code / Schema / DB；未 commit；未 push。

> **怎么读**：§0 是给 CEO 的一页结论；§1–§2 决定命名口径（**必读，否则后面的"Workspace"会指三个东西**）；§3–§5 是模型主体；§6–§13 逐条回答本轮 20 问；§14 是需要裁定的 Gate；§15 是如实保留的限制。

---

## 0. 一页结论

1. **采纳 CEO 裁定：每创建一个 Business，Curis 自动创建一个持久本地 Business Working Space。** 它是该 Business 全部长期业务资产（文档 / 研究 / 设计 / 代码 / 素材 / 产出 / Result 文件 / Evidence）的**物理归属**。
2. **裁定的真正重点是"否认句"**：**Employee / Conversation / Work / Execution / Provider 都不拥有业务资产。** 归属权只有一层——Business。其余五者要么是**责任**（Employee）、**关系**（Conversation）、**工作事实**（Work）、**过程**（Execution）、**能力**（Provider）。
3. **命名必须立即分叉，否则必然出错**：本模型下"Workspace"会同时指 **①运行空间（现有 `workspaces` 表）②执行工作区（RD per-Work worktree）③业务资产空间（本模型）**。建议**裸词 Workspace 只保留给①**，②改称 **Execution Workspace**，③用 **Business Working Space / `business_root`**。→ **Gate G1**
4. **目录层级：逻辑上承认 `Company → Department → Business`，物理上建议 Business 平铺。** 因为**路径一旦编码部门，跨部门调整就变成一次物理搬迁**；而部门归属在 DB 里只是一条绑定。→ **Gate G4**
5. **身份与名字必须分离。** `display_name` 可改；**资产归属键不可随改名变化**；**任何代码不得用名字拼路径，只能经绑定记录解析**。用户手动改名/移动**不可阻断**，只能被检测与找回。→ **Gate G3**
6. **Shared Base + Professional Package 两层，且 Professional Package 应当复用库里已有的 `curis.workspace-package/v2`（含 manifest / surfaces / schemas / digest / migration / rollback），不新建第二套包系统。** 需要新增的只是一个**声明式资产布局段**（候选 `assetLayout`）。→ **Gate G6**
7. **库内已有正确分工的样板**：`knowledge_entries`（`source_type='local_file'` + `source_path` + `content_sha256`）就是"**文件内容在文件系统、身份与关系在 DB**"的现成形态；应把它推广成通用规则，而**不是**把文件内容复制进 DB。
8. **执行区与资产区必须分离**：失败 Execution 的产物**永不进入正式资产目录**（`_runs/` 可整体销毁）；只有经过 Verification 的产出才**提升（promote）**为资产。→ **Gate G5**
9. **Git / Branch / Worktree / Repository 不是全局 Business 概念。** 全局只定义"专业包可以声明该业务的资产受版本控制"这一**能力位**；Git 语义属于 Development 专业包。→ **Gate G2**
10. **`Adopt Existing Folder`（原地纳管）应作为默认路径，而不是复制全部文件。** 库里已有先例（`KnowledgeService` 的 `local roots`：解析真实路径、按路径哈希做 id、只读、白名单后缀、限额）。RD 的 Canonical Project Root **应当能直接落在用户既有的代码目录上，不重新 clone**。
11. **本轮不需要开发、不需要视觉、不需要 Authority 改动就能成立**；需要的是 **8 项 Gate 裁定**（§14），裁定后才谈实现与 RD 视觉修订。

**状态**：`BUSINESS WORKING SPACE BASELINE CANDIDATE COMPLETE — READY FOR CEO REVIEW`

---

## 1. 本轮性质与范围

| 项 | 内容 |
|---|---|
| **要解决的唯一问题** | Curis 所有 Business 的**长期本地资产空间**应该如何定义 |
| **不解决** | Multi-Agent 编排机制（已完成，RD 报告）、Git 隔离机制（已裁定）、UI / Figma / 视觉、Runtime 实现、DB Schema 落地 |
| **输入** | CEO 本轮 16 条裁定 + `CURIS_RD_MULTI_AGENT_ORCHESTRATION_CONCLUSIONS.md` + 既有 Curis 权威（只读） + 现有 `backend/app` 代码（L2 证据） |
| **输出** | 本文件一份（**不生成大量重复文档**）+ 在 RD 结论文档追加一节 `Global Business Working Space Boundary` |
| **证据等级** | 沿用 RD 报告口径：`L1` 本地真实运行 → `L2` 源码 → `L3` 官方文档 → `L4` 官方产品说明 → `L5` 第三方 → `L6` 推断。本轮**未做 L1**（用户明确禁止创建真实目录），主力证据为 **L2 源码** + **既有权威 L3**。 |

### 1.1 本轮实际读到的实现证据（L2，`backend/app`，2026-09-20 工作树）

| 证据 | 位置 | 说明了什么 |
|---|---|---|
| `WorkspacePackageRuntime`（2887 行） | `backend/app/workspace_package_runtime.py` | **已有"工作空间包"机制**：声明式包 + 安装/更新/回滚/卸载/生命周期/导航 |
| 包 schema `curis.workspace-package/v1` `…/v2` | 同上 `PACKAGE_SCHEMA*` | 包格式已版本化 |
| 包存储根 `CURIS_WORKSPACE_PACKAGE_STORE`，默认 `<db_dir>/workspace-packages` | 同上 `__init__` | **已有本地文件系统根**，且默认跟随 DB 目录 |
| 内容寻址存储 `<store>/<packageId>/<version>/<digest>` + digest 校验 + 冲突报错 | `_store_package()` | **模板共享、按内容寻址、不可变**——包不是业务资产 |
| `installed_workspace_packages`（`(tenant_id, package_id, version)` 主键，含 `source_path` / `stored_path` / status `ACTIVE∨DISABLED∨UNINSTALLED∨BROKEN`） | `PACKAGE_DDL` | 包是**租户级共享**实体 |
| `workspace_package_instances`（`instance_id` / `company_id` / `workspace_id` unique / `package_id` / `package_version` / `package_digest` / status） | `PACKAGE_DDL` | **实例绑定到 company + workspace**——"模板 ↔ 实例"分层已在库里 |
| `workspace_package_objects` / `_activities` / `_lifecycle_events` | `PACKAGE_DDL` | 包内对象 + 活动 + **生命周期审计事件**已有 |
| `install(source, company_id, department_id, business_id, business_name, …)`，且校验 `canonical business identity and name are required` | `install()` | **`business_id` 已被当作 canonical 业务身份键**，且 install 已带 `department_id` |
| `uninstall()`：把 `stored_path` 移到 `.staging/uninstall-<uuid>` → 成功后 `rmtree`，失败则移回 | `uninstall()` | **已有"先暂存再删除 + 失败回滚"的安全删除模式**（也见 RISK-1） |
| `_remove_unreferenced_target()`：**先查 DB 引用，无引用才删**，并清理空父目录 | `_remove_unreferenced_target()` | 库里**已有"删除前查引用"的正确实现** |
| `ResultStore`：task / artifact / execution / trace / workflow / failure_log / tool_performance | `backend/app/result_store.py` | Result / Execution / Evidence-类记录**已是 DB 对象** |
| `artifacts` 表含 `content text` + `content_sha256` | `database.py:257` | ⚠️ **现有实现会把（小）制品内容存进 DB**——见 §8 边界规则 |
| `knowledge_entries`：`company_id` / `target_type` / `target_ref` / `source_type(manual∨local_file)` / `source_path` / `content_sha256` / `department_id` / `project_id` | `database.py:1086` | **外部本地文件"原地登记 + 摘要"的现成形态** |
| `KnowledgeService.CANONICAL_TARGETS = {"COMPANY","BUSINESS","WORKSPACE"}` | `knowledge_service.py:16` | **资产归属层的实现事实只有三层：Company / Business / Workspace；没有 DEPARTMENT** |
| `KnowledgeService` 本地根：`CURIS_KNOWLEDGE_ROOTS`（`os.pathsep` 分隔）、`resolve(strict=True)`、**按路径 sha256 前 16 位做 `root_id`**、只读、后缀白名单 `.md/.txt`、单文件 2MB、200 文件上限 | `knowledge_service.py:585-637` | **"原地纳管不复制"在 Curis 已存在**；且**身份用哈希而非名字** |
| `typed_object_references`（company_id / workspace_id / source_type·ref / relation / target_type·ref，唯一约束） | `database.py:1108` | **通用类型化关系层已存在**，注释明确"不成为第二套 Work/Context/Citation 系统" |
| `companies` 表：`company_id` / `name` / `status` / `default_department_ids_json` / **无任何路径字段** | `database.py:961` | **业务实体目前完全没有文件系统绑定**——本模型是从 0 到 1 |
| `departments` 表：`department_id` / `type_key` / `display_name` / `status` | `database.py:493` | 部门是**类型化**的（`type_key`），不是任意目录 |
| `workspaces` 表：`workspace_id` / **`business_id`** / `blueprint_json` / `status` / 三道门禁位 | `runtime/models.py` | **运行空间挂在 business 上**，与"Business 拥有资产"方向一致 |
| `commitments`：`business_id` + `department_id` + `workspace_id` | `runtime/models.py` | 承诺是"部门对业务的责任约定"，**部门通过承诺参与业务，而不是拥有业务目录** |
| `outcomes`：`business_id` / `run_id` / `evidence_ref` / `evidence_type` | `runtime/models.py` | **对外结果已带 evidence 引用** |
| `CURIS_DB` 默认 `data/curis.sqlite`（相对路径） | `main.py:1006` | 现有数据根是**相对 CWD 的仓库内目录**，不是用户数据目录——与"用户长期资产"定位不匹配，见 §9.4 |

---

## 2. 术语与命名冲突（**必读**）

本轮最大的实际风险不是模型难，而是**词不够用**。同一个词在现有实现、RD 报告、本轮裁定里已经指三个不同东西。

### 2.1 "Workspace" 的三义冲突

| 编号 | 指什么 | 现有证据 | 建议命名 | 处置 |
|---|---|---|---|---|
| **W-1** | **运行空间**：Curis 组织层的工作空间，有 blueprint / 三道门禁 / 状态 | `workspaces` 表（`runtime/models.py`）；`WorkspaceRuntime`；`curis.workspace-package` 实例绑定 `workspace_id` | **Workspace**（保留裸词） | **不改名**（已进入实现与实例规范） |
| **W-2** | **执行工作区**：一次 Work 的隔离工作目录（默认 git worktree，消耗品） | RD 报告 §4.1–4.2（`WorkspaceRecord`、Option D） | **Execution Workspace**（执行工作区） | RD 报告已用"Workspace = 一次 Work 的隔离工作目录"指它——**建议在 Authority 层面统一改称 Execution Workspace**，避免与 W-1 相撞 |
| **W-3** | **业务资产空间**：本轮的 Business Working Space | 无（本轮新增） | **Business Working Space**（产品词） / **`business_root`**（机器词） | 新增；**不得**简称 Workspace |

> **一致性质问**：为什么不干脆给 W-2 换个名字就行了？因为 W-2 已经在 RD 报告与 `WorkspaceRecord` 提案字段（`workspace_id` / `workspace_path`）里成形，**它才是后来者定义的词**；而 W-1 是已实现、已被 Instance Spec 消费的词。**改动成本低的一侧是 W-2。**

### 2.2 "Business" 的口径（**OPEN-1：不得由本轮自行裁定**）

库里同时存在：

- `business_directions.direction_id`（业务方向，`runtime/models.py:20`）
- `commitments.business_id` / `workspaces.business_id` / `outcomes.business_id`（归集键）
- `WorkspacePackageRuntime.install(...)` 的 `business_id` + `business_name`，且被断言为 **canonical business identity**

**问题**：`business_id` 是否等于 `business_directions.direction_id`？还是 Business 之下另有"经营方向"子层？

**本轮处理**：**不裁定、不发明第三答案**。本模型只依赖一个要求：

> **一个 Business 必须有一个稳定的、不可变的身份键**（下称 `business_id`）；它与其上层对象（BusinessDirection / Department）的映射口径由 Authority 一次性说清。

模型不因该选择而改变——这是刻意的（避免模型被未决口径绑死）。

### 2.3 本模型引入的术语（**均为候选，未获批准不得引用**）

| 术语 | 定义 | 不是什么 |
|---|---|---|
| **Business Working Space** | 一个 Business 的**长期业务资产物理归属**（本机目录） | ❌ 不是 W-1 运行空间；❌ 不是 W-2 执行工作区；❌ 不是 Conversation 附件仓库 |
| **`business_root`** | 上述空间的机器名 / 绑定记录字段 | ❌ 不是 `workspace_id` |
| **BusinessRootBinding** | DB 记录：`business_id` ↔ 物理路径 + 模式 + 健康状态 | ❌ 不是 Manifest（Manifest 是磁盘侧的镜像索引） |
| **Shared Base** | 所有 Business 共享的**最小**资产骨架（少数几项） | ❌ 不是"每个专业都生成几十个空目录" |
| **Professional Package** | 决定该业务**内部专业结构**的声明式包 | ❌ 不是 Provider；❌ 不是 Employee；❌ 不拥有资产 |
| **Asset Promotion** | 把 Execution 产出**提升**为正式业务资产的显式动作 | ❌ 不是"任务完成即自动入档" |
| **Execution Area（`_runs/`）** | 执行临时区，可整体销毁，**不是资产** | ❌ 不是"待整理区"（不得靠人手搬运） |
| **Adopt** | 对用户已有目录的**原地纳管** | ❌ 不是导入复制；❌ 不是移动用户目录 |

---

## 3. Business Working Space 是什么，为什么所有 Business 都需要（Q1、Q2）

### 3.1 定义（一句话 + 四条性质）

> **Business Working Space = 一个 Business 的长期资产的唯一物理归属地；它的生命周期等于 Business 的生命周期，与 Employee / Conversation / Work / Execution / Provider 的生命周期全部解耦。**

| 性质 | 含义 | 反面（本条要排除的东西） |
|---|---|---|
| **唯一** | 一个 Business 一处资产地（可以有一处原地纳管的外部根，但身份唯一） | ❌ 分散在多个会话目录 / 多个 Provider 工作区 |
| **长期** | 跨 Work、跨会话、跨 Provider、跨重启、跨月 | ❌ 随一次执行结束而消失 |
| **可外部寻址** | 是一个用户能打开的普通本机目录，不藏在应用私有容器里 | ❌ 应用关闭后不可读 |
| **归属明确** | 任何资产都能回答"属于哪个 Business" | ❌ 归属"某个员工"或"某个会话" |

### 3.2 为什么所有 Business 都需要（四条理由，逐条对应既有裁定）

1. **因为 Curis 的业务是长期经营的 Multi-Agent Business**（本轮 CEO 裁定）。持续经营必然累积：素材、研究、设计、产出、证据。**累积物必须有归宿，否则每次 Work 都从零开始。**
2. **因为"归属 Employee"会产生结构性错误。** 若资产归员工，则"员工停用 = 资产失踪"；而 Employee 是**责任承担者**（RD 报告 §4.3.3 已否决 `1 Employee = 1 Agent Process` 与"Employee 拥有代码"）。
3. **因为"归属 Conversation"会把记忆当仓库。** Conversation Context（C4）是**跨 Work 的关系记忆**，会被压缩/归档；把代码与素材放进去，等于把资产放进一个会自我压缩的容器。
4. **因为"归属 Execution"会污染真相。** Execution 是过程，产出里混着失败产物、临时文件、半成品。**资产必须能区分"验过的"和"跑过的"。**

### 3.3 与 RD 结论的关系（**上游/下游，不是替代**）

```
Business Working Space（本模型，全局）
      └── Development Professional Package（RD 的"专业实现"）
                └── Project（RD 内部的长期项目，R1 已裁定不升格）
                          └── Canonical Project Root（唯一工程真相）
                                    └── Execution Workspace（每 Work 一个，消耗品）
```

**一句话**：**RD 的 "Canonical Project Root" 是本模型下 Business Working Space 的一个专业子结构，不是它的同级或替代物。**

---

## 4. Company / Department / Business 的目录映射（Q3）

### 4.1 先回答"哪些资产属于 Company / Department，而不是某个 Business"

| 层级 | 属于它的资产 | 判据 | 实现先例 |
|---|---|---|---|
| **Company** | 公司级知识、公司级决策记录、共享参考、公司级报告、跨业务规范 | **撤掉任何一个业务它依然成立**；它描述"这家公司怎么做生意" | `KnowledgeService.CANONICAL_TARGETS` 含 `COMPANY` ✅；`companies.default_department_ids_json` |
| **Department** | 部门共享方法、部门知识、跨业务参考（例：研发的工程规范、内容的方法论） | **撤掉部门内任一业务它依然成立**；它描述"这类专业怎么做" | ⚠️ **实现里没有 DEPARTMENT 目标**（`CANONICAL_TARGETS = {COMPANY, BUSINESS, WORKSPACE}`）→ 见 **Gate G7** |
| **Business** | 素材 / 研究 / 设计 / 代码 / 产出 / 结果文件 / 证据 / 经营资料 | **能明确归属某个业务** | `install()` 已按 `business_id` 绑定 ✅ |
| **Workspace（W-1）** | 运行期对象：blueprint / stage / cycle 产物 | 运行空间自身的配置与运行记录 | `workspaces.blueprint_json` ✅ |

**本条最重要的一句规则**（来自 CEO 裁定的直接推论）：

> **能明确归属某个 Business 的资产，一律不得堆到 Company / Department。**

推论：**Company / Department 目录应当"小而稳定"**。它们是**共享层**，不是倾倒区。若 company 目录持续膨胀，说明业务归属判定出了问题。

### 4.2 物理布局：三个候选（**推荐 P2**）

**共同要求**：逻辑层级由 DB 与 UI 表达；物理布局只是实现选择，**不得反过来定义产品层级**。

**P1 — 层级目录（照抄组织树）**
```
<Data Root>/Company/{knowledge,decisions,references,reports}/
<Data Root>/Departments/<department_key>/{shared,wiki}/
<Data Root>/Businesses/<department_key>/<business_key>/{shared base + professional ext}
```
| 优点 | 缺点 |
|---|---|
| 人打开就能看懂组织关系；可直接在 Finder 里按部门浏览 | **路径编码了部门** → 跨部门调整 = 物理搬迁（本轮明确要避免的场景） |
| 与"一张组织树"的产品叙事一致 | 部门改名/类型调整会污染路径；`type_key` 是类型不是名字，但路径仍需要一个稳定名 |
| | 与**现有实现**冲突：`CANONICAL_TARGETS` 里没有 DEPARTMENT |

**P2 — 扁平业务层 + 逻辑层级在 DB（**推荐**）**
```
<Data Root>/                       ← Curis 本地数据根（一个，见 §9.4）
├── Company/                       ← Company 级共享资产（小而稳定）
├── Departments/<department_key>/  ← 部门级共享资产（可选，仅"跨业务方法/规范"）
├── Businesses/
│     └── <business_id>/           ← ★ Business Working Space（★ 用稳定身份命名）
│           ├── .curis/            ← 机器区（manifest、索引、健康状态）
│           ├── README.md
│           ├── assets/  outputs/  evidence/
│           ├── attachments/       ← Conversation 附件（C4，可独立清理）
│           └── _runs/             ← 执行临时区（可整体销毁，不计入资产）
└── _execution/                    ← 全局执行区（Execution Workspace / worktree，见 §12.1）
```
| 优点 | 缺点 |
|---|---|
| **跨部门调整 = 改一条 DB 绑定，零文件移动** | 人直接看目录看不出部门（需要 Curis 界面或 Manifest） |
| 与 `CANONICAL_TARGETS` 的 COMPANY/BUSINESS/WORKSPACE 三层次天然对齐 | 业务多时 `Businesses/` 会平铺很多目录（需靠索引/搜索，而非浏览） |
| 稳定 id 目录 → 改名永不影响路径 | 目录名不可读（需 Manifest / 别名补足可读性） |

**P3 — 混合（Company/Department 有目录，Business 平铺）**：等价于 P2 的实际形态；**P2 已包含 P3**。若 CEO 希望部门目录存在，P2 + `Departments/` 即是。

> **推荐 P2**，理由排序：①**"跨部门调整不得触发大量路径失效"是本轮明确诉求**；②与实现事实（无 DEPARTMENT 资产层）一致；③与"身份与名字分离"（Gate G3）天然一致。**→ Gate G4**

### 4.3 与"七区主导航"的关系（**不得倒推**）

业务空间是**产品导航**中的一个位置；Business Working Space 是**磁盘**上的一个目录。**两者不是同一张图**（详见 §13）。
**明确禁止**：因为磁盘上是 `Company / Departments / Businesses` 三层，就把它做成三级导航。

---

## 5. Shared Base + Professional Package（Q4、Q5）

### 5.1 Shared Base（最小集，**5 项 + 2 个辅助**）

CEO 裁定原文的反对目标是"**所有 Business 生成完全相同的几十个空目录**"。因此 Shared Base 必须**小**，且**空目录不落地**。

| # | 项 | 性质 | 必需 | 说明 |
|---|---|---|---|---|
| 1 | `.curis/manifest.json` | 文件 | ✅ | **机器身份**：business_id / 专业包 / 版本 / 入口索引。见 §11.3 |
| 2 | `README.md` | 文件 | ✅ | **人读**业务说明（可由 AI 生成初稿，用户可改）；不承担机器语义 |
| 3 | `assets/` | 目录 | ✅ | 原始素材与外部输入（用户交付物、采集回来的原始件） |
| 4 | `outputs/` | 目录 | ✅ | 已产出的成果（交付物、文档、成品）。**"已完成"是状态，不是目录** |
| 5 | `evidence/` | 目录 | ✅ | 长期证据（记录 / 报表 / 截图 / 回执） |
| A1 | `attachments/` | 目录 | 按需 | Conversation 附件（C4）。**不是业务资产**，可独立清理 |
| A2 | `_runs/` | 目录 | ✅（隐藏） | 执行临时区。**不计入资产、不参与备份、可整体销毁** |

**三条硬规则**：
1. **空目录不落地**——除 `.curis/` 与 `_runs/` 外，目录**在首次有内容时才创建**；Manifest 记录**声明**，磁盘反映**实际**。
2. **不做 `results/`**——Result 是**对象**（`ResultStore` 已有 task/artifact），其文件落在 `outputs/` 或 `evidence/`。**再开一个 `results/` 目录会造成"状态目录"与"对象"两套语义**。
3. **不做 `tests/` 资产目录**——RD 报告已定"测试与实现必须同一变更集"，测试代码属于仓库（Development 专业包内），不属于业务资产根。

### 5.2 Professional Package（扩展）

**关键结论：不要新建第二套包系统。** 库里已有 `curis.workspace-package/v2`（manifest / surfaces / schemas / digest / 安装 / 更新 / 迁移 / 回滚 / 生命周期事件）。本模型要求的是**在它上面增加一个声明段落**，而不是另造机制。

**Professional Package 的两层职责（建议拆分，避免混淆）**：

| 层 | 决定什么 | 现状 |
|---|---|---|
| **声明层（已实现）** | 运行空间的**对象与界面**：surfaces / schemas / views / requirements | `curis.workspace-package/v2` ✅ 已存在 |
| **资产层（候选新增）** | 该业务的**资产目录布局**：哪些目录、各自语义、与 surface 的映射 | ❌ 不存在 → 候选 `assetLayout` 段 |

**候选 `assetLayout` 形态（声明式，非硬编码）**：

```jsonc
// 候选：workspace-package manifest 的扩展段（未实现，未获批准）
"assetLayout": {
  "layoutVersion": "1",
  "directories": [
    { "key": "reference",  "path": "reference",  "class": "reference",  "surface": "research" },
    { "key": "production", "path": "production", "class": "working",    "surface": "production" }
  ],
  "managed": ["assets", "outputs", "evidence"],   // Shared Base，由 Curis 保证存在
  "lazyCreate": true                              // 扩展目录按需落地
}
```
设计约束（**每一条都来自本轮裁定**）：
- **声明式**：专业差异只能体现在数据里，不得体现为代码里的 `if business_type == …`。
- **可版本化 + 可迁移**：跟随包的 `digest` 与既有 migration/rollback 机制；布局变更必须能 dry-run。
- **不反向生成导航**：`surface` 是**映射提示**，不是"目录列表即菜单"（§13）。
- **可缺失**：目录缺失不阻断业务运行（只影响对应 surface 的"素材/产出"入口）。

### 5.3 三个专业包的候选扩展（**示例性质，名字未冻结**）

| 专业包 | 候选扩展目录 | 为什么是这些（而不是照抄 UI 导航） |
|---|---|---|
| **Development（RD）** | `product/`（需求与产品定义）`design/`（设计）`docs/`（工程文档与决策记录）`engineering/`（源码；**可为 Adopt 的外部 repo**）`quality/`（质量与验证记录） | 按**资产类型与生命周期**分；**测试代码不单独建资产目录**（与实现同仓）；`quality/` 放的是**验证记录**而非测试代码。→ 与 CEO 示例的差异点即在此 |
| **Content Growth** | `reference/`（参考素材）`production/`（制作中与成稿）`published/`（已发布与归档）`channels/`（账号与渠道资料，**不含任何凭据**）`insights/`（数据回流与分析） | UI 的「经营/研究/制作/发布/复盘」是**工作方式**；磁盘按**资产生命周期**（参考→制作→已发布→回流）分。**发放与账号不建两个目录**，因为发布物与渠道资料是同一批资产的两面 |
| **Music** | `reference/`（参考与灵感，**仅 Pattern Extraction，不存受版权保护的词曲原件**）`works/`（歌曲工程与分轨）`masters/`（成品与母带）`release/`（发行与元数据）`rights/`（版权与授权记录） | 音频是**大文件**：`masters/` 明确**不进 git**、走受控资产存储；`rights/` 独立是**法律风险可见性**要求（既有裁定：发行商允许上传 AI 音频 ≠ 拥有版权） |

> **不冻结纪律**：以上是**专业包的候选内容**，属于 Implementation Candidate（§14.2），需专业线各自 Review。

---

## 6. 资产归属规则：谁生成、归谁（Q6–Q10）

### 6.1 六主体归属表（**本模型的核心裁定**）

| 主体 | 它是什么 | 是否拥有业务资产 | 它的产出最终去哪 | 硬规则 |
|---|---|---|---|---|
| **Business** | 长期经营单元 | ✅ **唯一所有者** | — | 资产必须能回答"属于哪个 business_id" |
| **Employee** | 长期责任承担者（不是进程） | ❌ | 员工产生的**一切**产出，按**其当次 Work** 归属到 Business | 禁止按员工建目录（员工停用≠资产失踪） |
| **Conversation** | CEO ↔ Employee 的持续关系 | ❌ | 附件落 `attachments/`（**非资产**，可独立清理）；要成为资产必须**显式导入**（复刻 RD §4.2.2 的"显式导入"规则） | 禁止把"对话里出现过的文件"自动当资产 |
| **Work** | 有目标、可验收的执行单元 | ❌ | Work 本身**不产生目录**；它的产出通过 **Result** 归集并最终落 `outputs/` / `evidence/` | 禁止"一个 Work 一个文件夹"（会随 Work 爆炸且无法复用） |
| **Execution** | 一次运行（prompt/进程/沙箱/日志） | ❌ | 中间产物落 `_runs/<execution_id>/`；**只有提升后的产物**才进资产区 | 禁止 Execution 直写 `assets/` `outputs/` `evidence/` |
| **Provider** | 可替换的专业执行能力 | ❌ | Provider 的临时 session / 工作区**永不作为资产归宿** | 禁止把 Provider 工作区当"业务目录"（违反可替换性） |

### 6.2 Result 与真实文件的关系（Q9）

**Result 不是文件，是事实对象 + 引用。**

```
Result（DB 对象，已有 ResultStore 承载）
├── 结构化事实：目标 / 结论 / 验收结论 / 未解决项 / 时间 / 责任 / provider
└── 文件引用：business_asset_ref[] → 指向 Business Working Space 内的相对路径 + digest
```
规则：
1. **Result 永远不复制文件内容**（避免"同一个交付物两个版本"）。
2. **被 Result 引用的文件必须已在资产区内**（先提升、后引用；不是先引用、后期再补）。
3. **Result 的文件引用必须带 digest**（文件被外部改动可检测）。
4. `_runs/` 中的文件**不能被 Result 引用**（否则"可整体销毁"就不成立）。

### 6.3 Evidence（Q10）

| 情形 | 落点 | 理由 |
|---|---|---|
| 属于某业务、长期有用（经营数据回流、发布回执、验证报告、截图） | 该业务 `evidence/` | 与业务同生共死 |
| 跨业务、描述公司或专业方法 | `Company/` 或 `Departments/<key>/` | 归属判据见 §4.1 |
| 只是某次执行的日志/截图 | `_runs/<execution_id>/`（附保留期） | 是过程证据，不是资产 |
| 平台会话材料（Cookie / Authorization / 登录态） | **不进任何目录、不进 DB、不进备份** | 既有 G1 硬边界（`WAITING_FOR_USER` 系列） |

**两条禁止**（直接来自本轮裁定）：
- ❌ **Evidence 只留在 Provider 的临时 session 里**——Provider 一换就没了。
- ❌ **把"一次运行的完整日志"当业务证据长期保存**——日志是过程，Reference 时只存指针 + 摘要。

---

## 7. 生命周期：从执行到资产（Q11 前置）

### 7.1 主链路（CEO 裁定 §6 的机器化表述）

```
① Employee 开始 Work
② Assignment（Work → Provider）
③ Provider 在 Execution Workspace 内执行
④ Execution 产生文件 → 落 _runs/<execution_id>/（staging）
⑤ Verification（独立于执行；RD 报告 CO8）
⑥ Result Accepted（Gate，视风险等级）
⑦ Promotion：受控搬入 assets/ outputs/ evidence/ + 写 DB 资产记录（含 digest、来源 execution）
⑧ Result 只保存结构化事实 + 文件引用
⑨ 后续 Employee 通过 Result 的引用继续使用
```

### 7.2 提升（Promotion）规则

| 规则 | 内容 |
|---|---|
| **必须显式** | 提升是一个**动作**（有触发者、有时间、有原因），不是"任务完成即自动入档" |
| **必须带 provenance** | 记录 `origin_execution_id` / `provider` / `work_id` / `employee` / `content_sha256` |
| **必须可复算** | 提升后的文件 digest 与来源一致；不一致→报警而不是静默覆盖 |
| **冲突不覆盖** | 目标已存在同名文件 → `outputs/<name>--<short-digest>.<ext>` 并报告（**永不静默覆盖**） |
| **可回退** | 误提升 → 允许把该资产记录标为 `SUPERSEDED` 并移出（保留审计） |

### 7.3 失败 Execution 的处理（**不得污染正式资产**）

| 问题 | 结论 |
|---|---|
| **临时文件放哪** | `_runs/<execution_id>/`（业务资产根内、隐藏、**不参与资产统计与备份**）。W-2 执行工作区（worktree）另在 `_execution/`（§12.1），两者都不进资产区 |
| **失败产物是否保留** | **默认短暂保留**（含诊断价值，与 RD 报告 §4.2.2 第 3 条一致）：保留期内用户可选「保留为参考」或「立即销毁」 |
| **什么时候清理** | ①到达保留期（默认 7 天，候选）②用户显式销毁 ③业务归档时随 `_runs/` 整体销毁。**清理必须是可取消的**（先进 Trash/暂存，再真正删除，复刻 `uninstall()` 的暂存模式） |
| **什么时候升为正式资产** | 只有经 ⑦ Promotion。**"跑成功"不等于"是资产"**：一次成功的中间草稿也可能永远不该进 `outputs/` |
| **"保留为参考"落哪** | 仍在 `_runs/`，但**标记为可引用**（此时允许 Result 引用它）——**不搬进资产区**（避免把失败产物混进正式资产） |

---

## 8. DB 与 Filesystem 的分工（Q11）

### 8.1 分工总表

| 内容 | DB（Curis Runtime） | Filesystem | 谁是权威 |
|---|---|---|---|
| 身份（Business / Employee / Workspace / Provider） | ✅ 全量 | 仅 Manifest 镜像（`business_id`） | **DB** |
| 关系（谁属于谁、谁引用谁） | ✅ 全量（复用 `typed_object_references`） | ❌ | **DB** |
| 状态（生命周期 / 门禁 / 六态） | ✅ 全量 | ❌ | **DB** |
| 分配（Assignment / Workspace 分配） | ✅ 全量 | 无（路径由绑定记录给出） | **DB** |
| 决策（Decision / Gate） | ✅ 全量 | ❌ | **DB** |
| Work / Result metadata | ✅ 全量 | ❌ | **DB** |
| **文件指针**（路径 / digest / 大小 / 媒体类型） | ✅ | 文件本体 | **路径权威在 DB，内容权威在 FS** |
| 文档 / 代码 / 设计 / 素材 / 生成产出 / 证据文件 / 专业制品 | ❌（超大内容） | ✅ | **FS** |
| 模型调用记录 / 成本 / 审计 | ✅ | ❌ | **DB** |
| 凭据 / 令牌 / 登录态 | ❌（只存 ref + digest） | ❌（只驻 Keychain / `.env`） | **既不是 DB 也不是资产区**（既有硬约束） |

### 8.2 三条不可违反的规则

1. **内容权威在 FS，身份与关系权威在 DB。** 同一条信息不得两处都可写。
2. **❌ 不做"把文件内容复制进 DB 再在 DB 里做业务查询"**。⚠️ **本轮发现**：`artifacts` 表（`database.py:257`）**当前会把制品内容（`content text`）存进 DB**。这是**可接受的小文本制品特例**（成果摘要类），但**必须明确它的边界**：一旦扩大到二进制/大文件/素材，就会产生"DB 里一份、磁盘上一份"的双真相。→ 建议：**新资产体系一律只存指针**（`path` + `sha256` + `size` + `mime`），不复用 `artifacts.content` 作为大对象存储。
3. **❌ 不做"只有文件、没有 canonical 关系"**。任何进入资产区的文件必须有一条 DB 记录（否则它既不能问责、也不能被 Result 引用、也无法在改名后找回）。

### 8.3 库里已有的正确样板（应当复用而非重造）

| 样板 | 复用方式 |
|---|---|
| `knowledge_entries`（`source_type='local_file'` + `source_path` + `content_sha256` + 唯一索引 `(tenant_id, connector_id, source_path)`） | **"文件原地登记 + 摘要"的现成形态**：本模型的资产记录应当与它保持同一套语义（**不要把同一批文件登记两遍**；资产记录与 Knowledge 记录应当**互相引用**而不是各存一份） |
| `typed_object_references` | **关系层直接复用**：资产 ↔ Work / Result / Evidence 的关系一律走它，**不新建第二套引用系统**（该表注释已明确禁止变成"第二套 Work/Context/Citation 系统"） |
| `workspace_package_lifecycle_events` | Promotion / 回收 / 迁移都应产生**生命周期审计事件**（同一模式） |
| `uninstall()` 的"暂存 → 删除 → 失败回滚" | 资产销毁必须走同一模式（**永远先暂存，永不直接 `rmtree` 正式资产**） |
| `_remove_unreferenced_target()` 的"**先查引用，无引用才删**" | 资产删除的**前置条件**。⚠️ 见 §15 RISK-1：同一个文件里 `uninstall()` 没有做这个检查 |

### 8.4 候选新增记录（**仅提案，未实现、未获批准**）

```text
business_asset_roots                                  -- 每个 Business 一条（可多条=多根）
  business_id        text primary key / part
  root_mode          text   -- MANAGED | ADOPTED
  root_path          text   -- 绝对路径（托管模式下建议 <Data Root>/Businesses/<business_id>）
  display_alias      text   -- 人读别名（可空；不参与寻址）
  status             text   -- OK | MISSING | SUSPECT | LOST
  last_seen_at       text
  created_at         text

business_assets                                       -- 资产指针
  asset_id           text primary key
  business_id        text not null
  relative_path      text not null      -- 相对 root_path，禁止绝对路径
  asset_class        text               -- asset|output|evidence|attachment
  content_sha256     text not null
  size_bytes         integer
  media_type         text
  origin_execution_id text               -- provenance（可空=用户直接放入）
  origin_provider    text
  lifecycle_status   text               -- ACTIVE | SUPERSEDED | REMOVED
  promoted_at        text
  created_at         text
  -- 唯一约束建议：(business_id, relative_path)，(business_id, content_sha256)
```
> **刻意不设计的东西**：不给资产做"标签/集合/工作流状态"（那会变成第二个对象系统）；不做资产版本历史（那是版本控制或包机制的事）。

---

## 9. 自动 Provision（Q12）

### 9.1 新建 Business 的九步（候选）

```
① 创建 Business 记录（DB）
② 创建 Business Working Space 绑定记录（business_asset_roots，root_mode=MANAGED）
③ 创建物理根目录 + .curis/（最小：manifest.json）
④ 应用 Shared Base（仅 3 个数据目录；空目录不落地 → 实际只落 .curis/ 与 README.md）
⑤ 应用 Professional Package：解析 assetLayout → 记录"声明"，按需创建
⑥ 写 Business Manifest（§11.3）
⑦ 绑定 Employee / Responsibility（不创建任何员工目录）
⑧ 绑定默认 Workspace（W-1）
⑨ 进入 Operating（业务可被进入）
```
**幂等性要求**：①–⑥ 必须可重入；任一步失败 → **要么全成、要么留下可解释的半成品状态**（不得出现"有绑定记录但没有目录"或"有目录但没有记录"的隐性不一致）。**Provision 失败必须先于业务可见**。

### 9.2 失败与降级

| 场景 | 处理 |
|---|---|
| 目录已存在且非空（用户恰好放了个同名目录） | **不覆盖、不删除**；向上升级为 Human Gate：让用户选「纳管已有目录 / 换一个位置 / 取消」 |
| 目录不可写（权限） | Provision 失败并升级；**不静默降级为"仅 DB 无资产"**（那会产生"看起来有业务，其实没地方放东西"） |
| 磁盘空间不足 | 同上，升级 |
| 用户拒绝创建 | Business 仍可创建，但必须显示为**资产未就绪**（可见的缺口，不是隐形的） |

### 9.3 Manifest 最小字段（Q12 的核心问题）

**先说什么不该进 Manifest**：❌ 业务数据库内容的副本；❌ 员工/工作/结果清单；❌ 任何凭据；❌ 运行态。

**Manifest = 身份 + 类型 + 版本 + 入口索引**：

```jsonc
{
  "manifestSchema": "curis.business-manifest/v1",
  "businessId": "…",                  // 稳定身份（唯一必须长期不变的东西）
  "displayName": "…",                 // 可变；权威在 DB，此处仅为可读性镜像
  "rootMode": "MANAGED",              // MANAGED | ADOPTED
  "professionalPackages": [
    { "packageId": "…", "version": "…", "digest": "sha256:…" }
  ],
  "assetLayoutVersion": "1",
  "entryPaths": {                     // 语义 → 相对路径（机器读的入口索引）
    "assets": "assets", "outputs": "outputs", "evidence": "evidence",
    "runs": "_runs", "attachments": "attachments"
  },
  "createdAt": "…",
  "curisManifestVersion": 1
}
```
**允许 Manifest 承担的唯一"找回"职责**：当物理目录被改名/移动后，**靠 `businessId` 重新认出它**（§10）。这是 Manifest 存在的**核心理由**，其他内容都是便利。

### 9.4 数据根之争（**OPEN-2：本机现状与产品定位不匹配**）

**现状（L2）**：`CURIS_DB` 默认 `data/curis.sqlite`（**相对 CWD**）；包存储根默认跟随 DB 目录。→ 也就是说，当前数据库与包存储**挂在仓库目录里**。
**问题**：Business Working Space 装的是**用户的长期业务资产**（可能几十 GB）。它**不能**住在应用仓库/安装目录里——升级、迁移、甚至 `git clean` 都可能伤到它，而用户也无法在"应用目录"里管理和备份自己的资产。
**候选**：引入**一个显式的本地数据根**（例：macOS `~/Documents/Curis/` 或用户首次创建时选择的位置），DB / 包存储 / 业务资产 / 备份 全部相对它定位。
**→ 本轮不裁定**（涉及 Runtime 配置与迁移），列入 Gate G8。

---

## 10. 改名 / 移动 / 归档 / 删除（Q13、Q14）

### 10.1 核心机制：`display_name` 与稳定身份分离（**Gate G3**）

| 概念 | 可变 | 存在哪 | 谁消费 |
|---|---|---|---|
| `business_id`（**stable filesystem identity**） | ❌ 永不变 | DB + Manifest | 路径解析、绑定、引用 |
| `display_name` | ✅ 随意改 | DB（权威）+ Manifest（镜像） | UI、文档、报告 |
| `root_path` | ⚠️ 可变但**只在一个地方** | DB（绑定记录） | 路径解析 |
| 目录物理名 | 托管模式下 = `business_id`；纳管模式下 = 用户决定 | 磁盘 | 无人直接消费 |

> **一条硬规则（本轮最重要的实现级结论）**：
> **任何代码不得用名字拼路径，只能从绑定记录解析路径。**
> 满足这条，"UI 改名 → 路径大面积失效"在结构上就不可能发生。

### 10.2 五类变更的处置

| 变更 | 处置 | 是否动文件 |
|---|---|---|
| **Business 改名** | 只改 DB `display_name` + 同步 Manifest 镜像。可选提供"重命名物理目录"的**显式**动作（仅 MANAGED 模式） | 默认**不动** |
| **Department 调整（跨部门移动）** | 只改 DB 绑定（`commitments.department_id` 等）。**P2 布局下零文件移动**——这正是推荐 P2 的原因 | **不动** |
| **用户手动移动目录** | 检测 → `MISSING` → 按 Manifest `businessId` 扫描候选 → 找回并更新绑定 | 用户动，Curis 只更新记录 |
| **用户手动改名目录** | 同上（改名 ≈ 移动） | 同上 |
| **Business Archive** | ① 资产根**整体移入归档区**（不删除）② DB status → `ARCHIVED` ③ `_runs/` 整体销毁 ④ **Conversation / Decision / Result 记录保留**（与 RD 报告 §4.2.2 一致） | 移动，不删 |
| **Business Delete** | **两段式**：①**解除绑定**（unlink，不动文件；业务从 UI 消失）②**显式"删除本地资产"**才移入 Trash（复用 `uninstall()` 的暂存+回滚模式），并在 DB 留取证记录 | 第二阶段才动 |

### 10.3 一致性检测（低成本、必须做）

| 时机 | 动作 | 成本 |
|---|---|---|
| 应用启动 / 业务首次进入 | 对**当前业务**做一次 `exists()` + Manifest 校验 | 极低 |
| 用户主动"检查资产位置" | 全量校验（含 digest 抽样） | 中 |
| **不做** | 常驻全盘扫描、文件系统 watcher | ❌ 不建议（v1 单机自用，收益低于成本与风险） |

状态（候选，**不新造对外状态名**）：

| 内部状态 | 含义 | 用户可见表达 |
|---|---|---|
| `OK` | 路径存在 + Manifest 匹配 | 正常 |
| `MISSING` | 路径不存在 | 「找不到资产目录」+ 立即提供「指认新位置」 |
| `SUSPECT` | 目录在，但 Manifest 缺失/`businessId` 不匹配 | 「这个目录可能不是它的」+ 让用户确认 |
| `LOST` | 找不到且用户确认放弃 | 需 Human Gate 决定：重新定位 / 新建空资产空间 / 归档业务 |

**禁止**（本轮明确要求避免的失败模式）：
- ❌ 检测到丢失就**自动重建空目录**（用户会以为数据还在）。
- ❌ 检测到丢失就**静默降级为"该业务暂无资产"**。
- ❌ 把 `MISSING/LOST` 映射成新的状态名——**涉及用户介入的一律复用既有 `WAITING_FOR_USER` 语义**（与 §3.4 的既有裁定一致，不得另造第二套状态名）。

---

## 11. 外部已有业务迁入（Adopt）（Q15）

### 11.1 三种模式（**默认 ADOPT_IN_PLACE**）

| 模式 | 行为 | 何时用 | 风险 |
|---|---|---|---|
| **`ADOPT_IN_PLACE`（默认）** | **原地不动**：只在目标目录写 `.curis/`，并创建**缺失的** Shared Base 目录 | 用户已有长期经营的目录（代码项目 / 写作目录 / 音乐资产 / 内容素材） | 用户目录被 Curis 追加内容（必须严格限定为"只新增、不改不删"） |
| **`IMPORT_COPY`** | 复制一份到托管位置，原目录不动 | 用户想"纳管但不冒险" / 目录在被管理的同步盘 | 磁盘翻倍；两份内容易分叉（必须记录原路径做溯源） |
| **`MOVE_IN`** | 移动到托管位置 | 用户明确要求统一收纳 | 破坏用户既有路径引用（外部脚本/IDE/同步工具可能依赖） |

### 11.2 Adopt 的安全规则（**六条，全部为硬约束**）

1. **不移动、不重命名、不删除**用户已有文件（`ADOPT_IN_PLACE` 下）。
2. **只新增**：`.curis/`（Manifest + 本地索引）与**缺失的** Shared Base 目录。
3. **冲突不覆盖**：同名的 Curis 文件已存在 → 写 `<name>.curis-new` 并报告。
4. **不干预专业既有结构**：已有 `.git/`、`node_modules/`、构建产物目录 → 只识别、不整理、不清理。
5. **可逆**：提供"解除纳管"（只删 Curis 写入的 `.curis/`，其余一概不动）。
6. **先看后动**：Adopt 前必须给出**将要创建什么**的清单（dry-run），用户确认后才落盘。

### 11.3 建立 Professional Package 缺失目录

Adopt 时专业扩展目录通常**不存在**（用户的目录是他自己组织的）。规则：

- **不强制补齐**：缺失目录 → 标记为"未落地"，UI 上对应入口显示"尚无此类资产"，**不自动批量建空目录**。
- **按需落地**：第一次真的往里放东西时才创建（与 §5.1 的"空目录不落地"同一条规则）。
- **允许映射**：Adopt 时允许把**用户已有的目录**映射到专业语义（例：`notes/` → `reference`；`demo/` → `outputs`）。映射写在 Manifest 的 `entryPaths` 里——**这是 Adopt 与托管真正不同的地方**：托管模式路径是**规定的**，纳管模式路径是**记录的**。

### 11.4 与 RD 的直接衔接（**高价值**）

**Adopt 一个已有代码项目目录 = 直接得到 RD 的 Canonical Project Root，不需要重新 clone、不需要复制仓库。**

这同时回答了 RD 报告 §4.1 未充分覆盖的一个场景：**"项目已存在于本机"**（RD 研究默认了"项目在 Curis 内新建"）。→ 记为 **RD 补充点**（不修改 RD 报告结论，只登记扩展）。

---

## 12. 专业包如何嵌入（Q16、Q17、Q18）

### 12.1 Development（RD）

```
Business Working Space（本模型）
└── engineering/ 或一个 ADOPTED 的外部 repo 路径
      └── Project（RD 内部长期项目；R1 已裁定不升格）
            └── Canonical Project Root（唯一工程真相；含 .git）
                  └── [per Work] Execution Workspace（worktree，消耗品）
                        → 建议放 <Data Root>/_execution/worktrees/<work_id>/  ← ★ 见下
```

| 问题 | 结论 |
|---|---|
| RD Canonical Project Root 放哪 | ①**托管**：Business Working Space 内的 `engineering/<project>/`；②**纳管**：用户既有代码目录（原地） |
| worktree 放哪 | **建议放业务资产根之外**（`<Data Root>/_execution/worktrees/<work_id>`）。**理由**：worktree 是消耗品，若放在资产根内会污染资产树（被备份、被统计、"资产"里出现一堆并行副本），且与 RD 报告 I4（Workspace 可销毁）的语义相冲。技术上 git worktree 可在任意位置（共享 `.git` 通过 gitdir 指向），**不要求与主 checkout 同父目录**。→ **Gate G5**（这触及 RD 报告的 Option A 图示，需一并裁定） |
| 是否要为 RD 建一套目录 | **只建专业扩展目录**（§5.3），**不建 Git 概念目录**：不做 `branches/`、不做 `worktrees/`、不做 `merge-queue/` |
| 与 RD 报告的关系 | RD 报告是**专业实现**；本模型是**它的上游边界**。**RD 报告一句不改**（仅追加一节边界说明） |

### 12.2 Content Growth

```
Business Working Space
├── reference/   参考素材
├── production/  制作中与成稿
├── published/   已发布与归档
├── channels/    账号与渠道资料（凭据除外 → Keychain）
└── insights/    数据回流与分析
+ 经营方向（BusinessDirection）归属：见下
```
| 问题 | 结论 |
|---|---|
| **经营方向要不要建目录层** | **默认不建**（候选）。理由：①目录层级会随账号/方向增减而爆炸；②同一素材常被跨方向复用；③方向是**经营归属**，不是**文件分类**。→ 方向归属写在**资产记录的元数据**里，`channels/` 内每条账号资料标注所属方向 |
| 例外 | 若某方向有**法律或结算上必须物理隔离**的资产（如不同主体的合同），允许该方向独立子目录——**例外必须显式声明**（写进 Manifest），不得默认 |
| 明确不做 | ❌ 不做"发布队列"目录（那是运行时状态）｜❌ 不做账号凭据目录（凭据只进 Keychain） |

### 12.3 Music

```
Business Working Space
├── reference/   参考与灵感（仅 Pattern Extraction，不存受版权保护的词曲原件）
├── works/       歌曲工程与分轨
├── masters/     成品与母带（大文件 → 受控资产存储，不进 git）
├── release/     发行与元数据
└── rights/      版权与授权记录
```
| 问题 | 结论 |
|---|---|
| 大文件怎么办 | `masters/` 与 `works/` 属**大二进制**：**不进 git**、**不进 DB**、走文件系统 + 指针记录（`sha256` + size）。备份策略另行（Gate 外，属既有 Backup 权威范围） |
| 版权风险 | `rights/` 独立存在，是**法律风险可见性**要求（既有裁定：发行商允许上传 AI 音频 ≠ 拥有版权） |
| 版权红线 | `reference/` **禁止**存放受版权保护的词曲原件（既有硬边界：仅 Pattern Extraction + Original Recombination） |

### 12.4 一个必须显式写下的反面规则

> **❌ 禁止把 Git / Branch / Worktree / Repository 提升为全局 Business 概念。**
> 它们是 **Development 专业包内部**的实现选择。Music 与 Content Growth **不需要** worktree，也不应该在模型层"沾上" Git。
> 全局模型只保留一个**能力位**：*"该业务的专业包可以声明其资产受版本控制"*（`yes/no + 由哪个专业包负责`）。**如何版本控制，是专业包的事。**

---

## 13. Context 三层映射与"文件 ≠ UI 导航"（Q19 + 本轮裁定 §8、§14）

### 13.1 Context 三层映射（**候选**）

RD 报告的 C1–C4 是 **RD 研究产物**。从全局 Business 角度看，它少了一层上游、且 C1 层次被抬得过高：

| 层 | 名称（候选） | 回答什么问题 | 时间尺度 | 载体 | 与 RD 的关系 |
|---|---|---|---|---|---|
| **Global** | **G1 Business Context** | **这个业务长期是什么**：业务身份 / 目标 / 经营方向 / 渠道账号 / 长期决策 / 产出历史 / 团队与责任 / 证据库 | 月–年 | Business Working Space（Manifest + 资产 + DB 记录） | **新增（上游）** |
| **Global** | **G2 Professional Context** | **这类专业怎么做**：方法与规范（研发的工程规范 / 内容的平台规范 / 音乐的发行规范） | 年 | Professional Package 声明 + Company / Department 级共享知识 | **新增（上游）** |
| **Professional（RD）** | **P1 Project Context** | **这个项目是什么**：目标 / 架构 / 仓库 / 指令 / 决策 / 知识 / 历史 / 团队 | 月–年 | Canonical Project Root 内的**仓库内文档**（`AGENTS.md` 式地图 + `docs/`） | **= RD 的 C1，下沉一层** |
| **Professional（RD）** | **P2 Work Context** | 这件工作要达成什么 | 小时–天 | Curis DB（持久事实，**不含 prompt / 日志 / 对话全文**） | = RD 的 C2（不变） |
| **Professional（RD）** | **P3 Execution Context** | 这次运行发生了什么 | 分钟–小时 | append-only 事件流，结束即冻结为只读 | = RD 的 C3（不变） |
| **Global** | **C4 Conversation Context** | CEO ↔ Employee 的持续关系 | 月–年（跨 Work） | Curis DB | 不变（本来就跨业务） |

**本映射要说明的三件事**：

1. **C1 不应"上升"为 Business Context——它是被"下沉"了。** 原 C1 描述的是**某个项目**的长期信息，那正是 P1；而"业务长期是什么"（G1）在原 C1 里**根本不存在**。所以正确动作不是把 C1 改名成 Business Context，而是**新增 G1/G2 作为上游，并把原 C1 明确为 P1**。
2. **G1 ≠ C4。** G1 是**事实与资产**（有归宿、可引用）；C4 是**关系与过程**（会被压缩、会被归档）。两者都叫"长期"，但一个在磁盘上，一个在对话里。
3. **承载位置的差异必须守住**：G1 的权威在 **Business Working Space + DB**；P1 的权威在 **仓库内文档**（因为它必须随代码版本化）；Provider **永远不读 G1**（Provider 只收到它被派发时的 Self-contained Work Context + 项目地图）——这与 RD 报告"上下文不自动继承"的官方结论一致。

> **明确不做的**：本轮**不修改** RD 报告的 C1–C4 定义（用户明确要求"不要直接改 Authority"，且只允许在 RD 报告追加一节边界说明）。以上是**映射候选**。

### 13.2 文件系统 ≠ UI 导航（本轮裁定 §14 的落地）

**原则**：

| 维度 | 文件系统 | UI 导航 |
|---|---|---|
| 按什么设计 | **资产生命周期与专业归属** | **工作方式**（用户当下要做什么） |
| 变化频率 | 低（改布局 = 迁移） | 高（随工作流演进） |
| 单位 | 目录 / 文件 | 面（surface） / 入口 / 动线 |

**两条硬规则**：
1. **禁止从目录树生成导航**（磁盘上有几个目录就出几个菜单项）。
2. **映射必须显式登记**：`assetLayout` 里声明 `surface ↔ path`；**没有登记映射的目录就是"没有界面入口的存储"**，这是允许的、正常的（不是缺陷）。

**反例对照表（证明 1:1 是错的）**：

| 专业 | UI 的工作方式（示例） | 磁盘的真实结构 | 为什么不能 1:1 |
|---|---|---|---|
| **Music** | 经营 / 研究 / 制作 / 发布 / 复盘 | `reference/ works/ masters/ release/ rights/` | 「经营」与「复盘」**没有对应目录**——它们是**动作**，不是资产类别；而 `rights/` 在 UI 里**没有独立入口**（它出现在发布与合规的上下文里） |
| **Content Growth** | 经营 / 研究 / 制作 / 发布 / 复盘 | `reference/ production/ published/ channels/ insights/` | 「经营」跨 `channels/ + insights/ + published/`；单一导航项无法对应单一目录 |

---

## 14. 需要 CEO 裁定的 Gate

### 14.1 八项 Gate（**建议进入未来 Authority 的候选**）

| # | Gate 表述 | 若采纳，影响 |
|---|---|---|
| **G1** | **接受三义 "Workspace" 分叉**：裸词 `Workspace` 只指"运行空间"；RD 的"一次 Work 的隔离工作目录"改称 **Execution Workspace**；本模型用 **Business Working Space** | 产品与 Runtime 命名；RD 报告术语；Instance Spec |
| **G2** | **接受"资产只归 Business"五条边界**：Employee / Conversation / Work / Execution / Provider **均不拥有业务资产** | 全部资产归属逻辑、UI 表达（员工不显示目录） |
| **G3** | **接受 `display_name` 与稳定身份分离**：资产归属键永不变、路径只从绑定记录解析 | 改名/移动的可用性；实现级硬规则 |
| **G4** | **Business 物理平铺（P2）**：逻辑层级在 DB，物理 `<Businesses>/<business_id>` | 跨部门调整成本；可读性（靠 Manifest/界面补） |
| **G5** | **执行区与资产区分离**：Execution Workspace（worktree）/ `_runs/` 均在业务资产根之外（或隐藏且排除于资产语义） | 备份/统计/资产可信度；**并触及 RD 报告 Option A 的图示** |
| **G6** | **Professional Package 扩展方式**：复用既有 `curis.workspace-package/v2`，新增声明式 `assetLayout`，**不新建第二套包系统** | 实现路径；避免双包系统 |
| **G7** | **DEPARTMENT 是否作为资产归属层** | ⚠️ **实现现状无此层**（`CANONICAL_TARGETS` 仅 COMPANY/BUSINESS/WORKSPACE）。若要部门级资产，需明确它**是否只是"共享层"**（本模型建议：**是共享层，不是资产所有者**） |
| **G8** | **显式本地数据根**（DB / 包存储 / 业务资产 / 备份 统一相对它定位），而非当前"相对 CWD 的仓库内 `data/`" | Runtime 配置与迁移；用户资产的长期可管理性 |

### 14.2 仍只是 Implementation Candidate（Q20：不进 Authority）

目录具体英文名｜Shared Base 的精确清单｜`assetLayout` schema 与版本号｜`business_asset_roots` / `business_assets` 表结构｜Manifest 字段表｜Adopt 三模式的默认值与 dry-run 交互｜`_runs/` 保留期默认值（建议 7 天）｜一致性检测的状态机细节｜三专业包的扩展目录清单（需各专业线 Review）｜大文件（音乐/视频）的受控存储策略｜备份范围与排除规则。

**判定口径**（与 AGENTS.md 一致）：**候选结构一律标注 CANDIDATE，未获批准不得作为 Authority 引用**。

### 14.3 与既有裁定的对齐检查

| 既有裁定 | 本模型 | 状态 |
|---|---|---|
| R1：Project 不升格，`Company → Department → Business → Workspace` 不变 | 本模型**不新增组织层级**；Project 仍是 RD 内部的 Professional Object（§12.1） | ✅ 一致 |
| R2：不恢复 Company-level Project Center | 本模型不引入 Project 级导航 | ✅ 一致 |
| R3：七区主导航不变 | §13.2 明确"禁止从目录树生成导航" | ✅ 一致 |
| R4 / M1：Professional Workspace 可以很简单 | §5.1 Shared Base 保持最小 + 空目录不落地 | ✅ 一致 |
| 不得另造状态名（复用 `WAITING_FOR_USER` / `EFFECT_UNKNOWN`） | §10.3 明确涉及用户介入的复用既有语义 | ✅ 一致 |
| v1 = 单机本地桌面自用 | 本模型是**本机目录**，无租户/计费/Marketplace 语义 | ✅ 一致 |
| 能力可替换不写死 | Provider 不拥有资产；Provider 工作区永不作为资产归宿 | ✅ 一致 |
| 凭据治理（只存 ref + digest，不落明文） | `channels/`、Manifest、备份**均排除凭据** | ✅ 一致 |

---

## 15. 已知限制与未解决未知区（不得省略）

| # | 限制 / 未知 | 性质 |
|---|---|---|
| **L1** | **本轮未做任何本地真实运行**：未创建目录、未改动文件系统、未跑 Provision、未做 Adopt 演练。全部结论为 **L2 源码 + L3 既有权威 + L6 推断**。用户本轮明确禁止"Filesystem 真实创建"。 | 边界 |
| **OPEN-1** | `business_id` 与 `business_directions.direction_id` 的口径未定（§2.2）。**本轮刻意不裁定**。 | 待 Authority |
| **OPEN-2** | 本地数据根位置未定（§9.4）。当前实现为相对 CWD 的 `data/`。 | 待裁定（G8） |
| **U1** | `installed_workspace_packages.stored_path` 与"业务资产目录"的关系**未在实现层确认**：包存储是内容寻址的共享存储，不是业务资产。**两者是否应彻底分离、是否需要 per-business 物化**，需实现层确认。 | 未知区 |
| **U2** | macOS 上"数万文件的大资产树"对 Spotlight / Time Machine / 同步盘（iCloud / Dropbox）的实际影响未验证。若用户把业务资产放在同步盘，`.curis/`、`_runs/`、worktree 可能与同步冲突（L6 推断，未实测）。 | 未知区 |
| **U3** | `artifacts.content`（DB 存内容）的**既有边界**未在 Authority 中写明。本模型只提出"新资产体系不复用大对象存储"的规则；既有行为**本轮不改**。 | 待收敛 |
| **U4** | RD 报告的 `Workspace` 用词（W-2）与 W-1 的冲突，**本轮只提议**（G1），未改 RD 报告正文。 | 待裁定 |
| **RISK-1** | ⚠️ **在一份文件里发现两种互相冲突的删除策略**：`_remove_unreferenced_target()` **先查 DB 引用，无引用才删**；而 `uninstall()` 直接把包的 `stored_path` 移入暂存后 `rmtree`，**未见引用检查**。既然 `installed_workspace_packages` 的主键是 `(tenant_id, package_id, version)`（**租户级共享**），当同一包被多个 business 实例引用时，卸载其中一个是**可能影响其他实例**的。**本轮未运行验证**，仅登记为需实现层核实的风险。 | 实现风险 |

---

## 16. 本轮交付边界声明

| 项 | 内容 |
|---|---|
| **新增** | 本文件 1 份。**未生成大量重复文档。** |
| **追加** | `docs/research/rd-multi-agent-development/CURIS_RD_MULTI_AGENT_ORCHESTRATION_CONCLUSIONS.md` 追加一节 `Global Business Working Space Boundary`（**很短，说明 RD Project Working Space 是全局 Business Working Space 下的 Development 特化**）。**未重写原 84KB 报告的其他内容。** |
| **未动** | Authority / Blueprint / Master Map / Page Map / UI Blueprint / Runtime / Code / Schema / DB / RD HTML / Figma / Frontend / Backend |
| **git** | **未 commit、未 push**；仅新增文件与追加一节 |
| **状态** | `BUSINESS WORKING SPACE BASELINE CANDIDATE COMPLETE — READY FOR CEO REVIEW` |

**STOP。** 等待 CEO 就 §14.1 的 8 项 Gate 给出裁定；裁定前不进入实现，也不进入 RD 定向视觉修订。
