# CONTENT GROWTH — MULTI-ACCOUNT PUBLISHING JOURNEY
### 多账号发布旅程：Channel 添加 · 多账号结构 · Variant 生成 · 目标选择 · 9 态真实状态 · 失败/部分成功/驳回重提完整连续流程

Status: **RESEARCH / EXPERT RECOMMENDATION**（非 Frozen，非 Authority 修改）
Companion: `CONTENT_GROWTH_END_TO_END_JOURNEY_MODEL.md`（主文件·固定步骤格式·词汇表·Journey E/F 概述·Final Acceptance）· `CONTENT_GROWTH_CHANNEL_ACCOUNT_PUBLISHING_MODEL.md`（统一 Channel 模型·9 态·Calendar）· `Curis_Content_Growth_Domain_Authority.md`（Frozen·只消费）。
本文件范围：从「内容标可发布」之后到「每账号 per-Account 真相回流并可读回执」的全部按钮级操作；覆盖 Channel 添加、多账号结构建立、发布目标选择、Variant 三档生成、9 态状态机连续模拟、一次真实多账号发布剧本、Calendar 角色。**不**涉及内容创作本身（见 Doc 3）、不修改 Authority、不决定 UI/IA/Runtime/Schema/DB。

---

## 0. 红线与纪律

- **RESEARCH 状态**：本文件为产品细节研究，所有描述以文字即可完整模拟每个动作，**不画 UI / Wireframe / Figma / 视觉 / 前端 / Runtime / Schema / DB / Authority**。
- **复用既有对象**（不新造 primitive）：
  - Channel = Channel 对象 + Module + Connector `[CURIS-AUTH]``CHANNEL_NE_ACCOUNT`。
  - 多账号 = Channel Account（每账号独立 `positioning` / `tone_style`），经 OfficeAccountBinding 派生 Account Pool。
  - 发布 = Content Variant（绑单账号）+ Publication（per-Account 唯一真相源）。
  - 团队 = 陈帆（Channel Operator，负责渠道/账号/发布/反馈归集）· 李想（Producer）· 王颖（Research&Intel）。
- **必须体现 Frozen 不变量**（每条以下方标记引用）：
  - `CHANNEL_NE_ACCOUNT`：XHS/Douyin/TikTok/YouTube/Bilibili/公众号/视频号 = Channel（非独立 Workspace）；Channel 与 Channel Account 严格分离。
  - `OAUTH_FAILURE_KEEPS_ACCOUNT`：OAuth 失效 → 账号保留 + 授权降级 + 历史保留 + 当前执行降级，不删除账号。
  - `TARGET_IS_ACCOUNT_NOT_PLATFORM`：Target 粒度是账号；绑 N 账号 ≠ 每条内容群发所有账号。
  - `TARGET_NE_ELIGIBILITY`：Target（想发哪）≠ Eligibility（能不能发）；失效仍是 Target 仅 BLOCKED，禁静默删。
  - `PUBLICATION_PER_ACCOUNT_TRUTH`：状态/回执/时间逐账号独立，无「整体发布成功」概念。
  - `FACT_NOT_ROLLED_BACK`：已发生事实不得篡改/回滚其他账号。
  - `FUTURE_EXECUTION_GOVERNED_BY_POLICY`：未执行部分是否继续，读 distribution_execution_policy（BEST_EFFORT / ALL_REQUIRED），不把「不回滚」误读为「无条件继续」。
  - `NO_CROSS_ACCOUNT_CONTEXT_LEAK`：A 账号 Variant 不得串 B 账号 tone/策略/Knowledge。
  - `RECEIPT_FROM_CONNECTOR`：回执由 Connector 回填，不伪造。
  - `DISTRIBUTION_POLICY_IS_UNIQUE_SOURCE`：policy 唯一定义于契约④，本文件只读取服从。
  - `SCHEDULING_IS_CONDITIONAL`：scheduled 仅官方支持时有效，否则标不支持，不写死。
- **稳定动作词汇（语义锁定，UI 文案可微调）**：添加渠道 / 加账号 / 重新授权 / 发布 / 准备发布 / 生成预览 / 选为推荐版 / 重试 / 改后重提 / 查看回执 / 仅本次使用 / 加入长期监控 / 问员工。
- 证据标记：`[CURIS-AUTH]`=消费 Frozen 语义；`[REUSE]`=复用已有对象/行为。
- 全程禁止「UI 阶段再决定」；per-Account 真相必须说清，绝不允许一个「发布成功」覆盖所有账号。

---

## 1. 添加 CHANNEL（从内容「发布」触发或「渠道」入口）

### STEP 01
【用户当前看到】内容 Draft 已标「✅ 可发布」（见主文件 D05），用户点「发布」→ 因尚未连接任何 Channel，发布面板显示空态：「你还没有连接发布渠道。要发到哪？」下方平台网格：小红书 / 抖音 / TikTok / YouTube / Bilibili / 公众号 / 视频号。或者用户在「渠道」入口（低频区）主动点「+ 添加渠道」也到达同一网格。
【用户动作】点「小红书」（或「抖音」等）。
【立即反馈】网格该项高亮，弹出一行说明：「将打开小红书官方授权页，授权后成为你的『渠道』。」按钮「去授权 / 以后再说」。
【系统后台】尚未创建 Channel 对象；仅记录用户意图 `pending_channel=XHS`。
【Employee 行为】无（纯用户授权动作）。
【页面/状态变化】停留当前面板；未跳转前无对象创建。
【可返回/可撤销】「以后再说」→ 回到发布面板空态；授权中途取消 → 不建 Channel。
【异常】平台网格某项标灰（如该 Office 所在区域不支持）→ 该项显示「当前区域不可用」并给理由；仍可选其他。
【下一步】授权成功 → STEP 02；用户从「渠道」入口来 → STEP 02 同路径。

