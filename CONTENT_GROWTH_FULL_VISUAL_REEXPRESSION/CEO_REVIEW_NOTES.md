# CEO Review Notes — Content Growth Full Visual Re-expression

Authority Class: VISUAL EXPLORATION PROTOTYPE  
Status: Ready for CEO Review  
Scope: 七区 Overview + 关键 Detail / Work / Conversation / Artifact 视图

---

## 关键截图清单

| 文件 | 内容 |
|---|---|
| `screenshots/ceo-review-operate.png` | 经营：账号 Portfolio + 风险判断 |
| `screenshots/ceo-review-research.png` | 研究与选题：来源 / 提炼 / 输出 三栏证据链 |
| `screenshots/ceo-review-production.png` | 内容制作：Method Section + Dense Work Rows |
| `screenshots/ceo-review-publish.png` | 发布：时间线 + 状态分组队列 |
| `screenshots/ceo-review-accounts.png` | 账号：账号档案卡 |
| `screenshots/ceo-review-analytics.png` | 复盘：判断墙 + 实验 / 学习 / 数据缺口 |
| `screenshots/ceo-review-assets.png` | 素材：素材表 + 数字人卡 + 素材请求 |
| `screenshots/ceo-review-work-W-202.png` | Production Work 详情（Brief / Script / Version / Review / Timeline / Conversation 入口） |
| `screenshots/ceo-review-reference-REF-1.png` | Reference 详情（来源 / 结构拆解 / Evidence / Applicability） |
| `screenshots/ceo-review-account-xhs-brand.png` | Account 详情（Profile / 实验结果 / 绑定 / 历史） |
| `screenshots/ceo-review-conversation-e-zhou.png` | Employee Conversation（结果卡片 + 快捷动作） |

入口：`pages/index.html`，hash 路由。

---

## 各区为什么这样表达

### 1. 经营
- **工作任务**：从 Portfolio 高度判断账号健康、库存风险、下一决策。
- **选择**：平台带状账号卡 + CEO-level summary strip + 待决策 / 动态 side stack。
- **相比旧 HTML**：不再把经营做成 Dashboard 指标卡墙；账号按平台分组，库存天数和趋势直接显示在卡上，判断所需信息一眼可见。

### 2. 研究与选题
- **工作任务**：追踪 Reference → 灵感 → 知识 → Proposal 的转化链。
- **选择**：三栏证据墙（来源 / 提炼 / 输出），每栏内部用 evidence card。
- **相比旧 HTML**：不再把参考和提案混在表格里；来源、知识状态、提案目标账号形成横向阅读流。

### 3. 内容制作
- **工作任务**：按 Production Method 管理工作队列，快速定位阻塞和下一步。
- **选择**：Method Section + Dense Work Rows（已接受方向）。每行保留 Work、账号、方法、阶段、状态、Owner、进度、Artifact、Next step。
- **相比旧 HTML**：去掉旧 Workbench 的复杂步骤展开；Overview 只保留队列判断所需字段，点击进入 Work Detail 才看脚本、版本、Review checklist、Timeline。

### 4. 发布
- **工作任务**：排期、回执核验、人工接续。
- **选择**：顶部时间线 + 按状态分组的发布队列 + 发布准备度 side card。
- **相比旧 HTML**：从表格改为“时间+状态”双维度；超时未回执、需人工发布的项在 Next decision 条中突出。

### 5. 账号
- **工作任务**：管理账号定位、绑定、内容历史与实验结论。
- **选择**：账号档案卡（定位、受众、目标、策略、实验、结果、趋势、下一步、绑定状态）。
- **相比旧 HTML**：从列表改为可读性更强的档案卡；账号本身作为长期资产，需要完整上下文而不是只显示当前指标。

### 6. 复盘
- **工作任务**：形成判断、运行实验、沉淀学习、识别数据缺口。
- **选择**：判断墙 + 实验表格 + 学习卡 + 数据缺口卡。
- **相比旧 HTML**：不再只是数据图表；把“判断—反例—限制—下一步”作为核心阅读单元，突出不确定性而非仅展示数字。

