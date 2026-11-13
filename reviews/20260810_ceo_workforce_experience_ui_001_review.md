# CEO-WORKFORCE-EXPERIENCE-UI-001 Review

Status: Review  
Decision: `PASS_CEO_WORKFORCE_EXPERIENCE_UI`  
Date: 2026-08-10

## 结论

PASS。CEO Desk 已用 Runtime Company / AI Organization 快照呈现
`CEO → CEO Assistant → 专业 AI 员工` 责任关系；CEO Assistant 作为公司级首位 AI 员工计入
CEO Desk 与 Assistant 简报，不再出现“Assistant 已存在但 AI 员工为 0”的矛盾。共享 Assistant
首次进入 CEO Desk 自动打开，显示公司简报、待 CEO、风险和“我正在关注”的 Workspace 返回入口。

## 实际改动文件

- `frontend/app/ceo-office/page.js`
- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `reviews/20260810_ceo_workforce_experience_ui_001_review.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

未修改 Backend、Desktop、Runtime schema、活动数据库、旧组织 API、导航、prototype 或真实平台 API。

## 产品与安全边界

- Workforce Card 是 Runtime 事实的只读投影，显示身份、状态、汇报对象、能力引用、运行引用、
  组织版本和主要动作；缺失值明确为“未记录 / 尚无”。
- 专业 AI 员工只按 `parent_id` 判断是否向 CEO Assistant 汇报，不生成示例员工或第二套组织状态。
- Assistant 查询只汇总 Runtime 快照；执行意图保持 fail-closed，已删除不可达的旧 Task 成功展示分支。
- Assistant 仍是根布局共享浮层，没有第三列或 Workspace 专属 Assistant。

## 浏览器视觉验收

Codex In-app Browser，`http://localhost:3000`，1440×900：

- Workspace Portal：3 个真实 Workspace，状态、蓝图和 Simulation 门禁可见；
- Workspace Studio：三类 Workspace 的最小创建入口可用，仍明确受 Simulation / CEO 验收门禁约束；
- 研发、小红书、抖音 / TikTok 三个运行现场具有独立业务语言和空态；
- CEO Desk：AI 团队运行图与 Assistant 关注空间可见，Assistant 计数为 1；
- fresh 最终页浏览器 warning / error 日志为 0。

证据：

- `/tmp/curis-desktop-complete-browser-20260810/01-workspace-portal.png`
- `/tmp/curis-desktop-complete-browser-20260810/02-workspace-studio.png`
- `/tmp/curis-desktop-complete-browser-20260810/03-rd-workbench.png`
- `/tmp/curis-desktop-complete-browser-20260810/04-xhs-workbench.png`
- `/tmp/curis-desktop-complete-browser-20260810/05-ttk-workbench.png`
- `/tmp/curis-desktop-complete-browser-20260810/08-ceo-assistant-final.png`

## 自动验证

```text
Frontend Runtime focused tests: 23 passed, 0 failed
Scoped ESLint: PASS
Next production build: PASS, 44/44 static pages
Scoped git diff check: PASS
```

活动 `data/curis.sqlite` 仅只读观察，SHA-256=
`884b2adeba5a61fb3bce68ddcf6d81b1453a730fb5df8740678537fe363d7662`。

## 未进入范围

Workspace Studio 当前仍是最小 Runtime Workspace 创建入口。Blueprint 4.13 中的岗位 / 能力 / 工具 /
知识 / 节奏装配、Simulation 工作台、审批交付和回滚需要新的明确 Issue；本 Review 不把当前三步表单写成
完整 Workspace Studio，也不授权扩展到旧链或清单外文件。
