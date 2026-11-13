# CURIS PRODUCT DERIVATION METHOD V2 — VALIDATION

> Status: Draft（推导方法 V2 验证报告 · 供 CEO / ChatGPT 核对）
> Authority Class: REVIEW — 方法验证与场景推导，不修改任何 Authority / Blueprint / Navigation / UI。
> Updated: 2026-09-14 · S1–S6（第一轮 V2）+ S7（ROUND 2 P0）+ S8–S14（ROUND 2 CONTINUE：经营模型推透）· STOP FOR CEO / CHATGPT REVIEW
> 方法来源：CEO《PRODUCT DERIVATION METHOD V2》指令（2026-09-14）；两个示范（复用/复制员工、账号三上下文）已完整消化。
> 关联：CURIS_PRODUCT_CAPABILITY_DERIVATION_LEDGER.md（本轮新增能力台账）；CURIS_PRODUCT_DERIVATION_GAP_REGISTER.md（G-13 起新增，每条注明 Derived From Scenario）；CURIS_PRODUCT_DERIVATION_ROUND1_CORRECTION.md（保留，本轮末尾给出 V2 检查结论）。
> 标注：【事实】项目资料记载；【判断】本轮推导结论；【OPTION】两个合理方案并存，继续找场景区分，不强行二选一；【NOT YET JUSTIFIED】推不出来，不硬造。

---

# 0. 方法 V2 一句话与十七步速览

**一句话**：先完整模拟真实用户怎么经营，观察他在哪里遇到选择、分叉、异常和规模化困难；只有被真实场景逼出来的能力，Curis 才增加。禁止从"应该有什么对象/字段/功能"出发。

十七步：①REALITY 现实怎么经营 → ②ACTORS 谁参与 → ③OBJECTS 现实里有什么 → ④HAPPY PATH 正常怎么走 → ⑤USER CHOICES 用户还有哪些合理做法 → ⑥BRANCHES 每个选择的成功/失败/换人/共享/复制/暂停/删除/恢复/多个/规模 → ⑦CONSEQUENCES 不支持会怎样（没有真实问题就不加）→ ⑧PRODUCT CAPABILITY 才第一次说功能 → ⑨MINIMUM MODEL 最少对象（先复用现有）→ ⑩OWNERSHIP/SCOPE 真相归谁 → ⑪CONTEXTUAL PROJECTION 哪些上下文看哪些字段 → ⑫PLACEMENT 放哪+为什么 → ⑬CROSS-BUSINESS 换业务还成立吗 → ⑭SCALE 扩到 10 业务/50 员工还成立吗 → ⑮REVERSIBILITY 用户改主意怎么办 → ⑯FAILURE 真实失败怎么理解与恢复 → ⑰ONLY THEN ABSTRACT 多案例跑通才许抽象共性。

---

# S1 — Employee 跨多个 Business 复用

**STEP 1 REALITY**：现实中一个老板雇了不错的设计师，会让设计同时服务自己的几个品牌——设计师本来就在多品牌间切换：每个品牌有自己的规范、各自的对接人、各自的交付，但他是同一个人、一份履历、一份工资。
**STEP 2 ACTORS**：CEO（想要设计能力但不想要三份管理负担）；各业务 Leader（分别提需求）；林墨（设计员工）；外部工具（图像生成、Figma）；各业务的素材/规范资料。
**STEP 3 OBJECTS（现实里有什么，先不抽象）**：设计师这个人；三份"在哪干什么"的安排；三套品牌规范与素材；三类交付物（封面/立绘/主图）；一条个人技能履历。
**STEP 4 HAPPY PATH**：内容 Leader 提"下周三篇笔记要封面" → 林墨在内容业务收到 → 用内容品牌规范做图 → 交付 → Leader 验收 → 结果归内容业务。同一周电商 Leader 也提需求 → 同样的事在电商上下文再发生一遍。
**STEP 5 USER CHOICES**：
- A 复用同一个林墨（省钱、履历集中、能力复用）；
- B 不复用，要独立设计员工（怕混淆）→ 展开为 S2；
- 【OPTION】C 部分外包（电商设计找外部）→ 本轮登记，不展开；
- 怎么加入新业务：他是已有员工，动作应该是"派任/组队"，不是重新走招聘；
- 两个业务同时要他：谁优先？【OPTION】CEO 排 / Leader 间协商 / 排期规则——场景不足，不强行定。
**STEP 6 BRANCHES**：成功（正常交付）；失败（能力不够/过载）；换人（某业务换了设计员工，另一条线不变）；共享冲突（两业务同时要用——负载问题，见 STEP 7）；暂停（某业务暂停→该条线暂停）；移除（某业务不再需要→撤该条任职线）；规模（10 门生意都要设计）；反转（CEO 后来想要独立员工→S2）。
**STEP 7 CONSEQUENCES（不支持会怎样）**：不支持复用→只能复制三个林墨→身份/履历/成本×3，管理崩（问题 1.16）；不支持按业务隔离上下文→电商图里混进小说世界观；对话不分线→谈封面时混着主图历史；结果不归属→"这张封面是给谁做的"说不清；**没有负载表达→三个 Leader 都往他身上压需求，没人知道他过载**（新发现的后果，见 G-13）。
**STEP 8 PRODUCT CAPABILITY（第一次允许说功能）**：「把员工派到另一门生意任职」（Reuse Employee）；「查看他在每门生意负责什么」（任职列表）；「和他在某门生意的对话」；「看到他的负载是否排满」（新）。
**STEP 9 MINIMUM MODEL**：复用现有 Employee Identity + Assignment（任职）+ Responsibility + Business Context + 按范围对话 + Work/Result——**无需新对象**；"负载/容量"的承载方式【OPTION】（任职线状态聚合 vs 新容量概念）——场景已逼出需求，形态未定，登记 G-13。
**STEP 10 OWNERSHIP/SCOPE**：Identity→Company；任职线→Business 范围；Work/Result→Business；对话线→任职范围。
**STEP 11 CONTEXTUAL PROJECTION**：业务团队视图（这条线：名+岗位+责任+状态）；Employee Detail（多线列表）；Quick Access（谁+哪门生意+是否需要我）；Search（一人多线）；Notification（业务+责任+员工三段）。
**STEP 12 PLACEMENT**：派任动作在"组织关系处/业务团队"（Add Where You Work）；任职列表在员工详情；对话线入口在对话区；负载在员工行。
**STEP 13 CROSS-BUSINESS**：研发（一个架构师服务两个产品业务）✓；电商（一个客服员工服务两个店铺业务）✓ → **CROSS-BUSINESS VALIDATED**。
**STEP 14 SCALE**：10 业务/50 员工/80 条任职线 → 必须双向可查：按人（员工目录：他在哪几门生意）与按线（业务团队：这条线上有谁）；只有业务视图时 CEO 无法盘点"我的设计师都有谁"——信息需求登记。
**STEP 15 REVERSIBILITY**：撤某条任职线→该线历史 Work/Result 保留、未来不再派活；加回来→历史还在。可逆 ✓。
**STEP 16 FAILURE**：他过载/阻塞→各条线显示"阻塞·原因"，身份不坏；某条线的 Provider 挂→只影响那条线的执行——**Identity / Connection / Execution 三分离**在此验证。
**STEP 17 ABSTRACT**：经 S1（并与 S2 对照）→"Employee Identity 与组织/经营关系分离"进 **Company OS Core**。

---

# S2 — CEO 不想复用，基于现有员工创建相似新员工

**STEP 1 REALITY**：老板说"这设计师很好，但小说业务我想要个专职的，别总被内容业务打断"——现实中是"照他再招一个"，新人是新的人：履历从零开始，但带着一份"入职配置"（师傅会什么、用什么工具、什么习惯）。
**STEP 2 ACTORS**：CEO（决策）；林墨（能力模板来源）；林溪（新员工）；小说 Leader（未来需求方）。
**STEP 3 OBJECTS**：一份能力配置（会什么/用什么工具/模型偏好/专业方法）；一个新身份（名字/头像）；一批**绝不能带走**的东西（对话史/工作记录/结果/任职/业务记忆/账号权限）。
**STEP 4 HAPPY PATH**：CEO 在林墨详情选「创建相似员工」→ 系统出示**复制预览**（将复制什么/不会复制什么）→ CEO 命名"林溪"→ 新员工创建、能力与林墨当前配置相同 → CEO 把林溪派到小说业务任职 → 林溪开始干活，履历从零积累。
**STEP 5 USER CHOICES**：
- 复用（S1）vs 复制（本场景）——两个都合理的真实选择，正是用户分叉点；
- 复制来源：【OPTION】从现有员工复制 vs 从专家模板创建（招募时的岗位能力包）——两个入口，机制可能同源（能力配置快照），继续找场景区分，不合并结论；
- 复制范围：全部能力 vs 子集（只要排版不要视频）；
- 【OPTION】是否记录"来自林墨"的师承关联——无真实需求证明前不加（纪律：没有真实问题就不加）。
**STEP 6 BRANCHES**：创建成功；创建后能力依赖的 Provider 未连接（林溪有能力但暂不可执行——诚实显示）；此后两人能力各自演进（分叉）；CEO 反悔想删林溪（无工作记录→可删；有记录→走离职式处理，历史保留）；CEO 后来想把林墨新学的方法也给林溪（能力差分同步——【OPTION】登记观察 G-15）；从一个专家模板一次创建整个团队（开业场景，登记为能力 CAP-010 关联 S20）。
**STEP 7 CONSEQUENCES**：没有「创建相似员工」→ CEO 手工重配一个新员工（模型/技能/工具逐项配）→ 又麻烦又容易漏；没有复制预览→用户害怕"会不会把聊天记录也复制走"→不敢用；没有排除历史→出现两个"林墨"，身份污染。
**STEP 8 PRODUCT CAPABILITY**：「创建相似员工」（含复制预览）；「给员工增配/调整能力」（把某技能/工具配给某员工，与 S3/S4 的 Binding 同源）。
**STEP 9 MINIMUM MODEL**：Employee 创建 + **Capability Snapshot**（复制时点的能力配置清单，新提出的支撑概念）+ 排除清单（Identity/Conversation/Work/Result/Assignment/Business Memory/Account Permission/Decision History——即"林墨的人生"）。快照形态【OPTION】（独立对象 vs 创建时一次性读取）——登记 G-14。
**STEP 10 OWNERSHIP/SCOPE**：新 Identity→Company；能力配置→员工（人级）；排除项→各自原归属不变。
**STEP 11 CONTEXTUAL PROJECTION**：创建时的复制预览（两列：将复制/不会复制）；创建后的新员工详情（履历空、能力满、无任职）。
**STEP 12 PLACEMENT**：入口两处——员工详情（从现有员工创建）与人才与能力（从专家模板创建）；预览是确认步骤。
**STEP 13 CROSS-BUSINESS**：研发（照着后端工程师再配一个）✓；电商（照着店铺运营再配一个）✓ → **VALIDATED**。
**STEP 14 SCALE**：开业时从模板一次建 5 人团队→需要"批量创建+分别命名+分别派任"；不支持的后果：开业流程退化成 5 次手动建档。
**STEP 15 REVERSIBILITY**：创建后可继续编辑能力；无工作记录可删除；有记录走离职保留历史；【OPTION】能力差分同步给"改主意"留门（G-15）。
**STEP 16 FAILURE**：复制的能力依赖未连接的 Provider→新员工如实显示"具备能力、暂不可执行"；复制中断→不产生半成品员工。
**STEP 17 ABSTRACT**：**复制能力 ≠ 复制身份/历史** → Company OS Core 原则（经 S2 并与 S1 对照验证）。

