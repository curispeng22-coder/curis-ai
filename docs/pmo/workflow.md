# Curis Low-Token Workflow V2

Updated: 2026-07-12

## Goal

Keep multi-seat work auditable while making context recovery and handoffs small. Active entry files describe only the current state; history stays in archives.

## Recovery

Every task starts in this order:

1. `knowledge/NOW.md`
2. Current Issue
3. Current Review, when one exists
4. Only the detailed files named by the Issue

Do not begin with repository-wide reading, full history, or all Contracts.

## Issue Lifecycle

1. 产品规划席 defines objective, scope, non-goals, allowed files, acceptance, and verification.
2. 总控决策席 participates only for a gate change or scope conflict.
3. 系统交付席 implements the approved Issue and runs focused checks.
4. 系统交付席 sends a compact handoff to 质量运行席.
5. 质量运行席 performs the required independent regression once and writes the Review.
6. Security-sensitive work also routes through 安全边界席.
7. 产品规划席 reads the Review and accepts, revises, or escalates; it does not rerun tests.
8. Accepted evidence goes to the main thread for a short user report.

## 单主执行线程模式

对每个已批准的唯一产品目标，系统交付席在本地授权范围内连续完成诊断、最小修复、focused 验证与重跑；不为每个小故障新建 Gate，也不经产品席或质量席逐步审批。质量席只做里程碑独立验收与最终 E2E。安全席只在密钥、外部出网、跨租户 / 隐私、不可逆数据或新范围时介入。产品规划席只维护一个目标、停点汇报和最终验收。

## Verification Budget

| Stage | Required work |
| --- | --- |
| Delivery | Focused tests only; no duplicate full regression/build/E2E |
| Quality | One full regression and required E2E, recorded in Review |
| Security | Only changed sensitive boundaries; otherwise reuse Quality evidence |
| Product | Review evidence and product acceptance, no rerun |
| Main thread | Final evidence check and closeout only |

Repeated full regression without changed evidence is prohibited.

Verification must reuse repository commands, seeds, and launchers. Executable `/tmp` scripts are not used when an existing project command or browser tool covers the same check. A permission prompt is handled immediately by switching to an approved command or reporting a blocker; a seat must not remain silently paused.

## 本地运行诊断权限

- 系统交付席、质量运行席在当前 Issue 已授权范围内，可直接操作本地项目的 Docker、端口、容器日志和本地网络，以完成启动、停止、检查或诊断；不向用户重复申请确认。
- 仅密钥注入、真实外部调用、不可逆数据处置或新增范围需要升级裁决。
- 若客户端对已授权本地操作仍硬性拦截，席位只记录 `PLATFORM_BLOCKED` 和已完成证据；不得将同一确认请求再次抛给用户。

## 浏览器本地验收 Fail-fast

- 每个 Issue 开始时必须标明浏览器验收是否为硬门槛。
- 本地 URL 预检最多 60 秒；权限弹窗、`networkidle` 超时、无响应或被客户端拦截时，立即结束浏览器步骤，记录 `PLATFORM_BLOCKED` 并回传。
- 非硬门槛可继续使用 API/测试证据完成验收；硬门槛立即进入停点汇报。禁止等待用户、重复弹窗或让任务悬挂。

## Handoff

```text
Issue:
Objective:
Special Constraints:
Next Seat:
```

Target: under 200 tokens. Link to the Issue or Review instead of copying its contents.

The sender must attempt direct thread delivery. If unavailable, return `Handoff: HANDOFF_REQUIRED` with the four-field payload.

## 停点汇报

活动链路进入 idle、`PLATFORM_BLOCKED`、`WAIT_FOR_OWNER_INJECTION`、`BLOCKED_L2` 或完成时，产品规划席必须主动向总负责人提交停点汇报，不得静默停机。固定六项：当前状态与停点；本轮完成事项及 SHA / Review；已实现的真实能力；未完成与唯一根因；下一步（自动继续或需总控 / 用户决定）；用户是否需要动作及精确动作。单主执行线程中的普通小故障不单独停点；次日仍未收口时，重复提交同样六项。

## Active Files

- `knowledge/NOW.md`: recovery entry, target 30-60 lines.
- `knowledge/CURRENT_CONTEXT.md`: current context, target under 100 lines.
- `PROJECT_STATUS.md`: current phase only, target under 80 lines.
- `TASKS.md`: Active / Next / Blocked only, target under 70 lines.
- `AGENTS.md`: shared rules and routing only, target under 140 lines.

When a file exceeds its target because of completed history, move that history into a dated archive file and leave a link.

## Main Thread

The main thread does not poll seat tasks and does not repeat seat work. It acts only when:

- a handoff reports `HANDOFF_REQUIRED`;
- user approval is required;
- final accepted evidence is ready.

Final user reports use Chinese plain language and stay concise. Technical detail remains in Issues, Reviews, and release documents.

## Source-Of-Truth Updates

- After an Issue: update `knowledge/NOW.md` and `knowledge/CURRENT_CONTEXT.md`.
- After a Sprint: also update `PROJECT_STATUS.md` and `TASKS.md`.
- Preserve durable decisions in Contracts or ADRs.
- Archive completed chronology; do not delete evidence.

## Scope Guards

- No role may exceed the current Issue.
- UI ambiguity routes to 产品规划席.
- Architecture ambiguity routes to 系统交付席.
- Gate conflicts route to 总控决策席.
- Secrets, external services, privacy, or sensitive data route to 安全边界席.
