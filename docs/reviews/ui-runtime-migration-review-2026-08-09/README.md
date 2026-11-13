# Curis UI Runtime Migration Review（2026-08-09）

Status: Review  
Decision: `PASS_TO_UI_RUNTIME_IMPLEMENTATION`  
Input: `PASS_RUNTIME_API_WITH_BASELINE_BLOCKERS`  

Runtime Foundation、三业务 Backend Simulation 和 Runtime API Adapter 已通过各自 Review。现在把目标产品第一次落到可实现的 CEO 使用界面；本 Review 只授权第一批 Company OS UI 迁移，不授权三业务页面全部重写，也不授权 Desktop 打包。

## 1. UI 不是新产品层

```text
Runtime API（唯一业务事实入口）
→ Company OS Shell（固定）
→ CEO Desk / Business Map / Workspace Portal
→ Workspace Runtime（业务特化）
→ Global CEO Assistant（共享身份与升级入口）
```

前端不能继续从 Project、Task、静态演示数据或 DOM 状态反推产品。旧页面与旧数据保留作为迁移参考，但不再成为 CEO 一级经营入口。

## 2. 本阶段用户路径

### 2.1 空公司首次进入

1. 打开 Curis，Runtime API 判断当前 Tenant 没有 Company；
2. 进入“空白但不空旷”的 Founding Guide，先看到 CEO Assistant 身份和一句欢迎；
3. CEO 表达经营意图，Assistant 只生成可修改的 FoundingRun 草案；
4. CEO 确认后才产生 Company / CEO Assistant，离开可恢复，失败不显示假成功；
5. 完成后进入 CEO Desk，而不是直接进入 Project 列表。

### 2.2 已有公司进入

1. 进入 CEO Desk，首屏是 Operating Day：今日摘要、需要 CEO 处理的事项、风险、AI 团队状态、业务版图和最近结果；
2. 点击业务版图进入 Workspace Portal；
3. 点击某一办公室进入运行态 Workspace；
4. Assistant 作为共享浮层按上下文出现，不占固定第三栏，不创建第二套聊天任务系统；
5. 高影响动作回到 CEO Decision / Acceptance，完成后回到 CEO Desk。

## 3. 固定 Company OS Shell

- Desktop First：`220px` 侧栏、`52px` 顶栏、全宽主内容和一个 Global Assistant 层；
- 导航只表达公司稳定路径：CEO 工作台、经营、业务、AI 团队、工作空间、会议工作台、决策室、动态办公室、公司资源；
- 办公室入口由配置的 Workspace 生成，不与公司级栏目平级；
- 旧 Project / Task / Execution 页面不删除，先从一级导航移入 Workspace 内部或迁移兼容入口；
- 主题只保留系统 / 浅色 / 深色，深色主按钮品牌绿，浅色主按钮深色实心；所有用户文案中文。

## 4. 第一批屏幕契约

| 屏幕 | CEO 看到什么 | 主要动作 | Runtime 来源 |
| --- | --- | --- | --- |
| Founding Guide | Assistant、经营意图、草案状态、下一步 | 创建 / 修改 / 继续 / 放弃 | FoundingRun API |
| CEO Desk | 今日经营摘要、Matters、风险、AI 团队、业务版图、结果回流 | 查看、委派、决策、验收、回到办公室 | Company Snapshot + Simulation 投影 |
| Business Map | 每个业务的目标结果、当前周期、证据新鲜度、办公室状态 | 进入 Workspace、扩展 / 暂停 / 查看影响 | Company Snapshot / Workspace |
| Workspace Portal | 已配置办公室、活跃周期、待 CEO 验收、阻塞 | 进入办公室、查看运行状态 | Company Snapshot / Simulation |
| Global Assistant | 当前页面上下文、事实 / 未知、需要 CEO 的原因、下一动作 | 查看、确认、退回、打开关联对象 | Runtime API 投影 |

本阶段不在 UI 中实现完整 RD / XHS / TTK 业务细节；这些页面在下一份 UI Issue 中分别交付，但必须复用同一 Shell、Assistant 和 API。

## 5. 空、加载、失败和权限状态

- 空公司：说明“尚未建立”，不填充假业务；给出 Assistant 和唯一下一步；
- 空业务版图：说明还没有业务，提供“从意图开始”与“复用已验证方案”两种入口；
- API 加载：保持页面结构，只在当前区域显示加载状态，不闪烁旧 Project 数据；
- API 失败：显示中文原因、重试、回到 CEO Desk，不显示堆栈、路径或密钥；
- 越权 / 跨 Company：统一无权访问，不泄漏对象存在性；
- `WAITING_CEO`：只显示等待与原因，不允许系统自动批准；
- 失效 Simulation：显示“需重新验证”，不能继续显示可运行成功态。

## 6. 视觉与交互验收

- 一个视口一个主要叙事和一个主要动作；
- 不使用 Dashboard 卡片墙、彩色大面板、渐变、霓虹和第三栏秘书；
- Assistant 采用自然发言流，事实 / 观点 / 决议使用轻标签，不给每条消息整块着色；
- 状态动作由 Runtime 合法转换生成，不能使用任意“下一步”或自由拖拽改写事实；
- 所有主动作支持键盘焦点、明确中文名称、禁用 / 错误 / 加载状态；
- UI Browser Evidence 必须覆盖空公司、已有公司、Assistant 打开、跨 Workspace、失败和恢复路径；
- 截图只能证明 UI，不能替代 Runtime / API / Simulation 证据。

## 7. 迁移边界

允许：

- 重组 Company OS Shell、CEO Desk、Business Map、Workspace Portal、Founding Guide 的信息层级；
- 将旧 Project / Task 入口移入兼容区；
- 新增 Runtime API 客户端、共享运行状态 Provider 和错误 / 空状态组件；
- 保留现有视觉令牌并清理 Terra 历史命名对用户的暴露。

禁止：

- 删除旧路由、旧表或活动数据；
- 复制三套 Company OS；
- 将 Assistant 做成固定侧栏 / 第三列；
- 在没有 Runtime API 的情况下恢复 mock 数据；
- 在本 Issue 接入真实平台 API 或修改 Desktop；
- 用视觉完成宣称产品完成。

## 8. 通过条件

1. 页面只从 Runtime API 读取目标对象，且 Company / Tenant 隔离；
2. 空公司能创建 FoundingRun 并恢复，已有公司能进入 CEO Desk；
3. CEO Desk、Business Map、Workspace Portal、Assistant 入口和错误状态均有浏览器证据；
4. 旧 Project / Task 页面不再是一级产品入口，但数据与兼容路由仍可访问；
5. 三主题、中文、220px / 52px Shell 和无第三栏规则逐页一致；
6. API / Runtime / Simulation 的既有聚焦回归继续通过；
7. Review 明确 UI 已通过的屏幕、未完成的三个 Workspace 细节和下一 Issue。

本 Review 通过后，执行 `issues/20260809_ui_runtime_migration_001.md`；完成后暂停，进入三个业务 Workspace UI Issue，最后才进入 Desktop 接入。