### STEP 02
【用户当前看到】点击「去授权」→ 跳转小红书官方 OAuth 页（或弹窗内嵌）；用户登录并点「同意授权」。
【立即反馈】平台页显示「授权成功」，自动回 Curis；面板顶部出现「小红书已连接 ✅」。
【系统后台】创建 Channel 对象（XHS，[REUSE] 统一 Channel 模型，`CHANNEL_NE_ACCOUNT`）+ 1 个 Channel Module 挂载（格式适配/发布执行等）+ 1 个 Connector 引用；陈帆（Channel Operator）自动接手后续账号配置准备。连接状态机初值 = `Connected`。
【Employee 行为】陈帆在后台确认 Connector 可达；若平台能力为 `CONDITIONAL`/`UNKNOWN`（如定时发布参数未经验证），陈帆在账号配置时不假设可用（遵 `SCHEDULING_IS_CONDITIONAL`）。
【页面/状态变化】渠道列表/发布面板出现「小红书 · 已连接 · 0 账号」；用户仍在发布流程中（无需退出重进）。
【可返回/可撤销】可「断开」（保留历史，见 STEP 04）；授权可逆但需平台侧操作，Curis 内点「断开」即停止调用。
【异常】授权被用户取消 → 回 STEP 01 空态，不建 Channel；授权回调超时 → 提示「授权未收到，重试 / 以后再说」。
【下一步】STEP 03（连接状态诚实表达）或 STEP 05（加第一个账号）。

### STEP 03
【用户当前看到】渠道列表里「小红书」一行显示连接状态徽标之一：Connected（绿）/ Not Connected（灰）/ Needs Permission（黄·权限不足）/ Failed（红·授权失败）/ Unavailable（黑·平台不支持 Connector）。用户点该行「查看状态」展开。
【立即反馈】展开显示：最近同步时间、Connector 健康、当前可发布能力（如「支持图文发布 ✅」「定时发布 ❓未验证」）。
【系统后台】状态值来自 Connector 回填，不臆造；`UNKNOWN`/`CONDITIONAL` 如实标注（[CURIS-AUTH]`SCHEDULING_IS_CONDITIONAL` 与 Capability Truth）。
【Employee 行为】若标 Unavailable/Failed，陈帆评估替代路径（见 STEP 04）。
【页面/状态变化】徽标即所见即所得，不美化。
【可返回/可撤销】「断开」/「重新授权」按需。
【异常】无独立异常；状态本身已表达异常。
【下一步】平台不支持 Connector → STEP 04；支持 → STEP 05。

### STEP 04
【用户当前看到】用户尝试添加某 Channel，平台网格该项标「Unavailable」+ 一行小字：「该平台当前无官方 Connector（API/授权未开放），无法自动发布。」
【用户动作】用户点该项查看详情，看到两种替代：「① 用 RPA/手动发布（非官方，合规风险自担）② 先跳过，等官方开放」。
【立即反馈】选①→ 该 Channel 标 `Unavailable` 但允许建立「手动发布」占位，发布时该 Channel 下账号只能「标记已发/待手动」；选②→ 不建，留待后续。
【系统后台】若选①：创建 Channel 对象（XHS 等）但 `connection_state=Unavailable` + `manual_mode=true`；明确不伪造回执（[CURIS-AUTH]`RECEIPT_FROM_CONNECTOR` 无法获得，故 Publication 状态仅记「待用户手动回填」）。
【Employee 行为】陈帆在发布后主动提示用户「该平台请自行发布并回填 URL」，不做自动执行。
【页面/状态变化】渠道列表该项标黑「Unavailable · 手动」；发布目标选择时该 Channel 下账号灰显并提示「需手动」。
【可返回/可撤销】可改选②删除该占位；手动回填的 URL 可编辑。
【异常】用户误以为自动成功 → 系统不生成任何「已发布」回执，只显示「待手动确认」，杜绝假成功。
【下一步】回到 STEP 05（加账号，无论自动/手动模式结构一致）。

---

## 2. 多账号结构（从第一次连接开始逐账号）

### STEP 05
【用户当前看到】Channel 详情（如「小红书」）显示账号列表空 +「加账号」按钮。用户点「加账号」。
【立即反馈】弹出该平台第 1 个账号的 OAuth（如小红书第 1 个号登录授权）；成功回显「账号已添加」。
【系统后台】创建 Channel Account（XHS·acc1，[REUSE] `CHANNEL_NE_ACCOUNT`），`authorization_state=Connected`；建立 OfficeAccountBinding（首版推荐 1 Account:1 Office [CURIS-AUTH]），派生进入 Account Pool。
【Employee 行为】陈帆准备询问定位；不自动假设。
【页面/状态变化】账号列表多一行（未命名/默认名 + 授权状态）；无定位标注。
【可返回/可撤销】可「断开」该账号（保留历史，遵 `OAUTH_FAILURE_KEEPS_ACCOUNT` 精神）；命名前可删。
【异常】授权过期 → 该账号 `authorization_state=Expired`，标红（见 STEP 17 续）；不阻断其他账号。
【下一步】STEP 06（命名 + 定位）。

### STEP 06
【用户当前看到】新账号行高亮「请命名并配置定位」。输入框预填「小红书账号1」，下方「定位」区显示王颖此前在 Office 级给的建议定位（来自主文件 A07：AI 科技主号·面向从业者·专业但易懂），并提供「用王颖建议 / 自定义」。
【用户动作】改命名为「AI科技主号」，点「用王颖建议」采纳定位；或改 Audience/Tone 后点「保存」。
【立即反馈】行更新为「AI科技主号」+ 定位标签「从业者·专业易懂」；保存成功气泡。
【系统后台】写 Channel Account.positioning / tone_style（每账号独立，[CURIS-AUTH]`NO_CROSS_ACCOUNT_CONTEXT_LEAK`）；该账号成为该 Channel 候选默认。
【Employee 行为】陈帆把账号级定位与 Office growth_context 对齐；如有偏差提示用户。
【页面/状态变化】账号行完整显示（名称+定位+授权）。
【可返回/可撤销】可随时「编辑」改名/改定位；历史版本留痕（不回滚事实）。
【异常】定位留空 → 系统标「未配置定位」，发布时该账号视为 Eligibility 降级（见 STEP 10 灰显）。
【下一步】STEP 07（设默认）或继续 STEP 05 加第 2、3 个账号。

