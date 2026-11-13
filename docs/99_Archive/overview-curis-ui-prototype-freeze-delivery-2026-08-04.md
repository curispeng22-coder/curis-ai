# Curis UI 原型冻结整改 · 交付概览（2026-08-04~05 · AB 闭环完成）

## 本次完成：A 类一致性快赢 + B 类能力闭环

### A 类（一致性快赢）
| 项 | 修复 | 验证 |
|---|---|---|
| A1 去除 workspace-studio 画布渐变网格 | 删除 `linear-gradient(...)` 背景，改为纯色 | 全站 `linear-gradient` 仅保留已冻结的合规用法 |
| A2 本地化用户可见英文术语 | `Outcome（VERIFIED）`→`成果（VERIFIED）`、`KPI（工作指标）`→`关键指标（工作指标）` | 已扫描并修正 |
| A3 顶栏高度统一 | 多页残留 `var(--topbar-height)` / `62px` 全部改为 `var(--ui-topbar-h: 52px)` | 真实 Chrome：17 页顶栏 52px |

### B 类（能力添加闭环）
| 项 | 修复 | 验证 |
|---|---|---|
| B1 AI Team 页能力资产库 + 添加 | `ai-organization.html` 新增「能力资产库」区块与添加抽屉 | 真实 Chrome：可添加模型/Agent/Skill/Tool/MCP |
| B2 能力绑定到员工 | 资产库内 select 绑定员工；员工抽屉显示静态能力 + 已绑定动态能力 | 真实 Chrome：绑定写入 localStorage，抽屉正确显示 |
| B3 runtime 顶栏能力切换器 | 5 个运行现场 / Shell 参考页顶部新增「当前能力」下拉；空态提供「＋ 配置能力」直达链接 | 真实 Chrome：24 项断言全绿 |

## 关键设计纪律
- 单一真源：能力切换逻辑统一在 `_system/runtime-capability.js`，5 页仅引用一行脚本。
- 数据契约：`localStorage['curis-capabilities']` / `curis-capability-binds` / `curis-runtime-cap:<page>` 三 key 支撑完整闭环。
- 安全性：AI 团队页资产库渲染全部用 `capEsc()` 转义，防御 XSS；runtime 下拉用 `document.createElement` + `textContent`，杜绝标签解析。
- 无障碍：select 原生键盘操作，变化通过 `aria-live` 播报，空态不断头。
- 本地化：能力类型存储英文标识，用户界面统一显示「模型 / AI 员工 / 技能 / 工具 / 连接器」。

## 新增 / 修改文件
- `curis-ui-prototype/_system/runtime-capability.js`（新增）
- `curis-ui-prototype/ai-organization.html`：能力资产库 + 添加抽屉 + 员工抽屉绑定能力
- `curis-ui-prototype/workspace-runtime-{department,shortvideo,software,xhs}.html`：注入能力切换器
- `curis-ui-prototype/workspace-shell-reference.html`：注入能力切换器
- `workspace-studio.html`、`ceo-day-demo.html`、`finance.html` 等 A 类修复页

## 验证结果（真实 Chrome 回归）
**通过 24/24，Console 错误 0 条**：
- 空态：下拉隐藏 + 出现「＋ 配置能力」直达链接 ✓
- AI 团队页：添加 2 个能力后资产库渲染 2 条 ✓
- AI 团队页 XSS：能力名中的标签未被解析为元素 ✓
- AI 团队页：能力可绑定到员工并写入存储 ✓
- AI 团队页：员工抽屉显示已绑定能力 ✓
- 5 个运行现场页：能力下拉读到资产库、分组正确、顶栏 52px、无注入元素 ✓
- 运行现场：切换后写入本页记忆、刷新保持、按页独立不串味 ✓
- 全站 12 个主要页顶栏统一 52px ✓

## 备注
- 验证脚本：`/Users/yy/.workbuddy/binaries/node/workspace/curis-cap-verify.js`
- 关键截图：`/Users/yy/Documents/Curis AI Workspace/.cache/shots/01-cap-library-dark.png`、`03-employee-bound.png`、`05-runtime-topbar.png`
