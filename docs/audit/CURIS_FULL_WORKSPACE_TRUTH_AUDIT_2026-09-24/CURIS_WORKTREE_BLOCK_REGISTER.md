# Worktree Block Register

Status: Review / protected. No worktree cleanup is permitted in Part 4.

| Path | State | Bytes | Block reason | Action |
|---|---|---:|---|---|
| `/private/tmp/curis-assistant-live-validation` | missing/prunable worktree path | 0 | MISSING; prunable metadata points to missing worktree path | REVIEW metadata only |
| `/private/tmp/curis-live-runtime-snapshot` | missing/prunable worktree path | 0 | MISSING; prunable metadata | REVIEW metadata only |
| `/private/tmp/curis-s10-clean.n8CNPY` | missing/prunable worktree path | 0 | MISSING; prunable metadata | REVIEW metadata only |
| `/private/tmp/curis-s11-clean` | missing/prunable worktree path | 0 | MISSING; prunable metadata | REVIEW metadata only |
| `/private/tmp/curis-s12-clean` | missing/prunable worktree path | 0 | MISSING; prunable metadata | REVIEW metadata only |
| `/Users/yy/.codex/worktrees/95a9/Curis AI Workspace` | worktree source + dependencies | 666288128 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/98d0/Curis AI Workspace` | worktree source + dependencies | 585306112 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/aeb0/Curis AI Workspace` | worktree source + dependencies | 3301838848 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/curis-shared-runtime-snapshot-20260813/Curis AI Workspace` | worktree source + dependencies | 47906816 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/d126/Curis AI Workspace` | worktree source + dependencies | 5254688768 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/rd-current-root-20260813/Curis AI Workspace` | worktree source + dependencies | 44810240 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/rd-migration-dd77` | worktree source + dependencies | 44802048 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/rd-shared-runtime-20260813/Curis AI Workspace` | worktree source + dependencies | 1201381376 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/ttk-current-root-20260813/Curis AI Workspace` | worktree source + dependencies | 44810240 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/ttk-shared-runtime-20260813/Curis AI Workspace` | worktree source + dependencies | 3286183936 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/xhs-current-root-20260813/Curis AI Workspace` | worktree source + dependencies | 44810240 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/xhs-dd77` | worktree source + dependencies | 530534400 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/.codex/worktrees/xhs-shared-runtime-20260813/Curis AI Workspace` | worktree source + dependencies | 585244672 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/ai-secretary-planning` | worktree source + dependencies | 1623159188 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/company-runtime-office-view` | worktree source + dependencies | 714955640 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/phase1c-ceo-office-first-slice` | worktree source + dependencies | 486371948 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/phase1c-company-project-bootstrap-ui` | worktree source + dependencies | 478702325 | Deletion loses user work/unique commits; main also dirty | KEEP; BLOCKED |

Registered non-root worktrees: 22; present worktrees blocked: 17; missing/prunable metadata: 5; removal candidates: 0.

The four in-repository branches and every external Codex worktree remain outside all Gate 2/3/4/5 file operations except exact generated child roots listed in Gate 3. Gate 3 must not remove a checkout or parent path.
