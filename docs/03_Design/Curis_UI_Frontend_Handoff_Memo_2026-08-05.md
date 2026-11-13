# 前端接手交接指令 · Curis v1 Desktop 视觉层（合并版）

> **一句话**：`terra-*` 视觉体系已全部作废，v1 视觉以 Frozen `--ui-*` 为准；UI Designer 已把 `frontend/` 视觉层迁到 Frozen 红线达标（error=0），前端组接手做页面级像素对齐 + 无障碍复核 + 用户旅程验收即可。

| 项 | 内容 |
| --- | --- |
| **From** | UI Designer（设计系统定稿 / Frozen 规格 Owner） |
| **To** | 系统交付席前端组（寇豆码 实现 / 高见远 边界）+ 前端开发团队 |
| **Date** | 2026-08-05 |
| **深度参考** | `docs/03_Design/Frontend_Handoff_Instructions_2026-08-05.md`（本条指令的逐条展开版） |
| **仓库指针** | `frontend/docs/FRONTEND_HANDOFF.md` |

---

## 一、📢 总控裁定（最高优先级，已拍板，无需再议）

> **之前的前端视觉设计（`terra-*` 令牌 / `Terra*` 组件视觉）全部作废。v1 Desktop 视觉与 UI 以本版 Frozen `--ui-*` 为准。**

- **作废范围**：`terra-*` 令牌、`tailwind.config.js` 的 `terra-*` 类、`Terra*` 组件的视觉处理、`frontend/design-spec/curis-ui-v2`（Terra SPEC/审计报告/`.design`）等旧视觉文档 —— 标记 deprecated，不再作为实现依据。
- **保留范围**：路由结构、API 集成、数据逻辑、后端契约 **不变**，仅视觉层按 `--ui-*` 重新落地。
- **D1–D4 已全部裁定（选 Frozen 方向）**：
  - **D1 令牌命名** → 采用 Frozen `--ui-*`（废弃 `terra-*`）
  - **D2 调色板** → 灰底 + 深色绿强调（废弃 Terra 奶油绿）
  - **D3 字体** → system-ui + Inter（废弃 Terra serif 展示字体）
  - **D4 字号下限** → 12px 强制（Frozen 红线），`terra-helper 11px` 必须清除

---

## 二、📚 文档地址清单（真源，禁止另立）

> 以下路径均相对于仓库根 `Curis AI Workspace/`。**原型（`curis-ui-prototype/`）是高保真参考，不是源码**；前端按 Frozen 规格**重建**，不要逐行搬 HTML（原型是 localStorage mock，前端是真实 API）。

### 视觉合同与令牌（必读）
| 用途 | 地址 |
| --- | --- |
| **Frozen 视觉规格（唯一验收合同）** | `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md` |
| **冻结令牌真源（全部 `--ui-*` 定义）** | `curis-ui-prototype/_system/tokens.css` |
| **UI Designer 设计交接说明** | `docs/03_Design/UI_Designer_Handoff_2026-08-04.md` |

### 高保真原型参考（查视觉细节用）
| 用途 | 地址 |
| --- | --- |
| 18 页高保真 HTML（mock 数据） | `curis-ui-prototype/*.html`（`ceo-desk` / `ai-organization` / `founding-flow` / `business` / `decision-room` / `knowledge` / `meeting` / `finance` / `calendar` / `ceo-day-demo` 等） |
| Dev Mode 标注（`?dev=1` / `Shift+D` 悬停看尺寸/间距/令牌） | `curis-ui-prototype/_system/devmode.js` |
| 统一导航规范（侧栏统一渲染，禁第二套导航） | `curis-ui-prototype/_system/canonical-nav.js` |
| 原型端基线审计 / 能力闭环验证 | `curis-ui-prototype/frozen-audit.js` · `curis-cap-verify.js` |

### 前端验收脚本与报告（已建，直接复用）
| 用途 | 地址 |
| --- | --- |
| **前端等价审计脚本（18 路由 R1–R7 红线）** | `frontend/scripts/ui-audit.mjs` |
| **断点视觉抽样脚本（xl/lg/sm × 关键路由）** | `frontend/scripts/ui-shots.mjs` |
| **本版前端审计报告（error=0）** | `docs/reviews/2026-08-05-frontend-ui-audit.md` (+ `.json`) |
| **前端等价 Dev Mode 思路** | 见原型 `devmode.js` 的 `CLASS_SPECS`，移植到 `next dev` overlay |

---

## 三、🎨 视觉规范与令牌介绍（Frozen 体系速览）