### STEP 07
【用户当前看到】用户在该 Channel 多个账号中点某个账号行「设为默认」。
【立即反馈】该行出现「默认」徽标；其余账号默认标消失。
【系统后台】更新 Channel 级 `default_account` 引用；写入 Office 的 default_target_account_set 候选（[CURIS-AUTH]`BINDING_DERIVES_POOL`）。
【Employee 行为】无。
【页面/状态变化】发布时该账号在树中自动勾选（见 STEP 09）。
【可返回/可撤销】可改设其他为默认。
【异常】无。
【下一步】STEP 08（用户示例矩阵逐账号展开）或日常进入 STEP 09。

### STEP 08（用户示例矩阵逐账号建立，连续示例）
【用户当前看到】用户按业务需要重复 STEP 05–07 建立如下矩阵（与主文件 E02 一致）：
```
XHS      ├ AI科技主号（默认）   ├ AI工具测评号   └ 个人IP号
Douyin   ├ 主号（默认）         └ 视频实验号
TikTok   ├ US（默认）           └ SEA
YouTube  └ 主号（默认）
Bilibili └ 主号（默认）
```
【用户动作】逐平台点「加账号」并命名/采纳定位/设默认。每个账号可复用王颖 Office 级建议或微调（如测评号 Tone=「犀利实测」，个人IP号 Tone=「第一人称分享」）。
【立即反馈】每加一个列表多一行 + 定位标签；陈帆不要求用户记忆谁是谁。
【系统后台】每账号独立 Channel Account + Binding + Pool 派生；每个账号 `positioning` 严格独立，互不串（`NO_CROSS_ACCOUNT_CONTEXT_LEAK`）。
【Employee 行为】陈帆核对每账号定位与 Office 整体定位不冲突；矩阵组（如 KOS）可分组但内容须差异（合规同质化红线，[REUSE] 主文件 §0）。
【页面/状态变化】各 Channel 详情显示完整账号矩阵；Account Pool 全集就绪。
【可返回/可撤销】任一账号可改名/改定位/断连/重授权；不影响其他。
【异常】某次 OAuth 失败 → 仅该账号 `Expired`，其余正常（[CURIS-AUTH]`OAUTH_FAILURE_KEEPS_ACCOUNT`）。
【下一步】日常发布进入 STEP 09（Context 过滤，多数不主动切账号）。

### STEP 09
【用户当前看到】日常在「内容」Surface 工作时，顶部 Context 栏显示「当前：XHS·AI科技主号（默认）」。用户多数时候**不主动切**；只有当发布选目标或陈帆推荐时才出现账号树。
【用户动作】默认无操作；仅在发布 STEP 10 展开账号树时选择。
【立即反馈】无强制切换界面；Context 栏随任务显示当前 Channel/Account 过滤。
【系统后台】无写操作；仅读取默认账号用于预览推荐。
【Employee 行为】陈帆在发布时按内容定位推荐账号（Context filter 出现），不要求用户记忆账号细节。
【页面/状态变化】Context 栏随任务切换显示。
【可返回/可撤销】不适用。
【异常】无。
【下一步】进入 STEP 10（发布目标选择）。

---

## 3. 发布目标选择（Channel → Account → Variant 树）

### STEP 10
【用户当前看到】Draft「可发布」后点「发布」→ 发布目标选择面板展开 Channel→Account→Variant 树：
```
发布到
☑ 小红书（已连接）
   ☑ AI科技主号（默认·推荐）
   ☐ AI工具测评号
   ☐ 个人IP号
☑ 抖音（已连接）
   ☑ 主号（默认·推荐）
```
每账号行右侧标注：定位匹配度 / 授权状态 / 最近发布。
【用户动作】用户勾选/取消勾选具体账号；可「全选本 Channel」「清空」。
【立即反馈】勾选即时高亮；不匹配账号灰显（见 STEP 11）；未连接账号标「未连接」（见 STEP 12）；权限不足标「需授权」并阻断（见 STEP 13）。
【系统后台】组装 Target Account Set = Office Default Set + AI Recommendation + Manual Override 三源合并裁决（[CURIS-AUTH]`TARGET_IS_ACCOUNT_NOT_PLATFORM` + `DISTRIBUTION_POLICY_IS_UNIQUE_SOURCE`）；Target 是账号粒度，非平台。
【Employee 行为】陈帆据内容定位在 AI Recommendation 中预勾推荐账号，用户可覆盖；复杂选择在后台处理（[REUSE] 主文件 §3.3）。
【页面/状态变化】树随勾选更新；底部出现「生成预览」按钮（灰直到至少勾选 1 个可发账号）。
【可返回/可撤销】可取消勾选回退；Target 中失效账号仍保留为 BLOCKED（不静默删，[CURIS-AUTH]`TARGET_NE_ELIGIBILITY`）。
【异常】全选均不可发 → 「生成预览」保持灰，提示先解决授权/连接。
【下一步】STEP 11/12/13 处理特殊态，或 STEP 14 生成 Variant 预览。

### STEP 11（账号不 Eligible：定位不匹配灰显 + 确认覆盖）
【用户当前看到】树中「个人IP号」灰显，行右侧小字红：「内容定位（专业测评）与该账号定位（第一人称分享）偏差大，不可直接勾选」。
【用户动作】用户若坚持，点该行「确认覆盖发布？」→ 弹确认：「将以『完全不同』档生成该账号 Variant，可能损害账号调性一致性，确认？」点「确认覆盖」。
【立即反馈】灰显解除并勾选，行标「⚠️ 覆盖发布」。
【系统后台】该账号仍计入 Target；Eligibility 派生为 BLOCKED→手动放行；记录 override 原因（[CURIS-AUTH]`TARGET_NE_ELIGIBILITY` 仍 Target 不删）。
【Employee 行为】陈帆对该账号走「完全不同」档 Variant（STEP 15），并在发布后提示风险。
【页面/状态变化】该行状态变「覆盖发布」；预览区将显式标注。
【可返回/可撤销】取消勾选即回灰显，无残留。
【异常】无。
【下一步】STEP 14（生成预览，该账号用重档）。

