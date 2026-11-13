# Curis Product Blueprint v1.0 · 验收审核

> ⚠️ **本审核结论已失效（INVALIDATED）。**
> 原因：评审基线错误——当时仅依据旧代码路由与旧一级结构（战略会议室 / 头脑风暴室 / 决策中心等）做一致性核验，未采用最新冻结产品定义、八大一级结构、CEO Office 方案、Assistant Runtime 与 Runtime View 决议。
> 该审核所对应的产物（`Source` 指向的、于 Curis 项目空间之外生成的旧 Blueprint）已被标记为 **REJECTED — Generated Outside Curis Project Context**，归档于 `docs/99_Archive/curis_blueprint_rejected/`。
> 唯一 Current Product Blueprint 已重建为 `docs/01_Product/Curis_Product_Blueprint.html`，并由独立 Agent 按最新冻结基线重新复审（见 `reviews/20260731_curis_product_blueprint_v1_rereview.md`）。
> 本文件仅作历史失败记录保留，其「达标，可作为唯一 Current」结论不再有效。

Status: Review

Date: 2026-07-31

Baseline: `main @ c0e1855f`

Artifact: `docs/01_Product/Curis_Product_Blueprint.html`

Source: `/Users/yy/Workbuddy/2026-07-31-01-07-06/Curis_Product_Blueprint_v1.0.html`

---

## 1. 结论

**达标，可作为唯一 Current Product Blueprint 使用；Status 定为 `Review`，不直接 `Frozen`。**

原因：交付物本身完整度、准确度、可执行性都达到"设计师照着画、开发照着做"的标准；
但文档自带 12 条未裁决开放问题（Q-1～Q-12），其中 3 条会改变页面存废与导航结构。
在这些问题被裁决前，Blueprint 不具备"不可再议"的 Frozen 属性。

## 2. 归档处置

| 项 | 处置 |
| --- | --- |
| 主交付物 | 复制到 `docs/01_Product/Curis_Product_Blueprint.html` |
| 文件命名 | **去掉版本号**。用户要求"唯一 Current Blueprint、禁止平行版本"，带 `v1.0` 的文件名必然催生 `v2.0` 第二个文件。版本号改为文档内声明 |
| `build/*.html` 分片 | 不迁移。属中间构建产物，可由主文件再生 |
| 旧 Blueprint | 仓库内无同名当前 Blueprint 需替换；历史 Workspace Blueprint 已在 `docs/99_Archive/curis_workspace_blueprint/`，保持 Deprecated |
| 治理登记 | `CURRENT_STATE.md` §11a、`Curis_Product_Context.md` References、`CHANGE_LOG.md`、`AGENTS.md` Product Blueprint 段 |

## 3. 交付要求对照

| # | 用户要求 | 结论 | 证据 |
| --- | --- | --- | --- |
| 01 | Product Vision | 达标 | §1.1～1.5，含"Curis 不是什么"反向定义 |
| 02 | Product Architecture | 达标 | §2.1 分层、2.2 对象模型、2.3 十模块关系、2.4 技术运行架构 |
| 03 | Feature Map | 达标 | §3.1 总览 + §3.2 十模块逐项明细 |
| 04 | Page Map | 达标 | §4.1 全 28 页清单（ID/路由/模块/状态/层级）+ 历史页面判定表 + §4.2 导航 + §4.3 关系图 |
| 05 | Page Blueprint（重点） | 达标 | P-00～P-27 共 28 页，每页含 页面目标 / ASCII 低保真布局 / 区域说明表（展示内容·为什么存在·更新方式）/ 页面状态 / 页面权限 / 跳转关系 |
| 06 | Interaction Blueprint（重点） | 达标 | 117 条 `IX-*` 交互链，统一六段式（触发→前端行为→后端触发→数据变化→界面反馈→落点）+ 三条全局红线 + 完整性自检表 |
| 07 | Workflow Blueprint | 达标 | W1～W8 八条主工作流 + 相互关系说明 |
| 08 | Runtime Collaboration | 达标 | Runtime 清单、协作时序、10 态状态机、事实源约定表 |
| 09 | Design Principles | 达标 | 参照坐标 + 六条视觉原则 + 设计语言基线 + 反面清单；未越界画 UI |
| 10 | Development Constraints | 达标 | 唯一性 / 变更顺序 / 一致性 / 数据真实性 / 安全 / 范围六类约束 |
| — | HTML 单文件 | 达标 | 334KB 单文件，**零外部依赖**（无 CDN、无外链），断网可读 |
| — | 导航可点击 | 达标 | 93 锚点 / 450 内链，**断链 0**；侧栏过滤、面包屑联动、主题切换、回顶 |
| — | 所有图统一风格 | 达标 | 47 个 `<pre>` ASCII 图统一栅格与线型；85 张表统一表头语义 |

