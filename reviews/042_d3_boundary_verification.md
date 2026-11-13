# D3 Append-Only Evolution Event Log 边界验证 (质量运行席)

- Date: 2026-07-07
- Reviewer seat: 质量运行席 (CONV-SEAT-QUALITY-001)
- Target: ADR-0020 + issues/047
- Verdict: PASS-WITH-NOTES

## A) Forbidden-scope compliance

**Verdict: PASS**

ADR-0020 的 Forbidden Scope 以「Same as ADR-0016 Forbidden Scope, plus:」为基底，并逐条覆盖了 issues/047 Forbidden Scope 的全部条目（删/改既有持久表、事件日志 UPDATE/DELETE、替代 source-of-truth 文件、Employee CRUD/多智能体/智能体抽象、复杂 UI、超出新增只读端点的 API 语义变更、ROI/经济/L5/L6、超出角色上下文的运行时提示集成、任务-角色关联/任务证据附件、向量库/embeddings/外部记忆、自动演化行为变更/自动代码自修改、未来层实现）。逐项比对 PROJECT_HANDOFF 禁止区 (line 304–323) 与 002 Non-Goals：

- 与 ADR-0016 Forbidden Scope 一致：未解除 human-approval gate，未引入外部服务/密钥/通道。
- 与 PROJECT_HANDOFF 禁止区一致：`evolution_events` 属「explicitly approved slices」下的 additive schema，不触碰「Persistence/schema changes except explicitly approved slices」；新增的 `/api/evolution-events` 属「explicitly approved additive endpoints」，不违反「API semantic changes beyond explicitly approved additive endpoints」。
- 与 002 Non-Goals 一致：未引入 Company/Employee CRUD、多智能体、业务模块、ROI、高级 UI、未受控架构变更、未经批准的自动代码自修改。

未发现「ADR-0020 许可了禁止区阻止的事项」或「ADR-0020 阻止了 gate 已授权的事项」的冲突。

**Minor note（见 Known gaps #1）**：ADR-0020 的 Forbidden Scope 列表是 ADR-0016 + issues/047 的部分重述，未显式复述 PROJECT_HANDOFF 禁止区中「架构锁绕过 / 未受控架构变更 / Evolution Governor 策略削弱 / 用 mock 数据或仿真替代发布验证」等条目。这些在意图上被继承而非被许可，不构成冲突，但建议显式引用以杜绝漂移。

## B) Schema/contract fidelity

**Verdict: PASS**

- **Schema 与 issues/047 Allowed Scope 匹配**：`evolution_events(event_id, correlation_id, event_type, payload, created_at)` 覆盖了 issues/047 要求的 event type、payload、correlation id、timestamp 四要素。✓
- **(i) 不删不改既有表**：计划在 `database.py` `initialize()` 的 `executescript` 中以 `create table if not exists evolution_events (...)` 追加，现有 `executescript` 模式完全容纳（database.py:30 起）；明确声明「No existing table is dropped, altered, or given an UPDATE/DELETE path」。✓
- **(ii) EvolutionEventLog 仅插入、无 update/delete**：`record()` 标为 INSERT ONLY，`get_by_correlation_id()` / `get_all()` 标为 SELECT ONLY；并设定不变量——代码层断言类无 update/delete 属性、模块内无 UPDATE/DELETE SQL 字符串。✓
- **(iii) correlation_id 串联 proposal→simulation→decision→rollback**：Governor `evaluate()` 每次运行生成单一 `correlation_id`，传入三次 store save 并自行 emit `proposal` 事件；`lock` 事件携带传入 `save_architecture_lock` 的 `correlation_id`（caller-supplied）。五类事件均可关联。✓
- **(iv) 五种事件类型均有真实写路径**：已核对 `result_store.py` 中四个 save 方法均存在——`save_evolution_simulation` (result_store.py:653)、`save_rollback_record` (result_store.py:698)、`save_evolution_decision` (result_store.py:736)、`save_architecture_lock` (result_store.py:627)；并核对 `evolution_governor.py` 的 `evaluate()` 确实调用了其中三个 save（evolution_governor.py:77/95/105）并构建 proposal（evolution_governor.py:42）。`proposal` 由 governor 自行 emit，`simulation`/`decision`/`rollback` 由三个 save 经 `_emit` 写出，`lock` 由 `save_architecture_lock` 写出——五种类型均有真实写路径。✓

