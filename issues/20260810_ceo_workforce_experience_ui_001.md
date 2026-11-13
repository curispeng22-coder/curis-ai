# CEO-WORKFORCE-EXPERIENCE-UI-001

Status: Completed  
Decision: `PASS_CEO_WORKFORCE_EXPERIENCE_UI`

## 1. 目的

把 Blueprint 4.13 / EvoFlow 研究转译中已经确定的“AI Workforce Card”和“CEO Assistant
第一位员工”在 Desktop 首屏真实呈现出来。当前 CEO Desk 只有员工数量和 Assistant 入口，
无法回答谁负责什么、向谁汇报、当前状态和下一步是什么；组织页又仍偏旧后台。

## 2. 产品边界

- CEO Desk 仍是唯一默认入口，不新增 Agent Center 或员工管理一级导航。
- 只消费已通过 Review 的 Runtime Company / AI Organization 快照，不从旧 Project / Task
  聚合组织事实。
- CEO Assistant 是 Company-level 首位 AI 员工；专业 AI 员工在其下按 `parent_id` / 状态
  展示，缺失字段显示“未记录”，不填充示例数据。
- 卡片是 Runtime 事实的只读投影；雇佣、能力装配、组织变更仍不在本 Issue 实现。
- 共享 Assistant 浮层保留两列 Shell，不增加第三栏；只补充主动汇报与“我正在关注”表达。

## 3. 允许范围

- `frontend/app/ceo-office/page.js`
- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- 本 Issue 对应 Review、Current State、Change Log

不得修改 Runtime schema、业务 API、活动数据库、旧组织 API、导航结构、Desktop Rust 壳或
外部平台 API。

## 4. 验收条件

1. CEO Desk 首屏出现 CEO → CEO Assistant → 专业 AI 员工的责任关系，而非仅显示数量。
2. 每张 Workforce Card 至少显示身份、状态、汇报对象、能力引用 / 结果上下文、主要动作
   的可用事实；缺失字段明确显示未记录。
3. Assistant 首次打开可见公司简报、待 CEO、风险和正在关注的工作空间，并能回到业务现场。
4. UI 不创建第二套员工 / Task / Agent 状态；Runtime API 失败时保持现有 fail-closed。
5. 前端聚焦测试、scoped ESLint、Next build 通过；桌面视觉保持纯色、克制、无额外彩色卡片。
