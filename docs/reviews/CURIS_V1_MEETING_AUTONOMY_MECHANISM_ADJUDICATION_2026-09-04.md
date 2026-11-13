# CURIS V1 — MEETING 发言机制自主权裁定书

Status: Review
Authority Class: REVIEW
Date: 2026-09-04
Owner: software-architect-2（高见远）
Re: Backlog `V1-P1-015 MEETING ROOM PRODUCTIZATION CLOSURE`
上游依据: `docs/reviews/CURIS_V1_MEETING_AUTONOMOUS_DISCUSSION_REVIEW.md`（2026-09-02，Disposition: IMPLEMENTED / PARTIAL）
代码基线: `backend/app/meeting_service.py`、`backend/app/api/meeting_router.py`、`backend/app/main.py`

---

## 0. 范围与立场声明（只读）

- 本裁定处于 **review-mode**，**未修改任何代码 / 文档 / 数据库 / Runtime**，未启动或停止任何服务进程，未 `git add/commit/push/stage`。
- 裁定对象**仅限 Meeting 发言机制**（谁在何时发言、发言顺序如何产生），不评审 CEO Desk / Organization Center / Knowledge Library / 视觉 / Figma / 导航 / Connector 架构。
- 所有结论均给出 `file:line` 证据。判定不因为「看起来像轮询」而给出，必须落到代码。
- 判据不放松：本裁定给 QA 的验收判据以「可证伪」为前提，不因希望验收通过而降低门槛。

---

## 一、裁定结论（三选一）

> **PARTIALLY AUTONOMOUS — 存在 2 处会稳定产生固定顺序观感的核心机制**（外加 1 处促成稳定交替的确定性惩罚、1 处架构性偏离）。

含义与边界：

- **不是 `NOT AUTONOMOUS`（deterministic round-robin）**：代码中没有 `next = (i+1) % n` 式的固定循环轮换；发言顺序会随「议题相关性」「事实/结果归属权」「CEO/Leader 点名」而改变（见 §2.6）。这与 2026-09-02 评审 §4「There is no round robin」一致。
- **也不是 `AUTONOMOUS`（代码层面无固定顺序）**：发言人由一段**确定性评分公式 + 字典序 tie-break** 在任意 LLM 调用之前选定（见 §2.2–§2.5），员工**从不自荐**「我现在是否该发言」。在「低相关性」退化场景下，顺序会塌缩为固定交替并结构性地排除平等地位的员工（见 §2.3）。
- **架构性偏离（最关键）**：CEO 对「真自主」的定义是「AI Employee 自主判断现在是否应该发言；Leader 只负责状态/上下文/调度机会/预算/timeout/并发/防循环，不应替员工决定固定发言顺序」。当前实现中，**发言顺序由系统公式 + 字典序 tie-break 决定，员工不参与选择，Leader 也不直接排顺序**（Leader 只产出 9 种 outcome）。因此按 CEO 的严格定义，本实现**未实现「真自主」**；本裁定在「三选一」框架内将其归为 `PARTIALLY AUTONOMOUS`，并明确指出它与「真自主」的定义冲突点（见 §2.5）。

**固定顺序/固定脚本观感来源（X 处）**：

| 编号 | 机制 | 代码位置 | 触发条件 |
| --- | --- | --- | --- |
| A | 字典序 `employeeRef` tie-break（核心 #1） | `meeting_service.py:678` | 任意一回合内 ≥2 名候选人最高分相同 |
| B | 低相关性退化塌缩为固定交替（核心 #2） | `meeting_service.py:650-678` + `:1082` | 无点名、无归属权、角色/责任词与议题词无重叠 |
| C | 上一轮发言者 −20 确定性惩罚 | `meeting_service.py:667-669` | 任意多回合讨论（促成稳定交替） |
| D | 架构性偏离：员工从不自荐，发言人为公式选定 | `meeting_service.py:626-678`（选定）先于 `:924`（LLM 发言） | 全场景（结构性） |

> X = **2 处核心机制（A、B）**；C 为促成稳定交替的确定性惩罚；D 为架构性原因，说明为何只能判 `PARTIALLY` 而非 `AUTONOMOUS`。

---

## 二、机制裁定书（逐条 file:line 证据）

### 2.1 发言选择的完整代码路径

