# Curis Workspace Obsidian Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成一套中文优先、可直接用 Obsidian 打开的 Curis Workspace 知识库，覆盖八大类目和 60 篇主题文档。

**Architecture:** 新知识库写入独立目录 `Curis Workspace/`，作为面向创始人、研发团队与投资人的叙事和导航层；现有 `PROJECT_STATUS.md`、`knowledge/`、`issues/`、`reviews/`、ADR 与产品空间文档继续作为事实源。所有文章以 YAML 属性、Wiki Link、内容状态和事实依据建立互联，并严格区分当前能力、已规划能力和战略方向。

**Tech Stack:** Markdown、Obsidian Wiki Link、YAML Frontmatter、Git、ripgrep。

## Global Constraints

- 输出目录固定为 `/Users/yy/Documents/Curis AI Workspace/Curis Workspace/`。
- 只创建用户指定的八个目录和 60 篇 Markdown 文档，不增加其他类目。
- 正文尽量使用中文；保留 API、Skill、Tool、Workflow、Capability、Model Router、Credential Vault、Usage Event、Value Event、Billing 等必要产品术语。
- 当前能力必须有项目事实源支持；未落地内容必须标注为 `planned` 或 `strategic`。
- 不修改运行时代码、项目 gate、现有事实源或安全边界。
- 不写入密钥、令牌、个人信息、生产凭证或未经验证的经营数字。
- 内容要求详细、精彩、简练，减少跨文档重复。

---

### Task 1: 产品愿景知识域

**Files:**
- Create: `Curis Workspace/01_产品愿景/产品定位.md`
- Create: `Curis Workspace/01_产品愿景/AI公司操作系统愿景.md`
- Create: `Curis Workspace/01_产品愿景/用户画像.md`
- Create: `Curis Workspace/01_产品愿景/产品哲学.md`
- Create: `Curis Workspace/01_产品愿景/长期战略.md`
- Create: `Curis Workspace/01_产品愿景/未来十年路线.md`

**Interfaces:**
- Consumes: `knowledge/000_Project_Brief.md`、`knowledge/002_Product_Vision.md`、`AGENTS.md`。
- Produces: 全库统一的产品定义、用户边界、产品哲学和长期叙事。

- [ ] **Step 1: 写入统一 Frontmatter 和产品愿景正文**

每篇文档必须包含 `title`、`aliases`、`tags`、`status`、`updated`，并围绕“AI Task Executor MVP → AI Company System”主线写作。

- [ ] **Step 2: 建立愿景域 Wiki Link**

将产品定位连接至 AI 公司操作系统愿景、商业模式、总体架构、版本路线和融资 BP。

- [ ] **Step 3: 验证愿景边界**

Run: `rg -n "当前能力|已规划|战略方向|AI Task Executor|AI Company System" 'Curis Workspace/01_产品愿景'`

Expected: 六篇文档均能清楚区分当前产品与最终愿景。

### Task 2: 商业模式知识域

**Files:**
- Create: `Curis Workspace/02_商业模式/商业模式设计.md`
- Create: `Curis Workspace/02_商业模式/Hybrid定价模型.md`
- Create: `Curis Workspace/02_商业模式/商业护城河分析.md`
- Create: `Curis Workspace/02_商业模式/Capability经济模型.md`
- Create: `Curis Workspace/02_商业模式/AI员工商业价值模型.md`
- Create: `Curis Workspace/02_商业模式/竞品分析.md`
- Create: `Curis Workspace/02_商业模式/商业化路线图.md`

**Interfaces:**
- Consumes: `docs/decisions/commercial-package-model-v1.md`、`docs/decisions/commercial-roadmap.md`、`docs/decisions/commercial-operation-roadmap.md`、共享产品文档。
- Produces: 收入逻辑、定价框架、能力经济、价值模型、竞争定位和商业化阶段。

- [ ] **Step 1: 写入商业模型正文**