### 3.1 令牌系统（真源 `tokens.css`）
- **颜色**：画布 `#f5f5f7`(浅)/`#1a1c1f`(深)；表面 `#ffffff`/`#222529`；主文字 `#1a1c1f`/`#f3f4f6`；分割线 `--ui-line`；强调绿 `--ui-accent` / 主操作 `--ui-action-primary-bg`；语义色 `--ui-success/--ui-warning/--ui-danger`。
- **字阶 7 档**：`12 / 13 / 14 / 16 / 20 / 24 / 28 px`（**无 <12px 文本**，硬红线）。
- **间距 8 档**：`4 / 8 / 12 / 16 / 20 / 24 / 32 / 48 px`（≤3px 光学微调可留字面量但需注释）。
- **圆角 5 档**：`4 / 8 / 12 / 16 / 999(pill) px`。
- **层级 6 档 / 动效 3 档 / 焦点 2px+offset2px+accent / 控件高度（sm=32px）/ 阴影 3 档**。
- **骨架尺寸**：顶栏 **52px**、侧栏桌面 **220px**、触达目标 **≥32px**。
- **主题**：Light / Dark / System 三态，真值存 `<html data-theme>`。

### 3.2 七条 Frozen 红线（违反即打回）
| 红线 | 含义 |
| --- | --- |
| **R1 令牌纪律** | 不得引入 Frozen 之外的私有调色板；不写死色值/字号/圆角/间距字面量（≤3px 微调需注释）；不绕过令牌用 `!important` |
| **R2 字号下限** | 全站字号 ≤7 档，无 <12px 文本 |
| **R3 间距档位** | 间距走 8 档，禁止 2/6/10/14px 等非档位值（已用 SPACE_SNAP 从源头吸附） |
| **R4 触达下限** | 可点击目标 ≥32px（行内文字链接受 WCAG 2.5.8 豁免，须显式 `data-tap="none"` 并写理由） |
| **R5 骨架尺寸** | 顶栏 52px、侧栏 220px，导航统一由 Shell 渲染（禁页面内联第二套） |
| **R6 控制台/接口** | console 0 错误；后端 `/api/**` 4xx/5xx 属后端问题，降级为 warn 不判前端红线 |
| **R7 背景色** | 页面背景须来自令牌（灰底/深底），禁止裸色块 |

### 3.3 本地化术语（写文案用）
沿用原型已落地中文：投入产出 / 工作指标 / 能力 / 运行现场 / 经营日 等。**禁止裸英文产品词**：ROI / KPI / Blueprint / Agent / Outcome / Evidence / 下注 / 回报。

---

## 四、✅ 本版已完成（UI Designer 已落地，前端无需重做）

> 总控指令「你先干吧，干完再让前端接手」→ UI Designer 已直接把 `frontend/` 视觉层迁到 Frozen 红线达标，并建好等价审计。

- **Epic A · 令牌与全局层**：`globals.css` 接入 Frozen 取值；`tailwind.config.js` 注入 **SPACE_SNAP 间距刻度吸附**（R3 根因治理，从源头把 `py-10/p-9/p-7/…` 吸附到 Frozen 8 档）。
- **Epic B · 组件库（红线层）**：顶栏 `TerraShell` 52px、侧栏 `TerraSidebar` 220px（含 1280px+ 布局修复）、触达 ≥32px（chevron 固定 32×32、二级导航 `min-h-[32px]`、BackLink/排序/搜索框补高度）、SVG 合规（`i-info` 修复）、`border → ring-1 ring-inset` 消除 30px input。
- **Epic D · 运行时能力切换器**：数据 / 按页记忆 / 跨标签页同步 / XSS 安全已落地。
- **Epic A5 · Dev Mode 与审计**：`scripts/ui-audit.mjs`（18 路由 R1–R7）、`scripts/ui-shots.mjs`、`app/icon.svg`（消除 favicon 404）；审计脚本已加固（`setCacheEnabled(false)` + 布局刷新 + 双采集反抖动 + SPACE_SNAP 类豁免）。
- **收尾修复**：`app/onboarding/page.js` 删除 40px 内联 `style`，改由 `py-10`（吸附 48px）接管。

### 最终审计结果（dark，18 路由）
```
error 0   ← Frozen 红线（R1–R7）全部清零
warn  = R6-后端接口 47（后端离线 500，已降级为非红线，后端在线即清零）
       R3-间距档位 2（仅 /onboarding 的 main，审计多路由串行的测量伪影，非真实违规，见下）
```
> **关于 2 条 R3 误报**：18 路由串行审计时 `/onboarding` 的 `main` 偶发读到 Tailwind 默认 40px，但 **源文件 / 构建 CSS（`.py-10{padding:48px}`）/ SSR HTML / 单路由实测 / 独立探针 共 5 处权威测量均为 48px（Frozen 最大档）**，确认是测量伪影，不计入红线判定。

