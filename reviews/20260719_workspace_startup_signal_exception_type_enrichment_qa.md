# Review 20260719 — 启动失败信号携带脱敏异常类型名（里程碑验收）

- Review date: 2026-07-19
- Reviewer seat: 软件 QA 工程师（independent milestone acceptance，非重复实现方单测）
- Subject: `backend/app/main.py` + `backend/tests/test_workspace_startup_stage_signal.py` 的「启动失败信号额外携带 `exception_type`（异常类名，脱敏）」改动
- Related: `docs/pmo/20260719_quota_handoff_plan.md`（先增强启动信号策略，处理已确认 `create_app_failed`）
- 改动状态：unstaged（未提交），仅磁盘落地

## 结论（Verdict）

**最终验收 = PASS_WITH_NOTES。**

- 初评（修复前）：FAIL — 目标失败路径（`module_import` 的 `ImportError` 处理）触发阻塞级 `NameError`，分类信号不 emit。
- 回归（Alex 修复后，2026-07-19）：两处 `except ImportError:` 已改为 `except ImportError as error:`（`main.py:77`、`:156`），独立复现确认 `NameError` 消失、信号正常 emit 且 `exception_type` 为真实类名、异常原文不泄漏。**代码改动本身满足全部验收项（脱敏红线 / 分类固定性 / unknown 单字段 / 一致性 / 不再 NameError），8/8 独立检查 PASS，`py_compile` 与 `git diff --check` 均 clean。**
- NOTES（非阻塞）：现有单测 `test_workspace_startup_stage_signal.py` 仍用 `ast`+`exec` 仅加载函数体、不执行运行期 `except ImportError:` handler（本轮回查时该 in-file 冒烟测试**尚未落地**），故该「假绿」覆盖缺口在冒烟测试合入前仍存在。team-lead 已授权由 engineer 在**现有**测试文件内追加运行期 handler 冒烟测试（保持两文件约束，不另建文件）；该测试落地后本 QA 可顺带确认其脱敏正确性，但不影响本次代码验收结论。
- 综上：改动**可合入**；测试加固为独立、非阻塞的后续动作。

---

## 原因（Root Cause / 证据）

### 阻塞缺陷：两处 `except ImportError:` 引用了未绑定的 `error`（FAIL 根因）

改动把模块导入失败的处理从
```python
_emit_startup_failure(_startup_failure_signal("module_import", "import_exception"))
```
改为
```python
_emit_startup_failure(_classified_signal("module_import", "import_exception", error))
```
新代码引用了 `error`，但对应 `except` 子句**没有**把异常绑定到 `error`：

- `backend/app/main.py:77` — `except ImportError:`（裸子句，无 `as error`）
- `backend/app/main.py:156` — `except ImportError:`（裸子句，无 `as error`）
- `backend/app/main.py:79` — `_classified_signal("module_import", "import_exception", error)` ← 引用未绑定名
- `backend/app/main.py:158` — `_classified_signal("module_import", "import_exception", error)` ← 引用未绑定名

全文件 `as error` 绑定点 grep 结果：模块级唯一绑定在 `main.py:3408`（`except Exception as error:`，位于 `create_app()` 外层，**远在 77/156 行之后**）；其余 `as error` 全部位于函数体内（≥ `main.py:846`）。模块级代码自上而下执行，第 77/156 行 handler 执行时 `error` 全局名尚不存在。

**运行时后果**（workspace 模式、模块导入失败）：handler 体执行到 `_classified_signal(..., error)` 即抛出 `NameError`，进程以未处理异常退出（伴随 Python traceback），**预期的 `{"failure_code":"import_failed","exception_type":"ImportError"}` 信号从未写入 stderr**。这恰好打在改动想增强的路径上，直接归零本次改动价值。

**独立实证**（不触发 `create_app()`，用相同 handler 结构最小复现）：
```
[PASS] module_import handler raises NameError (error unbound) -- name 'error' is not defined
[PASS] both except ImportError handlers do NOT bind 'error' but reference it -- handlers found: [(77, False, True), (156, False, True)]
```
（完整脚本见 `/tmp/qa_verify_signal.py`，未改动任何交付文件。）