---

# S3 — 员工缺 Coding 能力，用户手里有 API Provider

**STEP 1 REALITY**：公司要一个会写代码的人。老板手里有 OpenAI 的 API Key。他不会问"要不要支持 MCP"——他会想"我有 GPT 的钥匙，能不能让我的员工用上"。
**STEP 2 ACTORS**：CEO（拿钥匙的人）；开发员工（需要能力的人）；OpenAI（能力供给方）；Curis（编排者）。
**STEP 3 OBJECTS**：API Key（凭证）；可用模型清单；员工；一个编码任务。
**STEP 4 HAPPY PATH**：CEO 到设置里连接 Provider（贴 Key）→ 测试连接 → 发现可用模型 → 设默认/可选 → 给开发员工配"可用这些模型" → 员工接活时用模型干活 → 用量记账。
**STEP 5 USER CHOICES**：什么时候配（事前配好 vs 干活时缺能力提示再配——两条路径都要通）；给谁用（全员 vs 指定员工——成本考量）；用哪个模型（默认 vs 每次选 vs 按任务定）；额度用尽怎么办。
**STEP 6 BRANCHES**：Key 错误/网络失败；模型下线；配额用尽；换 Provider（OpenAI→DeepSeek）；多 Provider 共存（谁是默认）；Key 安全（凭证不入库——【事实】现行 Keychain 约束）。
**STEP 7 CONSEQUENCES**：不能接 Provider→员工永远"不会"写代码，Curis 空转；不区分授权→所有员工烧最贵模型，成本失控（问题 1.15）；不显示健康→用户误判"员工坏了"（其实是 Provider 挂了）。
**STEP 8 PRODUCT CAPABILITY**：「连接模型提供方」（含测试与发现模型）；「把模型能力配给员工」；「干活时选择用哪个模型」；「看模型花了多少钱」。
**STEP 9 MINIMUM MODEL**：**全部复用现有**——Provider 登记/测试/发现/设默认【事实：ModelManagement 已实现】+ 员工能力绑定【事实：已实现】+ 用量账【事实：已有】。V2 结论：此场景**不需要新对象**，是对现有模型的真实场景验证。
**STEP 10 OWNERSHIP/SCOPE**：Provider/Key→Company（INFRA）；绑定→员工或范围；用量→员工×Work。
**STEP 11 CONTEXTUAL PROJECTION**：Settings（连接+健康）；员工能力区（能用什么）；Work 执行记录（这次用了什么模型）。
**STEP 12 PLACEMENT**：连接在 Settings；绑定在员工；使用在 Work；记账进总账（Capability Lifecycle 各步归位）。
**STEP 13 CROSS-BUSINESS**：内容（写作模型）✓；电商（文案模型）✓ → **VALIDATED**。
**STEP 14 SCALE**：50 员工共用 2 个 Provider→"默认模型+例外"就够，不需要逐员工配置；用量按人分账回答"谁烧的钱"。
**STEP 15 REVERSIBILITY**：解绑、换默认、撤销 Key——员工身份与履历不变。
**STEP 16 FAILURE**：Provider 挂→标准失败行为：「该 Provider 不可用 → 员工仍在 → 可切换其他能力来源」（CEO 指令 27 的验证点）。
**STEP 17 ABSTRACT**：Provider 是能力供给者、身份与执行分离 → Core（经 S3+S4 双验证）。

---

# S4 — 员工缺 Coding 能力，用户没有 API，只有 Codex / Zcode 等外部 Agent

**STEP 1 REALITY**：老板没买 API，但订阅了 Codex（或装了 Zcode / Claude Code）。他想的是"我订阅的这个 AI 很能干，能不能让它替我的员工干活"。这是大量真实用户的付费现状——**订阅制执行者，不是钥匙**。
**STEP 2 ACTORS**：CEO（订阅者）；开发员工（Curis 里的责任人）；Codex（外部执行者）；GitHub（Codex 操作的对象）；Zcode/Claude Code（备选执行者）。
**STEP 3 OBJECTS**：一份订阅/账号；"Codex"这个执行者；它能干的事（编码）；它自带的工作环境（云端沙箱/本机）；它能用的工具（repo/terminal）。
**STEP 4 HAPPY PATH**：CEO 在设置里连接 Codex（登录/授权）→ 健康检查通过 → 给开发员工授权"可用 Codex 执行" → 员工接到开发任务 → 委托 Codex 执行 → 执行记录写明"由 Codex 执行" → 产出代码 → Result 归员工责任，Evidence 记录真实执行者。
**STEP 5 USER CHOICES**：同一能力两个来源——用 Codex 还是用 API 模型（执行选择）；一个员工同时配 Codex+Zcode（谁来干？按任务选/默认/对比后选用）；不同外部 Agent 分工（开发=Codex、Review=Claude Code、视觉检查=Browser Agent）；【OPTION】对比模式：两个执行者各做一版挑好的——真实需求存在（重要变更），保留为合法形态。
**STEP 6 BRANCHES**：订阅到期/失效；Codex 超时或失败（换 Zcode 重试或换 API 模型）；执行环境不可用；授权被收回；并行执行与选用；员工换人（接任者的授权）。
**STEP 7 CONSEQUENCES**：只支持 API→订阅制用户整体被挡在门外（ Curis 变成"必须先买 API 才能用"的产品）；没有执行归因→"这句代码谁写的"说不清，出事无法追责；没有失败切换→一次订阅到期整个研发停摆。
**STEP 8 PRODUCT CAPABILITY**：「连接外部 Agent」；「授权员工使用某外部 Agent」；「本次工作用哪个执行者」（执行选择含 Agent 选项）；「查看谁实际执行了」（执行审计）；「换一个执行者重试」。
**STEP 9 MINIMUM MODEL**：Round 1 C-06 的五层（Capability / Provider(Model|AgentRuntime) / Agent Runtime / Execution Environment / Tool Access）+ Registry + Binding + Health + Usage + Execution 归因记录。V2 验证：本场景需要的**正好**是这套，不需要更多——每层都能指着场景里的一个真实东西：订阅=Registry 项、Codex=Runtime Provider、沙箱/本机=Execution Environment、repo/terminal=Tool Access、授权=Binding、用量=Usage、谁干的=Execution 归因。
**STEP 10 OWNERSHIP/SCOPE**：Provider 登记→Company INFRA；授权→员工；执行记录→Work。
**STEP 11 CONTEXTUAL PROJECTION**：Settings（连接/健康/订阅状态）；员工能力行（能用哪些执行者）；Work 执行详情（谁干的）；失败提示（"Provider 不可用"≠"员工坏了"）。
**STEP 12 PLACEMENT**：连接在 Settings；授权在员工；使用在 Work；失败切换在执行现场。
**STEP 13 CROSS-BUSINESS**：研发（Codex 强需求）✓；内容（Browser Agent 做竞品观察/发布兜底）✓；电商/小说（弱需求，如实标 △）→ **VALIDATED（两业务强/中）**。
**STEP 14 SCALE**：多员工共用一个 Codex 订阅→并发与配额是真实约束，产品必须诚实显示"排队/受限"，不能伪装无限用——登记 G-18。
**STEP 15 REVERSIBILITY**：解绑 Agent、换 Provider、收回授权——员工身份/履历/责任不变。
**STEP 16 FAILURE**：Codex 不可用→「该执行提供者不可用 → 员工仍在 → 可切换 Zcode 或 API 模型」；这与"员工坏了"是两种完全不同的用户感知——Identity/Connection/Execution 分离的关键验证点。
**STEP 17 ABSTRACT**：Agent Runtime 与 Model Provider 同为 Provider 但**不同物种**（谁持有执行生命周期与工具）；执行归因必须记录 → Core。

---

# S5 — 内容发布到多个 Platform / Account（从"已审核完成"开始）