## C) Injection tightness & backward compatibility

**Verdict: PASS**

- `ResultStore.__init__(self, database, event_log=None)` 与 `EvolutionGovernor.__init__(self, store, event_log=None)` 均为**追加可选关键字参数**，未改动既有必需位置参数 `database` / `store`。旧测试 `ResultStore(database)` / `EvolutionGovernor(store)` 构造签名行为不变。✓
- `_emit` 守卫 `self.event_log is not None and correlation_id is not None`；当 `event_log=None` 或旧调用未传 `correlation_id` 时均不 emit，回归风险为零。✓
- 计划未要求修改两个构造函数的必需签名。✓

**Minor note（见 Known gaps #2）**：计划在 Injection 段声明 `orchestrator.py` 构造 `EvolutionGovernor(store, store.event_log)`，这要求 `ResultStore` 在 `__init__` 中设置 `self.event_log = event_log` 属性。当前文字仅描述签名 `(self, database, event_log=None)`，未显式声明会保存为 `self.event_log`。此为边界措辞缺口，意图明确，实现时应确认该属性存在。

## D) Verification plan completeness

**Verdict: PASS-WITH-NOTES**

ADR-0020 的 Verification Plan 覆盖了标准 diff 守卫（`git diff --name-only HEAD -- backend frontend`、`git diff --check`、对改动 backend/app 文件的 forbidden-scope 扫描）以及全部 slice-specific 断言：

- `evolution_events` 表在 `database.initialize()` 后存在 ✓
- `EvolutionEventLog` 无 update/delete 方法（仅插入不变量）✓
- `record` 插入、`get_by_correlation_id` 返回、payload 往返 ✓
- 同一 `correlation_id` 多事件同返、不同 `correlation_id` 不串 ✓
- `ResultStore`（带 event_log）emit `lock`/`simulation`/`decision`/`rollback` 并携带所供给 `correlation_id` ✓
- `EvolutionGovernor.evaluate()` emit `proposal`/`simulation`/`decision`/`rollback` 共享单一 `correlation_id`（从返回 dict 读取）✓
- 后端回归通过（event_log 为 None 时无行为变化）✓

所要求的七项 slice-specific 断言（表存在、无 update/delete 方法、record/get 往返、correlation 关联、store 级 emit、governor 级共享 correlation_id emit、回归通过）均已覆盖。

**Minor note（见 Known gaps #3）**：禁止区扫描在 ADR-0020 中仅为注释 `# forbidden-scope keyword scan on changed backend/app files`，未像 ADR-0016 Verification Plan 那样给出显式正则（如 `rg -n "Employee CRUD|..." `）。建议直接复用 ADR-0016 的显式关键词正则，避免实现期扫描口径漂移。

## Known gaps / open questions

1. **（A 文档）** ADR-0020 Forbidden Scope 应显式引用 PROJECT_HANDOFF 禁止区中与本切片相关的剩余条目（架构锁绕过 / 未受控架构变更 / Governor 策略削弱 / mock 或仿真替代发布验证），以与「Same as ADR-0016」基底形成完整闭环。当前为继承而非冲突，属低风险文档加固。
2. **（C 措辞）** Injection 段应明确 `ResultStore.__init__` 设置 `self.event_log = event_log`，否则 `orchestrator.py` 的 `store.event_log` 引用缺少边界依据。
3. **（D 完备性）** Verification Plan 的 forbidden-scope 扫描应给出 ADR-0016 同款的显式关键词正则，而非仅注释。

以上均不阻断边界接受，归为接受后实现期的边界澄清项。

## Next

若 PASS → 路由 **产品规划席** 接受边界；接受后 **系统交付席** 按 ADR-0020 实现。
