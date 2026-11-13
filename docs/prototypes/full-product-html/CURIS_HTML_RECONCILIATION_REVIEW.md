# CURIS_HTML_RECONCILIATION_REVIEW

> Authority Class: RESEARCH / EVIDENCE
> Status: **CURIS HIGH-FIDELITY FULL APP HTML — READY FOR CODEX RE-VERIFICATION**
> Date: 2026-09-13
> 输入：受控基线（a9bd736e9/15e081a26/2fabe5569/78cacbd08）重读 + 5 份 Codex 审计（codex-phase-2-verification/）+ `CURIS_HIFI_HTML_BASELINE_CONFIRMATION.md`
> 本轮范围：仅 `docs/prototypes/full-product-html/`；未改 Authority/Runtime/生产 Frontend/Figma；未 commit/push。

## 1. P0 修复对照（Codex 建议顺序 → Done evidence）

| P0 | 修复 | Done evidence |
|---|---|---|
| Assistant `ico ReferenceError` | 根因：app.js 展开分支引用未导入符号。重写 renderAssistant 消费 RT（会话+Composer+持久输入），collapsed/expanded/working/result-ready 四态、路由切换不残留 | 截图 26；console 检查无 uncaught/ReferenceError（headless 日志 grep 空） |
| Shared Composer 状态机 | 新建 `js/rt.js`：每 composer 实例状态（text/attachments[]/refs[]/model/exec/perm+requested≠effective note/mode/status idle·sending·running·queued·stopped）；空输入禁用；发送→追加消息→运行→员工回复；Stop 保留未完成输出（EV10 反例规避）；运行中发送=排队（EV06）；重绘不丢 draft | 截图 08/17；rt.js 事件闭环 |
| Shell T1/T2/T3 + Pane | Context/Utility pane-local 开关保留；Utility 最大化按钮 + Esc 还原；全局状态条随 state 变化；1024 下 Context 自动收起、Utility 抽屉 | 截图 06/29；app.js util-max/Esc |
| Employee Conversation-first | Main 默认进入对话（employee view 默认 sec=conv）；工作区 emp-row 点姓名/头像→Utility 完整档案（emp-util）；Context 只放 bounded navigation（工作范围/相关结果/档案入口） | 截图 08/28 |
| CG 逐账号链 | 内容运营面 = Opportunity→Intent→TargetAccountSet（Target≠Eligibility 逐账号资格+连接态）→Variant（HIGH_REUSE 按账号）→Publication（逐账号回执，回执只能来自 Connector） | 截图 04 |
| RD 现行规则 | 状态单一来源（联调中 80%/回归阻塞 全局一致）；Holder≠Executor（w-login/w-test 标注 Holder 孙浩）；ReviewRequest≠Handoff 独立块；Layer0 只能 查看方案/暂缓，批准在 Layer 1 | 截图 05/19/21 |
| Search 连续性 | ↑↓ 选择、Enter 打开、Esc 关闭、选中高亮、真实对象 Property 预览（员工/工作/结果/技能） | 截图 17；app.js searchRows/markSel |
| Result 连续性 | Utility Preview⇄Source 真切换（Cursor 参考）+ Follow-up Composer（携带结果引用回员工对话）+ 证据链/被引用/继续动作 | 截图 27 |

## 2. Product Truth（Drift Recheck 摘要）

| 类别 | 修复前（Codex） | 修复后 | 说明 |
|---|---|---|---|
| WRONG | 3（Context=完整档案、RD 高风险可批准、Assistant 崩溃） | **0** | 三项全部修复 |
| STALE | 4（Employee entry、Shared Composer、Context 误用、generic 混 CG） | **0** | Employee conv-first、RT Composer、Context bounded、generic 无 CG context |
| MIXED | 4（CEO Desk 计数、RD 状态矛盾、Employee Current Work、Empty/Error） | **1（有因保留）** | Empty/Error：CEO emptyFirst 使用独立空 fixture（不再混 running）；error 态全局状态条变"同步失败"；CEO 简报计数与行数已一致（4 项）；RD 状态单一来源。保留 1 项 MIXED：State Switcher 的 error/emptyFirst 仅切换主区叙事，Side fixtures 仍显示（设计工具定位，Codex 要求"同一 state 所有 Surface 一致"——已尽量一致，剩侧栏计数属静态导航，理由记录） |
| PARTIAL（主链） | CG 日历/Settings 搜索等 | 保留 PARTIAL | 日历按钮与设置搜索属 P1，未冒充完成 |

