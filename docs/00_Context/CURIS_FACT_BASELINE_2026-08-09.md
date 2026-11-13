# Curis 当前事实基线（2026-08-09）

Status: Review

Baseline: `main @ dd77c6724`（审计现场，不代表已批准产品基线）

本文件记录复位前的现场事实。它不是产品定义，也不授予任何文件当前产品权威。
本文件中的 Blueprint 4.4、旧前端和旧原型统计是审计时点快照；后续升级到 Blueprint 5.0 的内容不回写本快照，阅读当前状态必须回到 `CURRENT_STATE.md`。Blueprint 5.0 是当前产品目标形态，本文不再作为开发依据。
目标是把 Blueprint、旧前端、HTML 原型、WorkBuddy 产物和运行数据分开，供迁移决策使用。

## 1. 审计现场

| 项目 | 事实 | 结论 |
| --- | --- | --- |
| Git | `main @ dd77c6724`，工作树包含已修改和未跟踪文件 | 不是干净交付基线，必须先冻结 |
| 前端 | `frontend/`，Next.js；当前发现 54 个 `page.js` | 仍包含 Project/Task、Execution、开发者和实验入口 |
| 原型 | `curis-ui-prototype/` 顶层 20 个 HTML | 与前端、Blueprint 并非同一运行时 |
| 桌面 | Tauri 壳运行本机 FastAPI + Next sidecar | 当前是本机开发运行壳，不是独立分发产品 |
| 数据库 | `backend/data/curis.sqlite`、`data/*.sqlite`、多个 `.db` 并存 | 数据事实源需要重新确认，不能按文件名推断 |
| 产品 Blueprint | `docs/01_Product/Curis_Product_Blueprint.html`，4.4，Status: Review | 目标定义尚未冻结 |
| 当前事实入口 | `docs/00_Context/CURRENT_STATE.md` | 其批准基线仍是 `c0e1855f`，与审计现场有漂移 |

## 2. 三套产品心智

### 2.1 旧执行系统

```text
Project → Task → Workflow → Execution → Artifact
```

主要证据：`frontend/app/ceo-office/execution/`、`execution/pipeline/`、
`runtime-trace/`、`projects/` 以及旧的 Project/Task 说明文档。

### 2.2 HTML 原型系统

```text
固定业务类型 → 固定办公室 → 运行现场
```

主要证据：`curis-ui-prototype/`、`canonical-nav.js`、固定 software/xhs/shortvideo
页面和 localStorage 演示状态。

### 2.3 当前目标产品

```text
CEO → Company → CEO Assistant → AI Team
→ Business → Workspace → External Result
→ Evidence / Acceptance → CEO Decision → Company Change
```

这是当前唯一应该继续发展的产品心智，但必须吸收前端 UI 中已经证明必要的引导、
状态和交互链路，再回写到 Blueprint 后才能实现。

## 3. 当前可确认能力

| 能力 | 现场状态 | 产品判断 |
| --- | --- | --- |
| Next.js 构建 | `pnpm build` 可通过 | 工程构建存在，不代表产品闭环完成 |
| Lint | 当前存在 `<a>` 内链、渲染期副作用和依赖警告 | 不能作为稳定交付基线 |
| DeepSeek | 私有模型注册、绑定和一次真实 Task 执行已验证 | 执行能力已验证 |
| CEO Operating Day | 页面/API 存在 | Company 范围与 Assistant 范围不一致 |
| CEO Assistant | 抽屉和 Snapshot 存在，Identity 为空 | 第一位 AI 员工尚未成立 |
| Business | 14 个 Project/graph 记录可见 | 不是业务版图，且混入多 Company/fixture |
| Workspace | 门户为空，Studio 是基础表单 | 业务到工作空间的运行链未成立 |
| Meeting / Finance / Calendar | 页面显示“规划中” | 不能作为已交付产品入口 |

## 4. 复位基线结论

当前 Curis 是“已验证 AI 执行能力的 Project/Task-first 本地系统”，不是已验证的
Company OS。产品复位范围现为三条同步验证轨道：**研发工作台、小红书运营工作台、抖音 / TikTok 运营工作台**。
研发工作台的第一个真实 dogfood 任务是“Curis 的自研发”（工作项名：完善 Curis），不是新的业务类型；三条轨道同步完成
Workspace 视觉、外部结果和运行设计，且必须使用真实 Company / Business / Workspace 数据，
不得以固定演示数据代替运行事实。

## 5. 使用规则

1. 本文件只作为复位现场证据，不能覆盖 `CURRENT_STATE.md`、Frozen Decision 或当前 Blueprint。
2. 任何文件要恢复为当前产品依据，必须在迁移清单中标记 `Retain`，并通过产品评审。
3. 任何删除、移动数据库或改写历史记录前，必须完成引用扫描和备份。