### 7. 素材
- **工作任务**：素材可用性、授权、版本、数字人状态。
- **选择**：素材表 + 数字人卡 + 素材请求列表。
- **相比旧 HTML**：数字人作为独立生产资产独立展示；素材阻塞对 Work 的影响直接在 Account / Work 中引用。

---

## 关键 Detail / Work / Conversation / Artifact 表达

### Work Detail（#work/W-202）
- 顶部返回 Production。
- 顺序：Brief → Script → Version → Review Checklist → Assets → Timeline → Conversation 入口。
- Artifact（脚本）得到足够阅读空间，而不是被压缩成一行。

### Reference Detail（#reference/REF-1）
- 来源元数据 + 结构拆解（Theme / Hook / Opening / Structure / Rhythm / Visual / CTA / Why it works）+ Evidence + Applicability 表。
- 强调“参考如何被转化为本账号可用的知识”。

### Account Detail（#account/xhs-brand）
- Profile / 实验与结果 / 绑定状态 / 内容历史 / 发布历史。
- 账号定位与实验结论并重，避免只显示历史发布列表。

### Conversation（#conversation/e-zhou）
- 模拟与 Employee 的持续工作对话：工作状态 → 结果卡片 → 快捷动作。
- 不是通用 Chatbot；动作可直接跳到对应 Detail 或 Area。

---

## 相比旧完整 HTML 最重要的变化

1. **统一 SPA**：七区 + Detail 全部在 `index.html` 内通过 hash 路由完成，不再是一个区一个 HTML。
2. **Overview 与 Detail 分离**：Overview 只保留判断和队列所需信息，执行细节进入 Detail。
3. **Production 队列**：用 Method Section + Dense Work Rows 替代旧 Workbench。
4. **Employee 存在感**：通过 Owner Pill、Conversation 入口、Activity 体现，没有恢复 Employee Card Wall。
5. **Artifact 空间**：Script、Reference 拆解、版本、Review 都有独立卡片，不再只显示字段名和链接。
6. **Account Scope 贯穿**：账号 pill 出现在经营、研究、制作、发布、复盘各区，强调同一账号在不同阶段的状态。
7. **判断优先**：经营、研究、发布、复盘顶部都有 judgment strip，把“下一步需要 CEO 判断什么”放在最前面。

---

## 仍是 Mock / 未真实实现

- 所有数据来自 `assets/data.js`，无后端、无真实平台 API。
- Conversation 使用固定脚本，未按 Employee 或上下文动态生成。
- 发布回执、数据授权、数字人合成等状态为模拟值。
- 主题/颜色 token（`--cg-*`）仍是本轮视觉候选，不是 Frozen UI Token。
- 没有真实视频/图片预览，Artifact 以文本和占位结构表达。

---

## 发现的产品 / 交互问题

1. **Conversation 返回路径单一**：当前所有 Conversation 统一返回“经营”，但实际应从触发点返回（如 Work Detail 触发应返回 Work Detail）。
2. **Publish 状态映射存在缺口**：原数据中有 `human`、`unknown` 等状态，与 Production 的 `ready/review/blocked` 不完全对齐，需统一状态语义。
3. **Overview 中部分字段硬编码**：如 Production 的 artifactMap、方法判断函数基于标题关键词，产品层面应来自 Production Method 配置。
4. **Research → Proposal → Work 的立项链路已打通**，但 Proposal Detail 缺少 CEO Review 动作入口（目前只读）。
5. **数字人授权到期等素材风险**目前在素材区提示，但是否需要在经营/制作的 Next decision 中同步出现，可进一步讨论。
6. **1280×800 适配**：当前优先保证 1440×900 完整可读；1280×800 下部分 Dense Work Rows 表头可能需横向滚动或列隐藏策略。

---

## 下一步

等待 CEO Review 视觉方向与各区表达优先级。本轮目标：确认“七区是否都找到了合适自己的表达”，而非统一组件。
