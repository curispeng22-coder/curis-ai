# MVP Phase 1 / S1 — App Shell 与 Terra Design System Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_mvp_phase1_s1_app_shell_design_system.md`

## Conclusion

- 23/23 个 CEO Office 页面继续复用唯一 `TerraShell`，未新增第二套壳层。
- Shell 已补齐全局 AI Assistant Layer；当前未连接服务，界面明确说明未执行任何动作。
- Terra 原语补齐 `Input / Table / Modal / Drawer` 与三种业务卡片。
- 员工管理页实际采用 `EmployeeCard / TerraDrawer / TerraInput`；确认流程复用 `TerraModal`。
- 未新增依赖，未修改 API、数据库或 Mock 经营数据。

## Verification

- `pnpm --dir frontend lint`：PASS。
- `pnpm --dir frontend build`：PASS，26 个静态页面生成成功。
- `git diff --check`：PASS。
- 静态核对：CEO Office `page.js` 23 个，`TerraShell` 使用 23 个。
- Desktop browser：员工管理页面、全局 AI 秘书入口及抽屉可达；关闭行为通过。
- Mobile browser（390×844）：无横向溢出；AI 抽屉宽 356；导航抽屉标签完整可见；关闭态具备 `aria-hidden` 与 `inert`。

## Note

- 浏览器未使用外部登录；员工接口因此进入真实的 `Failed to fetch` 错误态。本 Review 不把未登录状态误报为员工数据流 E2E。

## Change Summary

- 复用现有 Shell，并加入有明确能力边界的全局 AI 助手抽屉。
- 使用原生 `<dialog>` 实现 Modal/Drawer 的焦点、Escape 与遮罩关闭。
- 补齐通用输入、表格和业务卡片；缺失事实统一显示 `未记录/未分配`。
- 移动端导航抽屉打开时显示完整标签，关闭时从辅助技术树隔离。

Handoff: sent to 产品规划席
