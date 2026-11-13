# CURIS_HTML_INTERACTION_RECHECK

> Authority Class: RESEARCH / EVIDENCE · Date: 2026-09-13
> 每项给出：操作路径 → 期望 → 实测结果（headless 渲染 + 代码路径；人工复验建议 Codex 执行）。

| 交互 | 路径 | 实测 |
|---|---|---|
| Composer 发送闭环 | 员工对话输入→Enter | user msg 追加 + sys 行 + running → 1.4s 员工回复追加 → 回 idle ✅ |
| Composer 空禁用 | 清空输入 | 发送 disabled ✅ |
| Composer 附件 | clip 菜单选文件 | chip 追加；× 移除 ✅ |
| @/# 引用 | @ 按钮菜单 | ref chip 追加/移除 ✅ |
| Model 菜单 | 模型 chip | 锚定菜单、当前 check、未配置项→解释行+不改值 ✅ |
| 权限档位 | 权限 chip 循环 | 最小→白名单→完全访问；effective 说明行（EV04） ✅ |
| Stop 保留输出 | 运行中点停止 | 状态 stopped+sys"未完成输出已保留"（EV10 反例规避） ✅ |
| Queue/Steering | 运行中再发送 | 排队提示（EV06） ✅ |
| Draft 持久 | 输入后切换 Surface 返回 | RT store 保留，不丢 ✅ |
| Assistant | ⌘J 或点击 pill | 展开=真会话+Composer；收起；拖动；路由切换不残留；无 console error ✅ |
| Search | ⌘K | 输入过滤、↑↓ 选择、Enter 打开对象、Esc 关闭、真实 Property 预览 ✅ |
| Result | Result Reference→Utility | Preview⇄Source 内容真切换；Follow-up 发送→同 thread 追加（回对话连续） ✅ |
| Utility 最大化 | header 按钮 | 覆盖 Main；Esc 还原 ✅ |
| Employee | 目录行点击 | Main=对话（默认 Tab conv）；姓名/头像→Utility 完整档案 ✅ |
| 工作区 emp-row | 点行展开 | 对话展开（同 thread 连续）；姓名→档案 ✅ |
| CG | 内容运营 Surface | 五段链展示；日历按钮 noop（PARTIAL 如实） ✅/PARTIAL |
| RD | 交付总览 | Layer0 仅 查看方案/暂缓；状态全局一致 ✅ |
| Talent | 安装技能 | 已安装⇄安装 状态切换 ✅ |
| Settings | 分类切换 | UI 状态更新（保存不接 Runtime，如实） ✅ |
| State Switcher | 左下 DESIGN TOOL | normal/emptyFirst/needsCEO/error 一致性（error→同步失败；empty→独立 fixture） ✅ |

结论：Composer / Assistant / Search / Result / Pane / Employee / CG / RD 八类主交互真实可操作；CG 日历、Settings 保存、More 菜单为已登记 PARTIAL。

## 视觉重构轮新增交互（2026-09-13 第二次）

| 交互 | 实测 |
|---|---|
| CG 列表⇄日历（?view=cal / seg-pill） | 真实切换周视图，事件含 done/warn 指示线 ✅ |
| Meeting Room | 讨论线程（RT thread）+ Composer 发言 + 证据 Context + Proposal→决议 Utility ✅ |
| 经营洞察 | 趋势折线（SVG）+ 渠道 bars + 洞察行来源跳转 ✅ |
| Settings 搜索 | 输入→250ms 过滤左导航（?q=）✅ |
| Settings 保存 | 按钮→"已保存 ✓（原型内存）"反馈 ✅ |
| Message Actions | 复制全文（剪贴板）/ 重新生成 / More 菜单（引用/升级/标记）✅ |
| 附件上传态 | 上传中→已附加；损坏文件→失败态（不可移除需重试文案）✅ |
| Utility divider | 拖拽 300–560px + localStorage 记忆 + min width ✅ |
