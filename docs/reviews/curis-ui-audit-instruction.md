# Curis UI 原型审核指令

> 把这条指令完整复制给审核 agent。它包含全部上下文，接收方无需额外信息即可执行。

---

## 一、你是谁、要做什么

你是一名资深 UI 设计审核员。请对 Curis 产品的 HTML 高保真原型做一次完整的设计系统合规审核，输出一份分级问题清单（P0 阻断 / P1 应修 / P2 优化 / 通过项）。

Curis 是「一人公司自动任务与工作流系统」的桌面应用原型。原型位置：`curis-ui-prototype/`（约 19 个 HTML 页 + 一个 729KB 的 `curis-prototype.js` mock 层 + `_system/` 冻结设计系统）。原型已经过 P0（令牌转换）、P1（主按钮纪律 / 统一助理抽屉 / mock 标识 / 加载空错状态）、P2（字体 / 布局 / 调色板清理）三轮返工，现在需要独立审核确认是否达到 Frozen 可交付标准。

## 二、冻结设计系统基准（唯一真相源）

审核的唯一基准是以下文件，任何偏离都算问题：

| 文件 | 作用 |
|---|---|
| `curis-ui-prototype/_system/tokens.css` | 所有颜色 / 字体 / 圆角 / 阴影令牌，深色 `#1a1c1f`（非纯黑）/ 浅色画布 `#f5f5f7` + 白卡 `#ffffff` |
| `curis-ui-prototype/_system/shell.css` | 共享 Shell（220px sidebar / 52px topbar）、按钮（`btn-primary`/`btn-secondary`/`btn-ghost`）、卡片、状态、骨架屏 / 空状态 / 错误状态 / mock badge |
| `curis-ui-prototype/_system/theme.js` | 主题控制器：dark / light / system 三态，持久化到 localStorage |
| `curis-ui-prototype/_system/assistant-drawer.css` + `.js` | 统一 Global Assistant 抽屉（FAB + 右滑面板），由 `curis-prototype.js` 自动加载到每页 |

**冻结铁律（违反即 P0/P1）：**
1. 颜色只用 `--ui-*` 令牌，禁止硬编码 hex（`#0f1012`/`#2b6cff` 等旧调色板色值必须为 0）。
2. 每页最多 1 个 `btn-primary`（深色实心主按钮），其余用 `btn-secondary`/`btn-ghost`。
3. 助理 UI 统一为 Global Assistant 抽屉，不得有本地 `curis-companion`/`assistant-mini`/`assistant-trigger`/`#drawer`/`.ask-fab` 等遗留。
4. 每页 topbar 必须有「示例数据」mock badge（`.mock-badge[data-curis-auto]`）。
5. 术语：`Agent` 保留英文不翻；`ROI`/`KPI` 保留英文，仅每页首次出现处加中文备注（如 `ROI（投入产出）`），正文保持纯英文。禁止用户可见的 Blueprint / Outcome / Evidence / 回报 / 下注 等违禁词。
6. 导航方案 A：四分组（公司 / 工作空间 / 经营工具 / 公司资源），运行时页归入「工作空间」。
7. 主题三态必须全正确：dark 全暗、light 全亮、system 跟随 OS 不出现深浅混杂。

## 三、审核范围（17 个页面 + 共享层）

```
ceo-desk.html          operating.html         business.html
ai-organization.html   workspace-portal.html  workspace-studio.html
founding-flow.html     decision-room.html     meeting.html
finance.html           knowledge.html         calendar.html
assets.html
workspace-runtime-software.html
workspace-runtime-xhs.html
workspace-runtime-shortvideo.html
workspace-runtime-department.html
```
跳过：`index.html`（重定向落地页）、`ceo-day-demo.html`（开发者调试页，已清理调色板但非用户可见界面）。

## 四、审核检查清单（逐项过）

### A. 设计令牌合规
- [ ] 每页 `<head>` 是否链接 `_system/tokens.css` + `_system/shell.css` + `_system/theme.js`。
- [ ] grep 全站：硬编码色值（`#` 开头的 6 位 hex）是否为 0（CSS 注释和 `curis-prototype.js` 的 token 定义除外）。
- [ ] 是否存在第二套私有调色板（Palette-A 的 `--bg-base-default` / Palette-B 的 `--bg/--panel` 未被 frozen-patch 映射到 `--ui-*`）。
- [ ] 渐变（`linear-gradient`/`radial-gradient`）是否为 0（冻结禁止大面积渐变）。

### B. 组件一致性
- [ ] 每页 `btn-primary` 数量 ≤ 1（用 Puppeteer 渲染后 `document.querySelectorAll('.btn-primary').length` 检查，不只看静态 HTML——mock JS 会动态生成按钮）。
- [ ] `btn-secondary`/`btn-ghost` 是否在 `shell.css` 有定义且样式正确。
- [ ] 卡片（`.card`）是否统一用 `--ui-surface` 背景 + `--ui-line` 边框。
- [ ] 状态标签（`.status`）是否文字 + 颜色双重表达（不只靠颜色）。

### C. 主题正确性（重点，刚修过 bug）
- [ ] dark 模式：全页深色，无浅色元素泄漏。
- [ ] light 模式：全页浅色，无深色元素泄漏（尤其检查 topbar / page-header / app-shell 等容器）。
- [ ] system 模式 + OS 浅色：应等于 light。
- [ ] system 模式 + OS 深色：应等于 dark。
- [ ] 切换主题后无闪烁、无残留。
- 方法：Puppeteer `page.emulateMediaFeatures([{name:'prefers-color-scheme',value:'light|dark'}])` + `localStorage.setItem('curis-theme','system')` + reload，截图对比。