1. **候选评分（确定性，无 LLM）** — `meeting_service.py:626-678` `_candidate_evaluation`：
   - CEO/Leader 点名 `requested == company_ref` → `+100`（`:651-653`）；
   - 持有本轮新增事实/结果归属权 → `+40`（`:654-656`）；
   - 角色/责任与议题词重叠 → `min(30, 8 + len(relevant)*3)`（`:657-663`）；
   - 是 Leader → `+5`（`:664-666`）；
   - 上一轮已发言且未被点名 → `−20`（`:667-669`）；
   - 最高分 `≤0` 时 `noProgressCount++`，reason 写「当前没有可证明的新增相关性」（`:675`）。
2. **排序 + tie-break** — `meeting_service.py:678`：
   ```python
   return sorted(candidates, key=lambda item: (-item["score"], item["employeeRef"]))
   ```
3. **选定** — `meeting_service.py:1082`：`selected = candidates[0]`（取排序后第一名）。
4. **连发保护** — `meeting_service.py:1083-1088`：若第一名等于上一轮发言者且连发次数达上限且未被点名，则改选下一个 `score > 0` 者。
5. **员工 LLM 仅写内容** — `meeting_service.py:924-936` `_speaker_prompt`：在被选定者上生成「贡献内容」，**不决定谁发言**。
6. **Leader LLM 仅定 outcome** — `meeting_service.py:938-951` `_leader_prompt`：产出 9 种 outcome（`:1150-1157` 白名单），**不直接排发言顺序**；仅通过 `REQUEST_SPECIFIC_EMPLOYEE`（`meeting_service.py:1213-1220`）间接把 `requestedSpeakerRef` 注入下一轮候选（下一轮 +100）。

**结论**：发言人是「评分公式 → 排序 → 取第一」在 LLM 之前决定的；两次 LLM 调用都发生在选定之后（一次写内容、一次定走向）。这与「员工自主判断是否发言」的定义相悖。

### 2.2 机制 A：字典序 `employeeRef` tie-break（核心固定顺序来源 #1）

- 位置：`meeting_service.py:678`。
- 行为：当多名候选人的 `score` 相等时，排序的第二关键字是 `employeeRef` 字典序（`-item["score"]` 为主，`item["employeeRef"]` 为辅）。`employeeRef` 是参与员工的稳定 ID（创建会议时传入的 `participant_refs`，见 `meeting_service.py:293`、`_participants:93-109`），不会因为讨论内容或 LLM 而改变。
- 后果：**任何「平局」都由代码按 ID 字典序固定地选同一个人**，与讨论内容、与模型随机性都无关。这是一个纯粹的、可复现的代码固定偏好序。
- 平局多常见：只要两名非 Leader 员工在同一回合拿到相同正分（例如都因持有被引用事实 +40，或都因相同的词重叠 +11），就会触发。在议题术语与多人角色术语重叠度接近的真实会议中，平局是常态而非例外。

### 2.3 机制 B：低相关性退化塌缩为固定交替（核心固定顺序来源 #2）

在「无点名、无事实/结果归属权、角色/责任词与议题词无重叠」的退化场景下，逐回合推导（`meeting_service.py:650-678` + `:1082`，连发保护 `:1083-1088`）：

设 Leader=L（ref 排序无关），员工 E1、E2 且 `E1.employeeRef < E2.employeeRef`（字典序）：

- 回合 1（事件 `MEETING_STARTED`）：L=+5，E1=0，E2=0 → 选 L，`lastVisibleSpeakerRef=L`。
- 回合 2（Leader 产出 `CONTINUE_DISCUSSION` → `LEADER_REQUEST`）：上一轮=L，L=+5−20=−15，E1=0，E2=0 → 选 E1（平局按字典序，E1 在前），`lastVisibleSpeakerRef=E1`。
- 回合 3：上一轮=E1，E1=0−20=−20，E2=0，L=+5（L 非上一轮）→ 选 L，`lastVisibleSpeakerRef=L`。
- 回合 4：同回合 2 → 选 E1。
- …… 交替：`L → E1 → L → E1 → L → E1`。

由于 `maxTurns=6`（`meeting_service.py:38`），**在 6 回合内 E2 始终排在平局末尾、从未获得发言机会**。这是一个由代码（tie-break + 连发惩罚 + 轮次上限）强制产生的**固定顺序**，且结构性地排除了平等地位、仅因 ID 字典序靠后的员工。