**STEP 1 REALITY**：内容做完了。运营要把内容发出去：挑账号→按平台要求适配→（有的要老板点头）→定时或立即发→**确认真的发出去了**（拿到链接）→过几天看数据。真实世界全是坑：平台没 API、授权过期、账号被封、发一半失败、平台改规则。
**STEP 2 ACTORS**：发布员工/内容 Leader（执行）；CEO（政策与高风险拍板）；平台（规则方，不受控）；账号（经营身份）；Curis（执行与记录者）。
**STEP 3 OBJECTS**：内容成品；按账号适配的版本；平台；自有账号；连接（授权通道）；发布计划；发布记录；回执；回流数据。
**STEP 4 HAPPY PATH**：已审核内容 → 选目标账号（可多选）→ 每个账号用对应适配版 → 按平台规则校验 → 定时/立即 → 经连接发布 → 拿回执（链接/编号/时间）→ 状态"已发布" → 数据回流。
**STEP 5 USER CHOICES（本场景是分叉最密的）**：立即 vs 定时；自动发 vs 人工确认（政策——Round 1 C-12 三档）；发一个账号 vs 全部矩阵；平台无 API 时【OPTION】浏览器自动化 vs 人工代发（都合法，如实标注）；CEO 逐条批 vs 按政策免批；失败后自动重试 vs 人工重试。
**STEP 6 BRANCHES（不止 Happy Path）**：
- **部分成功**：3 个账号成 1 个败→必须逐账号记状态，不能"一锅端"显示失败；
- **授权过期**：发布前检查失败→引导重连，账号与历史**不消失**【事实：OAUTH_FAILURE_KEEPS_ACCOUNT】；
- **平台规则变化**：适配校验不过→提示"规则已变，需要调整"（规则必须带来源与新鲜度，Round 1 C-14）；
- **账号被封**：该账号暂停发布，其他账号不受影响；
- **员工换人**：原发布员工离任→授权随责任交接或重新授予；
- **撤回**：已发出去的无法真撤——"删除"是平台上的**另一个对外动作**（新发现，G-16）；
- **批量**：一次发 10 个账号→风险升档（C-12）。
**STEP 7 CONSEQUENCES**：没有回执→"到底发没发出去"永远说不清，经营建立在猜测上；没有逐账号状态→一次失败全部重来；没有授权过期处理→业务静默中断；每条都让 CEO 批→CEO 变审批机器人（违背"日均动作<3"）；没有撤回语义→用户以为"删除=没发生过"（危险误解）。
**STEP 8 PRODUCT CAPABILITY**：「发布到账号」；「排期发布」；「为多账号生成适配版」；「重连账号授权」；「按政策自动发布/需确认」；「逐账号查看发布状态与回执」；「对已发布内容执行平台删除（作为新的对外动作）」。
**STEP 9 MINIMUM MODEL**：Platform / Owned Account / Connection（授权方式×协议两层，C-15）/ Action Grant（C-16 语义）/ Risk Policy（C-12）/ **Publication 逐账号记录**（【事实】现行 PUBLICATION_PER_ACCOUNT_TRUTH 一致）/ Receipt / Metrics。V2 新增确认：部分成功要求逐账号记录——与现行权威一致，验证而非新增。
**STEP 10 OWNERSHIP/SCOPE**：对象身份公司层、经营绑定业务层（C-13）；Publication/数据→业务；Connection→INFRA。
**STEP 11 CONTEXTUAL PROJECTION**：业务现场（发布队列/日历：将发/已发/失败+原因）；Settings（连接健康、授权方式）；员工授权（谁能发哪个账号）。
**STEP 12 PLACEMENT**：发布动作在业务现场；重连入口从失败提示直达 Settings（失败→恢复闭环）；政策设置在业务。
**STEP 13 CROSS-BUSINESS**：电商上架（店铺×商品 Listing×回执×数据）✓；研发 Deploy（环境×Release×回执）✓；小说连载（平台×章节）✓ → 对外动作骨架 **VALIDATED（四业务）**；专业语言各自保留（Publication/Listing/Deployment/Chapter Release）。
**STEP 14 SCALE**：10 账号×每天 3 条→发布队列必须按账号/状态聚合，CEO 只看异常；自动发布政策让 CEO 不逐条批——否则每天 30 条审批直接压垮注意力。
**STEP 15 REVERSIBILITY**：未发的可撤计划；已发的不可回滚（对外事实），只能"再发一条更正"；授权可重连；政策可改。
**STEP 16 FAILURE（逐类）**：授权过期（重连入口）；平台审核驳回（原因+修改后重发）；接口失败（重试/换通道）；规则不符（适配修正）；账号被封（该账号暂停）；平台宕机（等待重试）——用户始终能看到"哪一步、为什么、能做什么"。
**STEP 17 ABSTRACT**：对外动作骨架+逐目标记录+风险分档 → Core；Publication/Listing/Deployment 等专业词留在各业务（防过度抽象，CEO 指令 30）。

---

# S6 — 同一个外部对象在三个上下文出现

**STEP 1 REALITY**：同一个东西（比如小红书账号），老板在不同时刻关心完全不同的事：经营它时关心定位与数据；连不上时关心"怎么重新授权"；派活时关心"谁能用它发内容"。三个问题都是真的，但问的对象面不同。
**STEP 2 ACTORS**：CEO；员工（使用者）；平台（规则方）。
**STEP 3 OBJECTS**：账号——**同一个真相**，不是三个东西。
**STEP 4 HAPPY PATH（按三个上下文分别走）**：经营——看账号定位/发布史/数据，决定下月策略；连接——授权过期，进入重连，凭证状态更新；授权——新员工到岗，给他发布权、收走离职员工的权。
**STEP 5 USER CHOICES**：第一反应是"放 Settings"（因为要授权）；但经营信息（定位/受众/策略/数据）显然属于业务现场——用户自己就会在两个地方找它。
**STEP 6 BRANCHES**：经营侧（换策略/换负责人）；连接侧（换授权方式/换协议）；授权侧（授权/收权/到期）——三个上下文各自的分支互不干扰。
**STEP 7 CONSEQUENCES**：若做成三份数据（业务一份账号、Settings 一份、权限一份）→ 改一处别处不同步，是数据灾难；只放 Settings→经营信息埋没在配置堆里；只放业务→凭证细节泄漏到经营现场。
**STEP 8 PRODUCT CAPABILITY**：「从任何上下文看到它该看的那一面」；「从失败提示直达重连」。
**STEP 9 MINIMUM MODEL**：ONE TRUTH（公司层身份 + 经营绑定，C-13）+ CONTEXTUAL PROJECTION（投影不是数据副本）。
**STEP 10 OWNERSHIP/SCOPE**：真相在公司层（+业务经营绑定）；投影无所有权。
**STEP 11 CONTEXTUAL PROJECTION**：即本场景——业务=怎么经营（定位/受众/策略/发布史/数据）；Settings=怎么连接（授权方式/凭证状态/权限范围/最近同步）；员工=谁能做什么（账号名+动作权）。
**STEP 12 PLACEMENT**：三个入口各取所需；入口之间可跳（失败提示→Settings；授权行→员工）。
**STEP 13 CROSS-BUSINESS**：小红书账号（内容）✓；GitHub Repo（研发：经营=代码/PR；连接=GitHub OAuth；授权=开发读写/审核只读）✓；Shopify Store（电商：经营=商品/订单；连接=Shopify 授权；授权=运营改商品/财务读订单）✓ → **VALIDATED（三业务）**。
**STEP 14 SCALE**：50 个外部对象→全局搜索+从上下文直达；不需要"对象中心"大页。
**STEP 15 REVERSIBILITY**：转移经营绑定（业务关闭→对象回收不失家，C-13）；换授权方式；收权。
**STEP 16 FAILURE**：授权过期在三个上下文的一致表达——Settings 显示失效详情；业务显示"发布不可用"；员工显示"无权动作"。同一个事实，三种用户语言。
**STEP 17 ABSTRACT**：**ONE TRUTH — MULTIPLE CONTEXTUAL PROJECTIONS** → Company OS Core 原则（三业务验证）。

---

# CROSS-SCENARIO FINDINGS（S1–S6 跑完后才允许的总结）

## A. 已验证的 Company OS Core（每条注明验证场景）
| 共性 | 验证场景 |
|---|---|
| Employee Identity 与组织/经营关系分离 | S1、S2（对照） |
| Assignment（任职）与 Grant（授权）是两条记录 | S1、S3、S5 |
| Result ∈ Work ∈ Business；责任产出者+执行归因 | S1、S4、S5 |
| Evidence（用户层）与 Execution Audit（技术层）分层 | S3、S4、S5 |
| Capability Lifecycle（获得≠接入≠授权≠绑定≠使用≠记账） | S3、S4 |
| Provider 双类型：Model Provider vs Agent Runtime Provider | S3、S4（对照） |
| Identity / Connection / Execution 三分离的失败语义 | S1、S3、S4、S5 |
| 对外动作骨架（Intent→Action→Target→Execution→Receipt→State→Metrics）+ 逐目标记录 | S5（四业务复验） |
| ONE TRUTH — MULTIPLE CONTEXTUAL PROJECTIONS | S6（三业务） |
| 复制能力 ≠ 复制身份/历史 | S2（与 S1 对照） |
| 可逆性原则（任职可撤、绑定可解、授权可收、计划可撤、已发不可回滚） | S1、S2、S3、S5 |

## B. 已验证的 Business Professional Model（只属于特定业务）
- 内容：账号经营属性（定位/受众/策略）、Variant 按账号适配、Publication 逐账号、发布日历（S5/S6）；
- 研发：Repo/PR/Deploy/环境（S4/S6）；
- 电商：Store/Product/Order/Listing（S6）；
- 通用骨架的专业语言必须保留（Publication/Listing/Deployment/Chapter Release），**用户永远不看到"External Action"这个词**（防过度抽象）。

## C. 已验证的 Infrastructure / Provider Model
- 两类 Provider：Model Provider（只供大脑）与 Agent Runtime Provider（自带大脑+工具+环境+生命周期）；
- Connection = 一种授权方式（OAuth/API Key/本地会话/人工）× 一种或多种协议（MCP/REST/本地桥/连接器）；
- Registry / Binding / Health / Usage / Execution 归因五个部件缺一不可（S3/S4 逐一对上真实物）；
- Execution Environment 与 Tool Access 是 Agent Runtime Provider 的**属性**，Curis 不重建。

## D. 本轮新推出的 Product Capability（用户语言；详见 Ledger）
Reuse Employee（S1）；Create Similar Employee + 复制预览（S2）；连接模型提供方/绑定员工（S3，现行已具备，V2 场景确认）；连接外部 Agent/授权/换执行者重试（S4）；发布到账号/排期/多账号适配/重连授权/按政策自动发布/逐账号状态/平台删除作为新对外动作（S5）；跨上下文查看同一对象（S6）；授予/收回动作权限（S1/S5）；转移外部对象经营绑定（S5/S6）。

## E. 现有模型被证明不足的地方（不因 Authority 绕开）
1. **员工过载不可见**（S1）：三个 Leader 都能往同一员工压需求，没人知道他过载 → G-13；（ROUND 2 修正：G-13 已由"负载/容量"重构为 **AI EMPLOYEE RESOURCE / CONTENTION**——过载机制是 Provider 并发/Token 成本/Context 冲突/工具与账号排他/Agent 配额/优先级仲裁/审核瓶颈，NOT YET FINAL）；
2. **能力配置快照未定义**（S2）：「创建相似员工」需要"复制什么"的时点清单，现有模型无此支撑概念 → G-14；
3. **能力差分同步不存在**（S2 分支）：林墨后来学的新方法无法给林溪 →【OPTION】真实场景成立但频度未知 → G-15；
4. **"删除已发布内容"没有对外动作语义**（S5）：用户会误以为删除=没发生过 → G-16；
5. **发布队列的聚合信息需求**（S5 规模）：10 账号×3 条/天必须按账号/状态聚合 → G-17（信息需求，不做 UI）；
6. **共享 Agent 订阅的并发/配额诚实表达**（S4 规模）→ G-18。

## Round 1 Correction 的 V2 检查（CEO 指令 36）
用 S1–S6 对 Round 1 Correction C-01~C-18 逐一回测：C-02（Assignment/Grant 分离）被 S1/S3/S5 再次验证；C-04（快捷区三层信息模型）被 S1 再验证；C-06（Provider 分层）被 S4 完整验证；C-08（Result 归属）被 S1/S4/S5 验证；C-12（风险分档）被 S5 验证；C-13（Model B）被 S5/S6 验证；C-15（授权方式×协议）被 S5 验证。**未发现需要推翻的结论 → 本轮无 V2 SUPERSESSION CANDIDATE；Round 1 Correction 维持，等待你验收。**

---