使用“订阅基础费 + AI 员工/部门套餐 + 能力用量 + 增值治理服务”的 Hybrid 叙事；所有未验证价格和经营数字仅用公式、变量或区间逻辑表达。

- [ ] **Step 2: 写入护城河与竞品框架**

将护城河拆为执行闭环、组织上下文、能力供应、治理证据、数据复利和迁移成本；竞品采用类别对比，不伪造实时市场数据。

- [ ] **Step 3: 验证商业状态标记**

Run: `rg -L "status: (current|planned|strategic)" 'Curis Workspace/02_商业模式'/*.md`

Expected: 无输出。

### Task 3: 技术架构知识域

**Files:**
- Create: `Curis Workspace/03_技术架构/总体架构.md`
- Create: `Curis Workspace/03_技术架构/Admin与Workspace边界.md`
- Create: `Curis Workspace/03_技术架构/AI员工系统.md`
- Create: `Curis Workspace/03_技术架构/Employee Template系统.md`
- Create: `Curis Workspace/03_技术架构/Department系统.md`
- Create: `Curis Workspace/03_技术架构/Workflow系统.md`
- Create: `Curis Workspace/03_技术架构/Skill系统.md`
- Create: `Curis Workspace/03_技术架构/Tool系统.md`
- Create: `Curis Workspace/03_技术架构/Capability系统.md`
- Create: `Curis Workspace/03_技术架构/Model Router.md`
- Create: `Curis Workspace/03_技术架构/Credential Vault.md`
- Create: `Curis Workspace/03_技术架构/Usage Event系统.md`
- Create: `Curis Workspace/03_技术架构/Value Event系统.md`
- Create: `Curis Workspace/03_技术架构/Billing架构.md`

**Interfaces:**
- Consumes: `knowledge/003_Architecture.md`、`shared/architecture/`、`docs/decisions/ADR-0029-model-gateway-production-security-boundary.md`、`docs/decisions/ADR-0030-workspace-tenant-model-preference-boundaries.md`、`docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`、`docs/decisions/ADR-0032-workspace-department-activation-boundaries.md`、对应 phase issue。
- Produces: 统一的 L0-L6、Admin/Workspace、执行闭环、能力系统、安全与计费架构说明。

- [ ] **Step 1: 写入总体架构和产品空间边界**

明确当前实现 gate、未来架构、运行路径和 Admin/Workspace/shared 的所有权。

- [ ] **Step 2: 写入执行与组织子系统**

分别说明 AI 员工、模板、部门、工作流、Skill、Tool、Capability 的职责、关系、状态和非目标。

- [ ] **Step 3: 写入模型、安全、事件和计费子系统**

保持模型网关单一执行路径、凭证不出 Vault、Usage Event 计量、Value Event 价值归因、Billing 消费台账的边界。

- [ ] **Step 4: 验证架构主线**

Run: `rg -n "L0|L1|L2|L3|L4|L5|L6|ModelGatewayAdapter|Credential Vault|Usage Event|Value Event" 'Curis Workspace/03_技术架构'`

Expected: 关键分层与跨系统契约均有对应说明。

### Task 4: 开发规划知识域

**Files:**
- Create: `Curis Workspace/04_开发规划/版本路线.md`
- Create: `Curis Workspace/04_开发规划/Phase状态总览.md`
- Create: `Curis Workspace/04_开发规划/Sprint记录.md`
- Create: `Curis Workspace/04_开发规划/Codex开发规范.md`
- Create: `Curis Workspace/04_开发规划/Git流程规范.md`
- Create: `Curis Workspace/04_开发规划/Research到Development流程.md`
- Create: `Curis Workspace/04_开发规划/Issue规范.md`

**Interfaces:**
- Consumes: `PROJECT_STATUS.md`、`TASKS.md`、`knowledge/CURRENT_CONTEXT.md`、`AGENTS.md`、`issues/README.md`。
- Produces: 版本、Phase、Sprint、Issue、Git 和研究转开发的统一工作方式。