### STEP 12（账号未连接：标「未连接」）
【用户当前看到】树中某账号（如 Bilibili·主号）标「未连接」，勾选时弹出：「该账号未连接，请先连接或跳过。」
【用户动作】点「去连接」→ 跳 STEP 01–02 走 OAuth；或点「跳过」取消勾选。
【立即反馈】去连接 → 该账号变 Connected 后行恢复可选；跳过 → 取消勾选。
【系统后台】连接状态来自 Connector；未连接则不生成该账号 Variant（无目标即无 Variant）。
【Employee 行为】无。
【页面/状态变化】该行状态随连接结果变化。
【可返回/可撤销】连接可断；勾选可恢复。
【异常】连接失败 → 回 STEP 03 状态表达。
【下一步】连接成功 → 回 STEP 10 勾选；否则继续其他账号。

### STEP 13（账号权限不足：标「需授权」阻断）
【用户当前看到】树中「抖音·主号」标「需授权」（黄），勾选该行时按钮变红阻断：「该账号授权过期/权限不足，无法发布，请重新授权。」
【用户动作】点「重新授权」→ 跳平台 OAuth（同 STEP 02）；或点「跳过该账号」。
【立即反馈】重新授权成功 → 标变 Connected，可勾选；失败 → 停留「需授权」。
【系统后台】该账号 `authorization_state` 升级回 Connected（[CURIS-AUTH]`OAUTH_FAILURE_KEEPS_ACCOUNT` 反向：曾保留现恢复）；未授权前该账号 Publication 不可建（Eligibility=BLOCKED）。
【Employee 行为】陈帆监控到该账号在 Target 中但 BLOCKED，提示用户「抖音主号待授权，其余可先发」。
【页面/状态变化】该行黄标随授权变化；其余账号不受影响。
【可返回/可撤销】授权可逆。
【异常】授权持续失败 → 该账号持续 BLOCKED，发布时该账号单独 Failed/Blocked（不牵连其他）。
【下一步】授权成功 → 回 STEP 10；或继续其他账号进入 STEP 14。

---

## 4. VARIANT 生成（同一 Intent 发不同账号三档）

### STEP 14
【用户当前看到】用户勾选好账号（如 XHS·AI科技主号 + XHS·个人IP号 + 抖音·主号）后点「生成预览」。面板下方展开每账号一张 Variant 预览卡，顶部标注档位：**轻适配 / 重生成 / 完全不同**。
【用户动作】用户逐张看预览；可对某张点「改一点」输入局部调整，或点「比稿」并排比较。
【立即反馈】每张卡显示：标题/正文/标签/封面微调/适配说明；档位不同说明不同（见 STEP 15–16）。
【系统后台】为每个勾选账号创建 Content Variant（绑**且仅绑**该账号，[CURIS-AUTH]`INTENT_SHARED_UPSTREAM` + `NO_CROSS_ACCOUNT_CONTEXT_LEAK`）；Variant 只消费目标账号 Context，不串号。
【Employee 行为】陈帆（或李想视觉）生成各账号 Variant；CEO 默认只见最终结果投影，Employee Working View 可见全部 Variant 对比（[REUSE] 主文件 §4.2）。
【页面/状态变化】发布面板变「预览态」：每账号一卡 + 风险检查（合规/频率/定位）即时结果。
【可返回/可撤销】未发布前任意 Variant 可改/可删重建；取消勾选账号即删其 Variant。
【异常】某账号 Variant 生成失败 → 该卡标「生成失败，重试」；其余卡正常。
【下一步】STEP 15/16/17 按档位深入；或 STEP 18 进入发布确认。

### STEP 15（轻适配档：同平台同调性）
【用户当前看到】XHS·AI科技主号 预览卡标「轻适配」：标题改了 1 个热词、标签加了 3 个、封面未动；说明：「与主号调性一致，仅做平台格式适配。」
【用户动作】用户点「采用」或「改一点」微调标签。
【立即反馈】卡片更新；标记 reuse_mode=HIGH_REUSE。
【系统后台】Variant.reuse_mode=HIGH_REUSE（[CURIS-AUTH]`INTENT_SHARED_UPSTREAM`）；仅 metadata 级适配，共享 Intent 核心。
【Employee 行为】陈帆确认合规（如标签不违规）。
【页面/状态变化】卡片标「✓ 轻适配」。
【可返回/可撤销】改一点 → 局部 Patch 该 Variant，不影响其他账号。
【异常】无。
【下一步】进入发布确认 STEP 18。

### STEP 16（重生成档：跨平台/调性差异大）
【用户当前看到】抖音·主号 预览卡标「重生成」：正文结构重排为短视频口播稿、标题改为悬念式、新增口播标签；说明：「跨平台重生成，基于同一 Intent 核心。」
【用户动作】用户点「比稿」将该卡与 XHS 主号卡并排，看差异高亮；满意则点「采用」。
【立即反馈】并排显示差异（结构/语气/标签），采用后卡片标「✓ 重生成」。
【系统后台】Variant.reuse_mode=FULL_DIVERGENCE（或中间档）；绑定该账号，不携带其他账号 Context。
【Employee 行为】李想/陈帆执行重生成。
【页面/状态变化】卡片状态更新。
【可返回/可撤销】可改选其他版或「改一点」仅影响此账号。
【异常】无。
【下一步】STEP 18。

### STEP 17（完全不同档：账号定位迥异 + 串号防护）
【用户当前看到】XHS·个人IP号 预览卡标「完全不同」：第一人称「我实测了 GPT-5.6…」口吻，与主号第三人称专业口吻完全不同；卡片顶部红条：「⚠️ 独立 Draft，仅共享 Intent 核心，不继承主号任何 tone/策略。」
【用户动作】用户点「查看依据」确认未串号；满意点「采用」。
【立即反馈】卡片标「✓ 完全不同」；系统内部校验该 Variant 未引用主号 tone_style（[CURIS-AUTH]`NO_CROSS_ACCOUNT_CONTEXT_LEAK` 强制隔离）。
【系统后台】该 Variant 仅引用目标账号 Context + Intent 核心；审计记录「context_source=个人IP号，无外部账号泄漏」。
【Employee 行为】陈帆复核隔离合规。
【页面/状态变化】卡片状态更新；比稿视图中该卡与主号并列但不共享样式。
【可返回/可撤销】局部改只影响该账号。
【异常】若检测到误引其他账号 Context → 卡片标「⚠️ 串号风险」并阻止发布，回生成重做。
【下一步】全部 Variant 满意 → STEP 18 发布确认。

