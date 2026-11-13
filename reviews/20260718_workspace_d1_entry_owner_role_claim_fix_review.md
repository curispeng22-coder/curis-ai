# Workspace D1 入口 owner / CEO Claim 修复质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_d1_entry_owner_role_claim_fix.md`
- 分支：`feat/roadmap-r1r2`
- 固定修订：`d57da0da16ea39c16d65b4da500de6e5674257e0`
- 验证席：质量运行席

## 结论

**PASS。**

D1 `_preflight()` 已在 `_claim_once()` 前复用可信 membership 的 `identity.role`，仅允许 active `owner` / `ceo`。`member`、空角色和 revoked membership 均在 claim、模型、Tool、写入前拒绝，原质量阻塞已解除。

## 独立证据

- 修订仅修改 `backend/app/d1_single_model_toolchain.py` 与对应 focused 测试；D1 目标脚本、pytest、模型、凭据和通用入口未改。
- 调用顺序仍为 `_preflight()` → `_claim_once()`，角色判断位于 preflight 内。
- 允许集合精确为 `{owner, ceo}`，没有客户端角色参数或新增平行身份源。
- focused：`.venv/bin/python -m unittest tests.test_d1_single_model_toolchain_entry` → **6 passed / 0 failed**。
- compileall：PASS；`git diff --check 213a4364..d57da0da`：PASS。
- 负向用例对 `member`、空角色、revoked 分别断言 model=0，Reader/Writer/Git/claim 调用合计=0；正向 owner/ceo 均可进入唯一 claim。
- 未启动、未注 Key、未调用模型、未运行 D1 pytest、未写 D1 文件、未出网。

## Gate 判断

- 质量阻塞：**已解除**。
- 父入口 Gate：可在安全席同步 PASS 后收口。
- 父 D1 E2E：继续 `WAIT_FOR_OWNER_INJECTION`；本 Review 不授权启动或真实调用。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