触发条件：议题/事件词与参与员工角色·责任词无重叠（`_terms` 交集为空，`:657-660`）、且无 `requestedSpeakerRef`（`:645,651`）、无归属权匹配（`:654`）。在泛化议题 + 通用角色标题的会议中极易出现。

### 2.4 机制 C：上一轮发言者 −20 确定性惩罚（促成稳定交替）

- 位置：`meeting_service.py:667-669`。
- 行为：`company_ref == previous and not requested` → `score -= 20`。这是**确定性**的「近期发言抑制」，与内容无关，只与「上一轮是谁」有关。它与机制 A 的字典序 tie-break 叠加，使顺序在退化场景稳定成机械交替（见 §2.3），而非由相关性驱动的变化。

### 2.5 架构性偏离：员工从不自荐（机制 D）

- 选定发生在 `_candidate_evaluation`（`meeting_service.py:626-678`）这一**纯确定性函数**中，**早于**任何 LLM 调用（`_speaker_prompt` `:924`）。系统中**不存在任何「员工自荐 / 自认该发言」的步骤或持久化标志**：`turns[].candidates` 里只有系统算出的 `score` / `reasons` / `selected`，没有 `volunteered` 之类字段。
- 唯一由 Leader 影响的排序路径：`REQUEST_SPECIFIC_EMPLOYEE` 经 `leaderOutcome`（`meeting_service.py:1213-1220`）写入下一轮 `requestedSpeakerRef`，使该员工 +100（`:651-653`）。这属于「Leader 调度机会」范畴、符合 CEO 定义，但它是**强制单人点名**，不是自主。
- 因此：当前机制是「Leader/系统主导排序」，与 CEO 定义的「员工自主判断是否发言、Leader 不替员工定固定顺序」在结构上不一致。这是判 `PARTIALLY` 而非 `AUTONOMOUS` 的根本原因，也是未来若要达到「真自主」必须改造的点（例如引入员工自荐/意愿评估步骤）。

### 2.6 为什么不是 `NOT AUTONOMOUS`（deterministic round-robin）

- 代码中**没有** `(index+1) % n` 式固定循环；顺序会响应：
  - **议题相关性**（`:657-663`，随 `event_terms` 变化）；
  - **事实/结果归属权**（`:654-656`，随被引用 Work/Result/Evidence 的 `owner_ref` 变化）；
  - **CEO/Leader 点名**（`:651-653`，`@员工` 经 `add_message:366-377` 写入 `requestedSpeakerRef`）；
  - **Leader `REQUEST_SPECIFIC_EMPLOYEE`**（`:1213-1220` → 下一轮 +100）。
- 故它**不是**固定的 A→B→C→A 循环，与 `NOT AUTONOMOUS` 的严格定义（存在 deterministic round-robin）不符。这也与 2026-09-02 评审 §4 一致。

### 2.7 支持「部分自主」的正向证据（为何是 PARTIALLY 而非 NOT）

- Leader LLM 真实决定走向：`_leader_prompt` `:938-951` 的 9 种 outcome 由模型生成（`:1150-1157` 校验），可产出 `CONTINUE_DISCUSSION / REQUEST_EVIDENCE / UPDATE_PROPOSAL / NEEDS_CEO_DECISION / DISCUSSION_SUFFICIENT` 等，反映讨论状态而非固定脚本。
- 相关性加权随讨论内容变化（`:657-663`）：2026-09-02 评审 §4 的三员工实测中，Research 因「被选中的 Knowledge 与议题匹配其责任」先发言、无关 Finance 沉默——这是**内容驱动**而非 tie-break。
- CEO 离开后团队继续：`meeting_router.py:49-64` 的 `BackgroundTasks` 在 HTTP 响应后拥有进程内继续权，React 仅轮询持久化状态（2026-09-02 评审 §10）。说明讨论不依赖 CEO 每轮驱动，非「CEO 驱动轮询」。

综上：机制**部分**自主（走向与相关性由内容/模型驱动），但**发言顺序的选定**由确定性公式 + 字典序 tie-break 完成，并存在 §2.2–§2.3 的固定顺序观感机制 → **PARTIALLY AUTONOMOUS**。

---

## 三、可证伪的验收判据表（供 QA 跑完 E2E 后裁定）

所有字段均来自持久化数据：表 `strategy_meetings` 的 `orchestration_json`（JSON 路径以 `orchestration.` 前缀）、`timeline`（消息列表）、以及 `ai_usage_records`（`task_id`、`total_tokens`、`cost_amount`、`metering_status`、`occurred_at`）。

