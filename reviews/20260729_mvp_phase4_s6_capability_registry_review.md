# MVP Phase 4 / S6 — Capability Registry Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_mvp_phase4_s6_capability_registry.md`

## Conclusion

T013 / T014 的六类 Workspace Capability Registry 与五个历史 Skill 幂等迁移闭环通过，本 Issue 关闭。

## Implemented

- 复用既有 `official_models`、CapabilityCatalog 与稳定能力 ID；未新增表、依赖、Admin 或第二套 Registry。
- Workspace 用户可直接查看、注册和启停 Model / Agent / Skill / Tool / Workflow / Connector 六类能力。
- 列表、详情、类型计数、状态、来源、版本、描述与 I/O 契约均来自真实持久化数据。
- 五个 `skl_skill_*` 历史 Skill 从既有受控清单幂等登记，保持 `inactive / draft_candidate / NOASSERTION / commercial_use=false`。
- 历史 Skill 启用请求明确返回 422，许可复核前不发布、不实例化。
- Registry 只返回固定安全字段；描述与 I/O 等运行元数据在写入前复用统一敏感信息检查。

## Passed Evidence

- `backend/.venv/bin/python -m pytest -q backend/tests/test_mvp_phase4_s6_capability_registry.py backend/tests/test_d5_capability_catalog.py`：21 passed。
- `npm run lint`：PASS。
- `npm run build`：PASS，26 个静态页面生成成功。
- `git diff --check`：PASS。
- Desktop browser（隔离临时库）：
  - 在能力中心真实注册 `tool.release-check / 发布检查`，Tool 计数由 0 更新为 1；
  - 详情页展示真实 ID、类型、来源、版本、说明和 unknown 运行状态；
  - 普通能力停用、启用均持久化成功；
  - 历史 Skill 首次迁移 5 个，全部展示为停用；`skl_skill_code_review` 详情展示 NOASSERTION 许可边界；
  - 尝试启用历史 Skill 返回真实 422，页面保持“已停用”并显示许可复核错误。
- Mobile browser（390×844）：标题、事实卡、操作、类型横向筛选与 Skill 卡片单列可读，无可见横向溢出。

## Full Regression

在 `91a9be7b` 干净提交树应用本 Issue 暂存差异后执行：

```bash
backend/.venv/bin/python -m pytest -q backend/tests
```

结果：`1123 passed, 2 skipped, 0 failed`。

## Boundaries

- S7 Model Gateway 调用、Fallback 与成本统计未进入本 Sprint。
- 未扩展员工六类绑定，未启用 Marketplace、计费、配额或外部服务。
- 历史 Skill 原始候选资产未修改；Registry 只增加可追溯的停用登记。

Handoff: sent to main thread
