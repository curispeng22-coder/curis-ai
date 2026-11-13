# CURIS V1 — MEETING Employee 自我 Speak/Stay Silent 判断 最小改造设计

Status: Draft → Decision Locked (方案1, 2026-09-04)
Authority Class: REVIEW
Date: 2026-09-04
Owner: software-architect-2（高见远）
Re: T1 裁定 `docs/reviews/CURIS_V1_MEETING_AUTONOMY_MECHANISM_ADJUDICATION_2026-09-04.md`（结论 PARTIALLY AUTONOMOUS）
关联 Backlog: `V1-P1-015 MEETING ROOM PRODUCTIZATION CLOSURE`
代码基线: `backend/app/meeting_service.py`（1302 行，`MeetingService`）、`backend/app/api/meeting_router.py`、`backend/app/main.py:5559`
用户选择: **Option B**（不接受降低验收标准；不做大规模重构、不另开改造单）

---

## 0. 设计立场与红线

- 本文件为**设计稿（Draft）**，仅落盘，不实现。本次**不写任何业务代码、不修改 `meeting_service.py` 或其他文件**。
- 维持 `IMPLEMENTED / PARTIAL` 验收标准不降低；本设计为把 T1 裁定的「员工从不自我判断」缺口补成「员工具备 Speak/Stay Silent 自我判断能力」的最小路径。
- 范围仅限 Meeting 发言门控，不触及 CEO Desk / Organization Center / Knowledge Library / 视觉 / 导航。
- 改造须经审阅通过后，由工程师另行实现（不在本文件范围内）。

---

## (a) 当前机制确认：为什么员工从不自我判断

逐条 `file:line` 证据（均来自 `meeting_service.py`）：

1. **候选评分是确定性公式，无 LLM** — `_candidate_evaluation:626-678`：
   - CEO/Leader 点名 `requested == company_ref` → `+100`（`:651-653`）；
   - 持有本轮新增事实/结果归属权 → `+40`（`:654-656`）；
   - 角色/责任与议题词重叠 → `min(30, 8 + len(relevant)*3)`（`:657-663`）；
   - 是 Leader → `+5`（`:664-666`）；
   - 上一轮已发言且未被点名 → `−20`（`:667-669`）；
   - 最高分 `≤0` → `noProgressCount++`，reason 写「当前没有可证明的新增相关性」（`:675`）。
2. **排序 + 字典序 tie-break** — `:678`：
   ```python
   return sorted(candidates, key=lambda item: (-item["score"], item["employeeRef"]))
   ```
   平局时由 `employeeRef` 字典序恒定选同一人，与内容/模型无关（T1 机制 A）。
3. **低相关性坍缩** — `:650-678`：当无点名/无归属权/角色词与议题无重叠，非 Leader 分=0、Leader=5→−15，顺序塌缩为固定交替，字典序靠后员工被结构性排除（T1 机制 B）。
4. **连发惩罚** — `:667-669`：上一轮发言者 `−20`，确定性机械交替（T1 机制 C）。
5. **员工 LLM 仅在 speaker 选定后写内容** — `_speaker_prompt:924-936`，在 `advance():1092-1095` 被调用，输入是**已被选定的** `selected["employeeRef"]`。员工没有「我要不要发言」的入口。
6. **Leader LLM 仅定 outcome** — `_leader_prompt:938-951`，产出 9 种裁决（`:1150-1157` 白名单），不直接排发言顺序。
7. **编排循环** — `advance():1002-1252`：每轮 `for _ in range(maxTurns)`（`:1050`）中，`event = pending.pop(0)`（`:1065`）→ `candidates = self._candidate_evaluation(...)`（`:1066`）→ `selected = candidates[0]`（`:1082`）→ 连发保护（`:1083-1088`）→ 选定标记（`:1089`）→ `_run_employee(speaker)`（`:1092`）→ `_run_employee(leader)`（`:1139`）。

**结论**：`speaker` 在**任何 LLM 发言/判断调用之前**已由「确定性评分公式 + 字典序 tie-break」固定（`_candidate_evaluation:626-678` → `:678` → `:1082`）。系统中**不存在员工自荐（should_speak）或自认沉默（stay silent）的判断入口**；`turns[].candidates` 只有系统算出的 `score`/`reasons`/`selected`，无 `volunteered`/`selfJudgment` 字段。这直接违反产品要求 #2、#4、#5、#7。

