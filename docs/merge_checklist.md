# 合入清单（R1/R2 hardening）

本清单对应 `backend/scripts/pre_merge_check.py` 的自动化校验，亦可作为人工合入前核对项。

## 自动化校验（非零退出即阻断）

```bash
python backend/scripts/pre_merge_check.py
```

| # | 检查项 | 通过条件 |
| --- | --- | --- |
| 1 | 工作区干净 | `git status --porcelain` 为空 |
| 2 | 测试全绿 | `test_real_rd_executor.py` / `test_local_rd_toolset_sandbox.py` / `test_local_rd_toolset.py` 三个文件 pytest 全绿 |
| 3 | 与 main 无冲突 | `git fetch` + `git merge --no-commit --no-ff main` 干净，随后自动 `--abort` 撤销 |
| 4 | 提交归属线 | `git log 83f017bf..HEAD` 每 issue 独立提交（打印供人工复核） |
| 5 | 受保护文件未动 | `git diff --name-only 83f017bf..HEAD` 不含 `model_gateway` / `evolution_event_log` / `d1_gateway_client`（仅 `local_rd_toolset.py` 等允许变更） |

## 人工核对项

- [ ] 每个 issue 独立提交，提交信息含归属线 `(backend)`。
- [ ] 受保护文件（`model_gateway.py` / `evolution_event_log.py` / `d1_gateway_client.py`）未被改动。
- [ ] `local_rd_toolset.py` 仅改动 sandbox 相关逻辑；`read_file` / `apply_diff` 既有行为不变。
- [ ] 审计 / 脱敏 / 路径白名单在两分支（走 / 不走 sandbox）一致经过 `_execute` / `_audit` / `_safe_process_output`。
- [ ] 文档齐备：`backend/docs/real_rd_local_run.md`、`docs/r1r2_release_notes.md`。

## 合入步骤（由主理人执行，工程师不自行 merge 到 main）

1. 在 `feat/roadmap-r1r2` 本地提交完成（T01–T04 各自独立提交）。
2. 运行 `pre_merge_check.py` 全绿。
3. `git checkout main && git merge --no-ff feat/roadmap-r1r2`（或 PR 合入）。
4. 合入后于目标分支复跑 `pre_merge_check.py` 与 `pytest backend/tests/`。