## 4. 事实准确度抽查

对照 `frontend/app` 真实路由与 `CURRENT_STATE.md` 交叉核验：

- **路由**：Blueprint 列出的 31 条路由，除 1 处笔误外全部与真实 `app/` 目录一致。
- **LIVE / DRAFT 判定**：抽查 6 个标 DRAFT 的页面（decisions / reports /
  strategy-room / company-runtime / settings / analytics），源码中数据请求数为
  0（analytics 为 1，文档标"混合"），判定与代码事实一致。**未把样例快照说成已交付能力**。
- **历史页面判定**：`/`、`/projects/[project_id]`、`/platform*` 标为
  LEGACY / FUTURE / REDIRECT，与 `CURRENT_STATE.md` §8 Deprecated Directions 一致。

## 5. 审核中发现并已修正的缺陷

| # | 严重度 | 问题 | 修正 |
| --- | --- | --- | --- |
| D-1 | 中 | P-27 Assistant 可见范围写成 5 条**具体路由**，并据此在 Q-1 断言"其余 CEO 路由用户会突然失去助手"。实际实现 `frontend/components/assistant/GlobalAssistant.js:31` 是 **前缀匹配**（`WORKSPACE_PREFIXES`），`/ceo-office` 前缀已覆盖全部子路由——原描述会误导开发去做一个已经存在的能力 | 可见范围表改写为前缀规则，补齐不可见清单（`/`、`/login`、`/onboarding`、`/control/*`、`/platform/*`） |
| D-2 | 低 | 同表出现 `/ceo-office/employees`，真实路由为 `/ceo-office/organization/employees` | 已随 D-1 一并重写 |
| D-3 | 中 | Q-1 问题描述基于 D-1 的错误前提 | 重写 Q-1：真正待裁决的是另外 4 个 LEGACY 前缀（`/projects`、`/employees`、`/capabilities`、`/org-center`）是否随页面退役一并移除，与 Q-2 / Q-11 联动 |

修正后复验：断链 0、标签配平、28 页齐全、85 表 47 图不变。

## 6. 遗留风险与待裁决项

Blueprint §11.2 的 Q-1～Q-12 需 CEO 逐条裁决。按影响面排序，以下 4 条建议优先：

| 优先 | 编号 | 为什么先决 |
| --- | --- | --- |
| 1 | **Q-5 设置持久化** | 公司名称改不了 = 全局抬头与助手身份卡拿不到正确身份，是身份缺失不是小瑕疵 |
| 2 | **Q-6 CEO 四页数据来源** | P-03～P-08 占 CEO 模块大半篇幅却是样例快照，长期停留会让整个 CEO Office 失去可信度 |
| 3 | **Q-2 + Q-11 页面退役** | 决定 P-14 是否唯一项目工作台，直接影响 Page Map、导航与 Assistant 前缀清单 |
| 4 | **Q-8 Project 删除契约** | 与 `CURRENT_STATE.md` 的 `BLOCKED_PENDING_CONTRACT` 同一阻塞项，未定契约前按钮保持置灰 |

裁决结果**直接回写本 Blueprint 对应章节**，不另起文档。全部裁决完成后
将 §11a Status 由 `Review` 改为 `Frozen`。

## 7. 边界声明

- 本次仅做归档、登记与文档级缺陷修正，**未改动任何业务代码**。
- Blueprint 描述**目标态**；`docs/00_Context/CURRENT_STATE.md` 描述**已交付事实**。
  两者冲突时，已交付事实以 Current State 为准，目标设计以 Blueprint 为准。
- 未将 Blueprint 中 DRAFT / PLANNED 内容登记为已完成能力。