# CEO 问题 43.1–43.10 回答

**43.1 为什么"复用员工"和"创建相似员工"是两个不同产品能力？**
因为它们是同一步的两个真实用户选择（S1/S2）：复用=建立新的组织/经营关系（同一个人，多一条任职线，履历/成本集中）；复制=创建新的身份（新的人，能力相同，人生从零）。选择动机相反（省钱 vs 怕混淆）、后果不同（目录一人 vs 两人）、可逆路径不同（撤任职线 vs 离职处理）。合并成一个功能会丢掉其中一个真实选择。

**43.2 为什么员工能力、任职关系、权限不能混成一层？**
因为它们的变更频率、归属和语义都不同：能力清单跟人（"会不会"）、任职跟业务（"为谁干什么"）、权限跟资源（"被允许用什么"）。混层的直接后果（S1/S3/S5）：新增一个账号就要改任职记录；换业务任职会误删能力；无法回答"责任缺授权"这种执行准备问题。三条记录各自可逆、各自可审计。

**43.3 为什么必须支持 Codex/Zcode 等外部 Agent，不能只有 API Model？**
因为真实用户的付费现状是订阅制执行者（S4）：没有 API Key 的用户占很大比例，只有 API 意味着把这群人挡在门外；且外部 Agent 自带工具与执行环境（repo/terminal/沙箱），是"可被委托的执行者"，与"只供大脑的模型"是不同物种——混用会导致工具与环境建模错误。

**43.4 为什么 Talent、Settings、Employee 三处都出现能力相关内容，但职责不同？**
因为用户在三个时刻管理三件不同的事（Capability Lifecycle，C-10）：想获得新能力时→Talent（发现/招募/安装）；要让能力技术上可用时→Settings（连接/授权方式/健康）；要决定"谁被允许用"时→Employee（绑定/授权）。同一能力、三个生命周期阶段、三个入口。

**43.5 为什么同一个 Account 会同时出现在 Business、Settings 和 Employee Permission 中？**
因为经营它、连接它、授权人用它，是三个真实时刻的三个真实问题（S6）：怎么经营（业务现场）、怎么连接（Settings）、谁能用（员工授权）。用户自己就会在这三个地方找同一个东西。

**43.6 为什么这不是三份数据？**
因为三处显示的是**同一个真相的三个投影**（ONE TRUTH—MULTIPLE CONTEXTUAL PROJECTIONS）：账号的定位/数据/授权状态/动作权都是一份事实的不同侧面；做成三份数据必然不同步（S6 STEP 7 的数据灾难）。投影按"用户此刻在管理什么"裁剪字段。

**43.7 哪些第一轮已有模型经 V2 后仍然成立？**
见 CROSS-SCENARIO FINDINGS A 表的 11 条共性——全部经 S1–S6 再验证成立，含 Round 1 Correction 的 C-02/04/06/08/12/13/15。

**43.8 哪些第一轮结论被 V2 证明过早或错误？**
没有需要推翻的（无 V2 SUPERSESSION CANDIDATE）。但 V2 **新发现**了第一轮漏掉的真实需求：员工负载表达（S1）、能力配置快照（S2）、差分同步（S2）、平台删除的对外动作语义（S5）、发布队列聚合（S5）、共享订阅并发表达（S4）——这些是"第一轮推导停得太早"的地方，已登记 G-13~G-18。

**43.9 本轮新推出了哪些用户可理解的 Product Capability？**
见 FINDINGS D 的 14 项，全部用用户动作语言（Reuse Employee / Create Similar Employee / Connect External Agent / Reconnect Account / Grant Action Permission / Publish to Accounts / Switch Executor / Transfer External Object / Set Action Policy 等），逐条登记在 Ledger。

**43.10 这些 Capability 分别由什么真实业务场景推出？**
每条 Ledger 记录"Derived From Scenario"：CAP-001←S1；CAP-002←S2；CAP-003←S3；CAP-004/008←S4；CAP-005←S1+S5；CAP-006/007/009←S5；CAP-010←S5；CAP-011←S6。

---

# 方法自检：现场推导一个全新场景（完成标准演练，CEO 指令 44）

场景：「我有两个电商业务，都想让同一个运营员工管理，但我不想让两个 Store 的数据互相串。」

**REALITY**：现实里一个人代运营两家店很常见——两套商品/订单/广告，互不串数据，但要能切换。**ACTORS**：CEO、运营员工、两个 Store（Shopify）、各自的数据。**OBJECTS**：一个员工、两个店铺对象、两套订单/商品数据、两条授权。**CHOICES**：复用（两条任职线）vs 复制两个员工（本 CEO 明确选复用+隔离）；授权方式（每条线只授对应 Store）。**BRANCHES**：一个店授权过期→另一个店不受影响；换人→交接两条线之一；某店关闭→撤该线+撤该店授权，对象回收不失家。**CONSEQUENCES（不支持隔离）**：订单/商品数据互相串→分析错乱、发错店、权限混乱。**CAPABILITY**：派任（复用）+ 按线授权（Grant 挂对象）+ 按对象隔离上下文。**MINIMUM MODEL**：现有模型即可——任职线（S1）× Grant 按对象（S5/S6）× Operating Binding 按 Store（C-13）——**无需新对象**。**SCOPE**：Grant/数据按 Store 对象隔离；任职线挂各业务。**PROJECTION**：业务 A 现场只见 Store A 数据；员工详情两行任职；Settings 两条连接。**PLACEMENT**：派任在组织/团队；授权在员工；连接在 Settings。**CROSS-BUSINESS**：内容矩阵（一个运营员工管多账号、数据不串）✓ 同构。**SCALE**：5 店→5 条任职线+5 个 Grant，列表仍清晰。**FAILURE**：A 店授权过期→A 店显示"待重连"，B 店正常。**结论**：现有模型（S1+S5+S6 的组合）已能表达此场景，无需新概念——**方法 V2 可用，模型经受住现场新场景**。

---

---

# SECOND ROUND P0 — S7 BUSINESS OPERATING LOOP

> 场景（CEO 指令）：**CEO 连续三天没有打开 Content Growth。第四天回来时，为什么这门 Business 应该仍然已经向前推进？** 严格按 Method V2 十七步推导；不得以现有 Authority 为前提——但推导允许得出的结论之一是"现有某合同恰好回答了此场景"（如实标注）。

**STEP 1 REALITY**：现实对照——一家小店的老板出差三天。有店长：店照常开门、按每周计划上新、客人问题按老规矩处理、缺货自动补；只有大额折扣、供应商出问题才打电话。没店长：店三天没开门。所以"业务能不能自己往前走"取决于三件事：①有没有一个对经营负责的人（店长）；②有没有事先画好的圈（什么能自己定）；③有没有不需要老板点火的推进动力（节奏/排班/上游结果触发下一步）。**关键观察：老板不在场时，在场的不是老板本人，而是他的规则和授权。**
**STEP 2 ACTORS**：Business Leader（店长——经营责任人）；Employees（执行）；CEO（画圈者+接电话者）；外部平台/客户/供应商（信号与结果来源）；其他业务的 Leader（资源竞争者）。
**STEP 3 OBJECTS（现实里有什么）**：目标与"做成什么样算成功"；经营节奏与排期；进行中的工作与下一步；结果与证据；异常与阻塞；授权边界（政策/圈）；信号（数据变化/失败/周期到达）；学习记录；预算与资源。
**STEP 4 HAPPY PATH（三天逐日）**：
- Day 1：节奏到达（周三该发内容）→ 已审核库存有稿 → 政策允许自动发布 → 发到 3 个账号 → 回执正常 → 数据回流。
- Day 2：复盘点到达 → Leader 看上周数据：A 类标题效果好 → **在授权圈内**调整下周选题方向（Learning→Strategy Adjustment）→ 生成新 Work 派给文案员工（Employee Assignment）。
- Day 3：一篇商业化内容触发"需 CEO 确认"政策 → 挂起等待（不擅自发）；两篇普通内容照常走完审核与发布。
- Day 4：CEO 打开 → 看到**缺席期间摘要**：发生了什么 / 什么需要我（1 条待确认）/ 什么已自行恢复 / 什么升级了。
**STEP 5 USER CHOICES**：授权分档：全托管 / 关键动作确认 / 只看报告（CEO 选，落到政策）；Leader 的圈：打法调整在圈内，Goal/定位/预算/重大对外承诺出圈（CEO 画）；节奏谁定：Leader 拟定 CEO 确认【OPTION】vs CEO 直接定（场景不足，不强行定）；异常处理分档：自动重试 N 次→换通道→上报；CEO 回来看什么：缺席摘要 vs 逐现场巡查（必须摘要，否则巡查复辟）。
**STEP 6 BRANCHES**：节奏到了但内容库存空（blocked → Leader 决定：催生产/改排期/上报）；发布失败（自动重试→换通道→上报）；数据大跌（信号 → Leader 分析 → 圈内调整 or 上报定位问题）；员工阻塞（重派/换执行者——Execution 层失败语义）；**资源冲突**（两个业务抢同一员工/同一账号时段 → Priority 仲裁，连 G-13）；CEO 三天中远程插入（批准一条决策——Decision Gate 不因缺席失效）；重大异常（账号被封 → 直接升级）；连续失败（自动降速/暂停节奏并升级——不无限烧钱）。
**STEP 7 CONSEQUENCES**：无 Leader 自主产生 Work → CEO 一走业务就停（问题 1.8 的业务级形态）→ 一人多业务不成立；无成功定义 → Leader 无从判断好坏、该不该调 → 一切等老板；无节奏/信号 → 工作只能等人派 → 用户当项目经理复辟；无授权边界 → 事事上报（机器人）或放任（出事）；无缺席摘要 → CEO 回来逐个巡查 50 个现场；无 Learning→调整→下一轮 → 业务会"动"但不会"变好"（1.9）。
**STEP 8 PRODUCT CAPABILITY**：「给业务定目标与成功定义」「定经营节奏」「给 Leader 画授权圈」「业务自己排工作并派工」「结果自动触发下一步」「信号与告警」「异常自动恢复与分档升级」「缺席期间摘要」「复盘调整进入下一轮」——其中绝大部分是对现行已接受合同的**场景验证**（见 STEP 9），两条表达缺口登记 G-19/G-20。
**STEP 9 MINIMUM MODEL（先复用现有——本轮最重要的发现）**：
- Goal/成功定义：Business-level Goal/Direction【事实：现行 Authority】；成功定义需正式表达（连 G-20）；
- Leader Autonomy/Envelope：【事实】Autonomous Operating Lifecycle（Approved Strategy Envelope、CONTINUE/ADJUST、CEO Gate）已是 CEO Accepted 候选合同——本场景验证**它正是回答"业务为什么不停"的合同**；
- Operating Cadence：【事实】Blueprint 已有"Schedule/Trigger 是 Workspace 工作方式的一部分"；**Business 层的节奏/复盘点表达未定义** → G-20；
- Signal/Trigger：数据回流（注意：Round 2 修正后 Feedback/Metrics 属业务反馈层，**引用**对外动作，不属动作本身）+ 失败/阻塞事件 + 周期到达；
- Self-generated Work：【事实】现行"Work 默认从目标、策略、经营计划、团队运转、结果、触发器、日程或员工判断等真实经营上下文产生"——场景验证；
- Result→next Work：【事实】Work→Execution→Result/Evidence→Decision/next Work canonical 链 + Next Operating Cycle 语义；
- Employee Assignment：Organization Routing 自动解析、异常才 Leader 介入【事实】；
- Exception/Escalation：升级链 Employee→Leader→Business→Department→CEO【事实】+ P7 Decision Gate + C-12 风险分档；
- 缺席摘要：CEO Operating Day 跨日连续性合同（Day N→N+1）的**聚合形态**——缺席 N 天的一次性摘要+需要我清单 → 信息需求 G-19；
- Learning→Strategy Adjustment→Next Cycle：【事实】Operating Lifecycle 的 Review/Learning/CONTINUE/ADJUST。
**结论：S7 几乎不需要新对象——它验证的是"现行已接受的经营合同组合起来确实回答了核心问题"；真正的缺口只有两个表达登记（G-19/G-20）+ 资源争用模型（G-13 重构）。**
**STEP 10 OWNERSHIP/SCOPE**：Goal/成功定义/节奏/政策/Envelope→Business；执行→Workspace；Learning→业务（升级到公司需提炼，C-18）；缺席摘要→CEO 工作台（公司层投影）。
**STEP 11 CONTEXTUAL PROJECTION**：CEO 工作台（缺席摘要+需要我）；业务现场（本周节奏/进行中/复盘）；通知（升级事项，三段身份）。
**STEP 12 PLACEMENT**：政策/节奏/成功定义在 Business 设置；执行在 Workspace；摘要在 CEO 工作台。理由（A.4 规则）：CEO 此刻管理"公司今天怎么样"→工作台；Leader 此刻管理"这门生意怎么转"→业务；员工此刻管理"我手上的活"→工作现场。
**STEP 13 CROSS-BUSINESS TEST（四业务硬验证）**：