---

## (b) 最小改造方案

### b.1 设计目标与满足度映射

在 `speaker` 候选排序**之前**，为**每个有资格的员工**调用一次轻量 LLM「我是否应发言？」门控：

- 输入覆盖 8 类判断依据：Role / Responsibility / Current Work / Meeting Context / Existing Discussion / Evidence / Other Employees' opinions / Potential Contribution（要求 #3）。
- 员工输出结构化：`{should_speak: bool, contribution: str, confidence: float, reason: str}`。
- 仅 `should_speak=True` 的员工进入 `_candidate_evaluation` 排序；`should_speak=False` 的员工**显式记录沉默理由**（要求 #4 主动发言、#5 保持沉默）。
- 保留 Leader 对状态/预算/安全边界/9 种裁决的最终权（`_leader_prompt` 不变）（要求 #1）。
- 门控在每轮 `advance` 中对每个员工**重新执行** → 天然支持「因他人新观点/Evidence 重新判断并再次介入」（要求 #6）。
- `_candidate_evaluation` 降为**仅对自荐员工排序的次级信号**，不再单独决定「谁有资格发言」→ 满足要求 #7（最终发言不再仅由 Leader 相关性分数决定）。

### b.2 新增 / 修改函数签名

**新增方法 1（门控执行）** — 置于 `_leader_prompt:951` 之后：
```python
async def _employee_self_judgment(
    self, meeting: dict, assignment: dict, event: dict, context: dict
) -> dict[str, Any]:
    """为每个员工在候选排序前做轻量 Speak/Stay-Silent 自我判断。
    返回 {should_speak: bool, contribution: str, confidence: float, reason: str, usage: dict, taskRef: str}。
    """
    prompt = self._self_judgment_prompt(context, assignment)
    result = await self._run_employee(
        meeting, assignment, event=event, purpose="self-judgment",
        prompt=prompt, expected_type="meeting-self-judgment",
    )
    parsed = result["parsed"]
    return {
        "should_speak": bool(parsed.get("should_speak")),
        "contribution": str(parsed.get("contribution") or ""),
        "confidence": float(parsed.get("confidence") or 0.0),
        "reason": str(parsed.get("reason") or ""),
        "usage": result["usage"], "taskRef": result["taskRef"],
        "accepted": result["accepted"],
    }
```

**新增方法 2（prompt 模板）** — 同区域：
```python
def _self_judgment_prompt(self, context: dict, assignment: dict) -> str:
    # 组装 8 类依据（见 b.3），要求模型仅输出 JSON：
    # {should_speak: bool, contribution: str, confidence: float, reason: str}
```

**修改 1 — `advance()` 插入门控（精确位置）**：在 `:1065` `event = pending.pop(0)` **之后**、`:1066` `candidates = self._candidate_evaluation(...)` **之前**插入：
```python
# ---- Employee 自我判断门控（T1 改造：要求 #2/#4/#5/#6）----
self_judgments: dict[str, dict] = {}
turn_silences: list[dict] = []          # 仅在本回合完成时才持久化，保证 Restart 幂等
for emp_ref in meeting["participants"]:
    if emp_ref == meeting["leader_employee_id"]:
        continue                         # Leader 不自我提名，Leader 负责编排
    emp_assignment = assignments[emp_ref]
    gate_ctx = self._bounded_context(meeting, event, emp_ref, emp_assignment)  # 复用 :680-727，已含 Recent/Knowledge/Work/Result/Proposal
    judgment = await self._employee_self_judgment(meeting, emp_assignment, event, gate_ctx)
    self._merge_usage(state, judgment["usage"])               # 计入预算（见 (c)）
    if not judgment["accepted"]:
        return self._view(self._finish_advance(meeting, state, status="BLOCKED", outcome="BLOCKED",
            reason="员工自我判断模型调用或结果合同验证失败。", pending=pending))
    self_judgments[emp_ref] = judgment
    if not judgment["should_speak"]:
        turn_silences.append({
            "employeeRef": emp_ref, "eventId": event["eventId"],
            "confidence": judgment["confidence"], "reason": judgment["reason"],
            "evaluatedAt": _now(),
        })
```