---

## 5. 发布真实状态机（9 态逐一定义并连续模拟）

> 9 态语义锁定（[CURIS-AUTH]`PUBLICATION_PER_ACCOUNT_TRUTH`，逐账号独立，无整体成功）：

```
Ready            已就绪待发（Human-in-the-loop 确认前）
Needs Review     待人工审核（合规/品牌未过）
Needs Permission 待授权（账号/平台未就绪，BLOCKED）
Scheduled        已定时（每账号可不同时间，官方支持才有效）
Publishing       发布中（已提交 Connector，等待回执）
Platform Reviewing 平台审核中（平台侧排队/审核）
Published        已发布（平台回执确认，含真实 URL）
Failed           失败（附原因，Connector 回填）
Rejected         平台驳回（附原因，需改后重提）
```

### STEP 18（发布前看到什么 / 逐账号预览 / 时间选择）
【用户当前看到】所有 Variant 预览完成，面板底部「发布」按钮启用；上方显示「逐账号发布，每账号独立状态」。时间选项：① 全部立即 ② 各账号不同时间（定时，仅官方支持平台可选，[CURIS-AUTH]`SCHEDULING_IS_CONDITIONAL`）。
【用户动作】用户选「全部立即」；或展开某账号设「明早 9 点」（仅该平台支持时）。
【立即反馈】选定时 → 该账号 Variant 卡显示「⏰ 明早 9 点」；不支持定时的平台该项灰显「本平台不支持定时」。
【系统后台】创建 Publication 草稿（per-Account，status=Ready）；scheduled_at 仅在支持平台填值，否则置空标记不支持。
【Employee 行为】陈帆核对定时与频率合规（防超频）。
【页面/状态变化】每账号 Publication 进入 Ready。
【可返回/可撤销】发布前可改时间/改 Variant/取消勾选。
【异常】定时时间已过 → 提示「时间无效，改选未来」。
【下一步】STEP 19（Human-in-the-loop 确认发布）。

### STEP 19（Human-in-the-loop 确认）
【用户当前看到】点「发布」→ 弹出确认框：「将向以下 N 个账号提交发布（各账号独立回执）：XHS·AI科技主号 / XHS·个人IP号 / 抖音·主号。确认？」按钮「确认发布 / 再看看」。
【用户动作】点「确认发布」。
【立即反馈】按钮变「发布中…」；面板切到「发布状态」视图，每账号一行状态流。
【系统后台】每个 Variant 的 Publication.status 由 Ready → Publishing；调用对应 Connector 提交（[CURIS-AUTH]`RECEIPT_FROM_CONNECTOR` 待回填）。distribution_execution_policy 读取（BEST_EFFORT/ALL_REQUIRED）决定未执行部分是否继续（[CURIS-AUTH]`FUTURE_EXECUTION_GOVERNED_BY_POLICY`）。
【Employee 行为】陈帆监控提交与回执；失败账号触发重试/重授权流程。
【页面/状态变化】逐账号状态行出现，初始多为 Publishing。
【可返回/可撤销】发布已提交不可撤销事实（[CURIS-AUTH]`FACT_NOT_ROLLED_BACK`）；但 Scheduled 在到点前可改/撤。
【异常】确认框网络中断 → 提示「提交未确认，重试」；已提交的不重复提交。
【下一步】STEP 20–28 各态连续模拟。

### STEP 20（Ready / Needs Review / Needs Permission 三前态）
【用户当前看到】发布时某账号行显示：
- 「Needs Review」：该行标黄「待人工审核（品牌词待确认）」——若发布前审核未过（如 D05 漏项）；
- 「Needs Permission」：该行标黄「需授权」——即 STEP 13 的 BLOCKED 账号；
- 「Ready」：正常待发。
【用户动作】Needs Review → 点「去审核」补 AI 标识/事实；Needs Permission → 点「重新授权」（STEP 13 路径）。
【立即反馈】补完 → 该行转 Ready/Publishing；未处理 → 该账号保持 BLOCKED，不进 Publishing。
【系统后台】Needs Review/Permission 的 Publication 不调用 Connector；其余继续。policy=BEST_EFFORT 时其他账号照发；ALL_REQUIRED 时全部等待该账号就绪（[CURIS-AUTH]`FUTURE_EXECUTION_GOVERNED_BY_POLICY`）。
【Employee 行为】陈帆提示用户未就绪账号。
【页面/状态变化】各账号状态独立显示，不合并。
【可返回/可撤销】可处理后再发；或将该账号移出 Target。
【异常】无。
【下一步】就绪账号进入 STEP 21（Publishing）。

### STEP 21（Publishing → 真实回执回流）
【用户当前看到】账号行显示「发布中…」动画；数秒后变具体态（见 STEP 22–24）。
【用户动作】无（等待 Connector 回执）；可刷新看实时。
【立即反馈】状态随 Connector 回填即时变更（[CURIS-AUTH]`RECEIPT_FROM_CONNECTOR`）。
【系统后台】Connector 回填 Publication.status / receipt / published_url / platform_time；不伪造。
【Employee 行为】陈帆盯回执；迟到则标「回执待回」不假成功。
【页面/状态变化】行状态流动。
【可返回/可撤销】发布中不可撤（事实）。
【异常】Connector 无响应 → 标「回执待回」；超时策略由 policy 定。
【下一步】按平台返回进入 STEP 22/23/24。