| 环节 | 内容增长 | 研发 RD | 电商 | 小说 |
|---|---|---|---|---|
| 成功定义 | 涨粉/互动/转化 | 交付质量/线上稳定性 | 利润/复购 | 读者留存/完读/收入 |
| 节奏 | 每周 N 篇+每日数据检查 | 迭代周期/每日构建 | 每日订单巡检+每周选品 | 每周两更 |
| 信号 | 曝光/涨粉/评论/发布失败 | 测试失败/构建红/需求变更 | 库存告警/订单激增/差评 | 掉订/评论/榜单 |
| 圈内自主 | 选题方向/发布时间微调 | 技术方案/任务拆解 | 政策内调价/补货 | 大纲内情节微调 |
| 出圈升级 | 商业化内容/敏感话题 | 生产发布/预算 | 大额采购/大促 | 版权/签约 |
| 学习→调整 | 标题结构有效→下周多用 | 某类 bug 反复→补测试规范 | SKU 转化好→加库存 | 某类情节留存高→多写 |

四业务呈现**同一骨架、不同参数** → BUSINESS OPERATING LOOP 候选 Company OS Core **VALIDATED**。
**STEP 14 SCALE TEST**：10 门业务各自节奏+升级 → CEO 不巡查的保障 = 出圈才升级 + 工作台聚合摘要；若 10 业务同时 blocked → 系统性资源不足 → 进入 Resource Allocation（下一阶段议题；G-13 资源争用是它的前哨）。
**STEP 15 REVERSIBILITY**：收权/放权（改 Envelope）；暂停节奏（业务 pause → cadence 停 + 未完工作处置）；改成功定义（下周期生效，历史不重写）。
**STEP 16 FAILURE**：Provider 挂 → 重试/换执行者 → 仍不行 → 上报；账号被封 → 业务级异常 → 升级；数据源断 → "未知"诚实显示，Leader 在不完整信息下决策须标注；全员阻塞 → 业务 blocked 显式可见（"为什么停了"是用户语言）；连续失败 → 自动降速/暂停并升级（不无限烧钱）。
**STEP 17 ONLY THEN ABSTRACT**：**BUSINESS OPERATING LOOP** = 目标与成功定义 → 节奏与信号 → Leader 圈内判断 → 自生成 Work → 执行 → 结果/证据 →（异常→自恢复→分档升级）→ 学习 → 策略调整 → 下一轮。经四业务验证 → Company OS Core 候选。

## S7 核心问题回答：一门 Business 为什么能在 CEO 不持续操作下继续经营？

四个支柱，缺一即停：
1. **责任在场**——Leader 是经营责任人（店长）：持续感知、判断、推进、汇报；不是 dispatcher，也不是摆设。
2. **规则在场**——CEO 的意志以 Goal / 成功定义 / 授权圈 / 政策的形式**事先写好**；他不在场时，是他的规则在场（这是"放权不失控"的全部秘密）。
3. **动力在场**——节奏（Cadence 到达）、信号（数据/失败/周期）、结果触发下一步（Result→next Work）构成**不需要 CEO 点火**的推进循环。
4. **出圈有电话**——异常与高风险按分档升级（C-12 三档+升级链），CEO 只接需要他的；自动恢复先行，升级是最后手段。
反证：无责任→停摆；无规则→要么审批机器人要么失控；无动力→项目经理复辟；无升级→出事没人管。**四支柱回答了核心问题；回答不清就不进 Lifecycle/Navigation/UI——现在回答清楚了。**

---

---

# ROUND 2 CONTINUE — S8 ~ S14：把 Business Operating Loop 推透

> 纪律（CEO 指令 P0-8/9/11）：每个场景完整十七步；"现有已支持"必须分两栏——**场景推导需求 → 现有 Curis 对照**，顺序不许倒；本轮不讨论结构/导航/UI；G-13 不采用工时隐喻。

---

## S8 — BUSINESS OPERATING CONTEXT / STATE（Leader 每天根据什么经营）

**场景**：Content Growth Leader 每天开始工作时，必须知道什么才能真正经营，而不是随机生成任务？

**STEP 1 REALITY**：真实店长/内容负责人早上坐下，第一动作不是打开任务列表随机干活，而是**掌握现状**：本周目标进展、最近数据、库存还剩几篇、账号状态、昨天发布表现、什么卡住了、团队谁有空、有什么在等我拍板。第二动作才是"决定今天干什么"。没有第一步，第二步就是瞎猜。
**STEP 2 ACTORS**：Leader（主视角）；Employees（进行中事实的来源）；平台/数据源（信号）；CEO（待决与边界）。
**STEP 3 OBJECTS**：目标与策略（设定）；本周计划；进行中的工作；已完成结果；卡住的事；团队可用性；内容库存；账号与平台状态；最近发布与数据；异常；等 CEO 的事项。
**STEP 4 HAPPY PATH**：坐下 → 扫一眼经营现状 → 与本周计划对照 → 发现"库存够、A 账号在涨、B 账号有投诉" → 定今天重点（处理投诉/继续产出/准备复盘）→ 分派。
**STEP 5 USER CHOICES**：看现状的入口形态（一页总览 vs 逐现场查——OPTION）；颗粒度（业务级 vs 工作级）；CEO 待决要不要进 Leader 的现状视图（要——"等老板"是经营事实的一部分）。
**STEP 6 BRANCHES**：数据缺失（平台数据没回→必须显式"未知"，不能显示 0）；部分迟到（回执到了、数据没到）；库存空（状态）；多账号部分失败；员工全员忙；**策略刚被 CEO 改过（必须看到最新版，不能拿旧策略干活）**。
**STEP 7 CONSEQUENCES**：无可靠现状 → 靠记忆翻记录 → 判断质量崩坏、随机生成任务；缺失显示为 0 → 把"没回传"当"没效果"误判；看不到最新策略 → 干偏。
**STEP 8 PRODUCT CAPABILITY**：「查看业务的当前经营事实」（一屏分层现状）；「诚实表达未知与迟到」。
**STEP 9 MINIMUM MODEL**：本场景推出的核心是**五类事实分层**：
① **Persistent Truth**（设定，变更有痕）：Goal/Strategy/成功定义/授权圈/账号归属/团队构成；
② **Current State**（当前进行态）：进行中 Work 状态/库存水位/账号连接/员工与 Provider 可用性/待 CEO 事项；
③ **Signal**（新变化）：数据变化/新回执/新评论/失败告警——有"新"属性，看过即转 State 或 History；
④ **History**（已沉淀）：过去的 Work/Result/发布/复盘——供对照引用，不主动打扰；
⑤ **Unknown**（诚实缺失）：源未回传/授权过期拿不到/从未采集——与 0 严格区分。
两栏对照（P0-9）：需求"Leader 一屏掌握现状" → 现行只有 Workspace Current Operating 轻量摘要（经营状态/本轮重点/最新判断/下一步【事实】），**Business 层的经营事实面未定义** → G-21；需求"未知≠0" → 现行指标合同 Unknown/Freshness 语义【事实】→ match；五类分层命名 → 现行分散存在、未统一 → 表达原则登记。
**STEP 10 SCOPE**：Persistent Truth→Business；Current State→Business/Workspace；Signal→业务反馈层；History→Business；Unknown→标注在数据源处。
**STEP 11 PROJECTION**：Leader=五类一屏；CEO=聚合摘要（S13）；员工=自己那条线。
**STEP 12 PLACEMENT**：业务现场（Leader 打开业务的第一个面）；缺失标注在源。
**STEP 13 CROSS-BUSINESS**：内容（Persistent=打法/品牌口径；State=库存/账号/排期；Signal=爆款与投诉）｜研发（Persistent=技术路线；State=在途 Cycle/构建状态；Signal=构建红/新 Issue）｜电商（Persistent=选品定价策略；State=在售/库存/在途订单；Signal=订单激增/差评）｜小说（Persistent=大纲/定位；State=存稿水位/连载状态；Signal=掉订/评论）——四业务同构 ✓
**STEP 14 SCALE**：10 业务×各一事实面（Leader 各看各的）；员工 50 人→可用性聚合必须诚实（连 G-13）。
**STEP 15 REVERSIBILITY**：事实面是读投影；Persistent Truth 变更走版本留痕。
**STEP 16 FAILURE**：数据源断→该区显式 Unknown+原因+重试入口；分区独立加载（Partial Failure 语义【事实：CEO Desk 合同】）。
**STEP 17 ABSTRACT**：**Business Operating Context = 五类事实分层（Persistent Truth / Current State / Signal / History / Unknown）** → Core 候选（四业务验证）；G-21 登记。