**修改 2 — 候选过滤（紧接 `:1066` 之后）**：
```python
candidates = self._candidate_evaluation(meeting, event, assignments)
# 仅保留自我提名（should_speak=True）的候选；满足要求 #7（Leader 相关性分不再单独决定资格）
candidates = [c for c in candidates if self_judgments.get(c["employeeRef"], {}).get("should_speak", False)]
```
> `_candidate_evaluation` 本身**不修改**（最小改动），仅在其输出上做前置过滤。其 `score` 降级为「自荐员工之间的次级排序/再判断信号」。

**修改 3 — 沉默记录持久化（在 `:1167` 完成回合处）**：将 `turn_silences` 挂到本回合 turn 记录，并在 `state["silences"]` 上追加（仅在回合 COMPLETED 时写入，保证 Restart 不产生孤儿沉默/重复发言）：
```python
turn = {
    "turnId": f"meeting-turn-{uuid4()}", "event": event,
    "candidates": candidates, "speakerRef": selected["employeeRef"],
    "selfJudgments": self_judgments,          # 评审证据：每人 should_speak/confidence/reason
    "silences": turn_silences,                # 评审证据：沉默者及其理由（要求 #5）
    "leaderRef": meeting["leader_employee_id"], "leaderOutcome": outcome,
    ...
}
state["turns"] = [*state.get("turns", []), turn]
state["silences"] = [*state.get("silences", []), *turn_silences]   # 仅此处持久化
```

**修改 4 — `expected_type` 白名单**：`_run_employee` 在 `:831` 校验 `parsed.get("resultType") == expected_type`。需新增 `"meeting-self-judgment"` 到既有分发（与 `:1094` `meeting-contribution`、`:1142` `meeting-leader-evaluation` 并列）；prompt 要求模型返回对应 `resultType` 与字段。属小改动。

### b.3 `_self_judgment_prompt` 要点（覆盖 8 类依据）

```
你是会议参与者，角色：{role}，责任：{responsibility}。
请基于以下依据自行判断「我现在是否应该发言」：
1) Role / Responsibility：{role} / {responsibility} / {responsibilityKey}
2) Current Work：{你的 responsibilityRouting 状态 + meeting.work_refs/result_refs 摘要}
3) Meeting Context：{title} / {background} / 当前事件文本
4) Existing Discussion：{最近 ≤10 条 timeline MESSAGE（含 EMPLOYEE 发言）}
5) Evidence：{context_refs 中 EVIDENCE/RESULT + leader proposal.evidenceRefs}
6) Other Employees' opinions：{timeline 中其他 EMPLOYEE 的 MESSAGE 观点}
7) Potential Contribution：你若发言能带来的新东西（新事实/专业判断/风险/反对/Evidence 请求或引用/方案修改/明确问题）
仅当你能带来上述「新增值」且非总结前文、客套或只说同意时，should_speak=true；否则 false 并给 reason。
输出 JSON：{"resultType":"meeting-self-judgment","should_speak":bool,"contribution":str(≤200),"confidence":float[0,1],"reason":str(≤200)}
```
- 该门控为轻量调用：输入为已有 `_bounded_context`（`:680-727` 已含 Recent/Knowledge/Work/Result/Proposal/Decision），无需新增上下文构建；建议低 temperature 以稳定 bool 输出。
- 复用 `_bounded_context` 即可满足依据 3–6；依据 1–2 来自 `assignment`；依据 7 由模型在 `contribution` 中自述。

### b.4 与 `_candidate_evaluation` 的关系

- **关系：前置过滤（pre-filter），非取代**。门控决定「谁有资格发言」（员工自主）；`_candidate_evaluation` 仅对自荐集合做次级排序（其 `score` 仍用于 tie-break/次序，但不再决定资格）。
- 可选增强（非必须，留待评审决定）：将 `confidence` 纳入 `:678` 的排序键（如 `key=lambda c:(-(c["score"]+confidence_bonus), ...)`），进一步削弱字典序 tie-break 的固定观感。本设计默认**不改 `:678`**，先以「前置过滤」满足要求 #2/#4/#5/#6/#7。

### b.5 最小文件清单