> 判定前提：先过 C1（确认用的是真实云模型）。C1 不过，则本次 E2E 对「自主权」验收无效（必须重跑真实云模型）。
> 区分「代码强制轮询」与「模型偶然类似轮询」的**金标准**是 C8（同输入重复运行不变性测试）。

| 判据 | 看哪个字段（表 / JSON 路径） | PASS（支持真自主） | FAIL（代码固定顺序/预设脚本） | 模型偶然行为（不算 FAIL） | 说明 |
| --- | --- | --- | --- | --- | --- |
| **C1 真实云模型证据** | `ai_usage_records` 中 `task_id` ∈ 各 `turn.taskRefs`；`metering_status='confirmed'` 且 `cost_amount > 0` | 确认记录数 ≥ `turnCount × 2`（每回合 1 次员工 + 1 次 Leader），且 `cost_amount>0` | 全部 `unknown` 或 `cost=0` → 用的是确定性本地 provider，本轮 E2E 作废 | 无 | 验收前提；不过则整张表作废 |
| **C2 平局 tie-break 是否固定** | `orchestration.turns[].candidates[].score` + `turns[].speakerRef` | 出现平局（≥2 人最高分相同）的回合很少；或平局时 `speakerRef` 不恒为字典序最小者（即顺序随内容变化） | **每一次**平局 `speakerRef` 都 = 平局集中字典序最小 `employeeRef`（即机制 A 恒定生效） | 单次孤立平局恰好按字典序解析，不足以定罪；需整场系统性重复 | 直接验证 §2.2 |
| **C3 退化塌缩固定交替** | `orchestration.turns[].speakerRef` 序列 + 各回合 `candidates[].score` | 内容丰富的会议里，不同员工发言顺序随议题变化；`maxTurns` 内所有参与者 ≥1 次发言 | 序列塌缩为严格重复模式（如 `L→E_小→L→E_小…`），且字典序靠后员工 0 次发言，且各回合最高分均 ≤5（无相关性/归属权区分） | 若某员工 `reasons` 显示「当前没有可证明的新增相关性」而沉默，属内容/模型合理，非代码固定 | 直接验证 §2.3 |
| **C4 顺序是否由公式而非员工自选** | `orchestration.turns[].candidates`（含 `score`/`reasons`/`selected`） | —（结构性事实） | 每回合 `speakerRef == candidates[0].employeeRef` 且 `selected` 由系统在 LLM 前设定、无任何 `volunteered` 标志 → 员工从不自荐 | 无（这是代码事实，不由运行时变化） | 验证 §2.5 架构性偏离；为「非真自主」的结构性证据 |
| **C5 换人是否由相关性/点名驱动** | `orchestration.lastVisibleSpeakerRef`、`consecutiveVisibleTurns`、`turns[].leaderOutcome`、`pendingEvents[].requestedSpeakerRef` | 换人能对应 `REQUEST_SPECIFIC_EMPLOYEE`/`REQUEST_EVIDENCE` 或分数因相关性/归属权明显拉开 | 换人**仅**因 −20 惩罚 + 字典序 tie-break 的机械交替，无任何分数/点名差异支撑 | 偶发因 Leader 随机产出 `REQUEST_SPECIFIC_EMPLOYEE` 而换人，属模型合理 | 验证 §2.4 |
| **C6 CEO 离开后团队继续** | `timeline` 中 CEO 离场后的事件 + `orchestration.status`/`operating_state` | CEO 不再发消息后，`BackgroundTasks` 仍持续追加 `turns`，讨论自主推进至 `DISCUSSION_SUFFICIENT`/`NEEDS_CEO_DECISION` | 每轮都需 CEO 重新触发 `advance` 才继续 → 非自主 | 无 | 验证 §2.7 / 2026-09-02 §10 |
| **C7 Leader outcome 多样性（非脚本）** | `orchestration.turns[].leaderOutcome` | outcome 跨 `{CONTINUE_DISCUSSION, REQUEST_SPECIFIC_EMPLOYEE, REQUEST_EVIDENCE, UPDATE_PROPOSAL, DISCUSSION_SUFFICIENT, NEEDS_CEO_DECISION}` 变化，反映讨论状态 | 同一内容下每次重跑 outcome 序列逐字节相同（固定脚本） | 短会议 outcome 种类天然有限 | 验证 §2.7 |
| **C8 同输入重复运行不变性（金标准）** | 两次独立运行的 `turns[].speakerRef` 序列 + `turns[].candidates.score` | 两序列在「可归因于 `leaderOutcome`/`requestedSpeakerRef` 差异」处不同（说明 Leader LLM 影响了顺序） | 两次使用**相同脚本化 CEO 输入 + 相同参与者/议题**的真实云模型运行，`speakerRef` 序列**逐字节相同**（证明顺序由代码固定、与模型无关） | 仅有内容措辞差异导致的细微不同，但顺序不变 → 仍指向代码固定 | 因 `_candidate_evaluation`（`:626-678`）不含 LLM/随机，顺序是其纯函数；同输入下不变即证顺序非模型自主 |

