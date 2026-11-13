# Curis Naming Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Parent: `docs/Engineering/Curis_Engineering_Convention.md`

---

## 1. General Rules

- 名称应表达对象和用途，不表达创建工具或 Agent。
- 同一对象跨文档、设计、图片、Prototype、Prompt 和 Review 复用同一个
  `object-id`。
- `object-id` 使用小写英文与连字符：`ceo-office-overview`。
- 文件扩展名使用小写。
- Current 官方文件使用稳定名称，不包含 Revision ID。
- 禁止 `new`、`new2`、`latest`、`最新版`、`final`、`final-final`、`v2`、
  `copy`、`副本`、`workbuddy-version`、`codex-version`、Agent 名称、模型名称
  或无意义时间戳。
- Codex、WorkBuddy、ChatGPT、Claude、Gemini 及其他 Agent 只是 Contributor，
  不能成为文件或目录命名依据。

## 2. Document Naming

Current 规范或入口文档使用稳定、可读的 Pascal Snake Case：

```text
<Domain>_<Subject>_<Document_Type>.md
```

示例：

```text
Curis_Engineering_Convention.md
Curis_System_Architecture.md
AI_Collaboration_Convention.md
```

Current 文件名不带日期或 Revision ID。状态、Revision ID、基线和更新时间写在
文档头或 Current 登记记录中。

需要独立保存的 Revision 历史、审查证据和 Milestone 使用：

```text
YYYY-MM-DD-NNN_<object-id>_<purpose>.md
```

示例：

```text
2026-07-31-001_ceo-office-overview_review.md
```

普通修改依赖 Git 历史，不要求创建上述快照。

## 3. Image Naming

Current 图片使用稳定语义名称：

```text
<object-id>_<view>_<state>_<viewport>.<ext>
```

需要保存的 Revision/Milestone 图片快照使用：

```text
YYYY-MM-DD-NNN_<object-id>_<view>_<state>_<viewport>.<ext>
```

字段规则：

- `view`：页面或组件视图，如 `overview`、`detail`、`dialog`
- `state`：`default`、`empty`、`loading`、`error`、`success`
- `viewport`：`desktop-1440`、`desktop-1024`、`mobile-390` 或实际尺寸
- `<ext>`：`png`、`jpg`、`svg`，按真实格式填写

示例：

```text
ceo-office-overview_overview_default_desktop-1440.png
2026-07-31-001_ceo-office-overview_overview_default_desktop-1440.png
```

同一次修改的不同尺寸必须保留相同 Revision ID 和 `object-id`，只改变 `viewport`。
禁止使用截图工具默认名称。

## 4. Prototype Naming

Prototype 目录使用：

```text
YYYY-MM-DD-NNN_<object-id>_prototype/
```

目录内入口固定为 `index.html`；相关样式、脚本和资源使用语义名称，不重复目录前缀。

示例：

```text
2026-07-31-001_project-detail_prototype/
├── index.html
├── styles.css
└── assets/
```

上式用于需要保存的 Revision/Milestone 快照。Current Prototype 使用稳定的对象目录
和 `prototype/` 路径，不带日期或 Revision ID。一个对象只能有一个 Current
Prototype，不在活动目录并列多个 `final` 版本。

## 5. Prompt Naming

Prompt 文件使用：

```text
YYYY-MM-DD-NNN_<object-id>_<purpose>_prompt.md
```

示例：

```text
2026-07-31-001_employee-profile_generation_prompt.md
```

Current Prompt 使用稳定语义名称；上式只用于获批的必要历史或 Milestone 快照。

Prompt 文档头必须记录：

- Purpose
- Input contract
- Output contract
- Model-independent constraints
- Revision ID
- Owner or Issue

文件名不得包含模型名，除非该 Prompt 的契约明确只适用于该模型。

## 6. Revision ID

- 唯一格式：`YYYY-MM-DD-NNN`。
- 日期使用 Asia/Shanghai 的自然日。
- `NNN` 从 `001` 开始，在仓库内按当天递增，日期变化后重新从 `001` 开始。
- 同一次修改涉及的文档、图片、Prototype、Prompt、说明和 Review 共用同一个
  Revision ID。
- Revision ID 表示变更集合；Git SHA 负责精确内容追溯。
- 普通小修改不创建历史副本，只保留 Git 记录。
- 禁止使用 `rNN`、`v2`、`final-final`、`workbuddy-version`、
  `codex-version` 等平行版本命名。

## 7. Branch, Commit And Identifier Naming

- 分支：`feat/<scope>`、`fix/<scope>`、`docs/<scope>`、
  `integration/<candidate>` 或工作区指定 Agent 前缀。
- Commit：`<type>: <imperative summary>`。
- `<scope>` 和标识符使用小写 kebab-case。
- 不把个人姓名、Agent 名称或模型名称作为所有权标识。