- [ ] **Step 1: 提炼版本和 Phase 状态**

以当前项目事实为准，保留已完成、进行中、已批准待实施和未来 gate 四类状态。

- [ ] **Step 2: 写入开发规范**

保持五个运行席、Issue gate、验收证据、紧凑 handoff、范围与安全升级规则。

- [ ] **Step 3: 验证流程一致性**

Run: `rg -n "总控决策席|产品规划席|系统交付席|质量运行席|安全边界席|HANDOFF_REQUIRED" 'Curis Workspace/04_开发规划'`

Expected: 协作规范与 `AGENTS.md` 一致。

### Task 5: 创业历程知识域

**Files:**
- Create: `Curis Workspace/05_创业历程/项目历程.md`
- Create: `Curis Workspace/05_创业历程/关键决策.md`
- Create: `Curis Workspace/05_创业历程/架构演进记录.md`
- Create: `Curis Workspace/05_创业历程/商业模式演进.md`
- Create: `Curis Workspace/05_创业历程/失败经验记录.md`

**Interfaces:**
- Consumes: `knowledge/001_Project_History.md`、`knowledge/005_Key_Decisions.md`、ADR、issue 和 review 时间线。
- Produces: 可读的项目成长叙事、决策原因、演进路径和真实复盘。

- [ ] **Step 1: 写入项目与架构演进时间线**

按从执行器、工具系统、受控进化、Workspace 公司框架到商业多租户系统的顺序组织。

- [ ] **Step 2: 写入商业演进和失败经验**

只记录有来源支持的调整、受阻路径和经验；推演内容必须标注为战略复盘。

- [ ] **Step 3: 验证时间状态**

Run: `rg -n "2026|决策|经验|边界" 'Curis Workspace/05_创业历程'`

Expected: 五篇文档形成连续、可追溯的项目叙事。

### Task 6: 产品设计知识域

**Files:**
- Create: `Curis Workspace/06_产品设计/产品信息架构.md`
- Create: `Curis Workspace/06_产品设计/Admin Platform设计.md`
- Create: `Curis Workspace/06_产品设计/Workspace设计.md`
- Create: `Curis Workspace/06_产品设计/AI员工体验设计.md`
- Create: `Curis Workspace/06_产品设计/Workflow体验设计.md`
- Create: `Curis Workspace/06_产品设计/商业配置中心设计.md`
- Create: `Curis Workspace/06_产品设计/UI设计.md`
- Create: `Curis Workspace/06_产品设计/用户流程.md`

**Interfaces:**
- Consumes: `shared/product/`、`workspace/docs/`、`admin-platform/docs/`、已批准 UI 决策和产品流程。
- Produces: 双产品信息架构、核心体验、商业配置、界面原则和端到端用户流程。

- [ ] **Step 1: 写入双产品信息架构**

Admin Platform 面向平台运营者，Workspace 面向 CEO；共享契约不在两端重复定义。

- [ ] **Step 2: 写入关键体验**

覆盖创建公司、启用部门、配置 AI 员工、执行任务、组织工作流、查看证据、配置商业能力的完整体验。

- [ ] **Step 3: 验证产品边界**

Run: `rg -n "Admin Platform|Workspace|CEO|平台运营" 'Curis Workspace/06_产品设计'`

Expected: 双产品角色和流程无混淆。

### Task 7: 融资材料知识域

**Files:**
- Create: `Curis Workspace/07_融资材料/融资BP.md`
- Create: `Curis Workspace/07_融资材料/市场分析.md`
- Create: `Curis Workspace/07_融资材料/竞争格局.md`
- Create: `Curis Workspace/07_融资材料/为什么是现在.md`
- Create: `Curis Workspace/07_融资材料/商业模式.md`
- Create: `Curis Workspace/07_融资材料/未来估值逻辑.md`

