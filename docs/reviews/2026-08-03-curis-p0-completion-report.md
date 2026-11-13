# Curis UI 原型 P0 返工完成报告

**日期**：2026-08-03  
**范围**：`curis-ui-prototype/` 全部 17 个可交付页面  
**基线备份**：`curis-ui-prototype.bak/`

---

## 1. P0 目标

- 接入冻结设计系统共享基座（`_system/tokens.css` + `shell.css` + `theme.js`）。
- 统一使用 `--ui-*` 注册令牌，替换页面私有调色板。
- 移除 `#387bff` 第二 accent、移除渐变背景。
- 中文术语本地化（ROI→投入产出、Agent→AI员工、KPI→工作指标 等）。
- 统一侧栏为方案A导航：运行时页归入「工作空间」分组。
- 修复浅色主题下内容框与背景对比度不足的问题。

## 2. 完成内容

| 检查项 | 结果 | 说明 |
|---|---|---|
| `_system/` 基座接入 | 17/17 页 | 所有可交付页面均链接共享令牌与外壳样式。 |
| `#387bff` 第二 accent | 基本清零 | 全站静态检查为 0；仅 `ceo-desk.html` 的 patch 注释中残留 2 处，不影响渲染。 |
| `radial-gradient` 渐变 | 0 处 | 已剥离所有页面级装饰渐变。 |
| 用户可见英文违禁词 | 0 处 | ROI/Blueprint/Agent/KPI/Outcome/Evidence/下注/赌注 等已本地化。 |
| 导航分组 | 统一 | 全部页面侧栏采用「公司 / 工作空间 / 经营工具 / 公司资源」四组，运行时页进入「工作空间」。 |
| 浅色对比度 | 已修复 | 画布 `#f5f5f7`、卡片 `#ffffff`、次级表面 `#f7f8fa`。 |

## 3. 根因与修复

浅色对比度不足的根因是 `curis-prototype.js` 在运行时通过 `injectGlobalStyles` 把浅色画布硬编码为 `#f7f7f8`，覆盖了 `_system/tokens.css` 的 `--ui-bg`。

修复动作：
- `curis-prototype.js` 浅色令牌对齐冻结规范：
  - `--background` / `--bg-base-default`：`#f7f7f8` → `#f5f5f7`
  - `--bg-base-tertiary`：`#f0f1f3` → `#f7f8fa`
- `body[data-curis-neutral]` 运行时页的浅色 `--bg` / `--panel2` 同步对齐。

## 4. 验证

### 4.1 抽样截图

使用 puppeteer-core + Google Chrome 对三个代表页截深/浅色全页图，共 6 张：

- `business.html`（Palette-A / Tailwind v4）
- `meeting.html`（Palette-B / 自包含）
- `assets.html`（轻量页）

关键实测值（浅色）：
- body 背景：`rgb(245, 245, 247)` → `#f5f5f7`
- 卡片/侧栏：`#ffffff` / `#f7f8fa`
- 导航分组：符合方案A

### 4.2 静态合规检查

- `SYS`（_system 引用数）：3~4
- `GRAD`（渐变）：0
- `TERM`（违禁词）：0（`business.html` 出现 4 处 `Evidence` 均为代码标识符/类名/ID，非用户可见文案）

## 5. 仍存小问题

- 页脚文案 minor 不一致：`business.html` 显示「帮助」，`meeting.html` / `assets.html` 显示「帮助与反馈」。不影响功能，可在 P1 顺手统一。
- `ceo-day-demo.html` 使用第三套独立调色板，P0 阶段明确跳过，归入 P2 处理。
- 部分页面仍依赖 `curis-prototype.js` 的动态主题注入，虽已对齐，但长期应逐步解耦到 `_system/` 基座。

## 6. 下一步：P1 阶段

1. **主按钮纪律**：每页仅保留一个主按钮（深色实心），其余降级为次级/文字按钮。
2. **统一 Global Assistant 抽屉**：用共享的 CEO 助理抽屉替代各页静态 rail/悬浮卡片，减少重复实现。
3. **真实状态 + mock 标识**：为加载、空状态、错误状态提供统一组件，并在 mock 数据处加「示例数据」标识。
4. 继续抽检剩余页面，确保主题切换、导航、术语无回退。

## 7. 术语本地化策略修正（2026-08-03 补充）

### 7.1 第一轮：保留专有名词 + 加中文备注
用户反馈：此前强制把 `Agent` 翻成「AI员工」不合理——Agent 在 Curis 产品里有专属定义，不等于 AI员工；`ROI`、`KPI` 属行业专有名词，应保留英文并加中文备注。

修正（脚本 `fix_terms.py`，全站 17 页 + 转换脚本 `convert_p0.py` 术语表同步）：

| 术语 | 旧处理 | 新处理 |
|---|---|---|
| `Agent` | 翻成「AI员工」 | 保留 `Agent`，不加备注 |
| `ROI` | 翻成「投入产出」 | `ROI（投入产出）` |
| `KPI` | 翻成「工作指标」 | `KPI（工作指标）` |

其余已本地化术语（搭建方案 / 目标结果 / 依据 / 业务版图 / 反馈 / 业务方向 / 经营选择）用户未要求回退，保持不变。

### 7.2 第二轮：仅首次出现处加备注
用户确认：备注不要每处都加（太啰嗦），应「在首次出现处加备注，正文保持纯 `ROI` / `KPI`」。

修正（脚本 `fix_terms_v2.py`）：先还原全量备注为纯 `ROI` / `KPI`，再排除 `<head>` / `<script>` / HTML 注释后，对**每页首个可见 `ROI` / `KPI`** 加中文备注。

全站验证结果：
- `AI员工` = 0（全部回退为 `Agent`）
- `ROI（投入产出）` = 7 处（business / ceo-desk / decision-room / finance / operating / shortvideo / xhs 各 1 处，均为可见文案首现位置）
- `KPI（工作指标）` = 1 处（finance）
- 其余 `ROI` / `KPI` 在正文保持纯英文
- 其余术语计数未变，无误改

局限：`ai-organization.html` 的 3 个 `ROI` 位于 JS mock 数据、由前端动态渲染，不在静态 HTML 文本节点内，脚本未能自动加备注（备注=0）。如需一致，可单独在该页渲染逻辑处处理。

说明：本轮术语策略已稳定——专有名词保留英文，仅每页首现处附中文备注辅助理解。