---

## S9 — GOAL & SUCCESS DEFINITION（不是 KPI）

**场景**：CEO 说"三个月把 Curis 内容业务做起来"。Leader 凭什么知道现在做得好不好？

**STEP 1 REALITY**：现实中这句话落下来，店长必然追问（或自己补齐后请老板确认）：做到什么算"做起来"？多久？什么只是参考信号？不能牺牲什么？花多少钱？什么情况必须停/必须改？——没有这些，干完三个月老板说"不是我要的"。**目标从来不是一句话，是一组判断标准。**
**STEP 2 ACTORS**：CEO（给方向+确认标准）；Leader（补齐为可判断的定义）；分析师（提供对照事实）。
**STEP 3 OBJECTS**：最终目标；时间范围与检查点；成功状态；偏离/失败信号；约束（品牌底线/合规）；预算上限；停止与调整条件。
**STEP 4 HAPPY PATH**："三个月做起来" → Leader 澄清后落成：目标=建立"一人 AI 公司"主题专业认知；时间=3 个月按月检查；成功=首月 30 篇高质量+3k 粉、次月稳定互动、第三月自然转化线索；约束=不投放、品牌口径合规；预算=每月模型成本上限；停止条件=连续 4 周互动低于基线必须调打法而非硬扛 → CEO 确认 → 据此经营。
**STEP 5 USER CHOICES**：CEO 给粗目标 vs 完整定义（产品必须接受粗目标——Bootstrap 原则【事实】——Leader 提案补齐、CEO 确认）；里程碑制 vs 单点制【OPTION】（现实多为里程碑制）；指标谁定（Leader 提案+CEO 确认）。
**STEP 6 BRANCHES**：中途改目标（版本留痕；在途 Work 完成旧目标或迁移）；明显达不到（提前预警→上报→调策略或改目标——Goal 层升级）；成功定义中某指标数据源断（该指标 Unknown，按剩余指标+人工判断）；检查点到达（CEO 判断继续/调整/停止——Cycle 边界）。
**STEP 7 CONSEQUENCES**：无成功定义 → Leader 无法回答"好不好"（S7 空洞化）；**把指标当目标 → 刷量虚荣**（信号≠成功）；无约束 → 自主时踩品牌红线；无停止条件 → 无效打法硬扛烧钱。
**STEP 8 PRODUCT CAPABILITY**：「给业务定目标与时间范围」「定义成功/偏离/停止条件」「定约束与预算上限」「按检查点回顾达成」。
**STEP 9 MINIMUM MODEL**：两层对照——场景推导需求：Goal（去哪）/ Success Definition（怎么算好/坏/偏，含约束、预算、停止条件）/ Metric-Signal（看到的事实）**三层分离，不是一个 KPI 对象**。现有对照：Business-level Goal/Direction【事实】+ Operating Lifecycle 的 Success Contract 与 CEO Gate【事实：Approved Candidate】+ 指标合同（source/freshness/禁无契约评分【事实】）。缺口：**三层分离在产品语言中未显性**，容易被读成一个 KPI → 表达原则登记（Goal 对象+定义字段组+指标引用，不必然新对象）。
**STEP 10 SCOPE**：Goal/定义/约束→Business（Persistent Truth）；指标事实→业务数据与洞察；检查点→节奏。
**STEP 11 PROJECTION**：Leader=目标+当前对照（引用 S8 事实面）；CEO=达成概览；报告=逐条对照。
**STEP 12 PLACEMENT**：定目标在 Business；对照在业务现场与洞察。
**STEP 13 CROSS-BUSINESS**：内容（成功=粉丝/互动/转化线索；停止=连续 4 周低于基线）｜研发（成功=按期+P0 全过+崩溃率达标；停止=方案连续两周无法验证→换）｜电商（成功=毛利/退货率；停止=渠道连续亏损→停投）｜小说（成功=完读率/签约；停止=连续 N 章留存崩→改大纲或上报）——四业务同构 ✓
**STEP 14 SCALE**：10 业务×轻量定义（否则管理负担）；CEO 视角"哪门在轨道上"（连 S13）。
**STEP 15 REVERSIBILITY**：定义版本化；改后在途 Work 处置显式；历史可回看。
**STEP 16 FAILURE**：指标源断→Unknown；目标间资源冲突→升级；检查点错过→显式"未回顾"。
**STEP 17 ABSTRACT**：**Goal / Success Definition / Metric-Signal 三层分离** → Core 原则（四业务验证）。

---

## S10 — STRATEGY（Goal 与 Work 之间缺失的一层，本轮重点）

**场景**："三个月建立品牌认知"之下，Leader 的打法是"聚焦一人 AI 公司主题；小红书+视频为主；案例内容建专业认知；**暂不做付费投放**"——然后才有选题/文案/发布。

