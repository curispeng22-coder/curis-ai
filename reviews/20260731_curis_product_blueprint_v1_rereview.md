# Curis Product Blueprint v1.0 · 独立复审（重建版）

Status: Review

Date: 2026-07-31

Baseline: 最新冻结产品定义（CURRENT_STATE / Product_Context / Architecture / Design_System / Engineering_Convention / ADR-0033）+ 本次重建任务给定的最新八大一级结构、CEO Office 方案、Assistant Runtime 与 Runtime View 决议

Artifact: `docs/01_Product/Curis_Product_Blueprint.html`

Reviewer: 独立 general-purpose Agent（项目空间内，未参与生成）

## 判定：PASS-WITH-NOTES

可提升为唯一 Current Product Blueprint；转 Frozen 前须先裁决第 13 章 Q-1～Q-4。

## Q1–Q7 答复

- **Q1 是不是现在的 Curis**：是。定位（非任务管理器）、对象层级（CEO→Company→Business Department→Employee→Project→Task→Artifact，Capability 属 Employee，Knowledge/Memory 属资产层，Assistant 属 Runtime）、八大一级模块、CEO Office 结构、Assistant Runtime（ADR-0033）、Runtime View 均对齐冻结基线。
- **Q2 是否混入旧产品**：否。战略会议室 / 头脑风暴室 / 决策中心 / 旧项目中心 / 旧组织中心 / 旧经营分析 / 旧执行工作台 全文命中 0；仅作为排除项出现。明确「路由为目标态表达，不代表当前代码必已实现」。
- **Q3 只看这一份能否理解完整产品**：可以。覆盖定义/对象/模块/功能地图/页面地图/23 页蓝图/交互/16 流程/Runtime 架构/Runtime View/设计规则/MVP 边界/开放决策。
- **Q4 每页是否真画出来**：是。24 个 HTML/CSS 低保真窗体，含 Top Bar/左导航/主内容/右面板/卡片/表格/进度条/环形指标/对话框；`<pre>` ASCII 数量为 0。
- **Q5 可否直接进高保真**：可以。每页配「区域/展示/为什么/更新方式/状态/权限/跳转」七列表 + 状态覆盖。
- **Q6 建议成为唯一 Current**：建议。60 锚点零断链；外部依赖 0；单文件 ~114KB 离线可开；深/浅双主题 + localStorage。
- **Q7 建议 Frozen**：暂不。须先裁决 Q-1～Q-4。

## 技术核验

- 断链 0；外部依赖 0（无 CDN/http/img/link/script src）；单文件；深/浅双主题。
- Assistant Command 创建 Task：c02 §2.2、c07 铁律、c07 P-01 表、c08 F7、c09 协作主干均声明「Command 创建并启动既有 Task，不绕过业务服务」。通过。

## 复审发现的缺陷（已在生成后修复）

| 级别 | 位置 | 问题 | 状态 |
|---|---|---|---|
| P1 | section 包裹 | 章节无 `<h2>` 标题、导航仅显示数字 | 已修复：assemble 现注入 `<h2>` 并使用完整章节标题 |
| P1 | p01 | 顶栏标「导航默认折叠」但 mock 仍渲染完整导航 | 已修复：p01 mock 渲染折叠态（仅圆点） |
| P1 | CURRENT_STATE §11a | 旧登记「28 页 / Q-1～Q-12 / 附录 11.2」与新版不符 | 已修复：更新为 23 页 / Q-1～Q-4 / 无附录 |
| P2 | 页面导航标签 | `CEO Office`/`Knowledge` 与 c03 `Company`/`Knowledge Assets` 不一致 | 已修复：页面导航对齐模块名 |
| P2 | p23 | 登录页渲染完整工作区导航 | 已修复：p23 渲染极简登录导航 |
| P2 | 工具栏 `☰ 导航` | `collapseBtn2` 无事件 | 已修复：绑定折叠 |
| P2 | c01 §1.5 | 「（见排除清单）」悬空引用 | 已修复：移除悬空引用 |
| P2 | scroll-spy | 仅 observe `section[id]`，页面级高亮失效 | 已修复：同时 observe 页面 `div.psec` |
| P2 | 浅色 `.pill` 对比度 | 约 3:1 | 已缓解：字号调至 12px |

## 建议

修复上述项后，本 Blueprint 已达到唯一 Current 标准；裁决第 13 章 Q-1～Q-4 后即可转 Frozen。