### STEP 22（Published：真实 URL 在哪）
【用户当前看到】XHS·AI科技主号 行变绿「已发布 ✅」+ 可点链接「查看」；点开见真实平台 URL + 发布时间。
【用户动作】点「查看」→ 跳平台该帖；或点「查看回执」（STEP 28）。
【立即反馈】URL 可点击；驾驶舱⑥「发布结果」该账号显示「已发布 · 阅读中」。
【系统后台】Publication.status=Published，published_url 来自 Connector 回填（[CURIS-AUTH]`RECEIPT_FROM_CONNECTOR`）。
【Employee 行为】无。
【页面/状态变化】该账号状态卡固定为 Published。
【可返回/可撤销】已发布不可撤销；删帖需去平台。
【异常】URL 回填迟到 → 标「回执待回」直到到达。
【下一步】其他账号继续；最终进 STEP 25 汇总。

### STEP 23（Platform Reviewing：审核中）
【用户当前看到】抖音·主号 行显示「平台审核中 ⏳」（如抖音/公众号常需审核）；提示「平台审核中，预计数分钟~数小时」。
【用户动作】无（等待）；可稍后回来看。
【立即反馈】状态保持 Platform Reviewing；驾驶舱⑥显示「抖音·审核中」。
【系统后台】Publication.status=Platform Reviewing；平台最终回执决定 Published/Rejected。
【Employee 行为】陈帆监控；若久未回提示用户。
【页面/状态变化】状态卡不变。
【可返回/可撤销】审核中不可撤（事实未定，但已提交）。
【异常】审核超时无回执 → 标「回执待回」；不假成功。
【下一步】平台通过 → STEP 22；驳回 → STEP 24。

### STEP 24（Rejected：平台驳回 → 改后重提）
【用户当前看到】抖音·主号 行变红「已驳回 ✕」+ 原因：「疑似营销导流，违反社区规范」；按钮「改后重提 / 放弃该账号」。
【用户动作】点「改后重提」→ 回到该账号 Variant 编辑（STEP 14/17），按原因改（去导流语）→ 重新生成预览 → 确认重提。
【立即反馈】改后该账号 Publication 新建一次（新 Publication 记录，旧驳回记录保留不回滚，[CURIS-AUTH]`FACT_NOT_ROLLED_BACK`）；状态回 Publishing。
【系统后台】新 Publication（per-Account）关联修正后 Variant；原 Rejected Publication 留痕。
【Employee 行为】陈帆/李想按驳回原因改文案，确保合规。
【页面/状态变化】该账号行状态流转 Rejected→Publishing→（Published/再 Rejected）。
【可返回/可撤销】可「放弃该账号」移出，不影响其他已发布账号。
【异常】反复驳回 → 提示「多次驳回，建议换角度或放弃该账号」。
【下一步】重提成功 → STEP 22；失败 → 继续改。

### STEP 25（部分完成：某账号失败其他成功）
【用户当前看到】发布结果面板顶部总结：「部分完成 —— 成功 2 / 审核中 1 / 失败 1」。每账号独立状态卡（XHS主号 Published、XHS个人IP Published、抖音主号 Failed、Bilibili Needs Permission）。
【用户动作】用户看各卡；对 Failed 点「重试」，对 Needs Permission 点「重新授权」。
【立即反馈】面板如实分列，绝无「全部成功」覆盖（[CURIS-AUTH]`PUBLICATION_PER_ACCOUNT_TRUTH`）。
【系统后台】成功账号 Publication 已 Published 且 FACT 不动；失败/未授权账号独立处理（[CURIS-AUTH]`FACT_NOT_ROLLED_BACK`）。
【Employee 行为】陈帆分别处理失败与未授权账号。
【页面/状态变化】状态卡各自演进。
【可返回/可撤销】成功账号不可撤；失败/未授权可重试/授权。
【异常】无。
【下一步】STEP 26（Failed 重试）/ STEP 13（授权）/ STEP 24（驳回）。

### STEP 26（Failed：重试）
【用户当前看到】某账号行红「失败 ✕」+ 原因：「网络错误 / 媒体格式不支持 / 频率限制」。按钮「重试 / 改后重提 / 放弃」。
【用户动作】点「重试」→ 系统按原因重提交同 Variant；若原因需改（如格式）→ 点「改后重提」。
【立即反馈】重试 → 状态回 Publishing；成功则转 Published，失败则再回 Failed 并累计次数。
【系统后台】同一 Publication 重提交或新建重试 Publication；Connector 回填新回执（[CURIS-AUTH]`RECEIPT_FROM_CONNECTOR`）。
【Employee 行为】陈帆判断失败是否系统性（如频率限制需等冷却）。
【页面/状态变化】状态卡流转。
【可返回/可撤销】可放弃该账号，不影响其他。
【异常】连续失败超阈值 → 提示「多次失败，建议稍后或换账号」。
【下一步】成功 → STEP 22；仍失败 → 用户决定放弃或稍后。

### STEP 27（Scheduled 修改 / 撤）
【用户当前看到】某账号设了「明早 9 点」未到点，行显示「⏰ 已定时」。按钮「改时间 / 取消定时」。
【用户动作】点「改时间」→ 选新时间；或「取消定时」→ 转立即或移出。
【立即反馈】行更新时间或回 Ready。
【系统后台】Publication.scheduled_at 改/清；到点前不调 Connector；不支持定时平台本态不可用（[CURIS-AUTH]`SCHEDULING_IS_CONDITIONAL`）。
【Employee 行为】无。
【页面/状态变化】状态卡随改。
【可返回/可撤销】到点前可反复改；到点后成事实不可撤。
【异常】改到过去 → 提示无效。
【下一步】到点 → STEP 21。

### STEP 28（查看回执 / 记录在哪查）
【用户当前看到】任一账号行点「查看回执」→ Utility 打开 Publication 详情：状态 / 真实 URL / 平台返回时间 / 平台消息 / 关联 Variant。驾驶舱⑥「发布结果」汇总所有账号 Publication。
【用户动作】点 URL 跳平台；或关 Utility。
【立即反馈】详情展开，全部来自 Connector 回填（[CURIS-AUTH]`RECEIPT_FROM_CONNECTOR`）。
【系统后台】Publication Result 持久化；可历史查询每账号每次发布。
【Employee 行为】无。
【页面/状态变化】用户可回溯任意历史发布。
【可返回/可撤销】关 Utility 回面板。
【异常】回执迟到 → 详情标「回执待回」不假成功。
【下一步】进入 STEP 29 完整剧本串联，或 Journey G（数据回来）。