**STEP 1 REALITY**：店长不是从目标直接跳到每天的活。先有一套**打法**（怎么赢、不做什么），打法落成排期计划，计划才变成具体工作。打法错了，活干得再好也没用；打法变了，每天的活跟着变；打法本身是要被复盘的对象（"上月这打法不行，换"）。**没有 Strategy 的 Goal→Work 是零散任务，不是经营。**
**STEP 2 ACTORS**：CEO（确认大方向与"不做什么"）；Leader（制定与圈内调整）；员工（执行）；分析师（依据）。
**STEP 3 OBJECTS**：打法（聚焦/渠道/形态/**负空间=不做什么**）；打法下的计划与节奏；打法产生的 Work；打法依据（研究/数据）；打法历史版本；打法的有效性证据。
**STEP 4 HAPPY PATH**：Goal 确认 → Leader 制定 Strategy → CEO 确认（暂不投放是重大取舍）→ 落成计划与节奏（每周选题会/每周 3 篇/双平台）→ 计划产生 Work → Result 回流 → 复盘对照 Strategy → Learning：案例类效果好 → **圈内调整**（加大案例比重）→ 下轮计划更新 → 后续 Work 感知新计划。
**STEP 5 USER CHOICES**：谁起草（Leader 拟 CEO 确认——正常；CEO 直接给——合法）；调整幅度（细节=圈内；方向变更=出圈，如转付费投放/换主平台）；是否显式写"不做什么"（必须——Strategy 的本质是取舍）；粒度【OPTION】一份总打法 vs 每账号子打法。
**STEP 6 BRANCHES**：停止条件触发（数据证明打法无效→圈内调整 or 上报换打法）；CEO 改 Strategy（在途 Work 按发起时版本完成并标注【事实：运行中工作 pinned 旧版本】）；外部变化使打法失效（平台规则巨变→上报建议）；多业务打法冲突（抢同一渠道资源→资源协调）；**执行走样**（Work 与 Strategy 脱节——无溯源就发现不了）。
**STEP 7 CONSEQUENCES**：无 Strategy 层 → 工作失去一致性（今天 A 主题明天 B 主题，形不成认知积累）；Work 不知来自哪条打法 → 无法复盘打法有效性（学习断链）；Strategy 无历史 → 复盘说不清"当时为什么这么定"。
**STEP 8 PRODUCT CAPABILITY**：「制定/查看业务打法」「把打法落成计划与节奏」「CEO 确认打法与重大变更」「Leader 圈内调整」「回顾打法有效性（对照成功定义）」。
**STEP 9 MINIMUM MODEL**：两层对照——场景推导需求：Strategy 是**独立经营事实**（当前有效版本+版本历史+隶属 Goal+**Work 溯源**）。现有对照：`business_directions`（Strategy/Direction supporting truth）【事实：Canonical Business Spine】+ Approved Strategy Envelope（圈内自主调整）【事实：Operating Lifecycle】+ Team Operating/计划。**发现：推导与现行合同高度一致**；缺口：**Work→Strategy 的溯源关系未显性** → G-22（关系，非新对象）。
**STEP 10 SCOPE**：Strategy→Business（Persistent Truth，版本化）；计划/节奏→Business；Work→现场；有效性证据→反馈层。
**STEP 11 PROJECTION**：Leader=当前打法+计划+Work 溯源；CEO=批准与重大变更；复盘=打法 vs 结果对照。
**STEP 12 PLACEMENT**：打法在 Business；执行在 Workspace。
**STEP 13 CROSS-BUSINESS**：内容（打法=主题聚焦/双平台/案例优先/不投放）｜研发（打法=技术路线/自研 vs 集成/发布节奏；出圈=换架构）｜电商（打法=品类聚焦/渠道/定价；出圈=换主推品类）｜小说（打法=题材定位/更新节奏/平台选择；出圈=题材转向）——同构 ✓
**STEP 14 SCALE**：10 业务×轻打法（一段话+几条取舍）；CEO 看"各业务打法与目标是否一致"。
**STEP 15 REVERSIBILITY**：版本化——可回看、经确认可回退；在途 Work pinned 旧版本【事实】。
**STEP 16 FAILURE**：无研究就定打法→诚实标注"低信心/未经研究"；数据源断→有效性判断 Unknown；越圈调整→权限拦截/事后审计（连 S12）。
**STEP 17 ABSTRACT**：**Strategy 是 Goal 与 Work 之间的独立经营事实（含取舍负空间）；Work 溯源 Strategy；Result 反证 Strategy** → Core 原则（四业务验证；与 business_directions/Envelope 一致）。

---

## S11 — OPERATING DRIVERS（六种动力，不是只有 Schedule）

**场景**：业务为什么会自己产生下一项 Work？

**STEP 1 REALITY**：观察真实店长一周的推进来源：周一开选题会（**时间到了**）；周二某类内容爆了（**数据信号**）；库存只剩 2 篇低于安全线（**状态**）；发布完成 48 小时该复盘了（**上一项结果**）；平台突然改规则（**外部事件**）；还有——他"就是觉得"该做一个周年策划（**经营判断**，没有规则）。六种动力现实中并存且性质不同。
**STEP 2 ACTORS**：Leader（判断者）；系统（时间/状态/结果的机械触发）；外部世界（事件）；员工（承接）。
**STEP 3 OBJECTS**：节奏点；信号；状态阈值（安全线）；上一项 Result；外部事件；经营判断。
**STEP 4 HAPPY PATH（一周六例）**：TIME→周一选题会照开；SIGNAL→爆款出现→**Leader 看到信号后判断**"加做一条同类"；STATE→库存<2→按政策**自动**生成补货 Work；RESULT→发布完成 48h→复盘 Work 自动排入；EXTERNAL→平台改规则→告警→Leader 评估影响；JUDGMENT→"周年策划值得做"→直接新建 Work。
**STEP 5 USER CHOICES**：每类动力两种处置：**政策化机械触发（需政策授权——连 C-12/P4）vs 提示后由 Leader 判断**（默认后者）；每业务动力组合不同（内容靠节奏+信号；电商靠状态+外部事件；RD 靠结果链+外部事件；小说靠节奏+信号）。
**STEP 6 BRANCHES**：多动力同时到达（优先级仲裁，连 G-13）；触发的新 Work 与在途冲突（合并/排队）；误报（确认后取消）；Leader 判断被 CEO 否（留痕学习）。
**STEP 7 CONSEQUENCES**：只有 TIME → 业务只会按表干活，对市场无反应；只有 JUDGMENT → 全靠人盯；全部政策化自动触发 → 数据一抖就自动生成工作，业务变成失控机器——**必须区分"机械触发"与"提示判断"**。
**STEP 8 PRODUCT CAPABILITY**：「设定节奏」「设置安全线与政策化触发」「结果完成后自动进入下一步」「接收外部事件」「把信号呈给 Leader 判断」「Leader 直接发起 Work」。
**STEP 9 MINIMUM MODEL**：两层对照——场景推导需求：六类动力（TIME/SIGNAL/STATE/RESULT/EXTERNAL EVENT/LEADER JUDGMENT）×两种处置（机械触发需政策授权 / 提示待判断）。现有对照：Blueprint"Work 默认从目标、策略、经营计划、团队运转、结果、触发器、日程或员工判断等真实经营上下文产生"【事实——现行这句恰好枚举了这些来源，本场景是其场景化验证】+ Trigger/Schedule【事实】。缺口：六类动力的**用户语言分类与两档处置**未显性 → G-23。
**STEP 10 SCOPE**：节奏/安全线/政策→Business；信号→反馈层；判断→Leader；每个 Work 记录"来源动力"。
**STEP 11 PROJECTION**：Leader=动力日历+待判断信号；系统=触发留痕。
**STEP 12 PLACEMENT**：动力配置在 Business；触发执行在运行层。
**STEP 13 CROSS-BUSINESS**：内容（TIME 周选题会/SIGNAL 爆款/STATE 库存线/RESULT 48h 复盘/EXTERNAL 平台改规则/JUDGMENT 周年策划）｜研发（TIME 迭代会/SIGNAL 构建失败率升/STATE 待审 PR 堆积/RESULT 开发完自动进 Review/EXTERNAL GitHub Issue 与依赖公告/JUDGMENT 该还技术债了）｜电商（TIME 周选品/SIGNAL SKU 转化暴涨/STATE 库存线自动补货/RESULT 投放结束进复盘/EXTERNAL 供应商涨价/JUDGMENT 竞品降价跟不跟）｜小说（TIME 每周两更/SIGNAL 掉订加速/STATE 存稿<3 章催稿/RESULT 章节发布 48h 回流/EXTERNAL 平台征文/JUDGMENT 支线展开）——**四业务六动力全成立** ✓
**STEP 14 SCALE**：10 业务×多动力→每个 Work 必须记"来源动力"（否则复盘说不清工作为何产生）；CEO 只见政策化触发的异常与 Leader 的大动作。
**STEP 15 REVERSIBILITY**：政策可改（自动→提示）；误触发可取消（未开始）；已开始走 Work 生命周期。
**STEP 16 FAILURE**：触发条件数据源断→该动力 Unknown/暂停（诚实）；触发风暴（数据抖动连发）→防抖聚合（行为级）；提示长期不处理→升级（连 S13）。
**STEP 17 ABSTRACT**：**六类 Operating Drivers + "机械触发需政策授权 vs 提示待判断"两档处置** → Core 原则（四业务验证；与现行 Work 来源枚举一致，场景化）；G-23 登记。

---

## S12 — LEADER JUDGMENT & OPERATING ENVELOPE

**场景**：内容数据连续一周下降。Leader 面对一串决定——逐项问能不能自己定？

**STEP 1 REALITY**：老板对店长说"日常你看着办，大事打电话"。什么是日常什么是大事？不是风险等级一刀切，而是**看改变什么**：改变"怎么干"（圈内）；改变"卖什么/我是谁"（圈边）；改变"投多少钱/对外承诺什么"（圈外）。
**STEP 2 ACTORS**：Leader（判断与行动）；CEO（画圈与被升级）；员工（执行调整）。
**STEP 3 OBJECTS**：一串具体决定（逐项）；授权圈；Action Grant（员工层——对照项）。
**STEP 4 HAPPY PATH（八项逐判）**：①调整选题方向——**自主**（打法细节）；②调整发布时间——**自主**（执行细节）；③增加竞品研究——**自主**（小投入）；④图文转视频——**自主**（打法细节，量大但不动方向）；⑤调整本业务员工分工——**自主**（【事实】LEADER_OWNS_DIVISION_AND_COLLAB；但跨业务借人→上报）；⑥模型预算+50%——**上报**（【事实】material Budget 须 CEO Gate）；⑦改品牌定位——**上报**（【事实】protected Strategy Boundary）；⑧暂停某账号发文——**自主+留痕**（可逆执行层）；注销账号——**必须 CEO**（不可逆对外动作）。
**STEP 5 USER CHOICES**：CEO 风格谱系——全托管（圈大、只看周报）vs 强控制（圈小、细节确认）——**产品必须连续支持两极**（Envelope 是 CEO 的参数，不是产品写死）。
**STEP 6 BRANCHES**：圈内决定无效（继续调 or 升级"打法失效"）；需要跨业务资源（升级协调，连 G-13）；紧急来不及请示（政策可授"紧急止损权"——先止损再报告）；滥用圈（使用留痕+审计）。
**STEP 7 CONSEQUENCES**：无 Envelope → 事事请示或无边界放权；**把 Action Grant 与 Envelope 混层 → 给了员工发布权就等于 Leader 能改品牌**（荒谬）——两层对象不同：Grant=员工×对象×动作；Envelope=Leader×经营维度×幅度。
**STEP 8 PRODUCT CAPABILITY**：「CEO 按维度给 Leader 画圈」「Leader 圈内自主决定并留痕」「圈外升级（带建议）」「调整圈的大小」「查看圈的使用记录」。
**STEP 9 MINIMUM MODEL**：两层对照——场景推导需求：Envelope 按**经营维度**分档（策略权威/资源调配/预算/分工/对外动作/风险边界/定位边界），每维度取值（自主/需确认/禁止），CEO 可设、可改。现有对照：Approved Strategy Envelope【事实：Goal/Success Contract/Positioning/Target Audience/Business-Monetization Model/protected Strategy Boundary/material Budget/高影响不可逆承诺须 CEO Gate】+ 分工与协作归 Leader【事实】。**发现：推导与现行合同几乎一一对应——验证并维度化，非新增**；缺口：**按维度设置+两极连续可配**的表达未细化 → G-24。
**STEP 10 SCOPE**：Envelope→CEO 设置、挂 Business；使用留痕→Business。
**STEP 11 PROJECTION**：Leader=我的圈是什么（清楚知道什么能自己干）；CEO=圈设置+使用审计；升级事项带"为什么出圈+建议"。
**STEP 12 PLACEMENT**：圈设置在 Business；留痕在业务事实层。
**STEP 13 CROSS-BUSINESS**：内容（自主：选题/时间/形式/账号暂停；出圈：预算/定位/注销）｜研发（自主：技术方案/任务拆解/内部流程；出圈：生产发布/架构重写/对外开源承诺）｜电商（自主：政策内调价/补货/客服；出圈：大额采购/进新市场/品牌口径）｜小说（自主：情节微调/节奏/封面；出圈：签约条款/改编授权/题材转向）——维度相同、取值不同 ✓
**STEP 14 SCALE**：10 业务×各 Leader 各圈→按业务类型给**默认圈模板**、CEO 微调（行为级，登记观察）；圈内决定只留痕不打扰，CEO 抽查审计。
**STEP 15 REVERSIBILITY**：圈可改（对新决定生效）；已发生的圈内决定不可"收回"（经营事实）但可纠偏；升级可撤回（"这个你定"=下放留痕）。
**STEP 16 FAILURE**：圈未设置（新业务 Leader 无圈→默认最小圈+显式提醒 CEO 补设——fail-safe）；判断依据 Unknown（标注后仍可判断）；越圈操作被拦截→"超出你的授权圈，已转 CEO"。
**STEP 17 ABSTRACT**：**Leader Operating Envelope（经营维度×档位×CEO 连续可调）与 Action Grant（员工×对象×动作）是两层不同权限** → Core 原则（四业务验证；与现行 Envelope 合同一致并维度化）；G-24 登记。

---

## S13 — CEO ABSENCE / RETURN（3 天 vs 30 天）

**场景**：CEO 离开 3 天 / 30 天，回来分别需要知道什么？

**STEP 1 REALITY**：出差 3 天回来：扫一眼消息+问店长"有事吗"→10 分钟。出差 30 天：不可能 10 分钟——要看哪些店照常赚、哪店出过事已处理、谁改了打法（合理吗）、钱烧得对不对、什么等我拍板。**30 天的叙述不是"30 天日志"，而是"这段时间的变化与结论"（统计+叙述+例外）。**
**STEP 2 ACTORS**：CEO；各业务 Leader（各自缺席叙述）；助理（聚合者）；系统（压缩器）。
**STEP 3 OBJECTS**：缺席时段；正常推进（压缩为统计）；重大变化（展开）；策略调整记录（圈内留痕）；异常与处置结果；停了的业务及原因；值得看的 Result；等 CEO 的决定；资源异常；目标偏离。
**STEP 4 HAPPY PATH（30 天版）**：打开 → **公司级回归摘要**：一句话总览（10 业务：8 正常、1 待决、1 暂停）→ 重大变化 ≤5 条带因果（A 数据翻倍=策略调整生效；B 账号被封已恢复；C Leader 圈内调整了打法，留痕可查）→ 等你拍板 3 条（按业务分组、各带建议）→ 资源异常（模型成本超预期 20%，哪门业务）→ 目标偏离（D 进度落后，Leader 已调整、观察中）。逐条处理或下钻；**不看任何单独 Work**。
**STEP 5 USER CHOICES**：摘要深度分层（一句话/五条/下钻）；按业务分组 vs 按重要性【OPTION：默认重要性+可切业务】；30 天要不要"叙述线"（要——"发生了什么重要事情"是叙述不是列表）。
**STEP 6 BRANCHES**：全部正常（摘要极短——**安静是特性**）；多项重大异常（排序）；缺席期间 CEO 自己插入过决定（不再算待办）；不信任某业务（下钻完整叙述）。
**STEP 7 CONSEQUENCES**：无摘要→巡查复辟（50 现场×30 天）；全量 Work 列表→噪音淹没真正等的决定；只有统计没有叙述→知道"涨了"不知道"为什么"。
**STEP 8 PRODUCT CAPABILITY**：「缺席期间公司摘要（分层：总览→重大变化→待决→资源异常→目标偏离）」「逐业务缺席叙述（Leader 提供）」「带上下文下钻」。
**STEP 9 MINIMUM MODEL**：两层对照——场景推导需求：压缩规则（**正常=统计；例外=展开；待决=突出带建议；偏离=对照成功定义**）+ 3 天/30 天两档 + 叙述+例外结构。现有对照：CEO Operating Day 跨日连续性合同（Day N→N+1）【事实】+ CEO Desk attention-first【事实】+ 报告的 FACT/INTERPRETATION/UNKNOWN 结构【事实】+ G-19（S7 登记）。**G-19 在此被完整展开**：3 天=跨日连续性的自然延伸；30 天=聚合+叙述——信息需求落定，仍不做 UI。
**STEP 10 SCOPE**：摘要→公司层（工作台投影）；素材→各业务事实+Leader 叙述。
**STEP 11 PROJECTION**：即本场景（两档深度+可调时间窗）。
**STEP 12 PLACEMENT**：CEO 工作台；下钻到业务现场。
**STEP 13 CROSS-BUSINESS**：四业务的"正常推进压缩为什么"不同（发布数/迭代数/订单数/更新数），但**压缩-展开-待决-偏离**结构相同 ✓
**STEP 14 SCALE**：30 天×10 业务→压缩必须严格（正常=一行统计；例外才展开）；Leader 叙述是素材源。
**STEP 15 REVERSIBILITY**：时间窗可调；已处理移入已读；下钻状态保留。
**STEP 16 FAILURE**：某业务数据源断→该区块显式"数据不完整（原因）"而非静默缺席；Leader 叙述缺失→按事实聚合兜底并标注；生成失败→逐业务独立可看（Partial Failure）。
**STEP 17 ABSTRACT**：**CEO ATTENTION MODEL（正常→压缩；例外→展开；待决→突出带建议；一切可下钻）+ ABSENCE/RETURN SUMMARY（3 天/30 天两档，统计+叙述+例外）** → Core 原则（四业务验证；G-19 信息需求落定）。

---

## S14 — AI EMPLOYEE RESOURCE / CONTENTION（深化 G-13，不用工时隐喻）

**场景**：AI 员工为什么不能无限接 Work？（继续 Method V2；禁止 80% workload/8 小时/排班表，除非场景证明需要）

**STEP 1 REALITY**：现实对照不是"员工疲劳"，而是"一套共享基础设施的吞吐"：多门店共用的检验员一次只能验一批（排他）；供电有上限（并发）；电费有预算（成本）；供应商限购（配额）。AI 员工的"不能无限接"来自它的**资源链条**，不是它的疲劳。
**STEP 2 ACTORS**：员工（承接者）；Provider（模型 API/外部 Agent——并发与配额）；账号/工具（排他资源）；预算（公司/业务/员工层）；多业务 Leader（竞争者）；审核者（瓶颈岗位）。
**STEP 3 OBJECTS**：并发上限；订阅配额；Token/Cost 预算；排他会话（账号/浏览器/工具）；执行环境占用；上下文装载（跨线切换成本）；优先级；审核产能；外部限流。
**STEP 4 HAPPY PATH**：电商与内容 Leader 同时派活给林墨 → 发现：图像 Provider 并发有余量 ✓、本月成本预算有余 ✓、但品牌账号的浏览器会话正被电商任务占用（排他）→ 内容任务排队 → 状态"阻塞·账号会话被占用"→ 释放后自动继续。
**STEP 5 USER CHOICES**：冲突谁优先（政策：业务优先级/先到先得/CEO 指定）；预算超了（硬停/降级模型/请示）；要不要排班表——**七个争用机制没有一个需要排班 → 判定：不造排班表**。
**STEP 6 BRANCHES**：并发满（排队+诚实显示预计等待）；配额尽（本月 Codex 用完→换执行者/暂停该类任务/请示扩额）；成本超预算（按政策：硬停/降级/请示）；排他死锁（互等→检测并按优先级解）；审核瓶颈（生产快审核慢→审核者是业务瓶颈→升级 Leader，这是业务资源问题）；外部限流（退避重试）。
**STEP 7 CONSEQUENCES**：不表达争用→任务静默排队/失败，用户看到"员工卡住了"却不知道为什么（黑箱）；不区分类型→无法治理（加预算解决不了账号排他）；伪造"工时排满"→与真实机制脱节，误导管理。
**STEP 8 PRODUCT CAPABILITY**：「看到员工当前被什么资源卡住」（真实原因）；「设置预算与配额政策（公司/业务/员工三层）」「设置冲突优先级政策」「看到业务瓶颈资源（如审核产能）」。
**STEP 9 MINIMUM MODEL**：两层对照——场景推导需求：争用=**资源类型（并发/配额/成本/工具排他/账号排他/上下文/环境/优先级/审核/限流）× 占用状态 × 政策**。现有对照：Shared Employee UI Status 的"阻塞·<cause>"【事实——正是为诚实表达留的口子】+ Provider Health【事实】+ Usage Ledger【事实】。缺口：**争用类型枚举与政策层**未定义 → G-13 内容在本场景落定（七类+三类补充机制全部验证），剩表达形态（NOT YET FINAL 维持）。
**STEP 10 SCOPE**：预算/配额政策→公司/业务/员工三层；争用状态→员工行+执行现场；优先级→政策。
**STEP 11 PROJECTION**：Leader=我的业务里谁被什么卡住；CEO=跨业务资源异常（连 Resource Allocation 下一阶段）；员工行=阻塞·真实原因。
**STEP 12 PLACEMENT**：争用显示在执行现场与员工行；政策在设置/业务；瓶颈分析在洞察。
**STEP 13 CROSS-BUSINESS**：研发（Codex 配额+Repo 锁+审核瓶颈）✓ 电商（账号会话排他+成本预算）✓ 小说（写作模型并发+成本）✓ 内容（图像 API 并发+账号排他）✓——七类机制四业务全部复现 ✓
**STEP 14 SCALE**：50 员工/10 业务→争用从个别现象变成系统性资源分配问题→Resource Allocation（下一阶段）的入口；本场景只要求诚实表达+政策 hooks。
**STEP 15 REVERSIBILITY**：排队可取消；政策可改；降级可回升；队列按政策可调。
**STEP 16 FAILURE**：状态失真（显示空闲实际被排他占用）→ 诚实原则红线；预算未设→超支（默认建议设置+提醒，不静默）；死锁检测失败→超时升级。
**STEP 17 ABSTRACT**：**AI Employee Resource / Contention = 资源类型 × 占用状态 × 政策；明确不采用工时/排班隐喻** → Core 原则候选（四业务验证；G-13 内容落定）。

---

## ROUND 2 CONTINUE 收口：七个核心问题回答（CEO 指令 P0-13）

**1. Leader 每天根据什么事实经营 Business？**（S8）五类分层事实：**Persistent Truth**（目标/策略/成功定义/授权圈——当前有效版本）对照 **Current State**（进行中/库存/账号/团队可用/待 CEO），被 **Signal**（新变化）驱动，参考 **History**，并诚实面对 **Unknown**。判断=Signal/State 对照 Persistent Truth；缺一类事实，判断质量就塌一角。
**2. Goal、Success Definition、Strategy、Work 是什么关系？**（S9/S10）**Goal=去哪**（方向+时间）；**Success Definition=怎么算好/坏/偏**（判断标准+约束+预算+停止条件）；**Strategy=怎么赢**（打法+取舍负空间，Goal 之下、Work 之上的独立事实，版本化）；**Work=打法落成计划后的具体执行**（溯源 Strategy）。Metric-Signal 只是事实输入，绝不与 Goal 混淆（防虚荣指标）；Result 反证 Strategy，Learning 圈内调 Strategy、出圈升级 CEO。
**3. Business 为什么会自己产生下一项 Work？**（S11）六类动力：TIME / SIGNAL / STATE / RESULT / EXTERNAL EVENT / LEADER JUDGMENT；前五类可政策化为机械触发（需政策授权）或提示后由判断产生；其中 **RESULT→next Work 是最基本的连续动力**。CEO 的点火只在开业和改规则时需要。
**4. 哪些 Leader 自己定，哪些必须 CEO？**（S12）按 Envelope 维度：策略细节/执行细节/内部分工/小投入=**自主**（留痕）；Goal、定位、商业模式、material Budget、重大/不可逆对外承诺、跨业务资源=**CEO Gate**。Envelope 按 7 个经营维度设置、全托管到强控制连续可配；与 Action Grant（员工×对象×动作）是两层，不混。
**5. CEO 离开 30 天回来如何在很短时间重新掌握公司？**（S13）分层回归摘要：一句话总览（N 正常/M 异常/K 待决）→ 重大变化 ≤5 条带因果 → 等我拍板（带建议、按业务分组）→ 资源异常与目标偏离（对照成功定义）；**正常压成统计、例外才展开、一切可下钻**；逐业务有 Leader 叙述。10 分钟量级，不读任何单独 Work。
**6. AI Employee 真正会因为什么产生资源冲突？**（S14）不是工时——Provider 并发、订阅配额、Token/Cost 预算、Tool 排他、Account 排他、Context 冲突（跨线切换）、执行环境占用，外加优先级仲裁、审核瓶颈、外部限流；表达为"资源类型×占用状态×政策"，用"阻塞·真实原因"诚实显示；**不造排班表**。
**7. 换到 RD、电商、小说是否仍成立？**（S8–S14 各场景四业务验证）成立——五类事实、Goal 三层、Strategy 独立事实、六动力、Envelope 维度、回归摘要结构、争用机制在四个业务全部复现，**参数不同、骨架相同** → BUSINESS OPERATING MODEL 候选 Company OS Core。

---

# 完成标准与 STOP

- 交付：S8–S14 七个场景完整十七步（每个含两栏"场景推导需求→现有对照"）+ 七问收口；四业务交叉验证贯穿。
- 新登记：G-21（Business 层经营事实面）、G-22（Work→Strategy 溯源）、G-23（六动力分类与两档处置）、G-24（Envelope 维度化表达）；G-13 内容由 S14 落定（七类争用验证完成，表达形态 NOT YET FINAL）；G-19 信息需求由 S13 落定。
- Ledger 新增 CAP-012~CAP-017（三分类）。
- 未修改任何 Authority/Blueprint/结构/导航/UI/Runtime；未 commit/push。
- 七问已全部说清。等待 CEO / ChatGPT 确认 **BUSINESS OPERATING MODEL DERIVED** 后，才进入 Business Lifecycle / Success Definition 细化 / Resource Allocation / Activation / Evolution / Company Learning。

**STOP FOR CEO / CHATGPT REVIEW**
