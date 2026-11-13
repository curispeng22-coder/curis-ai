# Curis Folder Convention

Status: Frozen

Convention Version: 1.0

Revision ID: `2026-07-31-001`

Baseline: `main @ 135cab894eb2dddf518dd848ab4463d83cedc7b1`

Updated: 2026-07-31

Parent: `docs/Engineering/Curis_Engineering_Convention.md`

---

## 1. Principles

- 目录按职责和生命周期组织，不按 Agent、模型或个人组织。
- 新目录必须解决现有目录无法表达的当前需求。
- 先复用现有目录；禁止创建同义目录，如 `doc`/`docs`、`image`/`images`、
  `archive`/`old`。
- Current 与 History 不在同一活动目录并列竞争。
- 不为单个文件创建无必要的多层目录。
- 不按 Codex、WorkBuddy、ChatGPT、Claude、Gemini 或其他 Agent 建立资产目录。
- 同一业务对象的设计规范、效果图、Prototype 和说明按 `object-id` 聚合，不按
  PNG、HTML、Prompt 或生成工具任意分散。

## 2. Current Engineering Documents

工程规范固定在：

```text
docs/Engineering/
```

`Curis_Engineering_Convention.md` 是唯一入口，其余六个文件是专项章节。
禁止创建 `docs/Engineering-v2/`、`docs/conventions/` 或工具专属规范目录。

## 3. Lifecycle Placement

### Current

Current 保持在所属领域既有权威目录，并由 Frozen 入口或上级规范直接引用。
不得为了表示 Current 再复制到 `current/`、`latest/` 或根目录。

同一业务对象的非文档 Current 资产包采用稳定路径：

```text
<owner-directory>/assets/<object-id>/
├── design-spec.md
├── prototype/
├── <semantic-effect-image>.png
└── README.md
```

`README.md` 只在需要说明资产关系时存在。不要求现有资产为了匹配示例而迁移；
已有经治理确认的 Current 路径继续有效。

### Draft And Review

- 已存在 Current：在任务分支或 worktree 的同一稳定路径上修改，Git diff 即候选，
  不复制完整资产包。
- 尚无 Current：在预定的官方稳定路径创建一个 `Status: Draft` 或
  `Status: Review` 候选。
- 二进制候选确需与 Current 并存以供对照时，可临时放在：

```text
<owner-directory>/assets/<object-id>/.review/<revision-id>/
```

同一对象只允许一个 Review 候选。批准后将必要文件提升到稳定 Current 路径，并清理
`.review/` 候选；未批准候选不能替代 Current。

### Revision History

普通 Revision 只由 Git 历史保存，不创建 History 目录副本。

只有人工批准的重要设计节点或确需独立追溯的历史快照进入：

```text
docs/99_Archive/<domain>/<object-id>/revisions/<revision-id>/
```

若仓库已有经治理确认的历史目录，继续使用该目录；迁移前必须完成引用审计并更新
Inventory。禁止建立第二个 Archive 根目录。

### Milestone

Milestone 记录进入其事实类型的既有目录：

- Issue：现有 Issue 目录
- Review / 验收证据：现有 Review 目录
- Decision：`docs/07_Decisions/`
- Change Log：`docs/08_Change_Log/`

需要保存完整二进制 Milestone 快照时进入：

```text
docs/99_Archive/<domain>/<object-id>/milestones/<revision-id>/
```

Milestone 只在人工批准、重要设计节点、发布或验收需要时创建，不复制到 Current
目录。不同事实类型不得混放以“方便查找”。

## 4. Asset Placement

资产放在其所属对象目录或现有 Design/Review 证据目录，不得放在仓库根目录。

推荐结构：

```text
<owner-directory>/
├── <current-spec>
└── assets/
    └── <object-id>/
```

Prototype 可保留自身 `assets/`，但不得复制仓库已存在的共享 Current 资产。
同一对象按资产包聚合，不能为 `.png`、`.svg`、`.html` 或某个生成工具分别建立
平行对象目录。
生成缓存、依赖目录和构建输出不得作为 Current 资产目录。

## 5. Protected Runtime And Generated Folders

以下目录属于依赖或生成内容，不是工程知识源：

- `.venv/`
- `backend/.venv/`
- `frontend/.next/`
- `frontend/node_modules/`
- `frontend/ceo-evidence/node_modules/`
- `frontend/ceo-evidence/dist/assets/`

不得把规范、唯一原始设计或不可再生成证据放入这些目录。是否清理由对应工具和已批准
任务决定，文档治理不得擅自移动或删除。

## 6. Folder Change Procedure

移动或新建目录前：

1. 确认现有目录不能承载该对象。
2. 检查 Markdown、脚本、配置、Agent 和构建引用。
3. 确认对象的唯一 Current 和 `object-id`。
4. 使用可追溯的 Git 移动保留历史。
5. 更新全部有效引用、Inventory 和迁移记录。
6. 通过 Review 后再将旧路径标记为历史。

禁止仅为“看起来更整齐”迁移代码引用文件或大批历史资产。
