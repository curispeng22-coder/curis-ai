# D2 Evolution Governor Sandbox 边界验证 (质量运行席)

- Date: 2026-07-07
- Reviewer seat: 质量运行席 (CONV-SEAT-QUALITY-001)
- Target: ADR-0021 + issues/046
- Verdict: PASS-WITH-NOTES

## A) Forbidden-scope compliance

**Verdict: PASS-WITH-NOTES**

ADR-0021 的 Forbidden Scope 以「Same as ADR-0016 Forbidden Scope, plus D2-specific」承袭 ADR-0016，并补充了 D2 专属项（沙箱运行期写权威库/SQLite、未经人工批准自动生产变更、解除人工审批闸、改动 `evaluate()` 决策策略、新增端点等）。逐项比对：

- 与 ADR-0016 Forbidden Scope 一致：解除人工审批闸、Employee CRUD/扩展、多智能体/抽象层、公司组织(L5)/ROI/经济(L6)/业务模块、复杂 UI、外部服务/渠道/密钥、在沙箱或 append-only 日志之外改动权威库/SQLite —— 均承袭或被 D2 专属项覆盖。
- 与 PROJECT_HANDOFF 禁止区(304–323)基本一致：ROI/economy、公司组织、Employee CRUD、多智能体/抽象/路由、业务模块、外部连接器/渠道/密钥/支付通知、复杂 UI/dashboard、向量库/embedding/外部/隐藏记忆、运行时提示集成超角色上下文、task-role 关联/任务证据附件、API 语义变更、持久化/模式变更、自动代码自改/生产变更无审批、Evolution Governor 策略削弱 —— 均由「承袭 ADR-0016」或 D2 专属项覆盖。
- 与 002 Non-Goals 一致：Company CRUD、Employee CRUD、多智能体、业务模块、ROI、Advanced UI、Uncontrolled architecture changes、Automatic code self-modification without approval —— 均未授权，D2 不触碰。

**Notes（轻微缺口，非阻断）：** ADR-0021（经 ADR-0016）未将 PROJECT_HANDOFF 禁止区中的两项**显式**逐条重列：
1. 「Architecture lock bypass, uncontrolled architecture changes, or Evolution Governor policy weakening」—— 其中「Evolution Governor policy weakening」已被 D2 专属项「Changing existing Evolution Governor decision policy beyond the sandbox substrate」覆盖，但「Architecture lock bypass / uncontrolled architecture changes」在 ADR-0021 禁止列表中无独立条目（仅间接由承袭链隐含）。沙箱只读 `list_architecture_locks()` 构建快照、不绕过锁，实际风险低，但列举应补齐以达严格一致。
2. 「Mock data or simulation substitution for release verification」—— PROJECT_HANDOFF 禁止，ADR-0021 未显式列出（沙箱使用真实 throwaway 副本而非 mock，实际不违反，但枚举缺失）。

结论：ADR-0021 **未许可**任何禁止区阻塞之物，亦未阻断任何闸门已授权之物；仅禁止列表相对 PROJECT_HANDOFF 在枚举层面存在上述轻微缺口，建议在接受前补列。

## B) Schema/contract fidelity

**Verdict: PASS**

逐项确认 ADR-0021 边界契约满足全部五点：

- (i) 仅写 OS temp 一次性目录、绝不写权威库/SQLite：`run()` step 1 用 `tempfile.mkdtemp(prefix="curis-sandbox-")`（不在项目/repo 下），step 6 明定「Zero writes to the authoritative repo or SQLite」。✓
- (ii) throwaway 副本精确回滚至原始快照：step 5「Rolls back the throwaway copy exactly: writes `state_rolledback.json` equal to the original `state_snapshot`」。✓
- (iii) 不改输入：`_apply_proposal` 产生新 dict（step 3「does not mutate the input snapshot」），且明确为纯函数（step 7）。✓
- (iv) 增量 `demonstrate()` 不改 `evaluate()` 决策逻辑：`evolution_governor.py` 中 `evaluate()`（16–129 行）的决策逻辑（STABILITY>OPTIMIZATION>EVOLUTION 阈值、`failure_rate`/`latency_increase`/`workflow_inefficiency`、lock 阻断、`do_not_evolve`/`postpone_evolution`/`evolve`）完整存在且未变更；`demonstrate()` 仅构建快照并调用 `GovernorSandbox.run()`，属增量封装，不触碰 `evaluate()`。✓
- (v) 不新增端点：ADR-0021「No API endpoint」小节 + 禁止项「API semantic changes (therefore no new endpoint in D2)」。✓

附加确认：`self.store.list_architecture_locks()` 在 `evaluate()` 第 41 行已使用，证明该接口在 store 上可用，`demonstrate()` 依赖成立。✓

## C) Safety tightness

**Verdict: PASS**

- 沙箱绝不导入或调用 Database/ResultStore 写路径：Invariant 明定「It never imports or calls `Database`/`ResultStore` write paths」，且全部写操作都在 `tempfile.mkdtemp` 之下。✓
- 生产变更仍需沙箱之外、显式人工审批路径、闸门未解除：`demonstrate()` 注释「Any real production mutation still requires the explicit human-approval path outside the sandbox (unchanged gate — D2 does not lift it)」；禁止项含「Automatic production mutation without explicit human approval」与「Lifting the human-approval gate for code self-modification」。✓
- 沙箱为纯演示基底，无生产副作用，与 ADR-0016 Sub-decision B「writes nothing to the authoritative repo or SQLite, and requires explicit human approval before any production mutation」一致。✓

## D) Verification plan completeness

**Verdict: PASS**

ADR-0021 Verification Plan 覆盖标准 diff + 禁止域扫描，且 slice-specific 断言齐全，全部要求项均命中：

- 标准守卫：`git diff --name-only HEAD -- backend frontend`、`git diff --check`、backend/app 禁止域关键字扫描。✓
- 抛到 OS temp 下：`throwaway_path` is inside the OS temp dir (not under the project/repo)。✓
- applied≠rollback 但 rollback==original 精确：`applied_state` differs from `rollback_snapshot`；`rollback_snapshot` equals the original input snapshot exactly。✓
- `_apply_proposal` 纯函数：does not mutate its input dict。✓
- 权威 DB 不变：`demonstrate()` 后权威 SQLite 文件 size/mtime 未变、无 evolution events 发出。✓
- `evaluate()` 行为不变：backend regression 通过、其自有测试仍通过。✓
- 证据结构含 `applied_state`、`rollback_snapshot`、`throwaway_path`、`rolled_back=True`。✓

无遗漏项。

## Known gaps / open questions

1. ADR-0021 禁止列表宜显式补列 PROJECT_HANDOFF 禁止区项「Architecture lock bypass / uncontrolled architecture changes」（当前仅经 ADR-0016 间接隐含；实际沙箱只读锁、不绕过，风险低）。
2. ADR-0021 禁止列表宜显式补列 PROJECT_HANDOFF 禁止区项「Mock data or simulation substitution for release verification」（实际沙箱用真实 throwaway 副本，不违反，但枚举缺失）。
3. 两项均非阻断性，建议产品规划席在接受时一并补列以闭环禁止域枚举。

## Next

若 PASS → 路由 产品规划席 接受边界；接受后 系统交付席 按 ADR-0021 实现。