| 文件 | 改动类型 | 内容 |
| --- | --- | --- |
| `backend/app/meeting_service.py` | 修改 | 新增 `_employee_self_judgment`（~`:951` 后）、`_self_judgment_prompt`；`advance()` 插入门控循环（`:1065` 后）+ 候选过滤（`:1066` 后）+ 沉默持久化（`:1167`）；`expected_type` 白名单加 `meeting-self-judgment`（`:831` 附近）；`LIMITS`（`:37-45`）数值调整（见 (c)） |
| 无新增文件 | — | prompt 与门控同文件内聚，保持最小改动 |

> 若团队偏好 prompt 外置，可另增 `backend/app/meeting_prompts.py`，但非必须。

---

## (c) 对现有 runtime 影响评估

### c.1 CEO 离场 / 回归、Decision Gate、Work/Result、Restart 幂等

- **不受影响**：门控是 `advance()` 回合循环内（`:1050-1168`）的纯前置过滤，不改变事件流、`decision_ref` 处理（`:1016-1048`）、`leaderOutcome` 9 种裁决、或 `_finish_advance`。CEO 离场后 `BackgroundTasks`（`meeting_router.py:49-64`）继续、Decision Gate（`NEEDS_CEO_DECISION`）、Work/Result 回写链路完全保留。
- **Restart 幂等**：门控调用经 `_merge_usage`（`:962`）计入 `state["usage"]`/`providerCallCount`，但 state 仅在 `_save` 时落库（`:1079/1126/1167` 等）。若进程在门控后、回合完成前崩溃，未落库的 usage/沉默不持久化；Restart 从 DB 重载 `state`（`:1010/1051`）重新跑门控 → **不产生重复发言/重复 Work/孤儿沉默**。沉默记录 `turn_silences` 仅在本回合 COMPLETED（`:1167`）时挂入 `turn` 并追加 `state["silences"]`，与现有发言/Work 幂等模型一致。`release_key` 机制（`meeting:{id}:{event}:{purpose}:{employeeRef}`，`:729-753`）不涉及门控（门控不产生 Work/Result），无需改动。

### c.2 并发与单事务幂等

- `_claim_advance`（`:893-922`）单事务活跃 claim 不变；门控运行在已 claim 的 advance 内，并发 advance 仍被串行化。无新增并发风险。

### c.3 预算上限（`LIMITS:37-45`）影响与建议数值

新增「每轮每员工一次 LLM 调用」会冲击 `maxProviderCalls`（当前 12）。`_budget_reason`（`:965-980`）以 `providerCallCount`（`:962` 递增）为硬上限闸门：

- **每轮调用数** = 门控(E 名员工) + 发言(1) + Leader(1) = `E + 2`。3 员工 E2E → 5 次/轮；`maxTurns=6` → 上限需 ≥ `6 × 5 = 30`。
- **Token/Cost**：门控为轻量（短 prompt + bool/短文本输出，约 200–400 tok/次），主要开销仍是 speaker+leader 贡献。当前 `maxConfirmedTokens=8000` / `maxConfirmedCost="1.00"` 在 30 次调用下会偏紧。

**决策（2026-09-04 用户拍板，锁定 = 方案 1）**：仅上调全局 `maxProviderCalls`，token/cost 预算**保持**（用户明确：成本/token budget 仍须独立生效）。不引入第二套预算系统。

| 项 | 改动 | 锁定数值 |
| --- | --- | --- |
| `maxProviderCalls` | 12 → **30**（**全局** provider call 上限，非每员工 30） | 30 |
| `maxConfirmedTokens` | **保持**（token budget 独立生效） | 8000（不变） |
| `maxConfirmedCost` | **保持**（cost budget 独立生效） | "1.00"（不变） |
| `maxTurns` | 保持 | 6 |
| `maxConsecutiveTurns` | 保持 | 1 |
| `maxNoProgress` | 保持（不借调高以掩盖 provider call 增长） | 2 |
| `maxElapsedSeconds` | 保持 | 300 |

**用户 9 条硬约束（实现须逐条满足）**：
1. 30 是「全局 provider call 上限」，不是给每个 Employee 单独 30 次。
2. Speak/Stay Silent gate 必须计入这个全局 budget（providerCallCount）。
3. Leader call 必须计入这个全局 budget。
4. 实际 Employee response 也必须计入这个全局 budget。
5. 任何情况下不能绕过全局 budget。
6. 达到 budget 后必须安全停止，而不是继续调用。
7. UI / Meeting state 要正确反映 budget stop（复用既有 BLOCKED 路径与 reason）。
8. 不修改 maxRounds 等其他边界来掩盖 provider call 增长。
9. 成本/token budget 仍然必须独立生效（保持 8000 / "1.00"）。