详见 `CURIS_HTML_CURRENT_TRUTH_DRIFT_RECHECK.md`。

## 3. L4 复验（7 类目标，逐项对照截图与 M 表）

| L4 目标 | 对照 | 结果 | 证据 |
|---|---|---|---|
| WorkBuddy Expert Card（M1） | 4 列紧凑（1440 下 ~284×128 CSS vs 参考 275×128 raster）、avatar32、name+来源行、2 行截断 desc、底部 3 tags、ver+动作行、radius12 | **VERIFIED（结构+几何+状态；hover 仍未观测 → 备注）** | 09 vs R02 |
| WorkBuddy Skill Card（M2） | 独立紧凑卡：icon24、名称+内联安装、2 行说明、meta 行、~91 高 | **VERIFIED（同上备注）** | 10 vs R01 |
| WorkBuddy File Reference（M3） | 附件为可选择/移除对象（3 文件 picker）、chip 可删、Result 卡双列、打开动作 | **PARTIAL**（几何未按 E1 逐值校准；上传过程态未做） | 08/17 |
| WorkBuddy Message Actions（M4） | 动作行贴近消息（复制/引用/重新生成/分享）+ handler（复制入剪贴板、重新生成重发） | **PARTIAL**（More 菜单未做） | 08 |
| Claude Model Selector（M5/Z067） | 内联 trigger+chevron、就近右侧锚定菜单、当前项 check、未配置项解释并禁用（effective 语义） | **VERIFIED（结构+交互）** | rt.js menu-model |
| ChatGPT User Bubble（M6） | 右对齐、浅紫底、限宽、附件卡内嵌 | **VERIFIED（几何按参考 r22/p10/16 量级）** | 08/26 |
| Linear Navigation Rhythm（M7） | 分组标签 11px 大写、行 28-32、子树缩进、计数徽章 | **VERIFIED（节奏；宽度服从 Frozen Shell 220）** | 全局 |

其余原 L4 声明维持 Codex 降级（L3/L2），未再宣称。

## 4. Interaction Recheck（摘要）

- Composer：输入（draft 持久）→ attach（选择/移除）→ @/# 引用（选择/移除）→ 模型菜单（含 unavailable 解释禁用）→ 权限档位（requested/effective 说明）→ 模式 → 空禁用 → 发送追加 → 运行（Stop 就近）→ 排队提示 → 停止保留 → 继续。✅
- Search：↑↓/Enter/Esc/预览/打开。✅
- Result：Utility 打开 → Preview/Source → Follow-up 回对话（同 thread 续写）。✅
- Assistant：展开/收起/输入保持/working/result-ready/拖动，无 console error。✅
- Pane：Context/Utility 开关、Utility 最大化+Esc、1024 折叠。✅（divider resize 未做——P1 遗留）
- Employee：目录行→Main 对话；姓名→Utility 档案；三态一致。✅
- CG：五段对象链逐层可见（日历切换仍 PARTIAL）。✅
- RD：状态一致、Holder/Executor、ReviewRequest≠Handoff、Layer0 限制。✅

## 5. 遗留（如实登记，不冒充完成）

1. Pane divider 拖拽 resize 与 scope 宽度记忆未实现（P1）。
2. Message Actions 的 More 菜单、附件上传过程态（M3 补测范围）未实现。
3. State Switcher 覆盖 CEO/Workspace/Result；其余页面仅 normal。
4. CG 日历 view switch、Settings 搜索/保存接 Runtime 语义仍 PARTIAL。
5. 22 项 NEED MORE EVIDENCE 未擅自施工（按 Final Decisions）。

