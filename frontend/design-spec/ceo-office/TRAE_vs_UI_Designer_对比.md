# Trae 生成版 vs UI Designer 版 — CEO Office 前端对比

> 对比时间：2026-07-26
> 对比对象：
> - Trae：`/Users/yy/Library/Application Support/TRAE SOLO CN/.../curis-ceo-office`（23 个静态 HTML + SPEC.md + 校验报告）
> - UI Designer：`frontend/design-spec/ceo-office/`（44 空态页 + 13 示例页 + DESIGN.md + UI 规范，以及 `frontend/app/ceo-office` 的 Next.js 组件）

## 0. 最重要前提：设计语言是共享的

两个版本**用的是同一套 Terra 设计系统**。Trae 的 `colors_and_type.css` 里的 token 与我的 `DESIGN.md` 逐一对应：

| 维度 | Trae (`colors_and_type.css`) | UI Designer (`DESIGN.md`) |
|------|------------------------------|---------------------------|
| 主色 | `--curis-primary: #4a7c59` | `--color-primary-500: #4a7c59` |
| 暖琥珀 | `--curis-accent: #705c30` | `--color-accent: #705c30` |
| 奶油底 | `--curis-bg: #faf6f0` | `--color-cream: #faf6f0` |
| 标题字体 | Literata | Literata |
| 正文字体 | Nunito Sans | Nunito Sans |

甚至连 `--curis-background` / `--curis-card` 这类语义别名都一致。所以**"设计好不好看"不在这次的差异里——差异在实现方式、工具链、覆盖策略、QA 手段**。

---

## 1. 他（Trae）做的好在哪

1. **自动化设计校验（最大亮点）**
   自带 `solo-design` 技能 + `validation-report.json`：自动查「硬编码颜色」「单主色原则」「阴影透明度≤0.05」，产出 `passed` 结论 + 48 条 soft warning + 逐文件 repair plan。我同样要查这些，但靠人工截图 + 一致性规则，**没有机器闭环**。这是专业 Design Lint，值得直接搬。

2. **单文件自包含、可移植**
   每个 HTML 把整套 token + 组件样式内联进 `<style id="theme-vars">`，双击即开、不依赖构建，方便你直接预览/分享。

3. **页面内混带示例数据（预览更友好）**
   `ceo-office.html` 实测有 23 个卡片 + 14 处示例内容（非纯空态）。用户一眼能看出"装满长什么样"，比我"纯空态 + 另开 sample 页"在单次预览时更直观。

4. **设计工具集成度**
   有 `curis-ceo-office.design`（artboard 画板导出，含页面坐标）+ `runtime-orchestration-summary.json`，能对接设计工具做画板管理，工程化成熟。

5. **链接问题脚本化修复**
   `fix-cap-links.mjs` 说明它发现链接不一致后用脚本批量修，过程可复现、可重跑。

---

## 2. 我（UI Designer）做的好在哪

1. **覆盖全（广度碾压）**
   44 空态 + 13 示例 = **57 页**，9 一级 + 30 二级 + 10 三级，全导航树无 404；Trae 只有 **23 页**。

2. **正式 DESIGN.md（awesome-design-md 9 章标准）**
   这是给 AI 编程代理的机器可读桥接文档（视觉主题/调色板/排版 scale/组件 CSS/阴影层级/响应式/Agent 提示指南）。Trae 只有 `SPEC.md`（717 行、结构偏平，不如 9 章标准规范）。

3. **状态矩阵（空→单条→少量→满屏→溢出）**
   我在 UI 规范里显式定义了每个核心模块在各数据密度下的列数/密度/截断/分页规则。Trae 没有这份"装满后长什么样"的明确约定。

4. **走向真实生产代码**
   我把 shell/primitive/icon 落成 **Next.js/React 组件**（`TerraShell`/`TerraPrimitives`/`TerraIcons`），`npm run build` 通过、生产服务返回 200，并修了真实 bug（import 错处、fetch 失败回退空态）。Trae 停在静态 HTML。

5. **空态/填充态分离纪律**
   严格空态（不污染真实数据）+ 独立 sample 页（标注「示例·不进交付」），前端既知空也知满，且不会把假数据当真。

6. **贴合你需求的迭代闭环**
   按你多轮纠正迭代：Terra 锁定、能力中心改卡片网格、先出规范再出图、自己先截图检查。过程就是你的真实需求链。

---

## 3. 两者差异点（对照表）

| 维度 | Trae | UI Designer |
|------|------|-------------|
| 技术形态 | 静态 HTML（自包含） | 静态 HTML mockup + Next.js/React 生产组件 |
| 页面数 | 23 | 57（44 空态 + 13 示例） |
| 设计文档 | SPEC.md（717 行，偏平） | DESIGN.md（9 章标准）+ UI 规范（含状态矩阵） |
| QA 手段 | **自动 validator 闭环**（48 警告/0 阻断） | 人工截图自检 + 一致性规则 |
| 数据形态 | 页内混示例（预览直观） | 严格空态 + 独立 sample 页 |
| 交互 | 基本静态（`interactions:[]`） | 44 页静态 + 1 个 Next 页有真实 fetch/状态 |
| 能力子页 | agent/model/skill/tool/workflow 列表 + skill detail | 同结构 list + skill-detail（深度相当） |
| 设计工具对接 | 有 `.design` artboard 导出 | 无 |
| token 来源 | 直接借我的 Terra token | 我定义的权威 token |
| 链接一致性 | fix 脚本批量修 | 生成器统一产出，无散落 |

---

## 4. 能否结合 —— 能，而且应该结合

最佳组合是**两层流水线**：

1. **用 Trae 的 solo-design validator 做我的自动 QA 闸门**
   把那套规则（硬编码颜色、单主色、阴影透明度）套到我的 57 页，扫出我人工漏掉的漂移，补上机器闭环。这是它最该被吸收的能力。

2. **吸收 Trae「页内轻量示例」的预览优势**
   我的空态页可每个模块加一个折叠的「示例缩略」，减少前端理解成本，又保留"不污染真实数据"的纪律。

3. **分工：mockup 广覆盖用 Trae 式生成，生产实现用我的 React 组件层**
   - 广覆盖、快速出图、对接设计工具 → Trae 式静态生成 + validator 把关
   - 真实运行、对接后端、可维护组件 → 我的 Next.js 组件 + DESIGN.md

4. **统一 token 源**
   以我的 `DESIGN.md` 为唯一权威 token 源，Trae 的 `colors_and_type.css` 与之对齐（目前已一致，保持）。

5. **能力子页结构互认**
   两边能力域深度相当，直接共享同一套 agent/model/skill/tool/workflow 列表 + detail 结构，不重复造。

---

## 结论

- **Trae 强在**：快、广、有机器校验、可对接设计工具、预览直观。
- **我强在**：全、深（生产代码 + 状态矩阵 + 标准 DESIGN.md）、贴你的需求闭环。
- **建议**：静态 mockup 用 Trae 式生成 + validator 把关；生产实现用我的 React 组件层。两者 Terra token 已天然一致，合并零摩擦。
