# Content Growth HTML Targeted Revision Review

Status: Review
Authority Class: REVIEW
Disposition: TARGETED REVISION IMPROVED — NOT ACCEPTED; FIX REQUIRED
Date: 2026-09-16
Owner: CEO / HTML revision owner
Next Gate: STOP FOR CEO REVIEW

## 结论

产品表达方向已经落实，不需要再扩导航或重新研究。当前主要问题从“产品合同缺口”转为“HTML实现与事实一致性缺陷”。暂不通过定向修订验收。README的90/90是作者自测记录，不是独立验收；若使用前轮三选一，属于B方向成立但需定向修正，B不代表这些缺陷可忽略。

## 证据边界

本轮读取用户指定目录的新源码、README、自测脚本，并实际查看现存_shots3/F-production-lines.png及G-workflow-script.png。截图是交付目录中的作者证据，不是本轮重新操作浏览器取得；可能早于最终源码。上轮本地file访问被浏览器安全策略阻止，本轮未尝试替代浏览器/本地服务器绕过，也没有运行控制浏览器的测试脚本。以下问题是源码静态可定位路径，未宣称浏览器复现。

## 已明显改善

- app.js routeConv按team/employee/work/step分别解析实际接收人；旧conv-open路径已换为统一discuss。
- 会话按scope/对象/Work/Step/Account生成key，异步捕获sid，跨会话回写比旧全局S.conv方式可靠；消息有emp身份。
- Production Lines和Cross-line Queue共存；按方法展示步骤及承担人，不再固定12 Tabs。
- 开工出现Target Deliverables及必要规格，创建新Work，不再默认跳旧W-204。
- 步骤对话、版本记录、下游影响和员工入口已进入专业工作流程。产线/Workflow截图支持这些结构已被呈现。

## 必须修复

### P1-1 跨Proposal交付ID碰撞，Work可读取别的账号/提案合同

证据：data-wf.js 227–263，PROP-6/PROP-7各自重复TD-1/TD-2；delivById约280行遍历所有Proposal取第一个匹配，pages2.js:264仅传w.deliv。

路径：PROP-7的TD-2是抖音创始人IP、60秒；PROP-6的TD-2是抖音品牌号、25秒。新W-209标题/规格可正确，但Brief调用delivOfWork时得到PROP-6合同，WHY/GOAL可能变成品牌号目标。这不是Mock可忽略问题，而是同Work展示两套交付事实。

建议：使用现有Proposal＋Deliverable组合身份查找，或真实全局唯一ID；确认开工快照与当前Work输入一致。验收同名TD在两个Proposal均不串合同，包括单文件版本。

### P1-2 “采用备选”只改按钮，不改变实际开工

证据：pages.js:789–794只写S.delivAlt；openDeliverables只据此换按钮文案，deliv-confirm:704–725仍取原d.method/d.spec。

路径：PROP-7将8页改为9页、长文改短，或PROP-6数字人口播改屏幕演示，确认后仍按原规格/方法创建Work与团队步骤。

建议：采用备选形成明确已选交付值，预览摘要与Work/步骤/输入均消费同一值；若未支持选择，应明确不可用，不展示已采用。验收方法变化同时改变必要责任和步骤，页数变化回显到Brief。

### P1-3 无Owner提示后仍执行结果生成

证据：app.js:388–407，c.gap仅插入“不做执行”提示，随后仍写working、setTimeout、buildResult、applyResult；发送按钮未因此禁用，处理函数无return。

路径：无Owner Work的对话发送选题/灵感请求，仍可能新增数据或回复已完成；提示与状态矛盾。

建议：保存用户输入后终止执行分支，显示待分配及恢复入口；以后合法接收再推进。不能仅禁用按钮而留处理路径绕过。

### P1-4 组合提案与全局数据分析仍有跨账号落地

证据：app.js:584–599 findOrMakeCombo全局优先PROP-6/PROP-8，无当前账号/来源匹配，已有非空target不更新；applyResult(data)仍在无Account时默认dy-brand（约625行）。

路径：账号B组合请求复用账号A既有提案；Portfolio解释数据直接新增抖音品牌号实验，回复却称全部账号。原“硬编码目标”只修了topic/idea部分，未完全关闭。

建议：按当前对象/提案和明确目标复用；没对应对象才建立正确候选。没有Target的分析允许解释/未分配建议，不擅自创建账号实验。检验A→B→未分配三次输入互不串账。

### P2-5 Step影响按数组位置而非真实依赖，误伤并行步骤

证据：app.js:535–553使用m.steps.slice(idx+1)作为全部下游，把后续已开始/完成步骤统一改wait；data-wf方法定义为顺序数组，新Work也将前一项直接作为依赖。

问题：改脚本不必让已确认人物授权失效；产品允许独立准备并行，当前逻辑却把所有后续项当依赖。文案“没引用它的步骤不受影响”与算法不符。

建议：在当前Mock步骤事实中表达真实依赖，按被引用版本传播影响；不新增Runtime。保留旧结果，受影响的新制作状态另行说明。至少验证脚本变化影响合成/字幕，但不使独立授权检查失效。

### P2-6 展示经营合同的精确程度仍不足

证据：pages2.js:217成功判据优先prop.criteria；G-workflow-script截图W-209显示“见各Target Deliverable”，没有交付自己的具体判据。右侧视频Work缩略图还标“图文”。截图可能较旧，后者需浏览器确认。

建议：交付摘要读取当前Work准确交付合同；形式/规格预览由Format/Method/Spec驱动，而不是账号默认外观。修P1-1后同步核对这里。

## 视觉/专业表达建议（不阻塞核心语义）

F-production-lines截图顶部Team Presence、方法分组与跨线队列比旧版清楚；但大量“不是新导航”“唯一事实”“不重复计数”等合同解释占据日常操作空间。可留在说明/Review注释，主界面保留用户需要的负责人、目标、方法、规格、下一步。G-workflow-script里合同字段占据大量高度，实际脚本在下方；优先让当前产物与步骤工作更近，技术元数据按需查看。这是定向层级优化，不要求重画。

## 自测为什么没发现

_test-full.js检查交付数量、路线、Scope理由、产线计数和页面元素，能证明路径存在；不足以证明确认值传递、跨Proposal身份隔离、无Owner无副作用及真实依赖传播。保留现有检查，补四个P1的值级断言和一组并行依赖反例。不要以截图数量或90个PASS代替业务事实一致性。

## 下一步

先修P1-1到P1-4，再修步骤依赖与交付摘要；同步分文件与单文件产物。仅需定向HTML修正，不需要修改产品Authority。修后回报交付值、跨账号、无Owner、依赖反例证据；浏览器实操验收仍需合法可访问环境，本轮未完成。

本轮只新增此Review，未修改HTML、原型源码、测试、产品合同或Authority，未commit/push。

**STOP FOR CEO REVIEW。**

## 输入指纹

- `Content Growth Workspace.html` SHA256 `1a2169eab0f397152e2bccd0f1aa387eeb57ab82942c3ec57951b9787c84250c`
- `app.js` SHA256 `f1b0563841aa8bd6fb4af1a10adbf5aae500c67b8952cde5706f7f07078b5fe9`
- `pages.js` SHA256 `f24d8e158ce7d02da4ed6e92891585eaf8070eaec2fde7095cdfb8c1e5f44452`
- `pages2.js` SHA256 `ede03582207259bfa473783ed3743e4070c2341341281d7ab1f20ed3eadfe3ad`
- `data-wf.js` SHA256 `9d4e72279ebc716aa27b187042ab2ae5aedeefb22641dcb882dc3e80b1902118`