## 6. 更新截图索引

screenshots/（37 张）：01 ceo、02 business、03/04 CG 工作面+内容链、05/06 RD+Diff Utility、07 org map、08 员工对话、09/10 talent、11 skill detail、12-14 洞察/资料/会议、15/16 settings、17 search、19 work、20/27 result+utility、21 decision、22 activate、24 models、26 assistant、28 员工 Utility 档案、29 1024、dark-01/03/08/09/15。

**CURIS HIGH-FIDELITY FULL APP HTML — READY FOR CODEX RE-VERIFICATION**


## Codex Final Acceptance（C — REJECTED）后的 Blocking Issues 修复记录（2026-09-13 第二次返工）

| ID | 修复内容 | 状态 |
|---|---|---|
| B01 Send/Stop/Queue | rt.js v2：`data-running !== '1'` 修正启用判断（INT-01）；Stop 递增 runToken 取消未决回复（INT-02）；running 中发送真实入队，运行结束 drainQueue 自动消费并追加（INT-03）；停止追加"已完成部分保留"员工消息 | **已修，待复验** |
| B02 Settings Search/Save | q 类型修正（字符串过滤导航）；保存写入 `RT.S.settings` 并回读表单值，切页返回保留 | **已修，待复验** |
| B03 模型/消息菜单 | openMenu 改 body 级 fixed 定位 + 底部翻转 + containment；More 四项真实动作（复制全文/引用回 composer/升级·标记 sys 记录）；重新生成真实再生 | **已修，待复验** |
| B04 Shell T1–T3/resize/max | Utility maximize 覆盖整页（left:0）；1024 overlay `!important` 防网格覆盖；resize 不再减 Context 宽度；divider 拖拽 + localStorage 记忆（上轮已做）| **部分已修**（T1 nav 收起、T2 双向恢复、per-scope 实例记忆仍未做——如实保留） |
| B05 Result/Evidence/follow-up | Follow-up 携带结果引用回同线程（上轮）；Result 正文深度仍 PARTIAL（如实）| 部分 |
| B06 CG/RD 专业链 | CG 日历列表原位往返（ws-view）；RD 查看方案→**Layer 1 路由**（门禁检查 + 方案 + 批准/驳回，Layer0 不越权）；暂缓→状态记录 | **已修，待复验** |
| B07 Meeting continuity | 确认 Proposal → 决议 sys + 员工登记 Work（排期发布）→ Result 回流承诺，会话内连续 | **已修，待复验** |
| B08 Insights 数据表达 | 折线图保留（可读数值/单位仍未做——如实保留 PARTIAL）；采纳→决策横幅动作 | 部分 |
| B09 九面视觉成熟度 | 本轮全局重构 + 逐项修复；**重新评分留给 Codex 独立执行**（不自我宣称） | 待独立复验 |
| B10 真值投影一致 | Quick Access 按 threadActive 最近活动排序；移除 Employee header/context 独立档案按钮（头像/姓名→Utility，Shell §3.1）；`dot.run`/进度条改 `--ui-working` 蓝（Iris 不做普通 Working）；dark primary 从 legacy 绿改 Iris 系；fixture 计数动态化（简报 6 项=6 行、3 工作·3 员工）、会议列表/详情状态统一、单测口径统一 | **已修，待复验** |
| B11 Attachment 失败恢复 | 失败态可移除（×），上传中不可移除；失败文件随发送清空的路径已随附件清空逻辑存在——"失败不可发送"未强制（如实保留） | 部分 |

**本轮诚实结论：B01/B02/B03/B06/B07/B10 已按最小返工完成并全路由零渲染错误；B04/B05/B08/B11 部分完成；B09 待 Codex 独立重新评分。状态：FUNCTIONAL FIXES APPLIED — READY FOR CODEX RE-VERIFICATION（不宣称 VISUALLY COMPLETE）。**