> 为何交付席的 `pytest … 6 passed` 给了假绿：该测试用 `ast`+`exec` 仅加载函数体做单元断言，**从不真正执行 `except ImportError:` 运行期 handler**，因此 `NameError` 未被覆盖。这正是独立里程碑验收存在的意义。

---

### 已通过（独立复核，非重复单测）

以下各项本 QA 用独立 `ast`+`exec` 加载 + 实证复现交叉确认，**全部 PASS**：

1. **分类固定性（需求 2）** — `failure_code` 仅由 `_STARTUP_FAILURE_CODES` 固定 `(stage, signal)` 映射决定（`main.py:13-20, 24`）。`_classified_signal`（`main.py:30-34`）只调用 `_startup_failure_signal(stage, signal)` 并追加 `exception_type` 字段，**不改分类逻辑、不动态生成/拼接任何新 code**。
   - 证据：`main.py:32-33` → `result = _startup_failure_signal(stage, signal); result["exception_type"] = type(error).__name__`。

2. **脱敏红线（需求 3）**
   - `exception_type` 严格为 `type(error).__name__`（类名字符串），**绝不可能是 `str(error)`（消息）**。实证：`classified("create_app","factory_exception", ValueError("should not escape"))` → `exception_type == "ValueError"`，且 `"should not escape"` 不在结果中。
   - 信号构建函数体内**无 `str(error)` / `repr(error)` / `traceback` / `format_exc`**。grep 全文件 `traceback|format_exc|repr(error)` 零命中；所有 `str(error)` 均位于路由层 `raise HTTPException(..., detail=str(error))`（≥ `main.py:1488`），**不在启动失败 emit 链路**。
   - `_emit_startup_failure`（`main.py:54-55`）仅 `print(json.dumps(signal, ...), file=sys.stderr)`，信号字典只含固定字段 + 类名，不拼消息/堆栈/参数/路径/Key。
   - 异常消息（"should not escape"、"hidden"、"sensitive text must not escape"）均不泄漏进信号任一字段（实证断言通过）。

3. **unknown 单字段（需求 4）**
   - `_startup_failure_signal("unknown","unknown")` → `{"failure_code": "unknown"}`（实证 PASS）。
   - 未标记 / 畸形 marker 路径（`_signal_for_startup_error` 的 `not isinstance(marked, tuple) or len(marked) != 2` 分支，`main.py:49-50`）返回 `_startup_failure_signal()` → 严格单字段，**`exception_type` 不会被加入 unknown**（实证 PASS）。
   - 默认 marker `("create_app","factory_exception")` 为已知映射，正确产出 `create_app_failed` + `exception_type`（验证为预期行为，非泄漏）。

4. **一致性（需求 5）** — 两处 `module_import` 的 `ImportError` handler（`:79`、`:158`）均已改为携带 `exception_type`，无遗漏；`create_app` 顶层 handler（`:3410`）经 `_signal_for_startup_error(error)` 走分类路径（`error` 在此处由 `:3408` 正确绑定）。`except Exception:` 兜底（`:82-85`、`:161-164`）保持 `_startup_failure_signal()` 无 `exception_type`，符合原设计。

---

## 建议（Recommendation / 修复）

### 必须修（blocker，合入前）
把两处裸 `except ImportError:` 改为绑定异常名，**仅此一处关键字之差**，脱敏性不受影响（`error` 只流入 `type(error).__name__`，永不 `str/repr/traceback`）：

```diff
-    except ImportError:
+    except ImportError as error:
         if _workspace_startup():
             _emit_startup_failure(_classified_signal("module_import", "import_exception", error))
             raise SystemExit(1) from None
         raise
```
- `backend/app/main.py:77` → `except ImportError as error:`
- `backend/app/main.py:156` → `except ImportError as error:`

修复后建议在同一 import 块内、workspace 模式下用「故意缺失的 import」做运行期冒烟（或直接单测这两段 handler 的绑定），确认 stderr 能收到 `{"exception_type":"ImportError",...}` 而非 `NameError` traceback。

### 建议补（测试覆盖缺口，非 blocker）
新增针对**运行期 handler 绑定**的测试，而非仅用 `ast`+`exec` 加载函数体。最小做法：构造一个会抛 `ImportError` 的导入场景（例如临时 `sys.modules` 摘除某个可选依赖），断言 workspace 模式下 stderr 收到含 `exception_type` 的 JSON 且进程 `SystemExit(1)`，从而把本次 `NameError` 这类「绑定缺失」缺陷挡在 CI 内。