**Interfaces:**
- Consumes: 产品愿景、商业模式、技术架构、开发进展和商业路线图知识域。
- Produces: 一套内部融资叙事底稿，不冒充正式市场尽调或财务预测。

- [ ] **Step 1: 写入融资主叙事**

形成问题、时机、方案、壁垒、商业模式、进展、路线和融资用途的完整逻辑。

- [ ] **Step 2: 写入市场与估值框架**

使用可验证方法、类别和公式说明市场与估值，不编造 TAM、收入或客户数字。

- [ ] **Step 3: 验证风险声明**

Run: `rg -n "战略|假设|验证|不构成" 'Curis Workspace/07_融资材料'`

Expected: 推演性质和验证要求清晰可见。

### Task 8: 开发文档知识域

**Files:**
- Create: `Curis Workspace/08_开发文档/API设计.md`
- Create: `Curis Workspace/08_开发文档/数据库设计.md`
- Create: `Curis Workspace/08_开发文档/Contract规范.md`
- Create: `Curis Workspace/08_开发文档/系统状态.md`
- Create: `Curis Workspace/08_开发文档/当前版本说明.md`
- Create: `Curis Workspace/08_开发文档/测试规范.md`
- Create: `Curis Workspace/08_开发文档/部署说明.md`

**Interfaces:**
- Consumes: 当前后端路由、持久化实现、shared contracts、release 文档、测试入口和本地部署说明。
- Produces: 面向研发与运维的当前接口、数据、契约、状态、测试和部署摘要。

- [ ] **Step 1: 提取当前接口与数据库事实**

只记录代码或正式契约中存在的接口、实体和存储边界；规划接口独立标注。

- [ ] **Step 2: 写入契约、状态和版本说明**

突出多租户、能力来源、事件、错误、安全和向后兼容约束。

- [ ] **Step 3: 写入测试和部署说明**

给出本地/demo 当前可验证路径，并明确 hosted production 仍受 gate 与安全条件约束。

- [ ] **Step 4: 验证技术事实**

Run: `rg -n "POST /api/task|GET /api/tasks|SQLite|local/demo|生产" 'Curis Workspace/08_开发文档'`

Expected: 当前接口、存储和部署边界均可定位。

### Task 9: 全库一致性与 Obsidian 验收

**Files:**
- Verify: `Curis Workspace/**/*.md`

**Interfaces:**
- Consumes: Tasks 1-8 的 60 篇文档。
- Produces: 可直接打开、链接完整、状态一致、无敏感信息的 Obsidian 文档包。

- [ ] **Step 1: 验证目录和文件数量**

Run: `find 'Curis Workspace' -type d | sort && find 'Curis Workspace' -type f -name '*.md' | wc -l`

Expected: 根目录加八个分类目录；Markdown 文件数为 `60`。

- [ ] **Step 2: 扫描空文件和占位符**

Run: `find 'Curis Workspace' -type f -name '*.md' -size 0 -print; rg -n "TBD|TODO|待补充|占位符" 'Curis Workspace' || true`

Expected: 无空文件；无未完成占位内容。

- [ ] **Step 3: 验证 Frontmatter**

Run: `for f in 'Curis Workspace'/**/*.md; do head -1 "$f" | grep -qx -- '---' || echo "$f"; done`

Expected: 无输出。

- [ ] **Step 4: 验证 Wiki Link 目标**

提取所有 `[[目标]]`，按文件名和相对路径检查目标存在；Expected: 零失效链接。

- [ ] **Step 5: 扫描敏感信息和事实冲突**

Run: `rg -n "api[_-]?key|secret|token|password|sk-[A-Za-z0-9]" 'Curis Workspace' || true`

Expected: 仅允许安全边界说明中的通用术语，不得出现凭证值。

- [ ] **Step 6: 检查变更范围**

Run: `git status --short && git diff --check`

Expected: 只有计划文件、设计文件和 `Curis Workspace/` 文档包相关变更；无空白错误。