**STAY_SILENT 是一等合法结果**：每个 Employee 返回 `SPEAK` 或 `STAY_SILENT`；`STAY_SILENT` 不得被当作异常/失败，仅 `SPEAK` 的 Employee 进入后续 response generation；Leader 负责 orchestration 但**不能**替 Employee 做最终 Speak/Stay Silent 判断。

> 注：30 次调用在 8000 token 预算下可能先触及 token budget 而提前 BLOCKED——这是 token budget 作为独立安全边界正常生效，非缺陷；若 E2E 实测因此过早停止，再据 `ai_usage_records` 校准（不在本次最小改动范围）。

- **不突破的可接受性**：无论方案 1/2，门控调用都须进入 `ai_usage_records`（用量/成本真值），且受 `maxElapsedSeconds`（`:970`）与 token/cost 上限约束；不得为门控豁免成本计量（否则违反 2026-09-02 评审 §13 用量真值原则）。
- **`maxNoProgress=2`**：若员工连续自认沉默导致 `candidates` 过滤为空，走 `:1067` 的 `not candidates` 分支 → `noProgressCount++`，达 `maxNoProgress` 后自然停止（`:1070-1077`）。这正是要求 #5「可保持沉默」的正确终态，无需调整常量。

---

## (d) 测试方案

### d.1 单元（mock 员工判断，禁用真实模型）

| 用例 | 断言 | 映射要求 |
| --- | --- | --- |
| 门控 `should_speak=True` → 进入 `_candidate_evaluation` 排序 | mock 返回 True 的员工出现在 `candidates` 且 `selected` 可为其 | #2/#4 |
| 门控 `should_speak=False` → 被过滤 | mock 返回 False 的员工**不**进入 `candidates`；其 `reason` 写入 `turn.silences`/`state["silences"]` | #5 |
| 全员沉默 → 无进展停止 | 所有员工 mock False → `noProgressCount` 递增至 `maxNoProgress` 后 `DISCUSSION_SUFFICIENT(NO_PROGRESS)` | #5 |
| 再介入 | 轮 1 员工 X mock False（沉默），轮 2 注入「他人新 Evidence」后 X mock True → X 进入候选并发言 | #6 |
| 连发保护仍生效 | X 连续 True 且被选定，下一轮仍受 `:1083-1088` 连发保护 | #1（Leader 安全边界保留） |
| 预算闸门 | mock 门控计数使 `providerCallCount` 超 `maxProviderCalls` → `_budget_reason` 返回上限原因并 `BLOCKED` | 预算安全（§c.3） |
| 失败合同 | mock 门控 `accepted=False` → 走 `BLOCKED` 且不产生假发言/Work | 失败真值（2026-09-02 §15） |

### d.2 集成（真实云模型；**禁用** mock / deterministic provider）

环境：fresh packaged Desktop + 合法真实模型（沿用 T5 E2E 环境），3+ 员工，isolated SQLite。

| 用例 | 断言（看持久化字段） | 映射要求 |
| --- | --- | --- |
| 员工可主动发言 | 至少 1 名员工 `turn.speakerRef` 对应其 `selfJudgments[ref].should_speak=True`，且 `contribution` 非空 | #2/#4 |
| 员工可保持沉默 | `turn.silences` 中至少 1 条 `should_speak=False` 且 `reason` 合理；该员工当轮未出现在 `speakerRef` | #5 |
| 员工可因新观点重新介入 | 注入 `REQUEST_EVIDENCE`/新 RESULT 事件后，此前沉默员工在后续 `turn.selfJudgments[ref].should_speak` 变为 True 并发言 | #6 |
| 最终发言非仅由 Leader 相关性分决定 | 存在 `speakerRef` 其 `_candidate_evaluation` `score` 非最高，但因他人沉默被自荐集「挤出」→ 证明资格由员工自决（要求 #7） | #7 |
| 判定不退化成固定轮询 | 两次同输入真实云模型运行，`speakerRef` 序列不必相同（因 self-judgment 是模型输出）；且 `turns[].silences` 证明沉默是员工自决而非公式排除（对照 T1 判据 C2/C3/C8） | #7（反驳 T1 机制 A/B） |
| CEO 离场继续 | CEO 停发消息后 `BackgroundTasks` 仍追加 `turns` 至 `DISCUSSION_SUFFICIENT`/`NEEDS_CEO_DECISION` | #1 |
| 预算合规 | `ai_usage_records` 中本会议 `metering_status='confirmed'`、`cost_amount>0`、调用数 ≤ `maxProviderCalls`（方案 1）或 `gateCallCount ≤ maxGateCalls`（方案 2）；`maxElapsedSeconds` 内完成 | §c.3 |
| Restart 幂等 | 进程中途杀掉后同 event 重启：发言/Work/`silences` 计数不重复（`turnCount` 不变、无重复 `speakerRef` 同 event） | 幂等（§c.1） |
| 并发 | 并发两次 `advance` → 仅 1 个活跃 claim 胜出，无重复发言 | 并发（§c.2） |