**裁定汇总规则（给 QA 终审）**：
- C1 不过 → 验收无效，重跑真实云模型。
- C8 = FAIL（同输入两跑顺序不变）且 C2/C3 = FAIL → **确证代码固定顺序**，本机制对「真自主」验收 FAIL。
- C8 = PASS（顺序随 Leader outcome 变化）但 C4 仍为结构性事实、C2/C3 偶发 → **部分自主**，维持 `PARTIALLY`，但明确不满足 CEO「员工自主判断」定义。
- C7 = FAIL 且 C6 = FAIL → 偏「非自主/脚本化」，需结合 C8 复判。

---

## 四、观察清单（E2E 过程中必须采集的原始证据）

QA 在 E2E 进行中须逐项留存原始证据（API 响应 + DB 快照），以便事后终审：

1. **每次 `advance` 后的完整 `orchestration` JSON**：每次 `POST .../meetings/{id}/advance`（或 CEO 消息/`choose_decision`/`sync` 触发的后台 `advance`）完成后，立即 `GET .../meetings/{id}` 抓取 `orchestration`，重点保留 `turns`（每回合的 `candidates` 全量含 `score`/`reasons`/`selected`、`speakerRef`、`leaderOutcome`、`taskRefs`）、`lastVisibleSpeakerRef`、`consecutiveVisibleTurns`、`noProgressCount`、`pendingEvents`。
2. **DB 快照 `strategy_meetings.orchestration_json`**：会议结束（或达 `DISCUSSION_SUFFICIENT`/`BLOCKED`）后整表导出，供离线裁定。
3. **DB 快照 `strategy_meetings.timeline`**：重建真实发言顺序与每句作者（`actorType`/`actorRef`/`kind`/`text`）。
4. **`ai_usage_records` 全量**：筛选本会议 `taskRefs` 对应记录，确认 `metering_status='confirmed'`、`cost_amount>0`、记录数 ≥ `turnCount×2`；并用 `turns[].taskRefs` 顺序（[speaker, leader]，`meeting_service.py:1163`）区分员工调用与 Leader 调用。
5. **CEO 消息原文与 `@员工` 提及**：记录每次 `add_message` 的 `text`，以及是否含 `@name`（经 `meeting_service.py:366-377` 写 `requestedSpeakerRef`）——用于判断是否触发 +100 点名。
6. **参与者清单与角色/责任原文**：导出 `participants` 的 `employeeRef`(id)、`role`、`responsibility`、以及 `orchestration.assignments` 的 `responsibilityKey`（`meeting_service.py:312-321`）。用于离线重算 `_terms` 重叠与字典序 tie-break，预测 `speakerRef` 并比对实测。
7. **议题/背景与 `context_refs`**：`title`/`background` 与 `context_refs`（KNOWLEDGE/WORK/RESULT/EVIDENCE 引用）。用于离线重算 `event_terms`（`:632`）与归属权 `owner_refs`（`:636-643`）。
8. **两次同输入独立运行**（C8 必需）：用**相同**脚本化 CEO 输入 + **相同**参与者/议题/上下文，在真实云模型下跑 **两遍**，分别留存两套 `turns[].speakerRef` 序列与 `candidates.score`。为隔离 tie-break，建议设计「中性议题」：CEO 不 `@` 点名、且不触发 `REQUEST_SPECIFIC_EMPLOYEE`（若触发则如实记录），使顺序唯一信号为相关性（内容固定）+ 字典序 tie-break。两遍顺序若逐字节相同 → 证顺序代码固定。
9. **`leaderOutcome` 与 `requestedSpeakerRef` 轨迹**：逐回合记录 `turns[].leaderOutcome` 与 `pendingEvents` 中 `LEADER_REQUEST` 的 `requestedSpeakerRef`（`:1217-1220`），用于把「Leader 驱动的换人」与「公式 tie-break 换人」分开。
10. **CEO 离场连续性证据**：记录 CEO 停止发消息后的时间戳与之后自动追加的 `turns`/`timeline` 事件，确认 `BackgroundTasks`（`meeting_router.py:49-64`）在无新 CEO HTTP 触发下继续推进。

