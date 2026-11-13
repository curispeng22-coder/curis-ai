# CURIS CODEX COMPETITIVE VERIFICATION REVIEW

Authority Class: RESEARCH / EVIDENCE
Status: Review
Date: 2026-09-13
Disposition: FOR CEO / CHATGPT REVIEW — recommendations only; NO IMPLEMENTATION

本轮 **Phase 2 独立Verification完成并提交Review**；没有宣称早先“全部竞品深研究”已经完成。22项Reference仍为NEED MORE EVIDENCE，P1产品不以库存描述充当本轮实操。当前HTML **未通过像素与交互验收**。

## CEO 必答八项

1. **Zcode多少判断正确？** 主矩阵§3.1–3.14共133行：53 KEEP（39.8%，仅方向）、4 REPLACE、36 COMBINE、18 CURIS ORIGINAL、22 NEED MORE EVIDENCE。18项原创包含原本正确的L0及应退回原创的项，不能简单加成正确率；53 KEEP也不等于53项原数值/交互全部正确。
2. **哪些Best应替换？** Z003 Context不能把Codex右环境栏反向搬来，改为Curis Context职责+Linear集合导航；Z034 Expert Detail从Coze配置面改为WorkBuddy消费详情+Curis责任边界；Z086恢复与Z088 Resume从WorkBuddy泛任务描述改为Cursor中断续作的有限参考。这是4个原表行，不是4个不同产品。其余Search、Result、Agent Work属于COMBINE，不混入替换计数。
3. **EvoFlow加入哪里？** 10条独立补充登记：Employee/Agent/Work分层、Task Center与事项、Approval空态、Permission有效状态、能力与Context Inspector、运行/时长/队列提示、会话文件范围、Workflow高级项折叠、Automation定义/运行记录，以及Result/Stop恢复反例。9条正向参考+1条避免行为；没有新增L4、没有擅自新增Curis对象/一级导航。
4. **HTML多少L4实现？** 原24个含L4行，**0/24完整VERIFIED**。多数有部分结构，但几何、状态、动作没有共同完成。最终保留7类局部L4目标；未量全的状态不能成为可直接施工的完备像素规格。
5. **哪些只是文档说参考？** Expert/Skill实际复用三列大卡；Claude Composer变成900宽固定表单+定时重绘；Linear Search把完整搜索页误认浮层且Enter无动作；Cursor Source/Preview/Maximize只剩tab外观；Agent进度是静态计划/计时替身；Claude Error的Retry不执行；Assistant展开直接抛错。详见逐项Fidelity表。
6. **哪些被旧Truth污染？** Employee默认profile/Context完整档案、Shared Composer状态与执行身份处理、Shell T控件及缺少resize/maximize、generic Workspace使用CG context、RD高风险直接批准与相互矛盾状态、empty/error混合fixture。七区导航、Iris、Employee三态已正确；没有把合法渠道名或Work已完成误报成身份违规。
7. **CG/RD消费最新Authority了吗？** **部分消费，未通过完整验收**。CG正确Workspace/Operating入口，但逐账号Variant/Publication/eligibility/receipt链不足；RD确实有代码/测试/评审/发布专业结构，但Holder/Executor与Frozen Shared Shell supersession未完整落地。不是仅换标题，也不是两套软件。
8. **修补、部分大幅重做还是整体重做？** **大幅重做共享交互组件和受影响页面**。保留Company OS对象关系、七区、Iris、Business分域、已有路由与有价值阅读结构；重做Shared Composer、Pane controls、Search、Employee宿主、Agent/Result连续操作，再按CG/RD当前实例填专业链。全盘推翻会丢掉已正确结构，零碎调CSS则无法修复状态断点。

## 下一轮修复建议顺序（尚未执行）

