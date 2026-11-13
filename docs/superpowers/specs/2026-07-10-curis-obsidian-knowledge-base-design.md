# Curis Workspace Obsidian 知识库设计

日期：2026-07-10

## 目标

在不改变现有项目事实源的前提下，生成一套可直接作为 Obsidian Vault 使用的 Curis Workspace 中文知识库。知识库应完整表达产品愿景、商业逻辑、技术架构、开发历程、产品设计与融资故事，同时保持内容精彩、简练、可持续维护。

## 目标读者

- 创始人：统一长期愿景、阶段目标和关键判断。
- 产品与研发团队：快速理解边界、架构与当前进度。
- 潜在合作伙伴和投资人：理解市场机会、商业模式与竞争壁垒。
- 后续 AI 协作者：通过结构化事实与链接快速建立项目上下文。

## 内容原则

采用“完整创业叙事版”，但明确区分三种状态：

1. **当前能力**：已有代码、验收记录或正式项目状态支持的事实。
2. **已规划能力**：已有产品决策、架构决策或路线图支持，但尚未全部实现。
3. **战略方向**：为形成完整商业与融资叙事而补全的长期推演、市场判断和建议。

不得把战略推演写成已实现事实，不得覆盖或取代 `PROJECT_STATUS.md`、`TASKS.md`、`knowledge/`、`issues/`、`reviews/` 和正式 ADR。

## 输出位置

知识库根目录：

```text
/Users/yy/Documents/Curis AI Workspace/Curis Workspace/
```

该目录作为面向阅读与传播的 Obsidian 知识层；原项目文档继续作为开发事实源。

## 信息架构

```text
Curis Workspace/
├── 01_产品愿景/
│   ├── 产品定位.md
│   ├── AI公司操作系统愿景.md
│   ├── 用户画像.md
│   ├── 产品哲学.md
│   ├── 长期战略.md
│   └── 未来十年路线.md
├── 02_商业模式/
│   ├── 商业模式设计.md
│   ├── Hybrid定价模型.md
│   ├── 商业护城河分析.md
│   ├── Capability经济模型.md
│   ├── AI员工商业价值模型.md
│   ├── 竞品分析.md
│   └── 商业化路线图.md
├── 03_技术架构/
│   ├── 总体架构.md
│   ├── Admin与Workspace边界.md
│   ├── AI员工系统.md
│   ├── Employee Template系统.md
│   ├── Department系统.md
│   ├── Workflow系统.md
│   ├── Skill系统.md
│   ├── Tool系统.md
│   ├── Capability系统.md
│   ├── Model Router.md
│   ├── Credential Vault.md
│   ├── Usage Event系统.md
│   ├── Value Event系统.md
│   └── Billing架构.md
├── 04_开发规划/
│   ├── 版本路线.md
│   ├── Phase状态总览.md
│   ├── Sprint记录.md
│   ├── Codex开发规范.md
│   ├── Git流程规范.md
│   ├── Research到Development流程.md
│   └── Issue规范.md
├── 05_创业历程/
│   ├── 项目历程.md
│   ├── 关键决策.md
│   ├── 架构演进记录.md
│   ├── 商业模式演进.md
│   └── 失败经验记录.md
├── 06_产品设计/
│   ├── 产品信息架构.md
│   ├── Admin Platform设计.md
│   ├── Workspace设计.md
│   ├── AI员工体验设计.md
│   ├── Workflow体验设计.md
│   ├── 商业配置中心设计.md
│   ├── UI设计.md
│   └── 用户流程.md
├── 07_融资材料/
│   ├── 融资BP.md
│   ├── 市场分析.md
│   ├── 竞争格局.md
│   ├── 为什么是现在.md
│   ├── 商业模式.md
│   └── 未来估值逻辑.md
└── 08_开发文档/
    ├── API设计.md
    ├── 数据库设计.md
    ├── Contract规范.md
    ├── 系统状态.md
    ├── 当前版本说明.md
    ├── 测试规范.md
    └── 部署说明.md
```

## 导航设计

知识库严格保留用户指定的八大类目和 60 篇主题文档，不增加额外类目或根级入口文件。每篇文档使用 Obsidian Wiki Link 连接上游与下游主题，并在文首给出所属领域、内容状态和关键关联，在文末提供“相关文档”和“事实依据”小节。`01_产品愿景/产品定位.md` 同时承担全库叙事入口，`08_开发文档/系统状态.md` 承担当前事实入口。

## 文档统一结构

每篇 Markdown 文档包含精简 YAML 属性：

```yaml
---
title: 文档标题
aliases: []
tags: [curis]
status: current | planned | strategic
updated: 2026-07-10
---
```

正文根据主题选用以下模块，不机械堆满：

- 核心结论
- 为什么现在做
- 产品或系统设计
- 当前进展
- 边界与非目标
- 关键指标或验证方式
- 下一阶段
- 相关文档
- 事实依据

## 叙事主线

整套知识库围绕一条统一主线展开：

> Curis Workspace 从 AI Task Executor MVP 起步，先证明 AI 可以稳定、可追踪、可治理地完成任务，再逐步构建部门、AI 员工、工作流、能力供应与经营系统，最终成为面向个人创业者和小型组织的商业化多租户 AI Company System。

商业叙事强调：从“出售单次 AI 能力”升级为“交付一家公司可持续运行的数字组织基础设施”。

技术叙事保留 L0-L6 分层、v1.8 受控进化、Task 执行闭环、Workspace/Admin Platform 分离、多租户边界、官方与租户私有能力分层，以及模型网关和安全边界。

## 事实来源优先级

1. `AGENTS.md`：当前 gate、允许范围、禁止范围与协作协议。
2. `PROJECT_STATUS.md`、`TASKS.md`、`knowledge/CURRENT_CONTEXT.md`：当前进度。
3. `knowledge/000_Project_Brief.md`、`knowledge/002_Product_Vision.md`、`knowledge/003_Architecture.md`：产品和架构基线。
4. `docs/decisions/`：正式架构与商业决策。
5. `issues/` 与 `reviews/`：实施范围和验收证据。
6. `shared/`、`workspace/`、`admin-platform/`：产品空间与跨产品契约。

发生冲突时，以更新日期更近且治理层级更高的正式事实源为准，并在知识库中保留清晰的“当前 / 已规划 / 战略”标记。

## 质量标准

- 所有用户指定文档均存在，无空文件或占位符。
- 首页和文内链接可在 Obsidian 中正常导航。
- 产品定位、商业模式、总体架构、路线图、系统状态之间不存在阶段冲突。
- 当前能力均能追溯到项目事实源。
- 长期商业与融资推演不伪装成已经验证的数据。
- 不写入密钥、令牌、个人信息或生产凭证。
- 单篇文章以高信息密度为主，避免重复完整愿景和架构说明。

## 验证方式

- 检查八个目录和 60 个 Markdown 文件完整性。
- 扫描 `TODO`、`TBD`、空标题和失效 Wiki Link。
- 对照核心事实源检查产品阶段、架构层级、接口、数据模型和已完成进度。
- 检查当前、已规划、战略三种状态是否使用一致。
- 检查 Git 差异，确保不修改运行时代码或现有事实源。

## 非目标

- 不重构现有项目目录。
- 不迁移或删除现有 `knowledge/`、`docs/`、`issues/`、`reviews/`。
- 不修改产品 gate、实现范围或安全边界。
- 不把知识库直接作为生产配置或运行时数据源。
- 不伪造市场规模、收入、客户数量或融资数据。