### D. 布局合规
- [ ] 每页 Shell 是否 sidebar(220) + main 正确并排（grid `220px 1fr`），main 不被推到视口下方或右侧空白。
- [ ] 是否有 HTML 结构 bug（多余 `</div>` 提前关闭容器、孤儿 div）——用 `document.querySelector('.app,.app-shell,.curis-shell').children.length` 验证子元素数量符合预期。
- [ ] Studio 页面列数 ≤ 3（palette + canvas + config），宽度不超标。
- [ ] 运行时页第三列宽度 ≤ 320px。
- [ ] 无固定 `width: 1440px` 的画板式容器（应 `width: 100%` / `100vw` 填充视口）。

### E. 术语本地化
- [ ] grep `AI员工` = 0（应为 `Agent`）。
- [ ] grep `Blueprint`/`Outcome`/`Evidence`/`回报`/`下注`/`赌注` 在用户可见文案中 = 0。
- [ ] `ROI（投入产出）` 每页最多 1 处（首次出现），其余纯 `ROI`。
- [ ] `KPI（工作指标）` 同理。
- [ ] 注意：JS mock 动态渲染的文本（如 `ai-organization.html` 的 ROI 在 JS 里）静态 grep 抓不到，需渲染后检查。

### F. 可访问性（WCAG AA）
- [ ] 文本对比度 ≥ 4.5:1（normal text）/ 3:1（large text）——深浅两态都查。
- [ ] 所有按钮 / 链接 / 输入框有可聚焦样式（`:focus-visible`）。
- [ ] 交互元素最小触达区 44×44px（或 32px+ 紧凑场景）。
- [ ] `role`/`aria-label`/`aria-modal` 等语义属性完整（尤其抽屉 / 模态 / 导航）。
- [ ] 键盘可达：Tab 顺序合理，ESC 关闭抽屉 / 模态。

### G. 交互一致性
- [ ] 每页右下角有统一 Global Assistant FAB（`#assistant-fab`），点击滑出抽屉。
- [ ] 旧助理 UI（`curis-companion`/`assistant-mini`/`assistant-trigger`/`#drawer`/`.ask-fab`）在渲染后 DOM 中 = 0。
- [ ] 导航分组四组正确，active 项高亮。
- [ ] mock badge 在每页 topbar 可见。

### H. 视觉层级
- [ ] 字体：Inter 已加载（`tokens.css` 顶部 `@import`），标题 24px、卡片标题 15px、正文 14px、辅助 11-12px。
- [ ] 间距：4 的倍数体系（4/8/12/16/24/32），无任意奇数间距。
- [ ] 阴影：仅 `--ui-shadow`，无多层重影。
- [ ] 圆角：`--ui-radius`(12px) / `--ui-radius-sm`(8px) 统一。

## 五、技术方法建议

1. **静态扫描**：用 grep/ripgrep 扫硬编码色值、违禁词、旧类名、固定宽度。
2. **Puppeteer 渲染验证**：对 17 页逐页深 / 浅色截图 + DOM 探针（primary 数 / FAB / mock badge / 布局 rect）。
   - Chrome 路径：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
   - puppeteer-core 在 `/Users/yy/.workbuddy/binaries/node/workspace/node_modules`
   - node 在 `/Users/yy/.workbuddy/binaries/node/versions/22.22.2/bin/node`
   - `file://` 协议必须 `--no-proxy-server`。
   - 大批量截图逐页跑（一次一页），避免 OOM。
3. **对比度**：用 Chrome DevTools 的 Accessibility 面板或 `getComputedStyle` 取前景 / 背景算比值。
4. **不要只看静态 HTML**：`curis-prototype.js` 会在运行时改 DOM（动态生成按钮、清空容器、注入 badge），必须渲染后检查。

## 六、已知已修复项（勿重复报告）

- Bug 1：`tokens.css` 已加 `html[data-theme="system"]` 到浅色 media query，system 模式不再深浅混杂。
- Bug 2：`business.html` 已删多余 `</div>` + 孤儿帮助 div，`.app-shell` 不再提前关闭。
- Bug 3：`workspace-portal.html` 已去 body flex 居中 + 删多余 `</div>`，`.app` 正确包含 sidebar + main。
- P1-1：9 个超标页主按钮已降到每页 1 个；`founding-flow` acceptField 不再动态提升 primary。
- P1-2：`renderCompanion()` 已从初始化器移除，旧 companion 不再注入。
- P1-3：mock badge / skeleton / empty-state / error-state 已加。
- P2：Inter 字体已 `@import`；8 页已补 shell.css；Studio/shortvideo 列宽已收窄；ceo-day-demo 调色板已清理。

## 七、交付物

输出一份 Markdown 报告 `docs/reviews/YYYY-MM-DD-curis-ui-audit-report.md`，结构：

```
# Curis UI 原型审核报告

## 审核结论
[一句话：是否达到 Frozen 可交付标准 / 阻断项数量]

## 问题清单

### P0 阻断（必须修才能交付）
| # | 页面 | 问题 | 根因 | 建议 |
|---|---|---|---|---|

### P1 应修（交付前应修）
...

### P2 优化（后续迭代）
...

### 通过项
[列出确认合规的维度，如：令牌引用、主按钮纪律、助理抽屉统一、术语本地化 等]

## 截图证据
[关键问题的截图路径]
```

每个问题必须包含：页面文件名、具体行号或 DOM 位置、根因分析、修复建议。不要泛泛而谈「布局不好」，要精确到「workspace-portal.html L288 多余 </div> 导致 .app 提前关闭」这种程度。

## 八、开始

先读 `curis-ui-prototype/_system/tokens.css` 和 `shell.css` 建立基准，再逐页审核。遇到不确定是否违规的，按「是否偏离冻结令牌 / 是否破坏单页一主按钮 / 是否主题错乱」三条硬线判断。
