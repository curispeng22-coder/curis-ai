# 桌面 Shell 原型框架 · 1440 × 900

Status: Draft（本轮交付物说明，非产品文档）
Scope: 只画 App Shell 框架与可见折叠交互；不含任何业务页面、业务数据或占位内容。

文件：`curis-ui-prototype/shell-frame-1440x900.html`（单文件、零依赖、直接打开即可操作）
截图：`curis-ui-prototype/_shots-shell-frame/`（01 默认 / 02 仅 T2 / 03 四栏同开 / 04 仅 T3 / 05 拖拽后 / 06 导航收起 + `frame-check.json`）

## 1. 依据的当前权威

| 内容 | 来源 |
| --- | --- |
| 七个一级区域与固定顺序（CEO 工作台、业务空间、组织中心、人才与能力、经营洞察、资料库、会议） | `docs/01_Product/Curis_Product_UI_Blueprint.html` §11、§06；`docs/reviews/CURIS_V1_PRODUCT_FREEZE.md` |
| 一级导航 220px、当前态＝低对比 selected surface + 3px accent 指示、不用 emoji | 同上 §11 |
| 主工作区最小 560px、顶部 52px、内容 padding 24px、无辅助空间时吃满剩余宽度 | 同上 §11 |
| Context 按需 256px、可折叠至 0；Utility 按需 320–440px 可拖拽、默认关闭 | 同上 §11 |
| Four-Pane 是四职责、Nav+Main 默认、Context/Utility 按需、不得四列常驻或永久留空；T1/T2/T3 位置与双向契约；Pane-local Header；Utility Maximize | `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §1.1 / §1.5 / §1.5.1 |
| 主画布 / 表面 / 线 / 文字色（Light：Canvas `#F7F8FA`、Base `#FFFFFF`、Surface1 `#F1F3F5`、Surface2 `#E9EDF1`、Border `#DDE2E7`、Text `#1D232A`、Text2 `#4D5661`、Muted `#7C8794`、Disabled `#AAB2BC`） | `docs/03_Design/CURIS_VISUAL_STANDARD_V1.md` |
| 深灰蓝导航 `#3A4A52`（已接受探索 Writing `--rail` / Music `--nav`）、交互强调色 `#8FB850` | 已接受的三份业务 HTML 探索 + `CURIS_COLOR_DIRECTION_EXPLORATION/06_HYBRID_NOTES.md` |

配色说明：本帧不发明新配色。导航按本轮指令取已接受探索的深灰蓝并**不使用紫色**；`CURIS_VISUAL_STANDARD_V1.md` 记录的 `#806BE5` 未用于导航，该冻结文档**未做任何修改**，与它的差异作为待 CEO 决定的 Authority 对齐项登记（不在本轮处理）。导航左上三个窗口圆点是 macOS 系统窗口控件，不属于产品配色。

## 2. 结构（四栏职责，不是四列常驻）

- 第一栏 Navigation（220px，可完全收起）：窗口控件 + 对象搜索 + T1；七个一级区域；`最近对话` 分组；底部用户中心（头像 / CEO（你）/ 公司负责人 / 设置）。
- 第二栏 Context（按需 256px，208–360 可拖拽）：当前对象上下文。默认关闭；帧内显示诚实空态“当前没有选中对象”。
- 第三栏 Main（最小 560px，始终存在并优先占宽）：Pane-local Header（T1 转移位 / T2 / 面包屑 / 通知 / T3 / 更多）+ 主工作区。帧内不填业务页面，只显示空态。
- 第四栏 Utility（按需 360px，320–440 可拖拽）：当前对象的详情 / 证据 / 工具。默认关闭；展开后 T3 从 Main Header 转移到 Utility Header，并提供 Maximize。
- CEO Assistant：右下轻量悬浮覆盖入口，**不占栏、不是第五栏**（`.shell` 始终只有四个子节点）。

本帧没有第五栏、没有独立 ✕、没有 emoji 图标、没有演示数据标注条、没有产品介绍长文；`最近对话` 无真实记录时显示“还没有最近对话”，不造假数据。

## 3. 可见交互

| 操作 | 结果 |
| --- | --- |
| T2（Main Header 左侧） | 双向开合 Context；不影响 Utility |
| T3（折叠态在 Main Header 右侧） | 双向开合 Utility；展开后入口转移到 Utility Header 右侧 |
| T1（Navigation Header 右侧） | 完全收起/展开 Navigation；收起后入口转移到 Main Header 最左 |
| 拖拽 Context 右缘 / Utility 左缘 | 宽度受 208–360 / 320–440 限制，且 Main 永不低于 560px |
| 点击一级区域 | 只切换当前态与面包屑（原型内不进入业务页面） |

## 4. 已测结果（真实点击与拖拽，`frame-check.json`）

`assertions 32 · passed 32 · failed 0`

- 台面实测 1440 × 900；
- 默认 Nav + Main：Context / Utility 均关闭，Main = 1220px；
- 仅 T2：220 + 256 + 962 = 1440，Main 仍最宽；
- T2 + T3：220 + 256 + 604 + 360 = 1440，Main = 604px ≥ 560 且为最宽栏；
- 收起 Context 不影响 Utility（220 + 858 + 360 = 1440）；
- 拖拽 Utility 至下限 320 / 上限（该布局下受 Main≥560 约束为 404，而非 440）；
- T1 收起导航后 Main 吃掉 220px，T1 出现在 Main Header 最左并可恢复；
- CEO Assistant 为 `position:absolute` 覆盖层、父节点不是 `.shell`。

## 5. 本帧不包含（按本轮指令）

业务空间 / 组织中心 / 人才与能力 / 经营洞察 / 资料库 / 会议的具体页面，三种业务（内容增长 / 写作 / 音乐）页面，任何真实数据、结果、证据或未来占位内容；也未改动 `curis-ui-prototype/` 既有原型页面与任何冻结文档。
