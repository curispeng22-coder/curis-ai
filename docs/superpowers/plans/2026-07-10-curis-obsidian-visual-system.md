# Curis Workspace Obsidian Visual System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为现有 60 篇 Curis Workspace 中文知识文档加入兼容 Obsidian 的双层 Mermaid 视觉系统，使愿景、商业、架构、流程和开发状态可以快速理解。

**Architecture:** 直接在现有 Markdown 中插入 Mermaid fenced block，不新增图片资产或外部依赖。按八个知识域分批修改，每批独立检查 fenced block 数量、闭合、关键语义和 Git 差异，最终运行全库链接、敏感信息与回归验证。

**Tech Stack:** Markdown、Obsidian、Mermaid、ripgrep、Git。

## Global Constraints

- 图中中文优先，保留必要的 Task、Workflow、Skill、Tool、Capability、Billing 等术语。
- 优先使用 `flowchart`、`sequenceDiagram`、`stateDiagram-v2`、`erDiagram`。
- 一张图只表达一个中心结论，节点原则上不超过 15 个。
- 当前能力与未来 gate 必须在图中文字或线型中明确区分。
- 不引入外部资源、图片文件、插件、运行时代码或新产品承诺。
- 保留现有 Frontmatter、Wiki Link、事实依据和状态字段。

---

### Task 1: 产品愿景与商业模式视觉化

**Files:**
- Modify: `Curis Workspace/01_产品愿景/*.md`
- Modify: `Curis Workspace/02_商业模式/*.md`

**Interfaces:**
- Consumes: 现有产品定位、战略与商业正文。
- Produces: 产品进化、AI 公司系统、战略飞轮、十年路线、Hybrid 定价、护城河和商业化路线图。

- [ ] **Step 1:** 在 13 篇文档中加入 13 张高层 Mermaid 图。
- [ ] **Step 2:** 删除与新增图完全重复的 ASCII 流程块，保留解释正文。
- [ ] **Step 3:** 运行 `rg -n '^```mermaid$' 'Curis Workspace/01_产品愿景' 'Curis Workspace/02_商业模式'`，预期至少 13 个结果。
- [ ] **Step 4:** 运行 `git diff --check` 并提交 `docs(visual): illustrate vision and business knowledge`。

### Task 2: 技术架构视觉化

**Files:**
- Modify: `Curis Workspace/03_技术架构/*.md`

**Interfaces:**
- Consumes: L0-L6、执行链、双产品、员工、工作流、能力、安全、事件与 Billing 正文。
- Produces: 14 篇技术文档的架构图、关系图、时序图和状态图。

- [ ] **Step 1:** 为 14 篇技术文档各加入至少一张 Mermaid 图。
- [ ] **Step 2:** 在总体架构、Workflow、Credential Vault、Usage/Value/Billing 中使用细化流程或时序图。
- [ ] **Step 3:** 运行 `rg -n '^```mermaid$' 'Curis Workspace/03_技术架构'`，预期至少 14 个结果。
- [ ] **Step 4:** 运行 `git diff --check` 并提交 `docs(visual): illustrate technical architecture`。

### Task 3: 开发规划与创业历程视觉化

**Files:**
- Modify: `Curis Workspace/04_开发规划/*.md`
- Modify: `Curis Workspace/05_创业历程/*.md`

**Interfaces:**
- Consumes: 版本、Phase、Sprint、五席、Research/Issue 与项目演进正文。
- Produces: 路线、生命周期、协作和演进图。

- [ ] **Step 1:** 为版本、Phase、Sprint、Codex 五席、Research-to-Development、Issue 加入流程图。
- [ ] **Step 2:** 为项目历程、架构演进、商业演进加入时间/阶段图。
- [ ] **Step 3:** 运行 `rg -n '^```mermaid$' 'Curis Workspace/04_开发规划' 'Curis Workspace/05_创业历程'`，预期至少 9 个结果。
- [ ] **Step 4:** 运行 `git diff --check` 并提交 `docs(visual): illustrate delivery and evolution`。

### Task 4: 产品设计与融资视觉化

**Files:**
- Modify: `Curis Workspace/06_产品设计/*.md`
- Modify: `Curis Workspace/07_融资材料/*.md`

**Interfaces:**
- Consumes: 双产品 IA、员工/工作流体验、UI、用户流程与融资叙事。
- Produces: 产品地图、页面骨架、用户旅程、BP 逻辑、市场进入与估值阶梯。

- [ ] **Step 1:** 为 8 篇产品设计文档各加入至少一张 Mermaid 图。
- [ ] **Step 2:** 为融资 BP、市场分析和估值逻辑加入 3 张高层图。
- [ ] **Step 3:** 运行 `rg -n '^```mermaid$' 'Curis Workspace/06_产品设计' 'Curis Workspace/07_融资材料'`，预期至少 11 个结果。
- [ ] **Step 4:** 运行 `git diff --check` 并提交 `docs(visual): illustrate product and financing narratives`。

### Task 5: 开发文档视觉化

**Files:**
- Modify: `Curis Workspace/08_开发文档/*.md`

**Interfaces:**
- Consumes: API、数据库、Contract、系统状态、测试和部署正文。
- Produces: API 边界、数据域、契约层、系统状态、测试金字塔和部署拓扑。

- [ ] **Step 1:** 在 API、数据库、Contract、系统状态、测试和部署文档中加入 6 张 Mermaid 图。
- [ ] **Step 2:** 确保图只总结现有事实，不新增路由、表或生产承诺。
- [ ] **Step 3:** 运行 `rg -n '^```mermaid$' 'Curis Workspace/08_开发文档'`，预期至少 6 个结果。
- [ ] **Step 4:** 运行 `git diff --check` 并提交 `docs(visual): illustrate developer documentation`。

### Task 6: Obsidian 与全仓验收

**Files:**
- Verify: `Curis Workspace/**/*.md`

**Interfaces:**
- Consumes: Tasks 1-5 的 Mermaid 图。
- Produces: 可在 Obsidian 原生渲染、原知识结构不退化的视觉知识库。

- [ ] **Step 1:** 统计 Mermaid 图不少于 50 张。
- [ ] **Step 2:** 检查 Mermaid fenced block 开闭数量一致。
- [ ] **Step 3:** 检查文档仍为 60 篇、Wiki Link 零失效、Frontmatter 与状态零异常。
- [ ] **Step 4:** 扫描占位符和敏感凭证值，预期零命中。
- [ ] **Step 5:** 使用临时 SQLite 运行后端全量测试；运行前端 lint 与 build。
- [ ] **Step 6:** 检查 Git 范围，保留用户已有 `.workbuddy` 改动并完成分支交付。