---

## 6. 完整一次多账号发布连续剧本（从「把这个发到小红书和抖音」）

> 串联 STEP 01–28，模拟真实连续流程，体现 per-Account 真相与异常修复。

### STEP 29（发起：「把这个发到小红书和抖音」）
【用户当前看到】用户在对话/内容 Surface 输入：「把这个发到小红书和抖音。」系统识别为发布指令，跳转发布面板（Channel 已连、账号已建，见 §1–2）。
【用户动作】发送指令。
【立即反馈】面板预展开「小红书」「抖音」两 Channel 账号树，默认勾选各自默认账号（XHS·AI科技主号、抖音·主号）。
【系统后台】组装 Target = Office Default + AI 推荐；命中已连 Channel。
【Employee 行为】陈帆按内容定位建议是否追加账号（如加 XHS·测评号）。
【页面/状态变化】发布目标树展开。
【可返回/可撤销】可改勾选。
【异常】Channel 未连 → 回 STEP 01。
【下一步】STEP 30（系统推荐 + 不匹配提示）。

### STEP 30（系统推荐账号 + 不匹配提示）
【用户当前看到】树中陈帆在 AI 推荐里额外勾选「XHS·测评号」（因内容偏实测），并灰显「XHS·个人IP号」标「定位不匹配，确认覆盖？」（STEP 11）。
【用户动作】用户接受测评号勾选；对个人IP号点「跳过」（不覆盖）。
【立即反馈】树更新：XHS 主号+测评号勾选，个人IP号未选。
【系统后台】Target 含 3 账号（XHS主号/测评号/抖音主号），个人IP号留 BLOCKED 不静默删（[CURIS-AUTH]`TARGET_NE_ELIGIBILITY`）。
【Employee 行为】陈帆记录推荐理由。
【页面/状态变化】树状态定。
【可返回/可撤销】可再勾个人IP号走覆盖。
【异常】无。
【下一步】STEP 31（多选 + 生成 Variant）。

### STEP 31（多选 + 生成 Variant，某账号需重生成）
【用户当前看到】点「生成预览」→ 三张 Variant 卡：XHS主号「轻适配」、XHS测评号「重生成」（跨调性）、抖音主号「重生成」。
【用户动作】用户看预览；对 XHS主号点「采用」，对测评号点「比稿」确认差异后「采用」，对抖音主号点「改一点」调口播。
【立即反馈】三卡均标采用；底部「发布」启用。
【系统后台】三 Publication 草稿 Ready；每 Variant 绑单账号无串号（[CURIS-AUTH]`NO_CROSS_ACCOUNT_CONTEXT_LEAK`）。
【Employee 行为】陈帆核对各档合规。
【页面/状态变化】预览态完成。
【可返回/可撤销】未发前可改任意 Variant。
【异常】某卡生成失败 → 该卡重试，其余正常。
【下一步】STEP 32（某账号未授权）。

### STEP 32（某账号未授权 → 阻断）
【用户当前看到】抖音·主号 卡标「需授权」黄条（同 STEP 13）：「授权过期，无法发布。」
【用户动作】用户点「重新授权」→ 跳抖音 OAuth → 成功回 Connected。
【立即反馈】卡转正常，可发；若用户选「先跳过该账号」则抖音移出本次 Target。
【系统后台】抖音主号 `authorization_state` 恢复（[CURIS-AUTH]`OAUTH_FAILURE_KEEPS_ACCOUNT` 反向）；Publication 解除 BLOCKED。
【Employee 行为】陈帆提示「抖音已恢复，可发」。
【页面/状态变化】抖音卡状态正常。
【可返回/可撤销】授权可逆。
【异常】授权失败 → 抖音持续 BLOCKED，本剧本改为先发 XHS 两账号。
【下一步】STEP 33（某账号掉线修复/跳过）。

### STEP 33（某账号掉线 → 修复/跳过）
【用户当前看到】生成预览时 XHS·测评号 突然标「未连接」（网络/平台侧掉线，STEP 12）。
【用户动作】用户点「去连接」重试 OAuth 成功；或点「跳过该账号」先发主号。
【立即反馈】连接成功 → 卡恢复；跳过 → 该账号移出，XHS 仅主号发。
【系统后台】连接状态来自 Connector；未连不建 Publication。
【Employee 行为】陈帆监控掉线。
【页面/状态变化】树更新。
【可返回/可撤销】连接可重。
【异常】持续掉 → 先发其余。
【下一步】STEP 34（发布确认 → per-account 状态流）。

### STEP 34（发布确认 → per-account 状态流，含部分成功/失败）
【用户当前看到】点「确认发布」→ 状态视图：XHS主号 Publishing→Published✅(URL)；XHS测评号 Publishing→Platform Reviewing⏳；抖音主号 Publishing→Failed✕（原因：频率限制）。
【用户动作】用户点抖音「重试」；等测评号审核。
【立即反馈】抖音重试→Publishing→Published✅；测评号稍后 Platform Reviewing→Published✅。顶部总结：「成功 3 / 失败 0」。
【系统后台】每 Publication 独立回填（[CURIS-AUTH]`PUBLICATION_PER_ACCOUNT_TRUTH`）；无整体成功概念，仅逐账号 truth。
【Employee 行为】陈帆处理频率限制重试成功。
【页面/状态变化】三卡最终全 Published；若中途有失败则显「部分完成」(STEP 25)。
【可返回/可撤销】已发不可撤。
【异常】若测评号驳回 → 走 STEP 24 改后重提。
【下一步】STEP 28（查回执）或 Journey G。

### STEP 35（回执归档与下次复用）
【用户当前看到】驾驶舱⑥「发布结果」列出三账号 Publication；用户点任一「查看回执」见真实 URL。
【用户动作】点 URL 复核；关闭。
【立即反馈】详情展开（Connector 回填）。
【系统后台】Publication 持久化；下次同内容发布时「最近使用账号」优先勾选（[REUSE] 主文件 §3.2）。
【Employee 行为】无。
【页面/状态变化】无新。
【可返回/可撤销】关 Utility。
【异常】无。
【下一步】Journey G（数据回来）。