> 采集粒度建议：上述 1–4、8 为**强证据**（缺任一项则 C8/C2/C3 无法裁定）；5–7、9–10 为**辅助证据**（用于离线复算与归因）。

---

## 五、终审裁定方法（如何用上述证据做代码层终审）

1. **离线重算 `_candidate_evaluation`**：用清单 6–7 的输入，按 `meeting_service.py:626-678` 逐员工重算 `score` 与 `reasons`，按 `:678` 排序，取第一（`:1082`）。若预测 `speakerRef` 与实测 `turns[].speakerRef` 逐回合一致 → 顺序确由公式 + 字典序 tie-break 决定（机制 A/B/D 成立）。
2. **不变性测试（C8）**：两次同输入真实云模型运行的 `speakerRef` 序列若逐字节相同，而两次 Leader 内容/model 采样不同 → 顺序与模型无关、由代码固定。这是「代码强制」与「模型偶然」的决定性分界。
3. **区分代码固定 vs 模型偶然**：代码固定顺序**可复现且内容无关**（同输入必同序）；模型偶然的「看似轮询」必然伴随 `leaderOutcome`/`requestedSpeakerRef` 的 LLM 差异（清单 9），且同输入重跑会变化。若重跑不变 → 非偶然。
4. **退化塌缩核验（C3）**：若清单 3 显示字典序靠后员工 0 次发言且各回合最高分 ≤5，结合清单 6–7 确认其角色词与议题无重叠 → 机制 B 成立，属代码固定顺序。
5. **综合落点**：以上若多数为「代码固定」，则本机制对「真自主」验收 FAIL，维持/下调为 `PARTIALLY`（本裁定结论）或据 C6/C7 复判；若 C8 显示顺序随 Leader outcome 实质性变化，则至少「部分自主」，但仍因 C4（员工不自荐）不满足 CEO 严格定义。

---

## 六、给工程的改造提示（非本次任务范围，仅供后续）

若要将本机制推进到 CEO 定义的「真自主」，最小改造方向（不在本次 review 范围，不修改代码）：
- 在 `_candidate_evaluation`（`:626-678`）之外引入「员工自荐/意愿」步骤：让每位候选员工经一次轻量 LLM 调用自主评估「我现在是否应发言、贡献是什么」，再以该意愿作为评分输入之一，而非纯由系统公式 + 字典序 tie-break 强排。
- 将 `:678` 的字典序 tie-break 改为「当平局时由 Leader 或轮值机制按相关性细分」或引入随机/轮转盐，避免 ID 字典序恒定胜出造成 §2.3 的结构性排除。
- 在 `turns[].candidates` 增加 `volunteered`/`selfNomination` 标志，使「员工自主判断」在持久化数据中可观测、可验收。

---

## 七、结论重申

- **三选一结论：`PARTIALLY AUTONOMOUS`**。
- 固定顺序观感来源：核心 2 处（A 字典序 tie-break `:678`；B 低相关性退化塌缩 `:650-678`+`:1082`），加 1 处确定性连发惩罚 C（`:667-669`），加 1 处架构性偏离 D（员工从不自荐，选定在 LLM 之前 `:626-678` vs `:924`）。
- 非 `NOT AUTONOMOUS`：无 `(i+1)%n` 固定循环，顺序响应相关性/归属权/点名（§2.6）。
- 非 `AUTONOMOUS`：发言顺序由确定性公式 + 字典序 tie-break 决定，员工不参与选择（§2.2/§2.5）。
- 按 CEO 严格定义（员工自主判断是否发言、Leader 不替员工定固定顺序），本实现**未实现「真自主」**；本次在「三选一」框架内判 `PARTIALLY AUTONOMOUS`，并附可证伪判据表（§三）与观察清单（§四）供真实云模型 E2E 终审。

`NO COMMIT`
`NO PUSH`
`REVIEW-MODE / READ-ONLY`