### 已知未改（确认无害，仅记录）
`_classified_signal` 本身若被传入未知 `(stage, signal)` 也会追加 `exception_type`，但当前 shipping 代码路径**永不**以 unknown pair 调用它（unknown 只来自 `_startup_failure_signal()`），故红线不被突破。若需纵深防御，可在 `_classified_signal` 内对 `failure_code == "unknown"` 时跳过追加 `exception_type`，但非必需。

---

## Verification（本验收依据）

- 读取真实磁盘文件 `backend/app/main.py`、`backend/tests/test_workspace_startup_stage_signal.py`，确认 diff 与磁盘一致。
- grep 全文件 `as error` / `traceback` / `format_exc` / `repr(error)` / `str(error)`，逐条定位与定性（运行期路径 vs 路由层）。
- 独立脚本 `/tmp/qa_verify_signal.py`（`ast`+`exec` 加载信号函数，不触发 `create_app()`）：8 项断言全部 PASS，并在最小复现中确认 `NameError`。
- 交付席 focused verification（py_compile / pytest 6 passed / git diff --check）已获知，但**不依赖其结论**作为本验收依据。

## Regression（回归确认 · 2026-07-19 · Alex 修复后）

- 修复点已落盘：`main.py:77` → `except ImportError as error:`；`main.py:156` → `except ImportError as error:`（已 Read 核对）。
- 独立 AST 扫描：两处 `except ImportError` handler 现在均 `bind 'error'` 且引用它 → `[(77, True, True), (156, True, True)]`。
- 独立最小复现（同结构，真实 `import` 失败触发）：**不再抛 `NameError`**，信号正常 emit，内容 `{"failed_stage":"module_import","failure_signal":"import_exception","failure_code":"import_failed","exception_type":"ModuleNotFoundError"}`，异常原文（"does_not_exist" 等）未泄漏。
  - 说明：Python 3 真实 `import` 失败抛 `ModuleNotFoundError`（`ImportError` 子类），`type(error).__name__` 即 `"ModuleNotFoundError"`——这是**更精确的真实类名**，正是本次改动想暴露的真因，且不含模块名/路径，脱敏安全。
- 脱敏/分类/unknown 单字段/一致性全部复测 PASS（8/8）。
- `py_compile backend/app/main.py backend/tests/test_workspace_startup_stage_signal.py` → OK；`git diff --check` → clean。
- **结论：blocker 已消除，改动可接受合入。**

## Known gaps
- ~~阻塞缺陷：`main.py:77`、`:156` 的 `error` 未绑定 → `NameError`~~ — **已修复（回归 PASS）**。
- 测试覆盖缺口（非 blocker，已授权、待 engineer 落地）：现有单测用 `ast`+`exec` 只加载函数体、不执行运行期 `except ImportError:` handler，假绿风险仍在。team-lead 已授权由 engineer 在**现有** `test_workspace_startup_stage_signal.py` 内追加运行期 handler 冒烟测试（保持两文件约束、不另建文件）；截至本最终结论时该冒烟测试**尚未落地**。落地后建议本 QA 顺带确认其脱敏正确性。

## Scope risks
- 修复为纯一行关键字变更，风险极低，不影响任何脱敏/分类红线。
- 若未来有人把 `except ImportError:` 改回裸子句，会再次引入 `NameError`；新增运行期 smoke test 可挡住此类回归。

## Next Curis seat
- 改动已通过回归验收（PASS_WITH_NOTES），可合入。
- 后续动作（已授权、非阻塞）→ 软件工程师（Alex）：在现有 `test_workspace_startup_stage_signal.py` 内追加运行期 `except ImportError` handler 冒烟测试（保持两文件约束）。

## Handoff status
RESOLVED → 改动 ACCEPTED（PASS_WITH_NOTES）
- 非阻塞后续：engineer 在现有测试文件追加 in-file 运行期 handler 冒烟测试（team-lead 已授权）。
- 原始 blocker Payload（已执行）：「`main.py:77`、`:156` `except ImportError:` → `except ImportError as error:`；`error` 仅用于 `type(error).__name__`，脱敏红线不受影响。」