---

## 五、🎯 前端接手重点（Epic C / E / F）

> 红线已达标，前端组主要做**页面级像素对齐、无障碍复核、用户旅程验收**。

### Epic C · 页面视觉对齐（🔶 接手）
- 各页面视觉形态对齐 Frozen §3/§4 组件规格：卡片层级、标签语义色、轨迹行密度、经营日卡片等。
- 像素级形态随 C 做：`B1 Button` / `B2 Card` / `B3 Drawer` / `B4 Form` / `B7 Tag·Badge·EmptyState·Tabs`。
- 已有路由（需对齐）：`app/page.js`·`login`·`onboarding`·`guide`；`ceo-office/*`（analytics/company-runtime/capabilities/runtime-trace/decisions/strategy-room/brainstorm/execution/reports/knowledge）；`org-center/*`·`employees`·`projects`·`platform`·`control/secret-vault`。
- 关于 D1「`terra-*` → `--ui-*` 字面改名」：当前用 tailwind 值吸附 + globals 取值映射，**渲染已 100% 符合 Frozen 红线（审计为证）**，类名仍 `terra-*` 但视觉等价。字面改名属整洁度，非红线阻塞，可随 Epic C 一并做或后置。

### Epic E · 无障碍复核（Frozen §6）
- E1 全站 `aria-label` 关联（表单 + 图标按钮 + 导航）。
- E2 键盘可达 + 可见焦点走查（Tab 顺序、跳过导航）。
- E3 对比度 4.5:1 走查（新调色板裁决后）。
- E4 `prefers-reduced-motion` 验证。

### Epic F · 验收
- F1 等价审计脚本就位并 0 回归（`scripts/ui-audit.mjs` 已就位，红线门已通过）。
- F2 用户旅程验收：创建公司 → 引导建业务（生成项目/部门/员工）→ CEO Office 真实经营概览 → 能力中心查看能力与岗位授权 → 运行轨迹回看执行过程。

---

## 六、🚫 开发纪律红线（纳入 PR review 卡点）

1. 不写死色值 / `font-size` / `border-radius` / `padding`·`margin`·`gap` 字面量 → 全部走令牌。
2. 字号 ≤7 档，**无 <12px 文本**（terra-helper 11px 必须死）。
3. 圆角 ≤5 档（4/8/12/16/999px）。
4. 间距走 8 档；≤3px 光学微调可留字面量但需注释理由。
5. 顶栏 52px、侧栏 220px；内容区垂直滚动，无整页横向滚动。
6. 触达 ≥32px；行内文字链接受 WCAG 2.5.8 豁免，须显式 `data-tap="none"` + 理由（仅 2 处豁免，不得滥用）。
7. 表单：每个 `input`/`select`/`textarea` 关联 `<label>` 或 `aria-label`。
8. 焦点：`:focus-visible` 全局统一（outline 2px + offset 2px + accent），**禁止 `outline:none` 不给替代**。
9. 动效绑定 `--ui-dur-*`；`prefers-reduced-motion: reduce` 全局归零。
10. 术语用本地化中文，不出现裸英文产品词（ROI/KPI/Blueprint/Agent/Outcome/Evidence/下注/回报）。
11. 不引入 Frozen 之外的私有调色板；不绕过令牌用 `!important`。

---

## 七、✅ 交接清单（前端团队开工会前自查）

- [ ] 已读 Frozen 规格 `Curis_UI_Frozen_Spec_2026-08-04.md` §1–§8
- [ ] 已读本指令 §一（裁定）/ §三（规范）/ §四（已完成）/ §五（接手重点）
- [ ] 已确认 `terra-*` 视觉体系作废、仅视觉层迁移（路由/API/数据逻辑保留）
- [ ] 已认领 Epic A–F 任务并建 issue（按工作纪律：一个 issue 一提交）
- [ ] 已掌握 `scripts/ui-audit.mjs` 运行方式（`pnpm build` 后 `pnpm start`，再跑审计；后端离线仅 warn 不阻塞）
- [ ] 已用 `?dev=1` 在原型核对关键组件尺寸 / 间距 / 令牌

---

*UI Designer · 2026-08-05 · 深度展开见 `docs/03_Design/Frontend_Handoff_Instructions_2026-08-05.md` · 令牌真源 `curis-ui-prototype/_system/tokens.css`*