---

## 7. CALENDAR（统一多 Channel/多 Account 的 Draft/Scheduled/Published/Campaign）

### STEP 36（Calendar 为什么存在 + 谁用）
【用户当前看到】在「内容」Surface 内有一个视图入口「日历」（OPEN QUESTION Z1/Z7：建议作为「内容」Surface 内视图，非独立 L1 导航；专家异议独立 L1 已记录待裁决）。打开后时间轴显示：各 Channel 各账号的 Draft（灰）/ Scheduled（蓝）/ Published（绿）/ Campaign（紫带）。
【用户动作】CEO 通常不需进；陈帆/李想主用。陈帆点某天看排期。
【立即反馈】时间轴渲染；Gap（连续空白）、Conflict（同日同账号超频/撞车）标黄/红。
【系统后台】Calendar 聚合所有 Channel/Account 的 Publication + Scheduled + Draft + Campaign（[REUSE] 主文件 §6）。
【Employee 行为】陈帆发现 Gap（如某账号 3 天没发）→ 建议补内容；发现 Conflict（如两账号同刻发同质）→ 提示差异（合规同质化红线）。
【页面/状态变化】视图随筛选（按 Channel/Account）更新。
【可返回/可撤销】关视图回内容 Surface；不改数据。
【异常】无。
【下一步】STEP 37（发现 Gap/Conflict 动作）。

### STEP 37（发现 Gap/Conflict → 动作）
【用户当前看到】Calendar 标「⚠️ Gap：抖音主号 8/20–8/22 空白」「🔴 Conflict：XHS主号与测评号 8/21 同发同质标题」。
【用户动作】陈帆点 Gap→「补一条内容」起新 Intent；点 Conflict→「差异化这俩 Variant」回 STEP 17。
【立即反馈】Gap 触发新内容建议；Conflict 提示改文案。
【系统后台】读 Publication/Scheduled 聚合计算 Gap/Conflict（不修改事实）。
【Employee 行为】陈帆在后台协调，不强制 CEO 介入。
【页面/状态变化】Calendar 标注处理中。
【可返回/可撤销】可忽略标注。
【异常】无。
【下一步】回内容创作或发布流程。

### STEP 38（Calendar 与 CEO 的关系 + OPEN QUESTION）
【用户当前看到】CEO 驾驶舱已给发布结果（per-Account），通常不需 Calendar；Calendar 作为「内容」Surface 内视图出现（[REUSE] 主文件 §6.2）。
【用户动作】CEO 可选「不看」；陈帆主用。
【立即反馈】无强制。
【系统后台】无写。
【Employee 行为】陈帆用 Calendar 做排期治理。
【页面/状态变化】无。
【可返回/可撤销】不适用。
【异常】无。
【下一步】待 CEO 裁决 OPEN QUESTION Z1/Z7（Calendar 独立 L1 vs 内容内视图）。

> **OPEN QUESTION（待 CEO 裁决）**：Calendar 应作为「内容」Surface 内视图（专家推荐，降低 L1 噪音）还是独立 L1 导航（部分专家异议，便于跨 Office 排期）？本文件不裁决，仅标注。

---

## 8. 与 FINAL ACCEPTANCE 对应（引用主文件 §13 叙事）

以下逐段对应 CEO 给定叙事，给本文件 STEP 编号，证明产品可文字操作、无「UI 阶段再决定」缺口：

- **「我连接了 3 个小红书账号、2 个抖音账号。」**
  → STEP 01–04（添加 XHS Channel）→ STEP 05–08（加 3 个 XHS 账号：AI科技主号/AI工具测评号/个人IP号，命名+采纳定位+设默认）→ 重复连 Douyin + 2 账号。共得用户示例矩阵（§2 STEP 08）。

- **「我选择 XHS 主号和抖音主号发布。」**
  → STEP 10（发布目标树，勾 XHS·AI科技主号 + 抖音·主号，默认推荐自动勾选）→ STEP 14（生成预览）。

- **「抖音账号授权过期。」**
  → STEP 13（抖音主号标「需授权」黄条阻断）/ STEP 32（剧本中未授权阻断）；账号本身 `authorization_state=Expired` 但保留（[CURIS-AUTH]`OAUTH_FAILURE_KEEPS_ACCOUNT`）。

- **「我重新授权。」**
  → STEP 13「重新授权」走平台 OAuth → 账号恢复 Connected，解除 BLOCKED；STEP 32 剧本修复。

- **「小红书发布成功，抖音进入平台审核。」**
  → STEP 22（XHS·主号 Publication=Published，真实 URL 回填）+ STEP 23（抖音·主号=Platform Reviewing）；面板显「部分完成」独立态（STEP 25），无整体成功覆盖（[CURIS-AUTH]`PUBLICATION_PER_ACCOUNT_TRUTH`）。

- **「第二天数据回来。员工告诉我哪里有效、为什么、下一步建议。」**
  → STEP 28（回执已存档可查）+ 进入 Journey G（G01 Evaluation：收藏率↑12% 因 GPT-5.6 切中搜索红利 + 建议扩抖音）；本文件不展开数据回来，仅承接回执真相。

> 全程每动作在对应 STEP 有具体按钮/反馈/后台/员工/状态变化；per-Account 真相逐账号独立，未被任何「整体成功」覆盖。✅

---

*CONTENT GROWTH MULTI-ACCOUNT PUBLISHING JOURNEY — RESEARCH / EXPERT RECOMMENDATION — STOP FOR CEO REVIEW*

本文件为**纯研究**，**未修改**任何 Frois Authority / Runtime / Schema / UI / DB；所有行为挂在既有 Channel 对象 + Module + Connector 与 Publication/Variant 契约上。请在 CEO Review 中裁决：① Calendar 层级归属（OPEN QUESTION Z1/Z7）；② 默认 distribution_execution_policy（BEST_EFFORT / ALL_REQUIRED）在 Office 级默认值；③ Unavailable 平台「手动发布」占位是否纳入首版。