### d.3 断言 → 7 条产品要求 映射总表

| 产品要求 | 覆盖测试 |
| --- | --- |
| #1 Leader/Orchestrator 管状态/上下文/预算/调度/安全边界 | 连发保护用例、预算闸门用例、CEO 离场继续用例（`_leader_prompt` 不变） |
| #2 员工自身具备 Speak/Stay Silent 判断 | 门控 True/False 单元 + 主动发言集成 |
| #3 判断依据含 8 类 | `_self_judgment_prompt` 要点 + 集成中 `turn.selfJudgments` 字段可观测 |
| #4 员工可主动发言 | 主动发言集成 |
| #5 员工可保持沉默 | 沉默记录单元 + 全员沉默停止 + 保持沉默集成 |
| #6 因他人新观点/Evidence 重新介入 | 再介入单元 + 重新介入集成 |
| #7 不允许固定轮询/仅由 Leader 相关性分决定 | 非仅相关性分集成 + 不退化成固定轮询集成（对照 T1 C8） |

---

## (e) 风险与开放问题（供审阅）

1. **门控成本**：方案 1 把 `maxProviderCalls` 提到 30，真实云模型下实际 token/cost 需首跑后校准；若超 `maxConfirmedCost` 会提前 `BLOCKED`，需在 E2E 中观测并回调数值。
2. **门控稳定性**：`should_speak` 为 bool，低 temperature 仍可能偶发翻转；要求 #6 依赖此翻转，但要求 #7（非固定顺序）也受益于翻转——需在集成中验证两次同输入运行的 `speakerRef` 序列差异可归因于 self-judgment（而非 T1 的确定性 tie-break）。
3. **`_candidate_evaluation` 是否保留**：本设计保留其作为次级排序。若审阅认为应彻底移除以消除字典序 tie-break（T1 机制 A），可改为「自荐员工按 `confidence` 降序 + 连发保护」纯模型驱动排序——属更大改动，本设计不采用（遵循 Option B 最小改动）。
4. **`expected_type` 合同**：需确认 canonical Employee execution 能按 `meeting-self-judgment` 返回结构化 JSON；若既有执行器强制 `general-business-result`，需在 `_run_employee` 分发（`:831/876`）补一路轻量解析。

---

## 结论（Decision Locked, 2026-09-04）

本设计在**不改 `_candidate_evaluation` 公式、不破坏 CEO 离场/Decision Gate/Work-Result/Restart 幂等/并发** 的前提下，于 `advance()` 候选排序前插入「每员工轻量 LLM 自我判断门控」，使发言资格由员工自主决定（满足 #2/#4/#5/#6/#7），Leader 9 种裁决与预算安全边界保留（#1）。最小改动集中于 `meeting_service.py` 单文件（新增 2 方法 + 3 处插入 + `expected_type` 扩展 + `LIMITS` 数值）。

**预算决策（已锁定）**：`maxProviderCalls: 12 → 30`（全局上限，非每员工）；`maxConfirmedTokens` 保持 8000、`maxConfirmedCost` 保持 "1.00"（用户：token/cost budget 仍须独立生效）；`maxTurns=6`/`maxConsecutiveTurns=1`/`maxNoProgress=2`/`maxElapsedSeconds=300` 全部保持；不引入第二套预算系统。门控/Leader/Response 三次调用均计入全局 `providerCallCount`，达 30 即安全 STOP。`STAY_SILENT` 为员工一等合法结果。

设计稿完，进入实现阶段（交工程师寇豆码）。