| Priority | 具体Issue方向 | Done evidence |
|---|---|---|
| P0 | 修复Assistant ico ReferenceError | 全局展开/收起、切路由、输入不丢、无console错误 |
| P0 | Shared Composer状态闭环 | 空disabled、文件选择/移除、发送追加、运行/Stop/继续、draft与上下文保留 |
| P0 | Shell T1/T2/T3与Pane ownership | 开关位置迁移、resize/min width、maximize/Esc、focus/scroll、scope记忆 |
| P0 | Employee Conversation-first/Utility Detail | 同一员工进入Conversation，身份与当前工作一致 |
| P0 | CG逐账号发布链 | 每个target/variant/publication/eligibility/receipt可打开追溯 |
| P0 | RD现行规则与Decision | Holder≠Executor、ReviewRequest≠handoff、Layer0不直接批准高风险 |
| P0 | Search/Result连续性 | Arrow/Enter/Esc；真实preview/source；返回对话携带结果引用 |
| P1 | Talent Expert/Skill独立卡 | 对照M1/M2完成宽高/间距/状态与动作，再验hover/focus |
| P1 | Empty/Error/恢复一致性 | 正常/空/错/中断不混fixture；Retry确实重试并反馈 |

以上仍需CEO/ChatGPT Review与后续正式Issue；本轮没有执行修复或把Reference变为Product Authority。下一轮Reference只从[Final Decisions](CURIS_FINAL_COMPETITIVE_REFERENCE_DECISIONS.md)消费；Current Authority优先级不变。NEED MORE EVIDENCE条目在补证或明确降级前不可按L4施工。

## 交付物

- [Independent Reference Verification](CURIS_COMPETITIVE_REFERENCE_VERIFICATION.md)：133行逐项独立决策与计数。
- [HTML Pixel Fidelity Audit](CURIS_HTML_PIXEL_FIDELITY_AUDIT.md)：组件对照、24项L4核销、M1–M8测量。
- [Current Truth Drift Audit](CURIS_HTML_CURRENT_TRUTH_DRIFT_AUDIT.md)：25个Surface/子面裁决及CG/RD重点。
- [Final Reference Decisions](CURIS_FINAL_COMPETITIVE_REFERENCE_DECISIONS.md)：唯一下一轮Reference登记，含EV01–EV10。
- [Evidence Index](evidence/EVIDENCE_INDEX.md)：原图、DOM、限制、测试对象与版本。

文档均Status: Review、Authority Class: RESEARCH / EVIDENCE。未更新Current Pointer/CHANGE_LOG：本轮没有改Current Truth，只在独立research目录交付Verification。旧Zcode研究保持provenance；本轮输入hash最终验证见[evidence/integrity-check.json](evidence/integrity-check.json)。

## Review limits / disposition

真实操作：WorkBuddy、Claude（Gateway失败边界）、Cursor、EvoFlow0.6.1、Linear、Coze、ChatGPT无登录Web。Codex E5为旧实拍，当前Native工具禁止访问；未绕过。没有证据确认真实并行生命周期、审批通过/拒绝、完整Claude Memory、桌面ChatGPT/通知/重启恢复，相关项保留限制。

恢复参考Z086/Z088基于既有独立Cursor[中断截图](</Users/yy/Documents/Curis Competitive Research/2026-09-10/research/competitive-ui/cursor/20260910-interrupted.jpg>)及[继续结果](</Users/yy/Documents/Curis Competitive Research/2026-09-10/research/competitive-ui/cursor/20260910-resumed-result.jpg>)，是Sep10 provenance，不是本轮再执行；适用范围仅同任务继续，不能证明任意失败/重启/版本回滚。EvoFlow本轮Stop丢掉未完成响应，因此不得选为最佳恢复。

VERDICT: VERIFICATION READY FOR REVIEW; HTML FIDELITY NOT ACCEPTED; CURRENT AUTHORITY UNCHANGED; REFERENCE GAPS EXPLICIT.
Owner: CEO / ChatGPT Review. Next Gate: 接受或修订Decision Register，再授权HTML修复Issue。本轮STOP，无HTML/Figma/Runtime/Authority改动，无stage/commit/push。

**CURIS CODEX COMPETITIVE + HTML VERIFICATION — READY FOR CEO / CHATGPT REVIEW**
